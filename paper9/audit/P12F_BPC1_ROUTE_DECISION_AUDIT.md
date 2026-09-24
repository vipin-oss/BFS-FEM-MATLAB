# P12F — BPC-1 Forensic Decision Audit (before any Blueprint amendment)

**Decision audit only. Nothing was implemented, chosen, or edited.** No new solver run, no
manuscript/table/figure/plan change, no Blueprint change, no re-baseline. Routes (a)/(b)/(c) are
compared factually; no route is selected here.

Date 2026-09-24 · branch `phase-1-symbolic`. **Commit context:** the sandbox dropped `.git` and every
`*/out/` directory again (third incident) before this audit began; content was restored
byte-identically and re-materialised in `8b09322` (see
`audit/SANDBOX_GIT_RECOVERY_20260924.md`). The superseded local SHAs include the P12E commit
`ff139bf` cited in the task header; this audit sits on the re-materialised history.

Evidence: `audit/evidence/p12e/*` (run-1/run-2 JSON, probes, mutation matrix), the committed P4B
JSON/TXT, the Blueprint/plan text, and recomputations in
`audit/evidence/p12f/partA_verify.py` (+ output). Every number below was **re-derived from the
archived artifacts**, not quoted from a summary.

---

## 1. Part A — independent verification of the P12E findings

### 1.1 Errors recomputed from the controlled run's own ω and closed form

| mesh | ω_T (evidence JSON) | err = \|ω−ω_ex\|/ω_ex (recomputed) | P12E claim | JSON `rel_err` identical |
|---|---|---|---|---|
| 4² | 1.1648554069080328 | 1.509124622201602e-08 | 1.509125e-08 | ✔ |
| 8² | 1.164855390212688 | 7.586989914342928e-10 | 7.586990e-10 | ✔ |
| 16² | 1.1648553893823759 | 4.589631313550422e-11 | 4.589631e-11 | ✔ |
| 32² | 1.1648553893289668 | 4.593939323040078e-14 | 4.593939e-14 | ✔ |

ω_exact = 1.1648553893289133 (M11.3 closed form). The four claimed errors are confirmed.

### 1.2 Fit, CI, residual, criterion

| quantity | recomputed here | evidence JSON | verdict |
|---|---|---|---|
| four-level slope | `5.902372359347142` | `5.902372359347142` | **bit-identical** |
| 95 % CI | [1.622235580182, 10.182509138512] | same | identical |
| residual (log units) | 1.622134232836192 | 1.6221342328361956 | equal to 3.6e-15 (float ordering) |
| P1 / P2 / P3 / P4 | T / T / **F** / T | same | confirmed — `criterion_pass=False` |
| ε_Δ = max(d16_32, err32) | 4.5850373742271716e-11 (= d16_32) | same | confirmed (reported quantity) |

P3 margin: residual 1.62213 vs R_MAX = ln 1.5 = 0.405465 → **fails by 1.2167 in log units**.

### 1.3 Route-F determinism

Run 1 vs run 2 (archived JSONs): **identical in every field except `utc`** — ω (all four, full
float repr), `rel_err`, `slope`, `CI95`, `resid_max`, `eps_Delta`, `d16_32`, `criterion`,
`criterion_pass`, `solver_config`, and the exit code (1). Determinism holds **only within the pinned
configuration** (tol 1e-14, PCG64 seed 20260924, all five thread variables = 1) — the documented
G-1 result stands unchanged.

### 1.4 No hidden subset selection

| fit | slope | residual |
|---|---|---|
| **all four points** | **5.902372** | **1.6221** |
| 4, 8, 16 | 4.180559 | 0.0617 |
| 8, 16, 32 | 7.005754 | 1.3672 |
| 4, 8, 32 | 6.236693 | 0.7996 |

Reported slope == OLS over all four points, exactly. The Route-F patch removes the legacy
`err > 1e-14` filter (confirmed present in the diff as a removal) and the staged script contains
**zero** residual subset-selection constructs. No hidden subset was used.

### 1.5 The 32² datum vs the 4²→16² trend (three solver generations)

| dataset | errs (4²,8²,16²,32²) | 3-point (4,8,16) rate | trend-predicted err32 | observed/predicted |
|---|---|---|---|---|
| Route-F controlled | 1.509e-08, 7.587e-10, 4.590e-11, **4.594e-14** | 4.180559 | 2.4542e-12 | **1.87e-02** (53× below) |
| historical JSON (governing) | 1.509e-08, 7.587e-10, 4.632e-11, **2.478e-15** | 4.173919 | 2.4845e-12 | **9.97e-04** (1003× below) |
| historical TXT (run 1) | 1.509e-08, 7.587e-10, 4.614e-11, **1.201e-13** | 4.176712 | 2.4717e-12 | **4.86e-02** (21× below) |

**All Part A items are confirmed.** The 32² datum is below the coarser-mesh trend in every solver
generation that has ever produced it, by factors of 21× to 1003×.

---

## 2. Part B — is "numerical-resolution/floor datum" justified?

### 2.1 The five candidate explanations, tested against existing evidence

| # | explanation | verdict from existing evidence |
|---|---|---|
| 1 | **floating-point/machine-epsilon floor** | **No.** The datum (4.6e-14) is ~200× above double-precision ε (1.1e-16); a pure FP floor would not move with the start vector, yet it does (below) |
| 2 | **FE discretization error** | **Unresolvable at 32².** The measurement cannot be attributed to discretization at a precision better than the solver's own reproducibility (below); the true FE error is bounded above by ≈2.1e-13 |
| 3 | **configuration-specific superconvergence / cancellation** | **Consistent but unproven.** A genuine near-cancellation of the leading error coefficient at this k would look exactly like this; existing evidence *cannot separate* it from (1)/(5). It is a hypothesis, not an established fact |
| 4 | **mesh-resolution limitation** | **No.** The mesh is the finest prescribed; the limitation is numerical accuracy, not mesh resolution — in fact the mesh has been refined *past* the point the solver can verify |
| 5 | **residual / eigenvalue accuracy of the solver** | **Yes — the operative limit.** Documented: ARPACK's own criterion ratio ‖r‖/\|λ\| ≈ **1.28e-11** (much larger than `tol`), \|λ−RQ\|/λ = 4.1e-14 … 1.2e-12, and the ω value is reproducible across start vectors only to **1.6e-13** (relative) at this mesh/k |

### 2.2 The decisive measurement (already in the P12E evidence)

| configuration | ω(32²) reproducibility across two pre-registered start vectors | measured err32 | **datum / reproducibility** |
|---|---|---|---|
| 5i k = (0.31, 0.22)π/L | **1.60e-13** (relative) | 4.59e-14 | **0.29 — the datum is smaller than the uncertainty of its own measurement** |
| control k = (0.37, 0.19)π/L | **6.5e-15** | 6.09e-12 | **938 — the datum is resolved to ~0.1 %** |

Tolerance sweep at the 5i k (same seed): err32 = 5.03e-14 (tol 1e-12), 4.59e-14 (tol 1e-14),
3.70e-14 (tol 1e-15) — total movement 1.3e-14, i.e. **the datum is insensitive to `tol`**; the limit
is the shift-invert accuracy, not the requested tolerance. Seed sweep (same tol): err32 = 4.59e-14
(seed A) vs **2.06e-13** (seed B) — a factor 4.5 apart.

**Robustness consequence (matters for §4):** the *largest* realization ever observed at 32² in this
configuration (2.06e-13) still fails the four-level power law: slope 5.253, residual 1.022 > 0.405.
No seed, tolerance or thread choice rescues the four-level fit.

### 2.3 What the alternative-k experiment proves — and what it does NOT

**Proves:** the solver is *not* globally floor-limited at ~1e-13; at a different k, the same pinned
configuration resolves a 6.09e-12 discretization error with 6.5e-15 reproducibility (0.1 %
uncertainty), and the 8²→16²→32² rates there are 4.07 and 4.32 (clean, consistent). Therefore the
near-floor behaviour at the 5i k is **configuration-specific**, not an inherent property of the
method, matrix class or environment.

**Does NOT prove:** (i) that the 5i-k 32² datum *equals* the solver's accuracy floor — only that it
lies **below the resolvable threshold**; (ii) that the true FE error at 5i-k/32² is zero or
superconvergent — that is unresolvable with this solver; (iii) that another k would give a clean
*four-level* power law — the 4² point was never computed at the control k, and a coarse-mesh point
can be off-regime anywhere; (iv) that a "floor datum" label is *by itself* the right scientific
description at the 5i k — see the terminology hazard below.

### 2.4 Terminology hazard (recorded)

Two different "floors" must not be conflated:

- **ε_Δ (operational resolution floor, the study's published quantity)** = max(|ω32−ω16|/ω32, err32)
  = 4.585e-11 — dominated by the *16²* discretization error; it measures mesh change, **not** solver
  accuracy.
- **solver accuracy floor** at this k/mesh ≈ 1.6e-13 (from the reproducibility measurement).

Any amendment or manuscript wording that calls the 32² datum a "floor datum" must say which floor is
meant; the datum is *at-or-below the solver's resolution* (accuracy), not "equal to ε_Δ".

**Conclusion of Part B:** calling the 32² value a *datum at the numerical resolution limit* (rather
than a resolved discretization sample) **is evidence-supported**. Calling it *the solver floor* or
*proof of superconvergence* is **not** supported. The defensible statement is: *the 32² error at this
wavenumber is not distinguishable from the solver's numerical noise floor, so it carries no usable
information about the discretization exponent* — and this holds whichever of (2)/(3) is true.

---

## 3. Part G — statistical / numerical sensitivity (no new data manufactured)

### 3.1 Pairwise observed rates

| dataset | 4→8 | 8→16 | 16→32 |
|---|---|---|---|
| Route-F controlled | 4.314 | 4.047 | **9.964** |
| historical governing JSON | 4.314 | 4.034 | **14.190** |

The first two intervals agree at ≈4.0–4.3 in both generations; the last interval is 2.3–3.5× larger
than any plausible local exponent.

### 3.2 Legitimate fit variants

| fit | Route-F controlled slope (95 % CI; residual) | historical JSON slope (95 % CI; residual) |
|---|---|---|
| four levels 4,8,16,32 (**Blueprint-literal**) | 5.9024 ([1.6222, 10.1825]; 1.6221) | 7.1648 ([−0.2671, 14.5967]; 2.7965) |
| three levels 4,8,16 | **4.1806** ([3.2014, 5.1598]; 0.0617) | **4.1739** ([3.1454, 5.2025]; 0.0648) |
| three levels 8,16,32 | 7.0058 (residual 1.3672) | 7.0058 (residual 1.3672) |
| three levels 4,8,32 | 6.2367 (residual 0.7996) | — |

### 3.3 Why the 32² point dominates

The log-mesh abscissae are equally spaced (Δ=ln2), so the slope is driven by the extremes: leverage
on the slope is **0.45 for the 4² and 32² points** versus 0.05 for the 8²/16² points. A single
extreme point displaced **1.62 log-units (≈5×)** below the trend therefore rotates the fitted slope
by +1.72 (4.18 → 5.90) and inflates the residual to 1.62 — the power-law model is simply wrong for
that point. The 16→32 excursion is not a small perturbation; it is the dominant feature of the
four-point dataset.

### 3.4 The exclusion envelope

P3 (residual ≤ ln 1.5) is satisfied only for err32 ∈ [≈9.6e-13, ≈7e-12] — a factor-7 window.
Every datum ever observed at this k, in every configuration (2.5e-15 … 2.1e-13), lies 4.7×–380×
**below** that window. The four-level fit is inadmissible for the 5i k *as a matter of data*, not of
tuning.

---

## 4. Route (a) audit — 3-point (4², 8², 16²) fit + 32² as resolution/floor datum

| # | question | finding |
|---|---|---|
| 1 | Does this remain an "observed convergence rate" under the study's mathematical intent? | **Yes in intent, no in letter.** The Blueprint's intent (line 446/618) is an *observed* rate with CI and no theoretical order; a 3-level fit is still an observed rate. But both Blueprint texts say **"from the four refinement levels"** / "from the four meshes", so the letter is not met without an amendment |
| 2 | Is the three-level fit statistically meaningful? | **Yes, with limited power.** dof = 1 (t = 12.706), CI [3.2014, 5.1598] (width 1.96), residual 0.0617 (≈6 % deviation from the power law). The estimator is also the *reproducible* one: across solver generations it reads 4.173919 (governing JSON), 4.176712 (TXT), 4.180559 (Route-F) — spread **0.16 %**, versus 26.6 % for the deployed 4-level/±cut behaviour |
| 3 | Does it satisfy P1–P4? | **Yes** — recomputed here: P1 monotone ✔, P2 3.2014 ≥ 1.0 ✔, P3 0.0617 ≤ 0.4055 ✔, P4 4.585e-11 ≤ 1e-9 ✔. (Passing the criterion is *not* by itself evidence of admissibility — see 4/5) |
| 4 | Legitimate exclusion because the datum is beyond the resolution regime, or selective omission? | **Legitimate only if implemented as a rule, not as a choice.** Facts: the datum is below the reproducibility of its own measurement (0.29×) in *this* configuration; the same kind of rule applied at the control k **includes** 32² (938× margin); applied to the historical JSON/TXT data it also excludes 32² (2.5e-15 and 1.2e-13, both at/below that era's jitter). So a resolution-based rule is *not* answer-dependent — it tracks resolvability. Without a declared rule, the same exclusion is indistinguishable from selective omission |
| 5 | What objective, pre-declared rule could distinguish a floor point from a fit point? | **Rule R-fit (proposal, NOT adopted):** *a refinement level participates in the rate fit iff its relative error exceeds the measured numerical-resolution threshold by a pre-declared factor F, where the threshold is that level's eigenvalue reproducibility under two pre-registered start vectors at the pinned configuration; non-participating levels are reported as resolution data.* Alternative **Rule R-fixed:** *the finest prescribed level is always reported as the resolution datum and never participates in the rate fit* (simpler; but it would also discard a resolvable finest level, e.g. at the control k) |
| 6 | Can such a rule be stated before looking at the final p? | **Yes.** R-fit uses only quantities measured *before* the fit (errors + two-seed reproducibility per level) and no p. Robustness: at the 5i k the datum/precision ratio is **0.29**, so *any* F ≥ 1 excludes it — the outcome does not depend on the choice of F; and the 16² ratio is 1240, so F ≤ ~1000 keeps it. The rule's verdict is therefore stable across three orders of magnitude of F |

**Recorded risk (neutral):** Route (a) legitimises exactly the family of numbers the manuscript
already carries (4.17–4.18), so it will *look* like rubber-stamping. The audit's position: the case
for (a) rests on 4/5 — the resolution evidence and the pre-declared rule — not on the fact that it
passes P1–P4.

---

## 5. Route (b) audit — change k and/or mesh bands

| # | question | finding |
|---|---|---|
| 1 | What does changing k change scientifically? | The convergence study characterises one wavenumber's discretization behaviour. A different k validates the same numerical method but at a different point of the 1st BZ; the reported rate, the errors, ε_Δ and Fig. 5/Table 6 all change. **Crucially, the manuscript names the current k explicitly** (sec05 l.88: *"at fixed k = (0.31π/L, 0.22π/L)"*), so Route (b) requires manuscript edits beyond the numbers |
| 2 | Is an alternative k already evidenced? | **Partially.** P12E's control experiment at (0.37, 0.19)π/L provides 8², 16², 32² errors: 2.0452e-09, 1.2154e-10, 6.0921e-12 (two seeds each: 6.5e-15 spread at 32²). **The 4² point was never computed there** |
| 3 | Would the same four levels at another k give a clean four-level sequence? | **Not established.** The three known points at the control k give clean rates (8→16: 4.07; 16→32: 4.32) and 32² is resolved to 0.1 %, but the coarse 4² point (missing) could itself be off-regime — exactly the failure mode seen at 16³ elsewhere. Claiming "clean" requires the 4² datum |
| 4 | Would another k alter the scientific quantity being validated? | **Yes, the specific datum; no, the class of claim.** The study would then report the observed rate at k′ rather than at k. Both are legitimate; they are different numbers and must be labelled as such |
| 5 | Would selecting another k after observing failure be selection bias? | **Yes, if done post hoc without pre-declaration.** The failing observation is already in the record; choosing k′ now is choosing a configuration because the first one failed |
| 6 | What pre-declaration makes it defensible? | One of: (i) commit to reporting **both** k values (primary + secondary) with all four levels each, fixed now; (ii) declare a *rule* — "if the finest level is resolution-limited at the study k, compute the pre-declared fallback k′" — with k′ fixed by physical rationale (e.g. a fixed offset in the BZ) before computing; (iii) pre-register a two-k protocol with the decision rule and the exact reporting template. All three require a new production run (≥5 solves/level at two k values) |

**Recorded risk (neutral):** Route (b) produces a *new* datum rather than rationalising the existing
one, but it also discards the published numbers and the manuscript's stated k, and it can only be
made bias-free by pre-declaration.

---

## 6. Route (c) audit — retain the publication, document BPC-1

| # | question | finding |
|---|---|---|
| 1 | Exact deviation | (i) Blueprint §5.7 (and line 618) prescribe a fit over **four** refinement levels; the governing artifact's rate comes from **three** (4², 8², 16²) because of the fixed `err > 1e-14` cut; (ii) that cut is undocumented and contradicted by the code's own comment ("10·min_err"); (iii) plan row 5i's "16²→32² change ≤ ε_Δ" sub-check is tautological by the definition of ε_Δ = max(that change, err32) and therefore verifies nothing; (iv) the four-level fit of the same data is 7.165 with CI [−0.267, 14.597] — inadmissible, so the deviation cannot be "fixed" by simply reporting Blueprint-literally either |
| 2 | Can it be disclosed honestly? | **Yes.** The disclosure would state: the finest level is at/below the solver's numerical-resolution threshold at the study wavenumber (0.29× the reproducibility), the reported rate is the stable 3-level estimator (spread 0.16 %), and the four-level statistic is not a power law. This is a complete and truthful account; it is also an admission that the Blueprint's prescribed estimator is not the one reported |
| 3 | Can PCR5/G3 remain unmet? | **G3: unaffected** — it is the blueprint-locked *published-anchor* validation gate (Layers 1, 2a, 2b at ≤2 %), not a convergence gate; its current "not met" status is about those anchors. **PCR5: cannot be signed off as-is** — PCR5 is the manuscript cross-check covering §5.7 / Fig. 5(b) / Table 6 (Blueprint lines 894, 991), i.e. exactly the convergence evidence; leaving it unmet is consistent with, but does not resolve, the deviation |
| 4 | Can the paper proceed with a documented deviation? | **Procedurally yes; scientifically it depends on the claim.** The published rate is the *stable* estimator and the "no theoretical order claimed" caveat stays true, so the numbers are not wrong. What is wrong is the *protocol*: the paper would claim compliance with a locked Blueprint whose estimator it does not use. Documentation makes that honest; it does not make it compliant |
| 5 | Wording that would require qualification | (i) sec05 l.106 "fit … **across the mesh sequence**" → must state the fitted subset and why the finest level is excluded; (ii) tab06 footer "Fitted convergence rate (empirical least-squares): p = 4.17" → same qualification; (iii) fig. 5 trend-line label ("Empirical fit: p = 4.17") — drawn across four points from a three-point slope; (iv) sec09 l.8 "Monotone mesh convergence … **confirmed** an empirical … rate of p = 4.17" → "confirmed" overstates an observed single-configuration rate; (v) abstract — already safe ("observed empirical least-squares convergence rate … no theoretical order claimed") but the fit subset is unstated; (vi) the tautological ε_Δ sub-check must never be presented as independent verification |

---

## 7. Part F — Blueprint v1.3 §5.7 analysis

**Verbatim (line 446):** *"Bands at 4×4, 8×8, 16×16, 32×32 BFS cells; report the converged
first-gap edge and the numerical resolution floor ε_Δ — the smallest gap width distinguishable from
noise. This is what allows weak anisotropy effects to be claimed as real. **The observed convergence
rate is fitted by least squares from the four refinement levels (with 95 % CI); a theoretical order
is claimed only if justified by conforming-subspace eigenvalue theory (Babuška–Osborn), otherwise
the observed rate is reported as-is.**"* — and line 618: *"observed convergence rate fitted from the
four meshes (95 % CI) — no theoretical order claimed unless justified"*. The document is described as
a **locked plan** (line 999) and its content is marked [COR] (corollary) / [STR] (strong) — the
four-level instruction is inside the **[STR]** sentence.

| # | question | finding |
|---|---|---|
| 1 | Is Route (a) prohibited by v1.3? | **Yes, literally.** A reported rate fitted from three levels contradicts "fitted … from the four refinement levels" (and line 618). The *intent* (observed rate, CI, no theoretical order) is preserved by Route (a); the letter is not |
| 2 | Does treating 32² as a floor datum require an amendment? | **Yes**, for the protocol to be compliant. (An alternative reading — report the four-level rate with a "not a power law at the finest level" caveat — is *also* permitted by v1.3's letter but yields p = 7.165 / CI [−0.267, 14.597], which the study would then have to publish; that is the honest reading of "reported as-is") |
| 3 | Does the amendment change scientific scope or only the estimator definition? | **Only the estimator/reporting rule.** Bands (4²–32²), the observable, the closed-form reference, ε_Δ's operational definition, the P1–P4 acceptance set, and the "no theoretical order" rule are all unchanged. No new physics, no new validation layer |
| 4 | Can a minimal v1.4 preserve the original convergence requirement? | **Yes — it can strengthen it**, by making the resolution criterion explicit instead of implicit: every prescribed level is still computed and reported, and the fit is restricted to levels that are verifiably above the numerical resolution threshold (measured, pre-declared rule). Nothing in the old requirement is dropped |

### 7.1 DRAFT §5.7 replacement text — **NOT APPLIED**

> *Drafted for author review only. It is not in the Blueprint; Blueprint v1.3 remains byte-identical.*

> **5.7 — Layer 5 (continued): mesh convergence and the numerical resolution floor.**
> Bands at 4×4, 8×8, 16×16, 32×32 BFS cells. All four levels are computed and reported with their
> eigenvalues, relative errors and step-to-step changes. The numerical resolution floor ε_Δ is
> reported as the smallest frequency change distinguishable from numerical noise and is defined
> operationally in the calculation plan.
>
> The observed convergence rate is obtained by least squares from all prescribed refinement levels
> whose relative error is **verifiably above the numerical resolution threshold**: a level
> participates in the fit if and only if its relative error exceeds the level's measured eigenvalue
> reproducibility (obtained from two pre-registered start vectors at the frozen solver configuration)
> by the pre-declared factor F ≥ 1. Levels that do not meet this criterion are **not** fitted; they
> are reported as resolution-limited data, together with the criterion's inputs (their error and
> measured reproducibility). The rule, the factor F and the start-vector protocol are fixed before
> the calculation is run. The 95 % CI of the fit is reported; a theoretical order is claimed only if
> justified by conforming-subspace eigenvalue theory (Babuška–Osborn); otherwise the observed rate is
> reported as-is, with the number of fitted levels and the identity of any excluded level stated
> explicitly in the text, the table and the figure caption.

**Open wording decisions for the author (not decided here):** (i) whether F is fixed (e.g. F = 3) or
"F ≥ 1 measured" with the outcome reported; (ii) whether a fallback configuration (Route b) is
pre-registered in the same amendment; (iii) whether the amendment also states the reconstruction
requirement if a *later* re-run changes the excluded set.

---

## 8. Decision matrix (Part H) — factual comparison only, no ranking

| Route | Scientific validity | Blueprint compatibility | Selection-bias risk | Requires new production | Requires Blueprint amendment | Effect on current paper |
|---|---|---|---|---|---|---|
| **A** — 3-level fit (4², 8², 16²) + 32² as resolution datum | valid **iff** the exclusion is governed by a pre-declared, measured resolution rule; the estimator is the reproducible one (0.16 % across generations); its CI is wide (dof = 1) | **not compatible as-is**; compatible after an amendment that keeps all four levels reported (draft in §7.1) | **low if pre-declared** — the rule's verdict is independent of p (0.29 ratio ≪ 1) and it also excludes 32² in the historical data while including it at the control k; **high if retrofitted without the rule** | **No** for the estimator itself (data exist); **yes** if the amended protocol requires the two-seed reproducibility measurement (≈2 extra solves) | **Yes** (estimator/reporting rule only; scope unchanged) | numbers unchanged (4.17 / [3.15, 5.20] / 4.63e-11) but sec05, tab06, fig05 and the Blueprint cross-check need the fit-subset qualification; protocol becomes compliant |
| **B** — change k and/or mesh bands | valid if the new k is physically justified and pre-declared; the control-k evidence shows the method resolves 6.09e-12 at 32² with 0.1 % precision, but **no 4² datum exists at any alternative k**, and 8,16,32-only fits are not the prescribed estimator either | **not compatible as-is** for the same four-level clause; the amendment would additionally have to name the new k | **high unless pre-declared** — the failing configuration is already on record; a post hoc k choice is textbook selection | **Yes** — at minimum a 4² solve at k′; realistically a full four-level sequence at a pre-declared k′ | **Yes** (estimator text + the study configuration) | numbers change and sec05's explicit k = (0.31π/L, 0.22π/L) sentence must change; Table 6 / Fig. 5 regenerated; the published 4.17/4.63e-11 family is retired |
| **C** — keep the publication, document BPC-1 | the reported rate stays the stable estimator and the claim stays "observed, no theoretical order"; the protocol deviation is real and must be stated; the four-level statistic of the same data (7.165, CI [−0.267, 14.597]) shows the Blueprint-literal route is not available either | **not compatible** — the deviation persists indefinitely; PCR5's convergence evidence cannot be signed off against §5.7 | **none** (nothing is selected post hoc) | **No** | **No** | numbers unchanged; text gains a methods deviation note; the locked-Blueprint compliance statement is weakened; the ε_Δ sub-check remains tautological unless separately fixed |

---

## 9. Authorization boundary

**Available without new authorization (documentation/audit only):** this audit; recording BPC-1, the
resolution measurement and the two-floor terminology hazard; storing the draft §5.7 text as a
proposal; the existing guards and evidence checks.

**Requires explicit authorization:** ① adopting **Rule R-fit** (or R-fixed) and amending §5.7
(Route A) — estimator/reporting change, no numerical re-baseline of the reported values; ② any
**Route B** production run at a new k (new scientific production **plus** a pre-declaration protocol);
③ any statement in the manuscript about the fit subset; ④ fixing the tautological 5i sub-check;
⑤ regenerating Table 6 / Fig. 5 / JSON if a protocol change is decided; ⑥ any Blueprint v1.4
amendment (must be issued as a new locked version, never an in-place edit of v1.3).

---

## 10. Part I — required conclusions (no route chosen)

**10.1 Definitively established.**
1. The P12E evidence is exactly as reported (errors, slope 5.902372359347142, CI [1.622235580182,
   10.182509138512], residual 1.62213, P1/P2/P3/P4 = T/T/F/T, bit-reproducible reruns, no hidden
   subset).
2. At the study wavenumber the 32² datum is **below the reproducibility of its own measurement**
   (0.29×) and ~53× below the coarser-mesh trend; at 32² the solver resolves only ~1.6e-13.
3. The Blueprint-literal four-level fit is **inadmissible for these data** in every configuration
   tested (best case: slope 5.253, residual 1.022 > 0.405).
4. The published rate (4.17/4.18 family) is a **three-level** statistic, reproducible to 0.16 %
   across three solver generations.
5. The solver is **not** globally floor-limited (control k resolves 6.09e-12 at 0.1 %).

**10.2 Remains scientifically ambiguous.**
1. Whether the 5i-k 32² value is a true superconvergent discretization error or an accuracy-limited
   measurement — existing evidence cannot separate these; only the *consequence* (no usable
   discretization information) is established.
2. Whether the 4²–16² sequence is asymptotic to high precision (the 3-point residual 0.062 is small
   but nonzero; dof = 1 gives a wide CI).
3. Whether an alternative k would give a clean four-level power law (the 4² datum is missing; the
   control point could be off-regime).
4. Which of the three routes the author considers scientifically preferable — a judgement this audit
   deliberately does not make.

**10.3 Technically available routes.** All three: (a) — data are in hand; (b) — requires one new
four-level sequence at a pre-declared k; (c) — requires only a disclosed deviation note.

**10.4 Additional authorization/evidence each route requires.** (a) authorize Rule R-fit + §5.7 v1.4
draft (and the two-seed reproducibility measurement, ≈2 solves, if the rule is written that way);
(b) authorize the production run **and** pre-register k′ and the reporting template beforehand;
(c) authorize nothing numerically — only the manuscript deviation text.

**10.5 Can Blueprint v1.3 stay unchanged?** Technically yes (Route C leaves it untouched, at the cost
of a permanent documented deviation). For any route that *reports* a three-level rate as compliant,
**no** — an amendment (v1.4) is required, and it can be issued without weakening the convergence
requirement (§7.1 draft).

**10.6 Is another scientific calculation genuinely necessary?** Not for Route (a) or (c). For
Route (a) the only computation a strict version of the rule would add is the **two-seed
reproducibility measurement** (≈2 solves at 32², ~100 s) — a diagnostic, not a new science
calculation. Route (b) requires a new four-level production sequence by construction.

---

## 11. Immutability and regression (Parts K/L)

Protected artifacts re-verified against the P12E pre-change snapshot after this audit (zero
mismatches): Blueprint v1.3 `ca71b91a…`, P4B governing JSON `38384363…`, historical TXT `1daf0f32…`,
original P4B script `b1c8d996…`, P12C raw `5547bae4…`/`c8910c0d…`, P11D `1d4476f1…`/`7dbabbd3…`,
manuscript `latex/` tree `a0f4fb8c…`, `tables/out` `eda2a0e2…`, `figures/out` `2e21a83b…`; P12E
staged patch `03b902d2…` unchanged.

Full suite after this documentation addition, twice: **93 collected → 92 passed, 0 failed,
1 skipped, exit 0** (7.50 s / 6.59 s); logs `audit/logs/p12f_suite_run{1,2}.txt`
(`8a9c4ebc9aee0f1d…` / `19146c59a6ffa2a4…`). No new production, no manuscript change, no Blueprint
change, no P13, no push.

## 12. Scope limits

No solver run; no parameter sweep; no route selected; no threshold tuned; no manuscript, table,
figure, plan or Blueprint edit; no re-baseline; no import or reconstruction of any lost P12E value.
The draft §5.7 text in §7.1 is a proposal for review and is **not applied**.
