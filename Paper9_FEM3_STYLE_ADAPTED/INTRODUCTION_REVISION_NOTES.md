# Phase 1 — Introduction revision and review status

**Status date:** 2026-09-26  
**Review branch:** `arena/01a0dbe8-bfs-fem-matlab`  
**Source:** the newer Paper 9 manuscript at `OVERLEAF/manuscript.tex` in the user-linked Paper 9 / FEM3-style package. `OVERLEAF/PAPER9_ORIGINAL_manuscript.tex` is preserved and was not used as the active source.

## Current deliverables

- `OVERLEAF/sections/sec01_intro.tex` — first-pass rewrite of the Introduction. It has **no table** and cites **50 distinct sources**. The Introduction discusses phononic-crystal foundations; local Mindlin Form-II strain-gradient elasticity; inertia-law distinctions; 1D and 2D size-dependent phononic-crystal studies; classical anisotropy/orientation work; the qualified research gap; the paper's contributions; and article organization.
- `OVERLEAF/references.bib` — merged bibliography with **50 entries** (the original 15 retained, plus 23 selected FEM3 references and 12 focused phononic-crystal references). The source still uses normal BibTeX keys; the manuscript remains editable/Overleaf-oriented.
- `preview/Introduction_Review_Preview.pdf` — a four-page, table-free reading proof of the revised Introduction followed by the 50 references in first-citation order.
- `preview/build_intro_review.py` — generator for that PDF proof. `preview/requirements-review.txt` lists its optional ReportLab dependency.

The old `OVERLEAF/tables/tab01_literature_positioning.tex` fragment remains in the package for now, but the revised Introduction does not input or include it.

## Validation performed

- Exactly **50 unique citation keys** occur in the revised Introduction.
- All 50 keys resolve in `references.bib`; the bibliography parses as **50 entries with no BibTeX-parser warnings**.
- A static scan of the manuscript plus table fragments found no undefined citation keys or unused bibliography entries.
- The review-PDF generator verifies the 50-key count, the availability of each citation entry, absence of an Introduction table/input, and the four contribution items before producing the PDF.
- The high-wavenumber shear phase-speed expression was checked against Appendix A and is written in the Introduction as
  \[
  v_{T,\infty}=\sqrt{\mu/\rho}\,l_{\mathrm{eff}}/(\sqrt{10}\,\ell_{\mathrm{i}}).
  \]
  It replaces an incorrect shorthand expression in the initial draft.

## PDF and build limitation

The sandbox has no available `pdflatex`, `bibtex`, `latexmk`, `xelatex`, `lualatex`, or `tectonic`; the prior system-package installation attempt could not reach Debian repositories. Therefore:

- `preview/Introduction_Review_Preview.pdf` is a **ReportLab-generated editorial reading proof**, not a native TeX compilation. It is clearly labeled as Introduction-only and not the full manuscript.
- `OVERLEAF/manuscript.pdf`, `OVERLEAF/PAPER9_ORIGINAL_reference_build.pdf`, `preview/index.html`, and the old compile diagnostics are **baseline/historical artifacts**, not proof of the revised Introduction. They have not been overwritten.
- The exact LaTeX formatting, `elsarticle-num` rendering, and final pagination still need a normal `pdflatex` + BibTeX build (for example in Overleaf).

## Review gate

This is the first-pass Introduction only. No later sections, tables, figures, or results have been revised in this phase. **Wait for the user's approval of the Introduction/PDF before proceeding with any later manuscript changes.**