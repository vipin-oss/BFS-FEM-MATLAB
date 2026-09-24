# P12V — B2/B3 BLOCKER-RESOLUTION SOURCE AUDIT

**Phase:** P12V (forensic, audit only).
**Scope:** resolve or precisely bound the two remaining external-validation blockers of Phase 12:
B2 (Li et al. 2024, Fig. 2(b), strain-gradient panel) and B3 (Li et al. 2023, Fig. 4(c),
dipolar-gradient panel).
**Sources (authoritative, in-repo, byte-verified at the start of this phase):**

| file | sha256 |
|---|---|
| `paper9/analytic/li2024/s41598-024-75049-1.pdf` | `2ac5f45d77ee37569f69e8890b70200ae6982f669ecaccf6cb5aa162f0340513` |
| `paper9/analytic/li2023/17455030.2023.2222189.pdf` | `3f5103380302609ef2dfe76c8ade09cae79b2ebbd4fdb4da228576c331191aa7` |

**Method.** First-hand reading of the two PDFs (text extraction *and* rendered-page / raster
inspection where glyphs or signs matter), an independent digitizer written inside this phase
(`evidence/p12v/*.json`), and an independent re-derivation of the B3 transfer matrix from the
source's own Appendix 3. Digitisation is used as a **registration/structure tool only**: no
percentage, no error metric and no solver grade is derived from pixels. No parameter was tuned.
No production file, Blueprint, manuscript, gate or route was modified.

**Artifact retention.** PDFs, digitisations, checks and the audit record; no repository
behaviour change.

---

## Part A — B2 source map: Li et al. 2024, Fig. 2(b)

### A.1 What the source says, by page / equation / notation

| location | verbatim / value | notation class |
|---|---|---|
| p. 7, Eq. (54) | `f(ρ, a3, c33, f, l, l1, aA, ρ′, a′3, c′33, f′, l′, l′1, aB, k, ω) = 0` | `l`, `l1` are listed as **material coefficients of layer A** (same slot as ρ, a3, c33, f) |
| p. 7, after Eq. (54) | “where (ρ, a3, c33, f, l, l1) and aA are the material coefficients in layer A, while (ρ′, a′3, c′33, f′, l′, l′1) and aB are the material coefficients in layer B.” | `l`, `l1` are **layer-A material coefficients**; the primed set are layer-B |
| p. 7, reference values | “Choosing (ρ, a3, **b**) and ω0 = 2π / ( a_A/√(c33/ρ) + a_B/√(c′33/ρ′) )” | `b` = reference length; ω0 is a **transit-time** frequency |
| p. 7, non-dimensional block | `ρ̄ = ρ′/ρ`, `ā3 = a′3/a3`, `c̄33 = c33/(ρb²ω0²)`, `f̄ = f/(b²ω0√(ρa3))`, **`l̄ = l/b`**, **`l̄1 = l1/b`**, `āA = aA/b`, `c̄ = c′33/c33`, `F = f′/f`, `L = l′/l`, `L1 = l′1/l1`, `āB = aB/aA`, **`k̄ = kb/π`**, `ω̄ = ω/ω0` | the barred symbols are the dimensionless set; every barred quantity is printed **with an overbar** in the source |
| p. 7, Eq. (55) | `f(1, 1, c̄33, f̄, l̄, l̄1, āA, ρ̄, ā3, c̄, F, L, L1, āB, k̄, ω̄) = 0` | the dispersion relation is stated **in the barred set only** |
| p. 7 | `aA = aB = 0.01 m`; ρ = 3.23×10³ kg/m³, a3 = 8.4×10⁻¹¹ C²/Nm², c33 = 3.9×10¹¹ Pa | the only dimensioned lengths/materials of the numerical example |
| p. 8 | ρ′ = 5.8×10³ kg/m³, a′3 = 1.26×10⁻⁸ C²/Nm², c′33 = 1.62×10¹¹ Pa; `b = aA + aB` | cell = 0.02 m |
| p. 9, Fig. 2 caption | “**a** Classical elasticity (l = 0, l1 = 0, f = 0, L = 0, L1 = 0, F = 0); **b** gradient elasticity (**l = 10⁻⁵**, l1 = 2×10⁻⁵, f = 0, L = 5, L1 = 5, F = 0); **c** flexoelectric and gradient elasticity (l = 10⁻⁵, l1 = 2×10⁻⁵, f = 10⁻⁵, L = 5, L1 = 5, F = 20)” | bare, **unbarred** `l`; **no unit** |
| p. 9, raster title of panel (b) | `l = 1×10⁻⁵` | bare, **unbarred** `l`; no overbar, no unit (verified on the rendered raster) |
| p. 10–12, Fig. 3/4/5 captions | `l1 = 1×10⁻⁵`, `l = 4×10⁻⁵`, `l1 = 1×10⁻⁵`, `f = 10⁻⁵`, `L = 20`, `L1 = 5`, `F = 200`, `F = 20` | the same bare style throughout |

Occurrence audit of `l`, `l̄`, `l1`, `l̄1`, `b`, `aA`, `aB`, `k`, `k̄`, `ω`, `ω̄` and Eq. (55):
pp. 7–9 contain 1 definition (Eq. 54), 1 normalisation block, 1 dimensionless relation
(Eq. 55) and the figure captions; **no other occurrence of `l` with a unit or with a stated
normalisation** exists in the paper. There is no parameter table, no data-availability
supplement, and **no erratum / correction / supplementary file** anywhere in the workspace or
attached to the PDFs.

### A.2 The eight enumerated questions

1. **Explicit dimensional `l`?** — **NO.** The source never writes `l` with a unit and never
   gives a dimensional `l` for this example. `aA = aB = 0.01 m` is the only stated length.
2. **Explicit definition `l̄ = l/b`?** — **YES.** Printed in the p. 7 normalisation block
   (`l̄ = l/b`, `l̄1 = l1/b`), with the overbar set. This part of the chain is unambiguous.
3. **Is the caption `l = 10⁻⁵` dimensional or normalised?** — **NOT STATED.** The caption (and
   the raster label) use the **unbarred** symbol, while the source prints the overbar on every
   barred symbol it defines. The unbarred symbol is therefore formally the *dimensional* member
   of the pair; but the source gives no unit and no statement of which numbers the panels were
   computed from. Both readings are formally open; neither is authorised.
4. **Is there a sentence linking the caption value to Eq. (55)?** — **NO.** The captions merely
   list values; neither the figure discussion (p. 8) nor the body text states the mapping
   between the caption numbers and the barred set of Eq. (55).
5. **Another source basis (table, data statement, supplement, other version)?** — **NO.**
   No parameter table; no supplementary material; no erratum/correction (checked across the
   workspace and the PDF metadata).
6. **Does either admissible interpretation reproduce the published Fig. 2(b)?** — **NO**
   (decided on structure, not on curve closeness):
   * dimensional reading (`a = 0.01 m`, `l = 1×10⁻⁵ m`): `l/b = 5×10⁻⁴`, gradient correction
     O(10⁻⁶) → the computed panel **coincides with the classical Fig. 2(a)**;
   * barred reading (`l̄ = 1×10⁻⁵` → `l = 2×10⁻⁷ m`): same geometry, no material change;
     requires 52 131-digit adaptive precision to even resolve, and still yields the classical
     structure;
   * nanoscale reading (`cell = l = 1×10⁻⁵ m`, an *unstated* geometry): yields a different band
     structure that matches neither the published (b) nor the classical (a);
   * the published (b) panel is structurally different from (a) (lowest branch ω̄ ≈ 0.33 at
     k̄ = ±1 vs 0.475; first band gap ≈ [0.334, 0.643] vs [0.520, 0.980]).
7. **If neither interpretation is source-authorised, say exactly why.** — The source (i) prints
   the caption value with the **unbarred** symbol but without a unit, (ii) defines `l̄ = l/b`
   only for the barred symbol, (iii) states no geometry/parameter linkage for that panel, and
   (iv) contains no sentence connecting the caption number to Eq. (55). Therefore **no**
   admissible interpretation is authorised by the text; the interpretation is at best
   **ONLY INFERABLE**, and an inferred value must not be promoted to source data.
8. **Re-verification of the previously recorded quantities** (all re-derived in this phase;
   see `evidence/p12v/li2024_fig2_digitisation.json` and the P12T ledger):

   | quantity | re-verified value | status |
   |---|---|---|
   | `(lk)²`, dimensional reading | 4.1639×10⁻⁶ (k_A = 204.055 m⁻¹ at `ω̄ = 1`) | confirmed |
   | `(lk)²`, barred reading | 1.6655×10⁻⁹ (`l = 2×10⁻⁷ m`) | confirmed |
   | required adaptive precision (barred) | 52 131 = ⌈0.4343·Λ⌉ + 15, Λ = 119999.99 | confirmed |
   | classical-panel coincidence (dimensional) | band edges within ≤ 7×10⁻⁴ of Fig. 2(a) | confirmed |
   | micro reading | first gaps [0.0780, 0.2422], [0.3783, 0.3830], [0.7420, 0.7599], … | confirmed |
   | published (b) digitised (own, this phase) | k̄ = 0 → 0.866, 1.164, 1.779; k̄ = ±1 → 0.334, 0.643, 1.415, 1.515 | registration only |

### A.3 Verdict (B2)

**`SOURCE-AMBIGUOUS — DATA REQUIRED`.** B2 remains **`NOT_VALIDATED`** (ambiguity
`UNRESOLVED`). `quantitative_error` stays NULL; no percentage was derived; the interpretation
was not decided by curve closeness.

---

## Part B — B3 source chain: Li et al. 2023, Fig. 4(c)

### B.1 What Fig. 4(c) is

A **bilayer** (periodic laminate of two different **dipolar gradient** thermoelastic solids,
cell `a = a1 + a2`) in the **normal (vertical) propagation** situation, with the
**thermoelastic coupling ignored**; the solid curves are the paper's own (“Present”) result and
the dashed curves are the literature comparison. It is **not** homogeneous, **not** a pure
gradient-only model and **not** a dipolar-gradient-with-thermoelasticity case.

### B.2 Chain elements (verbatim location)

| element | where | content |
|---|---|---|
| caption | p. 15 (journal p. 5728) | “Figure 4. Comparison of dispersion and bandgap with existing literatures. (a) and (b) the dispersion curves for the classic elastic solids and the comparison with literature [59] and [34]; (c) the dispersion curves for the gradient elastic solids and the comparison with literature [34].” — **no parameter list** |
| body text | p. 15 | “Figure 4(c) shows the dispersion and bandgap for the dipolar gradient elastic solids but ignoring the thermoelastic coupling in the present model. It is noted that there is still a good consistence between our results and that reported in literature [34].” |
| equation of motion | p. 9, Eq. (26) | `(1 − c∇²)[(λ+μ)∇∇·u + μ∇²u] − ℜ∇θ = (1 − (d²/3)∇²) ρü` |
| dilatational / distortional split | p. 9, Eq. (28a,b) | `cμ∇⁴ψ − μ∇²ψ + ρψ̈ − ρ(d²/3)∇²ψ̈ = 0` |
| wave decomposition | p. 10–11, Eq. (33) | `ψ = F1 e^{i(ξx+βSV y−ωt)} + F2 e^{i(ξx−βSV y−ωt)} + D1 e^{−γSS y+i(ξx−ωt)} + D2 e^{γSS y+i(ξx−ωt)}` |
| state vector | p. 11, Eq. (34) | `{V} = {ux, uy, ux,y, uy,y, θ, Px, Py, Rx, Ry, qy}ᵀ` |
| tractions | p. 11 | `Px = 2μ(1−c∇²)εyx − c[…] + ρ(d²/3)üx,y`, `Rx = 2μcεyx,y`, `Ry = c[(λ+2μ)εyy,y + λεxx,y]` |
| transfer matrix | p. 12, Eqs. (35)–(37) | `{V_R} = [PR][PL]⁻¹{V_L} = [T]{V_L}`, `[Tj] = [P0j][G(aj)][P0j]⁻¹` |
| interface / Bloch | p. 13, Eqs. (38)–(42) | perfect-interface continuity `{V_L^A} = {V_R^A}`; `{V_R^B} = [T_B][T_A]{V_L^A}`; Bloch `{V_R^B} = e^{ika}{V_L^A}` with `a = a1 + a2`; `det([T_B][T_A] − e^{ika}[I]) = 0` |
| normal-propagation block | p. 13, Eqs. (44)–(45) | longitudinal and transverse fields; transverse: `Px = μ(1−c∇²)ux,y + ρ(d²/3)üx,y`, `Rx = μc ux,yy` |
| parameter definitions | p. 14 | `λ̄1 = λ1/(ρ1a1²ω0²)`, `μ̄1 = μ1/(ρ1a1²ω0²)`, **`c̄1 = c1/a1²`**, **`d̄1 = d1/a1`**, `C̄r1`, `ℜ̄1`, `κ̄1`, `τ̄1 = τ01ω0`; ratios `λR, μR, ρR, cR = c̄2/c̄1, dR = d̄2/d̄1, CrR, ℜR, κR, T0R, τR, aR = a2/a1`; **`k̄ = ka1/π`**, `ξ̄ = ξa1/π`, `ω̄ = ω/ω0`, `αR = α2/α1` |
| parameters given | p. 14 | `a1 = 10⁻⁵ m`, `ρ1 = 7.5×10³ kg/m³`, `μ1 = 2.3×10¹⁰ Pa`, `T01 = 300 K`, `ω0 = 4.1×10⁸ Hz`, `λ̄1 = 0.928`, `μ̄1 = 0.182`, `C̄r1 = 0.069`, `ℜ̄1 = 0.0167`, `κ̄1 = 2.3×10⁻⁵`, `λR = 0.047`, `μR = 0.056`, `ρR = 0.157`, `CrR = 2.257`, `ℜR = 0.057`, `κR = 0.407`, `T0R = 1`, `aR = 1` |
| base quantities | p. 14 | “Choosing `(a1, ρ1, T01)` and `ω0 = 2π/(a1/√(μ1/ρ1) + a2/√(μ2/ρ2))`” (transit-time form) |
| material assignment | p. 14 | “We choose material A is lead and material B is brass here.” |
| tables | — | **none** (no numeric tables in the paper) |
| Fig. 3 and its caption | p. 15 | “(a) Classical elasticity (c̄1 = c̄2 = d̄1 = d̄2 = τ̄1 = τ̄2 = α1 = α2 = 0); (b) **Gradient elasticity (c̄1 = 0.15, cR = 1.5, d̄1 = 0.25, dR = 1.5, τ̄1 = τ̄2 = α1 = α2 = 0)**; (c) Thermal and gradient elasticity (c̄1 = 0.15, cR = 1.5, d̄1 = 0.25, dR = 1.5, τR = 1, αR = 1)” |
| explicit Fig. 3(b) → Fig. 4(c) inheritance statement | — | **NONE FOUND** (searched the captions, the whole §6 discussion, and the conclusions) |
| Appendix 3 (transverse [P0]) | p. 22 | `p11 = iσSV, p12 = −iσSV, p13 = −τSS, p14 = τSS; p21 = p22 = σ²SV, p23 = p24 = τ²SS; p31 = p32 = −(μ−D)σ²SV − μcσ⁴SV, p33 = p34 = (μ−D)τ²SS − μcτ⁴SS; p41 = −cμiσ³SV, p42 = cμiσ³SV, p43 = −cμτ³SS, p44 = cμτ³SS`, with `D = ρd²ω²/3` |
| reference [34] | p. 21 | “Li YQ, Wei PJ. **Band gaps of elastic waves in 1-D phononic crystal with dipolar gradient elasticity.** Acta Mech. 2016;227:1005–1023.” (same authors as the present paper) |

Definitions of the symbols requested by the phase brief: `c` and `d` are the micro-stiffness
(length²) and micro-inertia (length) parameters of dipolar gradient elasticity, entering the
governing equation as shown above; `c̄1 = c1/a1²`, `d̄1 = d1/a1`; `a1`, `a2` are the two layer
thicknesses, `aR = a2/a1`; `ρ, μ, λ` are the mass density and the Lamé constants, normalised with
`(ρ1, a1, ω0)`; `ω0` is the **transit-time** frequency; `k̄` is printed as `ka1/π`; the branch
convention is the MT1/MT2/MT3 (longitudinal-thermal) plus SV/SS (transverse) mode set, with the
SS mode evanescent.

### B.3 Independent re-derivation of the B3 machinery (this phase)

An independent implementation was written **from the source's own Appendix 3**, forming
`[T] = [P0][G][P0]⁻¹` with `[G] = diag(e^{iσa}, e^{−iσa}, e^{−τa}, e^{τa})` and the σ/τ roots of
the source's own quartic (`σ² = (Δ−(1−ms))/(2c)`, `τ² = (Δ+(1−ms))/(2c)`, `ms = ω²d²/(3Vs²)`,
`Δ = √((1−ms)² + 4cω²/Vs²)`). Results (`evidence/p12v/b3_formulation_identity.txt`):

* the construction reproduces the **repository's closed-form layer matrix** to
  max|ΔT|/scale ≈ 1.2×10⁻¹⁶ … 5.0×10⁻¹⁶ (i.e. exactly, at 60-digit arithmetic) — the
  repository implements the source's formulation, not an approximation of it;
* the **verbatim printed second row** of Appendix 3 (`u,y = +σ²SV` for the propagating pair) is
  inconsistent with row 1 (`u = iσSV`); read literally it differs from the repository matrix by
  O(10⁻⁸…10⁻⁷) relative → it differs by a *column sign convention* (a diagonal similarity), which
  leaves the Bloch eigenvalues unchanged. Consequence: none for the band structure when handled
  consistently, but a naive verbatim transcription of Appendix 3 is not usable as printed;
* the **cell eigenvalues** re-evaluated at 60 and 120 digits reproduce the repository's band
  edges exactly: propagating at ω̄ = 0.15 (k̄ = 0.33929), 0.30 (0.73938), gap at ω̄ = 0.3391,
  second band from ω̄ = 1.021 (k̄ = 0.9758) — identical to `b3_dispersion()` and to the record
  (`reproduced_gaps` = [[0.3391, 1.0213], [1.4185, 1.8676], [2.4738, 2.9080]]);
* the same machinery reproduces the **published classical panels** — independent Rytov
  computation with the source's own materials and transit-time `ω0 = 4.114233×10⁸ rad/s`
  (vs stated 4.1×10⁸): transverse intervals 0–0.1947, 0.7421–0.8308, 1.2424–1.3745,
  1.5831–1.7006; digitised published Fig. 4(b) solid: 0.189, 0.725, 1.374, 1.511 at k̄ = ±1 and
  0.792, 1.238, 1.638 at k̄ = 0. **This agreement also fixes the abscissa convention**: the
  published panels are consistent with the **cell** abscissa `k̄ = k(a1+a2)/π`, not with the
  printed `k̄ = ka1/π` (which would differ by a factor 2 when `aR = 1`).

### B.4 The nine enumerated questions

1. **Caption contents** — no parameter list, no geometry, no data statement (B.2 row 1).
2. **Surrounding text** — one sentence (B.2 row 2): “dipolar gradient elastic solids but
   ignoring the thermoelastic coupling”; no numbers.
3. **Dipolar-gradient equations** — fully stated (Eqs. 26, 28, 33–45, Appendices 1–3).
4. **Transfer-matrix / Bloch formulation** — fully stated (Eqs. 35–43); verified equivalent to
   the repository implementation (B.3).
5. **Parameter definitions** — fully stated (p. 14), including `c̄1 = c1/a1²`, `d̄1 = d1/a1`,
   `k̄`, `ω̄`.
6. **Tables / data availability** — none.
7. **Fig. 3 and its caption** — the only place in the paper where a gradient parameter set is
   stated numerically (Fig. 3(b)); it belongs to a **different figure**, which also carries the
   thermoelastic switch off but is a three-model comparison, not the literature comparison.
8. **Explicit inheritance Fig. 3(b) → Fig. 4(c)** — **NOT PRESENT** in the source.
9. **Reference [34] and the curve identities** — [34] = Li & Wei, *Acta Mech.* 227:1005–1023
   (2016); the Fig. 4(c) legend distinguishes **solid “Present”** (this paper) from **dashed
   “Li and Wei [34]”** (literature). The three curve identities (classical limit, literature
   dashed curve, present dipolar-gradient curve) are **never** to be conflated.

### B.5 Residual mismatch (no tuning)

The reproduction's lowest branch tops at ω̄ = **0.3391** at k̄ ≈ 0.99; the published Fig. 4(c)
lowest **solid** curve reaches ω̄ ≈ **0.433** at k̄ = ±1 (independent digitisation this phase) /
**0.436** (P12T measurement). Residual ≈ −0.09…−0.10 in ω̄. The same machinery reproduces the
published **classical** panels, which localises the residual to the *dipolar-gradient
configuration actually used for Fig. 4(c)* — a quantity the source never states. Consistent with
the P12S/P12T rule, no parameter was scanned or tuned to remove this residual.

### B.6 Verdict (B3)

**`SOURCE-AMBIGUOUS — DATA REQUIRED`.** B3 remains **`NOT_VALIDATED`**, now with the added,
verified statements that (i) the implementation machinery *is* the source's formulation and is
numerically sound at 60/120 digits, and (ii) the residual is a source-side gap, not an
implementation defect.

---

## Part C — convention-difference matrix

| # | Item | Paper definition | Current implementation | Match? | Consequence |
|---|---|---|---|---|---|
| 1 | `ω0` (B3) | transit-time: `2π/(a1/√(μ1/ρ1) + a2/√(μ2/ρ2))`; stated value `4.1×10⁸ Hz` | `2π/(a1/Vs1 + a2/Vs2)` = 411 423 336.098 rad/s | **yes** (definition) | reproduces the stated number to 0.35 %; no effect on ω̄ ratios |
| 2 | unit label of `ω0` | labelled “Hz” while defined with `2π/…` (angular) | treated as angular (rad/s) | definition yes, label no | none for band ratios; documented unit-label inconsistency in the source |
| 3 | frequency vs angular frequency | `ω̄ = ω/ω0` with `ω = 2πf` in the wave factors | same | **yes** | none |
| 4 | `k̄` (B3) | printed `k̄ = ka1/π` (layer thickness) | `k̄ = k(a1+a2)/π` (cell), from the Bloch phase of `[T_B][T_A]` | **no (definition), yes (as plotted)** | factor-2 abscissa if taken literally; the published classical panels (0.071 at k̄=0.25, 0.189 at k̄=1) agree with the **cell** abscissa, so the printed form is inconsistent with the source's own figures |
| 5 | `k̄` (B2) | `k̄ = kb/π`, `b = aA + aB` | same | **yes** | none |
| 6 | branch ordering / state vector | MT1–MT3 (longitudinal) + SV/SS (transverse), `{u, u,y, P, R}` block for SH | 4×4 `{u, u,y, P, R}` block | **yes** (eigenvalues verified equal) | printed row-2 sign is a column convention; similarity-invariant |
| 7 | solid/dashed curve identity (Fig. 4) | solid = “Present” (paper), dashed = literature | record distinguishes “Present” from dashed [34] throughout | **yes** | prevents conflation of the present model with the literature curve |
| 8 | classical limit | Fig. 4(a)/(b) classical solids | independently reproduced (0.1947/0.7421/1.2424 …) | **yes** | validates materials, `ω0` and cell abscissa |
| 9 | gradient limit | `c̄1 = 0.15`, `d̄1 = 0.25`, `cR = dR = 1.5` (Fig. 3(b) caption only) | same values used for the B3 comparison | values yes, **inheritance not stated** | residual in B5 cannot be attributed to the implementation |
| 10 | dipolar length normalisation | `c̄1 = c1/a1²`, `d̄1 = d1/a1` | `c = c̄1·a1²`, `d = d̄1·a1` | **yes** | verified in code and in the closed form |
| 11 | sign of the higher-order term | `(1 − c∇²)`, micro-inertia `(1 − (d²/3)∇²)ρü` | `σ², τ²` from `cμk⁴ + (μ − ρω²d²/3)k² − ρω² = 0` | **yes** (re-derived this phase) | none |
| 12 | interface conditions | continuity of `{u, u,y, P, R}` (perfect interface) | state-vector continuity through `[Tj]` | **yes** | none |
| 13 | Bloch phase | `e^{ika}` with `a = a1 + a2` | `eig(T_B T_A)`, `k̄ = |arg λ|/π` | **yes** | none |
| 14 | material normalisation / factor `d²/3` | `ρ̄, ā3, c̄33, f̄, l̄, l1`, `μ̄1`, `λ̄1`; `d²/3` in the inertia operator | same normalisations and the same `d²/3` | **yes** | none |
| 15 | factor 2/3 and `d²/3` (B2) | `f̄ = f/(b²ω0√(ρa3))`, `c̄33 = c33/(ρb²ω0²)` | not used (B2 blocked upstream) | n/a | blocked by the B2 ambiguity |

---

## Part D — reference-audit

* Fig. 4(a) legend (raster): dashed curve labelled “Zheng and Wei **[59]**”; the caption of
  Fig. 4 lists “[59] and [34]”; the **body text** of the same page cites “[65] and [34]”.
  In the reference list, **[59]** is an unrelated buckling paper (Derbale, Bouazza & Benseddiq),
  whereas **[65]** is “Zheng M, Wei PJ. Band gaps of elastic waves in 1-D phononic crystals with
  imperfect interfaces. Int J Mine Metall Mater. 2009;16(5):608–614.” → the caption/legend label
  is a source-side citation slip; the intended reference is [65].
* **[34]** = Li & Wei, *Acta Mech.* 227:1005–1023 (2016) — the same authors' 1-D dipolar
  gradient phononic-crystal band-gap paper; it is the dashed curve in Figs. 4(b) and 4(c).
* Curve identities are kept distinct everywhere in this audit: **classical limit** (panel (a)/(b)
  solid) ≠ **literature [34]** (dashed) ≠ **present dipolar-gradient model** (panel (c) solid).

---

## Part E — classification of the missing items

| item | B2 | B3 |
|---|---|---|
| explicit dimensional parameter value | **NOT PROVIDED** | **EXPLICITLY PROVIDED** (`a1`, `ρ1`, `μ1`, `ω0`, ratios) |
| dimensionless definition of the gradient parameters | **EXPLICITLY PROVIDED** (`l̄ = l/b`, `l̄1 = l1/b`) | **EXPLICITLY PROVIDED** (`c̄1 = c1/a1²`, `d̄1 = d1/a1`) |
| which of `l` / `l̄` the caption number denotes | **ONLY INFERABLE** (unbarred symbol, no unit) | n/a |
| sentence linking caption values to the dispersion equation | **NOT PROVIDED** | **NOT PROVIDED** |
| inheritance of Fig. 3(b) parameters into Fig. 4(c) | n/a | **ONLY INFERABLE** |
| abscissa definition actually used in the panels | **NOT PROVIDED** | **DERIVABLE FROM SOURCE** (cell abscissa, from the published classical panels) |
| numerical tables | **NOT PROVIDED** | **NOT PROVIDED** |
| erratum / correction / supplement | **NOT PROVIDED** | **NOT PROVIDED** |

**Is a faithful reproduction possible without author data?** — **No** for both B2 and B3 as
published panels: each has at least one quantity that the source does not state (B2: the
dimensional/normalised meaning of the caption `l`; B3: the parameter set and normalisation
actually used for Fig. 4(c)). “Inferable” is not “provided”.

---

## Part F — no-tuning statement

Only exact source-defined transformations, unit/normalisation conversions, branch relabelling
and mathematically equivalent formulation checks were performed:

* re-derivation of the σ/τ roots from the source's own quartic (algebraic identity);
* `[P0][G][P0]⁻¹` built from Appendix 3 (exact, verified to ~10⁻¹⁶ at 60 digits);
* classical-limit evaluation with the source's own materials and stated conventions;
* digitisation used for registration/structure only.

Not performed: no scanning of unknown parameters, no selection by visual agreement, no change
of material properties, interface/boundary conditions or normalisation without source evidence.
No tuning route was opened into the validation pipeline.

---

## Part G — decisions

| benchmark | decision (one of the permitted set) |
|---|---|
| **B2** | **`SOURCE-AMBIGUOUS — DATA REQUIRED`** (not `RESOLVED_FROM_SOURCE`; not `RESOLVED_BY_CORROBORATING_SOURCE`) |
| **B3** | **`SOURCE-AMBIGUOUS — DATA REQUIRED`** (not `SOURCE-SUFFICIENT`; the mismatch is a source-side gap, and the formulation is *not* unreconstructable — it has been reconstructed and verified) |

`NOT_VALIDATED` **remains correct for both**; no PASS was forced; `quantitative_error` remains
NULL for B2 and B3.

---

## Part H — precise missing information (internal only — nothing sent)

* **B2:** the meaning of the caption value for Fig. 2(b): is `l = 10⁻⁵` the dimensional
  micro-stiffness length (and in which unit), or the dimensionless `l̄ = l/b`? Plus the layer
  thicknesses actually used for that panel. (One-line question on `l` vs `l̄` and the geometry.)
* **B3:** the parameter values and normalisation actually used to compute the solid “Present”
  curves of Fig. 4(c) (whether they are the Fig. 3(b) set), and the numeric data or the
  evaluation points of that curve; optionally the same for the dashed [34] curve.

Neither item changes the *materially different* nature of the existing blocker record; the
prepared author-data requests remain **unmodified and unsent**.

---

## Findings (reported, not silently fixed)

Two residual text-level items were found in the machine record while cross-checking, both in
`paper9/audit/benchmark_validation_record.json`, B3 block. They are **reported here only**; no
edit was made (the phase mandate is audit-only, and changing the record would also invalidate
its recorded `evidence_path_sha256`).

| id | location | issue | severity | note |
|---|---|---|---|---|
| **P12V-F1** | `benchmarks.B3.reproduction_status` | reads “lowest branch omega_bar(1) = 0.35 vs **source's own 0.50**” — the same conflation that P12T raised as F2 and that P12U corrected in `reason` (the source's own *gradient* curve is 0.436; 0.50 is the exact classical limit and the dashed literature [34] curve). The P12U guards cover `reason` but not this field. | low–medium | superseded value; `reason` already carries the correct attribution |
| **P12V-F2** | `benchmarks.B3.ambiguity_status` | reads “SOURCE_UNAVAILABLE (dipolar-gradient formulation/coefficient convention not pinned down)” — after this phase the formulation **has** been reconstructed and verified (repository matrix ≡ source Appendix 3 to ~1e-16), so the residual is the *unstated Fig. 4(c) configuration*, not the formulation. | low | superseded wording |

Both are text-level and change no route, gate or number: `route = NOT_VALIDATED`,
`quantitative_error = null` remain correct.

## Part I — manuscript impact

No manuscript edit. One clarification for any future impact proposal: an earlier wording
attributed the B3 residual to “the available dipolar-gradient implementation”; after this audit
the mechanism is verified to be the source's own formulation (numerically sound), so a future
note should attribute the residual to the **source's unstated Fig. 4(c) configuration**. No
change is proposed now.
