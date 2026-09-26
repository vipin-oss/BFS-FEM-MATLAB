# PHASE 1 LOCK CHECK — PRE-DERIVATION AUDIT RECORD
### Project: `paper10`
### Governing Blueprint: `RESEARCH_BLUEPRINT.md` (v1.2 — FINAL)
### Locked Blueprint Git Commit: `1ed2d5436f47ca923b0763bce281acf2e9988fe0`
**Date:** 2026-09-26  
**Auditor:** Mathematical Derivation Engine (Arena Agent)  
**Execution Stage:** Phase 1 (Analytical Derivation)

---

## 1. Governance & Configuration Lock

| Parameter / Item | Locked Specification | Verification Status |
|---|---|---|
| Blueprint Version | v1.2 (Final Pre-Execution Calibration) | **LOCKED** (matches file in `paper10/blueprint/`) |
| Git Commit Hash | `1ed2d54` | **LOCKED & VERIFIED** via `git log` |
| Primary Target Journal | *Applied Mathematical Modelling* (Elsevier, Q1) | **LOCKED** |
| Alternate Targets | *Composite Structures* / *IJSS* (Elsevier, Q1) | **LOCKED** |
| Validation Benchmark | Li, Wei & Zhou (2016), *Acta Mechanica* 227(4) | **LOCKED** (`paper10/source-papers/li2015.pdf`) |
| Secondary Benchmark | Papargyri-Beskou et al. (2009), *IJSS* 46(21) | **LOCKED** (`paper10/source-papers/PB2009.txt`) |

---

## 2. Mathematical System Specifications

### 2.1 Governing Equations Locked
1. **Mindlin Form-II Dipolar Gradient Elastodynamics with Thermal Coupling:**
   $$\mu (1 - c \nabla^2) \nabla^2 \mathbf{u} + (\lambda + \mu)(1 - c \nabla^2)\nabla(\nabla \cdot \mathbf{u}) - \beta \nabla \theta = \rho \ddot{\mathbf{u}} - \frac{\rho d^2}{3}\nabla^2 \ddot{\mathbf{u}}$$
2. **Dual-Phase-Lag (DPL) Energy Equation:**
   $$k \left( 1 + \tau_\theta \frac{\partial}{\partial t} \right) \nabla^2 \theta = \left( 1 + \tau_q \frac{\partial}{\partial t} \right) \left[ \rho c_v \frac{\partial \theta}{\partial t} + T_0 \beta \frac{\partial}{\partial t}(\nabla \cdot \mathbf{u}) \right]$$

### 2.2 Harmonic & Coordinate Conventions
- Time Harmonic Convention: $\exp(-i \omega t)$, yielding:
  $$\frac{\partial}{\partial t} \to -i \omega, \quad \frac{\partial^2}{\partial t^2} \to -\omega^2$$
- Spatial Coordinate Convention:
  - Wave propagation along the $x$-axis (normal to layering).
  - Layer interface planes lie in the $y-z$ plane.
  - In-plane coordinates: $(x, y)$, with apparent wavenumber $\xi$ along $y$: $\exp(i \xi y)$.
  - Normal incidence: $\xi = 0$.
- Unit Cell Layering:
  - Layer A: $x \in [0, a_1]$, thickness $a_1$.
  - Layer B: $x \in [a_1, a_1+a_2]$, thickness $a_2$.
  - Single cell length: $a = a_1 + a_2$.
  - Left boundary of cell: $x = 0$; Right boundary of cell: $x = a$.
  - Matrix multiplication order: $V(a) = T_B T_A V(0) \implies T_{\text{cell}} = T_B T_A$.
- Bloch-Floquet Periodicity:
  $$V(x + a) = \lambda V(x), \quad \lambda = e^{i k_x a}, \quad k_x = k_r + i k_i$$

### 2.3 State Vector Specifications
- **In-Plane Coupled State Vector ($10 \times 1$):**
  $$V_{\text{in}} = [u_x, u_y, u_{x,x}, u_{y,x}, \theta, P_x, P_y, R_x, R_y, q_x]^T$$
- **Anti-Plane Decoupled State Vector ($4 \times 4$):**
  $$V_{\text{anti}} = [u_z, u_{z,x}, P_z, R_z]^T$$

---

## 3. Parameter Lock & Provenance Verification

| Parameter | Symbol | Source Provenance | Value / Formula | Lock Status |
|---|---|---|---|---|
| Micro-stiffness scale | $c = g^2$ | Li et al. (2016) Eq. (3) | Layer A: $0.25 a^2$, Layer B: $c_1/0.77$ | **LOCKED** |
| Micro-inertia scale | $d = \sqrt{3} h$ | Li et al. (2016) Eq. (5) | Layer A: $0.5 a$, Layer B: $d_1/2.0$ | **LOCKED** |
| Lamé constants | $\lambda, \mu$ | Li et al. (2016) Section 6 | Derived from $V_p, V_s, \rho$ | **LOCKED** |
| Thermoelastic coupling | $\beta = (3\lambda+2\mu)\alpha_t$ | Standard thermoelasticity | $\beta_1, \beta_2$ from $\alpha_{t1}, \alpha_{t2}$ | **LOCKED** |
| Thermal conductivity | $k$ | Li, Askes et al. (2023) | $k_1 = 0.2, k_2 = 205 \, \text{W/(m}\cdot\text{K)}$ | **LOCKED** |
| Specific heat | $c_v$ | Li, Askes et al. (2023) | $c_{v1} = 1000, c_{v2} = 900 \, \text{J/(kg}\cdot\text{K)}$ | **LOCKED** |
| Thermal expansion | $\alpha_t$ | Li, Askes et al. (2023) | $\alpha_{t1} = 6.0\times 10^{-5}, \alpha_{t2} = 2.3\times 10^{-5} \, \text{K}^{-1}$ | **LOCKED** |
| Reference temperature | $T_0$ | Standard ambient | $300 \, \text{K}$ | **LOCKED** |
| Heat flux phase lag | $\tau_q$ | DPL model | Bounded range $[10^{-12}, 10^{-9}] \, \text{s}$ | **LOCKED** |
| Temp gradient phase lag | $\tau_\theta$ | DPL model | Bounded range $[10^{-13}, 10^{-10}] \, \text{s}$ | **LOCKED** |

---

## 4. Open-Item Check Prior to Derivation

- Genuinely unspecified parameters: **NONE**.
- Ambiguous governing equations: **NONE**.
- Interface conditions missing: **NONE** (All 10 conditions for in-plane and 4 conditions for anti-plane are matched).
- Blocker status: **CLEARED TO DERIVE**.
