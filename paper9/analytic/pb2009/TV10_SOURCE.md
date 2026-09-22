# TV10 — PB2009 source record (P2.5)

**Status:** OPEN. No original PDF in `paper9/analytic/` or `paper9/bib/`.
**Date:** 2026-09-22
**Rule:** transcribe only from available evidence; do not invent Eqs (22)–(28).

## Blueprint bibliographic claim

Papargyri-Beskou & Beskos (2009), *Int. J. Solids Struct.* **46**:2151–2159, Eqs (22)–(28).
Plan card **B5** / A5: infinite medium + axial bar, parameters `g²`, `h²`.

## Evidence actually retrieved (not the PDF)

1. ScienceDirect record [S0020768309001966](https://www.sciencedirect.com/science/article/pii/S0020768309001966), DOI [10.1016/j.ijsolstr.2009.05.002](https://doi.org/10.1016/j.ijsolstr.2009.05.002):
   - **Title:** Wave dispersion in gradient elastic solids and structures: A unified treatment
   - **Authors:** S. Papargyri-Beskou, **D. Polyzos**, D. E. Beskos (three authors, not two)
   - **Venue:** *IJSS* **46**(21), 15 October 2009, **pages 3751–3759** (not 2151–2159)
   - Abstract (verbatim sense): infinite space, axial bar, Bernoulli–Euler beam, Kirchhoff plate; simple gradient elasticity with **micro-elastic and micro-inertia** characteristics; micro-elastic terms alone do not give realistic dispersion; micro-inertia is required.
   - Publisher snippet (ScienceDirect HTML, not PDF page images) attributes:
     - infinite-space **Eq. (22)**: P and S **phase velocities as functions of wave number**, involving two microstructural constants **g²** and **h²**;
     - axial bar **Eqs (25), (26)** (EOM) and **Eq. (28)** (dispersion);
     - physical-velocity remark **g ≤ h**; **g = 0, h ≠ 0** still admissible.

2. *IJSS* vol. 46 (2009) issue 20 occupies pages 3505–3750. Page range **2151–2159** is therefore a **different article** (or a bibliographic error), not the unified-treatment paper.

## What is **not** transcribed

No equation bodies for (22)–(28). No constitutive operator, no exact placement of `g²`/`h²` in numerator/denominator, no bar EOM coefficients. Those remain **TV10**.

## Classification vs our Case-H (M10.2)

| Claim | Tag | Note |
|---|---|---|
| Bibliographic identity of B5 cite vs 46:2151–2159 | **[C] fail / mismatch** | intended paper is almost certainly 46:3751–3759 with Polyzos |
| Exact Eqs (22)–(28) as Layer-3 machine-precision target | **TV10 OPEN** | PDF absent |
| Structural analogy (isotropic `L`, `g² ↔ k·L·k/\|k\|²/10`, `h² ↔ ℓ²`) | **[B] candidate only** | **not** asserted as identity; not used as a numerical evaluator of PB2009 |
| Anisotropic `L` (our `l1≠l2`, `θ`) | **not in** the ScienceDirect abstract of PB2009 | Case-H anisotropy is **[A]** ours, not **[C]** PB2009 |

**Evaluator of PB2009 Eqs (22)–(28): not written.** Writing one would invent the missing formulas.

## Action required to close TV10

Place the original PDF (or a lawful extract of pp. 3751–3759 containing (22)–(28)) under `paper9/analytic/pb2009/` and transcribe symbol-by-symbol.
