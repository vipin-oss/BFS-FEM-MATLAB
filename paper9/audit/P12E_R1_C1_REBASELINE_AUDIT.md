# P12E — Controlled R-1 / C-1 Implementation and Single Re-Baseline: Audit Report

**OUTCOME: the controlled re-baseline was STOPPED at the authorized P1–P4 gate (P3 FAIL).
Nothing was installed.** No new governing JSON was created, no scientific artifact of the
repository was modified, no manuscript/table/figure/plan change was made. Route F *did* deliver
solver-level determinism and bit-reproducible reruns — but the Blueprint-literal four-level fit it
enables is **not a power law** at the 5i configuration, so its reported rate is scientifically
inadmissible and the estimator cannot be re-baselined as-is.

Date 2026-09-24 · HEAD `09d519680d234cb98a4021f55f7a986935a37f47` (branch `phase-1-symbolic`) ·
P12C base `0d985029`. No push · no P13 · no P12E values imported or reconstructed (the sandbox
contains no prior P12E artifacts — verified in the snapshot).

---

## 1. Authorization record

| item | authorization (user, 2026-09-24) | executed? |
|---|---|---|
| R-1 | **Route F**: tighten the 5i eigensolver tolerance to ≈1e-14, pin `v0`, pin the thread/BLAS environment, keep the Blueprint §5.7 four-level fit, ONE controlled re-baseline after gates are in place | implemented in a **staged copy** (§4); re-baseline **stopped at the gate** |
| C-1 | **P1–P4 predicate set** + the corresponding plan amendment | implemented and mutation-tested in the staged copy (§7/§8/§13); plan amendment **not applied** (blocked with the re-baseline) |
| constraints | Blueprint v1.3 unchanged unless an actual conflict is found; no 3-point route; no old P12E values; no push; no P13 | honoured (Blueprint conflict **was** found — BPC-1, §12/§18 — but not acted upon) |

## 2. Pre-change snapshot (machine-readable: `evidence/p12e/pre_change_snapshot.json`)

- HEAD `09d51968…`, branch `phase-1-symbolic`, working tree clean.
- host: Python 3.13.14 · NumPy 2.3.5 · SciPy 1.17.1 · Linux 6.1.158+; **thread environment
  unpinned** (all five variables unset at start — the documented G-1 exposure).
- protected hashes recorded (§11); aggregate tree hashes: `latex a0f4fb8c…`, `tables/out
  eda2a0e2…`, `figures/out 2e21a83b…`.
- P12E-artifact check: `paper9/audit/evidence/p12e/` did not exist, `paper9/archive/` does not
  exist, no `*P12E*` file anywhere in `paper9/` → **no prior P12E values are present or imported.**

## 3. Staging decision (and why the repository copy is untouched)

Per Part F, a failed P1–P4 gate forbids installing a re-baseline. To keep the repository in a
scientifically consistent state (the production script must remain the one that produced the
governing artifact), the full implementation was applied to a **mirror copy** at
`/home/user/p12e_stage/paper9/verification/suite/` and executed there; the exact patch is archived
as `evidence/p12e/routeF_patch.diff` (sha256 `03b902d233d9484a…`). The repository copy of
`p4b_5g_to_5i.py` is **byte-identical to the original** (`b1c8d9963b14a19e…`, §11), as required by
Part J. Nothing in the staged tree is committed; the patch is the executable record for the
follow-up decision.

## 4. Route-F implementation (staged; exact logic)

| # | change | exact logic |
|---|---|---|
| 1 | controlled environment | before `import numpy`: `_THREADS = os.environ.get("P4B_THREADS", "1")`, then the same value assigned to `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `VECLIB_MAXIMUM_THREADS` |
| 2 | tightened tolerance | `EIGSOLVER_TOL = 1e-14` (was `1e-12`). Justification: ARPACK's `tol` is relative to λ = ω², so the implied relative error on ω is `tol/2 = 5e-15` — ≈20× above double-precision ε and two orders below the smallest *resolvable* discretization error at the finest mesh |
| 3 | deterministic start vector | `V0_SEED = 20260924`; `deterministic_v0(nd) = np.random.default_rng(V0_SEED).standard_normal(nd)`; passed as `v0=` to `eigsh` |
| 4 | four-level fit | `FIT_MESHES = (4, 8, 16, 32)`; the script hard-fails if the mesh sequence differs; `slope, lo, hi, se = lsq_loglog_slope(hs, errs)` over **all four** points; `resid_max = loglog_max_abs_residual(...)`. The former `err > 1e-14` subset rule and its contradictory comment are removed |
| 5 | P1–P4 criterion | `check_5i_criterion(meshes, rel_err, d16_32, ci_lo, resid_max)` → P1 strict monotone decrease; P2 `ci_lo ≥ P_MIN = 1.0`; P3 `resid_max ≤ R_MAX = ln 1.5 = 0.405465…`; P4 `d16_32 ≤ FLOOR_MAX = 1e-9`. ε_Δ stays a **reported** quantity, no longer a threshold |
| 6 | record | JSON gains `run_label`, `solver_config` (tol, maxiter, v0, threads, env), `5i.fit_subset/fit_meshes/n_fit_points/resid_max/criterion/criterion_pass` |

Guardable constants introduced for the future guard tests: `EIGSOLVER_TOL`, `V0_SEED`,
`FIT_MESHES`, `P_MIN`, `R_MAX`, `FLOOR_MAX`, and the thread-pin source line.

## 5. Solver configuration and accuracy certification

Executed configuration (identical in both runs): `scipy.sparse.linalg.eigsh`, shift-invert
`which='SM'`, `tol=1e-14`, `maxiter=10000`, `v0` = PCG64 seed 20260924, all five thread variables
`"1"`; dense LAPACK path unchanged for n = 4 (nd = 128).

Independent certification of the 32² eigenpair (`evidence/p12e/certify32_fixed.py`):

| tol | seed | solve | \|λ−RQ\|/λ | ω(32²) | rel. err vs M11.3 |
|---|---|---|---|---|---|
| 1e-12 | 20260924 | 50 s | 1.15e-12 | 1.1648553893289719 | 5.03e-14 |
| 1e-14 | 20260924 | 51 s | 4.14e-14 | 1.1648553893289668 | 4.59e-14 |
| 1e-15 | 20260924 | 58 s | 5.94e-13 | 1.1648553893289564 | 3.70e-14 |

Seed variation at the authorized configuration: 8² 1.2e-14 · 16² 3.7e-14 · **32² 1.6e-13**
(relative), i.e. at the 5i k the 32² eigenvalue is reproducible only to ≈1.6e-13 — the same order
as the datum's own error. **Control experiment at a different k** (0.37, 0.19)π/L with the identical
configuration: err8 = 2.045e-9, err16 = 1.215e-10, **err32 = 6.092e-12 with seed spread 6.5e-15**
and ratio err16/err32 = 20.0 (normal h⁴ behaviour). Conclusion: the solver is *not* universally
floor-limited — the off-trend 32² datum at the 5i k is a **configuration-specific near-cancellation
of the leading discretization error**, not a solver artefact.

## 6. Four-level fit evidence (the Part E production calculation)

Run 1 (`evidence/p12e/production_run1.json`, sha256 `0c027bfc3c327f14…`), exit code **1**:

| mesh | nd | ω_T | rel. err |
|---|---|---|---|
| 4² | 128 | 1.1648554069080328 | 1.509125e-08 |
| 8² | 512 | 1.164855390212688 | 7.586990e-10 |
| 16² | 2048 | 1.1648553893823759 | 4.589631e-11 |
| 32² | 8192 | 1.1648553893289668 | 4.593939e-14 |

- **Fit (all four points):** slope **5.902372359347142**, 95 % CI **[1.622235580182,
  10.182509138512]**, se 0.9947, `resid_max` 1.62213423.
- **Four-point participation verified:** recomputing OLS over all four points reproduces the
  reported slope *exactly*; the subsets give materially different values (4,8,16 → 4.180559;
  8,16,32 → 7.005754), so no subset selection occurred. (`resid_max` differs from a Python-float
  recomputation in the 15th digit — float ordering, not a fit discrepancy.)
- ε_Δ = **4.5850373742271716e-11**, d16_32 = 4.5850373742271716e-11 (identical, reported only),
  `floor_flag` True, note "no theoretical order claimed", `P4B = "FAIL"`, rows **23 PASS / 1 FAIL**.

## 7. C-1: implementation and P1–P4 evidence

Implemented exactly as authorized (§4 item 5). On the run data:
**P1 True · P2 True (ci_lo 1.6222 ≥ 1.0) · P3 False (resid_max 1.6221 > 0.405465) · P4 True
(d16_32 4.585e-11 ≤ 1e-9) → `criterion_pass = False`.**

## 8. Synthetic discrimination (run before the scientific calculation, as required)

All required patterns behave correctly (`evidence/p12e/synthetic_discrimination_output.txt`):

| pattern | deployed legacy criterion | P1–P4 criterion |
|---|---|---|
| convergent 4th order | PASS | **PASS** (slope 4.000, ci_lo 3.998, resid 0.001) |
| convergent 2nd order | PASS | **PASS** (2.001 / 1.999 / 0.001) |
| flat plateau | PASS | **FAIL** (P1, P2) |
| oscillatory non-monotone | PASS | **FAIL** (P1, P2, P3, P4) |
| random noise ~1e-3 | PASS | **FAIL** (P1, P2, P4) |
| anti-convergent (growing) | PASS | **FAIL** (P1, P2, P4) |

Predicate-level falsification (mutation targets): P2, P3 and P4 each fail **alone** in a constructed
case; P1 is falsified on a non-monotone sequence and on an exact-tie sequence. **Documented
structural fact:** P1 is *logically implied* by the others for a decreasing, power-law-consistent
sequence (breaking monotonicity requires departing from the trend by ≥ the inter-mesh ratio 16), so
P1 can never fail alone while P2–P4 pass; it is asserted at predicate level and is not redundant as
a *reported* requirement. Guardrail cases also verified: a marginal p ≈ 1.06 law is **accepted**
(P2 exactly at the boundary) and a floor datum exactly at the P4 bound is **accepted**.

## 9. Controlled re-baseline result — GATE FAILED (STOP)

Per Part F the run was performed **once** under the frozen configuration; it failed the criterion,
so no governing JSON was created, no tolerance was tuned, no subset was chosen, and no rerun was
made to chase a PASS. The second execution (§10) is the **authorized reproducibility check**, not a
retry-to-pass.

**Why it fails — exact envelope** (`evidence/p12e/partI_and_band_output.txt`):

| err32 | four-level slope | resid_max | P3 |
|---|---|---|---|
| 2.48e-15 (committed historical datum) | 7.166 | 2.790 | fail |
| 4.59e-14 (Route-F run) | 5.902 | 1.622 | **fail** |
| 2.06e-13 (largest observed realization) | 5.253 | 1.022 | fail |
| 1.00e-12 | 4.569 | 0.390 | pass |
| 2.90e-12 (h⁴ trend from 16²) | 4.108 | 0.078 | pass |
| 1.00e-11 | 3.573 | 0.531 | fail |

P3 accepts only err32 ∈ **[≈9.6e-13, ≈7e-12]**. Every 32² realization ever observed at this
configuration — both committed runs, all probe runs, all tolerances 1e-12…1e-15 — lies in
**2.5e-15 … 2.1e-13**, i.e. **10–1000× below the smallest passing value**. The four-level estimator
is therefore inadmissible *by construction of the data*, not by tuning.

**Design-level analysis (Part F "return to design-level").**
1. The published P12D prediction (p ≈ 4.11–4.16) assumed the accurate 32² datum would sit near the
   h⁴ trend (2.6–2.9e-12). The accurate solve shows it does not: err32 ≲ 1.3e-13. The prediction was
   *conditional on the datum being on-trend*; it is not, so the prediction is not merely missed — it
   is refuted for that configuration.
2. The historical governing artifact fails the same criterion even harder: with the committed ω
   array the four-level fit is slope 7.165, CI **[−0.267, 14.597]**, resid 2.797 (**P2 and P3 fail**).
   The historical 3-point subset (4, 8, 16) passes everything: slope 4.174, CI [3.145, 5.202],
   resid 0.065 — and with the accurate solver it gives slope 4.181, CI [3.201, 5.160], resid 0.062.
3. Therefore **BPC-1 is not a wording issue but a substantive conflict**: the Blueprint-literal
   four-level fit is inadmissible at this configuration, while the published value 4.17 comes from a
   three-level subset the Blueprint does not sanction.
4. Options for the author's decision (design-level, none implemented): (a) **Blueprint v1.4** that
   defines the estimator as the discretization-dominated refinement subset plus an explicit floor
   datum (the P12D "Route C" shape; now *validated* by the new criterion — that subset passes all
   four predicates with the accurate solver); (b) change the **k / mesh set / observable** so all
   four prescribed points sit above the solver's accuracy floor (needs a Blueprint change if the
   bands change; a different k is testable from committed machinery and the control experiment shows
   such a configuration can be resolved to 6.5e-15); (c) extended-precision eigensolver (out of
   scope; does not by itself fix (1) because the datum is genuinely off-trend, not merely noisy).

## 10. Reproducibility result (Part I)

Two complete controlled executions, same pinned configuration:
**JSONs identical in every field except the `utc` timestamp** — ω (all four, 17 significant
digits), rel_err, slope, CI95, `resid_max`, ε_Δ, `d16_32`, criterion flags, and exit code (1) all
bit-identical. Solver-level determinism **is** achieved by Route F within the pinned configuration;
determinism had never been achieved before (`v0` unset + unpinned threads). Both runs took 56–58 s.

## 11. Historical artifact preservation (Part J) — all byte-identical

| artifact | sha256 (before = after) |
|---|---|
| Blueprint v1.3 | `ca71b91aba4ca4abe9f157eb…` |
| P4B **governing JSON** (unchanged, still governing) | `383843632e317c219b4df68f…` |
| P4B **historical TXT** | `1daf0f322260327919ee321f…` |
| P4B **production script** (original, not patched in the repo) | `b1c8d9963b14a19e0f62b294…` |
| P4B TXT provenance label | `6154a23bfc28e4050cb43631…` |
| P12C raw 32² / 64² (+sidecars) | `5547bae453964946…` / `c8910c0de2188b49…` |
| P11D convergence / Δ_X | `1d4476f12d0b8ae9…` / `7dbabbd3676c33d0…` |
| manuscript `ms.tex` / `sec05` / `sec09` | `917d9d594b9a86e3…` / `6ecad66761d3cce8…` / `174a46b3a6e85771…` |
| `tab02` / `tab06` | `9d1f1cc2d231d810…` / `59c8753d234b62a3…` |
| `plan/CALC_MASTER_PLAN.md` | `0e2c3a3a0e47d435…` |
| aggregate `latex` / `tables/out` / `figures/out` | `a0f4fb8c…` / `eda2a0e2…` / `2e21a83b…` (all unchanged) |

`git status` shows only the new audit files. No scientific artifact changed; nothing was archived
away or overwritten.

## 12. Manuscript / table / figure changes (Part G) — **none**, and why

Part G is conditional on a valid re-baseline; there is none, so no numerical content was touched.
The audit finding is nevertheless important for the paper:

- the manuscript's `p = 4.17`, CI [3.15, 5.20] and ε_Δ = 4.63e-11 remain **exactly as published**;
- the Blueprint-literal four-level fit of the *same* data yields 7.165 with CI [−0.267, 14.597] —
  i.e. the published rate is provably a **three-level** statistic, and the four-level statistic is
  not a power law (P2/P3 fail). This must be decided (and, if appropriate, documented or corrected)
  before the convergence claim is relied upon. No claim of determinism, theoretical order, or
  validated 5i convergence is added; none exists in the current text.

## 13. Mutation matrix (Part H) — 12/12 detected, control passes

Harness: `evidence/p12e/mutation_harness.py`, output `…_output.txt`; each mutation applied to an
isolated copy of the staged implementation inside the suite directory; the discrimination suite must
exit non-zero.

| # | mutation | result |
|---|---|---|
| M5 | solver tolerance 1e-14 → 1e-12 | DETECTED |
| M6 | `v0` seed 20260924 → 7 | DETECTED |
| M7 | thread pin default `"1"` → `"4"` | DETECTED (source-level pin + env assertions) |
| M8 | three-point fit (`FIT_MESHES = (4,8,16)`) | DETECTED |
| M9 | mesh list mutated (4,8,16,64) | DETECTED |
| M10 | P1 weakened (strict → non-strict) | DETECTED |
| M10b | P1 disabled | DETECTED |
| M11 | P2 threshold weakened (1.0 → 0.0) | DETECTED |
| M11b | P2 logic tightened (≥1.5) | DETECTED |
| M12 | P3 threshold weakened (ln1.5 → ln10) | DETECTED |
| M13 | P4 threshold weakened (1e-9 → 1e-5) | DETECTED |
| M13b | P4 logic tightened (`<` bound) | DETECTED |
| control | unmutated implementation | PASS (as expected) |

Hash/evidence-tampering mutations (14th item) are covered by the repository guards proven in
`bb32253` (9 fast-mode + 4 opt-in mutations detected, including coordinated value + hash-pin
tampering); they were not re-run because no production file changed.

## 14. Full regression (Parts H/J)

| run | collected | passed | failed | skipped | exit | runtime |
|---|---|---|---|---|---|---|
| repository suite #1 | 93 | 92 | 0 | 1 | 0 | 7.31 s |
| repository suite #2 | 93 | 92 | 0 | 1 | 0 | 7.03 s |
| B1 guard (fast) ×2 | 10 | 9 | 0 | 1 | 0 | 0.07 s / 0.07 s |
| staged discrimination suite | — | all checks | 0 | 0 | 0 | 0.5 s |
| staged mutation harness | 13 cases | 12 detected + control | 0 | 0 | 0 | 4.3 s |

Logs: `paper9/audit/logs/p12e_suite_run{1,2}.txt` (`450062bf7b844c6a…`). No test was changed.

## 15. Final R-1 status: **OPEN**

| R-1 sub-condition | result |
|---|---|
| solver nondeterminism controlled | **YES** — pinned `v0` + tol 1e-14 + pinned threads; reruns bit-identical (§10) |
| pipeline-level reproducibility | **YES for the executed configuration** — two runs, identical JSON except `utc` |
| four-level Blueprint fit actually used | **YES** — verified exactly (§6) |
| unauthorized fit-subset selection | **NONE** |
| **scientifically admissible re-baselined value** | **NO — P3 fails; the four-level sequence is not a power law** |

R-1 therefore **remains OPEN**: the numerical mechanism is fixed, but the estimator it makes
reproducible is inadmissible, so there is no defensible new published number. Closing R-1 now would
require deciding the BPC-1 question (§18) and re-baselining under that decision.

## 16. Final C-1 status: **OPEN** (per the explicit closure rule)

| C-1 closure condition (Part L) | result |
|---|---|
| P1–P4 implemented exactly | **YES** (§4/§7) |
| synthetic discrimination passes | **YES** (§8) |
| mutation tests detect criterion tampering | **YES** (§13) |
| **actual scientific data satisfy the criterion** | **NO — the 4²…32² data fail P3** |

The *criterion defect* itself (non-discriminant, tautological, arbitrary `1e-14` cut, comment drift)
is remedied by the validated design; the closure rule as written also requires the data to satisfy
it, which they do not. C-1 accordingly stays **OPEN**, with the residual issue reclassified from
"criterion defect" to **"estimator/Blueprint model defect"** (§9 item 3).

## 17. G-1 status: **CLOSED** (unchanged, `bb32253`)

Guard semantics revised to tolerance + property; verified green in default and
`OMP_NUM_THREADS=1` environments with the full mutation matrix. Nothing in P12E affects it.

## 18. PCR / gate implications, remaining blockers, and the exact next authorization required

**Gates (unchanged, not claimed):** PCR1 **NOT PASS** · G3 **not met** · G4 **not met** · P5 **NOT
PASS/OPEN** · B6 **PARTIAL**. No gate is promoted by this task; the 5i convergence row is now an
*explicitly demonstrated* open item rather than a silent one.

**Remaining blockers.**
1. **BPC-1 (now proven, not merely suspected).** Blueprint v1.3 §5.7 prescribes the four-level fit;
   at the 5i configuration that fit is not a power law (P2/P3 fail on both the historical and the
   accurate data). The published 4.17 is a three-level statistic. *Decision required.*
2. **Estimator admissibility.** The 32² datum sits 10–1000× below the trend envelope because the
   discretization error at that k nearly cancels; no tolerance, seed or thread setting changes this
   (demonstrated), and the solver is not the limiter (control experiment at another k: 6.09e-12
   resolved with 6.5e-15 spread).
3. **Manuscript consistency.** Until 1. is decided, the abstract's rate and the Blueprint's
   prescription disagree; nothing may be relaxed or "fixed" silently.
4. Unchanged historical items: P12C anchors, P5 status, P12E-era artifacts absent (not
   reconstructed), sandbox re-provisioning risk for `.git` and `*/out/`.

**Exact authorization required before any further implementation** (pick one):
- **(a) Blueprint v1.4 route** — amend §5.7 to define the reported rate from the discretization-
  dominated refinement subset with the final mesh reported as a floor datum; then re-run the
  authorized Route-F implementation (patch already prepared) with the estimator defined as
  4², 8², 16² and re-baseline Table 6 / Fig. 5 / manuscript once. *Numbers under this option (from
  the accurate run, ready for your inspection): slope 4.180559, CI [3.201, 5.160], resid 0.062,
  ε_Δ 4.585e-11 — all four predicates pass.*
- **(b) Reconfigure the study** — authorize a different k (or mesh bands) so all four prescribed
  points sit above the accuracy floor, then run the same four-level protocol.
- **(c) Keep the current publication as-is** — authorize only documentation of BPC-1 as a known
  deviation (no re-baseline); the manuscript numbers stay.

**Explicitly not done:** no `v0`/tolerance/thread change in the repository, no fit-subset change, no
criterion change, no plan amendment, no re-baseline, no manuscript/table/figure edit, no Blueprint
edit, no P13, no push.
