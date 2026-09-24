# P12AH — Table-layout repair and generator reconciliation (record)

**Phase:** P12AH · **Date:** 2026-09-24 · **Entry commit:** `b45ea785cadfc0ae09ffcba0c0d11153c6144bd4`
**Nature:** mechanical / editorial only. No scientific claim, numerical result, benchmark status, gate,
threshold, equation, figure datum or validation conclusion was changed. Submission remains NOT AUTHORISED.

## 1. Authorisation and scope

The P12AG report listed two follow-up items (its §B): (i) the stale `paper9/tables/gen/tab03_anchor_errors.py`
would, if run, have reverted the P12AF-audited Table 2 content, and (ii) Table 2's Status column was pushed
past the printed page by the longer P12AF labels — a layout-only wrap that P12AG deliberately did not apply
without authorisation. The same §B note recorded the other large overfull boxes (tab06 782.05, tab07 251.57,
tab01 214.16 pt, plus tab02 152.53 and tab04 67.63 pt). The PI instructed "do", authorising those items.
Nothing else was opened: no author contact, no benchmark hunt, no rerun, no gate change.

## 2. What changed (17 modified + 2 new files)

**Generators** (`paper9/tables/gen/`) — tab01, tab02, tab03, tab04, tab05, tab06, tab07. Fixing the
generators first means the generated `.tex` is a product, not a hand edit; `tab03`'s template, which was
stale, now embeds the P12AF-authorised table plus the layout correction, so running any generator can no
longer revert an audited record.

**Generated tables** (`paper9/tables/out/`) — the seven repaired files. Per table:

| table | layout correction applied |
|---|---|
| tab01 literature positioning | wrap the long text columns in `p{2.0/2.4/2.0 cm}`; `\footnotesize`; `\tabcolsep` 2 pt |
| tab02 parameter registry | wrap the value/unit/source columns (`p{2.5cm}`, `p{1.8cm}`, `L{3.0cm}`); `\scriptsize`; `\tabcolsep` 2 pt; zero-width break opportunity after each escaped underscore in long `\texttt` identifiers |
| tab03 anchor errors (Table 2) | width-aware `tabularx` all-X specification, `p{2.0cm}`/`p{2.4cm}` reference/status columns; `\tabcolsep` 2 pt; zero-width break hints in the long identifier labels |
| tab04 consistency suite | wrap the identity column `p{3.6cm}`; source column `L{4.0cm}` |
| tab05 gap summary | last column becomes a centred `p{2.2cm}` (the long header identity now wraps); note rows wrap across the full width |
| tab06 convergence floor | last column `p{2.0cm}`; `\footnotesize`; `\tabcolsep` 3 pt; note rows wrap across the full width |
| tab07 steering sweep | note rows wrap across the full width (`\multicolumn{5}{...p{\dimexpr\textwidth-2\tabcolsep\relax}...}`) |

**Guards / record files** — new `paper9/verification/suite/test_p12ah_generator_and_layout.py` (24 guards);
extensions in `test_p12af_manuscript_retiering.py` (phase-change allowlist) and
`test_p12ag_clean_build.py` (tolerate the zero-width hints; ignore layout-only markup when counting numeric
tokens; tab02 digest re-pinned — see §4); `test_p6_remediation.py` (same hint tolerance); new
`paper9/audit/P12AH_FIGURE_FRESHNESS.json`.

## 3. Content neutrality — proved, not asserted

Per table, undoing the documented layout edits returns the file **byte-for-byte** to the state the phase
found it in (sha256 pinned inside the guard):

| table | pre-layout sha256 |
|---|---|
| tab01_literature_positioning | `e47d4f70…` |
| tab02_parameters | `16c621f3…` |
| tab03_anchor_errors | `77fd7584…` (the P12AF bytes) |
| tab04_consistency_suite | `0ec19e55…` |
| tab05_gap_summary | `a696586b…` |
| tab06_convergence_floor | `478545af…` |
| tab07_steering_sweep | `bcf8ca92…` |

The guard also runs each generator in a scratch copy and asserts its output is byte-identical to the
committed file, compiles each table alone and asserts zero overfull boxes, and checks that the numeric
content is untouched.

## 4. Numerical invariance

`test_p12ag_clean_build.py` continues to pin the numeric tokens of the three tables P12AG repaired. Its pins
for `tab05` (`75bb31b6…`) and `tab06` (`192ffe3c…`) still hold **unchanged**; the `tab02` digest was
re-pinned (`60aabd3a…` → `c1c5eb93…`) because the original digest included the digits of the column
specification itself, which the layout repair necessarily changed. The re-pin is content-neutral: the guard's
byte-identity-after-undo check is the stronger statement and passes for `tab02`.

## 5. Build evidence (repo-only source, clean scratch tree)

| | before P12AH (entry `b45ea78`) | after P12AH |
|---|---|---|
| LaTeX errors | 0 | 0 |
| overfull boxes (whole manuscript) | 611 | **5** |
| underfull boxes | 5 | 4 |
| pages | 34 | 34 |
| undefined citations / references | 0 / 0 | 0 / 0 |

The five remaining overfull boxes are **body prose** paragraphs (3.07, 4.53, 7.67, 9.00, 15.78 pt) in
§5, §7 and Appendix A — not tables, and not touched (rewriting prose is outside this phase). Largest table
box per table, before → after (isolated builds): tab01 214.16 → 0; tab02 152.53 (563 boxes) → 0;
tab03 243.25 → 0; tab04 67.63 → 0; tab05 39.12 → 0; tab06 782.05 → 0; tab07 251.57 → 0.

Rendered output: `/home/user/p12ah_manuscript_build.pdf` (34 pp) with page captures
`p12ah_table2_fixed.png` and `p12ah_table6_fixed.png`. No word in the built PDF now lies beyond the text
block except the six caused by those five prose paragraphs.

## 6. Figure 5 freshness (supersedes P12J's mtime check)

Regenerating `fig05_mesh_convergence.pdf` yields different bytes under the installed matplotlib but a
**pixel-identical** raster (0 of 1 609 713 subpixels differ by more than 8/255), so the committed figure is
not stale. Freshness is now judged by hashing the inputs it derives from
(`P12AH_FIGURE_FRESHNESS.json`): figure `3d309eaa…`; inputs generator `7379ba9b…`, `p4b_5g_to_5i.json`
`38384363…`, `rule_rfit_governing.json` `349c56c6…`. The historical P12J script is left byte-unchanged.

## 7. Statuses — unchanged

B1 GRAPHICAL_VALIDATION / PASS · B2/B3 NOT VALIDATED · B3 ESTABLISHED / SOURCE-EQUIVALENT ·
`quantitative_error` NULL ×3 · PCR1 NOT PASS · G3/G4 NOT MET · P5 NOT PASS / OPEN · R-1 OPEN ·
C-1 closed as a criterion item · PCR5 PASS · author-data route NOT SENT / NOT AUTHORISED ·
external benchmark hunt CLOSED · **submission NOT AUTHORISED**.

## 8. Verification

Full suite **369 passed, 1 skipped** (355 passed, 1 skipped before this phase; +14 from the new guard file).
`test_p12ah_generator_and_layout.py` 24/24. Repository left clean apart from the new build product
`paper9/latex/ms.pdf` (untracked, as before).
