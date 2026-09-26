# Phase 4: Scientific Traceability Matrix

**Author:** Arena.ai Builder (Independent Research Engine)  
**Date:** 2026-09-26  
**Document ID:** P10-MAT-MS-01  
**Status:** FULLY TRACEABLE & VERIFIED  
**Governing Baseline:** `RESEARCH_BLUEPRINT.md` (v1.2 `1ed2d54`), Phase 3B Baseline (`5622c7b`)  

---

## 1. Executive Summary

This Traceability Matrix maps every equation, parameter, numerical value, validation claim, and figure in the manuscript (*“Dual-Phase-Lag (DPL) Thermoelastic Band-Gap Tuning and Acoustic Dissipation in 1D Periodic Metamaterials with Dipolar Gradient Elasticity”*) to its exact origin in the frozen scientific repository.

**Core Principle:** Zero invented data, zero unverified claims, zero circular derivations.

---

## 2. Complete Component-to-Source Mapping

| Manuscript Component | Topic / Content | Exact Archival Source Path | Verified File SHA / Commit |
| :--- | :--- | :--- | :--- |
| **Title & Scope** | DPL thermoelasticity + dipolar gradient metamaterials | `paper10/blueprint/RESEARCH_BLUEPRINT.md` (Sec. 1) | `1ed2d54` |
| **Eq. (1) Momentum** | Mindlin Form-II gradient elastodynamics PDE | `paper10/derivations/PHASE1_DERIVATION.md` (Sec. 1.1) | `e9ca21f` |
| **Eq. (2) DPL Energy** | Dual-Phase-Lag energy equation with coupling | `paper10/derivations/PHASE1_DERIVATION.md` (Sec. 1.2) | `e9ca21f` |
| **Eq. (3)–(4) Tractions** | Generalized monopolar $P_k$ and dipolar $R_k$ tractions | `paper10/derivations/PHASE1_DERIVATION.md` (Sec. 2.2, 2.3) | `e9ca21f` |
| **Eq. (5) Effective Cond.** | Complex frequency-dependent conductivity $k_{\text{eff}}(\omega)$ | `paper10/derivations/PHASE1_DERIVATION.md` (Eq. 3.1) | `e9ca21f` |
| **Eq. (6) State Vector** | 10-state in-plane vector $\mathbf{V}_{10} = [u_x, u_y, u_{x,x}, u_{y,x}, \theta, P_x, P_y, R_x, R_y, Q_x]^T$ | `paper10/derivations/PHASE1_DERIVATION.md` (Sec. 6.1) | `e9ca21f` |
| **Eq. (7) Transfer Matrix** | Modal transfer matrix $T_j = P_j G_j P_j^{-1}$ & $T_{\text{cell}} = T_B T_A$ | `paper10/derivations/PHASE1_DERIVATION.md` (Sec. 6.3) | `e9ca21f` |
| **Eq. (8) Generalized Eigen** | Interface matching pencil $A \mathbf{C} = \lambda B \mathbf{C}$ | `paper10/solver/coupled10.py`, `run_phase3b_production.py` | `ee61a02`, `5622c7b` |
| **Eq. (9) Bloch Multiplier** | Complex Bloch relation $\lambda = e^{i k_x a}, k_x = k_r + i k_i$ | `paper10/derivations/PHASE1_DERIVATION.md` (Sec. 6.4) | `e9ca21f` |
| **Conservative Limit** | $\beta \to 0$ is uncoupled mechanical conservative limit ($\det(T_{\text{mech}})=1$) | `paper10/audit/decisions/PHASE1_DERIVATION_DECISIONS.md` | `e9ca21f` |
| **Validation Benchmark** | Papargyri-Beskou (2009) Eq. 28 reproduced to $2.45 \times 10^{-15}$ | `paper10/validation/benchmark_papargyri_beskou_results.csv` | `ee61a02` |
| **Secondary Benchmark** | Classical phononic crystal band gaps (Li et al. 2016 Acta Mech) | `paper10/validation/PHASE2_BENCHMARK.md` | `ee61a02` |
| **Symplecticity Limit** | $|\det(T) - 1| = 2.66 \times 10^{-13}$ for conservative 2-layer cell | `paper10/validation/periodic_pilot_results.json` | `ee61a02` |
| **Material Parameters** | Epoxy (Layer A) and Aluminum (Layer B) baseline properties | `paper10/production/PHASE3_PARAMETER_MATRIX.md` (Sec. 1) | `add1a8e` |
| **Production Sweeps S1–S7** | 36 parameter cases, 100 frequency steps $\Omega \in [0.05, 1.80]$ | `paper10/production/PHASE3_PARAMETER_MATRIX.json` | `add1a8e` |
| **Equilibrated Condition #** | $\kappa(P_{\text{equil}}) \le 22.72$ (baseline), $\le 4648.99$ (classical limit) | `paper10/audit/PHASE3B_TARGETED_SCIENTIFIC_AUDIT.md` | `9ed2347`, `5622c7b` |
| **Evanescent Filtering** | 223 modes filtered in `S3_classical` due to float64 underflow ($|\lambda| < 10^{-15}$) | `paper10/audit/PHASE3B_POST_CORRECTION_AUDIT.md` | `5622c7b` |
| **Residual Floor** | Numerical noise floor $\alpha a \approx 1.67 \times 10^{-5}$ vs DPL dissipation $\alpha a \sim 10^{-4}-10^{-2}$ | `paper10/production/PHASE3B_PRODUCTION_REPORT.md` (Sec. 4) | `5622c7b` |
| **Band Gap Summary** | 64 total records: 41 closed gaps, 23 open boundary-truncated gaps | `paper10/production/results/PRODUCTION_BANDGAP_SUMMARY.csv` | `5622c7b` |
| **Baseline Gap 1** | Closed Bragg gap at $\Omega \in [0.6687, 0.7040]$ ($\Delta\Omega = 0.0354$) | `PRODUCTION_BANDGAP_SUMMARY.csv` (row 2) | `5622c7b` |
| **Baseline Gap 2** | Open Bragg gap at $\Omega_L = 1.3051$, `is_boundary_truncated = True` | `PRODUCTION_BANDGAP_SUMMARY.csv` (row 3) | `5622c7b` |
| **Identical Layers Limit** | $\chi = 0$: Bragg gap width $\Delta\Omega \equiv 0.0000$ (gradient dispersion active) | `PRODUCTION_BANDGAP_SUMMARY.csv` (row 4) | `5622c7b` |
| **Figure 1** | Baseline Bloch dispersion (multi-branch scatter) | `paper10/figures/phase3b/fig1_baseline_dispersion.png` | `5622c7b` |
| **Figure 2** | Calibrated baseline spatial attenuation ($\alpha a$ vs $\Omega$) | `paper10/figures/phase3b/fig2_baseline_attenuation.png` | `5622c7b` |
| **Figure 3** | Material contrast sweep ($\chi \in [0.0, 0.5, 1.0]$) | `paper10/figures/phase3b/fig3_material_contrast.png` | `5622c7b` |
| **Figure 4** | Calibrated gradient length scales ($d_1/a$ and $\sqrt{c_1}/a$) | `paper10/figures/phase3b/fig4_gradient_lengths.png` | `5622c7b` |
| **Figure 5** | Layer thickness filling fraction ($\eta \in [0.2, 0.5, 0.8]$) | `paper10/figures/phase3b/fig5_filling_fraction.png` | `5622c7b` |
| **Figure 6** | Calibrated DPL thermal relaxation ($\tau_q$) and retardation ($\tau_\theta$) | `paper10/figures/phase3b/fig6_dpl_lags.png` | `5622c7b` |
| **Figure 7** | Calibrated thermoelastic coupling intensity ($\alpha_t$) | `paper10/figures/phase3b/fig7_thermoelastic_coupling.png` | `5622c7b` |
| **Figure 8** | Factorial combined parameter interactions (6 panels) | `paper10/figures/phase3b/fig8_combined_interaction.png` | `5622c7b` |
| **Figure 9** | Calibrated band-gap summary plot with open-gap callout | `paper10/figures/phase3b/fig9_bandgap_summary.png` | `5622c7b` |
| **Figure 10** | Calibrated tripartite synthesis map | `paper10/figures/phase3b/fig10_synthesis_map.png` | `5622c7b` |

---

## 3. Strict Prohibitions & Verification Checkpoints

- **Prohibition 1 (No Invented Data):** Every numerical value in the manuscript text and tables matches the CSV datasets in `paper10/production/results/` to 4 significant digits.
- **Prohibition 2 (No Conflation of DPL Attenuation with Bragg Gaps):** Bragg gaps are defined strictly by real dispersion evanescent cutoffs ($\alpha a \gg 1$); DPL attenuation is defined as irreversible thermodynamic dissipation across pass bands ($\alpha a \sim 10^{-4}-10^{-2}$).
- **Prohibition 3 (No False Band-Gap Closures):** Gaps terminating at $\Omega = 1.8000$ are explicitly documented as open band gaps truncated by the upper boundary of the simulation window.
- **Prohibition 4 (Accurate Limiting Nomenclature):** The uncoupled limit $\beta \to 0$ is never called "isothermal".
- **Prohibition 5 (Conditioning Precision):** Equilibrated condition numbers ($\kappa \le 22.72$) are reported as the solver health metric, while raw dimensional values ($10^{15}-10^{20}$) are explained as SI unit artifacts.
