# Paper 9 — FEM 3 style adaptation

## Main manuscript

Set `OVERLEAF/manuscript.tex` as the Overleaf root document. Keep the full `OVERLEAF/` directory when uploading: the manuscript reads section files, tables, vector figures, and `references.bib` by relative path.

The separate supplementary source is `OVERLEAF/Supplementary_Material.tex` and uses the same bibliography.

## Important status notes

- `OVERLEAF/manuscript.pdf` is a pre-revision PDF and does **not** reflect the current `.tex` source. Recompile the source before circulating or submitting a proof.
- The numeric JSON/YAML inputs used to regenerate the data-driven figures are not included in this package. The existing vector figure files were retained; their plotted curves were not redrawn. Figure 4 is not included by the active manuscript because its embedded callouts contain internal run/provenance labels. Its benchmark results and limitations are reported in Supplementary Material S2.
- The author/team name and generic affiliation in the front matter were retained from the supplied source and should be confirmed or replaced before submission. The raw solver outputs are not included; see the data-availability statement in `OVERLEAF/manuscript.tex`.

The before/after restructuring plan and implementation notes are in `MANUSCRIPT_RESTRUCTURING_PLAN.md`.
