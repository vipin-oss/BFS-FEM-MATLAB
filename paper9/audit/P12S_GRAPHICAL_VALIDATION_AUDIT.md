# P12S — Graphical-validation implementation and B1/B2/B3 reproduction under Blueprint v1.5/A2

**Entry HEAD:** `70b7b0e9bf28cbb3d103770e68b9147b7bab68ff` (verified) · **Pre-work checkpoint:**
`270b8ab42246a2c20e0de8395aea8c8e5f068af4` (pushed + verified before any scientific work).
**Governing rule:** Blueprint v1.5 §13 / amendment A2 — routes `QUANTITATIVE_VALIDATION`,
`GRAPHICAL_VALIDATION`, `NOT_VALIDATED`; thresholds unchanged (≤ 2 %; ≤ 0.5 % classical).
This audit performs no author contact, sends nothing, and asserts **no percentage** anywhere.

---

## Phase A — forensic source extraction (authoritative PDFs in this repository)

Sources: `paper9/analytic/li2024/s41598-024-75049-1.pdf` (14 pp) and
`paper9/analytic/li2023/17455030.2023.2222189.pdf` (22 pp). Figures were extracted from the PDFs
themselves (`pypdf` image extraction) and are **read-only**; the PDFs are never modified.

### A.1 — Shared source facts (Li et al. 2024, Sci. Rep. 14:24035)

| Item | Value | Location |
|---|---|---|
| Materials | layer A = AlN, layer B = BaTiO₃ | p. 7 |
| ρ, a₃, c₃₃ (AlN) | 3.23×10³ kg/m³, 8.4×10⁻¹¹ C²/Nm², 3.9×10¹¹ Pa | p. 7 |
| ρ′, a₃′, c₃₃′ (BaTiO₃) | 5.8×10³ kg/m³, 1.26×10⁻⁸ C²/Nm², 1.62×10¹¹ Pa | p. 8 |
| Layer thicknesses | **a_A = a_B = 0.01 m** | p. 7 |
| Normalisation | Eq. (55): ρ̄=ρ′/ρ, ā₃=a₃′/a₃, c̄₃₃=c₃₃/(ρb²ω₀²), f̄=f/(b²ω₀√(ρa₃)), **l̄ = l/b**, **l̄₁ = l₁/b**, ā_A=a_A/b, c̄=c₃₃′/c₃₃, F=f′/f, L=l′/l, L₁=l₁′/l₁, ā_B=a_B/a_A, **k̄ = kb/π**, **ω̄ = ω/ω₀**; ω₀ = 2π/(a_A√(ρ/c₃₃) + a_B√(ρ′/c₃₃′)) | p. 7 |
| Interface / Bloch | perfect contact {V(z_B^L)} = {V(z_A^R)} (Eq. 49); Bloch {V(z_B^R)} = e^{ikb}{V(z_A^L)} (Eq. 51); det([T_B][T_A] − e^{ikb}[I]) = 0 (Eq. 53) | pp. 6–7 |
| Data availability | "The datasets used and/or analysed during the current study are available from the corresponding author on reasonable request." | p. 12 |

### A.2 — B1: Li 2024 **Fig. 2(a)**, p. 9 — caption verbatim

> "Fig. 2. Comparison of the dispersion curves and band gaps of dielectric phononic crystal based on three
> models. **a** Classical elasticity (l = 0, l₁ = 0, f = 0, L = 0, L₁ = 0, F = 0); …"

Axes: ω̄ (0–2) vs k̄ (−1 to 1) — read from the extracted panel. Branches: four classical branches with
vertices at k̄ = 0 (0.00 / 1.48 / 1.98) and k̄ = ±1 (1.48 / 0.51). **Branches/observables to compare:**
the four lowest branches, their vertices and the gap boundaries.

### A.3 — B2: Li 2024 **Fig. 2(b)**, p. 9 — the ambiguity, stated from the source

> "**b** gradient elasticity (l = 10⁻⁵, l₁ = 2 × 10⁻⁵, f = 0, **L = 5**, **L₁ = 5**, F = 0)"

The rendered panel is titled "l = 1×10⁻⁵" (image, p. 9). The body text (p. 7) defines **l̄ = l/b** and
states **a_A = a_B = 0.01 m ⇒ b = 0.02 m**. The source therefore gives a bare "l = 10⁻⁵" whose units are
**not stated** while its own normalisation requires a barred quantity; the ratios L = l′/l = 5,
L₁ = l₁′/l₁ = 5 *are* stated. Decision under A2.4: **the ambiguity is NOT resolved by the source** —
see §B.2 for the quantitative consequence.

### A.4 — B3: Li 2023 **Fig. 4(c)**, p. 15

Caption verbatim:
> "Figure 4. Comparison of dispersion and bandgap with existing literatures. (a) and (b) the dispersion
> curves for the classic elastic solids and the comparison with literature [59] and [34]; **(c) the
> dispersion curves for the gradient elastic solids and the comparison with literature [34]**."

Text (p. 15): "Figure 4(c) shows the dispersion and bandgap for the dipolar gradient elastic solids but
ignoring the thermoelastic coupling in the present model." **Fig. 4(c)'s caption states no parameter
values**; the parameters in force are the numerical-example data of p. 14 (a₁ = 10⁻⁵ m, ρ₁ = 7.5×10³
kg/m³, μ₁ = 2.3×10¹⁰ Pa, T₀₁ = 300 K, ω₀ = 4.1×10⁸ Hz, λ̄₁ = 0.928, μ̄₁ = 0.182, C̄r₁ = 0.069,
ℜ̄₁ = 0.0167, κ̄₁ = 2.3×10⁻⁵, λ_R = 0.047, μ_R = 0.056, ρ_R = 0.157, Cr_R = 2.257, ℜ_R = 0.057,
κ_R = 0.407, T₀R = 1, a_R = 1 (a₁ = a₂)) with the case-defining values of the **Fig. 3(b)** caption
(c̄₁ = 0.15, c_R = 1.5, d̄₁ = 0.25, d_R = 1.5; τ̄ and α zero), because (c) is exactly the "gradient
elasticity, thermoelastic coupling ignored" case with ratios c_R = c̄₂/c̄₁ = 1.5 and d_R = d̄₂/d̄₁ = 1.5.
Corroboration: ω₀ recomputed from the source's own formula = **4.115×10⁸ Hz** vs stated 4.1×10⁸ Hz.
Shared conventions: k̄ = ξa/π with a = a₁ + a₂; ω̄ = ω/ω₀; dipolar traction R_x = μc u_{x,yy}.

---

## Phase B — route determination

| | Source numerical values? | Sufficient graph + parameters? | Contradiction / ambiguity? | Route |
|---|---|---|---|---|
| **B1** | **No** (no tables anywhere in the paper; data on request only) | Yes — full parameter set + normalisation + BCs | none | **GRAPHICAL_VALIDATION** |
| **B2** | No | No — the one parameter that defines the panel is ambiguous | **Yes** | **NOT_VALIDATED** |
| **B3** | No | Graph yes, parameters yes — but the reproduction does not overlay | reproduction failure | **NOT_VALIDATED** |

---

## Phase C/D — B1 reproduction (PASS)

Independent classical Rytov solution implemented from the source's own equations and parameters
(`paper9/validation/p12s_reproduce.py::b1_dispersion`, using ω₀ of Eq. 55 and the AlN/BaTiO₃ data of
pp. 7–8). Overlay: `paper9/audit/evidence/p12s/B1_overlay.png` (left: published panel + registration
digits; right: reproduction vs published). The reproduction lies on the published curve: vertices
ω̄(0) = 0.00 / 1.4799 / 1.9799 and ω̄(±1) = 1.4799, 0.5099, matching the digitised reference within the
width of the printed curve — recorded as **graphical agreement, no percentage asserted**.
The rejected 0.48 % pixel metric (`P11A_FORENSIC_POST_RUN_AUDIT.md`) is **not** used or restated;
it remains `INVALID` as a solver-error claim.

## Phase E — B2 (NOT_VALIDATED)

Three labelled interpretations of the caption were evaluated with the repository's adaptive-precision
engine and with the displayed solutions (`paper9/audit/evidence/p12s/B2_overlay_interpretations.png`):

1. **Dimensional reading at the source geometry** (l = 10⁻⁵ m, a = 0.01 m; l/b = 5×10⁻⁴): the gradient
   correction is O((l k)²) ≈ 4×10⁻⁶ at ω̄ = 1 — the reproduction **coincides with the classical panel
   (Fig. 2(a))** and its band edges sit at ω̄ ≈ 0.480 / 0.520 / 0.979 / 1.021 / 1.498 / 1.978 / 2.016
   (adaptive precision 536 digits), whereas the published panel (b) differs strongly from (a).
2. **Barred reading** (l = l̄·b): the evanescent exponent doubles ⇒ the adaptive precision required is
   **52 131 decimal digits** ⇒ not simulable here; recorded as numerically infeasible.
3. **Micro-geometry reading** (a = l = 10⁻⁵ m): a completely different band/gap structure
   (first gap 0.078–0.242, then 0.742 / 0.785–1.103 / 1.123–1.435, …) and it contradicts the stated
   a_A = a_B = 0.01 m.

No interpretation reproduces the published panel (b) under the source-stated geometry, and none may be
selected without guessing → **B2 = NOT_VALIDATED** (ambiguity `UNRESOLVED`, per A2.4).

## Phase F — B3 (NOT_VALIDATED)

Reproduction attempted with the repository's dipolar-gradient TM machinery
(`paper9/validation/b1_b2_b3_solver.py::BenchmarkB3` formulas, ported to `p12s_reproduce.py::b3_dispersion`):
ω₀ = 4.115×10⁸ Hz ✓, but the reproduced lowest branch reaches ω̄ ≈ **0.35** at k̄ = 1 whereas the
source's own figure and the exact classical-limit value require **0.50**; the gap structure also
differs. The implementation cannot be validated against its own classical limit (overflow of
sinh(τa) as the gradient parameters → 0). Per the phase rule ("if a benchmark cannot be reproduced
faithfully, STOP and record NOT_VALIDATED; do not tune parameters until it matches") **no parameter was
tuned** and **B3 = NOT_VALIDATED**, with the blocker recorded as the unresolved formulation/coefficient
convention of the source's dipolar-gradient model (`SOURCE_UNAVAILABLE` item).

---

## Phase G — machine-readable record

`paper9/audit/benchmark_validation_record.json` — one entry per benchmark with: benchmark ID, source
citation, source figure, source page, parameter provenance, route, parameter completeness, ambiguity
status, reproduction status, overlay artifact + sha256, branch/observable compared,
`quantitative_error` (**NULL** for all three), `graphical_validation` (PASS / NOT_APPLICABLE), reason,
evidence path/hash. Raw reproduction output: `paper9/audit/evidence/p12s/p12s_validation_record.json`.

## Phase H — anti-fabrication tests

`paper9/verification/suite/test_p12s_anti_fabrication.py` (8 guards): graphical cannot become
quantitative because an overlay exists; missing numerics keep `quantitative_error = NULL`; parameter
ambiguity prevents PASS; a look-alike curve with a different parameter set cannot pass; digitisation
residuals cannot populate `quantitative_error`; a genuine quantitative dataset still follows ≤ 2 %
(0.5 % classical); B1/B2/B3 routes are independent; and the committed record itself is checked
(B2/B3 not promoted, no percentage fields present).

## Phase I — PCR1 / G3 evaluation under A2 (no promotion)

| Gate | Requirement under A2 | State | Verdict |
|---|---|---|---|
| PCR1 | all mandatory benchmarks (Layers 1, 2a, 2b) validated by an admissible route | B1 GRAPHICAL ✓ · **B2 NOT_VALIDATED ✗** · B3 NOT_VALIDATED ✗ | **NOT PASS** |
| G3 | same three gates, each met quantitatively or by the labelled graphical route | two anchors remain unvalidated | **NOT MET** |
| G4 | PI signature after PCR1–PCR8 checked | not reachable | **NOT MET** |

**Exact blocker:** both remaining failures are *source-side*, not computational —
B2 because the single parameter defining Fig. 2(b) is dimensionally ambiguous (A2.4 forbids choosing
silently, and the barred reading is numerically infeasible at 5.2×10⁴ digits), and B3 because the
source's dipolar-gradient formulation/convention cannot be pinned down from the published text, so the
independent implementation does not overlay Fig. 4(c). The gate definition was **not** changed; the
author-data request package (P12M/P12L) remains the higher-tier route that would close B2/B3
quantitatively if the source authors supplied the values.

Unchanged and unaffected: **P5** NOT PASS/OPEN, **R-1** OPEN, **PCR5** PASS, **P13** BLOCKED.
