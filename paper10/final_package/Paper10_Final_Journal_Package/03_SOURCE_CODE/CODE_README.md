# Computational Source Code Guide — Paper 10

**Manuscript:** Dual-Phase-Lag (DPL) Thermoelastic Band-Gap Tuning and Acoustic Dissipation in 1D Periodic Metamaterials with Dipolar Gradient Elasticity  
**Language:** Python 3.10+ (Standard Scientific Stack: `numpy>=1.24`, `scipy>=1.10`, `matplotlib>=3.7`)  

---

## 1. Directory Structure Overview

The source code package is modularized into five functional directories:

- `production/`: Execution pipelines for full parametric sweeps and figure rendering.
  - `run_phase3b_production.py`: Master production sweep runner (36 parameter cases, 100 frequency steps $\Omega \in [0.05, 1.80]$, 17,747 modal records in 12.4 s).
  - `run_pilot_sweep.py`: Phase 3A 6-case pilot sweep runner with Hungarian assignment branch tracking.
  - `regenerate_calibrated_figures.py`: Generates the final calibrated publication figures (Figs 2, 4, 6, 7, 9, 10) directly from frozen production datasets in 4.4 s.
- `transfer_matrix/`: Core Transfer Matrix Method (TMM) solvers.
  - `coupled10.py`: Full 10-state coupled in-plane solver (Mindlin Form-II dipolar gradient elasticity + Tzou DPL heat conduction), incorporating SVD nullspace mode extraction, two-sided row/column equilibration, and the Generalized Interface Eigenvalue Problem ($A\mathbf{c} = \lambda B\mathbf{c}$) with bounded exponentials $\le 1.0$.
  - `antiplane.py`: Decoupled 4-state anti-plane shear wave solver with exact analytical modal matrices and secular determinant root finder.
  - `parameters.py`: Authoritative material parameter dataclass and benchmark configurations (Epoxy Layer A, Aluminum Layer B).
- `validation/`: Independent benchmark verification scripts.
  - `run_benchmarks.py`: Solves Papargyri-Beskou et al. (2009) Eq. (28) across 50 points, verifying relative error $2.45 \times 10^{-15}$.
  - `run_periodic_pilot.py`: Evaluates two-layer periodic cell symplecticity ($|\det(T_{\text{mech}}) - 1.0| = 2.66 \times 10^{-13}$) and Bragg gap emergence.
  - `validate_benchmark_acta.py`: Verifies classical phononic band gaps against Li et al. (2016) Acta Mechanica ($\le 0.3\%$ relative error).
- `analytical/`: Formal mathematical derivation documentation.
  - `PHASE1_DERIVATION.md`: Complete symbolic derivations of governing equations, boundary tractions, and transfer matrices.
  - `PHASE1_SYMBOL_TABLE.md`: Exhaustive symbol and notation definition table.
- `utilities/`: Unit test suite.
  - `test_parameters.py`: Verification of material property consistency.
  - `test_antiplane.py`: Unit tests for 4-state antiplane solver.
  - `test_coupled10.py`: Unit tests for 10-state coupled solver and DPL sanity checks.

---

## 2. Reproduction Workflows

### 2.1 Reproducing Validation Benchmarks
To reproduce the independent external benchmarks:
```bash
python3 validation/run_benchmarks.py
python3 validation/run_periodic_pilot.py
```
*Expected Runtime:* $< 2$ seconds.  
*Key Output:* `benchmark_papargyri_beskou_results.csv` ($2.45 \times 10^{-15}$ relative error).

### 2.2 Regenerating Manuscript Figures (Fast Path)
To regenerate all 10 publication-quality figures directly from the frozen production CSV data without rerunning simulations:
```bash
python3 production/regenerate_calibrated_figures.py
```
*Expected Runtime:* $4.4$ seconds.  
*Key Output:* 10 publication figures at 300 DPI.

### 2.3 Reproducing Full Production Sweeps (Complete Path)
To rerun the full 36-case parametric production campaign:
```bash
python3 production/run_phase3b_production.py
```
*Expected Runtime:* $\approx 12.4$ seconds on standard multi-core CPU.  
*Key Output:* 17,747 modal records saved to `S1_results.csv` through `S7_results.csv`, `PRODUCTION_BANDGAP_SUMMARY.csv`, and `PRODUCTION_ATTENUATION_SUMMARY.csv`.

---

## 3. Computational Environment & Dependencies

- **Python Version:** 3.10 or higher.
- **Dependencies:**
  - `numpy>=1.24` (matrix operations, generalized eigenvalues via `scipy.linalg.eig`)
  - `scipy>=1.10` (linear sum assignment for Hungarian branch tracking, root finding)
  - `matplotlib>=3.7` (publication figure rendering)
- **Computational Complexity:**
  All solvers use closed-form characteristic roots and generalized interface eigenvalue pencils ($20 \times 20$ block matrices per unit cell). There are **no computationally expensive grid discretizations or FEM mesh solves**. A 100-frequency unit-cell sweep takes approximately $0.34$ seconds per case.
