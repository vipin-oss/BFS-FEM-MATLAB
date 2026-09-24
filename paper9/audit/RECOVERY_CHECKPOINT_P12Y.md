# RECOVERY CHECKPOINT — P12Y (final)

**Phase:** P12Y — traceability / governance cleanup audit of the two P12X follow-up findings.
One byte-minimal correction applied (**P12X-F1**); **P12X-F2** closed as historical-only, no
correction. No scientific state, gate, threshold or number changed.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Entry SHA (verified)** | **`7e74063aa452ef6275a1493e5a85cc06b276dcdb`** (P12X final; local = origin = ls-remote, clean tree) |
| **P12Y pre-work checkpoint** | **`798c0132c456f190349b3e84a63b509e2c1e3961`** (pushed + verified before any edit) |
| **P12Y audit / correction commit** | **`9b322922ddc3d00fdc2877e22cab54ae2e561e6d`** — “P12Y: traceability cleanup -- TV1 class synced to authoritative [S] + 15 F1/F2 guards” |
| **P12Y final checkpoint (this file)** | recorded in the P12Y delivery report |
| **Verified remote SHA** | pushed and re-verified (local = `origin/phase-1-symbolic` = `ls-remote`) |
| Tree at exit | clean (`git status --porcelain` empty) |
| Governing Blueprint | **v1.5** `b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91` (unchanged); v1.4 `2ae0b1e8…` frozen |
| Register before / after | `0b508bf7f15dc532b553b951382deaf315e38ebd33ecd5b5d765163bd3f49d38` → `4ce06f024bf41f12688998fd26c2861cf04dd9adaefbab93213d48698e573b04` |

## Dispositions

| Finding | Disposition | Basis |
|---|---|---|
| **P12X-F1** `traceability_matrix.csv` TV1 `CLOSED [C]` vs authoritative `CLOSED [S]` | **CORRECTION REQUIRED → CLOSED** | Genuine stale **active** register value: the CSV's TV rows were written at `c150c0d` (06:13) *before* the P11D retag commit `df7e26c` (09:12) and never re-synced; the register is cited as current by the master plan, the P10 governance records, the stage-1 blocker audit and the P8/P9 release audits. Brackets are the Blueprint v1.5 provenance classes “[C] cited / [A] analytically defined / [S] assumed-with-justification”. Correction = **status cell only** |
| **P12X-F2** `P12N` cites “authoritative Blueprint v1.4 (line 457 …)” | **HISTORICAL-ONLY / NO CORRECTION** | The citation sits in P12N's “Package consistency audit (read-only; **performed in this phase**)” — a statement of the state at its time — which the governing A2 amendment itself classifies so (“`P12K…Q*` remain valid as statements of the state *at their time*”, §5). `P12L` blocker record and `P12O` carry the same historical framing. Threshold substance unchanged: both frozen copies contain the same percent-value set `{0.5, 2, 40, 95}` and v1.5 states the quantitative criterion/thresholds unchanged; `PROVENANCE.md` declares v1.5 **CURRENT governing specification** and v1.4 **FROZEN, superseded**; the machine record's `governing_spec` = v1.5 |
| **P12Y-F3** (new observation, not corrected) | reported | The claim register's latest blueprint row is the P12H A1 row `BP-v1.4`; there is no A2/v1.5 row (A1 itself received four rows). Completeness gap only — no false statement; v1.5 is registered in `PROVENANCE.md`, the P12R amendment record and the machine record. Adding amendment rows is a content addition beyond this phase's minimal-correction rule |

## Exact files changed by P12Y

| File | Change |
|---|---|
| `paper9/audit/traceability_matrix.csv` | **1 line**: TV1 status cell `CLOSED [C]` → `CLOSED [S]` (note cell byte-identical; hash of the file with the TV1 line removed unchanged at `0407f460…`) |
| `paper9/verification/suite/test_p12y_traceability_cleanup.py` | **new** — 15 F1/F2 guards |
| `paper9/audit/P12Y_TRACEABILITY_GOVERNANCE_CLEANUP.md` | **new** — the audit record (Parts A–I) |
| `paper9/audit/RECOVERY_CHECKPOINT_P12Y.md` | **new** — pre-work version (`798c013`), now final |

Not changed: Blueprint v1.4/v1.5, `PROVENANCE.md`, Rule R-fit, manuscript, production/results/tables,
analytic sources and source PDFs, P12S/T/U/V evidence, raw P12S/P12U records, author-request
drafts/specification, `benchmark_validation_record.json`, `P12N`/`P12L`/`P12O`/`P12Q`, the JSON
traceability matrix.

## Regression counts

| Run | Result |
|---|---|
| P12Y guards | **15 passed** |
| targeted (P12Y + X + W + V + U + S + R) | **105 passed** |
| P12T independent-checks script (standalone) | 24 assertions: **15 True / 9 False**, output identical to the committed P12T record (the 9 = the eight extractor artefacts P12T documented + their aggregate flag) |
| named governance guards (P12C + P12H ×2 + P12R + P12S + P12U + P12V + P12W + P12X + P12Y) | **150 passed** (135 before P12Y) |
| full suite | **231 passed, 1 skipped** (216P/1S before) |
| P12J cross-check | **43 / 43** |

## Immutability result

524 tracked files compared with the entry snapshot → **exactly 1 changed** (`traceability_matrix.csv`,
the authorised correction) plus the three P12Y artifacts (checkpoint, audit record, guard suite). Byte-identical: Blueprint v1.5/v1.4,
`PROVENANCE.md`, Rule R-fit, manuscript (13 `.tex`, set hash `5ba2c22e…`), production (17), results
(32), tables (15), analytic sources (12), validation (19), P12S/T/U/V evidence (34), raw P12S/P12U
record `cffc0c88…`, `plan/blueprint/` (5). No numerical result, route, gate or threshold changed; no
source-evidence classification upgraded (TV1 moved **down** to the retagged class).

## Current gate states (unchanged)

| Item | State |
|---|---|
| B1 | `GRAPHICAL_VALIDATION` / PASS |
| B2 | `NOT_VALIDATED` / ambiguity `UNRESOLVED` |
| B3 | `NOT_VALIDATED`; `formulation_status = ESTABLISHED / SOURCE-EQUIVALENT` |
| `quantitative_error` | `[NULL, NULL, NULL]` (no `%` anywhere in the B1/B2/B3 blocks) |
| PCR1 / G3 / G4 | NOT PASS / NOT MET / NOT MET |
| P5 / R-1 / PCR5 | NOT PASS, OPEN / OPEN / PASS |
| P13 | BLOCKED |
| Manuscript | unchanged; author requests **NOT SENT** / NOT AUTHORIZED; PI decision PENDING |
