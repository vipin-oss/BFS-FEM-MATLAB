# RECOVERY CHECKPOINT — P12AD (pre-work)

**Phase:** P12AD — internal reconciliation and transition decision. Opened from the verified P12AC final
checkpoint `37f7186…` (tri-equal, clean tree). This file is the **pre-work** checkpoint; its final form is
written at the end of the phase.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Entry SHA (verified)** | **`37f71865b9414a25d915524bae2c32060c5536ae`** (P12AC final; local = origin = ls-remote; `porcelain` empty) |
| Baseline for immutability | `/home/user/p12ad_baseline_hashes.txt` — **546** tracked files at entry (content sha256) |
| Governing Blueprint | **v1.5** `b96c8e76…` — must remain byte-identical |
| Manuscript | `paper9/latex/ms.tex` `5422bc84…` + sections — must remain byte-identical (no edit in this phase) |
| 5i governing artefact | `paper9/verification/suite/p4b_5g_to_5i.json` `38384363…` (rate `4.173919246515192`) — must remain byte-identical |
| P5 headline artefact | `paper9/results/processed/p5_production_highlights.json` `ce28df21…` (commit `15814972…`, param_hash `09dd73f4…`) |
| Active benchmark record | `paper9/audit/benchmark_validation_record.json` `2fad2d92…` |
| Register | CSV `8d86528f…`; JSON `83ff8723…` |

## Scope declared before the decision

1. Record the scientific disposition unchanged: B1 `GRAPHICAL_VALIDATION`/`PASS`; B2 `NOT_VALIDATED` /
   source-limited; B3 `NOT_VALIDATED` / source-limited with formulation `ESTABLISHED / SOURCE-EQUIVALENT`;
   PCR1 `NOT PASS`; G3 `NOT MET`; G4 `NOT MET`. **Nothing is relabelled as PASS.**
2. Decide the **P5** internal reconciliation: which numerical production record is retained, and why; the
   decision is an internal production-record act and is **not** external benchmark validation.
3. Decide whether the specified **R-1** authorised rerun is necessary for the manuscript, or whether the
   existing reproducibility evidence suffices to retain the governing artefact with R-1 recorded as an
   internal governance item. No new numerical experiment; no change to the governing 5i value; no
   re-baseline.
4. Fix the **minimum explicit C-1 disposition** using the already-frozen Rule R-fit evidence where possible;
   the Rule R-fit text itself is not changed.
5. Produce the exact **manuscript limitation text** for B2/B3 — and **not** edit the manuscript.
6. Determine the **P13** transition: no claim that PCR1/G3/G4 passed; state exactly what the frozen gate
   architecture permits and the minimum authorised decision needed to enter final manuscript preparation.
7. Prove, by targeted regression/consistency checks, that this record alters no scientific result or gate.
8. Commit → push → fetch → verify local = origin = ls-remote; final checkpoint; clean tree.

## Explicitly not permitted in this phase

Author contact; author-request drafting or sending; further literature search; Blueprint v1.5 edits;
threshold changes; removal of B2/B3; fabricated benchmark percentages; changes to governing numerical
values; manuscript edits (STOP and report if an edit is found to be required by the governance rules);
any new benchmark-hunt phase; any metadata-only audit loop.

## Planned deliverables

* `paper9/audit/P12AD_INTERNAL_RECONCILIATION_DECISION.md` — the decision record (sections A–H).
* `paper9/verification/suite/test_p12ad_decision_record.py` — targeted consistency guards.
* this checkpoint (final form) at phase exit.

## Status at entry

Clean tree; no P12AD file exists yet; the P12AC decision record and all frozen artefacts are unmodified.
