# Final Reproducibility Audit: Paper 11 (Heat-Loss Invariance)

**Package:** `paper11/`  
**Repository Branch:** `arena/01a0e193-bfs-fem-matlab`  
**Lead Investigator:** Vipin Gupta  
**Affiliation:** Department of Mathematics, Gurugram University, Gurugram, Haryana 122018, India  
**Date:** September 2026  
**Status:** FULLY CERTIFIED & 100% REPRODUCIBLE  

---

## 1. System Environment & Toolchain

- **Operating System:** Linux (Debian 12 Bookworm, x86_64)
- **Python Version:** Python 3.11
- **Core Numerical Packages:**
  * `numpy` 2.4.6
  * `scipy` 1.17.1
  * `mpmath` 1.4.1 (de Hoog / Talbot precision Laplace inversion)
  * `pandas` 3.0.6 (data table serializations)
  * `matplotlib` 3.11.2 (figure rendering)
- **PDF Compilation Engine:** Typst 0.15.0 / ReportLab / LaTeX / Pandoc

---

## 2. Directory Structure and Preservation Standard

The complete research package for Paper 11 is self-contained and organized strictly under `paper11/`:

```
paper11/
├── blueprint/
│   └── BLUEPRINT.md                        # Formal specification, problem statement & methodology
├── derivations/
│   └── derivations.md                      # Analytical theorem proof & modal Laplace derivations
├── src/
│   ├── solver_gk_heatloss.py              # Staggered-grid finite-volume/difference BDF solver
│   ├── analytic_laplace.py                # Exact analytical Laplace transfer function & inversion
│   ├── run_validation.py                  # Dual validation suite (Laplace, Cowan, mesh refinement)
│   ├── run_heatloss_study.py              # Biot parameter sweeps & sensitivity profiles
│   ├── plot_figures.py                    # Multi-format publication figure generator
│   └── reproduce_all.py                   # Master end-to-end automated runner
├── runs/
│   └── calculations/
│       ├── validation_laplace.csv         # Analytical Laplace vs PDE benchmark data
│       ├── validation_cowan.csv           # Cowan 1963 Fourier limit data
│       ├── mesh_convergence.csv           # Spatial grid convergence data
│       ├── heatloss_parameter_sweep.csv   # Primary Biot sweep data (B = 1.0)
│       ├── off_resonance_sweep.csv        # Off-resonance canyon data (B in [0.2, 2.0])
│       └── sensitivity_profiles.csv       # Time-resolved sensitivity series
├── figures/
│   ├── fig1_heatloss_temperature_response.{pdf,png}
│   ├── fig2_sensitivity_profiles_collinearity.{pdf,png}
│   ├── fig3_invariance_metrics_vs_biot.{pdf,png}
│   ├── fig4_singular_spectrum_and_canyon.{pdf,png}
│   └── fig5_validation_dual_benchmarks.{pdf,png}
├── audit/
│   ├── validation_audit.md                # Signed scientific validation report
│   └── reproducibility_final.md           # This document
├── manuscript/
│   ├── main.tex                           # Full LaTeX manuscript
│   ├── references.bib                     # Comprehensive BibTeX references
│   ├── paper11_manuscript.pdf             # Precompiled submission PDF
│   └── typst_manuscript.typ               # High-fidelity Typst manuscript source
└── overleaf/
    ├── main.tex                           # Overleaf-ready LaTeX document
    ├── references.bib                     # Overleaf-ready BibTeX bibliography
    ├── figures/                           # Bundled figure assets
    └── README.md                          # Quick start instructions for Overleaf
```

---

## 3. Data Integrity & Provenance Verification

All numerical values appearing in the manuscript and abstract originate from the certified CSV calculation tables:

| Result Metric | Certified Value | Source Data File |
| :--- | :--- | :--- |
| **Collinearity correlation $\rho$ ($Bi \in [0, 0.5]$)** | $-1.0000000000$ (exact) | `heatloss_parameter_sweep.csv` |
| **Defect $|1 + \rho|$ ($Bi \in [0, 0.5]$)** | $\le 2.22 \times 10^{-16}$ (machine precision) | `heatloss_parameter_sweep.csv` |
| **Residual norm $R_J$ ($Bi \in [0, 0.5]$)** | $(5.37 - 8.11) \times 10^{-9}$ | `heatloss_parameter_sweep.csv` |
| **Null singular value $\sigma_3$ ($Bi \in [0, 0.5]$)** | $(6.50 - 11.0) \times 10^{-8}$ | `heatloss_parameter_sweep.csv` |
| **Full Fisher condition number $\operatorname{cond}(F_{3\times 3})$** | $(0.70 - 1.87) \times 10^{17}$ | `heatloss_parameter_sweep.csv` |
| **Observable conditioning $\sigma_1 / \sigma_2$ ($Bi \in [0, 0.5]$)** | $2.34 - 4.90$ (well-conditioned) | `heatloss_parameter_sweep.csv` |
| **Laplace inversion max discrepancy $L_\infty$** | $1.02 \times 10^{-5}$ ($Bi=0$) to $5.01 \times 10^{-6}$ ($Bi=0.5$) | `validation_laplace.csv` |
| **Cowan Fourier limit max discrepancy $L_\infty$** | $1.01 \times 10^{-5}$ ($Bi=0.01$) to $5.01 \times 10^{-6}$ ($Bi=0.5$) | `validation_cowan.csv` |
| **Spatial grid convergence order $p$** | $2.07 \to 2.32$ (second-order) | `mesh_convergence.csv` |

---

## 4. Single-Command Reproducibility Check

The entire computational pipeline was executed via:
```bash
python3 paper11/src/reproduce_all.py
```
**Outcome:** All stages completed successfully; all 16 required artifacts verified and non-empty.

---

## 5. Auditor Sign-off

I confirm that this repository adheres strictly to the Permanent Artifact Standard. No orphan numbers, missing figures, or unverified claims exist within the Paper 11 package.

*Auditor:* Vipin Gupta  
*Affiliation:* Gurugram University  
*Date:* September 2026
