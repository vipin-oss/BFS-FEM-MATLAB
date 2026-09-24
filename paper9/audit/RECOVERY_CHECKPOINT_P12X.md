# RECOVERY CHECKPOINT — P12X (pre-work)

**Phase:** P12X — final governance / gate-state audit after the P12W correction closure. Audit-only:
the phase asks whether every **active operative record** agrees that (i) B1 is
`GRAPHICAL_VALIDATION/PASS`, (ii) B2 is `NOT_VALIDATED` for source ambiguity, (iii) B3 is
`NOT_VALIDATED` for **missing source parameter/normalisation/curve data while its formulation is
established**, and (iv) no gate was promoted.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Starting SHA (entry, verified)** | **`f68eb7c0d70c90c14087d76d225c3ac053352cf4`** (P12W final checkpoint) |
| Entry verification | `git fetch` OK; local `HEAD` = `origin/phase-1-symbolic` = `ls-remote`; `git status --porcelain` empty |
| **P12X pre-work checkpoint (this file)** | recorded in the P12X delivery report |
| Governing Blueprint | **v1.5** `b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91` (unchanged) |
| Active machine record | `paper9/audit/benchmark_validation_record.json` = `9ea0d4c8039b42c2644db3c679e3ff4b42b2a8a72b3977f6e54c1d301b718b51` (P12W-corrected) |
| Frozen raw P12S/P12U record | `paper9/audit/evidence/p12s/p12s_validation_record.json` = `cffc0c889c79186b34b0d3775191e181e040dfb358e4c61f6c06a7f22f5c3a21` |
| Authoritative sources | li2024 `2ac5f45d…`; li2023 `3f510338…` |

## State to be verified (unchanged at exit)

| Item | Required state |
|---|---|
| B1 | `GRAPHICAL_VALIDATION` / PASS |
| B2 | `NOT_VALIDATED` / ambiguity `UNRESOLVED` / `quantitative_error` NULL |
| B3 | `NOT_VALIDATED` / formulation **established (source-equivalent)** / `quantitative_error` NULL |
| PCR1 / G3 / G4 | NOT PASS / NOT MET / NOT MET |
| P5 / R-1 / PCR5 | NOT PASS, OPEN / OPEN / PASS |
| P13 | BLOCKED |
| Author requests | drafts only; NOT SENT; no contact; PI decision PENDING |

## Off-limits this phase

Blueprint v1.5, manuscript, source PDFs, production/results/tables/validation data, P12S/T/U/V
evidence and records, historical P12U/P12V findings, author-data drafts, gate definitions. No new
validation route; no numerical change; no reopening of P12U/P12V findings.

Repository baseline hash snapshot: `/home/user/p12x_baseline_hashes.txt` (521 tracked files).
