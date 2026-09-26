# PHASE 1 SYMBOL TABLE — DPL THERMOELASTIC METAMATERIALS
### Project: `paper10`
### Document: `paper10/derivations/PHASE1_SYMBOL_TABLE.md`
**Date:** 2026-09-26  
**Status:** COMPLETE & AUDITABLE

---

| Symbol | Definition | Physical Meaning | SI Units | First Occurrence | Used In |
|---|---|---|---|---|---|
| $x, y, z$ | Cartesian coordinates | Spatial position vectors | $\text{m}$ | Section 1 | Kinematics, PDEs, TMM |
| $t$ | Time variable | Temporal coordinate | $\text{s}$ | Section 1 | Dynamic equations of motion |
| $\omega$ | Angular frequency | Wave circular frequency | $\text{rad/s}$ | Section 3 | Harmonic representation, TMM |
| $\xi$ | Apparent wavenumber | Wavenumber along interface ($y$) | $\text{m}^{-1}$ | Section 3 | Helmholtz decomposition, TMM |
| $u_x, u_y, u_z$ | Displacement components | Elastic displacement vector $\mathbf{u}$ | $\text{m}$ | Section 1 | Equations of motion, State Vector |
| $\theta$ | $T - T_0$ | Temperature increment above ambient | $\text{K}$ | Section 1 | DPL energy equation, State Vector |
| $T_0$ | Reference temperature | Absolute ambient temperature | $\text{K}$ | Section 1 | Thermoelastic energy equation |
| $\rho$ | Mass density | Volumetric mass density | $\text{kg/m}^3$ | Section 1 | Inertia terms, wave speeds |
| $\lambda, \mu$ | Lamé elastic constants | Classical elastic moduli | $\text{Pa}$ | Section 2 | Constitutive relations, wave speeds |
| $c = g^2$ | Micro-stiffness parameter | Square of micro-stiffness length scale | $\text{m}^2$ | Section 2 | Dipolar gradient strain energy |
| $d = \sqrt{3}h$| Micro-inertia parameter | Micro-inertia characteristic length | $\text{m}$ | Section 1 | Micro-inertia kinetic energy |
| $\alpha_t$ | Thermal expansion | Linear thermal expansion coefficient | $\text{K}^{-1}$ | Section 1 | Thermoelastic coupling factor |
| $\beta$ | $(3\lambda+2\mu)\alpha_t$ | Thermal stress coupling coefficient | $\text{Pa/K}$ | Section 1 | Momentum balance, stress tensor |
| $k$ | Thermal conductivity | Classical Fourier thermal conductivity | $\text{W/(m}\cdot\text{K)}$ | Section 1 | DPL constitutive relation |
| $c_v$ | Specific heat capacity | Specific heat at constant strain | $\text{J/(kg}\cdot\text{K)}$ | Section 1 | Energy conservation equation |
| $\tau_q$ | Heat flux phase lag | Relaxation time of thermal flux | $\text{s}$ | Section 1 | DPL heat conduction model |
| $\tau_\theta$ | Temp gradient phase lag | Retardation time of temperature gradient | $\text{s}$ | Section 1 | DPL heat conduction model |
| $k_{\text{eff}}(\omega)$ | $k \frac{1-i\omega\tau_\theta}{1-i\omega\tau_q}$ | Complex effective thermal conductivity | $\text{W/(m}\cdot\text{K)}$ | Section 3 | Frequency-domain DPL flux |
| $k_{\text{th}}^2(\omega)$| $\frac{i\omega\rho c_v}{k_{\text{eff}}(\omega)}$ | Complex thermal wave operator parameter | $\text{m}^{-2}$ | Section 3 | Coupled characteristic polynomial |
| $\eta_{\text{th}}(\omega)$| $\frac{i\omega T_0 \beta}{k_{\text{eff}}(\omega)}$ | Thermal-to-dilatational coupling factor | $\text{K/m}^2$ | Section 3 | Coupled energy equation |
| $V_p$ | $\sqrt{(\lambda+2\mu)/\rho}$ | Classical longitudinal wave speed | $\text{m/s}$ | Section 3 | Characteristic polynomial |
| $V_s$ | $\sqrt{\mu/\rho}$ | Classical transverse wave speed | $\text{m/s}$ | Section 3 | Characteristic polynomial |
| $m_p, m_s$ | $\frac{\omega^2 d^2}{3 V_{p,s}^2}$ | Non-dimensional micro-inertia numbers | Dimensionless | Section 3 | Characteristic roots $\sigma, \tau$ |
| $\Phi$ | Scalar potential | Longitudinal displacement potential | $\text{m}^2$ | Section 4 | Helmholtz wave decomposition |
| $\Psi$ | Vector potential ($z$) | Shear displacement potential | $\text{m}^2$ | Section 4 | Helmholtz wave decomposition |
| $P_x, P_y, P_z$ | Monopolar tractions | Generalized surface forces | $\text{Pa} = \text{N/m}^2$ | Section 2 | Boundary conditions, State Vector |
| $R_x, R_y, R_z$ | Dipolar tractions | Generalized surface hyperstresses | $\text{N/m}$ | Section 2 | Boundary conditions, State Vector |
| $q_x$ | Heat flux normal component| Conductive heat flux along $x$ | $\text{W/m}^2$ | Section 2 | Energy balance, State Vector |
| $a_1, a_2$ | Layer thicknesses | Geometric thickness of layers A and B | $\text{m}$ | Section 1 | Unit cell dimensions |
| $a$ | $a_1 + a_2$ | Lattice period of unit cell | $\text{m}$ | Section 1 | Bloch-Floquet theorem |
| $V_{\text{in}}(x)$ | 10-element vector | State vector for in-plane waves | Mixed SI | Section 5 | Transfer Matrix Method |
| $V_{\text{anti}}(x)$| 4-element vector | State vector for anti-plane waves | Mixed SI | Section 6 | Transfer Matrix Method |
| $T_j(\omega)$ | Layer transfer matrix | Relates state vector across layer $j$ | Dimensionless | Section 8 | Transfer Matrix Method |
| $T_{\text{cell}}(\omega)$| $T_B T_A$ | Composite unit cell transfer matrix | Dimensionless | Section 8 | Bloch eigenvalue problem |
| $\lambda$ | $e^{i k_x a}$ | Bloch eigenvalue / multiplier | Dimensionless | Section 9 | Bloch-Floquet dispersion |
| $k_r$ | $\text{Re}(k_x)$ | Bloch phase wavenumber | $\text{m}^{-1}$ | Section 9 | Dispersion curve, Pass bands |
| $k_i$ | $\text{Im}(k_x)$ | Bloch spatial attenuation constant | $\text{m}^{-1}$ | Section 9 | Band gaps, Material dissipation |
