# PHASE-1 DERIVATION AND MATHEMATICAL-AUDIT RECORD — MODULE M8
## Strong-form governing equations, natural/essential boundary terms, interface terms

Status: **M8 COMPLETE at symbolic level (25 checks PASSED)**. M1–M7 unchanged (separate record
`DERIVATION_M01_M07.md`); M9–M17 NOT STARTED. Phase 0 LOCKED (`main` @ `175ea9e`). No
scientific PASS is claimed: this record contains no numerical value, no benchmark comparison,
and no Bloch phase mapping (M9).

Governing inputs (read-only):
- Blueprint v1.3 `paper9/plan/blueprint/Paper9_Blueprint_v1.3.tex`
  (sha256 `ca71b91aba4ca4abe9f157eb595ac8c2f709d838957a08ea0dce7160685dbf9f`), eqs (31)–(35),
  built on (19)–(26).
- `paper9/plan/CALC_MASTER_PLAN.md` v1.1 §A (dependency map).
- `DERIVATION_M01_M07.md` (locked M1–M7 results), `AUDIT_F1_five_constant_vs_tensor_modulus.md`.
- Legacy [C] source (read-only, outside repo): `femcheck/FEM_Total/ptxt/FEM_1_Paper.txt`
  Eq (18) (effective stress `sigma_ij = tau_ij - q_ijm,m`), Eq (22) (strong form),
  Eq (36) (`q_ijm = (1/10) L_mn C_ijkl eps_kl,n`), Eq (37) (`q_ijm nu_m nu_j = 0`),
  Eq (38) (`u_i,nu = g_i`), §4 (classical and higher-order BCs; "one extra boundary condition
  per side"), §5 (surface tractions `t_i`, double tractions `r_i = q_ijm nu_m nu_j`, line forces
  `e_i = [[q_ijm nu_m mu_j]]` of the full Mindlin–Toupin form; the reduced Aifantis-type
  conditions used in the FE model neglect surface divergence and edge terms).

Provenance tags: `[C]` cited source · `[A]` derived in this work · `[S]` definition/structural.

Reproduce:

```
cd paper9/eqs/phase1
python3 scripts/m08_strong_form.py     # M8   (25 checks)
```

Deterministic, SymPy exact arithmetic, all quantities symbolic, writes no files.
Script sha256 (run in `checks/m08_strong_form.log`): `02a89ea982cd24c0a79b47b2e94eb3b6e05aa924b18c03f584e7987bb5ff3e7f`.

---

## M8.0 — Setting and conventions (all inherited, nothing re-assumed) `[S]`

Locked objects carried over verbatim from M1–M7:

| Object | Definition | Source |
|---|---|---|
| length tensor | `L = (A A^T)_rot`, `A = diag(l1,l2,l3)`, rotated by `theta` | M2, blueprint (5)–(9), (26) |
| strain / strain gradient | `eps_ij = (1/2)(u_i,j + u_j,i)`, `eta_ijk = eps_ij,k` | M3, (10)–(12) |
| Cauchy stress | `sigma_ij = C_ijkl eps_kl` | M4, (13)–(14) |
| double stress | `tau_ijk = (1/10) L_kn C_ijpq eta_pqn` | M4, (16)–(18) + (26) |
| energy | `W = (1/2) C_ijkl eps_ij eps_kl + (1/20) L_mn C_ijkl eta_ijm eta_kln` | M6, (22)–(24) |
| micro-inertia | `T` with `rho( u_i_ddot - ell^2 u_i_ddot,jj )` | M5, (19)–(21) |

`L = (A A^T)_rot` is used **exactly as implemented in (26)** — it is not replaced by the
five-constant isotropic family, and no `a_1..a_5` value is quoted anywhere in M8 (F1 audit:
`a_1..a_5` are the blueprint's explicitly labelled *isotropic-family presentation*; (26) is the
operational anisotropic model; they meet only on the single ray `L ∝ I`).

**Convention (fixed by M5 / blueprint (19)–(21)) `[C]`.** Time-harmonic fields are written
`u(x,t) = Re[ u_hat(x) e^{-i omega t} ]`, so `u_i_ddot -> -omega^2 u_i`. The strong-form
operator below is stated in the time domain (blueprint (31) as written) and in the
time-harmonic form required by the Bloch formulation (blueprint §3, M9+).

---

## M8.1 — Variational statement from which the strong form is derived `[A]`

The strong form is **derived**, not recalled. Start from Hamilton's principle applied to the
locked energy and micro-inertia of M5–M6 (blueprint (19)–(24)); for a test field `v_i`
(virtual displacement) the stationarity condition is the d'Alembert form

```
(M8.1)   W(u,v) := int_Omega [ sigma_ij eps_ij(v) + tau_ijk eta_ijk(v)
                                + rho ( u_i_ddot v_i + ell^2 u_i_ddot,j v_i,j ) ] dV = 0
```

for all admissible `v`. In the time-harmonic form (M5 reduction) this becomes

```
(M8.2)   W_h(u,v) := int_Omega [ sigma_ij eps_ij(v) + tau_ijk eta_ijk(v)
                                  - rho omega^2 ( u_i v_i + ell^2 u_i,j v_i,j ) ] dV = 0 .
```

This is the variational statement whose **exact** integration by parts M8 performs. Two
symmetries are needed and are verified in the script: `sigma_ij = sigma_ji` and
`tau_ijk = tau_jik` (the latter follows from `C_ijpq = C_jipq` and is what allows replacing
`delta eta_ijk = (1/2)(v_i,jk + v_j,ik)` by `v_i,jk`). `[A]` check [C5].

---

## M8.2 — Strong form (blueprint (31)) `[A]`, corroborated by `[C]`

Integration by parts of (M8.1) (verified exactly, see M8.7) gives

```
(M8.3)   W(u,v) = - int_Omega R_i v_i dV  +  (boundary terms, M8.3 below)

(M8.4)   R_i := sigma_ij,j - tau_ijk,jk - rho ( u_i_ddot - ell^2 u_i_ddot,jj )
```

Since (M8.1) must hold for arbitrary `v`, the governing equations are `R_i = 0`, i.e.

```
(M8.5)   sigma_ij,j - tau_ijk,jk = rho ( u_i_ddot - ell_i^2 u_i_ddot,jj )        [blueprint (31)]
```

Equivalently, with the **effective (total) stress** `Sigma_ij := sigma_ij - tau_ijk,k`
(= `tau_ij - q_ijm,m` of FEM_1 Eq (18) `[C]`, so `q_ijm == tau_ijk` under the M1–M7 index
mapping), and using the index symmetry `tau_ijk,jk = tau_ijk,kj`:

```
(M8.6)   Sigma_ij,j = rho ( u_i_ddot - ell_i^2 u_i_ddot,jj )
(M8.7)   time-harmonic:   sigma_ij,j - tau_ijk,jk + rho omega^2 ( u_i - ell^2 u_i,jj ) = 0
```

Body force (not in (31); recorded for completeness, matches FEM_1 Eq (22) `[C]`): a
volume-force density `P_i` is added to the right-hand member of (M8.5)–(M8.7) with a `+`
sign. It is not used in Phase 1 (no forcing in the band-structure problem).

**Contributions present (`[A]`, index-notation audit):**
- classical stress contribution: `sigma_ij,j` = `(C_ijkl eps_kl),j` — second order in `u`;
- higher-order/double-stress contribution: `- tau_ijk,jk` with `tau_ijk = (1/10)L_kn C_ijpq eta_pqn`
  — fourth order in `u`; the free index `i` of `tau` is carried by the first two indices, the
  length tensor contracts the **gradient index** `k` with the third index `n` (M4, F2);
- micro-inertia contribution: `- rho ell^2 u_i_ddot,jj` — second order in `u`, second order in
  time. Setting `ell = 0` returns the classical inertial term.

**Order and data count (`[A]`, `[C]` corroboration):** the operator (M8.5) contains fourth-order
spatial derivatives, hence one extra boundary condition per boundary is required — stated
identically in FEM_1 §4 `[C]` ("one higher-order boundary condition is required", "fourth-order
and needs one extra boundary condition per side").

---

## M8.3 — Natural/essential boundary terms from the integration by parts `[A]`, `[C]`

The exact boundary terms produced by the integration by parts (M8.1) are, in raw (pre-split)
form with outward unit normal `n_j`,

```
(M8.8)   int_dOmega [ ( sigma_ij n_j - tau_ijk,k n_j + rho ell^2 u_i_ddot,j n_j ) v_i
                       + tau_ijk n_k v_i,j ] dGamma                        (raw form, [A])
```

Using the flat-edge/surface split `v_i,j = n_j (D v_i) + a_j^alpha (D_alpha v_i)` with
`D := n_j d/dx_j` (normal derivative) and surface tangents `a_j^alpha`, and the surface
divergence theorem, (M8.8) becomes the **canonical four-quantity boundary operator**:

```
(M8.9)    int_dOmega [ t_i v_i + R_i (D v_i) ] dGamma  +  corner/edge terms

(M8.10)   t_i = ( sigma_ij - tau_ijk,k ) n_j + rho ell^2 u_i_ddot,j n_j - D_alpha ( tau_ijk n_k a_j^alpha )
               \_____ classical + higher-order traction _____/  \_ M5-a _/   \_ tangential redistribution _/

(M8.11)   R_i = tau_ijk n_j n_k                       (normal double traction)      [blueprint (32)-(35)]
```

and at points where the boundary normal is discontinuous, the **line/corner forces**

```
(M8.12)   e_i = [[ tau_ijk n_k a_j^alpha mu_alpha ]] ,      a_j^alpha mu_alpha = mu_j (edge co-normal)
```

For a flat face with orthonormal `(n, m)` (`m` = in-surface co-normal) the tangential double
traction is the scalar family

```
(M8.13)   q_i = tau_ijk n_k m_j ,   D_alpha ( tau_ijk n_k a_j^alpha ) -> d_s q_i ,
          e_i -> [[ q_i ]] ,
```

which is exactly the structure quoted in FEM_1 §5 `[C]`: "surface tractions `t_i`, double
tractions `r_i = q_ijm nu_m nu_j` and line forces `e_i = [[q_ijm nu_m mu_j]]` along edges where
the normal `nu` is discontinuous".

**Boundary data set (four quantities per direction), `[C]` blueprint (33)–(35) + `[A]`:**
- essential, classical: `u_i = u_i_bar` on `Gamma_u`  [blueprint (33); FEM_1 Eq (33)];
- essential, higher order: `u_i,nu := u_i,j n_j = g_i_bar` on `Gamma_g`  [blueprint/FEM_1 Eq (38)]
  — conjugate to the double-traction slot, i.e. enforced through **normal-derivative (Hermite)
  DOFs** (relevant to M13/M15);
- natural, classical: `t_i = t_i_bar` on `Gamma_t`; traction-free: `t_i = 0`  [blueprint (34)–(35)];
- natural, higher order: `R_i = R_i_bar` on `Gamma_q`; free: `R_i = n_j n_k tau_ijk = 0`
  [blueprint (32)–(35); FEM_1 Eq (37) in the reduced form `q_ijm nu_m nu_j = 0`].

Reduced (flat-face) counterpart used by the legacy model `[C]`: with `L_mn` constant the
operator commutes and FEM_1 Eq (39) states `L_mn d(sigma^cl_ij)/dx_n nu_m nu_j = 0`, i.e.
`R_i = 0` with the constant `1/10` dropped because the condition is homogeneous (multiplication
by a non-zero constant does not change the constraint) — M8 confirms algebraically that the
`1/10` is a common factor of `tau_ijk` and therefore of `R_i` (check [C2]/[C11]).

**Note M8-a (open item, NOT decided here).** `D_alpha (tau_ijk n_k a_j^alpha)` in (M8.10) and
the line forces (M8.12) are part of the mathematically exact IBP result (verified in check
[C8]). The legacy `[C]` model explicitly neglects "surface divergence and edge terms"
("reduced Aifantis-type condition, not the full Mindlin–Toupin form … noted as a limitation"),
and the blueprint's boundary data set (32)–(35) lists exactly the four quantities of the reduced
set. The bulk strong form (M8.5) is **identical** in both cases; only the assembled boundary
operator differs. Decision required before the element assembly (M13/M15) — recorded, not
silently decided. See §"Open items".

---

## M8.4 — Treatment of the micro-inertia boundary term (M5-a discharge at operator level) `[A]`

M5-a recorded the free-boundary term `rho ell_i^2 u_i_ddot,j n_j` as "to be discharged in M15".
M8 determines **exactly** where it enters the boundary operator:

1. It arises from the integration by parts of the micro-inertia part of the weak form, the term
   `rho ( u_i_ddot v_i + ell^2 u_i_ddot,j v_i,j )` in (M8.1):
   `int rho ell^2 u_i_ddot,j v_i,j dV = int_dGamma rho ell^2 u_i_ddot,j n_j v_i dGamma
   - int rho ell^2 u_i_ddot,jj v_i dV` (verified exactly, check [C1]/[C2]).
2. Therefore it is **conjugate to the value DOF `v_i`**, i.e. it belongs to the
   **classical-traction slot** `t_i` of (M8.10) — *not* to the double-traction slot `R_i`
   (check [C2]: the inertial part of the traction operator equals `+rho ell^2 u_i_ddot,j n_j`
   exactly, and the double-traction slot is unchanged: `R_i = tau_ijk n_j n_k`, no `ell`).
3. Sign: `+ rho ell^2 u_i_ddot,j n_j` (the same sign as the stress traction `(sigma_ij -
   tau_ijk,k) n_j`), verified by the two independent exact identities of checks [C1] and [C3b]
   against the d'Alembert weak form (M8.1) — this is the "sign from the variational derivation"
   requirement; no sign is taken on memory.
4. Time-harmonic form: with `u_i_ddot = -omega^2 u_i` the term becomes
   `- rho omega^2 ell^2 u_i,j n_j` (check [C3]), i.e. a **real, frequency-dependent boundary
   term proportional to the normal derivative** `u_i,nu` of the field. Under the Bloch
   reduction (M9) this is the term that must be paired with the complex Hermite/derivative DOFs
   with the correct phase factor — the consistency question raised by M5-a, now localised
   exactly: it is one additive term in the classical-traction slot.
5. Free surface: for a traction-free boundary the reduced condition is `t_i = 0`, i.e.
   `(sigma_ij - tau_ijk,k) n_j + rho ell^2 u_i_ddot,j n_j = 0` (in the reduced set of M8-a);
   the micro-inertia term therefore does **not** vanish on a free surface in general (it
   vanishes only if `u_i,j n_j = 0` on that surface, or in the zero-micro-inertia limit).

---

## M8.5 — Interface conditions (two-layer medium, as required by the bilayer cell) `[A]`, `[C]`

For a domain split into two sub-domains `Omega^A`, `Omega^B` with a common interface `Gamma_I`
(unit normal `n`), the same IBP applied in each sub-domain, summed, and using a `C^1` (globally
continuous value + continuous normal derivative) test field, gives

```
(M8.14)   sum_layers int R_i v_i dV = (outer boundary terms)
                                     + int_Gamma_I [ (t^A_i - t^B_i) v_i
                                                     + (R^A_i - R^B_i) (D v_i) ] dGamma
```

With no prescribed interface data, the interface integral must vanish for arbitrary admissible
`v`, which yields the **natural interface conditions** and, through the test space, the
**essential** ones:

| # | Condition | Type | Conjugate quantity |
|---|---|---|---|
| 1 | `u_i` continuous across `Gamma_I` | essential | displacement |
| 2 | normal derivative `u_i,j n_j` continuous | essential | derivative (Hermite) DOF |
| 3 | traction `t_i` continuous (`t^A_i = t^B_i`) | natural | classical traction |
| 4 | double traction `R_i` continuous (`R^A_i = R^B_i`) | natural | normal double traction |

i.e. **four conditions per interface per direction**, consistent with the fourth-order operator
in each layer and with the value + first-derivative DOF set of the `C^1` element used by the
Phase-1 discretisation (M13/M15). Signs verified exactly (check [C16]); the layered-material
form of `t_i` uses the layer's own `L`, `C`, `rho`, `ell`. No interface stiffness/spring or
imperfect-bond data are introduced (the blueprint validates against a perfect-interface bilayer
— Anchor A `[C]` limitation). Interface conditions are stated in the time-domain form; the
time-harmonic form is obtained with `u_i_ddot -> -omega^2 u_i` exactly as in M8.4(4).

---

## M8.6 — Limit cases: exactly which terms survive `[A]`

| Limit | `tau_ijk` / `R_i` | bulk operator | boundary operator | check |
|---|---|---|---|---|
| classical elasticity `L -> 0`, `ell -> 0` | `tau -> 0` (all components), `R_i -> 0` | `sigma^cl_ij,j = rho u_i_ddot` (time domain); `sigma^cl_ij,j + rho omega^2 u_i = 0` (harmonic) | `t_i = sigma^cl_ij n_j` only | [C12] |
| zero-gradient `L -> 0`, `ell > 0` | `tau -> 0`, `R_i -> 0`; higher-order **boundary** data reduce to the essential normal-derivative values only | `sigma^cl_ij,j + rho omega^2 ( u_i - ell^2 u_i,jj ) = 0` | `t_i = sigma^cl_ij n_j - rho omega^2 ell^2 u_i,j n_j` | [C13] |
| zero-micro-inertia `ell -> 0`, `L != 0` | unchanged (`tau`, `R_i`, `q_i` as derived) | `sigma_ij,j - tau_ijk,jk = rho u_i_ddot`; harmonic: `+ rho omega^2 u_i = 0` — **identical to FEM_1 Eq (22) `[C]`** | `t_i` retains the full classical + higher-order part; `R_i = n_j n_k tau_ijk = 0` on free faces | [C14] |
| homogeneous isotropic length `L = ell_L^2 I` | `tau_ijk = (1/10) ell_L^2 C_ijpq eta_pqk` | `(1 - (ell_L^2/10) LAPLACIAN) sigma^cl_ij,j + rho u_i_ddot - rho ell^2 u_i_ddot,jj = 0`; **reduces to M4 / FEM_1 Eq (22)** with `ell = 0`; Aifantis-type fourth-order operator, one extra BC per side | `R_i = (1/10) ell_L^2 C_ijpq eta_pqk n_j n_k`; homogeneous condition can drop the constant `1/10` | [C9], [C10], [C11] |

Reduction to M4 (isotropic-length specialisation) is verified in two independent ways:
(i) component identity `tau_ijk = (1/10) ell_L^2 C_ijpq eta_pqk` for all `(i,j,k)`;
(ii) operator identity `tau_ijk,jk = (1/10) ell_L^2 ( laplacian sigma_ij ),j`, giving the
classical `(1 - (ell^2/10) Lap)` gradient operator of the legacy formulation. The factor
`1/10 = (1/2)(1/5)` is traced to M1 (moment factor `1/5`) × F2 (symmetric-pair factor `1/2`),
and the isotropic-length member of (26) remains `(a_1..a_5) = (0, 0, lambda ell_L^2/20,
mu ell_L^2/10, 0)` (M4; independently re-derived in the F1 audit) — quoted here only as the
already-audited isotropic specialisation, never as the operational model.

**Note M8-b (statement of a limit, not a new result):** the `ell -> 0` row is the *only* place
where the M8 operator coincides with the legacy `[C]` strong form; the micro-inertia bulk term
`- rho ell^2 u_i_ddot,jj` has no counterpart in FEM_1 and its presence is what makes the
high-frequency phase velocity finite (M7(iii), Anchor B `[C]`). No new dispersion statement is
made in M8 (that is M16 / Phase 2).

---

## M8.7 — Dimensional audit (every strong-form and boundary term) `[A]`

Basis `(kg, m, s)`; `[Pa] = (1,-1,-2)`, `[rho] = (1,-3,0)`, `[ell] = [n_j] = 0` in length for
`n_j`, `[L] = (0,2,0)`, `[u] = (0,1,0)`, `[eta] = (0,-1,0)`, `[tau] = Pa m = (1,0,-2)`.
Executed in the script with a symbolic dimension algebra that also asserts term-by-term
homogeneity of every sum it encounters (check [C15]):

| Equation / slot | Terms | Dimension |
|---|---|---|
| (M8.5) time domain | `sigma_ij,j`, `tau_ijk,jk`, `rho u_i_ddot`, `rho ell^2 u_i_ddot,jj` | `(1,-2,-2)` = Pa/m each |
| (M8.7) time harmonic | `sigma_ij,j`, `tau_ijk,jk`, `rho omega^2 u_i`, `rho omega^2 ell^2 u_i,jj` | `(1,-2,-2)` = Pa/m each |
| traction slot (M8.10) | `sigma_ij n_j`, `tau_ijk,k n_j`, `rho ell^2 u_i_ddot,j n_j` | `(1,-1,-2)` = Pa each |
| tangential redistribution | `d_s q_i`, `q_i = tau_ijk n_k m_j` | `(1,-1,-2)` = Pa; `(1,0,-2)` = Pa m |
| double-traction slot (M8.11)–(M8.13) | `R_i`, `q_i`, `e_i = [[q_i]]` | `(1,0,-2)` = Pa m each |
| surface work | `t_i v_i`, `R_i D v_i`, `q_i d_s v_i` | `(1,0,-2)` = J/m² each |
| interface jumps (M8.14) | `[t_i]`, `[R_i]` | Pa, Pa m (their own slots) |

The two boundary slots are dimensionally **distinct** (`Pa` vs `Pa m`), consistent with their
conjugate DOFs (`v_i` and `D v_i`); both give `J/m²` in the weak form — no mixing is possible.

---

## M8.8 — Checks performed in M8 (all executed, all passed)

| # | Check | Type | Result |
|---|---|---|---|
| C1 | 1D exact variational identity, time domain, generic degree-4 polynomials: `int[sigma du' + tau du'' + rho(u_ddot du + ell^2 u_ddot' du')] = -int[{sigma' - tau'' - rho(u_ddot - ell^2 u_ddot'')} du] + [ (sigma - tau' + rho ell^2 u_ddot') du + tau du' ]` — sign of (M8.5) verified | index/sign | PASSED |
| C2 | M5-a tracking: the inertial part of the boundary operator conjugate to `du` is `+rho ell^2 u_ddot'`; the double-traction slot has no inertial part | sign/consistency | PASSED |
| C3 | time-harmonic reduction: residual `-> sigma' - tau'' + rho omega^2 (u - ell^2 u'')`, traction `-> sigma - tau' - rho omega^2 ell^2 u'` | consistency | PASSED |
| C3b | same 1D identity in the time-harmonic form (independent re-test) | sign | PASSED |
| C4 | energy consistency `W_g = (1/2) tau_ijk eta_ijk` (the double stress is the gradient of the locked energy) | energy | PASSED |
| C5 | tensor symmetry `tau_ijk = tau_jik` (and `sigma_ij = sigma_ji`) required by the IBP | symmetry | PASSED |
| C6 | 2D raw IBP identity on the unit square, **50 monomial test fields**: weak form + bulk residual = full raw boundary integrand (M8.8) | index/sign (2D) | PASSED |
| C7 | flat-edge chain rule `v_i,j = n_j D v_i + m_j d_s v_i` on all four edges (pointwise) | index | PASSED |
| C8 | tangential redistribution `int f d_s v ds = -int (d_s f) v ds + [f v]_start^end`; consequence: only `t_i` is modified (by `-d_s q_i`), `R_i` untouched, corner terms `[[q_i]]` | sign/canonical split | PASSED |
| C9 | isotropic-length specialisation `L = ell_L^2 I -> tau_ijk = (1/10) ell_L^2 C_ijpq eta_pqk` (reduction to M4) | limit | PASSED |
| C10 | `tau_ijk,jk = (1/10) ell_L^2 (lap sigma_ij),j`; operator `(1 - (ell_L^2/10) Lap)`; fourth order, one extra BC per side | limit/operator | PASSED |
| C11 | factor provenance `1/10 = (1/2)(1/5)` (M1 moment × F2 pair factor) and `W_g = (1/20) ell_L^2 C:eta:eta`; isotropic member `(a_1..a_5) = (0,0,lambda ell^2/20, mu ell^2/10, 0)` per M4/F1 | consistency | PASSED |
| C12 | classical limit (`L -> 0`, `ell -> 0`): `tau = 0`, Navier strong form, classical traction only | limit | PASSED |
| C13 | zero-gradient limit (`L -> 0`, `ell > 0`): double-stress and higher-order boundary terms vanish, micro-inertia operator and inertial traction survive | limit | PASSED |
| C14 | zero-micro-inertia limit (`ell = 0`): inertial operator becomes `rho u_i_ddot` / `rho omega^2 u_i`; gradient terms and both boundary slots untouched; coincides with FEM_1 Eq (22) `[C]` | limit | PASSED |
| C15 | dimensional audit (7 equation/slot groups, term-by-term, + 1 cross-slot distinctness check = 8 checks) | dimension | PASSED |
| C16 | two-layer interface identity with exact signs: `(t^A - t^B)` and `(R^A - R^B)` are the only interface flux terms; per-layer identities verified separately | sign/index | PASSED |
| C17 | interface data count: four conditions per interface per direction | structural | PASSED |

**25 checks, all PASSED** (script `scripts/m08_strong_form.py`, log `checks/m08_strong_form.log`).
All ten checks required by the M8 mandate are covered: index consistency (C1, C3b, C6, C7, C16),
IBP sign consistency (C1, C3b, C6, C8), tensor symmetry (C5), dimensional consistency (C15),
isotropic-length reduction (C9, C10, C11), classical limit (C12), gradient-free limit (C13),
micro-inertia-free limit (C14), boundary-term consistency (C2, C6, C8, C16), symbolic
simplification (every check is an exact SymPy simplification to `0`).

**Failures encountered and fixed during M8 (kept for traceability).**
1. First coding of the IBP identity used the *Lagrangian* inertial sign (`-rho(u_ddot du + ...)`),
   which does not reproduce (M8.5); the correct statement is the d'Alembert form (M8.1)
   (`+rho(u_ddot du + ell^2 u_ddot,j v_i,j)`), which yields `sigma_ij,j - tau_ijk,jk = rho(...)`.
   The sign is now fixed by the identity itself, not by memory.
2. The raw boundary term must differentiate `tau_ijk` with respect to the position of the
   **third (`k`)** index, `tau_ijk,k n_j`; differentiating with respect to the second index
   fails the identity for 48 of 50 test fields. Found by the 2D check, fixed, re-verified
   (all 50 fields, all four edges).
3. SymPy `subs(expr, expr)` does not replace an expression inside its own derivatives; the
   time-harmonic check therefore builds `u_i_ddot = -omega^2 u_i` as a field from the start
   (no substitution of composite expressions).
4. `eta_of` key generation must map `(2,1)->(1,2)` (independent-pair convention of M3/F2).

---

## TV DEPENDENCIES ENCOUNTERED

M8 is fully symbolic: **no TV item is resolved and none is required.** Every quantity in
(M8.1)–(M8.14) is either a locked M1–M7 object or a derivative of one; no numerical parameter,
no k-point, no band count, no material value appears. Forward dependencies are unchanged
(TV4 -> M10; TV6 -> M11/M14; TV7 -> M12/M15; TV1/TV2/TV8/TV9/TV12 -> Phase 3; TV10/TV11 ->
Phase 2/3; TV13 -> Phase 4B). The only M8 output that later modules consume is structural:
the operator forms (M8.10)–(M8.11) and the four interface conditions (M8.15 table).

---

## OPEN ITEMS FROM M8 (recorded, not decided)

- **M8-a — completeness of the assembled boundary operator.** The exact IBP boundary operator
  (M8.10)–(M8.13) contains the tangential redistribution `- D_alpha(tau_ijk n_k a_j^alpha)`
  (flat-face: `-d_s q_i`) and line/corner forces `e_i = [[q_i]]`. The legacy `[C]` model
  explicitly neglects surface divergence and edge terms ("reduced Aifantis-type condition …
  noted as a limitation"), and blueprint (32)–(35) lists the reduced four-quantity set.
  The bulk strong form is unaffected. **Decision required before M13/M15** (which boundary
  operator the assembled `K` implements). M8 does not decide; the term is verified to be the
  mathematically exact IBP result, so a decision either way can be documented.
- **M5-a (updated) — status.** Discharged at the operator level: the free micro-inertia term
  `rho ell^2 u_i_ddot,j n_j` enters the **classical-traction slot** with a `+` sign
  (time-harmonic: `-rho omega^2 ell^2 u_i,j n_j`), and is conjugate to the value DOF, not to the
  derivative DOF. The remaining M15 obligation is now specific: verify that the Bloch phase
  factor is applied consistently to this real, frequency-dependent term in the assembled
  boundary/`K` blocks (no boundary DOF double-counted).
- **M8-c — body force convention (informational).** Blueprint (31) has no volume force; FEM_1
  Eq (22) carries `P_i` with a `+` sign (M8.5). Phase 1 uses no forcing, so the convention is
  only recorded. No scope change.
- **M8-d — notation (informational).** FEM_1 `[C]` writes the double stress as `q_ijm` with the
  length contraction on the last index; the M1–M7 mapping `q_ijm == tau_ijk` holds. No
  blueprint notation is altered.

---

## TRACEABILITY (blueprint equation -> derivation -> script -> log -> status)

| Blueprint eqs | Object | Script | Log | Status |
|---|---|---|---|---|
| (31) | strong form `sigma_ij,j - tau_ijk,jk = rho(u_i_ddot - ell^2 u_i_ddot,jj)`, derived by IBP from (19)–(26) | `scripts/m08_strong_form.py` | `checks/m08_strong_form.log` | checks PASSED (C1, C3, C4, C5, C6, C12, C13, C14, C15) |
| (32)–(35) | surface double traction `R_i = n_j n_k tau_ijk`, classical traction, essential normal derivative, free-surface conditions | `scripts/m08_strong_form.py` | `checks/m08_strong_form.log` | checks PASSED (C2, C3, C7, C8, C15, C16) |
| (19)–(26) | inputs (energy, micro-inertia, (26) modulus) reused unchanged | `scripts/m08_strong_form.py` (consistency C4, C11) | `checks/m08_strong_form.log` | checks PASSED |
| interface (blueprint §3 layers) | four conditions per interface per direction | `scripts/m08_strong_form.py` | `checks/m08_strong_form.log` | checks PASSED (C16, C17) |

Total Phase-1 symbolic checks after M8: **76 (M1–M7) + 34 (F1 audit) + 25 (M8) = 135**, all
PASSED. These are internal mathematical checks (indices, signs, contractions, symmetries,
dimensions, limit reductions, blueprint traceability). They are **not** numerical verification
(tests 5a–5i, Phase 4A), **not** published-benchmark validation (Phase 3) and **not** results.

## NOT IN THIS DOCUMENT (not started)

M9 Bloch theorem for the `C^1` medium (36)–(43) — explicitly out of scope here (no phase
mapping, no Bloch boundary mapping, no reduced `K`/`M`); M10 IBZ path and k-sampling (44);
M11 non-dimensionalisation (45)–(47); M12 observables (48)–(52); M13 BFS element, `B`/`B_,i`,
32 DOF (53)–(56); M14 element matrices (57)–(61); M15 Bloch master–slave reduction, Hermitian
eigenproblem (62)–(71); M16 Appendix A asymptotics (A.1)–(A.6); M17 Appendix B energy flux
(B.1)–(B.8). Tests 5a–5i, published validation and TV resolution remain out of scope for
Phase 1.
