# Paper 11 Blueprint: Invariance of the Guyer–Krumhansl Fourier-Resonance Sensitivity Singularity to Boundary Heat Loss

**Status:** Phase 0 (Planning & Mathematical Specification)  
**Target Journal:** *International Journal of Heat and Mass Transfer* (or *Applied Thermal Engineering*)  
**Authors:** V. Gupta  
**Affiliation:** Department of Mathematics, Gurugram University, Gurugram, Haryana 122018, India  

---

## 1. Problem Statement & Motivation

In non-Fourier thermal characterization via laser flash analysis (ASTM E1461), the Guyer–Krumhansl (GK) equation incorporates heat flux relaxation $\tau_q$ and spatial nonlocality $\kappa^2$:
$$\rho c \, \frac{\partial T}{\partial t} + \frac{\partial q}{\partial x} = 0$$
$$\tau_q \, \frac{\partial q}{\partial t} + q + \lambda_0 \, \frac{\partial T}{\partial x} - \kappa^2 \, \frac{\partial^2 q}{\partial x^2} = 0$$

When the non-dimensional resonance ratio satisfies:
$$B = \frac{\kappa^2}{\alpha \tau_q} = 1 \qquad (\alpha = \lambda_0 / \rho c)$$
idealized adiabatic flash analyses demonstrate an exact algebraic cancellation in the Laplace-domain propagation factor ($m^2(s) = s/\alpha$). This causes an exact sensitivity colinearity:
$$\frac{\partial T}{\partial \tau_q} = -\alpha \, \frac{\partial T}{\partial \kappa^2}$$
rendering $\tau_q$ and $\kappa^2$ structurally non-identifiable.

However, all real laser flash experiments suffer from convective and radiative cooling at the irradiated and rear faces, characterized by the Biot numbers $Bi_0$ and $Bi_L$ (Cowan 1963, Cape & Lehman 1963). Experimentalists routinely apply heat-loss corrections to extract thermal parameters from the resulting cooling tails.

**Primary Research Question of Paper 11:**
> *Does boundary convective and radiative heat loss ($Bi > 0$) break the exact Fourier-resonance sensitivity colinearity and regularize the parameter singularity between relaxation time $\tau_q$ and nonlocality $\kappa^2$? Or is the Fourier-resonance degeneracy an intrinsic bulk invariant that persists identically despite boundary cooling?*

---

## 2. Governing Equations and Dimensionless Scaling

### Dimensional Coupled System
For a slab $x \in [0, L]$ with ambient temperature $T_0$:
1. Energy balance:
   $$\rho c \, \frac{\partial T}{\partial t} + \frac{\partial q}{\partial x} = 0$$
2. GK constitutive equation:
   $$\tau_q \, \frac{\partial q}{\partial t} + q + \lambda_0 \, \frac{\partial T}{\partial x} - \kappa^2 \, \frac{\partial^2 q}{\partial x^2} = 0$$
3. Robin boundary conditions with convective/radiative heat loss:
   * Front face ($x = 0$):
     $$q(0, t) = q_{\mathrm{pulse}}(t) - h_0 (T(0, t) - T_0)$$
   * Rear face ($x = L$):
     $$q(L, t) = h_L (T(L, t) - T_0)$$
4. Initial conditions:
   $$T(x, 0) = T_0, \qquad q(x, 0) = 0$$

### Dimensionless Normalization
Using scales:
$$x = L \hat{x}, \quad t = \frac{L^2}{\alpha_0} \hat{t}, \quad \Delta T_{\mathrm{ref}} = \frac{q_{\max} t_p}{\rho c L}, \quad \hat{T} = \frac{T - T_0}{\Delta T_{\mathrm{ref}}}, \quad \hat{q} = \frac{q}{q_{\max}}$$
$$\tau_\Delta = \frac{\alpha_0 t_p}{L^2}, \quad \hat{\tau}_q = \frac{\alpha_0 \tau_q}{L^2}, \quad \hat{\kappa}^2 = \frac{\kappa^2}{L^2}, \quad Bi_0 = \frac{h_0 L}{\lambda_0}, \quad Bi_L = \frac{h_L L}{\lambda_0}$$

The dimensionless system is (dropping hats):
$$\tau_\Delta \, \frac{\partial T}{\partial t} + \frac{\partial q}{\partial x} = 0$$
$$\tau_q \, \frac{\partial q}{\partial t} + q + \tau_\Delta \, \frac{\partial T}{\partial x} - \kappa^2 \, \frac{\partial^2 q}{\partial x^2} = 0$$
subject to:
$$q(0, t) = q_{\mathrm{pulse}}(t) - \tau_\Delta Bi_0 T(0, t)$$
$$q(1, t) = \tau_\Delta Bi_L T(1, t)$$

---

## 3. Mathematical Theorem & Analytical Benchmark

**Theorem 1 (Heat-Loss Invariance of Fourier Resonance):**  
*At the Fourier-resonance condition $B = \frac{\kappa^2}{\alpha \tau_q} = 1$, the Guyer–Krumhansl temperature field with arbitrary linear Robin boundary heat losses ($Bi_0, Bi_L \ge 0$) reduces identically to the classical Fourier heat conduction solution with the same boundary heat losses:*
$$\left. T_{\mathrm{GK}}(x, t; \tau_q, \kappa^2, Bi_0, Bi_L) \right|_{B=1} \equiv T_{\mathrm{Fourier}}(x, t; Bi_0, Bi_L)$$
*Consequently, the exact sensitivity colinearity:*
$$\frac{\partial T}{\partial \tau_q} = -\alpha \, \frac{\partial T}{\partial \kappa^2}$$
*holds identically for all Biot numbers $Bi_0, Bi_L$, for all times $t > 0$, and at all spatial locations $x \in [0, 1]$.*

**Corollary 1 (3-Parameter Fisher Information Rank):**  
*The 3-parameter sensitivity Jacobian $J = [J_{\tau_q} \;\; J_{\kappa^2} \;\; J_{Bi}]$ has rank exactly 2 at $B=1$. The parameter $Bi$ is fully identifiable from the cooling tail, but $(\tau_q, \kappa^2)$ remains strictly non-identifiable.*

---

## 4. Multi-Level Validation Strategy (Reviewer-Proof)

1. **Level 1 (Analytical Laplace Domain Transfer Function):**
   Exact closed-form Laplace transform solution inverted via high-precision Talbot contour integration, verified against the time-domain PDE solver to $< 10^{-6}$.
2. **Level 2 (Classical Cowan 1963 Fourier Benchmark):**
   In the singular limit $\tau_q, \kappa^2 \to 0$, the numerical GK solver matches the classical Cowan analytical series solution with convective heat loss.
3. **Level 3 (Adiabatic Baseline Recovery, $Bi \to 0$):**
   Matches the precursor baseline linear GK solver and reproduces the exact machine-precision colinearity ($R_J < 10^{-8}$).
4. **Level 4 (Spatial Mesh Convergence):**
   Grid refinement across $N_x \in \{100, 200, 400, 800\}$ confirming asymptotic second-order spatial convergence ($p \approx 2.0$).

---

## 5. Planned Artifact Deliverables

- `paper11/blueprint/BLUEPRINT.md` (this file)
- `paper11/derivations/derivations.md` (complete analytical theorem proof)
- `paper11/src/solver_gk_heatloss.py` (staggered-grid BDF solver)
- `paper11/src/analytic_laplace.py` (Laplace-domain Talbot solver)
- `paper11/src/run_heatloss_study.py` (systematic $Bi$ sweep driver)
- `paper11/src/run_validation.py` (Cowan Fourier and adiabatic benchmark driver)
- `paper11/src/plot_figures.py` (publication figures generator)
- `paper11/src/reproduce_all.py` (single-command master reproducibility runner)
- `paper11/runs/calculations/*.csv` (certified calculation tables)
- `paper11/figures/*.pdf` and `*.png` (standalone figures)
- `paper11/audit/*.md` (signed phase audit logs)
- `paper11/manuscript/` and `paper11/overleaf/` (submission manuscript with pre-compiled PDF)
