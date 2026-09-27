# Phase 3 Audit: Classical Nonlinear Fourier Limit Validation

**Date:** 2026-09-27  
**Status:** PASSED  
**Output Data:**
  - `paper10/runs/final-paper-calculations/table_02_fourier_limit_validation.csv`
  - `paper10/runs/final-paper-calculations/table_03_mesh_convergence.csv`  
**Execution Script:** `paper10/src/run_fourier_limit_validation.py`

---

## 1. Classical Limit Reduction Audit

Setting $\tau_q \to 0, \kappa^2 \to 0$ in the E1 Guyer–Krumhansl system collapses the flux constitutive law to $q = -\lambda_0[1 + \beta_T(T - T_0)] T_x$, yielding the classical nonlinear parabolic Fourier heat equation:
$$\rho c \, \frac{\partial T}{\partial t} = \frac{\partial}{\partial x}\left[\lambda_0\left(1 + \beta_T(T - T_0)\right)\frac{\partial T}{\partial x}\right]$$

---

## 2. Benchmark Agreement

Comparison between the E1 Fourier limit ($\tau_q = \kappa^2 = 0$, BDF solver) and an independently formulated Finite Volume Method (FVM) solver integrated with Radau IIA (5th-order implicit Runge-Kutta):

| $\varepsilon_\lambda$ | $\Delta T_{\mathrm{rear}}$ | $E_\infty$ | $t(E_\infty)$ | $E_2$ | $E_{\mathrm{peak}}$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **0.00** | $0.9999$ | $2.3214 \times 10^{-9}$ | $0.530$ | $2.0669 \times 10^{-9}$ | $1.9520 \times 10^{-9}$ |
| **0.01** | $0.9999$ | $2.1204 \times 10^{-9}$ | $0.500$ | $1.8734 \times 10^{-9}$ | $1.7493 \times 10^{-9}$ |
| **0.02** | $0.9999$ | $2.0061 \times 10^{-9}$ | $0.500$ | $1.7593 \times 10^{-9}$ | $1.6191 \times 10^{-9}$ |
| **0.05** | $0.9999$ | $1.6296 \times 10^{-9}$ | $0.470$ | $1.3844 \times 10^{-9}$ | $1.2276 \times 10^{-9}$ |

Agreement between the two independent codes is $\le 2.32 \times 10^{-9}$ across all tested fluence levels.

---

## 3. Spatial Mesh Refinement Audit
Reference solver errors against an $N_x = 800$ fine-grid benchmark:

| $\varepsilon_\lambda$ | $e_{100}$ | $e_{200}$ | $e_{400}$ | Order $p_{100 \to 200}$ | Order $p_{200 \to 400}$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **0.00** | $1.6280 \times 10^{-4}$ | $3.8775 \times 10^{-5}$ | $7.7556 \times 10^{-6}$ | **2.07** | **2.32** |
| **0.01** | $1.6535 \times 10^{-4}$ | $3.9382 \times 10^{-5}$ | $7.8771 \times 10^{-6}$ | **2.07** | **2.32** |
| **0.02** | $1.6766 \times 10^{-4}$ | $3.9932 \times 10^{-5}$ | $7.9871 \times 10^{-6}$ | **2.07** | **2.32** |
| **0.05** | $1.7541 \times 10^{-4}$ | $4.1780 \times 10^{-5}$ | $8.3567 \times 10^{-6}$ | **2.07** | **2.32** |

Confirmed asymptotic second-order spatial convergence, matching the documented spatial convergence rate of the precursor computational framework.
