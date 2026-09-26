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

---

## Phase-0 Addendum (2026-09-26): Scientific-Depth Expansion

This addendum records the Phase-0 expansion applied on top of the frozen v1.0 package. All frozen scientific artifacts (equations, solvers, S1-S7 production datasets, calibrated figures) remain byte-identical; the following content was ADDED:

1. **Bibliography expanded from 25 to 47 verified entries** (2024-2026 non-Fourier thermoelasticity in phononic/metamaterial contexts, gradient-elastic phononic crystals, thermoelastic damping in periodic/resonant structures, transfer-matrix and spectral methods for layered waveguides; plus foundational anchors: Zener 1937; Lim-Zhang-Reddy 2015; Metrikine-Askes 2002). All new entries were individually verified against publisher records. The bib key of the Li et al. thermoelastic band-gap paper was corrected from `li2023thermoelastic` to `li2026thermoelastic` (the true issue year of *Waves in Random and Complex Media* 36(4):5715-5735 is 2026; published online 9 June 2023 - year field unchanged, key corrected). Citations are now woven through Results, Discussion, Limitations, and Conclusions with explicit quantitative comparisons against prior published results.
2. **Three new figures (total 10 -> 13):** Fig. 1 unit-cell schematic (didactic); Fig. 2 Papargyri-Beskou benchmark overlay (archived validation data, no new runs); Fig. 12 supplementary 2-D (chi, eta) band-gap-width heatmap from a newly documented 121-case grid campaign (`run_chi_eta_grid.py`, solver verbatim; four frozen S2/S4 anchors reproduced exactly). Former Figs. 1-10 are renumbered to Figs. 3-11 and 13; file names unchanged for provenance (see `02_FIGURES/FIGURE_MANIFEST.md`).
3. **New supplementary datasets** in `04_PRODUCTION_DATA/`: `SUPP_CHI_ETA_GAP_SUMMARY.csv`, `SUPP_CHI_ETA_CASE_METRICS.csv`, `SUPP_CHI_ETA_GRID_META.json` (documented in `DATA_DICTIONARY.md`, Sec. 4).

No author/identity fields, document class, table formatting, or folder structure were modified.

---

## Phase-A Addendum (2026-09-26): Mode-Classification / Branch-Tracking Correction

A plotting-layer defect was identified and fixed (the solver and all frozen datasets remain byte-identical):

1. **Dispersion diagrams (Fig. 3 / `fig1_baseline_dispersion.png`, and the S2/S4/S7 dot panels):** the original code plotted the first five raw `branch_id` groups indiscriminately, drawing evanescent/complex-wavenumber modes (near `kr/π = 0` with αa ≈ 0.3-4.9) as if they were propagating branches - a dense vertical line across the entire frequency range. Fixed by an explicit classification step (`propagating` = kr/π > 0.01 AND αa < 0.05, solid points; `evanescent/complex-k` = otherwise, faint grey points with their own legend entry).

2. **Acoustic-branch tracking (Fig. 4 / `fig2_baseline_attenuation.png`):** the former `extract_acoustic_branch` preferred kr-continuity with a loose αa < 0.5 admission window and updated its anchor even inside stop bands, intermittently locking onto evanescent or higher-branch modes and producing ~10 spurious attenuation spikes (Ω ≈ 0.13, 0.3, 0.55, 0.63, 0.8, 0.87, 0.97, 1.42, 1.5, 1.6-1.65, 1.75). Corrected rule: the acoustic branch is the LEAST-ATTENUATED genuinely propagating mode at each frequency; inside stop bands it falls back to the least-attenuated evanescent continuation (flagged, drawn as open circles). After the fix, spikes appear ONLY at the documented stop bands: DPL Gap 1 [0.6687, 0.7040] (peak ≈ 4.5e-2), the open gap Ω_L = 1.3051 (branch continues to ≈ 1.35), and the conservative gap [1.5702, 1.6763] (peak 0.0913). Verified against `PRODUCTION_BANDGAP_SUMMARY.csv` and `PRODUCTION_ATTENUATION_SUMMARY.csv`.

3. **Supplementary grid:** the (χ, η) campaign was re-run with tracking-independent raw-mode gap extraction; all four frozen S2/S4 anchors still reproduce exactly, and the published gap summary is unchanged (115 records, byte-identical).

New/updated code: `03_SOURCE_CODE/production/branch_utils.py` (shared utilities), `regenerate_phaseA_figures.py` (dispersion regeneration), patched `run_phase3b_production.py`, `regenerate_calibrated_figures.py`, `run_chi_eta_grid.py`. Manuscript captions of Figs 3-4 updated accordingly; PDF recompiled.
