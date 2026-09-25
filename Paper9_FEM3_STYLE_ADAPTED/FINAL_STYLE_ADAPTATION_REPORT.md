# FINAL STYLE ADAPTATION REPORT — Paper9 → `Paper9_FEM3_STYLE_ADAPTED`

**Scope:** publication-style transformation of Paper9 using FEM_3 as the
formatting/style reference, with Paper9 remaining the source of scientific truth.
**Verification method:** programmatic comparison against the authoritative,
untampered Paper9 package (`MANIFEST.sha256` + byte/hash comparisons), runtime
instrumentation of the figure generators to prove data identity, and a **real
LaTeX compile under TeX Live** via GitHub Actions.

---

## 1. Objective

Restyle Paper9's **presentation layer** to follow FEM_3's manuscript and
figure/table conventions — without changing any scientific content (equations,
results, parameters, figures data, tables, references, authorship, claims).
The deliverable is a self-contained Overleaf-ready package under
`Paper9_FEM3_STYLE_ADAPTED/`, plus this verification record.

---

## 2. FEM_3 Style Characteristics

Extracted from the FEM_3 reference sources and rendered PDF:

- **Document class:** `\documentclass[preprint,12pt]{elsarticle}` (single-column
  author preprint; the two-column look in the published PDF is journal typesetting).
- **Geometry:** `\usepackage[a4paper,margin=1in]{geometry}`.
- **Front matter:** elsarticle `\begin{frontmatter}` with `\title`, `\author` +
  `\corref`/`\cortext`, multiple `\address`, `\journal{}`, `\begin{abstract}`,
  `\begin{keyword}` … `\sep` … `\end{keyword}`.
- **Fonts:** Times-family serif (SF* `sfrm/sfti/sfbx` fonts in the rendered PDF,
  i.e. New Century Schoolbook/Times family) for text; Computer-Modern maths.
- **Citations/bibliography:** `\bibliographystyle{elsarticle-num}` — numeric
  labels assigned in **first-citation** order (verified from the reference build
  where [1] is the first-cited work).
- **Tables:** `booktabs` (`\toprule/\midrule/\bottomrule`), `tabular`/`tabularx`.
- **Figures:** wide flat single-column panels; Times/STIX text and maths;
  soft dashed gray grids; boxed axes with thin frames; restrained dark palette
  (`#1f77b4` blue, `#d62728` red, `#2ca02c` green, `#ff7f0e` orange,
  `#9467bd` purple); thin-edged framed legends; modest markers; panel titles
  `(a)`/`(b)`.
- **Endmatter:** `Data availability statement`, `Conflict of interest disclosure
  statement`, `Acknowledgments` (HSHEC/HSRF) — present in FEM_3.

---

## 3. Paper9 Changes

Presentation-layer only:

| Layer | Paper9 original | Adapted (FEM_3 style) |
|---|---|---|
| Document class | `article` 11pt, A4, 2cm margins | `elsarticle` preprint, 12pt, A4, 1in margins |
| Front matter | `\title`(textbf)/`\author`+`\thanks`/`\abstract` + `\paragraph{Highlights/Keywords}`/`\date` | `frontmatter` + `\title`/`\author`+`\corref`/`\address`×2/`\journal{}`/`abstract`/`keyword`+`\sep` |
| Bibliography | `unsrt` | `elsarticle-num` (= same numeric order, by first citation) |
| Highlights | `\paragraph{Highlights:}` + itemize | `\section*{Highlights}` + itemize (same bullets) |
| Endmatter | absent in original | Data availability + COI + Acknowledgments added (FEM_3 convention; wording generalized, no new scientific content) |
| Figures | DejaVu/mixed styling | FEM_3 palette/grid/legend/fonts (data unchanged) |
| Tables | already booktabs | reused byte-identical |
| `\date{September 2026}` | present | omitted (elsarticle preprint has no date field) |

Text content (title, abstract, keywords, highlights, author team, affiliation,
funding sentence) is **preserved verbatim**; only the LaTeX containers changed.

---

## 4. Figure Transformation

All 14 figure generators were rewritten using the shared
`figures_gen/fem3style.py` module (STIX/Times text+math, dashed gray grid,
boxed axes, FEM_3 palette, framed legends, modest markers). The data-extraction
and value logic is preserved.

Data-identity proof (see §8):

| Figure | Original data source | Adapted data source | Data identical? | Only visual style changed? |
|---|---|---|---|---|
| fig01 ellipsoid tensor | `params/params_master.yaml` | same | **YES** | YES (lw/zorder) |
| fig02 lattice IBZ | `params/params_master.yaml` | same | **YES** | YES (s/width/lw) |
| fig03 BFS DOF Bloch | (hard-coded geometry) | same | **YES** | YES (lw/s) |
| fig04 benchmark validation | `validation/b1_b2_b3_solver` | same | **YES** | YES (lw/alpha) |
| fig05 mesh convergence | `p4b_5g_to_5i.json` + `rule_rfit_governing.json` | same | **YES** | YES (lw/ms/mew) |
| fig06 Case H dispersion | `p5_production_raw_mesh16.json` (S1) | same | **YES** | YES (lw/zorder) |
| fig07 Case C dispersion | `p11_caseC_raw.json` (S2) | same | **YES** | YES (lw/alpha) |
| fig08 theta sweep | `p5_production_raw_mesh16.json` (S3) | same | **YES** | YES (lw/ms) |
| fig09 AR sweep | `p5_production_raw_mesh16.json` (S4) | same | **YES** | YES (lw/ms) |
| fig10 design map 3D | `p5_production_raw_mesh16.json` (S5) | same | **YES** | YES (linewidths) |
| fig11 polar regimes | `p5_production_raw_mesh16.json` (S6) | same | **YES** | YES (s/lw/ms) |
| fig12 IFC steering | `p5_production_raw_mesh16.json` (S7) | same | **YES** | YES (lw) |
| fig13 energy microinertia | `p5_production_raw_mesh16.json` (S8/S9) | same | **YES** | YES (lw) |
| fig14 S7 steering sweep | `p12b_s7_theta_sweep_mesh16.json` | same | **YES** | YES (lw/ms/mew) |

Two scientific **value encodings** were deliberately preserved: `viridis`
(fig10) and `plasma` (fig11) colormaps, because they encode the design-map /
regime values and FEM_3 has no comparable surface/polar encoding.

---

## 5. Table Transformation

All 7 table fragments (`tab01…tab07`) are reused **byte-identically** from the
authoritative package (`sha256` equal to `MANIFEST.sha256`). Paper9 already used
booktabs, so no formatting change was required or made. Numeric-token content
is identical in all 7.

---

## 6. Citation and Reference Transformation

- `OVERLEAF/references.bib` is **byte-identical** to the authoritative Paper9
  bibliography (`sha256 e585c875…3568`), original keys intact.
- Only `\bibliographystyle{unsrt}` → `elsarticle-num`. Because elsarticle-num
  numbers by first citation and the section files are byte-identical, Paper9's
  first-citation order is unchanged, so the numeric labels equal the original
  `unsrt` numbering.
- **First-citation map** (verified programmatically):
  `[1] kushwaha1993`, `[2] mindlin1964`, `[3] toupin1962`,
  `[4] mindlineshel1968`, `[5] askesaifantis2011`, `[6] polyzosfotiadis2012`,
  `[7] papargyribeskou2009`, `[8] liweizhou2016`, `[9] zhanwei2010`,
  `[10] zhengwei2009`, `[11] hosseinizhang2021`, `[12] li2023anchorA`,
  `[13] li2024anchorB`, `[14] mishra2026anchorC`, `[15] bfs1965`.
- A numeric-keyed **preview** (`tables/references_numeric.bib`, ref1…ref15) and
  map (`tables/bib_key_map.txt`) are provided for the report; the active file
  keeps the authoritative keys.

---

## 7. Scientific Content Preservation

Verified unchanged, with cryptographic evidence:

- **11 section files** (`sec01…sec09`, `appA`, `appB`): byte-identical
  (`sha256` == `MANIFEST.sha256`). → all equations, derivations, governing &
  constitutive equations, boundary conditions, algorithm descriptions, and
  in-text results are untouched.
- **7 tables**: byte-identical → all parameter registries, error metrics,
  gap values, mesh values, steering values untouched.
- **`references.bib`**: byte-identical → bibliographic identities preserved.
- **Author team / affiliation / funding / title / abstract / keywords /
  highlights**: text strings present verbatim in both (formatting wrappers only
  differ).
- **Figure data**: 14/14 positional data identical (runtime instrumentation).
- **Physical model**: FEM_3's (different) model was never imported.

---

## 8. Validation / Audit Results

**A. Source audit (static):**
- 0 undefined references (44 `\ref`/`\eqref` targets all resolve to 111 labels).
- 0 undefined citations (15 keys cited = 15 bib entries).
- 14/14 figure assets present; 7/7 table inputs present; environments balanced.

**B. Cryptographic byte-identity vs authoritative `MANIFEST.sha256`:**
- 19/19 files IDENTICAL (11 sections + 7 tables + 1 bibliography).
- Frozen `PAPER9_ORIGINAL_manuscript.tex` identical to authoritative `manuscript.tex`.

**C. Figure data identity (runtime instrumentation, matplotlib monkey-patch):**
- Original and adapted generators executed in isolation; every numeric
  positional argument to every plotting call recorded and compared.
- 14/14 figures: **positional DATA IDENTICAL** (12-decimal canonical float
  equality); only style kwargs differ (lw/ms/s/zorder/alpha/mew/width/linewidths).

**D. Real LaTeX compile (TeX Live via GitHub Actions):**
- ADAPTED: `Output written on manuscript.pdf (39 pages)`; 0 errors; 0 undefined
  references; 0 undefined citations.
- ORIGINAL (authoritative, same engine): 34 pages; 0 errors; 0 undefined.
- Overfull boxes: original 7, adapted 52 (narrower 1in text column vs the
  original 2cm margins acting on byte-identical wide tables). "Float too large"
  is pre-existing in both (original 1254pt ≈ adapted 1323pt; same source,
  `tab02` master-parameter longtable, sec05 line 128). Reported as limitations,
  not silently altered.

---

## 9. Compilation Status

- **`REAL LATEX COMPILATION: PASS`** — genuine TeX Live (GitHub Actions,
  `texlive/texlive:latest-full` Docker) compiled the adapted manuscript with
  `pdflatex + bibtex + 2×pdflatex`; PDF produced: 39 pages, A4, 0 errors,
  0 undefined refs/cites. Artifact committed to the branch as
  `Paper9_FEM3_STYLE_ADAPTED/OVERLEAF/manuscript.pdf`, with
  `CI_COMPILE_DIAGNOSTICS.txt`.
- **`faster-latex (HTML/MathML) preview:` present** (`OVERLEAF/../preview/`),
  used only as a viewable render aid — **not** a substitute for the TeX Live
  compile.
- **Static source audit:** PASS (see §8A).

---

## 10. Remaining Limitations

1. **52 overfull `\hbox` warnings** in the adapted build (vs 7 in the original)
   arise from FEM_3's 1-inch margins narrowing the text column while tables
   remain byte-identical to Paper9. Not auto-fixed (any table-width change would
   alter scientific material or require a content-level decision).
2. **"Float too large" warnings** for the tall `tab02` master-parameter table
   are **pre-existing** (original 1254pt vs adapted 1323pt). Sizes shift with
   the geometry change; the table floats by itself on its page.
3. elsarticle preprint renders the manuscript **single-column**; the journal's
   production would re-typeset two columns. This matches FEM_3's own source.
4. `Data availability` / `Conflict of interest` / `Acknowledgments` blocks were
   **added** to match FEM_3 conventions (the original manuscript had none, and
   did not carry them). They contain no scientific content. Flagged transparently,
   not hidden.
5. `\date{September 2026}` was omitted (elsarticle preprint prints no date).
6. The keyword list differs from the original only by the trailing period
   ("Wave steering." → "Wave steering" inside `\begin{keyword}`).
7. The GitHub Actions temporary workflow used for compilation has been removed
   after use, leaving only the committed compiled PDF + diagnostics.

---

## 11. Final File Manifest

`Paper9_FEM3_STYLE_ADAPTED/`

```
OVERLEAF/manuscript.tex                          MAIN manuscript (elsarticle, FEM_3 style)  ← FINAL
OVERLEAF/manuscript.pdf                          TeX Live-compiled adaptive PDF (39 pages)
OVERLEAF/CI_COMPILE_DIAGNOSTICS.txt              compile diagnostics (0 errors, overfull counts)
OVERLEAF/references.bib                          bibliography (byte-identical, elsarticle-num)
OVERLEAF/sections/{sec01..sec09,appA,appB}.tex   11 sections (byte-identical)
OVERLEAF/tables/tab01..tab07_*.tex               7 tables (byte-identical)
OVERLEAF/figures/fig01..fig14_*.pdf              14 restyled FEM_3-style figures
OVERLEAF/gen/fig01..fig14_*.py                   original Paper9 generators (reference, untouched)
OVERLEAF/PAPER9_ORIGINAL_manuscript.tex          frozen authoritative manuscript
OVERLEAF/PAPER9_ORIGINAL_reference_build.pdf     frozen authoritative reference PDF
OVERLEAF/README.md                               (Overleaf usage notes, if present)

figures_gen/fem3style.py                         FEM_3 style module
figures_gen/fig01..fig14_*.py                    restyled generators (14)

tables/build_tables.py                           table builder (writes OVERLEAF/tables/)
tables/build_references.py                       reference builder
tables/tables_rebuilt/*.tex                      7 working copies
tables/references_numeric.bib                    numeric-keyed preview (report only)
tables/bib_key_map.txt                           first-citation key map

ORIGINAL/Paper9_FINAL_SOURCE_PACKAGE.zip         frozen original zip (36 MB, untracked in git)
ORIGINAL/FINAL_PACKAGE_AUDIT.md                  original audit
ORIGINAL/MANIFEST.sha256                         original SHA-256 manifest (verification authority)
ORIGINAL/references_original_keys.bib            original bibliography

preview/index.html + figure_png/                HTML/MathML preview (viewable render)
preview/README.md

REPORT/README.md                                 change report (A–G)
FINAL_STYLE_ADAPTATION_REPORT.md                 this report

PROGRAM/paper9/                                  authoritative program tree (copied; data source)
```

---

## Final Status

- SCIENTIFIC CONTENT: **PASS**
- FIGURE DATA: **PASS** (14/14 numerically identical; style only)
- TABLE DATA: **PASS** (7/7 byte-identical)
- REFERENCES: **PASS** (15 = 15, byte-identical, no additions/removals)
- SOURCE STRUCTURE: **PASS** (0 undefined refs/cites, all assets present)
- REAL LATEX COMPILATION: **PASS** (TeX Live, 39-page PDF, 0 errors)
- FEM_3 STYLE ADAPTATION: **PASS** (elsarticle frontmatter, elsarticle-num
  citations, Times-family fonts, FEM_3 figure language; intentional diffs listed
  in §10)
- FINAL PACKAGE: `/home/user/BFS-FEM-MATLAB/Paper9_FEM3_STYLE_ADAPTED/`
- FINAL COMMIT: see §"Git & commit"; the exact hash of the verification-report
  commit is reported in the delivery message.

---

## Git & commit

- Branch: `arena/01a0d8f7-bfs-fem-matlab`
- HEAD at time of final report commit: `7a4a5a4b08e33a915f19de93d7e52062491c8f6d`
  (report commit; final amended hash reported in the delivery message)
- Compiled PDF commit (CI): `5c742306d688e201fd549769615077242ee8f9d9`
- Authoritative Paper9 content: untouched (frozen under `ORIGINAL/`,
  `OVERLEAF/PAPER9_ORIGINAL_*`, and in git history at commit `0f1397b6`)
- FEM_3.zip: unmodified (untracked; sha256 `e312f486…6df9`, mtime 2026-09-25 14:28)
- Temporary GitHub Actions workflow: removed after the compile verification.
