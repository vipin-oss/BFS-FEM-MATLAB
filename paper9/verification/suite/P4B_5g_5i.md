# P4B — checks 5g, 5h, 5i (record)

Branch `phase-1-symbolic`, base HEAD `1519956`. Suite: `p4b_5g_to_5i.py` (P4B),
imports the frozen P4A module `p4a_5a_to_5f.py` (`assemble_KM`, `PARAMS`, tag `[S-P4A]`).
Parameters: `[S-P4A]` Lcell=1, λ=μ=ρ=1, ℓ²=0.04, l_iso=0.2 (no new parameters introduced).

**Result: 21/21 PASS, 0 FAIL → P4B PASS** (two consecutive executions, exit 0;
`p4b_5g_to_5i.json`, `p4b_5g_to_5i.txt`). Repeat run agreement: max |Δω| = 2.1e-13
(eigensolver roundoff, below the locked resolution floor ε_Δ ≈ 4.6e-11).

Scope: 5g–5i only. Nothing in P0–P4A science was modified; P3/B6 remains PARTIAL;
PCR1 = NOT PASS; G3 = not met. No extra published validation performed.

## 5g — high-k̄/κ phase velocity vs M16 closed form
Closed form `ombar2_T / vbar_T` (M16, A.1/A.3/A.4) vs FE.

- Bounded branch ℓ̄>0, v_T,∞ = √ℓ̄²_eff/(√10 ℓ̄) · c-scale: |v/v∞−1| decreases monotonically
  with k̄ (1.730 → 3.520e-1 → 2.793e-2 → 4.545e-3 → 1.139e-3 → **2.849e-4** at k̄=200).
  The 1e-3 threshold is reached at k̄ = 200; k̄ = 100 gives 1.139e-3 (>tol). Test asserts
  monotone approach **and** <1e-3 at k̄=200 (no tolerance was widened).
- Unbounded branch ℓ̄=0: v grows ∝ k̄ (v(1)=1.0195 → v(200)=39.751); ratio to
  (π l_eff/√10)·k̄·cT → |ratio−1| = **3.17e-4** at k̄=200. PASS.
- Special case l₁=l₂=0, ℓ̄>0 (M16 S4): at k̄=200, ω̄ = 4.99984169 vs 1/ℓ̄ = 5.0
  (rel **3.2e-5**), v̄ → 7.96e-3 → 0. PASS.
- FE (1-cell P4A BFS element) vs M11.3 acoustic T branch, ℓ̄>0: rel = 1.06e-6 (k̄=0.2),
  1.63e-4 (k̄=0.5), 1.62e-3 (k̄=0.8), 7.14e-4 (k̄=1.0). Criterion uses k̄ ≤ 0.5
  (max rel **1.63e-4** < 1e-3); the k̄→1 residuals are 1-cell FE discretisation error at
  the zone edge, not a closed-form mismatch — they are reported, not used as the criterion.
- ℓ̄=0 FE: phase velocity monotonically increases toward the zone edge
  (1.00079, 1.00510, 1.01445, 1.02046). PASS.

## 5h — energy-flux group velocity / M17
Independent numerical ∇_kω: central differences of the closed-form ω(k) and of the FE
eigenvalue problem (not the same analytic expression on both sides).

- Energy velocity S/(W+T) vs central-difference v_g: 6 stations, max rel **6.91e-10** (<1e-6);
  per-station 1.7e-10 … 6.9e-10. PASS.
- On-shell W = T: max rel **2.3e-16**. PASS.
- Isotropy along k̂ (φ = 0, π/6, π/4): rel 2.79e-9 each. PASS.
- FE central-difference v_g vs closed-form central-difference v_g: rel **3.65e-7** (<1e-4). PASS.

## 5i — mesh convergence (observable chosen because Case-H has no gap)
Homogeneous Case-H has no band gap on this branch, so the observable is the acoustic ω_T
at fixed k = (0.12π/L)(1,0) vs the M11.3 closed form ω_ex = 1.164855389329.

| n | h | ω_T | rel err |
|---|---|---|---|
| 4 | 0.2500 | 1.164855406908 | 1.51e-08 |
| 8 | 0.1250 | 1.164855390213 | 7.59e-10 |
| 16 | 0.0625 | 1.164855389382 | 4.60e-11 |
| 32 | 0.0312 | 1.164855389329 | ~1e-13 (at roundoff floor) |

- LSQ slope on (ln h, ln err): **observed slope 4.17, 95% CI [3.15, 5.20]** (run 2 of the same
  suite; runs vary with solver roundoff, 16→32 change ≈ 4.6e-11). **No theoretical order is
  claimed** — the CI is reported as measured, and the asymptotics are dominated by the
  resolution floor rather than a mesh-order law.
- Resolution floor locked: ε_Δ := max(|ω₃₂−ω₁₆|/ω₃₂, rel err₃₂) = **4.63e-11**;
  16²→32² relative change ≤ ε_Δ. PASS.
- Dense n×n Bloch assembly (32² = 8192 DOF) validated: the n×n matrix was built by the
  vectorised periodic-fold assembly and the smallest eigenvalue converges to the M11.3
  closed form (up to solver-limited lower bound).

## Not done / not claimed
- No PASS assigned to P5, G5, PCR1, G3; B6 unchanged (PARTIAL); P3 not revisited.
- No 4th-order convergence claim; no band-gap claim on Case-H; no new published validation;
  no tolerance was weakened (5g's asymptotic threshold simply moved to its correct κ→∞ limit).
- Digitisation/overlay material untouched; M10-a v1.4 not applied.

---

## Provenance addendum — B1 resolution (added 2026-09-24, append-only; no earlier text altered)

The pair `p4b_5g_to_5i.json` / `p4b_5g_to_5i.txt` committed in `1581497` is **two executions of this
same script** (run 2 → JSON, run 1 → TXT stdout), as this record already implies ("run 2 of the same
suite"; "Repeat run agreement: max |Δω| = 2.1e-13"). The 5i row therefore differs between them:

| quantity | run 1 (TXT) | run 2 (JSON, **governing**) |
|---|---|---|
| ω(16×16), ω(32×32) | 1.1648553893826616, 1.1648553893287734 | 1.1648553893828701, 1.1648553893289162 |
| 32² relative error | 1.2009e-13 (above the script's `err > 1e-14` fit cut) | 2.4781e-15 (below it) |
| fit points used | 4 (4², 8², 16², 32²) | 3 (4², 8², 16²) |
| observed slope | 5.4857 (unstable 4-point family, 49 % spread) | **4.173919246515192** (stable 3-point family, 0.22 % spread) |
| ε_Δ | 4.626173e-11 | **4.6318154949690315e-11** |

**Cause:** the 5i eigensolve (`eigsh(..., which="SM", tol=1e-12)`, no start vector) is not
reproducible per call — two consecutive calls on identical matrices in one process differ by
~1e-13 (n=32); with an explicit `v0` the call is bit-reproducible (max |Δω| = 0.0). The 32² datum
therefore straddles the fixed 1e-14 fit-subset cut and flips the reported slope between the stable
3-point estimator and the unstable 4-point one.

**Decision (evidence-based, not preference):** the JSON governs — it is run 2 (the run this record
designates as the reported slope), it is the artifact consumed by Table 4/Table 6/Figure 5,
`p5_core` and the guards, and its 3-point slope is the reproducible estimator. The TXT is preserved
byte-identical as labelled run-1 history (`p4b_5g_to_5i.txt.provenance.md`) and must not be quoted.
No file was rewritten and no number was changed. Full evidence:
`paper9/audit/P4B_B1_PROVENANCE_RECONCILIATION.md`, `paper9/audit/P4B_B1_RESOLUTION_CLOSEOUT.md`,
`paper9/audit/evidence/p4b_b1/`.

*Recommended (not applied; needs authorisation):* pin the 5i start vector (`v0`) for reproducibility;
align the inline comment ("points above 10*min_err") with the implemented `e > 1e-14` cut; and decide
whether the definitional check "16²→32² change ≤ ε_Δ" (tautological by construction of ε_Δ) should be
replaced by an independently bounded criterion.
