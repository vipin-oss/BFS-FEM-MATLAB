# DATA_PROVENANCE.md

## Chain

solver source (`solver/`, record hash `8c0abbabe66776dd`) → drivers
(`drivers/study1_baseline.py`, `study2_friction_map.py`, `study3_thermal.py`,
`study_bc.py`, `roots_diag.py`) → raw datasets (`results/raw/`, 13 CSV +
2 NPZ + MANIFEST.md + chain_log.txt) → figures (`figures/make_all_figures.py`)
→ `figures/output/fig1..fig11.pdf` → manuscript.

## Raw data custody

- `results/raw/` files are BYTE COPIES from the accepted upstream package
  `archive/QC_First_Paper_FINAL_REPRODUCIBLE_PACKAGE_2026-09-06.zip`
  (SHA-256 `b817860569293e4dfec88419068d83b59976e3d875095e698cb13ae0c4244ec2`;
  development repo commit `ea257c9`).
- Per-file checksums: `results/manifests/RAW_DATA_CHECKSUMS.sha256`;
  upstream file list: `results/manifests/RAW_DATA_MANIFEST.md`.
- RULE: raw data are read-only downstream. Nothing in the figure/manuscript
  pipeline ever writes into `results/raw/`. Integrity is re-checked by
  `tests/V0/test_V0_integrity.py`.

## Regeneration (from scratch)

`python3 run_all.py --from-scratch` re-runs all five drivers and the V0–V5
validation suite from solver source (regenerates the same raw values within
documented floating-point reproducibility; validation gates enforce it).

## Derived data

There are NO intermediate processed files: `results/processed/` is empty by
design; every derived quantity is recomputed at plot time from raw data
(see `audits/FIGURE_DATA_TRACEABILITY.md`).
