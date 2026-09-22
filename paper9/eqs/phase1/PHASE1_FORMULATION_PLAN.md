# PHASE-1 FORMULATION PLAN — module map (M1–M17)

Governing inputs (read-only):
- Blueprint v1.3 `paper9/plan/blueprint/Paper9_Blueprint_v1.3.tex`
  (sha256 `ca71b91aba4ca4abe9f157eb595ac8c2f709d838957a08ea0dce7160685dbf9f`), §2–§4, App. A–B,
  EQUATION REGISTER (1)–(71), (A.1)–(A.6), (B.1)–(B.8).
- `paper9/plan/CALC_MASTER_PLAN.md` v1.1 §A dependency map M1–M17.
- Legacy [C] sources for canonical forms (read-only, quoted with equation numbers in the
  derivation notes): `femcheck/FEM_Total/ptxt/FEM_1_Paper.txt` (ellipsoidal averaging,
  Eqs (2)–(12), (16)–(18)), `FEM_2_Paper.txt` (Eq (33) g²₂₂(α)), `FEM_3_Paper.txt`
  (§3.3 Eqs (15)–(19), (23)–(26): isotropic sixth-order Form-II modulus, a₁…a₅ basis).
  Legacy Eqs (84)–(85) of FEM_3 (single-length benchmark mapping) are NOT adopted —
  see DERIVATION_M01_M07.md §M4 for the documented difference.

Provenance tags: [C] canonical/published · [A] analytical derivation · [S] study/design
choice. Status labels: DRAFT / IN PROGRESS / TO BE VERIFIED / PASSED / FAILED / LOCKED.

| Module | Blueprint eqs | Script | Derivation notes | Status |
|---|---|---|---|---|
| M1 ellipsoidal domain + second-moment tensor | (1)–(4) | `scripts/m01_m02_length_tensor.py` | DERIVATION §M1 | checks PASSED (19 checks w/ M2) |
| M2 orientation rotation, g²₂₂(θ) | (5)–(9) | `scripts/m01_m02_length_tensor.py` | DERIVATION §M2 | checks PASSED (incl. mixed-term factor 2) |
| M3 kinematics ε, η, 2D counts | (10)–(12) | `scripts/m03_kinematics.py` | DERIVATION §M3 | checks PASSED (9 checks) |
| M4 Mindlin Form-II constitutive (C, D = (1/10)L⊗C, plane-strain) | (13)–(18) | `scripts/m04_form2_constitutive.py` | DERIVATION §M4 | checks PASSED (20 checks; theorem: iso limit = (0,0,λl²/20,μl²/10,0); note F1) |
| M5 micro-inertia T and inertial operator | (19)–(21) | `scripts/m05_micro_inertia.py` | DERIVATION §M5 | checks PASSED (7 checks; note M5-a) |
| M6 W, positive definiteness, eigenvalue invariance, K_g form | (22)–(26) | `scripts/m06_energy_definiteness.py` | DERIVATION §M6 | checks PASSED (11 checks; sufficient a₁..a₅ set; note F2) |
| M7 limit ladder (4 specialisations) | (27)–(30) | `scripts/m07_limit_ladder.py` | DERIVATION §M7 | checks PASSED (10 checks; notes M7-a/b) |
| M8 strong-form EOM + BC/interface quantities | (31)–(35) | `scripts/m08_strong_form.py` (next milestone) | §M8 | NOT STARTED |
| M9 Bloch theorem for C¹ medium (derived phase rules) | (36)–(43) | `scripts/m09_bloch_c1.py` (next milestone) | §M9 | NOT STARTED |
| M10 IBZ path Γ–X–M–Γ, k-sampling | (44) | path structure only; k-points/segment = TV4, unresolved | §M10 | NOT STARTED |
| M11 non-dimensionalisation | (45)–(47) | `scripts/m11_nondim.py` | §M11 | NOT STARTED |
| M12 observables (bands, gaps, S_θ, v_g, ⟨S⟩, identity) | (48)–(52) | `scripts/m12_observables.py` | §M12 | NOT STARTED |
| M13 BFS bicubic Hermite: shape functions, B, B_,i, 32 DOF, C¹ | (53)–(56) | `scripts/m13_bfs_shape.py` | §M13 | NOT STARTED |
| M14 element matrices K^c, K^g(θ,AR), M0, M^g; Gauss rule | (57)–(61) | `scripts/m14_element_matrices.py` | §M14 | NOT STARTED |
| M15 Bloch master–slave T(k); reduced Hermitian eigenproblem; K̄(k)=K̄(−k)^H | (62)–(71) | `scripts/m15_bloch_reduction.py` | §M15 | NOT STARTED |
| M16 Appendix A high-k asymptotics | (A.1)–(A.6) | `scripts/m16_asymptotics.py` | §M16 | NOT STARTED |
| M17 Appendix B energy-flux derivation | (B.1)–(B.8) | `scripts/m17_energy_flux.py` | §M17 | NOT STARTED |

Acceptance criteria (user-locked, Phase-1 §7) → where discharged:
internal consistency, dimensions, tensor symmetries → per-script checks (M1–M17);
characteristic-length tensor positive definite for admissible ellipsoids → M1/M2/M6;
BFS DOF ordering documented → M13; Bloch transformation + derivative-DOF phase factors
documented and verified → M9/M15; reduced K, M Hermitian by construction → M15;
eigenproblem dimensions verified → M15; non-dimensionalisation verified → M11;
M1–M17 traceable → this table + DERIVATION notes; blueprint traceability → equation
numbers cited per line in derivations.

TV policy: no TV item is resolved in Phase 1. Dependencies encountered are recorded in
PHASE1_MANIFEST.md. M1–M7 are fully symbolic — no TV value is required (production
parameters E, ν, l₁, l₂, l₃, ℓᵢ, θ, AR remain symbols; TV6/TV4/TV7 affect Phases 4–5 only).
