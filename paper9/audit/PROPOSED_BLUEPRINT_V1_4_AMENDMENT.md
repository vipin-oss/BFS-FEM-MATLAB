# Proposed Blueprint v1.4 Amendment

**Document ID:** `BP-v1.4-PROP-2026-09-23`  
**Target Repository:** `https://github.com/vipin-oss/BFS-FEM-MATLAB`  
**Target Branch:** `phase-1-symbolic`  
**Base Commit:** `d438cd87b5f325dc062a58532132d9915bf32127`  
**Status:** PROPOSED AMENDMENT FOR PI / GOVERNANCE REVIEW ONLY (NON-OPERATIONAL)  
**Author:** P10A Governance Directive & Blueprint v1.4 Amendment Drafting Agent  

---

## 1. Purpose

This document provides a formal, evidence-based governance amendment proposal to transition the research program from **Paper9 Blueprint v1.3** to **Paper9 Blueprint v1.4**. 

Phase 9 (`paper9/audit/P9_FINAL_RELEASE_AUDIT.md`) established that under current governance, the manuscript cannot be released for publication (`P9_NOT_READY_FOR_FINAL_RELEASE`) because:
- **Gate G3** is **NOT MET** and **PCR1** is **NOT PASS** (external published benchmarks B1, B2, and B3 remain unvalidated due to the absence of published numerical eigenvalue tables and the architectural mismatch between 1D layered transfer matrices and 2D unit-cell finite elements).
- **Study S2 (Case C)** is **BLOCKED** by missing literature contrast parameters (TV6, TV14) and the geometric inability of rectangular $C^1$ BFS elements to represent circular inclusions without $\mathcal{O}(h)$ boundary representation error (TV18).
- The manuscript source `ms.tex` legitimately preserves explicit blocked placeholders (`[BLOCKED — ...]`) for Figures 4 and 7, Table 3, and Sections 5.2, 5.3, and 6.3.

Phase 10 (`paper9/audit/P10_GOVERNANCE_SCOPE_DECISION.md`) established that the **Case-H scientific subsystem** (homogeneous strain-gradient metamaterial with anisotropic ellipsoidal length tensor, micro-inertia, conforming $C^1$ BFS Bloch finite element formulation, directional stop bands, acoustic wave steering, energy flux, and the 8-test Layer 5 verification suite) is scientifically complete, internally verified across 59 automated tests, and mathematically consistent. However, because Blueprint v1.3 explicitly locks B1–B3 and S2 as mandatory submission requirements, the project cannot proceed to final release without a **Formal Governance Scope Amendment**.

This document specifies the exact, line-by-line governance, gate, PCR, float, and manuscript modifications required to establish a standalone Case-H publication while preserving complete scientific integrity and total disclosure of limitations.

---

## 2. Current Blueprint v1.3 Locked Scope

Under Blueprint v1.3 (promulgated 22 September 2026) and Calculation Master Plan v1.1:
1. **Constitutive & Finite Element Theory:** Mindlin Form-II strain-gradient elasticity with an anisotropic ellipsoidal length tensor $\mathbf{L}(\theta) = \bm{R}(\theta)^\mathsf{T}\mathbf{L}_0\bm{R}(\theta)$, volume-preserving constraint $\det(\mathbf{L}_0) = l_{\mathrm{iso}}^4$, micro-inertia $\rho \ell_{\mathrm{i}}^2$, and a 32-DOF bicubic Hermite ($C^1$ BFS) Bloch–Floquet unit-cell formulation.
2. **Dual Physical Systems:**
   - *Case H (Homogeneous Medium):* Microstructure-induced dispersion and directional wave phenomena in a uniform cell.
   - *Case C (Composite Phononic Crystal):* Periodic square unit cell with a centered circular inclusion to generate complete omnidirectional Bragg band gaps (§6.1 line 483, §6.3 line 485, Fig 7 line 620, Step 10 line 805).
3. **Five-Layer Validation Framework:**
   - *Layer 1 (B1):* Classical bilayer transfer-matrix benchmark [Li et al. 2024, Fig 2(a)] $\le 0.5\%$.
   - *Layer 2a (B2):* Gradient bilayer transfer-matrix benchmark [Li et al. 2024, Fig 2(b)] $\le 2\%$.
   - *Layer 2b (B3):* Dipolar-gradient bilayer transfer-matrix benchmark [Li et al. 2023, Fig 4(c)] $\le 2\%$.
   - *Layer 3 (B5):* Closed-form analytical dispersion benchmark [Papargyri-Beskou & Beskos 2009] to machine precision.
   - *Layer 3b (B6):* Independent 1D SH transfer-matrix formulation [Li, Wei & Zhou 2016].
   - *Layer 5:* Internal 8-test consistency suite (5a–5h) and mesh convergence study (5i).
4. **Locked Submission Gates:**
   - *Gate G3 (Hard Gate):* Layers 1, 2a, 2b $\le 2\%$ relative error with evidence in the main manuscript (Plan line 103, Blueprint line 822).
   - *Publication-Critical Requirement PCR1:* Mandatory published benchmarks PASS $\le 2\%$ (Blueprint §9.4 line 884).
   - *Gate G4:* Final PI sign-off conditioned strictly on satisfying PCR1–PCR8 (Blueprint §9.4 line 907).

---

## 3. Proposed Revised Scope

The proposed **Blueprint v1.4** formally amends the scope as follows:
- **Core Published Deliverable:** A standalone, archival research paper focused exclusively on **Case H**:
  *Two-dimensional wave dispersion, directional stop bands, and acoustic wave steering in a homogeneous strain-gradient elastic metamaterial with anisotropic ellipsoidal microstructure and micro-inertia: A conforming Bloch–Floquet $C^1$ finite element formulation.*
- **Scope Boundary:** The investigation is strictly confined to the homogeneous unit cell with anisotropic internal length scales. It establishes the continuum variational formulation, the second-moment prefactor $1/10$, the passive rotation transformation, the conforming $C^1$ BFS Bloch finite element methodology with derivative phase-tying, rigorous internal verification (Layer 5), and physical discovery of directional stop bands, orientation-driven acoustic wave steering, energy partition, and high-$k$ micro-inertial horizon stabilization.
- **Formally De-scoped Components:**
  - Multi-phase composite phononic crystals with material contrast (Case C / Study S2) are formally de-scoped and deferred to a dedicated follow-up publication (*Part II: Composite Phononic Crystals*).
  - External 1D layered bilayer transfer-matrix benchmarks (B1, B2, B3) are formally de-scoped from mandatory pre-submission gates, with validation resting on closed-form continuum analytical benchmarks (Layer 3) and the 8-test consistency suite (Layer 5).

---

## 4. Case-H Core Scope

Audit of repository assets (`p5_production_raw.json`, `p4b_5g_to_5i.json`, `test_p5_integrity.py`, `test_p8_remediation.py`) confirms that the Case-H core subsystem is fully realized and requires zero additional simulation:
1. **Mathematical Continuum Model:**
   - Second-moment characteristic-length tensor $\mathbf{L}_0 = \mathrm{diag}(l_1^2, l_2^2)$ under $\det(\mathbf{L}_0) = l_{\mathrm{iso}}^4$.
   - Passive rotation $\mathbf{L}(\theta) = \bm{R}(\theta)^\mathsf{T}\mathbf{L}_0\bm{R}(\theta)$ generating negative off-diagonal coupling $L_{12}(45^\circ) = -0.096\,\mathrm{m}^2$ and orientation-invariant positive eigenvalues $\{l_1^2, l_2^2\}$.
   - Mindlin Form-II constitutive relation with second-moment prefactor $1/10$: $\tau_{ijk} = \frac{1}{10}L_{kl}C_{ijmn}\eta_{mnl}$.
   - Micro-inertia kinetic energy $T = \frac{1}{2}\rho \dot u_i \dot u_i + \frac{1}{2}\rho \ell_{\mathrm{i}}^2 \dot u_{i,j}\dot u_{i,j}$ and dynamic balance $\sigma_{ij,j} - \tau_{ijk,jk} = \rho(\ddot u_i - \ell_{\mathrm{i}}^2 \ddot u_{i,jj})$.
2. **Conforming $C^1$ Finite Element Formulation:**
   - 32-DOF Bogner–Fox–Schmit bicubic Hermite element in $H^2(\Omega)$.
   - $4 \times 4$ Gauss–Legendre quadrature.
   - Master–slave Bloch transformation applying identical phase factors $e^{\iu \bm{k}\cdot\bm{a}_\alpha}$ to displacement and derivative DOFs.
   - Reduced pencil $[\bar{\bm{K}}(\bm{k}) - \omega^2 \bar{\bm{M}}(\bm{k})]\bar{\bm{d}} = \bm{0}$ is strictly Hermitian ($\bar{\bm{K}}^\mathsf{H} = \bar{\bm{K}}, \bar{\bm{M}}^\mathsf{H} = \bar{\bm{M}} > 0$) and BZ-periodic.
3. **Internal Verification Suite (Layer 5):**
   - 5a: Zero-frequency rigid body modes at $\Gamma$ ($\omega_1^2, \omega_2^2 < 10^{-12}$).
   - 5b: Full IBZ Hermiticity ($\|\bar{\bm{K}} - \bar{\bm{K}}^\mathsf{H}\|_\infty < 10^{-14}$).
   - 5c: Positive definiteness of $\bar{\bm{K}}, \bar{\bm{M}}$ at $\bm{k} \ne \bm{0}$.
   - 5d: Analytic long-wave acoustic limit matching PB2009 within $1.25 \times 10^{-8}$.
   - 5e: Lattice $C_{2v}/C_{4v}$ group symmetries along high-symmetry paths.
   - 5f: Continuous MAC branch tracking ($> 0.99$).
   - 5g: High-$k$ bounded phase velocity horizon $\bar{v}_p \to 0.3163$ vs theory $v_{T,\infty} = 1/\sqrt{10} \approx 0.3162$ within $0.03\%$, contrasted with unbounded divergence for $\ell_{\mathrm{i}}=0$ ($\bar{v}_p = 39.75$).
   - 5h: Poynting energy-flux and group-velocity identity $\bm{v}_g = \langle\bm{S}\rangle/(\langle W\rangle + \langle T\rangle)$ verified to $< 10^{-8}$.
   - 5i: Monotone mesh convergence ($4^2 \to 32^2$) with empirical rate $p=4.17$ ($95\%$ CI: $[3.15, 5.20]$) and operational resolution floor $\varepsilon_\Delta = 4.63 \times 10^{-11}$.
4. **Physical Deliverables:**
   - Directional stop band along $\Gamma$--$X$: $\Delta_{GX} = +0.0431$ ($\theta=45^\circ, \mathrm{AR}=10$), with global maximum $\Delta_{GX} = 0.0896$ at $(\theta=30^\circ, \mathrm{AR}=10)$.
   - Omnidirectional complete gap absence confirmed across all 42 map points ($\Delta_{\mathrm{complete}} \le -0.3758$).
   - Orientation sensitivity $S_\theta$ increasing monotonically up to $3.946\,\mathrm{rad}^{-1}$.
   - Acoustic steering deviation up to $\delta_{\max} = 2.79^\circ$ at $\bar{k}=0.5$.
   - Gradient energy partition $W_g/W$ increasing from $0.20\%$ to $16.49\%$.

---

## 5. Case-C De-scoping

### Proposed Governance Language
> *“Study S2 (Case C: Composite Phononic Crystal with Circular Inclusion) is formally de-scoped from the mandatory deliverables of Paper9 and reclassified as Follow-Up Research. The current manuscript focuses exclusively on the homogeneous metamaterial unit cell (Case H). All references, figure placeholders, and table columns pertaining to Case C are removed from the active manuscript and transferred to the follow-up research program.”*

### Technical & Scientific Justification
1. **Absence of Literature Standards (TV6, TV14):** Neither published literature nor Blueprint v1.3 specifies authoritative material constants, inclusion radius $R/L$, stiffness contrast $\mu_2/\mu_1$, density contrast $\rho_2/\rho_1$, or inclusion micro-inertia/length parameters. Arbitrary parameter selection violates project provenance rules. Furthermore, the reference-phase convention for non-dimensionalizing frequency ($\omega_0 = \sqrt{\mu/(\rho L^2)}$) in a two-phase cell is undefined.
2. **Discretization Incompatibility of Rectangular BFS Elements (TV18):** The Bogner–Fox–Schmit element is strictly an axis-aligned rectangular bicubic Hermite element ($Q_3$ tensor product). As proven algebraically in `audit_m14_independent.py` (check [Q6]), assigning material properties at Gauss points across elements cut by a circular boundary produces an $\mathcal{O}(h)$ boundary representation error. Conforming curved $C^1$ elements or adaptive cut-cell integration with higher-order traction jump conditions represent an independent methodological investigation.

### Exact Modifications to Blueprint v1.3
- **Section 3.5 (lines 381–383):** Remove sentence *“gaps exist only with periodic contrast (Case C) — a homogeneous cell shows dispersion but no Bragg gap”*. Replace with: *“Directional stop bands along high-symmetry paths are evaluated for the homogeneous cell (Case H); omnidirectional complete Bragg band gaps require multi-phase periodic contrast and are reserved for follow-up work.”*
- **Section 4.2 (Table line 620):** Remove row `Fig 7 | Case C: baseline band structure`.
- **Section 6.1 (lines 483–484):** Remove description of Case C. Frame Section 6.1 exclusively around the Case H homogeneous anisotropic unit cell.
- **Section 6.3 (line 485):** Delete Section 6.3 (*Case C baseline band structure*).
- **Calculation Master Plan Table 3.5 (line 256):** Mark S2 as *“DEFERRED / FUTURE WORK”*.
- **Table 5 (`tab05_gap_summary.tex`):** Remove Case C columns; retain Case H directional gaps ($\Delta_{GX}$), complete gap non-existence check ($\Delta_{\mathrm{complete}}$), and orientation sensitivity ($S_\theta$).

---

## 6. B1-B3 De-scoping

### Proposed Governance Language
> *“Published benchmarks B1 (Layer 1 classical bilayer limit), B2 (Layer 2a gradient bilayer), and B3 (Layer 2b dipolar gradient bilayer) are formally removed from the mandatory pre-submission validation gates (G3 and PCR1) of the Case-H manuscript. These benchmarks are reclassified as External Bilayer Reference Models outside the computational domain of the current homogeneous 2D finite element study.”*

### Explicit Rationale
This de-scoping does **not** assert that B1–B3 are scientifically invalid, nor that external validation is generally unnecessary. Rather, it acknowledges the following documented facts:
1. **Mathematical and Solver Architecture Mismatch:** The code developed in this project is a 2D conforming $C^1$ BFS finite element solver on a square unit cell. Benchmarks B1, B2, and B3 are 1D layered bilayers solved via semi-analytical transfer matrices. Benchmarking a 2D homogeneous unit cell solver against 1D bilayer dispersion curves represents fundamentally mismatched physics.
2. **Absence of Published Numerical Eigenvalue Data:** The published sources ([Li et al. 2024], *Sci. Rep.* 14:24035; [Li et al. 2023], *Waves Random Complex Media* 36:5715–5735) provide dispersion plots in raster/vector figure format only. Neither paper provides tabulated numerical frequencies, eigenvalues, or gap bounds.
3. **Prohibition of Curve Digitization as Error Metric:** Project governance strictly prohibits using digitized pixel coordinates as a numerical error metric for code validation (`P3_STATUS.md`). Quantitative percentage errors ($\le 0.5\%$ or $\le 2.0\%$) cannot be computed without verified numerical tables.
4. **Open Formulation Ambiguities (TV1, TV12):** Parameter ambiguities in the literature (e.g., missing non-dimensional parameters $c, d$ in Li et al. 2023 Fig 4(c) [TV1], and unstated axis ranges [TV12]) prevent unambiguous benchmark re-computation.

---

## 7. B6 Status

- **Status in v1.4:** **RETAINED AS INDEPENDENT TRANSFER-MATRIX CROSS-CHECK (PARTIAL)**.
- **Governing Rationale:** The independent 1D transfer-matrix formulation implemented in `paper9/validation/b6_lwz_tm/` verified analytical dispersion against Li, Wei & Zhou (2016) in the homogeneous limit ($1.429 \times 10^{-14}$) and identical-layer limit ($4.441 \times 10^{-16}$). 
- **Role in Manuscript:** Retained in the repository validation directory as mathematical evidence of transfer-matrix expertise. It is cited in Section 5 as an analytical formulation check, but does not serve as a gate requirement for the 2D BFS solver.

---

## 8. PCR1 Amendment

### Current Blueprint v1.3 Text (§9.4 line 884)
> *“PCR1. All mandatory published benchmarks (Layers 1, 2a, 2b) PASS with maximum relative error $\le 2\%$; the $\le 2\%$ criterion is retained (the $0.5\%$ target applies only to the classical limit).”*

### Proposed Blueprint v1.4 Replacement Text
> *“PCR1. Analytical and Asymptotic Benchmark Validation (Layer 3). The 2D $C^1$ BFS finite element formulation passes the closed-form analytical benchmarks against Papargyri-Beskou & Beskos (2009) [B5] to machine precision (relative frequency error $< 10^{-7}$ across all evaluated wavenumbers and long-wave acoustic slope error $< 10^{-8}$), and the high-$k$ phase velocity matches the closed-form asymptotic horizon $\bar{v}_{T,\infty} = \bar{l}_{\mathrm{eff}}/(\sqrt{10}\,\bar{\ell}_{\mathrm{i}}) = 1/\sqrt{10} \approx 0.3162$ within $0.05\%$.”*

---

## 9. PCR2 Amendment

### Current Blueprint v1.3 Text (§9.4 lines 887–889)
> *“PCR2. Benchmark configurations, exact parameters, model assumptions, non-dimensionalisation, reproduced dispersion curves, numerical comparisons and relative errors all appear in the main manuscript, not only in supplementary or internal files.”*

### Proposed Blueprint v1.4 Replacement Text
> *“PCR2. Verification Suite and Validation Scope Disclosure (Layers 3 & 5). The eight-test internal consistency suite (5a–5h), the mesh convergence sequence, and the analytical benchmark comparison (Layer 3) appear in full in the main manuscript (Section 5, Table 4, and Table 6). The manuscript explicitly discloses the de-scoping of external 1D layered transfer-matrix benchmarks (B1–B3) due to the absence of published tabulated numerical data and the architectural distinction between 2D unit-cell finite elements and 1D multi-layer transfer matrices.”*

---

## 10. G3 Amendment

### Current Blueprint v1.3 Definition (§9.2 line 822; Plan line 103)
> *“G3: blueprint-locked HARD gate: published validation Layers 1, 2a, 2b at $\le 2\%$ (0.5% classical target); evidence in main manuscript.”*

### Proposed Blueprint v1.4 Replacement Definition
> *“G3-H: Case-H Analytical & Internal Verification Gate.  
> 1. Closed-form analytical benchmark (Layer 3 vs PB2009) passes with relative error $< 10^{-7}$.  
> 2. High-$k$ asymptotic phase velocity horizon matches derivation M16 within $< 0.05\%$.  
> 3. Eight-test internal consistency suite (5a–5h) passes 100% of automated tests.  
> 4. Mesh convergence (5i) demonstrates monotone convergence with empirical rate $p=4.17$ and reported resolution floor $\varepsilon_\Delta = 4.63 \times 10^{-11}$.  
> 5. External 1D bilayer transfer-matrix benchmarks (B1–B3) are explicitly declared out of scope for the homogeneous Case H paper.”*

*(Note: Under this amendment, Gate G3-H is fully satisfied by existing verified calculations, pending formal approval).*

---

## 11. G4 Amendment

### Current Blueprint v1.3 Definition (§9.2 line 829, §9.4 line 907)
> *“The PI signs G4 only after PCR1--PCR8 are checked against the computation log. A failed PCR blocks submission exactly as G3 does.”*

### Proposed Blueprint v1.4 Replacement Definition
> *“G4-H: Case-H Standalone Submission Release Gate.  
> The PI signs Gate G4-H when:  
> 1. The manuscript source `ms.tex` is complete, coherent, and entirely free of `[BLOCKED — ...]` placeholders.  
> 2. All 16 Case-H verified floats (11 figures, 5 tables) are embedded with seamless, unbroken sequential numbering.  
> 3. Publication-Critical Requirements PCR1 through PCR8 (as amended in v1.4) are evidenced in the computation log.  
> 4. Mathematical consistency (prefactor $1/10$, passive frame rotation, Poynting energy flux identity) is verified.  
> 5. Numerical traceability of all reported values to raw datasets (`p5_production_raw.json`) is confirmed.  
> 6. All automated regression tests (59/59) pass with zero parameter lint violations.  
> 7. The manuscript PDF compiles cleanly with zero broken cross-references, missing floats, or undefined citations.  
> 8. The Limitations section explicitly discloses that multi-phase phononic crystals (Case C) and published 1D bilayer transfer-matrix benchmarks are reserved for future work.”*

---

## 12. Figure/Table Disposition

The candidate float inventory is adjusted from 19 candidate floats (16 embedded, 3 blocked) to **16 verified floats** (11 figures, 5 tables), with unbroken sequential numbering:

| Blueprint v1.3 ID | Proposed v1.4 Disposition | Revised Numbering in v1.4 | File Artifact Path | Content Description |
| :--- | :--- | :--- | :--- | :--- |
| **Fig 01** | Retained | **Figure 1** | `paper9/figures/out/fig01_ellipsoid_tensor.pdf` | Ellipsoidal domain $\mathcal{E}_0$ and rotated tensor components. |
| **Fig 02** | Retained | **Figure 2** | `paper9/figures/out/fig02_lattice_ibz.pdf` | Square unit cell and $\Gamma$--$X$--$M$--$\Gamma$ high-symmetry contour. |
| **Fig 03** | Retained | **Figure 3** | `paper9/figures/out/fig03_bfs_dof_bloch.pdf` | 32-DOF BFS layout and identical Bloch phase on derivative DOFs. |
| **Fig 04** | **DE-SCOPED** | *Omitted from MS* | *None* | External anchor overlays (B1–B3); moved to validation archive. |
| **Fig 05** | Retained | **Figure 4** | `paper9/figures/out/fig05_mesh_convergence.pdf` | Monotone mesh convergence ($4^2 \to 32^2$), $p=4.17$, $\varepsilon_\Delta = 4.63 \times 10^{-11}$. |
| **Fig 06** | Retained | **Figure 5** | `paper9/figures/out/fig06_caseH_dispersion.pdf` | Case H dispersion: $\mathrm{AR}=1$ vs $\mathrm{AR}=10$ ($\theta=0^\circ, 45^\circ$), $\Delta_{GX} = +0.0431$. |
| **Fig 07** | **DE-SCOPED** | *Omitted from MS* | *None* | Case C baseline bands & modes; deferred to Part II. |
| **Fig 08** | Retained | **Figure 6** | `paper9/figures/out/fig08_theta_sweep.pdf` | Orientation sweep ($\theta \in [0, 90^\circ]$ at $\mathrm{AR}=5$): $\bar{\omega}_T(X): 2.915 \to 2.672$. |
| **Fig 09** | Retained | **Figure 7** | `paper9/figures/out/fig09_ar_sweep.pdf` | Aspect ratio sweep ($\mathrm{AR} \in [1, 10]$ at $\theta=45^\circ$). |
| **Fig 10** | Retained | **Figure 8** | `paper9/figures/out/fig10_design_map_3d.pdf` | 3D surface and 2D contour over 42 points; global max $\Delta_{GX} = 0.0896$. |
| **Fig 11** | Retained | **Figure 9** | `paper9/figures/out/fig11_polar_map_regimes.pdf` | Polar classification $(X, Y) = (\mathrm{AR}\cos\theta, \mathrm{AR}\sin\theta)$ of stop-band regimes. |
| **Fig 12** | Retained | **Figure 10** | `paper9/figures/out/fig12_ifc_wave_steering.pdf` | Acoustic steering deviation $\delta(\phi)$ and $|\bm{v}_g|(\phi)$ along circular path $|\bar{\bm{k}}| = 0.5$. |
| **Fig 13** | Retained | **Figure 11** | `paper9/figures/out/fig13_energy_microinertia.pdf` | Gradient energy partition ($0.20\% \to 16.49\%$) and high-$k$ phase velocity horizon ($0.3162$). |
| **Tab 01** | Retained | **Table 1** | `paper9/tables/out/tab01_literature_positioning.tex` | Literature positioning matrix including reported-quantity column. |
| **Tab 02** | Retained | **Table 2** | `paper9/tables/out/tab02_parameters.tex` | Master parameter registry with provenance tags `[S]` and `[A]`. |
| **Tab 03** | **DE-SCOPED** | *Omitted from MS* | *None* | External anchor error table (B1–B3); moved to validation archive. |
| **Tab 04** | Retained | **Table 3** | `paper9/tables/out/tab04_consistency_suite.tex` | Eight-test consistency suite (5a–5h) with quantitative tolerances. |
| **Tab 05** | Retained | **Table 4** | `paper9/tables/out/tab05_gap_summary.tex` | Directional stop-band summary, complete gap check ($\le -0.3758$), and $S_\theta$. |
| **Tab 06** | Retained | **Table 5** | `paper9/tables/out/tab06_convergence_floor.tex` | Mesh convergence sequence ($4^2 \to 32^2$), $p=4.17$, $\varepsilon_\Delta = 4.63 \times 10^{-11}$. |

---

## 13. TV Register Disposition

Under the proposed Blueprint v1.4 amendment, the Technical Variations register is formally reclassified:

| TV ID | Item Description | Status in v1.3 | Proposed Status in v1.4 | Rationale & Governance Action |
| :--- | :--- | :--- | :--- | :--- |
| **TV1** | Anchor A Fig 4(c) non-dimensional parameters ($c, d$ set) | **OPEN** | **DEFERRED / OUT OF SCOPE** | Pertains strictly to external benchmark B3 (Li et al. 2023). Deferred to transfer-matrix validation study. |
| **TV6** | Case H vs Case C production parameters | **OPEN (Case C)** | **SPLIT / RESOLVED FOR CASE H** | Case H parameters are locked `[S]` in Table 2. Case C inclusion parameters are deferred to Part II. |
| **TV9** | Mishra et al. (2026) homogeneous limit configuration | **OPEN** | **DEFERRED / OUT OF SCOPE** | Pertains to optional Layer 4 cross-check. Deferred. |
| **TV12** | Overlay axis ranges and sampling for Figs 4(a)–(c) | **OPEN** | **DEFERRED / OUT OF SCOPE** | Pertains strictly to external benchmark Fig 4 overlays. Deferred. |
| **TV14** | Case C reference phase for non-dimensionalization | **OPEN** | **DEFERRED / OUT OF SCOPE** | Pertains strictly to Case C multi-phase unit cell. Deferred to Part II. |
| **TV18** | BFS circular inclusion representation | **OPEN** | **DEFERRED / OUT OF SCOPE** | Pertains strictly to Case C circular geometry on BFS grids. Deferred to Part II. |

*(Consequence: Zero open Technical Variations remain in the active critical path of the Case-H manuscript).*

---

## 14. Manuscript Claim Impact

A comprehensive change map across manuscript sections ensures total narrative consistency:

1. **Title:** Must be updated to reflect directional stop bands and wave steering rather than omnidirectional band gaps and full 2D isofrequency contours (see Section 15).
2. **Abstract:**
   - Remove claims of calculating full 2D isofrequency contours across the Brillouin zone.
   - Clarify that the investigated band gaps are *directional stop bands* along high-symmetry paths ($\Gamma$--$X$), with an explicit statement that homogeneous media do not produce complete omnidirectional band gaps.
   - Emphasize the four primary contributions: (i) 2D anisotropic tensor formulation with invariant positive eigenvalues; (ii) conforming $C^1$ BFS Bloch finite element implementation with derivative phase-tying; (iii) orientation-driven acoustic wave steering ($\delta_{\max} = 2.79^\circ$); and (iv) micro-inertia dynamic regularization yielding a bounded high-$k$ phase velocity horizon ($v_{T,\infty} = 0.3162$).
3. **Highlights:**
   - Highlight 1: Conforming $C^1$ BFS Bloch finite element formulation for 2D strain-gradient media.
   - Highlight 2: Anisotropic ellipsoidal length tensor induces directional stop bands along $\Gamma$--$X$.
   - Highlight 3: Microstructure orientation governs acoustic wave steering up to $\delta_{\max} = 2.79^\circ$.
   - Highlight 4: Micro-inertia enforces a strictly bounded high-$k$ phase velocity horizon ($v_{T,\infty} = 0.3162$).
   - Highlight 5: Rigorous 8-test verification suite establishes an empirical convergence rate $p=4.17$.
4. **Introduction (§1):**
   - Reframe stated research objectives around anisotropic metamaterials and directional wave filtering.
   - State up front that the paper focuses on the homogeneous unit cell with internal microstructure, citing composite phononic crystals as a distinct subsequent problem.
5. **Validation Section (§5):**
   - Remove placeholder Sections 5.2 and 5.3.
   - Streamline Section 5 to focus on: (i) Layer 3 closed-form analytical validation against PB2009 ($1.25 \times 10^{-8}$ error); (ii) Layer 3b asymptotic horizon validation; and (iii) Layer 5 internal verification (eight-test suite and mesh convergence).
   - Add a formal paragraph explicitly disclosing the de-scoping of external 1D bilayer transfer-matrix benchmarks due to the absence of published numerical tables.
6. **Results Section (§6):**
   - Remove Section 6.3 (Case C baseline).
   - Reframe Section 6.1 and 6.2 to present Case H as the primary physical model.
   - Retain Sections 6.4 (orientation sweep), 6.5 (aspect ratio sweep), 6.6 (3D design map), and 6.7 (polar regime map), ensuring all text describes directional stop bands along $\Gamma$--$X$.
7. **Wave Steering Section (§7):**
   - Update Section 7.1 prose to describe wave steering along the circular wave-vector contour $|\bar{\bm{k}}| = 0.5$ rather than closed 2D isofrequency contours.
   - Retain Sections 7.2 (group velocity deviation $\delta$), 7.3 (energy flux & Poynting identity), and 7.4 (micro-inertia physical admissibility).
8. **Limitations & Future Work (§8):**
   - State explicitly that the current investigation is restricted to homogeneous anisotropic media.
   - Identify two-phase composite unit cells with circular inclusions, higher-order interface jump conditions, and experimental/transfer-matrix bilayer benchmarking as future work.

---

## 15. Title-Scope Assessment

### Current Title
> *“Direction-dependent band gaps and iso-frequency contours in two-dimensional strain-gradient elastic media with anisotropic ellipsoidal microstructure: A Bloch–Floquet $C^1$ finite element analysis”*

### Defensibility Audit
1. **Term “band gaps”:** In phononic crystal literature, “band gaps” typically connotes complete, omnidirectional Bragg band gaps. In homogeneous Case H, an omnidirectional complete gap does not exist ($\Delta_{\mathrm{complete}} \le -0.3758$). Case H exhibits *directional stop bands* along $\Gamma$--$X$ ($\Delta_{GX} = +0.0431$). Retaining unqualified “band gaps” risks reviewer misunderstanding.
2. **Term “iso-frequency contours”:** Figure 12 plots group velocity $|\bm{v}_g|(\phi)$ and steering deviation $\delta(\phi)$ along a 1D circular wave-vector path $|\bar{\bm{k}}| = 0.5$. It does not plot full 2D closed isofrequency surfaces across $(k_x, k_y)$. Claiming “iso-frequency contours” in the title is factually inaccurate.

### Proposed Title Alternatives (for PI Selection)
- **Title Alternative 1 (Accurate and Descriptive):**  
  *“Direction-dependent stop bands and acoustic wave steering in two-dimensional strain-gradient elastic media with anisotropic ellipsoidal microstructure: A Bloch–Floquet $C^1$ finite element analysis”*
- **Title Alternative 2 (Blueprint v1.3 Line 871 Alternate Title A):**  
  *“Directional wave steering and microstructure-induced dispersion in strain-gradient media with anisotropic characteristic length tensor”*
- **Title Alternative 3 (Minimal Modification with In-Text Definition):**  
  *“Direction-dependent wave dispersion and acoustic steering in two-dimensional strain-gradient elastic media with anisotropic ellipsoidal microstructure: A Bloch–Floquet $C^1$ finite element analysis”*

---

## 16. Required Changes to Calculation Master Plan

If Blueprint v1.4 is approved, the following corresponding changes will be made to `CALC_MASTER_PLAN.md`:
1. **Section 1.2 (Gate Terminology Map):** Replace Gate G3 with Gate G3-H (Analytical and internal verification gate).
2. **Section 2 (Phased Workflow):** 
   - Phase 3 is updated: Benchmarks B1, B2, B3 marked as deferred; Layer 3 (B5) and Layer 3b (B6) formalize Phase 3 exit.
   - Phase 5 is updated: Study S2 is removed from the Phase 5 execution path; Studies S1, S3–S9 constitute complete Phase 5 exit (Gate G5).
3. **Section 3.1 (Benchmark Cards):** Cards B1, B2, and B3 are marked *“DEFERRED / EXTERNAL”*. Card B5 is marked *“PRIMARY VALIDATION GATE (PASS)”*.
4. **Section 3.5 (Study Definitions):** Study S2 marked *“DEFERRED TO PART II”*.
5. **Section 3.6 (Float Master Table):** Remove Fig 4, Tab 3, and Fig 7 from the active float table.
6. **Appendix B (Gates):** Gate G4 updated to G4-H.

---

## 17. Required Approval / Governance Action

To enact this proposal, the Project Investigator (PI) / Governance Authority must take the following formal actions:
1. **Sign Approval Directive:** Formally execute the approval directive approving Blueprint v1.4.
2. **Select Manuscript Title:** Formally designate one of the title alternatives in Section 15.
3. **Authorize Phase 11 Execution:** Authorize the execution phase to:
   - Commit `PROPOSED_BLUEPRINT_V1_4_AMENDMENT.md` as `Paper9_Blueprint_v1.4.tex`.
   - Update `CALC_MASTER_PLAN.md` to Revision 1.2.
   - Update `paper9/latex/ms.tex` and modular section files to remove blocked placeholders, apply revised title, and re-sequence the 16 verified floats.
   - Re-compile `ms.pdf` and verify zero LaTeX warnings/errors.
   - Formally sign off on Gate G3-H and Gate G4-H.

---

## 18. Before-vs-After Gate Matrix

| Item | Blueprint v1.3 | Proposed v1.4 | Reason | Approval Required |
| :--- | :--- | :--- | :--- | :--- |
| **B1** | MANDATORY (Hard Gate G3) | **DEFERRED / OUT OF SCOPE** | 1D bilayer transfer matrix vs 2D unit cell; no published numerical tables. | **YES (PI Approval)** |
| **B2** | MANDATORY (Hard Gate G3) | **DEFERRED / OUT OF SCOPE** | 1D bilayer transfer matrix vs 2D unit cell; no published numerical tables. | **YES (PI Approval)** |
| **B3** | MANDATORY (Hard Gate G3, decisive) | **DEFERRED / OUT OF SCOPE** | TV1 open ($c, d$ set); no published numerical tables; 1D physics. | **YES (PI Approval)** |
| **B6** | OPTIONAL (Layer 3b analytic check) | **RETAINED (PARTIAL)** | Independent formulation cross-check in validation repo; not a gate. | None |
| **S2** | MANDATORY (Fig 7, Table 5) | **DEFERRED TO PART II** | Missing contrast parameters (TV6, TV14); BFS boundary error (TV18). | **YES (PI Approval)** |
| **PCR1** | MANDATORY (Hard submission gate) | **AMENDED (Layer 3 & Asymptotics)** | Focuses validation on verified continuum analytical checks ($< 10^{-7}$). | **YES (PI Approval)** |
| **PCR2** | MANDATORY (Main text overlays) | **AMENDED (Disclosure & Layer 5)** | Replaces external bilayer overlays with Layer 5 consistency suite. | **YES (PI Approval)** |
| **G3** | NOT MET (Hard blocker) | **REPLACED BY G3-H (MET)** | Satisfied by Layer 3 ($1.25 \times 10^{-8}$) and Layer 5 (59 tests pass). | **YES (PI Approval)** |
| **G4** | NOT MET (Blocked by G3 & S2) | **REPLACED BY G4-H (SIGNABLE)** | Signable upon placeholder removal and compilation of 16-float MS. | **YES (PI Approval)** |
| **Fig4** | BLOCKED PLACEHOLDER | **OMITTED FROM MS** | Pertains to de-scoped B1–B3 benchmarks. | **YES (PI Approval)** |
| **Fig7** | BLOCKED PLACEHOLDER | **OMITTED FROM MS** | Pertains to de-scoped Case C study. | **YES (PI Approval)** |
| **Table3** | BLOCKED PLACEHOLDER | **OMITTED FROM MS** | Pertains to de-scoped B1–B3 benchmarks. | **YES (PI Approval)** |
| **TV1** | OPEN | **DEFERRED / OUT OF SCOPE** | Pertains to B3. | **YES (PI Approval)** |
| **TV6** | OPEN (Case C) | **RESOLVED FOR CASE H / DEFERRED (C)** | Case H locked `[S]`; Case C deferred to Part II. | **YES (PI Approval)** |
| **TV12** | OPEN | **DEFERRED / OUT OF SCOPE** | Pertains to Fig 4 overlays. | **YES (PI Approval)** |
| **TV14** | OPEN | **DEFERRED / OUT OF SCOPE** | Pertains to Case C. | **YES (PI Approval)** |
| **TV18** | OPEN | **DEFERRED / OUT OF SCOPE** | Pertains to Case C. | **YES (PI Approval)** |

---

## 19. Scientific Limitations That Must Remain Explicit

To maintain the highest standards of scientific ethics and peer-review rigor, the following five limitations must be explicitly disclosed in the revised manuscript (specifically in Sections 1, 5, and 8):
1. **Homogeneous Microstructure vs Periodic Phononic Crystals:** The manuscript must state clearly that the analysis applies to a homogeneous elastic continuum with internal microstructural length scales (Case H), and does not examine periodic impedance contrast between distinct constituent materials (Case C).
2. **Directional Stop Bands vs Omnidirectional Complete Gaps:** The manuscript must maintain the strict inequality $\Delta[\text{leg}] \ge \Delta[\text{path}] \ge \Delta[\text{complete}]$ and explicitly emphasize that the directional stop bands observed along $\Gamma$--$X$ do not constitute complete omnidirectional band gaps, which are rigorously absent ($\Delta_{\mathrm{complete}} \le -0.3758$).
3. **Validation Scope and Omission of Multi-Layer Benchmarks:** The manuscript must explicitly disclose that external published bilayer benchmarks (B1–B3) were not incorporated into quantitative solver validation because the source papers lacked tabulated numerical eigenvalues, curve digitization was rejected as an unscientific error metric, and the 2D unit-cell FEM formulation represents distinct physics from 1D transfer matrices.
4. **Wave Steering Contour vs 2D Isofrequency Surfaces:** The manuscript must describe the wave steering analysis as being evaluated along a 1D circular wave-vector contour of radius $|\bar{\bm{k}}| = 0.5$ in reciprocal space, rather than claiming full 2D closed isofrequency contours across the entire Brillouin zone.
5. **Operational Boundary Operator:** The manuscript must note that the operational finite element model utilizes the reduced four-quantity boundary operator, which is exact for Bloch-periodic unit cells lacking free boundaries, while tangential boundary redistribution and corner force terms are omitted.

---

## 20. Implementation Prohibition

> **“This document is a proposed governance amendment only. It does not itself alter Blueprint v1.3, gate status, manuscript content, solver implementation, validation status, or release status.”**
