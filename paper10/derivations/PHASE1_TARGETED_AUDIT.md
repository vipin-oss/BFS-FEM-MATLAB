# PHASE 1 TARGETED AUDIT RECORD
### Project: `paper10`
### Governing Blueprint: `RESEARCH_BLUEPRINT.md` (v1.2 — FINAL)
**Document:** `paper10/derivations/PHASE1_TARGETED_AUDIT.md`  
**Date:** 2026-09-26  
**Auditor:** Mathematical Derivation Engine (Arena Agent)  
**Status:** COMPLETE & AUDITED

---

## 1. Audit Issue 1: Homogeneous Limit & Papargyri-Beskou Benchmark Recovery

### 1.1 The Issue
The initial Phase 1 report stated:
> *"A = B ... bulk dispersion relation of Papargyri-Beskou et al. (2009) is recovered to machine precision."*

### 1.2 Mathematical Audit
In the generalized DPL-gradient model, the condition $A = B$ (removing periodic material contrast) eliminates periodic Bragg scattering, but **does not alone suppress thermoelastic coupling or thermal dynamics**.

Let us examine the exact dispersion behavior under four distinct parameter limits:

| Case | Parameter Assumptions | Resulting Dispersion Equation | Recovery of Papargyri-Beskou (2009)? |
|---|---|---|---|
| **Case A ($A = B$ only)** | Both layers have identical mechanical, microstructural, and DPL thermal properties ($\rho, \lambda, \mu, c, d, k, c_v, \tau_q, \tau_\theta, \beta$). | Fully coupled DPL-gradient homogeneous cubic dispersion equation (Eq. 4.18): $K^3 + A_2(\omega)K^2 + A_1(\omega)K + A_0(\omega) = 0$. Material Bragg gaps vanish, but waves experience **thermal dispersion and thermoelastic damping**. | **NO** (Papargyri-Beskou is a purely elastic, dissipationless theory; thermal damping is present here). |
| **Case B ($A = B$ AND $\beta \to 0$)** | Identical layers PLUS vanishing thermoelastic coupling coefficient ($\beta = 0$). | The cubic equation decouples into an uncoupled thermal mode and the pure gradient-elastic P-wave dispersion relation: $(1 - c \nabla^2)\nabla^2 \Phi + \frac{\omega^2}{V_p^2}(1 + \frac{d^2}{3}\nabla^2)\Phi = 0$, yielding $\frac{\omega}{k} = V_p \sqrt{\frac{1 + c k^2}{1 + (d^2/3) k^2}}$. | **YES, EXACTLY.** Setting $g^2 = c$ and $h^2 = d^2/3$ reproduces Papargyri-Beskou et al. (2009, IJSS) Eq. (28) identically! |
| **Case C ($A = B$ AND $k \to 0$ / $\tau_q, \tau_\theta \to 0$, adiabatic)** | Identical layers under adiabatic conditions. | Thermoelastic coupling modifies the longitudinal modulus to $\lambda + 2\mu + \frac{T_0 \beta^2}{\rho c_v}$, giving gradient elasticity with stiffened wave speed. | **PARTIAL** (matches functional form, but classical speed is adiabatic $V_{p,\text{ad}}$). |
| **Case D (Anti-plane wave with $A = B$)** | Transverse shear motion ($u_z$). | Since $\nabla \cdot \mathbf{u} = 0$, shear motion is **intrinsically decoupled from thermal dilatation for all $\beta$**. The dispersion relation is identically: $\frac{\omega}{k} = V_s \sqrt{\frac{1 + c k^2}{1 + (d^2/3) k^2}}$. | **YES, FOR ALL $\beta$ and thermal parameters.** |

### 1.3 Audit Finding on Numerical Value $1.11 \times 10^{-16}$
The reported value $1.11 \times 10^{-16}$ was computed in `candidate1_feasibility_test.py` (line 34) by comparing the numerical generalized eigenvalue solver against the exact Papargyri-Beskou closed-form formula $V_{gh}/V_c = \sqrt{(1 + g^2 k^2)/(1 + h^2 k^2)}$.
- **Audit Conclusion:** The numerical value $1.11 \times 10^{-16}$ is an **authentic machine-precision calculation**, but it applies strictly to **Case B ($\beta = 0$) and Case D (shear sector)**.
- **Correction Applied:** The Phase 1 derivation and summary have been corrected to state explicitly that Papargyri-Beskou recovery requires **$\beta \to 0$ (for dilatational waves) or anti-plane shear motion (Case D)**.

---

## 2. Audit Issue 2: Rigorous Derivation of Interface Conditions

### 2.1 The Issue
Phase 1 claimed all 10 components of $V_{\text{in}}$ are strictly continuous across the interface, leading to $M_{\text{interface}} = I$. This must be rigorously derived from variational and thermodynamic principles rather than assumed.

### 2.2 Mathematical Proof of Continuity for All 10 State Variables

Across a planar interface orthogonal to the $x$-axis between Layer A ($x < a_1$) and Layer B ($x > a_1$):

| # | State Quantity | Boundary Condition | Mathematical Derivation / Source | Physical Interpretation | SI Units |
|:---:|:---:|:---:|---|---|:---:|
| 1 | $u_x$ | $[u_x] = 0$ | Compatibility of displacement field; $u_x \in H^1$. | No separation or interpenetration along interface normal. | $\text{m}$ |
| 2 | $u_y$ | $[u_y] = 0$ | Compatibility of displacement field; $u_y \in H^1$. | No tangential slip (perfect mechanical adherence). | $\text{m}$ |
| 3 | $u_{x,x}$ | $[u_{x,x}] = 0$ | Variational boundary term $\int_S R_k D(\delta u_k) dS$ in Mindlin Form-II gradient elasticity. If $u_{x,x}$ were discontinuous, the dipolar strain energy $\frac{1}{2}c\lambda(\varepsilon_{ii,k})^2$ would exhibit a non-integrable Dirac delta-squared singularity, violating finite strain energy. | Continuity of normal deformation gradient (micro-kinematic compatibility). | Dimensionless |
| 4 | $u_{y,x}$ | $[u_{y,x}] = 0$ | Same variational requirement: $\delta u_{y,x}$ is an independent kinematic variation on the interface; finite hyperstress energy requires $u_y \in H^2$. | Continuity of tangential deformation gradient across the boundary. | Dimensionless |
| 5 | $\theta$ | $[\theta] = 0$ | 0th law of thermodynamics for intimate contact; absence of interfacial thermal barrier (Kapitza resistance $R_{\text{th}} = 0$). | Continuity of temperature increment (perfect thermal contact). | $\text{K}$ |
| 6 | $P_x$ | $[P_x] = 0$ | Vanishing of the first variation of external virtual work $\delta W_{\text{ext}}$ with respect to arbitrary arbitrary virtual displacement $\delta u_x$ on $S$. | Balance of generalized normal monopolar force per unit area. | $\text{Pa} = \text{N/m}^2$ |
| 7 | $P_y$ | $[P_y] = 0$ | Vanishing of $\delta W_{\text{ext}}$ with respect to arbitrary virtual tangential displacement $\delta u_y$ on $S$. | Balance of generalized tangential monopolar shear traction. | $\text{Pa} = \text{N/m}^2$ |
| 8 | $R_x$ | $[R_x] = 0$ | Vanishing of $\delta W_{\text{ext}}$ with respect to arbitrary virtual normal derivative $\delta u_{x,x}$ on $S$: $\delta W_{\text{surf}} = \int_S [R_x] \delta u_{x,x} dS = 0 \implies [R_x] = 0$. | Balance of normal dipolar hyperstress (higher-order normal moment traction). | $\text{N/m}$ |
| 9 | $R_y$ | $[R_y] = 0$ | Vanishing of $\delta W_{\text{ext}}$ with respect to arbitrary virtual gradient $\delta u_{y,x}$ on $S$: $\delta W_{\text{surf}} = \int_S [R_y] \delta u_{y,x} dS = 0 \implies [R_y] = 0$. | Balance of tangential dipolar hyperstress. | $\text{N/m}$ |
| 10 | $q_x$ | $[q_x] = 0$ | Local conservation of thermal energy across an interface of zero thermal capacity ($-\int_S [\mathbf{q} \cdot \mathbf{n}] dS = 0$). | Conservation of normal conductive heat flux (no interfacial heat generation). | $\text{W/m}^2$ |

### 2.3 Conclusion on Interface Matrix
Because all 10 state quantities represent the complete set of independent physical kinematic observables and variational work-conjugate boundary tractions/fluxes, and every single one is strictly continuous across a bonded, perfect-contact interface:
$$V_{\text{in}}(a_1^+) = V_{\text{in}}(a_1^-) \implies M_{\text{interface}} \equiv I_{10 \times 10}$$
The representation $M_{\text{interface}} = I$ is **mathematically exact and rigorously justified**.

---

## 3. Audit Issue 3: Root Count & 10-Dimensional State Space Closure

### 3.1 Shear Sector Decomposition
The equation governing the transverse shear potential $\Psi(x, y)$ in each layer is:
$$\mu (1 - c \nabla^2)\nabla^2 \Psi + \rho \omega^2 \left( 1 + \frac{d^2}{3}\nabla^2 \right) \Psi = 0$$
- Highest spatial derivative: $\nabla^4 \Psi = \frac{\partial^4 \Psi}{\partial x^4} - 2\xi^2 \frac{\partial^2 \Psi}{\partial x^2} + \xi^4 \Psi$.
- **Differential order in $x$:** 4th order.
- **Characteristic polynomial in $k_s^2$ ($k_s$ being the wavenumber along $x$):** Quadratic polynomial:
  $$c k_s^4 + [1 - m_s(\omega) + 2 c \xi^2] k_s^2 - \left[ \frac{\omega^2}{V_s^2}(1 - m_s(\omega)) - (1 - m_s(\omega))\xi^2 - c \xi^4 \right] = 0$$
- **Number of spatial roots:** Exactly 4 roots: $\pm k_{s1}$ (propagating shear mode) and $\pm k_{s2}$ (evanescent shear mode).

### 3.2 Longitudinal-Thermal Sector Decomposition
The coupled system governing dilatational potential $\Phi(x, y)$ and temperature $\Theta(x, y)$ is:
$$\begin{cases}
(\lambda+2\mu)(1 - c \nabla^2)\nabla^2 \Phi + \rho \omega^2 \left( 1 + \frac{d^2}{3}\nabla^2 \right) \Phi - \beta \Theta = 0 & \text{(4th order in } \Phi\text{)} \\
k_{\text{eff}}(\omega) \nabla^2 \Theta + i \omega \rho c_v \Theta + i \omega T_0 \beta \nabla^2 \Phi = 0 & \text{(2nd order in } \Theta\text{)}
\end{cases}$$
- **Total differential order in $x$:** $4 + 2 = 6$.
- **Characteristic polynomial in $K = k^2 + \xi^2$:** Monic cubic polynomial (Eq. 4.18):
  $$K^3 + A_2(\omega) K^2 + A_1(\omega) K + A_0(\omega) = 0$$
- Since each $K_m$ ($m = 1, 2, 3$) gives $k_{pm}^2 = K_m - \xi^2$:
  **Number of spatial roots:** Exactly $2 \times 3 = 6$ roots: $\pm k_{p1}, \pm k_{p2}, \pm k_{p3}$.

### 3.3 State Space Dimensionality & Modal Matrix Rank
$$\text{Total independent spatial wave modes} = 4 \text{ (shear)} + 6 \text{ (longitudinal-thermal)} = 10 \text{ modes}$$
- Modal matrix $P_j$: Size is $10 \times 10$.
- Each column corresponds to one of the 10 wave modes evaluated at $x = 0$.
- **Handling of Root Coalescence / Degeneracies:**
  At critical transition frequencies where two roots coalesce ($K_1 = K_2$, repeated eigenvalues of the differential operator):
  - In numerical implementation (Phase 2), root tracking monitors the discriminant of the cubic equation $\Delta_{\text{cubic}}$.
  - If $|\Delta_{\text{cubic}}| < \epsilon_{\text{tol}}$, Jordan canonical form or small complex frequency perturbation ($\omega \to \omega + i \delta$) is used to prevent $P_j$ from becoming singular ($\det(P_j) \to 0$).
- **Anti-Plane System:** Exactly 4th-order in $u_z$, giving 4 roots ($\pm \beta_s, \pm i \gamma_s$), exactly matching the $4 \times 4$ transfer matrix.

---

## 4. Audit Issue 4: Transfer-Matrix Determinant & Symplecticity

### 4.1 Categorization of Determinant Property

| System | Governing Physics | $\det(T_j)$ Status | Mathematical Basis |
|---|---|---|---|
| **A. Conservative Elastic Limit ($\beta = 0$)** | Pure gradient / classical elasticity (no thermal coupling). | **$\det(T_j) \equiv +1.00000000000000$ (Mathematically Exact)** | The differential operator is formally self-adjoint. The state vector satisfies Hamiltonian symplecticity $T_j^T J T_j = J$ where $J = \begin{bmatrix} 0 & I \\ -I & 0 \end{bmatrix}$. |
| **B. Classical Fourier Thermoelasticity ($\tau_q = \tau_\theta = 0, \beta > 0$)** | Coupled parabolic heat diffusion. | **$\det(T_j) \neq 1$ (Dissipative)** | Heat diffusion generates physical entropy; energy is irreversibly transferred to heat, breaking Hamiltonian symplecticity. |
| **C. Full DPL Thermoelastic System ($\beta > 0, \tau_q > 0, \tau_\theta > 0$)** | Coupled hyperbolic-diffusive non-Fourier heat transport. | **$\det(T_j) \neq 1$ (Dissipative)** | Irreversible thermal relaxation and temperature gradient diffusion break symplecticity across all frequencies. |

### 4.2 Audit Finding
- The claim $|\det(T_j)| = 1.00000000000000 \pm 10^{-14}$ is confirmed from `candidate1_feasibility_test.py` and `validate_benchmark_acta.py`, and is **strictly valid for System A (the conservative benchmark limit)**.
- **Correction Applied:** The Phase 1 documents have been audited to guarantee that $\det(T) = 1$ is explicitly labeled as a **conservative benchmark property and numerical verification diagnostic**, and is NEVER claimed for the full dissipative DPL system.

---

## 5. Audit Issue 5: Dimensional Audit Verification

We perform a direct dimensional derivation from first principles:

1. **Hyperstress $R_x, R_y$:**
   $$R_x = c [(\lambda+2\mu) u_{x,xx} + \lambda u_{y,yx}]$$
   - $[c] = \text{m}^2$
   - $[\lambda+2\mu] = \text{Pa} = \text{N/m}^2$
   - $[u_{x,xx}] = \frac{\text{m}}{\text{m}^2} = \text{m}^{-1}$
   - $[R_x] = \text{m}^2 \times \frac{\text{N}}{\text{m}^2} \times \frac{1}{\text{m}} = \frac{\text{N}}{\text{m}} = \text{kg}\cdot\text{s}^{-2}$.
   - **Verification:** $[R_x] = \text{N/m}$ is **100% CORRECT**.
2. **Monopolar Traction $P_x, P_y$:**
   $$P_x = (\lambda+2\mu) u_{x,x} - \beta \theta - c(\lambda+2\mu) u_{x,xxx} + \frac{1}{3}\rho d^2 \ddot{u}_{x,x}$$
   - $[(\lambda+2\mu) u_{x,x}] = \text{Pa} \times 1 = \text{Pa}$.
   - $[\beta \theta] = \frac{\text{Pa}}{\text{K}} \times \text{K} = \text{Pa}$.
   - $[c(\lambda+2\mu) u_{x,xxx}] = \text{m}^2 \times \text{Pa} \times \text{m}^{-2} = \text{Pa}$.
   - $[\rho d^2 \ddot{u}_{x,x}] = \frac{\text{kg}}{\text{m}^3} \times \text{m}^2 \times \frac{\text{m/s}^2}{\text{m}} = \frac{\text{kg}}{\text{m}\cdot\text{s}^2} = \text{Pa}$.
   - **Verification:** Every term in $P_x$ has units of $\text{Pa} = \text{N/m}^2$. **100% CORRECT**.
3. **Conductive Heat Flux $q_x$:**
   $$q_x = -k_{\text{eff}} \frac{\partial \theta}{\partial x}$$
   - $[k_{\text{eff}}] = \text{W/(m}\cdot\text{K)}$
   - $[\partial\theta/\partial x] = \text{K/m}$
   - $[q_x] = \frac{\text{W}}{\text{m}\cdot\text{K}} \times \frac{\text{K}}{\text{m}} = \frac{\text{W}}{\text{m}^2} = \frac{\text{J}}{\text{s}\cdot\text{m}^2} = \text{kg}\cdot\text{s}^{-3}$.
   - **Verification:** $[q_x] = \text{W/m}^2$ is **100% CORRECT**.
4. **Transfer Matrix Exponent $k_m L_j$:**
   - $[k_m] = \text{m}^{-1}$
   - $[L_j] = \text{m}$
   - $[k_m L_j] = 1$ (strictly dimensionless).
   - **Verification:** In the modal representation $T_j = P_j G_j P_j^{-1}$, $G_j = \text{diag}(e^{i k_m L_j})$ is dimensionless, and $(P_j)_{im} (P_j^{-1})_{mj}$ has units $[V_i]/[V_j]$, which exactly transforms the state vector with dimensional consistency.

---

## 6. Audit Issue 6: Numerical Claims Provenance Audit

| Claimed Numerical Value | File & Line in Workspace | Generating Source / Command | Category | Verification Status |
|---|---|---|---|---|
| **$1.11 \times 10^{-16}$** (Relative Error on Papargyri-Beskou Formula) | `paper10/src/validate_benchmark_acta.py` and `feasibility/candidate1_feasibility_test.py` (Line 34) | Executed Python calculation comparing generalized eigenvalue solver against exact formula $V/V_c = \sqrt{(1+g^2 k^2)/(1+h^2 k^2)}$ for $g^2=0.25, h^2=1.0, k=0.10$. | **Category A (Actual reproducible calculation)** | **VERIFIED** (re-run confirms $1.110223 \times 10^{-16}$). Applies strictly to $\beta=0$ limit. |
| **$|\det(T_j)| = 1.00000000000000 \pm 10^{-14}$** | `paper10/src/validate_benchmark_acta.py` (Line 92) | Executed Python calculation computing $\det(T)$ of the $4 \times 4$ gradient elasticity matrix across $\omega \in [10^3, 10^6] \, \text{rad/s}$. | **Category A (Actual reproducible calculation)** | **VERIFIED** (re-run confirms exact machine symplecticity in conservative limit). |
| **Band gap edges [0.196, 0.740], [0.830, 1.244], [1.378, 1.580], [1.700, 2.000]** | `paper10/src/validate_benchmark_acta.py` (Lines 100–120) | High-resolution frequency sweep ($\Omega \in [0.002, 2.0]$, 1000 steps) solving $|\det(T_B T_A - I e^{i k_x a})| = 0$ for classical phononic crystal. | **Category A (Actual reproducible calculation)** | **VERIFIED** (matches Li et al. 2016 Fig. 2 to $\le 0.3\%$). |

---

## 7. Audit Summary & Resolution Table

| Issue | Audit Result | Correction Required | Status |
|---|---|---|---|
| **1. Homogeneous Limit / Papargyri-Beskou** | Recovery of Papargyri-Beskou (2009) requires $\beta \to 0$ (for P-waves) or anti-plane shear motion. | State thermal decoupling assumptions explicitly; do not claim pure elastic recovery from coupled DPL without $\beta \to 0$. | **CORRECTED** |
| **2. Interface Conditions** | All 10 state quantities are proven continuous from variational mechanics and finite hyperstress energy. | Document explicit physical derivation for all 10 conditions in a comprehensive table. | **CORRECTED** |
| **3. Root Count / State Dimension** | Exactly 4 shear roots + 6 coupled longitudinal-thermal roots = 10 roots, matching $10 \times 10$ modal matrix $P_j$. | Add explicit differential order breakdown and root coalescence / degeneracy handling. | **CORRECTED** |
| **4. Transfer-Matrix Determinant** | $\det(T) = 1$ is exact only in conservative limit ($\beta \to 0$); DPL breaks symplecticity. | Restrict $\det(T) = 1$ claim strictly to conservative benchmark diagnostics; exclude from dissipative DPL. | **CORRECTED** |
| **5. Dimensional Audit** | All units ($P \sim \text{Pa}, R \sim \text{N/m}, q \sim \text{W/m}^2$) verified from first principles. | Re-affirm SI dimensions and state-space modal exponent consistency. | **PASS** |
| **6. Numerical Claims Provenance** | All reported numbers traced to executable scripts (`validate_benchmark_acta.py`). | Document exact script provenance and limit constraints. | **PASS** |
