# Final Scientific Change Report: Paper 11 (Heat-Loss Invariance)

**Title:** Invariance of the Guyer–Krumhansl Fourier-Resonance Sensitivity Singularity to Boundary Heat Loss in Laser Flash Testing  
**Lead Investigator:** Vipin Gupta  
**Affiliation:** Department of Mathematics, Gurugram University, Gurugram, Haryana 122018, India  
**Date:** September 2026  
**Status:** FULLY CERTIFIED & COMPLETED  

---

## Executive Summary

This report documents the exhaustive scientific audit, mathematical verification, literature positioning, and manuscript revision executed for **Paper 11**. 

Paper 11 investigates whether convective and radiative boundary heat loss breaks the Guyer--Krumhansl (GK) Fourier-resonance parameter identifiability singularity at $B \equiv \kappa^2 / (\alpha_0 \tau_q) = 1$. Through rigorous independent symbolic and numerical audits, we establish that Robin boundary heat loss leaves the local sensitivity collinearity $\partial T / \partial \tau_q = -\alpha_0 \partial T / \partial \kappa^2$ strictly invariant across all Biot numbers ($Bi \in [0.001, 0.5]$), asymmetric cooling configurations, and interior spatial locations. Both independent decision gates—**Gate 1 (Mathematical/Numerical Audit)** and **Gate 2 (Literature Novelty Audit)**—have formally **PASSED**. All manuscript assets, precompiled PDF deliverables, and Overleaf distribution archives have been updated and verified.

---

## Section A: Independent Decision Gate Audits

### Gate 1: Independent Mathematical & Numerical Audit (PASS)
An independent mathematical and computational verification suite was authored from first principles in `paper11/audit/independent_audit/`:
1. **Symbolic Proof (`derivation_check.py`):** SymPy derivation confirmed that at $B = 1$, both $m(s) \to \sqrt{s}$ and the dynamic surface impedance $\lambda_{\mathrm{eff}}(s) \to \lambda_0$, causing the full Laplace-domain transfer function $\bar{T}_{\mathrm{GK}}(x, s)|_{B=1} \equiv \bar{T}_{\mathrm{Fourier}}(x, s)$ identically.
2. **Asymmetric Boundary Verification (`asymmetric_Bi_check.py`):** Tested asymmetric pairs $(Bi_0, Bi_L) \in \{(0.01, 0.10), (0.05, 0.20), (0.10, 0.50)\}$ across multiple interior points ($x = 0.0, 0.25, 0.50, 0.75, 1.0$) and pulse waveforms; analytical discrepancy is identically $0.00 \times 10^0$.
3. **Independent Numerical Solver (`numerical_check.py`):** An independent finite-difference solver reproduced the time-domain PDE solution within $L_\infty \le 1.02 \times 10^{-5}$ across all Biot numbers, with spatial grid refinement confirming second-order convergence ($p = 2.07 \to 2.32$).
4. **Independent Sensitivity & SVD Audit (`sensitivity_check.py`):** Verified $\rho = -1.0000000000$ ($|1+\rho| \le 2.22 \times 10^{-16}$), $R_J \sim 10^{-9}$, $\operatorname{cond}(F_{2\times 2}) \sim 10^{17}$, and clean subspace separation in the 3-parameter system $(\sigma_1 / \sigma_2 \in [2.34, 4.90]$, $\sigma_3 \sim 10^{-8}$, null vector projection error $< 10^{-15}$).

### Gate 2: Literature Novelty & Journal Fit Audit (NOVELTY PASS)
Seven audit reports were completed and committed in `paper11/audit/literature_final/`:
1. **Prior Art Demarcation:**
   - Both et al. (2016) [J. Non-Equilib. Thermodyn. 41, 41–48]: Observed the algebraic $B = 1$ resonance in adiabatic room-temperature pulse experiments; did not address boundary heat loss or parameter identifiability/sensitivity.
   - Kovács (2018) [Int. J. Heat Mass Transf. 127, 631–636]: Exact Laplace inversion of GK laser flash under strictly adiabatic conditions ($Bi = 0$); forward problem only.
   - Cowan (1963) & Cape–Lehman (1963): Classical Fourier heat-loss models with surface convection/radiation; no non-Fourier constitutive terms.
2. **Novelty Gap Certified:** No prior study in the literature has addressed whether boundary convective/radiative heat loss preserves or regularizes the Guyer--Krumhansl Fourier-resonance sensitivity collinearity.
3. **Journal Target:** *International Journal of Heat and Mass Transfer* (Primary Target) or *Journal of Non-Equilibrium Thermodynamics* (Alternative).

---

## Section B: Summary of Manuscript Enhancements

The manuscript files (`paper11/manuscript/main.tex`, `paper11/overleaf/main.tex`, and `paper11/manuscript/typst_manuscript.typ`) were updated with the following scientific enhancements:

1. **Qualified Priority Claims:** Replaced all absolute priority assertions with rigorous scientific phrasing: *"To the best of our knowledge, this work establishes the first rigorous proof that boundary convective and radiative heat loss cannot regularize the Guyer--Krumhansl Fourier-resonance sensitivity singularity."*
2. **Robin Boundary Sign Conventions:** Explicitly defined unit normal outward vectors ($-\hat{\bm{x}}$ at $x = 0$, $+\hat{\bm{x}}$ at $x = L$) and net boundary flux balances:
   $$q(0, t) = q_{\mathrm{laser}}(t) - h_0 [T(0, t) - T_0], \qquad q(L, t) = h_L [T(L, t) - T_0].$$
3. **Formal Statement of Theorem 1:** Explicitly stated all mathematical assumptions:
   - Linear 1D Guyer--Krumhansl model with constant bulk material properties.
   - Finite slab geometry $x \in [0, L]$.
   - Linear Robin convective/radiative boundary conditions with arbitrary non-negative Biot numbers $Bi_0, Bi_L \ge 0$.
   - Quiescent initial conditions ($T(x, 0) = T_0$, $q(x, 0) = 0$).
   - Admissible laser pulse excitation $q_{\mathrm{pulse}}(t)$.
   - Dynamic surface thermal conductivity operator collapse $\lambda_{\mathrm{eff}}(s) \equiv \lambda_0$.
4. **Dual Validation & Spatial Mesh Breakdown:** Integrated complete validation tables and explained that spatial grid refinement ($N_x \in \{100, 200, 400, 800\}$, $p = 2.07 \to 2.32$) confirms that the $N_x = 400$ grid discretization error ($6.80 \times 10^{-6}$) fully accounts for the minor remaining discrepancy observed against the continuous analytical Laplace inversion ($1.02 \times 10^{-5}$).
5. **Physical Nuances in Regularization Discussion:**
   - *Sample Thickness Tuning ($L$):* Clarified that for bulk materials with constant properties, $B \equiv \kappa^2 / (\alpha_0 \tau_q)$ is scale-invariant and independent of $L$. However, reducing $L$ shortens the diffusion timescale $t_{\mathrm{diff}} = L^2 / \alpha_0$, amplifying off-resonance sensitivity or activating size-dependent $\kappa(L)$ in nanolayers.
   - *Multi-Thickness Joint Inversion:* Clarified that at exact $B \equiv 1$, all thicknesses collapse identically to their Fourier curves; however, away from resonance ($B \ne 1$), joint inversion across multiple thicknesses provides powerful regularization against experimental noise.
   - *Contrast with Bulk Nonlinearity:* Contrasted boundary heat loss with high-fluence bulk nonlinearities ($\lambda(T) = \lambda_0(1 + \beta_T \theta)$), which create an internal spatial gradient $\alpha(x, t)$ that destroys the uniform resonance condition throughout the sample.
6. **Literature Citations:** Added full bibliographic entry for Both et al. (2016) with DOI (`10.1515/jnet-2015-0037`) across `references.bib` files and integrated it into the introduction.

---

## Section C: Artifact Verification and Integrity

| Artifact Path | Format | Status | Verification Details |
| :--- | :--- | :--- | :--- |
| `paper11/manuscript/main.tex` | LaTeX | Certified | Synchronized with all scientific revisions |
| `paper11/manuscript/references.bib` | BibTeX | Certified | 13 references, all DOIs verified |
| `paper11/manuscript/typst_manuscript.typ` | Typst | Certified | Compiles cleanly with Typst 0.10.0 |
| `paper11/manuscript/paper11_manuscript.pdf` | PDF | Certified | 13 pages, 1.6 MB, high-resolution figures |
| `paper11/overleaf/main.tex` | LaTeX | Certified | Exact duplicate of manuscript source |
| `paper11/overleaf/references.bib` | BibTeX | Certified | Exact duplicate of references |
| `paper11/overleaf/manuscript.pdf` | PDF | Certified | Standalone precompiled PDF copy |
| `Paper11_Overleaf_Ready.zip` | ZIP | Certified | Tested with `unzip -t`, 0 CRC errors |

---

## Section D: Final Decision

**FINAL DECISION: PASS**  
The research package for Paper 11 satisfies all mathematical, numerical, literature, and journal requirements. All assets are preserved under permanent repository standards on branch `arena/01a0e193-bfs-fem-matlab`.
