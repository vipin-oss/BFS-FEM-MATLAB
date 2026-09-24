# P12C Manuscript Numerical Cross-Check (Part J)

Every Case-C number currently used in the manuscript, plus the P4B convergence-rate / resolution-floor
values, mapped to an authoritative source. No new scientific numbers were produced here; every
“source” value below was re-read from the files during this audit (and, where marked, recomputed).
Columns: **location → printed → meaning → authoritative source → exact match? → status.**

## A. Case C (`latex/sections/sec06_results.tex` and downstream)

| # | location | printed | meaning | authoritative source | match | status |
|---|---|---|---|---|---|---|
| 1 | sec06 material ¶ | χ_μ = 25.0 | modulus contrast | `p11_caseC_raw.json metadata.contrast_mu` = 25.0 | ✔ | OK |
| 2 | sec06 material ¶ | χ_ρ = 5.546 | density contrast | `metadata.contrast_rho` = 5.546 (6333/1142 = 5.5455) | ✔ | OK |
| 3 | sec06 material ¶ | ρm 1142, μm 1.48, λm 4.57, ρi 6333, μi 37.0, λi 95.0 | dimensional data | raw `metadata.matrix` / `.inclusion` strings: Epoxy (λ=3.088, ℓ²=0.01), YBCO (ρ=5.546, μ=25.0, λ=64.19, ℓ²=0.04); λm/μm = 3.088 ✔, λi/μi = 64.19/25 = 2.568 ✔ | ✔ | OK |
| 4 | sec06 material ¶ | ℓ_m = 0.10L, ℓ_i = 0.20L | gradient lengths | raw strings `ell2=0.01` / `ell2=0.04` → ℓ = 0.10L / 0.20L | ✔ | OK |
| 5 | sec06 material ¶ | c_t,m = 1138.4 m/s | nondimensionalisation | √(1.48×10⁹/1142) = 1138.41 | ✔ | OK (derived, stated as derived) |
| 6 | sec06 ¶ + Fig. 8(a) cap | 4.5698, 7.1430 | max ω̄₃ / min ω̄₄ (4², 21²) | `p11d_caseC_gap_convergence.json` cell `4x4_FE_21x21_BZ`: ω3_max = 4.569792917, ω4_min = 7.142979832 | ✔ | OK |
| 7 | sec06 ¶ + Fig. 8(b) cap | 2.5732 (21²); 2.5728 (41²) | Δ_complete (4²) | same file: `4x4_FE_21x21_BZ.delta_complete` = 2.5731869148; `4x4_FE_41x41_BZ` = 2.5728033505 | ✔ | OK |
| 8 | sec06 ¶ + cap | 43.94 % | Δ/ω̄_mid (4²) | `norm_gap_pct` = 43.938134375 (recomputed 43.93813) | ✔ | OK |
| 9 | sec06 ¶ | ~4×10⁻⁴ | BZ sampling accuracy 21²→41² | difference of #7 pair = 3.8356×10⁻⁴ | ✔ | OK |
| 10 | sec06 inequality eq/¶ | 2.6114, 2.7563, 3.2871; min = 2.6114; each ≥ 2.5732 | Γ–X, X–M, M–Γ leg gaps, min leg, path gap | `per_mesh_gaps['4x4']`: Δ_GX = 2.611378, Δ_XM = 2.7563017, Δ_MG = 3.2871113, Δ_path = Δ_complete = 2.5731869 (identical in `p11_caseC_raw.json radius_sweep.r_30.gap_34`) | ✔ | OK |
| 11 | sec06 mesh item | 2.5732 / 2.2504 / 2.0722 / 1.9736 / 1.9179 | Δ_complete 4²→64² (21²) | `comparison_vs_4_8_16.delta_complete_21x21` (4²…32²) + J64 `post_64_report.delta_complete_64_21x21` = 1.9178891171692278 | ✔ | OK |
| 12 | sec06 mesh item | 200 / 648 / 2312 / 8712 / 33800 | global DOFs | 8(N+1)²; J32/J64 cell records `fe_dofs` = 8712 / 33800 | ✔ | OK |
| 13 | sec06 mesh item | Δ_X = 2.7563 / 2.2504 / 2.0722 / 1.9736 / 1.9179 | X-point gaps | `p11d_deltaX_check.json` (2.7563017 / 2.2503884 / 2.0722484) + J32/J64 `path_32/64.delta_XM` (1.9736363157 / 1.9178891171) | ✔ | OK (kept explicitly distinct from #11) |
| 14 | sec06 mesh item | d₁ 0.3228, d₂ 0.17814, d₃ 0.09861, d₄ 0.05575 | successive decrements | J32 `comparison_vs_4_8_16.successive_decrements` (0.3227984994 / 0.1781399883 / 0.0986121121) + J64 `post_64_report` d₄ = 0.05574719776 | ✔ | OK |
| 15 | sec06 mesh item | 0.552 / 0.554 / 0.565; rule ≥0.5 fired twice | decrement ratios + rule | recomputed (d₂/d₁ = 0.55187, d₃/d₂ = 0.55357, d₄/d₃ = 0.56532) = J64 `d4_over_d3` 0.5653179569583828 + `parent_rule_evaluation.r` 0.5535652777739338 (decision “RUN 64x64”, trigger true) | ✔ | OK |
| 16 | sec06 mesh item | “not mesh-converged … 2.5732 is the 4×4-mesh result” | status | Parts A4/B; asserted by Part G guards | ✔ | OK |
| 17 | sec06 quadrature item | 2.7563 / 2.7226 / 2.7862; −1.22 % / +1.08 % | Δ_X at 4² for 16/36/64 Gauss pts | `p11_caseC_convergence.json quadrature_sensitivity` (4x4/6x6/8x8 → gap_at_X 2.7563 / 2.7226 / 2.7862); percentages = deviation from the 4×4 value: −1.2219 %, +1.0848 % | ✔ | OK after Part C re-scope |
| 18 | sec06 BZ item | < 5×10⁻⁴; 2.5732→2.5728; 4 dp at 8²/16²; 6 dp at 32²/64² | BZ-grid sensitivity | P11D 11²/21²/41² cells; J32/J64 11²-vs-21² diffs (6.3×10⁻¹⁰ / 1.8×10⁻⁹) | ✔ | OK |
| 19 | sec06 sweep ¶ + Fig. 8(b) | 0.8288 (16.61 %), 2.5732 (43.94 %), 2.4426 (37.00 %) | Δ_complete at r₀/a = 0.20/0.30/0.40 (4², 21²) | `p11_caseC_raw.json radius_sweep.r_20/r_30/r_40.gap_34.delta_complete` = 0.8288312 / 2.5731869 / 2.4425734; `norm_gap_width` = 0.1661046 / 0.4393813 / 0.3700323; independent recompute min(ω₄) − max(ω₃) from `path_bands` reproduces 0.8288311899 | ✔ | OK |
| 20 | sec06 sweep ¶ | f = 28.27 %; f ∈ [12.6 %, 50.3 %] | filling fractions | `radius_sweep.*.filling_fraction`: 0.2827433388; 0.1256637061 / 0.5026548246 | ✔ | OK |
| 21 | sec08 ¶2, sec09 ¶5 | series + “2.5732 at the 4×4 mesh” | status restatement | as #11/#16 | ✔ | OK |

## B. P4B slope / resolution floor (ms.tex, sec05, sec06, sec09, Table 6, Fig. 5)

| # | location | printed | meaning | authoritative source | match | status |
|---|---|---|---|---|---|---|
| 22 | ms.tex abstract; sec05 eq. (line 108); Table 6 footer | p = 4.17 (95 % CI [3.15, 5.20]) | observed LSQ rate; **no theoretical order claimed** | `verification/suite/p4b_5g_to_5i.json` 5i: slope 4.173919246515192, CI95 [3.1453687594104447, 5.202469733619939], `note` = “no theoretical order claimed” | ✔ | OK (caveat added, Part C) |
| 23 | ms.tex abstract; sec05; Table 6 footer | ε_Δ = 4.63×10⁻¹¹ | operational resolution floor | JSON 5i `eps_Delta` = 4.6318154949690315×10⁻¹¹ = \|ω₃₂−ω₁₆\|/ω₃₂ (recomputed exactly); Table 6 footer: max(\|ω₃₂−ω₁₆\|/ω₃₂, err₃₂) | ✔ | OK after Part E equation fix |
| 24 | Fig. 5 caption (a)/(b) | error curve; stepwise variation → floor | figure content | `figures/gen/fig05_mesh_convergence.py` reads JSON 5i `rel_err` and stepwise \|Δω\|/ω | ✔ | OK after Part C caption fix (verified live in Part E) |
| 25 | Table 6 rows | ω̄_T = 1.164855406908 / 390213 / 389383 / 389329; err 1.51e-8 / 7.59e-10 / 4.63e-11 / 2.48e-15; exact 1.164855389329 | Case-H acoustic convergence | `tables/out/tab06_convergence_floor.tex` (auto-generated) vs JSON 5i `omega`/`rel_err`/`omega_exact` = 1.1648553893289133 | ✔ | OK |
| 26 | sec05 §5.2; sec09; ms.tex | “eight-test internal consistency suite” | tests 5a–5h | Table 4 (`tables/out/tab04_consistency_suite.tex`, auto-generated) matches `P4A_5a_5f.md` + `P4B_5g_5i.md` | ✔ | OK after Part C list fix |

## C. Out-of-scope spot checks (Case H / P12B; unchanged by this audit)

| location | printed | source | match |
|---|---|---|---|
| ms.tex abstract; sec06/08/09 | Δ_complete ≤ −0.3758 | `results/processed/table5_gap_summary.json` (−0.37584813907) | ✔ |
| sec06 ¶ + caption; sec08; sec09 | Δ_GX = 0.0896 max at (θ=30°, AR=10); 0.0431 at θ=45°, AR=10 | table5 rows (max Δ_GX = 0.089602 at θ=30°, AR=10; 0.0431 on the AR=10/θ=45° row) | ✔ |
| ms.tex abstract; sec06; sec09 | S_θ = 3.946 rad⁻¹ (monotone in AR) | table5 `sensitivity_Stheta` (1.155 / 1.343 / 1.542 / 1.589 / 3.946 for AR = 2/3/5/7/10; AR=1 ≈ 0) | ✔ |
| ms.tex abstract; sec09 | δ_max = 2.79° (span [2.79°, 2.82°]), M_s = 0.0000° | P12B steering-FoM evidence (`P12B_STEERING_FOM.md`, fig12/fig14; PCR7 verified in Part F) | ✔ |
| ms.tex abstract | v_T,∞ = 0.3162 | JSON 5g `vinf_T` = 0.3162277660168379 | ✔ |

**Flags carried (not number errors).** (i) The P4B run **log** `p4b_5g_to_5i.txt` reports slope 5.4857
and ε_Δ 4.626×10⁻¹¹ from an earlier execution; the manuscript follows the governing JSON — the
divergence remains open in this tree and is carried as a release blocker (Part E F-1, Part K).
(ii) `latex/sections/sec06_results.tex` line 39 prints the same numbers as the equation (2.6114 etc.);
they are internally consistent.
