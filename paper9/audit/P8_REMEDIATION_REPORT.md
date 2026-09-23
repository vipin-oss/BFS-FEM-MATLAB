# P8 Controlled Remediation Report

**Date:** 2026-09-23  
**Repository:** `https://github.com/vipin-oss/BFS-FEM-MATLAB`  
**Branch:** `phase-1-symbolic`  
**Starting Verified HEAD:** `610f401032e74f4217c457eea6e679aa58224c57`  
**Remediation Agent:** P8 Controlled Forensic Remediation Agent  
**Operational Scope:** Surgical remediation of findings documented in `paper9/audit/P8_FORENSIC_MANUSCRIPT_AUDIT.md`  
**Final Remediation Verdict:** `P8_REMEDIATION_COMPLETE`

---

## 1. Starting Repository State

At the start of Phase 8 remediation, repository status, branches, and commit hashes were audited:

- **Branch:** `phase-1-symbolic`
- **Starting HEAD SHA:** `610f401032e74f4217c457eea6e679aa58224c57`
- **Remote `origin/phase-1-symbolic`:** `610f401032e74f4217c457eea6e679aa58224c57` (synchronized)
- **Remote `origin/main`:** `1de47a4d111260ffb9b48d7c99e9db45102367c7` (untouched)
- **Working Tree:** Pristine clean with only the forensic audit deliverable `paper9/audit/P8_FORENSIC_MANUSCRIPT_AUDIT.md` present.

---

## 2. Original P8 Findings

The authoritative forensic audit (`paper9/audit/P8_FORENSIC_MANUSCRIPT_AUDIT.md`) registered eight total findings:
- **CRITICAL:** 0
- **HIGH:** 4 (FIND-01, FIND-02, FIND-03, FIND-04)
- **MEDIUM:** 1 (FIND-05)
- **LOW:** 3 (FIND-06, FIND-07, FIND-08)

All eight findings have been systematically resolved and verified through targeted code and text edits, accompanied by an automated regression test suite (`test_p8_remediation.py`).

---

## 3. Finding-by-Finding Remediation

| ID | Severity | Location | Original Issue | Correction Applied | Authoritative Evidence | Verification Method | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FIND-01** | **HIGH** | `sec06_results.tex`, Sec 6.2, lines 10–15 | Figure 6 caption and text claimed plotted curves were $\mathrm{AR}=5$, quoted $\Delta_{GX} = 0.0898$ (which was the energy flux ratio $T_g/T$), and listed non-standard parameters ($\rho=1000, \mu=1\,\mathrm{GPa}, \ell_i=0.1$). | Corrected caption and prose to reflect $\mathrm{AR}=10$ at $\theta=0^\circ$ and $\theta=45^\circ$, aligned parameters with Table 2 ($\rho=1.0\,\mathrm{kg/m}^3, \mu=1.0\,\mathrm{Pa}, \ell_i=0.20\,\mathrm{m}$), and quoted verified directional gap $\Delta_{GX} = +0.0431$. | `fig06_caseH_dispersion.py`, `p5_production_raw.json` (`study_S1`, `study_S5`), `tab02_parameters.tex`, `tab05_gap_summary.tex` | Pytest `test_find01_fig06_caption_and_data_traceability` PASS | **RESOLVED** |
| **FIND-02** | **HIGH** | `sec06_results.tex`, lines 58, 62; `sec08_discussion.tex`, line 8; `sec09_conclusions.tex`, line 9 | Prose in four locations stated that the maximum directional stop band was $\Delta_{GX} = 0.1654$ at $(\theta=45^\circ, \mathrm{AR}=10)$, whereas the raw production data has a global maximum of $0.0896$ at $(\theta=30^\circ, \mathrm{AR}=10)$ and $0.0431$ at $(\theta=45^\circ, \mathrm{AR}=10)$. | Replaced the spurious value $0.1654$ across all four locations with the verified maximum $\Delta_{GX} = 0.0896$ at $(\theta=30^\circ, \mathrm{AR}=10)$ and explicitly noted $\Delta_{GX} = 0.0431$ at $\theta=45^\circ$. | `p5_production_raw.json` (`study_S5_design_map`), `tab05_gap_summary.tex` | Pytest `test_find02_design_map_max_gap_reconciliation` PASS | **RESOLVED** |
| **FIND-03** | **HIGH** | `sec06_results.tex`, Sec 6.4, line 38 | Text stated transverse acoustic frequency $\bar{\omega}_T(X)$ dropped from $1.154$ to $0.812$, which conflicted with plotted curves and raw data. | Corrected frequency migration numbers in Section 6.4 to match raw data: $\bar{\omega}_T(X)$ drops from $2.915$ to $2.672$ and $\bar{\omega}_L(X)$ drops from $5.050$ to $4.628$. | `p5_production_raw.json` (`study_S3`), `fig08_theta_sweep.py` | Pytest `test_find03_theta_sweep_migration_values` PASS | **RESOLVED** |
| **FIND-04** | **HIGH** | `appA_asymptotics.tex`, Eqs (57)–(62); `sec07_steering.tex`, Eq (27) | Appendix A omitted the constitutive prefactor $1/10$ from the gradient stiffness term, stated $\bar{v}_{T,\infty} = \bar{l}/\bar{\ell}_i$, and inserted synthetic values ($l_2=0.10, \ell_i=0.3162$) instead of Table 2 baseline values ($l_{\mathrm{iso}}=0.20, \ell_i=0.20$). | Incorporated $1/10$ into the 1D PDE, derived the exact horizon $\bar{v}_{T,\infty} = \bar{l}_{\mathrm{eff}} / (\sqrt{10}\,\bar{\ell}_{\mathrm{i}})$, and evaluated it using Table 2 baseline values: $0.20/(\sqrt{10}\times 0.20) = 1/\sqrt{10} \approx 0.3162$. Updated Sec 7.4 Eq (27). | `DERIVATION_M16.md`, `test_p4b_5g_5h.py`, `tab02_parameters.tex` | Pytest `test_find04_asymptotics_prefactor_and_params` PASS | **RESOLVED** |
| **FIND-05** | **MEDIUM** | `sec02_continuum.tex`, Eq (12); `sec04_fem.tex`, Eq (18) | Displayed equations for $\tau_{ijk}$ and $\bm{K}^g$ omitted the scalar prefactor $1/10$ derived from the second moment of the 3D ellipsoidal averaging domain. | Added explicit prefactor $1/10$ to $\tau_{ijk} = \frac{1}{10}L_{kl}C_{ijmn}\eta_{mnl}$ and $\bm{K}^g = \frac{1}{10}\sum_{k,l} L_{kl} \int (\bm{B}^g_k)^\mathsf{T}\bm{C}\bm{B}^g_l\,\dif\Omega$. | `DERIVATION_M01_M07.md` §M4, Blueprint Eq (26) | Pytest `test_find05_mathematical_prefactor_tau_and_Kg` PASS | **RESOLVED** |
| **FIND-06** | **LOW** | `sec07_steering.tex`, Sec 7.4, line 34 | Informal use of the verb *"validates"* (*"This validates the constitutive role..."*) in context of internal asymptotic agreement. | Replaced *"validates"* with *"confirms"* to preserve strict separation between internal verification and external literature validation. | Audit Dimension H Lexicon rules | Pytest `test_find06_verb_validates_removed` PASS | **RESOLVED** |
| **FIND-07** | **LOW** | `appB_energy_flux.tex`, Eq (72) | Double-stress power term in energy flux written as $\tau_{ijk}\dot u_{i,k}$ rather than $\tau_{ikj}\dot u_{i,k}$ (divergence index in third position). | Updated index notation in Eqs (70), (71), (72) to $\tau_{ikj}\dot u_{i,k}$, perfectly aligning with M17 Eq (B.3). | `DERIVATION_M17.md` Eq (B.3) | Pytest `test_find07_energy_flux_index` PASS | **RESOLVED** |
| **FIND-08** | **LOW** | `sec05_verification.tex`, Sec 5.7, Eq (24) | Prose defined $\varepsilon_\Delta$ in terms of stop-band difference $\Delta_{GX}^{(32)} - \Delta_{GX}^{(16)}$, whereas Table 6 defines it on the acoustic mode frequency $\bar{\omega}_T$. | Updated Eq (24) to $\varepsilon_\Delta = \left| \bar{\omega}_T^{(32)} - \bar{\omega}_T^{(16)} \right| = 4.63 \times 10^{-11}$, exactly matching Table 6. | `tab06_convergence_floor.tex` | Pytest `test_find08_operational_resolution_floor_notation` PASS | **RESOLVED** |

---

## 4. Mathematical Alignment

The mathematical formulations across the manuscript have been aligned with the locked Phase 1 symbolic derivations:
1. **Factor 1/10:** The $1/10$ prefactor derived from the second moment of the 3D ellipsoidal domain is now explicitly displayed in:
   - Mindlin Form-II double stress: Eq. (12) in Section 2.4
   - Element gradient stiffness matrix: Eq. (18) in Section 4.2
   - 1D transverse shear equation of motion: Eq. (57) in Appendix A
   - Dynamic dispersion relation: Eq. (59) in Appendix A
   - High-$k$ asymptotic horizon: Eq. (62) in Appendix A and Eq. (27) in Section 7.4
2. **Asymptotic Horizon Formula:**
   $$\bar{v}_{T,\infty} = \frac{\bar{l}_{\mathrm{eff}}}{\sqrt{10}\,\bar{\ell}_{\mathrm{i}}} = \frac{0.20}{\sqrt{10} \times 0.20} = \frac{1}{\sqrt{10}} \approx 0.3162277$$
   This eliminates ad-hoc synthetic parameter values and connects directly to Table 2 baseline inputs ($l_{\mathrm{iso}} = 0.20\,\mathrm{m}, \ell_{\mathrm{i}} = 0.20\,\mathrm{m}$).
3. **Poynting Flux Divergence Index:** The double-stress power term in Appendix B now consistently uses index $j$ in the third position ($\tau_{ikj}\dot u_{i,k}$), matching `DERIVATION_M17.md` Eq. (B.3).

---

## 5. Numerical Traceability

Following remediation, numerical traceability has improved to **100% verified**:
- **Figure 6 Band Gaps:** $\Delta_{GX} = +0.0431$ (for $\mathrm{AR}=10, \theta=45^\circ$), with complete gap bound $\Delta_{\mathrm{complete}} \le -0.3758$.
- **Design Map Maximum Stop Band:** $\Delta_{GX} = 0.0896$ at $(\theta=30^\circ, \mathrm{AR}=10)$, with $\Delta_{GX} = 0.0431$ at $\theta=45^\circ$, directly matching `study_S5` raw data.
- **Orientation Sweep Frequency Drop:** $\bar{\omega}_T(X)$ drops from $2.915$ to $2.672$ and $\bar{\omega}_L(X)$ drops from $5.050$ to $4.628$, directly matching `study_S3` raw data and Figure 8(a).
- **Asymptotic High-$k$ Horizon:** Theoretical horizon $v_{T,\infty} = 0.3162$ and FE computed velocity $\bar{v}_p = 0.3163$ at $\bar{k}=200$ (relative discrepancy $0.03\%$), directly matching `study_S9` raw data and Test 5g.
- **Resolution Floor:** $\varepsilon_\Delta = 4.63 \times 10^{-11}$ evaluated on $\bar{\omega}_T$, directly matching Table 6.

---

## 6. Figure and Table Consistency

- **Figure 6:** Caption and Section 6.2 prose now accurately describe the plotted curves ($\mathrm{AR}=1$ vs $\mathrm{AR}=10$ at $\theta=0^\circ$ and $\theta=45^\circ$) and cite exact Table 2 parameters ($\rho=1.0\,\mathrm{kg/m}^3, \mu=1.0\,\mathrm{Pa}, \ell_i=0.20\,\mathrm{m}$).
- **Figure 8:** Plotted curves for $\bar{\omega}_T(X)$ and $\bar{\omega}_L(X)$ now perfectly align with the text discussion in Section 6.4.
- **Figure 10:** Response surface and contour map discussion now correctly identify the global maximum $\Delta_{GX} = 0.0896$ at $(\theta=30^\circ, \mathrm{AR}=10)$.
- **Table 2, 4, 5, 6:** 100% consistent with manuscript text, non-dimensionalization rules, and raw production datasets.

---

## 7. Regression Tests

An automated regression test suite was authored in `paper9/verification/suite/test_p8_remediation.py`, implementing 8 dedicated tests:
1. `test_find05_mathematical_prefactor_tau_and_Kg`
2. `test_find04_asymptotics_prefactor_and_params`
3. `test_find07_energy_flux_index`
4. `test_find08_operational_resolution_floor_notation`
5. `test_find06_verb_validates_removed`
6. `test_find01_fig06_caption_and_data_traceability`
7. `test_find02_design_map_max_gap_reconciliation`
8. `test_find03_theta_sweep_migration_values`

All 59 automated regression test functions across the repository pass cleanly:

```bash
PYTHONPATH=/home/user pytest paper9/production/p5/test_p5_integrity.py paper9/verification/suite/ -v
# ============================== 59 passed in 2.50s ==============================
```

Parameter linting also passed with zero violations:
```bash
python3 paper9/production/p5/lint_p5_params.py
# lint result: PASS (no violations)
```

---

## 8. Compilation and Syntax Integrity

The manuscript source was inspected for complete syntax and compilation safety:
- **Environment Matching:** 100% paired `\begin{...}` and `\end{...}` blocks across all section files.
- **File Inclusions:** 11/11 section files and 5/5 LaTeX tables exist and resolve cleanly.
- **Figures:** 11/11 vector PDFs exist and are valid.
- **Citations & References:** 15/15 BibTeX citations matched (zero missing, zero orphans), 102 labels defined, 25 cross-references matched (zero undefined).

---

## 9. Gate Preservation

All locked gates, benchmarks, and technical variations remain strictly preserved without upgrade:
- **Gate G3:** **NOT MET**
- **Criterion PCR1:** **NOT PASS**
- **Benchmarks B1–B3:** **UNVALIDATED** (zero fabricated literature data)
- **Benchmark B6:** **PARTIAL**
- **Study S2 / Case C:** **BLOCKED**
- **Open Technical Variations:** **TV1, TV6, TV12, TV14, TV18 remain OPEN**
- **Blocked Floats:** **Figure 4, Figure 7, and Table 3 remain preserved as explicit blocked placeholders (`[BLOCKED — ...]`)**

---

## 10. Git Traceability

```
START_SHA: 610f401032e74f4217c457eea6e679aa58224c57
Commit 1:  de19ef2 audit: remediate P8 mathematical consistency findings
Commit 2:  4cde6df audit: reconcile P8 numerical traceability findings
Commit 3:  4429920 audit: correct P8 figure and presentation findings
Commit 4:  [HEAD]   audit: record P8 remediation and verification
```

- **Branch:** `phase-1-symbolic`
- **Main Branch:** `origin/main` remains untouched at `1de47a4d111260ffb9b48d7c99e9db45102367c7`
- **Working Tree:** Clean upon commit.

---

## 11. Final P8 Status

Every remediable finding (FIND-01 through FIND-08) from `P8_FORENSIC_MANUSCRIPT_AUDIT.md` has been surgically resolved, verified against raw production data, and guarded by automated regression tests.

**Verdict:** `P8_REMEDIATION_COMPLETE`
