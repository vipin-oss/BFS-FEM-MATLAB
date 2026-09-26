# Figure Manifest — Paper 10

**Manuscript:** Dual-Phase-Lag (DPL) Thermoelastic Band-Gap Tuning and Acoustic Dissipation in 1D Periodic Metamaterials with Dipolar Gradient Elasticity  
**Resolution:** 300 DPI (Publication-Quality Raster PNG)  
**Total Figures:** 10 Figures  

---

| Fig. # | File Name | Manuscript Location & Caption | Source Data / Script | Resolution | Format |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **Fig. 1** | `fig1_baseline_dispersion.png` | Sec. 5.1, Page 9: Baseline Bloch dispersion diagram ($\Omega$ versus $k_r a / \pi$) for Family S1 (Conservative vs Active DPL). | `S1_results.csv` via `run_phase3b_production.py` | 300 DPI | PNG |
| **Fig. 2** | `fig2_baseline_attenuation.png` | Sec. 5.1, Page 9: Calibrated baseline spatial acoustic attenuation $\alpha a = \|k_i a\|$ versus normalized frequency $\Omega$ for Family S1. | `S1_results.csv` via `regenerate_calibrated_figures.py` | 300 DPI | PNG |
| **Fig. 3** | `fig3_material_contrast.png` | Sec. 5.2, Page 10: Material contrast sweep (Family S2) showing the emergence and evolution of Bragg band gaps across $\chi \in \{0.0, 0.5, 1.0\}$. | `S2_results.csv` via `run_phase3b_production.py` | 300 DPI | PNG |
| **Fig. 4** | `fig4_gradient_lengths.png` | Sec. 5.3, Page 11: Dipolar gradient-elastic length-scale sensitivity on continuous acoustic dispersion (Family S3): (a) $d_1/a$; (b) $\sqrt{c_1}/a$. | `S3_results.csv` via `regenerate_calibrated_figures.py` | 300 DPI | PNG |
| **Fig. 5** | `fig5_filling_fraction.png` | Sec. 5.4, Page 12: Filling fraction sweep (Family S4) illustrating the effect of layer thickness ratio $\eta = a_1/a$ on band-gap placement. | `S4_results.csv` via `run_phase3b_production.py` | 300 DPI | PNG |
| **Fig. 6** | `fig6_dpl_lags.png` | Sec. 5.5, Page 12: Dual-Phase-Lag (DPL) non-Fourier thermal time lags on continuous acoustic attenuation (Family S5): (a) $\tau_q$; (b) $\tau_\theta$. | `S5_results.csv` via `regenerate_calibrated_figures.py` | 300 DPI | PNG |
| **Fig. 7** | `fig7_thermoelastic_coupling.png` | Sec. 5.6, Page 13: Thermoelastic coupling intensity sensitivity and band-edge blunting (Family S6): (a) dispersion; (b) attenuation. | `S6_results.csv` via `regenerate_calibrated_figures.py` | 300 DPI | PNG |
| **Fig. 8** | `fig8_combined_interaction.png` | Sec. 5.7, Page 14: Factorial combined parameter interaction study (Family S7) across six distinct mechanism pairings. | `S7_results.csv` via `run_phase3b_production.py` | 300 DPI | PNG |
| **Fig. 9** | `fig9_bandgap_summary.png` | Sec. 5.8, Page 14: Authoritative Bragg band-gap summary (Family S2 and S4) with explicit open-boundary callout for Gap 2 at $\Omega = 1.80$. | `PRODUCTION_BANDGAP_SUMMARY.csv` via `regenerate_calibrated_figures.py` | 300 DPI | PNG |
| **Fig. 10** | `fig10_synthesis_map.png` | Sec. 5.8, Page 15: Scientific synthesis map demonstrating the tripartite decoupling among Bragg scattering, gradient dispersion, and DPL dissipation. | `S1_results.csv`, `S3_results.csv` via `regenerate_calibrated_figures.py` | 300 DPI | PNG |

---
*Note: All single-branch figures (Figs 2, 4, 6, 7, 10) use continuous propagating acoustic branch extraction (`extract_acoustic_branch`) directly from the frozen production records.*
