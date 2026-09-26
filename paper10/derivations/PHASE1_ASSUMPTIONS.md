# PHASE 1 ASSUMPTIONS RECORD — DPL THERMOELASTIC METAMATERIALS
### Project: `paper10`
### Document: `paper10/derivations/PHASE1_ASSUMPTIONS.md`
**Date:** 2026-09-26  
**Status:** COMPLETE & AUDITABLE

---

## 1. Continuum & Kinematic Assumptions
1. **Infinitesimal Deformation:** The elastic deformations and displacement gradients are assumed sufficiently small such that the linear strain tensor $\varepsilon_{ij} = \frac{1}{2}(u_{i,j} + u_{j,i})$ and linear rotation tensor are valid. Geometric nonlinearities (finite strain / von Kármán terms) are excluded.
2. **Mindlin Form-II Dipolar Gradient Elasticity:** The strain energy density $W$ depends quadratically on both the strain tensor $\varepsilon_{ij}$ and the first gradient of the strain tensor $\varepsilon_{ij,k}$. The second and higher gradients are neglected.
3. **Centrosymmetric & Isotropic Media:** Each individual layer (Layer A and Layer B) is assumed to be chemically homogeneous, elastically isotropic, and centrosymmetric, eliminating coupling tensors between strain and strain gradient of odd rank ($f_{ijklm} = 0$).
4. **Single Micro-Length Scale per Gradient Mechanism:** A single micro-stiffness length-scale parameter $c = g^2$ and a single micro-inertia length-scale parameter $d = \sqrt{3}h$ are employed per material, consistent with the simplified Mindlin Form-II formulation adopted by Papargyri-Beskou et al. (2009) and Li, Wei & Zhou (2016).

---

## 2. Thermal Transport & Thermodynamic Assumptions
5. **Linearized Dual-Phase-Lag (DPL) Model:** Non-Fourier heat transport is described by Tzou's dual-phase-lag model expanded to first order in time derivatives: $\mathbf{q} + \tau_q \dot{\mathbf{q}} = -k \nabla\theta - k\tau_\theta \nabla\dot{\theta}$. Second- and higher-order Taylor expansions are neglected.
6. **Thermodynamic Admissibility:** The phase lags satisfy $\tau_q \ge \tau_\theta > 0$ and $k > 0$, ensuring compliance with the second law of thermodynamics, non-negative entropy production, and absence of spontaneous instability.
7. **Small Temperature Variations:** The temperature rise $|\theta| = |T - T_0| \ll T_0$ is small compared to the absolute reference temperature ($T_0 = 300 \, \text{K}$), justifying constant thermo-physical material parameters ($k, c_v, \alpha_t, \lambda, \mu$).
8. **Absence of Internal Sources:** No internal volumetric heat sources ($Q = 0$) or body forces ($\mathbf{f} = 0$) are present within the domain.

---

## 3. Wave Propagation & Interface Assumptions
9. **Steady-State Time-Harmonic Regime:** All dynamic field variables vary harmonically in time as $e^{-i\omega t}$. Transient startup and initial-boundary value transients are not considered.
10. **Planar Interface & 1D Periodicity:** Layers are infinite and invariant along the $z$-direction, with flat, parallel interfaces perpendicular to the $x$-axis. Wave propagation occurs in the $x-y$ plane with apparent wavenumber $\xi$.
11. **Perfect Mechanical & Micro-Kinematic Contact:** Across layer interfaces, there is no slip, no separation, and no micro-discontinuity: displacements ($u_x, u_y, u_z$) and normal derivatives ($u_{x,x}, u_{y,x}, u_{z,x}$) are strictly continuous.
12. **Perfect Thermal Contact:** The interface exhibits zero thermal contact resistance ($[\theta] = 0$) and continuous normal conductive heat flux ($[q_x] = 0$).
13. **Bloch-Floquet Periodicity:** The medium consists of an infinite periodic sequence of unit cells of length $a = a_1 + a_2$. Edge boundaries and finite-structure truncation effects are governed by the classical Bloch theorem.
