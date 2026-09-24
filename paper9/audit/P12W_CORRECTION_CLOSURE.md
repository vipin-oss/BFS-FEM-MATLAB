# P12W — CORRECTION CLOSURE FOR P12V-F1 / P12V-F2 (final validation state)

**Phase:** P12W — text-only closure of the two findings that P12V reported but did not fix.
**Scope guard:** no scientific status, route, gate, overlay, evidence hash, provenance string or
numerical result may change; no tuning; no author contact; no Blueprint or manuscript edit;
P12U F1–F4 not reopened; P13 untouched.

| Field | Value |
|---|---|
| Entry SHA (verified) | `cbb26b52b7abeeb9cfc247bc6ba10978c96d697f` (local = origin = ls-remote; clean tree) |
| P12W pre-work checkpoint | `1f5cd5f4116a9793c05b1329afeaf6d81be2842c` (pushed and verified before any edit) |
| Correction commit | recorded in the P12W delivery report |
| Final recovery checkpoint | `paper9/audit/RECOVERY_CHECKPOINT_P12W.md` (final form) |
| Active record before | `paper9/audit/benchmark_validation_record.json` = `cdbfe6c2d7e0e19b98940815e4478c1c9a1a432f3ad1d4b4698b00349d451df3` (P12U content) |
| Active record after | `9ea0d4c8039b42c2644db3c679e3ff4b42b2a8a72b3977f6e54c1d301b718b51` |
| Frozen raw record | `paper9/audit/evidence/p12s/p12s_validation_record.json` = `cffc0c889c79186b34b0d3775191e181e040dfb358e4c61f6c06a7f22f5c3a21` (byte-identical, untouched) |

## P12V-F1 — `benchmarks.B3.reproduction_status`

**Defect (P12V report):** `"NOT REPRODUCED (lowest branch omega_bar(1) = 0.35 vs source's own
0.50)"` attributed the classical/literature level 0.50 to the source's own published curve — the
same conflation P12T raised (as F2) and P12U corrected inside `reason`.

**Corrected text (only this field):**

> NOT REPRODUCED (the source-formulation-equivalent reproduction -- repository layer matrix equal to
> the source's own Appendix 3 formulation [P0][G][P0]^-1, re-evaluated at 60/120 digits -- gives the
> lowest branch omega_bar ~= 0.3391 at k_bar = 1; P12T's reading of the same curve = 0.35) vs the
> published solid ('Present') gradient curve of Fig. 4(c) at ~0.433-0.436 there (own digitisation
> 0.433; P12T measurement 0.436); the exact classical limit 0.500 and the dashed literature [34]
> curve (~0.50) are separate quantities and are NOT the source's Present gradient value; the
> mismatch is source-side (the Fig. 4(c) parameter set/normalisation is unstated), not an
> implementation-formulation defect; no parameter was tuned

The three quantities are now distinguished in one field: **reproduced (source-formulation) ≈ 0.3391**
· **published solid "Present" gradient curve ≈ 0.433–0.436** · **classical limit 0.500 / dashed
literature [34] ≈ 0.50**. The superseded "0.50 = source's own" attribution is gone; the previously
recorded 0.35 reading is retained as P12T's reading of the same reproduced curve.

## P12V-F2 — `benchmarks.B3.ambiguity_status`

**Defect (P12V report):** `"SOURCE_UNAVAILABLE (dipolar-gradient formulation/coefficient convention
not pinned down)"` — superseded by the P12V formulation identity (repository matrix ≡ source
Appendix 3 to ~1e-16 at 60 digits; recorded bands reproduced).

**Corrected text (only this field):**

> UNRESOLVED -- NOT the formulation: the dipolar-gradient layer-matrix formulation is established as
> the source's own (repository matrix equal to the Appendix 3 [P0][G][P0]^-1 to ~1e-16 at 60 digits;
> the recorded bands are reproduced); the residual ambiguity is the source's unstated Fig. 4(c)
> parameter set/normalisation and exact curve data, with no inheritance of the Fig. 3(b) values
> assumed; B3 remains NOT_VALIDATED (the superseded formulation-attribution clause kept inside this
> record's frozen P12S-era 'reason' string is historical text, not the operative status)

It states (i) the formulation **is** the source's own, (ii) the residual is the missing Fig. 4(c)
configuration/normalisation/curve data, (iii) no Fig. 3(b) inheritance is assumed, (iv) B3 stays
`NOT_VALIDATED`. It does not upgrade anything and does not imply formulation ambiguity.

## Part C — propagation / consistency

* Repo-wide search for the two obsolete strings: **one occurrence each**, both inside
  `paper9/audit/benchmark_validation_record.json`; no other file (active record, evidence, results,
  scripts, tables, manuscript) contained them, so no cross-file propagation was needed.
* One **consequential** span inside the same active record carried the same superseded claim:
  `gate_state.blocker` read “B2 and B3 remain NOT_VALIDATED (source-side ambiguity / **unverifiable
  formulation**); gate definitions unchanged”. It contradicted the corrected F2 field, so it was
  closed under Part C's internal-contradiction rule:

  > B2 and B3 remain NOT_VALIDATED (source-side data gaps: B2 = unresolved caption geometry/length
  > scale; B3 = unstated Fig. 4(c) parameter set/normalisation and curve data -- the B3 formulation
  > itself is verified as the source's own Appendix 3); gate definitions unchanged

  No gate value changed (`PCR1 NOT PASS`, `G3 NOT MET`, `G4 NOT MET`, `P5 NOT PASS/OPEN`, `R-1 OPEN`,
  `PCR5 PASS`, `P13 BLOCKED` — untouched).
* **Frozen by design (not corrected, by rule):** the P12S-era `reason` strings, including the clause
  “the unresolved question (which dipolar-gradient formulation / coefficient convention the source
  used) is a SOURCE_UNAVAILABLE item”. That string is pinned byte-identical between the active record
  and the raw P12S/P12U record by the P12U guards
  (`test_record_b3_reason_matches_the_corrected_script_output`), and P12W may not alter P12U records
  or weaken existing tests. The corrected `ambiguity_status` therefore flags it explicitly as
  historical text and not the operative status.
* **Historical audit documents untouched:** `P12V_B2_B3_SOURCE_AUDIT.md` still quotes both defects as
  findings (F1/F2 reported, not silently fixed at the time); P12S/P12T/P12U audits and checkpoints
  unchanged; nothing rewritten retrospectively.

## Tests (Part D)

New `paper9/verification/suite/test_p12w_correction_closure.py` (12 guards): the three-quantity
distinction in `reproduction_status`; absence of the obsolete conflation in the active record;
preservation of the historical finding in the P12V audit; the four F2 requirements; the frozen-reason
flagging; the closed `gate_state.blocker` clause; B1/B2/B3 statuses unchanged; route/gate/number/
hash/provenance invariants; the record content pin; the frozen raw record; the P12U
reason-equality surface. `test_p12v_source_audit.py` keeps its exact-content pin, re-pointed to the
intentionally corrected record (documented in the test docstring) — no guard weakened, no test
deleted.

## Status at exit (unchanged)

| Item | Status |
|---|---|
| B1 | `GRAPHICAL_VALIDATION` / PASS |
| B2 | `NOT_VALIDATED` / ambiguity `UNRESOLVED` |
| B3 | `NOT_VALIDATED` |
| `quantitative_error` | `[NULL, NULL, NULL]` |
| PCR1 / G3 / G4 | NOT PASS / NOT MET / NOT MET |
| P5 / R-1 / PCR5 | NOT PASS, OPEN / OPEN / PASS |
| P13 | BLOCKED |
| Manuscript | unchanged (0 diffs) |
| Blueprint | v1.5 `b96c8e76…` unchanged |
| Author requests | NOT SENT; drafts unmodified; no contact; PI decision PENDING |
