# DERIVATION M15 — Bloch reduction (blueprint §4.4–4.6, eqs. (62)–(71))

Status: **checks PASSED (25/25)** · Script `scripts/m15_bloch_reduction.py` · Log `checks/m15_bloch_reduction.log`.
Inputs: M9 (40)–(43); M13 BFS + interpolation; M14 real `K,M`; M15-a ruling (a);
M10-a (T defined on half BZ; no complete-gap sampling). Blueprint v1.3 **not edited**.

## M15.1 Phase and `T(k)` `[A]` (62)–(65)

Lattice `a₁=(L,0)`, `a₂=(0,L)`. `μ_x=e^{i k_x L}`, `μ_y=e^{i k_y L}` unimodular for real `k`;
`μ(−k)=conj μ(k)`; `μ(a₁+a₂)=μ_x μ_y`.

Bloch field `u=q(x) e^{i k·x}` with **periodic** envelope `q(x+a)=q(x)`:

```
u(x+a)= μ_a u(x)
∂u(x+a)= μ_a ∂u(x)     (μ_a independent of x ⇒ commutes with ∇)
```

Same multiplier on `{u, u_x, u_y, u_xy}` and both components. **No conjugate phase on derivatives.
No value-only phase.** (M9 (41)–(43); M13 interpolation.)

One rectangular cell (all nodes corners): 8 masters (origin, 2×4 types), 24 slaves.

```
(M15.1)  d = T(k) d̄ ,   T(k) ∈ C^{32×8}
         T = blkdiag(I_8, μ_x I_8, μ_x μ_y I_8, μ_y I_8)
```

in the **TV17 provisional** node order (0,1,2,3). Independent reference: `T_{I,a}=e^{i k·x_{node(I)}} δ_{local,a}`
agrees with the edge-product table at generic interior `k=(3π/(7L), 2π/(5L))`.

`n×n` mesh of the cell ⇒ `8 n²` reduced DOFs (M13). TV7 band count `N` not chosen.

## M15.2 Reduced matrices `[A]` (66)

Unreduced `K=K^c+K^g`, `M=M_0+ℓ² M^g` real symmetric (M14).

```
(M15.2)  K̄(k)= T(k)^H K T(k) ,   M̄(k)= T(k)^H M T(k)
(M15.3)  [K̄(k) − ω² M̄(k)] d̄ = 0
```

Sizes 8×8 on the 1-cell. No phase inside the M14 integrands.

## M15.3 Identities — M15-a pair, not (68) `[A]`

Because `K` is real symmetric and `T(−k)=conj T(k)`:

```
(M15.4)  K̄^H(k) = K̄(k)                 (always)
(M15.5)  K̄(−k)  = conj K̄(k)            (always)
(M15.6)  K̄(−k)^H = K̄(k)^T
```

Hence **blueprint (68) `K̄(k)=K̄(−k)^H` ⇔ `K̄` real**, true at Γ, X, M (phases ±1) and **false** at
generic interior `k` (executable residual `||K̄−K̄(−k)^H||/||K̄|| ≈ 0.676`). Same pair for `M̄`.

Spectrum: `ω(−k)=ω(k)` (Hermitian conjugated pencil). `T(k+b₁)=T(k)` ⇒ **matrix** periodicity
`K̄(k+G)=K̄(k)`, hence spectral `ω(k+G)=ω(k)`.

## M15.4 Phase-sensitive tests `[A]`

Generic `k` interpolant (finite-difference traces, independent of the tying table): `u,u_x,u_y,u_xy`
on `x=L` equal `μ_x` times traces on `x=0` (mixed-derivative FD tolerance `2×10^{-4}`).

Negative controls at the same `k`:

| wrong T | `u_x` Bloch residual | `K̄` Hermitian? |
|---|---|---|
| value-only phase | O(1) | yes (blind) |
| conjugate phase on `{u_x,u_{xy}}` | O(1) | yes |

At Γ both wrong `T` coincide with the correct `T` (tests blind at Γ/X/M).

## M15.5 Jacobi / MAC (69)–(71)

Jacobi `D_{ii}=1/√|K̄_{ii}|` defined; `cond(D K̄ D)` finite on the test pencil. **Not** a production
`κ(θ,AR)`. MAC continuation is a solver protocol, not executed on bands.

## M15.6 TV / not done

TV17, TV18, TV4, TV6, TV7, TV14, TV15 **OPEN**. No complete-gap sampling (M10-a). No Case H/C.
Blueprint (68) text **not** replaced (M15-a amendment unauthorised). M16/M17 not started.
