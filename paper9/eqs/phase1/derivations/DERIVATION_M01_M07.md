# PHASE-1 DERIVATION AND MATHEMATICAL-AUDIT RECORD — MODULES M1–M7

Status: **IN PROGRESS (Phase 1)** — modules M1–M7 complete at symbolic level (checks PASSED);
M8–M17 NOT STARTED. Phase 0 is LOCKED (main @ 175ea9e); no scientific PASS is claimed.

Governing inputs (read-only):
- Blueprint v1.3, `paper9/plan/blueprint/Paper9_Blueprint_v1.3.tex`
  (sha256 `ca71b91aba4ca4abe9f157eb595ac8c2f709d838957a08ea0dce7160685dbf9f`), §2–§4,
  EQUATION REGISTER (1)–(71), (A.1)–(A.6), (B.1)–(B.8).
- `paper9/plan/CALC_MASTER_PLAN.md` v1.1 §A (dependency map M1–M17).
- Legacy [C] sources, quoted by equation number: `femcheck/FEM_Total/ptxt/FEM_1_Paper.txt`
  (ellipsoidal averaging, Eqs (2)–(12), (16)–(18)), `FEM_2_Paper.txt` (Eq (33)),
  `FEM_3_Paper.txt` (§3.3 Eqs (15)–(19), (23)–(26); Eqs (84)–(85) discussed in note F1).

Provenance tags: `[C]` canonical/published · `[A]` analytical derivation (this work) ·
`[S]` study/design choice. Every equation below states its tag, assumptions, the checks
performed, and the script/log that produced them.

Reproduce:

```
cd paper9/eqs/phase1
python3 scripts/m01_m02_length_tensor.py     # M1, M2   (19 checks)
python3 scripts/m03_kinematics.py            # M3       ( 9 checks)
python3 scripts/m04_form2_constitutive.py    # M4       (20 checks)
python3 scripts/m05_micro_inertia.py         # M5       ( 7 checks)
python3 scripts/m06_energy_definiteness.py   # M6       (11 checks)
python3 scripts/m07_limit_ladder.py          # M7       (10 checks)
```

All scripts are deterministic, use SymPy exact arithmetic, take no numerical parameter
values (all material/geometry quantities are symbols), and write no files.

Notation mapping (blueprint ↔ legacy): `l1,l2,l3` ↔ `a1,a2,a3` (FEM_1/FEM_2 semi-axes);
`(A A^T)_mn` = `L_mn`; `eta_ijk = eps_ij,k` ↔ `G_ABC`; `tau_ijk` ↔ `q_ijm` (FEM_1) / `Sigma_IJK`
(FEM_3); `ell_i` = scalar micro-inertia length (see note N-1).

---

## M1 — Ellipsoidal averaging domain and characteristic-length tensor  (blueprint (1)–(4)) `[C]+[A]`

**Objects.** Averaging neighbourhood `V = { xi : sum_i xi_i^2/l_i^2 <= 1 }` with semi-axes
`l1,l2,l3 > 0`, `|V| = (4 pi/3) l1 l2 l3`, uniform kernel `p(xi) = 1/|V|` (blueprint (1)–(2)).
Affine map from the unit ball `xi = A u`, `A = diag(l1,l2,l3)`, `dV_xi = det(A) dV_u`
(blueprint (3)).

**Derivation.**
1. Unit-ball moments, computed by explicit spherical integration (exact):
   `(1/|V_ball|) int u_i u_j dV = (1/5) delta_ij` and all first/odd moments vanish.
   Checks: `u1^2 = u2^2 = u3^2 = 1/5`, `u1 u2 = 0`.
2. Push forward with the volume element `det A`: `(1/|V|) int_V xi_i xi_j dV =
   (1/5) (A A^T)_ij`, i.e. `(A A^T)_mn = l_m^2 delta_mn` in principal axes
   (blueprint (3)–(4)). Verified as a full 3x3 identity (the earlier version of this check
   that omitted `det A` failed — the volume element is essential; log recorded).
3. Weakly nonlocal average of a Taylor-expanded strain field
   `eps(x+xi) = eps + xi_i eps,_i + (1/2) xi_i xi_j eps,ij + O(|xi|^3)` gives, because the
   kernel is uniform and the domain centrosymmetric (odd moments vanish),
   `eps_tilde = eps + (1/10) (A A^T)_ij eps,ij + O(l_max^4 grad^4 eps)`,
   with `1/10 = (1/2) x (1/5)` — verified exactly for a generic quadratic field
   (blueprint (2), (7)-class identity; FEM_1 Eq (7)).

**Assumptions (explicit).** (a) small strain, smooth field; (b) weakly nonlocal regime
`l_max << L_eps`; (c) `V ⊂ Omega`, i.e. no boundary truncation of the neighbourhood (bulk
approximation, FEM_1 discussion); (d) uniform kernel; (e) ellipsoid axes = principal axes of
the fabric tensor. All are inherited from the blueprint/locked model; none is added here.

**Dimensional audit.** `[l_i] = m`, `[(A A^T)] = m^2`, `[1/10] = 1`, `[eps,ij] = 1/m^2`, so
`(1/10)(A A^T)_ij eps,ij` is dimensionless — consistent with `eps_tilde`.

**Recorded choice.** The 3D coefficient `1/10` is retained in the plane-strain reduction; a
1D segment would give `1/6` and a 2D ellipse `1/8` (FEM_1). Using `1/10` is the `[C]`
choice of the legacy model and the blueprint; it is a model decision, not a derivation.
**No TV item is required by M1.**

---

## M2 — Orientation of the length tensor  (blueprint (5)–(9), part of (25)) `[C]+[A]`

**Derivation.**
1. `R(theta)` = rotation about `z` (blueprint (5)); verified `R^T R = I`, `det R = 1`.
2. `(A A^T)_rot = R^T diag(l1^2,l2^2,l3^2) R` (blueprint (6)) with explicit components
   `L11 = l1^2 cos^2 + l2^2 sin^2`, `L12 = (l2^2 - l1^2) cos sin`,
   `L22 = l1^2 sin^2 + l2^2 cos^2`, `L33 = l3^2`, `L13 = L23 = 0` (blueprint (7)–(8)).
3. The operator `L_ell = (A A^T)_rot,ij d^2/dx_i dx_j` therefore carries a **mixed term
   `2 L12 d^2/dx1 dx2`**; verified by expanding the quadratic form `xi^T (A A^T)_rot xi`
   (factor 2 explicit), and `L12` vanishes only if `theta ∈ {0, 90°}` or `l1 = l2` — the
   mixed derivative is precisely the anisotropy mechanism (blueprint (7)).
4. In-plane closed form `g^2_22(theta) = L22/5 = (l1^2 sin^2 + l2^2 cos^2)/5`
   (blueprint (9)) equals FEM_2 Eq (33) under `a_i <-> l_i` (notation mapping only).
5. Eigenvalue invariance (blueprint (25), used by §2.6): the characteristic polynomial of
   `(A A^T)_rot` equals `(x - l1^2)(x - l2^2)(x - l3^2)` for all `theta`; hence positive
   definiteness is orientation-independent (in-plane block: trace `= l1^2 + l2^2 > 0`,
   determinant `= l1^2 l2^2 > 0` for `l_i > 0`).
6. `theta -> theta + 90°` with `l1 <-> l2`: full-matrix identity verified
   (`(A A^T)_rot(theta+90; l1,l2) = (A A^T)_rot(theta; l2,l1)`), hence
   `g^2_22(theta+90; l1,l2) = g^2_22(theta; l2,l1)` (blueprint (30), see note M7-b for the
   spectrum-level caveat).

**Dimensional audit.** `[(A A^T)_rot] = m^2`, `[g^2_22] = m^2`.
**No TV item is required by M2.**

---

## M3 — Kinematics  (blueprint (10)–(12)) `[C]+[A]`

**Derivation and checks.**
1. `eps_ij = (1/2)(u_i,j + u_j,i)` symmetric by construction (blueprint (10)).
2. `eta_ijk = eps_ij,k` symmetric in `(i,j)` for every `k` (blueprint (11)); compatibility
   `eta_ijk,l = eta_ijl,k` (mixed partials commute) verified.
3. Plane strain `(u1(x1,x2), u2(x1,x2), 0)`: `eps_13 = eps_23 = eps_33 = 0` and every `eta`
   component carrying the index `3` vanishes.
4. Component counts (blueprint (12)): 3D strain map `u_i,j -> eps_ij` has rank 6
   (antisymmetric part is the kernel); 3D `{u_k,ij} -> eta` map has rank 18. In-plane plane
   strain: 3 independent strain components `{eps_11, eps_22, eps_12}` and 6 independent
   strain-gradient components `{eta_111, eta_221, eta_121, eta_112, eta_222, eta_122}`,
   verified by the rank of the explicit 6x6 second-derivative map (rank 6).

**Assumptions.** Small strain; no couple-stress/micropolar kinematics; plane strain
(`eps_33 = 0` imposed kinematically — note `sigma_33 = lambda(eps_11+eps_22) != 0`, verified in
M4: this is plane *strain*, not plane stress).

**Dimensional audit.** `[eps] = 1`, `[eta] = 1/m`.
**No TV item is required by M3.**

---

## M4 — Mindlin Form-II constitutive relations  (blueprint (13)–(18)) `[C]+[A]`

**1. Cauchy stress (blueprint (13)–(15)).** `sigma_ij = C_ijkl eps_kl` with
`C_ijkl = lambda delta_ij delta_kl + mu (delta_ik delta_jl + delta_il delta_jk)` — verified
identically equal to `lambda delta_ij eps_kk + 2 mu eps_ij`.
**Plane-strain reduction (blueprint (18)).** With `eps_33 = eps_13 = eps_23 = 0` the reduced
modulus on the pair ordering `(11,22,12)` is
`C_bar = [[lambda+2mu, lambda, 0], [lambda, lambda+2mu, 0], [0, 0, 2 mu]]` (verified
symbolically). Convention: the shear entry is written with `eps_12` (not `gamma_12 = 2 eps_12`);
see note F2 — this convention propagates to the mass/gradient matrices in M14 and must be
carried explicitly.

**2. Double stress and sixth-order modulus (blueprint (16)–(17), (26)).** The implemented
model is the *factorized* Form-II modulus
`D_ijm|kln = (1/10) L_mn C_ijkl`, i.e. `tau_ijk = (1/10) L_mn C_ijkl eta_kln`, which is exactly
FEM_1 Eq (17) (`q_ijm = (1/10) L_mn C_ijkl eps_kl,n`) and the modulus implied by the
anisotropic stiffness of blueprint (26). Derived and verified here `[A]`:
- `dW/dn_ijk = (2 - delta_ij) x (1/10) L_kn C_ijrs eta_rsn`, i.e. the tensor double stress
  `tau_ijk` times the symmetric-pair multiplicity `c_ij = 2 - delta_ij` (see note F2);
- Form-II minor symmetries: `tau_ijk = tau_jik` (FEM_3 Eq (24)); modulus symmetries
  `D_ijm|kln = D_jim|kln`, `= D_ijn|klm` (gradient pair, since `L = L^T`) and the major
  symmetry `D_ijm|kln = D_kln|ijm` (Hessian symmetry of the energy);
- plane-strain 6x6 modulus (ordering `(11,22,12) x (1,2)`) is symmetric (major symmetry).

**3. Relation to the five-constant isotropic basis (blueprint (16)–(18)) `[A]` — main Phase-1
result of M4.** With the FEM_3 Eq (18) invariant basis
`Psi_g = a1 eta_ABB eta_ACC + a2 eta_AAC eta_CBB + a3 eta_AAC eta_BBC + a4 eta_ABC eta_ABC +
a5 eta_ABC eta_CBA`, the five invariants are linearly independent (rank 5, verified), so the
coefficients of any member of the family are unique. The **isotropic-length limit of the
implemented (blueprint (26)) model is exactly and uniquely**
```
(a1, a2, a3, a4, a5) = (0, 0, lambda l^2/20, mu l^2/10, 0)        [L = l^2 I]
```
(solved symbolically by exact linear algebra; no numerical values involved). Equivalently, the
implemented anisotropic gradient energy is *outside* the isotropic five-constant family when
`l1 != l2`: for the test field `eta_111 = 1` rotated by `cos = 3/5, sin = 4/5` the rotation
difference of `W_g` factors as `-4 (l1-l2)(l1+l2)(lambda+2mu)/125` (a test-field diagnostic,
not a physical result), while all five invariants are exactly rotation-invariant.

**4. Positive definiteness (blueprint (22)–(24)).** In plane strain
`M6 = (1/10) L_bar (x) C_bar` (Kronecker, verified symbolically) with
`L_bar = diag(l1^2, l2^2)`; hence `M6` is positive definite iff `L_bar` is PD (`l_i > 0`) and
`C_bar` is PD (`mu > 0`, `lambda + mu > 0`; verified: leading minors `lambda+2mu`,
`det C_bar = 8 mu^2 (lambda+mu)`). This is the *exact* PD criterion for the implemented model.

**5. Dimensional audit.** `[C] = Pa`, `[L] = m^2`, `[D] = [a_p] = Pa m^2` (matches FEM_3
Eq (19)), `[tau] = Pa m`, `[sigma] = Pa`, `[eta] = 1/m`.

**Recorded finding — see note F1** (five-constant convention; FEM_3 Eqs (84)–(85)).

---

## M5 — Micro-inertia  (blueprint (19)–(21)) `[C]+[A]`

**Derivation.**
1. Kinetic energy density (blueprint (19))
   `T = (1/2) rho u_i_dot u_i_dot + (1/2) rho ell_i^2 u_i_dot,j u_i_dot,j`.
2. Variational treatment: `delta int T dt = - int [ rho u_i_ddot delta u_i +
   rho ell_i^2 u_i_ddot,j delta u_i,j ] dt` (integration by parts in time, zero endpoint
   variations); spatial integration by parts of the second term gives the inertial virtual-work
   density `- rho (u_i_ddot - ell_i^2 u_i_ddot,jj)` (blueprint (20)) plus the boundary term
   `- contour rho ell_i^2 u_i_ddot,j n_j delta u_i` (natural data: normal derivative of the
   acceleration, see note M5-a).
   The 1D integration-by-parts identity was verified exactly on generic polynomials
   (`int f'' g = -int f' g' + [f' g]`), and the resulting operator checked by substitution.
3. Time-harmonic reduction with the **fixed convention** `u = Re[ u_hat(x) e^{-i omega t} ]`
   (so `u_ddot = -omega^2 u`): `rho(u_ddot - ell^2 u_ddot,jj) = -omega^2 rho(u_hat - ell^2
   u_hat,jj)`, giving the weak form `omega^2 [ int rho u_hat delta u_hat + ell^2 int rho
   u_hat,j delta u_hat,j ]`, i.e. `M = M0 + ell^2 M^g` (blueprint (60)–(61)) — sign
   bookkeeping verified symbolically.
4. Limits used in the ladder (M7): the inertial operator bounds the phase velocity
   (blueprint (20), (A-class)) — structural check in M7(iii); full proof in M16.

**Assumptions.** Micro-inertia is isotropic with a single scalar length `ell_i` (see note N-1);
`rho` constant within each phase; the micro-inertia term is the only higher-order inertial term.

**Dimensional audit.** `[rho] = kg/m^3`, `[rho u_ddot] = kg/(m^2 s^2) = Pa/m` (matches
`[sigma_ij,j]`), `[rho ell^2 u_ddot,jj] = kg/(m^2 s^2)` (same), `[T] = J/m^3`.
**No TV item is required by M5** (`ell_i` stays symbolic; its production value is a Phase-4/5
input, TV6-adjacent).

---

## M6 — Strain energy, positive definiteness, anisotropic `K_g`  (blueprint (22)–(26)) `[A]`

**1. Energy decomposition (blueprint (22)).** `W = (1/2) C_ijkl eps_ij eps_kl +
(1/20) L_mn C_ijkl eps_ij,m eps_kl,n`, verified consistent with the `(1/10) L (x) C` modulus:
`W_g = (1/2) tau_ijk eta_ijk` identically.

**2. Positive definiteness.**
- Implemented model: plane-strain regrouping verified exactly
  `W_g = (1/20) sum_mn L_mn q_m^T (D_c C_bar) q_n` (out-of-plane `eta = 0`), with `q_m` the
  strain-pair vector at gradient index `m` and `D_c = diag(1,1,2)` (note F2). Since `L` and
  `D_c C_bar` are PD, `W_g >= 0` with equality iff `eta = 0`.
- General five-constant family (blueprint (22)–(24), FEM_3 Eq (18)): the three exact
  identities below were verified symbolically (with `t_A = eta_ABB`, `v_C = eta_AAC`):
  `T1 T3 - T2^2 = (1/2) sum_AB (t_A v_B - t_B v_A)^2 >= 0`,
  `T4 + T5 = (1/2) sum (eta_ABC + eta_CBA)^2 >= 0`,
  `T4 - T5 = (1/2) sum (eta_ABC - eta_CBA)^2 >= 0`.
  They give the **sufficient** conditions `a1 >= 0`, `a3 >= 0`, `4 a1 a3 >= a2^2`,
  `a4 >= |a5|` for `W_g >= 0` on the whole family. (Sufficient, not necessary: for the
  implemented model `a3 = lambda l^2/20 < 0` is allowed when `lambda < 0`, while `W_g` remains
  PD by the Kronecker argument — recorded as a remark, not a contradiction.)
- Rotation independence of PD (blueprint (25)): see M2.5.

**3. Anisotropic gradient stiffness (blueprint (26)).** Verified as an assembly identity with
symbolic `B_,i` matrices: `dW_g/dd = K_g d` with
`K_g = (1/10) sum_i sum_j L_ij B^T_,i (D_c C_bar) B_,j` and `K_g = K_g^T` by construction
(major symmetry of `C`, symmetry of `L`). The **explicit** form is recorded as note F2; it is
the same object as blueprint (26) once the symmetric-pair factor is carried explicitly.

**Dimensional audit.** `[W] = Pa`, `[K_g] = Pa m^2`, `[B_,i] = 1/m`.

---

## M7 — Specialisations / limit ladder  (blueprint (27)–(30)) `[C]+[A]`

| Limit | Statement | Verification |
|---|---|---|
| (i) `l_i -> 0`, `ell_i -> 0` | `(A A^T)_rot -> 0`, `tau -> 0`, strong form `-> sigma_ij,j = rho u_i_ddot` | verified (tensor + substitution) |
| (ii) `AR = 1` (`l1=l2=l3=l`) | `(A A^T)_rot = l^2 I` for every `theta`; `g^2_22 = l^2/5` | verified |
| (iii) `ell_i -> 0` | gradient elasticity without micro-inertia: bounded-vs-unbounded phase velocity | 1D structural check: `v^2 = (C/rho)(1 + (1/10) l^2 k^2)` strictly increasing, `-> infinity`; with `ell > 0`: `v^2 -> (C/rho) l^2/(10 ell^2)` finite |
| (iv) `theta -> theta + 90°`, `l1<->l2` | full-matrix tensor identity; `g^2_22` identity | verified (see note M7-b) |

Note M7-a: the 1D dispersion expressions above are *structural consistency checks* of the
ladder, not scientific results. The full 2D high-`k` asymptotics with the anisotropic tensor is
Appendix A and belongs to **M16** (Phase 1 module list), not to Phase 2 derivations.
Note M7-b: the spectrum-level statement `omega_n(theta+90; AR) = omega_n(theta; 1/AR)` requires
in addition that the unit cell (Case C inclusion geometry and lattice) be invariant under the
same 90° rotation — true for the square cell with a centred inclusion; to be re-checked in
M10/M15 (recorded, not assumed).

**No TV item is required by M7.**

---

## FORMULATION NOTES (recorded, not silently decided)

**F1 — five-constant presentation vs factorized modulus — RESOLVED 2026-09-22 (audit
`AUDIT_F1_five_constant_vs_tensor_modulus.md`, 34 checks): the blueprint's five constants are
its explicitly labelled *isotropic* family; the implemented anisotropic model is (26) as written;
the two agree exactly in the isotropic-length sub-case. The text below is the original M4
finding, kept verbatim for traceability.**
Blueprint §2.4/§2.6 presents the isotropic sixth-order modulus through `a1..a5` (eqs (16)–(18),
(22)–(24)) while eq (26) implements the anisotropic operator with `(A A^T)_rot` and the meshed
`1/10` coefficient. M4 proves these are consistent *only as a sub-case*: the implemented model
is exactly `(a1,a2,a3,a4,a5) = (0, 0, lambda l^2/20, mu l^2/10, 0)` when the length tensor is
isotropic, and for `l1 != l2` it leaves the isotropic five-constant family altogether (the
`a_p` are scalars, while the implemented modulus is tensor-valued in `L`).
Consequence: the legacy FEM_3 Eqs (84)–(85) mapping is **not** the isotropic limit of blueprint
(26) (`a1 = ell^2(7mu+3lambda)/60 != 0`, `a2 = ell^2 lambda/6 != 0`,
`a5 = ell^2(7mu+3lambda)/60 != 0`, while (26) forces `a1 = a2 = a5 = 0`; no rescaling of `ell`
can reconcile this). Phase 1 therefore implements **(26) as written** (it is explicit) and
records the mismatch. Any future statement that compares Paper 9 with a single-length
five-constant benchmark must first resolve which convention the benchmark uses (Phase 3 /
Anchor A territory). Until then, no `a1..a5` values are quoted for Paper 9 in any deliverable.

**F2 — symmetric-pair (off-diagonal) factor conventions (derived; carry into M13/M14).**
With the independent strain pairs ordered `(11,22,12)` and the `eps_12` (not `gamma_12`)
convention, the factor `c_p = 2 - delta_p` appears in three equivalent guises, all verified in
M4/M6: (a) constitutive matrix (`sigma_12 = 2 mu eps_12`: shear-pair entry `2 mu`);
(b) derivative multiplicity `dW/dn_p = c_p (stress component)`; (c) energy pairing
`W = (1/2) sum_p c_p sigma_p eps_p` (equivalently `D_c = diag(1,1,2)`), giving the explicit
`K_g = (1/10) sum_ij L_ij B^T_,i (D_c C_bar) B_,j`. Blueprint (26) is the shorthand form; the
explicit factor must appear in the M14 assembly to avoid a silent factor-2 error on the shear
strain-gradient components. No equation *meaning* is altered.

**M5-a — free micro-inertia boundary term (to be discharged in M15).** The inertial term
produces the natural boundary data `rho ell_i^2 u_i_ddot,j n_j`; under the Bloch reduction this
touches the **normal-derivative DOFs**. M15 must verify that the Bloch phase is applied
consistently to this term and that no boundary DOF is double-counted (recorded here, not decided).

**N-1 — notation note (`ell_i`).** Blueprint (19)–(21) writes `ell_i` but uses it as a single
scalar micro-inertia length (no free index in the equations). Phase 1 treats `ell_i` as a scalar
`ell`. If a direction-dependent (tensor) micro-inertia was intended, that is a specification
change and has **not** been adopted.

**N-2 — kernel/coefficient.** The `1/10` (3D ellipsoid) coefficient is retained in 1D/2D
reductions by the blueprint; the alternative 1D/2D coefficients (1/6, 1/8) are not used
(recorded, matching [C] FEM_1).

---

## TV DEPENDENCIES ENCOUNTERED

M1–M7 are fully symbolic: **no TV item is resolved, and none is required** (all production
parameters remain symbols: `lambda, mu, l1, l2, l3, ell, theta, AR, rho`). Forward dependencies
recorded in `PHASE1_MANIFEST.md`: TV4 (k-points per IBZ segment) → M10; TV6 (Case H/C production
parameters) → M11/M14; TV7 (band count `N` + spurious-filter documentation) → M12/M15;
TV1/TV2/TV8/TV9/TV12 (anchor panel data) → Phase 3; TV10/TV11 (PB2009/LWZ2016 transcription) →
Phase 2/3; TV13 (`eps_Delta` wording) → Phase 4B. None of these may be guessed.

---

## TRACEABILITY (blueprint equation → derivation → script → log → status)

| Blueprint eqs | Object | Script | Log | Status |
|---|---|---|---|---|
| (1)–(4) | ellipsoidal domain, second-moment tensor | `scripts/m01_m02_length_tensor.py` | `checks/m01_m02_length_tensor.log` | checks PASSED |
| (5)–(9) | rotation, `(A A^T)_rot`, `g^2_22`, mixed term | `scripts/m01_m02_length_tensor.py` | `checks/m01_m02_length_tensor.log` | checks PASSED |
| (10)–(12) | kinematics, component counts, compatibility | `scripts/m03_kinematics.py` | `checks/m03_kinematics.log` | checks PASSED |
| (13)–(15) | `sigma`, Voigt, plane strain | `scripts/m04_form2_constitutive.py` | `checks/m04_form2_constitutive.log` | checks PASSED |
| (16)–(18) | five-constant modulus, plane-strain reduction, F1 | `scripts/m04_form2_constitutive.py`; F1 audit `scripts/audit_f1_five_constant.py` | `checks/m04_form2_constitutive.log`; `checks/audit_f1_five_constant.log` | checks PASSED (note F1 RESOLVED — see audit) |
| (19)–(21) | micro-inertia, inertial operator, Hamilton | `scripts/m05_micro_inertia.py` | `checks/m05_micro_inertia.log` | checks PASSED (note M5-a open) |
| (22)–(24) | energy, positive definiteness | `scripts/m06_energy_definiteness.py` | `checks/m06_energy_definiteness.log` | checks PASSED |
| (25) | eigenvalue invariance under rotation | `scripts/m01_m02_length_tensor.py`, `m06_energy_definiteness.py` | both logs | checks PASSED |
| (26) | anisotropic `K_g` assembly form | `scripts/m06_energy_definiteness.py` | `checks/m06_energy_definiteness.log` | checks PASSED (note F2) |
| (27)–(30) | limit ladder | `scripts/m07_limit_ladder.py` | `checks/m07_limit_ladder.log` | checks PASSED |

Total: **76 symbolic checks PASSED** (M1+M2 19, M3 9, M4 20, M5 7, M6 11, M7 10).

## NOT IN THIS DOCUMENT (later Phase-1 modules; not started)

M8 strong form + boundary/interfaces (31)–(35); M9 Bloch theorem for the `C^1` medium
(36)–(43); M10 IBZ path and `k`-sampling (44); M11 non-dimensionalisation (45)–(47);
M12 observables (48)–(52); M13 BFS element, `B`/`B_,i`, 32 DOF (53)–(56); M14 element matrices
(57)–(61); M15 Bloch master–slave reduction, Hermitian eigenproblem (62)–(71); M16 Appendix A
asymptotics (A.1)–(A.6); M17 Appendix B energy flux (B.1)–(B.8).

Phase 1 status: **IN PROGRESS — no scientific PASS claimed.**
