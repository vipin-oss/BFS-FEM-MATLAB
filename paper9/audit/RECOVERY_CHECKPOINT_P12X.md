# RECOVERY CHECKPOINT — P12X (final)

**Phase:** P12X — final governance / gate-state audit after the P12W correction closure.
Outcome: **CORRECTIONS REQUIRED → one record correction applied** (additive `formulation_status`
field; no data, gate, route or number changed). Audit-only otherwise.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Entry SHA (verified)** | **`f68eb7c0d70c90c14087d76d225c3ac053352cf4`** (P12W final; local = origin = ls-remote, clean tree) |
| **P12X pre-work checkpoint** | **`5a84fc93457e16d61cf4a7288be1c4ce41407083`** (pushed + verified before any edit) |
| **P12X audit / correction commit** | **`b5e1ba263d805819cc1b6be46bfe229b02a9b9fd`** — “P12X: governance consistency audit -- B3 formulation_status field + 25 governance guards” |
| **P12X final checkpoint (this file)** | recorded in the P12X delivery report |
| **Verified remote SHA** | pushed and re-verified (local = `origin/phase-1-symbolic` = `ls-remote`) |
| Tree at exit | clean (`git status --porcelain` empty) |
| Governing Blueprint | **v1.5** `b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91` (unchanged) |
| Rule R-fit | `d4fed492…` (unchanged) |
| Active machine record | `9ea0d4c8039b42c2644db3c679e3ff4b42b2a8a72b3977f6e54c1d301b718b51` → **`2fad2d92a07eadf4f00fbb952e983bd897984d5579711052c7c0deafe72672d2`** |
| Frozen raw P12S/P12U record | `cffc0c889c79186b34b0d3775191e181e040dfb358e4c61f6c06a7f22f5c3a21` (byte-identical) |

## Exact files changed by P12X

| File | Change |
|---|---|
| `paper9/audit/benchmark_validation_record.json` | **+1 line**: added `benchmarks.B3.formulation_status` (ESTABLISHED / SOURCE-EQUIVALENT; retires the frozen `reason` clause at field level; names the residual data gap). Verified as the only leaf difference |
| `paper9/verification/suite/test_p12x_governance_consistency.py` | **new** — 25 governance-consistency guards |
| `paper9/verification/suite/test_p12v_source_audit.py` | content pin re-pointed to the corrected record (docstring records both corrections) |
| `paper9/verification/suite/test_p12w_correction_closure.py` | content pin re-pointed (docstring records the additive P12X field) |
| `paper9/audit/P12X_GOVERNANCE_CONSISTENCY_AUDIT.md` | **new** — the audit (Parts A–J, classification table, findings) |
| `paper9/audit/RECOVERY_CHECKPOINT_P12X.md` | **new** — pre-work version (`5a84fc9`), now final |

## Governance verdict

* **Verdict:** `CORRECTIONS REQUIRED` → corrected (one additive record field; no other change).
* **Stale active contradictions found:** yes — 1 substantive: the active record's B3 block carried
  no explicit machine-readable formulation status, so the superseded clause inside the frozen
  P12S-era `reason` string remained readable as an operative claim. It cannot be rewritten (Part G:
  raw P12U records byte-identical; no guard may be weakened) and is retired at field level instead.
* **Findings reported, not corrected:** `P12X-F1` `traceability_matrix.csv` TV1 reads `CLOSED [C]`
  (authoritative JSON: `CLOSED [S]`); `P12X-F2` `P12N` cites Blueprint v1.4 line numbers (v1.5
  governs; thresholds unchanged). Neither touches a gate, route, status or number.

## B3 formulation vs validation (not conflated)

| Item | State |
|---|---|
| B3 formulation | **ESTABLISHED / SOURCE-EQUIVALENT** (Appendix 3 `[P0][G][P0]⁻¹` ≡ repository matrix ~1e-16 at 60 digits; bands reproduced at 0.3391 / 1.021) |
| B3 validation | **NOT_VALIDATED** (residual = source's unstated Fig. 4(c) parameter set / normalisation / curve data; no Fig. 3(b) inheritance treated as authoritative) |
| Curve identities | reproduced ≈ 0.3391 · published solid “Present” ≈ 0.433–0.436 · classical 0.500 / dashed [34] ≈ 0.50 — distinct in `reproduction_status` |

## Status at exit (unchanged)

| Item | Status |
|---|---|
| B1 | `GRAPHICAL_VALIDATION` / PASS |
| B2 | `NOT_VALIDATED` / ambiguity `UNRESOLVED` |
| B3 | `NOT_VALIDATED` |
| `quantitative_error` | `[NULL, NULL, NULL]` (no `%` anywhere in the B1/B2/B3 blocks) |
| **PCR1 / G3 / G4** | **NOT PASS / NOT MET / NOT MET** |
| **P5 / R-1 / PCR5** | **NOT PASS, OPEN / OPEN / PASS** |
| **P13** | **BLOCKED** |
| Manuscript | unchanged (13 `.tex` files byte-identical; set hash `5ba2c22e…`) |
| Author requests | **NOT SENT** / NOT AUTHORIZED; drafts + spec byte-identical (`2f68e66f…`, `8acb70f1…`); no contact; PI decision PENDING |

## Verification performed

* new P12X guards → **25 passed**;
* targeted (P12X + P12W + P12V + P12U + P12S + P12R) → **90 passed**;
* named guard files (P12C + P12H ×2 + P12R + P12S + P12U + P12V + P12W + P12X) → **135 passed**
  (110 before P12X);
* full regression suite `paper9/verification/suite` → **216 passed, 1 skipped** (191P/1S before);
* P12J cross-check → **43 checks passed, 0 failed**;
* immutability → 521 tracked files compared with the entry snapshot: **exactly 3 changed** (the
  record correction plus the two re-pointed pins); Blueprint v1.5, Rule R-fit, manuscript,
  production, results, tables, analytic sources, P12S/T/U/V evidence and all P12 audit documents
  byte-identical; raw P12S/P12U record untouched;
* no production numerical result changed; no gate, route or status altered; no parameter tuned; no
  author contact; P12U/P12V findings not reopened.
