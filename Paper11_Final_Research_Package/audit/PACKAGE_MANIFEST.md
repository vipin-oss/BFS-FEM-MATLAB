# Package Manifest: Paper 11 Research Package

**Title:** Invariance of the Guyer–Krumhansl Fourier-Resonance Sensitivity Singularity to Boundary Heat Loss in Laser Flash Testing  
**Author:** Vipin Gupta (Gurugram University)  
**Package:** `Paper11_Final_Research_Package/`  
**Date:** September 2026  

---

## Complete File Manifest

| Relative Path | File Purpose | Required for Reproduction? | Required for Overleaf? |
| :--- | :--- | :---: | :---: |
| `README.md` | Primary package overview, quick start, status | No | No |
| `OVERVIEW.md` | Comprehensive scientific summary and findings | No | No |
| **`manuscript/`** | | | |
| `manuscript/main.tex` | Authoritative publication LaTeX source | No | No |
| `manuscript/references.bib` | Complete BibTeX bibliography (13 items, DOIs) | No | No |
| `manuscript/paper11_manuscript.pdf` | Certified precompiled 13-page publication PDF | No | No |
| `manuscript/elsarticle-num.bst` | Standard BibTeX style file | No | No |
| **`overleaf/`** | | | |
| `overleaf/main.tex` | Isolated root LaTeX document for Overleaf | No | **Yes** |
| `overleaf/references.bib` | Isolated BibTeX references for Overleaf | No | **Yes** |
| `overleaf/README.md` | Overleaf compilation instructions | No | **Yes** |
| `overleaf/manuscript.pdf` | Standalone compiled reference PDF | No | **Yes** |
| `overleaf/elsarticle-num.bst` | Local BibTeX style file for standalone compilation | No | **Yes** |
| `overleaf/figures/fig1_heatloss_temperature_response.pdf` | Figure 1 vector PDF | No | **Yes** |
| `overleaf/figures/fig1_heatloss_temperature_response.png` | Figure 1 raster PNG | No | **Yes** |
| `overleaf/figures/fig2_sensitivity_profiles_collinearity.pdf` | Figure 2 vector PDF | No | **Yes** |
| `overleaf/figures/fig2_sensitivity_profiles_collinearity.png` | Figure 2 raster PNG | No | **Yes** |
| `overleaf/figures/fig3_invariance_metrics_vs_biot.pdf` | Figure 3 vector PDF | No | **Yes** |
| `overleaf/figures/fig3_invariance_metrics_vs_biot.png` | Figure 3 raster PNG | No | **Yes** |
| `overleaf/figures/fig4_singular_spectrum_and_canyon.pdf` | Figure 4 vector PDF | No | **Yes** |
| `overleaf/figures/fig4_singular_spectrum_and_canyon.png` | Figure 4 raster PNG | No | **Yes** |
| `overleaf/figures/fig5_validation_dual_benchmarks.pdf` | Figure 5 vector PDF | No | **Yes** |
| `overleaf/figures/fig5_validation_dual_benchmarks.png` | Figure 5 raster PNG | No | **Yes** |
| **`program/`** | | | |
| `program/README.md` | Program documentation and execution guide | **Yes** | No |
| `program/requirements.txt` | Python package dependency specifications | **Yes** | No |
| `program/solver_gk_heatloss.py` | 1D staggered-grid BDF numerical solver | **Yes** | No |
| `program/analytic_laplace.py` | Analytical Laplace transforms & de Hoog inversion | **Yes** | No |
| `program/run_validation.py` | Dual benchmark validation runner | **Yes** | No |
| `program/run_heatloss_study.py` | Parameter sweep & sensitivity calculator | **Yes** | No |
| `program/plot_figures.py` | Publication figure generator | **Yes** | No |
| `program/reproduce_all.py` | Master automated reproduction runner | **Yes** | No |
| **`data/`** | | | |
| `data/validation_laplace.csv` | Laplace benchmark comparison data table | **Yes** | No |
| `data/validation_cowan.csv` | Cowan Fourier limit benchmark data table | **Yes** | No |
| `data/mesh_convergence.csv` | Spatial grid refinement convergence data table | **Yes** | No |
| `data/heatloss_parameter_sweep.csv` | Primary Biot sweep and SVD spectrum table | **Yes** | No |
| `data/off_resonance_sweep.csv` | Off-resonance singularity canyon table | **Yes** | No |
| `data/sensitivity_profiles.csv` | Time-resolved sensitivity profiles series | **Yes** | No |
| **`figures/`** | | | |
| `figures/fig1_heatloss_temperature_response.pdf` | Figure 1 vector PDF | **Yes** | No |
| `figures/fig1_heatloss_temperature_response.png` | Figure 1 raster 300-DPI PNG | **Yes** | No |
| `figures/fig2_sensitivity_profiles_collinearity.pdf` | Figure 2 vector PDF | **Yes** | No |
| `figures/fig2_sensitivity_profiles_collinearity.png` | Figure 2 raster 300-DPI PNG | **Yes** | No |
| `figures/fig3_invariance_metrics_vs_biot.pdf` | Figure 3 vector PDF | **Yes** | No |
| `figures/fig3_invariance_metrics_vs_biot.png` | Figure 3 raster 300-DPI PNG | **Yes** | No |
| `figures/fig4_singular_spectrum_and_canyon.pdf` | Figure 4 vector PDF | **Yes** | No |
| `figures/fig4_singular_spectrum_and_canyon.png` | Figure 4 raster 300-DPI PNG | **Yes** | No |
| `figures/fig5_validation_dual_benchmarks.pdf` | Figure 5 vector PDF | **Yes** | No |
| `figures/fig5_validation_dual_benchmarks.png` | Figure 5 raster 300-DPI PNG | **Yes** | No |
| **`derivations/`** | | | |
| `derivations/derivations.md` | Complete analytical proofs and modal derivations | No | No |
| **`blueprint/`** | | | |
| `blueprint/BLUEPRINT.md` | Formal mathematical specification & architecture | No | No |
| **`audit/`** | | | |
| `audit/PACKAGE_MANIFEST.md` | This manifest document | No | No |
| `audit/FINAL_SCIENTIFIC_CHANGE_REPORT.md` | Master record of audits, revisions & decisions | No | No |
| `audit/validation_audit.md` | Signed scientific validation certificate | No | No |
| `audit/reproducibility_final.md` | Reproducibility protocol & verification report | No | No |
| `audit/independent_audit/README.md` | Independent audit suite guide | No | No |
| `audit/independent_audit/derivation_check.py` | SymPy analytical proof verification script | No | No |
| `audit/independent_audit/numerical_check.py` | Independent solver verification script | No | No |
| `audit/independent_audit/asymmetric_Bi_check.py` | Asymmetric Biot number verification script | No | No |
| `audit/independent_audit/sensitivity_check.py` | Independent sensitivity & SVD verification | No | No |
| `audit/independent_audit/numerical_check_results.csv` | Independent numerical solver output | No | No |
| `audit/independent_audit/sensitivity_audit_results.csv` | Independent sensitivity metrics output | No | No |
| `audit/independent_audit/off_resonance_audit_results.csv` | Independent off-resonance sweep output | No | No |
| `audit/independent_audit/literature_novelty.md` | Independent novelty verification record | No | No |
| `audit/independent_audit/final_verdict.md` | Gate 1 signed audit verdict (PASS) | No | No |
| `audit/literature_final/README.md` | Literature audit suite guide | No | No |
| `audit/literature_final/literature_search_log.md` | Literature query log and retrieval records | No | No |
| `audit/literature_final/prior_art_table.md` | Exhaustive prior art comparison matrix | No | No |
| `audit/literature_final/novelty_gap.md` | Formal novelty demarcation report | No | No |
| `audit/literature_final/journal_fit.md` | Target journal alignment & criteria audit | No | No |
| `audit/literature_final/experimental_claim_audit.md` | Experimental boundary audit report | No | No |
| `audit/literature_final/final_novelty_verdict.md` | Gate 2 signed novelty verdict (PASS) | No | No |
