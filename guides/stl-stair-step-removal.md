# STL Stair-Step Removal Guide

How to remove terracing/banding from a CT-derived STL while keeping detail.
Worked example: a skull mesh (`skull_merged.stl`, 470 k tris) with visible
bands on the dome. Companion script: `../utilities/python/stl-destep.py`.

## Key finding: measure the bands before smoothing

The visible defect was **broad, shallow ripples (~8–16 mm wavelength)**,
not 0.8 mm voxel cliffs — even though the source CT had 0.8 mm slices.
This decided everything: voxel-scale smoothers (σ ≤ 0.8 mm) failed, and
only dome-scale fairing (diffusion ~15 mm) cleared the bands.

What actually diagnosed it:

- **Screenshot band measurement.** Threshold the skull silhouette, derive
  mm/px from the known model height, average brightness per row over the
  dome, detrend, FFT. Dominant periods came out at 8–24 mm — no sub-mm
  peak. This measures the complaint directly instead of guessing.
- **Full-res grazing-light closeups.** Smooth shading (like a slicer
  preview) + low sun altitude + no decimation. Decimated previews and
  soft lighting wash the bands out; flat-shaded or amplified maps drown
  in facet noise. This was the only visualization that clearly separated
  the winner from the rest.
- **Mid-sagittal profiles.** Useful to prove *no drift* (all candidates
  agreed within ~0.1 mm) but useless for seeing the steps — too shallow
  at 1:1 aspect.

What did **not** work as a metric: residual RMS against a smoothed copy
(the "macro" reference distorts and dominates), raw FFT amplitudes across
different tessellations (not comparable), and shading-roughness RMS
(measures incoherent facet noise, while bands are *coherent* ripple).

## Methods tested, ranked by visible band removal

1. **Masked Taubin fairing, strong (winner).** 600 iterations of
   λ0.5/μ−0.53 Laplacian flow under a smooth positional mask covering
   only the dome; 1.0 mm displacement clamp. Bands gone, face/teeth/jaw
   bit-identical. Cost: dome moved up to 1 mm (p95 0.34 mm), −0.35% vol.
2. **Source re-extraction, strong** (`medsurface labelmap extract`,
   mask σ 0.8 mm, 60 + 20 mesh iters). Reduced but did not erase the
   broad bands, and melted thin midface bone up to ~5 mm locally.
   Re-extraction fixes voxel-scale steps, not broad ripples.
3. **Source re-extraction, medium** (finer 0.33 mm grid, σ 0.65).
   Barely better than the original on the dome; same midface cost.
4. **Conservative masked Taubin** (120 iters, 0.6 mm clamp). Safe
   (max drift 0.33 mm) but too weak for broad bands.
5. **Screened Poisson** (1.5 M samples, depth 10, → 450 k tris).
   Very faithful (mean drift 0.009 mm) but faithfully reproduced the
   ripples — reconstruction follows the surface it is given.
6. **Bilateral normal filter (negative result).** Smoothed normals
   (σs 1.0, σr 0.5) + vertex refit moved almost nothing (mean
   0.005 mm): it preserved the shallow terrace ramps as "features".
7. **ML mesh denoising.** Not tested — no local models, and classical
   methods already spanned the tradeoff without hallucination risk.

## Recommended redo

```bash
stl-destep.py skull_merged.stl -o skull_desteped.stl \
    --axis z --full -555 --zero -600 --validate
```

Defaults (600 iters, λ0.5/μ−0.53, 1.0 mm clamp) are the winning values;
only the mask bounds are mesh-specific. General rule: set `--full`/`--zero`
so the mask covers the ripple zone with margin, and keep it clear of
detail — masked-out vertices never move. Raise iterations (~sqrt scaling
of diffusion length) until bands clear under grazing light.

## Gotchas

- **Fairing folds sliver triangles.** Expect a handful of disoriented /
  self-intersecting faces after strong smoothing. Fix by reverting folded
  faces (+1 ring) to original positions — a few dozen verts out of 235 k,
  then re-validate. `medsurface repair` fixes topology, *not* folded
  geometry, so it cannot repair this.
- **Re-extraction is global.** Mask smoothing cannot spare the face while
  fixing the dome; σ ≥ 0.65 mm measurably damaged thin anterior bone
  here. Prefer masked mesh fairing when detail and ripples coexist.
- **Finer grids have limits.** A 0.3 mm resample grid exceeded the
  500 M-voxel default cap (611 M); 0.33 mm fit. Finer ≠ smoother anyway
  when the artifact is broader than the voxels.
- **Validate everything.** Every candidate here ended watertight with
  0 holes and 0 self-intersections — check with
  `medsurface validate model.stl` before printing.
- **open3d OffscreenRenderer** printed black frames in this headless
  setup (scene/camera API mismatch); matplotlib `plot_trisurf` on
  full-res crops was the reliable renderer.
