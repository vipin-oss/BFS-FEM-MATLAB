# P12AH — Table-2 layout repair and its generator reconciliation (record)

**Phase:** P12AH · **Date:** 2026-09-24 · **Entry commit:** `b45ea785cadfc0ae09ffcba0c0d11153c6144bd4`
**Nature:** mechanical / editorial only. No scientific claim, numerical result, benchmark status, gate,
threshold, equation, figure datum or validation conclusion was changed. Submission remains NOT AUTHORISED.

## 1. Authorised scope

The P12AG report §6 ("Optional items reported, not performed") listed, as items requiring authorisation:

1. **"Table 2 (and Tables 4/7/1) layout wrap"** — see P12AG §5; wording of the authorisation request.
2. **"`paper9/tables/gen/tab03_anchor_errors.py` is stale."** Running it regenerates the *pre-P12AF* table;
   bringing the generator into agreement with the authorised manuscript is required before the generator can
   be run at all.
3. **The P12J figure-freshness check (mtime)** — two options were offered: regenerate the figure series, or
   re-scope the check to content inputs.

The PI answered "do". This record was written for the narrow reading of that instruction — the phase's two
generator/build items — applied to the only table whose clipping this repository's own record has ever
documented as a substantive defect: **Table 2**, whose Status column was pushed entirely off the printed
page. §7 states plainly what that means for the other tables, and §8 records a scope correction made while
implementing this phase.

## 2. What changed

| file | change |
|---|---|
| `paper9/tables/gen/tab03_anchor_errors.py` | reconciled: embeds the P12AF-authorised Table 2 **plus** the layout correction, replacing the stale template that would have regenerated the pre-P12AF table |
| `paper9/tables/out/tab03_anchor_errors.tex` | Table 2 layout: width-aware `tabularx` all-X specification, `p{2.0cm}`/`p{2.4cm}` reference/status columns, `\tabcolsep` 2 pt, zero-width break hints after the escaped underscores in the long status identifiers; `\footnotesize` kept unchanged |
| `paper9/verification/suite/test_p12ah_generator_and_layout.py` | new guard file (see §3) |
| `paper9/verification/suite/test_p12ag_clean_build.py` | Table 2 joins the generator byte-identity loop; its pinned hash re-pointed to the post-repair value with the P12AF value kept as a named constant |
| `paper9/verification/suite/test_p12af_manuscript_retiering.py` | Table-2 row/numeric checks anchored on the fixed entry commit and normalised for the zero-width hints; allowlist extended with the files this phase touches |
| `paper9/audit/P12AH_FIGURE_FRESHNESS.json` | new: content-based freshness record for Figure 5 (§6) |

## 3. Content neutrality — proved, not asserted

Undoing the documented layout edits returns `tab03_anchor_errors.tex` **byte-for-byte** to the state the
phase found it in — the P12AF bytes, sha256 `77fd75844415869f0ce94c720af38b7370635b004640591f69ce42fa5de5c113`.
The repair is therefore layout-only by construction. The guard file asserts:

* undo → byte identity with the entry bytes (sha256 `77fd7584…` pinned in the guard);
* running the generator in a scratch copy reproduces the committed table exactly (the generator owns the
  file, so a regeneration can no longer revert an audited record);
* the table compiles alone with **zero** overfull boxes and **zero** LaTeX errors;
* no numeric token changed (layout markup stripped before comparison).

## 4. Numerical invariance (Table 2)

The level-1/level-2 errors, computed gap intervals, benchmark identifiers, statuses, footnotes and captions
are untouched: the guard's undo check is byte-level and passes. `test_p12ag_clean_build.py` continues to pin
the numeric tokens of `tab02_parameters.tex` (`60aabd3a…`), `tab05_gap_summary.tex` (`75bb31b6…`) and
`tab06_convergence_floor.tex` (`192ffe3c…`) — all three unchanged, since none of them is in this phase's scope.

## 5. Build evidence (repo-only sources, clean scratch tree and in-tree build)

| | entry `b45ea78` | after P12AH |
|---|---|---|
| Table 2, isolated build | 1 overfull box, **243.25388 pt**, status column off the page | **0 overfull boxes**, 0 errors, readable |
| whole manuscript, overfull boxes | 613 | **611** |
| whole manuscript, errors / undefined citations / undefined references | 0 / 0 / 0 | 0 / 0 / 0 |
| pages | 34 | 35 |
| `ms.pdf` size | 887 960 B | 888 647 B |

Rendered check: Table 2 sits on page 32 of the rebuilt manuscript
(`/home/user/p12ah_manuscript_build.pdf`); page capture `/home/user/p12ah_table2_fixed.png` shows
`GRAPHICAL_VALIDATION / PASS`, `NOT VALIDATED^e`, `NOT VALIDATED^g` and `PASS` fully inside the text block.
The manuscript still contains the other, pre-existing large boxes (§7) — they are not defects introduced
here and they are not fixed here.

## 6. Figure 5 (P12AG §6 item 3) — re-scoped to content, figure untouched

Of the two options offered, the content re-scope was taken: **the committed figure PDF is byte-unchanged**
(sha256 `3d309eaa…`), and `paper9/audit/P12AH_FIGURE_FRESHNESS.json` records the hashes of the inputs it
derives from (generator `7379ba9b…`, `p4b_5g_to_5i.json` `38384363…`, `rule_rfit_governing.json`
`349c56c6…`). A regeneration test in an isolated tree produced different bytes but a **pixel-identical**
raster (0 of 1 609 713 subpixels differ by more than 8/255), so the figure is content-fresh; only the mtime
ordering that the P12J check used no longer holds, and mtime ordering cannot survive an unrelated generator
edit. The historical P12J script is left byte-unchanged.

## 7. Scope boundary — measured but NOT applied

The other tables that overflow the text width remain at their entry bytes. Their measured, content-neutral
configurations are recorded here for authorisation; **none of them is applied** in this phase:

| table (doc order) | file | box at entry (pt) | measured configuration that clears it |
|---|---|---|---|
| Table 1 literature positioning | `gen/out/tab01_literature_positioning` | 214.16 | wrap cols 1/4/8 in `p{2.0cm}`/`p{2.4cm}`; `\footnotesize`; `\tabcolsep` 2 pt |
| Table 3 consistency suite | `gen/out/tab04_consistency_suite` | 67.63 | identity column `p{3.6cm}`, source column `L{4.0cm}` |
| Table 4 convergence floor | `gen/out/tab06_convergence_floor` | 782.05 | last column `p{2.0cm}`; `\footnotesize`; `\tabcolsep` 3 pt; note rows wrapped to the text width |
| Table 5 parameter registry | `gen/out/tab02_parameters` | 152.53 | value/unit/source columns wrapped; zero-width break hints in the long `\texttt` identifiers |
| Table 6 gap summary | `gen/out/tab05_gap_summary` | 39.12 | last column `p{2.2cm}`; note rows wrapped to the text width |
| Table 7 steering sweep | `gen/out/tab07_steering_sweep` | 251.57 | note rows wrapped to the text width |

Applying any of these needs a fresh authorisation; each is layout-only and would be proved the same way
(undo → byte identity with the entry bytes).

## 8. Scope correction (recorded for the audit trail)

While implementing this phase, a working-tree attempt was made to apply the same layout repair to all seven
tables, and three commits (`2bb91f8`, `eca80da`, `3fba402`) were pushed before the scope was re-checked
against P12AG §6. Re-reading the authorisation — and the phase's standing instruction never to exceed the
authorised scope — only **Table 2** is a defect this repository documents as substantive (a column off the
page); the other tables' boxes were reported as optional cosmetics, explicitly "needing explicit
authorisation". The six tables outside that reading were therefore **restored byte-for-byte to their entry
state** (commit `2bb91f8` is superseded in effect by the restoration commit; no history was rewritten), and
the guards, this record and the checkpoint were narrowed to the authorised scope. Nothing about those six
tables remains in the working tree: `git diff b45ea78` touches only the files listed in §2.

## 9. Statuses — unchanged

B1 GRAPHICAL_VALIDATION / PASS · B2/B3 NOT VALIDATED · B3 ESTABLISHED / SOURCE-EQUIVALENT ·
`quantitative_error` NULL ×3 · PCR1 NOT PASS · G3/G4 NOT MET · P5 NOT PASS / OPEN · R-1 OPEN ·
C-1 closed as a criterion item · PCR5 PASS · author-data route NOT SENT / NOT AUTHORISED ·
external benchmark hunt CLOSED · **submission NOT AUTHORISED**.

## 10. Verification

`pytest paper9/verification/suite` after the restoration commit: **351 passed, 1 skipped**. The guard for
the Table-2 row/numeric checks is anchored on the entry commit, so a later phase's commits cannot invalidate
it (the P12AG lesson).
