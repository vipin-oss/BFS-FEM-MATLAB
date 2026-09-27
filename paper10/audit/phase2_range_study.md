# Phase 2 Audit: Systematic Finite-Fluence Range Study

**Date:** 2026-09-27  
**Status:** PASSED  
**Output Data:** `paper10/runs/final-paper-calculations/table_01_range_study.csv`  
**Execution Script:** `paper10/src/run_range_study.py`

---

## 1. Summary of Parameter Sweep Results

Evaluation across 6 fluence levels $\varepsilon_\lambda = \beta_T(T_{\mathrm{end}} - T_0) \in [0.0, 0.05]$ under fixed nominal resonance settings ($\alpha = 1.0, \tau_q = 0.02, \kappa^2 = 0.02, B = 1.0, \tau_\Delta = 0.04, N_x = 200, h_{\text{rel}} = 10^{-4}$):

| $\varepsilon_\lambda$ | $\rho(J_{\tau_q}, J_{\kappa^2})$ | $1 + \rho$ | $R_J$ | $\sigma_1$ | $\sigma_2$ | $\sigma_1 / \sigma_2$ | $\operatorname{cond}(F)$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0.000** | $-1.000000000000$ | $-2.22 \times 10^{-16}$ | $7.38 \times 10^{-9}$ | $31.723$ | $1.07 \times 10^{-7}$ | $2.95 \times 10^{8}$ | $8.71 \times 10^{16}$ |
| **0.005** | $-0.999997065439$ | $2.93 \times 10^{-6}$ | $4.69 \times 10^{-3}$ | $31.781$ | $0.0385$ | $825.56$ | $6.82 \times 10^{5}$ |
| **0.010** | $-0.999988369562$ | $1.16 \times 10^{-5}$ | $9.32 \times 10^{-3}$ | $31.839$ | $0.0768$ | $414.70$ | $1.72 \times 10^{5}$ |
| **0.020** | $-0.999954297208$ | $4.57 \times 10^{-5}$ | $1.84 \times 10^{-2}$ | $31.956$ | $0.1527$ | $209.22$ | $4.38 \times 10^{4}$ |
| **0.030** | $-0.999898893055$ | $1.01 \times 10^{-4}$ | $2.72 \times 10^{-2}$ | $32.074$ | $0.2280$ | $140.68$ | $1.98 \times 10^{4}$ |
| **0.050** | $-0.999727876243$ | $2.72 \times 10^{-4}$ | $4.42 \times 10^{-2}$ | $32.312$ | $0.3767$ | $85.79$ | $7.36 \times 10^{3}$ |

---

## 2. Trend Analysis
* **Strict Monotonicity:** Regularisation starts immediately at $\varepsilon_\lambda > 0$ with no threshold or deadband.
* **Asymptotic Power Laws:**
  $$\sigma_2 \approx 7.6 \times \varepsilon_\lambda, \qquad R_J \approx 0.90 \times \varepsilon_\lambda, \qquad \operatorname{cond}(F) \propto \varepsilon_\lambda^{-2}$$
* **Physical Plausibility:** Literature data (Ray et al. 2021, Assael et al. 2005) confirm $\varepsilon_\lambda = \beta_T \Delta T \approx 0.5\% - 5\%$ is fully attainable under standard ASTM E1461 pulse heating ($\Delta T \approx 1 - 10\,\si{\kelvin}$).
