# Stage 1 — Blocker Audit & Resolution Record

**Date of Audit:** 2026-09-22  
**Branch:** `phase-1-symbolic`  
**Governing Documents:** `CALC_MASTER_PLAN.md` §B, §E, §H; Blueprint §5, §6; `paper9/audit/traceability_matrix.csv`

---

## 1. Stage 1A: Published Validation Gate G3 / PCR1 (B1, B2, B3)

### Findings
1. **Primary Sources Examined:**
   - `paper9/analytic/li2024/s41598-024-75049-1.pdf` (Li et al., *Sci. Rep.* 14:24035, 2024)
   - `paper9/analytic/li2023/17455030.2023.2222189.pdf` (Li et al., *Waves Random Complex Media* 36:5715–5735, 2023)
2. **Tabulated Data Absence:**
   - Neither source PDF provides tabulated frequencies $\omega(k)$, band-gap boundary values, or numeric tables of eigenvalues. All benchmark results are presented solely as line curves in rasterized figures.
3. **Methodological Independence & Solver Scope:**
   - The primary research solver in this project is the 2D $C^1$ BFS bicubic Hermite finite element code (`paper9/solver/bfs_bloch_solver.py`), constructed for 2D square unit cells.
   - Li 2024 and Li 2023 both employ a 1D analytical transfer-matrix (TM) formulation across planar layers. An independently written 1D TM code does not validate the 2D BFS finite element implementation.
4. **Digitization Constraint:**
   - Per Blueprint §5 and Master Plan §K: *"Curve digitisation is permitted only to draw overlay figures, never to compute error numbers."*
   - In the absence of published tables, any reported error percentage would reflect digitization pixel uncertainty rather than a rigorous solver tolerance check ($\le 2\%$).
5. **Conclusion:**
   - G3 cannot be genuinely closed without inventing data or violating the digitization ban.
   - **Status:** **BLOCKED**. Gate **G3 = NOT MET**, **PCR1 = NOT PASS**.

---

## 2. Stage 1B: Technical Verification Items TV1 & TV12

### Findings
1. **TV1 — Li 2023 Fig. 4(c) Non-dimensional Parameters:**
   - Li 2023 Page 15, Figure 4(c) compares the authors' gradient elastic model against literature reference [34] (LWZ 2016).
   - Neither the figure caption nor the main text specifies the non-dimensional parameters $(\bar c_1, c_R, \bar d_1, d_R)$ for this panel.
   - Candidate sets exist in Fig. 3(b) of Li 2023 $(\bar c_1=0.15, c_R=1.5, \bar d_1=0.25, d_R=1.5)$ and in LWZ 2016 Fig. 10 $(\bar c_1=0.15, \bar d_1=0.25, \bar c=0.77, \bar d=0.77)$, but neither is stated in the text.
   - Selecting a set would constitute unverified guesswork.
   - **Status:** **TV1 remains OPEN.**
2. **TV12 — Overlay Axis Ranges and Sampling:**
   - Numerical axis limits (minima, maxima, and tick values) for Fig. 4(a)–(c) are not printed in the source text.
   - **Status:** **TV12 remains OPEN.**

---

## 3. Stage 1C: Case C Production Configuration (TV6, TV14, TV18)

### Findings
1. **TV6 (Case C Parameters):**
   - The repository contains no locked or published parameters for Case C: inclusion radius $R/L$, matrix vs inclusion Young's moduli ($E_m, E_i$), Poisson's ratios ($\nu_m, \nu_i$), densities ($\rho_m, \rho_i$), or inclusion gradient lengths ($l_{1,i}, l_{2,i}, \ell_{i,i}$).
   - Creating these values would violate the rule against inventing parameters.
   - **Status:** **TV6 (Case C) remains OPEN.**
2. **TV14 (Case C Reference Phase Non-dimensionalization):**
   - Which constituent phase defines $\omega_0 = \sqrt{\mu/(\rho L^2)}$ in a two-phase composite cell is undefined.
   - **Status:** **TV14 remains OPEN.**
3. **TV18 (Circular Inclusion Representation on BFS Grid):**
   - The BFS bicubic Hermite element is strictly axis-aligned rectangular ($Q_3$ tensor product). It lacks isoparametric curvilinear mapping.
   - Assigning material properties at Gauss points across elements cut by a circular boundary incurs an $O(h)$ boundary area error (demonstrated in `audit_m14_independent.py` check [Q6]).
   - A conforming boundary-fitted $C^1$ discretization is not part of the locked formulation.
   - **Status:** **TV18 remains OPEN.**
4. **Study S2 Status:**
   - Because TV6, TV14, and TV18 are unresolved, Study S2 (Case C baseline) cannot be executed without speculative modeling.
   - **Status:** **Study S2 is BLOCKED.**

---

## 4. Stage 1D: Benchmark B6 Quantitative Status

### Findings
1. **Governing Reference:** Li, Wei & Zhou (*Acta Mech.* 227:1005–1023, 2016).
2. **Independent Code Assets:**
   - `paper9/validation/b6_lwz_tm/lwz_tm_sh_normal.py`
   - `paper9/validation/b6_lwz_tm/run_lwz_tm_validation.py`
3. **Quantitative Evidence Achieved:**
   - L1 (homogeneous limit vs Eq. 14.1): max relative error $1.429 \times 10^{-14} \le 10^{-8}$ (**PASS**).
   - L2 (identical bilayer identity): max relative error $4.441 \times 10^{-16} \le 10^{-12}$ (**PASS**).
4. **Fig. 3 Quantitative Comparison:**
   - LWZ 2016 contains no numerical table of dispersion curves or band-gap edges.
   - The caption provides Left (normal, $\bar\xi=0$), Middle (edges vs $\bar\xi$), and Right (oblique, $\bar\xi\neq 0$ with no numerical $\bar\xi$).
   - Without published numbers, a quantitative error percentage against the figure cannot be computed.
5. **Conclusion:**
   - **Status:** **B6 remains PARTIAL** (L1/L2 verified; Fig. 3 quantitative comparison blocked).

---

## 5. Summary of Blocker Actions

| Blocker Item | Decision / Action Taken | Impact on Phase 6 |
|---|---|---|
| **Gate G3 / PCR1** | Preserve as **NOT PASS / NOT MET**; no simulated validation. | Fig 4 and Table 3 blocked from production. |
| **TV1 / TV12** | Preserve as **OPEN**; ambiguity documented. | Fig 4(c) overlay blocked. |
| **TV6 (Case C) / TV14 / TV18** | Preserve as **OPEN**; no parameters invented. | Fig 7 and Case C columns in Table 5 blocked. |
| **Study S2** | Mark **BLOCKED**; skip Stage 2. | Fig 7 omitted from generated floats. |
| **B6** | Preserve as **PARTIAL**; no status inflation. | Preserves rigorous gate standards. |
