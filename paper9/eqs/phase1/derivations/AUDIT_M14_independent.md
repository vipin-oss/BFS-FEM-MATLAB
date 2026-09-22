# AUDIT M14 (independent cross-audit) — Element matrices K^c, K^g(θ,AR), M₀, M^g and the integration rule (blueprint §4.2–4.3, eqs. (57)–(61))

Status: **checks PASSED (24/24)** · Script `scripts/audit_m14_independent.py` · Log `checks/audit_m14_independent.log`.

> **Provenance.** Derived in a separate session concurrently with the primary M14 record (`DERIVATION_M14.md`,
> commit `4c09aad`), without access to it; filed as an independent cross-check, primary record unchanged.
> Concurrence: same (57)–(61) objects, same 4×4 Gauss–Legendre conclusion from degree-6 product integrands,
> same TV17/TV18 status. Additional here: exact Hessian verification against the M6/M5 energies, exact
> kernels/ranks, the θ+90° ↔ l₁↔l₂ element identity, exact mesh-scaling law, per-class degree table incl. the
> (5,5) mixed block (3×3-exact), and the executable demonstration that Gauss-point material sampling in a cut
> element is not exact (TV18).
Harness notes: exact-rational element size (3/2 × 5/7) and Pythagorean angle (cos, sin) = (3/5, 4/5) are used where full
symbolic simplification of 32×32 trig matrices is intractable; K^g is handled through its exact decomposition
`(L₁₁A_xx + L₂₂A_yy + L₁₂(A_xy+A_xyᵀ))/10`; numerical ranks use 30-digit SVD with the exact kernels verified separately (S5).
Scope source (repository text): Blueprint v1.3 lines 400–401 (§4.2–4.3), register 584–585; plan row M14
(line 49: inputs M4, M6, M13, M5; "integrand ≤ quartic → rule stated & justified"; output element matrices;
consumer M15). Inputs: M4 (18)/(26) `C̄`, `τ_ijk = (1/10)L_kn C_ijpq η_pqn`; M2 (6) `L(θ)`; M5 kinetic
energy; M6 energy `W = ½σε + ½τη`, `D_c = diag(1,1,2)`, assembly identity; M8 weak form (M8.2); M13
`N, B, B,i`, 32-DOF layout, degrees; M11 scales; M12 energy identity; M15-a (not used here — pre-Bloch).

## M14.1 Exact scope `[L]`

§4.2: `K^c`, `K^g(θ,AR)`, "Gauss–Legendre order required (the integrand contains second derivatives of
cubics ⇒ up to quartic; state the rule used and justify it)" (57)–(59). §4.3: `M₀`, `M^g`,
`M = M₀ + ℓ_i² M^g` (60)–(61). No Bloch reduction (62)–(65 = §4.4, M15). No material values.

## M14.2 Derivation from the locked weak form `[A]` (D1–D4)

Time-harmonic weak form (M8.2), per element, `u = N d`, `v = N δd`, `d` real:

```
(57)  K^c  = ∫_e Bᵀ G B dA,                 G := D_c C̄ = diag(1,1,2)·C̄   (3×3, symmetric PD)
(58)  K^g  = (1/10) Σ_{i,j} L_ij(θ) ∫_e B,iᵀ G B,j dA
           = (1/10)[ L₁₁ A_xx + L₂₂ A_yy + L₁₂ (A_xy + A_xyᵀ) ],  A_ij := ∫ B,iᵀ G B,j dA
(60)  M₀   = ∫_e ρ Nᵀ N dA
(61)  M^g  = ∫_e ρ (N,xᵀ N,x + N,yᵀ N,y) dA,     M = M₀ + ℓ² M^g
element pencil:  (K^c + K^g) − ω² M
```

Each was verified as the exact Hessian of the corresponding locked energy: `½dᵀK^c d = ∫½C_ijkl ε_ij ε_kl`,
`½dᵀK^g d = ∫½τ_ijk η_ijk` with the full index form of (26), `½dᵀM d = ∫½ρ(u·u + ℓ² u_i,j u_i,j)` — for a
generic rational DOF vector on a rational rectangle (D1–D3). The pair factor `D_c` is what makes the
tensor-shear `B` (M13) energy-consistent (`qᵀGq = σ_ij ε_ij`). Sign: micro-inertia **adds** to the mass
(`+ℓ²M^g`), matching `ρω²(u − ℓ²u,jj)` in the strong form and `T_g ≥ 0` in M5/M12 (D4).

## M14.3 Structure `[A]` (S1–S6)

32×32; all four matrices **real and symmetric** (exact); no complex quantity at element level — Bloch phases
enter only through the M15 transformation (S1–S2). `G` symmetric PD with eigenvalues `2(λ+μ), 2μ, 4μ`; `L`
symmetric PD; the 6×6 gradient modulus `(1/10) L ⊗ G` symmetric PD (S3). `M₀` SPD; `M^g` PSD with kernel =
the 2 constant displacement fields (rank 30) (S4). `K^c`: rigid modes (2 translations + rotation) in the
kernel exactly, rank 29 — PSD with exactly the physical kernel, no spurious mode; `K^g`: kernel = affine
fields (3 rigid + 3 constant strains), rank 26; constant strain gives `dᵀK^c d = h_x h_y qᵀGq` (S5–S6).

## M14.4 Limits `[A]` (L1–L4)

`l₁ = l₂ = 0 ⇒ K^g = 0`; `ℓ = 0 ⇒ M = M₀` (classical BFS plane-strain element). `l₁ = l₂ = l ⇒
K^g = (l²/10)(A_xx + A_yy)`, θ-independent. θ enters only via `L(θ)`: `K^g(θ+90°; l₁,l₂) = K^g(θ; l₂,l₁)`
(M7 (30) at element level), period 180°. At θ = 0 the mixed block vanishes; at generic θ the cross term
`(l₁²−l₂²) sinθ cosθ (A_xy + A_xyᵀ)/10` is present and non-zero.

## M14.5 Units and scaling `[A]` (U1–U3)

`[K^c] = [K^g] = Pa` (per unit thickness, value-DOF entries), `[M₀] = [ℓ²M^g] = kg/m` (per unit
thickness), `ω²M ~ K`. Exact mesh-scaling law under `h → c h` with physical-derivative DOFs
(`S = diag(1,c,c,c²)` per node/component): `K^c → S K^c S`, `K^g → c⁻² S K^g S`, `M₀ → c² S M₀ S`,
`M^g → S M^g S` ⇒ `K^g/K^c ~ (l/h)²`, `ℓ²M^g/M₀ ~ (ℓ/h)²`: gradient effects are resolved only when `h` is
comparable to `l, ℓ` — a statement for the §5.7 convergence design, not a value choice. M11 pencil
`K/μ − ω̄² M/(ρL²)` with the parameter set `{λ/μ, l̄₁, l̄₂, θ, ℓ̄, h/L}` (U3).

## M14.6 Quadrature — derived from the actual integrands `[A]` (Q1–Q6)

| integrand class | degree (x, y) | exact tensor Gauss–Legendre (n per direction, 2n−1 ≥ deg) |
|---|---|---|
| `NᵀN` (M₀) | (6, 6) | **n = 4** |
| `N,xᵀN,x + N,yᵀN,y` (M^g) | (6, 6) | **n = 4** |
| `BᵀGB` (K^c) | (6, 6) | **n = 4** |
| `B,xᵀGB,x` (K^g, L₁₁) | (4, 6) | n = 4 (n = 3 fails in y) |
| `B,yᵀGB,y` (K^g, L₂₂) | (6, 4) | n = 4 |
| `B,xᵀGB,y + B,yᵀGB,x` (K^g, L₁₂) | (5, 5) | n = 3 |

Hence **4×4 Gauss–Legendre is the minimal tensor rule that integrates every element matrix exactly on a
homogeneous rectangle** (Q1–Q2). Verified executably with exact Legendre roots on representative entries:
4×4 reproduces the exact symbolic integrals of all six classes; 3×3 is *not* exact for `NᵀN` and `BᵀGB`
but is exact for the mixed `K^g` class (Q3–Q4). The blueprint sentence "second derivatives of cubics ⇒ up to
quartic" describes a factor, not the product; a "quartic-motivated" 3×3 or 2×2 rule would under-integrate
`M₀`, `M^g`, `K^c` and the diagonal `K^g` blocks. Affine map `x = h_x(1+ξ)/2`, `J = h_x h_y/4` (Q5).

**Exact vs practical integration (Case C, TV18).** The tensor Gauss rule is exact only for polynomial
integrands, i.e. within a homogeneous element. An element cut by the circular inclusion carries a
discontinuous material field: sampling ρ, λ, μ, l, ℓ at Gauss points integrates a piecewise-constant
indicator with O(h) area error per cut element (demonstrated: the 4×4 Gauss "area" of a quarter disc in the
unit square deviates from π/4 by > 10⁻³) — **not exact** (Q6). The blueprint (§6.1, Table 2) specifies the
inclusion radius/contrast as parameters but *no interface-integration rule*. Options the production phase
will have to choose from (not chosen here): (i) mesh-conforming staircase (material per element, error O(h)
in geometry, integration exact per element); (ii) Gauss-point material assignment (sub-cell resolution,
still O(h)); (iii) sub-cell/adaptive quadrature in cut elements. Any of these must be reported in §5.7 as a
convergence variable → remains **TV18** (updated with this classification).

## M14.7 Provisional DOF ordering (TV17) `[S]`

The audit uses `index = 8(node−1) + 4(comp−1) + type`, type ∈ {u, u,x, u,y, u,xy}, nodes CCW from the
origin — reversible (`node = idx // 8`, `comp = (idx % 8) // 4`, `type = idx % 4`), verified dimensionally;
it is **not** a manuscript convention. TV17 stays open.

## M14.8 Energy / micro-inertia consistency (M5, M8, M12) `[A]`

`M^g` is exactly the Gram matrix of `∇N`, i.e. the discretisation of `ρℓ² u̇_i,j v_i,j` in (M8.1); the
kinetic energy `½ω²dᵀMd` equals the M5 density integrated; the M12 micro-inertia flux term
`−ρℓ² ü_i,j u̇_i` is the boundary term of exactly this integration by parts — the element formulation is the
volume counterpart and does not remove it (it becomes the natural datum on element/cell boundaries, M8-a
(O4)). Signs consistent throughout (D3–D4).

## M14.9 Not done / not changed

No Bloch reduction (62)–(71); no material values; Blueprint v1.3 unchanged; TV4, TV6, TV14, TV15, TV16
untouched; M12 remains PARTIAL; M15-a ruling untouched (pre-Bloch matrices are real symmetric, which is the
input M15-a assumes).
