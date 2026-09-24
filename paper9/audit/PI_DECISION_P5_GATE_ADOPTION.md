# PI decision record — P5 production-gate adoption

**Status: `APPROVED / CLOSED` — PI authorisation recorded 2026-09-24 (§6). P5 is now `PASS` as the
production gate.** The authorisation was conveyed by the PI as an explicit instruction in the project
context and is recorded below with its exact text; no wet signature is claimed.

| field | value |
|---|---|
| prepared | 2026-09-24 |
| prepared at HEAD | `ca57a9d55774fadcbe1c5d17bf929fc8fa3ec516` (branch `phase-1-symbolic`, tri-equal verified) |
| prepared by | repository-side preparation; the PI authorisation of §6 was recorded on 2026-09-24 |
| phase numbering | **none** — this is a decision record, not an audit phase, and it authorises no work |
| came into force | **2026-09-24**, on the PI's authorisation recorded in §6 |
| companion record | `paper9/audit/PI_DECISION_R1_MEASURED_ADJUDICATION.md` (same package) |

---

## 1. The decision — as adopted (one line, quotable)

> **PI DECISION (P5), adopted 2026-09-24.** *I adopt the Part A production matrix
> (`paper9/results/raw/p5_production_raw.json`, commit `15814972…`, `param_hash 09dd73f4…`, sha256 `0af7445a…`)
> together with the P11/P12C Case-C artifacts as the canonical Phase-5 production record, and I adopt the gate
> statement **P5 PASS / G5 PASS** (G5 = plan-level Phase-5 study completeness, not a validation gate), with the
> Part B pilot record retained verbatim as history and the “Branch-level P5 gate: CONTESTED” label superseded;
> this adoption changes no scientific number, amends no Blueprint text, constitutes no satisfaction of PCR1, G3 or
> G4, does not authorise submission, and leaves B2 and B3 NOT_VALIDATED.*

**Signature options (recorded as presented).** (A) adopt as written; (B) adopt with amendments the PI
specifies in the signature block; (C) do not adopt, and state exactly what else the gate requires.
**Selected: A — adopt as written.** There is no other open question: the *record*
question is closed on repository evidence (§2), and adopting one of the two recorded gate sentences is a PI act
(P12AD §B; P12AE §C).

## 2. Why this decision is evidence-complete

| # | element of the recorded dispute | state of evidence |
|---|---|---|
| 1 | **which record is the production record** | decided in-repo: `P12AD` §B selects **Part A** (`p5_production_raw.json`, sha256 `0af7445a…`; `p5_production_highlights.json`, sha256 `ce28df21…`; commit `15814972…`, `param_hash 09dd73f4…`); preserved unchanged by `P12AE` §C |
| 2 | **only complete production matrix** | Part A: studies S1, S3–S9 (8 studies, 42-point (θ, AR) map). Part B: pilot only — its own §6 states the production set was blocked on TV4/TV6/TV7/TV14 (scope: no Case-C assembly, no AR parameter, no S8/S9 drivers) |
| 3 | **register conformance** | Part A's production metadata matches the `LOCKED [S]` values exactly: `N_seg` = 40 (121 path nodes), `N_kx`×`N_ky` = 41×81 half-BZ (TV4); `N_bands` = 4 (TV7); θ grid 0→90° by 15° (TV16); AR ∈ {1,2,3,5,7,10}. Part B's values (61-pt path, 41×41 full-BZ, N = 8, θ = 30°) are non-conforming |
| 4 | **study completeness incl. S2 (Case C)** | S2 is delivered by the P11/P12C Case-C artifacts (`p11_caseC_convergence.json`, `p11d_caseC_gap_convergence.json`, `p12c_caseC_{32,64}_gap_convergence.json`), with TV6-CaseC/TV14/TV18 `LOCKED [S]` in the active `traceability_matrix.json` |
| 5 | **the recorded objection: “no numeric cross-validation between the pipelines has been executed”** | **executed and closed.** At both pipelines' own operating points (Part A pilot: θ = 45°, AR = 3 area-preserving, l₁ = 0.3464101615, l₂ = 0.1154700538; Part B pilot: θ = 30°, l₁ = 0.30, l₂ = 0.10), at Γ, an interior point k = (0.3π/L, 0.4π/L) and X: single-element **K, M bitwise identical**; reduced Bloch **K, M** relative difference ≤ 6.98 × 10⁻¹⁶ (Γ), 1.57 × 10⁻¹⁶ (interior), 2.31 × 10⁻¹⁶ (X); **spectra** max abs difference 1.78 × 10⁻¹⁵ (interior), 4.89 × 10⁻¹⁵ (X). At Γ the ω-difference is meaningless by construction (the zero/rigid cluster differs by ±5.8 × 10⁻¹⁶, which the √ amplifies to ≤ 3.5 × 10⁻⁸; the physical branches coincide with 0.0 difference) |

**Conclusion carried by (1)–(5).** The two lineages are **operator-identical**; the recorded divergence is a
convention/sampling/scope divergence (path length, zone grid, reported band count, pilot orientation, AR
parameterisation) and **not** a numerical disagreement. The premise of the "CONTESTED" label is therefore
empirically obsolete. Nothing further is computable that would change the choice: the remaining item is the gate
*sentence*, which is a PI act.

## 3. What this authorisation changes — exact and minimal (applied 2026-09-24)

On signature only the following governance effect exists:

1. the branch's adopted P5 gate sentence becomes **P5 PASS / G5 PASS** (production gate; G5 = plan-level Phase-5
   study completeness — `paper9/plan/CALC_MASTER_PLAN.md`, renamed from G3b, *not* a validation gate);
2. the canonical production record is the Part A matrix named in §1, extended for S2 by the P11/P12C Case-C
   artifacts;
3. the “Branch-level P5 gate: CONTESTED” label is superseded; `paper9/audit/P5_STATUS.md` is retained **verbatim**
   as history (byte-unchanged, sha256 `1a410f22…`).

**Applied on 2026-09-24** (the PI directed the minimal governance effect to be recorded; see §7): the active
record `paper9/audit/benchmark_validation_record.json` now carries `gate_state.P5` = `PASS` and a
`pi_authorisations_2026_09_24` provenance block citing this record. **No numerical artifact, table, figure,
manuscript or Blueprint text was touched**, and no historical record was rewritten.

## 4. Mandatory non-satisfaction statement (applies to any granting)

> **This adoption is a production-gate statement only.** It does **not** constitute satisfaction of PCR1, G3 or
> G4; it does **not** authorise submission (submission remains NOT AUTHORISED); it changes **no** scientific
> number, threshold or gate definition; it does not amend the Blueprint; and **benchmarks B2 and B3 remain
> `NOT_VALIDATED`** with `quantitative_error` NULL. P13 remains blocked.

## 5. Disclosed residuals (recorded honestly; none blocks the decision)

* **S2 delivery path.** S2 was produced by the P11/P12C Case-C work, not by the Part A runner. Its zone sampling
  is 11²/21²/41² sub-zone grids rather than the TV4-locked 41×81 half-BZ; the manuscript states its grids and
  bounds the sampling sensitivity (21²→41² changes the 4×4 value by ≈ 4 × 10⁻⁴). This is a **disclosed deviation**,
  not a defect, and the Case-C numbers are unchanged (43.94 % is explicitly the 4×4 result and is labelled
  not-mesh-converged).
* **Record staleness (not edited here).** `paper9/audit/P5_TV_RESOLUTION.md` — a P5-era record (base `15814972…`)
  — still lists TV6-CaseC/TV14/TV18 as OPEN although the **active** `traceability_matrix.json` carries them
  `LOCKED [S]` from P11. Reported for transparency; correcting a historical phase record is not done silently.

## 6. Signature block

```
P5 PRODUCTION-GATE ADOPTION

State:  [ ] PROPOSED / READY FOR PI SIGNATURE        [x] APPROVED / CLOSED
        (approved and closed on 2026-09-24)

Decision (selected):     [x] A — adopt as written     [ ] B — adopt with amendments     [ ] C — not adopted

PI decision text (verbatim, as conveyed 2026-09-24):
    "OPTION A — adopt as written.
     Adopt the Part-A production record together with the P11/P12C Case-C artifacts as the
     canonical Phase-5 production record and adopt the gate statement P5 PASS / G5 PASS."

Amendments / conditions: none.

PI: Vipin Gupta (name per repository metadata; PI-correctable)   Date: 2026-09-24
    (authorisation conveyed as an explicit PI instruction in the project context; no wet signature claimed)

Recorded by: P12C Post-Closeout Audit Agent (repository-side recording of the PI's instruction)
    Date: 2026-09-24
```

**Explicit distinction (state at closure).** The `PROPOSED / READY FOR PI SIGNATURE` state ended when the PI
issued the authorisation above; `APPROVED / CLOSED` exists **only** by that authorisation and was applied by the
minimal governance change listed in §7.

## 7. Applied governance effect (2026-09-24, minimal)

| file | change |
|---|---|
| `paper9/audit/benchmark_validation_record.json` | `gate_state.P5`: `NOT PASS/OPEN` → `PASS`; provenance block `pi_authorisations_2026_09_24.P5` added (decision text pointer, effect, record path, non-satisfaction). **All other fields, values, hashes and reason strings byte-identical** |
| `paper9/audit/PI_DECISION_P5_GATE_ADOPTION.md` | this record: state → `APPROVED / CLOSED`, PI authorisation recorded with date and exact text |
| `paper9/audit/PI_DECISION_PACKAGE_P5_R1.md` | package state and status matrix updated to the authorised closures |
| `paper9/verification/suite/` governance guards | the byte pin of the active record re-pointed in the eight guard files that carried it (`test_p12ac`, `test_p12ad`, `test_p12ae`, `test_p12af`, `test_p12ag`, `test_p12v`, `test_p12w`, `test_p12z`) and the live-value expectations for P5/R-1 in `test_p12aa`, `test_p12ab`, `test_p12ad`, `test_p12ae`, `test_p12af`, `test_p12ag`, `test_p12u`, `test_p12w`, `test_p12x`, `test_p12y`, `test_p12z` updated to the authorised values; every other gate, benchmark field, number, reason string and historical assertion is unchanged — most stringently the prohibitions for PCR1/G3/G4/P13, which stay in force |

**Not changed by this authorisation:** `paper9/audit/P5_STATUS.md` (`1a410f22…`, verbatim history), the P12AA
and P12AB phase matrices (their P5/R-1 rows keep the phase-era statuses), the Blueprint (all versions), Rule
R-fit, the manuscript and all LaTeX, all figures and tables, all results artifacts, and every benchmark
classification. B2 and B3 remain `NOT_VALIDATED`; PCR1 `NOT PASS`; G3/G4 `NOT MET`; submission not authorised.
