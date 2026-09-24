# P12D — Post-B1 / C-1 Controlled Remediation Design Audit

**Design only — nothing in this document has been implemented.**
Date 2026-09-24 · HEAD `bb322539c8a9738bd19af91d677d846a84d1e81d` · branch `phase-1-symbolic` ·
P12C base `0d985029`. No push · no P12E/P13 · no P12C calculation · no new scientific production ·
no solver run · Blueprint v1.3, P4B outputs, authoritative JSON/TXT, P12C evidence and the
manuscript numerical baseline untouched.

Evidence: committed JSON/TXT/script, the 21-realization bundle, the Blueprint/plan text, and two
pure post-processing design probes (synthetic sequences + committed evidence only):
`audit/evidence/p12d/partC_baseline_impact.py`, `audit/evidence/p12d/partB_criterion_prototype.py`
with their outputs.

**Terminology (strict).** *Artifact-level reproducibility* · *pipeline-level reproducibility* ·
*solver-level determinism* · *scientific validation* · *guard robustness* — as defined in
`P4B_POST_B1_INDEPENDENT_AUDIT.md` §1 and `P4B_POST_B1_REMEDIATION_READINESS.md`.

## 1. Executive status

| item | status | one-line |
|---|---|---|
| **R-1** pipeline-level reproducibility | **OPEN** | estimator branch flips with solver realization; a *new* finding changes the remediation options: the Blueprint-prescribed fit is the **four-level** fit, which the deployed `err > 1e-14` cut sometimes violates |
| **C-1** 5i criterion | **OPEN** | deployed acceptance is non-discriminant; a discriminant replacement is designed and prototype-tested here (synthetic patterns) |
| **G-1** environment-sensitive guard | **CLOSED** | closed in `bb32253` (tolerance + property semantics; verified default and `OMP_NUM_THREADS=1`) |
| **BPC-1** Blueprint-compatibility finding | **NEW** | Blueprint v1.3 §5.7 prescribes "fitted by least squares **from the four refinement levels**"; the deployed cut reports a **three-level** fit in the governing run → the current published p = 4.17 comes from a fit subset the Blueprint does not sanction |
| published baseline | frozen | slope 4.173919246515192 · CI [3.1453687594104447, 5.202469733619939] · ε_Δ 4.6318154949690315e-11 remain the governing historical artifact; nothing regenerated |

**No remediation route that fixes R-1 preserves the published numbers.** All routes that make the
pipeline reproducible change the reported p (and usually the CI); the only zero-change action is
documentation. This is the central result of this design audit and the reason no implementation is
proposed without authorization.

## 2. R-1 root cause (from committed evidence only)

**Determinism ledger of the six stages** (unchanged from `P4B_R1_PIPELINE_REPRODUCIBILITY_AUDIT.md`):

| stage | verdict | evidence |
|---|---|---|
| 1 matrix assembly | deterministic | K/M CSR hashes equal on rebuild (n=8 `995ad3727f727cdd`, n=16 `e0a3e09d53517ce2`) |
| 2 eigenproblem definition | deterministic | same matrices ⇒ same K̄, M̄; dense path n=4 (nd=128), iterative path n≥8 |
| 3 eigensolver realization | **non-deterministic** | `eigsh(..., which="SM", tol=1e-12)` without `v0`; identical matrices in one process differ by 9.9e-14 (n=16) / 5.5e-13 (n=32); explicit `v0` ⇒ 0.0 |
| 4 post-processing | deterministic | repeated evaluation on identical ω arrays bit-identical |
| 5 fit-subset selection | deterministic, but fed by stage 3 | `if e > 1e-14` |
| 6 regression / reporting | deterministic | OLS reproduces both committed slopes exactly |

**Quantified failure.**
- Declared solver tolerance `tol = 1e-12` is *relative on λ = ω²*, so the implied relative error on ω
  is `tol/2 = 5.0e-13`. Observed per-mesh ω spread across the 21 realizations:
  **2.9e-14 (4²) · 1.06e-13 (8²) · 5.9e-13 (16²) · 1.26e-12 (32²)** — consistent with the declared
  tolerance and increasing with problem size. No branch jumps: the variation is solver-accuracy
  jitter, not a changed eigenbranch.
- The fit predicate `err > 1e-14` has an inclusion window of **±1.165e-14 in ω (2.33e-14 wide)** —
  *30–50× narrower than the solver's own error bar at n = 32* (5e-13 … 1.3e-12). Whether a point is
  fitted is therefore decided by solver noise.
- Consequence: over the 21 documented realizations the deployed rule selects **3 points 1/21 times
  and 4 points 20/21 times**, and the reported slope spans **4.173919 … 5.497868 (26.6 %)**.
- **The 32² datum cannot be a discretization sample.** Extrapolating the committed 16² error with the
  fitted rate gives 2.566e-12 at h = 1/32 (2.895e-12 with p = 4), while the committed JSON reports
  **2.478e-15** — a factor ≈ 1.0e-3 smaller. The datum is simultaneously (i) far below the
  discretization trend and (ii) at/below the solver error bar; no fitting rule can make it carry
  discretization information. It can only serve as a *floor datum*.
- ε_Δ inherits the same realization dependence: **4.550e-11 … 4.679e-11 (2.78 %)** across the same
  21 realizations; the quoted 4.63e-11 occurs in 6/21 draws.

**Artifact-level vs pipeline-level.** Artifact-level reproducibility of the governing JSON is
**established** (slope/CI/ε_Δ re-derive exactly from its own ω array; provenance fixed by B1).
Pipeline-level reproducibility is **not established** (a fresh run reports a different slope in 20/21
cases). Solver-level determinism is **not established** for the iterative path. **Scientific
validation of p = 4.17 is not claimed anywhere and is not established by any of this.**

## 3. R-1 candidate controls (design comparison)

| # | control | changes published baseline? | changes executed behaviour? | changes acceptance criterion? | authorization? | guard-only? |
|---|---|---|---|---|---|---|
| **A** | explicit `v0` | only on regeneration (new realization) | **yes** (pins the draw) | no | **yes** | no (production code) |
| **B** | fixed BLAS/thread environment | no, if not regenerated; per-configuration bit values otherwise | **yes** (environment) | no | **yes** | partially (a CI wrapper could pin env without touching production) |
| **C** | pre-declared fit subset (3-point + floor datum) | no, if not regenerated (run 2 identical under the rule); **yes on regeneration** (typical p = 4.18) | **yes** | **yes** | **yes** | no |
| **D** | deterministic eigenvalue ordering/selection | no | **no effective change** | no | n/a | no |
| **E** | combinations A+B, A+C, A+B+C | as per components | yes | A+B: no · +C: yes | **yes** | no |
| **F** | tighten solver tolerance (e.g. `tol` 1e-12 → 1e-14) | **yes on regeneration** (predicted p ≈ 4.11–4.16, CI [3.88, 4.33]) | yes (cost ↑) | no | **yes** | no |

Notes established from existing evidence:

- **D is a no-op.** `acoustic_omegas` sorts eigenvalues and takes index 0; the selection is already
  deterministic given the values. The non-determinism is in *how accurately ARPACK returns the
  smallest eigenvalue*, not in which index is taken (per-mesh spreads above show smooth jitter, no
  swaps). D therefore cannot fix R-1 and must not be presented as a fix.
- **B alone** does not fix the branch problem: within a fixed configuration the jitter remains
  (seeded runs: err32 = 1.17e-13 … 7.14e-13, all 4-point). It only makes one configuration
  repeatable.
- **A alone** freezes an arbitrary draw: the pipeline becomes reproducible *for that pinned
  configuration*, but the reported rate is whatever the pinned realization gives (in the four-level
  family unless C is also adopted), and it would differ from the committed 4.17 unless the pinned
  draw reproduces run 2's lucky cancellation — probability ≲ 1/21 on the evidence.
- **C alone** stabilizes the *estimator* (0.222 % spread, CI width unchanged in kind) but conflicts
  with Blueprint §5.7 (see §8) and, on regeneration, changes the quoted value (typical **4.18**, not
  4.17 — the committed run is the low outlier of the 3-point family).
- **F** is the only control that makes the **Blueprint-prescribed four-level fit** both meaningful
  and deterministic: with a truthful 32² datum the four points follow the trend
  (predicted 4-level fit **p = 4.108 (err32 from p=4) / 4.160 (err32 from p=4.1739)**, CI95
  **[3.88, 4.33] / [4.00, 4.32]** — i.e. *tighter* than the current CI) and the branch flip
  disappears by construction. It requires a new production solve (forbidden now) and a re-baseline.
- **A+C** is the combination that makes a *stable, reproducible* number, but it is the combination
  that most clearly departs from the Blueprint text.

## 4. C-1 current failure (recap, unchanged)

Deployed acceptance = {four finite ω values} ∧ {slope finite} ∧ {ε_Δ finite} ∧
{`d16_32 ≤ ε_Δ`}, the last being tautological by construction of ε_Δ = max(d16_32, err32). Replicated
on synthetic sequences (previous audit, re-shown in this task's prototype): PASSES flat, oscillatory,
random-noise **and anti-convergent** sequences. `err > 1e-14` is an undocumented arbitrary constant
that contradicts its own comment ("10·min_err"); the commented rule would have selected 3 points in
**both** committed runs (4.176712 / 4.173919).

## 5. Proposed non-tautological criterion (design; prototype-tested)

**Reported quantity (unchanged in kind):** observed rate `p` from a least-squares fit of
log(rel err) vs log h with 95 % CI; no theoretical order claimed. *(Blueprint-consistent: §5.7.)*

**Acceptance predicates (new; all pre-declared, none derived from the quantity under test):**

| id | predicate | pre-declared constant | provenance of the constant |
|---|---|---|---|
| P1 | strict monotone decrease of rel err over the pre-declared meshes | — | property of any convergent sequence |
| P2 | CI **lower bound** of the discretization-dominated sub-fit ≥ `P_MIN` | `P_MIN = 1.0` | weakest non-trivial convergence claim (≥ linear decrease per refinement); prescribed convention |
| P3 | power-law residual of that sub-fit ≤ `R_MAX` | `R_MAX = ln 1.5 ≈ 0.405` | "each point within a factor 1.5 of the fitted line"; prescribed convention |
| P4 | final-doubling floor datum `d16_32 ≤ FLOOR_MAX` | `FLOOR_MAX = 1e-9` | "final doubling changes ω by ≤ 1e-9 relative"; = 2000× the solver error bar implied by the declared tolerance (`tol/2 = 5e-13`); re-derive by the same rule if the tolerance changes |
| P5 | sanity: ω finite, decreasing in mesh; fits defined | — | structural |

**Prototype results** (`partB_criterion_prototype.py`):

| pattern | deployed | proposed | decisive predicate |
|---|---|---|---|
| convergent, 4th order | PASS | PASS | — |
| convergent, 2nd order | PASS | PASS | — (lower rate is legitimately reported as-is) |
| **flat plateau** | PASS | **FAIL** | P1 |
| **oscillatory** | PASS | **FAIL** | P1 |
| **random noise** | PASS | **FAIL** | P1 |
| **anti-convergent (growing)** | PASS | **FAIL** | P1 |
| floor-only (all < 1e-14) | FAIL | FAIL | P2 |
| **committed evidence (21/21 realizations)** | PASS | **PASS 21/21** | margins: CI-lo ≥ 3.145 (≥ 2.145 above P_MIN); residual ≤ 0.065 (≥ 0.34 below R_MAX); floor ≤ 4.68e-11 (21× below FLOOR_MAX) |

The criterion is therefore discriminant on all five mandated patterns while *not* flapping on the
real data. Note the design separates two roles the deployed code conflates: the **reported fit**
(Blueprint §5.7) and the **stability/quality predicates** (P1–P4). P4 replaces the tautological
sub-check with a prescribed bound, and ε_Δ remains a *reported derived quantity* (definition
untouched) rather than an acceptance threshold.

**Governance caveats.** (i) The plan row 5i text ("16²→32² change ≤ ε_Δ") must be amended to match
(plan-level change, not Blueprint). (ii) The choice of which meshes feed the **reported** fit is a
Blueprint question (§8) — the predicates above deliberately do not depend on resolving it, so C-1
can be closed independently of R-1.

## 6. Baseline-impact matrix (what would change if a route were authorized)

*Nothing changes unless a regeneration happens.* With that premise stated, the table gives the
distribution of outputs a fresh run would produce, from the 21 documented realizations
(committed values shown for reference):

| output | committed (governing) | status-quo rule re-run | pre-declared 3-point (C) | Blueprint-literal 4-level (current solver) | 4-level with truthful datum (F, predicted) |
|---|---|---|---|---|---|
| p (file value) | **4.173919246515192** | 4.1739 … 5.4979 | 4.1739 … 4.1832 | 4.6426 … 7.1648 | ≈ 4.108 / 4.160 |
| p as quoted (2 dp) | 4.17 | 4.17 once; 4.6–5.5 otherwise | **4.18 in 20/21 draws** | 4.64–7.16 | ≈ 4.11–4.16 |
| CI95 quoted | [3.15, 5.20] | lo 2.22–3.48 · hi 5.20–8.78 | lo 3.145–3.223 · hi 5.14–5.20 | lo **−0.27** … 3.48 · hi 5.80–14.60 | ≈ [3.88, 4.33] |
| ε_Δ quoted (3 sf) | 4.63e-11 | 4.55–4.68e-11 (4.63e-11 in 6/21) | same | same | same (definition unchanged) |
| JSON `utc`, `rows`, `PASS` text | fixed | new values | new values | new values | new values |
| guard pins (`JSON_SHA`, `PY_SHA`, literals) | fixed | must be re-issued (test-level) | must be re-issued | must be re-issued | must be re-issued |
| Table 6 / Fig. 5 / ms abstract / sec05 / sec09 | 4.17, [3.15,5.20], 4.63e-11 | stale → must be updated | stale → **4.18-family** | stale → 4.6+ / wide CI | stale → ≈4.11–4.16 / tight CI |
| P12C Case-C numbers in the same manuscript | unaffected by any route (different study) | — | — | — | — |

**Explicit preservation rules proposed:** the current JSON/TXT pair remains the **governing historical
artifact** under every route until a separately authorized re-baseline replaces it; any re-baseline
must archive the present pair *and* its guards' pins as history and re-issue both sides in one
commit. No route may silently overwrite them.

## 7. Authorization boundary

**SAFE NOW (no authorization needed; documentation/guard only)**

| item | form |
|---|---|
| this P12D design audit + probes | `audit/P12D_R1_C1_REMEDIATION_DESIGN.md`, `audit/evidence/p12d/*` |
| labelling the governing JSON as a *single realized run* of a nondeterministic solver (mirroring the TXT label) | documentation file next to the artifact |
| recording BPC-1 (Blueprint §5.7 four-level prescription vs the deployed cut) as a documented deviation | audit/governance record |
| evidence-preservation checks (hash pins, literal freeze) | existing guard `test_p4b_b1_json_txt_consistency.py` |
| synthetic-pattern tests of the *proposed* criterion | permitted as design evidence, but they assert nothing about production until the criterion is adopted — kept out of the suite for now |

**REQUIRES EXPLICIT AUTHORIZATION (not implemented, not started)**

| item | exact change | consequence |
|---|---|---|
| ① change solver start vector | production `p4b_5g_to_5i.py`: pass explicit `v0` in `acoustic_omegas` | determines the draw; enables solver-level determinism per environment; new output values |
| ② pin solver/thread environment | execution wrapper / CI environment pin (not the scientific code) | makes ① bit-reproducible per configuration; documented last-bit sensitivity remains across configurations |
| ③ change fit-subset selection | production: replace `err > 1e-14` with a pre-declared rule | stabilizing the estimator; **Blueprint §5.7 conflict if it excludes a refinement level** |
| ④ change 5i acceptance logic | production checks + plan row-5i text | closes C-1; plan amendment required |
| ⑤ regenerate / re-baseline published outputs | new JSON (and TXT run log), new guard pins, updated Table 6/Fig. 5/ms text | changes published p/CI/ε_Δ precision — re-baselining |
| ⑥ change manuscript values | ms.tex, sec05, sec09, tables/out, figures/out | follows from ⑤ only |

## 8. Blueprint compatibility

**Blueprint v1.3 §5.7 (verbatim):** *"Bands at 4×4, 8×8, 16×16, 32×32 BFS cells; report the
converged first-gap edge and the numerical resolution floor ε_Δ — the smallest gap width
distinguishable from noise. … The observed convergence rate is fitted by least squares **from the
four refinement levels** (with 95 % CI); a theoretical order is claimed only if justified by
conforming-subspace eigenvalue theory (Babuška–Osborn), otherwise the observed rate is reported
as-is."* (Also line 618: *"observed convergence rate fitted from the four meshes"*; checklist line
838: *"Observed convergence rate reported; no unjustified theoretical order claimed"*.)

| proposal | Blueprint-compatible? | detail |
|---|---|---|
| C-1 criterion redesign (§5) | **Yes, in principle** | adds verification predicates; does not change the reported-rate definition, does not claim an order. Requires a **plan** row-5i text amendment (the tautological check is named there), not a Blueprint amendment. |
| Route C (pre-declared 3-point fit as the reported fit) | **NO — BPC-1 conflict** | §5.7 requires the reported rate to be fitted from the four refinement levels; a three-level fit is a different statistic. **Stop at design level** (this task): implementing it would require a Blueprint amendment (v1.4), which is outside the current constraints. |
| Route F (tighten `tol`, keep four-level fit) | **Yes** | the prescribed four-level fit becomes meaningful and reproducible; solver tolerance is an implementation parameter, not a Blueprint quantity. Cost and re-baseline consequences remain. |
| Route A+B (pin draw/environment, keep four-level fit) | **Yes** | deterministic realization of the prescribed statistic; the reported value changes to that realization. |
| ε_Δ definition | **Yes as-is** | the Blueprint prescribes *reporting* ε_Δ and its meaning; the formula lives in the plan/record and is untouched by every route above. |
| pre-existing deviation: Blueprint asks for the **converged first-gap edge**, the study reports the acoustic ω̄_T | flagged, **class 2** | Case-H has no gap; the choice is documented in `P4B_5g_5i.md` but is a deviation from §5.7's literal object. Either record it explicitly as an accepted deviation or fold it into a future Blueprint revision; no action taken. |

## 9. Mutation-test design (for the eventual authorized implementation)

All rows are design-level; none is implemented now. "Existing guard" = the B1 guard as committed in
`bb32253`; "new" = to be added with the authorized change.

| # | mutation | where | expected detection mechanism | status |
|---|---|---|---|---|
| 1 | remove `v0` pin / reseed | production solver call | new pipeline test: N seeded fresh runs must reproduce the pinned value/estimator within tolerance | new |
| 2 | fit-subset flip (point added/removed) | fit-selection rule | reported slope must equal the fit of the declared subset; branch must be identical across runs | new (assert released-subset identity) + existing literal freeze |
| 3 | tolerance mutation (`1e-14` / `P_MIN` / `R_MAX` / `FLOOR_MAX`) | constants | constants are pre-declared and pinned by test; changing them fails loudly | new (pin constants) |
| 4 | monotonicity mutation | ω sequence | P1 predicate | new (criterion test on artifact data) |
| 5 | anti-convergence pattern | synthetic sequence through the criterion | P1/P2 (slope negative, CI-lo < P_MIN) | new (criterion unit test, synthetic) |
| 6 | plateau pattern | synthetic | P1/P2 | new |
| 7 | oscillation pattern | synthetic | P1/P3 | new |
| 8 | random-noise pattern | synthetic | P1/P2/P3 | new |
| 9 | hash/evidence tampering (JSON, TXT, provenance label, committed literals, coordinated hash-pin update) | artifacts + guard | existing byte-hash pins + hash-independent literal freeze (proven: 9 fast-mode + 4 opt-in mutations detected, incl. the coordinated case) | **existing** |

## 10. Manuscript claim audit (Part G) — no edits made

| # | location | claim (abridged) | class | note |
|---|---|---|---|---|
| 1 | ms.tex abstract | "mesh convergence across 4² to 32² elements, yielding an observed empirical least-squares convergence rate of p = 4.17 (95 % CI [3.15, 5.20]; **no theoretical order claimed**) and a locked operational numerical resolution floor ε_Δ = 4.63e-11" | **1 defensible** | empirical, CI-qualified, order explicitly disclaimed; consistent with the governing artifact |
| 2 | sec05 l.106 + eq. (5.6) | "A least-squares power-law fit … across the mesh sequence yields an observed empirical convergence rate of p = 4.17 …" | **2 qualify** | does not state that the fit used **three** of the four meshes (BPC-1); fit-model notation differs from the implementation (Δω̄(h)−Δω̄(h_min) vs closed-form reference; numerically equivalent to 3.9e-5 in p) |
| 3 | sec09 l.8 | "**Monotone** mesh convergence across 4² to 32² grids **confirmed** an empirical least-squares rate of p = 4.17 …" | **2 qualify** | monotonicity holds 21/21 (defensible), but "confirmed" asserts more than "observed"; the rate is from one realized run |
| 4 | tables/out/tab06 l.12 footer | "Fitted convergence rate (empirical least-squares): p = 4.17 (95 % CI …; no theoretical order claimed)" | **2 qualify** | table shows four meshes' errors; the fit used three — add a fit-subset note |
| 5 | figures/gen/fig05 + fig. 5 caption | trend line labelled "Empirical fit: p = 4.17 (95 % CI …)"; "Layer 5 mesh convergence analysis" | **2 qualify** | same fit-subset qualification; the trend line is drawn over four points using a three-point slope |
| 6 | tables/out/tab02 l.23 | "ε_Δ = 4.63e-11 … [A] P4B 5i mesh convergence study (commit 1581497)" | **1 defensible** | provenance correct; note the value is one realization of a 2.78 %-wide family |
| 7 | sec05 l.111–118 | "asymptotic numerical resolution floor … 4.63e-11"; "all computed band gaps … exceed ε_Δ by at least eight orders of magnitude, establishing … strictly physical and immune to numerical discretization artifacts" | **1 defensible** | margin recomputed: log₁₀(0.0431/4.63e-11) = 8.97 ✔; the conclusion is robust to the ε_Δ realization spread (21× margin) |
| 8 | sec05 l.11 | "Layer 5: internal numerical verification suite … and mesh convergence to resolution floor" | **1 defensible** | descriptive |
| 9 | P4B record `P4B_5g_5i.md` + JSON `note` | "observed slope 4.17 … runs vary with solver roundoff" | **2 qualify** | already honest; should additionally state the fit subset (3 of 4 levels) and the Blueprint-deviation status (BPC-1) |
| — | any claim of *deterministic reproducibility*, *validated 5i convergence*, or a *theoretical order* | **absent** | **3 not applicable** | verified by scan; no such claim exists in manuscript, tables or figures. Nothing must be withdrawn. |

No manuscript or table text was modified.

## 11. Immutability evidence (Part H)

| artifact | sha256 (start = end) |
|---|---|
| `plan/blueprint/Paper9_Blueprint_v1.3.tex` | `ca71b91aba4ca4abe9f157eb…` |
| P12C 32² raw JSON / 64² raw JSON (+sidecars) | `5547bae453964946…` / `c8910c0de2188b49…` (sidecars verify) |
| P11D convergence / Δ_X | `1d4476f12d0b8ae9…` / `7dbabbd3676c33d0…` |
| P4B historical TXT / governing JSON / production script | `1daf0f3222603279…` / `383843632e317c21…` / `b1c8d9963b14a19e…` |
| manuscript baseline (aggregate): `latex/`, `tables/out/`, `figures/out/` | `9a87d57d31a0ed62…` / `677eade26cde4eac…` / `4e4297ebb826cad8…` |

All values re-checked after the audit was written and after the suite runs; `git diff` shows only the
new P12D files. Nothing protected changed.

## 12. Exact next authorization required

**None of the following was started.** Each item is a decision for the author:

**R-1 — choose exactly one route:**
- **Route F (recommended, Blueprint-compatible):** tighten the 5i eigensolver tolerance
  (`tol` 1e-12 → ≈1e-14) **and** pin `v0` **and** pin the execution thread environment; keep the
  Blueprint-prescribed **four-level** fit; accept one authorized re-baseline. Predicted outcome from
  committed evidence: p ≈ 4.11–4.16, CI ≈ [3.88, 4.33], branch flip gone by construction; cost: the
  32²/64² solves slow down (needs a timing check), and Table 6/Fig. 5/manuscript values must be
  updated in the same authorized change.
- **Route A+B (Blueprint-compatible, weaker):** pin `v0` + environment, keep the current rule; the
  pipeline becomes reproducible *for the pinned realization*, whose reported p will be a four-level
  value (4.64–7.16 family, wide CI) — i.e. the published number gets weaker.
- **Route C (not available now):** pre-declared three-level fit + floor datum — keeps the p ≈ 4.17–4.18
  family but **requires a Blueprint v1.4 amendment** (BPC-1) and a re-baseline; excluded by the
  current "do not modify Blueprint" constraint.
- **Route D (documentation only):** label the governing JSON as a single realized run, record BPC-1 as
  a documented deviation, leave the pipeline unreproducible and R-1 open as a known limitation.

**C-1 — authorize the discriminant predicate set** (§5: P1 monotonicity, P2 `CI-lo ≥ 1.0`, P3
power-law residual ≤ ln 1.5, P4 floor datum ≤ 1e-9; pre-declared constants, ε_Δ kept as a reported
quantity), together with the plan row-5i wording amendment; no Blueprint change required.

**Always required alongside any route:** re-issue the guard pins in the same commit; archive the
present JSON/TXT pair as history; do not silently overwrite evidence; keep "no theoretical order
claimed" in every artifact.

## 13. What was explicitly NOT done in this task

No solver run; no change to `p4b_5g_to_5i.py`; no `v0`; no thread pinning; no fit-subset change; no
criterion change; no regeneration of JSON/TXT; no manuscript, table or figure edit; no Blueprint
change; no P12E/P13 work; no push. R-1 and C-1 remain **OPEN**; G-1 remains **CLOSED**. Findings
BPC-1, the 32²-datum trustworthiness result and the Route F prediction are new design-level results
derived from committed evidence only.
