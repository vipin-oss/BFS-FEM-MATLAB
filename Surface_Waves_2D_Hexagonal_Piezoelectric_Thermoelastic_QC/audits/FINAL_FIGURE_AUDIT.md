# FINAL_FIGURE_AUDIT.md — Task 13 (presentation upgrade)

Audit date: 2026-09-07. Scope: every curve plotted in `submission/figures_pub/*.pdf`
(regenerated this task) was traced to its raw data and scanned for spikes, kinks,
jumps, branch-switching, and conditioning artifacts. **No data was hidden,
smoothed, deleted, or cropped.** Regeneration script:
`submission/make_figures_publication.py` (reads `study1_surface_waves/results/`
read-only; identical datasets to the accepted figures; captions live in
`FINAL_MANUSCRIPT.tex` only).

## 1. Lineage (raw data → script → figure → TEX caption)

| Figure PDF | Raw source (read-only) | Plotted quantity |
|---|---|---|
| fig1_schematic.pdf | hand-drawn schematic (no data) | geometry/fields |
| fig2a_elastic_limit.pdf | v2_elastic_limit.csv | velocity ratios (V2) |
| fig2b_model_limits.pdf | v3_model_limits.csv | \|ΔV\|/V limit reproduction (V3) |
| fig3_baseline_dispersion.pdf | study1_baseline.csv | V*(Ω*) per model |
| fig4_baseline_deltas.pdf | fig4_deltas.csv | Δ_BC, Δ_AC + ε_Δ floor |
| fig5_friction_1d.pdf | fig5_friction1d.csv | V*(Ω*) and Δ_BC at 3 D_w* slices |
| fig6_thermal.pdf | fig6_tau.csv | Δ_T(Ω*) per τ0* |
| fig7_phason_bc.pdf | fig7_bc_summary.csv | \|ΔV\|/V clamped vs free (C) |
| fig8_depth_roots.pdf | fig8_roots.csv | depth roots (Re p, Im p) 3×3 |
| fig8b_penetration.pdf | fig8_roots_summary.csv | δ*=1/\|Im p\|(Ω*) |
| fig9a_V_maps.pdf | fig9b_map_dBC.npz (V_B,V_C,Omega_c_ref) | V*(Ω*,D_w*) maps |
| fig9b_dBC_map.pdf | fig9b_map_dBC.npz (dBC) | log10 Δ_BC map |
| fig9c_dT_map.pdf | fig9c_map_dT.npz (dT) | log10 Δ_T map |

## 2. Automated scan (run 2026-09-07, this turn)

Method: per-curve consecutive-point relative step \|ΔV/V\|, NaN census,
root-count consistency (n_ad, n_grazing), condition numbers, map finiteness
and log-step smoothness. Threshold for flagging: 5×10⁻³ relative step.

| Dataset | Result |
|---|---|
| baseline A/B/C (121 pts each) | max step 2.578e-8 (A), 2.570e-6 (B/C); 0 NaN; n_ad=5, n_grazing=0 everywhere; cond(B) ≤ 5.06e10 (A) |
| v3 limits: V_A,V_B,V_C,V_C_Dw14,V_C_rhow0 | max step ≤ 5.4e-6; 0 NaN |
| v3 limits: V_C_Dw0 (frozen 1e-8 curve) | max step 5.422e-3 at Ω*=1e-3 — FLAGGED, see F1 |
| fig5, 9 slices (61 pts) | max step 4.3e-8 (A), 2.6e-4 (B/C at D_w*=1); 0 NaN |
| fig6, 5 τ curves (121 pts) | 0 NaN; max Δ_T 7.88e-5 (τ0*=1e-1); 17–30 sign reversals in Δ_T(Ω*) — see F3 |
| fig7 | dV/V_C ∈ [8.2e-12, 8.06e-6]; dV/V_A ∈ [7.5e-2, 4.1e-1] |
| fig8 roots (90 rows) | 10 roots per panel; admissible 42; residual max 5.996e-17 (admissible); NaN residual on 48 excluded roots — see F4; 6 grazing (model A) — see F4 |
| maps V_B/V_C/dBC (61×61) | all finite; V_C max log-step 1.1e-4 (smooth); dBC max 4.998e-3 |
| map dT (5×121) | all finite; max 7.879e-5 |
| resolution_bench | u_V=1.13e-9, ε_Δ=1.1299e-8 |

## 3. Flagged features — classification and disposition

**F1. Frozen 1e-8 evidence curve (Fig. 2b, dashed).** Max relative step 5.4e-3
between the first two points (Ω*=1e-3, 3e-3), with |V_C(D_w*=1e-8)−V_A|/V_A
reaching 3.107e-2 at Ω*=1e-3 and decaying to ≤1e-6 above. Classification:
**physical/singular limit** — as D_w*→0 the phason diffusion channel closes and
the C system approaches the degenerate A structure; at any *finite* friction the
approach is non-uniform at low Ω*. This curve is the documented singular-limit
evidence required by the freeze decision (kept deliberately, dashed, not
gated). Explained in the caption and §5; not hidden, not cropped.

**F2. Flat 1e-16 line in Fig. 6 (τ0*=4.3462e-3 curve).** Δ_T is identically
zero for this curve because τ0*=4.3462e-3 **is** the reference relaxation time
(Δ_T ≡ |V(τ0*)−V(τ_ref*)|/V(τ_ref*) with τ0*=τ_ref*). The plotted line is the
1e-16 display clip. Classification: **plotting convention**; stated in the
caption so the flat line is not mistaken for a numerical failure.

**F3. Non-monotonicity of Δ_T(Ω*) (17–30 sign reversals per τ curve).**
Continuous, small-amplitude oscillation about zero arising from the
interference between the thermoelastic and mechanical contributions as the
thermal penetration scale crosses the surface-wave scale. Classification:
**physical** (no step exceeds 1e-5 in Δ_T; curves are continuous).

**F4. NaN residuals and grazing flags in fig8_roots.csv.** Residuals are
recorded for admissible roots only (max 5.996e-17); the 48 excluded roots carry
NaN residuals by the logging convention, and 6 roots (all model A) are flagged
grazing near the V<√K3* degenerate region of model A. Classification:
**solver/logging convention, documented degeneracy** — excluded roots are
plotted as crosses, grazing as open squares; the admissible set (5 per panel
for the reported branch analysis) is unaffected. Stated in the Fig. 8 caption.

**F5. Legacy coarse-scan point in Fig. 2a (x=5).** The value 0.934208 is a
search-limited record from the exploratory stage-6 scan, superseded by the
production value v_R/v_S = 0.9326028. The point is **kept** (data not deleted)
with a neutral label ("excluded coarse-scan record") and is discussed in §5.
Classification: **branch-tracking artifact of the coarse exploratory scan**,
documented in the manuscript.

**F6. Ω_c reference line in Figs. 9a/9b.** Ω_c = D_w*/ρ_w* is plotted as a
reference line only; no phase transition or crossover is claimed at it in the
baseline window (Ω_c/ω0 ≈ 11467.5 lies far outside the scanned nondimensional
window in the dimensional sense). Classification: **reference annotation**.

**F7. Condition number growth (model A).** cond(B) reaches 5.06e10 for model A
at high Ω*, consistent with the documented degeneracy of the A branch
(√K3* = 0.3162 barrier); all reported A values passed the residual gate
(≤3.27e-9). Classification: **conditioning, documented and gated**.

## 4. Conclusion

No unexplained spike, kink, jump, or branch-switching artifact remains in any
plotted curve. All flagged features are physical singular-limit behaviour,
documented degeneracies, or plotting conventions, and each is explained at its
point of use in the manuscript. Figures regenerated this task preserve the
underlying numerical data exactly (same files, same quantities, same axis
variables as the accepted figures).
