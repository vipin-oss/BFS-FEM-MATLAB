# PAPER 9 — CALCULATION MASTER PLAN (PHASE 0)

**Version:** 1.0 · **Date:** 2026-09-22 · **Status:** PHASE 0 — awaiting user lock
**Governing specification:** `/home/user/femcheck/blueprint/Paper9_Blueprint.tex` (LOCKED v1.3 = v1.2 + one
editorial-only fix, 32 pp; frozen v1.2/v1.3 copies in `plan/blueprint/` with `PROVENANCE.md`)
**Companion sources:** `femcheck/PAPER9_DESIGN.md`, `femcheck/ANCHOR_DATA_SHEET.md`, `femcheck/anchors/` (downloaded anchor PDFs + text extracts)

This document converts the locked blueprint into an executable, reproducible research
workflow. **It derives nothing, computes nothing and invents nothing.** Every number that
is not already fixed by the blueprint or by a downloaded published source is marked
`TO BE VERIFIED` / `TO BE LOCKED` and assigned to a phase.

Working rules adopted verbatim from the project instruction: sequential phases; one phase
locked at a time; no scope change; no invented results or literature values; missing data
marked, not guessed; published-paper validation mandatory and manuscript-visible; visual
match never sufficient where independent reproduction is required; no claim of pass before
the calculation exists.

**Implementation language decision (recorded, rule 7):** primary implementation is
**Python 3 + NumPy/SciPy + SymPy + matplotlib (vector PDF figures)**. Reason: the execution
environment has no MATLAB licence; the blueprint's checklist permits "MATLAB R20xxb /
Python 3.x"; Python guarantees that every reported number can be regenerated here.
Symbolic work (derivations, dimensional audit, asymptotics) is done in SymPy with exact
rational arithmetic wherever possible.

---

## A. MATHEMATICAL DEPENDENCY MAP

IDs `M1…M17`. "Eqs" refers to the blueprint equation register (main text (1)–(71),
appendices (A.1)–(A.6), (B.1)–(B.8)). Provenance tags: `[C]` published source,
`[A]` analytical derivation, `[S]` study/design choice (locked with justification).

| ID | Component | Eqs | Must be derived after | Assumptions | Input parameters | Mathematical output | Needed by |
|---|---|---|---|---|---|---|---|
| M1 | Ellipsoidal nonlocal averaging domain; second-moment characteristic-length tensor | (1)–(4) | — | microstructure fabric = ellipsoid; small strain | `l1,l2,l3` [S-prod], | `(AᵀA)=diag(l1²,l2²,l3²)` | M2, M6, M14 |
| M2 | Orientation rotation of the length tensor | (5)–(9) | M1 | rotation about z (plane strain) | `θ` [S-prod] | `(AᵀA)_rot` components; `g²₂₂(θ)` | M6, M14, sweeps S3–S6 |
| M3 | Kinematics (strain, strain gradient, 2D component count) | (10)–(12) | — | small strain | — | `ε_ij`, `η_ijk`, count | M4, M13 |
| M4 | Mindlin Form-II constitutive relations (Cauchy + double stress; isotropic 6th-order modulus `a1…a5`; plane-strain reduction) | (13)–(18) | M3 | Form II; linear; isotropic modulus shape with anisotropic length tensor entering `K_g` | `E,ν` [S-prod or C], `a1…a5` [A from M1/M2 in isotropic limit] | `σ_ij`, `τ_ijk`, Voigt forms | M6, M8, M14 |
| M5 | Micro-inertia kinetic energy and inertial operator | (19)–(21) | — | gradient (micro-) inertia only | `ℓ_i` [S-prod / C-anchor] | `ρ(ü_i − ℓ_i²ü_i,jj)` | M8, M14, M16, S9 |
| M6 | Strain energy density; positive definiteness; anisotropic gradient stiffness `K_g` | (22)–(26) | M1,M2,M4 | rotation preserves eigenvalues `{l²}` | — | `W`, definiteness conditions, `K_g` | M8, M14, verification 5f |
| M7 | Limit ladder (classical / isotropic / no-micro-inertia / 90° symmetry) | (27)–(30) | M4–M6 | — | — | four specialisations | Phase 2 checks, verification 5c/5e |
| M8 | Strong-form EOM; boundary & interface quantities (4 per direction: u, ∂u/∂n, traction, double traction) | (31)–(35) | M4,M5,M6 | perfect interfaces | — | EOM, `R_i`, BC set | M9, M15, bench reference TM (4 interface conditions) |
| M9 | Bloch theorem for a C¹ medium (phase on value **and** derivative DOFs, derived not asserted) | (36)–(43) | M8 | time-harmonic `e^{−iωt}`; infinite periodic medium | lattice `a1,a2` | phase-factor rules for `{u, u,x, u,y, u,xy}` | M15 (headline C3) |
| M10 | IBZ path Γ–X–M–Γ and k-sampling | (44) | M9 | square lattice | k-points/segment = **TO BE LOCKED [S] (TV4)** | sampled path | M15, all band results |
| M11 | Non-dimensionalisation (own scheme + anchor schemes A and B) | (45)–(47) | M9 | — | `ω0=√(μ/(ρL²))`; Anchor A: `k̄=k·a1/π, ω̄=ω/ω0(=4.1e8)`; Anchor B: `k̄=k·b/π, ω0=2π/(a_A/√(c33/ρ)+a_B/√(c'33/ρ'))` [C] | barred variables | all comparisons, Phase 3 |
| M12 | Observables: bands, complete/partial gaps, normalised gap width, `S_θ`, phase velocity, `v_g`, time-averaged energy flux + identity `v_g=⟨S⟩/(⟨W⟩+⟨T⟩)` | (48)–(52) | M9,M11 | gaps require periodic contrast (Case C only) | — | observable definitions | Phase 5 metrics, S7–S8, verification 5h |
| M13 | BFS bicubic Hermite rectangle: shape functions, `B`, `B_,i`, 32 DOF/cell, C¹ conformity | (53)–(56) | M3 | conforming in H² | — | element interpolation | M14 |
| M14 | Element matrices `K^c`, `K^g(θ,AR)`, `M0`, `M^g`; Gauss rule justification | (57)–(61) | M4,M6,M13,M5 | integrand ≤ quartic → rule stated & justified | `θ,AR,ℓ_i` | element matrices | M15 |
| M15 | Bloch master–slave elimination `T(k)`; reduced Hermitian eigenproblem; proof `K̄(k)=K̄(−k)^H`; scaling, κ, MAC branch tracking | (62)–(71) | M9,M14 | — | solver tolerances [S] | `ω_n(k̄)` bands | everything numerical |
| M16 | Appendix A high-k asymptotics (unbounded for `ℓ_i=0`, bounded otherwise; dimensional check) | (A.1)–(A.6) | M8,M11 | leading-order balance | — | asymptotic phase-velocity laws | S9, §7.4, PCR7, verification 5g |
| M17 | Appendix B energy-flux derivation (energy balance → classical + double-stress flux; time-average; dimensional check) | (B.1)–(B.8) | M8,M12 | lossless | — | `⟨S⟩`, identity | S8, verification 5h |

**Mathematical dependency chain (condensed):**
`M1→M2→M6` and `M3→M4→M6`; `M5→M8`; `M6,M4,M5→M8→M9→M15`; `M13→M14→M15`;
`M11→M12`; `M15+M12 → all band/gap/IFC/flux results`; `M16` supports M5/M8 admissibility
claims; `M17` supports M12 flux identity. Symbolic layer (Phase 1–2) precedes numeric
layer (Phase 3–5) for every component.

---

## B. CALCULATION PHASES (execution sequence)

Numbering follows the instruction. One scientifically necessary re-ordering is declared
(rule 7): **Phase 4 is split** — solver-acceptance tests (5a–5f) run *before* Phase 3
(validation), because running published benchmarks on an unverified solver wastes effort
and can mask implementation bugs as model error; this matches the blueprint's own gate
order (G2 before G3). The remaining Phase 4 work (5g, 5h, 5i + Table 4/Fig 5/Table 6)
completes after Phase 3.

| Phase | Content | Entry criterion | Exit gate |
|---|---|---|---|
| **0** | Blueprint study + this master plan + file architecture | — | **User locks Phase 0 checklist (below)** |
| **1** | Mathematical formulation & solver build: P1.1 symbolic M1–M8; P1.2 symbolic M9–M12; P1.3 BFS element + patch test; P1.4 element matrices + quadrature rule; P1.5 Bloch reduction; P1.6 eigen-solver + MAC tracker; P1.7 automated dimensional audit of every register equation | Phase 0 locked | **G1:** all symbolic identities exact (rational arithmetic); patch test passes; dimensional audit clean; code hashes recorded |
| **2** | Analytical calculations & limiting cases: P2.1 Case-H homogeneous dispersion closed form; P2.2 long-wave acoustic limit; P2.3 high-k asymptotics (Appendix A completed); P2.4 Appendix B derivation + dimensional check; P2.5 PB2009 Eqs (22)–(28) transcription + independent evaluator [TV10]; P2.6 LWZ2016 1D PC closed form [TV11]; P2.7 limit-ladder symbolic checks (M7) | G1 | **G1b:** every analytic expression verified by two independent routes (SymPy vs hand-coded numeric); units consistent |
| **4A** | Solver acceptance: verification tests 5a–5f | G1 | **G2a:** 5a–5f pass at stated tolerances |
| **3** | Published-paper validation: P3.0 anchor parameter audit (resolve TV1, TV2, TV8, TV12 from the downloaded originals); P3.1 independent 1D transfer-matrix reference implementation (classical + dipolar gradient, 4 interface conditions per interface); P3.2 benchmark B1 (Layer 1); P3.3 B2 (Layer 2a); P3.4 B3 (Layer 2b); P3.5 B4 (Layer 2c, optional); P3.6 Layer 3 (P2.5/P2.6 vs solver); P3.7 Layer 4 (optional, TV9); P3.8 error tables + Fig 4 overlays + Table 3 | G2a | **G3 (hard):** Layers 1, 2a, 2b ≤ 2 % max relative error (≤0.5 % target classical). Fail ⇒ stop, debug via ANCHOR_DATA_SHEET troubleshooting table |
| **4B** | Full verification: 5g, 5h, 5i (mesh convergence, observed rate + 95 % CI, resolution floor ε_Δ); Table 4, Fig 5, Table 6 | G3 | **G2:** all eight tests + 5i pass; ε_Δ definition locked with evidence |
| **5** | Main scientific study: S1–S9 (Case H bands; Case C baseline; θ sweep; AR sweep; 42-point map; polar map + regimes; IFC + steering metrics; energy-flux partition; micro-inertia study) | G2 | **G5:** all sweeps complete at locked resolution; every claim quantity (normalised gap width, S_θ, δ_max, steering FoM) computed and cross-checked against ε_Δ |
| **6** | Figures 1–13 and Tables 1–6 generated only from `results/processed/` by versioned generator scripts; style QC | G5 | **G-F:** every panel traceable to a processed-data hash; vector output; 8 pt minimum |
| **7** | Manuscript construction (sections per blueprint; floats embedded; validation evidence in main text; PCR cross-check) | G-F | draft complete; PCR1–8 evidence pointers filled |
| **8** | Bibliography construction & verification (.bib; 3 appearances per anchor; ≥40 % refs 2021+; no orphans) | draft | **G-B:** citation audit clean |
| **9** | Final submission audit: traceability matrix, PCR1–8, language/ethics/funding checks, reproducibility dry-run (clean-room re-execution of manifest) | G-B | **G4:** release of the five final deliverables |

---

**Execution order (explicit, unambiguous):**
`P0 → P1 → P2 → P4A → P3 → P4B → P5 → P6 → P7 → P8 → P9`.
Phase 4A (solver acceptance, tests 5a–5f) runs **before** Phase 3 because cheap internal
checks catch implementation bugs before expensive published-validation runs; this mirrors
the blueprint's own gate order (G2-family checks before G3) and does **not** alter the
blueprint's scientific validation framework (layer definitions, gate meanings and
evidence rules are unchanged). Phase 4B completes the remaining verification (5g, 5h, 5i)
after Phase 3.

**Gate terminology map (blueprint-locked vs plan-level):**

| Gate | Level | Meaning | Achieved at |
|---|---|---|---|
| G1 | blueprint-locked | symbolic checks pass (week 3) | Phase 1 exit |
| G1b | plan sub-gate | two-route analytic cross-verification | Phase 2 exit |
| G2a | plan sub-gate | solver acceptance, tests 5a–5f | Phase 4A exit |
| **G3** | **blueprint-locked HARD gate** | published validation Layers 1, 2a, 2b at ≤2 % (0.5 % classical target); evidence in main manuscript | Phase 3 exit |
| G2 | blueprint-locked | internal verification pass (week-6 scope; completed at 4B with 5a–5h + 5i) | Phase 4B exit |
| G5 | plan-level (**renamed from G3b** in Phase 0 fix v1.1) | Phase-5 study completeness; **not** a validation gate and unrelated to G3 | Phase 5 exit |
| G-F, G-B | plan-level | figure/table and bibliography audits | Phase 6 / 8 exit |
| G4 | blueprint-locked | submission-ready | Phase 9 exit |

The rename G3b→G5 removes the only name collision with a blueprint-locked gate; G3 always
means the published-paper validation hard gate.

## C. PHASE 1 — MATHEMATICAL FORMULATION (specification only, no derivation now)

Ordered derivation/computation tasks; "check" = automated acceptance test.

| # | Object | Blueprint eqs | Method | Acceptance check |
|---|---|---|---|---|
| F1 | Ellipsoidal domain + second-moment tensor (M1) | (1)–(4) | SymPy | `(AᵀA)=diag(l²)` exact |
| F2 | Rotation, components, `g²₂₂(θ)` (M2) | (5)–(9) | SymPy | eigenvalues of `(AᵀA)_rot` = `{l²}` for random θ (eq 25) |
| F3 | Kinematics (M3) | (10)–(12) | SymPy | 2D plane-strain component count |
| F4 | Form-II constitutive + plane-strain reduction (M4) | (13)–(18) | SymPy | major/minor symmetries of `C`, `A` |
| F5 | Micro-inertia operator via Hamilton (M5) | (19)–(21) | SymPy | EOM term matches (20) |
| F6 | Energy, definiteness, `K_g` (M6) | (22)–(26) | SymPy | `W>0` conditions; rotation-invariance of eigenvalues |
| F7 | Limit ladder (M7) | (27)–(30) | SymPy substitutions | each limit reduces symbolically |
| F8 | EOM + BC/interface set (M8) | (31)–(35) | SymPy | 4 boundary quantities per direction; interface count = 4 |
| F9 | C¹ Bloch phase rules (M9) | (36)–(43) | SymPy + derivation text | phase on `∇u`, `u,xy` derived from Bloch condition |
| F10 | Non-dimensionalisation incl. anchor schemes (M11) | (45)–(47) | SymPy units | barred equations dimensionless |
| F11 | Observables + flux identity statement (M12) | (48)–(52) | SymPy | identity matches Appendix B result |
| F12 | BFS element: shape fns, `B`, `B_,i`, 32 DOF (M13) | (53)–(56) | code + SymPy | partition of unity; Kronecker delta; C¹ patch test |
| F13 | Element matrices + quadrature rule (M14) | (57)–(61) | code | symmetry of `K`, `M`; quadrature exactness on quartic integrand |
| F14 | Bloch reduction + Hermitian proof + MAC tracker (M15) | (62)–(71) | code | `‖K̄(k)−K̄(−k)^H‖/‖K̄‖<1e-12` symbolically for a 1-element model, numerically later |

## D. PHASE 2 — ANALYTICAL VALIDATION (specification only)

| # | Calculation | Purpose | Output |
|---|---|---|---|
| A1 | Homogeneous-medium (Case H) in-plane dispersion: longitudinal/shear branches with `(AᵀA)_rot`, with/without `ℓ_i` | closed-form reference for solver (Layer 3, Fig 6 context) | `ω̄(k̄,θ,AR)` formulas |
| A2 | Long-wave limit `ω→c|k|` (acoustic slopes `c_L,c_T`) | verification 5d reference | slope formulas |
| A3 | High-k asymptotics (Appendix A): unbounded phase velocity for `ℓ_i=0` (growth law), bounded for `ℓ_i>0` (limit value) | admissibility claim; verification 5g reference; §7.4 | (A.1)–(A.6) |
| A4 | Energy-flux derivation (Appendix B) + dimensional check | §3.5 Eq (52), §7.3, verification 5h | (B.1)–(B.8) |
| A5 | PB2009 closed-form dispersion (infinite medium + axial bar, `g²`,`h²`) [TV10] | Layer 3 machine-precision benchmark | evaluator script |
| A6 | LWZ2016 1D dipolar-gradient PC closed form [TV11] | Layer 3b benchmark | evaluator script |
| A7 | Limit-ladder + symmetry analytic checks (M7) | verification 5c/5e references | symbolic pass log |

## E. PHASE 3 — PUBLISHED-PAPER VALIDATION (hard requirement)

**Card ↔ Blueprint v1.2 mapping (verified against the validation matrix; nothing invented):**

| Card | Blueprint matrix row | Layer | Source | Type | Hard gate (G3)? | Required evidence |
|---|---|---|---|---|---|---|
| B1 | row 1 | 1 | Li, Li, Guo et al. 2024, *Sci. Rep.* 14:24035, Fig 2(a) | published | **YES** | Fig 4(a) overlay + Table 3 (branches, gap edges, per-quantity & max error, PASS/FAIL) |
| B2 | row 2a | 2 | same paper, Fig 2(b) | published | **YES** | Fig 4(b) + Table 3 |
| B3 | row 2b | 2 | Li, Askes, Gitman, Krynkin & Wei 2023, *WRAM* 36(4):5715–5735, Fig 4(c) | published | **YES** | Fig 4(c) + Table 3 |
| B4 | row 2c | 2 | same 2023 paper, Fig 3 (first two cases) | published | no (optional) | gap-width comparison, §5.3 |
| B5 | row 3 | 3 | Papargyri-Beskou & Beskos 2009, *IJSS* 46:2151–2159, Eqs (22)–(28) | analytical | no (machine-precision) | §5.4 + Table 3 annex |
| B6 | row 3b | 3 | Li, Wei & Zhou 2016, *Acta Mech.* 227:1005–1023 | analytical | no | §5.4 |
| B7 | row 4 | 4 | Mishra, Kumar & Sharma 2026, *Acta Mech.* 237:3951–3982 | published (independent method) | no (optional) | §5.5 |

Layer-5 rows (5a–5i) are internal verification and carry **no** B-card. Cards whose panel-level
parameters are not yet extracted remain marked TO BE VERIFIED inside each card (TV register).

Benchmark cards. Values quoted below are **already extracted** from the downloaded
published sources (`femcheck/anchors/`, `ANCHOR_DATA_SHEET.md`); anything not extractable
is marked `TO BE VERIFIED FROM ORIGINAL PUBLISHED PAPER`.

### B1 — Layer 1, classical elasticity limit (GATE)
- **Source:** Li, Li, Guo et al. (2024) *Sci. Rep.* **14**:24035, Fig 2(a). [C]
- **Reproduce:** classical (non-gradient) 1D bilayer dispersion + Bragg gaps.
- **Their model:** 1D periodic bilayer, classical elasticity, transfer matrix, `det([T_B][T_A]−e^{ikb}I)=0` (their Eq 53 with `l̄=ℓ̄_i=f=0`).
- **Parameters [C]:** AlN: ρ=3.23e3, c33=3.9e11; BaTiO₃: ρ'=5.8e3, c'33=1.62e11; a_A=a_B=0.01 m; ω0=2π/(a_A/√(c33/ρ)+a_B/√(c'33/ρ')); k̄=k·b/π, ω̄=ω/ω0. (`b` definition = a_A+a_B assumed — **TV2**.)
- **Our calculation:** (i) independent TM reference with our own code; (ii) our 2D C¹ Bloch FE reduced to the 1D normal-incidence bilayer (Layer-1 configuration).
- **Compare:** first four branch frequencies at stated k̄ + gap edges; quantities ω̄(k̄).
- **Error:** `e=|ω̄_ours−ω̄_ref|/ω̄_ref` per branch and per gap edge; max over set.
- **Plot/table:** Fig 4(a) overlay; Table 3 rows. **Criterion:** ≤2 % (target ≤0.5 %). **Manuscript:** §5.2, Fig 4, Table 3.

### B2 — Layer 2a, gradient elasticity, flexoelectricity suppressed (GATE)
- **Source:** same paper, Fig 2(b). [C]
- **Their model:** strain gradient + micro-inertia, flexoelectric off (`f=0`), EOM `σ_zz,z−μ_zzz,zz=ρ(ü_z−l₁²ü_z,zz)` (their Eq 17; note sign).
- **Parameters [C]:** as B1 plus `l̄=1e-5`, `ℓ̄_i=2e-5`, `f=0` (blueprint §5.3 locked).
- **Our calculation:** independent TM reference (gradient version, 4 interface conditions) + our FE in the same 1D limit.
- **Compare/error/plot/table/criterion/manuscript:** as B1 → Fig 4(b), Table 3, §5.3; ≤2 %.

### B3 — Layer 2b, isothermal dipolar-gradient bilayer (GATE, decisive)
- **Source:** Li, Askes, Gitman, Krynkin & Wei (2023) *Waves Random Complex Media* **36**(4):5715–5735, Fig 4(c) ("dipolar gradient elastic, thermoelastic coupling ignored"). [C]
- **Their model:** 1D Pb/brass bilayer, dipolar gradient elasticity, transfer matrix + Bloch.
- **Parameters [C, extracted]:** a₁=1e-5 m, a₂/a₁=1, ρ₁=7.5e3 kg/m³, μ₁=2.3e10 Pa, ω₀=4.1e8 Hz; k̄=k·a₁/π, ω̄=ω/ω₀; layer ratios λ_R=0.047, μ_R=0.056, ρ_R=0.157 (dimensional brass constants therefore not required for non-dimensional reproduction).
- **TO BE VERIFIED FROM ORIGINAL PUBLISHED PAPER (TV1):** the gradient-length and micro-inertia non-dimensional values (their c̄₁,c̄_R,d₁,d̄_R) used *in Fig 4(c)*; and the axis ranges/sampling for overlays (TV12).
- **Our calculation:** independent TM reference from their published equations + our C¹ Bloch FE in the 1D isothermal limit.
- **Compare:** dispersion branches + band-gap edges; first four branch frequencies at stated k̄.
- **Error/plot/table/criterion:** as B1 → Fig 4(c), Table 3, §5.3; ≤2 %.
- **Note (manuscript argument):** they use a transfer matrix, we a C¹ Bloch FE — method difference is the validation strength.

### B4 — Layer 2c, three-case band gaps (optional, not a gate)
- **Source:** same 2023 paper, Fig 3 (cases: classical / gradient / gradient-thermoelastic; first two only in our scope).
- **TO BE VERIFIED (TV8):** parameter sets per panel. Compare gap widths; report as optional configuration; no gate.

### B5 — Layer 3, closed-form analytic (mandatory, machine precision)
- **Source:** Papargyri-Beskou & Beskos (2009) *IJSS* **46**:2151–2159, Eqs (22)–(28) [TV10 transcription check].
- **Our calculation:** Case-H numerical bands vs their infinite-medium and axial-bar formulas; relative error target ~1e-10 (machine-precision class).
- **Evidence:** §5.4 text + Table 3 annex row; no new figure (blueprint keeps Fig count).

### B6 — Layer 3b, 1D dipolar-gradient PC closed form (analytic)
- **Source:** Li, Wei & Zhou (2016) *Acta Mech.* **227**:1005–1023 [TV11].
- **Compare:** 1D band structure; machine-precision class.

### B7 — Layer 4, independent published method (optional)
- **Source:** Mishra, Kumar & Sharma (2026) *Acta Mech.* **237**:3951–3982 (dynamic stiffness + Wittrick–Williams).
- **TO BE VERIFIED (TV9):** homogeneous-limit configuration used for cross-check. Optional layer; reported if retrievable.

**Independent-reproduction protocol (locked, blueprint §5):** reference values are
recomputed from the anchors' published equations/parameters with an independently written
TM code; digitised curves are used **only** to draw overlays, never to compute errors;
geometry, constants, constitutive assumptions, the four interface conditions, scaling and
axes are preserved exactly.

## F. PHASE 4 — NUMERICAL VERIFICATION (Layer 5)

**Definitive test count (verified against Blueprint v1.2, Phase 0 fix):** the locked internal
consistency **suite = eight automated tests 5a–5h** (blueprint §5.6 and Table 4). Row **5i**
is the **mesh-convergence / resolution-floor study** (blueprint matrix row 5i, §5.7; reported
in Fig 5 and Table 6): a mandatory Layer-5 verification row but **not** a ninth suite test.
Layer 5 therefore comprises **nine verification rows 5a–5i** = eight-test suite (Table 4)
+ convergence/resolution study (Fig 5, Table 6). No document may state "nine tests" nor count
5i inside the eight-test suite.

VALIDATION = agreement with external published/analytical reference (Layers 1–4).
VERIFICATION = internal mathematical/numerical consistency (Layer 5). The internal tests
are never described as published validation.

| Test | Purpose | Input | Calculation | Expected | Acceptance | Output | Manuscript |
|---|---|---|---|---|---|---|---|
| 5a | Hermiticity | reduced matrices on standard k-sweep | `‖K̄(k)−K̄(−k)^H‖/‖K̄‖` | 0 | <1e-12 every run | log + Table 4 | §5.6 |
| 5b | BZ periodicity | `ω(k+G)` vs `ω(k)` | max rel dev | 0 | <1e-10 | Table 4 | §5.6 |
| 5c | Rotational invariance AR=1 | θ-rotated runs | band rel dev | 0 | <1e-10 | Table 4 | §5.6 |
| 5d | Long-wave slope | k̄→0 vs A2 slopes | rel err of `c_L,c_T` | 0 | <1e-6 | Table 4 | §5.6 |
| 5e | 90° symmetry `l1↔l2` | paired runs | band rel dev | 0 | <1e-10 | Table 4 | §5.6 |
| 5f | Positive definiteness | `K̄,M̄` | Cholesky / min eig | >0 | success all k | Table 4 | §5.6 |
| 5g | Bounded phase velocity | `ℓ_i=0` vs `>0`, k→BZ edge; vs A3 growth law | phase-velocity trend | unbounded / bounded | qualitative + asymptotic rate match | Fig 13(b), Table 4 | §7.4, App A |
| 5h | Energy-flux identity | `⟨S⟩` vs `(⟨W⟩+⟨T⟩)v_g`; `v_g` vs central-diff `∇_kω` | rel norms | 0 | <1e-6 (identity), <1e-4 (v_g, step-studied) | Table 4 | §7.3, App B |
| 5i | Mesh convergence + resolution floor | meshes 4²,8²,16²,32² | gap-edge sequence; log-log LSQ fit | monotone convergence | observed rate with 95 % CI reported; **no theoretical order claimed**; ε_Δ = locked operational floor; 16²→32² change ≤ ε_Δ | Fig 5, Table 6 | §5.7 |

ε_Δ operational definition (to be locked in Phase 4B with evidence, [S-evidence]):
candidate = max over IBZ of |ω(32²)−ω(extrapolated)|; final wording fixed when computed.

## G. PHASE 5 — MAIN SCIENTIFIC STUDY

Locked ranges from blueprint §6–§7. Production material/geometry parameters for Case H/C
are **not** fixed by the blueprint → **TO BE LOCKED in Phase 5 as [S] design choices with
written justification** (TV6): `E,ν,ρ,l1,l2,ℓ_i,L`, inclusion radius & contrast. Mesh and
k-sampling from 5i/TV4. Bands reported: lowest N with documented spurious-branch filter
(N = **TO BE LOCKED [S]**, TV7).

| # | Study | Parameters / resolution | Baseline | Output | Quantity extracted | Fig/Table | Manuscript |
|---|---|---|---|---|---|---|---|
| S1 | Case H bands | AR=1 vs 10; locked mesh/k | AR=1 | bands Γ-X-M-Γ | microstructure-induced dispersion (no gaps) | Fig 6 | §6.2 |
| S2 | Case C baseline | locked mesh/k | — | bands + modes | first 3 complete/partial gaps, edges, widths | Fig 7, Table 5 | §6.3 |
| S3 | θ sweep | θ∈{0,15,…,90}° at AR=5 | θ=0 | stacked bands; gap edges vs θ | gap migration Γ-X→Γ-M | Fig 8 | §6.4 |
| S4 | AR sweep | AR∈{1,2,3,5,7,10} at θ=45° | AR=1 | bands; gap width vs AR | tunability | Fig 9 | §6.5 |
| S5 | Design map | 7×6=42 points | — | response surface + contour | first complete gap width(θ,AR) | Fig 10 | §6.6 |
| S6 | Polar map + regimes | (X=ARcosθ, Y=ARsinθ) | — | polar map; regime boundaries; inequality | complete-vs-partial classification | Fig 11, Table 5 | §6.7 |
| S7 | IFC + steering | 3 freq × 3 orientations | AR=1 | contours; δ vs direction | δ_max, steering FoM, normalised gap width, S_θ | Fig 12, Table 5 | §7.1–7.2 |
| S8 | Energy-flux partition | frequency sweep | — | classical vs gradient partition | flux ratio vs ω | Fig 13(a) | §7.3 |
| S9 | Micro-inertia study | ℓ̄_i=0 vs >0, k-sweep to BZ edge | ℓ̄_i>0 | phase velocity vs k | bounded/unbounded + A3 rate | Fig 13(b) | §7.4 |

## H. FIGURE / TABLE DEPENDENCY MAP

| Float | Purpose | Type | Source calculation | Needs earlier data? | Manuscript |
|---|---|---|---|---|---|
| Fig 1 | ellipsoid + rotated tensor | schematic | M1,M2 (analytic curves) | no (generated from formulas) | §2 |
| Fig 2 | lattice + IBZ | schematic | M10 | no | §3 |
| Fig 3 | BFS DOF + Bloch phase | schematic | M9,M13 | no | §4 |
| Fig 4 | anchor overlays (a)(b)(c) | **validation** | Phase 3 B1–B3 + digitised anchors (overlays only) | yes (P3) | §5 |
| Fig 5 | convergence + ε_Δ | **verification** | 5i | yes (P4B) | §5 |
| Fig 6 | Case H dispersion | result | S1 | yes | §6 |
| Fig 7 | Case C bands + modes | result | S2 | yes | §6 |
| Fig 8 | θ sweep | result | S3 | yes | §6 |
| Fig 9 | AR sweep | result | S4 | yes | §6 |
| Fig 10 | (θ,AR) map | result | S5 | yes | §6 |
| Fig 11 | polar map + regimes | result | S6 | yes | §6 |
| Fig 12 | IFC + δ | result | S7 | yes | §7 |
| Fig 13 | flux partition + micro-inertia | result + verification | S8,S9,5g | yes | §7 |
| Table 1 | literature positioning (+reported-quantity column) | review | manual + reference plan | no | §1 |
| Table 2 | parameters **with provenance tags** | input | params_master.yaml | yes (P5 lock) | §6 |
| Table 3 | anchor errors (branches, gap edges, per-qty, max, PASS/FAIL) | **validation** | P3 | yes | §5 |
| Table 4 | eight-test suite | **verification** | P4 | yes | §5 |
| Table 5 | gap summary + normalised width + S_θ | result | S2,S6,S7 | yes | §6 |
| Table 6 | convergence + observed rate + κ + ε_Δ | **verification** | 5i | yes | §5 |

## I. DATA & FILE ARCHITECTURE (created now, populated phase-by-phase)

```
femcheck/paper9/
  plan/          CALC_MASTER_PLAN.md, PHASE_LOG.md, lock checklists per phase
  eqs/           sym/ (SymPy scripts), derivations.md, eq_register_map.yaml (eq ↔ code ↔ manuscript)
  params/        params_master.yaml, anchor_A.yaml, anchor_B.yaml, PROVENANCE.md
  bench/         cards/ (B1–B7), reference_tm/ (independent transfer-matrix code), overlays/ (digitisation for plotting ONLY)
  analytic/      caseH/, asymptotics/, flux/, pb2009/, lwz2016/
  solver/        bfs/, bloch/, eigen/, tracking/, tests/
  validation/    L1/, L2a/, L2b/, L2c/, L3/, L4/, errors/
  verification/  suite/, convergence/
  production/    caseH/, caseC/, sweeps/, maps/, ifc/, flux/, microinertia/
  results/       raw/ (run outputs), processed/ (gap tables, metrics; ONLY source for figures/tables)
  figures/       gen/ (versioned generators), out/ (vector PDF)
  tables/        gen/, out/ (LaTeX fragments)
  latex/         ms.tex, elsarticle/, appendices/
  bib/           paper9.bib, audit/
  audit/         traceability_matrix.csv, pcr_checklist.md, final_audit.md
  release/       FINAL: (1) ms.tex (2) ms.pdf (3) paper9.bib (4) calculation package (5) reproducibility package
```
Run manifest per execution: `runs/<run_id>/manifest.json` = {run_id, UTC timestamp,
sha256 of every solver/eqs file, resolved parameter snapshot with provenance tags,
library versions, command line, sha256 of each output}.

## J. PARAMETER PROVENANCE

Tags: **[C]** canonical/published source (citation + location); **[A]** analytical
derivation (equation pointer); **[S]** study/design choice (written justification, phase,
who locked it). `params_master.yaml` schema per entry:
`{name, value, unit, tag, source, locked_in_phase, verified_by, run_id}`.
Rules: (i) the solver reads parameters **only** from params files — a lint check forbids
numeric literals in solver code; (ii) validation runs use immutable anchor copies
(tag `[C-anchor]`, file hash recorded); (iii) every number in Tables 2–6 and in manuscript
sentences traces to a params entry or a processed result; (iv) `[S]` entries require a
one-line justification and appear in Table 2 with the tag visible.
Currently known tags: anchor constants [C] (see cards B1–B3); sweep ranges θ, AR, map grid,
mesh levels [S-blueprint-locked]; Case H/C materials, L, inclusion contrast, k-points/
segment, N bands, ε_Δ definition → [S]-pending (TV4, TV6, TV7).

## K. ERROR & QUALITY CONTROL / TRACEABILITY

ID scheme: `EQ-n` (register), `RUN-id`, `RES-id` (processed quantity), `FIG-n`, `TAB-n`,
`MS-§x.y`. `audit/traceability_matrix.csv` rows: MS claim → FIG/TAB → RES → RUN → EQ →
params. Automated checks: dimensional audit (SymPy units, every register equation);
conditioning κ(θ,AR) reported per run; eigenvalue ordering + MAC continuation log with
step-halving events; convergence (5i); benchmark error (G3); reproducibility dry-run
(clean-room re-execution of one manifest per phase); figure/data consistency (generator
scripts embed processed-data sha256 into figure metadata); equation/result consistency
(manuscript numbers injected only from generated table/number snippets, never typed).
`plan/PHASE_LOG.md` records per phase: entry checklist, runs, gate decision, sign-off.

## L. FINAL ASSEMBLY LOGIC

calculations locked (G1,G1b,G2a) → validation locked (G3) → verification locked (G2) →
scientific results locked (G5) → figures/tables locked (G-F) → manuscript drafted (P7) →
bibliography verified (G-B) → LaTeX compiled & PDF checked → final audit (G4) →
**release/** receives the five deliverables, version-tagged `submission-v1.0`:
(1) `ms.tex`, (2) `ms.pdf`, (3) `paper9.bib`, (4) calculation package (`eqs/ analytic/
solver/ params/` + manifests), (5) reproducibility package (full `paper9/` snapshot minus
`release/`, with clean-room re-run instructions). No deliverable is finalised before G4.

---

## TO-BE-VERIFIED / TO-BE-LOCKED REGISTER (nothing guessed)

| ID | Item | Owner phase |
|---|---|---|
| TV1 | Anchor A Fig 4(c): gradient/micro-inertia non-dimensional values (c̄,d̄ set) for that panel | P3.0 |
| TV2 | Anchor B: `b` definition in k̄=k·b/π; Fig 2 axis ranges | P3.0 |
| TV4 | k-points per IBZ segment (blueprint §3.3 unspecified) | P5 (with 5i evidence) |
| TV6 | Case H/C production parameters (E,ν,ρ,l1,l2,ℓ_i,L, inclusion radius/contrast) | P5 [S] |
| TV7 | number of reported bands N + spurious-filter documentation | P4B/P5 [S] |
| TV8 | Anchor A Fig 3 per-panel parameter sets (optional 2c) | P3.0 |
| TV9 | Mishra 2026 homogeneous-limit configuration (optional L4) | P3.0 |
| TV10 | PB2009 Eqs (22)–(28) exact transcription | P2.5 |
| TV11 | LWZ2016 closed-form + parameters | P2.6 |
| TV12 | overlay axis ranges/sampling for Figs 4(a)–(c) | P3.0 |
| TV13 | ε_Δ operational definition final wording | P4B [S-evidence] |

## PHASE 0 LOCK CHECKLIST

- [ ] Blueprint v1.3 (= v1.2 + editorial-only Week-6 gate-wording fix) accepted as sole scientific specification (scope, exclusions, terminology).
- [ ] Phase sequence P0→P9 accepted with the explicit execution order P1→P2→P4A→P3→P4B→P5→P6→P7→P8→P9 (4A solver acceptance before P3; 4B after).
- [ ] Gates accepted per the gate terminology map: blueprint-locked G1, G2, G3 (≤2 %, 0.5 % classical), G4; plan-level G1b, G2a, G5 (formerly G3b, renamed in Phase 0 fix), G-F, G-B.
- [ ] Mathematical dependency map M1–M17 accepted.
- [ ] Benchmark cards B1–B7 accepted; hard gates = B1, B2, B3; evidence-in-manuscript rule confirmed.
- [ ] Verification structure accepted: eight-test suite 5a–5h (Table 4) + mesh-convergence/resolution-floor row 5i (Fig 5, Table 6) = nine Layer-5 verification rows; tolerances accepted.
- [ ] B1–B7 ↔ blueprint matrix mapping confirmed (Section E table); hard gates = B1, B2, B3 only.
- [ ] Production study list S1–S9 and locked sweep ranges accepted; no added studies.
- [ ] Figure/table map (13 figs, 6 tabs) accepted — no new floats.
- [ ] File architecture and run-manifest/provenance/traceability system accepted.
- [ ] TV register accepted: listed items will be read from originals or locked as [S], never guessed.
- [ ] Python 3 + NumPy/SciPy/SymPy as primary implementation accepted.
- [ ] No Phase 1 work begins until the user explicitly instructs it.

---

## PHASE 0 CONSISTENCY-FIX RECORD (plan v1.0 → v1.1, 2026-09-22)

1. **Test count.** Verified against Blueprint v1.2 (§5.6 "Eight automated tests", Table 4
   "Eight rows", matrix rows 5a–5h + 5i, checklist "eight"): the suite is **8 tests (5a–5h)**;
   **5i is retained** as the Layer-5 mesh-convergence/resolution-floor row (Fig 5, Table 6),
   not a ninth test. Section F note added; checklist wording corrected.
2. **Gates.** Blueprint-locked gates are G1, G2, G3, G4; G3 is the published-validation hard
   gate. The plan's Phase-5 completeness gate **G3b was renamed G5** (plan-level) and a gate
   terminology map was added to Section B. Scientific meaning unchanged; no blueprint gate renamed.
3. **Order.** Execution order `P1→P2→P4A→P3→P4B→P5→…` now stated explicitly in Section B with
   rationale; the blueprint validation framework is untouched.
4. **Mapping.** B1–B7 ↔ blueprint matrix rows 1/2a/2b/2c/3/3b/4 table added to Section E;
   hard gates = B1–B3; Layer 5 carries no card; unextracted panel parameters stay TO BE VERIFIED.
5. **Blueprint residual finding (recorded, NOT silently edited).** Blueprint v1.2's schedule
   week-6 row still reads "GATE G2 --- all 7 internal tests pass", a v1.0 leftover contradicted
   by §5.6 / Table 4 / checklist ("eight"). Authoritative count = 8 (+5i convergence row).
   Recommended as an editorial fix in the next blueprint revision (v1.3) with user approval.
   **RESOLVED (2026-09-22):** user authorised a minimal editorial-only revision; blueprint v1.3 created -
   week-6 G2 cell now reads "all 8 automated internal tests pass". v1.2 preserved frozen; three-hunk diff;
   no scientific content touched. See `../audit/phase0_change_record.md` item 6 and `blueprint/PROVENANCE.md`.
