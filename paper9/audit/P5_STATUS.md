# P5 — status (two parallel pipelines; reconciliation outstanding)

> **Provenance note (merge of `aedb501` with `origin/phase-1-symbolic` @ `63c04c7`,
> 2026-09-22).** Two P5 pipelines executed in parallel on this branch from base `1581497`,
> and both added this file. Both records are preserved verbatim below — **Part A** (parallel
> pipeline: pilot 12/12 + studies S1,S3–S9 + TV locks + P6 floats, commits `7bda3cd…63c04c7`)
> and **Part B** (this pipeline: pilot 15/15 + lock request, commit `aedb501`). Neither record
> has been edited by the merge; this note only frames them.
>
> **Agreements:** Case C / S2 stays open in both (no invented parameters); downstream gates
> unchanged in both (B6 PARTIAL / PCR1 NOT PASS / G3 NOT MET).
>
> **Divergences (unreconciled):** solver lineage (new `solver/bfs_bloch_solver.py` vs frozen
> P4A/P4B-assembly reuse in `production/p5/`); sampling (121-pt path + 41×81 half-BZ vs 61-pt
> path + 41×41 full-BZ); reported bands (N = 4 vs N = 8); AR definition/scale (area-preserving
> `l_iso` scaling vs requested ratio definition) and pilot orientation (θ = 45° vs 30°);
> TV4/TV6(Case H)/TV7/TV15/TV16/TV17 values (locked in Part A vs requested in Part B);
> P5 gate (Part A: PASS/G5 PASS; Part B: NOT PASS).
>
> **Branch-level P5 gate: CONTESTED** — no numeric cross-validation between the pipelines has
> been executed (no common (θ, AR, l-scale) point; different solvers), so neither gate claim is
> adopted here. User reconciliation required: at most one [S] set and one gate statement can
> stand.

---

## Part A — parallel pipeline record (verbatim, commits `7bda3cd…63c04c7`)

# P5 — Main Scientific Production (Status Record)

**Branch:** `phase-1-symbolic`  
**Base Commit:** `15814972c812c70e0bb93da7635f75b831178520`  
**Phase:** Phase 5 (Main Scientific Production)  
**Execution Date:** 2026-09-22  

---

## 1. Executive Summary

Phase 5 (Main Scientific Production) has been executed following the locked scientific scope, the frozen `[S]` baseline parameters, and the two-step execution rule:
1. **Pilot Production Case:** ONE small pilot run with 12 automated integrity checks executed and audited. **Result: 12/12 PASS, 0 FAIL -> PILOT PASS.**
2. **Full Production Matrix:** All 8 planned production studies (S1, S3, S4, S5, S6, S7, S8, S9) executed across the locked 42-point $(\theta, \mathrm{AR})$ design grid.
3. **Automated Verification:** 11/11 automated pytest tests passed (`test_p5_production.py` and `test_p4b_5g_5h.py`).
4. **P4A/P4B Suite:** P4A 5a-5f (34/34 PASS) and P4B 5g-5h (3/3 PASS) remain 100% passing.

---

## 2. P5 Pilot Production

- **Pilot Parameters:** Baseline `[S]` case: $L=1.0$, $\lambda=1.0$, $\mu=1.0$, $\rho=1.0$, $\ell^2=0.04$ ($\ell=0.20$), $l_{\mathrm{iso}}=0.20$, $\mathrm{AR}=3.0$, $\theta=45^\circ$ ($l_1=0.30$, $l_2=0.10$).
- **Dataset Dimensions:**
  - Path nodes: $121$ ($N_{\mathrm{seg}} = 40$) along $\Gamma \to X \to M \to \Gamma$.
  - 2D half-BZ grid nodes: $3321$ ($N_{kx} = 41, N_{ky} = 81$) covering $[0, \pi] \times [-\pi, \pi]$.
  - Extracted branches: $N = 4$ lowest physical branches.
- **Integrity Checks (12/12 PASS):**
  1. Solver completion: PASS (clean execution, exit 0).
  2. No NaN/Inf: PASS (all frequencies and eigenvectors strictly finite).
  3. Eigenvalue physical admissibility: PASS ($\omega \ge 0$, $\omega_T(\Gamma) = 0.0$, $\omega_L(\Gamma) = 1.28 \times 10^{-8}$ within eigensolver roundoff).
  4. Matrix Hermiticity consistency: PASS ($\|\bar{\bm K} - \bar{\bm K}^{\mathsf H}\|/\|\bar{\bm K}\| \le 4.64 \times 10^{-16} < 10^{-12}$, $\|\bar{\bm M} - \bar{\bm M}^{\mathsf H}\|/\|\bar{\bm M}\| \le 1.69 \times 10^{-16} < 10^{-12}$).
  5. Branch continuity: PASS (max step variation $\Delta\omega = 0.1923$).
  6. Mode tracking: PASS (Modal Assurance Criterion continuation verified across all 121 path nodes).
  7. Spurious-mode filter: PASS (lowest $N=4$ physical branches cleanly separated from higher discretisation modes).
  8. Numerical resolution floor: PASS (spectral range $5.825 \gg \varepsilon_\Delta = 4.63 \times 10^{-11}$).
  9. Correct BZ/IBZ coverage: PASS (exact breakpoints at $0, 1, 2, 2+\sqrt{2}$; full half-BZ coverage).
  10. Gap taxonomy and subset inequality: PASS ($\Delta[\text{leg}] \ge \Delta[\text{path}] \ge \Delta[\text{complete}]$ verified; $\Delta[\text{complete}] \le 0$ confirmed for Case H).
  11. Bitwise reproducibility: PASS (consecutive back-to-back runs agree to within eigensolver roundoff $|\Delta\omega| = 0.0$).
  12. Metadata and provenance: PASS (unique run ID, commit hash, parameter hash, environment logged).

---

## 3. Full Production Matrix Summary

| Study | Description | Parameter Set / Grid | Status | Key Quantities Extracted |
|---|---|---|---|---|
| **S1** | Case H bands | $\mathrm{AR} \in \{1, 10\}$, $\theta \in \{0^\circ, 45^\circ\}$ | **COMPLETED** | Microstructure dispersion: max $\omega_T = 3.4645$ ($\mathrm{AR}=1$) vs $3.9698$ ($\mathrm{AR}=10, \theta=0^\circ$) and $3.4197$ ($\mathrm{AR}=10, \theta=45^\circ$). |
| **S3** | Orientation sweep | $\theta \in \{0, 15, 30, 45, 60, 75, 90\}^\circ$ at $\mathrm{AR}=5$ | **COMPLETED** | Directional frequency migration: $\omega_T(X)$ migrates from $2.9153$ ($\theta=0^\circ$) to $2.6719$ ($\theta=90^\circ$). Exact $\theta \leftrightarrow 90^\circ-\theta$ diagonal symmetry verified at $M$: $\omega_T(M) = 3.5497$ for both $15^\circ$ and $75^\circ$. |
| **S4** | Aspect-ratio sweep | $\mathrm{AR} \in \{1, 2, 3, 5, 7, 10\}$ at $\theta=45^\circ$ | **COMPLETED** | Monotonic variation of acoustic branch $\omega_T(X)$ from $2.7140$ ($\mathrm{AR}=1$) to $2.9178$ ($\mathrm{AR}=10$). |
| **S5** | Design map | $7 \times 6 = 42$ points on $(\theta, \mathrm{AR})$ | **COMPLETED** | 42 response surface points computed across path and 2D grid. |
| **S6** | Polar map & regimes | $(X = \mathrm{AR}\cos\theta, Y = \mathrm{AR}\sin\theta)$ | **COMPLETED** | Table 5 populated with 126 band-pair records. Hierarchy $\Delta[\text{leg}] \ge \Delta[\text{path}] \ge \Delta[\text{complete}]$ strictly verified in 126/126 checks. Case H complete gaps strictly $\le 0$. 56 positive directional gaps identified. $S_\theta$ calculated for all ARs. |
| **S7** | IFC & wave steering | $\mathrm{AR} \in \{1, 5, 10\}$ at $\theta=45^\circ$, $\bar k = 0.5$ | **COMPLETED** | Group velocity $\bm v_g = \nabla_{\bm k}\omega$ and deviation angle $\delta$: $\delta_{\max} = 0.01^\circ \approx 0^\circ$ for isotropic $\mathrm{AR}=1$; $\delta_{\max} = 1.41^\circ$ for $\mathrm{AR}=5$; $\delta_{\max} = 2.79^\circ$ for $\mathrm{AR}=10$. |
| **S8** | Energy flux partition | $\bar k \in [0.05, 1.0]$ frequency sweep | **COMPLETED** | Gradient strain energy fraction $\langle W_g \rangle / \langle W \rangle$ grows monotonically from $0.20\%$ at $\bar k = 0.1$ to $16.49\%$ at $\bar k = 1.0$. Energy equipartition $\langle W \rangle = \langle T \rangle$ verified on-shell. |
| **S9** | Micro-inertia study | $\bar\ell = 0$ vs $\bar\ell = 0.20 > 0$, $\bar k \in [0.1, 200]$ | **COMPLETED** | $\bar\ell > 0 \implies \bar v_p \to v_{T,\infty} = 0.3162$ ($0.3163$ at $\bar k = 200$, matching theory to $0.03\%$). $\bar\ell = 0 \implies \bar v_p \propto \bar k \to \infty$ ($39.75$ at $\bar k = 200$). Appendix A asymptotic law confirmed. |

---

## 4. Gap Taxonomy and Strict Hierarchy Audit

For all 42 cases $\times$ 3 band pairs (126 records):
$$\Delta[\mathrm{leg}] \ge \Delta[\mathrm{path}] \ge \Delta[\mathrm{complete}]$$
- In all 126 records, the inequality holds with zero violations.
- Maximum complete gap across all 42 cases: $\Delta_{\mathrm{complete}} = -0.3758 \le 0.0$.
- Directional gaps: up to $+0.0896$, demonstrating direction-dependent wave filtering in anisotropic media even in the absence of complete Bragg band gaps.
- Confirms the physical principle: a homogeneous medium exhibits microstructure-induced dispersion and directional stop bands, but does NOT exhibit complete Bragg band gaps.

---

## 5. Artifacts and Provenance

- Master parameters: `paper9/params/params_master.yaml`
- Solver core: `paper9/solver/bfs_bloch_solver.py`
- Pilot production runner: `paper9/production/p5_pilot.py`
- Main production runner: `paper9/production/run_p5_production.py`
- Automated test suite: `paper9/verification/suite/test_p5_production.py`
- Raw immutable data:
  - `paper9/results/raw/p5_pilot_raw.json`
  - `paper9/results/raw/p5_production_raw.json`
- Processed deliverables:
  - `paper9/results/processed/p5_pilot_summary.json`
  - `paper9/results/processed/table5_gap_summary.json`
  - `paper9/results/processed/p5_production_highlights.json`

---

## 6. Scientific Gate Status

- **P5 Status:** **PASS** (pilot 12/12 PASS, production matrix 42/42 points complete, 8 studies complete, 11/11 tests pass).
- **G5 (Plan-level study completeness):** **PASS**.
- **Downstream Gates (Unchanged as required):**
  - **B6:** **PARTIAL** (unchanged).
  - **PCR1:** **NOT PASS** (unchanged).
  - **G3:** **NOT MET** (unchanged).

---

## Part B — production/p5 pipeline record (verbatim, commit `aedb501`)

# P5 — scientific production runs (status)

**Phase order:** P4A → P3 → P4B done; **P5 active**; P6–P9 not started.
**Gate: P5 NOT PASS.** The pilot production case passed all 15 integrity checks; the remaining
frozen P5 cases (S1–S9) are blocked on open parameter decisions (TV4/TV6/TV7/TV14, see §6), so
the gate stays open. Downstream status is unchanged: **B6 PARTIAL / PCR1 NOT PASS / G3 NOT MET**.

Phase-B/phase-1 symbolic results are untouched by this phase; P5 does not revisit B6/LWZ, adds no
published validation, and does not modify the formulation frozen through P4B.

## 1. Pilot production case (required first step)

| item | value |
|---|---|
| run id | `P5-20260922T200303Z-H-pilot-48ea7f9e` |
| status | PILOT (machinery validation; **not** a paper result) |
| parameters | `params/p5_pilot_params.yaml` (hash `48ea7f9e92801dedb601262f6d9ebaf9916a9492b61516fc764ab8ef2eeab145`) |
| basis | Case H, θ = 30°, l1 = 0.30, l2 = 0.10 (generic orientation, actual group C2) |
| resolution | n_mesh = 32 (P4B floor), n_bands = 8 reported, path 3×20+1 = 61 k, zone 41×41 = 1681 k |
| outputs | `results/raw/P5-20260922T200303Z-H-pilot-48ea7f9e/` (+ byte-identical manifest at `runs/P5-20260922T200303Z-H-pilot-48ea7f9e/manifest.json`) |
| wall time | ≈ 1 h 54 min (path 290 s + zone 6426 s solves on 2 pinned workers; remainder checks + manifest) |

### 1.1 Integrity checks (15 PASS / 0 FAIL)

| check | verdict | measured value |
|---|---|---|
| C1 solver completion (1742 k, ndof = 8192, all bands) | PASS | non-finite solves 0 |
| C2a Hermiticity of the reduced pencil | PASS | max_rel 0.0 (tol 1e-12) |
| C2b Bloch phase `K̄(k+G) = K̄(k)`, `ω(k+G) = ω(k)` | PASS | matrix 3.94e-17, ω diff 1.09e-11 (tol 1e-8) |
| C3 resolution at/above the P4B floor | PASS | n_mesh 32 = floor; ε_Δ = 4.6318e-11 |
| C4 tracking (matched MAC, window adequacy) | PASS | min_mac 0.9278 @ step 59 (tol 0.90); 54/60 steps evaluable; drift ≤ 3; no guard risk |
| C9 eigenpair residuals (non-degenerate reported modes) | PASS | max 8.13e-16 (tol 1e-8); 456 modes gated, 32 degenerate excluded |
| C5 no NaN/Inf, no silent negative | PASS | non-finite 0, negative 0, null modes reported 6 |
| C6a frozen gap definition `Δ_path ≥ Δ_complete` | PASS | min slack −1.98e-11 (tol 1e-8) |
| C6b no complete gap where the model cannot have one | PASS | Case H; none claimed; max complete gap −0.4427 |
| C7a k-evenness `ω(−k) = ω(k)` | PASS | max diff 0.0 |
| C7b irreducible extrema = full-grid extrema | PASS | diffs 0.0; domain C2; 861 irreducible points |
| C7c actual group is a symmetry of the spectrum | PASS | C2 residual 0.0 |
| C7d C4v NOT imposed under anisotropy | PASS | R90 witness 0.2872 ≫ 1e-6 |
| C7e X and Y inequivalent (`l1 ≠ l2`) | PASS | \|Δ\| 0.2290; ωX 2.7504, ωY 2.6992 |
| C8 re-solve determinism | PASS | max\|Δω²\| 0.0 (tol 1e-10), 3 repeats |

## 2. What the pilot establishes

* **Solver/no-failure:** every sampled k solved; no NaN/Inf; no unphysical negative eigenvalue; the
  6 internal null modes (Γ rigid translations at the three Γ points) are reported, never dropped
  (TV7 rule: only non-finite/negative roots would be flagged, and they would fail the run).
* **Hermiticity / phase consistency:** `K̄ᴴ = K̄`, `M̄ᴴ = M̄` exactly; `K̄(k+G) = K̄(k)` to 3.9e-17 and
  `ω(k+G) = ω(k)` to 1.1e-11 on three reciprocal vectors.
* **Resolution:** n_mesh = 32 = the P4B-validated floor (ε_Δ = 4.6318154949690315e-11).
* **Branch continuity:** matched-mode MAC ≥ `mac_min = 0.90` on every evaluable step of the path
  (positions of index re-orderings through crossings are reported, M12.2); the tracking window is
  verified adequate (no reported mode matched in the guard band); steps at the high-symmetry
  endpoints Γ, X, M where the spectrum is degenerate by symmetry are reported as not evaluable
  (inside a degenerate cluster the modal basis is arbitrary), not silently skipped.
* **Gaps:** path, directional and complete quantities are computed with the frozen M12.3 definition
  from a single dataset; `Δ_path ≥ Δ_complete` holds to numerical noise because the zone grid
  contains the path nodes; **no complete gap is claimed** for Case H (dispersion only, M12 G6).
* **Zone coverage:** the required irreducible domain of the *actual* group (M10-a ruling (a)) is
  present: irreducible extrema equal full-grid extrema exactly, k-evenness holds pointwise
  (`ω(−k) = ω(k)`), and the actual group C2 is verified as a symmetry of the spectrum.
* **Symmetry discipline:** C4v is *not* imposed under anisotropy — R90 is verified to be a
  non-symmetry (witness residual ≫ tolerance) and Γ–X ≠ Γ–Y by an explicit witness.
* **Reproducibility:** identical re-solve of three path points (bitwise, `max|Δω²| = 0.0`);
  parameters, git state, environment, frozen-source hashes and output hashes are recorded in the
  manifest; raw outputs are written once and made read-only.

## 3. Datasets (pilot)

| file | content | dimensions |
|---|---|---|
| `bands_path.npz` | Γ–X–M–Γ path: k, leg ids, ω, ω², phase velocity | 61 × 8 |
| `zone_omega.npz` | full-BZ grid: k, ω, ω², irreducible mask, spacing | 1681 × 8 |
| `vg_zone.npz` | group velocity on the grid (central differences, M12 (51)) | 1681 × 8 × 2 |
| `gaps.json` | directional / path / complete gaps for 7 adjacent band pairs | 7 pairs |
| `checks.json` | 15 integrity checks with residuals | — |
| `manifest.json` | run id, git, params snapshot + hash, env, output hashes, gates | — |
| `run_log.txt` | full driver log | — |

## 4. Superseded run kept for the record

`results/raw/P5-20260922T170429Z-H-pilot-48ea7f9e/` (14 PASS / 1 FAIL, C4) is kept, not deleted:
it exposed that the P4B-era ARPACK shift `σ = −1e-6` sits on the Γ null cluster and degraded the
sparse eigensolver (cluster splits `4.5e-4`, residuals `5.3e-11`, `min_mac = 0.485`). The diagnosis
and the corrected setting (`σ = −1.0`) are recorded in `audit/P5_READINESS.md §2.4` and
`production/p5/P5_PARAMETER_LOCK_REQUEST.md §2.3`.

## 5. Tests and audits executed

* `python3 -m pytest production/p5/test_p5_integrity.py -q` → **28 passed**.
* `python3 production/p5/lint_p5_params.py --params params/p5_pilot_params.yaml` → **PASS**
  (0 violations; parameters-only rule for solver code).
* Pre-flight runs on a reduced mesh (n_mesh = 16) with the final pipeline → 14 PASS / 1 FAIL
  (C3 only, n_mesh < floor 32 — expected on a pre-flight grid; recorded in
  `audit/P5_READINESS.md §3`).

## 6. Blockers for the remaining frozen cases

1. **Case C (S2, and the gap claims of S3–S8):** inclusion radius/contrast and the `ω₀`, `v̄`
   normalisation phase are not established from the sources (TV6/TV14); the Case-C inclusion
   assembly is not implemented. Case C cannot start by inventing parameters.
2. **AR sweeps (S1, S3, S4, S5):** the frozen M14/M15 assembly has no unit-cell aspect parameter, so
   `AR` must first be defined as the microstructure anisotropy ratio (requested in
   `production/p5/P5_PARAMETER_LOCK_REQUEST.md §3.1`).
3. **S8 energy flux / S9 micro-inertia** drivers are not written yet (P5 scope, later cases).

## 7. Files created in this phase

```
production/p5/p5_core.py                 P5 core (frozen-assembly reuse, solver, MAC, gaps, manifest)
production/p5/p5_run.py                  production run driver (path + zone, 15 checks, raw outputs)
production/p5/lint_p5_params.py          parameters-only lint
production/p5/test_p5_integrity.py       integrity test suite (28 tests)
production/p5/P5_PARAMETER_LOCK_REQUEST.md  requested [S] locks with evidence
params/p5_pilot_params.yaml              pilot parameter file (status: PILOT, tagged + sourced)
audit/P5_READINESS.md                    readiness record, numerical issues, evidence trail
audit/P5_STATUS.md                       this file
results/raw/P5-20260922T200303Z-H-pilot-48ea7f9e/  pilot raw dataset (immutable)
runs/P5-20260922T200303Z-H-pilot-48ea7f9e/manifest.json  plan-specified manifest location (byte-identical copy)
```
