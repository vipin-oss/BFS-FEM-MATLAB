# P12G — Route A / Rule R-fit Pre-Implementation Design Freeze

**Design freeze only. Nothing is implemented, nothing is authorized by this document, no solver was
run, no Blueprint/manuscript/plan file was edited.** The rule below was frozen in code *before* it was
applied to any dataset, and was not altered after seeing the outcomes.

Date 2026-09-24 · branch `phase-1-symbolic` · HEAD `db44f31dd5b82a9703c7f0f20963a3184c18d235`
(sandbox recovery commit — the fourth `.git` + `*/out/` loss this session; content restored
byte-identically, mapping legend in `audit/SANDBOX_GIT_RECOVERY_20260924.md`). No push · no P13.

Evidence for this freeze: `audit/evidence/p12g/rfit_freeze.py` + its output (rule definition,
10 adversarial cases, 4 historical applications, F-robustness window). Spread inputs are read from
the archived P12E/P4B evidence and their presence there is asserted by the script, so no threshold
input is invented here.

---

## 1. Current locked baseline

| item | value / status |
|---|---|
| governing P4B artifact | JSON slope **4.173919246515192**, CI **[3.1453687594104447, 5.202469733619939]**, ε_Δ **4.6318154949690315e-11** — unchanged, still governing |
| historical TXT | run-1 stdout, preserved and labelled; its 4-point slope 5.485710 is **not** cited anywhere |
| Blueprint v1.3 | byte-identical (`ca71b91a…`); §5.7/line 618 prescribe a fit **from the four refinement levels** |
| R-1 | **OPEN** (mechanism fixed in P12E; no admissible re-baselined value) |
| C-1 | **OPEN** (criterion defect remedied in design; actual data fail P3) |
| BPC-1 | open decision item: the published rate is a **three-level** statistic while the Blueprint prescribes four levels |
| G-1 | **CLOSED** (guard semantics, `bb32253` — content preserved) |
| gates | PCR1 NOT PASS · G3 not met · G4 not met · P5 NOT PASS/OPEN — **none is claimed closed here** |

## 2. Rule R-fit — exact definition (frozen)

**Inputs, per prescribed refinement level *i* ∈ {4², 8², 16², 32²}:**

- **e_i** — the level's relative error against the closed-form reference (existing definition of 5i).
- **s_i** — the level's *measured reproducibility*: the relative spread of the level's eigenvalue
  between the **two pre-registered start vectors** (PCG64 seeds **20260924** and **7**) at the
  **frozen solver configuration** (ARPACK shift-invert, `tol = 1e-14`, `maxiter = 10000`, all five
  BLAS/OMP thread variables pinned to `1`), i.e. `s_i = |ω_i(A) − ω_i(B)| / ω_i(A)`. For the dense
  path used at 4² (nd = 128 ≤ 128 ⇒ LAPACK `eigh`, bit-deterministic within a configuration), the
  declared numerical zero applies: **s_i := SPREAD_FLOOR = 1e-15**.

**Admission rule (uniform for every level, every k, every configuration):**

> **level *i* participates in the least-squares rate fit ⇔ e_i > F · max(s_i, SPREAD_FLOOR), with the frozen margin F = 3.**

- **Boundary:** the inequality is **strict**; exact equality (e_i = F·s_i) does **not** admit.
- **Guard:** the LS rate + CI are reported only if **≥ 3** levels are admissible (dof ≥ 1); otherwise
  the rate is **not reportable** and only the levels' (e_i, s_i) are reported.
- **Ordering requirement:** all e_i and s_i are computed and recorded **before** the fit; the rule
  references no fitted quantity.
- **Reporting requirement:** every non-admitting level is reported with its e_i, s_i and the ratio
  e_i/s_i, and its exclusion is a *reported fact*, not a silent omission.

**Independence (by construction):** the rule's inputs are the per-level error and the per-level
measurement reproducibility only. It contains no reference to the slope, the CI, the residual, the
P1–P4 status, or the outcome of any fit — so no route by which the reported rate can influence
admissibility exists inside the rule.

## 3. Threshold provenance

| constant | frozen value | provenance |
|---|---|---|
| F | **3** | a stated *decision margin*: a level's error must exceed three times the reproducibility of that level's own measurement. Not derived from any fit; chosen before application |
| SPREAD_FLOOR | **1e-15** | declared numerical zero for the bit-deterministic dense path (≈9× double-precision ε; no dense-path spread was ever observed) |
| seeds | **20260924, 7** | the two start vectors already used in the archived P12E probes; pre-registered here as the measurement protocol |
| tol / maxiter / threads | **1e-14 / 10000 / all = 1** | the P12E Route-F configuration |

**Robustness window (the anti-tuning guarantee).** Over the three archived datasets that must stay
excluded and the three levels that must stay admitted, every recorded verdict is unchanged for
**F ∈ (0.2866, 78.24)** — a 273×-wide interval. The frozen F = 3 sits **10.5× above** the exclusion
boundary and **26× below** the inclusion boundary. The decision set is therefore not a function of
the threshold anywhere near the chosen value; **the threshold cannot be tuned to produce any
particular slope.**

## 4. Circularity / selection-bias audit (Part B)

Metric note recorded first: adding a point to a fit of the same model **can never reduce the SSE**
(SSE₄ ≥ SSE₃ is a theorem; 0/400 000 seeded random cases improved it), and the max-abs log residual
also failed to improve in the same search. The operational "improves / worsens" metric used below is
therefore the **reported CI width** and the movement of the fitted slope; the adversarial cases were
located by a declared seeded search and then frozen as literals.

| case | construction | (e₃₂, s₃₂) → ratio | rule verdict | effect of including the point |
|---|---|---|---|---|
| B1 | finest point **above** trend, above floor | (1e-10, 1e-16) → 1e5 | **RETAINED** | slope 4.00 → 2.39, CI width 0.010 → 7.98 (**worsens**) |
| B2 | finest point **below** trend, above floor | (2.5e-12, 1e-16) → 2500 | **RETAINED** | slope 4.00 → 3.99, CI 0.010 → 0.048 |
| **B3** | **same pair whose inclusion IMPROVES** | (2.441e-12, 5e-12) → **0.488** | **EXCLUDED** | slope 2.776 → 2.834, CI width 28.55 → 4.33 (**improves 6.6×**) |
| **B4** | **identical (e₃₂,s₃₂) pair, inclusion WORSENS** | (2.441e-12, 5e-12) → **0.488** | **EXCLUDED** | slope 1.702 → 2.723, CI width 0.350 → 5.07 (**worsens**) |
| B5 | above floor, inclusion worsens | (1e-10, 1e-12) → 100 | **RETAINED** | slope 4.00 → 2.39 (**worsens**) |
| B6 | noisy: e = s | (1e-11, 1e-11) → 1.0 | **EXCLUDED** | — |
| B7 | genuinely converged: e = s at the noise level | (3e-13, 3e-13) → 1.0 | **EXCLUDED** | — |
| B8 | exactly at the threshold (e = F·s) | (3e-12, 1e-12) → **3.000** | **EXCLUDED** (strict) | — |
| B9/B10 | identical pair under a steep (slope 4.00) and a shallow (slope 1.32) surrounding trend | (5e-13, 1e-12) → 0.5 | **EXCLUDED / EXCLUDED** | decision invariant to the surrounding data |

**B3/B4 is the decisive pair:** the *same* (e, s) inputs — hence the same rule verdict — with
inclusion **improving** the estimate in one dataset and **worsening** it in the other. The rule
cannot be reading the fit. All ten adversarial outcomes matched the pre-declared expectations.

## 5. Historical / control-k application (Part C — rule unaltered after seeing outcomes)

| dataset | per-level ratio (4², 8², 16², 32²) | verdict set | resulting LS rate |
|---|---|---|---|
| **1. Route-F controlled run** (two-seed spreads 1e-15*, 1.24e-14, 3.68e-14, 1.60e-13) | 1.5e7, 6.1e4, 1248, **0.287** | fit {4,8,16}; **exclude 32²** | **4.180559**, CI [3.2014, 5.1598], resid 0.0617 (dof 1) |
| **2. historical governing JSON** (21-realization spreads of its own era: 2.90e-14, 1.06e-13, 5.92e-13, 1.26e-12) | 5.2e5, 7132, 78.2, **0.00196** | fit {4,8,16}; **exclude 32²** | **4.173919246515192** — *identical to the published value* |
| **3. historical TXT run-1** (same era's spreads) | 5.2e5, 7133, 77.9, **0.0952** | fit {4,8,16}; **exclude 32²** | 4.176712 (the TXT's own 4-point value 5.485710 **rejected**) |
| **4. control-k evidence** (k = (0.37, 0.19)π/L; 4² not computed there) | –, 3.4e5, 755, **940** | fit {8,16,32}; **exclude nothing** | 4.195543, CI [3.2947, 5.0964], resid 0.0567 |

\* dense path ⇒ SPREAD_FLOOR.

Three facts establish that the decisions come from the pre-declared criterion rather than the
outcome:

1. **The rule sanctions the published value.** Applied to the historical JSON's own data and its own
   era's measured reproducibility, it selects exactly {4², 8², 16²} and reproduces
   `4.173919246515192` bit-identically to the reported slope. (The rule did **not** have to agree with
   the JSON's arbitrary `err > 1e-14` cut — the cut flipped between runs; the rule does not.)
2. **The rule rejects the TXT's subset** on the same grounds — i.e. it does not merely ratify whatever
   happened historically.
3. **The rule retains the control-k point** (ratio 940), where the same condition is not met. So it is
   not a "always drop the finest mesh" rule.

## 6. The required two-seed measurement — **already in hand; no new solves needed**

Every quantity the frozen rule needs is **already archived**:

| need | where it exists |
|---|---|
| s₃₂, s₁₆, s₈ at the 5i k, pinned configuration, seeds 20260924 & 7 | `audit/evidence/p12e/verify_convergence_output.txt` lines 10–12 (`1.239e-14`, `3.679e-14`, `1.603e-13`); corroborated by `discriminate_output.txt` |
| s at the control k | `audit/evidence/p12e/discriminate_output.txt` lines 6–8 (`5.95e-15`, `1.61e-13`, `6.48e-15`) |
| s for the historical era (21 realizations, per mesh) | `audit/evidence/p4b_b1/repro_realizations_summary.json` → 2.897e-14, 1.064e-13, 5.921e-13, 1.262e-12 |
| s for the dense 4² path | bit-deterministic by construction ⇒ SPREAD_FLOOR (no solve needed) |

**Therefore: the `~2 additional solves (~100 s)` mentioned in P12F are NOT required for Route A as
frozen.** They would be needed only if (i) the author wanted a *third* seed for a tighter spread
estimate, or (ii) a new configuration (new k, new tol, changed mesh) were introduced — in which case
Rule R-fit's measurement protocol applies unchanged to that configuration. Explicitly: **no solve is
authorized or performed in this task.**

## 7. Draft Blueprint v1.4 §5.7 — **DRAFT / NOT APPLIED**

> *Nothing below is in the Blueprint. v1.3 remains byte-identical (`ca71b91a…`). This is a proposal
> for the author's decision; issuing it would require a new locked version, never an in-place edit.*

Replacement for the **[STR]** sentence of §5.7 (the rest of the row — bands, first-gap edge,
ε_Δ definition, "conforming-subspace" clause — is unchanged):

> **5.7 — Layer 5 (continued) — mesh convergence and resolution floor.** *[... existing [COR] text
> unchanged: bands at 4×4, 8×8, 16×16, 32×32 BFS cells; report the converged first-gap edge and the
> numerical resolution floor ε_Δ — the smallest gap width distinguishable from noise ...]* **[STR]**
> All four prescribed refinement levels are computed and reported with their eigenvalues, relative
> errors and step-to-step changes. The observed convergence rate is obtained by least squares from
> the levels whose relative error **exceeds the numerical resolution of the measurement**: a level
> participates in the fit if and only if its relative error is greater than the pre-declared factor
> F = 3 times the reproducibility of that level's eigenvalue, measured from two pre-registered start
> vectors at the frozen solver configuration (the protocol and F are fixed before the calculation is
> run and recorded with it). Levels that do not meet this criterion are reported as
> resolution-limited data, with their relative errors, their measured reproducibility and the
> resulting ratio, and are excluded from the fit; the identity of any excluded level is stated in the
> text, the table and the figure caption. The 95 % CI of the fit is reported; a theoretical order is
> claimed only if justified by conforming-subspace eigenvalue theory (Babuška–Osborn); otherwise the
> observed rate is reported as-is, together with the number of fitted levels. If fewer than three
> levels satisfy the criterion, no rate is reported.

Corresponding one-line edit to line 618's row: *"observed convergence rate fitted from the levels
that exceed the pre-declared resolution criterion (§5.7; 95 % CI) — the number of fitted levels and
any excluded level are stated — no theoretical order claimed unless justified"*.

**It is deliberately the smallest change that resolves BPC-1:** bands, observable, ε_Δ, the CI
requirement, the "no theoretical order" rule and the eight-test suite are all untouched, and the
requirement is made *more* explicit (every level still computed and reported; exclusion is now a
documented, rule-governed fact rather than an artefact of an undocumented constant).

## 8. Draft plan amendment (5i / PCR5) — **DRAFT / NOT APPLIED**

Replace plan row 5i's last two clauses and add a PCR5 note. The amendment must keep five quantities
distinct (this is the terminology requirement):

| quantity | definition | role |
|---|---|---|
| **FE discretization trend** | the power-law behaviour of e(h) for levels above the resolution limit | what the reported rate estimates |
| **numerical-resolution floor (measurement)** | per level: s_i, the two-start-vector reproducibility at the frozen configuration | **input to the admissibility rule** |
| **reproducibility spread** | the same s_i quoted as a reported uncertainty for each level | reported uncertainty, never an acceptance threshold |
| **observed rate** | LS slope + 95 % CI over the admissible levels; the number of fitted levels stated | the reported result (no theoretical order) |
| **reported ε_Δ** | max(|ω₃₂−ω₁₆|/ω₃₂, err₃₂) — an *operational* mesh-change floor, distinct from the solver-resolution floor | published resolution quantity |

Draft row-5i text:

> | 5i | Mesh convergence + resolution floor | meshes 4²,8²,16²,32²; per-level error e_i and measured reproducibility s_i (two pre-registered start vectors, frozen configuration) | log-log LS fit over levels with e_i > F·max(s_i, 1e-15), F = 3 pre-declared; excluded levels reported with e_i, s_i, ratio; < 3 admissible ⇒ no rate reported | monotone convergence; observed rate with 95 % CI; **no theoretical order claimed**; ε_Δ reported as the operational mesh-change floor (distinct from the resolution floor) | Fig 5, Table 6 | §5.7 |

PCR5 note (draft): *"PCR5 cross-check covers §5.7, Fig. 5(b), Table 6: verify that the reported rate
is the least-squares fit of exactly the admissible levels; that every excluded level is reported with
e_i, s_i and the ratio; that ε_Δ is reported as the operational mesh-change floor and is not
presented as a solver-resolution measure; and that no theoretical order is claimed."* This also
replaces the tautological "16²→32² change ≤ ε_Δ" sub-check, which verifies nothing.

## 9. Manuscript impact (no file edited)

**Common to any Route-A adoption (documentation-level):**

| location | what must change |
|---|---|
| `latex/sections/sec05_verification.tex` l.106 (the fit sentence) | state that the rate is fitted over the admissible refinement levels and name the excluded level + reason (resolution limit) |
| `tables/out/tab06_convergence_floor.tex` l.12 footer | same qualification (fit subset + excluded level); l.13 ε_Δ line unchanged |
| `figures/out/fig05_mesh_convergence.pdf` (generator `figures/gen/fig05_mesh_convergence.py` l.46–47) + fig. 5 caption | draw the trend line over the fitted levels only; caption states the subset and the excluded level |
| `latex/sections/sec09_conclusions.tex` l.8 | qualify "confirmed" → observed rate over the admissible levels, with the resolution-limited level noted |
| `latex/ms.tex` abstract | optional: name the fitted subset; the "observed … no theoretical order claimed" wording is already correct |
| audit/traceability | `verification/suite/P4B_5g_5i.md` addendum, the TXT provenance file, and (only if numbers change) the guard literals |

**Two sub-options with different numerical consequences — the author must choose one:**

| sub-option | numbers | what it costs |
|---|---|---|
| **A1 — sanction the current artifact** | **unchanged**: 4.173919246515192 / [3.1453687594104447, 5.202469733619939] / 4.6318154949690315e-11 (the rule applied to the artifact's own evidence selects exactly its subset — §5 fact 1) | documentation only; the historical artifact keeps governing; no re-baseline |
| **A2 — re-baseline with the Route-F configuration** | **changes**: 4.180559 / [3.2014, 5.1598] / ε_Δ 4.585037e-11 (quoted at 2 dp/3 sf in the manuscript: p 4.17 → **4.18**, ε_Δ 4.63 → **4.59** ×10⁻¹¹) | one authorized re-baseline: new governing JSON, guard pin re-issue, Table 6 / Fig. 5 / sec05 / sec09 / abstract updates |

Neither sub-option is chosen here.

## 10. Exact implementation steps after authorization (not performed)

1. Authorize **A1** or **A2** and the §5.7/plan texts (§7/§8).
2. Apply Rule R-fit to `p4b_5g_to_5i.py`: per-level e_i, s_i inputs; admission
   `e_i > F·max(s_i, 1e-15)`; the < 3-level guard; record e_i, s_i, ratio, decisions in the JSON.
3. Guards: pin F, SPREAD_FLOOR, seeds, tol, thread pinning, the mesh tuple; test that a mutated rule
   (F change, subset change, mesh change) fails; extend the existing hash/literal guards.
4. **A1 only:** add the evidence file that documents the rule's application to the historical
   artifact (no numeric change, no regeneration).
   **A2 only:** execute the single authorized Route-F production run; create the new governing JSON;
   archive the present JSON/TXT pair as history; re-issue the literal/hash pins in one commit.
5. Manuscript/table/figure edits per §9; run the synthetic discrimination, criterion, mutation,
   reproducibility (×2) and full-suite checks; immutability re-verification of every historical
   artifact.
6. Commit (single focused commit for A2; documentation commit for A1). No push without instruction.

## 11. Explicit non-authorization status

- Route A is **not** adopted; Rule R-fit is **not** implemented in any production file.
- Blueprint v1.3 is **unchanged**; the §5.7 text in §7 is a **DRAFT / NOT APPLIED**.
- The plan amendment in §8 is **DRAFT / NOT APPLIED**; the tautological 5i sub-check is **still in
  place**.
- No solver was run in this task; the two extra solves are **not needed** for the freeze (§6) and were
  **not** performed.
- No manuscript/table/figure/JSON/TXT file was edited; no re-baseline occurred.
- **R-1 remains OPEN · C-1 remains OPEN · G-1 remains CLOSED · BPC-1 remains an open decision item ·
  G3, PCR1, PCR5, G4 and P5 are not claimed closed.**

## 12. Immutability and regression

All 15 protected artifacts plus the `latex/`, `tables/out/` and `figures/out/` trees re-hash to the
P12E pre-change snapshot values with **zero mismatches** (Blueprint `ca71b91a…`, P4B JSON
`38384363…`, TXT `1daf0f32…`, P4B script `b1c8d996…`, P12C raw `5547bae4…`/`c8910c0d…`, P11D
`1d4476f1…`/`7dbabbd3…`, manuscript trees `a0f4fb8c…`/`eda2a0e2…`/`2e21a83b…`). Suite run twice after
this documentation-only addition (exact counts/runtimes in the commit record and
`audit/logs/p12g_suite_run{1,2}.txt`). No new production, no manuscript change, no Blueprint change,
no P13, no push.
