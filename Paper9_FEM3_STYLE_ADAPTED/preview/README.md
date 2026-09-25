# HTML/MathML preview of the adapted manuscript

`index.html` is a self-contained, viewable render of the full adapted manuscript
(all 11 sections + 7 tables), produced with the `@arena.ai/faster-latex`
Rust/WASM renderer (HTML + MathML Core):

- Citations are numbered `[1]…[15]` by **first citation**, matching the
  `elsarticle-num` convention of the FEM₃ style reference (and equal to Paper9's
  original `unsrt` numbering). They resolve against `references.bbl`, a
  preview-only `.bbl` built from the byte-identical `OVERLEAF/references.bib`
  (plain-text DOI; not part of the Overleaf package).
- `figure_png/*.png` are the 14 FEM₃-style restyled figures rasterized at 160 dpi.
- elsarticle's class-level frontmatter macros (`\corref/\cortext/\keyword/\sep`)
  and `\subequations` are shimmed for the HTML engine only; the real LaTeX deck in
  `OVERLEAF/` uses genuine elsarticle.

**Live view:** served at `preview/index.html` (port 8618) via a static file server.

**Regenerate:** requires the `faster-latex` package plus the flatten/shim/bbl
steps (intermediate `flat.tex`, `flat_out.html`, `references.bbl`). The
authoritative source for all content is `OVERLEAF/` — this preview is a fidelity
aid, **not** a substitute for a real `pdflatex + bibtex` run on Overleaf.
