# PHASE-1 AUDIT RECORD — M8-a
## Boundary operator: exact variational (tangential + corner) terms vs the reduced four-quantity model

Status: **RESOLVED — interpretation (A)**: Blueprint v1.3 specifies the **reduced four-quantity
boundary model** as the operational paper model; the **fully variationally exact** boundary
operator (tangential redistribution + corner/line forces) is retained in M8 and here as a
**documented mathematical caveat** with a precisely delimited scope. No silently chosen middle
ground: both formulations are stated, their difference is quantified exactly, and the scope in
which the difference has no effect on the planned computations is verified.

Scope of this audit: M8-a ONLY. No blueprint file, no M1–M7 mathematics, no solver/Bloch code,
no tests 5a–5i, no published validation, no TV item, no numerical parameter value.
Script: `scripts/audit_m8a_boundary_operator.py` — **17 checks, all PASSED**
(`checks/audit_m8a_boundary_operator.log`).

Inputs (read-only): Blueprint v1.3
(sha256 `ca71b91aba4ca4abe9f157eb595ac8c2f709d838957a08ea0dce7160685dbf9f`),
`DERIVATION_M08.md`, `DERIVATION_M01_M07.md`,
legacy `[C]` `femcheck/FEM_Total/ptxt/FEM_1_Paper.txt`.

---

## 1. What the exact integration by parts gives (M8, unchanged) `[A]`

From the locked M5–M6 weak form the exact boundary integrand is

```
(X1)  [ (sigma_ij - tau_ijk,k) n_j + rho ell^2 u_i_ddot,j n_j - D_alpha( tau_ijk n_k a_j^alpha ) ] v_i
      + R_i D v_i                                    (canonical),  R_i = tau_ijk n_j n_k
(X2)  e_i = [[ tau_ijk n_k a_j^alpha mu_alpha ]]      (corner / line forces)
(X3)  raw form:  ( sigma_ij n_j - tau_ijk,k n_j + rho ell^2 u_i_ddot,j n_j ) v_i + tau_ijk n_k v_i,j
```

The only relation between the two models (verified exactly, this audit [A3], [A3b], and M8 [C6],
[C8]) is

```
(X4)  (exact tau-part) = sum_edges [ R_i D v_i - (d_s q_i) v_i ] + sum_corners [q_i v_i]
      (reduced tau-part) = sum_edges [ R_i D v_i ]
      => (exact) - (reduced) = - sum_edges int (d_s q_i) v_i ds + sum_corners [q_i v_i]
```

with `q_i = tau_ijk n_k m_j` on a flat face (`m` = edge co-normal). Statement (X4) is a
**model difference**, not a rearrangement: it is non-zero for generic non-uniform fields
([A8], exact value printed in the log) and vanishes only in special cases ([A9], [A13]).

---

## 2. Blueprint v1.3 evidence (question 1) `[C]`

| Location | Verbatim wording | Evidential weight |
|---|---|---|
| §2.8 row, line 357 | "**Equations of motion and boundary conditions.** Strong form `sigma_ij,j - tau_ijk,jk = rho( u_i_ddot - ell_i^2 u_i_ddot,jj )`; surface double traction `R_i = n_j n_k tau_ijk`; **the four boundary quantities per direction (classical traction, double traction, displacement, normal derivative)**." | The boundary data are **enumerated exhaustively as four quantities per direction**; only the double traction is given an explicit formula; **no surface-divergence, edge or line-force term appears anywhere** |
| Equation register, line 571 | "`(32)--(35)` Double traction `R_i`, **four BC quantities per direction**, higher-order BCs & §2.8" | The register names exactly one higher-order natural datum: `R_i` |
| Risk table, line 421 | "Interface conditions (Case C) — Gradient elasticity needs **four** conditions per interface (displacement, normal derivative, traction, double traction). **Missing one silently shifts the gap edges.**" | The blueprint treats the count of four as *complete* and warns about count failures; a fifth (corner) datum of the exact model is never mentioned, so it is not part of the specified model |
| §4.1, line 399 | "4 DOF per node per displacement component `{u, u_,x, u_,y, u_,xy}`; 2 components × 4 nodes × 4 DOF = **32 DOF per cell**; `C^1` inter-element continuity" | The discretisation carries value and derivative DOFs only — the natural data of the reduced model (`u_i`, `u_i,nu`, `t_i`, `R_i`); no line-force/point-data variable exists |
| §4.4, line 402 | "Partition cell DOFs into interior / edge / corner. For each periodic pair, `d_slave = T(k) d_master` with `T` diagonal complex phase." | Bloch conditions are imposed by **DOF tying**, not by evaluating boundary operators — the boundary operator is not assembled |
| Scope table, line 179 | "Boundary conditions: Real periodic tying, or clamped/traction → **Complex Bloch phase on value and derivative DOFs**" | The cell boundary of the planned problem is periodic/constrained, not a free surface with prescribed natural data |
| Summary, line 1062 | "Bogner–Fox–Schmit `C^1` rectangle, 32 DOF/cell, complex Bloch phase on value *and* derivative DOFs, Hermitian reduced eigenproblem over Γ–X–M–Γ" | Same conclusion as above |

**Reading.** The blueprint is precise exactly where the physical model is delicate (strong form,
`R_i`, micro-inertia sign, phase sign on derivative DOFs, interface-condition count, retention
of the `1/10` coefficient). It specifies the second-order-plus-gradient boundary structure by
**listing the four boundary quantities per direction** and defines explicitly only `R_i`. It
never mentions surface divergence, tangential redistribution, edge terms or line forces, and its
discretisation has no variable able to carry such a datum. The natural reading is therefore that
**the four-quantity boundary set is the intended, operational boundary model of the paper**, with
the exact variational operator remaining as a property of the underlying theory.

Interpretation (A) is recorded; interpretation (B) ("blueprint requires the full variational
boundary operator") is **not** supported: no blueprint statement requests the tangential or edge
terms, and the blueprint's own interface-count warning would be incomplete under (B).

---

## 3. Legacy `[C]` evidence (question 2)

| Location | Content | Relation to this audit |
|---|---|---|
| FEM_1 Eq (18) | `sigma_ij = tau_ij - q_ijm,m` (effective stress; `q_ijm == tau_ijk` in M1–M7 notation) | the reduced traction slot `(sigma_ij - tau_ijk,k) n_j` |
| FEM_1 Eqs (33)–(35) | `u_i = u_bar_i` on `Gamma_u`; `sigma_ij nu_j = t_bar_i` on `Gamma_t`; `sigma_ij nu_j = 0` traction-free, with `sigma_ij` the effective stress | the reduced classical boundary data |
| FEM_1 Eq (36) | `q_ijm = (1/10) L_mn C_ijkl eps_kl,n` | the double stress used throughout M8 |
| FEM_1 Eq (37) | higher-order natural condition `q_ijm nu_m nu_j = 0` on `Gamma_q` | the reduced double-traction data |
| FEM_1 Eq (38) | essential higher-order condition `u_i,nu = g_bar_i` on `Gamma_g` | the derivative DOF of the reduced set |
| FEM_1 Eq (39) | `L_mn d(sigma^cl_ij)/dx_n nu_m nu_j = 0` ("the factor 1/10 has been omitted since the boundary condition is homogeneous") | the reduced natural condition in the isotropic-length case |
| FEM_1 §4 close | "This condition represents the **reduced** higher-order natural boundary condition adopted in the present formulation." | the model is explicitly declared *reduced* |
| FEM_1 §4 close | "For the spherical case on a flat surface `x_3 = const` with `nu = (0,0,1)`, the conditions become `sigma_i3 = 0` and `d sigma^cl_i3/dx_3 = 0` … **This is a reduced Aifantis-type condition, not the full Mindlin–Toupin form with surface divergence, noted as a limitation.**" | the surface-divergence term is *named* and *explicitly excluded* |
| FEM_1 §5 | "In full Mindlin–Toupin second-gradient theory the variational principle yields surface tractions `t_i`, double tractions `r_i = q_ijm nu_m nu_j` and line forces `e_i = [[q_ijm nu_m mu_j]]` along edges where the normal `nu` is discontinuous … **Surface divergence and edge terms are neglected**, consistent with the phenomenological Aifantis-type model." | the exact terms are acknowledged as the general variational structure and deliberately neglected — i.e. the legacy formulation is the reduced model, and the neglect is stated as a limitation |
| FEM_1 §5 | "Higher-order conditions are of two types … **Essential**: `u_i,nu` … enforced through Hermite derivative DOFs … **Natural**: `q_ijm nu_m nu_j = 0` … **Natural conditions are satisfied variationally.**" | four quantities per direction, natural data satisfied variationally in the reduced model |

So the legacy `[C]` source used for the anchor-adjacent modelling is unambiguously the **reduced**
four-quantity model, with the neglect of the exact terms reported as a limitation. Blueprint v1.3
is consistent with it.

---

## 4. Conclusion (A) and the exact statement of the caveat

**Operational model of Paper 9 (recorded):**

```
(O1)  bulk            sigma_ij,j - tau_ijk,jk = rho( u_i_ddot - ell_i^2 u_i_ddot,jj )
(O2)  essential       u_i = u_bar_i        (classical)        ;  u_i,nu = u_i,j n_j = g_bar_i (higher order)
(O3)  natural         t_i^red := ( sigma_ij - tau_ijk,k ) n_j + rho ell^2 u_i_ddot,j n_j = t_bar_i
(O4)  natural (HO)    R_i := n_j n_k tau_ijk = R_bar_i          ; free: R_i = 0
(O5)  interface       u_i, u_i,nu continuous (essential) ; t_i^red, R_i continuous (natural)  [4 per direction]
(O6)  cell boundary   periodic pairs with Bloch phase on value and derivative DOFs (§4.4)
```

Time-harmonic: `u_i_ddot -> -omega^2 u_i`, so `t_i^red = ( sigma_ij - tau_ijk,k ) n_j - rho omega^2 ell^2 u_i,j n_j`.

**Documented mathematical caveat (retained from M8):** the *fully* variationally exact boundary
operator is

```
(C1)  t_i^exact = t_i^red - D_alpha( tau_ijk n_k a_j^alpha )     (flat face: - d_s q_i,  q_i = tau_ijk n_k m_j)
(C2)  e_i = [[ tau_ijk n_k a_j^alpha mu_alpha ]]                  (corner / line forces)
(C3)  free surface: t_i^exact = 0 and R_i = 0 and e_i = 0
```

The operational model (O3)–(O4) drops `(C1)`'s second term and `(C2)`. By (X4) this is a **model
reduction relative to the exact variational boundary operator** and must be stated as such in the
manuscript's limitations (it is not a rearrangement of the same model). Quantified: the dropped
term is non-zero for generic fields ([A2] smooth boundary, [A8]/[A9] cell edges, [A11] free-surface
condition), and vanishes identically only in special situations ([A9]: fields with `d_s q_i = 0`
along the edges, e.g. uniform-strain fields; [A13]: **in 1D**).

---

## 5. Mathematics of the two terms on the rectangular (and periodic) cell (questions 5, 6, 7)

**5.1 Smooth boundary (no corners).** On a closed smooth curve the exact operator carries
`- int (d_s q_i) v_i ds` with **no corner terms** ([A1], verified by exact trigonometric
integration on the unit circle). The dropped term is non-zero there ([A2]). So the tangential
term is **not** a corner artefact.

**5.2 Rectangular cell: exact decomposition.** Per edge, `int q_i d_s v_i ds + int (d_s q_i) v_i ds
= [q_i v_i]_start^end` ([A3]); globally the raw `tau`-boundary integral equals the canonical
`tau`-integral plus the four corner terms ([A3b]). The corner terms are therefore *exactly* the
endpoint pieces of the tangential integration by parts — they belong to the same reduced/neglected
family, not to a separate effect.

**5.3 Corner terms do not vanish on a rectangular cell.** For the cell corner `(1,0)` the corner
term is `q_i^(edge ending) - q_i^(edge starting) = -(tau_i12 + tau_i21)` ([A4]); it vanishes only
under the special condition `tau_i12 = -tau_i21`, which isotropy of the length tensor does not
imply ([A4b]: non-zero for the anisotropic case and for `L = ell_L^2 I`). The total corner sum for
a non-periodic field is non-zero ([A4c]). **No vanishing is assumed simply because the cell is
rectangular.**

**5.4 Periodic cell — cancellation is partial, and exact only in one-phase-zero directions.**
With the periodicity (Bloch-type) phase relation of the field,
`tau(x+1,y) = mu_x tau(x,y)`, `tau(x,y+1) = mu_y tau(x,y)`, the four edge quantities reduce to two
([A5]: `Q_l = Q_r = +tau_i21`, `Q_t = Q_b = -tau_i12`), and the four corner terms give the exact
closed form

```
(K1)  sum_corners = ( tau_i12 + tau_i21 ) ( 1 - mu_x ) ( 1 - mu_y )            [A7, exact]
```

- `mu_x = mu_y = 1` (Γ point, i.e. exact periodicity): **telescoping cancellation**, `sum_corners = 0`
  exactly ([A6]).
- `mu_x = 1` or `mu_y = 1`: `sum_corners = 0` exactly — the Γ point, and the whole Γ–X leg of the
  Γ–X–M–Γ path, where `k_y = 0` hence `mu_y = 1`.
- otherwise — the Γ–M and X–M legs (in particular at X and M, where `mu_x = -1`, `mu_y = -1` resp.
  `mu_y = 1` only at X): `sum_corners != 0` (at X the cancellation comes from `mu_y = 1`).

So on the rectangular Bloch cell the corner terms **neither vanish identically nor are they
negligible**; they cancel only along the phase-zero segments. Under the operational model (O3)–(O6)
they are omitted *by specification* (documented reduction), not because they vanish.
*(The phase relation above is used only as a periodicity property of the field; the M9 Bloch
formulation is not derived here.)*

**5.5 Can the tangential redistribution be omitted without changing the model?** No. Omitting it
changes the free-surface natural condition ([A11]: exact `t_i^red - d_s q_i = 0` vs reduced
`t_i^red = 0`) and changes the boundary integrand by a non-zero amount ([A8]). Omitting it is
therefore a **model reduction** (exactly what `[C]` calls a "reduced Aifantis-type condition …
noted as a limitation"), and it must be stated. It is *not* merely a rewritten form of the same
boundary operator.

---

## 6. Consequences (questions 5, 8)

**6.1 What the planned computations actually use.** Case H and Case C are Bloch-periodic unit
cells: by blueprint §4.4 the cell boundary carries Bloch conditions on value and derivative DOFs;
**no free surface and no prescribed natural data are present on the cell boundary** (blueprint
lines 179, 402). The element matrices are assembled from the **volume** weak form, which is
**identical in both formulations**; the boundary terms (exact or reduced) are not assembled.
Therefore, for the planned Case H/C computations, the M8-a distinction does **not** change the
discrete equations. This is a scope statement about what M13/M15 assemble; it is not the M9
derivation, and it holds only while the cell has no free boundary and no boundary traction is
post-processed.

**6.2 Where the distinction would matter.** (i) Any free-surface computation (none planned);
(ii) any extraction of boundary tractions/double tractions from the solution (would need the
exact `t_i` or a stated reduced convention); (iii) the 2D/3D legacy comparison beyond the 1D
anchors (the legacy model is reduced, so a like-for-like comparison is reduced-vs-reduced — which
is what (O3)–(O4) provides).

**6.3 M13/M15 (C¹ BFS implementation) — sufficiency of the reduced four-quantity model: yes.**
- The BFS element provides `{u, u_,x, u_,y, u_,xy}` per node per component (blueprint §4.1); on a
  straight face `u_i,nu = u_i,x nu_x + u_i,y nu_y` is available, `R_i` and `t_i^red` are natural
  data, hence the **four quantities per direction** (O2)–(O4) are realisable;
- the four interface conditions (O5) map onto shared edge DOFs — consistent with blueprint
  line 421 and with M8 checks C16/C17;
- the Bloch master–slave reduction (`d_slave = T(k) d_master`, phase on value **and** derivative
  DOFs) is defined on value/derivative DOFs, as the reduced model requires;
- the exact model would additionally require corner/line-force data (`e_i`, generically non-zero
  by [A4]), i.e. point data beyond the DOF layout — another indication that the blueprint's
  operational model is the reduced one.

**6.4 What M13/M15 must implement (recorded, not started).** Nothing changes in the planned
element, assembly or reduction steps. The only additions are bookkeeping obligations:
(i) the reduced free-surface conditions (O3)–(O4) must be used verbatim **if** any free-surface
case is ever added (none is planned in 5a–5i), and (ii) the manuscript's limitations must state
the reduction (surface divergence / edge terms neglected; exact operator (X1)–(X2) is the full
Mindlin–Toupin structure), together with the periodic-cell cancellation result (K1) as the precise
statement of *when* the omission is exact on a periodic cell (the Γ point and the Γ–X leg, where
`mu_y = 1`).

---

## 7. Checks performed (question: explicit symbolic checks; all executed, all passed)

| # | Check | Result |
|---|---|---|
| A1 | smooth-edge boundary identity: `int_C q_i d_s v_i ds = - int_C (d_s q_i) v_i ds` on the circle, exact trigonometric integration, **no corner terms** | PASSED |
| A2 | non-vanishing certificate on the smooth boundary (dropped term is a non-zero expression in `lambda, mu, L11, L12, L22`) | PASSED |
| A3 | rectangular-cell per-edge endpoint identity `int q d_s v + int (d_s q) v = [q v]_start^end`, all four edges, CCW convention | PASSED |
| A3b | global decomposition: raw tau-boundary = canonical tau-boundary + corner sum | PASSED |
| A4 | corner term at (1,0) `= -(tau_i12 + tau_i21)` in abstract components; vanishes only for `tau_i12 = -tau_i21` | PASSED |
| A4b | field-based certificate: corner term non-zero for anisotropic `L` **and** for `L = ell_L^2 I` | PASSED |
| A4c | total corner sum non-zero for non-periodic (reduced) boundary data | PASSED |
| A5 | edge-quantity identities `Q_l = Q_r = +tau_i21`, `Q_t = Q_b = -tau_i12` | PASSED |
| A6 | exact periodicity (`mu_x = mu_y = 1`): corner terms cancel telescopically | PASSED |
| A7 | closed form `sum_corners = (tau_i12 + tau_i21)(1 - mu_x)(1 - mu_y)`; cancellation iff one phase is unity (Γ point, Γ–X leg); non-cancellation for generic phases (interior of Γ–M and X–M, and at X, M) | PASSED |
| A8 | model-reduction quantification: (exact − reduced) boundary term `= - sum_edges int (d_s q_i) v_i ds + sum_corners` and non-zero for non-uniform fields | PASSED |
| A9 | tangential term vanishes iff `d_s q_i = 0` (uniform-strain certificate) and is non-zero otherwise | PASSED |
| A10 / A10b | `[C]`-consistency: reduced `t_i^red = 0` ⟺ `(1 - (ell_L^2/10) Lap) sigma^cl_ij n_j = 0` (FEM_1 (34)/(39)); reduced `R_i = 0` ⟺ `q_ijm nu_m nu_j = 0` (FEM_1 (37)) | PASSED |
| A11 | exact and reduced free-surface conditions differ by exactly `d_s q_i` (non-zero) | PASSED |
| A12 | boundary-data count: four quantities per direction vs the additional (fifth) corner datum of the exact model | PASSED |
| A13 | 1D: no tangential/corner terms exist, so exact = reduced identically (relevant to the 1D anchor comparisons) | PASSED |

**17 checks, all PASSED.** Script `scripts/audit_m8a_boundary_operator.py`
(sha256 `55fdc22fad799fd5608722ee1f783cbe859e38ef69c48e925492d49b7f6b0dce`),
log `checks/audit_m8a_boundary_operator.log`.

**Failures encountered and fixed during the audit (kept for traceability).** (1) The
circle-based check initially used the double stress evaluated at `(x,y)` instead of on the
circle, giving an `x`-dependent "identity" — fixed by substituting the parametrisation before
forming `q_i`. (2) The corner/periodicity checks were first written with field-derived
components (expressions) rather than independent abstract components, so the substitution-based
vanishing tests were meaningless — fixed by introducing abstract `tau_ijk` components with the
single symmetry `tau_ijk = tau_jik`. (3) The corner phase factors were initially assigned
per vertex instead of per field point (`mu_x` on both edge quantities at `(1,0)`, `mu_x mu_y` at
`(1,1)`, `mu_y` at `(0,1)`), which produced a wrong closed form; corrected and verified exactly,
giving (K1).

---

## 8. Recorded outcome, notes and dependencies

- **M8-a — RESOLVED, interpretation (A).** Operational model = reduced four-quantity boundary
  set (O1)–(O6). Exact variational boundary operator (X1)–(X2) retained as a documented
  mathematical caveat; the reduction must be stated in the manuscript limitations.
- **M8-a-1 (new, recorded).** Periodic-cell corner-term behaviour: `sum_corners = (tau_i12 +
  tau_i21)(1 - mu_x)(1 - mu_y)`; cancellation at the Γ point and along the phase-zero path
  segments only. Informational for M15 (the effects are omitted in the operational model, but the
  statement documents *when* the omission is exact).
- **M8-c, M8-d** (body-force convention, `q_ijm == tau_ijk` notation) unchanged.
- **No new TV dependency.** Audit fully symbolic; no parameter value, no k-point, no band count.
- **No blueprint modification.** No M1–M7 mathematics altered. No solver/Bloch code touched.
  M9 not started.

## 9. Traceability

| Object | Source | Record | Checks | Status |
|---|---|---|---|---|
| M8-a boundary-operator question | blueprint §2.8 (line 357), register (570–571), risk table (421); FEM_1 §4–§5 | this record; `DERIVATION_M08.md` note M8-a | `scripts/audit_m8a_boundary_operator.py`, `checks/audit_m8a_boundary_operator.log` | RESOLVED — interpretation (A) |
| operational boundary model | derived from the above evidence | this record §4 (O1)–(O6) | A10, A10b, A11, A12 | LOCKED for M13/M15 (no blueprint edit) |
| exact boundary operator (caveat) | M8 (X1)–(X2) | `DERIVATION_M08.md` §M8.3 (unchanged) | A1, A3, A3b, A8 | retained as caveat |
