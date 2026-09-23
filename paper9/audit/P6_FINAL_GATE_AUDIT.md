# P6 Final Gate Audit: Independent Readiness Assessment

**Date:** 2026-09-23  
**Auditor:** Final P6 Gate & Readiness Auditor (Arena.ai)  
**Branch:** `phase-1-symbolic`  
**Operational Mode:** STRICT READ-ONLY AUDIT. Zero production or solver files modified. Only this single audit report is authored.

---

## 1. Repository State

* **Branch:** `phase-1-symbolic`
* **Starting / Expected HEAD:** `c457531d3e908178ee873e52c09143044ee5fc20`
* **Current Local HEAD:** `c457531d3e908178ee873e52c09143044ee5fc20`
* **Remote `origin/phase-1-symbolic` SHA:** `c457531d3e908178ee873e52c09143044ee5fc20`
* **Local == Remote Synchronization:** **SYNCHRONIZED** (`git diff HEAD origin/phase-1-symbolic` is empty).
* **Working Tree State:** Clean prior to report writing (`git status --short` was empty).
* **`origin/main` SHA:** `1de47a4d111260ffb9b48d7c99e9db45102367c7` (**UNTOUCHED**).

---

## 2. Seven Remediation Checks

All seven forensic discrepancies identified in `P6_FORENSIC_AUDIT.md` and remediated in `P6_FORENSIC_REMEDIATION.md` were independently inspected directly in the generator source code, verified output PDFs, and generated LaTeX fragments.

### Finding 1: Mode Polarization Labeling in Figs 8 & 9
* **Verdict:** **PASS / FIXED**
* **Evidence:**
  - BFS modal eigenvector inspection at $X = (\pi/L, 0)$ proves:
    * Branch 0 ($\omega \approx 2.915$): $u_y > 1.0, u_x = 0 \implies$ Transverse acoustic.
    * Branch 1 ($\omega \approx 2.976$): $u_x = 0, u_y = 0, u_{y,x} \ne 0 \implies$ Transverse microstructural gradient.
    * Branch 2 ($\omega \approx 5.050$): $u_x > 1.0, u_y = 0 \implies$ Longitudinal acoustic ($c_L/c_T = \sqrt{(\lambda+2\mu)/\mu} = \sqrt{3} \approx 1.732$).
    * Branch 3 ($\omega \approx 5.155$): $u_x = 0, u_y = 0, u_{x,x} \ne 0 \implies$ Longitudinal microstructural gradient.
  - In `fig08_theta_sweep.py` (lines 32–33) and `fig09_ar_sweep.py` (lines 31–32), `om_X_L` now extracts existing data `omega_X[2]` (longitudinal acoustic) rather than `omega_X[1]`.
  - Reconstructed PDF text streams from `fig08_theta_sweep.pdf` and `fig09_ar_sweep.pdf` verify labels:
    `Transverse acoustic \omega_T(X)` and `Longitudinal acoustic \omega_L(X)`.
  - Panel (a) and panel (b) branch selections are completely aligned: both panels plot branch 1 (transverse acoustic) and branch 3 (longitudinal acoustic) at $X$ and $M$ respectively.
* **Files Inspected:** `paper9/figures/gen/fig08_theta_sweep.py`, `paper9/figures/gen/fig09_ar_sweep.py`, `paper9/figures/out/fig08_theta_sweep.pdf`, `paper9/figures/out/fig09_ar_sweep.pdf`.

### Finding 2: Figure 1 Passive Coordinate Rotation Convention
* **Verdict:** **PASS / FIXED**
* **Evidence:**
  - `fig01_ellipsoid_tensor.py` line 73 defines $L_{12} = (l_2^2 - l_1^2)\sin\theta\cos\theta$, matching Blueprint Eq. (8), `DERIVATION_M01_M07.md`, and `paper9/solver/bfs_bloch_solver.py::L_plane`.
  - Numerical checks confirmed:
    * At $\theta = 0^\circ$: $\mathbf{L} = \mathrm{diag}(l_1^2, l_2^2) = \mathrm{diag}(0.20, 0.008)\,\mathrm{m}^2, L_{12} = 0$.
    * At $\theta = 90^\circ$: $\mathbf{L} = \mathrm{diag}(l_2^2, l_1^2) = \mathrm{diag}(0.008, 0.20)\,\mathrm{m}^2, L_{12} = 0$.
    * At $\theta = 45^\circ$: $L_{12} = (l_2^2 - l_1^2)/2 = -0.096\,\mathrm{m}^2 < 0$ for $l_1 > l_2$.
    * Eigenvalues of $\mathbf{L}(\theta)$ are identically $\{l_1^2, l_2^2\} = \{0.20, 0.008\}$ across all $\theta \in [0, \pi]$.
* **Files Inspected:** `paper9/figures/gen/fig01_ellipsoid_tensor.py`, `paper9/figures/out/fig01_ellipsoid_tensor.pdf`, `paper9/solver/bfs_bloch_solver.py`.

### Finding 3: Convergence Order Language in Figure 5 & Table 6
* **Verdict:** **PASS / FIXED**
* **Evidence:**
  - In `fig05_mesh_convergence.pdf`, the trend line is labeled:
    `Empirical fit: p = 4.17 (95% CI: [3.15, 5.20])`.
  - In `tab06_convergence_floor.tex`, line 12 explicitly reads:
    `\textbf{Fitted convergence rate (empirical least-squares):} $p = 4.17$ (95\% CI: $[3.15, 5.20]$; no theoretical order claimed)`.
  - Zero occurrences of `\mathcal{O}(h`, `O(h^`, `Babuška--Osborn conforming`, `Babuška-Osborn`, `fourth-order convergence`, or `theoretical fourth-order` exist in the P6 outputs.
  - Verified numerical values preserved: $p = 4.17$, 95% CI $[3.15, 5.20]$, and $\varepsilon_\Delta = 4.63 \times 10^{-11}$.
* **Files Inspected:** `paper9/figures/gen/fig05_mesh_convergence.py`, `paper9/figures/out/fig05_mesh_convergence.pdf`, `paper9/tables/gen/tab06_convergence_floor.py`, `paper9/tables/out/tab06_convergence_floor.tex`.

### Finding 4: Scope of Figure 12 (Wave-Vector Steering)
* **Verdict:** **PASS / FIXED**
* **Evidence:**
  - `fig12_ifc_wave_steering.py` docstring and panel titles explicitly specify:
    * Panel (a): `(a) Steering Deviation \delta(\phi) at \bar{k} = 0.5`
    * Panel (b): `(b) Group Velocity Magnitude |\mathbf{v}_g|(\phi) at \bar{k} = 0.5`
  - Reconstructed PDF stream confirms titles and axes specify $\bar{k} = 0.5$.
  - Zero claims of closed 2D iso-frequency contours exist in the generated figure.
  - Filename `fig12_ifc_wave_steering.pdf` preserved to maintain build pipeline integrity.
* **Files Inspected:** `paper9/figures/gen/fig12_ifc_wave_steering.py`, `paper9/figures/out/fig12_ifc_wave_steering.pdf`.

### Finding 5: Directional Gap Terminology in Figure 11
* **Verdict:** **PASS / FIXED**
* **Evidence:**
  - In `fig11_polar_map_regimes.py`, the legend explicitly reads:
    `\Delta_{GX} > 0 \text{ (Directional stop band, } \Gamma-X\text{)}` and `\Delta_{GX} \le 0 \text{ (Pass band, } \Gamma-X\text{)}`.
  - Panel (a) title is `(a) Polar Directional Regimes (\Gamma-X)`.
  - Colorbar label is `Directional gap \Delta_{GX}`.
  - Reconstructed PDF stream confirms `Directional stop band, X`. Complete gap terminology is strictly reserved for full 2D zone evaluations (where Case H exhibits $\Delta_{\mathrm{complete}} \le -0.3758$).
* **Files Inspected:** `paper9/figures/gen/fig11_polar_map_regimes.py`, `paper9/figures/out/fig11_polar_map_regimes.pdf`.

### Finding 6: LaTeX Syntax in Table 2 (`tab02_parameters.tex`)
* **Verdict:** **PASS / FIXED**
* **Evidence:**
  - Table line 14 formats the scaling rule value as `\texttt{volume\_equivalent}`.
  - In line 14, formulas in text columns are typeset with proper math syntax: `$\det(\mathbf{A}^\mathsf{T} \mathbf{A}) = l_{\mathrm{iso}}^4; $l_1 = l_{\mathrm{iso}}\sqrt{\mathrm{AR}}, l_2 = l_{\mathrm{iso}}/\sqrt{\mathrm{AR}}$`.
  - In lines 15–16, underscore in `CALC\_MASTER\_PLAN` is escaped.
  - Zero unescaped underscores or carets exist outside math mode.
* **Files Inspected:** `paper9/tables/gen/tab02_parameters.py`, `paper9/tables/out/tab02_parameters.tex`.

### Finding 7: Publication Scientific Notation in Table 4 (`tab04_consistency_suite.tex`)
* **Verdict:** **PASS / FIXED**
* **Evidence:**
  - Test 5g error is formatted as `$2.85 \times 10^{-4}$` ($< 10^{-3}$, PASS).
  - Test 5h error is formatted as `$6.91 \times 10^{-10}$` ($< 10^{-6}$, PASS).
  - Matches the publication formatting of tests 5a–5e ($2.01 \times 10^{-16}$, etc.).
  - All 8 tests marked `\textbf{PASS}` with unchanged numerical values.
* **Files Inspected:** `paper9/tables/gen/tab04_consistency_suite.py`, `paper9/tables/out/tab04_consistency_suite.tex`.

---

## 3. Float Inventory & Resolution of 19 vs 20 Floats

### Authoritative Specification vs Actual Float Accounting
Inspection of Blueprint Section 6.0 (`Paper9_Blueprint_v1.3.tex`, lines 605–670) establishes the canonical float register:
* **Canonical Figures:** Exactly 13 figures (Figs 1–13). There is **no Figure 14** in Blueprint v1.3.
* **Canonical Tables:** Exactly 6 tables (Tabs 1–6).
* **Authoritative Total Candidate Floats:** **19 floats** ($13 \text{ figures} + 6 \text{ tables}$).

### Detailed Accounting

| Float Group | Authoritative Items | Generated & Verified | Blocked (Zero Fabrication) |
|---|:---:|:---:|:---:|
| **Figures** | 13 (Figs 1–13) | **11** (Figs 1, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13) | **2** (Fig 4 [anchors], Fig 7 [Case C]) |
| **Tables** | 6 (Tabs 1–6) | **5** (Tabs 1, 2, 4, 5, 6) | **1** (Tab 3 [anchor errors]) |
| **Total** | **19 candidate floats** | **16 floats generated** | **3 floats legitimately blocked** |

### Resolution of the 19 vs 20 Discrepancy
The mention of "20 candidate floats" in early Stage 0 notes arose from an informal speculative counting of a hypothetical "Fig 14" (e.g. an optional second Case C modal panel or auxiliary anchor plot). However, Blueprint v1.3 Section 6.0 defines exactly 13 figures (Figs 1–13) and 6 tables (Tabs 1–6), yielding an authoritative total of **19 floats**.
Because no Figure 14 exists in the Blueprint or Master Plan, the 19 vs 20 discrepancy is purely a historical counting artifact with **zero missing deliverables and zero adverse consequence**.

---

## 4. Provenance Audit

The data lineage of every generated float was traced to authorized master parameter files and verified Phase-4/Phase-5 outputs:

| Float ID | Primary Data Source | Path to Source | Parameter / Data Hash |
|---|---|---|---|
| **Fig 1** | Analytical / Master Parameters | `paper9/params/params_master.yaml` | `5bf229bdaebf` |
| **Fig 2** | Lattice Geometry Specification | `paper9/params/params_master.yaml` | `5bf229bdaebf` |
| **Fig 3** | BFS 32-DOF Geometric Layout | Analytical schematic | n/a |
| **Fig 5** | Layer 5 Mesh Convergence (5i) | `paper9/verification/suite/p4b_5g_to_5i.json` | `383843632e31` |
| **Fig 6** | Study S1 Baseline Dispersion | `paper9/results/raw/p5_production_raw.json` | `0af7445a4c5e` |
| **Fig 8** | Study S3 Orientation Sweep | `paper9/results/raw/p5_production_raw.json` | `0af7445a4c5e` |
| **Fig 9** | Study S4 Aspect Ratio Sweep | `paper9/results/raw/p5_production_raw.json` | `0af7445a4c5e` |
| **Fig 10** | Study S5 Design Map (42 pts) | `paper9/results/raw/p5_production_raw.json` | `0af7445a4c5e` |
| **Fig 11** | Study S6 Polar Map & Sensitivity | `paper9/results/raw/p5_production_raw.json` | `0af7445a4c5e` |
| **Fig 12** | Study S7 Wave Steering ($\bar{k}=0.5$) | `paper9/results/raw/p5_production_raw.json` | `0af7445a4c5e` |
| **Fig 13** | Studies S8 ($W_g/W$) & S9 ($v_p$) | `paper9/results/raw/p5_production_raw.json` | `0af7445a4c5e` |
| **Tab 1** | Blueprint §1.4 Literature Review | Blueprint §1.4 text | n/a |
| **Tab 2** | Master Parameter Registry | `paper9/params/params_master.yaml` | `5bf229bdaebf` |
| **Tab 4** | Verification Suite (5a–5h) | `paper9/verification/suite/p4b_5g_to_5i.json` | `383843632e31` |
| **Tab 5** | Band Gap Summary & Taxonomy | `paper9/results/processed/table5_gap_summary.json` | `f0e1c2001fab` |
| **Tab 6** | Convergence Rate & Floor (5i) | `paper9/verification/suite/p4b_5g_to_5i.json` | `383843632e31` |

**Hardcoding Audit:** Inspected all generator scripts. Zero hardcoded scientific results were found; all plotted values and table cells are ingested directly from immutable JSON/YAML records.

---

## 5. Numerical Spot Checks

Nine independent numerical cross-checks were conducted between the generated floats, raw production datasets (`p5_production_raw.json`, `table5_gap_summary.json`), and analytical benchmarks:

1. **Study S1 (Case H Baseline):**
   - At $\Gamma$: $\omega_1 = 0.0, \omega_2 = 8.43 \times 10^{-8}$ (acoustic rigid modes at 0).
   - Rotational Invariance at $\mathrm{AR}=1$: At $X$, $\omega(\mathrm{AR}=1, \theta=0^\circ) = [2.714025777154, 2.736003341686]$, while $\omega(\mathrm{AR}=1, \theta=45^\circ) = [2.714025777154, 2.736003341686]$ (discrepancy $< 4 \times 10^{-15}$, exact invariance verified).
2. **Study S3 ($\theta$ Sweep at $\mathrm{AR}=5$):**
   - Endpoints at $X$: $\theta = 0^\circ \to [2.9153, 2.9761, 5.0495, 5.1547]$; $\theta = 90^\circ \to [2.6719, 2.6854, 4.6279, 4.6513]$.
   - Diagonal symmetry at $M$ about $\theta = 45^\circ$: $\max|\omega_M(\theta) - \omega_M(90^\circ - \theta)| < 2.7 \times 10^{-15}$ across all pairs.
3. **Study S4 ($\mathrm{AR}$ Sweep at $\theta=45^\circ$):**
   - Ingests 6 aspect ratios: $\mathrm{AR} \in \{1.0, 2.0, 3.0, 5.0, 7.0, 10.0\}$. Monotonic variation confirmed.
4. **Study S5 (3D Design Map):**
   - Exactly $7 \times 6 = 42$ computed design points verified.
5. **Study S6 & Table 5 (Complete vs Directional Gap Taxonomy):**
   - Across all 126 band-pair entries:
     $$\Delta[\mathrm{leg}] \ge \Delta[\mathrm{path}] \ge \Delta[\mathrm{complete}]$$
     holds with **126/126 checks PASS (0 violations)**.
   - Positive directional gaps along any leg: exactly **56 configurations**.
   - Positive complete gaps: **0** (all complete gaps $\le -0.3758 \le 0$).
6. **Study S7 (Wave Steering at $\bar{k}=0.5$):**
   - Maximum steering deviation angles: $\delta_{\max}(\mathrm{AR}=1) = 0.01^\circ \approx 0^\circ$, $\delta_{\max}(\mathrm{AR}=5) = 1.41^\circ$, $\delta_{\max}(\mathrm{AR}=10) = 2.79^\circ$.
7. **Study S8 (Energy Partition Monotonicity):**
   - Monotonic growth of gradient energy partition: $W_g/W = 0.20\%$ at $\bar{k}=0.1$, $W_g/W = 16.49\%$ at $\bar{k}=1.0$.
8. **Study S9 (Micro-Inertia Asymptotics):**
   - Theoretical asymptote: $v_{T,\infty} = 0.3162$.
   - Bounded branch at $\bar{k}=200$: $\bar{v}_p = 0.3163$ (relative error $0.03\%$).
   - Unbounded branch ($\ell=0$) at $\bar{k}=200$: $\bar{v}_p = 39.75$ ($>120\times$ bounded speed).
9. **Mesh Convergence (Row 5i):**
   - Empirical least-squares rate: $p = 4.17$ with 95% CI $[3.15, 5.20]$.
   - Operational numerical resolution floor: $\varepsilon_\Delta = 4.63 \times 10^{-11}$.

---

## 6. Verification Test Suite Execution

All test suites were executed in strict read-only mode:

```bash
pytest paper9/verification/suite/test_p6_generators.py -q
# Output: 4 passed in 0.02s

pytest paper9/verification/suite/test_p5_production.py -q
# Output: 8 passed in 0.10s

pytest paper9/verification/suite/test_p4b_5g_5h.py -q
# Output: 3 passed in 0.20s

pytest paper9/verification/suite/test_p6_remediation.py -q
# Output: 7 passed in 0.20s

pytest paper9/verification/suite/ -q
# Output: 22 passed in 0.27s

pytest paper9/production/p5/test_p5_integrity.py -q
# Output: 28 passed in 1.93s

python3 paper9/production/p5/lint_p5_params.py
# Output: params file: ... (hash 48ea7f9e92801ded...)
#         production/p5/p5_core.py: literals=102 frozen-assembly calls checked=1 violations=0
#         production/p5/p5_run.py: literals=125 frozen-assembly calls checked=0 violations=0
#         lint result: PASS (no violations)
```

**Combined Automated Health:** **50 automated test functions PASS, 0 FAIL, 0 warnings, 0 parameter lint violations.**

---

## 7. Gate & Verification Status Matrix

| Gate / Item | Description | Authoritative Status | Rationale / Grounding |
|---|---|:---:|---|
| **G1** | Formulation & limit ladder | **MET** | Phase 1 M1–M17 symbolic derivations locked. |
| **G2** | Verification suite & floor | **MET** | Phase 4B tests 5a–5i pass; $\varepsilon_\Delta = 4.63 \times 10^{-11}$ locked. |
| **G3** | Published anchor replication | **NOT MET** | B1–B3 published curve comparison unvalidated. Preserved. |
| **G4** | Production execution | **PARTIAL** | Case H complete (42/42 points); Case C unrun. |
| **G5** | Manuscript integration | **NOT STARTED** | P7–P9 pending. |
| **G-F** | Float generation audit | **PARTIAL** | 16/19 permissible floats verified; 3/19 legitimately blocked. |
| **PCR1** | Layer 1 classical limit (Li 2024 Fig 2a) | **NOT PASS** | Blocked by Gate G3. Preserved. |
| **PCR2** | Layer 2a gradient elastic (Li 2024 Fig 2b) | **NOT PASS** | Blocked by Gate G3. Preserved. |
| **PCR3** | Layer 2b dipolar gradient (Li 2023 Fig 4c) | **NOT PASS** | Blocked by Gate G3. Preserved. |
| **PCR4** | Layer 3 closed-form analytical limit | **PASS** | Validated to machine precision in Test 5d. |
| **PCR5** | Layer 5 internal numerical consistency | **PASS** | Tests 5a–5f verified (P4A). |
| **PCR6** | Micro-inertia bounded phase velocity | **PASS** | Test 5g verified (P4B). |
| **PCR7** | Energy-flux / group-velocity identity | **PASS** | Test 5h verified (P4B). |
| **PCR8** | Mesh convergence & resolution floor | **PASS** | Test 5i verified (P4B). |
| **B1** | Anchor A (Li et al. 2023) | **NOT MET** | Published curves unvalidated. |
| **B2** | Anchor B (Li et al. 2024) | **NOT MET** | Published curves unvalidated. |
| **B3** | Anchor C (Mishra et al. 2026) | **NOT MET** | Dynamic stiffness cross-check unvalidated. |
| **B6** | Quantitative validation feasibility | **PARTIAL** | Preserved. |
| **S2** | Case C baseline bands & modes | **BLOCKED** | TV6, TV14, TV18 unresolved. Preserved. |
| **TV1** | Anchor parameter grounding | **OPEN** | Preserved. |
| **TV6** | Case C production parameters | **OPEN** | Preserved. |
| **TV9** | Boundary operator formulation | **RESOLVED** | Frozen in Phase 1 (M8a). |
| **TV12** | Anchor interface conditions | **OPEN** | Preserved. |
| **TV14** | Case C reference phase normalisation | **OPEN** | Preserved. |
| **TV18** | Case C circular inclusion representation | **OPEN** | Preserved. |

---

## 8. P7 Readiness Decision

### Decision: `READY_FOR_P7_LIMITED_SCOPE`

Phase 6 deliverables for all verified, locked, and permissible topics are complete, internally consistent, mathematically verified, and free of editorial overstatements. Phase 7 manuscript drafting may proceed **strictly within the limited scope** defined below.

### Permitted P7 Scope (Authorized to Draft)
1. **Title, Abstract, Introduction:**
   - Continuum theory motivation, higher-order gradient elasticity, micro-inertia momentum equations.
   - Literature positioning (Table 1: 9 rows, 4 "Yes" columns; emphasizing uniqueness in combining 2D, micro-inertia, anisotropic length tensor, and BFS Bloch FE).
2. **Section 2 (Mathematical Formulation):**
   - Nonlocal ellipsoidal averaging neighborhood and characteristic length tensor $\mathbf{L}(\theta)$ (Eqs. 1–9, Fig 1).
   - Form-II strain-gradient constitutive equations and micro-inertia kinetic energy density.
   - Energy positive definiteness and the limit ladder (M7).
3. **Section 3 (Periodic Medium & Boundary Operators):**
   - Square lattice geometry, Brillouin zone, and IBZ path $\Gamma-X-M-\Gamma$ (Fig 2).
   - $C^1$ boundary operators and time-averaged energy flux tensor with double-stress work rate.
4. **Section 4 ($C^1$ BFS Finite Element Bloch Formulation):**
   - 32-DOF BFS rectangular element layout (Fig 3).
   - Bloch periodic boundary conditions with phase factors applied to both value and normal/tangential/cross derivative DOFs.
   - Reduced generalized Hermitian eigenvalue pencil $(\mathbf{\bar K}, \mathbf{\bar M})$.
5. **Section 5 (Layer 5 Internal Numerical Verification & Convergence):**
   - Eight-test internal consistency suite (Table 4: tests 5a–5h).
   - Mesh convergence across $4^2 \to 32^2$ meshes, empirical least-squares rate $p=4.17$ (95% CI: $[3.15, 5.20]$), and numerical resolution floor $\varepsilon_\Delta = 4.63 \times 10^{-11}$ (Fig 5, Table 6).
   - Master parameters registry with provenance tags (Table 2).
6. **Section 6 (Case H Band Structure Results):**
   - Case H microstructure-induced dispersion (Fig 6).
   - Directional frequency migration along $\Gamma-X$ vs orientation $\theta$ (Fig 8) and aspect ratio $\mathrm{AR}$ (Fig 9).
   - $(\theta, \mathrm{AR})$ design map for directional stop band $\Delta_{GX}$ (Fig 10).
   - Polar design map and orientation sensitivity $S_\theta(\mathrm{AR})$ (Fig 11, Table 5).
   - Explicit distinction between directional gaps and complete band gaps; proof that homogeneous Case H exhibits no complete band gap.
7. **Section 7 (Anisotropic Wave Steering & Physical Admissibility):**
   - Wave-vector steering deviation $\delta(\phi)$ and group velocity magnitude $|\mathbf{v}_g|(\phi)$ at $\bar{k} = 0.5$ (Fig 12).
   - Classical vs gradient energy partition $W_g/W, T_g/T$ (Fig 13(a)).
   - Micro-inertia necessity and bounded high-$k$ phase velocity asymptotics ($v_{T,\infty} = 0.3162$, Fig 13(b), Appendix A).

### Prohibited P7 Scope (Strictly Excluded Until Unlocked)
1. **DO NOT Draft Published Anchor Replications (Section 5.2–5.3):**
   - Layer 1 (Li 2024 Fig 2a), Layer 2a (Li 2024 Fig 2b), and Layer 2b (Li 2023 Fig 4c) must **not** be presented as passed validations.
   - Do not claim Gate G3 or PCR1 are met.
   - Figure 4 and Table 3 must remain excluded/blocked placeholders.
2. **DO NOT Draft Case C Results (Section 6.3):**
   - Periodic phononic crystal inclusion calculations (Study S2) remain blocked.
   - Do not invent inclusion contrast, radius, or interface jump condition parameters.
   - Figure 7 must remain excluded/blocked.
3. **DO NOT Claim Complete Band Gaps for Case H:**
   - Homogeneous micro-inertia material does not possess an omnidirectional band gap ($\Delta_{\mathrm{complete}} \le -0.3758$). All positive gaps must be qualified strictly as directional/partial stop bands (primarily along $\Gamma-X$).
4. **DO NOT Claim Asymptotic Theoretical Fourth-Order Convergence:**
   - The observed convergence rate $p=4.17$ must be reported strictly as an empirical least-squares fit across the tested meshes ($h = 1/4$ to $1/32$) without claiming an asymptotic $\mathcal{O}(h^4)$ theorem.

---

## 9. Remaining Blockers

The following items are legitimately blocked and require upstream resolution before full manuscript completion:
1. **Gate G3 / PCR1 / B1–B3:** Quantitative validation against published 1D transfer-matrix curves from Li et al. (2023, 2024) and Mishra et al. (2026).
2. **TV1 / TV12:** Anchor material parameters and interface boundary condition grounding.
3. **Study S2 / Case C / Fig 7:** Phononic crystal circular inclusion formulation, interface continuity across material contrast, and baseline band calculations.
4. **TV6 / TV14 / TV18:** Inclusion radius/contrast grounding, reference phase normalisation, and FE representation of inclusions.

---

## 10. Final Safety Statement

This audit was conducted in **strict read-only mode**. No production scripts, solver code, master parameter files, raw calculation records, generated figures, or generated tables were modified. Only this single independent audit document (`paper9/audit/P6_FINAL_GATE_AUDIT.md`) was written to record the authoritative readiness determination.
