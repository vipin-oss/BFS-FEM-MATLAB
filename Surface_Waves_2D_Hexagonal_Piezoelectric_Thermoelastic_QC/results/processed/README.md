# results/processed/

This directory is intentionally EMPTY in the shipped package.

No derived/processed dataset exists between `results/raw/` and the figures:
every derived quantity (branch differences, gate ratios, chi = Omega*/D_w*
relabelling, log10 floors) is recomputed in-place by
`figures/scripts/make_all_figures.py` directly from the raw CSV/NPZ files.
Keeping the provenance chain raw -> script -> PDF (no intermediate file)
is what guarantees traceability; see audits/FIGURE_DATA_TRACEABILITY.md.
