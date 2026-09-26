# PHASE 1 DERIVATION DECISIONS RECORD
### Project: `paper10`
### Document: `paper10/audit/decisions/PHASE1_DERIVATION_DECISIONS.md`
**Date:** 2026-09-26  
**Auditor / Author:** Mathematical Derivation Engine (Arena Agent)  
**Status:** COMPLETE & AUDITABLE

---

### Decision 1: Modal Spectral Representation ($T_j = P_j G_j P_j^{-1}$) over Direct Matrix Exponential ($\exp(A_j L_j)$)
- **Context:** In Transfer Matrix formulations, one can either form a first-order system $dV/dx = A V$ and compute $T = \exp(A L)$ numerically, or solve the characteristic polynomial analytically, find the 10 exact eigenvectors, and construct $T = P G P^{-1}$ where $G$ is diagonal.
- **Decision:** Adopt the **modal spectral representation** $T_j = P_j G_j P_j^{-1}$.
- **Rationale:** 
  1. The direct matrix exponential of a $10 \times 10$ matrix containing vastly different physical scales ($u \sim 10^{-9} \, \text{m}$, $\theta \sim 1 \, \text{K}$, $P \sim 10^6 \, \text{Pa}$, $R \sim 10^3 \, \text{N/m}$) suffers from severe numerical scaling and roundoff errors in Padé approximations.
  2. The modal form $P G P^{-1}$ allows analytical calculation of characteristic roots via the exact cubic formula, guaranteeing machine-precision dispersion relations.
  3. It matches the proven mathematical architecture of Li, Wei & Zhou (2016, *Acta Mechanica*) and Li, Askes et al. (2023, *WRCM*), enabling direct limiting-case validation.

---

### Decision 2: State Vector Ordering & Interface Matching
- **Context:** State variables can be grouped by kinematic vs dynamic quantities, or layer-by-layer.
- **Decision:** Lock the state vector ordering as:
  $$V_{\text{in}} = [u_x, u_y, u_{x,x}, u_{y,x}, \theta, P_x, P_y, R_x, R_y, q_x]^T$$
  grouping generalized displacements and thermal potential in positions 1–5, and generalized conjugate tractions, hyperstresses, and normal heat flux in positions 6–10.
- **Rationale:**
  1. This maintains a clear block-bipartite structure between generalized configuration coordinates and generalized forces.
  2. In the uncoupled elastic limit ($\beta \to 0$), the 5th and 10th rows/columns decouple cleanly, leaving the exact $8 \times 8$ in-plane gradient elasticity state vector of Li et al. (2016).
  3. In the anti-plane case, the same logic produces $V_{\text{anti}} = [u_z, u_{z,x}, P_z, R_z]^T$ (positions 1–2 displacements, positions 3–4 tractions).

---

### Decision 3: Decoupling Strategy via Helmholtz Potentials
- **Context:** Direct substitution of displacements into the coupled gradient equations yields a coupled 6th-order system in $u_x, u_y, \theta$.
- **Decision:** Use Helmholtz vector decomposition: $\mathbf{U} = \nabla\Phi + \nabla\times(\Psi\mathbf{e}_z)$.
- **Rationale:**
  1. The transverse shear potential $\Psi$ completely decouples from the thermal field $\Theta$, reducing the shear wave propagation to an exact 4th-order polynomial identical to pure gradient elasticity.
  2. Dilatational coupling is isolated entirely into the scalar pair $(\Phi, \Theta)$, yielding a monic cubic polynomial in $K = k^2 + \xi^2$.
  3. This drastically reduces the algebraic complexity and eliminates spurious numerical roots.

---

### Decision 4: Interface Transmission Matrix ($M_{\text{interface}} = I$)
- **Context:** Across the interface between Layer A and Layer B, one must verify whether the state vector undergoes a jump or is continuous.
- **Decision:** Establish that $V_R^A = V_L^B \implies M_{\text{interface}} = I_{10 \times 10}$.
- **Rationale:**
  1. Under Mindlin Form-II gradient elasticity, continuity of $u_i$ and $u_{i,x}$ is required by variational energy boundedness.
  2. Equilibrium of boundary tractions requires $P_i$ and $R_i$ to be continuous.
  3. Perfect thermal contact requires $\theta$ and $q_x$ to be continuous.
  4. Since all 10 state variables are physical boundary observables that are continuous, the interface transmission matrix is identically the identity matrix.

---

### Decision 5: Conservative Symplecticity vs. Dissipative Attenuation
- **Context:** In literature, unimodularity $\det(T) = 1$ is often mistakenly asserted for dissipative systems.
- **Decision:** Explicitly restrict the mathematical claim $\det(T) = 1$ to the **conservative elastic limit** ($\beta \to 0$).
- **Rationale:**
  1. Dual-Phase-Lag thermal diffusion is physically irreversible; entropy production breaks Hamiltonian symplecticity.
  2. Asserting $\det(T) = 1$ for the coupled DPL system would be a fatal scientific error that reviewers in *Applied Mathematical Modelling* or *IJSS* would reject.
  3. Retaining $\det(T) = 1$ as a Level 1 / Level 2 benchmark diagnostic in the uncoupled limit provides an ironclad numerical verification gate while preserving thermodynamic truth.
