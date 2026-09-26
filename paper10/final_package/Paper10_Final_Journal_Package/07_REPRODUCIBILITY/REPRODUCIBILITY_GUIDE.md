# Comprehensive Reproducibility Guide — Paper 10

**Manuscript Title:** Dual-Phase-Lag (DPL) Thermoelastic Band-Gap Tuning and Acoustic Dissipation in 1D Periodic Metamaterials with Dipolar Gradient Elasticity  
**Governing Baseline:** `RESEARCH_BLUEPRINT.md` (v1.2 `1ed2d54`)  
**Frozen Production Baseline Commit:** `f92e86462c42d9d4b7dce78309daac9ac53d7cef`  

---

## 1. End-to-End Scientific Workflow Chain

This research adheres to the AI Research Workflow v6 (Blueprint-First: External Validation Upfront):

```
┌────────────────────────────────────────────────────────────────────────┐
│ STAGE 1: Research Blueprint Locked (Commit 1ed2d54)                    │
│   • Model scope, physical assumptions, novelty boundary locked         │
│   • 5-Level validation hierarchy established upfront                   │
├────────────────────────────────────────────────────────────────────────┤
│ STAGE 2: Phase 1 Analytical Derivation (Commit e9ca21f)                │
│   • Mindlin Form-II gradient elasticity + Tzou DPL heat conduction     │
│   • Variational boundary tractions from Hamilton's principle           │
│   • 10-state and 4-state state-space formulations derived              │
├────────────────────────────────────────────────────────────────────────┤
│ STAGE 3: Phase 2 Solver Implementation & Validation (Commit ee61a02)   │
│   • External benchmark: Papargyri-Beskou (2009) (error = 2.45e-15)     │
│   • External benchmark: Li et al. (2016) classical limit (error <= 0.3%)│
│   • Symplecticity verification: |det(T_mech) - 1.0| = 2.66e-13         │
├────────────────────────────────────────────────────────────────────────┤
│ STAGE 4: Phase 3A Parameter Matrix & Pilot Sweeps (Commit 505d9aa)     │
│   • Locked 36-case parameter matrix (Epoxy Layer A, Aluminum Layer B)  │
│   • Hungarian assignment branch tracking verified                      │
├────────────────────────────────────────────────────────────────────────┤
│ STAGE 5: Phase 3B Full Production Sweeps (Commit 5622c7b)              │
│   • Generalized Interface Eigenvalue Problem (Ac = lambda Bc)          │
│   • Two-sided canonical equilibration: kappa(P_equil) <= 22.72         │
│   • 36 cases, 100 frequencies, 17,747 records generated in 12.4 s      │
│   • Post-correction audit: open Gap 2 qualified, figures calibrated    │
├────────────────────────────────────────────────────────────────────────┤
│ STAGE 6: Phase 4 Manuscript Synthesis & Audit (Commit a709ff5, f92e864)│
│   • 19-page manuscript in LaTeX and PDF (37 equations, 10 figures)     │
│   • Pre-submission audit and final 4 corrections verified              │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Practical Execution Order

To reproduce the study from the repository package:

### Step 1: Environment Setup
Ensure Python 3.10+ is installed with `numpy`, `scipy`, and `matplotlib`:
```bash
python3 --version
python3 -c "import numpy, scipy, matplotlib; print('Core dependencies available.')"
```

### Step 2: Validate Against Published Benchmarks
Execute the external validation suite:
```bash
python3 03_SOURCE_CODE/validation/run_benchmarks.py
python3 03_SOURCE_CODE/validation/run_periodic_pilot.py
```
*Expected Output:*
- Maximum relative error against Papargyri-Beskou Eq. (28) $\le 2.45 \times 10^{-15}$.
- Secular determinant residual $\le 1.90 \times 10^{-14}$.
- Symplectic determinant error $\le 2.66 \times 10^{-13}$.

### Step 3: Fast Figure Regeneration (Recommended)
Regenerate all 10 manuscript figures from the authoritative frozen datasets:
```bash
python3 03_SOURCE_CODE/production/regenerate_calibrated_figures.py
```
*Runtime:* $\approx 4.4$ seconds. All 10 figures saved at 300 DPI.

### Step 4: Full Production Sweep Reproduction (Optional Verification)
To regenerate all 17,747 modal records across the 36 parameter cases:
```bash
python3 03_SOURCE_CODE/production/run_phase3b_production.py
```
*Runtime:* $\approx 12.4$ seconds.  
*Note:* The datasets in `04_PRODUCTION_DATA/` are **frozen**. Running this script will reproduce identical CSV files.

### Step 5: Manuscript PDF Compilation
To compile the manuscript PDF from LaTeX source:
```bash
cd 01_MANUSCRIPT
./compile_manuscript.sh
```
*Result:* Standalone compilation produces `Paper10_Manuscript.pdf` (19 pages) with all figures, equations, and citations resolved.

---

## 3. Strict Boundary & Limitation Guidelines

1. **Frozen Production Datasets:** Datasets in `04_PRODUCTION_DATA/` represent the frozen archival baseline and must not be altered.
2. **Boundary-Truncated Gaps:** 23 records in `PRODUCTION_BANDGAP_SUMMARY.csv` terminating at $\Omega = 1.8000$ (e.g., Gap 2 of baseline) are open bands truncated by the frequency window ceiling. They are not closed physical band gaps.
3. **Conditioning Precision:** Solver stability is governed by the equilibrated modal matrix ($\kappa \le 22.72$). Raw SI condition numbers ($\sim 10^{15} - 10^{20}$) are artifacts of dimensional units.
