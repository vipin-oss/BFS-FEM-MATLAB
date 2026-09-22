# PHASE-1 DERIVATION AND MATHEMATICAL-AUDIT RECORD — MODULE M9
## Bloch theorem for the C¹ gradient-elastic medium: lattice structure and the derived phase rules

Status: **M9 COMPLETE at symbolic level — 45 checks PASSED**. M1–M8 unchanged (separate records
`DERIVATION_M01_M07.md`, `DERIVATION_M08.md`, `AUDIT_M8a_boundary_operator.md`); M10–M17 NOT
STARTED. Phase 0 LOCKED (`main` @ `175ea9e`). No scientific PASS is claimed: this record contains
no numerical parameter value, no benchmark comparison, no solver code and no band-structure result.

**One forward-scope item is flagged and NOT repaired** (§M9.8): the blueprint's Sec 4.5 statement
"prove K̄(k) = K̄(−k)^H" (eq. (68)) and the Sec 4 pitfalls test built on it cannot be established
from the locked formulation in their literal form. It is an M15-scope claim; it does not affect any
M9 equation. Recorded as **M15-a**, status TO BE VERIFIED — a ruling is required before M15.

Governing inputs (read-only):
- Blueprint v1.3 `paper9/plan/blueprint/Paper9_Blueprint_v1.3.tex`
  (sha256 `ca71b91aba4ca4abe9f157eb595ac8c2f709d838957a08ea0dce7160685dbf9f`), Sec 3.1–3.2
  (equations (36)–(43)), with C3 (line 158), the Sec 4.4/4.5 rows (lines 402–403), the pitfalls
  table (line 416) and the register rows 573–579.
- `paper9/plan/CALC_MASTER_PLAN.md` v1.1 §A row M9 and §F9.
- Locked Phase-1 results: `DERIVATION_M01_M07.md` (M1–M7), `DERIVATION_M08.md` (M8, operational
  strong form and boundary/interface quantities), `AUDIT_M8a_boundary_operator.md` (M8-a: the
  reduced four-quantity boundary model (O1)–(O6) is the operational model; interpretation (A)),
  `AUDIT_F1_five_constant_vs_tensor_modulus.md` (F1: a₁…a₅ are the labelled isotropic family, (26)
  is the operational anisotropic modulus).
- Legacy `[C]` source check (read-only, outside repo): `femcheck/FEM_Total/ptxt/FEM_1_Paper.txt`
  contains **no** Bloch/Floquet/periodicity/reciprocal-lattice material (grep: the only matches for
  "periodic" are literature titles about triply periodic minimal surfaces). **M9 therefore has no
  `[C]` source**: it is derived `[A]` from the blueprint and the locked M1–M8 formulation only.

Provenance tags: `[C]` cited source · `[A]` derived in this work · `[S]` definition/structural choice.

Reproduce:

```
cd paper9/eqs/phase1
python3 scripts/m09_bloch_c1.py     # M9   (45 checks)
```

Deterministic (two consecutive runs give byte-identical output), SymPy exact arithmetic, all
quantities symbolic, writes no files.
Script sha256 (pre-run = post-run, recorded in `checks/m09_bloch_c1.log`):
`c5980f4d9d60141ca3c859c6a07ec4fb9e49b37472e5664118a2e8689f228ace`.

Note on record preservation: the status line of `DERIVATION_M08.md` ("M9–M17 NOT STARTED") is
historical, as of that record's own commit; previous records are **not** re-edited. The living
status is carried by `PHASE1_MANIFEST.md`.

---

## M9.0 — Exact M9 scope, preserved terminology `[S]`

Blueprint v1.3, Sec 3.1–3.2 (verbatim content of the two rows, line 377 and line 378):

- **3.1** "Unit cell Ω_cell = [0,L]×[0,L]; lattice vectors **a**₁, **a**₂; reciprocal vectors
  **b**₁, **b**₂; first Brillouin zone." → equations **(36)–(38)**.
- **3.2** "**Bloch theorem for a C¹ gradient-elastic medium.** Time-harmonic ansatz;
  **u**(**x**+**a**_α) = **u**(**x**) e^{i **k**·**a**_α}. **Then the critical step:** because the weak
  form contains first derivatives as independent DOFs, the *same* phase factor must be imposed on
  ∇**u** and on ∂²**u**/∂x∂y. **Derive this from the Bloch condition rather than asserting it.**"
  → equations **(39)–(43)**.

Module row (plan v1.1 §A M9): "Bloch theorem for a C¹ medium (phase on value **and** derivative
DOFs, derived not asserted) — (36)–(43) — depends on M8 — assumption: time-harmonic `e^{−iωt}`,
infinite periodic medium — input: lattice `a1,a2` — output: phase-factor rules for
`{u, u,x, u,y, u,xy}` → M15 (headline C3)".

Terminology preserved throughout: *unit cell, lattice vectors, reciprocal vectors, first Brillouin
zone, irreducible Brillouin zone, time-harmonic Bloch ansatz, Bloch condition, phase factor,
critical step, value and derivative DOFs, master–slave (tying) route.*

**Allocation of the eight equations** `[S]` (the blueprint states the content of (41)–(43)
collectively, it does not enumerate them; the allocation below is the natural reading and is
recorded as a presentation choice, not as a blueprint claim):

```
(36) unit cell Omega_cell = [0,L] x [0,L]
(37) lattice vectors a_alpha = L e_alpha
(38) reciprocal vectors b_alpha = (2 pi / L) e_alpha  (b_alpha . a_beta = 2 pi delta_alpha,beta)
     and the first Brillouin zone as the box |k_1| <= pi/L, |k_2| <= pi/L
(39) time-harmonic Bloch ansatz  u_i = Re[ uhat_i(x) e^{i (k.x - omega t)} ],  uhat lattice-periodic
(40) Bloch condition             u(x + a_alpha) = u(x) e^{i k . a_alpha}
(41) phase factor on grad u      u_i,j(x + a_alpha) = mu_alpha u_i,j(x)
(42) phase factor on d^2u/dx dy  u_i,xy(x + a_alpha) = mu_alpha u_i,xy(x)
(43) phase factor on all DOFs    D^m u(x + a_alpha) = mu_alpha D^m u(x), every multi-index |m| <= 2
                                 (value, u_,x, u_,y, u_,xy)
```

Out of M9 scope by the blueprint's own register: (44) IBZ path and k-sampling = M10 (TV4
unresolved); (45)–(47) non-dimensionalisation = M11; (53)–(61) element data = M13/M14; (62)–(71)
Bloch transformation, reduced matrices, eigenproblem, scaling/MAC = M15.

---

## M9.1 — Inherited setting and conventions (nothing re-assumed) `[S]`

| Object | Value used | Source |
|---|---|---|
| bulk operator | (O1) `sigma_ij,j - tau_ijk,jk = rho( u_i_ddot - ell^2 u_i_ddot,jj )` | M8; M8-a §4 |
| boundary model | (O2)–(O4): essential `u_i`, `u_i,nu`; natural `t_i^red = (sigma_ij - tau_ijk,k)n_j + rho ell^2 u_i_ddot,j n_j`, `R_i = n_j n_k tau_ijk`; (O5) four interface conditions/direction; (O6) periodic pairs with Bloch phase on value and derivative DOFs | M8-a (interpretation (A)) |
| time convention | `u(x,t) = Re[ uhat(x) e^{-i omega t} ]` ⇒ `u_i_ddot -> -omega^2 u_i` | M5/M8 |
| length tensor | `L = (A^T A)_rot`, generic `[[L11, L12],[L12, L22]]` in 2D | M2/M4, (26) |
| double stress | `tau_ijk = (1/10) L_kn C_ijpq eta_pqn` | M4, (16)–(18) |
| classical modulus | isotropic `C` of (13)–(15), plane-strain `C̄ = [[lam+2mu, lam, 0],[lam, lam+2mu, 0],[0,0,2mu]]` | M4 |

Extensional convention: the Wavenumber is **real** on the IBZ path and the field is the complex
representative (the physical field is its real part). The five constants a₁…a₅ are **not** used
anywhere in M9 (F1 audit); the anisotropic (26) is the model, as in M8.

---

## M9.2 — Unit cell, lattice, reciprocal lattice, first Brillouin zone: (36)–(38) `[A]`

**(S1) Unit cell (36).** Ω_cell = [0,L]×[0,L] has area L² and its four corners are exactly
`{0, a_1, a_2, a_1+a_2}`: it is a fundamental domain of the square Bravais lattice generated by
`a_1, a_2`. (Blueprint Sec 3.1.)

**(S2) Lattice vectors (37).** `a_1 = L e_1`, `a_2 = L e_2`; the Gram matrix is
`a_alpha · a_beta = L^2 delta_alpha,beta`, i.e. an orthogonal lattice with equal lattice constant
`L` — a **square** lattice, as the blueprint's IBZ `Γ–X–M–Γ` requires.

**(S3) Reciprocal vectors (38) — solved, not recalled.** The defining relations
`b_alpha · a_beta = 2 pi delta_alpha,beta` are a 2×2 linear system whose determinant is
`det Gram(a_1,a_2) = L^4 != 0`; hence the solution is unique and equals

```
b_1 = (2 pi/L) e_1 ,   b_2 = (2 pi/L) e_2 .
```

The **2π convention is forced by the blueprint's own data**: with the alternative convention
`b_alpha · a_beta = delta_alpha,beta` one would get `X = (1/(2L), 0)`, which differs from the
blueprint's `X = (pi/L, 0)` by `pi/L - 1/(2L) != 0`. There is therefore no convention ambiguity to
resolve here (recorded because the blueprint's register names the reciprocal vectors without
writing the defining relation).

**(S4) First Brillouin zone (38).** Two equivalent characterisations are verified:
`{|k·a_1| <= pi and |k·a_2| <= pi}  ⇔  {|k_1| <= pi/L and |k_2| <= pi/L}`. The Voronoi
(nearest-reciprocal-lattice-point) characterisation gives the same set: for every
`G = m b_1 + n b_2 != 0`,

```
|k - G|^2 - |k|^2 = |G|^2 - 2 k.G  >=  (4 pi^2/L^2)[ m^2 + n^2 - (|m| + |n|) ]  >=  0 ,
```

because `|m| + |n| <= m^2 + n^2` for every integer pair except `(0,0)` (equality for
`(±1,0), (0,±1)` — the four binding constraints — and also for `(±1,±1)`, which touch only the
corner points). The four binding constraints are exactly the box facets: for `G = b_1`,
`|k-b_1|^2 - |k|^2 = (2 pi/L)^2 - 2(2 pi/L) k_1 >= 0  ⇔  k_1 <= pi/L`, and likewise for the other
three nearest neighbours. Hence **the first BZ is the square `[-pi/L, pi/L]^2`** with
`Γ = (0,0)`, `X = b_1/2 = (pi/L, 0)`, `M = (b_1+b_2)/2 = (pi/L, pi/L)`, and `|X| = pi/L`,
`|M| = sqrt(2) pi/L`. The whole `Γ–X–M–Γ` path lies inside the first BZ (each leg is affine in
`t ∈ [0,1]`; `|k_i(t)|` is convex, hence bounded by its endpoint values `le pi/L`; a rational grid
corroborates). The triangle `Γ-X-M` has area `pi^2/(2L^2) = (1/8)·(4 pi^2/L^2)`, i.e. **1/8 of the
BZ area** — the irreducible Brillouin zone occupies 1/8 of the BZ for the square lattice (factor 8
= order of the point group). *The discretisation of the path and the number of k-points per segment
are M10 / TV4 and are not fixed here.*

**(S5) k is defined modulo the reciprocal lattice.** For `G = m b_1 + n b_2`,
`exp(i G·a_alpha) = 1`, hence `mu_alpha(k+G) = mu_alpha(k)`: both the Bloch condition (40) and the
tying `T(k)` are b-periodic in k. Restricting k to the first BZ is therefore a *definition* (no
information is lost), not an assumption, and `kbar = k L/pi` (M11) takes the values `(0,0)` at Γ,
`(1,0)` at X, `(1,1)` at M with the BZ equal to `{|kbar_1| <= 1, |kbar_2| <= 1}`.

**(S6) Real k.** For `k = k_r + i beta` one has `|exp(i k·a)| = exp(-beta·a)`, so a complex k means
a **non-unitary** tying (evanescent fields / complex band structure). The blueprint's band problem
uses real k on the IBZ path; complex-k attenuation is **out of scope** in Phase 1 and is recorded
as a scope statement, not as a TV item. For real k the phases are unimodular (used in M9.7).

---

## M9.3 — Bloch theorem and the derived phase rules: (39)–(43) `[A]`

**(T1) Ansatz (39).** `u_i(x,t) = Re[ uhat_i(x) e^{i(k·x - omega t)} ]` with a **lattice-periodic**
envelope `uhat_i(x + a_alpha) = uhat_i(x)`. Verified: (i) `d^2/dt^2 U = -omega^2 U`, i.e. the ansatz
carries the same `e^{-i omega t}` convention as M5/M8 — no sign freedom is introduced; (ii) the
envelope is periodic (checked on the Fourier basis of the periodic space).

**(T2) Bloch condition (40).** `u(x + a_alpha) = mu_alpha u(x)` with `mu_alpha = e^{i k·a_alpha}`.
The equivalence with (39) is **derived, not asserted**: with `uhat := u e^{-i k·x}` one has the
exact identity

```
(T4)  uhat(x+a) - uhat(x) = e^{-i k.x} ( u(x+a) e^{-i k.a} - u(x) )            [exact, generic u]
```

so "uhat lattice-periodic" ⇔ "(40) holds". Verified for a generic (non-Fourier) field `u(x,y)`. The
phase map `a -> e^{i k·a}` is a lattice homomorphism: `u(x+a_1+a_2) = mu_x mu_y u(x)` in either
order and `u(x+2a_1) = mu_x^2 u(x)`.

**(T3) The critical step, proved — the same phase factor on ∇u, on ∂²u/∂x∂y and on every
derivative DOF.** The phase factor `mu_alpha = e^{i k·a_alpha}` is **independent of x**
(`∂_j mu_alpha = 0`), so the lattice-translation operator commutes with `∂_j`; therefore

```
(41)  u_i,j(x + a_alpha) = mu_alpha u_i,j(x)          (all four Cartesian components)
(42)  u_i,xy(x + a_alpha) = mu_alpha u_i,xy(x)        (the mixed-derivative DOF)
(43)  D^m u(x + a_alpha) = mu_alpha D^m u(x)          (every multi-index |m| <= 3)
```

**No derivative correction term can appear** — the phase is one and the same for value, first and
mixed derivatives. This is the blueprint's requirement "derive this from the Bloch condition rather
than asserting it", discharged. The rule is **not vacuous**; four negative controls are exhibited
with their exact residuals:

| wrong variant | exact residual |
|---|---|
| phase on the value DOF only (`u_,x` tied with phase 1) | `(mu_x - 1) u_,x` |
| phase on `u_,x` but not on `u_,xy` | `(mu_x - 1) u_,xy` |
| opposite phase `mu_x^{-1}` | `(mu_x - mu_x^{-1}) u` |
| an extra constant factor `c != 1` | `(1 - c) mu_x u` |

**(T5) Operator covariance (equivalent formulation, used as a cross-check).** With
`u = uhat e^{i k·x}` the M8 time-harmonic operator satisfies, term by term and for both components,

```
O[u] = e^{i k.x} O_k[uhat] ,      O_k = O with  partial -> partial + i k ,
```

verified for each of the four structural contributions (classical `sigma_ij,j`; double stress
`-tau_ijk,jk`; mass `rho omega^2 u_i`; micro-inertia `-rho omega^2 ell^2 u_i,jj`) with the generic
anisotropic `L` of (26). The `partial -> partial - i k` variant **fails** on every envelope mode
with `q != 0`; on the **uniform** envelope `q = 0` the two variants coincide *identically*, because
the operator contains only 2nd and 4th derivatives (an even number of derivative factors) and is
therefore even in k at `q = 0`. *Consequence recorded for M15: any check of the k-shift sign must
use a non-uniform envelope.*

---

## M9.4 — DOF-level statement and the cell realisation `[A]`, `[S]`

**(D1) DOF-level rule.** The BFS element carries, per node and per component, the DOF set
`{u, u_,x, u_,y, u_,xy}`; 4 nodes × 2 components × 4 DOFs = **32 DOFs per cell** (blueprint Sec 4.1).
By (41)–(43) **all four types** of a node carry the same phase factor, so the tying block of a
periodic node pair is

```
(D2)  T_pair = mu_alpha I_8        (8 = 2 components x 4 DOF types),
```

i.e. a **diagonal complex phase matrix** — exactly the "T diagonal complex phase" of blueprint
Sec 4.4. This is the content of contribution C3 ("complex phase factor applied consistently to the
value *and* to all first- and mixed-derivative degrees of freedom").

**(D3) Edge and corner realisation.** With `mu_x = e^{i k_1 L}`, `mu_y = e^{i k_2 L}`:
right edge vs left edge → `mu_x`; top vs bottom → `mu_y`; the corner `(L,L)` is reached from
`(0,0)` by `a_1+a_2` (`mu_x mu_y`), from `(L,0)` by `a_2` (`mu_y`) and from `(0,L)` by `a_1`
(`mu_x`); the three relations compose consistently (the product around the cycle is 1) and act on
all 8 DOFs of the corner node. This is the DOF-level counterpart of the corner bookkeeping recorded
as **M8-a-1** (informational); M9 verifies only the phase content, not the corner-term signs.

**(D4) Counting illustration (single BFS cell).** The 4 nodes form exactly 4 Bloch equivalence
classes `{0, a_1, a_2, a_1+a_2}`; with 3 slave classes, `3 × 8 = 24` DOFs are tied and
`32 − 24 = 8` independent DOFs remain. *Shown for orientation only*: the general reduced DOF count
with the interior/edge/corner partition is blueprint (65), i.e. M15 scope; the mesh resolution
(TV7) is unresolved and is not fixed here.

---

## M9.5 — Consistency with the reduced four-quantity boundary model (M8-a) `[A]`

**(B1) The four operational quantities are phase-consistent.** `t_i^red` (O3) and `R_i` (O4) are
homogeneous of degree one in the field, so by (T3) they transform with the **same** `mu_alpha` at
translated points (translation preserves the outward normal of a face):

```
t_i^red(x+a) = mu_a t_i^red(x) ,      R_i(x+a) = mu_a R_i(x) .
```

Hence value DOFs, normal-derivative DOFs and natural data all use one and the same phase; **no
separate rule is needed for the boundary model** and none is introduced.

**(B2) M5-a — FULLY DISCHARGED.** The free micro-inertia boundary term of M5/M8,
`- rho omega^2 ell^2 u_i,j n_j`, (i) inherits `mu` from `u_i,j` and (ii) is conjugate to the **value
DOF** (M8 check C2 fixed that slot), which carries the same `mu`. Its discrete contribution
therefore involves no phase mismatch, and the obligation recorded by M5-a ("check the Bloch phase
on this term") reduces to the ordinary value-DOF tying of (T3). No residue remains.

**(B3) No silent switch to the exact Mindlin–Toupin operator.** The two terms that the exact
boundary operator adds — the tangential redistribution `d_s q_i` (`q_i = tau_ijk n_k m_j`) and the
corner/line force `e_i = [[q_i]]` — **also** carry the same `mu`: `d_s q_i` keeps `mu` because the
phase is x-independent (the derivative acts only on the master-side field), and the corner jump is
a sum of `±tau` components evaluated at one point. Verified explicitly, including the reproduction
of the four edge quantities of the M8-a audit ([A5]): with the oriented-tangent convention,
`q_i = +tau_i21` (right), `+tau_i21` (left), `-tau_i12` (top), `-tau_i12` (bottom) — recomputed
here independently from the M4 double stress. **Consequence: equations (39)–(43) are identical in
the reduced formulation (A) and in the exact operator; M9 commits to neither, and the operational
model of M8-a is neither changed nor re-opened.**

**(B4) Interface conditions are Bloch-covariant.** The four interface conditions of M8 (O5) —
`[u_i] = 0`, `[u_i,j n_j] = 0`, `[t_i^red] = 0`, `[R_i] = 0` — are pointwise and both layers carry
the same phase; each jump therefore transforms as `jump(x_I + a) = mu jump(x_I)`, so a vanishing
jump at an interface point implies a vanishing jump at every lattice translate. **No extra interface
phase factor is required** (bilayer Case C). The `C¹` continuity of the test/trial space, and hence
the essential pair of interface conditions, is untouched by the phase rule.

---

## M9.6 — Compatibility with (26), the M7 ladder, and the precondition `[A]`

**(26)-compatibility.** For the generic anisotropic `L = [[L11, L12],[L12, L22]]` (`L12 != 0`,
`L11 != L22`, i.e. `theta != 0`, `AR != 1`) with the isotropic classical `C̄`, the phase
equivariance is verified component by component: `eps(x+a) = mu eps(x)`, `eta(x+a) = mu eta(x)`,
`sigma(x+a) = mu sigma(x)`, `tau(x+a) = mu tau(x)` (epsilon and sigma: 4 components each;
eta and tau: 8 each), for both lattice vectors and
several envelope modes. The negative control `tau(x+a) = tau(x)` (phase removed) fails, so the phase
is not removable. **No isotropy of `L` is used or needed anywhere in M9.**

**Isotropic member `L = ell_L^2 I`.** `tau_ijk = (1/10) ell_L^2 C_ijpq eta_pqk` for every
component, and the phase rules are unchanged: the phase factor's free symbols are exactly
`{k_1, k_2, L}` and contain **no** material parameter (`lambda, mu, rho, ell, omega, L11, L12, L22,
ell_L`). The Bloch formulation is therefore parameter-free — as it must be, being kinematic.

**Ladder invariance (M7, blueprint (27)–(30)).** All four specialisations leave (39)–(43) unchanged:
(i) classical (`L -> 0`, `ell -> 0`); (ii) `AR = 1` (isotropic length tensor); (iii) no
micro-inertia (`ell -> 0`); (iv) `theta -> theta + 90°` with `l1 <-> l2`. Only the operator being
reduced changes; the Bloch structure does not.

**Precondition (stated explicitly).** The phase rules require the constitutive data (`C`, `rho`,
`L`) to be **lattice-periodic**. Verified both ways: with a lattice-periodic modulation
`g(x) = 1 + g_per cos(2 pi x/L)` the equivariance `sigma(x+a) = mu sigma(x)` still holds exactly,
whereas with a non-periodic (graded) modulation it fails by exactly
`mu (C:eps) g_slope`. Case H (homogeneous) and Case C (bilayer cell) both satisfy the precondition;
a functionally graded or random microstructure would not, and would need a different (non-Bloch)
treatment. This is implicit in the blueprint's "periodic contrast (Case C)"; M9 states it.

---

## M9.7 — Dimensions and symmetry of every M9 object `[A]`

Basis `(kg, m, s)`. Dimension vectors written as `(kg, m, s)`.

| Object | Dimension | Symmetry / property |
|---|---|---|
| `k_i` (real, on the IBZ path) | `(0,-1,0)` | `1/m`; real |
| `a_alpha` | `(0,1,0)` | `m`; `a_alpha·a_beta = L^2 delta` |
| `k·a_alpha`, `kbar` | `(0,0,0)` | dimensionless; `∂_j (k·a) = 0` |
| `b_alpha` | `(0,-1,0)` | `1/m`; `b_alpha·a_beta = 2 pi delta` |
| `mu_alpha` | `(0,0,0)` | dimensionless, unimodular for real k, `mu_alpha(-k) = conj(mu_alpha(k)) = 1/mu_alpha(k)` |
| `T(k)` (tying) | `(0,0,0)` | diagonal unitary, `T(-k) = T(k)^H`, `T^H T = I` |
| `T_pair` | `(0,0,0)` | `mu_alpha I_8`, diagonal |
| `K̄, M̄` (reduced) | as `K`, `M` | Hermitian for real k; `K̄(-k) = conj(K̄(k))` (see M9.8) |

No dimension mixing is possible: every M9 object is dimensionless except `k`, `b` (1/m) and
`a` (m), and the two BZ inequalities `|k_i| <= pi/L` are dimensionally consistent.

**Phase lemma (the operative statement for M15) `[A]`.** For a **real symmetric** `K` and a tying
built from the Bloch phases (diagonal, unimodular):

```
(P1)  Kbar(-k) = conj(Kbar(k))                    [always]
      Kbar^H = Kbar                                [always, Hermitian]
      ⇒  charpoly(Kbar(k)) = charpoly(Kbar(-k))    ⇒  omega_n(k) = omega_n(-k), v_g odd
```

Verified exactly on the minimal model (3 nodes, one periodic pair; the verified reduced matrix is
`K̄ = [[a+e+2d cos theta, b+f e^{-i theta}],[b+f e^{+i theta}, c]]`). This is what an eigenproblem
needs: real eigenvalues and the physical k-symmetry. **M9 supplies the phase lemma; the assembled
proof for the actual `K`, `M` is M15's obligation ((66)–(68)).**

---

## M9.8 — FORWARD-FLAGGED FINDING: blueprint (68) and the Sec 4 pitfall test `[S]`, `[A]`
### *(M15 scope — recorded, documented, NOT repaired; requires a ruling before M15)*

**What the blueprint says** (verbatim, lines 403, 416, 587):

- Sec 4.5 row: "**Reduced Hermitian eigenproblem** `[K̄(k) − ω̄² M̄(k)] d̄ = 0`; **prove
  K̄(k) = K̄(−k)^H**; solver choice and the number of lowest bands extracted." → (66)–(68).
- Register (66)–(68): "Reduced Hermitian eigenproblem; `K̄(k) = K̄(−k)^H`".
- Pitfalls table: "**Non-Hermitian K̄** | Wrong sign of the phase on the derivative DOFs. Test
  `||K̄(k) − K̄(−k)^H|| / ||K̄|| < 1e−12` on every run."

**What is provable (M9 phase lemma, verified).** For the tying route that the blueprint itself
prescribes in Sec 4.4 (`d_slave = T(k) d_master`, `T` diagonal phase, phases = the ones derived in
M9.3) and a real symmetric `K`, one gets **always** `K̄^H = K̄` and `K̄(−k) = conj(K̄(k))`, hence
`K̄(−k)^H = conj(K̄(k)) = K̄(k)^T`. Consequently the literal claim (68) is **exactly equivalent to
"K̄(k) is real (real symmetric)"** — an extra condition, not a consequence of the formulation.

**Exact counterexamples (both verified symbolically in this module).**

1. 1D, two elements, three nodes, one periodic pair `c_2 = mu c_0`, `K` real symmetric with entries
   `a, b, c` (diagonal) and interior couplings `d` (master↔slave) and `f` (interior↔slave):

   ```
   Kbar(k) - Kbar(-k)^H = 2 i Im(Kbar_12) [[0,-1],[1,0]]  =  -2 i f sin(theta) [[0,-1],[1,0]]
   ```

   non-zero whenever `f sin(theta) != 0`; `K̄` is real ⇔ `f sin(theta) = 0`. The violation is
   **O(1)**, not a tolerance effect: with `a=c=e=b=f=1`, `theta = pi/2` one gets
   `Kbar = [[2, 1-i],[1+i, 1]]`, `||Kbar||_F^2 = 9` against `||Kbar - Kbar(-k)^H||_F^2 = 8`, i.e. a relative violation
   `2 sqrt(2)/3 = 0.943` against a required `1e-12`.
2. With the DOF-type structure of the `C¹` cell (a value DOF and a derivative DOF, each coupled to
   its image class): `K̄ − conj(K̄) = 2 i (K_{14} − K_{32}) sin(theta) [[0,1],[-1,0]]`, so realness
   requires the accidental degeneracy `K_{(0,type1),(1,type2)} = K_{(1,type1),(0,type2)}`, which
   real symmetry does **not** provide (symmetry pairs `K_ij` with `K_ji`, not with `K_i'j'`).

**Route diagnosis (why the claim exists).** (68) *is* true for the **other** mathematically
equivalent route — the envelope / k-shift formulation, whose reduced matrix is **complex
symmetric**, `K_e = K_0 + i k K_1 + k^2 K_2` with all real symmetric `K_i`: then
`K_e(k) = K_e(−k)^H` holds identically (verified) — **but that matrix is not Hermitian**
(`K_e − K_e^H = 2 i qk E2 [[0,1],[-1,0]] != 0`), so the "Hermitian eigenproblem" of Sec 4.5 fails
in that route. The two statements of Sec 4.4/4.5 therefore cannot both be asserted of one matrix:
(68) is the complex-symmetric-route property, Hermiticity is the tying-route property. The blueprint
prescribes the tying route (§4.4) and calls the problem Hermitian (§4.5) — with those two, (68)
must be replaced by the pair `K̄^H = K̄` and `K̄(−k) = conj(K̄(k))`, which give the same physical
statements (`omega_n(k) = omega_n(−k)`, real eigenvalues).

**Second, independent consequence of the same analysis (detectability).** If the phase *sign* on the
derivative DOFs is wrong (value DOF with `mu`, derivative DOF with `mu^{-1}`), the wrong reduced
matrix is **still Hermitian, still satisfies `K̄(−k) = conj(K̄(k))`, still has `omega(k) = omega(−k)`**,
yet differs from the correct one by a non-zero amount (all verified). So:
(i) the pitfalls row's stated cause ("Non-Hermitian K̄" from a wrong phase sign) is not the
mechanism — a unimodular (wrong-sign) phase keeps `K̄` Hermitian; and (ii) the proposed test
`||K̄(k) − K̄(−k)^H||/||K̄|| < 1e−12` **fails for a correct tying implementation as well** (by
counterexample 1), while it does not isolate the stated error. **No internal invariance test of the
listed kind can detect a unimodular phase error on the derivative DOFs**; only comparison with an
independent reference can — the analytic Case-H / 1D dispersion already planned as Phase-2 tasks
P2.1/P2.2, or the Phase-3 published anchors. *This is a QA-design statement about which test can
detect which error; it adds no new workstream (the reference comparisons are already in the
approved plan) and it does not modify any blueprint equation.*

**What has NOT been done (deliberate).** No blueprint edit; no change to (66)–(68); no change to any
M1–M8 result; no replacement of the test by another test; no assumption that the blueprint is wrong
in intent. The equations as written are left exactly as they are.

**Ruling required (recorded as M15-a, status TO BE VERIFIED).** One of the following needs the
user's decision before M15 is derived/implemented: (a) restate (68) as the pair of general
relations (`K̄^H = K̄`, `K̄(−k) = conj(K̄(k))`) and re-base the Sec 4 test on them; (b) keep (68)
literally, accepting that it presupposes realness of the reduced matrices and will have to be
"proved" only under the accidental degeneracy that real symmetry does not supply; or (c) defer the
question to M15 with the test replaced by the Hermiticity + conjugation pair plus the reference
checks of P2.1/P2.2/Phase 3. **M9 does not choose between these.**

---

## M9.9 — Module notes (ambiguities, gaps, conventions) `[S]`

- **M9-a (routes).** Two mathematically equivalent formulations exist: (R1) DOF tying with the
  diagonal phase `T(k)` (blueprint Sec 4.4 — **selected**, and the route on which (39)–(43) act),
  and (R2) the envelope substitution `u = uhat e^{i k·x}` with `partial -> partial + i k`
  (verified equivalent at the operator level, (T5)). They are NOT interchangeable at the level of
  "what the DOFs mean": in (R1) the constrained vector is the full-field DOF vector, in (R2) it is
  the envelope vector, and mixing the two (e.g. importing the `i k` terms into a tying-route
  assembly) would double-count the phase. The blueprint is explicit (§4.4 diagonal `T`), so this is
  a **noted hazard, not an ambiguity**. M15 must state which route it implements.
- **M9-b (sign coupling).** With `e^{-i omega t}` the spatial factor is `e^{+i k·x}` and the phase
  is `e^{+i k·a}`. This is fixed by the ansatz (T1) and matches the blueprint's own (40). The
  opposite choice would merely map `k -> -k` in (40); the blueprint's (40) is unambiguous, and the
  physically reported quantity that is sensitive to it is `v_g` (not the band frequencies, which are
  even in k — see (P1)). Recorded as a convention, not an ambiguity.
- **M9-c (normal-derivative basis).** The Cartesian DOFs always carry `+mu`; the
  normal-derivative quantities pick up a relative `−1` on the opposite face,
  `u_{i,nu}(x=L) = −mu_x u_{i,nu}(x=0)` and likewise for the mixed normal–tangential derivative,
  because the outward normal flips. The blueprint's BFS DOF set is Cartesian, so **its Sec 4.4
  tying carries no sign**; the sign appears only if the tying is re-expressed in the
  normal-derivative basis (relevant to the essential DOF `u_{i,nu}` of (O2)). This fills a
  definitional gap and is the precise content of the Sec 4 phrase "phase sign on derivative DOFs".
- **M9-d (precondition).** Lattice periodicity of `C`, `rho`, `L` (M9.6) is implicit in the
  blueprint's "periodic contrast"; stated explicitly here.
- **M9-e (scope).** Complex k / evanescent waves: out of scope (S6). k-point sampling: M10/TV4.
  Non-dimensionalisation: M11. No numerical parameter value is used anywhere in M9.
- **M9-f (equation allocation).** The individual content of (41)–(43) is not enumerated in the
  blueprint (Sec 3.2 states it collectively); the allocation of M9.0 is the natural reading and is a
  presentation choice `[S]`, not a claim about the blueprint.
- **M9-g (QA remark).** At the uniform envelope `q = 0` the k-shift sign is unobservable (T5); any
  test of it must use `q != 0`. Related: M15-a above.
- **M15-a (new, forward).** The Sec 4.5/(68) finding of M9.8 — status TO BE VERIFIED, ruling
  required before M15, no repair applied.

---

## M9.10 — Checks actually performed (45, all executed, all PASSED)

| # | Check | Type | Result |
|---|---|---|---|
| [L1] | cell = fundamental domain; corners = lattice points | structure | PASSED |
| [L2] | `a_alpha·a_beta = L^2 delta` (square lattice) | algebra | PASSED |
| [L3] | `b_alpha` solved from `b_alpha·a_beta = 2 pi delta` (⇒ `(2pi/L) e_alpha`) | derivation | PASSED |
| [L4] | uniqueness of `b_alpha` (Gram determinant `L^4 != 0`) | algebra | PASSED |
| [L5] | 2π convention forced by the blueprint's own `X` | consistency | PASSED |
| [L6] | `{|k·a_alpha| <= pi} ⇔ {|k_i| <= pi/L}` | algebra | PASSED |
| [L7a] | Voronoi identity `|k−G|² − |k|² = |G|² − 2k·G` | algebra | PASSED |
| [L7b] | box ⇒ Voronoi inequality for every `G`; binding facets = `±b_1, ±b_2` | derivation | PASSED |
| [L7c] | diagonal `G` touches only the corners; equality set = 8 pairs | algebra | PASSED |
| [L8] | Γ, X, M coordinates, lengths, equidistance (BZ boundary) | structure | PASSED |
| [L9] | whole `Γ–X–M–Γ` path inside the BZ (endpoints + convexity + grid) | geometry | PASSED |
| [L10] | IBZ triangle = 1/8 of the BZ area | geometry | PASSED |
| [L11] | k modulo the reciprocal lattice (`mu_alpha(k+G) = mu_alpha(k)`) | symmetry | PASSED |
| [L12] | `kbar` consistency (Γ, X, M values; BZ as `|kbar_i| <= 1`) | dimensions | PASSED |
| [L13] | real k ⇔ unimodular tying; complex k ⇒ `e^{-beta·a}` (scope) | scope/sign | PASSED |
| [B1] | (39)+(40): `d²/dt² U = −omega²U`; periodic envelope; Bloch condition | sign/derivation | PASSED |
| [B2] | (39) ⇔ (40) for a generic field (exact identity) | equivalence | PASSED |
| [B3] | phase map is a lattice homomorphism (both orders, `2a_1`) | symmetry | PASSED |
| [B4] | (41) ∇u rule, all 4 components, several modes, both components | derivation | PASSED |
| [B5] | (42) mixed derivative `u_,xy` | derivation | PASSED |
| [B6] | (43) all multi-indices `|m| <= 3` | derivation | PASSED |
| [B7] | four negative controls with exact residuals | non-vacuity | PASSED |
| [B8] | critical step proved (`∂_j mu = 0`; envelope route; `+ik` sign) | derivation/sign | PASSED |
| [B9a] | operator covariance `O[u] = e^{ikx} O_k[uhat]`, 4 terms, 3 modes, 2 components | operator | PASSED |
| [B9b] | k-shift sign control; `q = 0` degeneracy recorded | sign/non-vacuity | PASSED |
| [B10] | 32 DOF/cell; `T_pair = mu_alpha I_8` diagonal | structure | PASSED |
| [B11] | corner triple identification consistent (cycle product 1) | consistency | PASSED |
| [B12] | equivalence classes and tied-DOF arithmetic (illustration) | structure | PASSED |
| [C1] | (26)-compatibility: `eps, eta, sigma, tau` equivariance, generic anisotropic `L` | anisotropy | PASSED |
| [C2] | isotropic member `L = ell_L² I`; phase factor parameter-free | limit/dimensions | PASSED |
| [C3] | ladder invariance (4 M7 rungs) | limit | PASSED |
| [C4] | (O3)–(O4) `t_i^red`, `R_i` equivariance | boundary model | PASSED |
| [C5] | M5-a discharged (phase + conjugate DOF) | consistency | PASSED |
| [C6a] | edge quantities `q_i` reproduce M8-a [A5]; phase on parallel faces | cross-module | PASSED |
| [C6b] | exact-operator terms (`d_s q_i`, `[[q_i]]`) carry the same phase — no silent switch | scope | PASSED |
| [C7] | interface conditions Bloch-covariant (4 jumps) | boundary model | PASSED |
| [C8] | Γ/X/M exact phases; `mu_y = 1` on `Γ–X` (M8-a-1 consistency) | cross-module | PASSED |
| [C9] | normal-derivative vs Cartesian DOF signs on opposite faces | sign | PASSED |
| [C10] | unimodularity; `T(−k) = T(k)^H`; `T` unitary | symmetry | PASSED |
| [C11] | phase lemma: Hermitian, conjugation, charpoly invariance (model) | derivation | PASSED |
| [C12] | periodic-coefficient precondition (periodic vs graded modulus) | precondition | PASSED |
| [X1] | literal (68) ⇔ `K̄` real; exact counterexample; O(1) violation | **flag** | PASSED (claim refuted) |
| [X2] | DOF-type counterexample; realness ⇔ accidental degeneracy | **flag** | PASSED (claim refuted) |
| [X3] | route diagnosis: (68) holds in the complex-symmetric route only | **flag** | PASSED |
| [X4] | unimodular phase-sign error is invisible to all listed invariants | **flag** | PASSED |

Provenance of "PASSED (claim refuted)": the check verifies a **negative** statement — that the
literal blueprint claim does not follow — and the verification itself succeeded. No blueprint
statement was modified.

---

## M9.11 — What M9 does NOT do (forward obligations, unchanged)

- **M10**: IBZ path discretisation and k-points per segment (44) — TV4 unresolved, not guessed.
- **M11**: non-dimensionalisation (45)–(47); M9 uses only the internal consistency `kbar = kL/pi`.
- **M13/M14**: BFS shape functions, `B`, `B_,i` (53)–(56), element matrices (57)–(61). M9 fixes only
  which DOFs carry the phase.
- **M15**: Bloch transformation `T(k)` assembly, reduced matrices (62)–(65), the reduced DOF count for
  a general mesh, the eigenproblem (66)–(68), Jacobi scaling, κ, MAC tracking (69)–(71). M9 supplies
  the phase lemma (P1) and the DOF-level rule (D1)–(D3); it does NOT assemble, solve or post-process
  anything.
- **M15-a**: the (68)/test ruling of M9.8 — pending the user's decision.
- No numerical solver code, no mesh, no material parameter, no published validation, no band
  structure, no test 5a–5i, no TV resolution, no blueprint edit, no change to M1–M8 mathematics.
