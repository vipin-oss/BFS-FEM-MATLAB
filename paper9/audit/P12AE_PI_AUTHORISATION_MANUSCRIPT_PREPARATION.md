# P12AE — PI AUTHORISATION RECORD: CONTROLLED MANUSCRIPT PREPARATION

**Status: GRANTED — decisions A–F — recorded 2026-09-24 (recording provenance in the signature block).**
In force from the recording date.
**This record made no manuscript edit.** It is the authorisation instrument; the scoped editing it
authorises (decision B) is performed by the phase that recorded the grant (P12AF). Before the recording,
P13 remained `BLOCKED` and no manuscript byte could change.

**Prepared by:** P12AE (internal authorisation-preparation phase) · **Branch:** `phase-1-symbolic`
· **Entry:** P12AD final checkpoint `8d93d3f`, HEAD `cd5fa0c` (verified tri-equal, clean)
· **P12AE pre-work checkpoint:** `347ef73`.

**Recording history.** Before 2026-09-24 no explicit PI approval for this transition existed in the
repository: `P12Q_PI_DECISION_HANDOFF.md` §2 (Option A/B **neither selected**; "The agent does not select
either option"), `P12P_ACTION_GATE.md` ("No explicit PI authorization to send exists in the repository"),
`P12AD` §F (the transition "may begin only under an explicit PI authorisation recorded as an internal
preparation act"), and no repository record containing an approved P13-transition or manuscript-editing
decision. The grant was then conveyed by the PI as an explicit instruction in the project context and
recorded on 2026-09-24 (see the signature block). This paragraph is retained as the pre-grant history of
the instrument.

---

## The authorisation (decisions A–F)

### A. P13 manuscript-preparation transition — PREPARATION ONLY

> **AUTHORISE P13 MANUSCRIPT-PREPARATION TRANSITION ONLY. This does NOT mean PCR1, G3, or G4 has passed.
> It does NOT authorise submission.**

Granting (A) permits the project to enter the final manuscript-preparation stage as an internal
preparation act. It promotes no gate, changes no status, and confers no submission right.

### B. Manuscript editing — scoped and bounded

Granting (B) authorises the manuscript editing required to:

1. **insert the approved B1/B2/B3 limitation statement** — the text recorded in P12AD §E and reproduced
   verbatim in the Annex below;
2. **perform the required A2 manuscript re-tiering** — the Blueprint v1.5 §A2.8 obligation that the
   manuscript's validation wording "must later be re-tiered to match the state actually achieved", using
   the prepared impact list `P12S_MANUSCRIPT_IMPACT.md` (J.1–J.5);
3. **preserve B2 and B3 as `NOT_VALIDATED`** — they must not be promoted, softened or described as
   validated by any wording;
4. **preserve the B3 formulation status as `ESTABLISHED / SOURCE-EQUIVALENT`** — stated as a
   formulation-consistency finding and explicitly **not** as a validation;
5. **state explicitly that no numerical agreement value and no error percentage is claimed for B2/B3**
   (A2.5: graphical agreement must never be converted into a numerical error);
6. **state that the limitation is due to source-data / parameter availability, not evidence of solver
   failure.**

**Scope of the authorised edit (nothing outside this list may change):**

| Target | Permitted edit |
|---|---|
| `paper9/latex/sections/sec05_verification.tex` | the B1/B2/B3 paragraphs, the Evidence-Hierarchy Declaration, and the Fig. 4 caption wording — re-tiered to the state actually achieved, plus insertion of the Annex limitation statement |
| `paper9/tables/out/tab03_anchor_errors.tex` | the benchmark status cells only (B1 → graphical-route status per A2.2; B2, B3 → `NOT_VALIDATED`) |
| everything else | **unchanged** — no other section, no abstract/introduction/conclusion sentence, no figure data, no table number |

**Bound** within the edit: no percentage, ratio or "agreement" figure may be introduced anywhere; no
gate sentence may change except to keep Gate G3 formally `NOT MET`; no production number, parameter,
classification or threshold may change; the edit is byte-minimal and reviewed against this list.

### C. P5 — preserved exactly as P12AD recorded it

Granting (C) preserves, without change:

* the **retained numerical production record = the Part A matrix**
  (`paper9/results/raw/p5_production_raw.json` + `paper9/results/processed/p5_production_highlights.json`,
  commit `15814972…`, `param_hash 09dd73f4…`) — the record question decided in P12AD §B;
* **the P5 PASS gate sentence is NOT adopted**;
* **P5 remains `NOT PASS/OPEN`** until separately authorised; `paper9/audit/P5_STATUS.md` stays
  byte-unchanged, including its "Branch-level P5 gate: CONTESTED" wording.

### D. R-1 — preserved exactly

Granting (D) preserves R-1 as **`OPEN` as an internal governance item**; **no rerun and no re-baseline is
authorised by this phase**. The governing 5i artefact, its rate `4.173919246515192`, its CI and `ε_Δ` stay
byte-identical. The specified P12AB Part E re-execution remains available only under a separate
authorisation.

### E. C-1 — preserved exactly

Granting (E) preserves C-1 as **closed as a criterion item under the frozen Rule R-fit** (F = 3 strict,
adopted under A1), with the residual estimator/Blueprint model defect documented as a limitation. **No
amendment to Rule R-fit** is made or authorised; the P1–P4 predicate set remains non-governing.

### F. Non-satisfaction statement (mandatory in any granting of this instrument)

> **This authorisation permits controlled manuscript preparation only. It does not constitute PCR1, G3, or
> G4 satisfaction and does not authorise submission.**

---

## What this authorisation does NOT do

| Item | State after granting (unchanged) |
|---|---|
| PCR1 | **NOT PASS** |
| G3 | **NOT MET** |
| G4 | **NOT MET** |
| P5 | **NOT PASS/OPEN** |
| R-1 | **OPEN** |
| PCR5 | **PASS** (unchanged) |
| C-1 | closed as a criterion item; Rule R-fit unamended |
| B1 / B2 / B3 | `GRAPHICAL_VALIDATION` / PASS · `NOT_VALIDATED` · `NOT_VALIDATED` (formulation `ESTABLISHED / SOURCE-EQUIVALENT`); `quantitative_error` NULL ×3 |
| Submission | **not authorised**; still prohibited while PCR1 fails / G3 is unmet |
| Author-data route | **NOT SENT / NOT AUTHORISED** — this instrument sends nothing and contacts no author |
| Blueprint v1.5 / Rule R-fit / thresholds / routes / gate definitions / numerical results / benchmark classifications / source files | **byte-unchanged** |
| External benchmark hunt | **permanently CLOSED**; no reopening under this instrument |

## Order of operations (status of each step at this recording)

1. ✅ **DONE 2026-09-24** — the granting is recorded (signature block above; P12AF internal act).
2. **IN PROGRESS (P12AF)** — the scoped manuscript edit of decision B, and nothing else;
3. the edit is verified against this record's scope list, the manuscript hash recorded, and the gate
   statuses re-asserted as unchanged;
4. any further stage — including any submission decision — requires its own authorisation, and submission
   remains prohibited while PCR1 fails and G3 is unmet.

**Phase note (unchanged in substance).** P12AE created this authorisation record only and changed no
manuscript byte; the scoped editing authorised by decision B is performed by the phase that recorded the
grant (P12AF).

---

## Signature block — GRANTED

| Field | Value |
|---|---|
| Decision | **☒ GRANT decisions A–F** (in full; the partial-grant branch is unused) |
| PI name | **Vipin Gupta** — *provenance:* the repository owner account `vipin-oss` (`https://github.com/vipin-oss/BFS-FEM-MATLAB`) and the commit-author identity `Vipin Gupta <vipin@gurugramuniversity.ac.in>` recorded in this repository's own history. The repository contains **no separate PI signature record**, and the manuscript author block names only "Phase-1/P7 Collaborative Research Team". If the PI's formal name differs from the identity above, this field must be corrected by the PI: nothing beyond the repository's own identity metadata has been inferred. |
| Date | **2026-09-24** (UTC; Asia/Calcutta same date) |
| Recorded as | **☒ internal act recorded in this file by the agent under the PI's explicit instruction conveyed in the project context (P12AF), committed to this repository** — the recording commit is the authoritative timestamp. ☐ PI wet/electronic signature (not supplied; not claimed). |

**Recording provenance (verbatim scope).** The PI's instruction for this phase was: *"The PI has now
authorised the manuscript-preparation transition. Record the grant in the P12AE signature block as an
explicit internal act."* The grant therefore covers **decisions A–F as written above, in full**, and
nothing else; this file is not a PI-signed artefact and does not claim to be one.

Any partial grant must reproduce decisions A and F verbatim, and no partial grant may promote, lower or
re-define any gate, threshold, route or benchmark classification. *(Unused — the grant is in full.)*

---

## Annex — the approved limitation statement (verbatim from P12AD §E)

> *External benchmark coverage.* Three external benchmarks support the band-structure discussion.
> Benchmark B1 (Layer 1, classical limit) is validated by the labelled **graphical** route: the source
> publishes no machine-readable numerical data, so its curve is reproduced from the source-stated
> parameters and compared as an explicitly labelled overlay, with **no** numerical percentage asserted.
> Benchmarks B2 (Layer 2a) and B3 (Layer 2b) could **not** be quantitatively or authoritatively validated:
> neither source publishes numerical curve data, and the parameter and normalisation information published
> with the relevant figures is insufficient to reproduce them independently — for Layer 2a the definition
> and units of the length-scale parameter are ambiguous as published, and for Layer 2b the parameter set
> and normalisation of the published dispersion figure are not stated. These two benchmarks are therefore
> reported as **not validated**, and the corresponding verification gate is **not** claimed as met. **No
> numerical agreement value and no error percentage is claimed for any of the three benchmarks.** The
> gradient-elasticity formulation implemented here has been verified against the formulation printed in
> the source that defines it to machine precision (≤ 4 × 10⁻¹⁵ on the transfer matrix and the dispersion
> relation); this is a formulation-consistency check and **not** a validation of the two benchmarks. These
> limitations reflect the information published with the source articles, not any deficiency of the
> present solver or of its verification suite.

---

## Verification performed by this phase (targeted guards only)

| Check | Result |
|---|---|
| `paper9/verification/suite/test_p12ae_authorisation_record.py` | **17 passed** |
| Full suite `paper9/verification/suite` | **317 passed, 1 skipped, 0 failed** |
| Manuscript | byte-identical (set `5ba2c22e…`) — no edit made by this phase |
| Blueprint v1.5 / Rule R-fit / machine record / `P5_STATUS.md` / register | byte-identical (asserted by guards) |
| Benchmark classifications and PCR1/G3/G4 | unchanged (asserted against the live machine record) |
| Immutability vs entry | 0 changed / 0 removed; added: this record, its guards, the P12AE checkpoint |

## Files added by this phase

| File | Purpose |
|---|---|
| `paper9/audit/P12AE_PI_AUTHORISATION_MANUSCRIPT_PREPARATION.md` | this authorisation record (decisions A–F; proposed / ready-to-sign) |
| `paper9/verification/suite/test_p12ae_authorisation_record.py` | targeted guards proving no record/classification/manuscript change |
| `paper9/audit/RECOVERY_CHECKPOINT_P12AE.md` | pre-work + final recovery checkpoint |
