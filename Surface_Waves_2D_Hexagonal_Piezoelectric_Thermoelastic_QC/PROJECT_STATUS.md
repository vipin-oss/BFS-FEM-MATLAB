# PROJECT_STATUS.md — state at GitHub archival (2026-09-07)

## Status: COMPLETE AND ACCEPTED (science frozen)

Research Paper 1 is finished through final packaging and GitHub archival.
The scientific and computational baseline is ACCEPTED; no open scientific
questions remain in scope. Remaining work is submission logistics only.

## Manuscript

- `manuscript/FINAL_MANUSCRIPT.{tex,bib,pdf}` — 29 pages, 11 figures,
  3 tables; compilation: 0 errors, 0 LaTeX warnings, 0 undefined
  references, 0 undefined citations (rerun-stable).
- Journal-source figure copies in `manuscript/figures/` (auto-synced by
  run_all.py). No supplementary material.

## Final validated results (all re-checked at runtime)

Rayleigh rel. err 1.04e-11; quasi-static limits 0.62145378 / 0.93260276;
model gates 1.11e-9 / 3.27e-9; max Δ_BC 9.48e-6 with 95/121 production
points below the benchmarked resolution floor (71/121 evidence at
Ω* ≥ 0.31622776602); Δ_AC ≈ 0.334 (resolvable); max Δ_T 7.88e-5;
phason-BC effect ≤ 8.06e-6; P_w,A ≈ 0.991; Ω*δ* flat (1.99 / 1.29 / 1.29);
branch identity at Ω*=1000: V_C(D_w*→0) = 0.3107266158, |ΔV| = 2.4e-11 —
the incorrect ~0.467 phonon branch is NOT selected.

## Verification

- `verification/verify_invariants.py`: **22/22 PASS** (latest run in
  verification/reports/INVARIANT_CHECK.md).
- Validation suite V0–V5 present (tests/V*/) with logs in
  results/validation/.
- Solver status: production, unmodified branch tracker; record hash
  `8c0abbabe66776dd`.

## Figures

- 11 scientific figures; PDF count: 11 (`figures/output/figN.pdf`,
  authoritative); EPS count: 11 (`figures/output/FigNN.eps`, pdftops
  conversions; Fig10 contains one matplotlib-embedded raster colour-mesh
  layer, identical in PDF and EPS); source scripts: 2
  (`make_all_figures.py` + `style.py`) + 1 historical upstream script.
- Regeneration is content-deterministic (clean-room verified).

## Literature

- BibTeX entries: 47 (`literature/all_references.bib`); reference PDFs
  redistributed: 0 (copyright; availability status in
  `literature/MISSING_REFERENCE_PAPERS.md`); style sample: 1 (author-provided).

## Reproduction

- `python3 run_all.py` — latest result: REPRODUCTION: PASS (see
  REPRODUCTION_REPORT.md and audits/CLEAN_ROOM_REPRODUCTION_REPORT.md).

## Fingerprints

- Upstream accepted package (raw-data source):
  `QC_First_Paper_FINAL_REPRODUCIBLE_PACKAGE_2026-09-06.zip`
  SHA-256 `b817860569293e4dfec88419068d83b59976e3d875095e698cb13ae0c4244ec2`
- Task-15 package:
  `FINAL_QC_SURFACE_WAVES_PAPER_PACKAGE_2026-09-07.zip`
  SHA-256 `1c7c55d7672ecf8d9229a44a2b68b0dfe2348e7305042f11a9e87036e8042fe6`
- Final research-archive ZIP (kept outside git; equals this tree + the two
  ZIPs above): `FINAL_QC_SURFACE_WAVES_RESEARCH_ARCHIVE_2026-09-07.zip`
  SHA-256 `e6bc9fffe8e6e30efa2635bf7dd26719924ced7ea7c6206272507505de15800f`
- Development-repo git provenance: `ea257c9` (study1_surface_waves).

## GitHub

- Repository: https://github.com/vipin-oss/BFS-FEM-MATLAB (branch `main`)
- Project directory: `Surface_Waves_2D_Hexagonal_Piezoelectric_Thermoelastic_QC/`
- Commit SHA: see `git log` (recorded in the commit immediately following
  this file's creation; no credentials in history).

## Deliberately excluded from git (and why)

- The three ZIP archives (repo tracks `*.zip` via LFS; they are byte
  duplicates of this unpacked tree — SHAs recorded above and in
  `archive/README.md`; integrity guaranteed by `manifests/CHECKSUMS.sha256`).
- LaTeX build artifacts (.aux/.log/.out/.bbl/.blg) and `__pycache__`
  (regenerable; see .gitignore — validation evidence logs are kept).

## Remaining (submission logistics only)

Author/affiliation/funding/COI block (intentionally not invented);
deboissieu2012 page range (camera-ready flag); re-verify journal metrics
(AMM-Engl. Ed. JIF 4.9 primary; Acta Mechanica JIF 4.0 backup).
