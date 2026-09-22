# TV10 — PB2009 source record (equation-level, from supplied PDF)

**Status:** CLOSED for exact transcription of Eqs. (22)–(28). Mapping to our Case-H remains **[B]** (not an identity).
**PDF:** `paper9/analytic/pb2009/papargyri-beskou2009.pdf`
**sha256:** `8ca9c8208d5fbe4a24fa954be641c98eba95bfdb97f9fc17e1a227479c3a8ddb`
**Git blob on `main`:** `51cd382c34ec3f99218cf1dfa4f3fd5182977933` (`papargyri-beskou2009.pdf` at repo root; not checked out on this branch)
**Date:** 2026-09-22

PDF page *n* = journal page **3750+n** (footer verified: PDF p.3 → 3753; PDF p.5 → 3755).

## Identity **[C]** (PDF p.1 / journal 3751)

Papargyri-Beskou, S.; Polyzos, D.; Beskos, D.E. (2009). Wave dispersion in gradient elastic solids and structures: A unified treatment. *Int. J. Solids Struct.* **46**:3751–3759. DOI 10.1016/j.ijsolstr.2009.05.002.

Blueprint 46:2151–2159 / two-author cite remains a bibliographic error.

## Constitutive / EOM needed to read (22)–(28) **[C]**

Simplest Mindlin Form II, one gradient coefficient `g²` (length²), plus micro-inertia `h²` (PDF p.1, p.3).

Potential (12), PDF p.3 / 3753:

`Ŵ = e_ij s_ij + g² ∂_i e_jk ∂_i s_jk`

with `â1=â3=â5=0`, `â2 = k g²/2`, `â4 = l g²`, hence `l₁² = l₂² = g²`.

Stresses (15)–(17), same page:

- `s_ij = 2 l e_ij + k e_ii δ_ij`
- `λ_ijk = g² ∂_i s_jk`
- `r_ij = s_ij − g² ∇² s_ij`  (minus sign in front of `g²`)

EOM (14), PDF p.3 / 3753 (k,l = Lamé λ,μ; q = ρ):

`(1 − g² ∇²)[ l ∇²u + (k+l) ∇(∇·u) ] = q (ü − h² ∇² ü)`

Restrictions (13), PDF p.3 / 3753:

`l > 0`, `k+2l > 0`, `g² > 0`, `h² > 0`.

## Infinite-space dispersion **[C]** — PDF p.3 / 3753

From Helmholtz split (18)–(19) into (14):

**(20)**  `ω² = C_p² k_p² (1 + g² k_p²) / (1 + h² k_p²)`,  `C_p² = (k+2l)/q`

**(21)**  `ω² = C_s² k_s² (1 + g² k_s²) / (1 + h² k_s²)`,  `C_s² = l/q`

**(22)**  `V_{p,s} = ω / k_{p,s} = C_{p,s} √[ (1 + g² k_{p,s}²) / (1 + h² k_{p,s}²) ]`

Eq. (22) **is** the infinite-space P/S phase-velocity law. Also valid in 2-D with S → SV (PDF p.4 / 3754).

**(23)** h=0: `V = C √(1+g²k²)` unbounded as k→∞ (unacceptable).

**(24)** g=0: `V = C / √(1+h²k²)` bounded (acceptable).

## g vs h **[C]** — PDF p.4 / 3754

From (22): `V_{p,s} ≤ C_{p,s}` ⇒ **`g ≤ h`**; `V_{p,s} ≥ C_{p,s}` ⇒ `g ≥ h`.

Also: `g=h` or `g=h=0` ⇒ no dispersion, `V=C`. `h>g`: lattice-like decreasing V. `h<g`: granular-like increasing V. `h=0`: unbounded, not acceptable.

## Axial bar **[C]** — PDF p.5 / 3755

**(25)**  `E u'' − g² E u'''' = q ü − q h² ü''`

**(26)**  `r = E e − g² E e''`

**(27)**  `u = U exp[i(kx − ωt)]`

**(28)**  `V_gh = ω/k = √(E/q) √[(1+g²k²)/(1+h²k²)] = V_c √[(1+g²k²)/(1+h²k²)]`

As `k→∞`, `V_gh/V_c = g/h`. `g=h` or both zero: classical non-dispersive.

## Mapping to our Case-H (M10.2) **[A]/[B]** — not claimed as PB identity

Our locked **[A]** (isotropic `L = l² I`):

`ω_T² = (μ/ρ) k² (1 + l² k² / 10) / (1 + ℓ² k²)`  
`ω_L² = ((λ+2μ)/ρ) k² (1 + l² k² / 10) / (1 + ℓ² k²)`

Compare with (20)–(21). Same **functional form** iff

| PB **[C]** | our **[A]** | grade |
|---|---|---|
| `C_s² = l/q`, `C_p²=(k+2l)/q` | `μ/ρ`, `(λ+2μ)/ρ` | **[B]** notation (same Lamé/ρ) |
| numerator coefficient `g²` | `l²/10`  (`k·L·k/\|k\|²/10`) | **[B]** *specialisation + identification*, **not** derived from PB (12) |
| denominator coefficient `h²` | `ℓ²` | **[B]** EOM-slot match of (14) vs M8 Laplacian micro-inertia |

**`g² ↔ l²/10` is not source-supported as an exact constitutive identity.** PB never writes a factor `1/10`. The `1/10` is ours (Form-II isotropic length-tensor reduction, M4/M6). It is justified **only** as: *if* we specialise Case-H to isotropic `L` *and* we **define** `g² := l²/10`, `h² := ℓ²`, then (20)–(22) and M10.2 coincide algebraically.

Anisotropic `L(θ)`, `l1≠l2`: **not in PB2009**. Not transferable.

Layer-3 use: evaluate **[C]** (22) and (28) in *their* `(g,h)`; compare to our solver only after the isotropic identification above.

**TV10 closed** because (22)–(28) are now transcribed from the PDF with numbers and pages. The mapping is recorded as **[B]**, not as **[C]**.
