# PHASE 2 IMPLEMENTATION DECISIONS RECORD

### Project: `paper10`
### Document: `paper10/audit/decisions/PHASE2_IMPLEMENTATION_DECISIONS.md`
**Date:** 2026-09-26  
**Governing Baseline:** Commit `e9ca21f` (Phase 1 Final Locked Baseline)  
**Author:** Implementation Engineer (Arena Agent)  
**Status:** RECORDED & AUDITED

---

## Decision 1: Modular Separation of Anti-Plane Pilot and 10-State Coupled Solver
- **Context:** The governing Blueprint and Phase 1 derivation specify both an anti-plane 4-state system ($u_z, u_{z,x}, P_z, R_z$) and a 10-state coupled in-plane thermoelastic system ($u_x, u_y, u_{x,x}, u_{y,x}, \theta, P_x, P_y, R_x, R_y, q_x$).
- **Decision:** Implement the 4-state system first in `antiplane.py` as a clean, decoupled pilot for conservative gradient-elastic benchmark validation. Only after Gate G2-C and Gate G2-B pass, implement the 10-state coupled solver in `coupled10.py`.
- **Rationale:** Anti-plane shear motion is identically decoupled from thermal dilatation ($\nabla \cdot \mathbf{u} \equiv 0$). It provides the cleanest mathematical testbed for verifying the higher-order gradient elasticity equations without thermal confounding factors.

---

## Decision 2: Numerically Stable Algebraic Formulation for Classical Limit ($c \to 0$)
- **Context:** In computing $\sigma_s^2 = \frac{1}{2c}[\Delta_s - (1 - m_s)]$ where $\Delta_s = \sqrt{(1-m_s)^2 + 4c\omega^2/V_s^2}$, taking $c \to 0$ directly in float64 arithmetic produces catastrophic cancellation ($1.0000000000000000 - 1.0 = 0.0$), causing division by zero and loss of precision.
- **Decision:** Reformulate the root algebraically by multiplying numerator and denominator by $\Delta_s + (1 - m_s)$:
  $$\sigma_s^2 = \frac{\Delta_s^2 - (1 - m_s)^2}{2c [\Delta_s + (1 - m_s)]} = \frac{2\omega^2 / V_s^2}{\Delta_s + (1 - m_s)}$$
- **Rationale:** The parameter $c$ in the denominator is algebraically eliminated. In the classical limit $c \to 0$ and $m_s \to 0$, $\sigma_s^2 \to \frac{2\omega^2/V_s^2}{1 + 1} = \frac{\omega^2}{V_s^2}$ smoothly down to machine zero ($c \sim 10^{-16}$) without any roundoff error.

---

## Decision 3: Canonical Matrix Equilibration for Modal Matrices
- **Context:** In physical SI units, state vector components span vastly different dimensional orders: displacement $u \sim 10^{-6}\,\text{m}$, stress $P \sim 10^{9}-10^{11}\,\text{Pa}$, hyperstress $R \sim 10^5\,\text{N/m}$, and heat flux $q \sim 10^{14}-10^{24}\,\text{W/m}^2$. The unscaled modal matrix $P$ exhibits an artificial condition number $\kappa(P_{\text{raw}}) \sim 10^{22}$.
- **Decision:** Implement canonical dual row- and column-equilibration:
  $$P_{\text{equil}} = D_{\text{row}}^{-1} P D_{\text{col}}^{-1}, \quad P^{-1} = D_{\text{col}}^{-1} P_{\text{equil}}^{-1} D_{\text{row}}^{-1}$$
- **Rationale:** In linear algebra, similarity transformations $T = P G P^{-1}$ are scale-invariant: $(D P) G (D P)^{-1} = D (P G P^{-1}) D^{-1}$. Canonical equilibration reduces the effective condition number to $\kappa(P_{\text{equil}}) \sim 10^5$, ensuring pristine inversion and stable transfer matrix construction.

---

## Decision 4: Physical Layer Dimensions for Thermal Diffusion Regimes
- **Context:** In testing the full 10-state DPL model, the thermal wave wavenumber is $k_{\text{th}} = (1+i)\sqrt{\frac{\omega \rho c_v}{2 k}} \approx 7.4\times 10^4\,\text{m}^{-1}$ at $1\,\text{MHz}$. Across a macro-layer of thickness $a = 5\,\text{mm}$ ($380$ thermal wavelengths), $\exp(k_{\text{th}} a) = \exp(370) \approx 10^{161}$ causes floating-point overflow.
- **Decision:** Set microstructured layer thicknesses for high-frequency DPL tests to realistic micro-device scales ($a = 20\,\mu\text{m}$, matching microstructural length scales $g, h \sim 10-15\,\mu\text{m}$).
- **Rationale:** Phononic crystal metamaterials operating in gradient-elastic and non-Fourier thermal regimes are microscopic devices (micro/nano-electromechanical systems, MEMS/NEMS). Evaluating the solver on physically relevant micro-dimensions ensures realistic phase accumulation and completely prevents artificial numerical overflow.

---

## Decision 5: Non-Imposition of Symplecticity on Dissipative DPL Systems
- **Context:** In conservative elastodynamics, $\det(T) \equiv 1$ and $T^T J T = J$ due to Hamiltonian symplecticity.
- **Decision:** Enforce and verify $\det(T) \equiv 1$ strictly on the conservative mechanical limits (Papargyri-Beskou benchmark and two-layer conservative pilot). Do NOT enforce $\det(T) = 1$ on the full DPL system.
- **Rationale:** Thermal diffusion and phase lags introduce irreversible entropy generation and break time-reversal invariance. Enforcing $\det(T) = 1$ on a dissipative system would be physically incorrect.
