# P12C Quadrature / FEM Forensic Audit (Part D)

Base `phase-1-symbolic @ 0d985029` (+ Part C corrections committed separately) · 2026-09-24.
Audited against the frozen foundation: `DERIVATION_M14.md` (§M14.3, §M14.6), M13
(`DERIVATION_M13.md`, `m13_bfs_shape.log`), `AUDIT_M14_independent.md` (Q1–Q6), TV18.
Independent verification: `audit/probes/quadrature_degree_probe.py` (new, reproducible;
rebuilds the bicubic Hermite element from scratch and re-derives the rule requirements).

## 1. Degree audit (what the integrands actually are)

Frozen M13/M14 degrees, per coordinate (x, y), with the minimal tensor Gauss rule n
satisfying 2n−1 ≥ deg:

| integrand class | degree (x, y) | minimal n |
|---|---|---|
| `NᵀN` (M₀) | (6, 6) | 4 |
| `N,ᵢᵀ N,ᵢ` (M^g) | (6, 6) | 4 |
| `BᵀGB` (K^c) | (6, 6) envelope (e.g. (4,6)/(6,4)/(5,5) blocks) | 4 |
| `B,xᵀGB,x` (K^g, L₁₁) | (4, 6) | 4 (3 fails in y) |
| `B,yᵀGB,y` (K^g, L₂₂) | (6, 4) | 4 (3 fails in x) |
| `B,xᵀGB,y + B,yᵀGB,x` (K^g, L₁₂) | (5, 5) | 3 |

**Independent verification (probe output).**
- Monomial sweep (unit square, 0…8 exponents): largest passing exponent n=2 → 3; n=3 → 5;
  n=4 → 7 — exactly 2n−1.
- Real element assembly, tensor rules vs an n = 12 reference (relative Frobenius):

| n | K^c | K^g | M₀ |
|---|---|---|---|
| 2 | 1.74e-1 | 3.47e-2 | 1.62e-1 |
| 3 | 6.80e-3 | 6.08e-3 | 9.45e-3 |
| 4 | 1.22e-15 | 7.31e-16 | 5.98e-16 |

Verdict: **2×2 and 3×3 are insufficient; 4×4 is the minimal tensor rule that integrates
every homogeneous-rectangle element matrix exactly.** The frozen M14 claim is confirmed
independently. The blueprint's “quartic” phrase is the degree of a factor, not of the
product integrand (M14.3; Part C corrected the one manuscript sentence that repeated it).

## 2. Exact vs inexact — the boundary of the exactness claim

- **Exact (verified):** element matrices on a *homogeneous* affine rectangle — K^c, K^g(θ,AR),
  M₀, M^g — because the integrands are polynomials and 4×4 is exact through degree 7/axis.
- **Not exact (verified):** an element **cut** by the circular inclusion. The material field
  is a piecewise-constant indicator sampled at Gauss points, so the sampled area is a
  staircase of the true interface. Independent demonstration (4×4 Gauss per sub-element,
  quarter-disc area vs π/4):

| sub-elements | h | |error| |
|---|---|---|
| 1 (single cut element) | 1 | 7.09e-2 |
| 4 | 0.5 | 1.20e-2 |
| 16 | 0.25 | 2.73e-3 |
| 64 | 0.125 | 1.19e-3 |
| 256 | 0.0625 | 3.90e-4 |
| 1024 | 0.03125 | 1.22e-4 |

  The error is **not** quadrature exactness — it decreases roughly ∝ h (consistent with M14's
  documented “O(h) area error per cut element”), and the single-element deviation 7.1e-2 is
  ≫ 10⁻³ as M14 (Q6) states. **No exactness claim may be attached to cut/interface elements.**

## 3. Over-generalization check (homogeneous → cut elements)

- Frozen status: TV18 = **LOCKED [S]** — “standard immersed Gauss-quadrature indicator
  function on a regular mesh” with the O(h) interface approximation documented; the option
  list (mesh-conforming / Gauss-point material / sub-cell adaptive) remains classified in M14.
- Repo-wide search: **zero** occurrences of “exact interface”, “exact curved interface”, or
  equivalent claims in any active text. The only “quadrature invariance” language was in
  sec06 (Part B F-2 / Part C C-7) and has been replaced by a scoped statement.
- One over-generalization existed until this audit: sec04 stated the rule “integrates all
  terms exactly” with no scoping (and with the wrong degrees). **Corrected in Part C** — the
  sentence now states degree-6 product integrands, the minimality of 4×4 for homogeneous
  elements, and the O(h) sub-cell treatment in cut elements, pointing to §Case C.

## 4. The 4×4 / 6×6 / 8×8 study — how is it described?

- **Source**: `p11_caseC_convergence.json` `quadrature_sensitivity` (preserved P11B-era file):
  observable `gap_at_X` (X-point directional gap) on the **4×4 mesh**: 2.7563 / 2.7226 / 2.7862.
- Frozen production operator uses `n_gauss = 4` everywhere (verified by code: P11B module
  default, P11D `n_gauss=4`, P12C 32²/64² `n_gauss=4`).
- **Historical wording** (`P11B_REMEDIATION_AUDIT.md`): “band gap width is invariant to within
  1.22 %… quadrature errors negligible”. Classified **B (historical)**: it is a one-observable,
  one-mesh numerical statement, not a proof; it is a preserved audit record and is **not
  edited** (history-preservation rule). The active manuscript text (Part C) now reads:
  X-point directional gaps at the fixed 4×4 mesh, deviations −1.22 %/+1.08 % from the 16-point
  result, no proof/exact/invariance claim.
- Justification status: the *mathematical* exactness statement is justified only for
  homogeneous elements (§1); the *numerical* interchangeability of rules at 4×4 is justified
  for the reported X-gap at that resolution (§2/§4 data); neither is presented as a proof of
  interface-quadrature exactness.

## 5. Verdict

- Frozen M14 quadrature foundation: **verified, stands** (degree 6/axis; 4×4 minimal exact;
  3×3 fails on M₀/K^c/K^g-diagonal; cut elements O(h)).
- Active-text defects found: 1 (sec04 degree/scoping) → corrected in Part C.
- No unaddressed FEM/quadrature math defect found. No new calculations introduced; the probe
  reads no repository data.
