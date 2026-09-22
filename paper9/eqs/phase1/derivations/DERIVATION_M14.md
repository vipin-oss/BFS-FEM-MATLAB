# DERIVATION M14 — Element matrices and quadrature (blueprint §4.2–4.3, eqs. (57)–(61))

Status: **checks PASSED (24/24)** · Script `scripts/m14_element_matrices.py` · Log `checks/m14_element_matrices.log`.
Inputs: Blueprint v1.3 lines 400–401, register 584–585; M8.2 weak form; M4 (26); M6 `K_g` identity;
M13 BFS `N,B,B_,i` and integrand degrees; M5 micro-inertia. Pre-Bloch homogeneous rectangle only.
Tags `[A]` derived, `[L]` locked, `[S]` TV.

**Not done:** Bloch `T(k)` / reduced matrices (M15); Case C; circular inclusion; blueprint edit.

## M14.1 Weak form → matrices `[A]`

M8.2 on one rectangle `A`, time-harmonic, homogeneous `C,L,ρ,ℓ`:

```
W_h(v,u) = ∫_A [ σ(v):ε(u) + τ(v):η(u) − ρ ω² (u·v + ℓ² u_,j·v_,j) ] dA
```

With `q = B d`, `q_,i = B_,i d`, `u = N d`, `G = D_c C̄`, `D_c = diag(1,1,2)`,
`τ_ijk = (1/10) L_kn C_ijpq η_pqn` (26), and M6 `2W_g = (1/10) L_mn q_m^T G q_n`:

```
(M14.1)  K^c  = ∫_A B^T G B dA                         (57)
(M14.2)  K^g  = (1/10) Σ_{m,n} L_mn ∫_A B_,m^T G B_,n dA   (58)–(59); L = R^T diag(l1²,l2²) R
(M14.3)  M0   = ρ ∫_A N^T N dA                           (60)
(M14.4)  M^g  = ρ ∫_A (N_,x^T N_,x + N_,y^T N_,y) dA     (60)
(M14.5)  M    = M0 + ℓ_i² M^g                            (61)
```

All four (plus `K^c+K^g`) are **real symmetric** 32×32. No `k`, no Bloch phase (M15).
`θ,AR` enter **only** through `L` in `K^g`. Affine Jacobian of the rectangle is the constant `h_x h_y`.

Indexing used in the executable 32-vector is the **M13 provisional** map
`index = 8(node−1)+4(comp−1)+type` (**TV17**, not blueprint-locked). The bilinear forms (M14.1)–(M14.5)
are independent of that ordering.

## M14.2 Units `[A]`

Value–value blocks: `[K^c]=[K^g]=Pa` (2-D energy / displacement²). `[M0]=ρ·area = kg m⁻¹` as a 2-D
membrane; M11’s `kg m⁻²` is the same per unit thickness if thickness is carried as 1 m.
`[M^g]=kg m⁻³` so `ℓ² M^g` matches `[M0]`.

## M14.3 Quadrature `[A]` — not the blueprint “quartic” rule

1-D Gauss–Legendre with `n` nodes is exact on `P_{2n−1}`. M13/M14 degrees per coordinate:

| integrand | max degree / coord | minimal `n` (`2n−1 ≥ deg`) |
|---|---|---|
| `N^T N` (`M0`) | 6 | 4 |
| `B^T G B` (`K^c`) | 6 (undifferentiated dir.) | 4 |
| `B_,i^T G B_,j` (`K^g`) | 6 | 4 |
| `N_,j^T N_,j` (`M^g`) | 6 | 4 |

Blueprint §4.2 “second derivatives of cubics ⇒ up to quartic” is the degree of **one** second
derivative, not of the **product** integrand. Overruled by M13 (degree 6 per direction).

**Rule adopted:** 4×4 Gauss–Legendre product on the affine rectangle (exact through degree 7 per
axis). The same rule is used for all four integrands. 2×2 (exact ≤ 3) and 3×3 (exact ≤ 5) are
insufficient; executable monomial tests: 3×3 fails on `x^6`; 4×4 exact for `x^p y^q`, `p,q≤7`;
2×2 fails on `x^4`; 3×3 vs 4×4 `M0` entries differ.

## M14.4 Structure checks `[A]` (numeric 4×4 Gauss, unit square)

On `h_x=h_y=1`, `λ=μ=ρ=1`, `L=I`: `K^c` SPSD with numerical kernel dimension 3 (2-D rigid);
`K^g` SPSD (linear fields, `η=0`); `M0` SPD; `M^g` SPSD (constants). Shear: `G_33=4μ` matches
`σ:ε` with tensor `ε12` (M13). `K^g` isotropic under `L11↔L22` at AR=1 and changes when `AR≠1`.

## M14.5 TV / scope

| id | status |
|---|---|
| **TV17** | OPEN. Provisional ordering used for indexing only. |
| **TV18** | OPEN. Homogeneous rectangle only; no circular inclusion, no area-fraction model. |
| TV4, TV6, TV7, TV14, TV15 | OPEN, unused as numbers. |
| F2 | `G=D_c C̄` as locked in M4/M13; not re-opened. |
| M15-a | not used (no `K̄(k)`). |

## M14.6 Downstream

M15 consumes real `K^c,K^g,M0,M^g` and applies complex `T(k)` afterwards. Do not insert phases into
the element integrands.
