# FINAL Package Audit — Paper9_FINAL_SOURCE_PACKAGE v1.0 (2026-09-25)

## 1. Source

- Repository: `vipin-oss/BFS-FEM-MATLAB`, branch `phase-1-symbolic`
- Commit: `0f1397b60f709641a0f3389f4ced9a704d61736c` (285 commits, clean tree)
- Method: `git archive HEAD paper9` extracted byte-identical into `PROGRAM/paper9/`
  (verified with `diff -r` against an independent extraction — zero differences)
- Governing spec at source: Blueprint v1.6 (`de46c3bb…58ff`); v1.5 (`b96c8e76…`)
  and v1.4 (`2ae0b1e8…`) preserved byte-identically inside the package

## 2. Package structure

```
Paper9_FINAL_SOURCE_PACKAGE/                     (ONE top-level folder)
├── README.md                  (AI-friendly guide + quick start + status)
├── REPRODUCIBILITY.md         (envs, commands, production config, checkpoints)
├── MANIFEST.md                (content files: type + purpose + status + sha256)
├── MANIFEST.sha256            (648 entries; `sha256sum -c` clean)
├── VERSION.txt                (package/source/manuscript/spec/validation state)
├── FINAL_PACKAGE_AUDIT.md     (this file)
├── PROGRAM/                   (608 files)
│   ├── run_all.py             (master entry point: verify/regen/full)
│   ├── requirements.txt       (pinned Python env, verified)
│   ├── README.md              (PROGRAM guide + scope + frozen list)
│   ├── output/README.txt      (runtime workspace note; shipped empty)
│   └── paper9/                (604 files, byte-identical to git archive)
└── OVERLEAF/                  (36 files)
    ├── manuscript.tex         (main file; 1 path edit vs repo ms.tex)
    ├── references.bib         (separate .bib; byte-identical to repo)
    ├── manuscript.pdf         (reference build from these exact sources)
    ├── sections/ (11)         (path edits only: 7 table + 14 figure paths)
    ├── tables/ (7)            (byte-identical to repo)
    ├── figures/ (14 PDFs)     (byte-identical to repo)
    └── README.md
```

ZIP: `Paper9_FINAL_SOURCE_PACKAGE.zip`, ~37 MB, 731 entries, `unzip -t` clean.
SHA-256 filled at final build (§11).

## 3. Inclusion audit (whole-tree survey before packaging)

- Implementation language: **Python 3 only** — zero `.m` files in the repo; the master
  plan records the Python-3 decision explicitly (no MATLAB licence). Entry point is
  therefore `run_all.py`, not `run_all.m`.
- Dependencies (import scan of all 141 `.py` files): numpy, scipy, matplotlib, sympy,
  mpmath, pillow, PyYAML, pytest — pinned in `requirements.txt` to the verified set
  (matches the original production run manifest: python 3.13.14, numpy 2.3.5, scipy 1.17.1).
- Randomness: none except fixed `arpack_v0_seed = 0` — deterministic end-to-end.
- Network: **zero** `http/github/urlopen/requests` references in any project code —
  fully offline-capable.
- No `__pycache__`, caches, autosaves, editor files, or temp files are tracked, so none
  are packaged. LaTeX aux files are git-ignored (never tracked).

## 4. OVERLEAF compile test (from the packaged folder, then from the ZIP)

- Command: `pdflatex → bibtex → pdflatex ×3` (TeX Live); every pass exit 0
- Result: **34 pages · Figures 1–14 · Tables 1–7 · 15 bibitems · 0 errors ·
  0 undefined references · 0 undefined citations · 0 missing files**
- 7 overfull / 3 underfull warnings — identical to the authoritative repo build (cosmetic)
- Extracted-text sha256 `239cc142…cea1a3` — **identical to the authoritative repo build**,
  proving the 22 mechanical path edits changed no manuscript content
- Every `\includegraphics` (14/14) and `\input{tables/…}` (7/7) resolves inside the folder

## 5. Reproducibility tests (clean-room: extracted ZIP, never the repo)

| Test | Command (in extracted copy) | Result |
|---|---|---|
| Integrity | `sha256sum -c MANIFEST.sha256` | **648/648 OK, 0 FAILED** |
| Verify | `PROGRAM/run_all.py verify` | env OK · layout OK · 14/14 checksums OK · **pytest 386 passed, 9 skipped, 4 deselected, 0 failed**, exit 0 |
| Regen figs/tabs | `PROGRAM/run_all.py regen` | 21/21 generators ran; **7/7 `.tex` + 3/3 PNG byte-identical; 14/14 PDFs content-identical** (byte drift = matplotlib timestamps only), exit 0; repeat run identical (idempotent) |
| Manuscript | OVERLEAF build (above) | 34 pp, text-identical to authoritative |
| Refusal | `run_all.py full` (no flag) | correctly refuses, exit 1 |
| Secrets scan | grep token/key patterns | **clean** |
| New-file paths | absolute-path grep over all 12 new packaging files | **clean** (24 pre-existing `/home` refs confined to `paper9/`, kept as documented history) |

About the 386 vs in-git 395: 4 tests require git history (exact node IDs deselected in
`run_all.py`) and 5 self-skip with "git history unavailable". All 9 pass in the git
clone; the deselect list is printed on every run. No git-dependent test was edited.
`full` recompute was NOT executed (multi-hour; forbidden to rerun here); its stages are
the project's own commands with package-relative checkpoint dirs, arg-parse tested only.

## 6. Figure audit

| Fig | Manuscript ref | File | Format | Generated by (data source) | OVERLEAF | PROGRAM | Verified |
|---|---|---|---|---|---|---|---|
| 1 | sec02 | fig01_ellipsoid_tensor.pdf | PDF | fig01…py ← params_master.yaml | ✅ | ✅ | regen TEXT-IDENTICAL |
| 2 | sec03 | fig02_lattice_ibz.pdf | PDF | fig02…py ← params_master.yaml | ✅ | ✅ | regen TEXT-IDENTICAL |
| 3 | sec04 | fig03_bfs_dof_bloch.pdf | PDF | fig03…py (pure schematic) | ✅ | ✅ | regen TEXT-IDENTICAL |
| 4 | sec05 | fig04_benchmark_validation.pdf | PDF | fig04…py ← B1/B3 TM engines (recomputed) | ✅ | ✅ | regen TEXT-IDENTICAL |
| 5 | sec05 | fig05_mesh_convergence.pdf | PDF | fig05…py ← p4b_5g_to_5i.json + rule_rfit_governing.json | ✅ | ✅ | regen TEXT-IDENTICAL |
| 6 | sec06 | fig06_caseH_dispersion.pdf | PDF | fig06…py ← p5_production_raw_mesh16.json | ✅ | ✅ | regen TEXT-IDENTICAL |
| 7 | sec06 | fig07_caseC_dispersion.pdf | PDF | fig07…py ← p11_caseC_raw.json | ✅ | ✅ | regen TEXT-IDENTICAL |
| 8 | sec06 | fig08_theta_sweep.pdf | PDF | fig08…py ← p5_production_raw_mesh16.json | ✅ | ✅ | regen TEXT-IDENTICAL |
| 9 | sec06 | fig09_ar_sweep.pdf | PDF | fig09…py ← p5_production_raw_mesh16.json | ✅ | ✅ | regen TEXT-IDENTICAL |
| 10 | sec06 | fig10_design_map_3d.pdf | PDF | fig10…py ← p5_production_raw_mesh16.json | ✅ | ✅ | regen TEXT-IDENTICAL |
| 11 | sec06 | fig11_polar_map_regimes.pdf | PDF | fig11…py ← p5_production_raw_mesh16.json | ✅ | ✅ | regen TEXT-IDENTICAL |
| 12 | sec07 | fig12_ifc_wave_steering.pdf | PDF | fig12…py ← p5_production_raw_mesh16.json | ✅ | ✅ | regen TEXT-IDENTICAL |
| 13 | sec07 | fig13_energy_microinertia.pdf | PDF | fig13…py ← p5_production_raw_mesh16.json | ✅ | ✅ | regen TEXT-IDENTICAL |
| 14 | sec07 | fig14_s7_steering_sweep.pdf | PDF | fig14…py ← p12b_s7_theta_sweep_mesh16.json | ✅ | ✅ | regen TEXT-IDENTICAL |

PNG duplicates (`fig04/fig07/fig14.png`) are audit-use only in `PROGRAM` (regen
BYTE-IDENTICAL) and intentionally absent from `OVERLEAF` (manuscript cites PDFs only).
No supplementary figures exist. No figure was edited, re-rendered for aesthetics, or
replaced: production data → manuscript bytes is the shipped chain, verified above.

## 7. Data audit

- **AUTHORITATIVE production:** `results/raw/p5_production_raw_mesh16.json` (+`.npz`
  grids), mesh-8 pair, `p12b_s7_theta_sweep_mesh16.json`, `p11_caseC_raw.json`,
  `table5_gap_summary_mesh16.json`, `p5_production_highlights_mesh16.json` — all shipped,
  checksummed (§5 spot-check 14/14 OK), never edited.
- **Intermediate:** pilot raw/summary, mesh-8 grids, P11D registries, convergence JSONs —
  shipped under `results/raw/` + `audit/evidence/` as run history.
- **Validation:** B2 registry, B3 pinned run, P12S record/overlays, Layer-3 scripts —
  shipped; statuses frozen (B1 PASS; B2/B3 NOT_VALIDATED; null ×3).
- **Figure/table-gen data:** §6 "Generated by" column — all present in-package.
- **Temporary/cache:** none tracked, none shipped. `PROGRAM/output/` is the only runtime
  location (shipped empty).
- No numerical value, threshold, gate status, or benchmark classification was changed by
  packaging (proven by §5 checksums + the byte-identical `paper9/` tree).

## 8. Packaging fixes made during testing (audit trail, not science)

1. `run_all.py:_backup` — first version collided `figures/out` + `tables/out` on basename
   `out`; fixed to `figures_out/`/`tables_out` (+ matching compare path). Found by regen test.
2. `run_all.py` deselects — first version deselected a whole parametrized test (8 nodes,
   hiding 4 passing params); narrowed to the 4 exact failing node IDs. Found by verify test.
3. Manifest generator — first version hashed the human manifest into itself (never converged);
   manifests now exclude self-references. Found by `sha256sum -c`.
4. No project file was touched by any fix — all three were in new packaging code.

## 9. Intentionally excluded

| Item | Why |
|---|---|
| `.git/` (history) | ZIP cannot carry it; consequence documented (4 deselects + 5 skips) |
| `Research Policy…docx` (repo root) | unrelated university admin document; zero references from the project |
| `.gitignore` | git-only; meaningless in a ZIP |
| `manuscript.bbl` / aux files | regenerated by every build; only the reference `manuscript.pdf` is kept |
| PNG figure duplicates (OVERLEAF only) | manuscript cites PDFs; PNGs retained in `PROGRAM` |
| `PROGRAM/output/` contents | runtime workspace by design (shipped empty) |

## 10. Remaining limitations (genuinely unresolvable in a ZIP)

1. 9 suite tests need git history (4 deselected, 5 self-skip) — all pass in the clone.
2. Regenerated PDFs are content-identical, not byte-identical (timestamps).
3. P12S re-execution needs external digitised panels (`/home/user/p12s_extract`) — shipped
   P12S record + overlays are authoritative instead.
4. `full` recompute not executed during packaging (compute cost + standing instruction).
5. `sources/` PDFs are third-party copyrighted papers, included (as in the repo) so every
   pinned hash resolves offline; redistribution rights remain with the publishers.
6. Historical absolute paths (`run_mesh16_pipeline.sh` checkpoints, two `p12c_*64` path
   inserts, audit probes) are preserved verbatim as history; `run_all.py` routes around
   them with relative paths instead of editing them.
7. `verify` must run BEFORE `regen` on a fresh copy (§5 row 4): one project test pins
   fig05's shipped bytes, so verify-after-regen shows that 1 expected, reversible failure.

## 11. Final build record (2026-09-25)

- Final ZIP: `Paper9_FINAL_SOURCE_PACKAGE.zip`, one top folder, **731 entries**
  (650 files + 81 directories), ~37 MB, `unzip -t` clean. (The ZIP's own SHA-256 is
  stated in the delivery report, not here — a file cannot contain its container's hash.)
- 12-point clean-room on the final ZIP (fresh extraction, `verify` before `regen`):
  P1 one top folder · P2 649/649 checksums · P3 verify exit 0 (386/9/0) ·
  P4 regen exit 0 (14/14 TEXT-IDENTICAL, 10 BYTE-IDENTICAL) · P5 TeX 4 passes exit 0 ·
  P6 34 pages · P7 14/14 figures · P8 Tables 1–7 · P9 15 bibitems · P10 0/0/0/0 ·
  P11 extracted-text sha `239cc142…cea1a3`, identical to authoritative ·
  P12 no `.git`, no network use, no new-file absolute paths.
- Statuses reconfirmed at final build: B1 PASS; B2/B3 NOT_VALIDATED; null ×3;
  PCR1–PCR8 PASS; G1/G2/G3 MET; G4 NOT MET; P13 BLOCKED. Packaging changed no gate.
