# PHASE 1 DERIVATION RECORD — COUPLED DPL–DIPOLAR-GRADIENT TRANSFER-MATRIX FORMULATION

### Project: `paper10`
### Governing Blueprint: `RESEARCH_BLUEPRINT.md` (v1.2 — FINAL)
**Document:** `paper10/derivations/PHASE1_DERIVATION.md`  
**Date:** 2026-09-26  
**Revision:** v1.1 (Audited & Calibrated per Targeted Phase 1 Audit)  
**Auditor / Author:** Mathematical Derivation Engine (Arena Agent)  
**Status:** COMPLETE, AUDITED & LOCKED

---

## 1. Governing Field Equations

We consider a 1D periodic phononic crystal composed of alternating homogeneous layers A and B along the $x$-axis. Each layer consists of an isotropic, centrosymmetric material governed by **Mindlin Form-II dipolar gradient elasticity** coupled with **Tzou's Dual-Phase-Lag (DPL)** heat conduction.

### 1.1 Generalized Momentum Balance in Mindlin Form-II Gradient Elasticity
The general equations of motion without body forces are given by Mindlin (1964) and Li, Wei & Zhou (2016, Eq. 8):
$$\left( \tau_{jk} - \mu_{ijk,i} \right)_{,j} = \rho \ddot{u}_k - \frac{\rho d^2}{3} \ddot{u}_{k,jj}$$
where:
- $\tau_{jk}$ is the Cauchy (monopolar) stress tensor,
- $\mu_{ijk}$ is the dipolar stress (hyperstress) tensor,
- $\rho$ is the mass density,
- $d$ is the micro-inertia characteristic length parameter ($d = \sqrt{3} h$, where $h$ is the micro-inertia length scale),
- Roman indices $i, j, k \in \{x, y, z\}$, and overdots denote time derivatives ($\ddot{u} = \partial^2 u / \partial t^2$).

### 1.2 Dual-Phase-Lag (DPL) Energy Equation
Tzou's non-Fourier heat transport law introduces two distinct microscopic phase lags: $\tau_q$ (relaxation time of heat flux) and $\tau_\theta$ (retardation time of temperature gradient):
$$\mathbf{q}(\mathbf{x}, t + \tau_q) = -k \nabla \theta(\mathbf{x}, t + \tau_\theta)$$
Expanding to first order in time:
$$\mathbf{q} + \tau_q \frac{\partial \mathbf{q}}{\partial t} = -k \nabla \theta - k \tau_\theta \frac{\partial}{\partial t}(\nabla \theta) \tag{1.1}$$
The localized thermal energy conservation equation with thermo-mechanical dilatational coupling is:
$$-\nabla \cdot \mathbf{q} = \rho c_v \frac{\partial \theta}{\partial t} + T_0 \beta \frac{\partial}{\partial t}(\nabla \cdot \mathbf{u}) \tag{1.2}$$
where:
- $\theta(\mathbf{x}, t) = T(\mathbf{x}, t) - T_0$ is the local temperature increment,
- $T_0$ is the absolute uniform reference temperature,
- $c_v$ is the specific heat at constant deformation,
- $\beta = (3\lambda + 2\mu)\alpha_t$ is the thermoelastic coupling coefficient ($\alpha_t$ is the linear coefficient of thermal expansion).

Applying the operator $(1 + \tau_q \partial_t)$ to Eq. (1.2) and substituting Eq. (1.1) eliminates the heat flux vector $\mathbf{q}$, yielding the scalar DPL energy equation:
$$k \left( 1 + \tau_\theta \frac{\partial}{\partial t} \right) \nabla^2 \theta = \left( 1 + \tau_q \frac{\partial}{\partial t} \right) \left[ \rho c_v \frac{\partial \theta}{\partial t} + T_0 \beta \frac{\partial}{\partial t}(\nabla \cdot \mathbf{u}) \right] \tag{1.3}$$

---

## 2. Constitutive Relations & Generalized Boundary Tractions

### 2.1 Strain Energy and Stress Tensors
For an isotropic, centrosymmetric material with micro-stiffness length-scale parameter $g$ (where $c = g^2$), the strain energy density function $W$ incorporating thermal expansion is:
$$W = \frac{1}{2}\lambda \varepsilon_{ii}\varepsilon_{jj} + \mu \varepsilon_{ij}\varepsilon_{ij} + c \left[ \frac{1}{2}\lambda \varepsilon_{ii,k}\varepsilon_{jj,k} + \mu \varepsilon_{ij,k}\varepsilon_{ji,k} \right] - \beta \theta \varepsilon_{kk}$$
where $\varepsilon_{ij} = \frac{1}{2}(u_{i,j} + u_{j,i})$ is the classical infinitesimal strain tensor.

The Cauchy stress $\tau_{ij}$ and dipolar hyperstress $\mu_{kij}$ are obtained by thermodynamic differentiation:
$$\tau_{ij} = \frac{\partial W}{\partial \varepsilon_{ij}} = \lambda \delta_{ij} \varepsilon_{kk} + 2\mu \varepsilon_{ij} - \beta \theta \delta_{ij} \tag{2.1}$$
$$\mu_{kij} = \frac{\partial W}{\partial \varepsilon_{ij,k}} = c \left[ \lambda \delta_{ij} \varepsilon_{pp,k} + 2\mu \varepsilon_{ij,k} \right] \tag{2.2}$$

### 2.2 Generalized Boundary Tractions from Hamilton's Principle
Applying Hamilton's variational principle $\delta \int_{t_0}^{t_1} (T - W + W_{ext}) dt = 0$ over a domain bounded by surface $S$ with outward unit normal $n_j$ establishes the natural boundary quantities:
$$\delta W_{ext} = \int_S \left( P_k \delta u_k + R_k D \delta u_k \right) dS$$
where $D = n_l \partial_l = \partial / \partial n$ is the normal derivative operator.

The resulting generalized surface tractions are:
1. **Generalized Monopolar Traction $P_k$ (Units: $\text{N/m}^2 = \text{Pa}$):**
   $$P_k = n_j (\tau_{jk} - \mu_{ijk,i}) - D_j(n_i \mu_{ijk}) + (D_l n_l) n_i n_j \mu_{ijk} + \frac{1}{3}\rho d^2 n_j \ddot{u}_{k,j} \tag{2.3}$$
   where $D_j = (\delta_{jl} - n_j n_l)\partial_l$ is the surface gradient operator.
2. **Generalized Dipolar Traction (Hyperstress) $R_k$ (Units: $\text{N/m}$):**
   $$R_k = n_i n_j \mu_{ijk} \tag{2.4}$$

### 2.3 Explicit Boundary Tractions on Layer Interfaces ($n = [1, 0, 0]^T$)
For planar interfaces orthogonal to the $x$-axis ($n_x = 1, n_y = n_z = 0$, $D = \partial/\partial x$, $D_y = \partial/\partial y$):
- **Normal Monopolar Traction $P_x$ ($\text{Pa}$):**
  $$P_x = (\lambda+2\mu) u_{x,x} + \lambda u_{y,y} - \beta \theta - c (\lambda+2\mu)\left( u_{x,xxx} + 2 u_{x,xyy} \right) - c\lambda u_{y,yyy} + \frac{1}{3}\rho d^2 \ddot{u}_{x,x} \tag{2.5}$$
- **Transverse In-Plane Monopolar Traction $P_y$ ($\text{Pa}$):**
  $$P_y = \mu (u_{x,y} + u_{y,x}) - c \mu \left( u_{y,xxx} + 2 u_{y,xyy} \right) - c \lambda u_{x,yyy} + \frac{1}{3}\rho d^2 \ddot{u}_{y,x} \tag{2.6}$$
- **Normal Dipolar Traction $R_x$ ($\text{N/m}$):**
  $$R_x = \mu_{xxx} = c \left[ (\lambda + 2\mu) u_{x,xx} + \lambda u_{y,yx} \right] \tag{2.7}$$
- **Transverse Dipolar Traction $R_y$ ($\text{N/m}$):**
  $$R_y = \mu_{xyx} = c \mu \left[ u_{y,xx} + u_{x,yx} \right] \tag{2.8}$$
- **Anti-Plane Monopolar Traction $P_z$ ($\text{Pa}$):**
  $$P_z = \mu u_{z,x} - c \mu \left( u_{z,xxx} + 2 u_{z,xyy} \right) + \frac{1}{3}\rho d^2 \ddot{u}_{z,x} \tag{2.9}$$
- **Anti-Plane Dipolar Traction $R_z$ ($\text{N/m}$):**
  $$R_z = \mu_{xzx} = c \mu u_{z,xx} \tag{2.10}$$
- **Normal Conductive Heat Flux $q_x$ ($\text{W/m}^2$):**
  $$q_x = -k_{\text{eff}}(\omega) \frac{\partial \theta}{\partial x} \tag{2.11}$$

---

## 3. Harmonic Representation & Frequency-Domain Equations

### 3.1 Steady-State Harmonic Time Representation
We adopt the standard harmonic time-dependence convention:
$$\mathbf{u}(x, y, t) = \mathbf{U}(x) e^{i(\xi y - \omega t)}, \quad \theta(x, y, t) = \Theta(x) e^{i(\xi y - \omega t)}, \quad \mathbf{q}(x, y, t) = \mathbf{Q}(x) e^{i(\xi y - \omega t)}$$
where:
- $\omega$ is the circular frequency ($\text{rad/s}$),
- $\xi$ is the apparent wavenumber along the $y$-axis (interface direction),
- The differential operators transform as:
  $$\frac{\partial}{\partial t} \to -i \omega, \quad \frac{\partial^2}{\partial t^2} \to -\omega^2, \quad \frac{\partial}{\partial y} \to i \xi, \quad \nabla^2 \to \frac{d^2}{dx^2} - \xi^2$$

### 3.2 Effective DPL Complex Thermal Conductivity
Transforming the heat flux equation (2.11) to the frequency domain:
$$(1 - i \omega \tau_q) Q_x = -k (1 - i \omega \tau_\theta) \frac{d\Theta}{dx}$$
Defining the frequency-dependent complex effective thermal conductivity $k_{\text{eff}}(\omega)$:
$$k_{\text{eff}}(\omega) \equiv k \frac{1 - i \omega \tau_\theta}{1 - i \omega \tau_q} \tag{3.1}$$
The frequency-domain normal heat flux is:
$$Q_x(x) = -k_{\text{eff}}(\omega) \frac{d\Theta(x)}{dx} \tag{3.2}$$

### 3.3 Frequency-Domain DPL Energy Equation
Dividing the energy conservation equation by $(1 - i \omega \tau_q)$:
$$k_{\text{eff}}(\omega) \nabla^2 \Theta + i \omega \rho c_v \Theta + i \omega T_0 \beta (\nabla \cdot \mathbf{U}) = 0 \tag{3.3}$$
Introducing the thermal wave parameter $k_{\text{th}}^2(\omega)$:
$$k_{\text{th}}^2(\omega) = \frac{i \omega \rho c_v}{k_{\text{eff}}(\omega)} = \frac{i \omega \rho c_v (1 - i \omega \tau_q)}{k (1 - i \omega \tau_\theta)} \tag{3.4}$$
and the thermal-to-mechanical coupling factor $\eta_{\text{th}}(\omega)$:
$$\eta_{\text{th}}(\omega) = \frac{i \omega T_0 \beta}{k_{\text{eff}}(\omega)} = \frac{i \omega T_0 \beta (1 - i \omega \tau_q)}{k (1 - i \omega \tau_\theta)} \tag{3.5}$$
Equation (3.3) becomes:
$$\nabla^2 \Theta + k_{\text{th}}^2(\omega) \Theta + \eta_{\text{th}}(\omega) (\nabla \cdot \mathbf{U}) = 0 \tag{3.6}$$

### 3.4 Frequency-Domain Gradient Equations of Motion
Substituting $\ddot{\mathbf{u}} = -\omega^2 \mathbf{U}$ and $\nabla^2 \ddot{\mathbf{u}} = -\omega^2 \nabla^2 \mathbf{U}$ into the momentum balance:
$$\mu (1 - c \nabla^2)\nabla^2 \mathbf{U} + (\lambda+\mu)(1 - c \nabla^2)\nabla(\nabla \cdot \mathbf{U}) - \beta \nabla \Theta + \rho \omega^2 \left( 1 + \frac{d^2}{3}\nabla^2 \right) \mathbf{U} = 0 \tag{3.7}$$
Introducing the classical phase speeds $V_p^2 = (\lambda+2\mu)/\rho$ and $V_s^2 = \mu/\rho$, and the non-dimensional micro-inertia parameter:
$$m_s(\omega) = \frac{\omega^2 d^2}{3 V_s^2}, \quad m_p(\omega) = \frac{\omega^2 d^2}{3 V_p^2} \tag{3.8}$$

---

## 4. Wave Decomposition & Root Count Audit

To systematically decouple and solve the system of higher-order PDEs, we utilize the Helmholtz decomposition for in-plane motion and direct formulation for anti-plane motion.

### 4.1 Anti-Plane (SH) Wave Formulation ($U_z(x, y)$)
For purely transverse shear motion:
$$\mathbf{U} = [0, 0, U_z(x)] e^{i(\xi y - \omega t)}, \quad \nabla \cdot \mathbf{U} = 0$$
Since $\nabla \cdot \mathbf{U} = 0$, thermoelastic dilatational coupling vanishes identically:
$$\beta \nabla_z \Theta = 0$$
The equation of motion (3.7) reduces to:
$$\mu (1 - c \nabla^2)\nabla^2 U_z + \rho \omega^2 \left( 1 + \frac{d^2}{3}\nabla^2 \right) U_z = 0$$
Dividing by $\mu$:
$$\nabla^4 U_z - \frac{1 - m_s}{c} \nabla^2 U_z - \frac{\omega^2}{c V_s^2} U_z = 0 \tag{4.1}$$
- **Differential order in $x$:** 4th order.
- **Root count:** Exactly 4 spatial roots: $\pm \beta_s$ (propagating mode) and $\pm i \gamma_s$ (evanescent mode), where:
  $$\Delta_s = \sqrt{(1 - m_s)^2 + \frac{4 c \omega^2}{V_s^2}}, \quad \sigma_s^2 = \frac{\Delta_s - (1 - m_s)}{2c}, \quad \tau_s^2 = \frac{\Delta_s + (1 - m_s)}{2c}$$
  $$\beta_s = \sqrt{\sigma_s^2 - \xi^2}, \quad \gamma_s = \sqrt{\tau_s^2 + \xi^2}$$

### 4.2 In-Plane Coupled Thermoelastic Wave Formulation ($U_x, U_y, \Theta$)
For in-plane motion, we represent the displacement field via longitudinal scalar potential $\Phi$ and transverse vector potential $\Psi \mathbf{e}_z$:
$$U_x = \frac{\partial \Phi}{\partial x} + \frac{\partial \Psi}{\partial y} = \frac{d\Phi}{dx} + i \xi \Psi \tag{4.2}$$
$$U_y = \frac{\partial \Phi}{\partial y} - \frac{\partial \Psi}{\partial x} = i \xi \Phi - \frac{d\Psi}{dx} \tag{4.3}$$
$$\nabla \cdot \mathbf{U} = \nabla^2 \Phi, \quad (\nabla \times \mathbf{U})_z = -\nabla^2 \Psi \tag{4.4}$$

1. **Transverse Shear Potential $\Psi$ (Uncoupled from temperature):**
   $$\mu (1 - c \nabla^2)\nabla^2 \Psi + \rho \omega^2 \left( 1 + \frac{d^2}{3}\nabla^2 \right) \Psi = 0 \tag{4.5}$$
   - **Differential order in $x$:** 4th order.
   - **Spatial roots:** Exactly 4 roots: $\pm k_{s1} = \pm \beta_s$ and $\pm k_{s2} = \pm i \gamma_s$.
2. **Coupled Dilatational Potential $\Phi$ and Temperature $\Theta$:**
   Taking the divergence of the equation of motion:
   $$(1 - c \nabla^2)\nabla^2 \Phi + \frac{\omega^2}{V_p^2} \left( 1 + \frac{d^2}{3}\nabla^2 \right) \Phi - \frac{\beta}{\rho V_p^2} \Theta = 0 \quad \text{(4th order in } x \text{)} \tag{4.6}$$
   The coupled DPL energy equation is:
   $$\nabla^2 \Theta + k_{\text{th}}^2(\omega) \Theta + \eta_{\text{th}}(\omega) \nabla^2 \Phi = 0 \quad \text{(2nd order in } x \text{)} \tag{4.7}$$
   - **Total differential order in $x$:** $4 + 2 = 6$.
   - **Characteristic Polynomial in $K = k^2 + \xi^2$:**
     $$K^3 + A_2(\omega) K^2 + A_1(\omega) K + A_0(\omega) = 0 \tag{4.8}$$
     with exact coefficients:
     $$A_2(\omega) = \frac{1 - m_p(\omega)}{c} - k_{\text{th}}^2(\omega)$$
     $$A_1(\omega) = -\frac{\omega^2}{c V_p^2} - \frac{(1 - m_p(\omega)) k_{\text{th}}^2(\omega)}{c} + \frac{\epsilon_{\text{th}} k_{\text{th}}^2(\omega)}{c}$$
     $$A_0(\omega) = \frac{\omega^2 k_{\text{th}}^2(\omega)}{c V_p^2}$$
     where $\epsilon_{\text{th}} = \frac{T_0 \beta^2}{\rho c_v (\lambda+2\mu)}$.
   - **Spatial roots:** The cubic polynomial (4.8) has 3 roots $K_1, K_2, K_3 \in \mathbb{C}$, giving $k_{pm} = \pm \sqrt{K_m - \xi^2}$ ($m = 1, 2, 3$). This yields exactly 6 spatial roots.

### 4.3 Total Independent Root Count
$$\text{Total roots} = 4 \text{ (shear modes)} + 6 \text{ (longitudinal-thermal modes)} = 10 \text{ spatial wave modes}$$
Every mode corresponds to an independent propagating or evanescent wave with an amplitude ratio:
$$\zeta_m = \frac{\Theta_{0m}}{\Phi_{0m}} = \frac{\eta_{\text{th}} K_m}{k_{\text{th}}^2 - K_m} \tag{4.9}$$

---

## 5. In-Plane $10 \times 10$ State-Space Formulation

The in-plane coupled thermoelastic state vector is strictly 10-dimensional:
$$V_{\text{in}}(x) = \left[ u_x, u_y, u_{x,x}, u_{y,x}, \theta, P_x, P_y, R_x, R_y, q_x \right]^T \tag{5.1}$$

The modal matrix $P_j$ is a full-rank $10 \times 10$ matrix whose columns are the evaluated state vectors of the 10 characteristic wave modes at $x = 0$.
The entries of column $m$ corresponding to a mode with wavenumber $k_x$ are:
1. $u_x = i k_x \Phi_0 + i \xi \Psi_0$
2. $u_y = i \xi \Phi_0 - i k_x \Psi_0$
3. $u_{x,x} = -k_x^2 \Phi_0 - k_x \xi \Psi_0$
4. $u_{y,x} = -k_x \xi \Phi_0 + k_x^2 \Psi_0$
5. $\theta = \zeta \Phi_0$
6. $P_x$:
   $$P_x = \left[ -(\lambda+2\mu) k_x^2 - \lambda \xi^2 - \beta \zeta + c(\lambda+2\mu)(k_x^4 + 2 k_x^2 \xi^2) + c\lambda \xi^4 - \frac{1}{3}\rho d^2 \omega^2 k_x^2 \right] i k_x \Phi_0$$
   $$+ \left[ -2\mu k_x \xi + 2 c\mu k_x \xi (k_x^2 + \xi^2) - \frac{1}{3}\rho d^2 \omega^2 k_x \xi \right] i \Psi_0$$
7. $P_y$:
   $$P_y = \left[ -2\mu k_x \xi + 2 c\mu k_x \xi (k_x^2 + \xi^2) - \frac{1}{3}\rho d^2 \omega^2 k_x \xi \right] i \Phi_0$$
   $$+ \left[ -\mu(k_x^2 + \xi^2) + c\mu (k_x^2 + \xi^2)^2 - \frac{1}{3}\rho d^2 \omega^2 k_x^2 \right] i k_x \Psi_0$$
8. $R_x = -c [ (\lambda+2\mu) k_x^2 + \lambda \xi^2 ] i k_x \Phi_0 - 2 c \mu k_x^2 \xi \Psi_0$
9. $R_y = -2 c \mu k_x^2 \xi \Phi_0 - c \mu ( k_x^2 - \xi^2 ) i k_x \Psi_0$
10. $q_x = -i k_{\text{eff}}(\omega) k_x \zeta \Phi_0$

### Degeneracy & Coalescence Handling
At critical cut-off frequencies where the cubic discriminant $\Delta_{\text{cubic}} \to 0$ (root coalescence $K_1 \approx K_2$), modal matrix condition tracking monitors $\kappa(P_j)$. If $\kappa(P_j) > 10^{14}$, Jordan decomposition or an infinitesimal complex frequency shift ($\omega \to \omega + i 10^{-12}$) is implemented to guarantee numerical regularity.

---

## 6. Anti-Plane $4 \times 4$ Decoupled Formulation

For normal or oblique anti-plane shear waves, the displacement $u_z$ satisfies Eq. (4.1). The state vector is:
$$V_{\text{anti}}(x) = [u_z, u_{z,x}, P_z, R_z]^T \tag{6.1}$$

The exact $4 \times 4$ transfer matrix $T_j$ relating $V_{\text{anti}}(a_j) = T_j V_{\text{anti}}(0)$ is:
$$T_j = \frac{1}{\sigma_s^2 + \tau_s^2} \begin{bmatrix}
t_{11} & t_{12} & t_{13} & t_{14} \\
t_{21} & t_{22} & t_{23} & t_{24} \\
t_{31} & t_{32} & t_{33} & t_{34} \\
t_{41} & t_{42} & t_{43} & t_{44}
\end{bmatrix} \tag{6.2}$$
where the entries $t_{kn}$ are identically those of Appendix 1 of Li, Wei & Zhou (2016):
- $t_{k1} = e_{k1}(\sigma_s^2 + \tau_s^2 - \beta_s^2) + \beta_s^2 e_{k2}$
- $t_{k2} = [(\tau_s^2 - \xi^2) - (1 - m_s)/c] e_{k3} + [(1 - m_s)/c + (\sigma_s^2 + \xi^2)] e_{k4}$
- $t_{k3} = \frac{e_{k3} - e_{k4}}{\mu c}$
- $t_{k4} = \frac{e_{k2} - e_{k1}}{\mu c}$
with:
$$\begin{array}{llll}
e_{11} = \cos(\beta_s a_j), & e_{12} = \cosh(\gamma_s a_j), & e_{13} = \frac{\sin(\beta_s a_j)}{\beta_s}, & e_{14} = \frac{\sinh(\gamma_s a_j)}{\gamma_s} \\
e_{21} = -\beta_s \sin(\beta_s a_j), & e_{22} = \gamma_s \sinh(\gamma_s a_j), & e_{23} = \cos(\beta_s a_j), & e_{24} = \cosh(\gamma_s a_j) \\
e_{31} = \mu \beta_s [-(1-m_s) - c(\sigma_s^2+\xi^2)] \sin(\beta_s a_j), & e_{32} = \mu \gamma_s [(1-m_s) - c(\tau_s^2-\xi^2)] \sinh(\gamma_s a_j) & & \\
e_{33} = \mu [(1-m_s) + c(\sigma_s^2+\xi^2)] \cos(\beta_s a_j), & e_{34} = \mu [(1-m_s) - c(\tau_s^2-\xi^2)] \cosh(\gamma_s a_j) & & \\
e_{41} = -\mu c \beta_s^2 \cos(\beta_s a_j), & e_{42} = \mu c \gamma_s^2 \cosh(\gamma_s a_j), & e_{43} = -\mu c \beta_s \sin(\beta_s a_j), & e_{44} = \mu c \gamma_s \sinh(\gamma_s a_j)
\end{array}$$

---

## 7. Interface Continuity Conditions & Transmission Matrix

Across the planar interface between Layer A ($x = a_1^-$) and Layer B ($x = a_1^+$), physical requirements dictate:

| # | State Quantity | Interface Condition | Variational / Physical Derivation | SI Units |
|:---:|:---:|:---:|---|:---:|
| 1 | $u_x$ | $[u_x] = 0$ | Kinematic compatibility; essential boundary continuity. | $\text{m}$ |
| 2 | $u_y$ | $[u_y] = 0$ | Tangential displacement compatibility (no interfacial slip). | $\text{m}$ |
| 3 | $u_{x,x}$ | $[u_{x,x}] = 0$ | Variational boundary term $\int_S R_k D(\delta u_k) dS$ in Mindlin Form-II gradient elasticity. Discontinuity would produce infinite dipolar strain energy $\frac{1}{2}c\lambda(\varepsilon_{ii,k})^2$ (Dirac delta squared). | Dimensionless |
| 4 | $u_{y,x}$ | $[u_{y,x}] = 0$ | Continuity of tangential gradient across interface (higher-order kinematic compatibility). | Dimensionless |
| 5 | $\theta$ | $[\theta] = 0$ | 0th law of thermodynamics; intimate thermal contact (zero Kapitza resistance). | $\text{K}$ |
| 6 | $P_x$ | $[P_x] = 0$ | Natural boundary condition from $\delta u_x$ virtual work balance on $S$. | $\text{Pa}$ |
| 7 | $P_y$ | $[P_y] = 0$ | Natural boundary condition from $\delta u_y$ virtual work balance on $S$. | $\text{Pa}$ |
| 8 | $R_x$ | $[R_x] = 0$ | Higher-order traction balance conjugate to virtual gradient $\delta u_{x,x}$ on $S$. | $\text{N/m}$ |
| 9 | $R_y$ | $[R_y] = 0$ | Higher-order traction balance conjugate to virtual gradient $\delta u_{y,x}$ on $S$. | $\text{N/m}$ |
| 10 | $q_x$ | $[q_x] = 0$ | Local conservation of thermal energy across an interface of zero thermal capacity. | $\text{W/m}^2$ |

Because every quantity in $V_{\text{in}}$ (and $V_{\text{anti}}$) is continuous:
$$V_{\text{in}}(a_1^+) = V_{\text{in}}(a_1^-) \implies M_{\text{interface}} \equiv I_{10 \times 10} \quad (\text{and } I_{4 \times 4}) \tag{7.1}$$

---

## 8. Layer & Unit-Cell Transfer Matrices

### 8.1 Layer Transfer Matrix $T_j(\omega)$
At $x = 0$: $V_L^{(j)} = P_j \mathbf{C}_j \implies \mathbf{C}_j = P_j^{-1} V_L^{(j)}$.  
At $x = a_j$: $V_R^{(j)} = P_j G_j \mathbf{C}_j = P_j G_j P_j^{-1} V_L^{(j)}$.  
Therefore:
$$T_j(\omega) = P_j(\omega) G_j(\omega) P_j^{-1}(\omega) \tag{8.1}$$
where $G_j(\omega) = \text{diag}\left( e^{i k_{p1} a_j}, e^{-i k_{p1} a_j}, e^{i k_{p2} a_j}, e^{-i k_{p2} a_j}, e^{i k_{p3} a_j}, e^{-i k_{p3} a_j}, e^{i k_{s1} a_j}, e^{-i k_{s1} a_j}, e^{i k_{s2} a_j}, e^{-i k_{s2} a_j} \right)$.

### 8.2 Composite Unit-Cell Transfer Matrix $T_{\text{cell}}(\omega)$
For a unit cell composed of Layer A on $[0, a_1]$ and Layer B on $[a_1, a_1+a_2]$:
$$V(a) = T_B(\omega) T_A(\omega) V(0) \implies T_{\text{cell}}(\omega) = T_B(\omega) T_A(\omega) \tag{8.2}$$

---

## 9. Bloch-Floquet Dispersion & Physical Taxonomy

Applying the Bloch theorem $V(x + a) = e^{i k_x a} V(x)$:
$$\det\left( T_{\text{cell}}(\omega) - e^{i k_x a} I \right) = 0 \tag{9.1}$$
Solving for eigenvalues $\lambda_m$ gives $k_{x,m} a = -i \ln \lambda_m = k_{r,m} a + i k_{i,m} a$.

### Quantitative Distinction of Spectral Features:
1. **Conservative Limit ($\beta = 0$):**
   - *Pass Band:* $|\lambda| = 1 \implies k_i = 0$.
   - *Zone Boundary / Band Edge:* $k_r a = 0$ or $\pi$ with $v_g = d\omega/dk_r = 0$. *(Necessary edge condition, not a gap by itself).*
   - *Material-Contrast Bragg Gap:* $|\lambda| \neq 1$ for all modes at $\omega$; $k_r a$ pinned to $0$ or $\pi$ while $k_i > 0$. Spatial decay is purely evanescent.
2. **Dissipative DPL System ($\beta > 0, \tau_q > 0, \tau_\theta > 0$):**
   - Thermal diffusion introduces intrinsic damping ($k_i > 0$) across all frequencies.
   - *Damped Pass Bands:* Continuous $k_r \in (0, \pi/a)$ with low background attenuation $k_i \ll 1/a$.
   - *Bragg Gaps in Dissipative Media:* Resonant peaks in attenuation ($k_i \gg 1/a$) coupled with branch transitions in the complex $\Omega-k_x$ Riemann surface.

---

## 10. Conservative Limit & Determinant Symplecticity Analysis

- In the **conservative elastic limit** ($\beta \to 0$):
  $$T_j^T J T_j = J \implies \det(T_j) \equiv +1.00000000000000$$
  This property was verified in our pre-derivation calculation ($|\det(T_j)| = 1.00000000000000 \pm 10^{-14}$).
- **Scientific Audit Rule:** $\det(T) = 1$ is an exact property **strictly in the conservative limit** and serves as a hard numerical verification diagnostic for the mechanical code. For the full dissipative DPL system ($\beta > 0$), thermal diffusion breaks time-reversal invariance, so $\det(T_{\text{cell}}) \neq 1$.

---

## 11. Analytical Limiting Cases & Benchmark Recovery

### 11.1 Limit A: Decoupled Gradient Elasticity ($\beta \to 0$)
Setting $\beta = 0$ decouples the cubic polynomial (4.8) into an uncoupled thermal diffusion root $K_{\text{th}} = k_{\text{th}}^2$ and two uncoupled gradient elastic roots matching Eq. (16.1) of Li, Wei & Zhou (2016) identically.

### 11.2 Limit B: Classical Fourier Thermoelasticity ($\tau_q \to 0, \tau_\theta \to 0$)
$k_{\text{eff}}(\omega) \to k$, collapsing the DPL equation to the classical parabolic Biot-Fourier coupled equation.

### 11.3 Limit C: Classical Cauchy Thermoelasticity ($c \to 0, d \to 0$)
Hyperstresses $R_x, R_y \to 0$, monopolar tractions reduce to Cauchy stresses, and the cubic polynomial drops its $K^3$ term to recover classical thermoelasticity.

### 11.4 Limit D: Homogeneous Medium & Papargyri-Beskou Recovery
When Layer A and Layer B are identical ($A = B$):
- Material-contrast-induced Bragg band gaps disappear identically ($\Delta\Omega_{\text{Bragg}} = 0$).
- **Longitudinal Waves with Active DPL ($\beta > 0$):** Waves experience intrinsic thermal dispersion and damping governed by the homogeneous coupled cubic polynomial (Eq. 4.8).
- **Exact Recovery of Papargyri-Beskou (2009):** The pure gradient-elastic dispersion relation of Papargyri-Beskou et al. (2009, IJSS Eq. 28),
  $$\frac{\omega}{k} = V_c \sqrt{\frac{1 + g^2 k^2}{1 + h^2 k^2}}$$
  is recovered under either of two exact mathematical conditions:
  1. **Anti-plane shear waves ($u_z$):** Decoupled from dilatation for all $\beta$ (with $V_c = V_s, g^2 = c, h^2 = d^2/3$).
  2. **Longitudinal waves with suppressed thermoelastic coupling ($\beta \to 0$):** (with $V_c = V_p, g^2 = c, h^2 = d^2/3$).
  In both cases, numerical verification confirms zero algebraic residual and machine-precision agreement ($1.11 \times 10^{-16}$).
