# Replacing CT Teeth in a Skull STL with Intraoral Scans

How to swap the blurry, CT-derived teeth of a skull mesh for crisp intraoral
scans (e.g. CEREC/iTero exports) so that the crowns emerge naturally from the
CT bone, without gum, seams, curtains, or collars. Worked example: a
CT-derived skull (`skull_edited.stl`, 306 k tris, 0.4 mm labelmap) plus
upper/lower scans. The accepted result was v6 (`skull_edited_claude.stl`).
Companion script: `../utilities/python/skull-teeth-replace.py`.

## TL;DR

```bash
skull-teeth-replace.py all \
  --skull-stl skull.stl --skull-mask skull.nii.gz \
  --teeth-upper ct/teeth_upper.nii.gz --teeth-lower ct/teeth_lower.nii.gz \
  --scan-upper upper_jaw.stl --scan-lower lower_jaw.stl \
  --printable-upper "upper jaw printable.stl" \
  --printable-lower "lower jaw printable.stl" \
  --work work/ --out skull_teeth.stl \
  --blender "flatpak run --filesystem=$PWD --command=blender org.blender.Blender"
```

The script is a `uv run --script` file with inline dependencies (meshlib,
trimesh, scipy, SimpleITK, networkx). It needs about 16 GB of RAM and takes
about 13 minutes on 12 cores. Rerunning it on the original inputs reproduced
the accepted v6 to a median of 0.0003 mm (p99.9 0.04 mm). Then inspect `work/labels_*.ply`, `work/renders/*.png`
and `work/validate.json`, and do the final manual cleanup in a sculpting tool.

## Inputs and how to prepare them

| Input             | What it is                               | Notes                                                                                                                                                  |
| ----------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Skull STL         | Closed mesh extracted from the CT        | Must be in the CT world frame (SimpleITK/LPS mm), not re-centred.                                                                                      |
| Skull labelmap    | Binary mask the STL came from            | Used for inside/outside far from the surface and for the gum/tooth prior.                                                                              |
| CT teeth masks    | Upper and lower tooth segmentations      | TotalSegmentator `teeth_upper`/`teeth_lower` work fine; they are coarse (0.3×0.3×0.8 mm here), and that is enough.                                     |
| Edited scans      | Open intraoral scans, one per jaw        | Trim to the teeth plus a thin gum band (Meshmixer). Delete loose fragments. Upper and lower may be in unrelated frames; each is registered separately. |
| Printable scans   | Closed solids made from the edited scans | Scan + extruded base (e.g. BlueSkyPlan "printable model"). Needed because inside/outside of an **open** scan is only defined right at its surface.     |
| Raw CT (optional) | Intensity volume                         | Only for diagnostics (e.g. checking wisdom teeth). Here: `older_versions/v6/GS_nativ_1mm_axial_spine_removed.nrrd`, same grid as the masks.            |

Tools: `uv`, Blender (Flatpak is fine) for QA renders, ImageMagick `montage`
for contact sheets. meshlib does the heavy lifting (exact distance volumes,
marching cubes, hole stitching, self-intersection repair, decimation).
Local `pymeshlab`/`open3d` are not needed.

## Pipeline

### 1. Register each scan to the CT teeth (`register`)

- **Target:** skull-mesh faces whose centroid lies in the CT teeth mask
  dilated by about 0.9 mm in-plane and one slice in z, with 25 k surface
  samples and face normals. **Do not enlarge the dilation.** A 1.3 mm × 1.6 mm
  dilation pulled alveolar bone into the target and rotated the lower jaw by
  1.5° (0.6 mm) while even *raising* the ICP score. The only visible sign was
  sunken lower molars in the output.
- **Source:** 10 k vertices of the scan's largest component.
- **Multi-start ICP:** align the PCA frames with 4 axis-sign combinations and
  ±30° rotations about the arch normal, then run 60 iterations of
  point-to-plane ICP with a trimming threshold going from 3 mm to 0.8 mm.
  Score each start by inlier fraction plus target coverage.
- **Proper rotations only:** the SVD frames can have det −1, so correct the
  sign combination with `det(ct_v)·det(sc_v)`. Otherwise one jaw registers as
  its **mirror image** with a deceptively good score. This happened here and
  was caught by `det(R) = −1`.
- **Expected quality:** 40–60 % inliers, about 0.43 mm RMS. The CT crowns are
  blurred, so do not expect better.
- **Printable to scan:** ICP from 4 flip candidates, scored by the median
  distance from the scan to the printable surface. It should end below about
  0.1 mm (here 0.035 mm).

Verify: render scan and skull together (front, side, underside). Crowns should
interleave with the CT crowns, and the gum band should sit just outside the
bone.

### 2. Tooth/gum segmentation of the scans (`labels`)

The skull has no gums, so gum must be dropped and only the crowns kept. The
segmentation has three steps:

1. **Distance prior.** `tooth = (d < 0.4 & dt < 1.0) | (db > 3 & dt < 2)`.
   - `d` is the scan vertex's signed distance to the skull mask.
   - `dt` is its distance to the CT teeth mask.
   - `db` is its distance to "bone", meaning skull minus the dilated teeth.

   The second clause keeps incisal edges, which the CT rounds off. Smooth the
   labels with 10 neighbour-averaging passes and drop islands (fewer than
   3000 tooth vertices or 400 gum vertices).

   Distance alone leaves a 0.5–1 mm band of gum labelled as tooth at the
   gingival margin, plus patches where the gum lies close to the bone.
2. **Concavity.** `H = dot(v − smooth⁸(v), n)`, where negative means concave.
   The gingival margin shows up as a crisp concave line.
3. **Graph cut.** Run a max-flow over mesh edges (`scipy.sparse.csgraph.maximum_flow`)
   with edge capacity `1000·len·exp(−(concavity/0.03)²)`.
   - Hard constraints: prior U > 2 mm is tooth; U < −1.5 mm and scan-boundary
     vertices are gum.
   - Cutting along the crease is almost free, so the boundary snaps onto the
     real gumline.

Outputs per jaw:

- `U`: signed distance to the label boundary, positive on tooth.
- `Ub`: distance to the scan's open rim.
- `labels_*.ply`: coloured labels (blue tooth, red gum). **Inspect these.**
  If gum still sits inside the blue, the prior thresholds need tuning for
  that data set.

### 3. One signed-distance field for the whole teeth region (`field`)

Everything is computed on a 0.1 mm grid covering the scans plus 7 mm (about
220 M voxels) and turned into a surface with a single marching cubes. **No
mesh booleans are used for the teeth.** Every boolean-based attempt produced
near-coincident surfaces, sliver seams, and self-intersections.

Distance volumes, all from `meshlib.meshToDistanceVolume`:

- `SSK`: exact signed distance to the skull STL, with the sign from the
  winding rule. Beyond 5 mm the sign comes from the labelmap.
- `P_j`: distance to the closed printable of jaw j, sign from the winding
  rule, within R + 0.5 = 3.5 mm.
- Within 0.5 mm of the crown, the exact open-scan distance (sign from the
  projection normal) replaces `P_j`. Where its sign disagrees with the
  printable by more than 0.15 mm, the printable wins. This keeps the scan's
  exact crown surface (the printable has shallow dents) without the open-scan
  sign failures.

Per-voxel weights for jaw j. They come from the 12 nearest scan vertices with
Gaussian weights (σ 0.15 mm) relative to the nearest one, which keeps `w`
continuous:

```
w_j  = smooth(U/1.0) · depth · rimf         # 0 on gum, 1 on crown (1 mm ramp)
depth: inside the crown  1 → 0 between 1.8 and 2.8 mm  (CT takes over deep inside)
       outside the crown 1 → 0 between 0.8 and 1.4 mm  (how far the scan may delete CT)
rimf = smooth((Ub−0.8)/1.2) · smooth((d_rim − d_nearest − 0.2)/0.8)
                                             # no scan authority past the open rim
c_j  = F · (1 − smooth(−U/3)) · depth        # neck over-thickness removed from CT
G_j  = (1 − w_j)·(SSK + c_j) + w_j·P_j       # jaw j alone: CT blended into scan
```

Combination of the two jaws:

```
α    = smooth((d_lower − d_upper)/0.6 + 0.5)  # ownership: nearer scan surface wins
T    = min_j ( P_j + (1 − w_j)·(R + 1) )       # union of scanned crowns only
G    = min( α·G_upper + (1 − α)·G_lower , T )
```

Each term exists because of a specific failure in earlier versions:

- **Blend, not a cut.** A hard lateral cut at the gumline leaves exposed
  "curtain" walls and frayed edges. The blend makes the crown flow into the
  CT neck over 1 mm.
- **Value = `P_j`, never a penalised value.** An early version used
  `s + (1−w)·K` as the value. That pushed the surface inward by up to
  `w(1−w)K ≈ 1 mm` and produced a trough with a raised rim around every
  tooth.
- **Neck shrink `c`.** CT blur makes the neck up to 1–1.5 mm fatter than the
  crown. Without the shrink, every tooth gets a collar. F is measured on crown
  vertices within 0.8 mm of the gumline and averaged over 1.5 mm along the
  arch.
- **Ownership α.** A single max(w) across jaws let the upper crowns' weight
  apply the lower **gum** of the printable, which gave cracks with lips
  buccally.
- **Crown union T.** Without it, where cusps interdigitate, the other jaw's
  ownership hollows out cusp tips. The `(R+1)` penalty keeps T ≥ 0.5 wherever
  w = 0, so it never adds material outside a scanned crown.
- **Short outward reach (0.8 → 1.4 mm).** With 2.8 mm, the upper crowns
  deleted up to 1.5 mm of the (unscanned) lower **wisdom teeth**, which sit
  1.6–2.1 mm below them. A mask-based exception using the CT teeth
  segmentation was worse, because the coarse mask left a lump under a molar.
  The short reach alone still removes the fused CT blur between crowns
  (0.5–0.8 mm).
- **`rimf`.** Distally on the last molars the scan ends *on* the tooth. The
  printable's base walls start there, which caused flanges, and open-scan
  signs flip there, which caused staircase patches.
- **Voids.** Deep inside some crowns the CT mask is hollow. The enclosed
  cavities are dropped in `assemble`.

### 4. Stitch the local region into the skull (`assemble`)

- **Local part:** marching-cubes faces fully inside the grid box shrunk by
  2.4 mm. Keep components with more than 2000 faces, and drop watertight
  components with negative volume (cavities).
- **Skull part:** original faces with no vertex inside the box shrunk by
  2.0 mm. **Load the STL with vertex merging.** STL is triangle soup; with
  `process=False` every face becomes its own hole (285 k "holes").
- **Stitching:** in the gap of about 1.2–1.5 mm both surfaces follow the same
  bone, so the boundary loops pair up 1:1 by mean distance (here 4 pairs).
  `meshlib.stitchHoles(a, b)` bridges each pair. This avoids booleans on
  coincident surfaces entirely.
- **Repair and decimation:** a few self-intersections from stitching are
  fixed with `localFixSelfIntersections` (Relax). The CutAndFill method made
  things worse here. Decimate with `maxError 0.005 mm`, then check again.
  Result: 1.74 M tris, watertight, 0 holes, 0 self-intersections.

### 5. Validate and look (`validate`, `render`)

`validate.json` reports holes, self-intersections, components (the input's
tiny internal bodies are kept as they were), volume, and the **max deviation
of the input skull more than 3 mm from any scan**. That value must stay near
0 (here ≤ 0.12 mm); it proves nothing outside the teeth was touched. It is how
the wisdom-tooth cut was finally quantified.

Renders:

- Orthographic overviews are occluded by the jaw and cheek bones inside the
  mouth. Use **perspective cameras inside the mouth** aimed at the last
  molars (the script does that) and at any complaint location.
- For a precise diagnosis, **ray-cast** from the camera through the pixel of
  an artifact (`meshlib.rayMeshIntersect`) to get its 3D point.
- Then **probe every field component there**: `findSignedDistance` to skull,
  printable, and scan, plus U and Ub. Every hard bug in this project was
  found this way in minutes, after hours of guessing.

## Parameters

| Parameter                     | Value        | Effect of changing it                                                                                                         |
| ----------------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `H`                           | 0.1 mm       | Field resolution. 0.15 visibly softens crown detail; 0.1 needs about 16 GB.                                                   |
| `R`                           | 3.0 mm       | Scan influence band; the grid margin is R + 4.                                                                                |
| `W`                           | 1.0 mm       | Gumline blend width. Wider looks softer but shows more CT neck.                                                               |
| `OUT_FULL`/`OUT_ZERO`         | 0.8 / 1.4 mm | How far a scan may delete CT outside its crown. Larger cuts unscanned neighbours (wisdom teeth); smaller leaves blur collars. |
| `IN_FULL`/`IN_ZERO`           | 1.8 / 2.8 mm | Depth of scan authority inside the crown.                                                                                     |
| `FAT_MAX`                     | 1.5 mm       | Cap for neck shrink.                                                                                                          |
| `TAU`                         | 0.4 mm       | Label prior; raise for noisy registrations.                                                                                   |
| `GC_SIGMA`                    | 0.03         | Concavity scale of the graph cut; lower snaps harder to creases.                                                              |
| `STITCH_OUTER`/`STITCH_INNER` | 2.0 / 2.4 mm | Stitch gap. The skull's largest triangles must fit into the gap.                                                              |
| `DECIMATE_ERR`                | 0.005 mm     | Final size (about 87 MB STL here).                                                                                            |

## Symptom → cause → fix (what went wrong on the way)

| Symptom                                      | Cause                                                                           | Fix                                                                  |
| -------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| One jaw mirrored after ICP                   | SVD frame with det −1                                                           | Enforce det +1 when building the start rotation                      |
| Tall "curtains" at molars, frayed gumline    | Hard lateral cut; scan gum band outside bone                                    | Field blend instead of cut; drop gum via labels                      |
| Gum still on the model                       | Distance-only labels                                                            | Curvature-guided graph cut                                           |
| Thick collar or trough with rim around teeth | Penalty term leaked into the value; CT neck blur                                | Use penalty only for selection (later replaced); neck shrink `c`     |
| Rough dotted seams, 100+ self-intersections  | Booleans on near-coincident surfaces                                            | Single field + marching cubes + stitching                            |
| Horizontal step on an incisor                | Per-jaw union reintroduced CT removed by the other jaw                          | Proper jaw combination                                               |
| Grainy transition band                       | Hard switch between point-to-plane and Euclidean distance; per-face label jumps | Exact meshlib distance volumes; barycentric/Gaussian-averaged labels |
| Staircase patches on distal molars           | Open-scan winding sign flips near the scan opening                              | Projection-normal sign near the surface, printable sign as arbiter   |
| Thin flanges at last molars                  | Printable base walls where the scan ends on the tooth                           | `rimf` (no authority past the rim)                                   |
| Cracks with lips at lower buccal gum         | max(w) across jaws applied lower gum from the printable                         | Nearest-surface ownership α                                          |
| Crumbly occlusal contact line, hollow cusps  | Ownership cuts through interdigitating cusps                                    | Crown union T                                                        |
| Wisdom teeth "cut off"                       | Outward reach 2.8 mm deleted unscanned opposite-jaw teeth                       | Outward reach 0.8 → 1.4 mm                                           |
| Lump under upper molar                       | CT-mask exception kept blur                                                     | Drop the mask exception                                              |
| Line at lingual neck of last molars          | Neck shrink disabled near the rim                                               | Keep neck shrink everywhere                                          |

## Operational gotchas

- **meshlib volume conventions:** `getNumpy3Darray` is indexed `[x, y, z]`,
  and samples sit at voxel **centres**, `origin + (i + 0.5)·h`. Pass
  `origin = lo − h/2` to sample at `lo + i·h`. Values beyond `maxDistSq` are
  NaN.
- **Sign modes:** `WindingRule` for closed meshes is robust. For open scans
  it fails near the opening, and `ProjectionNormal` fails in concave pockets
  and far away. Use open-scan signs only within about 0.5 mm of the crown.
- **Vertex order:** labels are per scan vertex. Keep one loaded copy (PLY
  preserves order; the script builds meshlib meshes from the same numpy
  arrays).
- **KD-tree speed:** queries far from a clustered point set are about 50×
  slower. Always pass `distance_upper_bound`.
- **Mask resampling:** masks have their own direction matrix (a 2.5° rotation
  here). Always go through SimpleITK physical coordinates, never raw indices.
- **Blender Flatpak:** it cannot see `/tmp` unless you pass
  `--filesystem=<dir>`. Render large scenes with perspective cameras and
  `clip_start ≈ 0.05`.
- **Long background jobs:** start them with `setsid nohup … &`. A `timeout`
  wrapper or tool timeout otherwise kills the job. Do not `pkill -f` a
  pattern that also matches your own shell command.

## Diagnosing unscanned teeth (wisdom teeth)

1. Calibrate enamel on the raw CT by sampling 0.7 mm inside scanned crowns.
   Here enamel was about 3400 and cortical bone about 1400, after a σ 0.7
   voxel Gaussian.
2. Threshold at about 2600 and keep the voxels more than 2 mm from the
   scans. Here that gave 4 clusters of 150–210 mm³ behind the last molars.
3. Take intensity profiles through each cluster toward the occlusal side.
   If the enamel drops straight into soft tissue, the teeth are erupted, and
   the model surface must sit roughly at their crown tops.
4. Compare the new model with the input there. Any cut-in above 0.3 mm means
   the outward reach is too long.

## Manual cleanup afterwards

- Interdental spaces carry some of the scanner's own noise; smooth them
  lightly.
- Wisdom teeth are only as sharp as the CT segmentation. If needed, rebuild
  their crowns from the raw CT (iso about 1500 on the smoothed intensities)
  in the same field framework.
- The stitch strip lies on plain bone about 2 mm inside the grid box. It is
  flat but has large triangles; remesh it if it catches the light.
