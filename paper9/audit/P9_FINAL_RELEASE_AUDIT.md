# P9 Final Release Audit Report

**Date:** 2026-09-23  
**Repository:** `https://github.com/vipin-oss/BFS-FEM-MATLAB`  
**Audited Branch:** `phase-1-symbolic`  
**Audited HEAD Commit:** `d438cd87b5f325dc062a58532132d9915bf32127`  
**Auditor:** P9 Final Pre-Submission / Release-Gate Audit Agent  
**Operational Scope:** Forensic evaluation of repository readiness against locked Blueprint v1.3 and Calculation Master Plan gates  
**Audit Verdict:** `P9_NOT_READY_FOR_FINAL_RELEASE`

---

## 1. Repository State

The repository state was inspected prior to audit execution:

```bash
git status
# On branch phase-1-symbolic
# Your branch is up to date with 'origin/phase-1-symbolic'.
# nothing to commit, working tree clean

git branch --show-current
# phase-1-symbolic

git rev-parse HEAD
# d438cd87b5f325dc062a58532132d9915bf32127

git rev-parse origin/phase-1-symbolic
# d438cd87b5f325dc062a58532132d9915bf32127

git rev-parse origin/main
# 1de47a4d111260ffb9b48d7c99e9db45102367c7
```

- **Branch:** `phase-1-symbolic`
- **Verified HEAD:** `d438cd87b5f325dc062a58532132d9915bf32127` (synchronized with `origin/phase-1-symbolic`)
- **Main Branch:** `origin/main` remains untouched at `1de47a4d111260ffb9b48d7c99e9db45102367c7`
- **Working Tree:** Pristine clean. In accordance with P9 instructions, this audit operates in strict READ-ONLY mode; no source, solver, parameter, or manuscript files are modified.

---

## 2. P6 / P7 / P8 Status Verification

A forensic review of the preceding audit phases confirms sequential integrity:

1. **Phase 6 (Gate Audit & Floats):**
   - Established formal readiness verdict `READY_FOR_P7_LIMITED_SCOPE`.
   - Generated 16 permissible float artifacts (11 vector figure PDFs in `paper9/figures/out/`, 5 LaTeX tables in `paper9/tables/out/`).
   - Reconciled the 19 candidate float register (16 verified embedded, 3 legitimately blocked: Fig 4, Tab 3, Fig 7).
   - Preserved locked gates: G3 = NOT MET, PCR1 = NOT PASS, B1–B3 = UNVALIDATED, B6 = PARTIAL, S2 = BLOCKED.
2. **Phase 7 (Limited-Scope Manuscript Drafting):**
   - Authored complete manuscript source `paper9/latex/ms.tex` with modular sections in `paper9/latex/sections/` and verified bibliography `paper9/bib/paper9.bib`.
   - Embedded 16 verified floats with exact Blueprint numbering and zero gaps.
   - Enforced explicit blocked placeholders (`[BLOCKED — ...]`) for Fig 4, Tab 3, Fig 7, and Sections 5.2, 5.3, 6.3.
   - Established 51 automated regression tests and zero parameter lint violations.
3. **Phase 8 (Forensic Manuscript Audit & Remediation):**
   - Identified 4 HIGH, 1 MEDIUM, 3 LOW findings in `P8_FORENSIC_MANUSCRIPT_AUDIT.md`.
   - Executed surgical remediation across four logical commits (`de19ef2`, `4cde6df`, `4429920`, `d438cd8`):
     - Integrated factor $1/10$ into displayed constitutive double-stress and element stiffness equations.
     - Aligned Appendix A 1D PDE with locked derivation M16, establishing exact asymptotic horizon $\bar{v}_{T,\infty} = \bar{l}_{\mathrm{eff}} / (\sqrt{10}\,\bar{\ell}_{\mathrm{i}}) \approx 0.3162$ evaluated using Table 2 baseline parameters ($l_{\mathrm{iso}} = 0.20\,\mathrm{m}, \ell_{\mathrm{i}} = 0.20\,\mathrm{m}$).
     - Corrected Figure 6 caption and Section 6.2 prose to accurately reflect plotted $\mathrm{AR}=10$ curves, Table 2 parameters, and verified directional gap $\Delta_{GX} = +0.0431$.
     - Reconciled global design map maximum to $\Delta_{GX} = 0.0896$ at $(\theta=30^\circ, \mathrm{AR}=10)$ across all manuscript occurrences.
     - Corrected orientation sweep frequency drops to $\bar{\omega}_T(X): 2.915 \to 2.672$ and $\bar{\omega}_L(X): 5.050 \to 4.628$.
     - Expanded regression test suite to 59/59 passing automated test functions (`test_p8_remediation.py`).

---

## 3. Mathematical Integrity

The manuscript's mathematical formulation was audited against the locked symbolic derivations (`DERIVATION_M01_M07.md` through `DERIVATION_M17.md`):

1. **Length Tensor & Rotation:**
   - Ellipsoidal domain $\mathcal{E}_0$ with semi-axes $l_1, l_2$ under area-preserving constraint $\det(\mathbf{L}_0) = l_1^2 l_2^2 = l_{\mathrm{iso}}^4$.
   - Passive rotation $\mathbf{L}(\theta) = \bm{R}(\theta)^\mathsf{T} \mathbf{L}_0 \bm{R}(\theta)$ generates negative off-diagonal coupling $L_{12}(45^\circ) = -0.096\,\mathrm{m}^2$.
   - Eigenvalues $\mathrm{spec}(\mathbf{L}(\theta)) \equiv \{l_1^2, l_2^2\}$ are orientation-invariant, rigorously proving positive definiteness for all $\theta$.
2. **Mindlin Form-II Constitutive Model:**
   - Cauchy stress: $\sigma_{ij} = C_{ijkl}\varepsilon_{kl} = \lambda \delta_{ij}\varepsilon_{kk} + 2\mu \varepsilon_{ij}$.
   - Double stress: $\tau_{ijk} = \frac{1}{10} L_{kl} C_{ijmn}\eta_{mnl}$, incorporating the second-moment prefactor $1/10$.
   - Strain energy density: $W = \frac{1}{2}\sigma_{ij}\varepsilon_{ij} + \frac{1}{2}\tau_{ijk}\eta_{ijk} > 0$.
3. **Micro-Inertia & Dynamic Equilibrium:**
   - Kinetic energy density: $T = \frac{1}{2}\rho \dot u_i \dot u_i + \frac{1}{2}\rho \ell_{\mathrm{i}}^2 \dot u_{i,j}\dot u_{i,j}$.
   - Strong form: $\sigma_{ij,j} - \tau_{ijk,jk} = \rho(\ddot u_i - \ell_{\mathrm{i}}^2 \ddot u_{i,jj})$.
   - Boundary tractions: classical $p_i = \sigma_{ij}n_j - n_j n_k \tau_{ijk,k}$ and double traction $R_i = n_j n_k \tau_{ijk}$.
4. **$C^1$ BFS Finite Element Discretisation:**
   - 32 DOFs per cell: 4 vertices $\times$ 2 displacement components $\times$ 4 DOFs $\{u, u_{,x}, u_{,y}, u_{,xy}\}$.
   - Conforming in $H^2(\Omega)$, guaranteeing inter-element slope continuity.
   - Exact $4 \times 4$ Gauss–Legendre quadrature integrating quartic polynomial integrands without rank deficiency.
   - Master–slave Bloch reduction applying identical complex phase transformations $e^{\iu \bm{k}\cdot\bm{a}_\alpha}$ across value and derivative DOFs.
   - Reduced pencil $[\bar{\bm{K}}(\bm{k}) - \omega^2 \bar{\bm{M}}(\bm{k})]\bar{\bm{d}} = \bm{0}$ is strictly Hermitian ($\bar{\bm{K}}^\mathsf{H} = \bar{\bm{K}}, \bar{\bm{M}}^\mathsf{H} = \bar{\bm{M}} > 0$) and BZ-periodic.
5. **Energy Conservation & Poynting Flux:**
   - Instantaneous flux: $S_j = -(\sigma_{ij} - \tau_{ijk,k})\dot u_i - \tau_{ikj}\dot u_{i,k} - \rho \ell_{\mathrm{i}}^2 \dot u_i \ddot u_{i,j}$.
   - Fundamental identity $\bm{v}_g = \langle\bm{S}\rangle/(\langle W\rangle + \langle T\rangle)$ verified numerically in Test 5h ($< 10^{-8}$ discrepancy).

---

## 4. Numerical Reproducibility

All reported values trace directly to authoritative raw datasets (`p5_production_raw.json`), parameter registries, and verification logs:

- **Empirical Convergence Rate:** $p = 4.17$ ($95\%$ CI: $[3.15, 5.20]$) across $4^2, 8^2, 16^2, 32^2$ meshes.
- **Operational Resolution Floor:** $\varepsilon_\Delta = 4.63 \times 10^{-11}$ evaluated on acoustic mode $\bar{\omega}_T$.
- **Acoustic Analytic Error:** $1.25 \times 10^{-8}$ against Papargyri-Beskou & Beskos (2009) (Test 5d).
- **Directional Stop Band:** $\Delta_{GX} = +0.0431$ for $\mathrm{AR}=10, \theta=45^\circ$.
- **Global Design Map Maximum:** $\Delta_{GX} = 0.0896$ at $(\theta=30^\circ, \mathrm{AR}=10)$.
- **Complete Gap Non-existence:** $\Delta_{\mathrm{complete}} \le -0.3758$ across all 42 evaluated design configurations.
- **Orientation Sensitivity:** $S_\theta$ increases monotonically from $0.000\,\mathrm{rad}^{-1}$ ($\mathrm{AR}=1$) to $3.946\,\mathrm{rad}^{-1}$ ($\mathrm{AR}=10$).
- **Acoustic Wave Steering:** Peak angular deviation $\delta_{\max} = 2.79^\circ$ at $\bar{k} = 0.5$ ($\mathrm{AR}=10, \theta=45^\circ$).
- **Gradient Energy Partition:** Monotonic increase from $W_g/W = 0.20\%$ ($\bar{k}=0.1$) to $16.49\%$ ($\bar{k}=1.0$).
- **Micro-Inertia Asymptotic Horizon:** Bounded phase velocity $\bar{v}_p = 0.3163$ at $\bar{k}=200$ (matching theoretical horizon $v_{T,\infty} = 0.3162$ within $0.03\%$), contrasted with unbounded divergence $\bar{v}_p = 39.75$ for $\ell_{\mathrm{i}} = 0$.

---

## 5. Published Benchmark Audit

A forensic examination was conducted on each candidate external validation benchmark:

### Benchmark B1 (Layer 1 Classical Limit)
- **Source:** Li, Li, Guo et al. (2024), *Sci. Rep.* 14:24035, Fig 2(a).
- **Physical Model:** 1D periodic bilayer (AlN/BaTiO3) in classical elasticity, solved via transfer matrix.
- **Tabulated Data Availability:** None. The published paper provides raster/vector plots without tables of numerical frequencies or gap edges.
- **Solver Compatibility:** The repository contains a 2D homogeneous Case H BFS finite element solver. It does not contain a 1D multi-layer transfer-matrix or finite element solver.
- **Error Metric Feasibility:** Under project governance, digitizing published plots is permitted for visual overlay ONLY, never for error computation. Consequently, no quantitative relative error metric ($e \le 0.5\%$) can be computed without published numerical tables or author-provided data.
- **Verdict:** **UNVALIDATED / BLOCKED**.

### Benchmark B2 (Layer 2a Gradient Elasticity, Flexoelectricity Suppressed)
- **Source:** Li, Li, Guo et al. (2024), *Sci. Rep.* 14:24035, Fig 2(b).
- **Physical Model:** 1D periodic bilayer with dipolar gradient elasticity and micro-inertia ($f=0$).
- **Tabulated Data Availability:** None published.
- **Notation Ambiguity:** Figure 2 caption writes $l = 10^{-5}$ unbarred, whereas the plan locked non-dimensional $\bar{l} = 10^{-5}$.
- **Solver Compatibility:** Same blocker as B1; no 1D bilayer solver exists in the repository.
- **Verdict:** **UNVALIDATED / BLOCKED**.

### Benchmark B3 (Layer 2b Isothermal Dipolar-Gradient Bilayer)
- **Source:** Li, Askes, Gitman, Krynkin & Wei (2023), *Waves Random Complex Media* 36(4):5715–5735, Fig 4(c).
- **Physical Model:** 1D periodic Pb/brass bilayer in dipolar gradient elasticity.
- **Open Parameters (TV1):** The non-dimensional parameters ($c_1, c_R, d_1, d_R$) specific to Fig 4(c) are omitted in the published text.
- **Sampling Parameters (TV12):** Overlay axis ranges and wavenumber sampling are unstated.
- **Tabulated Data Availability:** None published.
- **Verdict:** **UNVALIDATED / BLOCKED**.

---

## 6. Independent Validation Audit (Benchmark B6)

- **Source:** Li, Wei & Zhou (2016), *Acta Mech.* 227:1005–1023.
- **Implementation:** An independent 1D SH-wave transfer-matrix solver is implemented in `paper9/validation/b6_lwz_tm/`.
- **Numerical Verification:**
  - L1 homogeneous limit check: matches analytical dispersion Eq. (14.1) within max relative error $1.429 \times 10^{-14}$.
  - L2 identical-layer limit check: matches within $4.441 \times 10^{-16}$.
- **Scope & Limitations:**
  - B6 serves as an independent formulation cross-check for 1D transfer matrices.
  - It does not validate the 2D anisotropic BFS finite element solver.
  - Figure 3 of LWZ 2016 lacks published numerical tables; hence quantitative percentage error against the published curve cannot be computed without unauthorized digitization.
- **Verdict:** **PARTIAL**. Retained as PARTIAL in strict compliance with governance rules.

---

## 7. Case-C / Study S2 Audit

Study S2 investigates a 2D composite phononic crystal with a circular inclusion in a square unit cell to generate complete omnidirectional band gaps. An exhaustive audit reveals that Study S2 is blocked by three foundational items:

1. **TV6 (Case C Production Parameters):**
   - Neither Blueprint v1.3 nor any cited literature establishes authoritative material properties, inclusion radius $R/L$, stiffness contrast $\mu_2/\mu_1$, density contrast $\rho_2/\rho_1$, or gradient length scales for the inclusion.
   - Inventing arbitrary numbers violates the project's zero-fabrication mandate.
2. **TV14 (Reference Phase Non-Dimensionalization):**
   - In a two-phase unit cell, which constituent phase defines the reference frequency $\omega_0 = \sqrt{\mu/(\rho L^2)}$ and phase velocity scaling is undefined.
3. **TV18 (Circular Inclusion Representation on BFS Grid):**
   - The Bogner--Fox--Schmit bicubic Hermite element is strictly an axis-aligned rectangular element ($Q_3$ tensor product). It lacks isoparametric curvilinear mappings.
   - Elements intersected by a circular boundary experience discontinuous material fields. Assigning material properties at Gauss points integrates a discontinuous step function, producing an $\mathcal{O}(h)$ boundary area error (demonstrated algebraically in `audit_m14_independent.py` check [Q6]).
   - Conforming curved $C^1$ interface elements with higher-order interface traction jump conditions (TV6) are not part of the locked mathematical formulation.
- **Verdict:** **S2 = BLOCKED BY INSUFFICIENT SOURCE-SPECIFIED DATA**.

---

## 8. Technical Variations (TV) Register

| TV ID | Item Description | Status | Evidence / Repository Location | Action Required to Close |
| :--- | :--- | :--- | :--- | :--- |
| **TV1** | Anchor A Fig 4(c) non-dimensional parameters ($c, d$ set) | **OPEN** | `paper9/validation/P3_STATUS.md`, `P3_TV_RESOLUTION.md` | Requires author correspondence or supplemental published data from Li et al. (2023). |
| **TV6** | Case H vs Case C production parameters | **OPEN (Case C)** | `p5_pilot_params.yaml`, `tab02_parameters.tex` | Case H is locked [S]; Case C parameters require external authoritative literature lock. |
| **TV9** | Mishra et al. (2026) homogeneous limit configuration | **OPEN** | `paper9/validation/P3_STATUS.md` | Optional Layer 4 cross-check configuration to be retrieved. |
| **TV12** | Overlay axis ranges and sampling for Figs 4(a)–(c) | **OPEN** | `paper9/validation/P3_TV_RESOLUTION.md` | Pertains to published overlay generation for Gate G3. |
| **TV14** | Case C reference phase for non-dimensionalization | **OPEN** | `traceability_matrix.csv` (M11), `STAGE1_BLOCKERS_AUDIT.md` | Constitutive specification required for two-phase composite cell. |
| **TV18** | BFS circular inclusion representation | **OPEN** | `audit_m14_independent.py` check [Q6], `DERIVATION_M13.md` | Requires formulation of cut-cell or adaptive sub-cell quadrature for $C^1$ Hermite elements. |

---

## 9. Figure and Table Audit

Blueprint v1.3 specifies 13 figures and 6 tables (19 candidate floats). All 19 floats are accounted for:

| Float ID | Role | Status | Source / Generator / Data | Caption & Parameters |
| :--- | :--- | :--- | :--- | :--- |
| **Fig 01** | Theory | **EMBEDDED** | `fig01_ellipsoid_tensor.py` (M1, M2) | Ellipsoid schematic and rotated tensor components; verified passive rotation. |
| **Fig 02** | Theory | **EMBEDDED** | `fig02_lattice_ibz.py` (M10) | Square unit cell and $\Gamma$--$X$--$M$--$\Gamma$ high-symmetry contour. |
| **Fig 03** | Method | **EMBEDDED** | `fig03_bfs_dof_bloch.py` (M9, M13) | 32-DOF BFS layout and identical Bloch phase on value/derivative DOFs. |
| **Fig 04** | Validation | **BLOCKED** | *None* | Explicit placeholder: `[BLOCKED — G3/PCR1 literature numerical validation not yet established]`. |
| **Fig 05** | Verification | **EMBEDDED** | `fig05_mesh_convergence.py` (`p4b_5g_to_5i.json`) | Monotone convergence ($4^2 \to 32^2$), $p=4.17$, $\varepsilon_\Delta = 4.63 \times 10^{-11}$. |
| **Fig 06** | Case H Result | **EMBEDDED** | `fig06_caseH_dispersion.py` (`p5_production_raw.json`) | Case H dispersion: $\mathrm{AR}=1$ vs $\mathrm{AR}=10$ ($\theta=0^\circ, 45^\circ$); $\Delta_{GX} = +0.0431$, $\Delta_{\mathrm{complete}} \le -0.3758$. |
| **Fig 07** | Case C Result | **BLOCKED** | *None* | Explicit placeholder: `[BLOCKED — Case C/S2 parameters and formulation unresolved]`. |
| **Fig 08** | Sweep Result | **EMBEDDED** | `fig08_theta_sweep.py` (`p5_production_raw.json`) | Orientation sweep ($\theta \in [0, 90^\circ]$ at $\mathrm{AR}=5$): $\bar{\omega}_T(X): 2.915 \to 2.672$, diagonal symmetry at $M$. |
| **Fig 09** | Sweep Result | **EMBEDDED** | `fig09_ar_sweep.py` (`p5_production_raw.json`) | Aspect ratio sweep ($\mathrm{AR} \in [1, 10]$ at $\theta=45^\circ$). |
| **Fig 10** | Design Map | **EMBEDDED** | `fig10_design_map_3d.py` (`p5_production_raw.json`) | 3D surface and 2D contour over 42 points; global maximum $\Delta_{GX} = 0.0896$ at $(\theta=30^\circ, \mathrm{AR}=10)$. |
| **Fig 11** | Polar Map | **EMBEDDED** | `fig11_polar_map_regimes.py` (`p5_production_raw.json`) | Polar classification $(X, Y) = (\mathrm{AR}\cos\theta, \mathrm{AR}\sin\theta)$ of stop-band vs pass-band regimes. |
| **Fig 12** | Steering | **EMBEDDED** | `fig12_ifc_wave_steering.py` (`p5_production_raw.json`) | Steering deviation $\delta(\phi)$ and $|\bm{v}_g|(\phi)$ along circular path $|\bar{\bm{k}}| = 0.5$; $\delta_{\max} = 2.79^\circ$. |
| **Fig 13** | Physics | **EMBEDDED** | `fig13_energy_microinertia.py` (`p5_production_raw.json`) | Gradient energy partition ($0.20\% \to 16.49\%$) and high-$k$ phase velocity asymptotics ($v_{T,\infty} = 0.3162$). |
| **Tab 01** | Literature | **EMBEDDED** | `tab01_literature_positioning.tex` | Positioning matrix including reported-quantity column and research gaps. |
| **Tab 02** | Parameters | **EMBEDDED** | `tab02_parameters.tex` | Master parameter registry with provenance tags `[S]` and `[A]`. |
| **Tab 03** | Validation | **BLOCKED** | *None* | Explicit placeholder: `[BLOCKED — G3/PCR1 literature numerical validation not yet established]`. |
| **Tab 04** | Verification | **EMBEDDED** | `tab04_consistency_suite.tex` | Eight-test consistency suite (5a–5h) with quantitative tolerances and pass status. |
| **Tab 05** | Gap Summary | **EMBEDDED** | `tab05_gap_summary.tex` | Directional gap summary, complete gap check ($\le -0.3758$), and $S_\theta$ up to $3.946\,\mathrm{rad}^{-1}$. |
| **Tab 06** | Convergence | **EMBEDDED** | `tab06_convergence_floor.tex` | Mesh convergence sequence ($4^2 \to 32^2$), $p=4.17$, $\varepsilon_\Delta = 4.63 \times 10^{-11}$. |

---

## 10. Manuscript Claim Audit

Every section of the remediated manuscript was evaluated to verify that no unsupported claims exist:
- **No Complete Band Gap in Case H:** Strictly maintained across all sections, tables, and captions. Case H produces directional stop bands ($\Delta_{GX} > 0$), but never a complete omnidirectional band gap ($\Delta_{\mathrm{complete}} \le -0.3758$).
- **No False Literature Validation:** Sections 5.2, 5.3, Figure 4, and Table 3 explicitly preserve their blocked status without fabricating numerical data.
- **No False Case C Results:** Section 6.3 and Figure 7 explicitly preserve their blocked status without claiming phononic crystal band gaps.
- **No Theoretical $\mathcal{O}(h^4)$ Convergence:** Text and Table 6 cite an empirical least-squares fit ($p = 4.17$, $95\%$ CI: $[3.15, 5.20]$) and resolution floor $\varepsilon_\Delta = 4.63 \times 10^{-11}$.
- **No Closed 2D IFC Claims:** Figure 12 is described strictly as wave steering along a circular wave-vector contour $|\bar{\bm{k}}| = 0.5$.

---

## 11. Automated Verification

The entire repository test architecture was executed and verified:

```bash
PYTHONPATH=/home/user pytest paper9/production/p5/test_p5_integrity.py paper9/verification/suite/ -v
# ============================== 59 passed in 2.25s ==============================
```

- **59/59 Automated Regression Tests PASS (100%):**
  - 28/28 tests in `test_p5_integrity.py` PASS
  - 3/3 tests in `test_p4b_5g_5h.py` PASS
  - 8/8 tests in `test_p5_production.py` PASS
  - 4/4 tests in `test_p6_generators.py` PASS
  - 7/7 tests in `test_p6_remediation.py` PASS
  - 1/1 test in `test_p7_manuscript.py` PASS
  - 8/8 tests in `test_p8_remediation.py` PASS
- **Parameter Lint:** `lint_p5_params.py` completed with 0 violations.
- **LaTeX Compilation Safety:**
  - 100% paired `\begin{...}` and `\end{...}` blocks.
  - 11/11 section files resolved.
  - 5/5 LaTeX tables resolved.
  - 11/11 vector PDFs resolved.
  - 15/15 BibTeX citations matched (0 orphans, 0 undefined).
  - 102 labels and 25 cross-references matched (0 undefined).

---

## 12. Gate Matrix

| Gate / Requirement | Description | Status | Authoritative Evidence | Remaining Action to Close |
| :--- | :--- | :--- | :--- | :--- |
| **G1** | Symbolic formulation and patch tests | **MET** | `DERIVATION_M01_M07.md` through `M17.md` | None (closed in Phase 1). |
| **G1b** | Two-route analytical cross-verification | **MET** | `paper9/validation/L3/` | None (closed in Phase 2). |
| **G2a** | Solver acceptance (tests 5a–5f) | **MET** | `p4a_5a_to_5f.py` (34/34 PASS) | None (closed in Phase 4A). |
| **G2** | Internal numerical verification (5a–5h + 5i) | **MET** | `p4b_5g_to_5i.py`, `tab04`, `tab06` | None (closed in Phase 4B). |
| **G3** | Published benchmark validation (Layers 1, 2a, 2b $\le 2\%$) | **NOT MET** | `P3_STATUS.md`, `STAGE1_BLOCKERS_AUDIT.md` | Blocked by absence of published numerical tables for B1–B3 and lack of 1D bilayer C1 solver. |
| **G4** | Submission-ready release | **NOT MET** | Blueprint v1.3 line 881, line 907 | Blocked by Gate G3, PCR1, and Study S2. |
| **G5** | Main scientific study completeness | **PARTIAL** | `p5_production_raw.json` | Case H (S1, S3–S9) complete; Case C (S2) blocked. |
| **G-F** | Float inventory verification | **PARTIAL** | `P6_GF_AUDIT.md`, Float Register | 16/19 verified embedded; 3/19 legitimately blocked. |
| **PCR1** | Published benchmarks PASS $\le 2\%$ | **NOT PASS** | `P3_STATUS.md`, Section 5.2–5.3 | Requires quantitative B1, B2, B3 validation. |
| **PCR2** | Benchmarks in main manuscript | **NOT PASS** | Sections 5.2, 5.3, Fig 4, Tab 3 | Blocked pending G3/PCR1 resolution. |
| **PCR3** | Analytical checks pass (Layer 3, App A, App B) | **PASS** | Test 5d, 5g, 5h, Appendices A & B | Fully satisfied. |
| **PCR4** | Eight-test suite tabulated (Table 4) | **PASS** | `tab04_consistency_suite.tex` | Fully satisfied. |
| **PCR5** | Mesh convergence and resolution floor (Table 6) | **PASS** | `tab06_convergence_floor.tex`, Fig 5 | Fully satisfied ($p=4.17, \varepsilon_\Delta = 4.63 \times 10^{-11}$). |
| **PCR6** | Master parameters with provenance tags (Table 2) | **PASS** | `tab02_parameters.tex` | Fully satisfied (tags `[S]` and `[A]`). |
| **PCR7** | Physical claims supported ($S_\theta, \delta_{\max}, v_{T,\infty}$) | **PASS** | Figs 10, 11, 12, 13; Tabs 5, 6 | Fully satisfied. |
| **PCR8** | Hedged novelty claims and research gaps in Table 1 | **PASS** | Section 1, Table 1 | Fully satisfied. |
| **B1** | Layer 1 classical limit benchmark | **UNVALIDATED** | `P3_STATUS.md` | Blocked by missing published tables and 1D solver. |
| **B2** | Layer 2a gradient elasticity benchmark | **UNVALIDATED** | `P3_STATUS.md` | Blocked by missing published tables and 1D solver. |
| **B3** | Layer 2b dipolar-gradient bilayer benchmark | **UNVALIDATED** | `P3_STATUS.md` | Blocked by TV1, TV12, and missing published tables. |
| **B4** | Layer 2c optional benchmark | **UNVALIDATED** | `P3_STATUS.md` | Optional; unexecuted. |
| **B5** | Layer 3 closed-form analytical benchmark | **PASS** | `p3_layer3_pb2009.py` (11/11 PASS) | Fully satisfied ($1.25 \times 10^{-8}$ error). |
| **B6** | Layer 3b independent 1D transfer matrix | **PARTIAL** | `b6_lwz_tm/` | Formulation verified; curve validation blocked by missing tables. |
| **S2** | Case C periodic phononic crystal study | **BLOCKED** | `STAGE1_BLOCKERS_AUDIT.md` | Blocked by TV6 (Case C), TV14, TV18. |
| **TV1** | Anchor A Fig 4(c) parameters | **OPEN** | `P3_STATUS.md` | Requires author-provided data from Li et al. (2023). |
| **TV6** | Case C production parameters | **OPEN** | `STAGE1_BLOCKERS_AUDIT.md` | Requires external authoritative specification. |
| **TV9** | Mishra 2026 homogeneous limit | **OPEN** | `P3_STATUS.md` | Optional Layer 4 cross-check. |
| **TV12** | Fig 4 overlay axis ranges and sampling | **OPEN** | `P3_STATUS.md` | Pertains to published overlay generation. |
| **TV14** | Case C reference phase non-dimensionalization | **OPEN** | `traceability_matrix.csv` (M11) | Requires constitutive multi-phase convention. |
| **TV18** | BFS circular inclusion representation | **OPEN** | `audit_m14_independent.py` [Q6] | Requires cut-cell or sub-cell $C^1$ quadrature method. |

---

## 13. Remaining Blockers

A rigorous forensic synthesis identifies four fundamental scientific blockers preventing final release under the locked Blueprint v1.3 specification:

1. **Blocker 1 (Missing Published Numerical Benchmark Tables):**
   - Published anchors (Li et al. 2023, 2024) present dispersion curves in raster/vector plots without accompanying numerical frequency tables or gap bounds.
   - Project governance strictly prohibits using digitized pixels as an error metric for code validation. Without published numerical tables, quantitative relative errors cannot be established.
2. **Blocker 2 (1D vs 2D Solver Architecture Mismatch):**
   - The repository's solver is a 2D $C^1$ BFS finite element formulation for homogeneous square unit cells.
   - Published benchmarks B1, B2, and B3 are 1D layered bilayers solved via transfer matrix. Comparing 2D Case H dispersion against 1D bilayer dispersion represents incompatible physics.
3. **Blocker 3 (Unresolved Technical Variations TV1, TV12):**
   - The non-dimensional parameters ($c_1, c_R, d_1, d_R$) for Li et al. (2023) Fig 4(c) remain unstated in the literature.
4. **Blocker 4 (Case C Composite Phononic Crystal Formulation & Meshing - TV6, TV14, TV18):**
   - Case C material contrast and inclusion radius remain unstated in literature.
   - The rectangular BFS element lacks curvilinear mapping, creating $\mathcal{O}(h)$ boundary representation error across circular interfaces. Conforming curved $C^1$ interface elements are outside the existing solver architecture.

---

## 14. Final Release Decision

Applying the strict, non-subjective Decision Rules established by project governance:
- **`P9_READY_FOR_FINAL_RELEASE`** is permitted ONLY if all mandatory release gates are satisfied. Because Gate G3 = NOT MET, PCR1 = NOT PASS, PCR2 = NOT PASS, and Gate G4 cannot be signed, the project cannot be marked ready for final release.
- **`P9_READY_WITH_EXPLICIT_VALIDATION_LIMITATIONS`** would apply if the manuscript were ready for submission under documented limitations. However, Blueprint v1.3 line 881 explicitly mandates that the manuscript *cannot be submitted* to the target journal (*IJMS*) while G3 and PCR1 remain unsatisfied, and the submission package cannot contain literal `[BLOCKED — ...]` placeholders in place of figures and sections.
- **`P9_NOT_READY_FOR_FINAL_RELEASE`** is mandated when unresolved mandatory validation and formulation blockers prevent a defensible final submission.

Therefore, the authoritative forensic verdict is:

**Verdict:** `P9_NOT_READY_FOR_FINAL_RELEASE`

*(Note for Project Governance: While the manuscript cannot be released for full journal submission under the original Blueprint v1.3 scope, the limited-scope Case H formulation, wave steering analysis, and Layer 5 verification suite are 100% verified, mathematically aligned, and completely traceable. If governance formally amends the project scope to de-couple Case C and published 1D bilayer validation into a separate follow-up publication, the current codebase provides an unassailable foundation).*

---

## 15. Exact Next Actions

To systematically resolve the remaining blockers and achieve full Gate G4 release:

1. **De-coupling or External Data Acquisition for Gate G3 (P10):**
   - Option A (Preferred): Obtain verified numerical benchmark tables directly from the authors of Li et al. (2023, 2024), or formally authorize a calibrated independent 1D transfer-matrix benchmark script.
   - Option B (Scope Amendment): Formally amend Blueprint v1.3 to classify 1D transfer-matrix benchmarking as an external annex, allowing submission of the 2D Case H anisotropic metamaterial steering study on the strength of its Layer 5 verification suite and closed-form analytical matching (B5).
2. **Formulation of 1D Bilayer $C^1$ FE Solver (P11):**
   - If 1D benchmarks B1–B3 must be reproduced by finite elements, implement a dedicated 1D 2-node Hermite element ($C^1$) with periodic boundary tying across bimaterial interfaces.
3. **Resolution of Case C Circular Inclusion (P12):**
   - Select an authoritative, published 2D phononic crystal parameter set (closing TV6 and TV14).
   - Implement an adaptive quadtree sub-cell integration or quad-meshed boundary-fitted $C^1$ discretization (closing TV18).
   - Execute Study S2 to generate Figure 7 and complete Table 5.
4. **Final Gate G4 Sign-off (P13):**
   - Remove blocked placeholders, compile final `ms.pdf`, and release the five submission deliverables.
