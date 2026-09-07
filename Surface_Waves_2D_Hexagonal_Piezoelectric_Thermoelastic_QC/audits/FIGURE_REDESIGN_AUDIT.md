# FIGURE_REDESIGN_AUDIT.md — Task 14 (final visual audit)

Visual language (consistent, grayscale-safe): model A = vermilion solid,
B = blue dashed, C = green dash-dot (same in every figure); D_w* levels =
four distinct colours (orange/sky/purple/grey) with model shown by line
style; τ0* levels = viridis ramp; maps/surfaces = viridis or magma
(perceptual, no rainbow); floors always dotted black; sub-floor regions
grey-shaded; panel letters (a)(b)(c) outside top-left; serif mathtext
throughout; no embedded captions/titles.

Per-figure audit (Part-25 questions: necessary / readable / enough info /
more informative than before / meaningful curves / traceable / spikes
explained / 3D justified / conventions consistent / caption only in TEX /
text explains physics):

| Fig | Old form | New form | Q1–Q11 verdict |
|---|---|---|---|
| 1 | raster-like schematic WITH embedded title+paragraph | clean continuum-mechanics schematic: half-space, triad, decay envelope, δ* bracket, BC line, fields/model box; no embedded caption | all pass; embedded text removed (violation fixed) |
| 2 | two separate figures; overlapping annotations (2a) | single 2-panel: compact benchmarks + gates with roundoff band; legend/labels de-cluttered | all pass |
| 3 | one flat 2-curve plot | 3 panels: branch identity / absolute B–C separation vs floor / P_w mode character | reader now sees WHY A differs |
| 4 | ΔBC+ΔAC with floor | 3 panels: ΔBC / ΔBC÷floor (unity criterion) / ΔAC (1.4e7×floor) | distinguishes indistinguishable/resolvable/separated without arbitrary thresholds |
| 5 | 9 overlapping curves + blank panel (a) | 3 panels: B/C V* at 4 D_w* (2 colourschemes+styles) / ΔBC / χ-collapse master curve | new info: χ organises the separation |
| 6 | 5-curve plot, reference dominated | 2 panels: Δ_T(Ω*) + Δ_T(τ0*Ω*) merged-branch evidence; reference shown as clip note | new info: relaxation-controlled collapse |
| 7 | single sparse curve | 2 panels: speed change + penetration-depth change; model-A statement as figure note | BC physics visible; degenerate A values NOT plotted |
| 8 | nine tiny panels, shared clutter | enlarged 3×3, per-panel scaling, unified markers, single legend | readable clusters |
| 9 | two flat 2D heatmaps | TRUE 3D: V_B, V_C surfaces + base contours; log10 Δ_BC surface with plateau/front/skirt; Ω_c base reference dashed "reference only" | 3D justified (two swept params); z-ranges exact (no exaggeration); skirt explained |
| 10 | discrete-band heatmap | heatmap on exact 5×121 grid + sample dots; no interpolation; reference row noted | traceable |
| 11 | 3-point penetration curves | 2 panels: 121-pt δ*(Ω*) + Ω*δ*≈const (1.99 / 1.29) scaling verification | new info: quantitative localisation check |

Figure count: 13 → 11 (merged 2a+2b; merged 7+old-12 role; 9c→10; 8b→11).
Page layout: figures land within one page of their first citation (verified
in compiled PDF, pp. 6–23); no orphan blank pages; captions attached.

Scientific preservation: zero changes to equations, parameters, numbers,
gates, floors, branch identities, conclusions (diff-audited during rewrite;
all values re-read from raw files by the script, never typed).
