# P2.1 — Case-H homogeneous dispersion (from P1, not from PB2009)

**Provenance:** M10.2 `[A]` (DERIVATION_M10.md), M11.3 `[A]`, M16.1 `[L]` locked.
**Not** a transcription of PB2009.

## Locked dimensional form (M10.2)

\[
\omega_L^2 = \frac{\lambda+2\mu}{\rho}\, |k|^2 \frac{1 + k\cdot L\cdot k/10}{1 + \ell^2 |k|^2},\qquad
\omega_T^2 = \frac{\mu}{\rho}\, |k|^2 \frac{1 + k\cdot L\cdot k/10}{1 + \ell^2 |k|^2}.
\]

`L` is the in-plane length tensor (`l1², l2²` after rotation by `θ`). Factor `1/10` is from Form-II isotropic modulus reduction (M4/M6), **[A]**.

## Isotropic specialisation (P2 table)

Let `l1 = l2 = l`, so `k·L·k = l² |k|²` independent of `θ` and of `k̂`.

| Quantity | Anisotropic Case-H `[A]` | Isotropic specialisation `[A]` |
|---|---|---|
| `k·L·k` | `\|k\|² (l1² cos²(φ−θ) + l2² sin²(φ−θ))` | `l² \|k\|²` |
| `ω_T²` | `(μ/ρ) k² (1 + k·L·k/10)/(1+ℓ²k²)` | `(μ/ρ) k² (1 + l² k²/10)/(1+ℓ²k²)` |
| `ω_L²` | same with `(λ+2μ)/ρ` | same with `(λ+2μ)/ρ` |
| long-wave `k→0` (P2.2) | `c_T=√(μ/ρ)`, `c_L=√((λ+2μ)/ρ)` | identical |
| high-k, `ℓ>0` (P2.3 / M16) | `v_{T,∞} = √(μ/ρ)·l_eff/(√10 ℓ)` | `v_{T,∞} = √(μ/ρ)·l/(√10 ℓ)` |
| high-k, `ℓ=0` | `v_T ∼ (π l_eff/√10) κ` unbounded | same with `l` |

## Candidate map to PB2009 `(g,h)` — **not locked**

ScienceDirect attributes to the intended paper a two-constant `(g²,h²)` infinite-space phase velocity depending on `k`. A **possible** `[B]` dictionary, **if** their infinite-space law is of the form `c(k)=c0 √((1+g²k²)/(1+h²k²))`, would be:

- `g² ↔ l²/10` (isotropic)
- `h² ↔ ℓ²`

This dictionary is **not** used as a numerical target. It is recorded only so it is not rediscovered as a guess later. **TV10 stays OPEN.**

Anisotropic `L` has **no** counterpart in the PB2009 abstract.

## P2.2 / P2.3 / P2.4 / P2.7

Already executed in P1:

| Item | Where | Status |
|---|---|---|
| P2.2 long-wave | M10.2 + M11 | `[A]` |
| P2.3 high-k | M16 17/17 | `[A]` |
| P2.4 flux | M17 13/13 | `[A]` |
| P2.7 limit ladder | M07 | `[A]` |

P2 adds a two-route (SymPy vs float) check of the **isotropic** specialisation only (`p2_caseH_isotropic.py`).
