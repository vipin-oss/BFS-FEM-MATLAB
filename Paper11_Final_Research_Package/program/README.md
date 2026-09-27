# Computational Source Program: Paper 11

**Paper:** Invariance of the Guyer–Krumhansl Fourier-Resonance Sensitivity Singularity to Boundary Heat Loss in Laser Flash Testing  
**Lead Investigator:** Vipin Gupta  
**Affiliation:** Department of Mathematics, Gurugram University, Gurugram, Haryana 122018, India  

---

## 1. System Environment & Requirements

- **Python Version:** Python 3.10+ (tested on Python 3.11.2, x86_64 Linux)
- **Dependencies:** Listed in `requirements.txt`:
  * `numpy >= 1.24.0`
  * `scipy >= 1.10.0`
  * `mpmath >= 1.3.0`
  * `pandas >= 2.0.0`
  * `matplotlib >= 3.7.0`
  * `sympy >= 1.12`

### Installation Command
From this directory:
```bash
pip install -r requirements.txt
```

---

## 2. Master Reproduction Command

To reproduce all numerical calculations, dual benchmarks, sensitivity parameter sweeps, and publication figures in a single automated run:

```bash
python reproduce_all.py
```
*(Approximate runtime: 15–20 seconds on standard 4-core CPU)*

All outputs will automatically be populated in:
- `../data/` (CSV calculation tables)
- `../figures/` (Vector PDF and 300-DPI PNG figures)
- `../overleaf/figures/` (Bundled Overleaf figures)

---

## 3. Individual Script Execution & Purpose

| Script Name | Purpose | Output Location |
| :--- | :--- | :--- |
| `solver_gk_heatloss.py` | Core 1D staggered-grid BDF numerical solver with Robin convective/radiative cooling. | Importable module |
| `analytic_laplace.py` | Exact closed-form Laplace transfer functions and de Hoog high-precision inversion routines. | Importable module |
| `run_validation.py` | Runs the dual validation suite: (1) Laplace vs PDE benchmark, (2) Cowan (1963) Fourier limit, (3) spatial grid refinement. | `../data/validation_laplace.csv`<br>`../data/validation_cowan.csv`<br>`../data/mesh_convergence.csv` |
| `run_heatloss_study.py` | Computes Biot number sweeps ($Bi \in [0, 0.5]$), sensitivity Jacobians, collinearity metrics, SVD spectra, and off-resonance condition canyon. | `../data/heatloss_parameter_sweep.csv`<br>`../data/off_resonance_sweep.csv`<br>`../data/sensitivity_profiles.csv` |
| `plot_figures.py` | Generates all 5 publication-ready figures in dual formats (vector PDF and 300-DPI PNG). | `../figures/`<br>`../overleaf/figures/` |
| `reproduce_all.py` | Master orchestrator running validation, production calculations, plotting, and integrity certification. | Console audit log |

---

## 4. Verification Standards

Each script is completely self-contained and operates using relative paths to sibling directories (`../data/`, `../figures/`, `../overleaf/`). No external paths to any host directory or remote repository are required.
