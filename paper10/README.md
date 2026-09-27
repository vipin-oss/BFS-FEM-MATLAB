# Paper 10 Research Package
## Extension E1: Finite-Fluence Nonlinear Guyer–Krumhansl Heat Conduction

**Title:** Regularization of the Guyer–Krumhansl Fourier-Resonance Sensitivity Singularity by Finite Laser Pulse Fluence  
**Author:** V. Gupta  
**Affiliation:** Department of Mathematics, Gurugram University, Gurugram, Haryana 122018, India  
**Target Journal:** *International Journal of Heat and Mass Transfer*  
**Date:** 2026-09-27  
**Validation Status:** FINAL AUDIT PASSED (All Corrections Applied, 100% Reproducible)  

---

## 1. Executive Summary

This repository contains the complete, permanent, fully reproducible scientific research package for Paper 10 (Extension E1). The study investigates the effect of finite laser pulse fluence on the parameter identifiability of the Guyer–Krumhansl (GK) equation at the classical Fourier-resonance condition $B = \frac{\kappa^2}{\alpha \tau_q} = 1$.

In linear conduction, the relaxation time $\tau_q$ and nonlocality $\kappa^2$ exhibit an exact analytical sensitivity colinearity ($J_{\tau_q} = -\alpha J_{\kappa^2}$), rendering the Fisher information matrix singular ($\operatorname{cond}(F) \sim 10^{17}$). By incorporating temperature-dependent thermal conductivity $\lambda(T) = \lambda_0[1 + \beta_T(T-T_0)]$ induced by finite laser pulse fluence, we demonstrate that the non-uniform internal temperature distribution breaks this exact resonance cancellation. The null singular value activates linearly ($\sigma_2 \sim \varepsilon_\lambda^{0.9908}$, $R^2 = 0.999993$) and the condition number regularizes quadratically ($\operatorname{cond}(F) \sim \varepsilon_\lambda^{-1.9678}$, $R^2 = 0.999975$) to $7.36 \times 10^3$ at $\varepsilon_\lambda = 0.05$.

---

## 2. Directory Structure & Folder Guide

The research package is structured into clean, modular, self-documenting directories:

```text
paper10/ (or Paper10_Research_Package/)
├── README.md               # Master package documentation (this file)
├── blueprint/              # Scientific specification, research questions & limiting cases
│   └── BLUEPRINT.md        # Audited mathematical blueprint
├── derivations/            # Full step-by-step analytical mathematical proofs
│   └── derivations.md      # Scaling, resonance cancellation & nonlinear Fourier reduction
├── src/                    # Certified Python forward solvers and analysis drivers
│   ├── solver_e1.py        # Staggered-grid BDF solver for E1 and its Fourier limit
│   ├── solver_ref_fourier.py # Independent conservative FVM Radau IIA reference solver
│   ├── run_range_study.py  # 6-point finite-fluence parameter sweep driver
│   ├── run_fourier_limit_validation.py # Fourier limit validation & mesh convergence driver
│   ├── plot_figures.py     # Publication-grade vector PDF and PNG generator
│   └── reproduce_all.py    # Master end-to-end automated reproduction pipeline
├── runs/                   # Certified machine-readable calculation outputs
│   └── final-paper-calculations/
│       ├── table_01_range_study.csv            # Range sweep metrics (rho, sigma, cond(F))
│       ├── table_02_fourier_limit_validation.csv # E1 vs independent FVM benchmark metrics
│       └── table_03_mesh_convergence.csv       # Mesh refinement study (p = 2.07-2.32)
├── figures/                # Publication figures (PDF vector + PNG raster)
│   ├── Fig01_thermograms.pdf / .png            # Thermograms & Fourier-limit convergence
│   └── Fig02_sensitivity_colinearity.pdf / .png # Sensitivity mode activation & cond(F)
├── audit/                  # Formal audit logs and signed validation reports
│   ├── phase1_kill_screen.md                   # Phase 1 kill-screen verification
│   ├── phase2_range_study.md                   # Phase 2 parameter study audit
│   ├── phase3_fourier_limit_validation.md      # Phase 3 classical limit validation audit
│   └── reproducibility_final.md                # Master reproducibility verification audit
├── manuscript/             # Git-tracked submission manuscript files
│   ├── manuscript.tex      # Elsevier elsarticle LaTeX manuscript
│   ├── references.bib      # Complete BibTeX bibliography (12/12 references resolved)
│   ├── elsarticle.cls      # Document class file
│   ├── elsarticle-num.bst  # Bibliography style file
│   └── manuscript.pdf      # Compiled manuscript PDF
└── overleaf/               # Completely self-contained Overleaf project package
    ├── README.md           # Overleaf-specific user guide and instructions
    ├── manuscript.tex      # LaTeX source with self-contained relative paths
    ├── references.bib      # Full BibTeX database
    ├── elsarticle.cls      # Document class
    ├── elsarticle-num.bst  # Bibliography style
    ├── manuscript.pdf      # Audited compiled manuscript PDF
    └── figures/            # Local figures directory
        ├── Fig01_thermograms.pdf / .png
        └── Fig02_sensitivity_colinearity.pdf / .png
```

---

## 3. The `overleaf/` Folder: Self-Contained Overleaf Project

The `overleaf/` subfolder is designed for direct upload to Overleaf or submission to journal production portals. It is completely isolated from all parent directories:
* **Zero External Relative Paths:** No `../figures`, `../src`, or machine-dependent paths.
* **Pre-compiled PDF Included:** `overleaf/manuscript.pdf` is pre-compiled and verified against `manuscript.tex`, `references.bib`, and local `figures/`.
* **Complete Style Support:** Contains official `elsarticle.cls` and `elsarticle-num.bst`.
* **Downloadable Archive:** Also distributed as `Paper10_Overleaf_Ready.zip` at the repository root.

---

## 4. How to Reproduce All Numerical Results

To regenerate the entire dataset, calculation tables, convergence studies, and publication figures from scratch, run:

```bash
python3 paper10/src/reproduce_all.py
```

Execution takes approximately 60 seconds on a standard workstation and executes:
1. `compute_range_study()` $\to$ generates `table_01_range_study.csv`
2. `compute_fourier_validation()` $\to$ generates `table_02_fourier_limit_validation.csv`
3. `compute_mesh_convergence()` $\to$ generates `table_03_mesh_convergence.csv`
4. `generate_figures()` $\to$ outputs `Fig01` and `Fig02` in both PDF and PNG formats
5. Automated assertions verifying bit-for-bit or numerical tolerance convergence.

---

## 5. Summary of Validated Scientific Findings

1. **Exact Resonance Cancellation ($B=1$):**
   In linear conduction ($\varepsilon_\lambda = 0$), $J_{\tau_q} = -\alpha J_{\kappa^2}$ is recovered to solver precision ($\rho = -1.000000000000$, $R_J = 7.38 \times 10^{-9}$, $\operatorname{cond}(F) = 8.71 \times 10^{16}$).
2. **Smooth, Monotonic Lifting:**
   Lifting occurs without any deadband or threshold for all $\varepsilon_\lambda \ne 0$.
3. **Empirical Asymptotic Power Laws:**
   * Null singular value: $\sigma_2 \sim \varepsilon_\lambda^{0.9908}$ ($R^2 = 0.999993$, linear slope $\approx 7.6 \, \varepsilon_\lambda$)
   * Colinearity departure: $R_J \sim \varepsilon_\lambda^{0.9751}$ ($R^2 = 0.999935$, linear slope $\approx 0.90 \, \varepsilon_\lambda$)
   * Correlation deficit: $1 + \rho \sim \varepsilon_\lambda^{1.9684}$ ($R^2 = 0.999976$)
   * Fisher condition number: $\operatorname{cond}(F) \sim \varepsilon_\lambda^{-1.9678}$ ($R^2 = 0.999975$), falling from $\sim 10^{17}$ to $7.36 \times 10^3$ at $\varepsilon_\lambda = 0.05$.
4. **Independent Classical Fourier Limit Benchmark:**
   Agreement with independent FVM Radau IIA solver is $E_\infty \le 2.32 \times 10^{-9}$ across all fluence levels on the common grid, with spatial discretization error bounded at $e_{200} \approx 3.9 \times 10^{-5}$ ($p \approx 2.07\text{--}2.32$).
5. **Physical Fluence Calibration:**
   * Routine low-fluence flash tests (ASTM E1461, $\Delta T \approx 1$--$3\,\si{\kelvin}$) achieve $\varepsilon_\lambda \approx 0.1\%$--$1.0\%$ ($\operatorname{cond}(F) \sim 10^5$).
   * Intentional elevated-fluence pulses ($\Delta T \approx 5$--$15\,\si{\kelvin}$) achieve $\varepsilon_\lambda \approx 2\%$--$5\%$ ($\operatorname{cond}(F) \sim 7.4 \times 10^3$).
   * Regularisation is sign-symmetric for $\beta_T < 0$ (crystals, rocks, semiconductors) and $\beta_T > 0$ (polymers), with strictly positive conductivity ($1 + \varepsilon_\lambda \hat{T} \ge 0.67 > 0$) throughout the slab.
