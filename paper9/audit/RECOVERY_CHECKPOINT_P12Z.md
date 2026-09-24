# RECOVERY CHECKPOINT — P12Z (final)

**Phase:** P12Z — traceability register current-version / A2 governance audit (P12Y-F3 disposition).
**Decision: A — `NO CORRECTION — CURRENT TRACEABILITY SUFFICIENT`.** No register row added, no existing
row edited, no file outside the P12Z artifacts touched. No scientific state, gate, threshold, route or
number changed.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Entry SHA (verified)** | **`cb6a4c61041716345381e988c337290b85b5640a`** (P12Y final; local = origin = ls-remote, clean tree) |
| **P12Z pre-work checkpoint** | **`316f0d68556ae8709acf2f87bf697c19c754378c`** (pushed + verified before any edit) |
| **P12Z audit commit** | **`f9fa162d7cdec3b9ad5b6f03f4525ee462a6a390`** — “P12Z: register current-version / A2 governance audit -- decision A (no correction; v1.5/A2 traceable via PROVENANCE + machine record) + 17 guards” |
| **P12Z final checkpoint** | the commit carrying this file (its own SHA is stated in the P12Z delivery report — a commit cannot contain its own hash) |
| **Verified remote SHA** | pushed and re-verified (local = `origin/phase-1-symbolic` = `ls-remote`) |
| Tree at exit | clean (`git status --porcelain` empty) |
| **Decision** | **A** — no correction; the absence of a dedicated `BP-v1.5/A2` register row is a register-design/practice choice that creates no loss of traceability |
| Register at entry and exit | `traceability_matrix.csv` `4ce06f024bf41f12688998fd26c2861cf04dd9adaefbab93213d48698e573b04`; `traceability_matrix.json` `f332e03117b60643ecd901d64c585d3accac401b55c7bca54054d5bff1118b6f` (**byte-identical; no row added**) |
| Governing Blueprint | **v1.5** `b96c8e76…` (CURRENT, unchanged); v1.4 `2ae0b1e8…` (FROZEN, superseded, unchanged) |

## Decision basis

* **Schema** (`paper9/audit/README.md`; master plan §K): the register maps claim → figure/table →
  processed → raw → run manifest → code → equation → parameters, with rows appended by the phase that
  locks the claim (the `phase` column). No rule requires a row per governing blueprint revision; the
  register's own `BP-v1.3` row cites `paper9/plan/blueprint/PROVENANCE.md` as its derivation document —
  the authoritative version ledger.
* **Version chain** (P12R additive block in `PROVENANCE.md`): v1.5 `b96c8e76…` **CURRENT governing
  specification**; v1.4 `2ae0b1e8…` **FROZEN, superseded by v1.5; byte-identical since creation**; the
  file itself declares the older rows stale-but-deliberately-unedited (the register's `BP-v1.4` row is
  the same point-in-time convention, phase-stamped `P12H`).
* **Machine identifiability**: `paper9/audit/benchmark_validation_record.json` →
  `governing_spec = "Paper9_Blueprint v1.5 (A2 graphical-validation route)"` (the only machine record
  carrying the field).
* **A2 chain**: v1.5 §13 (`\section{AMENDMENT A2 …}`, A2.1–A2.8, the three evidence states);
  `BLUEPRINT_V1_5_GRAPHICAL_VALIDATION_AMENDMENT.md` `c008a00e…` (eight-block delta, “no gate moves
  because A2 exists”, thresholds unchanged, historical records classified not rewritten);
  `benchmark_validation_route.py` `c5b26190…` (fixed identifiers, thresholds 2.0 / 0.5 restated);
  `test_p12r_graphical_validation_route.py` `8e83d16e…`; B1 `GRAPHICAL_VALIDATION`/PASS, B2/B3
  `NOT_VALIDATED` in the machine record.
* **No loss of traceability** in any of the six required links (B1 graphical; B2 ambiguity; B3
  source-data insufficiency; `quantitative_error` NULL policy; A2 graphical tier; machine-identifiable
  governing spec). Adding a row would be a completeness addition, not a fix — none was made.

## Reported, not corrected (recorded for a separately authorised cleanup)

| ID | Observation |
|---|---|
| **P12Z-O1** | The `BP-v1.4` row (and the JSON `p12h_amendment.blueprint.v1.4_sha256`) cite `0089754b076ff9e3…` — the **P12H-time** v1.4 hash; the frozen v1.4 file is `2ae0b1e8f37e10a0…` after the P12J C1 correction. Authoritative current hash is registered in `PROVENANCE.md`; the row is consistent with the P12H audit it cites |
| **P12Z-O2** | The `PLAN-5i` row (and JSON `p12h_amendment.plan.sha256`) cite the plan's post-amendment hash `a45a5448a76764d5…`, which matches **no reachable revision** of `paper9/plan/CALC_MASTER_PLAN.md` (pre-amendment `0e2c3a3a…` verified at `fb9bd5d`; the amended file = `1f1c080b…` at `dd42e81` and at HEAD; no CRLF/LF/newline or progressive-reconstruction variant reproduces it). The artifact itself is intact; the citation is a P12H-era bookkeeping error. Not corrected (historical row; outside the A2 decision) |
| **P12Z-O3** | Three TV rows differ from the JSON **only in the state word** (`TV6` `PARTIAL [S]` vs `LOCKED [S]`; `TV14`/`TV18` `CLOSED [S]` vs `LOCKED [S]`); provenance class `[S]` agrees in every case — no provenance conflict, no gate implication, not rewritten |

## Exact changed files

| File | Change |
|---|---|
| `paper9/audit/P12Z_REGISTER_CURRENT_VERSION_AUDIT.md` | **new** — the audit record (Parts A–K) |
| `paper9/verification/suite/test_p12z_register_current_version.py` | **new** — 17 governance guards |
| `paper9/audit/RECOVERY_CHECKPOINT_P12Z.md` | **new** — this checkpoint (pre-work form `316f0d6`, final form here) |

Nothing else changed: register CSV/JSON, Blueprint v1.4/v1.5, `PROVENANCE.md`, the A2 amendment record,
Rule R-fit, manuscript, production/results/tables, analytic sources, validation assets, source PDFs,
P12S–P12Y evidence, raw P12S/P12U records, author-request drafts/specification, machine records.

## Regression counts

| Run | Result |
|---|---|
| P12Z guards | **17 passed** |
| targeted (P12Z + Y + X + W + V + U + S + R) | **122 passed** |
| named governance guards (P11D, P12A, P12B, P12C ×3, P12H ×2, P12R, P12S, P12U, P12V, P12W, P12X, P12Y, P12Z) | **196 passed** (150 before P12Z) |
| full suite `paper9/verification/suite` | **248 passed, 1 skipped** (231P/1S before) |
| `paper9/audit/check_traceability.py` | 18/18 TVs CLOSED / LOCKED — “100 % of Technical Variations are formally CLOSED and verified” |
| P12J cross-check | **43 / 43** |
| P12T standalone independent-checks script | 24 assertions: **15 True / 9 False**, output byte-identical to the committed P12T record (the 9 = the extractor artefacts P12T documented + their aggregate flag) |

No test weakened, relaxed or deleted; the P12Y guard that pins the absence of a `BP-v1.5` row remains
in force (and was re-verified).

## Immutability result

`/home/user/p12z_baseline_hashes.txt` (527 tracked files at entry) → **0 tracked files changed**;
1 new tracked file (`RECOVERY_CHECKPOINT_P12Z.md`, added by this phase) plus the two untracked P12Z
artifacts at commit time. Byte-identical groups: `paper9/plan/blueprint/` (5), `paper9/latex/` (13),
`paper9/production/` (17), `paper9/results/` (32), `paper9/tables/` (15), `paper9/analytic/` (12),
`paper9/validation/` (19), `paper9/audit/evidence/p12s|p12t|p12u|p12v|p12h/`, `paper9/sources/` (7),
`paper9/verification/suite/` (34 at entry), `paper9/audit/` (258 at entry). No numerical result, route,
gate or threshold changed; no source-evidence classification upgraded.

## Current gate states (unchanged)

| Item | State |
|---|---|
| B1 | `GRAPHICAL_VALIDATION` / PASS |
| B2 | `NOT_VALIDATED` / ambiguity `UNRESOLVED` |
| B3 | `NOT_VALIDATED`; `formulation_status = ESTABLISHED / SOURCE-EQUIVALENT` |
| `quantitative_error` | `[NULL, NULL, NULL]` |
| PCR1 / G3 / G4 | NOT PASS / NOT MET / NOT MET |
| P5 / R-1 / PCR5 | NOT PASS/OPEN / OPEN / PASS |
| P13 | BLOCKED |
| Manuscript | unchanged (byte-identical) |
| Author requests | NOT SENT / NOT AUTHORIZED; PI decision PENDING |
