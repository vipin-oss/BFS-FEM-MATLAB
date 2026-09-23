# Phase 6 Forensic Remediation Report

**Date:** 2026-09-23  
**Auditor / Agent:** Phase-6 Revision Agent (Arena.ai)  
**Branch:** `phase-1-symbolic`  
**Starting HEAD:** `63c04c72af74782c1bd1e7b2ab23a6a96d5197f2` (origin fast-forward merge base `23ae4507bcb4b03f5fd1e91ec0b3626bb2a94867`)  
**Scope:** Remediation of the seven discrepancies identified in `paper9/audit/P6_FORENSIC_AUDIT.md`.

---

## 1. Executive Summary & Status Preservations

The Phase-6 visual and tabular deliverables have undergone a forensic remediation cycle. All seven findings from `paper9/audit/P6_FORENSIC_AUDIT.md` have been corrected, verified against verified physical datasets, and confirmed by automated regression tests.

### Preserved Downstream & Validation Statuses (Strict Safety Locks)
- **Gate G3 (Anchor Validation):** **NOT MET** (preserved; zero synthetic curves or error numbers fabricated).
- **PCR1 (Published Comparative Replication 1):** **NOT PASS** (preserved).
- **B6 (Quantitative Validation Feasibility):** **PARTIAL** (preserved).
- **Study S2 / Case C (Phononic Crystal Inclusions):** **BLOCKED** (preserved; no artificial contrast or radius assumed).
- **Open TV Register Items:** **TV1, TV6, TV9, TV12, TV14, TV18 remain OPEN**.
- **Gate G-F (Float Audit):** **PARTIAL** (16/19 permissible floats fully generated and verified; 3/19 legitimately blocked).
- **Manuscript Phases P7 / P8 / P9:** **NOT STARTED** (preserved).

---

## 2. Forensic Findings & Detailed Remediations

### Finding 1 (High Priority): Mode Polarization Labeling in Figures 8 and 9
- **Audit Issue:** `fig08_theta_sweep.py` and `fig09_ar_sweep.py` extracted `omega_X[0]` and `omega_X[1]`, labeling branch 1 as "Longitudinal $\omega_L(X)$". BFS eigenvector inspection at $X = (\pi/L, 0)$ proves that branch 0 ($\omega \approx 2.915$) is the transverse acoustic mode ($u_y$ displacement) and branch 1 ($\omega \approx 2.976$) is the transverse microstructural/gradient mode ($u_{y,x}$ gradient DOF). Branch 2 ($\omega \approx 5.050$) is the true longitudinal acoustic mode ($u_x$ displacement, matching $c_L/c_T = \sqrt{(\lambda+2\mu)/\mu} = \sqrt{3} \approx 1.732$).
- **Correction Made:**
  - In `fig08_theta_sweep.py`: updated `om_X_L = [item['omega_X'][2] for item in data]` (branch 3 in 1-based indexing) and labeled `Transverse acoustic \omega_T(X)` and `Longitudinal acoustic \omega_L(X)`.
  - In `fig09_ar_sweep.py`: updated `om_X_L = [item['omega_X'][2] for item in data]` and updated labels identically.
  - Aligned panel (a) branch selection with panel (b), which already plots branch 1 (`omega_M[0]`) and branch 3 (`omega_M[2]`).
- **Files Modified:** `paper9/figures/gen/fig08_theta_sweep.py`, `paper9/figures/gen/fig09_ar_sweep.py`.
- **Files Regenerated:** `paper9/figures/out/fig08_theta_sweep.pdf`, `paper9/figures/out/fig09_ar_sweep.pdf`.
- **Regression Test:** `test_finding1_modal_polarization_at_X` in `paper9/verification/suite/test_p6_remediation.py` verifies $u_x/u_y$ eigenvector components and bans branch 1 from being called longitudinal.

---

### Finding 2 (Moderate Priority): Sign of $L_{12}$ in Figure 1 ($\mathbf{L}(\theta)$)
- **Audit Issue:** `fig01_ellipsoid_tensor.py` line 66 defined $L_{12} = (l_1^2 - l_2^2)\sin\theta\cos\theta$ (active ellipse frame), whereas Blueprint Eq. (8), `DERIVATION_M01_M07.md`, and `bfs_bloch_solver.py` use the locked passive coordinate rotation $\mathbf{L} = \mathbf{R}^\mathsf{T} \mathrm{diag}(l_1^2, l_2^2) \mathbf{R}$, giving $L_{12} = (l_2^2 - l_1^2)\sin\theta\cos\theta$. For $l_1 > l_2$, this is negative at $\theta = 45^\circ$.
- **Correction Made:** Updated line 66 to $L_{12} = (l_2^2 - l_1^2)\sin\theta\cos\theta$, matching `bfs_bloch_solver.L_plane`.
- **Files Modified:** `paper9/figures/gen/fig01_ellipsoid_tensor.py`.
- **Files Regenerated:** `paper9/figures/out/fig01_ellipsoid_tensor.pdf`.
- **Regression Test:** `test_finding2_passive_rotation_tensor_L` verifies $\theta=0^\circ$, $\theta=90^\circ$ diagonal swapping, negative $L_{12}$ at $\theta=45^\circ$, and eigenvalue invariance across $[0, 90^\circ]$.

---

### Finding 3 (Moderate Priority): Convergence Order Language in Figure 5 & Table 6
- **Audit Issue:** `fig05_mesh_convergence.py` labeled the fit as `Fit: \mathcal{O}(h^{4.17})` and Table 6 included `Babuška--Osborn conforming`, implying a theoretical asymptotic theorem in violation of CALC_MASTER_PLAN line 240 ("observed rate with 95 % CI reported; no theoretical order claimed").
- **Correction Made:**
  - In `fig05_mesh_convergence.py`: revised label to `Empirical fit: p = 4.17 (95% CI: [3.15, 5.20])`.
  - In `tab06_convergence_floor.py`: updated note to `\textbf{Fitted convergence rate (empirical least-squares):} $p = 4.17$ (95\% CI: $[3.15, 5.20]$; no theoretical order claimed)`.
  - Preserved numerical values: $p = 4.17$, 95% CI $[3.15, 5.20]$, and $\varepsilon_\Delta = 4.63 \times 10^{-11}$.
- **Files Modified:** `paper9/figures/gen/fig05_mesh_convergence.py`, `paper9/tables/gen/tab06_convergence_floor.py`.
- **Files Regenerated:** `paper9/figures/out/fig05_mesh_convergence.pdf`, `paper9/tables/out/tab06_convergence_floor.tex`.
- **Regression Test:** `test_finding3_convergence_order_language` enforces absence of big-$\mathcal{O}$ and Babuška–Osborn claims.

---

### Finding 4 (Moderate Priority): Scope Description of Figure 12
- **Audit Issue:** Figure 12 does not plot 2D closed iso-frequency contours in wavenumber space (which were not serialized in `p5_production_raw.json`), but rather the wave-vector steering deviation $\delta(\phi)$ and group velocity magnitude $|\mathbf{v}_g|(\phi)$ along a circular sampling path at fixed $|\mathbf{k}| = \bar k = 0.5$.
- **Correction Made:**
  - Updated module docstring and titles in `fig12_ifc_wave_steering.py` to:
    - Panel (a): `(a) Steering Deviation \delta(\phi) at \bar{k} = 0.5`
    - Panel (b): `(b) Group Velocity Magnitude |\mathbf{v}_g|(\phi) at \bar{k} = 0.5`
  - Fixed x-axis label on panel (b) to `Wave vector direction \phi [deg]`.
  - Kept filename `fig12_ifc_wave_steering.pdf` unchanged to ensure build pipeline stability.
  - Manuscript note: the manuscript caption for Figure 12 must describe circular wave-vector steering profiles at $\bar k = 0.5$ rather than closed 2D wavenumber loops.
- **Files Modified:** `paper9/figures/gen/fig12_ifc_wave_steering.py`.
- **Files Regenerated:** `paper9/figures/out/fig12_ifc_wave_steering.pdf`.
- **Regression Test:** `test_finding4_fig12_scope_description` verifies accurate description of $\bar k = 0.5$ steering deviation.

---

### Finding 5 (Low Priority): Directional Gap Qualification in Figure 11
- **Audit Issue:** Figure 11 panel (a) legend labeled $\Delta_{GX} > 0$ merely as `(Stop band)`, risking conflation with an omnidirectional/complete band gap (strictly disproven for Case H in Table 5).
- **Correction Made:**
  - Panel (a) legend updated to `\Delta_{GX} > 0 (Directional stop band, \Gamma-X)` and `\Delta_{GX} \le 0 (Pass band, \Gamma-X)`.
  - Panel (a) title updated to `(a) Polar Directional Regimes (\Gamma-X)`.
  - Colorbar label updated to `Directional gap \Delta_{GX}`.
- **Files Modified:** `paper9/figures/gen/fig11_polar_map_regimes.py`.
- **Files Regenerated:** `paper9/figures/out/fig11_polar_map_regimes.pdf`.
- **Regression Test:** `test_finding5_gap_classification_terminology` verifies explicit directional gap qualification.

---

### Finding 6 (Low Priority): LaTeX Syntax in Table 2 (`tab02_parameters.tex`)
- **Audit Issue:** `$volume_equivalent$` contained an unescaped underscore in math mode, and text columns contained unescaped carets and underscores (`det(A^T A) = l_iso^4; l1=l_iso*sqrt(AR)`).
- **Correction Made:**
  - Formatted `volume_equivalent` as `\texttt{volume\_equivalent}`.
  - Sanitized math fragments in text cells to `\det(\mathbf{A}^\mathsf{T} \mathbf{A}) = l_{\mathrm{iso}}^4; $l_1 = l_{\mathrm{iso}}\sqrt{\mathrm{AR}}, l_2 = l_{\mathrm{iso}}/\sqrt{\mathrm{AR}}$`.
  - Escaped underscores in `CALC\_MASTER\_PLAN`.
- **Files Modified:** `paper9/tables/gen/tab02_parameters.py`.
- **Files Regenerated:** `paper9/tables/out/tab02_parameters.tex`.
- **Regression Test:** `test_finding6_table2_latex_safety` checks for clean LaTeX escaping.

---

### Finding 7 (Low Priority): Scientific Notation in Table 4 (`tab04_consistency_suite.tex`)
- **Audit Issue:** Tests 5g and 5h were formatted in raw Python exponential notation (`2.85e-04`, `6.91e-10`).
- **Correction Made:** Implemented `fmt_sci()` producing publication-grade LaTeX: `$2.85 \times 10^{-4}$` and `$6.91 \times 10^{-10}$`.
- **Files Modified:** `paper9/tables/gen/tab04_consistency_suite.py`.
- **Files Regenerated:** `paper9/tables/out/tab04_consistency_suite.tex`.
- **Regression Test:** `test_finding7_table4_scientific_notation` checks for standard scientific notation.

---

## 3. Data Integrity & Blocked Items Audit

- **Raw Scientific Data:** Verified that `paper9/results/raw/p5_production_raw.json` and all `.npz` files are completely untouched and unmodified.
- **Scientific Production JSON:** Zero changes to computed values. All values displayed in regenerated figures and tables originate from the locked Phase-5 production dataset.
- **Solver Equations:** Zero modifications to `paper9/solver/bfs_bloch_solver.py`.
- **Blocked Floats Non-Fabrication:**
  - Figure 4 (Anchor overlays): **BLOCKED** (no file created).
  - Table 3 (Anchor error table): **BLOCKED** (no file created).
  - Figure 7 (Case C bands & modes): **BLOCKED** (no file created).
- **Total Floats Present:** 16/19 permissible floats generated and verified.

---

## 4. Verification & Test Suite Execution

All test suites executed with 100% passing results:
```
pytest paper9/verification/suite/test_p6_generators.py -q   -> 4 passed in 0.01s
pytest paper9/verification/suite/test_p5_production.py -q   -> 8 passed in 0.10s
pytest paper9/verification/suite/test_p4b_5g_5h.py -q       -> 3 passed in 0.20s
pytest paper9/verification/suite/test_p6_remediation.py -q  -> 7 passed in 0.19s
pytest paper9/verification/suite/ -q                        -> 22 passed in 0.26s
pytest paper9/production/p5/test_p5_integrity.py -q         -> 28 passed in 2.20s
python3 paper9/production/p5/lint_p5_params.py              -> PASS (0 violations)
```

---

## 5. Logical Git Commit Structure

1. **Commit 1 (`1204fa6`):**
   `fix: correct P6 mode and tensor figure conventions`
   - Fig 1 ($L_{12}$ passive sign), Figs 8 & 9 (branch 2 longitudinal acoustic extraction)
   - Added regression test `test_p6_remediation.py`.
2. **Commit 2 (`ee061a7`):**
   `fix: clarify P6 convergence and gap terminology`
   - Fig 5 & Table 6 (empirical slope without theoretical claim)
   - Fig 11 (directional stop band qualification).
3. **Commit 3 (`d9aeaf8`):**
   `fix: align P6 figure scope and table formatting`
   - Fig 12 ($\bar k = 0.5$ wave-vector steering scope description)
   - Table 2 (escaped LaTeX syntax and `\texttt{volume\_equivalent}`)
   - Table 4 (publication-grade scientific notation for 5g and 5h).
4. **Commit 4 (Pending):**
   `audit: record P6 forensic remediation and audit reports`
   - Records `P6_FORENSIC_AUDIT.md` and `P6_FORENSIC_REMEDIATION.md`.
