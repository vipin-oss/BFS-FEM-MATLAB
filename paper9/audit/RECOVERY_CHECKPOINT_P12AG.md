# RECOVERY CHECKPOINT — P12AG (final)

**Phase completed:** P12AG — clean-build repair. The manuscript now compiles from the repository itself
with **zero LaTeX errors**; only mechanical build defects were repaired. No scientific claim, numerical
value, benchmark status, gate, threshold, figure or conclusion changed.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Entry (verified tri-equal, clean) | `dbd68b600c641a20ede810c5110e9d3bed2ae101` (P12AF final checkpoint) |
| **P12AG main commit** | **`e8f5e1b3df7b636d8767e034f1d3b135a3766994`** |
| **P12AG final checkpoint commit** | `74155d621b61dad6f1041ea646dac3f6140a3577` |
| P12AG guard-scoping commit (no content change) | `08782ef` — the `ms.tex` repair guard anchored on the pre-repair commit `dbd68b6` so it holds before and after the phase commit |
| Verified at exit | local = `origin/phase-1-symbolic` = `ls-remote`, working tree clean |
| Immutability baseline (555 files at entry) | `/home/user/p12ag_baseline_hashes.txt` |
| Manuscript set hash — entry | `a934223187f6e78effe1a5caa93e307808f5958f99911c571ba929194022aaec` |
| **Manuscript set hash — after P12AG** | **`243bb4d3d3d1ce5235e2d8d52bf6a095f8440b9d6accf4407dd640dedf35450e`** (one package line added to `ms.tex`) |
| Build | **0 errors · 0 undefined citations · 0 undefined references · 0 missing files · 34 pages**; overfull 613 (identical size multiset to the pre-repair tables) |
| Build PDF (workspace copy, not committed) | `/home/user/p12ag_manuscript_build.pdf` |
| Phase record | `paper9/audit/P12AG_CLEAN_BUILD_REPAIR_RECORD.md` |

## What changed

1. `paper9/latex/ms.tex` — one added line `\usepackage{ragged2e}` (the `\RaggedRight` column types used
   it but the preamble never declared it: 101 fatal undefined-control-sequence errors).
2. `paper9/tables/gen/tab06_convergence_floor.py`, `tab05_gap_summary.py` — malformed `\multicolumn`
   column specs `{@{l@{}` → `{@{}l@{` (tab06 ×2, tab05 ×2), restored missing content braces (tab05),
   removed a stray `}` and an extra `}` before a row terminator (tab06); outputs regenerated.
3. `paper9/tables/gen/tab02_parameters.py` — `sanitize_latex()` now escapes raw text-mode `_`/`^`
   outside `$…$`; `tab02_parameters.tex` regenerated (66 "Missing $ inserted" errors removed).
4. Five manuscript-set pins re-pointed to the post-repair hash (never loosened, each annotated).
5. New guards `paper9/verification/suite/test_p12ag_clean_build.py` (11, including a full build in a
   scratch tree) and this checkpoint + the phase record.

## Verification at exit

| Check | Result |
|---|---|
| Full suite | **345 passed, 1 skipped, 0 failed** (P12AF: 334/1) |
| Clean-build guard | passes: `pdflatex → bibtex → pdflatex×3` from repository sources, zero errors |
| Traceability / provenance | 18/18 closed, 0 open · register provenance PASS (A=0, B=3, C=2, D=0) |
| P12J final verification | 42/43 — the failure is the **mtime-ordering** check for Figure 5 (§6.3 of the phase record); no content is affected |
| Numerics | numeric-token digests of the three repaired tables identical before/after |
| P12AF content | `sec05_verification.tex` and `tab03_anchor_errors.tex` byte-identical |
| Statuses | B1 GRAPHICAL_VALIDATION/PASS · B2/B3 NOT_VALIDATED · B3 ESTABLISHED/SOURCE-EQUIVALENT · PCR1 NOT PASS · G3/G4 NOT MET · P5 NOT PASS/OPEN · R-1 OPEN · submission NOT AUTHORISED |

## Reported, not performed (each needs authorisation)

1. **Table 2 layout wrap** — the Status column is pushed off the printed page (pre-existing 173.2 pt
   overflow + 70.0 pt from the P12AF status labels). Fixing it is a cosmetic layout change.
2. **`tab03_anchor_errors.py` is stale** — running it emits the pre-P12AF table; the generated file was
   therefore left at the P12AF-authorised bytes. Reconciling generator with record is a scientific-record change.
3. **P12J figure check** — re-satisfying it honestly means regenerating Figure 5, and a test regeneration
   produced different bytes from the committed figure (matplotlib environment), so it was left untouched.
4. The other large pre-existing boxes (Table 4 782.05 pt, Table 7 251.57 pt, Table 1 214.16 pt).

## Next step

Unchanged from P12AF: closing B2/B3 requires the prepared author-data route (P12L/P12M — **NOT SENT, NOT
AUTHORISED**); the external hunt stays permanently closed; PCR1 remains the formal blocker; submission
remains prohibited.
