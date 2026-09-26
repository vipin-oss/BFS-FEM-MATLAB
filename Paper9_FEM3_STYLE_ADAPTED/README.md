# Paper 9 — FEM 3 style adaptation

## Main manuscript

Set `OVERLEAF/manuscript.tex` as the Overleaf root document. Keep the full `OVERLEAF/` directory when uploading: the manuscript reads section files, tables, vector figures, and `references.bib` by relative path.

The separate supplementary source is `OVERLEAF/Supplementary_Material.tex` and uses the same bibliography.

## Important status notes

- `OVERLEAF/manuscript.pdf` is the pre-second-pass build until the branch's GitHub Actions TeX build completes. It is stale relative to the current `.tex` source and must not be circulated or submitted; the rebuilt PDF will be committed back to this branch by the workflow.
- The active manuscript uses the requested `5p,twocolumn` hierarchy. Active figures and tables in Sections 2–7 are full-width floats.
- The numeric JSON/YAML inputs used to regenerate the data-driven figures are not included in this package. Existing vector plots were retained without redrawing their curves; selected legends were moved into clear plot regions and remaining crowded keys use light translucent frames. Figure 4 is not included by the active manuscript because its embedded callouts contain internal run/provenance labels. Its benchmark results and limitations are reported in Supplementary Material S2.
- The author/team name and generic affiliation in the front matter were retained from the supplied source and should be confirmed or replaced before submission. The raw solver outputs are not included; see the data-availability statement in `OVERLEAF/manuscript.tex`.

The before/after restructuring plan and implementation notes are in `MANUSCRIPT_RESTRUCTURING_PLAN.md`.
