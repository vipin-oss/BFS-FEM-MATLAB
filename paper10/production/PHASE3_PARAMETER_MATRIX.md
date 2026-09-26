# PHASE 3 AUTHORITATIVE PRODUCTION PARAMETER MATRIX

### Project: `paper10`
### Document: `paper10/production/PHASE3_PARAMETER_MATRIX.md`
**Date:** 2026-09-26  
**Governing Baseline:** `RESEARCH_BLUEPRINT.md` (v1.2 locked at commit `1ed2d54`)  
**Status:** FULLY LOCKED & TRACEABLE (Zero Invented Data)

---

## 1. Overview & Classification Hierarchy

The production parameter matrix for Paper 10 is derived directly and without modification from Section 6 and Section 7 (Phase 4) of the locked Research Blueprint (`paper10/blueprint/RESEARCH_BLUEPRINT.md`).

All parameters are categorized into four distinct functional tiers:
1. **Fixed Baseline Parameters:** Core material constants, geometric period, and ambient conditions that remain invariant across standard simulations.
2. **Primary Sweep Parameters:** Parameters explicitly designated by the Blueprint for systematic parametric sweeps (phase lags $\tau_q, \tau_\theta$, micro-inertia $h$, and layer thickness ratio $\eta$).
3. **Secondary Study Parameters:** Parameters utilized for specific physical sensitivity investigations (oblique incidence $\xi$, micro-stiffness scale $g$, identical-layer limit $A = B$).
4. **Validation / Benchmark Parameters:** Archival values reserved strictly for independent limiting-case validation gates (Papargyri-Beskou 2009, Li et al. 2016).

---

## 2. Comprehensive Master Parameter Table

| Parameter | Symbol | Baseline | Sweep / Study Values | Units | Classification | Purpose | Blueprint Source |
|---|:---:|---:|:---|:---:|:---:|---|---|
| **Lattice Period** | $a$ | $0.01$ | Fixed ($0.01$) | $\text{m}$ | Fixed | Global geometric unit-cell period | Blueprint §6 |
| **Layer A Thickness Ratio** | $\eta = a_1/a$ | $0.5$ | $[0.2, 0.5, 0.8]$ | Dimensionless | Primary | Geometric asymmetry & Bragg tuning | Blueprint §6, §7 |
| **Layer A Thickness** | $a_1$ | $0.005$ | $\eta \cdot a$ | $\text{m}$ | Derived | Thickness of Layer A (Epoxy) | Blueprint §6 |
| **Layer B Thickness** | $a_2$ | $0.005$ | $(1-\eta) \cdot a$ | $\text{m}$ | Derived | Thickness of Layer B (Al) | Blueprint §6 |
| **Layer A Density** | $\rho_1$ | $1180.0$ | Fixed ($1180.0$) | $\text{kg/m}^3$ | Fixed | Mass density of Layer A (Epoxy) | Blueprint §6 (Li 2016) |
| **Layer A Shear Speed** | $V_{s1}$ | $1160.0$ | Fixed ($1160.0$) | $\text{m/s}$ | Fixed | Classical shear wave speed in Layer A | Blueprint §6 (Li 2016) |
| **Layer A Long. Speed** | $V_{p1}$ | $2830.0$ | Fixed ($2830.0$) | $\text{m/s}$ | Fixed | Classical longitudinal speed in Layer A | Blueprint §6 (Li 2016) |
| **Layer A Shear Modulus** | $\mu_1$ | $1.5878 \times 10^9$ | $\rho_1 V_{s1}^2$ | $\text{Pa}$ | Derived | Second Lamé parameter of Layer A | Blueprint §6 |
| **Layer A First Lamé** | $\lambda_1$ | $6.2748 \times 10^9$ | $\rho_1 V_{p1}^2 - 2\mu_1$ | $\text{Pa}$ | Derived | First Lamé parameter of Layer A | Blueprint §6 |
| **Layer A Micro-Stiffness**| $c_1 = g_1^2$| $0.25 a^2$ | $[0.01, 0.25, 0.64] a^2$ | $\text{m}^2$ | Secondary | Dipolar gradient strain energy scale | Blueprint §6 ($\bar{c}_1=0.5$) |
| **Layer A Micro-Inertia**  | $d_1 = \sqrt{3}h_1$ | $0.5 a$ | $[0.1, 0.5, 1.0] a$ | $\text{m}$ | Primary | Micro-inertia kinetic energy scale | Blueprint §6, §7 ($\bar{d}_1=0.5$) |
| **Layer B Density** | $\rho_2$ | $185.614$ | $0.1573 \rho_1$ | $\text{kg/m}^3$ | Fixed | Normalized mass density of Layer B | Blueprint §6 (ratio 0.1573) |
| **Layer B Shear Speed** | $V_{s2}$ | $689.852$ | $0.5947 V_{s1}$ | $\text{m/s}$ | Fixed | Transverse wave speed in Layer B | Blueprint §6 (ratio 0.5947) |
| **Layer B Long. Speed** | $V_{p2}$ | $1590.46$ | $0.562 V_{p1}$ | $\text{m/s}$ | Fixed | Dilatational wave speed in Layer B | Blueprint §6 (ratio 0.562) |
| **Layer B Shear Modulus** | $\mu_2$ | $8.8333 \times 10^7$ | $\rho_2 V_{s2}^2$ | $\text{Pa}$ | Derived | Second Lamé parameter of Layer B | Blueprint §6 |
| **Layer B First Lamé** | $\lambda_2$ | $2.9285 \times 10^8$ | $\rho_2 V_{p2}^2 - 2\mu_2$ | $\text{Pa}$ | Derived | First Lamé parameter of Layer B | Blueprint §6 |
| **Layer B Micro-Stiffness**| $c_2 = g_2^2$| $c_1 / 0.77$ | Ratio $\bar{c}=0.77$ | $\text{m}^2$ | Fixed | Modulus ratio locked to Li et al. | Blueprint §6 |
| **Layer B Micro-Inertia**  | $d_2 = \sqrt{3}h_2$ | $d_1 / 2.0$ | Ratio $\bar{d}=2.0$ | $\text{m}$ | Fixed | Micro-inertia ratio locked to Li et al. | Blueprint §6 |
| **Layer A Conductivity**   | $k_1$ | $0.2$ | Fixed ($0.2$) | $\text{W/(m}\cdot\text{K)}$ | Fixed | Thermal conductivity of Layer A | Blueprint §6 (Li 2023) |
| **Layer B Conductivity**   | $k_2$ | $205.0$ | Fixed ($205.0$) | $\text{W/(m}\cdot\text{K)}$ | Fixed | Thermal conductivity of Layer B | Blueprint §6 (Li 2023) |
| **Layer A Specific Heat**  | $c_{v1}$ | $1000.0$ | Fixed ($1000.0$) | $\text{J/(kg}\cdot\text{K)}$ | Fixed | Specific heat capacity of Layer A | Blueprint §6 (Li 2023) |
| **Layer B Specific Heat**  | $c_{v2}$ | $900.0$ | Fixed ($900.0$) | $\text{J/(kg}\cdot\text{K)}$ | Fixed | Specific heat capacity of Layer B | Blueprint §6 (Li 2023) |
| **Layer A Thermal Expansion**| $\alpha_{t1}$ | $6.0 \times 10^{-5}$ | Fixed ($6.0 \times 10^{-5}$) | $\text{K}^{-1}$ | Fixed | Thermal expansion coefficient Layer A | Blueprint §6 (Li 2023) |
| **Layer B Thermal Expansion**| $\alpha_{t2}$ | $2.3 \times 10^{-5}$ | Fixed ($2.3 \times 10^{-5}$) | $\text{K}^{-1}$ | Fixed | Thermal expansion coefficient Layer B | Blueprint §6 (Li 2023) |
| **Reference Temperature**  | $T_0$ | $300.0$ | Fixed ($300.0$) | $\text{K}$ | Fixed | Ambient absolute temperature | Blueprint §6 |
| **Heat Flux Phase Lag**    | $\tau_q$ | $1.0 \times 10^{-11}$| $[10^{-12}, 10^{-11}, 10^{-9}]$| $\text{s}$ | Primary | Non-Fourier heat flux relaxation lag | Blueprint §6, §7 |
| **Temp. Grad. Phase Lag**  | $\tau_\theta$ | $2.0 \times 10^{-12}$| $[10^{-13}, 2\times 10^{-12}, 10^{-10}]$| $\text{s}$ | Primary | Temperature gradient retardation lag | Blueprint §6, §7 |
| **Thermoelastic Coupling** | $\beta_j$ | Active | $\beta_j \to 0$ | $\text{Pa/K}$ | Secondary | Uncoupled mechanical conservative limit | Blueprint §2, §3 |
| **Apparent Wavenumber**    | $\xi$ | $0.0$ | $[0.0, 50.0, 100.0]$ | $\text{m}^{-1}$ | Secondary | Oblique interface wave propagation | Blueprint §4, §6 |
| **Normalized Frequency**   | $\Omega$ | $[0.05, 1.80]$ | Grid sampling | Dimensionless | Sweep | $\Omega = \omega a / (2\pi v_m)$ | Blueprint §4, §6 |

---

## 3. Traceability Verification & Open Items Check

- **Missing Parameters:** NONE.
- **Unspecified Ranges:** NONE.
- **Ambiguous Units:** NONE (All SI derived: $\text{m}, \text{s}, \text{kg}, \text{Pa}, \text{W}, \text{K}$).
- **Status of Parameter Matrix:** **100% LOCKED AND AUDITABLE**.
