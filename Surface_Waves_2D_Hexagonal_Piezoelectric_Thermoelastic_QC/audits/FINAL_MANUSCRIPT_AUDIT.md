# FINAL_MANUSCRIPT_AUDIT.md

Audit of `manuscript/FINAL_MANUSCRIPT.tex` as shipped in this package
(polishing closure; science frozen per Task-15 scope).

## 1. Science-preservation check (PART 27)

Executed by `verification/verify_invariants.py` (machine check; full log in
`verification/INVARIANT_CHECK.md`). All headline values re-read from the
shipped raw data:

| Headline value | Required | Verified | Status |
|---|---|---|---|
| Δ_BC evidence points below floor | 95/121 | 95 | PASS |
| Δ_BC evidence @Ω*≥0.31622776602 | 71/121 | 71 | PASS |
| max Δ_BC | ≈9.48e-6 | 9.482871836095e-6 | PASS |
| max Δ_AC | ≈0.334 | 0.3336348457622 | PASS |
| gates C→A / C→B | 1.11e-9 / 3.27e-9 | 1.1097e-9 / 3.2659e-9 | PASS |
| max Δ_T | ≈7.88e-5 | 7.879368e-5 | PASS |
| phason-BC effect | ≤8.06e-6 | 8.060893e-6 | PASS |
| P_w,A(1e-3) | ≈0.991 | 0.9909460140495867 | PASS |
| Rayleigh rel. err | ≈1.1e-11 | 1.0391e-11 | PASS |
| branch identity @Ω*=1000 | V_C(D_w*→0)=0.3107266158, Δ=2.4e-11, NOT 0.467 | 0.3107266158152, Δ=2.36e-11 | PASS |
| Ω*δ* flatness (A/B/C) | flat | 1.989 / 1.292 / 1.292 | PASS |
| vP/v0, vS/v0, ε_Δ, V_A, V_B, quasi-static limits | frozen set | as in INVARIANT_CHECK.md | PASS |

No headline value changed → no STOP condition triggered.

## 2. Content checks

- Equations, constants, boundary conditions, nondimensionalisation,
  Models A/B/C, branch identities, resolution-floor arguments and
  conclusions: unchanged from the accepted manuscript (polishing only).
- "Resolution-resolvable region" phrasing kept; no phase-transition claims.
- 1e-16 dips retained, shaded, and explained as numerical cancellation
  reproduced at ~1e-9 — not deleted or smoothed.
- No Model-A clamped differences plotted; no fabricated curves or fits.
- Captions live ONLY in the .tex `\caption{}` commands; no caption/figure
  numbers inside PDFs. Fig. 1 remains a caption-free concept schematic.
- No invented authors, affiliations, funding, or conflict-of-interest text.
- Figure count: 11 (within 9–11). Page count: 29 (within 26–30, ~28 target).
  Tables: 3. Grayscale-legible line-style/colour language per style.py.
- Compilation: pdflatex, rerun loop until cross-references stabilise;
  0 errors, 0 undefined references (see REPRODUCTION_REPORT.md).

## 3. Data-provenance check

Every figure is regenerated from `results/raw/` by
`figures/make_all_figures.py`; grep of the script for validated
result values returns zero hand-typed hits (annotation strings are
data-formatted). Full mapping in `audits/FIGURE_DATA_TRACEABILITY.md`.
