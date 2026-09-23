# P10 Governance & Scope Decision Audit

**Date:** 2026-09-23  
**Repository:** `https://github.com/vipin-oss/BFS-FEM-MATLAB`  
**Audited Branch:** `phase-1-symbolic`  
**Audited HEAD Commit:** `d438cd87b5f325dc062a58532132d9915bf32127`  
**Operational Scope:** READ-ONLY governance and scope decision audit evaluating Path A (Case-H standalone manuscript via formal governance amendment) versus Path B (continuation of full original scope via additional solver implementation, literature data acquisition, and Case-C formulation).  
**Governance Classification:** `FULL_SCOPE_IS_CURRENTLY_GOVERNANCE_LOCKED`

---

## 1. Repository Baseline

The baseline repository state was verified via read-only git commands prior to audit execution:

```bash
git status
# On branch phase-1-symbolic
# Your branch is up to date with 'origin/phase-1-symbolic'.
# Untracked files: paper9/audit/P9_FINAL_RELEASE_AUDIT.md
# nothing added to commit but untracked files present

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
- **Main Branch:** `origin/main` remains untouched at `1de47a4d111260ffb9b48d7c99e9db45102367c7` (0 commits ahead, 0 commits behind on `main`).
- **Working Tree:** No solver code, parameters, tests, or manuscript text files have been modified. This audit operates under strict non-destructive read-only governance.

---

## 2. Authoritative Governance Documents

The audit inspected and cross-referenced the following governing records:

1. **`paper9/plan/blueprint/Paper9_Blueprint_v1.3.tex`**: The primary constitutional document defining the manuscript structure (Sections 1–9, Appendices A–B), 19 candidate floats (13 figures, 6 tables), Gate criteria (G1–G4), Publication-Critical Requirements (PCR1–PCR8), and target journal specifications.
2. **`paper9/plan/CALC_MASTER_PLAN.md`**: The operational calculation master plan establishing the phased execution workflow, gate progression rules, benchmark cards (B1–B7), study definitions (S1–S9), and technical variation registers.
3. **`paper9/audit/P6_FINAL_GATE_AUDIT.md`**: Authoritative gate review certifying `READY_FOR_P7_LIMITED_SCOPE` and locking G3 = NOT MET, PCR1 = NOT PASS, S2 = BLOCKED.
4. **`paper9/audit/P7_LIMITED_SCOPE_DRAFT_AUDIT.md`**: Authoritative audit recording the construction of the limited-scope manuscript `ms.tex` with 16 verified floats and 3 explicit placeholders.
5. **`paper9/audit/P8_FORENSIC_MANUSCRIPT_AUDIT.md`**: Forensic audit identifying 8 mathematical, numerical, and figure presentation findings.
6. **`paper9/audit/P8_REMEDIATION_REPORT.md`**: Report certifying 100% completion and verification of P8 remediations across git commits `de19ef2`, `4cde6df`, `4429920`, and `d438cd8`.
7. **`paper9/audit/P9_FINAL_RELEASE_AUDIT.md`**: Release-gate audit establishing the verdict `P9_NOT_READY_FOR_FINAL_RELEASE` under the locked Blueprint v1.3 criteria.
8. **`paper9/audit/traceability_matrix.csv`**: Complete traceability register tracking 71 blueprint equations, matrices, and parameters across derivations, code, and manuscript sections.
9. **`paper9/validation/P3_STATUS.md` & `paper9/audit/P3_SOURCE_AUDIT.md`**: Forensic audit records establishing that published anchors B1, B2, and B3 lack tabulated numerical data in the literature, rendering quantitative error evaluation blocked.
10. **`paper9/audit/STAGE1_BLOCKERS_AUDIT.md`**: Root-cause analysis of B1–B3, B6, and Study S2 (Case C) blockers.
11. **`paper9/audit/P3_TV_RESOLUTION.md`**: Detailed status tracking of Technical Variations TV1 through TV18.
12. **`paper9/latex/ms.tex`**: Current compiled manuscript source and its modular section files in `paper9/latex/sections/`.
13. **`paper9/tables/out/tab01_literature_positioning.tex`**: Literature positioning matrix establishing claimed research gaps and novelty.
14. **`paper9/params/p5_pilot_params.yaml` & `tab02_parameters.tex`**: Master parameter registries with provenance tags `[C]`, `[A]`, `[S]`.

---

## 3. Current Locked Scope

Under Blueprint v1.3 and Calculation Master Plan v1.1, the project's locked scope consists of:
- **Constitutive Theory:** Mindlin Form-II strain-gradient elasticity with anisotropic characteristic length tensor $\mathbf{L}(\theta) = \bm{R}(\theta)^\mathsf{T} \mathbf{L}_0 \bm{R}(\theta)$, volume-preserving constraint $\det(\mathbf{L}_0) = l_1^2 l_2^2 = l_{\mathrm{iso}}^4$, and micro-inertia $\rho \ell_{\mathrm{i}}^2$.
- **Discretization:** Conforming $C^1$ Bogner–Fox–Schmit (BFS) bicubic Hermite finite elements on a square unit cell ($L=1\,\mathrm{m}$), 32 DOFs per cell, with Bloch–Floquet periodic boundary conditions applied identically to displacement and spatial derivative DOFs.
- **Physical Studies:**
  - **Case H (Homogeneous Medium):** Microstructure-induced dispersion (S1), orientation angle sweep $\theta \in [0, 90^\circ]$ (S3), aspect ratio sweep $\mathrm{AR} \in [1, 10]$ (S4), 42-point design map (S5), polar regime map (S6), acoustic wave steering (S7), gradient energy partition (S8), and micro-inertia high-$k$ phase velocity asymptotics (S9). Status: **100% COMPLETE AND VERIFIED**.
  - **Case C (Periodic Phononic Crystal):** Unit cell containing a matrix and a centered circular inclusion to generate complete omnidirectional Bragg band gaps (S2). Status: **BLOCKED BY INSUFFICIENT SOURCE-SPECIFIED DATA**.
- **Validation Framework:**
  - **Published Benchmarks (B1, B2, B3):** Mandatory 1D bilayer transfer-matrix benchmarks from Li et al. (2024) [B1, B2] and Li et al. (2023) [B3] evaluated to $\le 0.5\%$ (classical) and $\le 2.0\%$ (gradient). Status: **UNVALIDATED / BLOCKED**.
  - **Analytical Benchmark (B5 / Layer 3):** Closed-form homogeneous dispersion against Papargyri-Beskou & Beskos (2009). Status: **PASS** ($1.25 \times 10^{-8}$ error).
  - **Independent Formulation (B6 / Layer 3b):** 1D transfer-matrix formulation against Li, Wei & Zhou (2016). Status: **PARTIAL** ($< 1.5 \times 10^{-14}$ error on limiting cases; published curve blocked by lack of tabulated data).
  - **Internal Verification (Layer 5):** Eight-test consistency suite (5a–5h) and mesh convergence (5i) with empirical rate $p=4.17$ and resolution floor $\varepsilon_\Delta = 4.63 \times 10^{-11}$. Status: **PASS**.

---

## 4. Mandatory-vs-Optional Requirements

A comprehensive audit of the governing documents was conducted to separate mandatory requirements from optional design choices:

| Requirement | Governing Source | Mandatory? | Exact Governing Language & Evidence | Consequence in Current Repo |
| :--- | :--- | :--- | :--- | :--- |
| **B1** (Layer 1 Classical Bilayer) | Blueprint v1.3 §9.4 (line 884); Plan Table B (line 151) | **MANDATORY** | "PCR1. All mandatory published benchmarks (Layers 1, 2a, 2b) PASS with maximum relative error $\le 2\%$... Hard gate (G3)? YES" | Unvalidated; blocks G3 and G4 under current governance. |
| **B2** (Layer 2a Gradient Bilayer) | Blueprint v1.3 §9.4 (line 884); Plan Table B (line 152) | **MANDATORY** | "PCR1. All mandatory published benchmarks (Layers 1, 2a, 2b) PASS... Hard gate (G3)? YES" | Unvalidated; blocks G3 and G4 under current governance. |
| **B3** (Layer 2b Bilayer, Decisive) | Blueprint v1.3 §9.4 (line 884); Plan Table B (line 153) | **MANDATORY** | "PCR1. All mandatory published benchmarks (Layers 1, 2a, 2b) PASS... Hard gate (G3)? YES (decisive)" | Unvalidated; TV1 open; blocks G3 and G4 under current governance. |
| **B6** (Layer 3b 1D SH Transfer Matrix) | Blueprint v1.3 §5.4 (line 681); Plan Table B (line 156) | **OPTIONAL** | "Hard gate (G3)? no; Layer 3b, 1D dipolar-gradient PC closed form (analytic)" | Status is PARTIAL; does not block G3 or G4 by itself. |
| **S2** (Case C Baseline Band Structure) | Blueprint v1.3 §6.3 (line 485), Table 4.2 (line 620); Plan Table 3.5 (line 256) | **MANDATORY** | "6.3 Case C baseline band structure along $\Gamma$-X-M-$\Gamma$... Fig 7 Case C baseline band structure; Table 5 gap summary" | Blocked by TV6, TV14, TV18; leaves Fig 7 and Table 3 as blocked placeholders. |
| **G3** (Published Validation Gate) | Blueprint v1.3 §9.2 (line 822); Plan §B (line 103) | **MANDATORY** | "G3: blueprint-locked HARD gate: published validation Layers 1, 2a, 2b at $\le2\%$... Fail $\implies$ stop" | Status is NOT MET; prevents G4 sign-off. |
| **PCR1** (Benchmark Error $\le 2\%$) | Blueprint v1.3 §9.4 (line 881, 884, 907) | **MANDATORY** | "The manuscript cannot be submitted until every line below is true... A failed PCR blocks submission exactly as G3 does." | Status is NOT PASS; legally blocks submission under current Blueprint. |
| **G4** (Final Submission Gate) | Blueprint v1.3 §9.2 (line 829), §9.4 (line 907); Plan §B (line 107) | **MANDATORY** | "The PI signs G4 only after PCR1--PCR8 are checked against the computation log. A failed PCR blocks submission exactly as G3 does." | Status is NOT MET; submission blocked. |
| **Case H** (Homogeneous Metamaterial) | Blueprint v1.3 §6.1–6.2 (lines 483–484); Plan Table 3.5 (line 255) | **MANDATORY** | "6.1 Baseline configuration... Case H = homogeneous cell; 6.2 Case H results: microstructure-induced dispersion" | 100% complete, verified, and traceable. |
| **Case C** (Composite Phononic Crystal) | Blueprint v1.3 §6.1, §6.3 (lines 483, 485); Plan §A (line 47) | **MANDATORY** | "gaps exist only with periodic contrast (Case C)... Case C = matrix with a centred circular inclusion" | Blocked by TV6, TV14, TV18; cannot be executed with current data/code. |
| **TV1** (Anchor A Fig 4(c) Parameters) | Plan Table TV (line 360); `P3_TV_RESOLUTION.md` | **MANDATORY** for B3 | "Anchor A Fig 4(c) non-dimensional parameters ($c, d$ set) from Li et al. (2023)" | Status is OPEN; prevents execution of B3. |
| **TV6** (Case C Parameters) | Plan Table TV (line 360); `tab02_parameters.tex` | **MANDATORY** for Case C | "Case H/C production parameters (E,ν,ρ,l1,l2,ℓ_i,L, inclusion radius/contrast)" | Locked [S] for Case H; OPEN for Case C. Blocks S2. |
| **TV12** (Fig 4 Overlay Axis Ranges) | Plan Table TV (line 360); `P3_TV_RESOLUTION.md` | **MANDATORY** for Fig 4 | "Overlay axis ranges and sampling for Figs 4(a)–(c)" | Status is OPEN; prevents generation of Fig 4 overlays. |
| **TV14** (Case C Reference Phase) | Plan Table TV (line 368); `traceability_matrix.csv` (M11) | **MANDATORY** for Case C | "Case C: which phase's $\mu, \rho$ and which $L$ define $\omega_0$ and $\bar{v}$" | Status is OPEN; prevents non-dimensionalization of Case C. |
| **TV18** (BFS Circular Inclusion) | `traceability_matrix.csv` (M14); `STAGE1_BLOCKERS_AUDIT.md` | **MANDATORY** for Case C | "BFS circular inclusion representation: cut elements suffer $\mathcal{O}(h)$ area error" | Status is OPEN; prevents valid FEM discretization of circular inclusion. |

---

## 5. Path A — Case-H Standalone

### Scientific Content Retained
Audit of repository evidence demonstrates that the Case-H scientific subsystem is self-contained, fully implemented, and mathematically rigorous:
- **Anisotropic Microstructure Formulation:** Second-moment characteristic-length tensor $\mathbf{L}_0 = \mathrm{diag}(l_1^2, l_2^2)$ under area preservation $\det(\mathbf{L}_0) = l_{\mathrm{iso}}^4$; passive frame rotation $\mathbf{L}(\theta) = \bm{R}(\theta)^\mathsf{T}\mathbf{L}_0\bm{R}(\theta)$ generating negative off-diagonal coupling $L_{12}(45^\circ) = -0.096\,\mathrm{m}^2$; proven positive definiteness $\mathrm{spec}(\mathbf{L}(\theta)) \equiv \{l_1^2, l_2^2\} > 0$ for all $\theta$.
- **Mindlin Form-II Continuum:** Cauchy stress $\sigma_{ij} = C_{ijkl}\varepsilon_{kl}$; double stress $\tau_{ijk} = \frac{1}{10}L_{kl}C_{ijmn}\eta_{mnl}$ incorporating the rigorous second-moment prefactor $1/10$; positive-definite strain energy density $W > 0$.
- **Micro-Inertia Dynamics:** Kinetic energy density $T = \frac{1}{2}\rho \dot u_i \dot u_i + \frac{1}{2}\rho \ell_{\mathrm{i}}^2 \dot u_{i,j}\dot u_{i,j}$; dynamic equilibrium $\sigma_{ij,j} - \tau_{ijk,jk} = \rho(\ddot u_i - \ell_{\mathrm{i}}^2 \ddot u_{i,jj})$; traction $p_i$ and double traction $R_i$.
- **Conforming $C^1$ BFS Bloch Formulation:** 32-DOF bicubic Hermite element in $H^2(\Omega)$; exact $4 \times 4$ Gauss–Legendre quadrature; master–slave Bloch reduction applying identical phase shift $e^{\iu \bm{k}\cdot\bm{a}_\alpha}$ to displacement and derivative DOFs; strictly Hermitian reduced pencil ($\bar{\bm{K}} = \bar{\bm{K}}^\mathsf{H}$, $\bar{\bm{M}} = \bar{\bm{M}}^\mathsf{H} > 0$) with BZ periodicity.
- **Layer 5 Verification Suite:** Rigid-body modes at $\Gamma$ (5a); Hermiticity across IBZ (5b); positive definiteness (5c); closed-form acoustic limit error $1.25 \times 10^{-8}$ vs PB2009 (5d); lattice symmetry (5e); branch tracking MAC $> 0.99$ (5f); high-$k$ phase velocity horizon $v_{T,\infty} = 1/\sqrt{10} \approx 0.3162$ vs unbounded $\ell_{\mathrm{i}}=0$ (5g); Poynting energy flux identity $\bm{v}_g = \langle\bm{S}\rangle/(\langle W\rangle + \langle T\rangle)$ to $< 10^{-8}$ (5h); monotone mesh convergence ($4^2 \to 32^2$) with observed rate $p=4.17$ and resolution floor $\varepsilon_\Delta = 4.63 \times 10^{-11}$ (5i).
- **Physical Discoveries:** Directional stop band along $\Gamma$--$X$ ($\Delta_{GX} = +0.0431$ nominal, max $0.0896$ at $\theta=30^\circ, \mathrm{AR}=10$); omnidirectional complete gap absence ($\Delta_{\mathrm{complete}} \le -0.3758$); orientation sensitivity up to $S_\theta = 3.946\,\mathrm{rad}^{-1}$; peak acoustic steering deviation $\delta_{\max} = 2.79^\circ$ at $\bar{k}=0.5$; gradient energy partition increasing from $0.20\%$ to $16.49\%$.

### Claims Requiring Narrowing
Under Path A, the following claims must be narrowed or rephrased:
1. **Band Gaps vs Directional Stop Bands:** All references must strictly refer to *directional stop bands* along high-symmetry paths (specifically $\Gamma$--$X$). Any claim of "band gaps" without qualification must be avoided, and the absence of complete omnidirectional band gaps in homogeneous media must remain an explicit physical finding.
2. **Iso-Frequency Contours:** Claims of calculating full 2D isofrequency contours (IFCs) across the BZ must be narrowed to "acoustic wave steering and group velocity variation evaluated along circular wave-vector contours ($|\bar{\bm{k}}| = 0.5$)".
3. **Phononic Crystals vs Metamaterials:** The scope must be framed as a continuous metamaterial with sub-scale microstructure rather than a composite phononic crystal.
4. **Case C / Inclusions:** Moved entirely to future work.

### Validation Changes
If B1–B3 are de-scoped:
- **Gate G3:** Replaced by Gate G3-Alt (Closed-form analytical validation against PB2009 and LWZ2016 homogeneous limits, combined with the 8-test Layer 5 consistency suite).
- **PCR1:** Amended to mandate passing Layer 3 analytical checks to machine precision ($< 10^{-7}$) and asymptotic horizon verification to $< 0.05\%$, removing the requirement for published bilayer transfer-matrix benchmarks.
- **PCR2:** Amended to remove the requirement for external published benchmark overlays in the main manuscript.
- **Table 1:** Literature positioning table updated to reflect that validation is achieved via closed-form continuum limits and a rigorous 8-test internal verification suite, citing multi-phase bilayer benchmarks as future work.

### Figure/Table Changes
- **Figure 4 (Anchor Overlays):** Formally removed from the manuscript float inventory rather than retained as a blocked placeholder.
- **Table 3 (Anchor Error Metrics):** Formally removed from the float inventory.
- **Figure 7 (Case C Baseline Bands & Modes):** Formally removed from the float inventory.
- **Float Count:** Reduced from 19 candidate floats (16 embedded, 3 blocked) to 16 verified floats (11 figures, 5 tables), with exact sequential numbering (Figures 1–11, Tables 1–5 in the final standalone paper).

### Manuscript Sections Affected
- **Title:** Adjusted to remove "iso-frequency contours" and clarify directional stop bands (e.g., *"Direction-dependent stop bands and acoustic wave steering in two-dimensional strain-gradient elastic media with anisotropic ellipsoidal microstructure: A Bloch–Floquet $C^1$ finite element analysis"* or Blueprint Alternate Title A).
- **Abstract & Introduction (§1):** Reframed to focus exclusively on Case H anisotropic metamaterial dynamics; remove promises of comparing homogeneous dispersion against periodic Bragg phononic crystals.
- **Validation Section (§5):** Remove Sections 5.2 and 5.3 (B1–B3 placeholders); streamline Section 5 to present the Layer 3 analytical benchmark (PB2009), asymptotic verification, and the Layer 5 consistency suite.
- **Results Section (§6):** Remove Section 6.3 (Case C placeholder); expand Section 6.2 to discuss the physical mechanics of the $\Gamma$--$X$ directional stop band.
- **Discussion & Limitations (§8):** Reframe limitations to state that the current study focuses on homogeneous anisotropic microstructure, identifying two-phase composite unit cells with high-order interface jump conditions as future work.

### Governance Amendment Required
Path A cannot be enacted informally. It requires:
1. Promulgation of **Blueprint v1.4** (or formal PI Governance Scope Amendment Document).
2. Explicit re-definition of Gate G3, PCR1, and PCR2.
3. Formal de-scoping of Study S2 (Case C) and candidate floats Fig 4, Tab 3, Fig 7.

---

## 6. Path B — Full Original Scope

If project governance preserves the original full scope, the following substantial scientific, algorithmic, and data work packages must be completed:

### B1–B3 Work Package
1. **Numerical Data Acquisition:**
   - Authoritative tabulated numerical frequency data must be obtained for Li et al. (2024) Figs 2(a), 2(b) and Li et al. (2023) Fig 4(c).
   - Because project governance strictly prohibits using curve digitization as an error metric, these tables must be retrieved via direct author correspondence or open data repositories.
2. **Closure of Open TVs:**
   - **TV1:** Obtain the exact non-dimensional parameters ($c_1, c_R, d_1, d_R$) for Fig 4(c) of Li et al. (2023).
   - **TV12:** Establish locked axis ranges, frequency scales, and wavenumber sampling for Fig 4(a)–(c).
3. **Implementation of 1D Bilayer $C^1$ Finite Element Solver:**
   - The existing 2D Case H BFS code cannot compute 1D bilayer dispersion.
   - A dedicated 1D 2-node $C^1$ Hermite finite element solver must be developed.
   - The solver must implement 1D strain-gradient stiffness with the $1/10$ prefactor, 1D micro-inertia mass matrices, Bloch boundary conditions, and explicit coupling across bimaterial interfaces enforcing all four interface conditions ($[u]=0, [u_{,x}]=0, [p]=0, [R]=0$).
4. **Benchmark Execution & Tabulation:**
   - Run the 1D FE solver against B1, B2, and B3.
   - Compute maximum and per-quantity relative errors against published tables.
   - Verify that errors meet $\le 0.5\%$ (B1) and $\le 2.0\%$ (B2, B3).

### G3/PCR1 Closure
- Populate Table 3 with quantitative error metrics and PASS/FAIL marks.
- Generate Figure 4 vector PDF showing the exact overlays.
- Draft Sections 5.2 and 5.3 in `ms.tex`.
- Formally certify Gate G3 = MET and PCR1 = PASS.

### Case-C / S2 Work Package
1. **Closure of TV6 & TV14 (Case C Parameters & Scaling):**
   - Identify an authoritative, literature-backed parameter set for the composite cell: matrix constants ($E_m, \nu_m, \rho_m, l_{m}, \ell_{\mathrm{i},m}$), inclusion constants ($E_i, \nu_i, \rho_i, l_{i}, \ell_{\mathrm{i},i}$), and radius $R/L$.
   - Formulate and lock the reference frequency convention $\omega_0 = \sqrt{\mu_{\mathrm{ref}} / (\rho_{\mathrm{ref}} L^2)}$ for a two-phase unit cell.
2. **Formulation and Implementation of TV18 (Circular Interface Representation):**
   - Rectangular BFS bicubic Hermite elements suffer an $\mathcal{O}(h)$ boundary representation error across circular interfaces when standard Gauss quadrature is applied to discontinuous material fields.
   - An advanced numerical formulation must be developed: either an adaptive quadtree sub-cell integration scheme that integrates smooth sub-elements along the circle $r=R$, or a curvilinear conforming $C^1$ discretization.
   - Higher-order interface jump conditions must be enforced across the circular boundary.
3. **Execution of Study S2:**
   - Assemble the composite unit cell and perform mesh convergence.
   - Compute the full band structure along $\Gamma$--$X$--$M$--$\Gamma$.
   - Extract the first three complete and partial band gaps.
   - Compute and plot the Bloch eigenmode shapes at the gap edges.

### TV Closure
- Close TV1, TV6, TV12, TV14, and TV18.

### Figure/Table Completion
- Generate `fig04_anchor_overlays.pdf` and embed in Section 5.
- Generate `tab03_anchor_validation.tex` and embed in Section 5.
- Generate `fig07_caseC_bands_modes.pdf` and embed in Section 6.
- Populate the Case C columns in Table 5 (`tab05_gap_summary.tex`).

### Final G4 Conditions
- Verify PCR1 through PCR8 in the computation log.
- Remove all `[BLOCKED — ...]` placeholders.
- PI signs off on Gate G4; compile `ms.pdf` and package final deliverables.

---

## 7. Direct Comparison

| Dimension | Path A: Case H Standalone | Path B: Original Full Scope |
| :--- | :--- | :--- |
| **Core Scientific Contribution** | 2D strain-gradient anisotropic metamaterial with ellipsoidal length tensor, micro-inertia, $C^1$ BFS Bloch FE formulation, directional stop bands, acoustic wave steering, energy flux, and 8-test Layer 5 verification suite. | Everything in Path A, PLUS 1D bilayer published benchmark validation (B1–B3) and 2D composite phononic crystal with circular inclusion for omnidirectional Bragg gaps (Case C / S2). |
| **Required Validation** | Layer 3 analytical validation (PB2009 to $1.25 \times 10^{-8}$), Layer 3b asymptotic horizon ($0.03\%$), and Layer 5 consistency suite (5a–5h) plus mesh convergence ($p=4.17$). | Layers 1, 2a, 2b published benchmark validation ($\le 2\%$ relative error vs Li et al. 2023, 2024), Fig 4 overlays, Table 3 error metrics, plus all Layer 3 and Layer 5 checks. |
| **Additional Solver Development** | None. Existing 2D BFS solver (`p5_core.py`, `p5_run.py`) is complete, verified, and locked. | Substantial: (1) New 1D 2-node $C^1$ Hermite FE solver with 4 interface conditions; (2) Cut-cell or adaptive sub-cell integration scheme for circular inclusion on rectangular BFS grid (TV18). |
| **Additional Data Acquisition** | None. Uses existing verified datasets (`p5_production_raw.json`, `p4b_5g_to_5i.json`). | External tabulated numerical eigenvalues for Li et al. (2024) Figs 2(a), 2(b) and Li et al. (2023) Fig 4(c) (closing TV1, TV12); published or standardized composite parameters (closing TV6, TV14). |
| **Case-C Work** | Fully de-scoped and deferred to future work. | Full formulation, implementation, convergence testing, baseline run (S2), band-gap extraction, mode shape visualization, Fig 7 generation, and Table 5 completion. |
| **Manuscript Changes** | Title adjustment; remove blocked placeholders (Fig 4, Tab 3, Fig 7, Sec 5.2, 5.3, 6.3); reframe introduction/conclusions around homogeneous metamaterial steering; reduce float count to 16 verified floats. | Replace blocked placeholders with completed Fig 4, Tab 3, Fig 7; write full text for Sec 5.2, 5.3, 6.3; update Table 5 with Case C gaps; maintain full 19-float inventory. |
| **Remaining Blockers** | None within the Case H scope; requires only formal governance approval to amend Blueprint v1.3. | TV1, TV6, TV12, TV14, TV18, missing published data for B1–B3, absence of 1D bilayer solver, geometric cut-cell integration for BFS circular inclusion. |
| **Governance Amendment Required** | **YES.** Requires formal amendment of Blueprint v1.3 to Blueprint v1.4, revising PCR1, PCR2, G3, G-F, and Section 6.3 to de-scope B1–B3 and Case C. | **NO.** Path B aligns with the current text of Blueprint v1.3; however, it requires project timeline extension and technical work package authorization. |
| **Release Condition** | Approval of Blueprint v1.4 by PI / governance authority; editorial cleanup of placeholders; re-compilation of `ms.tex`. | Completion and verification of 1D FE solver, external data acquisition, G3/PCR1 validation, cut-cell integration, S2 execution, and Gate G4 sign-off. |

---

## 8. Title / Abstract / Novelty Scope Audit

A detailed audit of the manuscript metadata was performed against Path A requirements:

1. **Title Audit:**
   - *Current Title:* “Direction-dependent band gaps and iso-frequency contours in two-dimensional strain-gradient elastic media with anisotropic ellipsoidal microstructure: A Bloch–Floquet $C^1$ finite element analysis”
   - *Audit Finding on "band gaps":* In homogeneous Case H, complete omnidirectional band gaps do not exist ($\Delta_{\mathrm{complete}} \le -0.3758$). Case H produces *directional stop bands* along $\Gamma$--$X$ ($\Delta_{GX} = +0.0431$). Retaining "band gaps" without qualification is misleading.
   - *Audit Finding on "iso-frequency contours":* Figure 12 computes acoustic wave steering deviation $\delta(\phi)$ and group velocity $|\bm{v}_g|(\phi)$ along a 1D circular wave-vector path $|\bar{\bm{k}}| = 0.5$. It does not plot 2D closed isofrequency contours across the $(k_x, k_y)$ plane.
   - *Conclusion:* Under Path A, the title **must be modified**. Recommended modification:
     *“Direction-dependent stop bands and acoustic wave steering in two-dimensional strain-gradient elastic media with anisotropic ellipsoidal microstructure: A Bloch–Floquet $C^1$ finite element analysis”*
     (or Blueprint v1.3 line 871 Alternate Title A: *“Directional wave steering and microstructure-induced dispersion in strain-gradient media with anisotropic characteristic length tensor”*).
2. **Abstract, Highlights, and Introduction:**
   - Must be aligned to emphasize the 2D tensor formulation, passive rotation, directional stop bands along $\Gamma$--$X$, acoustic steering up to $\delta_{\max} = 2.79^\circ$, and micro-inertia stabilization ($v_{T,\infty} = 0.3162$), while removing unfulfilled claims regarding omnidirectional band gaps or two-phase phononic crystals.
3. **Table 1 (Literature Positioning):**
   - The unique contributions of the work—namely: (1) 2D anisotropic tensor microstructure; (2) conforming $C^1$ BFS Bloch finite element with phase tying on derivative DOFs; (3) micro-inertia dynamic stabilization; and (4) acoustic wave steering analysis—are already established in Table 1 based entirely on Case H. The positioning does not depend on Case C or B1–B3 for its novelty.

---

## 9. Scientific Validity vs Governance Compliance

The audit establishes a sharp, fundamental distinction between scientific validity and governance compliance:

1. **Scientific Validity:**
   - The Case-H formulation, numerical solver, and verification suite are scientifically sound, rigorous, and completely verified.
   - Discretization errors are bounded and quantified ($p=4.17$, $\varepsilon_\Delta = 4.63 \times 10^{-11}$).
   - Dynamic conservation laws (Poynting flux identity $\bm{v}_g = \langle\bm{S}\rangle/\langle W+T\rangle$) hold to $< 10^{-8}$.
   - Limiting analytical cases match published theory to $1.25 \times 10^{-8}$ (PB2009) and $0.03\%$ (asymptotic horizon).
   - From a purely technical standpoint, Case H constitutes a complete, high-quality archival contribution.
2. **Governance Compliance:**
   - Project governance (Blueprint v1.3 Section 9.4 and Calculation Master Plan Section B) is an absolute, binding contract.
   - Blueprint v1.3 line 881 explicitly mandates: *"The manuscript cannot be submitted until every line below is true and evidenced in the computation log... PCR1: All mandatory published benchmarks (Layers 1, 2a, 2b) PASS with maximum relative error $\le 2\%$... A failed PCR blocks submission exactly as G3 does."*
   - Line 907 designates the PI as the gate owner who signs G4 only after PCR1–PCR8 are checked.
   - There is no self-executing waiver or automatic exemption for missing literature data in Blueprint v1.3.
   - Therefore, scientific validity alone cannot override project governance. To submit Case H as a standalone paper, governance must be formally updated through an authoritative amendment.

---

## 10. Remaining Blockers

A synthesis of the remaining blockers confirms:

1. **Under Path A (Case H Standalone):**
   - **Zero Technical Blockers:** The code, parameters, raw datasets, figures, tables, and test suite for Case H are complete and verified.
   - **One Governance Blocker:** Blueprint v1.3 must be formally amended to Blueprint v1.4 to de-scope B1–B3 and Case C, redefine G3/PCR1, and adjust float requirements.
2. **Under Path B (Original Full Scope):**
   - **Blocker 1 (Data):** Published numerical tables for B1, B2, B3 do not exist in the literature (prohibiting quantitative validation under the rule forbidding curve digitization).
   - **Blocker 2 (Parameters):** TV1 ($c, d$ parameters for Li et al. 2023 Fig 4(c)) and TV12 (axis limits) remain OPEN.
   - **Blocker 3 (Solver Architecture):** A 1D bilayer $C^1$ finite element solver with 4 interface conditions per bimaterial interface does not exist in the repository.
   - **Blocker 4 (Case C Parameters):** TV6 (Case C material contrast and inclusion radius) and TV14 (reference phase scaling) remain OPEN.
   - **Blocker 5 (Case C Discretization):** TV18 remains OPEN (the rectangular BFS element incurs an $\mathcal{O}(h)$ boundary representation error across circular interfaces, requiring cut-cell adaptive quadrature or curvilinear elements).

---

## 11. Governance Classification

Applying the rigorous decision logic defined by project governance:
- `CASE_H_STANDALONE_IS_GOVERNANCE_PLAUSIBLE` would imply that the existing governance documents currently contain an automatic mechanism or built-in waiver to de-scope the project. No such self-executing mechanism exists in Blueprint v1.3.
- `GOVERNANCE_AMENDMENT_REQUIRED` accurately states that formal administrative action is necessary before either path can proceed to release.
- `FULL_SCOPE_IS_CURRENTLY_GOVERNANCE_LOCKED` is the foundational, objective classification because Blueprint v1.3 explicitly makes B1–B3 and S2 mandatory, locks Gate G3 and PCR1 as hard submission blockers, and provides no current mechanism permitting their removal without formal amendment.

Therefore, the authoritative classification is:

### **Classification:** `FULL_SCOPE_IS_CURRENTLY_GOVERNANCE_LOCKED`

*(Consequence: Because full scope is currently governance-locked, the manuscript cannot be released under either path today: Path B is blocked by outstanding scientific and data requirements, while Path A is blocked by the necessity of a formal Governance Amendment to Blueprint v1.3).*

---

## 12. Exact Next Governance Action

The formal next governance action required from the Project Investigator (PI) / Governance Authority is:

**Action:** Issue a formal **Governance Scope Determination Directive** choosing between:

1. **Directive A (Authorize Blueprint v1.4 for Standalone Case-H Submission):**
   - Promulgate *Paper9 Blueprint v1.4*, formally amending:
     - Section 5: Redefine validation to rely on closed-form analytical benchmarks (Layer 3) and the 8-test internal verification suite (Layer 5), moving 1D bilayer transfer-matrix benchmarks (B1–B3) to future work.
     - Section 6: De-scope Case C (Study S2) to a separate follow-up publication on composite phononic crystals.
     - Section 9.4: Revise PCR1 and PCR2 to match the amended validation scope.
     - Float Inventory: Reduce candidate floats from 19 to 16, formally removing blocked placeholders (Fig 4, Tab 3, Fig 7).
     - Title: Update title to reflect directional stop bands and acoustic wave steering.
   - Authorize editorial cleanup of `ms.tex` and compilation of the final submission package.

2. **Directive B (Authorize Work Packages for Full Scope Completion):**
   - Commission the formal technical work packages required to execute Path B:
     - Work Package B1: Author correspondence for B1–B3 numerical tables; resolution of TV1 and TV12.
     - Work Package B2: Implementation and verification of a 1D 2-node $C^1$ Hermite finite element solver.
     - Work Package B3: Literature definition of Case C parameters (TV6, TV14) and implementation of cut-cell adaptive quadrature for circular inclusions on BFS grids (TV18).
     - Work Package B4: Execution of Study S2, generation of Fig 4, Tab 3, Fig 7, and closure of Gate G3, PCR1, and Gate G4.
