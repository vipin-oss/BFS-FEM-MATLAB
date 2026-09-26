# Paper 10: Final Journal & Reproducibility Package

**Title:** Dual-Phase-Lag (DPL) Thermoelastic Band-Gap Tuning and Acoustic Dissipation in 1D Periodic Metamaterials with Dipolar Gradient Elasticity  
**Target Journals:** *Applied Mathematical Modelling* / *Composite Structures*  
**Repository:** `vipin-oss/BFS-FEM-MATLAB`  
**Working Branch:** `arena/01a0dcde-bfs-fem-matlab`  
**Frozen Baseline Commit:** `f92e86462c42d9d4b7dce78309daac9ac53d7cef`  
**Author / Engine:** Arena.ai Builder (Independent Research Engine)  
**Date:** 2026-09-26  

---

## 1. Package Contents Overview

This package contains the complete, self-contained, and fully reproducible scientific research artifact:

- `00_README/`: Overview, full package manifest, and frozen milestone provenance.
- `01_MANUSCRIPT/`: LaTeX source (`Paper10_Manuscript.tex`), compiled 19-page PDF (`Paper10_Manuscript.pdf`), bibliography (`references.bib`), and build script (`compile_manuscript.sh`).
- `02_FIGURES/`: All 10 publication-quality 300-DPI raster figures and detailed `FIGURE_MANIFEST.md`.
- `03_SOURCE_CODE/`: Complete modular computational Python codebase (`production/`, `transfer_matrix/`, `validation/`, `analytical/`, `utilities/`) and `CODE_README.md`.
- `04_PRODUCTION_DATA/`: All frozen machine-readable CSV/JSON datasets (17,747 modal records across 36 cases) and comprehensive `DATA_DICTIONARY.md`.
- `05_VALIDATION/`: Independent published benchmarks (Papargyri-Beskou et al., 2009; Li et al., 2016), symplecticity tests, and `VALIDATION_README.md`.
- `06_AUDIT_RECORD/`: Complete five-part scientific, traceability, and pre-submission audit reports.
- `07_REPRODUCIBILITY/`: Step-by-step reproduction instructions, execution order, and environment specifications.
- `08_GIT_PROVENANCE/`: Exact Git commit hash, working tree status, log, and file inventory.

---

## 2. Key Scientific Findings

1. **Bragg Stop Bands vs. DPL Dissipation:**
   Bragg band gaps arise from geometric wave reflection across periodic acoustic impedance mismatches ($Z_B / Z_A$), producing reactive spatial evanescence ($\alpha a \approx 4.915$), whereas DPL thermoelasticity establishes an active thermodynamic dissipation floor ($\alpha a \sim 2.2 \times 10^{-4}$ to $5.5 \times 10^{-2}$) across all propagating pass bands.
2. **Material Contrast Independence:**
   In the identical-layers limit ($\chi = 0$), acoustic impedance contrast vanishes, completely eliminating Bragg band gaps ($\Delta\Omega \equiv 0.0000$). Intrinsic dipolar gradient dispersion and thermal attenuation remain active throughout the homogeneous medium.
3. **Opposing Micro-Length Scale Modulations:**
   Micro-stiffness ($\sqrt{c}/a$) induces dispersive stiffening, increasing acoustic phase velocity and shifting band-gap edges to higher frequencies. Conversely, kinetic micro-inertia ($d/a$) induces dispersive softening, lowering phase velocity and shifting band gaps downward.
4. **Boundary Truncation Integrity:**
   All 23 band-gap records terminating at the frequency ceiling $\Omega = 1.8000$ (e.g., baseline Gap 2, $\Omega_L = 1.3051$) are explicitly documented as open attenuation bands whose upper physical edge lies beyond the investigated window.
5. **Algorithmic Conditioning:**
   By formulating interface matching into a Generalized Interface Eigenvalue Problem ($A\mathbf{c} = \lambda B\mathbf{c}$) with bounded directional exponentials ($\le 1.0$) and canonical equilibration, modal matrix conditioning is strictly maintained at $\kappa(P_{\text{equil}}) \le 22.72$ (baseline) and $\le 4648.99$ (classical limit).

---

## 3. Quick Start

To verify validation benchmarks:
```bash
python3 03_SOURCE_CODE/validation/run_benchmarks.py
```

To regenerate all 10 manuscript figures from frozen data:
```bash
python3 03_SOURCE_CODE/production/regenerate_calibrated_figures.py
```

To recompile the manuscript PDF:
```bash
cd 01_MANUSCRIPT && ./compile_manuscript.sh
```
