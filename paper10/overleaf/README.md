# Overleaf Manuscript Package: Paper 10 (Extension E1)

**Title:** Regularization of the Guyer–Krumhansl Fourier-Resonance Sensitivity Singularity by Finite Laser Pulse Fluence  
**Author:** V. Gupta  
**Affiliation:** Department of Mathematics, Gurugram University, Gurugram, Haryana 122018, India  
**Target Journal:** *International Journal of Heat and Mass Transfer*  
**Date:** 2026-09-27  
**Document Class:** Elsevier `elsarticle` (`preprint, 12pt, a4paper`)  

---

## 1. Overview & Contents

This folder is a completely self-contained, publication-ready Overleaf project. It contains all source files, bibliographies, document classes, figures, and compiled outputs required to view, edit, and compile the manuscript with zero external dependencies.

```text
overleaf/
├── README.md               # This complete user guide and project documentation
├── manuscript.tex          # Master LaTeX submission source file (audited version)
├── references.bib          # Complete BibTeX bibliography (12/12 references resolved)
├── elsarticle.cls          # Official Elsevier document class definition
├── elsarticle-num.bst      # Elsevier numbered bibliography style
├── manuscript.pdf          # Pre-compiled high-resolution manuscript PDF (7 pages)
└── figures/                # Standalone vector PDF and raster PNG figures
    ├── Fig01_thermograms.pdf
    ├── Fig01_thermograms.png
    ├── Fig02_sensitivity_colinearity.pdf
    └── Fig02_sensitivity_colinearity.png
```

---

## 2. Overleaf Compilation Instructions

To compile this project on Overleaf:
1. Log in to your [Overleaf](https://www.overleaf.com) account.
2. Click **New Project** $\to$ **Upload Project**.
3. Upload the `Paper10_Overleaf_Ready.zip` archive (or upload the files in this folder directly into a blank project).
4. Ensure that the project settings specify:
   * **Main document:** `manuscript.tex`
   * **Compiler:** `pdfLaTeX` (or `XeLaTeX` / `LuaLaTeX`; all standard TeX engines are supported)
   * **TeX Live version:** `2023` or newer
5. Click **Recompile**. The document will compile cleanly on the first pass with zero missing-reference errors.

---

## 3. Local Command-Line Compilation

To compile this project locally from your terminal:

### Standard TeX Live / MacTeX / MiKTeX
```bash
cd overleaf/
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex
```

### Using Tectonic
```bash
cd overleaf/
tectonic manuscript.tex
```

All figures are located in the local `figures/` subfolder, and the document header specifies `\graphicspath{{figures/}{./}}`, ensuring that figure resolution works identically across all operating systems.

---

## 4. Reproducibility & Artifact Preservation

* **`manuscript.pdf`:** The included PDF is the exact, bit-for-bit compiled artifact generated from `manuscript.tex`, `references.bib`, and `figures/`.
* **Zero External Dependencies:** No file paths reference external folders (`../figures`, `../src`, `C:\`, `/home/user`, etc.).
* **Figure Integrity:** Both vector (`.pdf`) and high-resolution raster (`.png`) versions of Fig. 1 and Fig. 2 are archived.
* **Bibliographic Precision:** Every citation key referenced in `manuscript.tex` exists in `references.bib` with verified DOIs and volume/page metadata.

---

## 5. Relationship to Full Research Package

This `overleaf/` folder is the submission- and publication-facing component of the complete research package. The parent package contains:

* `blueprint/`: Complete mathematical specification, problem statement, research questions, and limiting case definitions (`BLUEPRINT.md`).
* `derivations/`: Step-by-step analytical derivations of the non-dimensional scaling, the $B=1$ resonance identity, and the continuous nonlinear Fourier reduction (`derivations.md`).
* `src/`: Certified Python forward solvers (`solver_e1.py`), independent conservative FVM reference solver (`solver_ref_fourier.py`), range sweep scripts (`run_range_study.py`), Fourier limit validation drivers (`run_fourier_limit_validation.py`), plotting scripts (`plot_figures.py`), and the master automated reproduction script (`reproduce_all.py`).
* `runs/`: Machine-readable CSV output tables (`table_01_range_study.csv`, `table_02_fourier_limit_validation.csv`, `table_03_mesh_convergence.csv`).
* `figures/`: Master publication figures in vector PDF and PNG formats.
* `audit/`: Signed audit reports for Phase 1 (Kill-Screen), Phase 2 (Range Study), Phase 3 (Nonlinear Fourier Limit), and Master Reproducibility.
* `manuscript/`: Git-tracked manuscript sources.
* `overleaf/`: Self-contained Overleaf submission package (this folder).

---

## 6. Scientific Summary & Established Validation

1. **Lifting of Resonance Singularity:** In linear Guyer–Krumhansl heat conduction at the Fourier resonance $B = \kappa^2/(\alpha \tau_q) = 1$, the sensitivities of relaxation time $\tau_q$ and nonlocality $\kappa^2$ are exactly collinear ($J_{\tau_q} = -\alpha J_{\kappa^2}$), rendering the parameter pair non-identifiable ($\operatorname{cond}(F) = 8.71 \times 10^{16}$).
2. **Finite-Fluence Regularisation:** When finite pulse energy induces temperature-dependent thermal conductivity $\lambda(T) = \lambda_0[1 + \beta_T(T-T_0)]$, the transient through-slab temperature gradient breaks the internal algebraic resonance cancellation. The second parameter direction activates linearly ($\sigma_2 \sim \varepsilon_\lambda^{0.9908}$, $R^2 = 0.999993$), dropping the condition number quadratically ($\operatorname{cond}(F) \sim \varepsilon_\lambda^{-1.9678}$, $R^2 = 0.999975$) to $7.36 \times 10^3$ at $\varepsilon_\lambda = 0.05$.
3. **Classical Fourier Limit PASS:** In the singular limit $\tau_q \to 0, \kappa^2 \to 0$, the E1 model agrees with an independent conservative Finite Volume Method (Radau IIA) reference solver to $E_\infty \le 2.32 \times 10^{-9}$ on a common grid, with spatial discretization error bounded separately ($e_{200} \approx 3.9 \times 10^{-5}$) under asymptotic second-order spatial convergence ($p \approx 2.07\text{--}2.32$).
4. **Physical Plausibility & Sign Invariance:** Routine low-fluence flash tests ($\Delta T \approx 1\text{--}3\,\si{\kelvin}$) achieve $\varepsilon_\lambda \approx 0.1\%\text{--}1.0\%$ ($\operatorname{cond}(F) \sim 10^5$), while intentional elevated-fluence pulses ($\Delta T \approx 5\text{--}15\,\si{\kelvin}$) achieve $\varepsilon_\lambda \approx 2\%\text{--}5\%$ ($\operatorname{cond}(F) \sim 7.4 \times 10^3$). The regularisation is sign-symmetric for $\beta_T < 0$ (crystals, rocks, semiconductors) and $\beta_T > 0$ (polymers), with strictly positive conductivity ($1 + \varepsilon_\lambda \hat{T} \ge 0.67 > 0$) throughout the domain.

---

## 7. Numerical Reproducibility Warning

The PDF in this folder is a compiled artifact. Numerical values and figures must never be altered by manual editing of the `.tex` or `.pdf` files. All computations, tables, and figures must be regenerated using `python3 src/reproduce_all.py` from the full research package root.
