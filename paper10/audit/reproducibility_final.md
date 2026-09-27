# Paper 10 Reproducibility Report

**Date:** 2026-09-27  
**Master Script:** `paper10/src/reproduce_all.py`  
**Execution Environment:** Linux 6.6.137+, Python 3.11, NumPy 2.4.6, SciPy 1.17.1, Matplotlib 3.11.2  
**Status:** 100% REPRODUCIBLE (ALL CHECKS PASSED)

---

## 1. Automated Pipeline Verification

Executing:
```bash
python3 paper10/src/reproduce_all.py
```
regenerates the entire research dataset from scratch:
1. **`paper10/runs/final-paper-calculations/table_01_range_study.csv`**
   - 6 rows ($\varepsilon_\lambda \in [0.0, 0.05]$).
   - Baseline singular condition number $\operatorname{cond}(F) = 8.7094 \times 10^{16}$ recovered.
   - Fluence-regularised condition number $\operatorname{cond}(F) = 7.3595 \times 10^3$ at $\varepsilon_\lambda = 0.05$ matched to within $< 0.1$.
2. **`paper10/runs/final-paper-calculations/table_02_fourier_limit_validation.csv`**
   - 4 rows ($\varepsilon_\lambda \in [0.0, 0.01, 0.02, 0.05]$).
   - Maximum point-wise discrepancy $E_\infty \le 2.3214 \times 10^{-9}$ against independent FVM Radau IIA reference solver.
3. **`paper10/runs/final-paper-calculations/table_03_mesh_convergence.csv`**
   - 4 rows ($N_x \in [100, 200, 400]$ vs fine grid $N_x = 800$).
   - Observed spatial convergence orders $p \approx 2.07 - 2.32$ verified across all fluence levels.
4. **`paper10/figures/`**
   - `Fig01_thermograms.pdf` (vector) and `Fig01_thermograms.png` (high-res raster).
   - `Fig02_sensitivity_colinearity.pdf` (vector) and `Fig02_sensitivity_colinearity.png` (high-res raster).

---

## 2. Integrity of the Reproducibility Chain

Every numerical value reported in the study follows the unbroken chain:
$$\boxed{\text{Physical equation}} \;\longrightarrow\; \boxed{\text{Source script in } \texttt{paper10/src/}} \;\longrightarrow\; \boxed{\text{Raw data in } \texttt{paper10/runs/}} \;\longrightarrow\; \boxed{\text{Vector figures in } \texttt{paper10/figures/}} \;\longrightarrow\; \boxed{\text{Audit logs in } \texttt{paper10/audit/}}$$
No value is copied from memory, chat history, or undocumented manual prototypes.
