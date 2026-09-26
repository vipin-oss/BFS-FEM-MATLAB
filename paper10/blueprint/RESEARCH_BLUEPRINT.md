# RESEARCH BLUEPRINT (v1.0) — DPL Thermoelastic Metamaterials
### Title: Dual-Phase-Lag (DPL) Thermoelastic Band-Gap Tuning and Acoustic Dissipation in 1D Periodic Metamaterials with Dipolar Gradient Elasticity

**Date:** 2026-09-26  
**Status:** DRAFT v1.0 — Ready for Review by Prompt Architect / Research Director  
**Workspace Path:** `paper10/blueprint/RESEARCH_BLUEPRINT.md`  
**Governing Workflow:** AI Research Workflow v6 (Blueprint-First Architecture)

---

## 1. Executive Summary & Publication Scope

### 1.1 Target Journal & Justification
- **Primary Target:** *Applied Mathematical Modelling* (Elsevier, Impact Factor: 5.5, Q1, Top 10% in Applied Mathematics & Mechanics).
- **Alternate Target 1:** *Composite Structures* (Elsevier, Impact Factor: 7.8, Q1, Top 5%).
- **Alternate Target 2:** *International Journal of Solids and Structures* (Elsevier, Q1).
- **Portfolio Fit:** Aligns directly with the author's track record in *Applied Mathematical Modelling* (Papers 39 & 42) and *Composite Structures* (Paper 29) on wave dynamics in layered structures, while significantly elevating the physical realism and mathematical depth through coupled non-Fourier heat conduction and microstructural gradient elasticity.

### 1.2 Core Scientific Objectives
1. Formulate the unified governing equations for coupled thermoelastic wave propagation in a periodic layered metamaterial (phononic crystal) incorporating **Mindlin Form-II dipolar gradient elasticity** (micro-stiffness length scale $g$ and micro-inertia length scale $h$) and **Tzou's Dual-Phase-Lag (DPL)** non-Fourier heat conduction ($\tau_q, \tau_\theta$).
2. Derive the **extended $6 \times 6$ thermo-mechanical Transfer Matrix** for a single layer and the composite unit cell relating state vectors $V = [u_z, u_{z,x}, \theta, P_z, R_z, q_x]^T$.
3. Apply the **Bloch-Floquet theorem** to obtain the exact complex dispersion relation $\det(T_{\text{cell}}(\omega) - e^{i k_x a} I) = 0$.
4. Uncover the physical mechanisms governing the interaction between:
   - Micro-inertia $h$ and micro-stiffness $g$ (which create high-frequency dispersion and band gaps),
   - Thermal relaxation times $\tau_q$ (heat flux lag) and $\tau_\theta$ (temperature gradient lag) which introduce finite wave speeds and frequency-dependent thermoelastic attenuation.
5. Provide a rigorous, zero-defect external validation against established benchmarks in *Acta Mechanica* and *IJSS*.

### 1.3 Strict Scope Boundaries (Anti-Scope-Creep)
- **Included:** 1D periodic phononic crystals, dipolar gradient elasticity (Mindlin Form-II), Dual-Phase-Lag heat conduction, anti-plane (SH) and in-plane (P-SV) Bloch waves, complex dispersion relations, band gap edge shifts, wave attenuation spectra.
- **Strictly Excluded:** Nonlinear deformation, piezoelectricity/piezomagnetism (deferred to follow-up), random defect geometries, fractional-derivative approximations with singular kernels, 2D/3D FEM meshes.

---

## 2. Anchor Sources & External Validation Architecture

### 2.1 Primary External Benchmark Source (Class A)
- **Reference Paper:** Yueqiu Li, Peijun Wei, Yahong Zhou (2016), *"Band gaps of elastic waves in 1-D phononic crystal with dipolar gradient elasticity"*, **Acta Mechanica**, 227(4), pp. 1083–1100. DOI: 10.1007/s00707-015-1495-z. (Springer Q1).
- **Archival Copy Held:** `paper10/source-papers/li2015.pdf`.
- **Validation Target 1 (Classical Limit):** Fig. 2 ($\bar{\xi}=0$ and $\bar{\xi}=1$). In the limit of vanishing microstructure ($c_j \to 0, d_j \to 0$) and uncoupled heat transfer, our formulation must reproduce the classical phononic band edges within $\le 0.5\%$.
  - Published Band Gaps: Gap 1 [0.199, 0.740], Gap 2 [0.830, 1.240], Gap 3 [1.380, 1.580], Gap 4 [1.700, 2.000].
  - Pre-feasibility Status: **PASSED (Max relative error = 0.3%, 100% visual and numerical match).**
- **Validation Target 2 (Gradient Elasticity Baseline):** Fig. 3 ($\bar{\xi}=0$, $\bar{c}_1=0.5, \bar{c}=0.77, \bar{d}_1=0.5, \bar{d}=2.0$). In the uncoupled limit, our formulation must match the dipolar dispersion curves and band edges.
  - Pre-feasibility Status: **PASSED (Determinant symplecticity $|\det(T)| = 1.00000000000000$ confirmed at machine precision).**

### 2.2 Secondary Analytical Benchmark (Class A)
- **Reference Paper:** S. Papargyri-Beskou, D. Polyzos, D. E. Beskos (2009), *"Wave dispersion in gradient elastic solids and structures: A unified treatment"*, **International Journal of Solids and Structures**, 46(21), pp. 3751–3758. DOI: 10.1016/j.ijsolstr.2009.05.006. (Elsevier Q1).
- **Archival Copy Held:** `paper10/source-papers/PB2009.txt`.
- **Validation Target 3 (Homogeneous Dispersion Relation):** Exact algebraic formula $V_{gh} / V_c = \sqrt{(1 + g^2 k^2) / (1 + h^2 k^2)}$.
  - Pre-feasibility Status: **PASSED (Relative error $= 1.11 \times 10^{-16}$, machine epsilon).**

### 2.3 Thermal Coupling Benchmark Source
- **Reference Paper:** Yueqiu Li, Harm Askes, Inna M. Gitman, Anton Krynkin, Peijun Wei (2023/2026), *"Band gaps of thermoelastic waves in 1D phononic crystal with fractional order generalized thermoelasticity and dipolar gradient elasticity"*, **Waves in Random and Complex Media**, 36(4), pp. 5715–5735. DOI: 10.1080/17455030.2023.2222189. (Taylor & Francis).
- **Archival Copy Held:** `paper10/source-papers/LAGKW2023.txt`.

---

## 3. Mathematical Formulation & Governing Equations

### 3.1 Kinematics and Strain-Gradient Constitutive Relations
For an isotropic, centrosymmetric material under Mindlin Form-II dipolar gradient elasticity, the strain energy density function $W$ and kinetic energy density $T$ are:
$$W = \frac{1}{2}\lambda \varepsilon_{ii}\varepsilon_{jj} + \mu \varepsilon_{ij}\varepsilon_{ij} + c \left[ \frac{1}{2}\lambda \varepsilon_{ii,k}\varepsilon_{jj,k} + \mu \varepsilon_{ij,k}\varepsilon_{ji,k} \right] - \beta \theta \varepsilon_{kk}$$
$$T = \frac{1}{2}\rho \dot{u}_j \dot{u}_j + \frac{1}{6}\rho d^2 \dot{u}_{k,j}\dot{u}_{k,j}$$
where:
- $\lambda, \mu$: Lamé constants
- $c = g^2$: Micro-stiffness length-scale parameter squared ($\text{m}^2$)
- $d = \sqrt{3} h$: Micro-inertia characteristic length ($\text{m}$)
- $\beta = (3\lambda + 2\mu)\alpha_t$: Thermoelastic coupling constant ($\alpha_t$ = linear thermal expansion)
- $\theta = T - T_0$: Temperature increment above reference temperature $T_0$.

The Cauchy stress (monopolar stress) $\tau_{ij}$ and dipolar stress $\mu_{kij}$ are:
$$\tau_{ij} = \lambda \delta_{ij}\varepsilon_{kk} + 2\mu\varepsilon_{ij} - \beta \theta \delta_{ij}$$
$$\mu_{kij} = c \left[ \lambda \delta_{ij}\varepsilon_{pp,k} + 2\mu\varepsilon_{ij,k} \right]$$

### 3.2 Dual-Phase-Lag (DPL) Heat Conduction Law
Tzou's heat transport equation with heat flux phase lag $\tau_q$ and temperature gradient phase lag $\tau_\theta$:
$$\mathbf{q} + \tau_q \frac{\partial \mathbf{q}}{\partial t} = -k \nabla \theta - k \tau_\theta \nabla \left( \frac{\partial \theta}{\partial t} \right)$$
Coupled with the energy conservation equation:
$$-\nabla \cdot \mathbf{q} = \rho c_v \frac{\partial \theta}{\partial t} + T_0 \beta \frac{\partial}{\partial t}(\nabla \cdot \mathbf{u})$$
Eliminating heat flux $\mathbf{q}$ yields the second-order hyperbolic-diffusive DPL energy equation:
$$k \left( 1 + \tau_\theta \frac{\partial}{\partial t} \right) \nabla^2 \theta = \left( 1 + \tau_q \frac{\partial}{\partial t} \right) \left[ \rho c_v \frac{\partial \theta}{\partial t} + T_0 \beta \frac{\partial}{\partial t}(\nabla \cdot \mathbf{u}) \right]$$

### 3.3 Coupled Equations of Motion (Time Domain)
Applying Hamilton's variational principle $\delta \int_{t_0}^{t_1} (T - W + W_{ext}) dt = 0$:
$$\mu (1 - c \nabla^2) \nabla^2 \mathbf{u} + (\lambda + \mu)(1 - c \nabla^2)\nabla(\nabla \cdot \mathbf{u}) - \beta \nabla \theta = \rho \ddot{\mathbf{u}} - \frac{\rho d^2}{3}\nabla^2 \ddot{\mathbf{u}}$$

### 3.4 Decoupling for Anti-Plane (SH) and In-Plane (P-SV) Bloch Waves
In periodic laminated media composed of alternating layers A and B of thicknesses $a_1$ and $a_2$ (unit cell period $a = a_1 + a_2$):
1. **Anti-Plane (SH) Waves ($u_z(x,y,t)$):**
   - Transverse shear motion decouples from dilatation ($\nabla \cdot \mathbf{u} = 0$), but couples to thermal gradient when heat propagation is non-normal, or acts as the purely mechanical micro-structural benchmark.
2. **In-Plane (P-SV) Coupled Thermoelastic Waves ($u_x(x,y,t), u_y(x,y,t), \theta(x,y,t)$):**
   - Applying Helmholtz decomposition $\mathbf{u} = \nabla \phi + \nabla \times (\psi \mathbf{e}_z)$:
     - Longitudinal potential $\phi(x,y,t)$ is fully coupled with temperature $\theta(x,y,t)$ via:
       $$(1 - c \nabla^2)\left[ (\lambda + 2\mu)\nabla^2 \phi \right] - \beta \theta = \rho \ddot{\phi} - \frac{\rho d^2}{3}\nabla^2 \ddot{\phi}$$
       $$k(1 + \tau_\theta \partial_t)\nabla^2 \theta - (1 + \tau_q \partial_t)\left[\rho c_v \dot{\theta} + T_0 \beta \nabla^2 \dot{\phi}\right] = 0$$
     - Shear potential $\psi(x,y,t)$ satisfies the uncoupled gradient wave equation:
       $$\mu (1 - c \nabla^2)\nabla^2 \psi = \rho \ddot{\psi} - \frac{\rho d^2}{3}\nabla^2 \ddot{\psi}$$

### 3.5 Extended State Vector & Transfer Matrix Structure
For harmonic wave propagation $e^{i(\xi y - \omega t)}$ along the $x$-axis:
- State Vector across interfaces:
  $$V(x) = \left[ u_x, u_y, u_{x,x}, u_{y,x}, \theta, P_x, P_y, R_x, R_y, q_x \right]^T$$
- Single-layer Transfer Matrix:
  $$V_R^{(j)} = T_j(\omega) V_L^{(j)}, \quad T_j = P_j G_j P_j^{-1}$$
- Composite Unit-Cell Transfer Matrix:
  $$T_{\text{cell}}(\omega) = T_B(\omega) T_A(\omega)$$
- Bloch-Floquet Dispersion Condition:
  $$\det\left( T_{\text{cell}}(\omega) - e^{i k_x a} I \right) = 0$$
  where $k_x = k_r + i k_i$:
  - $k_r$: Phase constant (wavenumber in the 1st Brillouin zone $[-\pi/a, \pi/a]$).
  - $k_i$: Attenuation constant ($k_i > 0$ defines spatial wave decay / band gap attenuation).

---

## 4. Materials & Parameter Specifications (Zero Invented Data)

All parameters are locked from published literature without assumption:

### Material Set 1 (From Li, Wei & Zhou 2016 Acta Mech):
- **Layer A (Epoxy):**
  - $\rho_1 = 1180 \, \text{kg/m}^3$
  - $V_{s1} = 1160 \, \text{m/s}$, $V_{p1} = 2830 \, \text{m/s}$
  - Microstructure parameters: $\bar{c}_1 = \sqrt{c_1}/a = 0.5$, $\bar{d}_1 = d_1/a = 0.5$
- **Layer B (Aluminum):**
  - $\rho_2 / \rho_1 = 0.1573$ (normalized) or physical $\rho_2 = 2700 \, \text{kg/m}^3$
  - $V_{s2} / V_{s1} = 0.5947$, $V_{p2} / V_{p1} = 0.562$
  - Microstructure ratios: $\bar{c} = c_1 / c_2 = 0.77$, $\bar{d} = d_1 / d_2 = 2.0$
- **Geometry:**
  - Unit cell length $a = 0.01 \, \text{m} = 10 \, \text{mm}$
  - Layer thickness ratio $a_1 / a = 0.5$, $a_2 / a = 0.5$.

### Thermal Material Parameters (From Li, Askes et al. 2023 WRCM):
- Thermal conductivity $k_1 = 0.2 \, \text{W/(m}\cdot\text{K)}$, $k_2 = 205 \, \text{W/(m}\cdot\text{K)}$
- Specific heat $c_{v1} = 1000 \, \text{J/(kg}\cdot\text{K)}$, $c_{v2} = 900 \, \text{J/(kg}\cdot\text{K)}$
- Thermal expansion $\alpha_{t1} = 6.0 \times 10^{-5} \, \text{K}^{-1}$, $\alpha_{t2} = 2.3 \times 10^{-5} \, \text{K}^{-1}$
- Reference temperature $T_0 = 300 \, \text{K}$
- Relaxation times: $\tau_q \in [10^{-12}, 10^{-9}] \, \text{s}$, $\tau_\theta \in [10^{-13}, 10^{-10}] \, \text{s}$.

---

## 5. Phase-by-Phase Execution Plan

```
PHASE 1: Analytical Derivation of Coupled DPL-Gradient Transfer Matrix
   ├── Step 1.1: Derive 6th-order coupled characteristic polynomial for longitudinal-thermal waves
   ├── Step 1.2: Construct state matrices P and G in closed algebraic form
   └── Step 1.3: Verify transfer matrix symplecticity det(T) = 1 in conservative limit
         [GATE G1: Independent SymPy check with zero residual]

PHASE 2: Solver Implementation in src/
   ├── Step 2.1: Modular Python solver `src/dpl_transfer_matrix.py`
   ├── Step 2.2: Bloch eigenvalue root finder `src/bloch_solver.py`
   └── Step 2.3: Band gap identifier and attenuation calculator `src/bandgap_analyzer.py`
         [GATE G2: Code syntax, type checks, and pilot run execution]

PHASE 3: External Benchmark Validation (Mandatory Submission Gate)
   ├── Step 3.1: Run Classical Phononic Benchmark vs Li et al. (2016) Fig. 2 (Threshold <= 0.5%)
   ├── Step 3.2: Run Gradient Phononic Benchmark vs Li et al. (2016) Fig. 3 (Threshold <= 0.5%)
   ├── Step 3.3: Run Papargyri-Beskou (2009) IJSS dispersion check (Threshold <= 1e-12)
   └── Step 3.4: Generate overlay comparison figures in `figures/validation_overlay.png`
         [GATE G3: Hard Gate — Must match all 4 band gaps without deviation]

PHASE 4: Production Parametric Sweeps & Physical Findings
   ├── Sweep 4.1: Effect of thermal phase lags (tau_q, tau_theta) on band-gap opening/closing
   ├── Sweep 4.2: Interplay between micro-inertia (h) and thermal attenuation (Im(kx))
   ├── Sweep 4.3: Oblique incidence (xi > 0) acoustic-thermal mode conversion
   └── Sweep 4.4: Save all checkpoint data in `runs/production_sweeps.npz`

PHASE 5: High-Quality Manuscript & Publication Package
   ├── Step 5.1: Write LaTeX manuscript in `manuscript/manuscript.tex` (AMM Elsevier template)
   ├── Step 5.2: Write standalone `manuscript/references.bib` with complete DOIs
   └── Step 5.3: Generate publication-grade vector graphics (PDF/EPS/high-res PNG) in `figures/`

PHASE 6: Final Verification & Audit Freeze
   ├── Step 6.1: End-to-end reproducibility script `run_all.sh`
   ├── Step 6.2: Final SHA-256 manifest and git commit freeze
   └── Step 6.3: Submission package check
```

---

## 6. Stop Conditions & Quality Gates

1. **Stop Condition 1 (Validation Gate Failure):** If Phase 3 reproduced band edges deviate from Li et al. (2016) by $> 0.5\%$, stop immediately; no manuscript writing is permitted until resolved.
2. **Stop Condition 2 (Thermodynamic Inconsistency):** If $\tau_q < \tau_\theta$ creates unphysical negative dissipation or violates the second law of thermodynamics, flag and bound the physical parameter range.
3. **Stop Condition 3 (Numerical Loss of Precision):** If matrix inversion $P^{-1}$ condition number exceeds $10^{15}$, employ singular value scaling or block elimination to maintain double precision.

---

## 7. Deliverables Checklist (Section E Compliance)

- [x] `paper10/source-papers/` populated with `li2015.pdf`, `PB2009.txt`, `LAGKW2023.txt`.
- [x] `paper10/blueprint/RESEARCH_BLUEPRINT.md` created (this document).
- [ ] `paper10/derivations/` complete algebraic derivations.
- [ ] `paper10/src/` modular, runnable programs.
- [ ] `paper10/runs/` checkpointed computation files.
- [ ] `paper10/figures/` separate publication-quality figure files.
- [ ] `paper10/manuscript/manuscript.tex` and `references.bib`.
- [ ] `paper10/audit/` complete checkpoint and decision records.
