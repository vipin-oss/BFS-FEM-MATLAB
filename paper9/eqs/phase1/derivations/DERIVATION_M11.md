# DERIVATION M11 — Non-dimensionalisation (blueprint §3.4, eqs. (45)–(47))

Status: **checks PASSED (18/18)** · Script `scripts/m11_nondim.py` · Log `checks/m11_nondim.log`.
Scope source (read from the repository): Blueprint v1.3 line 380 (§3.4), line 577 (register), lines 765–766
(notation/units), 470 (anchor scaling preserved), 636 (axes); `CALC_MASTER_PLAN.md` row M11 (line 46:
own scheme + anchor schemes A and B `[C]`), F10 (line 127), benchmark cards B1–B3 (lines 166–190), TV1/TV2;
`PHASE1_FORMULATION_PLAN.md` line 32. Inputs: M1–M7 (L tensor (6), constitutive (26) with the 1/10
coefficient), M8 strong form (M8.7), M9 phases, M10 Case-H dispersion [S2] and path (44), M10-a ruling (a),
M15-a pair. Tags `[A]` derived here, `[L]` locked, `[C]` published anchor, `[S]` to be specified.

## M11.1 Exact M11 scope extracted `[L]`

Blueprint §3.4 (the entire M11 text):
`k̄ = kL/π`, `ω̄ = ω/ω₀`, `ω₀ = √(μ/(ρL²))`, `l̄_m = l_m/L`, `ℓ̄_i = ℓ_i/L`, `v̄ = (ω/k)/√(μ/ρ)` — equations
(45) (k̄), (46) (ω̄, ω₀), (47) (l̄, ℓ̄, v̄) per register line 577. Plan row M11 adds: the anchor schemes A and B
must be *implemented exactly as published* for comparisons (blueprint line 470, 802), not replaced by ours.
Acceptance (plan F10): "barred equations dimensionless". No numerical value enters M11.

Hidden assumptions surfaced (§M11.6): which `μ`, `ρ`, `L` in Case C; meaning of `k` in `v̄`; anchor
constants `b`, `ω₀A` (existing TV2/TV1).

## M11.2 Units of the scales `[A]` (U1–U2)

`[μ] = Pa = kg m⁻¹ s⁻²`, `[ρ] = kg m⁻³`, `[L] = m` ⇒ `μ/(ρL²)` has units s⁻² ⇒ `ω₀` in s⁻¹ ✔.
`√(μ/ρ)` has units m s⁻¹ (shear speed) ⇒ `v̄` dimensionless ✔. `k̄, l̄, ℓ̄` trivially dimensionless.

## M11.3 Dimensionless form of the locked operator `[A]` (D1–D3)

Substituting (45)–(47) into the Case-H plane-wave operator of M8.7/M10 [S1],
`H(k) = (1 + k·L·k/10) Γ_cl(k) − ρω²(1 + ℓ²|k|²) I`, and dividing by the stiffness scale `μ/L²`:

```
(M11.1)  L̄ := L/L² = Rᵀ diag(l̄₁², l̄₂²) R                       (θ unchanged)
(M11.2)  H̄(k̄) := H/(μ/L²)
              = (1 + π² k̄·L̄·k̄/10) [ π²|k̄|² I + π²(λ/μ + 1) k̄ k̄ᵀ ] − ω̄² (1 + π² ℓ̄² |k̄|²) I
```

`L, ρ, μ` are eliminated exactly; the surviving dimensionless parameter set of the homogeneous problem is
`{λ/μ (⇔ ν), l̄₁, l̄₂, θ, ℓ̄}` (5 parameters; AR = l̄₁/l̄₂ is invariant). The factors `π²` come from the
π in (45) and are **not** optional: with `k̄ = kL/π` the BZ boundary is `k̄ = 1` and the dimensionless
groups read `π² k̄·L̄·k̄` and `π² ℓ̄² |k̄|²`.

## M11.4 Barred dispersion, velocities `[A]` (D4–D7, L1–L2)

```
(M11.3)  ω̄_T² = π²|k̄|² (1 + π² k̄·L̄·k̄/10) / (1 + π² ℓ̄² |k̄|²),     ω̄_L² = (λ/μ + 2) ω̄_T²
(M11.4)  v̄ = (ω/k)/√(μ/ρ) = ω̄/(π k̄)            (k = |k|, phase velocity along k̂)
(M11.5)  ∂ω/∂k = √(μ/ρ) (1/π) ∂ω̄/∂k̄            (group velocity; δ = ∠v_g − ∠k scale-invariant)
```

Verified: (M11.3) solves `det H̄ = 0` (D5); classical limit `v̄_T = 1`, `v̄_L = √(λ/μ+2)` (D6); the M7/M16
ladder in barred form — `l̄ = ℓ̄ = 0` ⇒ `ω̄_T = πk̄`; AR = 1 ⇒ isotropic factor; `ℓ̄ = 0` ⇒ `ω̄² ~ π⁴ l̄² k̄⁴/10`
unbounded; `ℓ̄ > 0` ⇒ `ω̄²/k̄² → π² l̄_dir²/(10 ℓ̄²)` bounded (L1); 1-D normal-incidence form for the anchor
comparisons (L2).

## M11.5 Consistency with M9, M10, M10-a, M15-a, eigenproblem `[A]` (B1–B5)

- M9: `μ_α = e^{i k·a_α} = e^{iπ k̄_α}`; X ⇒ `μ_x = −1`; M ⇒ `μ_x = μ_y = −1` (B1). Phase and time
  conventions (`e^{i(k·x − ωt)}`) are untouched by scaling.
- M10: the path abscissa `s L/π ∈ {0, 1, 2, 2+√2}` is the (45) normalisation — the M10 `k̄` **is** the
  blueprint `k̄` (B2). M10-a: the symmetry group is defined by `Q L̄ Qᵀ = L̄ ⇔ Q L Qᵀ = L`; irreducible-zone
  fractions and ruling (a) unchanged (B5).
- Eigenproblem (66) (to be built in M15): `K − ω² M = μ [ K/μ − ω̄² M/(ρL²) ]` with `K̄ := K/μ`,
  `M̄ := M/(ρL²)` (2-D per unit thickness: `[K] = Pa`, `[M] = kg m⁻²`). Both scale factors are real
  positive scalars ⇒ eigenvectors unchanged, eigenvalues divided by `ω₀²`, Hermiticity and the M15-a pair
  `K̄ᴴ = K̄`, `K̄(−k) = conj K̄(k)` preserved verbatim (B3, B4). The invalid generic identity
  `K̄(k) = K̄(−k)ᴴ` is not used. **Notation clash noted:** blueprint (66) already writes `K̄, M̄` for the
  *Bloch-reduced* matrices; M11's bar means *non-dimensional*. Mapping recorded: in M15 the reduced
  non-dimensional matrices will be written `K̄(k̄)/μ`-scaled internally and the manuscript must state once
  that bars on matrices denote the reduced non-dimensional operators (TV14 below).

## M11.6 Anchor schemes (mapping only, no equation change) `[C]` (A1–A2)

- Anchor A (B3 card): `k̄_A = k a₁/π`, `ω̄_A = ω/ω₀A`, `ω₀A = 4.1e8 s⁻¹` quoted. Same *form* as (45)–(46)
  with `L → a₁`; conversion `ω̄_A = ω̄·ω₀/ω₀A`, `k̄_A = k̄·a₁/L`. Whether `ω₀A` equals `√(μ₁/(ρ₁a₁²))`
  is **not** assumed (with the card's `μ₁ = 2.3e10`, `ρ₁ = 7.5e3`, `a₁ = 1e-5` that expression is
  ≈1.75e8, not 4.1e8 — a `[C]` fact to be settled at P3.0, see TV1/TV15).
- Anchor B (B1/B2 cards): `ω₀B = 2π/(a_A/√(c₃₃/ρ) + a_B/√(c′₃₃/ρ′))` — units s⁻¹ (2π over the bilayer
  one-way travel time), *not* of the form `√(μ/(ρL²))`; `k̄_B = k b/π`, `b` = TV2. Conversion
  `ω̄_B = ω̄·ω₀/ω₀B`.
Implementation consequence: comparisons must convert from dimensional `ω, k` using each anchor's own
`(ω₀, length)`; never re-scale our `ω̄` by ratios of *assumed* constants.

## M11.7 Hidden assumptions / ambiguities — recorded, not resolved `[S]`

| id | issue | why it matters | disposition |
|---|---|---|---|
| **TV14 (new)** | Case C has two phases (matrix / inclusion). §3.4 does not say which `μ, ρ` define `ω₀` and `v̄`, nor whether `l_m, ℓ_i` are per-phase. Also `L` = lattice constant (§3.3) assumed. | Every reported `ω̄` and Table 5 value depends on it; anchor B shows a non-matrix-based choice is possible. | TV item; to be locked with TV6 (production parameters). Recommended (not decided): matrix-phase `μ, ρ`, `L` = cell edge. |
| **TV15 (new)** | `v̄ = (ω/k)/√(μ/ρ)` uses scalar `k`; for anisotropic media phase velocity is along `k̂` while group velocity is not. §3.4 does not name the branch or direction. | §7.2 deviation angle and §7.4 asymptotics use both. | TV item: state `v̄_n(k̂) = ω̄_n/(π k̄)` per branch and direction in M12 wording. |
| TV1/TV2 (existing) | anchor constants `ω₀A`, `b` | anchor conversions | unchanged, P3.0 |
| notation | bar = reduced (66)–(68) vs bar = non-dimensional (45)–(47) | M15 matrix naming | recorded in §M11.5; manuscript sentence needed (part of TV14 wording or the pending v1.4 amendment) |

None of these alters the scientific model; none is guessed here.

## M11.8 Downstream (not executed)

M12 (observables) consumes (M11.3)–(M11.5) and needs TV15 wording plus the M10-a amendment authorisation.
M15 consumes the matrix scaling of §M11.5 (real positive scalars; M15-a pair intact). M16 (Appendix A)
consumes the barred asymptotics of L1. No blocker for M11 itself; M12 remains blocked on the M10-a
amendment; M15 not started.
