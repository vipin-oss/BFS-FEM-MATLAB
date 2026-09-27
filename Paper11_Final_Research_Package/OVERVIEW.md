# Comprehensive Scientific Overview: Paper 11

**Title:** Invariance of the Guyer–Krumhansl Fourier-Resonance Sensitivity Singularity to Boundary Heat Loss in Laser Flash Testing  
**Lead Investigator:** Vipin Gupta  
**Affiliation:** Department of Mathematics, Gurugram University, Gurugram, Haryana 122018, India  

---

## 1. Problem Statement and Physical Motivation

In transient non-Fourier heat conduction characterization via the laser flash method (ASTM E1461), the Guyer--Krumhansl (GK) model accounts for both thermal relaxation and nonlocal phonon scattering through the non-dimensional system:
$$\tau_\Delta \frac{\partial \theta}{\partial t} + \frac{\partial q}{\partial x} = 0,$$
$$\tau_q \frac{\partial q}{\partial t} + q + \tau_\Delta \frac{\partial \theta}{\partial x} - \kappa^2 \frac{\partial^2 q}{\partial x^2} = 0.$$

In an idealized adiabatic analysis ($Bi = 0$), when the parameters satisfy the special algebraic condition $B \equiv \kappa^2 / (\alpha_0 \tau_q) = 1$ ("Fourier resonance"), the temperature field exhibits an exact local sensitivity collinearity:
$$\frac{\partial T}{\partial \tau_q} = -\alpha_0 \frac{\partial T}{\partial \kappa^2}.$$
This collinearity causes the Fisher Information Matrix (FIM) to become rank-deficient ($\operatorname{rank} = 1 < 2$), rendering simultaneous extraction of $\tau_q$ and $\kappa^2$ impossible from temperature measurements alone.

In actual experiments, samples invariably exchange heat with the surrounding environment via convective and radiative cooling ($Bi_0, Bi_L > 0$), producing pronounced cooling tails. In experimental practice, thermal metrologists routinely exploit cooling tails to fit heat-loss parameters, often assuming that the richer transient signal introduces independent degrees of freedom that regularize ill-posed inverse problems.

**The Fundamental Research Question:**  
*Does realistic Robin convective and radiative surface heat loss break the Fourier-resonance parameter singularity between $\tau_q$ and $\kappa^2$? Or is the Fourier-resonance sensitivity collinearity an intrinsic bulk property that remains strictly invariant to boundary cooling?*

---

## 2. Core Theoretical Result: Theorem 1

In the Laplace domain, the general spatial solution for heat flux satisfies:
$$\bar{q}(x, s) = -\tau_\Delta \mu(s) \frac{d\bar{\theta}}{dx}, \qquad \mu(s) \equiv \frac{1 + \kappa^2 s}{1 + \tau_q s},$$
corresponding to a dynamic surface thermal conductivity:
$$\lambda_{\mathrm{eff}}(s) = \lambda_0 \left[\frac{1 + \left(\frac{\kappa^2}{\alpha_0}\right)s}{1 + \tau_q s}\right].$$

At the Fourier-resonance condition $B = 1$ ($\kappa^2 = \alpha_0 \tau_q$):
1. **Dynamic Surface Impedance Collapse:** $\mu(s) \equiv 1 \implies \lambda_{\mathrm{eff}}(s) \equiv \lambda_0$.
2. **Bulk Propagation Operator Collapse:** $m(s) = \sqrt{\frac{s(1+\tau_q s)}{1+\kappa^2 s}} \equiv \sqrt{s}$.

Because both the bulk differential operator and the dynamic surface impedance lose all dependence on $\tau_q$ and $\kappa^2$ simultaneously, the two-point Robin boundary-value problem is formally and identically equivalent to classical Fourier diffusion with surface convection.

> **Theorem 1 (Heat-Loss Invariance at Fourier Resonance).**  
> *For arbitrary non-negative Biot numbers $Bi_0, Bi_L \ge 0$, arbitrary pulse excitation $q_{\mathrm{pulse}}(t)$, all spatial locations $x \in [0, 1]$, and all times $t \ge 0$:*
> $$\left. \theta_{\mathrm{GK}}(x, t; \tau_q, \kappa^2, Bi_0, Bi_L) \right|_{B=1} \equiv \theta_{\mathrm{Fourier}}(x, t; Bi_0, Bi_L).$$

---

## 3. Certified Numerical Findings & Robustness Metrics

The mathematical theorem is validated by extensive numerical simulations across three decades of Biot numbers ($Bi \in [0.001, 0.5]$):

- **Collinearity Correlation:** $\rho \equiv -1.0000000000$ across all $Bi$, with $|1+\rho| \le 2.22 \times 10^{-16}$ (machine epsilon limit).
- **Residual Norm:** $\|J_{\tau_q} + \alpha_0 J_{\kappa^2}\| / \|J_{\tau_q}\| \approx (5.37 - 8.11) \times 10^{-9}$ (finite-difference truncation limit).
- **Condition Number:** $\operatorname{cond}(F_{2\times 2}) \sim 10^{17}$ pinned horizontally at the floating-point singularity floor.
- **Asymmetric Cooling:** Tested asymmetric configurations $(Bi_0, Bi_L) \in \{(0.01, 0.10), (0.05, 0.20), (0.10, 0.50)\}$; analytical discrepancy is identically $0.00 \times 10^0$.
- **Full-Field Invariance:** Probing interior points $x \in \{0.25, 0.50, 0.75\}$ and front face $x = 0$ confirms field-level identity with zero residual error.

---

## 4. Singular Value Decomposition in 3-Parameter Inversion $(\tau_q, \kappa^2, Bi)$

When experimentalists attempt to simultaneously fit $(\tau_q, \kappa^2, Bi)$:
1. **Identifiable Subspace ($\sigma_1, \sigma_2$):**  
   $\sigma_1 \in [26.2, 31.8]$ represents the primary thermal diffusion mode.  
   $\sigma_2 \in [5.35, 13.57]$ corresponds directly to the convective cooling tail.  
   The condition ratio $\sigma_1 / \sigma_2 \in [2.34, 4.90]$ demonstrates that the Biot number $Bi$ is cleanly and accurately identifiable from transient data.
2. **Persistent Null Subspace ($\sigma_3$):**  
   $\sigma_3 \sim 10^{-8}$ corresponds strictly to the null vector $\bm{v}_{\mathrm{null}} = (1, \alpha_0, 0)^\top$ (direction cosine $1.000000$). Boundary cooling populates an entirely orthogonal dimension in parameter space and provides strictly zero projection onto the null vector.

---

## 5. Dual Validation Architecture

1. **Exact de Hoog Laplace Inversion:**  
   The exact analytical closed-form rear-face transfer function matches the time-domain PDE solver within $L_\infty \le 1.02 \times 10^{-5}$ across all Biot numbers.
2. **Classical Cowan (1963) Fourier Heat-Loss Limit:**  
   In the singular limit $\tau_q \to 0, \kappa^2 \to 0$, the PDE solver reproduces Cowan's transcendental eigenvalue Fourier series within $L_\infty \le 1.01 \times 10^{-5}$.
3. **Spatial Grid Refinement:**  
   Simulations across $N_x \in \{100, 200, 400, 800\}$ yield errors $e_{100} = 1.43 \times 10^{-4}$, $e_{200} = 3.40 \times 10^{-5}$, and $e_{400} = 6.80 \times 10^{-6}$, confirming asymptotic second-order spatial accuracy ($p = 2.07 \to 2.32$). The grid discretization error on $N_x = 400$ fully accounts for the minor remaining discrepancy observed against continuous Laplace inversion.

---

## 6. Physical Nuances and Experimental Implications

1. **Insufficiency of Standard Heat-Loss Corrections:**  
   Standard flash corrections (Cowan or Cape--Lehman methods) cannot resolve the non-Fourier parameter degeneracy for materials operating near Fourier resonance.
2. **Sample Thickness Tuning ($L$):**  
   For bulk materials with constant properties, $B \equiv \kappa^2 / (\alpha_0 \tau_q)$ is scale-invariant. However, reducing $L$ shortens the diffusion timescale $t_{\mathrm{diff}} = L^2 / \alpha_0$, amplifying sensitivity amplitudes off-resonance or activating size-dependent nonlocality $\kappa(L)$ in nanolayers.
3. **Multi-Thickness Joint Inversion:**  
   At exact resonance ($B \equiv 1$), all thicknesses collapse identically to their Fourier curves; however, away from resonance ($B \ne 1$), multi-thickness joint inversion provides powerful regularization against noise.
4. **Contrast with Bulk Constitutive Non-Linearity:**  
   Unlike surface cooling, high-fluence nonlinear conductivity ($\lambda(T) = \lambda_0(1 + \beta_T \theta)$) creates an internal spatial gradient $\alpha(x, t)$ that destroys the uniform resonance condition throughout the sample, regularizing the condition number from $10^{17}$ to $7.3 \times 10^3$.
