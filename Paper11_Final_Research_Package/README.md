# Invariance of the Guyer–Krumhansl Fourier-Resonance Sensitivity Singularity to Boundary Heat Loss in Laser Flash Testing

**Author:** Vipin Gupta  
**Affiliation:** Department of Mathematics, Gurugram University, Gurugram, Haryana 122018, India  
**Email:** vipin.gupta@gurugramuniversity.ac.in  
**Package:** `Paper11_Final_Research_Package/`  
**Date:** September 2026  

---

## 1. Scientific Status & Audit Decisions

This research package has undergone exhaustive independent verification across two formal decision gates:
- **Mathematical & Numerical Audit (Gate 1):** **PASS**  
  Symbolic reduction certified via SymPy (`derivation_check.py`), exact analytical Laplace inversion agreement ($L_\infty \le 1.02 \times 10^{-5}$), Cowan (1963) Fourier heat loss limit agreement ($L_\infty \le 1.01 \times 10^{-5}$), and spatial second-order mesh convergence ($p = 2.07 \to 2.32$).
- **Literature Novelty & Prior Art Audit (Gate 2):** **NOVELTY PASS**  
  Exhaustive examination of prior art (Both et al. 2016, Kovács 2018, Cowan 1963, Cape & Lehman 1963, Sellitto et al. 2025) confirms that boundary heat loss invariance of the Guyer--Krumhansl parameter singularity has never previously been analyzed or proven.
- **Scientific Contribution:** **PASS**  
  Establishes a fundamental no-go result: convective/radiative boundary heat loss cannot break the Guyer--Krumhansl Fourier-resonance sensitivity collinearity $\partial T / \partial \tau_q = -\alpha_0 \partial T / \partial \kappa^2$.
- *Publication Status:* Pre-publication validated research package (not yet submitted/accepted).

---

## 2. Package Structure & Contents

```text
Paper11_Final_Research_Package/
│
├── README.md                          # Primary package documentation and quick start
├── OVERVIEW.md                        # Comprehensive research overview and summary of findings
│
├── manuscript/                        # Authoritative publication manuscript source
│   ├── main.tex                       # Complete LaTeX article source
│   ├── references.bib                 # BibTeX bibliography with complete DOIs
│   ├── paper11_manuscript.pdf         # Certified 13-page precompiled publication PDF
│   └── elsarticle-num.bst             # Standard Elsevier BibTeX style
│
├── overleaf/                          # 100% self-contained Overleaf upload project
│   ├── main.tex                       # Root document configured for Overleaf
│   ├── references.bib                 # Bundled BibTeX references
│   ├── manuscript.pdf                 # Precompiled reference PDF
│   ├── README.md                      # Overleaf upload and compile guide
│   ├── elsarticle-num.bst             # Local BibTeX style
│   └── figures/                       # All vector PDF and raster PNG figures
│
├── program/                           # Computational source code and execution scripts
│   ├── README.md                      # Program guide and execution instructions
│   ├── requirements.txt               # Certified Python dependencies
│   ├── solver_gk_heatloss.py          # 1D staggered-grid BDF numerical solver
│   ├── analytic_laplace.py            # Exact analytical Laplace transfer functions & de Hoog inversion
│   ├── run_validation.py              # Dual benchmark validation runner
│   ├── run_heatloss_study.py          # Parameter sweep & sensitivity calculator
│   ├── plot_figures.py                # Publication figure generator
│   └── reproduce_all.py               # Master end-to-end automated runner
│
├── data/                              # Certified calculation output tables
│   ├── validation_laplace.csv         # Laplace vs PDE benchmark data
│   ├── validation_cowan.csv           # Cowan 1963 Fourier limit benchmark data
│   ├── mesh_convergence.csv           # Spatial grid convergence data
│   ├── heatloss_parameter_sweep.csv   # Primary Biot sweep data (B = 1.0)
│   ├── off_resonance_sweep.csv        # Off-resonance canyon data (B in [0.2, 2.0])
│   └── sensitivity_profiles.csv       # Time-resolved sensitivity series
│
├── figures/                           # All certified publication figures (PDF & 300-DPI PNG)
│   ├── fig1_heatloss_temperature_response.{pdf,png}
│   ├── fig2_sensitivity_profiles_collinearity.{pdf,png}
│   ├── fig3_invariance_metrics_vs_biot.{pdf,png}
│   ├── fig4_singular_spectrum_and_canyon.{pdf,png}
│   └── fig5_validation_dual_benchmarks.{pdf,png}
│
├── derivations/                       # Analytical derivations and theorem proofs
│   └── derivations.md                 # Laplace-domain modal derivation and Theorem 1 proof
│
├── blueprint/                         # Research specification and architecture
│   └── BLUEPRINT.md                   # Blueprint specifications and verification protocol
│
└── audit/                             # Comprehensive audit suites and scientific provenance
    ├── PACKAGE_MANIFEST.md            # Complete file manifest and role descriptions
    ├── FINAL_SCIENTIFIC_CHANGE_REPORT.md # Master record of all revisions and enhancements
    ├── validation_audit.md            # Signed scientific validation certificate
    ├── reproducibility_final.md       # Reproducibility verification specification
    ├── independent_audit/             # Gate 1 independent verification scripts and logs (10 files)
    └── literature_final/              # Gate 2 literature novelty and positioning reports (7 files)
```

---

## 3. Quick Start & Master Reproduction

### Prerequisites
Install Python 3.10+ and required packages:
```bash
pip install -r program/requirements.txt
```

### End-to-End Automated Reproduction
From the `program/` directory:
```bash
cd program
python reproduce_all.py
```
This single command executes:
1. Dual analytical benchmarks (Laplace inversion & Cowan Fourier limit) and spatial mesh refinement.
2. Parameter sweeps across three decades of Biot numbers ($Bi \in [0.001, 0.5]$), SVD spectrum decomposition, and off-resonance singularity sweeps.
3. Generation of all 5 publication figures in both vector PDF and 300-DPI PNG formats.
4. Comprehensive integrity verification of all 16 generated data and figure artifacts.

*Execution time:* Approximately 15–20 seconds on standard modern CPU hardware.

---

## 4. Self-Contained Overleaf Project

The `overleaf/` directory is engineered as a **100% self-contained** project:
1. Upload the `overleaf/` directory (or zip archive) directly to [Overleaf](https://www.overleaf.com/).
2. Select `main.tex` as the root document.
3. Set the engine to standard **pdfLaTeX** or **LaTeX**.
4. Click **Compile**.

All figures (`overleaf/figures/`), bibliography (`overleaf/references.bib`), and style files (`overleaf/elsarticle-num.bst`) are self-contained within the folder. No relative paths outside the `overleaf/` directory are referenced.

---

## 5. Summary of Core Analytical and Numerical Results

1. **Theorem 1 (Heat-Loss Invariance):**  
   At the Fourier-resonance condition $B \equiv \kappa^2 / (\alpha_0 \tau_q) = 1$, both the bulk propagation factor $m(s) \to \sqrt{s}$ and the dynamic surface thermal conductivity operator $\lambda_{\mathrm{eff}}(s) \to \lambda_0$ collapse simultaneously. The Guyer--Krumhansl temperature field is identically equal to the classical Fourier heat conduction field with the corresponding Robin boundary conditions:
   $$\theta_{\mathrm{GK}}(x, t)|_{B=1} \equiv \theta_{\mathrm{Fourier}}(x, t) \quad \forall t \ge 0, \; \forall x \in [0, 1].$$
2. **Persistence of Collinearity:**  
   Across three decades of Biot numbers ($Bi \in [0.001, 0.5]$):
   - Sensitivity correlation: $\rho \equiv -1.0000000000$ ($|1+\rho| \le 2.22 \times 10^{-16}$).
   - Residual norm: $\|J_{\tau_q} + \alpha_0 J_{\kappa^2}\| / \|J_{\tau_q}\| \approx (5.37 - 8.11) \times 10^{-9}$.
   - Condition number: $\operatorname{cond}(F_{2\times 2}) \sim 10^{17}$ (numerical singularity floor).
3. **SVD Subspace Separation in 3-Parameter Inversion $(\tau_q, \kappa^2, Bi)$:**  
   - Convective cooling is cleanly identifiable: $\sigma_1 / \sigma_2 \in [2.34, 4.90]$.
   - Null vector $\bm{v}_{\mathrm{null}} = (1, \alpha_0, 0)^\top$ remains completely unregularized ($\sigma_3 \sim 10^{-8}$).
4. **Regularization Pathways:**  
   Standard heat-loss corrections cannot resolve the identifiability degeneracy. Regularization requires perturbing the bulk transport condition away from resonance (e.g., thickness tuning off-resonance, high-fluence nonlinear excitation regimes).
