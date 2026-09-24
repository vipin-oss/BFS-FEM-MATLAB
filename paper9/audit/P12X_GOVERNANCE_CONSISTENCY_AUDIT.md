# P12X — FINAL GOVERNANCE / GATE-STATE AUDIT AFTER P12W

**Phase:** P12X. **Scope:** verify that the active repository state consistently distinguishes
B1 = `GRAPHICAL_VALIDATION`/PASS · B2 = `NOT_VALIDATED` (source ambiguity) · B3 = `NOT_VALIDATED`
(source parameter/normalisation/curve data missing **while the formulation is established**), with
PCR1 NOT PASS · G3 NOT MET · G4 NOT MET · P5 NOT PASS/OPEN · R-1 OPEN · PCR5 PASS · P13 BLOCKED —
and that no active record, gate-state record or derived artifact claims B3's **formulation** is
unresolved. No gate may be promoted; no data, Blueprint or manuscript may change.

| Field | Value |
|---|---|
| Entry SHA (verified) | `f68eb7c0d70c90c14087d76d225c3ac053352cf4` (local = origin = ls-remote; clean tree) |
| Pre-work checkpoint | `5a84fc93457e16d61cf4a7288be1c4ce41407083` (pushed + verified before any edit) |
| Correction commit | recorded in the P12X delivery report |
| Final checkpoint | `paper9/audit/RECOVERY_CHECKPOINT_P12X.md` (final form) |
| Active record before / after | `9ea0d4c8039b42c2644db3c679e3ff4b42b2a8a72b3977f6e54c1d301b718b51` → `2fad2d92a07eadf4f00fbb952e983bd897984d5579711052c7c0deafe72672d2` |
| Frozen raw P12S/P12U record | `cffc0c889c79186b34b0d3775191e181e040dfb358e4c61f6c06a7f22f5c3a21` (byte-identical) |

## Part A — recovery

`git fetch` → local `HEAD` = `origin/phase-1-symbolic` = `ls-remote` = `f68eb7c0…`;
`git status --porcelain` empty; pre-work checkpoint `5a84fc9` pushed and re-verified before any edit.
Baseline hash snapshot of 521 tracked files taken at entry (`/home/user/p12x_baseline_hashes.txt`).

## Part B — active-state consistency search (classification)

Every hit of the stale-language families is classified: **A** active operative · **B** historical
audit record · **C** evidence / frozen quote · **D** derived test expectation · **E** manuscript ·
**F** irrelevant.

| Family | Locations (post-P12W state) | Class |
|---|---|---|
| `unverifiable formulation` | `RECOVERY_CHECKPOINT_P12W.md` (correction record), `P12W_CORRECTION_CLOSURE.md`, P12W/P12X test expectations | **B / D** — no active record |
| `dipolar-gradient formulation/coefficient convention not pinned down` | `P12V_B2_B3_SOURCE_AUDIT.md` (the finding as recorded), `P12W_CORRECTION_CLOSURE.md`, `RECOVERY_CHECKPOINT_P12W.md` | **B** — historical findings preserved verbatim |
| `not pinned down` / `cannot be pinned down` | P12S audit + checkpoint, P12T audit, P12S manuscript-impact **proposal**, P12V/P12W records | **B** — historical; the proposal was never applied |
| `coefficient convention` | P12S/P12T/P12U/P12V/P12W records, P12S raw record + `p12s_run.py` (frozen generator text), **active record `reason`** , P12L/P12M author questions | **B / C / F** — see the frozen-clause note below; the P12L/P12M mentions are *questions to the authors*, not status claims |
| `source's own 0.50` | `P12V_B2_B3_SOURCE_AUDIT.md` (F1 as found), `RECOVERY_CHECKPOINT_P12W.md` (F1 CLOSED row) | **B** — none active |
| `implementation defect` | P12V audit + checkpoint (“source-side, **not** an implementation defect”) | **B** — the negation of the stale claim |
| B2 `l`/`l̄` ambiguity wording | `benchmark_evidence.json`, active record B2 block, manuscript §5.1 | **A / E** — the *operative* B2 ambiguity, intended |
| “B1/B2/B3 BLOCKED” | `OVERNIGHT_AUTONOMOUS_STATUS.md` (early-phase status record) | **B** — historical, no formulation claim |
| TV1 provenance tag | `traceability_matrix.csv` row TV1 reads `CLOSED [C]` while the authoritative `traceability_matrix.json` reads `CLOSED [S]` (P11D retag) | **A** — stale derived entry → finding **P12X-F1** |
| Blueprint version citation | `P12N_AUTHOR_DATA_HANDOFF.md` §4 cites the “authoritative Blueprint v1.4” line numbers (thresholds unchanged by the v1.5 A2 amendment) | **A** — currency observation → **P12X-F2** |

**Frozen-clause note (the one substantive hit).** The active record's `benchmarks.B3.reason` string
still ends “…the unresolved question (which dipolar-gradient formulation / coefficient convention
the source used) is a SOURCE_UNAVAILABLE item”. That string is the P12S run record's own field,
byte-pinned to `evidence/p12s/p12s_validation_record.json` by the P12U guard
(`record.reason == raw.reason`). Part G of this phase forbids editing raw P12U records, and no
existing guard may be weakened, so the clause **cannot** be rewritten. It is therefore classified
**C (frozen evidence quote)** and retired at *field level* instead of edited.

## Part C — B3 operative logic (verified)

| Requirement | Verification |
|---|---|
| formulation ESTABLISHED / SOURCE-EQUIVALENT | **new operative field** `benchmarks.B3.formulation_status` (added by this phase, see Part J) carries the P12V identity (Appendix 3 `[P0][G][P0]⁻¹`, ~1e-16 at 60 digits), the reproduced band edges (0.3391 / 1.021) and “source-side, not an implementation-formulation defect” |
| validation NOT_VALIDATED | `route = "NOT_VALIDATED"`, `graphical_validation = "NOT_APPLICABLE"` — unchanged |
| reason = missing Fig. 4(c) parameter set/normalisation/curve data | carried in `formulation_status`, `ambiguity_status` and `gate_state.blocker`; no Fig. 3(b) inheritance is treated as authoritative (`parameter_provenance` says “inheritance is inferred”, `benchmark_evidence.json` says “provenance [S] (inherited), never [C]”) |
| not conflated | `formulation_status` contains no “PASS”; `ambiguity_status` begins `UNRESOLVED -- NOT the formulation`; `route` still `NOT_VALIDATED` |
| 0.3391 reproduced | present in `formulation_status` and `reproduction_status` |
| published solid “Present” ≈ 0.433–0.436 | present in `reproduction_status` as a band (“0.433-0.436”; own digitisation 0.433, P12T 0.436) |
| classical/dashed literature level ≈ 0.500 | present as `0.500` (classical limit) and `~0.50` (dashed [34]); explicitly “NOT the source's Present gradient value” |
| `quantitative_error` NULL / no % claimed | `quantitative_error = null`; the B3 block contains no `%` at all |

## Part D — B2 operative logic (verified)

`route = NOT_VALIDATED` · `ambiguity_status = "UNRESOLVED (dimensional vs barred reading of l; A2.4
forbids silent choice)"` · `quantitative_error = null` · `parameter_completeness = "INCOMPLETE (l
units/definition not resolvable from source)"`. Reason is structural/source-based: the bare
unlabelled `'l = 1e-5'` caption value; `Eq. 55 defines l_bar = l/b`; the dimensional reading
“coincides with the classical panel and contradicts the published panel (b)”; the micro geometry
gives a different structure; “No interpretation is selected”. `reproduction_status = NOT REPRODUCED
under any admissible interpretation`; `branch_observables = not compared (no admissible reproduction
to compare)`. Graphical closeness is **not** converted into any quantitative statement (no `%`, no
digitised error). Author data remains the stated route to a definitive resolution (Part F).

## Part E — gate logic (verified, no promotion)

| Record | PCR1 | G3 | G4 | P5 | R-1 | PCR5 | P13 |
|---|---|---|---|---|---|---|---|
| `benchmark_validation_record.json` (`gate_state`) | NOT PASS | NOT MET | NOT MET | NOT PASS/OPEN | OPEN | PASS | BLOCKED |
| `P11D_PCR_MAPPING.md` | NOT MET (≤2 % not computable) | NOT MET | NOT MET (G4 cannot PASS) | — | — | PASS | — |
| `P12N`, `P12O`, `P12P`, `P12Q` (live chain) | NOT PASS | NOT MET | NOT MET | NOT PASS / OPEN | OPEN | PASS | BLOCKED |
| `BLUEPRINT_V1_5_GRAPHICAL_VALIDATION_AMENDMENT.md` | — | — | — | — | OPEN (unchanged) | — | — |
| `P5_STATUS.md` (active gate record) | — | — | — | CONTESTED — **neither claim adopted** (= record's NOT PASS/OPEN) | — | — | — |
| `benchmark_evidence.json` + traceability matrix | no gate-status claims; B1/B2/B3 `quantitative_error` NULL | | | | | | |

No active record claims PCR1 PASS, G3 MET, G4 MET, P5 PASS, R-1 CLOSED, P13 UNBLOCKED or a B3
validation PASS (asserted mechanically in the new guards). No contradiction: B3's residual is stated
everywhere as the missing source data, not as a formulation defect.

## Part F — author-data logic (verified, unchanged)

* B2 requirement: dimensional vs barred `l` (units), the normalising length used for Fig. 2(b) and
  the parameter set behind that panel — `P12L` §2 (“this is the blocking question”).
* B3 requirement: the numerical points/edges underlying Fig. 4(c), the non-dimensional coefficients
  **actually used for that panel** and their normalisation length — `P12L` §3.
* Requests remain drafts: `P12M` and `P12L` byte-identical to their recorded hashes (`2f68e66f…`,
  `8acb70f1…`); `P12N/P12O/P12P` say **NOT SENT**; `P12Q` says **NOT AUTHORIZED / NOT SENT**;
  no author data received; no option selected (PI decision PENDING). Nothing altered.

## Part G — immutability (verified)

521 tracked files compared with the entry snapshot → **exactly 3 changed**, all intentional
(this phase's record correction plus the two re-pointed content pins). Byte-identical: Blueprint
v1.5 `b96c8e76…`, Rule R-fit `d4fed492…`, manuscript (`paper9/latex/`, 13 files), production (17),
results (32), tables (15), `paper9/analytic/` sources (12), validation (19), P12S/T/U/V evidence
(34), all P12 audit documents, `paper9/plan/` (7). The raw P12S/P12U record is untouched.

## Part H — tests

New `paper9/verification/suite/test_p12x_governance_consistency.py` (**25 guards**): the three
benchmark statuses; the B3 formulation-status field and its separation from validation; NULL
quantitative errors and the absence of any `%`; the seven gate states; gate agreement across the
five active governance records; promoted-gate prohibition; the stale-wording scan over all active
records (with the frozen-string carve-out and its field-level retirement); the preservation of the
historical P12V/P12T wording; the frozen `reason` byte-identity and its explicit supersession; no
Fig. 3(b) inheritance treated as authoritative; the structural B2 reason; the three-curve
distinctness; author-data draft/not-sent state; the P5 contested record; and the immutability
anchors (Blueprint, Rule R-fit, frozen records, P12U guard file, manuscript `.tex` set). Existing
guards were not weakened; the P12V/P12W content pins were re-pointed once, with the reason recorded
in their docstrings.

## Part J — decision

**OUTCOME 2 — CORRECTIONS REQUIRED (one correction, applied).** No active record claimed a promoted
gate and none contained a *rewritable* formulation-unresolved claim; but the B3 block carried no
explicit machine-readable formulation status, so the superseded claim surviving inside the frozen
`reason` string was covered only by prose in `ambiguity_status` and remained readable as an
operative assertion. Correction (Part J allowances: text/record only, no data, no gate):

* **added** `benchmarks.B3.formulation_status` — one ASCII field, no number changed (verified
  field-by-field: the only leaf difference against the previous revision is this added field). It
  states ESTABLISHED / SOURCE-EQUIVALENT with the P12V evidence, marks the earlier
  formulation/coefficient-convention attribution **SUPERSEDED** and the frozen `reason` clause
  **not operative**, and names the residual blocker as the source's unstated Fig. 4(c) parameter
  set/normalisation and curve data.

### Findings reported, not corrected (out of this phase's audited state, recorded for the PI)

* **P12X-F1** — `paper9/audit/traceability_matrix.csv` row **TV1** reads `CLOSED [C]` while the
  authoritative `traceability_matrix.json` reads `CLOSED [S]` (P11D retag; the manuscript repeats
  the retag). The CSV is a legacy P11-schema projection not consumed by any checker or test; the
  provenance claim is about the B3 parameter anchor, not the formulation, so it is reported rather
  than edited (no cosmetic rewrite of legacy records without a mandate).
* **P12X-F2** — `P12N` §4 cites the “authoritative Blueprint v1.4” line numbers; the governing
  document is v1.5 (A2 amendment, thresholds unchanged). No operative contradiction; the live
  PI-handoff chain was left byte-identical.

Neither finding changes any gate, route, status or number.
