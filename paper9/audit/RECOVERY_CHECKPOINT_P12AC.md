# RECOVERY CHECKPOINT — P12AC (pre-work)

**Phase:** P12AC — final scientific literature-resolution pass: candidate classification and the
formal recording of **Decision B** for the external benchmarks B2/B3. Opened after P12AB closed
(`5093c58…`, tri-equal, clean). This file is the **pre-work** checkpoint; its final form is written at
the end of the phase and records the phase SHAs.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Entry SHA (verified)** | **`5093c587a20d643c16f533f1458e8b52129265d6`** (P12AB final; local = origin = ls-remote; `git status --porcelain` empty) |
| Governing Blueprint | **v1.5** `b96c8e76…` CURRENT (unchanged); v1.4 `2ae0b1e8…` FROZEN / superseded |
| Active machine record | `paper9/audit/benchmark_validation_record.json` `2fad2d92…` |
| Register | CSV `8d86528f…`; JSON `83ff8723…` |
| Manuscript | 12 `.tex` under `paper9/latex/`, set hash `5ba2c22e…` |

## Scope declared before the audit

1. **One bounded literature resolution only.** No new audit-only phase, no metadata/reconciliation loop,
   no author contact, no author-data requests.
2. **B2/B3 replacement search, classification only.** Every candidate is classified
   **ACCEPTABLE** / **SUPPORTING ONLY** / **NOT COMPATIBLE**, with the exact reason. No forced matching,
   no parameter tuning, no percentage asserted for a graphical source.
3. **No framework movement.** No change to Blueprint v1.5, PCR1, G3, G4, Rule R-fit, any threshold, any
   validation route, any gate state or any numerical result.
4. **If no admissible replacement exists:** record the formal **Decision B** — *"B2/B3 remain
   source-limited and NOT_VALIDATED because the published sources do not provide sufficient
   authoritative parameter/curve information"* — and **stop the benchmark hunt permanently**.
5. **Path-forward determinations** (PCR1 satisfiability, manuscript limitation statement, P5 with B2/B3
   explicitly `NOT_VALIDATED`, R-1/C-1 independence, P13 entry under an authorised internal decision).
6. **Commit/push only if substantive.** Substantive = the Decision B record, the classification record,
   the evidence script/JSON and a guard test; nothing else may change.

## Planned deliverables

* `paper9/audit/P12AC_LITERATURE_RESOLUTION_DECISION_B.md` — classification table, LWZ2016 verification
  chain, retraction of the earlier Appendix-3 mismatch note, formal Decision B, path-forward answers,
  proposed manuscript limitation statement.
* `paper9/audit/evidence/p12ac/lwz_tm_equivalence_check.py` + `lwz_tm_equivalence_results.json` —
  rerunnable equivalence/digitisation evidence.
* `paper9/verification/suite/test_p12ac_decision_b.py` — guard.
* this checkpoint (final form) at phase exit.

## Status at entry

Clean tree; no phase files exist yet; the literature-resolution work of this pass so far exists only as
scratch under `/home/user/p12lit/` (outside the repository).
