# FINAL PRODUCTION REPORT — Task 13 (presentation upgrade)

Date: 2026-09-07. Baseline: Task-12 production (21 pp). Scope: manuscript
enhancement only — literature, figure presentation, physical interpretation,
journal-quality structure. Science frozen; no new simulations.

# 1. Status

COMPLETE. FINAL_MANUSCRIPT.{tex,pdf,bib} rebuilt at presentation quality;
all Task-13 deliverables written (see submission/ listing in the checklist).

# 2. Length and structure (P2, P3, P19, P27)

- Total length: **30 pages** (target 26–30).
- Introduction: pages 2–5 (~3 pp), subsections 1.1–1.5 with the 15-point
  progression (QC continuum → phonon/phason → phason dynamics relevance →
  inertial/diffusive/telegraph → dynamic QC theories → piezoelectric QC →
  thermoelasticity/LS → anisotropic surface waves → known QC waves → known
  piezo/thermo QC → 2D-hex gap → methodology → contributions → scope →
  roadmap). Slightly above the ~2-pp guide because the verified bibliography
  grew to 47 entries; no filler content — each paragraph states what it
  establishes and why it matters here.
- Discussion: §7.1–7.9 (~2.7 pp), mechanism-based (P9, P15–P17): branch
  selection; model A = phason kinetic-energy channel (V*≈0.3107 is 1.7% below
  √K3*, near-grazing degeneracy linked); model B = slaved dissipative phasons
  (P_w ≤ 1.8×10⁻⁵, no independent inertia, degree-count argument); model C =
  Ω/Ω_c competition with the sweep-boundary/material-crossover distinction;
  thermal smallness via T0β1*≈2.3×10⁻³ and τ0*Ω*≳1; phason BC physics;
  penetration structure; 1D-vs-2D comparison; limitations.
- Conclusions: 6 items, each result + physical meaning + modelling implication.

# 3. References (P4, P5, P23)

- **47 entries** (18 retained + 29 new), all verified by web search this
  session or in the Task-10 Crossref audit; tiers and unverified-field flags
  in FINAL_REFERENCE_AUDIT.md. Target "≈55" not reached deliberately: no
  padding references were added (P4 forbids counting-driven additions).
- Corrections made during verification: Fan & Mai = AMR 57:325–343 (2004)
  (not 56:549, 2003); Lubensky–Ramaswamy–Toner = PRB 32:7444 (not PRL).
- Rejected unverifiable candidates: Socolar 1991; Abe 2000; Results-in-Physics
  60 (2024) (conflicting article numbers); Crystals 14:170 (authors
  unconfirmed); Chadwick & Windle 1964 (replaced by verified Chadwick & Seet
  1970).
- Script check: 0 orphan bibitems, 0 undefined cite keys, 0 duplicates.
- 1D-hex vs 2D-hex distinction enforced at every citation site (P5).

# 4. Figures (P10–P13, P26)

| Fig | File (figures_pub/ unless noted) | Raw source | Caption-only-in-tex |
|---|---|---|---|
| 1 | figures/fig1_schematic.pdf | schematic (no data) | yes |
| 2a | fig2a_elastic_limit.pdf | v2_elastic_limit.csv | yes |
| 2b | fig2b_model_limits.pdf | v3_model_limits.csv | yes |
| 3 | fig3_baseline_dispersion.pdf | study1_baseline.csv | yes |
| 4 | fig4_baseline_deltas.pdf | fig4_deltas.csv | yes |
| 5 | fig5_friction_1d.pdf | fig5_friction1d.csv | yes |
| 6 | fig6_thermal.pdf | fig6_tau.csv | yes |
| 7 | fig7_phason_bc.pdf | fig7_bc_summary.csv | yes |
| 8 | fig8_depth_roots.pdf | fig8_roots.csv | yes |
| 8b | fig8b_penetration.pdf | fig8_roots_summary.csv | yes |
| 9a | fig9a_V_maps.pdf | fig9b_map_dBC.npz | yes |
| 9b | fig9b_dBC_map.pdf | fig9b_map_dBC.npz | yes |
| 9c | fig9c_dT_map.pdf | fig9c_map_dT.npz | yes |

# 5. Suspicious features (P10) — scanned and classified

| ID | Feature | Classification | Disposition |
|---|---|---|---|
| F1 | fig2b frozen 1e-8 curve, 5.4e-3 step / 3.1e-2 max at Ω=1e-3 | physical singular limit (non-uniform D_w→0) | kept, dashed, explained |
| F2 | fig6 flat 1e-16 line (τ*=4.346e-3) | plotting clip of Δ_T≡0 (reference τ) | kept, captioned |
| F3 | fig6 17–30 sign reversals per curve | physical interference | kept, explained §6.5 |
| F4 | fig8 48 NaN residuals + 6 grazing (model A) | logging convention + documented degeneracy | kept, captioned; admissible residuals ≤6.0e-17 |
| F5 | fig2a legacy record 0.934208 | coarse-scan root-tracking artefact | kept, neutral label, excluded from conclusions |
| F6 | fig9 Ω_c line | reference annotation | labelled "reference line only" |
| F7 | cond(B)≤5.1e10 (model A) | conditioning, documented | gated by residuals (≤3.27e-9) |

No spike, kink, jump, or branch switch elsewhere: max curve step 2.6e-6
(baseline/limits), 2.6e-4 (D_w*=1 slices); maps smooth (max log-step 1.1e-4).
No data hidden, smoothed, deleted, or cropped.

# 6. Scientific preservation — PASS

Every equation, parameter value, gate, threshold, and numerical claim carried
over verbatim from the frozen Task-12 text (diffed section-by-section while
rewriting): Ω_c/ω0≈11467.5 reference-line-only; no crossover claim in the
baseline window; 95/121 + 91/121 footnote; E2 convention; model-A clamped
degeneracy handling; k11 6-vs-5.3 disclosure; surrogate labels; u_V=1.13e-9 /
ε_Δ=1.1299e-8 floors; all Study 1–3 numbers unchanged. No new simulations;
package ZIP sha256 unchanged (`b8178605…c4244ec2` re-verified this session);
git history untouched.

# 7. LaTeX quality — PASS

pdflatex ×2, rc=0, **0 errors, 0 LaTeX warnings**, no overfull box ≥10 pt,
30 pages, 13 figures embedded, all citations resolved. Placeholders
(authors/funding/archive ID) clearly marked as required.

# 8. Remaining author inputs

Author block (names/affiliations/ORCID/email), funding and conflict-of-interest
statements, author contributions, public archive identifier, publisher class
file at portal submission.

# 9. Final Verdict

🟢 **MANUSCRIPT READY FOR FINAL SUBMISSION** (figures scientifically and
visually ready; pending only the author-input placeholders listed in §8).

# 10. Task 14 — figure redesign (2026-09-07)

- Figure set 13 → 11 (merged 2a+2b; 9c → Fig. 10; 8b → Fig. 11; old Fig. 12
  role absorbed into Fig. 7(b)). Script: `figures_v2/make_figures_v2.py`.
- Fig. 1 redrawn without embedded title/caption text; Figs. 2–8, 10, 11
  upgraded to multi-panel professional layouts; Fig. 9 is now a genuine 3D
  representation (V_B, V_C, log10 Δ_BC surfaces + base-plane contour
  projections; z-axes span exactly the data ranges; Ω_c base reference line
  labelled "reference only — no claimed transition").
- Consistent visual language: A vermilion solid / B blue dashed / C green
  dash-dot everywhere; D_w* by colour, model by line style; viridis/magma
  maps; floors dotted; sub-floor shaded; panel letters; serif mathtext;
  grayscale-safe.
- New information extracted from EXISTING data only: χ=Ω*/Ω_c collapse
  (Fig. 5c), |V_B−V_C| vs absolute floor (Fig. 3b), ΔBC/floor unity criterion
  (Fig. 4b), Δ_T(τ0*Ω*) merged branch (Fig. 6b), δ* change under clamping
  (Fig. 7b), Ω*δ*≈const localisation check (Fig. 11b).
- Spike/anomaly audit (SPIKE_AND_ANOMALY_AUDIT.md): all large relative steps
  occur in derived difference quantities at sign-nodes/roundoff cancellation
  (underlying V* curves smooth: max step 2.6e-6 baseline, 2.6e-4 slices);
  classified and kept with explanation; no smoothing/deletion; no
  interpolation added features (3D/heatmaps render the exact grids).
- Deliverables added: FIGURE_REDESIGN_AUDIT.md,
  FIGURE_DATA_TRACEABILITY.md, SPIKE_AND_ANOMALY_AUDIT.md; changelog updated.
- Layout: 30 pp (within 26–30), figures within one page of first citation,
  captions attached; 0 errors / 0 warnings.

# 11. Superseded Task-13 verdict (record)

🟢 MANUSCRIPT READY FOR FINAL SUBMISSION (Task-13 state).
