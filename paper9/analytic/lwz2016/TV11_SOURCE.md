# TV11 — LWZ2016 source record (equation-level, from supplied PDF)

**Status:** CLOSED for TM/Bloch dispersion equation + constitutive `(c,d)` + four interface conditions. **Not** a validation source for 2-D anisotropic Case-H.
**PDF:** `paper9/analytic/lwz2016/li2015.pdf`
**sha256:** `88115557af9e9fb46c5f1bd64fdc023f1e6ca45a01257404d6115a6afc0cb48e`
**Git blob on `main`:** `5a267ed9751e5ae511b158742bd1d19f5442a03d` (`li2015.pdf` at repo root)
**Date:** 2026-09-22

PDF has 19 pages covering *Acta Mech.* **227**:1005–1023 (no printed journal footers). Citations below use **PDF page**.

## Identity **[C]** (PDF p.1)

Li, Yueqiu; Wei, Peijun; Zhou, Yahong (2016). Band gaps of elastic waves in 1-D phononic crystal with dipolar gradient elasticity. *Acta Mechanica* **227**:1005–1023. DOI 10.1007/s00707-015-1495-z.

## Constitutive / EOM **[C]** — PDF pp.3–4

Strain energy (3):

`W = (½ λ ε_ii ε_jj + μ ε_ij ε_ij) + (½ λ c ε_ii,k ε_jj,k + μ c ε_ij,k ε_ji,k)`

**(4.1)** `τ_ij = λ δ_ij ε_pp + 2μ ε_ij`  (monopolar)

**(4.2)** `μ_kij = c (λ δ_ij ε_pp + 2μ ε_ij),_k`  (dipolar); `c` has dimension m².

Kinetic energy **(5)**: `T = ½ ρ ú_j ú_j + (1/6) ρ d² ú_{k,j} ú_{k,j}`  (`d` = microstructure length).

EOM **(8)**: `(τ_jk − μ_ijk,i),_j + F_k = ρ ü_k − ρ d²/3 ü_{k,jj}`

Displacement form **(10)** PDF p.4:

`(1 − c ∇²)[(λ+μ) ∇∇·u + μ ∇²u] = ρ ü − ρ (d²/3) ∇² ü`

## Homogeneous-solid dispersion (single gradient solid, not the PC) **[C]**

Anti-plane travelling SH **(14.1)** PDF p.4:

`ω² = σ_sh² V_s² (1 + c σ_sh²) / (1 + d² σ_sh² / 3)`,  `V_s² = μ/ρ`

In-plane P/SV **(20.1)–(20.2)** PDF p.5:

`ω² = σ_p² V_p² (1 + c σ_p²) / (1 + d² σ_p² / 3)`,  `V_p² = (λ+2μ)/ρ`

`ω² = σ_s² V_s² (1 + c σ_s²) / (1 + d² σ_s² / 3)`

Evanescent companions (14.2), (20.3)–(20.4) exist; not a Case-H band.

These **are** homogeneous closed forms for *one* isotropic dipolar-gradient solid. They are **not** the 1-D PC result. They match PB (20)–(21) iff `c = g²` and `d²/3 = h²` **[B]**.

## Four interface / state-vector conditions **[C]**

Abstract + PDF p.2: continuity of **displacement**, **normal derivative of displacement**, **monopolar traction P**, **dipolar traction R**.

Anti-plane state **(23)** PDF p.7: `V = [u_z, u_{z,x}, P_z, R_z]^T`

Perfect interface **(28)** PDF p.7: `V_A^R = V_B^L`

In-plane state **(34)** PDF p.8: `V = [u_x, u_y, u_{x,x}, u_{y,x}, P_x, P_y, R_x, R_y]^T` (8-vector)

Tractions (22.1–2), (33.1–4), (9.1–2) as written in the PDF.

## TM / Bloch **[C]**

Layer map **(25)–(26)** PDF p.7: `V^R = T V^L`, `T = P G P^{-1}`

Cell **(29)**: `V_B^R = T_B T_A V_A^L`

Bloch **(30)**: `V_B^R = exp(i k_x a) V_A^L`, `a = a1+a2`

Dispersion **(32)** PDF p.7 (anti-plane, oblique):

`| T_B T_A − I exp(i k_x a) | = f(ω, ξ, k_x) = 0`

In-plane **(39)** PDF p.8: same determinant, 8×8 T.

Normal incidence **(40)** PDF p.9: `|T_B T_A − I exp(i k a)| = f(ω,k) = 0` (P, SV, SH decoupled).

Explicit T entries: Appendix 1–3 (PDF pp.16–18). Not re-typed here in full; evaluator may read the PDF.

## Numerical example parameters **[C]** — PDF p.10

`V_p1/V_s1 = 2.6621`, `V_p2/V_p1 = 0.562`, `V_s2/V_s1 = 0.5947`, `ρ2/ρ1 = 0.1573`, `a1/a = 0.5`.

Fig. 3 gradient case: `c̄1 = √c1/a = 0.5`, `c̄ = c1/c2 = 0.77`, `d̄1 = d1/a = 0.5`, `d̄ = d1/d2 = 2`.

Non-dimensional law (44)–(45) PDF p.9.

## Relevance

| Target | Transferable? | Tag |
|---|---|---|
| Present 2-D anisotropic Case-H | **No** | **[C] different problem** (periodic bilayer vs homogeneous anisotropic `L`) |
| Homogeneous isotropic infinite medium | Yes, via (14.1)/(20.*), not via (32) | **[C]** single-solid; **[B]** vs Case-H after `c ↔ l²/10`, `d²/3 ↔ ℓ²` |
| Future 1-D Case-C TM (P3 B6) | Yes: bilayer, 4 (anti-plane) or 8 (in-plane) interface quantities, (32)/(39)/(40) | **[C]** formulation; SH-normal TM in `validation/b6_lwz_tm/` (B6 **PARTIAL**; Fig. 3 **BLOCKED**) |

**TV11 closed** for the intended Layer-3b *source equation* (TM/Bloch determinant + `(c,d)`). It is **not** closed as a Case-H validator.
