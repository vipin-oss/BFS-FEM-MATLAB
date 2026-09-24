# P12AI — Final manuscript closure (record)

**Phase:** P12AI · **Date:** 2026-09-24 · **Entry commit:** `e986a13fdd82e8df1e2c93a534aa6ae4163bd8e6` (P12AH final)
**Purpose:** close the manuscript build. Mechanical/editorial only — no scientific claim, numerical result,
benchmark status, gate, threshold, equation, figure datum or validation conclusion was changed.

## 1. Inspection first (P12AI decision, applied here)

The build was reproduced from repository sources and the rendered PDF measured with the text-run extraction
clip widened beyond the page box (a page *is* its MediaBox; ink beyond it is printed by nothing). Result:
of the six tables P12AH left untouched, **five printed content outside the physical page** and one did not:

| table | P12HI-era box | observed in the rendered PDF | decision |
|---|---:|---|---|
| Table 1 (tab01) | 214.16 pt | ink to 802 pt; *Orientation θ*, *Numerical method*, *Reported* columns off-page (66 words) | **repair** |
| Table 3 (tab04) | 67.63 pt | every status printed **"PAS"** instead of "\textbf{PASS}"; header "Stat" | **repair** |
| Table 4 (tab06) | 782.05 pt | ink to 1 318 pt; header "In rate fit?" cut; note sentence about the 32² level / Rule R-fit exclusion lost (31 words) | **repair** |
| Table 5 (tab02) | 152.53 pt | whole *Physical interpretation* column off-page (69 words); Source header cut | **repair** |
| Table 6 (tab05) | 39.12 pt | fully printed; one note line 38 pt into the margin, 17 pt clear of the page edge | **leave unchanged** |
| Table 7 (tab07) | 251.57 pt | entire last column (ϕ\* for AR = 10) off-page; notes lost (17 words) | **repair** |

## 2. Corrections applied (five tables, minimum, content-neutral)

Applied to the **generators** (never by hand-editing generated output), then regenerated:

| table | change |
|---|---|
| tab01 (Table 1) | wrap cols 1/4/8 in ragged `p{2.0cm}` / `p{2.4cm}` / `p{2.0cm}`; `\footnotesize`; `\tabcolsep` 2 pt |
| tab02 (Table 5) | value/unit/source columns wrapped (`p{2.5cm}`, `p{1.8cm}`, `L{3.0cm}`); `\scriptsize`; `\tabcolsep` 2 pt; zero-width break opportunities after escaped underscores in long identifiers |
| tab04 (Table 3) | identity column ragged `p{3.6cm}`, its budget `L{4.5cm}` → `L{4.0cm}` (no font change) |
| tab06 (Table 4) | last column ragged `p{2.0cm}`; `\footnotesize`; `\tabcolsep` 3 pt; note rows wrapped to the text width |
| tab07 (Table 7) | note rows wrapped to the text width (nothing else) |

`tab05` (Table 6) was **not** modified and is asserted byte-identical to the entry commit.

Layout only: column specification, table-internal font size, column separation, zero-width break
opportunities, and the width of the full-width note rows. No character, number, symbol, caption, footnote
text, figure, reference or claim changed.

## 3. Content-neutrality proof (per table, byte-level)

Undoing the documented layout edits reproduces the pinned pre-layout content exactly:

| table | undo target | sha256 (pin held by the guard) |
|---|---|---|
| tab01 | entry-commit bytes | `e47d4f70…` |
| tab02 | entry-commit bytes | `16c621f3…` |
| tab03 | P12AF content (P12AH repair) | `77fd7584…` |
| tab04 | entry-commit bytes | `0ec19e55…` |
| tab05 | *not modified* | `a696586b…` |
| tab06 | entry-commit bytes | `478545af…` |
| tab07 | entry-commit bytes | `bcf8ca92…` |

`test_p12ah_generator_and_layout.py` also re-runs every generator in a scratch copy (byte identity with the
committed table), compiles every repaired table alone (zero errors, zero overfull boxes) and checks the
numeric content is unchanged.

## 4. Final build (repository sources only)

| check | result |
|---|---|
| LaTeX errors | **0** |
| missing files | **0** |
| undefined citations / references | **0 / 0** |
| bibliography | resolves; 15 entries, `unsrt.bst`, no bibtex errors |
| figures | 21 figure captions present, Figures 1–14 included, none regenerated (`fig05` still `3d309eaa…`) |
| tables | Tables 1–7 all present; every table fully inside the text block |
| overfull boxes | **611 → 6** (five are body-prose paragraphs 3.07–15.78 pt; one is the Table 6 alignment box, harmless) |
| underfull boxes | 3 |
| pages / size | 34 pp / 904 992 B (page count reflowed from 35 as the tables grew more compact — no content removed) |
| reproducibility | a second, independent scratch-tree build gives byte-identical per-page content streams on all 34 pages |

Rendered evidence: `/home/user/p12ai_final_build.pdf` and `/home/user/p12ai_final_tables.png`.

## 5. Scientific status — unchanged (frozen, not relabelled)

B1 GRAPHICAL_VALIDATION / PASS · B2/B3 NOT VALIDATED · B3 ESTABLISHED / SOURCE-EQUIVALENT ·
`quantitative_error` NULL ×3 · PCR1 NOT PASS · G3/G4 NOT MET · P5 NOT PASS / OPEN · R-1 OPEN ·
C-1 closed as a criterion item · PCR5 PASS · author-data route NOT SENT / NOT AUTHORISED ·
external benchmark hunt CLOSED · **submission NOT AUTHORISED**.

## 6. Verification

Full suite: **375 passed, 1 skipped** (the skip is the environment-conditional TeX check). The manuscript
build is declared closed at the commit recorded in `RECOVERY_CHECKPOINT_P12AI.md`.
