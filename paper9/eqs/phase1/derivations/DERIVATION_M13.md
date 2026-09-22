# DERIVATION M13 — Bogner–Fox–Schmit bicubic Hermite rectangle (blueprint §4.1, eqs. (53)–(56))

Status: **checks PASSED (24/24)** · Script `scripts/m13_bfs_shape.py` · Log `checks/m13_bfs_shape.log`.
Scope source (repository text): Blueprint v1.3 line 399 (§4.1), 583 (register (53)–(56)), 408/616 (Fig. 3),
1062; `CALC_MASTER_PLAN.md` row M13 (line 48: depends on M3; "conforming in H²"; output "element
interpolation"; consumer M14); `PHASE1_FORMULATION_PLAN.md` line 34/43 ("BFS DOF ordering documented →
M13"). Inputs: M3 kinematics `ε_ij = (u_i,j+u_j,i)/2`, `η_ijk = ε_ij,k`; M4/M6 pair ordering
`q = (ε₁₁, ε₂₂, ε₁₂)` with `C̄` (shear entry 2μ) and `D_c = diag(1,1,2)`; M9 phases (40)–(43) on
value, first- and mixed-derivative DOFs; M8 weak form (M8.2) requires `u ∈ H²`. **Not done here:** element
matrices (57)–(61) = M14; Bloch transformation/reduced matrices (62)–(71) = M15.

## M13.1 Exact scope `[L]`

§4.1: "Tensor product of 1D cubic Hermite; 4 DOF per node per displacement component {u, u,x, u,y, u,xy};
2 components × 4 nodes × 4 DOF = 32 DOF per cell; C¹ inter-element continuity, conforming in H²(Ω). Shape
functions and the B / B,i matrices." Acceptance: `H²` conformity (plan) and the interpolation objects
needed by M14.

## M13.2 (53) Shape functions — derived `[A]` (S1–S5)

1-D cubic Hermite on `[0,h]`, `t = s/h`: `H_v0 = 1−3t²+2t³`, `H_d0 = h(t−2t²+t³)`, `H_v1 = 3t²−2t³`,
`H_d1 = h(−t²+t³)`; derivative DOFs are **physical** derivatives (factor h). Kronecker property and cubic
completeness verified (S1–S2). Bicubic: `N_(n,type)(x,y) = H^x_(·)(x) H^y_(·)(y)` with the x-factor a
value function for types {u, u,y} and a slope function for {u,x, u,xy}, the y-factor a value function for
{u, u,x} and a slope function for {u,y, u,xy}. Nodes 1(0,0), 2(h_x,0), 3(h_x,h_y), 4(0,h_y) (CCW).
Verified: full Kronecker property `D_type′ N_(n,type)(node m) = δ_nm δ_type,type′` (256 conditions, S3);
span = Q₃, rank 16, exact reproduction of any bicubic with its nodal data (S4); partition of unity and
linear completeness (S5).

## M13.3 (56) DOF layout, C¹ and H² conformity `[A]` (S6–S8)

Per node per component `{u, u,x, u,y, u,xy}` → 8 per node → **32 per element/cell** (blueprint). Element
DOF ordering adopted for the audit and for M14/M15 unless the blueprint says otherwise:
`index = 8(node−1) + 4(comp−1) + type`, type ∈ {0:u, 1:u,x, 2:u,y, 3:u,xy}. The blueprint does not fix
an ordering → **TV17** (bookkeeping only; no mathematical content).

On the edge `x = h_x` (shared with the right neighbour): traces of `u` **and of the normal derivative
`u,x`** of all off-edge functions vanish; for edge nodes the trace of `u` is the 1-D Hermite in y carried
by `{u, u,y}` and the trace of `u,x` is the 1-D Hermite in y carried by `{u,x, u,xy}` (S6–S7). Hence `u`
and `∂u/∂n` are continuous across the edge iff the shared nodal DOFs coincide — **the mixed DOF `u,xy` is
necessary for C¹** (it is the tangential derivative of the normal slope). Same for `y = h_y` (S8).
Piecewise-Q₃ and globally C¹ ⇒ `u ∈ H²(Ω)`: conforming for the M8 weak form (which contains `η = ∇ε`,
second derivatives). Second derivatives are in general discontinuous across edges (admissible).

## M13.4 (54)–(55) B and B,i — derived `[A]` (B1–B5)

With `u = N d` (2×32): `q = B d`, `B` (3×32) rows `[N,x ; 0]`, `[0 ; N,y]`, `[N,y ; N,x]/2` — **tensor
shear `ε₁₂`**, consistent with the locked `C̄` (2μ entry) and `D_c = diag(1,1,2)`; using `γ₁₂` here would
double-count the shear energy with that `C̄` (B1). `B,i := ∂B/∂x_i` (3×32 each) gives `η_(··)i = q,i`, the
strain-gradient pairs of M3 (11); compatibility `(B,x),y = (B,y),x` (B2). Null spaces: rigid-body modes
(2 translations + rotation) in `ker B` identically; constant-strain fields in `ker B,i`; quadratic fields
give exact constant strain gradients (Q₃ ⊃ P₂) (B4–B5). These are the element-level patch-test identities.

Polynomial degrees (computed, B3): `N` total degree 6 (3 per direction); `B` entries total 5; `B,x`
entries total 4 (degree 2 in x, 3 in y). Integrands for M14: `NᵀN` degree 6 per direction, `BᵀGB` ≤ 6 per
direction, `B,iᵀ G B,j` ≤ 6 per direction. **The blueprint's §4.2 phrase "second derivatives of cubics ⇒
up to quartic" is not the degree of the product integrand** — the M14 Gauss rule must be justified against
degree 6 per direction (exact with 4 points per direction on a rectangle, i.e. 4×4; to be stated and
justified in M14, not decided here). Recorded as a note for M14, no TV needed (M14's own scope).

## M13.5 Units, mapping, matrix structure `[A]` (U1–U3)

Units: `N_u` dimensionless, `N_(u,x), N_(u,y)` ~ m, `N_(u,xy)` ~ m²; B entries 1/m, 1, m per type so `q`
is dimensionless; scaling `h → ch` multiplies type-k functions by `c^k` (U1). Mapping: axis-aligned
rectangle, affine `x = h_x(1+ξ)/2`, constant Jacobian `J = h_x h_y/4`, `∂/∂x = (2/h_x)∂/∂ξ`; **no
isoparametric distortion** — BFS loses C¹ on non-affine maps, so the Case-C cell (square lattice, centred
circular inclusion) must be meshed by axis-aligned rectangles with the inclusion represented through the
material field at quadrature points (staircase/area-fraction) — an unstated blueprint assumption →
**TV18**. Structure: for symmetric `G = D_c C̄` and symmetric `L`, `BᵀGB` and `Σ L_ij B,iᵀ G B,j` are
symmetric integrands; the 16 scalar functions are independent so the Gram (mass) matrix is positive
definite (U3). Values are M14.

## M13.6 Bloch phase at the interpolation level (M9 (40)–(43)) `[A]` (P1–P4)

For one L×L cell with node-1 DOFs as masters and slave nodes phased `node 2 = μ_x·node 1`, `node 4 =
μ_y·node 1`, `node 3 = μ_xμ_y·node 1` for **all four DOF types** and both components (M9 (43)), the
interpolated field satisfies **identically along the whole edge** `u(L,y) = μ_x u(0,y)`,
`u,x(L,y) = μ_x u,x(0,y)`, `u(x,L) = μ_y u(x,0)`, `u,y(x,L) = μ_y u,y(x,0)` for generic complex DOFs —
verified at Γ, X, M **and at a generic interior k** `(3π/7L, 2π/5L)` (P1). Negative controls at the
generic k: phase on value DOFs only fails (P2); conjugate phase on the x-derivative DOFs fails at generic k
but is **invisible at Γ, X, M** where μ is real (P3) — high-symmetry points alone do not validate the
derivative-DOF phase (agrees with M15-a F4a). The tying is x-independent and multiplicative (P4). No
reduced-matrix identity is used or implied; `K̄(k) = K̄(−k)ᴴ` does not appear.

## M13.7 Assembly compatibility `[A]` (A1)

The Kronecker property is coordinate-based with physical derivatives, so the 8 DOFs of a node shared by up
to four elements are the same physical quantities → direct scatter-add with one global DOF per
(node, component, type). Counting for an n×n mesh of the cell: `8(n+1)²` DOFs before periodicity, `8n²`
after Bloch tying (n = 1: 32 → 8) — the M15 dimension bookkeeping starts from this.

## M13.8 Assumptions not stated in the blueprint → TV `[S]`

| id | item | consequence |
|---|---|---|
| **TV17 (new)** | element/global DOF ordering and node numbering (not fixed by §4.1) | bookkeeping for M14/M15 code; ordering above adopted provisionally |
| **TV18 (new)** | BFS requires axis-aligned rectangles (no isoparametric map); representation of the circular inclusion of Case C (material field at Gauss points / area fraction / boundary-fitted is impossible with BFS) | mesh-convergence study §5.7 and TV6 (inclusion radius/contrast) |
| note for M14 | integrand degree 6 per direction, not "quartic" | quadrature rule justification (M14 scope) |
| unchanged | TV4, TV6, TV14, TV15, TV16 | not touched |

## M13.9 Not changed

Blueprint v1.3 (sha `ca71b91a…`), M1–M12 records, M12 partial status and its micro-inertia-flux finding,
M15-a ruling. M14, M15 not started.
