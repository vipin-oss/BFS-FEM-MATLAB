# PHASE 2 REPRODUCIBILITY RECORD

### Project: `paper10`
### Document: `paper10/validation/PHASE2_REPRODUCIBILITY.md`
**Date:** 2026-09-26  
**Governing Baseline:** Commit `e9ca21f`  
**Phase 2 Target:** Minimal Solver Implementation + Conservative Benchmark Gate  
**Status:** 100% REPRODUCIBLE FROM CLEAN CHECKOUT

---

## 1. System & Runtime Environment

| Attribute | Value / Specification |
|---|---|
| Repository | `vipin-oss/BFS-FEM-MATLAB` |
| Working Branch | `arena/01a0dcde-bfs-fem-matlab` |
| Operating System | Linux (Ubuntu 24.04 LTS / x86_64) |
| Language & Runtime | Python 3.11.14 |
| Core Packages | `numpy 2.4.6`, `scipy 1.17.1`, `matplotlib 3.11.2` |
| Arithmetic Precision | IEEE 754 double precision (`float64`, `complex128`) |
| Random Seeds | None (Deterministic algorithms only; zero stochastic components) |

---

## 2. Solver Parameters & Convergence Tolerances

- **Brent root finder tolerance:** `xtol = 1e-12`, `rtol = 1e-12`.
- **Equilibration method:** Dual $L_2$ row-scaling followed by column-scaling:
  $$P_{\text{equil}} = D_{\text{row}}^{-1} P D_{\text{col}}^{-1}, \quad D_{\text{row}} = \text{diag}(\|P_{i,:}\|_2), \quad D_{\text{col}} = \text{diag}(\|P_{:,j}\|_2)$$
- **Condition number monitoring:** Scaled threshold $\kappa(P_{\text{equil}}) < 10^{14}$.
- **Bloch eigenvalue branch convention:** Standard principal branch of complex logarithm $\text{Ln}(\lambda)$:
  $$k_x a = -i \ln \lambda = \text{Arg}(\lambda) - i \ln |\lambda|$$
  $k_r a = \text{Re}(k_x a)$ mapped to the first Brillouin zone $[0, \pi]$; $k_i a = |\text{Im}(k_x a)| \ge 0$.

---

## 3. Step-by-Step Reproduction Procedure

From a clean workspace checkout of branch `arena/01a0dcde-bfs-fem-matlab`:

### Step 1: Run Unit Tests
```bash
python3 paper10/tests/test_parameters.py
python3 paper10/tests/test_antiplane.py
python3 paper10/tests/test_coupled10.py
```
*Expected Result:* All tests report `PASS` with zero assertions tripped.

### Step 2: Run External Benchmarks (Gates G2-B & G2-C)
```bash
python3 paper10/validation/run_benchmarks.py
```
*Expected Result:*
- Gate G2-C (Papargyri-Beskou): Maximum relative error $= 3.87\times 10^{-16} \le 0.5\%$.
- Gate G2-B (Classical Limit): Asymptotic error $= 1.33\times 10^{-12} \le 0.5\%$.
- Output files created:
  - `paper10/validation/benchmark_papargyri_beskou_results.csv`
  - `paper10/validation/benchmark_papargyri_beskou_results.json`
  - `paper10/figures/fig1_papargyri_beskou_benchmark.png`
  - `paper10/figures/fig2_benchmark_relative_error.png`
  - `paper10/figures/fig3_classical_limit.png`

### Step 3: Run Periodic Unit-Cell Pilot (Gate G2-D)
```bash
python3 paper10/validation/run_periodic_pilot.py
```
*Expected Result:*
- Gate G2-D: Reports 252 pass-band points, 2 Bragg gaps, $\lvert\det(T_{\text{cell}})-1\rvert = 2.66\times 10^{-13}$.
- Output files created:
  - `paper10/validation/periodic_pilot_results.json`
  - `paper10/figures/fig4_two_layer_bloch.png`
