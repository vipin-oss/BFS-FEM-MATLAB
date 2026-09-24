# P12AD — Internal Reconciliation and Transition Decision

**Phase:** P12AD (internal reconciliation and transition decision — no new science, no new benchmark
search, no gate change). **Branch:** `phase-1-symbolic`. **Entry state:** P12AC final checkpoint
`37f7186…` (verified tri-equal, clean); P12AD pre-work checkpoint `a80d96c…` committed, pushed and
verified before this record was written.

**Purpose.** Convert the closed P12AC decision set into the minimum set of *internal* decisions that the
repository can take on its own evidence — P5 record retention, R-1, C-1, the manuscript limitation text and
the P13 transition — and state exactly which remaining acts require explicit external (PI) authorisation.
This record closes the external-validation hunt permanently (§H) and creates no new gate, lowers no gate,
alters no threshold, route, numerical result, Blueprint byte or manuscript byte.

---

## A. Scientific validation status (exact, unchanged)

| Item | Status (exact) | Basis |
|---|---|---|
| **B1** (Layer 1, classical limit) | `GRAPHICAL_VALIDATION` / **PASS** | labelled overlay route (A2 §13); `quantitative_error` NULL |
| **B2** (Layer 2a, gradient elasticity) | **`NOT_VALIDATED`** — source-limited | no machine-readable source data; quantitative route impossible; graphical route not admissible (published length-scale definition/units ambiguous: dimensional `l` vs barred `l̄`) |
| **B3** (Layer 2b, dipolar gradient) | **`NOT_VALIDATED`** — source-limited; formulation `ESTABLISHED / SOURCE-EQUIVALENT` | repository layer matrix equal to the source's own Appendix 3 `[P0][G][P0]⁻¹` to ~1e-16 at 60 digits; Fig. 4(c) parameter set/normalisation and curve data unstated in the source |
| **`quantitative_error`** | **NULL × 3** | no percentage, error bar or agreement number is attached to any benchmark |
| **PCR1** | **NOT PASS** | item 1 is the sole failing item (B2/B3 satisfy neither admissible route); items 2–8 satisfied per the P12C status matrix, subject to the separately authorised A2 manuscript re-tiering edit |
| **G3** | **NOT MET** | same evidence as PCR1 item 1 |
| **G4** | **NOT MET** | PI signature gate over the PCR set; PCR1 fails |
| **P5** | **NOT PASS/OPEN** | production gate; record retention decided in §B, gate statement still a PI act |
| **R-1** | **OPEN** | internal governance item; governing artefact retained (§C) |
| **PCR5** | **PASS** | unchanged |
| **P13** | **BLOCKED** | until the authorisation of §F exists |
| Author-data route | **NOT SENT / NOT AUTHORISED**; no data received | P12Q handoff, Option A/B neither selected |

**Non-relabelling rule (binding on every downstream record):** none of B2, B3, PCR1, G3 or G4 may be
restated as validated, passed or met. B3's formulation status is a *formulation-consistency* finding and
explicitly **not** a validation.

---

## B. P5 disposition — retained numerical production record (internal decision)

**Decision (final for this phase).** The numerical production record retained as the branch's P5 production
record is the **Part A pipeline**:

* `paper9/results/raw/p5_production_raw.json` (sha256 `0af7445a…`, `git_commit 15814972…`,
  `param_hash 09dd73f4…`, 8 studies S1, S3–S9, 42-point (θ, AR) design map), with
* `paper9/results/processed/p5_production_highlights.json` (sha256 `ce28df21…`, same `param_hash`).

**Why this record, on the repository's own evidence** (P12AB Part D):
1. it is the **only complete production matrix** in the repository — the Part B pipeline never ran its
   production set (its own record states the frozen cases were blocked on TV4/TV6/TV7/TV14);
2. its conventions are the ones **later locked and registered** — TV4 (`N_seg = 40`, 121 path nodes,
   41×81 half-BZ), TV6-Case-H, TV7 (`N = 4`), TV15/TV16 — i.e. the register adopted this pipeline's
   design, not the alternative's;
3. **no manuscript claim depends on it** (P12C §2: zero `production/P5` hits under `latex/sections/`), so
   the retention choice changes no published number;
4. **Rule R-fit and the 5i estimator are untouched** by this decision.

The Part B pipeline record (`audit/P5_STATUS.md`, Part B: pilot 15/15; production set not run) is retained
verbatim as history; nothing is deleted and its text is not edited.

**What this decision is not.** It is *not* external benchmark validation, and it does **not** adopt the
Part A gate statement (`P5 PASS / G5 PASS`). The branch still carries two contradictory recorded gate
statements, and adopting one of them is a PI act (see §G item 3). **P5 therefore remains
`NOT PASS/OPEN`** and `P5_STATUS.md` stays byte-unchanged, including its "Branch-level P5 gate:
CONTESTED" wording. The cross-validation run specified in P12AB Part D remains available if the PI prefers
a numeric basis for the gate statement; **no solver was run in this phase**.

*Consequence for PCR1/G3/G4:* **none** — all three are preserved exactly as in §A. P5 is a parallel
production gate and is not on the `B2/B3 → PCR1 → G3 → G4` chain.

---

## C. R-1 disposition — governing artefact retained; R-1 stays OPEN as an internal governance item

**Question put to this phase.** Is the authorised rerun (P12AB Part E) necessary for the scientific
manuscript?

**Determination: no.** The existing reproducibility evidence is sufficient to retain the governing 5i
artefact for manuscript purposes, for three reasons that are all verifiable in-repo:

1. **The manuscript makes no bitwise-reproducibility claim.** Its mesh-convergence text reports the
   *observed* empirical rate under the pre-declared rule, and explicitly identifies the 32² level as
   resolution-limited rather than reproducible-at-that-error (Fig. 5 caption, Table 6 and the text of
   `sec05_verification.tex` all carry this).
2. **The fit-subset verdict is robust, not realization-dependent.** Property C (frozen Rule R-fit
   protocol determinism) is established: the rule returns a unique verdict for every k, its verdicts are
   identical across a 273×-wide F window, it reproduces the governing rate bit-exactly
   (`4.173919246515192`), and **no recorded realization admits the 32² level** (worst-case family margin
   4.49×; 1527× at the governing artefact). The unrealized property (B: reproducibility of the governing
   artefact under the deployed, unpinned configuration) therefore cannot change the reported rate.
3. **Property A is established where the manuscript relies on it** (solver determinism for the Route-F
   configuration), and the G-1 environment sensitivity item is closed.

**Therefore:** the governing artefact is retained; **R-1 remains `OPEN`** (class B) as an *internal
governance item*, not a science blocker; the specified rerun (P12AB Part E: two independent realizations on
the deployed configuration, `tol = 1e-12`, unpinned start vector, `n_mesh ∈ {4, 8, 16, 32}`, then the
unchanged frozen rule) remains the exact minimum action that would establish property B — available, not
required, and **not executed here**.

**Prohibitions restated:** no new numerical experiment was run; the governing value
`4.173919246515192`, its CI and `ε_Δ = 4.6318154949690315e-11` are unchanged; no re-baseline; the
historical TXT's 4-point slope `5.485710` remains uncited; the governing JSON/TXT/script are byte-identical.

---

## D. C-1 disposition — minimum explicit internal disposition

**Facts (unchanged).** The criterion defect (non-discriminant acceptance, arbitrary `err > 1e-14` cut,
tautological tolerance handling) was remedied in design (P12D/P12E); the **frozen Rule R-fit** (`F = 3`
strict, pre-declared, SPREAD_FLOOR `1e-15`, seeds `20260924`/`7`) is validated (10 adversarial cases,
4 historical/control applications, 273×-wide robustness window) and was **adopted as the governing
admissibility rule** under the PI-authorised A1 action (P12H). The *residual* P12E observation is that the
4²…32² data fail P3 of the *proposed* P1–P4 predicate set (i.e. the four-level sequence is not a power law)
— an **estimator/Blueprint model defect**, not a criterion defect.

**Decision (final for this phase).** Under the rule actually in force, the criterion item is closed:

* the criterion governing the 5i estimator is **frozen Rule R-fit** — discriminant, validated, applied,
  and it reproduces the governing reported rate bit-exactly; the legacy `err > 1e-14` cut is **no longer
  governing**;
* the residual estimator/Blueprint model defect is disposed of as a **documented scientific limitation
  that the manuscript already carries in its own wording** — the rate is reported as an observed empirical
  value with no theoretical order claimed, and the excluded 32² level is reported with its relative error,
  its measured reproducibility and their ratio (Table 6), satisfying the rule's reporting requirement;
* **Rule R-fit is not changed**, no threshold is changed, and the P1–P4 predicate set remains a
  non-governing proposal (no Plan amendment made here).

**Alternative reading recorded for honesty:** if the PI intends the P12E P1–P4 predicate set (rather than
the frozen rule) to remain C-1's closure criterion, then C-1 stays `OPEN` and the minimum action is the
PI's explicit choice between the frozen rule (already in force) and an authorised estimator/Plan amendment
— a Blueprint-scope action explicitly outside this phase (§G item 5).

---

## E. Exact manuscript limitation text (for insertion only under separate authorisation)

The manuscript is **not edited by this phase** (byte-unchanged, §Files). The text below refines P12AC §6(b)
and is the exact text to be inserted, in the verification section, if and when manuscript editing is
authorised:

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

Requirements check (publication-appropriate and complete): B1 graphically validated ✔; B2/B3 not
quantitatively or authoritatively validated because required parameter/curve information is unavailable or
ambiguous ✔; the B3 formulation itself independently established as source-equivalent ✔; limitations are
source-data limitations, not solver failure ✔; no quantitative error percentage claimed for B2/B3 ✔.

---

## F. P13 transition decision

**Under the frozen architecture, P13 (final manuscript preparation) is not itself a gate.** Blueprint
v1.5 rows 13–14 prescribe the writing/assembly work and then `GATE G4 — submission-ready`; the
prohibitions attach to **submission** ("Do not submit" while G3 fails; "The manuscript cannot be submitted
until every line below is true" for PCR1), not to preparation. Nothing in the frozen record blocks a
*preparation* stage that claims no gate.

**Determination.** The project may enter a final manuscript-preparation / submission-decision stage with
B2/B3 explicitly retained `NOT_VALIDATED` and the §E limitation disclosed, **only under an explicit PI
authorisation recorded as an internal preparation act**, and only with all of the following conditions
holding in the same authorised decision:

1. B2/B3 stay `NOT_VALIDATED` and PCR1 / G3 / G4 stay `NOT PASS` / `NOT MET` in every active artefact; no
   unvalidated benchmark is presented as validated; **no gate is promoted**;
2. the §E limitation statement is carried by the manuscript, and the **A2 manuscript re-tiering**
   (amendment §8 item 1: every validation sentence states the tier actually achieved; a graphically
   validated benchmark may not be described with a percentage) is included in the same authorised editing;
3. **submission remains prohibited** while PCR1 fails (G4 is a PI signature gate);
4. the P5 disposition of §B (record retained; gate statement still a PI act), the R-1 disposition of §C
   (governing artefact retained; R-1 open as an internal governance item) and the C-1 disposition of §D
   are recorded as decided or explicitly left open in that decision;
5. no threshold, validation route, gate definition or numerical result changes, and the author-data route
   stays **NOT SENT / NOT AUTHORISED** (Decision B removes the expectation of author data; it does not
   send anything).

**If the PI does not authorise the transition, P13 stays `BLOCKED`** and the minimum authorised decision
is exactly the authorisation sentence in §G item 1. This record neither starts P13 nor authorises
submission.

---

## G. Exact minimum remaining authorisations

| # | Authorisation required | Scope / wording |
|---|---|---|
| 1 | **P13 transition (preparation stage)** | one recorded sentence: *"PI authorises the transition to the final manuscript-preparation stage as an internal preparation act; no gate is promoted, PCR1/G3/G4 remain NOT PASS/NOT MET, and submission remains prohibited."* |
| 2 | **Manuscript editing** | byte-minimal edit authorising (i) insertion of the §E limitation statement and (ii) the A2 validation-sentence re-tiering; every other manuscript byte frozen |
| 3 | **P5 gate statement** | adopt the Part-A production-record gate statement (with the Part B record retained verbatim as history) **or** record the continuation of `NOT PASS/OPEN`. The *record* question is already decided here (§B); only the gate sentence is open |
| 4 | **R-1** | (a) accept retention of the governing artefact with R-1 open as an internal governance item (the status quo), **or** (b) authorise the P12AB Part E two-realization rerun to establish property B. A re-baseline is a separate decision and would change published numbers — not recommended and not covered by (a)/(b) |
| 5 | **C-1** | accept the §D disposition (frozen Rule R-fit governing; estimator defect documented as a limitation) **or** authorise an estimator/Plan amendment (a Blueprint-scope action) |
| 6 | **Author-data route** | no action needed to maintain `NOT SENT / NOT AUTHORISED`; Option A (send) remains a PI act and is not required by Decision B |

No item above authorises, and none of them requires, a threshold change, a gate redefinition, a route
change, a numerical re-run (except #4b, which is explicitly an authorised run) or any edit to a frozen
artefact.

---

## H. External benchmark hunt — permanently CLOSED

Decision B (P12AC §5) is carried forward verbatim in effect: *B2/B3 remain source-limited and
NOT_VALIDATED because the published sources do not provide sufficient authoritative parameter/curve
information*; this is a property of the published record, **not** a solver defect. The classification pass
(P12AC §2) established that **no admissible ACCEPTABLE replacement or augmentation exists** for either
benchmark (Li 2024 and Li 2023 are the incumbents; LWZ2016 Fig. 3 is SUPPORTING ONLY; PB2009, Mishra 2026,
Zhan & Wei 2010, Zheng & Wei 2009 and the two content-mismatched PDFs are NOT COMPATIBLE, each for its
recorded reason), and the bounded external query returned nothing further.

**The search for a published replacement or augmentation of B2/B3 is CLOSED PERMANENTLY.** No further
candidate search, benchmark-hunt phase, literature pass or metadata-only audit loop on this question is
authorised, and this record must not be reopened as a hunt. The only admissible future route to a
quantitative benchmark remains an actual external delivery of source numerical data (the preserved
author-data route, a PI act), which would then be handled by the existing P12N receipt sequence — and even
then, only under the unchanged ≤ 2 % rule.

---

## Verification performed by this phase (targeted only)

| Check | Result |
|---|---|
| New guards `paper9/verification/suite/test_p12ad_decision_record.py` | **18 passed** |
| Full verification suite `paper9/verification/suite` | **300 passed, 1 skipped** (0 failed) |
| `audit/check_traceability.py` | **18/18 CLOSED / LOCKED; 0 open** |
| `audit/check_register_provenance.py` | **PASS — A=0 / B=3 / C=2 / D=0** |
| Frozen-hash invariants (Blueprint v1.5 `b96c8e76…`, Rule R-fit `d4fed492…`, governing JSON `38384363…`, machine record `2fad2d92…`, register JSON `83ff8723…` / CSV `8d86528f…`, `P5_STATUS.md` `1a410f22…`, manuscript set `5ba2c22e…`) | unchanged (asserted by the guards) |
| Governing 5i artefact | byte-identical; rate `4.173919246515192`, CI `[3.1453687594104447, 5.202469733619939]`, `ε_Δ 4.6318154949690315e-11` |
| P5 production record | `param_hash 09dd73f4…` and `git_commit 15814972…` confirmed in both raw and highlights artefacts |
| Manuscript | byte-unchanged (no edit made; §E delivered as text only) |
| Machine record / register / gate tables | statuses identical to §A — no promotion, no stale wording introduced |
| Immutability vs entry (`37f7186`, 546 tracked files) | **0 changed / 0 removed**; added: this record, its guard suite, the P12AD checkpoint |

## Files added by this phase

| File | Purpose |
|---|---|
| `paper9/audit/P12AD_INTERNAL_RECONCILIATION_DECISION.md` | this record (§§A–H) |
| `paper9/verification/suite/test_p12ad_decision_record.py` | guards: statuses, retention decision, limitation text, no-promotion, frozen hashes |
| `paper9/audit/RECOVERY_CHECKPOINT_P12AD.md` | pre-work + final recovery checkpoint |
