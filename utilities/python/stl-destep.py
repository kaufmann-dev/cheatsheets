#!/usr/bin/env python3
"""Remove stair-step / terracing ripples from an STL by masked fairing.

Method: uniform-Laplacian Taubin smoothing applied per-iteration under a
smooth positional mask, so only the ripple zone moves and detail elsewhere
is bit-identical. Displacement is clamped, then any triangles folded by the
fairing are reverted to their original positions (topology is untouched,
so a watertight input stays watertight).

Requirements: Python 3.10+, trimesh, numpy, scipy.
Optional: `medsurface` on PATH for `--validate`.

Example (skull dome bands, +Z up, teeth/jaw protected below):
  stl-destep.py skull_merged.stl -o skull_desteped.stl \\
      --axis z --full -555 --zero -600 --iterations 600 --max-disp 1.0

Tuning: raise --iterations (diffusion grows ~sqrt(iters)) until the bands
visibly clear under grazing light; keep --zero/--full clear of detail you
must keep, since masked-out vertices never move.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import trimesh
from scipy import sparse

AXIS_INDEX = {"x": 0, "y": 1, "z": 2}


class CliError(Exception):
    """Represent a user-facing CLI error."""

    def __init__(self, message: str, exit_code: int = 2) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Remove stair-step ripples from an STL by masked Taubin fairing.")
    p.add_argument("input", type=Path, help="Input .stl (never modified).")
    p.add_argument("-o", "--output", type=Path, default=None,
                   help="Output .stl (default: <input-stem>_desteped.stl).")
    p.add_argument("--axis", choices="xyz", default="z",
                   help="Mask axis; ripple zone is at high coords (default: z).")
    p.add_argument("--full", type=float, required=True,
                   help="Mask = 1 (full fairing) at/above this coordinate.")
    p.add_argument("--zero", type=float, required=True,
                   help="Mask = 0 (frozen) at/below this coordinate.")
    p.add_argument("--invert", action="store_true",
                   help="Fair low coords instead (mask = 1 below --full).")
    p.add_argument("--iterations", type=int, default=600,
                   help="Taubin iterations; diffusion ~ sqrt(iters) (default: 600).")
    p.add_argument("--lamb", type=float, default=0.5, help="Taubin lambda (default: 0.5).")
    p.add_argument("--mu", type=float, default=-0.53, help="Taubin mu (default: -0.53).")
    p.add_argument("--max-disp", type=float, default=1.0,
                   help="Clamp per-vertex displacement to this (model units).")
    p.add_argument("--unfold-dot", type=float, default=0.2,
                   help="Revert faces whose normal rotated past this dot product.")
    p.add_argument("--no-unfold", action="store_true",
                   help="Skip the fold-repair pass (not recommended).")
    p.add_argument("--validate", action="store_true",
                   help="Run `medsurface validate` on the output when available.")
    p.add_argument("--quiet", action="store_true", help="Only print the final summary.")
    return p.parse_args(argv)


def smooth_mask(coord: np.ndarray, full: float, zero: float, invert: bool) -> np.ndarray:
    if full == zero:
        raise CliError("--full and --zero must differ.")
    t = np.clip((coord - zero) / (full - zero), 0.0, 1.0)
    w = 0.5 - 0.5 * np.cos(np.pi * t)
    return 1.0 - w if invert else w


def uniform_laplacian(n: int, edges: np.ndarray) -> sparse.csr_matrix:
    row = np.concatenate([edges[:, 0], edges[:, 1]])
    col = np.concatenate([edges[:, 1], edges[:, 0]])
    adj = sparse.coo_matrix((np.ones(len(row)), (row, col)), shape=(n, n)).tocsr()
    deg = np.asarray(adj.sum(1)).ravel()
    deg[deg == 0] = 1
    return sparse.diags(1.0 / deg) @ adj - sparse.eye(n)


def masked_taubin(v0: np.ndarray, lap: sparse.csr_matrix, w: np.ndarray,
                  lamb: float, mu: float, iters: int, quiet: bool) -> np.ndarray:
    v = v0.copy()
    for it in range(iters):
        k = lamb if it % 2 == 0 else mu
        v += (w * k)[:, None] * (lap @ v)
        if not quiet and (it + 1) % max(1, iters // 4) == 0:
            d = np.linalg.norm(v - v0, axis=1)
            print(f"  iter {it + 1}/{iters}: mean|d|={d.mean():.4f} max|d|={d.max():.3f}")
    return v


def unfold_repair(mesh: trimesh.Trimesh, v_orig: np.ndarray, n_orig: np.ndarray,
                  dot_min: float, quiet: bool) -> int:
    """Revert vertices of faces folded by fairing (plus 1-ring) to original."""
    faces = np.asarray(mesh.faces)
    neighbors = mesh.vertex_neighbors
    v = np.asarray(mesh.vertices, dtype=np.float64)
    reverted: set[int] = set()
    for _ in range(5):
        mesh.vertices = v
        n = np.asarray(mesh.face_normals)
        bad = np.where(np.einsum("ij,ij->i", n, n_orig) < dot_min)[0]
        if len(bad) == 0:
            break
        verts = set(faces[bad].ravel().tolist())
        for x in list(verts):
            verts.update(neighbors[x])
        fresh = [x for x in verts if x not in reverted]
        v[list(verts)] = v_orig[list(verts)]
        reverted.update(fresh)
    mesh.vertices = v
    if not quiet:
        print(f"  unfold repair: {len(reverted)} verts reverted")
    return len(reverted)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        if not args.input.is_file():
            raise CliError(f"input not found: {args.input}")
        if args.iterations < 1:
            raise CliError("--iterations must be >= 1.")
        out = args.output or args.input.with_name(f"{args.input.stem}_desteped.stl")
        if out.resolve() == args.input.resolve():
            raise CliError("output must differ from input; the input is never modified.")

        mesh = trimesh.load(args.input, force="mesh")
        v0 = np.asarray(mesh.vertices, dtype=np.float64)
        n0 = np.asarray(mesh.face_normals, dtype=np.float64)
        vol0 = abs(mesh.volume)
        if not args.quiet:
            print(f"input: {len(mesh.faces)} tris, watertight={mesh.is_watertight}, "
                  f"vol={vol0:.0f}")

        w = smooth_mask(v0[:, AXIS_INDEX[args.axis]], args.full, args.zero, args.invert)
        if not args.quiet:
            print(f"mask: full={np.mean(w > 0.99) * 100:.1f}% "
                  f"frozen={np.mean(w < 0.01) * 100:.1f}%")
        if w.max() <= 0:
            raise CliError("mask is zero everywhere; check --full/--zero/--invert.")

        lap = uniform_laplacian(len(v0), np.asarray(mesh.edges_unique, dtype=np.int64))
        v = masked_taubin(v0, lap, w, args.lamb, args.mu, args.iterations, args.quiet)

        delta = v - v0
        dist = np.linalg.norm(delta, axis=1)
        over = dist > args.max_disp
        if over.any():
            delta[over] *= (args.max_disp / dist[over])[:, None]
        mesh.vertices = v0 + delta

        if not args.no_unfold:
            unfold_repair(mesh, v0, n0, args.unfold_dot, args.quiet)

        mesh.remove_infinite_values()
        mesh.export(out)
        d = np.linalg.norm(np.asarray(mesh.vertices) - v0, axis=1)
        print(f"wrote {out}: {len(mesh.faces)} tris, watertight={mesh.is_watertight}, "
              f"vol={abs(mesh.volume):.0f} ({(abs(mesh.volume) - vol0) / vol0 * 100:+.2f}%), "
              f"disp max={d.max():.3f} mean={d.mean():.4f} "
              f"rms={float(np.sqrt((d ** 2).mean())):.4f} p95={np.percentile(d, 95):.4f}")

        if args.validate:
            exe = shutil.which("medsurface")
            if exe is None:
                print("note: medsurface not on PATH, skipping validation.")
            else:
                r = subprocess.run([exe, "validate", str(out)], capture_output=True, text=True)
                print(r.stdout[-600:] if r.returncode == 0 else r.stdout + r.stderr)
        return 0
    except CliError as e:
        print(f"error: {e}", file=sys.stderr)
        return e.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
