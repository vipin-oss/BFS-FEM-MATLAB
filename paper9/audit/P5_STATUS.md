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
