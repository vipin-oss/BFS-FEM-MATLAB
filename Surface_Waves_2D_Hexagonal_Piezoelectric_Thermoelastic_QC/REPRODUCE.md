# REPRODUCE.md — exact reproduction instructions

## 0. Requirements

- Python 3.9+ (developed on 3.13; only numpy + matplotlib + pypdf used)
- `pip install -r requirements.txt` (or `conda env create -f environment.yml`)
- LaTeX for the manuscript: `texlive-latex-base`, `texlive-latex-recommended`,
  `texlive-latex-extra`, `texlive-fonts-recommended` (Debian/Ubuntu names).
  Without LaTeX, run_all.py still does env check + invariants + figures and
  skips compilation.

## 1. Default reproduction (from shipped raw data) — recommended

```bash
python3 run_all.py
```

Steps: environment check → science-preservation invariants (must PASS 22/22)
→ regenerate all 11 figures from `results/raw/` → sync journal figure copies
→ compile manuscript (pdflatex, rerun until cross-references stabilise) →
write `REPRODUCTION_REPORT.md`.

Expected output: `REPRODUCTION: PASS`; report shows
`29 pages, 0 errors, 0 LaTeX warnings, 0 undefined refs; figures 11; tables 3`.

## 2. Science gate only (fastest check after any edit)

```bash
python3 run_all.py --check-only      # or: python3 verification/verify_invariants.py
```

Expected: 22 × [PASS], `OVERALL: PASS`, exit code 0. Any failure = the
accepted baseline changed → STOP (do not proceed; see PART-27 rule in
audits/FINAL_MANUSCRIPT_AUDIT.md).

## 3. Full production from solver source (slower)

```bash
python3 run_all.py --from-scratch
```

Runs `drivers/study1_baseline.py`, `study2_friction_map.py`,
`study3_thermal.py`, `study_bc.py`, `roots_diag.py`, then `tests/V*/`.
Validation gates (V0–V5) enforce agreement with the accepted raw data.

## 4. Individual pieces

- Figures only: `python3 figures/make_all_figures.py`
  (writes `figures/output/fig1.pdf … fig11.pdf`; deterministic content —
  only PDF timestamps vary between runs)
- One test: `python3 tests/V2/test_V2_elastic_limit.py` (etc. for V0–V5)
- Manuscript only: `cd manuscript && pdflatex FINAL_MANUSCRIPT && bibtex
  FINAL_MANUSCRIPT && pdflatex FINAL_MANUSCRIPT && pdflatex FINAL_MANUSCRIPT`

## 5. Integrity checks

```bash
sha256sum -c manifests/CHECKSUMS.sha256          # every shipped file
(cd results/raw && sha256sum -c ../manifests/RAW_DATA_CHECKSUMS.sha256)
```

## 6. Troubleshooting

- `pdflatex: MISSING` → install the texlive packages above; figures and
  invariants still run.
- Matplotlib backend errors on headless machines: the script forces the
  `Agg` backend; none expected.
- A figure differs visually after regeneration on a different matplotlib
  version: compare content, not bytes (fonts/timestamps vary); the data
  layer is version-independent (pure CSV/NPZ reads).
- If `verify_invariants.py` fails: DO NOT edit the checks or the data.
  Inspect what changed (git-style diff against `archive/` snapshots),
  because every headline value is part of the accepted baseline.
