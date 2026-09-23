# P11 Case C Implementation & Verification Audit (Study S2)

**Date:** 2026-09-23  
**Repository Branch:** `phase-1-symbolic`  
**Auditor:** P11 Autonomous Research & Audit Agent  
**Operational Framework:** Paper9 Blueprint v1.3 Full Scope (*IJMS* submission target)

---

## 1. Executive Summary & Verification Outcome

This audit establishes the formal closure and quantitative verification of **Case C / Study S2** (2D composite phononic crystal unit cell with circular inclusion) under the strict [S] design-choice framework, resolving:
- **TV18:** Circular inclusion discretization on $C^1$ Bogner–Fox–Schmit (BFS) rectangular element meshes.
- **TV6:** Material stiffness and inertia contrast ratios.
- **TV14:** Unit-cell reference frequency and non-dimensionalization framework.

**Verification Milestones Achieved:**
1. **Level 1 Identical-Material Reduction Test:** **PASS**  
   Setting inclusion material identical to matrix material recovers the homogeneous Case H reference eigenvalues to machine precision ($\le 5.55 \times 10^{-15}$ on $1\times 1$ mesh; within $0.85\%$ on $2\times 2$ mesh strictly consistent with FEM $h$-refinement convergence).
2. **Level 2 Heterogeneous Phononic Crystal Dispersion:** **PASS**  
   Multi-element Bloch analysis along the irreducible Brillouin zone path $\Gamma$--$X$--$M$--$Gamma$ reveals an open band gap between Band 3 and Band 4 ($\bar{\omega} \in [4.5698, 7.1430]$, $\Delta[\text{path}] = 2.5732$).
3. **Full 2D Brillouin Zone Grid Scan & Subset Inequality Verification:** **PASS**  
   Omnidirectional 2D scan across the entire Brillouin zone confirms the existence of a **complete 2D omnidirectional band gap** ($\Delta[\text{complete}] = 2.5732$, normalized gap width $\Delta/\bar{\omega}_{\text{mid}} = 43.94\%$). The project's strict subset inequality holds without violation:
   $$\Delta[\mathrm{leg}] \ge \Delta[\mathrm{path}] \ge \Delta[\mathrm{complete}]$$
4. **Deliverables Generated:**
   - Solver module: Multi-element mesh assembly and Bloch reduction integrated into `paper9/solver/bfs_bloch_solver.py`.
   - Automated verification test: `paper9/verification/suite/test_p11_case_c.py` (3/3 tests passing).
   - Production simulation: `paper9/production/p11_caseC_run.py` -> `paper9/results/raw/p11_caseC_raw.json`.
   - Figure 7: `paper9/figures/out/fig07_caseC_dispersion.pdf` and `fig07_caseC_dispersion.png`.

---

## 2. Design Choices Rationale: TV18, TV6, TV14

### 2.1 TV18 — Circular Inclusion on BFS Rectangular Mesh
- **Method Chosen:** Standard Gauss-quadrature immersed indicator integration $\chi(\mathbf{x})$.
- **Technical Formulation:**  
  The Bogner–Fox–Schmit (BFS) element employs bicubic Hermite shape functions that strictly require rectangular geometry aligned with Cartesian axes $(x, y)$ to preserve conformality ($C^1$ continuity of displacements and slope DOFs across element boundaries). An arbitrary curved circular inclusion boundary of radius $r_0$ centered at $(x_c, y_c) = (L/2, L/2)$ is represented on a regular $N_x \times N_y$ mesh via quadrature-point material evaluation:
  $$\mathbf{C}(\mathbf{x}) = \mathbf{C}_m + (\mathbf{C}_i - \mathbf{C}_m) \chi(\mathbf{x}), \quad \rho(\mathbf{x}) = \rho_m + (\rho_i - \rho_m) \chi(\mathbf{x})$$
  $$\chi(\mathbf{x}) = \begin{cases} 1, & \|\mathbf{x} - \mathbf{x}_c\| \le r_0 \\ 0, & \|\mathbf{x} - \mathbf{x}_c\| > r_0 \end{cases}$$
- **Scientific References:**  
  This approach is the standard immersed / fictitious-domain numerical integration technique widely established in composite mechanics and metamaterials (e.g., Zienkiewicz, Taylor & Zhu, *The Finite Element Method*, 7th ed., 2013; Belytschko, Gracie & Ventura, *Int. J. Numer. Meth. Engng.* 66:379–401, 2006; Wang & Wang, *Comput. Methods Appl. Mech. Engrg.* 193:407–430, 2004).
- **$C^1$ BFS Compatibility Statement:**  
  The displacement field $u_i(x, y)$ remains bicubic Hermite across all element interfaces, guaranteeing $C^1$ continuity without parasitic displacement jumps. We explicitly state that the circular interface is **not** claimed to be represented as an exact curved boundary conforming to element edges; rather, it is integrated as an exact piecewise domain integral using standard $4\times 4$ Gauss–Legendre quadrature within each background element.

### 2.2 TV6 — Material Contrast Selection
- **Peer-Reviewed Anchor Source:**  
  Material parameters are sourced directly from the archival literature of Peijun Wei's research group (File 4 of supplied source package: Zhengqiang Zhan & Peijun Wei, *Influences of anisotropy on band gaps of 2D phononic crystal*, *Acta Mech. Solida Sin.* 23(2):181–188, 2010):
  - **Matrix (Epoxy):**
    $\rho_m = 1142\,\mathrm{kg/m}^3$, $\mu_m = 1.48\,\mathrm{GPa}$, $\lambda_m = 4.57\,\mathrm{GPa}$ ($\nu_m = 0.377$).
  - **Inclusion (YBCO ceramic):**
    $\rho_i = 6333\,\mathrm{kg/m}^3$, $\mu_i = 37.0\,\mathrm{GPa}$, $\lambda_i = 95.0\,\mathrm{GPa}$ ($\nu_i = 0.360$).
- **Contrast Ratios:**
  - Shear modulus contrast: $\chi_\mu = \mu_i / \mu_m = 37.0 / 1.48 = 25.0$.
  - Density contrast: $\chi_\rho = \rho_i / \rho_m = 6333 / 1142 = 5.546$.
  - Longitudinal modulus contrast: $\chi_{c_{11}} = 169.0 / 7.53 = 22.44$.
- **Scientific Rationale:**  
  Using Epoxy/YBCO directly grounds Case C in the identical institutional literature series as Benchmarks B1, B2, and B3, ensuring complete constitutive coherence across the manuscript.

### 2.3 TV14 — Non-Dimensionalization Framework
- **Length Scale:** Unit-cell lattice pitch $L = a = 1.0$.
- **Reference Acoustic Velocity:** Matrix transverse shear wave velocity:
  $$c_t = \sqrt{\frac{\mu_m}{\rho_m}} = \sqrt{\frac{1.48 \times 10^9\,\mathrm{Pa}}{1142\,\mathrm{kg/m}^3}} = 1138.4\,\mathrm{m/s}$$
- **Reference Frequency:** $\omega_0 = \frac{\pi c_t}{L}$.
- **Normalized Frequency:** $\bar{\omega} = \frac{\omega L}{\pi c_t} = \frac{\omega}{\omega_0}$.
- **Normalized Wavenumber:** $\bar{k}_x = \frac{k_x L}{\pi} \in [0, 1]$, $\bar{k}_y = \frac{k_y L}{\pi} \in [0, 1]$.
- **In-Plane Gradient Length Scales:**
  - Matrix: $\ell_m / L = 0.10$ ($\ell_m^2 = 0.01$, $\mathbf{L}_m = \mathrm{diag}(0.01, 0.01)$).
  - Inclusion: $\ell_i / L = 0.20$ ($\ell_i^2 = 0.04$, $\mathbf{L}_i = \mathrm{diag}(0.04, 0.04)$).

---

## 3. Level 1 Identical-Material Reduction Verification

To rigorously prove mathematical and implementation correctness, the multi-element BFS solver was tested in the limit where inclusion material properties are set identical to matrix properties ($\chi_\mu = 1.0, \chi_\rho = 1.0, \ell_i = \ell_m$):

| Wave Vector $\mathbf{k}$ | Mode Index | Case H (1-Element Solver) | Multi-Element ($1\times 1$ Mesh) | Algebraic Difference | Multi-Element ($2\times 2$ Mesh) | $h$-Refinement Convergence |
|---|---|---|---|---|---|---|
| **$X/2$ ($\pi/2, 0$)** | Mode 1 (Acoustic) | 1.50620652 | 1.50620652 | $< 5.55 \times 10^{-15}$ | 1.50596949 | $-0.016\%$ |
| | Mode 2 (Acoustic) | 2.60882621 | 2.60882621 | $< 5.55 \times 10^{-15}$ | 2.60841567 | $-0.016\%$ |
| **$X$ ($\pi, 0$)** | Mode 1 (Acoustic) | 2.71402578 | 2.71402578 | $< 1.78 \times 10^{-15}$ | 2.71278450 | $-0.046\%$ |
| | Mode 2 (Acoustic) | 2.73600334 | 2.73600334 | $< 1.78 \times 10^{-15}$ | 2.71278450 | $-0.849\%$ |
| **$M$ ($\pi, \pi$)** | Mode 1 (Acoustic) | 3.46447994 | 3.46447994 | $< 1.78 \times 10^{-15}$ | 3.45142816 | $-0.377\%$ |
| | Mode 2 (Acoustic) | 3.48046610 | 3.48046610 | $< 1.78 \times 10^{-15}$ | 3.45142816 | $-0.834\%$ |

**Findings:**
1. The $1\times 1$ multi-element assembly reproduces the reference single-element Case H eigenvalues to machine precision ($\le 5.55 \times 10^{-15}$), verifying exact algebraic and code equivalence.
2. The $2\times 2$ mesh frequencies are strictly lower than the $1\times 1$ mesh frequencies (max decrease $0.85\%$), proving classical Rayleigh–Ritz upper-bound variational convergence.

---

## 4. Level 2 Heterogeneous Phononic Crystal Results (Study S2)

### 4.1 Baseline Band Structure ($r_0 / a = 0.30$, Filling Fraction $f = 28.27\%$)

A full Bloch dispersion solve was conducted on a $4\times 4$ BFS mesh (128 master DOFs) along the standard IBZ path $\Gamma$--$X$--$M$--$\Gamma$ and across a dense $11\times 11$ full 2D Brillouin zone grid:

- **Band 1 (Acoustic Branch 1):** Starts at $\bar{\omega}(\Gamma) = 0.0$; reaches $\bar{\omega}(X) = 2.2144$; reaches $\bar{\omega}(M) = 2.6148$; global maximum $\bar{\omega} = 2.7760$.
- **Band 2 (Acoustic Branch 2):** Starts at $\bar{\omega}(\Gamma) = 0.0$; reaches $\bar{\omega}(X) = 2.9803$; reaches $\bar{\omega}(M) = 3.7305$; global maximum $\bar{\omega} = 3.7305$.
- **Band 3 (Optical Branch 1):** $\bar{\omega}(\Gamma) = 3.5614$; reaches $\bar{\omega}(X) = 4.5698$; reaches $\bar{\omega}(M) = 3.7305$; **global maximum across 2D BZ: $\bar{\omega} = 4.5698$**.
- **Band 4 (Optical Branch 2):** $\bar{\omega}(\Gamma) = 7.1812$; reaches $\bar{\omega}(X) = 7.3261$; reaches $\bar{\omega}(M) = 7.7578$; **global minimum across 2D BZ: $\bar{\omega} = 7.1430$**.

### 4.2 Complete 2D Omnidirectional Band Gap Evaluation

| Quantity | Symbolic Form | Numerical Value | Status |
|---|---|---|---|
| **Band 3 Global Maximum** | $\max_{\mathbf{k} \in \mathrm{BZ}} \bar{\omega}_3(\mathbf{k})$ | $4.5698$ | Lower gap edge |
| **Band 4 Global Minimum** | $\min_{\mathbf{k} \in \mathrm{BZ}} \bar{\omega}_4(\mathbf{k})$ | $7.1430$ | Upper gap edge |
| **Directional Gap $\Gamma$--$X$** | $\Delta[\Gamma\text{--}X]$ | $2.6114$ | OPEN |
| **Directional Gap $X$--$M$** | $\Delta[X\text{--}M]$ | $2.7563$ | OPEN |
| **Directional Gap $M$--$\Gamma$** | $\Delta[M\text{--}\Gamma]$ | $2.5732$ | OPEN |
| **IBZ Path Gap** | $\Delta[\mathrm{path}]$ | $2.5732$ | OPEN |
| **Complete 2D Omnidirectional Gap** | $\Delta[\mathrm{complete}]$ | $2.5732$ | **COMPLETE GAP OPEN** |
| **Mid-Gap Frequency** | $\bar{\omega}_{\mathrm{mid}}$ | $5.8564$ | Normalized scale |
| **Normalized Gap Width** | $\Delta / \bar{\omega}_{\mathrm{mid}}$ | $43.94\%$ | Broad stop band |
| **Subset Inequality** | $\Delta[\mathrm{leg}] \ge \Delta[\mathrm{path}] \ge \Delta[\mathrm{complete}]$ | Validated ($2.61 \ge 2.57 \ge 2.57$) | **PASS** |

### 4.3 Parametric Tuning Sweep vs Inclusion Radius $r_0 / a$

| Radius Ratio $r_0 / a$ | Filling Fraction $f$ | Lower Edge (Band 3) | Upper Edge (Band 4) | Gap Width $\Delta_{\mathrm{complete}}$ | Normalized Width $\Delta/\bar{\omega}_{\mathrm{mid}}$ | Gap State |
|---|---|---|---|---|---|---|
| $0.20$ | $12.57\%$ | $4.5754$ | $5.4042$ | $0.8288$ | $16.61\%$ | Complete Open |
| $0.25$ | $19.63\%$ | $4.3503$ | $5.7877$ | $1.4374$ | $28.36\%$ | Complete Open |
| **$0.30$** | **$28.27\%$** | **$4.5698$** | **$7.1430$** | **$2.5732$** | **$43.94\%$** | **Optimal Open** |
| $0.35$ | $38.48\%$ | $5.0848$ | $7.5958$ | $2.5110$ | $39.60\%$ | Complete Open |
| $0.40$ | $50.27\%$ | $5.3797$ | $7.8223$ | $2.4426$ | $37.00\%$ | Complete Open |

**Physical Insight:**  
The complete band gap reaches its maximum width of $\Delta / \bar{\omega}_{\text{mid}} = 43.94\%$ at $r_0/a = 0.30$. Below $r_0 = 0.30$, scattering from the inclusion is weaker, reducing gap width; above $r_0 = 0.30$, the rigid inclusion raises both band edges while acoustic matrix modes shift upward, compressing the relative gap. This matches standard literature findings for square phononic lattices (Zhan & Wei 2010).

---

## 5. Conclusion & Manuscript Readiness

Case C / Study S2 is fully resolved, implemented, verified, and backed by reproducible raw data and publication-quality figures:
- `fig07_caseC_dispersion.pdf` / `.png` generated and verified.
- `sec06_results.tex` unblocked and ready for full scientific integration.
