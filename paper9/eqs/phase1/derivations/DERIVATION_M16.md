# DERIVATION M16 — Appendix A high-`k̄` asymptotics (blueprint (A.1)–(A.6))

Status: **checks PASSED (17/17)** · Script `scripts/m16_asymptotics.py` · Log `checks/m16_asymptotics.log`.
Locked input: M11.3 Case-H barred dispersion. Homogeneous only. Blueprint v1.3 not edited.
Register mapping (blueprint lines 589, 532): (A.1)–(A.3) leading-order / unbounded `ℓ̄=0`;
(A.4)–(A.6) bounded `ℓ̄>0`, dimensional check, admissibility.

## M16.1 Locked dispersion `[L]`

```
ω̄_T² = π² κ² (1 + π² κ² l_eff² / 10) / (1 + π² ℓ̄² κ²) ,   κ = |k̄|
ω̄_L² = (λ/μ + 2) ω̄_T²
v̄ = ω̄ / (π κ)
l_eff²(φ) = l̄₁² cos²(φ−θ) + l̄₂² sin²(φ−θ) = k̂·L̄·k̂
```

`L̄` is the barred length tensor, **not** `ℓ̄² I`.

## M16.2 `ℓ̄>0` — (A.1), (A.2), (A.4)

Divide num/den by `κ²` and take `κ→∞`:

```
(A.1)  ω̄_T² = C_T(φ) κ² [ 1 + (10/(π² l_eff²) − 1/(π² ℓ̄²))/κ² + O(κ^{-4}) ]
       C_T(φ) = π² l_eff²(φ) / (10 ℓ̄²)
       ω̄_T ∼ [π l_eff / (√10 ℓ̄)] κ
(A.2)  ω̄_L² = (λ/μ+2) ω̄_T²  for all κ;  ω̄_L/ω̄_T = √(λ/μ+2)
               independent of κ, ℓ̄, θ, φ
(A.4)  v̄_T,∞(φ) = l_eff(φ) / (√10 ℓ̄)   finite
       v̄_L,∞(φ) = √(λ/μ+2) v̄_T,∞(φ)
```

Micro-inertia enters **only** through the denominator `1+π² ℓ̄² κ²`, which supplies the `κ²` that
cancels the gradient-stiffness `κ⁴` and leaves a finite speed.

## M16.3 `ℓ̄=0` — (A.3)

```
(A.3)  ω̄_T² ∼ (π⁴ l_eff² / 10) κ⁴ ,   ω̄_T ∼ (π² l_eff/√10) κ²
       v̄_T ∼ (π l_eff / √10) κ  → ∞   (linear in k̄)
```

The scaling is derived, not asserted.

## M16.4 Dimensional form and admissibility — (A.5), (A.6)

```
(A.5)  v_{T,∞} = √(μ/ρ) · l_eff / (√10 ℓ) ,   l_eff² = k̂·L·k̂   [m/s]
(A.6)  ℓ̄>0 and l_eff>0 ⇒ bounded high-k phase velocity (admissible in the sense of App. A);
       ℓ̄=0 and l_eff>0 ⇒ v̄ ∼ k̄ unbounded (inadmissible high-k wave speed).
```

No claim about dissipation, experiments, or band gaps.

## M16.5 Directional special cases

| case | `l_eff²` | `v̄_T,∞` |
|---|---|---|
| isotropic `l̄₁=l̄₂` | `l̄₁²` (no φ,θ) | `l̄₁/(√10 ℓ̄)` |
| `φ=θ` | `l̄₁²` | `l̄₁/(√10 ℓ̄)` |
| `φ=θ+π/2` | `l̄₂²` | `l̄₂/(√10 ℓ̄)` |
| `l̄₁≠l̄₂` | anisotropic | `C_T(0)≠C_T(π/2)` |
| `l̄₁=l̄₂=0`, `ℓ̄>0` | 0 | `ω̄_T→1/ℓ̄`, `v̄→0` (not `L̄=ℓ̄²I`) |

## M16.6 TV

TV4, TV6, TV7, TV14, TV15, TV17, TV18 remain OPEN. Finite-`κ` spots are sanity only.
