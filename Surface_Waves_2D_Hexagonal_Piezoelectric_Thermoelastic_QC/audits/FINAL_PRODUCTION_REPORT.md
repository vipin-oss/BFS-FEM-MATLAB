# FINAL_PRODUCTION_REPORT.md

## 1. Status

🟢 FINAL PAPER + FIGURE PIPELINE + COMPLETE REPRODUCIBLE PACKAGE READY.
Task-15 closure: polishing only; science frozen; all 30 parts executed.

## 2. Manuscript statistics

- File: `manuscript/FINAL_MANUSCRIPT.pdf` (built by run_all.py)
- Pages: 29 (target 26–30, ~28 preferred) — PASS
- Figures: 11 (target 9–11) — PASS; tables: 3
- Compilation: pdflatex with rerun loop until cross-references stabilise;
  0 errors, 0 LaTeX warnings, 0 undefined references
- Captions only in .tex; no caption/number text inside figure PDFs;
  no invented author/funding/COI content

## 3. Figures

| # | File | Topic | Source (raw) | Vector | Content-deterministic |
|---|---|---|---|---|---|
| 1 | fig1.pdf | Configuration-I schematic (code-drawn) | — | PDF | yes |
| 2 | fig2.pdf | Verification benchmarks & model-limit gates | v2_elastic_limit.csv, v3_model_limits.csv | PDF | yes |
| 3 | fig8.pdf | Depth-root structure of M(Ω*,k*,p) | fig8_roots.csv | PDF | yes |
| 4 | fig3.pdf | Baseline V*(Ω*), \|V_B−V_C\|, P_w | study1_baseline.csv | PDF | yes |
| 5 | fig4.pdf | Δ_BC vs floor (95/121), Δ_AC | fig4_deltas.csv, resolution_bench.csv | PDF | yes |
| 6 | fig5.pdf | Study-2 friction slices, χ=Ω*/D_w* | fig9b_map_dBC.npz | PDF | yes |
| 7 | fig9.pdf | 3D Study-2 grid views | fig9b_map_dBC.npz | PDF | yes |
| 8 | fig6.pdf | Study-3 thermal sensitivity Δ_T | fig6_tau.csv | PDF | yes |
| 9 | fig10.pdf | 3D thermal map log10 Δ_T | fig9c_map_dT.npz | PDF | yes |
| 10 | fig7.pdf | Phason-BC clamped vs free (≤8.06e-6) | fig7_bc_summary.csv | PDF | yes |
| 11 | fig11.pdf | Surface localisation δ*, flat Ω*δ* | study1_baseline.csv | PDF | yes |

## 4. Spike/anomaly summary

All features classified (audits/SPIKE_AND_ANOMALY_AUDIT.md): 1e-16 dips =
NUMERICAL CANCELLATION (retained, shaded, captioned; limits reproduced at
≤3.3e-9); 0.934208 marker = legacy coarse-scan branch record (labelled
excluded); Δ_T dips = PHYSICAL interference nodes; 3D −16 skirt =
sub-resolution roundoff region (no transition claimed). Nothing deleted,
smoothed, or clipped.

## 5. 3D figures

fig9.pdf: genuine 61×61 computed grid (3721 points), rstride=1, no
interpolation/smoothing/z-exaggeration; base contours are render-only
projections; Ω_c* drawn as reference crossover line only.
fig10.pdf: exact-cell pcolormesh over the 5×121 swept (τ0*, Ω*) samples;
every cell is a computed value; sample points marked.

## 6. Reproducibility

- `python3 run_all.py` from clean extraction: PASS (env check → invariants →
  figures → compile → report). Clean-room test in a fresh directory with all
  generated artifacts deleted: invariants PASS 22/22, 11 figures regenerated
  content-identical (stream-level comparison), manuscript 29 pp / 0 errors /
  0 warnings / 0 undefined refs. REPRODUCTION_REPORT.md: PASS.
- `--from-scratch` mode runs all 5 drivers + validation tests from solver
  source; `--check-only` runs the invariant gate only.
- No absolute paths; all locations resolved relative to the package root.
- Raw data in results/raw/ are byte copies of the accepted upstream package
  (sha256 b817860569293e4dfec88419068d83b59976e3d875095e698cb13ae0c4244ec2);
  never modified.

## 7. Science preservation (PART 27)

verification/INVARIANT_CHECK.md: OVERALL PASS (22/22), including branch
identity at Ω*=1000: V_C(D_w*→0) = 0.3107266158 (|ΔV| = 2.4e-11, NOT the
0.467 phonon branch), 95/121, 71/121, max Δ_BC 9.48e-6, Δ_AC 0.334, gates
1.11e-9/3.27e-9, Δ_T 7.88e-5, BC ≤8.06e-6, P_w,A 0.991, Rayleigh rel err
1.04e-11. No headline value changed; no STOP triggered.

## 8. Package

- Path: FINAL_RESEARCH_PAPER_PACKAGE/ (this directory; 80 shipped files,
  ≈3.5 MB before archiving)
- Archive: FINAL_QC_SURFACE_WAVES_PAPER_PACKAGE_2026-09-07.zip (contains
  the manuscript PDF and the full source package; sha256 recorded in the
  delivery message and manifests/CHECKSUMS.sha256 covers the tree)
- Command: `python3 run_all.py` (modes: default reproduce / --check-only /
  --from-scratch)

## 9. Final Verdict

🟢 PASS — final paper, fully programmatic figure pipeline, and complete
reproducible package delivered; no further action required.
