# Paper 9 — FEM 3 style adaptation

## Main manuscript

Set `OVERLEAF/manuscript.tex` as the Overleaf root document. Keep the full `OVERLEAF/` directory when uploading: the manuscript reads section files, tables, vector figures, and `references.bib` by relative path.

The separate supplementary source is `OVERLEAF/Supplementary_Material.tex` and uses the same bibliography.

## Important status notes

- `OVERLEAF/manuscript.pdf` is the 24-page result of CI run `36237892487`; its final rendered layout was reviewed page-by-page. The checklist, including figure, table, heading, equation, and page-break checks, is `MANUSCRIPT_FINAL_PDF_CHECKLIST.md`.
- The active manuscript uses the requested `5p,twocolumn` hierarchy. Active figures and tables in Sections 2–7 are full-width floats. Figures 12 and 13 remain separate and full-size to keep the caption clear of the footer and preserve plot readability.
- The numeric JSON/YAML inputs used to regenerate the data-driven figures are not included in this package. Existing vector plots were retained without redrawing their curves. Twenty-four legend frames across twelve figures are placed below their axes, and the remaining explanatory key is in clear diagram whitespace; no legend covers plotted data. The canonical FEM_3-styled generators in `figures_gen/` use the same external placement; `OVERLEAF/gen/` retains the original reference generators. Figure 4 is not included by the active manuscript because its embedded callouts contain internal run/provenance labels. Its benchmark results and limitations are reported in Supplementary Material S2.
- The author/team name and generic affiliation in the front matter were retained from the supplied source and should be confirmed or replaced before submission. The raw solver outputs are not included; see the data-availability statement in `OVERLEAF/manuscript.tex`.

The before/after restructuring plan and implementation notes are in `MANUSCRIPT_RESTRUCTURING_PLAN.md`.
