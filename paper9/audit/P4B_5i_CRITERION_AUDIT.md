# P4B 5i Criterion Audit (+ fit-cut comment/implementation drift)

Date 2026-09-24 · HEAD `6f7850d` · branch `phase-1-symbolic`. Audit only — **the criterion was not
modified** (task Part C: "Do not modify it yet"; Part G prohibits changing the fit data / 5i
scientific criterion without explicit classification and authorization).
Evidence: script lines 404-462 of `p4b_5g_to_5i.py`; committed JSON/TXT; the 21-realization bundle;
and a predicate-for-predicate replication on synthetic sequences
(`/home/user/p4b_remediation_logs/partC_probe.py`).

## 1. What the deployed logic actually does (l.404-462)

```python
om_ex = sqrt(ombar2_T(kbar, ellbar, le2)) * w0          # M11.3 closed form
for n in [4, 8, 16, 32]:                                 # measured omega_T per mesh
    om = acoustic_omegas(...); err = |om - om_ex| / om_ex
diffs_16_32 = |oms[-1] - oms[-2]| / oms[-1]
floor_flag  = errs[-1] < 1e-12 or (...)                   # REPORTED ONLY, no assertion uses it
use = [pts with e > 1e-14]                                # fit-subset predicate (fixed constant)
slope, lo, hi, se = lsq_loglog_slope(use) if len(use) >= 3 else (nan,...)
eps_delta = max(diffs_16_32, errs[-1])
# checks emitted:
#  A1 "computed omega_T on 4,8,16,32 meshes"          -> len==4 and all finite
#  A2 "LSQ slope+95% CI reported ... "                -> isfinite(slope)
#  A3 "resolution floor eps_Delta locked as max(...)" -> isfinite(eps_delta)
#  A4 "16^2->32^2 relative change <= eps_Delta"       -> diffs_16_32 <= eps_delta + 1e-30
```

## 2. Independent vs derived quantities

| quantity | status | source |
|---|---|---|
| ω_T(4², 8², 16², 32²) | **independently measured** | FE eigensolve (stage 3 of the R-1 trace) |
| ω_ex = 1.164855389329 | **independently prescribed** | M11.3 closed form (analytical, not FE) |
| rel_err(i) | derived | from the two above |
| d16_32 | derived | from ω(32²), ω(16²) |
| ε_Δ = max(d16_32, err32) | **derived, not prescribed** | definition in the plan row 5i / `CALC_MASTER_PLAN.md` ("candidate = max over IBZ of \|ω(32²) − ω(extrapolated)\|; final wording fixed when computed") |
| slope, CI95 | derived | OLS over the selected points |

The acceptance predicate (A1–A4) uses **only derived quantities and finiteness**. The one
independently-prescribed quantity (ω_ex) is never compared against a tolerance.

## 3. Discrimination test (deployed logic replicated on synthetic sequences)

| synthetic error sequence | what it represents | deployed verdict |
|---|---|---|
| `1e-8, 6.25e-10, 3.91e-11, 2.44e-12` | ideal 4th-order (reference) | PASS |
| `1e-8, 2.5e-9, 6.25e-10, 1.56e-10` | 2nd-order | PASS |
| `1e-8, 2e-8, 4e-8, 8e-8` | **anti-convergent (errors grow 1st-order under refinement)** | **PASS** |
| `1e-3, 1e-3, 1e-3, 1e-3` | flat plateau, no convergence at all | PASS |
| `1e-8, 9e-8, 1e-9, 5e-9` | oscillating, non-monotone | PASS |
| `9.1e-4, 1.02e-3, 9.8e-4, 1.05e-3` | pure random noise around 1e-3 | PASS |
| `1e-8, 1e-15, 1e-16, 1e-17` | degenerate: < 3 points above the cut | FAIL (slope = NaN) |

**Result: the deployed 5i criterion is non-discriminating.** It accepts any finite four-value error
sequence — including an anti-convergent one — provided at least three errors exceed 1e-14. Its only
failure mode is a degenerate fit subset.

## 4. Answers to the mandated questions

| question | finding |
|---|---|
| What is actually being accepted? | Row 5i is accepted **structurally**: four finite ω values + a finite fit + a finite derived ε_Δ + the definitional sub-check. |
| Which quantities are independently measured? | only ω_T(4²…32²) (solver) and ω_ex (analytic). |
| Which are derived from the same data? | rel_err, d16_32, ε_Δ, slope, CI — i.e. **everything the predicate tests**. |
| Is ε_Δ independently prescribed or data-derived? | **Data-derived by design** — `max(|ω₃₂−ω₁₆|/ω₃₂, err₃₂)`. The plan anticipated locking a definition "with evidence"; it did not prescribe a tolerance. |
| Is `err > 1e-14` arbitrary? | **Yes.** No derivation in plan, Blueprint, record or commit history; not machine-epsilon (2.2e-16), not tied to the declared solver tolerance (`tol=1e-12` on λ ⇒ ≈5e-13 at ω level), not resolution-dependent. See §5. |
| Can the criterion accept a non-convergent sequence? | **Yes** — demonstrated above (anti-convergent, flat, noisy all PASS). |
| Can a solver-noise branch change *acceptance*? | **No** in practice: acceptance is invariant to the branch (both branches pass). The branch changes the *reported* slope (5.4857 vs 4.1739). The only theoretical acceptance flip is a degenerate subset (<3 points above the cut), unreachable at these meshes (errors 1.5e-8 … 1e-11 for 4²/8²/16²). |
| Is `d16_32 ≤ ε_Δ` independent evidence? | **No — class C (tautological).** ε_Δ is defined as the max that includes d16_32, so the sub-check is `x ≤ max(x, y)`. Verified to the last bit in both committed runs (d16_32 == ε_Δ exactly). |

## 5. Fit-cut comment/implementation drift (task Part D)

**The discrepancy.** Comment (l.427): *"if last errors ~ machine / search floor, LSQ only on points
above 10*min_err"*. Implementation (l.428-432): `floor_flag = errs[-1] < 1e-12 or (...)` — and a
**separate, fixed** `if e > 1e-14`. The variable that implements the commented rule
(`floor_flag`) is computed but only printed/reported; it is used by no assertion and by no branch.

1. **Historical intent.** Not recoverable beyond the comment itself: the file entered history in a
   single commit (`1581497`), with no design note prescribing a numeric cut; the plan row 5i
   specifies meshes, fit form and ε_Δ, **not** a fit-subset rule. The comment's prose is the only
   statement of intent, and it describes an adaptive rule, whereas the code implements a fixed one.
2. **Numerical consequence (computed, not assumed).** Applying the commented rule to the committed
   arrays (pure post-processing):

   | run | deployed rule | commented rule (10·min_err) |
   |---|---|---|
   | TXT (run 1) | 4 points → slope **5.485710** | 3 points → slope **4.176712** |
   | JSON (run 2) | 3 points → slope **4.173919** | 3 points → slope **4.173919** (unchanged) |

   Over the 21 documented realizations the commented rule selects 3 points **21/21** times
   (vs 1/21 for the deployed rule) and yields slope spread 0.222 % (vs 26.6 %).
3. **Did it affect run 1?** Yes — run 1 is in the 4-point branch *because* of the fixed cut; under
   the commented rule it would have reported 4.176712.
4. **Did it affect run 2?** No — both rules select the same 3 points for run 2's data, so its
   reported slope/CI/ε_Δ are identical under either rule.
5. **Is changing only the comment sufficient?** No. A comment fix would leave the divergence between
   stated intent and executed logic intact, and the executed logic is the one that decides the
   reported estimator. (A comment-only fix is *safe* but *insufficient*; a logic fix is a criterion
   change — see Part F of the readiness report.)
6. **Would changing the implementation require re-baselining?** For the **committed governing
   artifact: no numerical change** (verified above: identical slope/CI/ε_Δ for run 2's data). For the
   **executed pipeline: yes, behaviour changes** (branch selection becomes rule-predetermined), and
   the script's hash pin in the guard would have to be re-issued. Therefore it is classified as
   *criterion-changing* and is **not implemented** without explicit authorization.

## 6. Status

**C-1 OPEN** (criterion non-discriminant; arbitrary cut; comment≠code drift). Nothing modified.
The remediation options, their expected effects and the authorization requirements are in
`P4B_POST_B1_REMEDIATION_READINESS.md` §2/§5.
