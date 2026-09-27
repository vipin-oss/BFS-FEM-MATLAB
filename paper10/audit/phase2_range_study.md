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
* **Empirical Asymptotic Power Laws:**
  $$\sigma_2 \sim \varepsilon_\lambda^{0.9908} \; (R^2 = 0.999993, \approx 7.6 \, \varepsilon_\lambda), \qquad R_J \sim \varepsilon_\lambda^{0.9751} \; (R^2 = 0.999935, \approx 0.90 \, \varepsilon_\lambda), \qquad \operatorname{cond}(F) \sim \varepsilon_\lambda^{-1.9678} \; (R^2 = 0.999975)$$
* **Physical Plausibility & Fluence Calibration:**
  - *Routine low-fluence tests:* Standard ASTM E1461 laser flash tests typically maintain $\Delta T \approx 1$--$3\,\si{\kelvin}$ to suppress radiative losses. With typical $|\beta_T| \approx (0.5$--$3.0) \times 10^{-3}\,\si{\kelvin^{-1}}$, this produces $\varepsilon_\lambda \approx 0.1\%$--$1.0\%$. Even in this routine regime, $\operatorname{cond}(F)$ is regularized from $\sim 10^{17}$ down to $\sim 10^5$.
  - *Elevated-fluence pulses:* Operating at moderate temperature rises $\Delta T \approx 5$--$15\,\si{\kelvin}$ achieves $\varepsilon_\lambda \approx 2\%$--$5\%$ in materials with pronounced temperature dependence, dropping $\operatorname{cond}(F)$ to $\sim 7.4 \times 10^3$.
* **Sign Invariance & Physical Admissibility:**
  - Negative temperature coefficients ($\beta_T < 0$, e.g., rocks, semiconductors, dielectric ceramics where Umklapp phonon scattering dominates) produce sign-symmetric regularization ($\sigma_2 = 0.4008, \operatorname{cond}(F) = 6.05 \times 10^3$ at $\varepsilon_\lambda = -0.05$).
  - Physical conductivity remains strictly positive ($1 + \varepsilon_\lambda \hat{T} \ge 0.70 > 0$), ensuring thermodynamic and physical admissibility.
