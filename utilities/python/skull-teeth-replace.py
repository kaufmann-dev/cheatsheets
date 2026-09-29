#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10,<3.13"
# dependencies = [
#   "meshlib==3.1.3.297",
#   "trimesh>=4",
#   "numpy>=2",
#   "scipy>=1.13",
#   "SimpleITK>=2.3",
#   "networkx>=3",
# ]
# ///
"""Replace the CT-derived teeth of a skull STL with intraoral scans.

Pipeline (see ../../guides/skull-teeth-scan-replacement.md):

  register  multi-start ICP of each open scan onto the CT teeth of the skull;
            ICP of each closed "printable" model onto its open scan
  labels    tooth/gum segmentation of each scan: distance prior, then a
            curvature-guided graph cut along the gingival crease
  field     one signed-distance field for the whole teeth region:
            blend CT skull <-> scan crowns (per-jaw ownership, crown union)
  assemble  marching cubes of that field, stitched into the untouched skull
            outside the region (no booleans), repair + decimate
  validate  topology checks + deviation from the input skull outside the teeth
  render    optional Blender QA renders (front + in-mouth views)

Inputs (all in the CT world frame except the scans):
  --skull-stl      closed skull mesh extracted from the CT (world/LPS mm)
  --skull-mask     binary labelmap the skull STL came from (NIfTI/NRRD)
  --teeth-upper / --teeth-lower   CT teeth segmentations (e.g. TotalSegmentator)
  --scan-upper / --scan-lower     edited open intraoral scans (teeth + thin gum)
  --printable-upper / --printable-lower   closed solids made from those scans

Example:
  skull-teeth-replace.py all \\
    --skull-stl skull_edited.stl --skull-mask skull_edited.nii.gz \\
    --teeth-upper ct/teeth_upper.nii.gz --teeth-lower ct/teeth_lower.nii.gz \\
    --scan-upper upper_jaw.stl --scan-lower lower_jaw.stl \\
    --printable-upper "upper jaw printable.stl" \\
    --printable-lower "lower jaw printable.stl" \\
    --work work/ --out skull_v1.stl

Stages cache their outputs in --work; rerun a single stage with its name.
Needs ~16 GB RAM for a ~220 M-voxel field grid (0.1 mm).
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import SimpleITK as sitk
import trimesh
from scipy import ndimage as ndi
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.csgraph import breadth_first_order, connected_components, maximum_flow
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation

JAWS = ("upper", "lower")

# ---------------------------------------------------------------- parameters
# Values that produced the accepted result. Units: mm.
P = dict(
    H=0.1,            # field voxel size
    R=3.0,            # scan influence band
    MARGIN=4.0,       # grid margin beyond R around the scans
    W=1.0,            # gumline blend width (tooth side)
    GUMFADE=3.0,      # neck-shrink fade distance into the gum side
    OUT_FULL=0.8,     # scan may remove CT material up to this far outside its crown...
    OUT_ZERO=1.4,     # ...fading to zero here (protects unscanned teeth, e.g. wisdom teeth)
    IN_FULL=1.8,      # scan authority inside a crown, fading...
    IN_ZERO=2.8,      # ...to CT here
    OWNER_BLEND=0.6,  # width of the upper/lower ownership blend
    NEAR_SCAN=0.5,    # use exact open-scan distance within this band of the crown
    SIGN_TOL=0.15,    # printable vs scan sign disagreement tolerance
    FAT_MAX=1.5,      # max CT over-thickness removed at the neck
    TAU=0.4,          # initial label: scan within TAU of skull = tooth candidate
    BONE_NEAR=3.0, TEETH_NEAR=1.0,
    GC_TOOTH_CORE=2.0, GC_GUM_CORE=-1.5, GC_SIGMA=0.03,
    STITCH_OUTER=2.0,  # skull faces removed inside grid box shrunk by this
    STITCH_INNER=2.4,  # local faces kept inside grid box shrunk by this
    DECIMATE_ERR=0.005,
)


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def smooth(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------- image helpers
class Img:
    """SimpleITK image + world<->index helpers (world = physical LPS mm)."""

    def __init__(self, path_or_img):
        self.im = sitk.ReadImage(str(path_or_img)) if not isinstance(path_or_img, sitk.Image) else path_or_img
        self.O = np.array(self.im.GetOrigin())
        self.S = np.array(self.im.GetSpacing())
        self.D = np.array(self.im.GetDirection()).reshape(3, 3)
        self.Di = np.linalg.inv(self.D)

    def arr(self):
        return sitk.GetArrayFromImage(self.im)  # z, y, x

    def to_index(self, p):  # continuous (x, y, z) index
        return ((p - self.O) @ self.Di.T) / self.S

    def sample(self, a, p, order=1, cval=0.0):
        g = self.to_index(p)
        return ndi.map_coordinates(a, [g[:, 2], g[:, 1], g[:, 0]], order=order, mode="constant", cval=cval)


def largest_component(m):
    parts = m.split(only_watertight=False)
    return max(parts, key=lambda b: len(b.faces))


def boundary_vertices(m):
    e = m.edges_sorted
    u, c = np.unique(e, axis=0, return_counts=True)
    return np.unique(u[c == 1])


def vertex_adjacency(m):
    e = m.edges_unique
    n = len(m.vertices)
    A = coo_matrix((np.ones(2 * len(e)), (np.r_[e[:, 0], e[:, 1]], np.r_[e[:, 1], e[:, 0]])), shape=(n, n)).tocsr()
    return A


# ================================================================ stage: register
def icp(src, tgt, tn, T, iters=60, thr0=3.0, thr1=0.8):
    tree = cKDTree(tgt)
    for k in range(iters):
        thr = thr0 + (thr1 - thr0) * min(1, k / (iters * 0.6))
        p = src @ T[:3, :3].T + T[:3, 3]
        d, i = tree.query(p, workers=-1)
        w = d < thr
        if w.sum() < 50:
            break
        q, n, ps = tgt[i[w]], tn[i[w]], p[w]
        A = np.hstack([np.cross(ps, n), n])
        b = ((q - ps) * n).sum(1)
        x = np.linalg.lstsq(A, b, rcond=None)[0]
        dT = np.eye(4)
        dT[:3, :3] = Rotation.from_rotvec(x[:3]).as_matrix()
        dT[:3, 3] = x[3:]
        T = dT @ T
    p = src @ T[:3, :3].T + T[:3, 3]
    d, _ = tree.query(p, workers=-1)
    return T, d


def stage_register(a, work):
    skull = trimesh.load(a.skull_stl)
    rng = np.random.default_rng(0)
    result = {}
    for jaw in JAWS:
        tm = Img(getattr(a, f"teeth_{jaw}"))
        # ~0.9 mm dilation, one slice in z. Larger targets pull in alveolar bone
        # and bias ICP (1.5 deg / 0.6 mm off in testing) despite higher scores.
        rad = [max(1, int(round(0.9 / s))) for s in tm.S]
        dil = Img(sitk.BinaryDilate(tm.im, rad))
        sel = dil.sample(dil.arr().astype(np.float32), skull.triangles_center, order=0) > 0.5
        sub = skull.submesh([np.where(sel)[0]], append=True)
        tgt, fi = trimesh.sample.sample_surface(sub, 25000, seed=1)
        tn = sub.face_normals[fi]

        scan = largest_component(trimesh.load(getattr(a, f"scan_{jaw}")))
        src = scan.vertices[rng.choice(len(scan.vertices), min(10000, len(scan.vertices)), replace=False)]

        def frame(Pp):
            c = Pp.mean(0)
            _, _, vt = np.linalg.svd(Pp - c, full_matrices=False)
            return c, vt

        cc, cv = frame(tgt)
        sc, sv = frame(src)
        best = None
        for sx in (1, -1):
            for sy in (1, -1):
                for ang in np.radians([-30, 0, 30]):
                    A = np.diag([sx, sy, 1.0])
                    A[2, 2] = np.linalg.det(cv) * np.linalg.det(sv) * sx * sy  # proper rotations only
                    R = Rotation.from_rotvec(cv[2] * ang).as_matrix() @ (cv.T @ A @ sv)
                    T = np.eye(4)
                    T[:3, :3] = R
                    T[:3, 3] = cc - R @ sc
                    T, d = icp(src, tgt, tn, T)
                    frac = (d < 0.8).mean()
                    dt, _ = cKDTree(src @ T[:3, :3].T + T[:3, 3]).query(tgt, workers=-1)
                    cov = (dt < 0.8).mean()
                    rms = np.sqrt((d[d < 0.8] ** 2).mean()) if (d < 0.8).any() else 9
                    log(f"  {jaw} start sx={sx:+d} sy={sy:+d} rot={np.degrees(ang):+.0f}: inliers {frac:.3f} coverage {cov:.3f} rms {rms:.3f}")
                    if best is None or frac + cov > best[0]:
                        best = (frac + cov, T, frac, cov)
        T = best[1]
        assert np.linalg.det(T[:3, :3]) > 0
        scan_ct = scan.copy()
        scan_ct.apply_transform(T)
        scan_ct.export(work / f"scan_{jaw}.ply")  # PLY keeps vertex order
        np.save(work / f"T_scan_{jaw}.npy", T)
        log(f"{jaw}: best inliers {best[2]:.3f} coverage {best[3]:.3f}")

        # printable (closed) -> open scan (both in their original scan frame)
        pr = trimesh.load(getattr(a, f"printable_{jaw}"))
        e_tree = cKDTree(scan.vertices)
        tnn = scan.vertex_normals
        psrc = pr.vertices[:: max(1, len(pr.vertices) // 30000)]
        best_p = None
        for flip in (np.eye(3), np.diag([1, -1, -1]), np.diag([-1, 1, -1]), np.diag([-1, -1, 1])):
            Tp = np.eye(4)
            Tp[:3, :3] = flip
            Tp[:3, 3] = np.median(scan.vertices, 0) - flip @ np.median(psrc, 0)
            Tp, _ = icp(psrc, scan.vertices, tnn, Tp, iters=50, thr0=5.0, thr1=0.3)
            # score: how well the scan is covered by the printable surface
            ps_, _ = trimesh.sample.sample_surface(pr, 400000, seed=2)
            q = ps_ @ Tp[:3, :3].T + Tp[:3, 3]
            dd, _ = cKDTree(q).query(scan.vertices, workers=-1)
            med = np.median(dd)
            if best_p is None or med < best_p[0]:
                best_p = (med, Tp)
        Tp = best_p[1]
        pr_ct = pr.copy()
        pr_ct.apply_transform(T @ Tp)
        pr_ct.export(work / f"printable_{jaw}.ply")
        log(f"{jaw}: printable->scan median distance {best_p[0]:.3f} mm (should be < ~0.1)")
        result[jaw] = dict(inliers=best[2], coverage=best[3], printable_median=best_p[0])
    (work / "register.json").write_text(json.dumps(result, indent=2))


# ================================================================ stage: labels
def stage_labels(a, work):
    sk = Img(a.skull_mask)
    skm = sk.arr() > 0
    teeth = np.zeros_like(skm)
    for jaw in JAWS:
        t = sitk.Resample(sitk.ReadImage(getattr(a, f"teeth_{jaw}")), sk.im, sitk.Transform(), sitk.sitkNearestNeighbor, 0)
        teeth |= sitk.GetArrayFromImage(t) > 0
    sp = tuple(sk.S[::-1])
    it = max(1, int(round(0.8 / sk.S.min())))
    bone = skm & ~ndi.binary_dilation(teeth, iterations=it)
    log("labels: distance transforms")
    sdf = (ndi.distance_transform_edt(~skm, sampling=sp) - ndi.distance_transform_edt(skm, sampling=sp)).astype(np.float32)
    edt_bone = ndi.distance_transform_edt(~bone, sampling=sp).astype(np.float32)
    edt_teeth = ndi.distance_transform_edt(~teeth, sampling=sp).astype(np.float32)

    for jaw in JAWS:
        s = trimesh.load(work / f"scan_{jaw}.ply", process=False)
        v, n = s.vertices, s.vertex_normals
        A = vertex_adjacency(s)
        deg = np.asarray(A.sum(1)).ravel()
        bv = boundary_vertices(s)

        # 1) distance prior: tooth where the scan hugs the CT teeth
        d = sk.sample(sdf, v, cval=5)
        db = sk.sample(edt_bone, v, cval=9)
        dt = sk.sample(edt_teeth, v, cval=9)
        tooth = ((d < P["TAU"]) & (dt < P["TEETH_NEAR"])) | ((db > P["BONE_NEAR"]) & (dt < 2.0))
        lab = tooth.astype(float)
        for _ in range(10):
            lab = (A @ lab + lab) / (deg + 1)
        tooth = lab > 0.5
        tooth = _drop_islands(A, tooth, 3000, 400)
        U0 = _signed_label_distance(v, tooth, bv)

        # 2) concavity (gumline is a concave crease)
        ps = v.copy()
        for _ in range(8):
            ps = (A @ ps + ps) / (deg + 1)[:, None]
        H = np.einsum("ij,ij->i", v - ps, n)

        # 3) graph cut inside the uncertain band around the prior boundary
        e = s.edges_unique
        L = s.edges_unique_length
        conc = np.maximum(0, -np.minimum(H[e[:, 0]], H[e[:, 1]]))
        w = np.maximum(1, np.round(1000 * L * np.exp(-((conc / P["GC_SIGMA"]) ** 2)))).astype(np.int64)
        nv = len(v)
        src_, snk = nv, nv + 1
        INF = 10**8
        t_core = np.where(U0 > P["GC_TOOTH_CORE"])[0]
        g_core = np.union1d(np.where(U0 < P["GC_GUM_CORE"])[0], bv)
        rows = np.concatenate([e[:, 0], e[:, 1], np.full(len(t_core), src_), g_core])
        cols = np.concatenate([e[:, 1], e[:, 0], t_core, np.full(len(g_core), snk)])
        cap = np.concatenate([w, w, np.full(len(t_core), INF), np.full(len(g_core), INF)])
        G = csr_matrix((cap.astype(np.int64), (rows, cols)), shape=(nv + 2, nv + 2))
        G.sum_duplicates()
        G.data = np.minimum(G.data, INF).astype(np.int32)
        r = maximum_flow(G, src_, snk)
        Rm = (G - r.flow).tocsr()
        Rm.data = (Rm.data > 0).astype(np.int8)
        Rm.eliminate_zeros()
        reach = breadth_first_order(Rm, src_, directed=True, return_predecessors=False)
        tooth = np.zeros(nv + 2, bool)
        tooth[reach] = True
        tooth = _drop_islands(A, tooth[:nv], 3000, 400)
        U = _signed_label_distance(v, tooth, bv)
        Ub = cKDTree(v[bv]).query(v)[0]
        np.save(work / f"U_{jaw}.npy", U)
        np.save(work / f"Ub_{jaw}.npy", Ub)
        col = np.where(tooth[:, None], [60, 110, 230, 255], [220, 40, 40, 255]).astype(np.uint8)
        s2 = s.copy()
        s2.visual.vertex_colors = col
        s2.export(work / f"labels_{jaw}.ply")
        log(f"labels {jaw}: tooth fraction {tooth.mean():.3f} (prior {(U0 > 0).mean():.3f}); check labels_{jaw}.ply")


def _drop_islands(A, flag, min_true, min_false):
    flag = flag.copy()
    for val, mn in ((True, min_true), (False, min_false)):
        idx = np.where(flag == val)[0]
        if len(idx) == 0:
            continue
        _, cc = connected_components(A[idx][:, idx], directed=False)
        small = np.bincount(cc)[cc] < mn
        flag[idx[small]] = not val
    return flag


def _signed_label_distance(v, tooth, bv):
    excl = ~tooth
    excl[bv] = True
    U = np.zeros(len(v))
    if (~excl).any() and excl.any():
        U[~excl] = cKDTree(v[excl]).query(v[~excl])[0]
        U[excl] = -cKDTree(v[~excl]).query(v[excl])[0]
    return U


# ================================================================ stage: field
def stage_field(a, work):
    import meshlib.mrmeshpy as mr
    import meshlib.mrmeshnumpy as mn

    H, R = P["H"], P["R"]
    scans = {j: trimesh.load(work / f"scan_{j}.ply", process=False) for j in JAWS}
    allv = np.vstack([scans[j].vertices for j in JAWS])
    lo = allv.min(0) - R - P["MARGIN"]
    hi = allv.max(0) + R + P["MARGIN"]
    shp = (np.ceil((hi - lo) / H).astype(int) + 1)
    np.save(work / "grid_lo.npy", lo)
    np.save(work / "grid_shp.npy", shp)
    log(f"field grid {shp.tolist()} = {np.prod(shp) / 1e6:.0f} M voxels")

    def mrmesh(tm):
        return mn.meshFromFacesVerts(tm.faces.astype(np.int32), tm.vertices.astype(np.float32))

    def vol(mesh, maxd, mode):
        p = mr.MeshToDistanceVolumeParams()
        p.vol.origin = mr.Vector3f(*(lo - 0.5 * H))  # meshlib samples voxel centres
        p.vol.voxelSize = mr.Vector3f(H, H, H)
        p.vol.dimensions = mr.Vector3i(*[int(x) for x in shp])
        p.dist.signMode = mode
        p.dist.maxDistSq = maxd * maxd
        return mn.getNumpy3Darray(mr.meshToDistanceVolume(mr.MeshPart(mesh), p)).astype(np.float32)  # [x, y, z]

    def tri(Aa, pts):  # trilinear sample of a grid array at world points
        g = (pts - lo) / H
        i = np.clip(np.floor(g).astype(int), 0, shp - 2)
        f = g - i
        out = 0
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    ww = (f[:, 0] if dx else 1 - f[:, 0]) * (f[:, 1] if dy else 1 - f[:, 1]) * (f[:, 2] if dz else 1 - f[:, 2])
                    out = out + ww * Aa[i[:, 0] + dx, i[:, 1] + dy, i[:, 2] + dz]
        return out

    # exact signed distance to the skull (winding number sign; closed mesh)
    skull = trimesh.load(a.skull_stl)
    SSK = vol(mrmesh(skull), 5.0, mr.SignDetectionMode.WindingRule)
    nan = ~np.isfinite(SSK)
    sk = Img(a.skull_mask)
    ska = (sk.arr() > 0).astype(np.float32)
    idx = np.argwhere(nan)
    inside = sk.sample(ska, idx * H + lo, order=0) > 0.5
    SSK[tuple(idx.T)] = np.where(inside, -5.0, 5.0)
    del idx, inside, nan, ska
    log("field: skull distance done")

    GJ, D0 = {}, {}
    TMIN = np.full(shp, np.inf, np.float32)
    for jaw in JAWS:
        s = scans[jaw]
        V = s.vertices
        U = np.load(work / f"U_{jaw}.npy")
        Ub = np.load(work / f"Ub_{jaw}.npy")
        pr = trimesh.load(work / f"printable_{jaw}.ply")
        Pv = vol(mrmesh(pr), R + 0.5, mr.SignDetectionMode.WindingRule)
        # near the crown use the exact open-scan distance (sign by projection
        # normal); fall back to the printable where they disagree
        Dv = vol(mrmesh(s), 0.6, mr.SignDetectionMode.ProjectionNormal)
        near = np.isfinite(Dv) & (np.abs(Dv) < P["NEAR_SCAN"]) & np.isfinite(Pv)
        agree = near & ((np.sign(Dv) == np.sign(Pv)) | (np.abs(Pv) < P["SIGN_TOL"]))
        Pv[agree] = Dv[agree]
        del Dv, near, agree
        fin = np.isfinite(Pv)
        GJ[jaw] = SSK.copy()
        D0[jaw] = np.full(shp, R + 5, np.float32)

        # CT over-thickness at the neck (measured on crown vertices next to the gumline)
        dv = tri(SSK, V)
        bnd = (U > 0) & (U < 0.8)
        fat = np.clip(-dv, 0, P["FAT_MAX"])
        tb = cKDTree(V[bnd])
        fb = fat[bnd]
        dd, ii = tb.query(V, k=64, distance_upper_bound=1.5)
        ok = np.isfinite(dd)
        F = np.where(ok.any(1), np.where(ok, fb[np.where(ok, ii, 0)], 0).sum(1) / np.maximum(ok.sum(1), 1), 0).astype(np.float32)
        if (~ok.any(1)).any():
            _, ni = tb.query(V[~ok.any(1)])
            F[~ok.any(1)] = fb[ni]

        rim = boundary_vertices(s)
        trim = cKDTree(V[rim])
        tree = cKDTree(V)
        X = np.argwhere(fin)
        CH = 6_000_000
        for k in range(0, len(X), CH):
            Xi = X[k:k + CH]
            x = Xi * H + lo
            idt = tuple(Xi.T)
            dk, ik = tree.query(x, k=12, workers=-1)
            g = np.exp(-((dk - dk[:, :1]) ** 2) / (2 * 0.15**2))
            gs = g.sum(1)
            Uk = (g * U[ik]).sum(1) / gs
            Fk = (g * F[ik]).sum(1) / gs
            Ubk = (g * Ub[ik]).sum(1) / gs
            drim = trim.query(x, workers=-1, distance_upper_bound=R + 3)[0]
            drim = np.where(np.isfinite(drim), drim, R + 3)
            pj = Pv[idt]
            inward = 1 - smooth((-pj - P["IN_FULL"]) / (P["IN_ZERO"] - P["IN_FULL"]))
            outward = 1 - smooth((pj - P["OUT_FULL"]) / (P["OUT_ZERO"] - P["OUT_FULL"]))
            depth = np.where(pj < 0, inward, outward) * (1 - smooth((dk[:, 0] - (R - 0.2)) / 0.6))
            rimf = smooth((Ubk - 0.8) / 1.2) * smooth((drim - dk[:, 0] - 0.2) / 0.8)
            w = smooth(Uk / P["W"]) * depth * rimf
            c = Fk * (1 - smooth(-Uk / P["GUMFADE"])) * depth
            GJ[jaw][idt] = (1 - w) * (SSK[idt] + c) + w * pj
            D0[jaw][idt] = dk[:, 0]
            TMIN[idt] = np.minimum(TMIN[idt], pj + (1 - w) * (R + 1))
        del Pv, X, fin
        log(f"field: {jaw} done")

    al = smooth((D0["lower"] - D0["upper"]) / P["OWNER_BLEND"] + 0.5)  # 1 = owned by upper
    G = np.minimum(al * GJ["upper"] + (1 - al) * GJ["lower"], TMIN)
    del GJ, D0, al, SSK, TMIN
    v = mn.simpleVolumeFrom3Darray(G)
    v.voxelSize = mr.Vector3f(H, H, H)
    mp = mr.MarchingCubesParams()
    mp.origin = mr.Vector3f(*lo)
    mp.iso = 0.0
    mp.lessInside = True
    mesh = mr.marchingCubes(v, mp)
    mr.saveMesh(mesh, str(work / "local.ply"))
    log(f"field: local mesh {mesh.topology.numValidFaces()} faces")


# ================================================================ stage: assemble
def stage_assemble(a, work):
    import meshlib.mrmeshpy as mr

    lo = np.load(work / "grid_lo.npy")
    shp = np.load(work / "grid_shp.npy")
    hi = lo + (shp - 1) * P["H"]

    # local part: faces fully inside the inner box, big components, no voids
    lm = trimesh.load(work / "local.ply", process=False)
    Vl, Fl = lm.vertices, lm.faces
    L0, L1 = lo + P["STITCH_INNER"], hi - P["STITCH_INNER"]
    inL = np.all((Vl > L0) & (Vl < L1), 1)
    F = Fl[inL[Fl].all(1)]
    n = len(Vl)
    e = np.vstack([F[:, [0, 1]], F[:, [1, 2]]])
    _, lab = connected_components(coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(n, n)), directed=False)
    fl = lab[F[:, 0]]
    cnt = np.bincount(fl)
    keep = cnt > 2000
    for ci in np.where(keep)[0]:
        sub = trimesh.Trimesh(Vl, F[fl == ci], process=False)
        if sub.is_watertight and sub.volume < 0:  # enclosed void
            keep[ci] = False
            log(f"assemble: dropped void {sub.volume:.1f} mm3")
    F = F[keep[fl]]
    used = np.unique(F)
    remap = -np.ones(n, int)
    remap[used] = np.arange(len(used))
    trimesh.Trimesh(Vl[used], remap[F], process=False).export(work / "part_local.ply")

    # skull part: faces with no vertex in the outer box (vertices must be merged!)
    sk = trimesh.load(a.skull_stl)  # process=True merges STL triangle soup
    B0, B1 = lo + P["STITCH_OUTER"], hi - P["STITCH_OUTER"]
    inB = np.all((sk.vertices > B0) & (sk.vertices < B1), 1)
    skp = sk.submesh([np.where(~inB[sk.faces].any(1))[0]], append=True)
    skp.merge_vertices()
    skp.export(work / "part_skull.ply")

    # stitch matching boundary loops
    m = mr.loadMesh(str(work / "part_skull.ply"))
    na = m.topology.lastValidFace().get() + 1
    m.addMesh(mr.loadMesh(str(work / "part_local.ply")))

    def loop_pts(e_):
        path = mr.trackRightBoundaryLoop(m.topology, e_)
        return np.array([[m.orgPnt(x).x, m.orgPnt(x).y, m.orgPnt(x).z] for x in path])

    holes = list(m.topology.findHoleRepresentiveEdges())
    pts = [loop_pts(h) for h in holes]
    side = [0 if m.topology.left(h.sym()).get() < na else 1 for h in holes]
    S = [i for i in range(len(holes)) if side[i] == 0]
    Lc = [i for i in range(len(holes)) if side[i] == 1]
    log(f"assemble: {len(S)} skull loops, {len(Lc)} local loops")
    used_l = set()
    for i in sorted(S, key=lambda i: -len(pts[i])):
        best = None
        for j in Lc:
            if j in used_l:
                continue
            pi, pj = pts[i], pts[j]
            d = np.min(np.linalg.norm(pi[:: max(1, len(pi) // 60), None] - pj[None, :: max(1, len(pj) // 200)], axis=2), axis=1).mean()
            if best is None or d < best[0]:
                best = (d, j)
        if best is None or best[0] > 2.5:
            sys.exit(f"assemble: no partner for skull loop {i} (len {len(pts[i])}); adjust STITCH_* or the grid margin")
        used_l.add(best[1])
        mr.stitchHoles(m, holes[i], holes[best[1]], mr.StitchHolesParams())
    if set(Lc) - used_l:
        sys.exit("assemble: unpaired local loops remain")

    def fix(mm, tag):
        st = mr.SelfIntersections.Settings()
        st.method = mr.SelfIntersections.Settings.Method.Relax
        st.relaxIterations = 10
        st.maxExpand = 5
        k = mr.findSelfCollidingTrianglesBS(mm).count()
        it = 0
        while k and it < 8:
            mr.localFixSelfIntersections(mm, st)
            k = mr.findSelfCollidingTrianglesBS(mm).count()
            it += 1
        log(f"assemble: {tag}: faces {mm.topology.numValidFaces()} holes {mm.topology.findNumHoles()} self-intersections {k}")
        return k

    fix(m, "stitched")
    ds = mr.DecimateSettings()
    ds.maxError = P["DECIMATE_ERR"]
    ds.strategy = mr.DecimateStrategy.MinimizeError
    ds.packMesh = True
    ds.maxTriangleAspectRatio = 20
    ds.stabilizer = 0.001
    mr.decimateMesh(m, ds)
    k = fix(m, "decimated")
    if k or m.topology.findNumHoles():
        log("WARNING: output not clean, inspect before printing")
    mr.saveMesh(m, str(a.out))
    log(f"wrote {a.out}")


# ================================================================ stage: validate
def stage_validate(a, work):
    import meshlib.mrmeshpy as mr
    import meshlib.mrmeshnumpy as mn

    out = mr.loadMesh(str(a.out))
    orig = mr.loadMesh(str(a.skull_stl))
    rep = dict(
        faces=out.topology.numValidFaces(),
        holes=out.topology.findNumHoles(),
        self_intersections=mr.findSelfCollidingTrianglesBS(out).count(),
        volume=out.volume(),
        volume_input=orig.volume(),
    )
    tm = trimesh.load(a.out)
    rep["components"] = [(len(b.faces), round(b.volume, 2)) for b in sorted(tm.split(only_watertight=False), key=lambda b: -len(b.faces))[:8]]
    # everything >3 mm from the scans must be (nearly) unchanged
    sv = np.vstack([trimesh.load(work / f"scan_{j}.ply", process=False).vertices for j in JAWS])
    lo = np.load(work / "grid_lo.npy")
    hi = lo + (np.load(work / "grid_shp.npy") - 1) * P["H"]
    V = mn.getNumpyVerts(orig)
    box = np.all((V > lo) & (V < hi), 1)
    far = np.where(box)[0]
    far = far[cKDTree(sv).query(V[far])[0] > 3.0][::2]
    d = np.array([mr.findSignedDistance(mr.Vector3f(*map(float, V[i])), out).dist for i in far])
    rep["unchanged_region_vertices"] = int(len(d))
    rep["unchanged_region_max_dev"] = float(np.abs(d).max()) if len(d) else 0.0
    rep["unchanged_region_n_over_0.3mm"] = int((np.abs(d) > 0.3).sum())
    (work / "validate.json").write_text(json.dumps(rep, indent=2))
    for k, v in rep.items():
        print(f"  {k}: {v}")


# ================================================================ stage: render
BLENDER_SCRIPT = r'''
import bpy, sys, os
from mathutils import Vector, Matrix
a = sys.argv[sys.argv.index("--")+1:]
out, mesh = a[0], a[1]
views = [v.split(";") for v in a[2:]]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'OBJECT'
sc.render.resolution_x = sc.render.resolution_y = 1000
bpy.ops.wm.stl_import(filepath=mesh)
o = bpy.context.selected_objects[0]; o.color = (0.85, 0.85, 0.85, 1)
cam = bpy.data.objects.new("C", bpy.data.cameras.new("C")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.clip_start = 0.05; cam.data.clip_end = 2000
for name, pos, tgt, lens in views:
    cp = Vector([float(x) for x in pos.split(",")]); tg = Vector([float(x) for x in tgt.split(",")])
    cam.data.lens = float(lens); cam.location = cp
    d = (tg - cp).normalized(); z = -d; up = Vector((0, 0, 1))
    if abs(d.dot(up)) > 0.95: up = Vector((0, 1, 0))
    x = up.cross(z).normalized(); y = z.cross(x)
    cam.rotation_euler = Matrix((x, y, z)).transposed().to_euler()
    sc.render.filepath = os.path.join(out, name + ".png")
    bpy.ops.render.render(write_still=True)
'''


def stage_render(a, work):
    scans = {j: trimesh.load(work / f"scan_{j}.ply", process=False).vertices for j in JAWS}
    allv = np.vstack(list(scans.values()))
    c = allv.mean(0)
    # anterior = side of the arch opposite to the arch's open end: use PCA-free heuristic
    # (incisors are the scan points farthest from the molars' centroid along y in LPS: -y)
    ant = allv[np.argmin(allv[:, 1])]
    post_y = allv[:, 1].max()
    mid_x = np.median(allv[:, 0])
    zc = c[2]
    views = [f"front;{ant[0]:.1f},{ant[1] - 45:.1f},{zc:.1f};{ant[0]:.1f},{ant[1]:.1f},{zc:.1f};50"]
    for jaw in JAWS:
        v = scans[jaw]
        zj = np.median(v[:, 2])
        for sgn, nm in ((1, "R"), (-1, "L")):
            side = v[np.sign(v[:, 0] - mid_x) == sgn]
            back = side[side[:, 1] > np.percentile(side[:, 1], 90)].mean(0)
            cam = np.array([mid_x + sgn * 2, back[1] - 12, zj])
            views.append(f"{jaw}_{nm}_back;{cam[0]:.1f},{cam[1]:.1f},{cam[2]:.1f};{back[0]:.1f},{back[1] + 4:.1f},{back[2]:.1f};24")
    outdir = work / "renders"
    outdir.mkdir(exist_ok=True)
    script = work / "render_blender.py"
    script.write_text(BLENDER_SCRIPT)
    cmd = a.blender.split() + ["-b", "--python", str(script), "--", str(outdir), str(Path(a.out).resolve())] + views
    log("render:", " ".join(cmd[:4]), "...")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    log(f"renders in {outdir}")


# ================================================================ main
STAGES = dict(register=stage_register, labels=stage_labels, field=stage_field, assemble=stage_assemble, validate=stage_validate, render=stage_render)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=[*STAGES, "all"])
    for k in ("skull-stl", "skull-mask", "teeth-upper", "teeth-lower", "scan-upper", "scan-lower", "printable-upper", "printable-lower"):
        ap.add_argument(f"--{k}", required=True, type=Path)
    ap.add_argument("--work", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--blender", default="blender", help='Blender command, e.g. "flatpak run --filesystem=/tmp --command=blender org.blender.Blender"')
    a = ap.parse_args()
    a.work.mkdir(parents=True, exist_ok=True)
    order = ["register", "labels", "field", "assemble", "validate"] if a.stage == "all" else [a.stage]
    for st in order:
        log(f"=== {st}")
        STAGES[st](a, a.work)
    if a.stage == "all" and shutil.which(a.blender.split()[0]):
        try:
            stage_render(a, a.work)
        except subprocess.CalledProcessError as exc:
            log(f"render skipped: {exc}")


if __name__ == "__main__":
    main()
