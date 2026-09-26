# Provenance — Paper 10 Final Journal Package (integrated copy)

**Date of integration:** 2026-09-26
**Integrated by:** Arena.ai Agent session on branch `arena/01a0de21-bfs-fem-matlab`

## Source

| Item | Value |
| :--- | :--- |
| Origin branch | `arena/01a0dcde-bfs-fem-matlab` (repo `vipin-oss/BFS-FEM-MATLAB`) |
| Origin tip commit at integration | `65e7d915bc824681efa2921d5adefecf05b0f938` |
| Package frozen baseline (inside docs) | `f92e86462c42d9d4b7dce78309daac9ac53d7cef` |
| Artifact | `paper10/final_package/Paper10_Final_Journal_Package.zip` (7,209,144 bytes) |

## What was placed here

1. `Paper10_Final_Journal_Package.zip` — the authoritative archive, copied byte-for-byte from the origin branch blob.
2. `Paper10_Final_Journal_Package/` — the intact unpacked tree, extracted **directly from that zip** (74 files + 1 symlink `01_MANUSCRIPT/figures -> ../02_FIGURES`).

## Integrity verification performed

- SHA-256 audit of all 74 extracted files against `00_README/PACKAGE_MANIFEST.md`:
  **72/74 exact matches**.
  - `00_README/PACKAGE_MANIFEST.md` — expected mismatch (a manifest cannot contain its own hash).
  - `01_MANUSCRIPT/Paper10_Manuscript.pdf` — size matches manifest (3,414,879 B); hash differs, consistent with a PDF recompile after hashing.
- Zip blob size on origin branch matches: 7,209,144 bytes.

## Warning about the origin branch's loose tree

The **loose (unpacked) copy committed alongside the zip** on `arena/01a0dcde-bfs-fem-matlab`
(`paper10/final_package/Paper10_Final_Journal_Package/` at commit `65e7d91`) is **corrupted**:
several files are 0 bytes (e.g. `VERSION_AND_PROVENANCE.md`, `fig9_bandgap_summary.png`,
`PRODUCTION_BANDGAP_SUMMARY.csv`, `S1_results.json`) and several report pathological sizes
(≥ 2 GiB, e.g. `fig3_material_contrast.png`, `S7_results.json`).

**The zip in this directory is the authoritative artifact.** Do not re-copy the loose tree
from the origin branch; use the extraction stored here instead.

## Contents (see `Paper10_Final_Journal_Package/00_README/README.md` for full detail)

- `00_README` – manifest (SHA-256 for all files), provenance chain, package overview
- `01_MANUSCRIPT` – LaTeX source, 19-page PDF, references.bib, compile script
- `02_FIGURES` – 10 publication figures (300 DPI PNG)
- `03_SOURCE_CODE` – Python TMM solvers (`coupled10.py`, `antiplane.py`, `parameters.py`), production/validation scripts, unit tests
- `04_PRODUCTION_DATA` – 7 sweep families (36 cases, 17,747 modal records) + summaries
- `05_VALIDATION` – Papargyri-Beskou (2009) & Li (2016) benchmark results
- `06_AUDIT_RECORD` – Phase-4 audits, traceability matrix, pre-submission audit + corrections
- `07_REPRODUCIBILITY` – run order, environment (Python 3.11.2 / NumPy 2.4.6 / SciPy 1.17.1)
- `08_GIT_PROVENANCE` – frozen commit hash, log, status, file inventory
