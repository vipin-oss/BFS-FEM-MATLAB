# Novelty Gap Statement: Paper 11

**Document ID:** AUDIT-PAPER11-GAP  
**Date:** September 2026  

---

### What is Known

1. In classical laser flash testing, convective and radiative surface cooling causes an exponential temperature decay (cooling tail), which can be quantitatively corrected to retrieve accurate thermal diffusivity values using the classical Cowan (1963) or Cape & Lehman (1963) transcendental eigenvalue solutions.
2. The Guyer–Krumhansl (GK) equation accounts for non-local and memory effects in phonon-hydrodynamic and heterogeneous thermal transport through flux relaxation time $\tau_q$ and mean-free-path square parameter $\kappa^2$.
3. When the dimensionless resonance ratio satisfies $B \equiv \frac{\kappa^2}{\alpha_0 \tau_q} = 1$, the bulk Guyer–Krumhansl partial differential equation algebraically reduces to the classical Fourier diffusion equation (Both et al. 2016, Kovács 2018). Under idealized adiabatic boundary conditions ($Bi = 0$), this algebraic cancellation produces an exact sensitivity collinearity $\partial T / \partial \tau_q = -\alpha_0 \partial T / \partial \kappa^2$, which causes the Fisher Information Matrix to degenerate to rank 1.

---

### What Has Not Been Established

1. Whether boundary convective and radiative heat losses ($Bi_0, Bi_L > 0$) break or preserve this sensitivity collinearity.
2. How the Guyer–Krumhansl heat flux boundary operator behaves under Robin convective cooling in the Laplace domain. Specifically, whether the dynamic surface impedance $\lambda_{\mathrm{eff}}(s) = \lambda_0 \left[\frac{1 + (\kappa^2/\alpha_0)s}{1 + \tau_q s}\right]$ retains any relaxation-time dependence at resonance.
3. Whether the cooling tail observed in actual flash experiments provides independent statistical information capable of regularizing the local $(\tau_q, \kappa^2)$ sensitivity singularity.
4. The algebraic rank, singular value spectrum, and conditioning of the simultaneous 3-parameter estimation problem $(\tau_q, \kappa^2, Bi)$ in non-Fourier thermal metrology.

---

### What Paper 11 Establishes

1. **Analytical Invariance Theorem:** At $B = 1$, the Guyer–Krumhansl temperature field with arbitrary front and rear Robin boundary heat losses ($Bi_0, Bi_L \ge 0$) is mathematically identical to the classical Fourier heat conduction solution with the corresponding heat losses for all time $t \ge 0$, all spatial positions $x \in [0, 1]$, and arbitrary thermal excitations.
2. **Dynamic Surface Impedance Collapse:** At $B = 1$, the dynamic thermal conductivity operator collapses identically to the baseline Fourier conductivity ($\lambda_{\mathrm{eff}}(s) \equiv \lambda_0$). Hence, no non-Fourier parameter survives in either the bulk Helmholtz ODE or the Robin boundary conditions.
3. **Robustness of Sensitivity Collinearity:** The exact collinearity $\bm{J}_{\tau_q}(t) = -\alpha_0 \bm{J}_{\kappa^2}(t)$ is an intrinsic bulk property that remains strictly invariant across all Biot numbers ($Bi \in [0.001, 0.5]$), with correlation coefficient $\rho \equiv -1.0000000000$ and condition number $\operatorname{cond}(F_{2\times 2}) \sim 10^{17}$.
4. **Three-Parameter Subspace Decomposition:** In the simultaneous estimation of $(\tau_q, \kappa^2, Bi)$, the Fisher Information Matrix decomposes into an identifiable 2D subspace ($\sigma_1 / \sigma_2 \in [2.34, 4.90]$) corresponding to diffusion and cooling, alongside an isolated null vector $(1, \alpha_0, 0)^\top$ with singular value $\sigma_3 \sim 10^{-8}$. Boundary cooling allows accurate estimation of $Bi$, but provides zero regularization for the $(\tau_q, \kappa^2)$ pair.

---

### Why That Difference Matters

In experimental laser flash characterization, experimentalists routinely assume that fitting cooling tails or incorporating boundary heat-loss corrections provides additional observational degrees of freedom that can help disambiguate complex constitutive models. 

Paper 11 disproves this assumption for Guyer–Krumhansl transport near Fourier resonance. It establishes a rigorous **no-go result**: boundary heat-loss corrections cannot resolve the structural indeterminacy between thermal relaxation and nonlocality. Consequently, experimentalists seeking to characterize non-Fourier parameters cannot rely on boundary cooling corrections, and must instead pursue strategies that perturb the bulk transport condition away from $B = 1$—such as tuning specimen thickness, performing joint multi-thickness inversions, or operating in high-fluence nonlinear thermal regimes.
