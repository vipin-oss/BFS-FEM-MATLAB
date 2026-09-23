# P8 Forensic Manuscript Audit Report

**Date:** 2026-09-23  
**Repository:** `https://github.com/vipin-oss/BFS-FEM-MATLAB`  
**Audited Branch:** `phase-1-symbolic`  
**Audited HEAD Commit:** `610f401032e74f4217c457eea6e679aa58224c57`  
**Auditor:** P8 Forensic Manuscript Audit Agent  
**Operational Mode:** STRICT READ-ONLY AUDIT  
**Audit Decision:** `P8_PASS_WITH_REMEDIATION`

---

## 1. Repository State

Prior to beginning the audit, the repository environment and Git boundaries were inspected and verified against the absolute safety rules:

```bash
git status
# On branch phase-1-symbolic
# Your branch is up to date with 'origin/phase-1-symbolic'.
# nothing to commit, working tree clean

git branch --show-current
# phase-1-symbolic

git rev-parse HEAD
# 610f401032e74f4217c457eea6e679aa58224c57

git rev-parse origin/phase-1-symbolic
# 610f401032e74f4217c457eea6e679aa58224c57

git rev-parse origin/main
# 1de47a4d111260ffb9b48d7c99e9db45102367c7
```

- **Branch:** `phase-1-symbolic`
- **HEAD SHA:** `610f401032e74f4217c457eea6e679aa58224c57` (synchronized with `origin/phase-1-symbolic`)
- **Main Branch:** `origin/main` remains untouched at `1de47a4d111260ffb9b48d7c99e9db45102367c7`
- **Working Tree:** Pristine clean before authoring this audit report. No solver, code, figure, table, or manuscript source files were modified.

---

## 2. Audit Scope

This forensic audit evaluates the limited-scope manuscript established during Phase 7 (`paper9/latex/ms.tex`, modular section files in `paper9/latex/sections/`, Appendices A and B, bibliography `paper9/bib/paper9.bib`, and supporting audit reports).

The audit cross-checks all manuscript content against authoritative repository sources:
1. Master derivation documents: `paper9/eqs/phase1/derivations/DERIVATION_M01_M07.md` through `DERIVATION_M17.md`
2. Architectural specifications: Blueprint v1.3 (`paper9/plan/blueprint/Paper9_Blueprint_v1.3.tex`) and Master Calculation Plan (`paper9/plan/CALC_MASTER_PLAN.md`)
3. Traceability matrices: `paper9/audit/traceability_matrix.csv`
4. Prior forensic gate audits: `paper9/audit/P6_FINAL_GATE_AUDIT.md` and `paper9/audit/P7_LIMITED_SCOPE_DRAFT_AUDIT.md`
5. Computational evidence: P5 raw production datasets (`paper9/results/raw/p5_production_raw.json`), simulation parameters (`paper9/params/p5_pilot_params.yaml`), and generated figure/table artifacts (`paper9/figures/out/`, `paper9/tables/out/`)
6. Verification test suites: 51 automated regression test functions in `paper9/production/p5/` and `paper9/verification/suite/`.

---

## 3. Mathematical Consistency

Every governing equation in the manuscript was evaluated against the locked derivations:

1. **Ellipsoidal Averaging Domain & Second-Moment Tensor ($\mathbf{L}_0$):**
   - Manuscript: Eqs. (1)–(3) define $\mathcal{E}_0$ with semi-axes $l_1, l_2$ and volume-equivalent constraint $\det(\mathbf{L}_0) = l_{\mathrm{iso}}^4$.
   - Authority: `DERIVATION_M01_M07.md` §M1 and Blueprint (1)–(4).
   - Verdict: **CONSISTENT**.
2. **Passive Rotation Convention & Length Tensor $\mathbf{L}(\theta)$:**
   - Manuscript: Eqs. (4)–(6) specify $\bm{x}' = \bm{R}(\theta)\bm{x}$ with $\bm{R}(\theta) = \begin{bmatrix} \cos\theta & \sin\theta \\ -\sin\theta & \cos\theta \end{bmatrix}$ and $\mathbf{L}(\theta) = \bm{R}^\mathsf{T} \mathbf{L}_0 \bm{R}$. Explicit components $L_{11}, L_{22}, L_{12}$ match locked passive rotation.
   - Authority: `DERIVATION_M01_M07.md` §M2 and Blueprint (5)–(9).
   - Verdict: **CONSISTENT**.
3. **Positive Definiteness Invariance:**
   - Manuscript: Eq. (7) demonstrates $\mathrm{spec}(\mathbf{L}(\theta)) \equiv \{l_1^2, l_2^2\} > 0$ for all $\theta$, guaranteeing positive definiteness under rotation.
   - Authority: `DERIVATION_M01_M07.md` §M2.5 and Blueprint (25).
   - Verdict: **CONSISTENT**.
4. **Kinematics & Strain Gradients:**
   - Manuscript: Eqs. (8)–(9) state $\varepsilon_{ij} = \frac{1}{2}(u_{i,j}+u_{j,i})$ and $\eta_{ijk} = \varepsilon_{ij,k}$. Component counts (3 strains, 6 strain gradients in 2D plane strain) match locked derivation.
   - Authority: `DERIVATION_M01_M07.md` §M3 and Blueprint (10)–(12).
   - Verdict: **CONSISTENT**.
5. **Mindlin Form-II Constitutive Relations & Pre-Factor:**
   - Manuscript: Section 2.4, Eq. (12) defines Cauchy stress $\sigma_{ij} = C_{ijkl}\varepsilon_{kl}$ and double stress $\tau_{ijk} = L_{kl} C_{ijmn}\eta_{mnl}$.
   - Authority: `DERIVATION_M01_M07.md` §M4 and Blueprint Eq. (26) state $\tau_{ijk} = \frac{1}{10} L_{kl} C_{ijmn}\eta_{mnl}$ where the factor $1/10$ originates from the second moment of the 3D ellipsoid.
   - Discrepancy: Section 2.4 Eq. (12) and Section 4.2 Eq. (18) omit the scalar factor $1/10$ in the displayed expression. Recorded as **Finding 5** (MEDIUM).
6. **Micro-Inertia Formulation & Strong Form:**
   - Manuscript: Section 2.5, Eqs. (13)–(14) define $T = \frac{1}{2}\rho \dot u_i \dot u_i + \frac{1}{2}\rho \ell_{\mathrm{i}}^2 \dot u_{i,j}\dot u_{i,j}$ and bulk equilibrium $\sigma_{ij,j} - \tau_{ijk,jk} = \rho(\ddot u_i - \ell_{\mathrm{i}}^2 \ddot u_{i,jj})$.
   - Authority: `DERIVATION_M08.md` §M8.2 and Blueprint (19)–(21), (31).
   - Verdict: **CONSISTENT**.
7. **Boundary Operators:**
   - Manuscript: Eq. (15) defines effective classical traction $p_i = \sigma_{ij}n_j - n_j n_k \tau_{ijk,k}$ and double traction $R_i = n_j n_k \tau_{ijk}$.
   - Authority: `DERIVATION_M08.md` §M8.3 and Blueprint (32)–(35).
   - Verdict: **CONSISTENT**.
8. **Bloch Ansatz & Derivative Degrees of Freedom:**
   - Manuscript: Section 3.2, Eqs. (18)–(19) derive that $u_i$, $\nabla u_i$, and $\frac{\partial^2 u_i}{\partial x \partial y}$ all transform with the identical Bloch phase $e^{\iu \bm{k}\cdot\bm{a}_\alpha}$.
   - Authority: `DERIVATION_M09.md` and Blueprint (39)–(43).
   - Verdict: **CONSISTENT**.
9. **Reduced Hermitian Eigenproblem:**
   - Manuscript: Section 4.5, Eqs. (22)–(23) define $[\bar{\bm{K}}(\bm{k}) - \omega^2 \bar{\bm{M}}(\bm{k})]\bar{\bm{d}} = \bm{0}$ and prove Hermiticity $\bar{\bm{K}}^\mathsf{H} = \bar{\bm{K}}, \bar{\bm{M}}^\mathsf{H} = \bar{\bm{M}} > 0$.
   - Authority: `DERIVATION_M15.md` and Blueprint (66)–(68).
   - Verdict: **CONSISTENT**.

---

## 4. Symbol and Notation Audit

A systematic scan of all notation across the manuscript was executed:
- **$\lambda, \mu, \rho$:** Standard isotropic Lamé moduli and mass density; consistently used throughout.
- **$\ell_{\mathrm{i}}$ vs $l$:** Consistently distinguished: $\ell_{\mathrm{i}}$ denotes scalar micro-inertia length parameter, while $l$ ($l_{\mathrm{iso}}, l_1, l_2$) denotes characteristic gradient-stiffness lengths.
- **$L$ (scalar unit cell constant) vs $\mathbf{L}$ (second-order length tensor):** Disambiguated by formatting ($L$ italic scalar vs $\mathbf{L}$ bold uppercase tensor / $L_{ij}$ indexed components).
- **$\mathrm{AR}$ and $\theta$:** Aspect ratio $l_1/l_2$ and orientation angle in degrees ($^\circ$) or radians ($\mathrm{rad}$). Explicitly tracked and labeled with units.
- **Wavenumber & Frequency Normalization:** Non-dimensional $\bar{k} = k L / \pi$ and $\bar{\omega} = \omega / \omega_0$ with $\omega_0 = \sqrt{\mu/(\rho L^2)}$ are consistently applied.
- **Gaps & Convergence:** $\Delta[\text{leg}], \Delta[\text{path}], \Delta[\text{complete}]$ and $\varepsilon_\Delta$ are uniquely defined.

---

## 5. Dimensional and Nondimensional Audit

All normalized equations and reported data were checked against the locked non-dimensionalization rules:
- $\bar{k} = k L / \pi$ (so the zone edge $X$ is at $\bar{k}_x = 1.0$).
- $\bar{\omega} = \omega / \omega_0$ where $\omega_0 = \sqrt{\mu/(\rho L^2)}$.
- Acoustic wave speeds: $c_T = 1.0$, $c_L = \sqrt{3} \approx 1.73205$ for $\lambda/\mu = 1.0, \nu = 0.25$.
- Normalized phase velocity: $\bar{v}_p = (\omega/k)/\sqrt{\mu/\rho} = \bar{\omega}/(\pi \bar{k})$.
- Asymptotic phase velocity: $\bar{v}_{T,\infty} = \bar{l}_{\mathrm{eff}} / (\sqrt{10}\,\bar{\ell}_{\mathrm{i}})$.
- Check: All simulation data in `p5_production_raw.json` adhere to this exact non-dimensional scaling.

---

## 6. Numerical Traceability

Every numerical value stated in the manuscript prose, tables, and figure captions was cross-referenced against `p5_production_raw.json`, `p5_pilot_params.yaml`, and verification test logs:

| Item | Manuscript Value | Authoritative Source | Source Value | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Complete Gap Bound** | $\Delta_{\mathrm{complete}} \le -0.3758$ | `p5_production_raw.json` (`study_S5`) | $-0.375848$ | **VERIFIED** |
| **Convergence Rate** | $p = 4.17$ | `tab06_convergence_floor.tex` | $4.17$ | **VERIFIED** |
| **95% CI** | $[3.15, 5.20]$ | `tab06_convergence_floor.tex` | $[3.15, 5.20]$ | **VERIFIED** |
| **Resolution Floor** | $\varepsilon_\Delta = 4.63 \times 10^{-11}$ | `tab06_convergence_floor.tex` | $4.63 \times 10^{-11}$ | **VERIFIED** |
| **Peak Steering Angle** | $\delta_{\max} = 2.79^\circ$ | `p5_production_raw.json` (`study_S7`) | $2.786599^\circ$ | **VERIFIED** |
| **Orientation Sensitivity** | $S_\theta = 3.946\,\mathrm{rad}^{-1}$ | `p5_production_raw.json` (`study_S6`) | $3.946480\,\mathrm{rad}^{-1}$ | **VERIFIED** |
| **Gradient Energy ($\bar{k}=0.1$)** | $W_g/W = 0.20\%$ | `p5_production_raw.json` (`study_S8`) | $0.001970 \implies 0.20\%$ | **VERIFIED** |
| **Gradient Energy ($\bar{k}=1.0$)** | $W_g/W = 16.49\%$ | `p5_production_raw.json` (`study_S8`) | $0.164852 \implies 16.49\%$ | **VERIFIED** |
| **High-$k$ Bounded Speed** | $\bar{v}_p = 0.3163$ ($\bar{k}=200$) | `p5_production_raw.json` (`study_S9`) | $0.316318$ | **VERIFIED** |
| **High-$k$ Unbounded Speed** | $\bar{v}_p = 39.75$ ($\bar{k}=200$) | `p5_production_raw.json` (`study_S9`) | $39.750933$ | **VERIFIED** |
| **Acoustic Error** | $1.25 \times 10^{-8}$ | `p4a_5a_to_5f.py` log (Test 5d) | $1.253 \times 10^{-8}$ | **VERIFIED** |
| **Fig 6 Stop Band** | $\Delta_{GX} = 0.0898$ | `p5_production_raw.json` | $T_g/T = 0.08983$ (flux) | **DISCREPANCY (Finding 1)** |
| **Fig 6 Parameters** | $\rho=1000, \mu=1\,\mathrm{GPa}, \ell_i=0.1$ | `tab02_parameters.tex` | $\rho=1.0, \mu=1.0, \ell_i=0.20$ | **DISCREPANCY (Finding 1)** |
| **Design Map Max Gap** | $\Delta_{GX} = 0.1654$ | `p5_production_raw.json` (`study_S5`) | $\max \Delta_{GX} = 0.08960$ | **DISCREPANCY (Finding 2)** |
| **$\theta$-Sweep Migration** | $\bar{\omega}_T(X): 1.154 \to 0.812$ | `p5_production_raw.json` (`study_S3`) | $2.9153 \to 2.6719$ | **DISCREPANCY (Finding 3)** |
| **App A Asymptotic Horizon**| $l_2=0.10, \ell_i=0.3162$ | Table 2 / M16 derivation | $l_{\mathrm{iso}}=0.20, \ell_i=0.20$ | **DISCREPANCY (Finding 4)** |

---

## 7. Figure–Text Audit

Every embedded figure was inspected for fidelity against its caption, manuscript discussion, and generating script:

- **Figure 1 (`fig01_ellipsoid_tensor.pdf`):** Accurately presents averaging ellipses for $\mathrm{AR} \in \{1, 3, 5, 10\}$ and passive rotation tensor components $L_{11}, L_{22}, L_{12}$ with negative off-diagonal $L_{12}(45^\circ) = -0.096\,\mathrm{m}^2$.
- **Figure 2 (`fig02_lattice_ibz.pdf`):** Correctly shows square periodic unit cell and $\Gamma$--$X$--$M$--$\Gamma$ high-symmetry contour.
- **Figure 3 (`fig03_bfs_dof_bloch.pdf`):** Correctly illustrates the 32-DOF BFS layout and identical Bloch phase transformations on displacement and derivative DOFs.
- **Figure 5 (`fig05_mesh_convergence.pdf`):** Monotone convergence across $4^2 \to 32^2$ elements; empirical rate $p=4.17$ and resolution floor $\varepsilon_\Delta = 4.63 \times 10^{-11}$.
- **Figure 6 (`fig06_caseH_dispersion.pdf`):** Plotted data in `fig06_caseH_dispersion.py` displays $\mathrm{AR}=1$ vs $\mathrm{AR}=10$ ($\theta=0^\circ$ and $45^\circ$), whereas caption and Section 6.2 text claim $\mathrm{AR}=5$. Caption also lists non-standard dimensional parameters. Recorded as **Finding 1** (HIGH).
- **Figure 8 (`fig08_theta_sweep.pdf`):** Accurately plots $\bar{\omega}_T(X)$, $\bar{\omega}_L(X)$, and corner frequencies at $M$ demonstrating diagonal symmetry. Prose misstates the frequency values ($1.154 \to 0.812$ instead of $2.915 \to 2.672$). Recorded as **Finding 3** (HIGH).
- **Figure 9 (`fig09_ar_sweep.pdf`):** Accurately plots aspect ratio sweep $\mathrm{AR} \in [1, 10]$ at $\theta=45^\circ$.
- **Figure 10 (`fig10_design_map_3d.pdf`):** Accurately visualizes response surface and 2D contour over 42 grid points. Caption and Section 6.6 text claim a maximum of $\Delta_{GX} = 0.1654$, whereas the plotted data has a maximum of $0.0896$. Recorded as **Finding 2** (HIGH).
- **Figure 11 (`fig11_polar_map_regimes.pdf`):** Accurately maps pass-band vs stop-band regimes in polar space $(X, Y) = (\mathrm{AR}\cos\theta, \mathrm{AR}\sin\theta)$.
- **Figure 12 (`fig12_ifc_wave_steering.pdf`):** Accurately presents steering deviation $\delta(\phi)$ and $|\bm{v}_g|(\phi)$ along the circular path $|\bar{\bm{k}}| = 0.5$. Text strictly describes this as circular wave-vector steering without asserting a closed 2D IFC.
- **Figure 13 (`fig13_energy_microinertia.pdf`):** Accurately displays monotonic growth of $W_g/W$ and high-$k$ phase velocity asymptotics bounding to $0.3162$ for $\ell_{\mathrm{i}} > 0$ vs diverging to $39.75$ for $\ell_{\mathrm{i}} = 0$.

---

## 8. Table–Text Audit

Every embedded table was inspected for LaTeX formatting safety and numerical accuracy:

- **Table 1 (`tab01_literature_positioning.tex`):** Positioning matrix correctly embeds without errors. Clean formatting and accurate citations.
- **Table 2 (`tab02_parameters.tex`):** Master parameters table includes provenance tags `[S]` and `[A]`. LaTeX escaping of set braces and units is clean.
- **Table 4 (`tab04_consistency_suite.tex`):** 8 consistency checks (5a–5h) match `p4a_5a_to_5f.py` and `p4b_5g_to_5i.py` exactly. Scientific notation is correctly formatted.
- **Table 5 (`tab05_gap_summary.tex`):** Gap summary table correctly reflects `study_S5` data, verifying $\Delta[\text{leg}] \ge \Delta[\text{path}] \ge \Delta[\text{complete}]$ across all entries and listing orientation sensitivity $S_\theta$ up to $3.946\,\mathrm{rad}^{-1}$.
- **Table 6 (`tab06_convergence_floor.tex`):** Mesh convergence metrics match `fig05` and text ($p=4.17$, $\varepsilon_\Delta = 4.63 \times 10^{-11}$).
- **LaTeX Safety:** All ampersands, underscores, and special characters in embedded tables are properly escaped. Zero compilation warnings or bad boxes.

---

## 9. Verification vs Validation Audit

A rigorous terminological audit was performed on all occurrences of "validation", "verification", and related variants:
- **Gate G3 & Criterion PCR1:** Both explicitly preserved as NOT MET / NOT PASS in Sections 5.1, 5.2, 5.3, and 8.3.
- **Benchmarks B1, B2, B3:** Accurately designated as UNVALIDATED.
- **Benchmark B6:** Accurately preserved as PARTIAL.
- **Verification vs Validation Lexicon:** Internal numerical consistency checks (5a–5h), mesh convergence, and algebraic identities are properly designated as "verification".
- **Minor Lexical Finding:** In Section 7.4 (line 34), the phrase *"This validates the constitutive role of micro-inertia..."* is used in an informal sense. While scientifically clear in context, it is flagged under **Finding 6** (LOW) for lexical precision.

---

## 10. Band-Gap Scientific Audit

A dedicated text scan was conducted across all files for band-gap taxonomy and claims:
- **Nested Set Inequality:** $\Delta[\text{leg}] \ge \Delta[\text{path}] \ge \Delta[\text{complete}]$ is rigorously defined in Section 3.4 and confirmed across 100% of evaluated configurations.
- **Case H Complete Band Gap:** Every mention of Case H band gaps strictly identifies them as directional stop bands ($\Delta_{GX} > 0$).
- **Non-positive Complete Gap:** The manuscript repeatedly and explicitly states that homogeneous Case H has no complete band gap ($\Delta_{\mathrm{complete}} \le -0.3758$).
- **Omnidirectional Claims:** No claim of an omnidirectional or complete band gap is made for Case H anywhere in the manuscript.

---

## 11. Convergence Audit

Statements regarding mesh convergence and asymptotic behavior were inspected:
- **Empirical Fit:** The convergence rate is consistently stated as an empirical least-squares power-law fit ($p = 4.17$, $95\%$ CI: $[3.15, 5.20]$).
- **Absence of Over-Claims:** No assertion of theoretical fourth-order convergence ($\mathcal{O}(h^4)$ or $\mathcal{O}(h^{4.17})$) is made.
- **Operational Floor:** The numerical resolution floor is documented as $\varepsilon_\Delta = 4.63 \times 10^{-11}$.

---

## 12. High-$k$ Asymptotic Audit

Appendix A was audited against the locked derivation `DERIVATION_M16.md`:
- **Bounded Horizon:** The existence of a finite high-$k$ phase velocity horizon for $\ell_{\mathrm{i}} > 0$ versus an unbounded speed for $\ell_{\mathrm{i}} = 0$ is proven and verified.
- **Constitutive Pre-Factor Discrepancy:** The 1D PDE in Appendix A wrote $\mu l^2 \partial^4 u/\partial x^4$ instead of $\frac{1}{10}\mu l_{\mathrm{eff}}^2 \partial^4 u/\partial x^4$, omitting the second-moment factor $1/10$. Consequently, the formula was stated as $\bar{v}_{T,\infty} = \bar{l}/\bar{\ell}_{\mathrm{i}}$, and synthetic parameter values ($l_2 = 0.10, \ell_i = 0.3162277$) were plugged in to reach $0.3162$, whereas the authoritative derivation M16 yields $\bar{v}_{T,\infty} = \bar{l}_{\mathrm{eff}}/(\sqrt{10}\,\bar{\ell}_{\mathrm{i}})$ which attains $0.3162277$ with the true Table 2 baseline parameters ($l_{\mathrm{iso}} = 0.20, \ell_{\mathrm{i}} = 0.20$). Recorded as **Finding 4** (HIGH).

---

## 13. Energy-Flux Audit

Appendix B was audited against `DERIVATION_M17.md`:
- **Poynting Theorem:** Local balance $\partial_t(W+T) + \nabla\cdot\bm{S} = 0$ is rigorously derived.
- **Flux Components:** Classical traction power, double-stress power, and micro-inertia flux are all included.
- **Group Velocity Identity:** $\bm{v}_g = \langle\bm{S}\rangle/(\langle W\rangle + \langle T\rangle)$ is correctly derived and cross-referenced to Test 5h.
- **Index Placement:** In Eq. (72), the double stress power term $\tau_{ijk}\dot u_{i,k}$ places the divergence index in the second position rather than the third position $\tau_{ikj}\dot u_{i,k}$ from M17. Recorded as **Finding 7** (LOW).

---

## 14. Abstract, Highlights, and Conclusions Audit

Front and back matter were examined for claim inflation:
- **Abstract:** Accurately reflects limited scope, cites Layer 5 verification, reports Case H directional stop bands without complete gaps, and states that literature benchmarking is an open verification gateway.
- **Highlights:** 5 bullets strictly adhering to verified deliverables. Zero claims of literature validation or complete band gaps.
- **Conclusions:** 6 numbered items summarizing verified findings. Item 4 cites directional stop bands up to $\Delta_{GX} = 0.1654$ (flagged under **Finding 2**), but correctly reinforces the absence of complete band gaps.

---

## 15. Introduction and Novelty Audit

Section 1 was checked for literature positioning and novelty assertions:
- **Hedged Claims:** Phrases such as "to the best of our knowledge" and "within the scope of published literature" are consistently employed.
- **No False Reproduction Claims:** Does not claim numerical reproduction of anchors A, B, or C.
- **Table 1 Support:** Positioning claims in Section 1.4 directly align with the columns of Table 1.

---

## 16. Citation and Reference Audit

The bibliography `paper9/bib/paper9.bib` and citations in the text were audited:
- **Total BibTeX Entries:** 15.
- **Citations in Text:** 15 unique keys.
- **Orphan Entries:** 0 (all 15 references are cited in the body text).
- **Undefined Citations:** 0.
- **Metadata Accuracy:** DOIs, authors, journals, volumes, and page numbers match authentic published literature records.

---

## 17. Cross-Reference Audit

All internal LaTeX cross-references were verified:
- **Total Labels Defined:** 102.
- **Total References (`\ref`):** 25.
- **Undefined References:** 0.
- **Stale or Broken References:** 0.
- **Float References:** All 16 embedded floats (11 figures, 5 tables) are referenced with exact Blueprint numbering and zero gaps.

---

## 18. Compilation Audit

A comprehensive syntax and structure audit was performed:
- **Environment Matching:** All 11 section files and `ms.tex` have 100% paired `\begin{...}` and `\end{...}` blocks.
- **File Inclusions:** All 11 `\input{...}` files exist and resolve properly.
- **Image Files:** All 11 `\includegraphics{...}` files exist as valid, non-empty vector PDFs.
- **Table Inclusions:** All 5 table files exist and are valid LaTeX tabular environments.
- **Regression Tests:** 51/51 pytest functions pass cleanly.
- **Parameter Lint:** 0 violations.

---

## 19. Findings Register

The complete register of forensic findings is compiled below:

| ID | Location | Finding | Severity | Evidence | Scientific Impact | Recommended Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FIND-01** | `sec06_results.tex`, Sec 6.2, lines 10–15 | Figure 6 caption and text state $\mathrm{AR}=5$ and quote $\Delta_{GX} = 0.0898$, whereas the plotted data is $\mathrm{AR}=10$ ($\theta=0^\circ, 45^\circ$) and $0.0898$ is the energy flux ratio $T_g/T$. Caption also lists discordant parameters. | **HIGH** | `fig06_caseH_dispersion.py`, `p5_production_raw.json` (`study_S1` and `study_S8`) | Discrepancy between figure, prose, and raw data; does not affect physical conclusion. | In P9, update caption and prose to reflect $\mathrm{AR}=10$, list correct parameters ($\rho=1, \mu=1, \ell_i=0.2$), and quote exact gap values from Table 5. |
| **FIND-02** | `sec06_results.tex`, lines 58, 62; `sec08_discussion.tex`, line 8; `sec09_conclusions.tex`, line 9 | Text states maximum directional gap is $\Delta_{GX} = 0.1654$ at $(\theta=45^\circ, \mathrm{AR}=10)$, whereas raw data in `study_S5` shows global maximum is $0.08960$ at $(\theta=30^\circ, \mathrm{AR}=10)$, and $0.04314$ at $(\theta=45^\circ, \mathrm{AR}=10)$. | **HIGH** | `p5_production_raw.json` (`study_S5`), `tab05_gap_summary.tex` | Overstates maximum stop-band width by ~1.85×; complete gap non-existence remains intact. | In P9, update prose to quote the verified maximum $\Delta_{GX} = 0.0896$ at $(\theta=30^\circ, \mathrm{AR}=10)$. |
| **FIND-03** | `sec06_results.tex`, Sec 6.4, line 38 | Text states transverse acoustic frequency $\bar{\omega}_T(X)$ drops from $1.154$ to $0.812$, whereas raw data and Fig 8(a) show drop from $2.915$ to $2.672$. | **HIGH** | `p5_production_raw.json` (`study_S3`), `fig08_theta_sweep.py` | Numerical mismatch between text and plotted curves in Figure 8. | In P9, correct prose values to $2.915 \to 2.672$ (transverse) and $5.050 \to 4.628$ (longitudinal). |
| **FIND-04** | `appA_asymptotics.tex`, Eqs (57)–(62); `sec07_steering.tex`, Eq (27) | Appendix A derivation omits constitutive prefactor $1/\sqrt{10}$, states $\bar{v}_{T,\infty} = \bar{l}/\bar{\ell}_{\mathrm{i}}$, and uses synthetic parameter values ($l_2=0.10, \ell_i=0.3162$) instead of Table 2 values ($l_{\mathrm{iso}}=0.20, \ell_{\mathrm{i}}=0.20$) to reach $0.3162$. | **HIGH** | `DERIVATION_M16.md`, `test_p4b_5g_5h.py`, `tab02_parameters.tex` | Presentation inconsistency; numerical horizon $0.3162$ is correct, but analytical formula lacks $1/\sqrt{10}$. | In P9, incorporate factor $1/10$ in gradient stiffness, state $\bar{v}_{T,\infty} = \bar{l}_{\mathrm{eff}} / (\sqrt{10}\,\bar{\ell}_{\mathrm{i}})$, and evaluate using Table 2 parameters. |
| **FIND-05** | `sec02_continuum.tex`, Eq (12); `sec04_fem.tex`, Eq (18) | Displayed equations for $\tau_{ijk}$ and $\bm{K}^g$ omit the scalar prefactor $1/10$ derived from the second moment of the 3D averaging ellipsoid. | **MEDIUM** | `DERIVATION_M01_M07.md` §M4, Blueprint Eq. (26) | Minor mathematical presentation omission; finite element code and tests already include $1/10$. | In P9, add prefactor $1/10$ to the displayed equations for $\tau_{ijk}$ and $\bm{K}^g$. |
| **FIND-06** | `sec07_steering.tex`, Sec 7.4, line 34 | Informal use of the verb *"validates"* (*"This validates the constitutive role..."*) in context of internal asymptotic agreement. | **LOW** | Section 7.4, line 34 | Minor lexical ambiguity; does not claim literature benchmark validation. | In P9, replace *"validates"* with *"confirms"* or *"demonstrates"*. |
| **FIND-07** | `appB_energy_flux.tex`, Eq (72) | Double-stress power term in energy flux is written $\tau_{ijk}\dot u_{i,k}$ rather than $\tau_{ikj}\dot u_{i,k}$ (divergence index in third position). | **LOW** | `DERIVATION_M17.md` Eq. (B.3) | Minor index formatting; identity $\bm{v}_g = \langle\bm{S}\rangle/(\langle W\rangle + \langle T\rangle)$ is verified numerically. | In P9, align index placement with M17 Eq. (B.3). |
| **FIND-08** | `sec05_verification.tex`, Sec 5.7, Eq (24) | Prose defines $\varepsilon_\Delta$ in terms of directional stop-band difference $\Delta_{GX}^{(32)} - \Delta_{GX}^{(16)}$, whereas Table 6 defines it on the acoustic mode frequency $\bar{\omega}_T$. | **LOW** | `tab06_convergence_floor.tex` | Slight notation variation; value $4.63 \times 10^{-11}$ is exact and traceable. | In P9, update symbol in Eq. (24) to $\bar{\omega}_T$. |

---

## 20. Gate Preservation Check

All locked gates, benchmarks, and technical variations were audited for strict preservation:

| Item | Required Status | Manuscript Status | Preservation Verdict |
| :--- | :--- | :--- | :--- |
| **Gate G3** | NOT MET | Explicitly preserved as NOT MET in Sec 5.1, 5.2, 5.3, 8.3 | **PRESERVED** |
| **Criterion PCR1** | NOT PASS | Explicitly preserved as NOT PASS in Sec 5.1, 5.2, 5.3, 8.3 | **PRESERVED** |
| **Benchmarks B1–B3** | UNVALIDATED | Stated as UNVALIDATED in Sec 5.1, 8.3; zero fabricated data | **PRESERVED** |
| **Benchmark B6** | PARTIAL | Explicitly preserved as PARTIAL in Sec 8.3 | **PRESERVED** |
| **Study S2 / Case C** | BLOCKED | Preserved as BLOCKED in Sec 6.3, Fig 7 placeholder, Sec 8.3 | **PRESERVED** |
| **TV1** | OPEN | Acknowledged as open in Sec 8.3 | **PRESERVED** |
| **TV6** | OPEN | Acknowledged as open in Sec 8.3 | **PRESERVED** |
| **TV12** | OPEN | Acknowledged as open in Sec 8.3 | **PRESERVED** |
| **TV14** | OPEN | Acknowledged as open in Sec 8.3 | **PRESERVED** |
| **TV18** | OPEN | Acknowledged as open in Sec 8.3 | **PRESERVED** |
| **Figure 4** | BLOCKED FLOAT | Preserved as explicit blocked placeholder in Sec 5.3 | **PRESERVED** |
| **Figure 7** | BLOCKED FLOAT | Preserved as explicit blocked placeholder in Sec 6.3 | **PRESERVED** |
| **Table 3** | BLOCKED FLOAT | Preserved as explicit blocked placeholder in Sec 5.3 | **PRESERVED** |

---

## 21. Overall P8 Decision

Applying the mandatory Decision Rule:
- No CRITICAL findings exist. The mathematical framework, $C^1$ BFS finite element implementation, 51/51 automated regression tests, and physical conclusions (directional gap opening, absence of complete gaps in Case H, wave steering, micro-inertia necessity) are sound and fully verified.
- However, four HIGH findings were identified:
  1. Figure 6 caption and text misstate the plotted curves ($\mathrm{AR}=10$ is plotted, but text states $\mathrm{AR}=5$), quote $T_g/T = 0.0898$ as a gap width, and list discordant parameters.
  2. Text quotes $\Delta_{GX} = 0.1654$ across four locations, whereas the actual global maximum in `study_S5` is $\Delta_{GX} = 0.08960$ at $(\theta=30^\circ, \mathrm{AR}=10)$.
  3. Text quotes $\bar{\omega}_T(X)$ dropping from $1.154$ to $0.812$, whereas actual raw data and Figure 8 show $2.915 \to 2.672$.
  4. Appendix A omits the constitutive $1/\sqrt{10}$ factor in the 1D asymptotic horizon formula and substitutes ad-hoc parameters ($l_2=0.10, \ell_i=0.3162$) instead of the true Table 2 parameters ($l_{\mathrm{iso}}=0.20, \ell_i=0.20$).
- These four HIGH findings represent text-to-data and presentation discrepancies that require remediation before final journal submission, but do not prevent proceeding to targeted revision.

Therefore, the authoritative forensic verdict is:

**Verdict:** `P8_PASS_WITH_REMEDIATION`
