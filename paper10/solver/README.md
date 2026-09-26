# Phase 2 Solver — Modular Architecture & Usage Guide

### Project: `paper10`
**Document:** `paper10/solver/README.md`  
**Governing Baseline:** Commit `e9ca21f` (Phase 1 Final Locked Baseline)  
**Status:** IMPLEMENTED, AUDITED & VALIDATED

---

## 1. Overview

The `paper10/solver/` package provides a minimal, modular, and mathematically rigorous Transfer Matrix Method (TMM) implementation for phononic metamaterials governed by Mindlin Form-II dipolar gradient elasticity coupled with Tzou Dual-Phase-Lag (DPL) heat conduction.

The architecture strictly separates physics parameter definitions, 4-state conservative anti-plane dynamics, 10-state coupled thermoelastic dynamics, and periodic unit-cell Bloch analysis.

---

## 2. Directory & Module Structure

```
paper10/solver/
├── __init__.py           # Package marker
├── parameters.py         # Material parameters, phase speeds, microscale lengths, DPL parameters
├── antiplane.py          # 4-state decoupled SH shear solver, modal/analytical TMM, symplecticity diagnostics
├── coupled10.py          # Full 10-state coupled DPL-gradient solver, cubic polynomial, canonical equilibration
└── README.md             # This documentation
```

---

## 3. Module Details & Capabilities

### 3.1 `parameters.py`
- `MaterialParameters`: Immutable dataclass encapsulating:
  - Mechanical properties: $\rho$, $\mu$, $\lambda$, $c = g^2$, $d = \sqrt{3}h$.
  - Thermal properties: $k$, $c_v$, $\alpha_t$, $T_0$, $\tau_q$, $\tau_\theta$.
  - Derived parameters: $V_s$, $V_p$, $\beta = (3\lambda+2\mu)\alpha_t$, $m_s(\omega)$, $m_p(\omega)$, $k_{\text{eff}}(\omega)$, $k_{\text{th}}^2(\omega)$, $\eta_{\text{th}}(\omega)$.
- Factory functions:
  - `get_benchmark_papargyri_beskou_material()`: Standard benchmark solid for conservative gradient elasticity validation.
  - `get_li_acta_mech_materials(a)`: Dual-layer metamaterial benchmark from Li, Wei & Zhou (2016, *Acta Mechanica*).

### 3.2 `antiplane.py`
- `AntiPlaneSolver`: 4-state formulation for out-of-plane shear waves:
  $$V_{\text{anti}} = [u_z, u_{z,x}, P_z, R_z]^T$$
- Roots: Exactly 4 spatial roots ($\pm \beta_s, \pm i \gamma_s$) derived from:
  $$c K^2 + (1 - m_s) K - \frac{\omega^2}{V_s^2} = 0$$
- Numerically stable root formulation avoiding catastrophic loss of significance as $c \to 0$:
  $$\sigma_s^2 = \frac{2\omega^2/V_s^2}{\sqrt{(1-m_s)^2 + 4c\omega^2/V_s^2} + (1-m_s)}$$
- Two independent transfer matrix implementations:
  1. Modal decomposition: $T = P G P^{-1}$ with dimensional row-equilibration.
  2. Closed-form analytical formula from Li et al. (2016, Appendix 1).
  *(Cross-check confirms relative discrepancy $< 1.34 \times 10^{-14}$, machine precision).*
- Symplecticity verification: $\det(T) \equiv 1$ and $\|T^T J T - J\| < 10^{-7}$.
- Unit-cell Bloch solver: $T_{\text{cell}} = T_B T_A$ with eigenvalues $\lambda = e^{i k_x a}$.

### 3.3 `coupled10.py`
- `Coupled10StateSolver`: Full 10-state coupled in-plane thermoelastic solver:
  $$V_{\text{in}} = [u_x, u_y, u_{x,x}, u_{y,x}, \theta, P_x, P_y, R_x, R_y, q_x]^T$$
- Characteristic roots: Exactly 10 roots:
  - 4 shear roots: $\pm \beta_s, \pm i \gamma_s$.
  - 6 longitudinal-thermal roots: $\pm \sqrt{K_m - \xi^2}$ ($m = 1, 2, 3$) from the exact cubic polynomial.
- State vector evaluation from first-principles constitutive relations.
- Canonical matrix equilibration: Dual row- and column-balancing ensures $\kappa(P_{\text{equil}}) \sim 10^5$, completely regularizing unscaled $10^{22}$ dimensional disparities.
- Periodic unit-cell Bloch analysis for coupled complex bands.

---

## 4. How to Run Unit Tests & Benchmarks

From the repository root (`/home/user/BFS-FEM-MATLAB`):

```bash
# Run unit tests
python3 paper10/tests/test_parameters.py
python3 paper10/tests/test_antiplane.py
python3 paper10/tests/test_coupled10.py

# Run benchmark validations (Gates G2-B & G2-C)
python3 paper10/validation/run_benchmarks.py

# Run periodic two-layer pilot (Gate G2-D)
python3 paper10/validation/run_periodic_pilot.py
```
