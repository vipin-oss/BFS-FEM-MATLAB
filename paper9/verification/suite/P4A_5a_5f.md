# P4A — tests 5a–5f (early solver verification)

**Date:** 2026-09-22  
**Solver:** 1 homogeneous BFS rectangle = unit cell `L=1`. Assembly = M14 4×4 Gauss; `T(k)` = M15 (same unimodular phase on `{u,u_x,u_y,u_xy}`). Reduced pencil 8×8.  
**Not done:** 5g–5i, P3, production bands, Blueprint, TV10/TV11.

## Parameters `[S-P4A]`

| name | value |
|---|---|
| λ, μ, ρ | 1, 1, 1 |
| ℓ² | 0.04 |
| isotropic l | 0.2 (`l1=l2`) |
| anisotropic | l1=0.30, l2=0.10 |
| L_cell = hx = hy | 1 |
| python / numpy | 3.13.14 / 2.3.5 |
| two-run | identical logs (deterministic) |

`c_T=1`, `c_L=√3`. Length tensor: M02 `L = R^T diag(l1²,l2²) R`.

## Compact table

| Test | Purpose | Configuration | Metric | Tolerance | Result |
|---|---|---|---|---|---|
| 5a | Hermiticity `K̄^H=K̄`, `M̄^H=M̄` | interior (2), Γ, X, M; 8×8 | max rel Frobenius | < 1e-12 | **PASS** |
| 5b | `K̄(k+G)=K̄(k)` + eig | interior k; G=b1,b2,b1+b2 | rel matrix / eig | < 1e-12 / 1e-10 | **PASS** |
| 5c | rotation AR=1 | l1=l2=0.2; θ∈{0,15,37,90,128}°; interior k | max rel eig | < 1e-10 | **PASS** |
| 5d | acoustic slope | k=(κ,0), κ=1e-2…1e-4 | rel \|v−c\|/c | < 1e-6 (≥2 κ) | **PASS** |
| 5e | θ→θ+90°, l1↔l2 | l1≠l2; 3 interior k | max rel eig | < 1e-10 | **PASS** |
| 5f | definiteness | Γ and interior | see below | formulation | **PASS** |

## Residuals (run 2, identical to run 1)

**5a** max rel `K̄`: **2.012e-16**; `M̄`: **5.628e-17**. dim 8×8 (unreduced 32×32).

**5b** interior k=(3π/7, 2π/5). Matrix rel ≤ **4.0e-16**; eig rel ≤ **9.7e-16**.

**5c** max rel eig vs θ=0: **9.635e-16**.

**5d** sequence max(eT,eL): 1.800e-6 (κ=1e-2, *above* 1e-6 as O(κ²) Case-H dispersion), 1.620e-7, 1.800e-8, **1.253e-8** (κ=3e-4, best), 2.253e-7 (κ=1e-4, roundoff on vT). Four κ meet <1e-6. Do not use a single κ.

**5e** with swap: max rel **6.438e-16**. Without swap (negative control): **0.179**.

**5f** Γ `K̄` eigs: **−1.65e-16**, **5.33e-18**, then 5.36e-3, … (two translation nulls expected; **not** requiring PD at Γ). Γ `M̄` min **9.887e-5** > 0, cond ~1.01e4. Interior `K̄` min **9.785e-3** > 0; `M̄` min **3.617e-4**; min ω² **3.028**.

## Counts

34 checks, **34 PASS**, 0 FAIL. 5g–5i not run (P4B). P3 not started.
