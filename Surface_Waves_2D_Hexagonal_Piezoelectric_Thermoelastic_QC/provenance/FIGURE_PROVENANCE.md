# FIGURE_PROVENANCE.md

Every figure is program-generated from `results/raw/` by
`figures/make_all_figures.py` (styling: `figures/style.py`; historical
upstream script preserved at `figures/scripts/make_figures_original_package.py`).

- Command: `python3 figures/make_all_figures.py` (or `python3 run_all.py`,
  which also refreshes the journal copies in `manuscript/figures/`).
- Figure→data mapping: `audits/FIGURE_DATA_TRACEABILITY.md`; per-figure
  sizes/topics: `manifests/FIGURE_MANIFEST.md`.
- fig1.pdf (schematic) is code-drawn vector art — no external artwork, no
  bitmap sources (`figures/source/` is intentionally empty).
- No hand-typed result values: annotation strings are data-formatted
  (`"%.12f" % ana` etc.); grep of the script for validated result values
  returns zero hits. Hard-coded non-data constants (axis limits, colours,
  1e-16 display clip, grid-row indices, legacy 0.934208 record) are
  documented in the traceability audit.
- Regeneration is content-deterministic: clean-room runs produce
  stream-identical PDFs (only embedded timestamps differ) — verified
  2026-09-07.
- Captions exist ONLY in `manuscript/FINAL_MANUSCRIPT.tex` `\caption{}`
  commands; figure files carry axes, ticks, legends, panel letters and short
  scientific annotations only.
- Spike/anomaly handling (nothing smoothed, deleted, or clipped):
  `audits/SPIKE_AND_ANOMALY_AUDIT.md`.
