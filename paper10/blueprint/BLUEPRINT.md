# Paper 10 Blueprint: Regularization of the Guyer–Krumhansl Fourier-Resonance Parameter Degeneracy by Finite Laser Pulse Fluence

**Status:** Phase 1 (Kill-Screen), Phase 2 (Range Study), and Phase 3 (Classical Nonlinear Fourier Validation) **PASSED**.  
**Governing Directive:** Reproducibility & Artifact Preservation Rule.  
**Target Journal:** *International Journal of Heat and Mass Transfer* (or *Applied Thermal Engineering*).

---

## 1. Scientific Objective and Core Problem

In linear Guyer–Krumhansl (GK) heat conduction:
$$\rho c \, \frac{\partial T}{\partial t} + \frac{\partial q}{\partial x} = 0$$
$$\tau_q \, \frac{\partial q}{\partial t} + q + \lambda_0 \, \frac{\partial T}{\partial x} - \kappa^2 \, \frac{\partial^2 q}{\partial x^2} = 0$$
when the Fourier-resonance condition holds:
$$B = \frac{\kappa^2}{\alpha \tau_q} = 1 \qquad (\alpha = \lambda_0 / \rho c)$$
the propagation factor simplifies identically to the classical Fourier factor ($m^2(s) = s/\alpha$). Consequently, the rear-face temperature response becomes completely independent of $\tau_q$, producing the exact analytical sensitivity colinearity:
$$\frac{\partial T}{\partial \tau_q} = -\alpha \, \frac{\partial T}{\partial \kappa^2}$$
This causes structural non-identifiability: the sensitivity Jacobian has rank 1, the Fisher Information Matrix (FIM) has determinant 0, and the relaxation time $\tau_q$ cannot be separated from the nonlocal length $\kappa^2$ from temperature measurements alone.

**Primary Research Question:**
> *Can the temperature dependence of thermal conductivity induced by finite laser pulse fluence ($\lambda(T) = \lambda_0[1 + \beta_T(T-T_0)]$) break this exact sensitivity colinearity and regularize the Fourier-resonance parameter singularity in practical laser flash experiments?*

---

## 2. Governing Equations of Extension E1

The one-dimensional finite-fluence Guyer–Krumhansl formulation across a slab $x \in [0, L]$ is:
1. **Internal Energy Balance:**
   $$\rho c \, \frac{\partial T}{\partial t} + \frac{\partial q}{\partial x} = 0$$
2. **Finite-Fluence Constitutive Relation:**
   $$\tau_q \, \frac{\partial q}{\partial t} + q + \lambda_0\left[1 + \beta_T(T - T_0)\right]\frac{\partial T}{\partial x} - \kappa^2 \, \frac{\partial^2 q}{\partial x^2} = 0$$

### Dimensionless Scaling
Using $T_{\mathrm{end}} - T_0 = \frac{q_{\max} t_p}{\rho c L}$, $\tau_\Delta = \frac{\alpha t_p}{L^2}$, $\hat{\tau}_q = \frac{\alpha \tau_q}{L^2}$, $\hat{\kappa}^2 = \frac{\kappa^2}{L^2}$, and fluence parameter:
$$\varepsilon_\lambda = \beta_T(T_{\mathrm{end}} - T_0)$$
the dimensionless system is:
$$\tau_\Delta \, \frac{\partial \hat{T}}{\partial \hat{t}} + \frac{\partial \hat{q}}{\partial \hat{x}} = 0$$
$$\hat{\tau}_q \, \frac{\partial \hat{q}}{\partial \hat{t}} + \hat{q} + \tau_\Delta\left(1 + \varepsilon_\lambda \hat{T}\right)\frac{\partial \hat{T}}{\partial \hat{x}} - \hat{\kappa}^2 \, \frac{\partial^2 \hat{q}}{\partial \hat{x}^2} = 0$$
subject to the standard flash boundary conditions:
* Front face ($\hat{x} = 0$): $\hat{q}(0, \hat{t}) = 1 - \cos(2\pi \hat{t}/\tau_\Delta)$ for $0 < \hat{t} \le \tau_\Delta$, and $0$ for $\hat{t} > \tau_\Delta$.
* Rear face ($\hat{x} = 1$): $\hat{q}(1, \hat{t}) = 0$ (adiabatic).
* Initial conditions: $\hat{T}(\hat{x}, 0) = 0, \hat{q}(\hat{x}, 0) = 0$.

---

## 3. Strict Limiting Cases and Recovery Paths

The E1 model preserves two rigorous, mathematically clean reduction paths:

### Level 1: Linear Guyer–Krumhansl Baseline Recovery
$$\varepsilon_\lambda \to 0 \quad \Longrightarrow \quad \text{Precursor validated linear GK model recovered identically.}$$
* Confirmed: Relative sensitivity colinearity error $\le 7.38 \times 10^{-9}$, $\rho = -1.000000000000$, $\operatorname{cond}(F) \sim 10^{17}$.

### Level 2: Classical Nonlinear Fourier Limit
$$\tau_q \to 0, \; \kappa^2 \to 0 \quad \Longrightarrow \quad \rho c \, \frac{\partial T}{\partial t} = \frac{\partial}{\partial x}\left[\lambda_0(1 + \beta_T(T-T_0))\frac{\partial T}{\partial x}\right]$$
* Confirmed: Exact agreement ($E_\infty \le 2.3 \times 10^{-9}$) against independently formulated Finite Volume Radau IIA reference solver across all $\varepsilon_\lambda \in [0, 0.05]$.

---

## 4. Key Scientific Results Established

1. **Systematic Lifting of Rank Deficiency:**
   Under finite fluence ($\varepsilon_\lambda > 0$), the local effective diffusivity $\alpha(x,t) = \lambda(x,t)/\rho c$ becomes non-uniform through the slab, causing the local resonance ratio $B(x,t) = \frac{\kappa^2}{\alpha(x,t)\tau_q} = \frac{1}{1 + \varepsilon_\lambda T(x,t)}$ to depart from unity.
2. **Asymptotic Power-Law Scaling:**
   * Null singular value: $\sigma_2 \approx 7.6 \times \varepsilon_\lambda$ (linear activation of the second parameter direction).
   * Relative identity departure: $R_J = \frac{\|J_{\tau_q} + \alpha J_{\kappa^2}\|}{\|J_{\tau_q}\|} \approx 0.90 \times \varepsilon_\lambda$.
   * Condition number: $\operatorname{cond}(F) \propto \varepsilon_\lambda^{-2}$ (drops from $8.7 \times 10^{16}$ at $\varepsilon_\lambda = 0$ to $7.36 \times 10^3$ at $\varepsilon_\lambda = 0.05$).
3. **Physical Plausibility:**
   Representative published values of $\beta_T$ in geological rocks (Ray et al. 2021), ceramics, polymers (Assael et al. 2005), and semiconductors confirm that the range $\varepsilon_\lambda \in [0.005, 0.05]$ is directly realized under standard ASTM E1461 laser flash temperature rises ($\Delta T \approx 1 - 10\,\si{\kelvin}$).
