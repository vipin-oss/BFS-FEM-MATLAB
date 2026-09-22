# PHASE-1 MANIFEST (living record — updated at each Phase-1 milestone)

Status: **IN PROGRESS (Phase 1)** — no scientific PASS claimed.

## 1. Git
| Field | Value |
|---|---|
| Branch | `phase-1-symbolic` |
| Base commit (Phase 0 LOCK) | `175ea9e6a5927e52f222b60b4b9acbe498162ac5` |
| Phase-1 setup commit | `7112eb8` (eqs/phase1 package + M1–M17 formulation plan) |
| This milestone commit | recorded in the commit that adds this file; the manifest is re-hashed and re-committed whenever a module status changes |
| Remote | `origin` = `https://github.com/vipin-oss/BFS-FEM-MATLAB.git` (push status recorded in the milestone commit message / final report) |

## 2. Governing inputs (read-only, hashes)
| File | sha256 |
|---|---|
| `paper9/plan/blueprint/Paper9_Blueprint_v1.3.tex` | `ca71b91aba4ca4abe9f157eb595ac8c2f709d838957a08ea0dce7160685dbf9f` |
| `paper9/plan/blueprint/Paper9_Blueprint_v1.2.tex` (frozen) | `742acc9e…fe9c` (full hash in `plan/blueprint/PROVENANCE.md`) |
| `paper9/plan/CALC_MASTER_PLAN.md` v1.1 | tracked in git; see commit history |

Legacy [C] sources used (read-only, outside the repo): `femcheck/FEM_Total/ptxt/FEM_1_Paper.txt`,
`FEM_2_Paper.txt`, `FEM_3_Paper.txt` (quoted by equation number in the derivation notes).

## 3. Phase-1 source files (status: DRAFT/IN PROGRESS; hashes below)
| File | sha256 | Purpose |
|---|---|---|
| `scripts/m01_m02_length_tensor.py` | `feca32ddfd251d91e17d97a25d2217847065c40a97b0fc411c2b92a1ed649ae8` | M1+M2: averaging, second moments, rotation, mixed term (blueprint (1)–(9), part of (25)) |
| `scripts/m03_kinematics.py` | `60da747ea55a37e298d55a0b2f0da350d2dc366abda41904f06ab0994afd638d` | M3: kinematics, counts, compatibility ((10)–(12)) |
| `scripts/m04_form2_constitutive.py` | `ce830e76fb84070b547475286aebd639560b891997007d7fb18432465622c722` | M4: Form-II constitutive, five-constant relation, symmetries, PD ((13)–(18)) |
| `scripts/m05_micro_inertia.py` | `9516429628a6d92b53246aefbf088ee230546cdd661ee982c3bf21c43e9b64af` | M5: micro-inertia, inertial operator, time-harmonic reduction ((19)–(21)) |
| `scripts/m06_energy_definiteness.py` | `93137f55f7659b824ef0da18d8bda361f82f2769ed6c6202b12525e60eaea35a` | M6: energy, PD identities, `K_g` assembly ((22)–(26)) |
| `scripts/m07_limit_ladder.py` | `c4b31a3395e12856b74a21a3cc3f41b715a3d21544e24d0dd45cce1f2d20c93e` | M7: limit ladder ((27)–(30)) |
| `derivations/DERIVATION_M01_M07.md` | `8d17fa1ff3aa6cb28814942a4dcbcde264f80acfdec50368c7ba77bfaaadebec` | M1–M7 derivation + mathematical audit + notes F1, F2, M5-a, M7-a/b, N-1, N-2 |
| `scripts/audit_f1_five_constant.py` | `41e3a32fa31aa6a83653caf13d633d7b0a8d934c7ed90ffcd8f7ad7890bc19ee` | F1 audit: isotropic representation, non-representability certificates, plane-strain identifiability, FEM_3 (84)–(85) |
| `derivations/AUDIT_F1_five_constant_vs_tensor_modulus.md` | see git | F1 audit record (RESOLVED, interpretation (A)) |
| `scripts/m08_strong_form.py` | `02a89ea982cd24c0a79b47b2e94eb3b6e05aa924b18c03f584e7987bb5ff3e7f` | M8: strong form (31), boundary/interface terms (32)–(35), micro-inertia boundary term, limit reductions, dimensional audit |
| `derivations/DERIVATION_M08.md` | `4066e46e2f19602d97a4d749af0dda0c49be035eb83019598255650326333565` | M8 derivation + audit record (25 checks; notes M8-a (now RESOLVED), M8-c, M8-d) |
| `scripts/audit_m8a_boundary_operator.py` | `55fdc22fad799fd5608722ee1f783cbe859e38ef69c48e925492d49b7f6b0dce` | M8-a audit: tangential redistribution, corner/line forces, rectangular- and periodic-cell behaviour, model-reduction quantification |
| `derivations/AUDIT_M8a_boundary_operator.md` | `6d20c4e8fbf31f2ad208f76f271267d2365ce0fd9378d36ecfec705c4f7e9379` | M8-a audit record (RESOLVED — interpretation (A): reduced four-quantity model operational; exact operator retained as caveat) |
| `scripts/m09_bloch_c1.py` | `c5980f4d9d60141ca3c859c6a07ec4fb9e49b37472e5664118a2e8689f228ace` | M9: unit cell/lattice/reciprocal lattice/first BZ (36)–(38); Bloch ansatz and the DERIVED phase rules (39)–(43); consistency with the reduced four-quantity model, anisotropic (26), M7 ladder, phase lemma; forward check of blueprint (68) |
| `derivations/DERIVATION_M09.md` | `15235d1ae244cbf168fde6e7fa1ac486e7a835b6fefff71a4f1569677546d60f` | M9 derivation + mathematical audit record (45 checks; notes M9-a…M9-g; M15-a flagged, not repaired) |
| `scripts/audit_m15a_eq68_identity.py` | `590268236408fead836d878bd58e3748a9238c61c66c905092f6d8e77fede8dc` | M15-a audit/ruling on blueprint (68): independent re-derivation of the reduced-matrix identities, independent counterexample check, wrong-sign phase detectability, options (a)/(b)/(c) |
| `derivations/AUDIT_M15a_eq68_identity.md` | `fde0cb231fcf3a4b25038c1b4a42368ed8b98b5bcccfa86a2681006ccd4a1850` | M15-a ruling record (RESOLVED — option (a)); proposed blueprint amendment recorded, NOT applied; M9 erratum register |
| `scripts/audit_m15a_hermiticity_test.py` | `bd801ef3a0ac1365e27f6be90826252852704f129805aa3f2d0d5b711580e505` | M15-a SECOND, independent audit (different models: 6-DOF three-phase pattern; C¹ Hermite cell derived from shape functions; sesquilinear vs bilinear envelope matrices; missing-phase variant; T1–T4 test structure incl. the finding that the 5d long-wave slope is blind and that the Bloch-wave consistency test T3 detects the sign error) |
| `derivations/AUDIT_M15a_hermiticity_test.md` | `8fd4ff367760362bb082214c73ada25e92994ba9dce75ce104536a3fab4eab97` | M15-a second audit record — concurs with ruling (a); proposed v1.4 wording for lines 403/416/587/row 5a; NOT applied |
| `scripts/m10_ibz_path.py` | `ed2707064151d4bc5a953cc23d7f1b880ff90d54c544a3a572cf81a51a2ad0ab` | M10: path (44) parametrised/sampled (N_seg symbolic = TV4); Case-H dispersion derived from (O1)+(26)+M9 ansatz; symmetry group vs (theta, AR); irreducible zone; M15-a pair = k-evenness; M7 ladder; M7-b re-check |
| `derivations/DERIVATION_M10.md` | `4081f9ffbff6e7fd977a1ca111210bd8e55e36aea5741de08ba4d4d6d37760b7` | M10 derivation + audit record (23 checks; FLAG M10-a: Γ–X–M–Γ is the IBZ boundary only for AR = 1 — ruling required) |
| `scripts/audit_m10a_ibz_scope.py` | `221f06b098f84dd0074c49d4aa920f43219452ea949766e49670834c24d3cc0b` | M10-a audit: independent symmetry-group/irreducible-zone derivation, fundamental-domain cover tests, path-vs-zone extremum mismatch (exact), option screening (a)/(b)/(c) |
| `derivations/AUDIT_M10a_ibz_scope.md` | `878e1a29d0b8f6945f0594c140befb0ec477117435aedae00547f9c06873e781` | M10-a record: RULING (a); affected blueprint text; three-way gap taxonomy; required sampling; proposed v1.4 amendment (NOT applied); M11 may proceed, M12 blocked on amendment |
| `scripts/m11_nondim.py` | `ff8cec8a6f025f7133e27025d734738724fa548f70e1815660858f2b4faa0b1d` | M11: (45)-(47) units; dimensionless operator H̄ and barred Case-H dispersion derived; v̄, v_g scaling; M9/M10/M10-a/M15-a consistency under scaling; limits; anchor A/B scheme mapping |
| `derivations/DERIVATION_M11.md` | `3c519ffb2b2ef0d363c4ac0e2bbac625f5da5580d22b068905bbd2cf98578d87` | M11 record (18 checks; new TV14 = which μ,ρ,L define ω₀ in Case C; TV15 = branch/direction in v̄; bar-notation clash (45)-(47) vs (66) recorded) |
| `scripts/m12_observables.py` | `aebef5a5a2245377919509b1c996bccee599a394a0fec9dd838473de978f5180` | M12 (executable part): (48) band-function properties; (49) gap definitions/monotonicity/invariances (no values, no sampling protocol); (50)-(51) velocities, deviation angle; (52) energy balance + flux DERIVED, v_g = <S>/<W+T> exact on Case-H wave |
| `derivations/DERIVATION_M12.md` | `9518b1c423ffb1f3caab57a47c1b36ef336caa9f38c0b5e4ee726748e15c6505` | M12 record: PARTIAL — (49) sampling protocol BLOCKED (no authorisation for M10-a amendment in repo); TV16 opened; micro-inertia flux term found in (52) |
| `scripts/m13_bfs_shape.py` | `a23ad732882dd6ea89b22bf525fa725f9af3ef7f34e8840b2057df7eff0ffa8c` | M13: BFS bicubic Hermite (53) Kronecker/completeness/Q3; (56) 32-DOF layout, C¹ traces incl. mixed DOF, H² conformity; (54)-(55) B, B_,i from M3 kinematics, null spaces, degrees; units, affine map; M9 phase on all DOF types verified at Γ, X, M, generic k + negative controls; assembly counting |
| `derivations/DERIVATION_M13.md` | `162dad09c823d27f80a1de32a04b632924d05dc955aeeeb63362cc65ce6e61dd` | M13 record (24 checks; TV17 DOF ordering, TV18 rectangular-mesh/inclusion representation; note for M14: integrand degree 6 per direction, not 'quartic') |
| `scripts/m14_element_matrices.py` | `b4c7a10be70d370699759a838b1ee5030840a8dca8b3a6f1918d1dd8e8962d57` | M14: K^c, K^g, M0, M^g, M from M8.2; 4×4 Gauss (degree 6); real 32×32 pre-Bloch |
| `derivations/DERIVATION_M14.md` | `d874958d672f3e088359a8dbf2532d5a562df38707505405968a9ac023e61644` | M14 record (24 checks; TV17/TV18 open; no Bloch; blueprint quartic rule overruled) |
| `scripts/m15_bloch_reduction.py` | `1b062c0a20ec09f4f0fb5ea5fc4014d45ae30b8f9f068ed5088467e624dcb7d3` | M15: T(k) 32x8, Kbar=T^H K T, M15-a pair, false (68) interior residual, phase-sensitive negative controls |
| `derivations/DERIVATION_M15.md` | `30dbffdca763666fe5c08e89413e443562b12da024986c2ccc94a0a12678614c` | M15 record (25 checks; blueprint (68) not edited; TV17 open) |
| `scripts/m16_asymptotics.py` | `3a24639222efa6fba6282e8396cfa6617200ad09907ff990112efaa88068359b` | M16: App A (A.1)-(A.6) high-kbar Case-H asymptotics |
| `derivations/DERIVATION_M16.md` | `2e51ef7af52460bbe2f27cf81c12f36ac853528779864ca6c6e53d14c2b16b80` | M16 record (17 checks; bounded/unbounded; directional l_eff; L/T ratio) |
| `checks/*.log` | generated by the scripts (see §4) | captured stdout of each run; never hand-edited |
| `PHASE1_FORMULATION_PLAN.md` | see git | module map M1–M17, acceptance mapping, TV policy |

## 4. Checks actually performed (this milestone)
| Script | Checks | Result | Log |
|---|---|---|---|
| `m01_m02_length_tensor.py` | 19 | PASSED | `checks/m01_m02_length_tensor.log` |
| `m03_kinematics.py` | 9 | PASSED | `checks/m03_kinematics.log` |
| `m04_form2_constitutive.py` | 20 | PASSED | `checks/m04_form2_constitutive.log` |
| `m05_micro_inertia.py` | 7 | PASSED | `checks/m05_micro_inertia.log` |
| `m06_energy_definiteness.py` | 11 | PASSED | `checks/m06_energy_definiteness.log` |
| `m07_limit_ladder.py` | 10 | PASSED | `checks/m07_limit_ladder.log` |
| `audit_f1_five_constant.py` (F1 audit) | 34 | PASSED | `checks/audit_f1_five_constant.log` |
| `m08_strong_form.py` (M8) | 25 | PASSED | `checks/m08_strong_form.log` |
| `audit_m8a_boundary_operator.py` (M8-a audit) | 17 | PASSED | `checks/audit_m8a_boundary_operator.log` |
| `m09_bloch_c1.py` (M9) | 45 | PASSED | `checks/m09_bloch_c1.log` |
| `audit_m15a_eq68_identity.py` (M15-a) | 37 | PASSED | `checks/audit_m15a_eq68_identity.log` |
| `audit_m15a_hermiticity_test.py` (M15-a, second independent audit) | 30 | PASSED | `checks/audit_m15a_hermiticity_test.log` |
| `m10_ibz_path.py` (M10) | 23 | PASSED | `checks/m10_ibz_path.log` |
| `audit_m10a_ibz_scope.py` (M10-a) | 26 | PASSED | `checks/audit_m10a_ibz_scope.log` |
| `m11_nondim.py` (M11) | 18 | PASSED | `checks/m11_nondim.log` |
| `m12_observables.py` (M12, executable scope) | 22 | PASSED | `checks/m12_observables.log` |
| `m13_bfs_shape.py` (M13) | 24 | PASSED | `checks/m13_bfs_shape.log` |
| `m14_element_matrices.py` (M14) | 24 | PASSED | `checks/m14_element_matrices.log` |
| `m15_bloch_reduction.py` (M15) | 25 | PASSED | `checks/m15_bloch_reduction.log` |
| `m16_asymptotics.py` (M16) | 17 | PASSED | `checks/m16_asymptotics.log` |
| **Total** | **443** | **ALL PASSED (symbolic)** | — |

Scope of these checks: internal mathematical consistency (indices, signs, tensor
contractions, symmetries, dimensions) and blueprint traceability. They are **not** numerical
verification (tests 5a–5i, Phase 4A), **not** published-benchmark validation (Phase 3), and
**not** scientific results.

Failures encountered and fixed during this milestone (kept for traceability): missing `det A`
volume element in the moment integral; SymPy sequential `dict` substitution masquerading as a
swap (fixed with `simultaneous=True`); monomial bookkeeping with `as_coefficients_dict` mixing
parameters into keys (fixed with `Poly` in the `eta` variables); unconstrained (non-symmetric)
`L` symbol matrix (fixed: `L = L^T` is a property of `A A^T`); plane-strain regrouping applied
to full 3D `eta` (fixed: out-of-plane components set to zero); the off-diagonal pair factor
(F2) appearing in the energy/derivative/assembly identities.
M8 additions (same paragraph, for traceability): the Lagrangian (rather than d'Alembert)
inertial sign does not reproduce (31) -- fixed by the exact identity; the raw boundary term
must differentiate `tau_ijk` with respect to the **third** (`k`) index -- `tau_ijk,k n_j` --
otherwise the IBP identity fails for 48 of 50 test fields (found by the 2D check, fixed,
re-verified for all 50 fields and all four edges); SymPy `subs` does not replace an
expression inside its own derivatives (the time-harmonic check builds `u_ddot = -omega^2 u`
as a field instead); the gradient-component generator needs the `(2,1) -> (1,2)`
independent-pair mapping.
M9 additions (same paragraph, for traceability): the first-BZ equality set contains 8 pairs
(4 binding facets +-b_1, +-b_2 and 4 corner touches +-b_1+-b_2), not 4; symbolic Relational
comparisons on affine-in-t bounds are replaced by endpoint + convexity + rational-grid
checks; the k-shift SIGN at the uniform envelope q = 0 is unobservable (an even-order
operator), so sign controls must use q != 0.
M15-a additions (same paragraph, for traceability): a symbolic 16-DOF charpoly model is
intractable (switched to an 8-DOF model, 4 nodes x {u, u_x}); an integer K pattern can cancel
Im(K-bar) accidentally at an interior k-point ((5i+3j+7) mod 9 - 4 is real at (pi, pi/5)), so the
pattern was changed to (7i+3j+2) mod 11 - 5 after testing five candidates; the wrong-sign determinant
detector needs sv - q^2 != 0 (v = 1/2 with s = 2, q = 1 cancels).

## 5. Parameter / provenance status
No numerical parameter value is introduced in Phase 1. All quantities are symbolic:
`lambda, mu` [C/PROVISIONAL — value = TV6], `l1, l2, l3` [S-prod — TV6], `ell` [S-prod/C-anchor — TV6],
`rho` [C per phase — TV6], `theta` [S study variable], `AR = l1/l2` [S study variable],
`L` (cell size) [S — TV6]. Every symbol is documented in the derivation notes with its tag.

## 6. Software / environment
| Item | Version |
|---|---|
| Python | 3.13.14 |
| SymPy | 1.14.0 (exact arithmetic) |
| NumPy | 2.3.5 (environment check only; not used in Phase 1) |
| SciPy | 1.17.1 (available; not used in Phase 1) |
| LaTeX | pdfLaTeX, TeX Live (used for blueprint v1.3 compile check in Phase 0) |

Language rule (recorded in the plan as a rule-7 decision, pending user lock): blueprint allows
"MATLAB R20xxb / Python 3.x"; this environment has no MATLAB, so Phase 1 uses Python 3 +
SymPy. No MATLAB-only artifact is produced.

## 7. TV dependencies (unresolved — none resolved, none guessed)
| TV | Required by | Phase-1 status |
|---|---|---|
| TV1, TV2, TV8, TV9, TV12 | Phase 3 anchor work | NOT NEEDED in M1–M7 |
| TV4 (k-points per IBZ segment) | M10 | M10 done with N_seg SYMBOLIC; value still unresolved, not guessed; interacts with M10-a |
| TV6 (Case H/C production parameters) | M11, M14 | M11 done symbolically; TV6 still open |
| TV14 (NEW, M11) which phase's μ, ρ and which length L define ω₀, v̄ in Case C; per-phase l_m, ℓ_i? | M11 → M12, M15, P5 | open; lock with TV6 |
| TV15 (NEW, M11) v̄ per branch and per direction k̂ (anisotropic phase vs group velocity) | M11 → M12, §7.2 | open; M12 P1 confirms scalar k insufficient; no definition chosen |
| TV16 (NEW, M12) S_θ: angle unit (per rad / per deg), difference scheme on the 7-point θ grid, and which gap (complete/directional) enters | M12 → P5, Table 5 | open |
| TV17 (NEW, M13) element/global DOF ordering and node numbering (not fixed by §4.1); provisional: index = 8(node−1)+4(comp−1)+type, type∈{u,u,x,u,y,u,xy} | M13 → M14, M15 code | open (bookkeeping) |
| TV18 (NEW, M13) BFS needs axis-aligned rectangles (no isoparametric map): representation of the Case-C circular inclusion (material at Gauss points / area fraction) | M13 → M14, §5.7, TV6 | open |
| TV7 (band count `N`, spurious filter) | M12, M15 | forward dependency; not needed yet |
| TV10, TV11 | Phase 2/3 (Anchor D, PB2009/LWZ2016) | not needed in Phase 1 |
| TV13 (`eps_Delta` wording) | Phase 4B | not needed in Phase 1 |

## 8. Open formulation notes (recorded, not decided)
- **F1 — RESOLVED (2026-09-22)** five-constant presentation vs factorized (26) modulus: the
  blueprint's five constants are its explicitly labelled *isotropic* family (lines 300, 353, 355,
  356, 561, 562); the implemented anisotropic model is (26); the two coincide exactly in the
  isotropic-length sub-case with `(a₁…a₅) = (0,0,λℓ²/20, μℓ²/10, 0)` (independently re-derived,
  729/729 component comparison). Legacy FEM_3 (84)–(85) is a *different* member of the same
  isotropic family and is never equal to the isotropic limit of (26). New finding: in plane
  strain the combination `a₁ − 2a₂ + a₃ − a₄ + a₅` is not identifiable (restricted family rank
  4 of 5). See `derivations/AUDIT_F1_five_constant_vs_tensor_modulus.md`.
- **F2** symmetric-pair factor conventions (explicit `K_g` form for M14).
- **M5-a — FULLY DISCHARGED (M8 operator level 2026-09-22; Bloch phase in M9 2026-09-22)**: the
  free micro-inertia term `rho ell^2 u_i_ddot,j n_j` enters the **classical-traction slot** of the
  boundary operator with a `+` sign (time-harmonic: `-rho omega^2 ell^2 u_i,j n_j`); it is conjugate
  to the value DOF, not to the derivative DOF, and there is no inertial contribution to the
  double-traction slot. M9 closed the remaining obligation: the term inherits the phase factor
  `mu_alpha` from `u_i,j` and its conjugate DOF (value) carries the same `mu_alpha`, so its discrete
  contribution needs no separate phase rule (M9 checks [C4], [C5]). No residue remains.
- **M8-a — RESOLVED 2026-09-22 (audit `AUDIT_M8a_boundary_operator.md`, 17 checks): interpretation
  (A).** Blueprint v1.3 specifies the **reduced four-quantity boundary model** as the operational
  paper model (evidence: §2.8 line 357 enumerates exactly four quantities per direction and defines
  only `R_i`; register (32)–(35) names only `R_i`; risk table line 421 treats the count of four as
  complete; the 32-DOF BFS layout carries no corner/line-force datum). The **exact** variational
  boundary operator (tangential redistribution `-d_s q_i`, corner forces `e_i = [[q_i]]`) is retained
  as a documented mathematical caveat: dropping it is a **model reduction** (non-zero effect verified
  for generic fields), it must be stated in the manuscript limitations, and it coincides with the
  reduced operator in 1D. Scope: for the planned Bloch-periodic cells there is no free surface and no
  prescribed natural data, so the assembled volume weak form — and therefore M13/M15 — is unaffected.
  Operational model: audit §4, equations (O1)–(O6). No blueprint edit.
- **M8-a-1 (new, recorded)** periodic-cell corner-term behaviour: `sum_corners = (tau_i12 +
  tau_i21)(1 - mu_x)(1 - mu_y)`; exact telescoping cancellation iff `mu_x = 1` or `mu_y = 1`, i.e. the
  Γ point and the whole Γ–X leg (`k_y = 0`); non-zero on the Γ–M and X–M legs and at M. Informational
  for M15.
- **M15-a — RESOLVED 2026-09-22, ruling (a) (audit `AUDIT_M15a_eq68_identity.md`, 37 checks).**
  Blueprint (68) `K-bar(k) = K-bar(-k)^H` is NOT an identity of the operational formulation: with the
  tying route prescribed by Sec 4.4 the two unconditional identities are `K-bar^H = K-bar` and
  `K-bar(-k) = conj(K-bar(k))`, hence (68) is exactly equivalent to the extra hypothesis "`K-bar` is
  real" — true only on a measure-zero set of k (`k.dx in pi*Z` for every coupled pair; it passes at
  Gamma, X, M and fails on the interior of every IBZ leg). Ruling: replace (68) conceptually by the
  pair and re-base the Sec 4 test on it, supplementing it with an independent phase/sign validation
  (structural per-node phase ratio, tying-column membership / field-level derivative relation, and a
  reference comparison at a generic interior k). The wrong-sign derivative-DOF phase is NOT caught by
  Hermiticity or by k-evenness (both hold for it) although it changes the admissible subspace and the
  spectrum; it IS caught by the supplemented tests. The 1e-12 pitfalls test is therefore
  SUPPLEMENTED, not retained unchanged and not deferred. Proposed amendment text is recorded in the
  audit doc (Sec 4.5 clause + pitfalls row) — **the blueprint is NOT edited**. Second finding
  (erratum M15-a-E1): `DERIVATION_M09.md` §M9.8 item 1 prints the counterexample closed form with the
  opposite overall sign; no M9 conclusion or number is affected, and the M9 files were left untouched.
  **No M10 work started.**
- **M15-a — second independent audit 2026-09-22 (`AUDIT_M15a_hermiticity_test.md`, 30 checks): CONCURS,
  ruling (a).** Different models, no code shared with the first audit: (i) identities (I1)–(I7) on a 6-DOF
  pattern with all three phase types, explicit `Im K̄_01 = K04 sin θ2 − K13 sin θ1 − K34 sin(θ1−θ2)`;
  (ii) counterexample `9 / 8 / 2√2/3` reproduced exactly and by NumPy (`0.942809041582`); (iii) a 1D C¹
  Hermite gradient-elastic cell *derived from its shape functions* is Hermitian + conjugation-symmetric but
  NOT real — the literal (68) fails for a correct C¹ assembly (O(1) residual, zero only at Γ); (iv) the
  sesquilinear envelope matrix has the same structure as the tying route, only the non-Hermitian *bilinear*
  one satisfies (68); (v) wrong-sign AND missing derivative phases preserve Hermiticity, conjugation,
  k-evenness, BZ periodicity, coincide with the correct tying at Γ (wrong sign also at X); (vi) NEW: the
  long-wave slope test 5d is blind to them (relative error < 1e−6 at kh = 1e−3), whereas the internal
  Bloch-wave consistency test T3 (`T(k) d_master = d_full` for the interpolated plane wave; exact residual
  `ik(μ⁻¹−μ)`) and the Layer-3 dispersion at interior k (errors 8e−2 vs 1e−7 at kh = 0.3) detect them.
  Proposed blueprint wording in that record §7 (lines 403, 416, 587, row 5a). NOT applied.
- **M10-a — RESOLVED 2026-09-22, ruling (a)** (`AUDIT_M10a_ibz_scope.md`, 26 checks): path (44) kept for band
  diagrams and partial/directional gaps; complete gaps defined over the irreducible zone of the actual
  symmetry group (half-BZ grid valid for all cases). Blueprint v1.4 amendment proposed (terminology +
  sampling protocol, no model change) — NOT applied, authorisation pending. M11 may proceed; M12 blocked
  until the amendment is authorised. TV4 now has two parameters (N_seg, N_k), both open. Original flag: the path
  Γ–X–M–Γ of blueprint (44) is the IBZ boundary only for AR = 1. Derived exactly from the locked
  operator (Case-H dispersion, factor `1 + k·L·k/10`): symmetry group C4v (AR=1), C2v (θ ∈ {0,45,90}°,
  AR≠1), {I,−I} (generic θ); irreducible zone |BZ|/8, /4, /2. Partial gaps along the path remain
  well defined; *complete* gaps "over the whole IBZ" (§3.5/(49), M12; design map §6.6; Table 5) are not
  captured by the path for AR ≠ 1; test 5e must be stated as ω(θ+90;l1,l2) vs ω(θ;l2,l1) on the same
  path (or vs ω(θ;l1,l2) on the R90-rotated path). Options (a)/(b)/(c) in `DERIVATION_M10.md` §M10.6.
  M7-b discharged for Case H; conditional on a C4-invariant cell for Case C.
- **M8-c** body-force convention (blueprint (31) has none; FEM_1 Eq (22) carries `P_i` with a `+`
  sign). Phase 1 uses no forcing -- informational only.
- **M8-d** notation: FEM_1 writes the double stress `q_ijm`; the M1–M7 mapping `q_ijm == tau_ijk`
  holds (no blueprint notation altered).
- **N-1** `ell_i` treated as a scalar micro-inertia length.
- **N-2** `1/10` (3D) coefficient retained in 1D/2D reductions (blueprint/[C] choice).
- **M7-b** spectrum-level 90° symmetry requires a cell-invariant geometry (re-check in M10/M15).
