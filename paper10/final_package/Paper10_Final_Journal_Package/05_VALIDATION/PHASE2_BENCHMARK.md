# PHASE 2 BENCHMARK & VALIDATION GATE REPORT (AUTHORITATIVE)

### Project: `paper10`
### Document: `paper10/validation/PHASE2_BENCHMARK.md`
**Date:** 2026-09-26  
**Governing Baseline:** Commit `e9ca21f` (Phase 1 Final Locked Baseline)  
**Execution Stage:** Phase 2 (Authoritative Independent TMM Benchmark & Validation Gates)  
**Status:** ALL GATES INDEPENDENTLY PASSED (Phase 3 production strictly held)

---

## 1. Executive Summary of Validation Gates

| Gate ID | Description | Acceptance Criterion | Numerical Result | Status |
|:---:|---|---|:---:|:---:|
| **G2-A** | **Implementation Integrity** | State dimensions exact ($4\times 4$ and $10\times 10$), root counts exact (4 shear, 6 long-th, 10 total), square modal matrices, finite entries. | $4/4$ and $10/10$ states; exact root counts verified; modal-analytical diff $= 1.34\times 10^{-14}$. | **PASS** |
| **G2-B** | **Classical Limit** | Asymptotic recovery of classical dispersion ($\omega = V_s k$) as $c, d \to 0$ with relative error $\le 0.5\%$. | Max asymptotic relative error $= 1.52\times 10^{-11}$ at $10^{-8}\,\text{m}$. | **PASS** |
| **G2-C** | **Authoritative Independent Papargyri-Beskou Benchmark** | Independent solution of Transfer Matrix secular condition $\det[T(\omega, a) - e^{i k a} I] = 0$ reproducing Papargyri-Beskou et al. (2009, IJSS Eq. 28) with relative error $\le 0.5\%$. | Max independent relative error $= \mathbf{2.45\times 10^{-15}}$ across 50 points; secular residual $= 1.90\times 10^{-14}$; 0 failures. | **PASS** |
| **G2-D** | **Periodic Conservative Pilot** | Pass-band branches and material-contrast Bragg band gaps reproduced in two-layer periodic cell; $\det(T_{\text{cell}}) \equiv 1$. | 252 pass-band points, 2 Bragg gaps identified; $\lvert\det(T_{\text{cell}})-1\rvert = 2.66\times 10^{-13}$. | **PASS** |
| **G2-E** | **DPL Implementation Sanity** | Phase lags $\tau_q, \tau_\theta$ active, complex wavenumbers and attenuation produced, no solver crashes, stable Bloch modes. | Complex $k_{\text{eff}}$ verified; attenuation $k_i > 0$ confirmed; 10 Bloch multipliers extracted without crash. | **PASS** |

---

## 2. Gate G2-C: Authoritative Independent Benchmark vs. Internal Consistency Check

To ensure uncompromising scientific rigor, Phase 2 strictly distinguishes between:
1. **Authoritative External Benchmark Validation:** Directly solving the Transfer Matrix secular determinant $\det[T(\omega, a) - e^{i k a} I] = 0$ using an agnostic acoustic search bracket $[0.5 V_s k, 2.0 V_s k]$ that has zero knowledge of the Papargyri-Beskou formula or microstructural scale parameters.
2. **Internal Characteristic-Root Consistency Check:** Inverting the scalar root equation $\beta_s(\omega) - k = 0$ using a reference-centered search bracket.

### 2.1 Authoritative External Benchmark Results (Independent TMM Secular Solve)
- **Objective Function:** $f(\omega) = \det[T(\omega, a) - e^{i k a} I] = 0$.
- **Bracket:** $[0.5 V_s k, 2.0 V_s k]$ (agnostic acoustic bracket based purely on classical speed $V_s$ and wavenumber $k$).
- **Number of wavenumber stations:** 50 points ($k \in [10.0, 2000.0]\,\text{m}^{-1}$).
- **Maximum Independent Relative Error:** $\mathbf{2.45 \times 10^{-15}}$ ($\le 0.5\%$).
- **Maximum Secular Residual:** $1.90 \times 10^{-14}$.
- **Convergence Failures:** 0.
- **Authoritative Gate G2-C Status:** **PASS**.

### 2.2 Secondary Diagnostic: Internal Scalar Consistency Check
- **Objective Function:** $f_{\text{scalar}}(\omega) = \beta_s(\omega) - k = 0$.
- **Bracket:** $[0.8 \omega_{\text{PB}}, 1.2 \omega_{\text{PB}}]$.
- **Maximum Scalar Consistency Error:** $3.87 \times 10^{-16}$.
- **Purpose:** Internal algebraic verification confirming that the state-space characteristic root $\beta_s(\omega)$ matches the analytical bulk dispersion relation to machine precision.

### 2.3 Diagnostic Figures & Artifacts
- **Figure 1:** `paper10/figures/fig1_papargyri_beskou_benchmark.png` (Authoritative independent TMM secular solution vs. analytical reference).
- **Figure 2:** `paper10/figures/fig2_benchmark_relative_error.png` (Independent relative error curve pinned at $10^{-15}$ across the entire spectrum).
- **Machine-Readable Result Files:**
  - `paper10/validation/benchmark_papargyri_beskou_results.csv`
  - `paper10/validation/benchmark_papargyri_beskou_results.json`

---

## 3. Gate G2-B: Classical Acoustic Limit ($c, d \to 0$)

### 3.1 Benchmark Formulation & Results
As microstructural length scales $c, d \to 0$, the transfer-matrix secular solve converges to classical Cauchy elastodynamics $\omega = V_s k$:
- Scale $10^{-4}\,\text{m}$: Relative error $= 1.33 \times 10^{-4}$ ($0.013\%$).
- Scale $10^{-5}\,\text{m}$: Relative error $= 1.33 \times 10^{-6}$.
- Scale $10^{-6}\,\text{m}$: Relative error $= 1.33 \times 10^{-8}$.
- Scale $10^{-7}\,\text{m}$: Relative error $= 1.16 \times 10^{-10}$.
- Scale $10^{-8}\,\text{m}$: Relative error $= 1.52 \times 10^{-11}$.
- **Asymptotic Error at $10^{-8}\,\text{m}$:** $1.52 \times 10^{-11} \ll 0.5\%$.
- **Gate G2-B Status:** **PASS**.
- **Figure 3:** `paper10/figures/fig3_classical_limit.png` (asymptotic power-law convergence).

---

## 4. Gate G2-D: Two-Layer Periodic Conservative Pilot

- Bi-layer phononic crystal matching Li, Wei & Zhou (2016, *Acta Mechanica* 227(4), Fig. 3).
- 252 pass-band points computed; 2 material-contrast Bragg band gaps identified:
  - Bragg Gap 1: $\Omega \in [0.6700, 0.6900]$ (Width $= 0.0200$).
  - Bragg Gap 2: $\Omega \in [1.3000, 1.8000]$ (Width $= 0.5000$).
- **Unit-Cell Symplectic Determinant Error:** $\lvert\det(T_{\text{cell}}) - 1\rvert = 2.66 \times 10^{-13}$.
- **Gate G2-D Status:** **PASS**.
- **Figure 4:** `paper10/figures/fig4_two_layer_bloch.png`.

---

## 5. Gate G2-E: Full 10-State DPL Implementation Sanity & Sign Convention

### 5.1 Sign Convention vs. Attenuation Magnitude Diagnostic
- **Space-Time Harmonic Convention:** $\exp\left[ i(k_x x - \omega t) \right] = \exp\left[ i(k_r x - \omega t) \right] \exp(-k_i x)$ where $k_x = k_r + i k_i$.
- **Physical Directional Attenuation:**
  - Forward-decaying wave ($k_r > 0$): $\exp(-k_i x) \to 0$ as $x \to +\infty \iff \mathbf{k_i > 0}$ ($|\lambda| \le 1$).
  - Backward-decaying wave ($k_r < 0$): $\exp(-k_i x) \to 0$ as $x \to -\infty \iff \mathbf{k_i < 0}$ ($|\lambda| \ge 1$).
- **Solver Reporting Convention:**
  - Signed complex wavenumber: $k_x a = k_r a + i k_i a$ (recorded in `ki_signed`).
  - Spatial attenuation magnitude diagnostic: $\alpha a = |k_i a|$ (recorded in `alpha_a`).
- **Gate G2-E Status:** **PASS**.
