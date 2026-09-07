# FIGURE_DATA_TRACEABILITY.md (package version)

Every plotted numerical quantity traces to `results/raw/` (byte copies of the
accepted package). Script: `figures/make_all_figures.py`; styling:
`figures/style.py`; outputs: `figures/output/figN.pdf`.
No hand-entered result values; derived quantities are exact re-expressions
(difference, ratio, product, log10) — never fits.

| Figure | Script fn | Raw dataset | Columns/variables | Processing | Output |
|---|---|---|---|---|---|
| 1 | fig1() | none (code-drawn schematic) | — | vector drawing only | fig1.pdf |
| 2 | fig2() | v2_elastic_limit.csv; v3_model_limits.csv | kv pairs → markers; Omega,V_A,V_B,V_C_Dw14,V_C_rhow0,V_C_Dw0 → \|ΔV\|/V | abs ratio, log clip 1e-16 (display) | fig2.pdf |
| 3 | fig3() | study1_baseline.csv | model,Omega,V → (a); \|V_B−V_C\| → (b); model,Omega,P_w → (c) | abs difference; floors from resolution_bench.csv | fig3.pdf |
| 4 | fig4() | fig4_deltas.csv; resolution_bench.csv | Omega,Delta_BC,Delta_AC; eps_Delta | ratio to floor | fig4.pdf |
| 5 | fig5() | fig9b_map_dBC.npz | rows D_w*=1e-2,1,1e2,1e4 (grid idx 0/20/40/60): Omegas,V_B,V_C,dBC | χ=Ω*/D_w* relabelling | fig5.pdf |
| 6 | fig6() | fig6_tau.csv | Omega,tau0,Delta_T | x=τ0*Ω* relabelling (b) | fig6.pdf |
| 7 | fig7() | fig7_bc_summary.csv | Omega,dV_over_V_C,dPen_C | none | fig7.pdf |
| 8 | fig8() | fig8_roots.csv | model,Omega,Re_p,Im_p,admissible,grazing | none | fig8.pdf |
| 9 | fig9() | fig9b_map_dBC.npz | meshgrid(log Omegas, log Dws) vs V_B,V_C,log10 max(dBC,1e-16); Omega_c_ref | 3D surface rstride=1 + base contourf (render-only) | fig9.pdf |
| 10 | fig10() | fig9c_map_dT.npz | Omegas,taus,dT | log10 max(dT,1e-16); exact-cell pcolormesh; sample dots | fig10.pdf |
| 11 | fig11() | study1_baseline.csv | model,Omega,delta_pen; product Ω*δ* | none | fig11.pdf |

Hard-coded constants in the scripts (documented, non-data): axis/figure
limits, colours/line styles, 1e-16 display clip, grid-row indices
{0,20,40,60} (= exact grid values), and the legacy stage-6 record 0.934208
(documented in the upstream package `audit/IMPLEMENTATION_AUDIT.md`, shown
but excluded from conclusions). Grep `make_all_figures.py` for any validated
result value (0.31072662, 0.46630123, 0.9326028, 7.88e-5, 8.06e-6, …): zero
hits.

Captions exist only in `manuscript/FINAL_MANUSCRIPT.tex`; figure files
contain axes, ticks, legends, panel letters, and short scientific
annotations only.
