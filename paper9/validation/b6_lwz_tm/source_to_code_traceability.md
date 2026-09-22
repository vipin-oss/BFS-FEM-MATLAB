# B6 independent LWZ2016 1-D TM — source → code

**Governing source:** Li, Wei & Zhou, *Acta Mechanica* **227**:1005–1023 (2016), PDF `paper9/analytic/lwz2016/li2015.pdf`.  
**Not** Case-H / BFS, **not** PB2009, **not** Li 2023/2024.

**Status:** B6 **PARTIAL**. Level-1 homogeneous TM **PASS** vs closed form (14.1) at pre-declared 1e-8 (max rel k **1.429e-14**). Level-2 identical-layer **PASS** (**4.441e-16**). Fig. 3 quantitative **BLOCKED** (no tabulated ω(k); digitisation not an error metric). PCR1/G3 **NOT PASS**.

## Equations (PDF)

| Paper | Code | Notes |
|---|---|---|
| (14.1) p.4 travelling SH | `omega_from_sigma` | `ω² = σ² Vs² (1+cσ²)/(1+d²σ²/3)` |
| (12) p.4 σ, τ | `sigma_tau_from_omega` | real positive branches |
| App. 3 p.18, r=s, ε=μ | `layer_T_sh_normal` | 4×4 `T = t/(σ²+τ²)` |
| (29) p.6 `V_B^R = T_B T_A V_A^L` | `bilayer_T` = `TB @ TA` |
| (40) p.7 `\|T_B T_A − I e^{ika}\|=0` | `min_svd_residual` |

## Fig. 3 parameters (PDF p.10) — used for L2 scan only

`c̄₁ = √c₁/a = 0.5`, `d̄₁ = d₁/a = 0.5`, `c̄ = c₁/c₂ = 0.77`, `d̄ = d₁/d₂ = 2`, `a₁/a = 0.5`, `V_{s2}/V_{s1}=0.5947`, `ρ₂/ρ₁=0.1573`.  
Vertical axis in the paper: `ωa/(2π v_m)` with `v_m = a / (a₁/V_{s1}+a₂/V_{s2})`.

No table of ω(k). Digitisation is overlay-only and **not** used as an error metric.

**Fig. 3(b) quantitative vs paper: BLOCKED.** See `FIG3B_FEASIBILITY.md`. Caption is Left/middle/right, not a numbered table; no ω(k) points; right panel has no numerical \(\bar\xi\). L1/L2 code **unchanged**.

## Acceptance (declared before execution)

- **L1:** max relative \|k_Bloch − σ\| and \|λ − e^{iσa}\| **< 1e-8**.
- **L1 robustness:** half-thickness cell, same σ, still **< 1e-8**.
- **L2 quantitative:** identical layers recover (14.1) to **1e-7**.
- **L2 bilayer:** roots exist on first-BZ k-grid; coarse vs 2×-fine ω-grid max rel Δω **< 5e-3** (search resolution, not physics vs figure).

## Results (executed)

See `lwz_tm_results.json`. L1 max rel k **1.429e-14**, RMS **4.189e-15**. L2 identical max rel **4.441e-16**. L2 bilayer acoustic scan produced 8 (k̄, ω̄) samples; grid robustness max rel Δω **1.524e-3**.

## Not done

C¹ laminated FE. Case-H solver changes. B1/B2 `l` vs `l̄`. Fig. 4(c) numbers. P4B/P5.
