# PHASE-1 AUDIT — F1: five-constant isotropic presentation vs the `(AᵀA)_rot` tensor modulus

Status: **RESOLVED — interpretation (A): the five-constant presentation is the isotropic
specialisation; the implemented anisotropic model is Eq. (26).** No blueprint amendment, no
model change, no numerical values. Phase 1 overall remains **IN PROGRESS**.

Scope of this audit: F1 only (blueprint (16)–(18), (22)–(24) vs (26)). Documents/reads used:
Blueprint v1.3 (`paper9/plan/blueprint/Paper9_Blueprint_v1.3.tex`, sha256 `ca71b91a…dbf9f`),
`paper9/plan/CALC_MASTER_PLAN.md` v1.1 §A, `derivations/DERIVATION_M01_M07.md` (M4, M6),
legacy [C] sources `femcheck/FEM_Total/ptxt/FEM_1_Paper.txt`, `FEM_2_Paper.txt`,
`FEM_3_Paper.txt` (read-only; not modified).

Evidence program: `scripts/audit_f1_five_constant.py` → log `checks/audit_f1_five_constant.log`
(**34 checks PASSED**; exact SymPy arithmetic; all quantities symbolic — no material, geometric
or numerical parameter values are assigned anywhere).

---

## 1. Audit question

Blueprint v1.3 contains two presentations of the gradient constitutive law:

* the **isotropic five-constant scalar** presentation `a₁…a₅` (E3 (16)–(18); PD statements (22)–(24)), and
* the **anisotropic tensor** modulus implemented through `(AᵀA)_rot` in Eq. (26)
  (`K_g = (1/10) ΣᵢΣⱼ (AᵀA)_rot,ij Bᵀ,i C B,j`).

M4 of this phase proved symbolically that the isotropic-length limit of (26) is uniquely
`(a₁,a₂,a₃,a₄,a₅) = (0, 0, λℓ²/20, μℓ²/10, 0)` and that for `l₁ ≠ l₂` the model leaves the
five-constant scalar family. The question was whether the blueprint intends

**A.** the five-constant formulation **only** as the isotropic-length specialisation (the
anisotropic model being (26)), or
**B.** the five constants as **the** model of the anisotropic medium.

## 2. Blueprint v1.3 evidence (primary authority; wording verbatim, line numbers of the tex)

| Line | Verbatim wording | What it establishes |
|---|---|---|
| 300 (Nomenclature) | `Elastic / gradient moduli & C_ijkl, A_ijklmn, a_1…a_5 & 2 + 5 isotropic gradient constants` | the five constants are **named** "isotropic gradient constants" |
| 353 (§2.4) | `…double stress τ_ijk = A_ijklmn η_lmn; isotropic sixth-order gradient modulus written with the five constants a_1…a_5; plane-strain reduction` | the `a_p` presentation is qualified **isotropic**; the tensor `A` is written separately and generically |
| 355 (§2.6) | `Full W; sufficient conditions on (a_1…a_5) and on (AᵀA)_rot; the anisotropic gradient stiffness in the form K_g = (1/10) Σ_i Σ_j (AᵀA)_rot,ij Bᵀ,i C B_,j` | the two objects are listed side by side with distinct roles; **the anisotropic stiffness is (26)** |
| 356 (§2.7) | `(ii) AR = 1 = isotropic gradient elasticity` | isotropy is a **specialisation** in the limit ladder, not the general case |
| 562 (Equation register) | `(16)–(18) Isotropic sixth-order gradient modulus (a_1…a_5); plane-strain reduction` | register entry explicitly labelled isotropic |
| 561 (Equation register) | `(13)–(15) σ_ij = C_ijkl ε_kl; τ_ijk = A_ijklmn η_lmn; Voigt form` | the tensorial statement of the double stress carries **no** `a_p` claim |
| 264 (abstract plan) | `Verified in the isotropic, normal-incidence, isothermal limit against published 2023/2024 dipolar-gradient band structures` | the validation regime is explicitly the isotropic limit |

No statement anywhere in v1.3 assigns the five constants as functions of `l₁,l₂,l₃`, and no
statement claims (16)–(18) covers `l₁ ≠ l₂`. Conversely, the anisotropic model is stated only
operationally through (26) (and, in the continuum, through the `(AᵀA)_rot` operator of (3)–(9)).
The locked plan states the same in its own words (`CALC_MASTER_PLAN.md` §A, row M4):
*"isotropic modulus shape with anisotropic length tensor entering `K_g`"* and
*"`a1…a5` [A from M1/M2 in isotropic limit]"*.

**Conclusion (A): established by the blueprint's own wording**, not by inference from general
Mindlin theory. `[a_p] = Pa·m²` are the isotropic-family constants; the directional content of
the model lives in `(AᵀA)_rot` and reaches the discrete problem exclusively through (26).

## 3. Independent verification of the M4 mapping (different method than M4)

The M4 result was obtained by monomial-coefficient matching. This audit re-derived it from the
full second-derivative (Hessian) system on the 18 independent strain-gradient components:

* `[E2]` the five invariants `T₁…T₅` are linearly independent on the 18-component space
  (rank 5); the exact solution of the 171 independent Hessian equations is **unique**:
  `(a₁…a₅) = (0, 0, λℓ²/20, μℓ²/10, 0)`; substituting it satisfies all 171 equations exactly.
* `[E3]` **direct component comparison**: all `3⁶ = 729` index sextuples of `D_ABCPQR`
  (mapping onto the 171 independent entries) agree between `W26(L = ℓ²I)` and the five-constant
  form with those coefficients.
* `[E5x]`, `[E5y]` cross-consistency: the certificate entries coincide at the isotropic solution.

## 4. Can the anisotropic `l₁ ≠ l₂` tensor be represented by five scalars? — No

Structural certificates, all verified symbolically on the **general** family (i.e. for arbitrary
`a₁…a₅`, no values assumed), and on the **(26)-modulus** with a general symmetric `L`:

| # | Five-constant family (identically in `a_p`) | Eq. (26) modulus |
|---|---|---|
| `[E4a]` | `∂²W/∂η₁₁₁∂η₂₂₁ = ∂²W/∂η₂₂₂∂η₁₁₂ = a₂ + 2a₃` (**equal**) | `[E5a],[E5b]`: `L₁₁λ/10` vs `L₂₂λ/10` ⇒ forces `L₁₁ = L₂₂` |
| `[E4b]` | `∂²W/∂η₁₁₁∂η₂₂₂ = 0` (**vanishes**) | `[E5c]`: `L₁₂λ/10` ⇒ forces `L₁₂ = 0` |
| `[E4c]` | `∂²W/∂η₁₂₁² = ∂²W/∂η₁₂₂² = 2a₁ + 4a₄ + 2a₅` (**equal**) | `[E5d],[E5e]`: `2L₁₁μ/5` vs `2L₂₂μ/5` ⇒ `L₁₁ = L₂₂` (λ-independent) |
| `[E4d]` | `∂²W/∂η₁₂₁∂η₁₂₂ = 0` (**vanishes**) | `[E5f]`: `2L₁₂μ/5` ⇒ `L₁₂ = 0` (λ-independent) |
| `[E4e]` | all five invariants are invariant under rotation (checked with a rational rotation) | the family is isotropic as a set |

Because the family is rotation-invariant (`[E4e]`) while the identities are component
identities in whatever frame they are evaluated, representability implies `L₁₁ = L₂₂` and
`L₁₂ = 0` **in every frame**, hence `L ∝ I`. Combined with `[E2]`:

> `W26(L)` belongs to the five-constant isotropic family **iff** `L = ℓ²I`; the coefficients are
> then uniquely `(0, 0, λℓ²/20, μℓ²/10, 0)`. The image of the family `{W26(L)}` meets the
> isotropic family in exactly that single ray.

**Plane-strain (implemented) configuration** `[E6*]` — obtained by restricting *both* objects
component-wise (all components carrying index 3 set to zero; nothing re-invented):

* the same certificates hold: representable **iff** `L̄ = diag(L₁₁,L₂₂)` has `L₁₁ = L₂₂`,
  `L₁₂ = 0`, i.e. `L̄ ∝ I`;
* **new finding (identifiability):** the restricted five-constant family has **rank 4 of 5** —
  the combination
  `a₁ − 2a₂ + a₃ − a₄ + a₅`
  is **not identifiable from in-plane (plane-strain) data** alone. Verified by the null-space
  computation and by the exact identity `a₁T₁ − 2a₂T₂ + a₃T₃ − a₄T₄ + a₅T₅ = 0` on
  plane-strain fields, and demonstrated as non-uniqueness: `W5(a_sol + t·a₀) = W26(L = ℓ²I)`
  for every `t`. Consequence for later phases: any *plane-strain* comparison that quotes
  `a₁…a₅` determines only 4 combinations; the 3D identification (rank 5) is unique.

## 5. FEM_3 Eqs (84)–(85) — exact relationship (transcribed verbatim from the source)

Source: `femcheck/FEM_Total/ptxt/FEM_3_Paper.txt`, §7 "Verification against the strain-gradient
elasticity benchmark" (benchmark = **Shekarchizadeh et al.** simple-shear plate, ref. [1] of that
manuscript; the five-constant isotropic restriction is attributed there to **Mindlin [8]** and
**Mindlin & Eshel [10]**):

```
a1 = 2 c5 ,  a2 = 2 c3 ,  a3 = c4/2 ,  a4 = c6 ,  a5 = 2 c7            (84)
c3 = c4 = ℓ² λ / 12 ,  c5 = c7 = ℓ² (7 μ + 3 λ) / 120 ,
c6 = ℓ² (7 μ − 4 λ) / 120                                              (85)
```

Evaluated in the `a_p` basis `[E7]`:

```
(a1, a2, a3, a4, a5)_FEM3 = ( ℓ²(7μ+3λ)/60 , ℓ²λ/6 , ℓ²λ/24 , ℓ²(7μ−4λ)/120 , ℓ²(7μ+3λ)/60 )
```

Relationship established directly from the source material:

* **Same basis, different member.** Both are members of the same five-dimensional *isotropic*
  family (the `a_p` basis). Nothing else is shared: FEM_3 (84)–(85) is a **conversion of a
  specific benchmark's single-length constants** (`c3…c7` of the Shekarchizadeh et al. plate)
  into that basis.
* **Never equal to the isotropic limit of (26).** Equality would require `a₁ = 0`, i.e.
  `7μ + 3λ = 0` ⇒ `λ = −7μ/3`, which then gives `a₂ = −7μℓ²/18 ≠ 0` while (26) forces `a₂ = 0`.
  Hence for `ℓ > 0`, `μ > 0` the two parameterizations **never coincide** `[E7b]`.
* **Not reachable from the `L`-map at all** `[E7c]`: since `image{L ↦ W26(L)} ∩ isotropic family`
  = the single ray `(0,0,λℓ²/20,μℓ²/10,0)` (§4), the FEM_3 (84)–(85) member is outside the image
  for every `ℓ` and every admissible `λ, μ`.
* **No external source was modified**, and no derivation is attributed to FEM_3 that it does not
  state: (85) is a *definition* of `c3…c7` in that manuscript.

**Consequence for Paper 9:** Paper 9 implements **(26) as written**. Any future comparison with a
single-length five-constant benchmark (e.g. Anchor A's dipolar-gradient panel, blueprint rows
439–440 and 678) must first state which member that benchmark actually is; the FEM_3 (84)–(85)
member is *not* the isotropic limit of Paper 9's modulus, so a coefficient-level comparison
between the two would be a model mismatch, not a numerical error. This is a Phase 3
(benchmark-interpretation) obligation, recorded here; nothing in Phase 1 depends on it.

## 6. Consistency of the PD statements (blueprint (22)–(24))

* Blueprint (22)–(24) requests *sufficient conditions on `(a₁…a₅)` and on `(AᵀA)_rot`* — it does
  not claim these conditions are the criterion for the implemented model, and this audit finds
  no conflict: for the isotropic family the sufficient set `a₁ ≥ 0, a₃ ≥ 0, 4a₁a₃ ≥ a₂²,
  a₄ ≥ |a₅|` holds (M6, identities `T₁T₃−T₂² ≥ 0`, `T₄±T₅ ≥ 0`), while the implemented model's
  exact criterion is `L` positive definite **and** `C` positive definite (Kronecker argument,
  M6). The two statements describe different objects and must not be merged in the manuscript.
* `λ < 0` admissible materials: `a₃ = λℓ²/20 < 0` in the isotropic member while `W_g` remains
  positive definite via `L ⊗ C`. The sufficient set is therefore **strictly sufficient**
  (recorded in M6 as a remark; no contradiction with the blueprint).

## 7. Notation hazard (recorded, not a model issue)

Blueprint lines 439–440 and 678 write the Layer-2b target parameter as `a_1 = 10^{-5}` m — this is
the **anchor's lattice constant** (a length), whereas §2.4's `a_1` is a **gradient modulus**
(Pa·m²). The symbol collides. Phase 3 and the manuscript must disambiguate it (e.g. anchor lattice
constant `a` vs gradient constants `a₁…a₅`). No blueprint edit is made here (not authorized).

## 8. Downstream impact

| Downstream item | Effect of this resolution |
|---|---|
| M8–M17 (Phase 1) | **none** — they use `C`, `L = (AᵀA)_rot`, the strong form and (26); the `a_p` are not used operationally |
| §2.4/§2.6 manuscript text | must present `a₁…a₅` as the isotropic-family constants with PD sufficient conditions, and (26) as the implemented anisotropic modulus; the isotropic-limit coefficients `(0,0,λℓ²/20,μℓ²/10,0)` are the bridge statement |
| Layer 2b / Layer 1 (Phase 3, blueprint rows 678/440) | benchmark mapping must be derived from the **anchor's own constitutive relations**; a coefficient-level match to a five-constant member is impossible in general (FEM_3 member ≠ our isotropic member) |
| Any plane-strain `a_p` identification | only 4 of 5 combinations are identifiable (`a₁ − 2a₂ + a₃ − a₄ + a₅` is free) — must be stated if such a comparison is ever quoted |
| Tests 5a–5i (Phase 4A) | unaffected (they test Hermiticity, periodicity, symmetry, PD of `K̄, M̄`, bounded velocity, energy flux — none involves `a_p`) |

## 9. What was NOT done

No blueprint change; no constitutive-model change; no numerical parameter assigned; no TV item
resolved; no external source or benchmark file modified; no Phase-1 module other than the
documentation of F1 touched.

## 10. Traceability of this audit

| Evidence | Artifact |
|---|---|
| script | `paper9/eqs/phase1/scripts/audit_f1_five_constant.py` (sha256 `41e3a32fa31aa6a83653caf13d633d7b0a8d934c7ed90ffcd8f7ad7890bc19ee`) |
| log (34 checks PASSED) | `paper9/eqs/phase1/checks/audit_f1_five_constant.log` |
| blueprint wording | `Paper9_Blueprint_v1.3.tex` lines 300, 353, 355, 356, 561, 562, 264 (quoted in §2) |
| M4/M6 records | `derivations/DERIVATION_M01_M07.md` §§M4, M6 (notes F1, F2) |
| legacy [C] source | `FEM_3_Paper.txt` §7, Eqs (84)–(85) (transcribed verbatim in §5) |
