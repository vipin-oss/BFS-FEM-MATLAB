# P12C Manuscript Forensic Audit (Part C)

Base: `phase-1-symbolic @ 0d985029` · date 2026-09-24 · scope: `latex/ms.tex`,
`sec04_fem.tex`, `sec05_verification.tex`, `sec06_results.tex`, `sec08_discussion.tex`,
`sec09_conclusions.tex`. Method: statement-by-statement read against frozen evidence
(M13/M14, P4A/P4B records, P11D remediation, P12C raws, figures/tables generators).
Corrections applied **only** where the evidence is unambiguous; everything else is recorded.

## 1. Classification key

**A** correct/current · **B** stale-but-harmless · **C** misleading (evidence exists but wording
over/under-states) · **D** contradicts frozen evidence · **E** unsupported (no evidence).

## 2. Findings and actions

| # | File · statement (abridged) | Class | Action |
|---|---|---|---|
| C-1 | sec04 L47: “integrands … products of second derivatives (quartic polynomials) … third derivatives (quadratic polynomials) … $4\times4$ integrates all terms exactly” | **D** — contradicts M13/M14 (product integrands are degree **6 per coordinate**; the “quartic” phrase is explicitly overruled in `DERIVATION_M14.md` §M14.3; the 4×4 conclusion itself is correct) | **Fixed** (§3.1) |
| C-2 | sec05 L48: “Level 1 analytical tests PASS with machine precision ($<10^{-13}$)” | **C** — B3 `level1_homogeneous.max_error = 1.374 × 10⁻¹³` (tol 1e-12) exceeds 1e-13 | **Fixed** (§3.2) |
| C-3 | sec05 test list 5a–5h names/content | **D** — list was shifted vs the frozen P4A/P4B records and Table 4: text's “5a Rigid Body Modes”, “5b Hermiticity”, “5c Periodicity”, “5e Isotropic Rotational Invariance”, “5f PD of L(θ)” ≠ implemented 5a Hermiticity, 5b Periodicity, 5c Rotational invariance (AR=1), 5e rotation-swap symmetry, 5f matrix definiteness | **Fixed** (§3.3) |
| C-4 | sec05 L88: “for the baseline Case H configuration at θ = 45°, AR = 5” | **E** — the 5i run is isotropic ($l_1{=}l_2{=}l_{\mathrm{iso}}{=}0.2$, θ=0, φ=0); θ/AR are not parameters of the record | **Fixed** (§3.4) |
| C-5 | sec05 L88: “first six eigenfrequencies at the X point … directional stop band Δ_GX” + fig. 5 caption (b) “Monotone convergence of the directional stop band Δ_GX to ε_Δ” | **D** — fig05 (generator verified) plots the **acoustic ω̄_T** relative error (a) and **stepwise ω̄_T variation** (b); no Δ_GX, no six modes | **Fixed** (§3.5) |
| C-6 | sec05 5d bullet: “match analytical predictions within 1.25×10⁻⁸” | **C** — best-κ only; P4A record warns “do not use a single κ”; κ=10⁻² gives 1.80×10⁻⁶ (O(κ²) dispersion, above the 1e-6 test line) | **Fixed** (§3.3) |
| C-7 | sec06 L44: quadrature item “yields stop-band widths 2.7563/2.7226/2.7862 … quadrature invariance to within 1.22 %” | **C** — source field is `gap_at_X` (X-point directional gap, **4×4 mesh only**); “1.22 %” is the max one-sided deviation (−1.22 %/+1.08 %), spread 2.31 % | **Fixed** (§3.6) |
| C-8 | sec06 L22: “resolve the curved circular interface … without violating inter-element conformality … boundary approximated via piecewise numerical quadrature rather than an exact … representation” | **A** (honest; consistent with TV18/M14) | none |
| C-9 | sec06 mesh series, Δ_X vs Δ_complete, decrements/ratios, trigger rule, BZ item, sweep ¶, material ¶ | **A** — all values trace to raws (Part B table) | none |
| C-10 | sec08: “Case C is **fully solved**” | **C/D** — overclaim vs the paper's own not-mesh-converged status | **Fixed** (§3.7) |
| C-11 | sec08: “circular inclusion geometry is **resolved** using … (TV18)” | **C** — TV18 status is LOCKED [S]; approximation, not exact resolution | **Fixed** (§3.7) |
| C-12 | sec08: “All 18 project technical variations (TV1–TV18) are **resolved and closed**” | **D** — traceability matrix statuses: 8 CLOSED, 10 LOCKED; “closed” for all is inaccurate | **Fixed** (§3.7) |
| C-13 | sec08: Level-1 “relative error < 10⁻¹³” (same as C-2) | **C** | **Fixed** (§3.7) |
| C-14 | sec08: G3 NOT MET pending author tables; PCR1-linked language | **A** — matches `P11D_PCR_MAPPING.md` and gate records | none |
| C-15 | sec09: all seven conclusions (eight-test suite, p=4.17, ε_Δ, Case-C series + not-converged, steering, micro-inertia) | **A** (verified value-by-value in Parts A/B) | none |
| C-16 | ms.tex abstract: “…mesh convergence … **locking** an empirical least-squares convergence rate of p=4.17 (95 % CI [3.15,5.20]) and an operational numerical resolution floor…” | **C** — P4B record: observed slope, “no theoretical order claimed”; “locking” overstates, and the caveat was absent from the abstract | **Fixed** (§3.8) |
| C-17 | sec05/…: “Gate G3 remains formally NOT MET”; Evidence-Hierarchy declaration; “exact tolerances ≤0.5 %/≤2.0 % for Levels 1–2, qualitative overlay for heterogeneous bilayers” | **A** | none |
| C-18 | sec06/ms.tex: no “P5 production” claims present anywhere in the manuscript (grep: zero “production/P5” hits in `sections/`) | **A** (nothing to audit; Case-H numbers trace to `results/processed/table5_gap_summary.json`, e.g. Δ_complete ≤ −0.3758 → −0.37585) | none |

## 3. Applied corrections (exact, evidence-pinned)

### 3.1 sec04 (C-1)
**Before** the quartic/quadratic justification; **after**: “the element-matrix integrands are
products of their derivatives and reach degree six per coordinate; a standard 4×4 Gauss–Legendre
rule (exact through degree seven per axis) is therefore the minimal tensor rule that integrates
all homogeneous-element terms exactly without aliasing or rank deficiency. In elements cut by the
inclusion, the discontinuous material field is instead integrated by sub-cell Gauss sampling with
an O(h) geometric approximation (Section~\ref{sec:caseC_pc}).”
*Evidence*: `DERIVATION_M14.md` M14.3/M14.6 (Q1–Q6, incl. the explicit overruling of the
blueprint's “quartic” phrase); `AUDIT_M14_independent.md` (ranks 29/26/32/30 verified).

### 3.2 sec05 tolerance (C-2)
“Level 1 analytical tests PASS with **residuals ≤ 1.4×10⁻¹³ (locked tolerances ≤10⁻¹²)**.”
*Evidence*: `p11d_b3_run_P11D-B3-R1.json` `level1_homogeneous.max_error = 1.3741275e-13`, tol 1e-12;
B2 L1 4.10e-57; B1 < 2.22e-16. Level-2 sentence unchanged (all ≤4.19e-14 < 1e-13).

### 3.3 sec05 test list 5a–5h and 5d (C-3, C-6)
Rewritten to the frozen P4A/P4B record (`P4A_5a_5f.md`, `P4B_5g_5i.md`, auto-generated Table 4):
- 5a Hermiticity 2.01e-16 (K̄) / 5.63e-17 (M̄); 5b BZ periodicity ≤4.0e-16 matrix, 9.7e-16 eig for
  G∈{b₁,b₂,b₁+b₂}; 5c rotational invariance AR=1, θ∈{0,15,37,90,128}°, 9.63e-16;
- 5d multi-κ statement (four of five κ meet <10⁻⁶; best 1.25e-8 at κ=3e-4; κ=1e-2 deviation
  1.80e-6 flagged as O(κ²) Case-H dispersion, not implementation error);
- 5e rotation-swap symmetry 6.44e-16 (negative control 0.179); 5f definiteness (two Γ nulls
  −1.65e-16/5.3e-18, min interior ω²=3.028, M̄ min eig 9.9e-5); 5g/5h kept as written.
The old “L(θ) eigenvalues positive” bullet was removed here (L(θ) positive-definiteness remains
stated in the continuum sections where it belongs).

### 3.4 sec05 §5.3 configuration (C-4)
“for the homogeneous Case H verification parameters (λ=μ=ρ=1, ℓ²=0.04, l_iso=0.2) at fixed
k = (0.31π/L, 0.22π/L)”. *Evidence*: `p4b_5g_to_5i.py` 5i block (`kx, ky = 0.31π/L, 0.22π/L`;
PARAMS `[S-P4A]`), `p4b_5g_to_5i.json` `5i.k`.

### 3.5 sec05 figure 5 description + caption (C-5)
Both now describe panel (a) = relative error of the acoustic ω̄_T vs its closed-form value and
panel (b) = stepwise |Δω̄_T|/ω̄_T between refinements decreasing monotonically to ε_Δ.
*Evidence*: `figures/gen/fig05_mesh_convergence.py` (plots `5i.rel_err`, then
`|ω_{i+1}−ω_i|/ω_{i+1}`, hline = ε_Δ; titles “Eigenvalue Convergence (Case H)” /
“Stepwise Mesh Variation”).

### 3.6 sec06 quadrature item (C-7)
Now: “At the fixed 4×4 mesh, … yields X-point directional gaps Δ_X = 2.7563, 2.7226, 2.7862 —
deviations of −1.22 % and +1.08 % from the 16-point result — so the choice of quadrature rule is
immaterial for this observable at this resolution (the complete gap itself is assessed separately
above).” *Evidence*: `p11_caseC_convergence.json` `quadrature_sensitivity.*.gap_at_X`;
`P11B_REMEDIATION_AUDIT.md` table (“Gap at X”, baseline/±).

### 3.7 sec08 (C-10 … C-13)
- “Case C is **fully solved** and documented …” → “Case C is documented in Section~\ref{sec:caseC_pc}.”
- “geometry is **resolved** using Cartesian immersed Gauss–Legendre quadrature (TV18)” → “is
  **treated with the locked immersed Gauss–Legendre quadrature of TV18** (sub-cell material
  sampling; the circular boundary is approximated by piecewise numerical quadrature rather than an
  exact boundary-conforming representation)”.
- “All 18 … are **resolved and closed**” → “carry a **definitive recorded status (closed or locked
  to a specified choice)** in the master traceability matrix” (matrix: 8 CLOSED, 10 LOCKED).
- “TV18 is **resolved via** immersed Gauss quadrature” → “TV18 is **locked to** the standard
  immersed Gauss-quadrature treatment”.
- Level-1 tolerance aligned with §3.2.

### 3.8 ms.tex abstract (C-16)
“…yielding an observed empirical least-squares convergence rate of p=4.17 (95 % CI [3.15, 5.20];
**no theoretical order claimed**) and a locked operational numerical resolution floor of
ε_Δ = 4.63×10⁻¹¹.” *Evidence*: `P4B_5g_5i.md` (“observed slope … **no theoretical order is
claimed**”), Table 6 footer.

## 4. Deliberately not changed (recorded)

1. **sec06 quadrature-study provenance** — the numbers remain sourced from the preserved P11B-era
   file (Part B F-1/F-4). No new quadrature run exists in P12C (no new production calculations
   permitted), so the study cannot be re-scoped or re-run in this audit.
2. **sec08 “spread” nuance** — the corrected item states deviations ±1.22 %/+1.08 %; the total
   spread 2.31 % is now implicit (both endpoints given). No further edit.
3. **sec09** — no changes needed.
4. **Sec. 5.2/5.3 numbers** (Table 4/6 values) — auto-generated artifacts; not edited by hand.

## 5. Focus-list coverage

| Focus item | Verdict |
|---|---|
| “fully solved” | found once (sec08) → corrected |
| mesh convergence wording (Case H) | fig/text mis-description → corrected; p=4.17 now carries “no theoretical order claimed” in abstract |
| complete-gap convergence (Case C) | accurate and explicitly non-converged (Parts A/B) |
| quadrature exactness | sec04 degree error → corrected; cut-element O(h) now stated |
| interface integration | sec06 statement honest; sec08 TV18 wording corrected |
| 4×4/6×6/8×8 quadrature interpretation | observable/mesh now stated (X-gap at 4×4) |
| P5 production claims | none present (verified) |
| external validation | conservative; G3 NOT MET stated |
| PCR1/G3 status | consistent with records (NOT MET) |
| P4B order wording | “observed/empirical … no theoretical order claimed” (abstract fixed; body already correct) |
| 32²/64² results | accurate (Part A/B) |

## 6. Post-edit verification

```
python3 -m pytest paper9/verification/suite/test_p7_manuscript.py \
  test_p12c_caseC_32.py test_p12c_caseC_64.py test_p11b_forensic_remediation.py \
  test_p11d_remediation.py test_p12a_remediation.py -q
→ 34 passed in 1.87s
git diff --name-only  →  ms.tex, sec04, sec05, sec06, sec08 only
results/, production/, plan/blueprint/: zero changes (verified)
```
