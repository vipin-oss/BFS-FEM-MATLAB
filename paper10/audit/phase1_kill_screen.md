# Phase 1 Audit: Extension E1 Mechanism Kill-Screen

**Date:** 2026-09-27  
**Status:** PASSED  
**Objective:** Test whether introducing a temperature-dependent thermal conductivity $\lambda(T) = \lambda_0[1 + \beta_T(T - T_0)]$ breaks the exact sensitivity colinearity $J_{\tau_q} = -\alpha J_{\kappa^2}$ at the Fourier resonance $B = 1$.

---

## 1. Baseline Recovery ($\varepsilon_\lambda = 0.0$, $B = 1.0$)
* **Model Parameters:** $\alpha = 1.0$, $\tau_q = 0.02$, $\kappa^2 = 0.02$, $\tau_\Delta = 0.04$, $N_x = 200$.
* **Correlation $\rho$:** $-1.000000000000$ ($1 + \rho = -2.22 \times 10^{-16}$).
* **Relative Colinearity Deficit:** $R_J = \frac{\|J_{\tau_q} + \alpha J_{\kappa^2}\|}{\|J_{\tau_q}\|} = 7.3825 \times 10^{-9}$ (at ODE solver tolerance).
* **Singular Values:** $\sigma_1 = 31.723$, $\sigma_2 = 1.0749 \times 10^{-7}$.
* **Singular-Value Ratio:** $\sigma_1 / \sigma_2 = 2.9512 \times 10^8$.
* **Fisher Condition Number:** $\operatorname{cond}(F) = 8.7094 \times 10^{16}$ (strictly singular at machine precision).
* **Audit Verdict:** Baseline analytical identity verified to numerical precision.

---

## 2. Nonlinear Thermal Perturbation ($\varepsilon_\lambda = 0.05$, $B = 1.0$)
* **Relative Colinearity Deficit:** $R_J = 4.4217 \times 10^{-2}$ (4.42% departure from colinearity).
* **Correlation $\rho$:** $-0.999727876243$ ($1 + \rho = 2.7212 \times 10^{-4}$).
* **Singular Values:** $\sigma_1 = 32.312$, $\sigma_2 = 0.37665$.
* **Singular-Value Ratio:** $\sigma_1 / \sigma_2 = 85.79$.
* **Fisher Condition Number:** $\operatorname{cond}(F) = 7.3595 \times 10^3$ (13-order-of-magnitude reduction from $8.71 \times 10^{16}$).

---

## 3. Discretization and Differentiation Artifact Checks
1. **Sensitivity Step-Size Check ($h_{\text{rel}} \in [10^{-3}, 10^{-4}, 10^{-5}]$):**
   * $\sigma_2 = 0.37666, 0.37665, 0.37665$ (converged to 5 significant figures).
   * $\operatorname{cond}(F) = 7359.4, 7359.5, 7359.5$ (converged to 5 significant figures).
   * Proves the regularisation is not a finite-difference step artifact.
2. **Spatial Mesh Refinement ($N_x \in [100, 200, 400]$):**
   * $N_x = 100$: $\sigma_2 = 0.37669, \operatorname{cond}(F) = 7358.2, R_J = 0.04421$.
   * $N_x = 200$: $\sigma_2 = 0.37665, \operatorname{cond}(F) = 7359.5, R_J = 0.04422$.
   * $N_x = 400$: $\sigma_2 = 0.37664, \operatorname{cond}(F) = 7359.9, R_J = 0.04422$.
   * Monotonic second-order convergence confirms a genuine physical continuum effect.
