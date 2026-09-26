# PHASE 2 BENCHMARK & VALIDATION GATE REPORT

### Project: `paper10`
### Document: `paper10/validation/PHASE2_BENCHMARK.md`
**Date:** 2026-09-26  
**Governing Baseline:** Commit `e9ca21f` (Phase 1 Final Locked Baseline)  
**Execution Stage:** Phase 2 (Minimal Solver Implementation & Conservative Benchmark Gate)  
**Status:** ALL GATES PASSED (Phase 3 production strictly held)

---

## 1. Executive Summary of Validation Gates

| Gate ID | Description | Acceptance Criterion | Result | Status |
|:---:|---|---|:---:|:---:|
| **G2-A** | **Implementation Integrity** | State dimensions exact ($4\times 4$ and $10\times 10$), root counts exact (4 shear, 6 long-th, 10 total), square modal matrices, finite entries. | $4/4$ and $10/10$ states; exact root counts verified; modal-analytical diff $= 1.34\times 10^{-14}$. | **PASS** |
| **G2-B** | **Classical Limit** | Asymptotic recovery of classical dispersion ($\omega = V_s k$) as $c, d \to 0$ with relative error $\le 0.5\%$. | Max asymptotic relative error $= 1.33\times 10^{-12}$ at $10^{-8}\,\text{m}$. | **PASS** |
| **G2-C** | **Papargyri-Beskou Benchmark** | Exact reproduction of Papargyri-Beskou et al. (2009, IJSS Eq. 28) with maximum relative error $\le 0.5\%$. | Max relative error $= 3.87\times 10^{-16}$ (machine precision). | **PASS** |
| **G2-D** | **Periodic Conservative Pilot** | Pass-band branches and material-contrast Bragg band gaps reproduced in two-layer periodic cell; $\det(T_{\text{cell}}) \equiv 1$. | 252 pass-band points, 2 Bragg gaps identified; $\lvert\det(T_{\text{cell}})-1\rvert = 2.66\times 10^{-13}$. | **PASS** |
| **G2-E** | **DPL Implementation Sanity** | Phase lags $\tau_q, \tau_\theta$ active, complex wavenumbers and attenuation produced, no solver crashes, stable Bloch modes. | Complex $k_{\text{eff}}$ verified; attenuation $k_i > 0$ confirmed; 10 Bloch multipliers extracted without crash. | **PASS** |

---

## 2. Gate G2-C: Papargyri-Beskou (2009) Gradient Elasticity Benchmark

### 2.1 Benchmark Formulation
Papargyri-Beskou, Polyzos & Beskos (2009, *Int. J. Solids Struct.* 46(21), 3751–3758, Eq. 28) derived the closed-form bulk wave dispersion relation for 1D dipolar gradient elasticity with micro-inertia:
$$\omega_{\text{PB}}(k) = V_s k \sqrt{\frac{1 + c k^2}{1 + (d^2/3) k^2}}$$
where $c = g^2$ is the micro-stiffness length-scale squared and $d^2/3 = h^2$ is the micro-inertia length-scale squared.

### 2.2 Numerical Test Setup
- Solid properties: $\rho = 2000\,\text{kg/m}^3$, $V_s = 1000\,\text{m/s}$, $\mu = 2.0\times 10^9\,\text{Pa}$, $g = 0.001\,\text{m}$, $h = 0.0015\,\text{m}$.
- Conservative mechanical limit: $\beta \equiv 0$, uncoupled from temperature.
- Grid: 50 wavenumber stations across $k \in [10.0, 2000.0]\,\text{m}^{-1}$.
- Independent numerical solve: Secular root solver matching transfer-matrix Bloch eigenvalue $\lambda = e^{i k a}$.

### 2.3 Numerical Evidence
- **Maximum relative dispersion error:** $3.87\times 10^{-16}$ (target $\le 0.5\%$).
- **Maximum eigenvalue residual:** $9.86\times 10^{-12}$.
- **Worst scaled modal condition number:** $\kappa(P_{\text{scaled}}) = 2.41$.
- **Worst symplecticity determinant error:** $\lvert\det(T) - 1\rvert = 2.50\times 10^{-8}$.
- **Machine-readable results:**
  - CSV: `paper10/validation/benchmark_papargyri_beskou_results.csv`
  - JSON: `paper10/validation/benchmark_papargyri_beskou_results.json`
- **Diagnostic Figures:**
  - Figure 1: `paper10/figures/fig1_papargyri_beskou_benchmark.png` (exact visual overlay of analytical vs numerical dispersion).
  - Figure 2: `paper10/figures/fig2_benchmark_relative_error.png` (error curve pinned at machine epsilon $< 10^{-15}$).

---

## 3. Gate G2-B: Classical Acoustic Limit ($c, d \to 0$)

### 3.1 Benchmark Formulation
When microstructural parameters $c \to 0$ and $d \to 0$, gradient elasticity collapses asymptotically to classical Cauchy elastodynamics:
$$\omega_{\text{classical}}(k) = V_s k$$

### 3.2 Numerical Evidence
Testing microstructural length scales from $10^{-4}\,\text{m}$ down to $10^{-8}\,\text{m}$ at $k = 200\,\text{m}^{-1}$:
- Scale $10^{-4}\,\text{m}$: Relative error $= 1.33\times 10^{-4}$ ($0.013\%$).
- Scale $10^{-5}\,\text{m}$: Relative error $= 1.33\times 10^{-6}$.
- Scale $10^{-6}\,\text{m}$: Relative error $= 1.33\times 10^{-8}$.
- Scale $10^{-7}\,\text{m}$: Relative error $= 1.33\times 10^{-10}$.
- Scale $10^{-8}\,\text{m}$: Relative error $= 1.33\times 10^{-12}$.
- **Asymptotic error at $10^{-8}\,\text{m}$:** $1.33\times 10^{-12} \ll 0.5\%$.
- **Diagnostic Figure:** Figure 3: `paper10/figures/fig3_classical_limit.png` (power-law convergence with slope 2 in log-log scale).

---

## 4. Gate G2-D: Two-Layer Periodic Conservative Pilot

### 4.1 Benchmark Setup
A periodic bi-layer phononic crystal matching the locked parameters of Li, Wei & Zhou (2016, *Acta Mechanica* 227(4), Fig. 3):
- Layer A: $a_1 = 0.5\,\text{m}$, $\rho_1 = 1.0$, $V_{s1} = 1.0$, $c_1 = 0.25$, $d_1 = 0.5$.
- Layer B: $a_2 = 0.5\,\text{m}$, $\rho_2 = 0.1573$, $V_{s2} = 0.5947$, $c_2 = c_1 / 0.77$, $d_2 = d_1 / 2.0$.
- Period $a = a_1 + a_2 = 1.0\,\text{m}$.
- Circular frequency swept across $\Omega = \omega a / (2\pi v_m) \in [0.01, 1.80]$.

### 4.2 Numerical Evidence
- Total pass-band points computed: 252 points.
- Material-contrast Bragg band gaps identified:
  - **Gap 1:** $\Omega \in [0.6700, 0.6900]$ (Width $= 0.0200$).
  - **Gap 2:** $\Omega \in [1.3000, 1.8000]$ (Width $= 0.5000$).
- **Symplectic determinant check:** $\lvert\det(T_{\text{cell}}) - 1\rvert = 2.66\times 10^{-13}$.
- **Worst unit-cell condition number:** $\kappa(T_{\text{cell}}) = 2.42\times 10^5$.
- **Diagnostic Figure:** Figure 4: `paper10/figures/fig4_two_layer_bloch.png` (real pass bands and imaginary evanescent attenuation branches).

---

## 5. Gate G2-E: Full 10-State DPL Implementation Sanity

### 5.1 Test Setup
- Silicon-like microstructured solid with active DPL thermal conduction:
  - $\rho = 2330\,\text{kg/m}^3$, $\mu = 4.0\times 10^{10}\,\text{Pa}$, $\lambda = 6.0\times 10^{10}\,\text{Pa}$, $g = 10\,\mu\text{m}$, $h = 15\,\mu\text{m}$.
  - $k = 148\,\text{W/(m}\cdot\text{K)}$, $c_v = 700\,\text{J/(kg}\cdot\text{K)}$, $\alpha_t = 2.6\times 10^{-6}\,\text{K}^{-1}$, $T_0 = 300\,\text{K}$.
  - Phase lags: $\tau_q = 10\,\text{ps}$, $\tau_\theta = 2\,\text{ps}$.
  - Circular frequency: $\omega = 1.0\,\text{MHz}$.

### 5.2 Numerical Evidence
- Effective DPL thermal conductivity: $k_{\text{eff}} = 148.0 + 1.184\times 10^{-3} i\,\text{W/(m}\cdot\text{K)}$ (complex as required).
- Root counts: Exactly 4 shear roots and 6 coupled longitudinal-thermal roots (total = 10).
- Attenuation: Non-zero imaginary wavenumber parts ($k_i > 0$) confirm active thermoelastic dissipation.
- Condition numbers:
  - Unscaled raw modal matrix: $\kappa(P_{\text{raw}}) = 3.03\times 10^{22}$ (due to SI dimensional spans from $10^{-6}\,\text{m}$ to $10^{11}\,\text{Pa}$).
  - Canonical row- and column-equilibrated matrix: $\kappa(P_{\text{equil}}) = 3.73\times 10^5$.
  - Transfer matrix condition: $\kappa(T_{\text{equil}}) = 2.37\times 10^1$.
  - Periodic unit-cell condition: $\kappa(T_{\text{cell}}) = 2.89\times 10^3$.
- Bloch multipliers: All 10 complex eigenvalues extracted cleanly without numerical failures.
