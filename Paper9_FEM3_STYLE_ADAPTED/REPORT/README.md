# Transformation Report — Paper9 → `Paper9_FEM3_STYLE_ADAPTED`

**Target package:** `/Paper9_FEM3_STYLE_ADAPTED/`
**Reference style:** `FEM_3` (FEM₃ reference paper)
**Content source of truth:** `Paper9_FINAL_SOURCE_PACKAGE` (Paper9)
**Working branch:** `arena/01a0d8f7-bfs-fem-matlab`
**Frozen originals:** the authoritative Paper9 package and PDF remain **untouched**;
byte-identical copies are preserved inside this package under `ORIGINAL/` and
`OVERLEAF/PAPER9_ORIGINAL_*` (see F).

---

## A. What was changed (presentation only)

1. **Manuscript shell** — `OVERLEAF/manuscript.tex` was rewritten as a FEM₃‑style
   document:
   - `\documentclass[preprint,12pt]{elsarticle}` (identical to FEM₃'s source class),
     replacing Paper9's `article` 11pt.
   - FEM₃ geometry `\usepackage[a4paper,margin=1in]{geometry}`.
   - elsarticle `frontmatter` with `\title`, `\author`/`\corref`/`\cortext`,
     `\address`, `\begin{abstract}` and `\begin{keyword}` … `\sep` … `\end{keyword}`,
     and `\journal{International Journal of Mechanical Sciences}` — the exact
     frontmatter constructs of the FEM₃ reference.
   - Citation/bibliography style switched from `unsrt` to **`elsarticle-num`**
     (FEM₃'s numeric-by-first-citation convention).
   - Paper9's `Highlights`, `Data availability`, `Conflict of interest` and
     `Acknowledgments` blocks are retained verbatim.

2. **Preamble of styles/packages** — reduced to the FEM₃ working set extended only
   by packages the *byte‑identical* Paper9 sections demonstrably require:
   `tabularx`, `ragged2e` (for `\newcolumntype Y/L`), `enumitem` (sections use
   `\begin{enumerate}[label=…]`), `subcaption`, `[table]{xcolor}`, `siunitx`.
   The duplicated `\usepackage{xcolor}` and the unused `longtable`/`xltabular`
   from intermediate revisions were removed.

3. **Custom math macros** (`\bmx … \bmL, \barw, \bark, \ellbar, \lbar, \dif, \iu`)
   are preserved exactly as in Paper9 (they are scientific notation, not decoration).

4. **Front-matter text (title/abstract/keywords)** is Paper9's exact wording, placed
   into FEM₃'s layout. Nothing was rewritten for the style change.

5. **Figures** — all 14 Paper9 figures were regenerated in FEM₃'s graphical language
   (see C). The files in `OVERLEAF/figures/` are new PDFs; the underlying data,
   curves, and numerical values are unchanged.

6. **Tables** — the 7 table fragments are reused **byte‑identically** (see D);
   they are placed in `OVERLEAF/tables/` so the manuscript's `\input{tables/…}`
   resolves. (Paper9's fragments already use `booktabs`; no content change was
   needed or made.)

7. **Bibliography file** — `OVERLEAF/references.bib` is byte‑identical to the
   authoritative Paper9 `references.bib` (original keys). The *only* change is the
   `\bibliographystyle` line (unsrt → elsarticle-num); see D for the numbering
   equivalence and the numeric preview map.

---

## B. What was deliberately NOT changed (scientific content confirmation)

Confirmed unchanged, byte-for-byte where text was copied:

- **All 11 section files** (`sec01…sec09`, `appA`, `appB`) in
  `OVERLEAF/sections/` are **byte‑identical** to the authoritative Paper9
  `OVERLEAF/sections/`.
- **All 7 table fragments** (`OVERLEAF/tables/`) and the **bibliography**
  (`OVERLEAF/references.bib`) are likewise byte‑identical.
- **Cryptographic proof (final audit):** every one of these 19 files was
  verified `sha256`-identical against the authoritative package's untampered
  `ORIGINAL/MANIFEST.sha256` (extracted from the frozen
  `ORIGINAL/Paper9_FINAL_SOURCE_PACKAGE.zip`). **Result: 19/19 IDENTICAL.**
  The frozen `OVERLEAF/PAPER9_ORIGINAL_manuscript.tex` is also verified
  identical to the authoritative `OVERLEAF/manuscript.tex`; only the adapted
  `OVERLEAF/manuscript.tex` and the 14 restyled figure PDFs differ, by design.
- **Every equation, derivation, boundary condition, parameter, algorithm and
  numerical result** — including the scientific anchors listed in E.
- **Authors, title, journal, scope, contributions, novelty and conclusions.**
- **All 15 references** (no entry added, removed, or altered in any bibliographic
  field — only the internal `\cite` key naming convention is discussed, and even
  that was ultimately left untouched; see D).
- **All 14 figure curves, datasets, branches and parameters.** Only the plotting
  backend styling was changed (C), never the computed values.
- **The 7 tables** are byte‑identical to the authoritative table fragments.
- **The physical model is untouched.** FEM₃'s (different) constitutive model and
  equations were **not** imported at any point, per the standing directive that
  Paper9 is scientifically authoritative.

---

## C. Figure / graph changes

A shared style module `figures_gen/fem3style.py` encodes the FEM₃ visual language
extracted from the reference (EPS font/line probes + rendered pages):

- **Fonts:** STIX-General (a Times-family) for *both* text and maths
  (`mathtext.fontset='stix'`), matching FEM₃'s Times-family figures.
- **Grid:** soft dashed gray (0.5 … 0.8) `linestyle='--'`, `linewidth≈0.7`,
  `alpha≈0.5`, `zorder=0` (replaces Paper9's dotted `ls=':'` grids).
- **Axes:** thin box frames (`spines.linewidth=0.8`–`1.0`), modest tick label
  sizes (8–9 pt), labelled panel titles `(a)`/`(b)`.
- **Palette:** FEM₃'s restrained set — `#1f77b4` blue, `#d62728` red,
  `#2ca02c` green, `#ff7f0e` orange, `#9467bd` purple — with restrained line
  widths (≈1.5 pt) and small markers.
- **Legends:** thin-edged framed boxes (`framealpha≈0.9`, edge `0.35`, lw 0.8).
- **Layout:** FEM₃'s wide, flat single-column panels; `bbox_inches='tight'`;
  two-panel figures kept on one row.

Figure-by-figure (all keep their Paper9 data sources):

| Fig | Content | Styling applied |
|----|---------|-----------------|
| 01 | Microstructural ellipsoid / L(θ) tensor | STIX fonts, dashed grid, framed axes, FEM₃ palette |
| 02 | Direct lattice + BZ/IBZ/symmetry path | same; BZ fills softened |
| 03 | BFS 32-DOF element + Bloch coupling | label box + FEM₃ legend conventions |
| 04 | B1/B3 transfer-matrix benchmark (serif, wide) | kept wide/serif; FEM₃ palette/legend/grid; audit notes retained |
| 05 | Mesh convergence + observed rate | FEM₃ palette, log-log grid, anchored floor/CI text |
| 06 | Case H band structure Γ–X–M–Γ | FEM₃ palette, dashed gray grid |
| 07 | Case C dispersion + gap tuning (twin axis) | FEM₃ palette, hatched gap band, legend merged from twin axes |
| 08 | θ-sweep at AR=5 | FEM₃ palette/markers |
| 09 | AR-sweep at θ=45° | FEM₃ palette/markers |
| 10 | (θ,AR) design map 3D + contours | **viridis retained** — it is the Paper9 value encoding, not decoration |
| 11 | Polar regimes + Sθ sensitivity | **plasma retained** (value encoding); FEM₃ ambient styling |
| 12 | IFC steering δ(φ) + |v_g| | FEM₃ palette/markers, framed axes |
| 13 | Energy partition + high-k phase velocity | FEM₃ palette, log grid |
| 14 | S7 steering sweep (twin axis) | FEM₃ palette; open/solid marker convention retained for the mirror-symmetry proof |

**Data-identity verification (performed):**
- Every restyled generator resolves the **same data files/keys** as its Paper9
  original (`params_master.yaml`, `p5_production_raw_mesh16.json`,
  `p11_caseC_raw.json`, `p12b_s7_theta_sweep_mesh16.json`,
  `p4b_5g_to_5i.json`, `rule_rfit_governing.json`, solver modules) — audited via
  a source-diff of data references (only fig01/fig02 showed a tooling regex
  false-positive; both open the identical `params_master.yaml`).
- Original generators are preserved untouched as `OVERLEAF/gen/*.py` for
  reference.

---

## D. Reference / citation changes

- **Active bibliography:** `OVERLEAF/references.bib` is **byte‑identical**
  (SHA-256 `e585c875…568`) to the authoritative Paper9 bibliography, original
  keys intact. No bibliographic field changed.
- **Style:** `\bibliographystyle{unsrt}` → `\bibliographystyle{elsarticle-num}`,
  FEM₃'s citation convention. `elsarticle-num` numbers by **first citation**, and
  because the section files are byte‑identical, Paper9's first-citation order is
  unchanged — so the numeric labels equal Paper9's original `unsrt` numbering.
- **First-citation numbering map** (verified programmatically from section
  source, and against the FEM₃ build where [1] is the first-cited work):

  | # | key (unchanged) | | # | key (unchanged) |
  |--|-----------------|-|--|-----------------|
  | [1] | kushwaha1993 | | [9] | zhanwei2010 |
  | [2] | mindlin1964 | | [10] | zhengwei2009 |
  | [3] | toupin1962 | | [11] | hosseinizhang2021 |
  | [4] | mindlineshel1968 | | [12] | li2023anchorA |
  | [5] | askesaifantis2011 | | [13] | li2024anchorB |
  | [6] | polyzosfotiadis2012 | | [14] | mishra2026anchorC |
  | [7] | papargyribeskou2009 | | [15] | bfs1965 |
  | [8] | liweizhou2016 | | | |

- **Correction to an earlier working decision:** an intermediate step had
  renamed bib keys to `ref1…ref15`. This was **reversed** — renaming keys is
  unnecessary for the style change (elsarticle-num numbers by citation order, not
  by key), risks key/`\cite` divergence, and breaks byte-identity of the
  bibliography. The numeric-keyed file is retained only as a labelled *preview
  artifact*: `tables/references_numeric.bib` (with `tables/bib_key_map.txt`).
- **Reference/metadata integrity:** no reference was added, removed or altered;
  the count stays 15 (per the directive not to match FEM₃'s count by deleting
  valid entries).
- **Cite-key audit:** all 15 `\cite` keys used in the manuscript+tables resolve
  to bib entries, and all 15 bib entries are cited (no dangling cites, no orphans).

---

## E. Compilation status

**Honest status: this sandbox has no working TeX toolchain, so a native PDF
compile was not possible and is not claimed.** This was established earlier and
not re-attempted: `apt` TeX installs are blocked; CTAN/GitHub release-asset
downloads are blocked; npm `texlive@1.2.0` lacks required packages; native
Tectonic binaries fail on host glibc 2.36 / missing `libgraphite2.so.3`.
No "adapted PDF" is therefore shipped.

**What replaces the compile here (all run and passing):**

1. **`faster-latex` (Rust/WASM) HTML+MathML render of the full assembled
   manuscript** — all 11 sections + 7 tables inlined, elsarticle frontmatter
   shimmed for the HTML engine, and a hand-built `.bbl` companion
   (`preview/references.bbl`, plain DOI, first-citation numbering). Result:
   - **0 undefined references, 0 undefined citations**; 1289 MathML formulas,
     94 display-equation blocks rendered.
   - Live preview served at **`preview/index.html`** (see §G) with the restyled
     figures rasterized to PNG.
   - Note: the HTML engine does not `\usepackage` elsarticle's class-level
     frontmatter macros, so `\corref/\cortext/\keyword/\sep/\subequations` are
     shimmed/no-ops there. This is purely a fidelity preview, not a substitute
     for a real pdflatex+bibtex run on Overleaf.

2. **Static source audit of the real LaTeX deck** (what Overleaf will compile):
   - **Figures:** 14/14 `figure` environments balanced; 14/14 `\includegraphics`
     targets exist in `OVERLEAF/figures/`; no missing, no stray file.
   - **Tables:** 6 `table`+`table*` floats balanced plus `tab03`'s internal
     `table*`; all 7 `\input{tables/…}` targets present, byte‑identical to source
     of truth.
   - **Cross-references:** 111 defined `\label`s; all 44 distinct
     `\ref`/`\eqref` targets resolve (0 undefined).
   - **Citations:** 15 keys used; 15 bib entries; 0 undefined, 0 unused.
   - **Equations:** every equation/align/subequations environment balanced per
     section.

3. **Overleaf readiness** — the `OVERLEAF/` folder is a self-contained project:
   `manuscript.tex` + `sections/` + `tables/` + `figures/` (directory-independent
   relative `\includegraphics` + `\input` paths). Upload
   `Paper9_FEM3_STYLE_ADAPTED/OVERLEAF` to Overleaf, select
   `pdflatex + BibTeX`, and it will resolve (subject to a normal journal-style
   float-placement pass, as with the original).

**Expected real-LaTeX notes (not errors, but flagged for the compiler pass):**
- `tab03_anchor_errors.tex` is a `table*` fragment included inside sec05's text
  (Paper9 authored it that way; it compiles as a full-width float).
- Paper9's own section text is a two-column-ready style but FEM₃'s *source* uses
  single-column `preprint`; wide figures use `figure*`/`table*`. This mirrors the
  original package's structure and is left as Paper9 wrote it.

---

## F. Exact paths of modified / new files

New/changed inside **`/Paper9_FEM3_STYLE_ADAPTED/`** (relative paths):

```
OVERLEAF/manuscript.tex                     NEW      FEM_3-style shell (elsarticle frontmatter, preamble)
OVERLEAF/references.bib                     RESTORED byte-identical authoritative bibliography (original keys)
OVERLEAF/sections/{sec01…sec09,appA,appB}.tex  COPIED byte-identical (11 files)
OVERLEAF/tables/tab01…tab07_*.tex           COPIED byte-identical from PROGRAM/paper9/tables/out/
OVERLEAF/figures/fig01…fig14_*.pdf          NEW      restyled FEM_3-style figures (14 PDFs)
OVERLEAF/gen/fig01…fig14_*.py               COPIED  original Paper9 generators (reference, untouched)
OVERLEAF/PAPER9_ORIGINAL_manuscript.tex     FROZEN  authoritative Paper9 manuscript
OVERLEAF/PAPER9_ORIGINAL_reference_build.pdf FROZEN authoritative Paper9 reference PDF

figures_gen/fem3style.py                    NEW      FEM_3 figure-style module
figures_gen/fig01…fig14_*.py                NEW      restyled generators (14)

tables/build_tables.py                      NEW/UPD  writes OVERLEAF/tables/ + working copies
tables/build_references.py                  NEW/UPD  writes active bib + numeric preview + key map
tables/tables_rebuilt/*.tex                 WORKING copies (byte-identical to OVERLEAF/tables)
tables/references_numeric.bib               PREVIEW  ref1…ref15 keyed bibliography (report only)
tables/bib_key_map.txt                      MAP      [n] <-> original key <-> ref<n>

ORIGINAL/Paper9_FINAL_SOURCE_PACKAGE.zip    FROZEN  authoritative Paper9 (untouched original)
ORIGINAL/references_original_keys.bib       FROZEN  authoritative bibliography (byte-identical)

preview/index.html                          NEW      rendered manuscript preview (citations + bibliography resolved)
preview/figure_png/fig01…fig14_*.png        NEW      rasterized preview renders of the restyled figures
preview/flat.tex, flat_out.html, references.bbl  PREVIEW-only artifacts

PROGRAM/paper9/                             COPIED  authoritative 604-file program tree (source of truth,
                                                     unused by Overleaf but required by figures_gen/ + tables builders)
```

Files intentionally left untouched in the repository: the authoritative
`Paper9_FINAL_SOURCE_PACKAGE` content (frozen in `ORIGINAL/`) and everything
outside the adapted package.

---

## G. Final compiled PDF

No locally compiled PDF is available (see E for the honest toolchain status).

- **Reference build to compare against:** `OVERLEAF/PAPER9_ORIGINAL_reference_build.pdf`
  (the authoritative Paper9 PDF, frozen).
- **Interactive render:** a live HTML/MathML preview of the adapted manuscript is
  served at **`preview/index.html`** (port 8618) — figures are the restyled PDFs
  rasterized to PNG, citations are numbered `[1]…[15]` per elsarticle-num, and
  every cross-reference resolves.
- **To obtain the real adapted PDF:** upload `OVERLEAF/` to Overleaf
  (pdflatex + BibTeX, `elsarticle-num`) — the package is self-contained and has
  been statically audited with 0 unresolved references/citations and all
  figure/table assets present.

---

### Final consistency-audit summary

| Axis | Result |
|------|--------|
| Fonts | STIX/Times-family text+math in all 14 figures (probed per PDF) |
| Headings / frontmatter | FEM₃ elsarticle structure; Paper9 wording intact |
| Equations | 0 unbalanced environments; all Paper9 notation macros preserved |
| Figures | 14/14 balanced, present, data-identical to source |
| Captions | Paper9 captions unchanged |
| Tables | 7/7 byte-identical fragments, balanced floats |
| References | 15 entries, byte-identical, 0 dangling cites |
| Citations | elsarticle-num = Paper9's original unsrt numbering |
| Margins / spacing | FEM₃ geometry (a4paper, 1in) |
| Numbering | figure/table/equation/ref labels unchanged (labels & cross-refs intact) |
| Graph style | FEM₃ palette/grid/legend/spines; scientific colormaps preserved |
| **Scientific values anchors** | `p=4.17 (95% CI 3.15–5.20)`, `εΔ=4.63e-11`, `ΔGX=+0.0043 (AR=10,θ=45°)`, `Δ_complete ≤ −0.3235`, `max ΔGX=0.0677 (θ=0°,AR=7)`, `Sθ=2.34`, `δmax=1.41°(AR5)/2.78°(AR10)`, `Ms=0°/10°`, `vT∞≈0.3162 (FE 0.3163)` — all verified present in the final render |
