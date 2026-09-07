# SPIKE_AND_ANOMALY_AUDIT.md (package version)

Method: every final curve/surface inspected for NaN/Inf, duplicates,
unsorted points, isolated jumps, branch discontinuities, interpolation
overshoot, clipping, cancellation-dominated and conditioning-sensitive
regions (scripted scans over results/raw; 2026-09-07). Rule: never delete or
smooth; classify first. Classifications: PHYSICAL, NUMERICAL CANCELLATION,
BRANCH TRACKING, CONDITIONING, INTERPOLATION, PLOTTING.

| Figure | Location | Feature | Diagnosis | Evidence | Action |
|---|---|---|---|---|---|
| 2(b) | gate curves, scattered Ω* | dips to 1e-16 (2 and 7 cells) | NUMERICAL CANCELLATION | limits reproduced to ≤3.3e-9; dips where \|ΔV\|/V underflows; V-curves smooth (max step 2.6e-6) | retained; roundoff band shaded; caption explains |
| 2(a) | x=5.5 marker | 0.934208 legacy point | BRANCH TRACKING (coarse stage-6 scan) | upstream IMPLEMENTATION_AUDIT; production value 0.9326028 | open marker, labelled excluded |
| 3(b) | low-Ω* wiggle of \|V_B−V_C\| | sign-node dips | NUMERICAL CANCELLATION + PHYSICAL interference | abs values ≤4.4e-6; underlying V smooth | retained; floor+shading |
| 4(a,b) | Δ_BC below floor | wiggle/dips | NUMERICAL CANCELLATION | 95/121 below benchmarked floor | retained; shaded; ratio panel (b) |
| 5(b,c) | low-χ scatter | roundoff skirt | NUMERICAL CANCELLATION | master-curve collapse above floor | retained |
| 6(a,b) | sharp dips (e.g. Ω*≈40, τ0*=1e-2) | Δ_T sign nodes | PHYSICAL interference | nodes reproducible across τ; captioned | retained, not smoothed |
| 6(a,b) | reference row flat at clip | Δ_T≡0 by definition | PLOTTING | τ0*=τ_ref | dotted clip line, caption note |
| 7(a,b) | low-Ω* wiggle | cancellation below floor | NUMERICAL CANCELLATION | monotone growth above floor to 8.06e-6 | retained |
| 8 | model-A panels | grazing roots | PHYSICAL/CONDITIONING (V*<√K3* degeneracy) | solver flags; never admissible | open squares |
| 8 | excluded roots | NaN residuals | PLOTTING/logging | residuals recorded for admissible only (≤6.0e-17) | crosses; caption |
| 9(a,b) | S-shoulder ridge | relaxation front sliding with D_w* | PHYSICAL (genuine model behaviour) | matches 1D slices (Fig. 5) | retained; z not exaggerated |
| 9(c) | −16 skirt | Δ_BC zero/sub-floor region | NUMERICAL CANCELLATION | 1 exact zero of 3721; rest below floor | retained as resolution-indistinguishable region; no transition claimed |
| 10 | dark middle row | Δ_T≡0 reference | PLOTTING | definition | caption note |
| 3D | base contours | piecewise-linear render | INTERPOLATION (render-only) | rstride=1 surfaces; contours cannot add extrema | documented |
| — | model A cond(B) | up to 5.1e10 at high Ω* | CONDITIONING | gated residuals ≤3.27e-9 | recorded, not hidden |

No feature deleted, smoothed, or interpolated away. No unexplained spike
remains; branch-identity at Ω*=1000 verified from raw data
(|V_C(D_w*→0)−V_A| = 7.6e-11 at the phason branch 0.31072662, not the 0.467
phonon branch) — see verification/INVARIANT_CHECK.md.
