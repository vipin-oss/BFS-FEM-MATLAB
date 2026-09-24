# RECOVERY CHECKPOINT — P12W (pre-work)

**Phase:** P12W — correction closure for the two residual P12V text findings
(**P12V-F1** = `benchmarks.B3.reproduction_status` conflation "source's own 0.50";
**P12V-F2** = `benchmarks.B3.ambiguity_status` wording superseded by the verified
formulation identity). Text-only correction; no scientific status, route, gate or
numerical result may change.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Starting SHA (entry, verified)** | **`cbb26b52b7abeeb9cfc247bc6ba10978c96d697f`** (P12V final checkpoint) |
| Entry verification | `git fetch` OK; local `HEAD` = `origin/phase-1-symbolic` = `ls-remote` = `cbb26b52…`; `git status --porcelain` empty |
| **P12W pre-work checkpoint (this file)** | recorded in the P12W delivery report |
| Governing Blueprint | **v1.5** `b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91` (unchanged) |
| Authoritative sources | li2024 `2ac5f45d77ee37569f69e8890b70200ae6982f669ecaccf6cb5aa162f0340513`; li2023 `3f5103380302609ef2dfe76c8ade09cae79b2ebbd4fdb4da228576c331191aa7` |
| Active machine record, content hash **before** correction | `cdbfe6c2d7e0e19b98940815e4478c1c9a1a432f3ad1d4b4698b00349d451df3` (`paper9/audit/benchmark_validation_record.json`) |
| Raw P12S/P12U record (frozen) | `cffc0c889c79186b34b0d3775191e181e040dfb358e4c61f6c06a7f22f5c3a21` (`paper9/audit/evidence/p12s/p12s_validation_record.json`) |

## Exact target strings to be corrected (recorded before edit)

* F1 — `paper9/audit/benchmark_validation_record.json` line 154:
  `"reproduction_status": "NOT REPRODUCED (lowest branch omega_bar(1) = 0.35 vs source's own 0.50)"`
* F2 — same file, `benchmarks.B3.ambiguity_status`:
  `"SOURCE_UNAVAILABLE (dipolar-gradient formulation/coefficient convention not pinned down)"`

Repo-wide search for the two strings: **one occurrence each**, both inside
`benchmark_validation_record.json` (F1 also recorded, as a finding, in the P12V audit file —
historical, not corrected).

## Planned edit surface (declared before work)

1. `paper9/audit/benchmark_validation_record.json` — the two fields only (F1, F2); all other
   fields, numbers, hashes and gates preserved.
2. `paper9/verification/suite/test_p12v_source_audit.py` — the P12V content-pin of the active
   record (`cdbfe6c2…`) re-pointed at the corrected content, because P12W intentionally edits
   that record; the guard keeps its exact-content strictness.
3. `paper9/verification/suite/test_p12w_correction_closure.py` — new targeted F1/F2 guards.
4. `paper9/audit/P12W_CORRECTION_CLOSURE.md`, `paper9/audit/RECOVERY_CHECKPOINT_P12W.md` (this
   file, final form) — closure records.

Not touched: Blueprint v1.5, manuscript, source PDFs, P12S/P12U records and evidence, P12V
evidence (digitisation, formulation identity), P12V audit file (historical), production /
validation numbers, author-data drafts. Frozen P12S-era `reason` strings stay byte-identical
(guarded by P12U); the corrected **status** fields are the operative wording.

## Status at entry (must be unchanged at exit)

| Item | Status |
|---|---|
| B1 | `GRAPHICAL_VALIDATION` / PASS |
| B2 | `NOT_VALIDATED` / ambiguity `UNRESOLVED` |
| B3 | `NOT_VALIDATED` |
| `quantitative_error` | `[NULL, NULL, NULL]` |
| PCR1 / G3 / G4 | NOT PASS / NOT MET / NOT MET |
| P5 / R-1 / PCR5 | NOT PASS, OPEN / OPEN / PASS |
| P13 | BLOCKED |
| Manuscript | unchanged; author contact NONE; requests NOT SENT and unmodified |
