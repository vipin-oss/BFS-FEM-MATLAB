# Phase 3B Targeted Scientific Audit Report

**Author:** Arena.ai Builder (Independent Research Engine)  
**Date:** 2026-09-26  
**Document ID:** P10-AUDIT-3B-01  
**Audit Target Commit:** `a21d4d6faaff422ca75751ed5ee20a5e7bcee6fc`  
**Governing Baseline:** `RESEARCH_BLUEPRINT.md` (v1.2 `1ed2d54`), `PHASE3_PARAMETER_MATRIX.json` (`add1a8e`)  
**Hard Stop:** Manuscript writing is strictly paused. No governing equations modified.  

---

## Executive Summary & Audit Verdict

This document presents a rigorous, independent, and critical scientific audit of the Phase 3B production results and the claims published in `PHASE3B_PRODUCTION_REPORT.md`.

### Overall Audit Verdict: CONDITIONAL PASS

The underlying numerical data (17,747 modal records across 36 parameter cases in `paper10/production/results/`) are mathematically sound, fully reproducible, and physically valid. The generalized interface eigenvalue formulation ($A \mathbf{C} = \lambda B \mathbf{C}$) successfully eliminates transfer matrix exponential overflow and achieves machine-precision generalized eigenvalue residuals ($\le 4.89 \times 10^{-9}$ overall, and $\sim 10^{-15}$ for acoustic branches).

However, **four specific reporting, interpretation, and visual presentation issues** require formal qualification and correction prior to manuscript synthesis:
1. **Upper Frequency Boundary Truncation of Band Gaps (Section A):** 23 of the 64 reported band gap records terminate at $\Omega_U = 1.8000$, which is the artificial boundary of the computed frequency grid rather than a physical closed band edge.
2. **Condition Number Mislabeling (Section B):** The reported condition numbers $\kappa(P) \le 1.60 \times 10^{15}$ and $2.68 \times 10^{20}$ are the *unscaled dimensional SI* condition numbers ($\kappa(P_{\text{raw}})$) caused by a 1-character index unpacking mismatch in the production runner. The true equilibrated condition number is strictly bounded between **$1.35$ and $22.72$** (and up to $4.65 \times 10^3$ in the classical limit).
3. **Qualification of "0 Questionable Calculations" (Section C):** In the classical limit case (`S3_classical`), 223 evanescent boundary layer modes were legitimately filtered out due to extreme underflow ($|\lambda| < 10^{-15}$). This is physically expected as gradient length scales $c, d \to 0$, but must be explicitly documented rather than claiming zero filtered points.
4. **Single-Branch Selection in Line Figures (Section H):** In Figures 2, 4, 6, 7, and 10, the plotting script filtered on `branch_id == 0`, which in certain cases selected an evanescent gradient mode ($k_r a = 0$) rather than the propagating acoustic branch ($k_r a > 0$). While all multi-branch scatter plots (Figures 1, 3, 5, 8) correctly plot all modes, the single-line figures must be updated to track the acoustic mode specifically.

---

## Detailed Audit Findings by Section

### Section A: Audit of Reported Band Gaps (Issue A)
**Classification:** **QUALIFY / CORRECT**

#### 1. Audit Finding
In `PRODUCTION_BANDGAP_SUMMARY.csv`, 23 out of the 64 gap records list `Omega_U = 1.8000`. For example, for the baseline active DPL case (`S1_dpl`), Gap 2 is reported as:
$$
\Omega \in [1.3051, 1.8000], \qquad \Delta\Omega = 0.4949, \qquad \frac{\Delta\Omega}{\Omega_c} = 0.3188
$$
An inspection of the production script (`run_phase3b_production.py`, lines 212–225) reveals that if a band gap is active at the final frequency point of the sweep, the upper edge was set to:
$$
\Omega_U = \Omega_{\max} = 1.8000
$$
and $\Delta\Omega = 1.8000 - \Omega_L$.

#### 2. Physical Verdict
$\Omega = 1.8000$ is **NOT** a physical upper band edge where the optical branch re-enters the Brillouin zone. The band gap simply **remains open** at the upper limit of the investigated frequency window ($\Omega > 1.80$). 

#### 3. Required Correction
In all tables, texts, and summary figures:
- Any band gap terminating at $\Omega = 1.8000$ must be reported as:
  $$\Omega \ge \Omega_L \quad (\text{remains open beyond investigated window } \Omega = 1.80)$$
- Numerical gap widths $\Delta\Omega$ and gap-to-midgap ratios $\Delta\Omega/\Omega_c$ must **not** be reported as closed physical quantities for boundary-truncated gaps.
- The 23 truncated gap records in `PRODUCTION_BANDGAP_SUMMARY.csv` must be explicitly flagged with `is_boundary_truncated = True`.

---

### Section B: Audit of Numerical Conditioning Claims (Issue B)
**Classification:** **CORRECT / QUALIFY**

#### 1. Audit Finding
The report stated:
- Conservative limit: $\kappa(P_{\text{equil}}) \le 1.60 \times 10^{15}$
- Active DPL: $\kappa(P_{\text{equil}}) \le 2.68 \times 10^{20}$

These values contradicted the Phase 3A pilot values ($\kappa(P_{\text{equil}}) \approx 9.40$ to $22.7$).

#### 2. Root Cause Analysis
In `paper10/solver/coupled10.py` line 187, the function signature is:
```python
return P, cond_P_raw, cond_P_equil
```
In `paper10/production/run_phase3b_production.py` line 43:
```python
PA, cond_PA, _ = solverA.compute_modal_matrix(omega)
```
The variable `cond_PA` captured the **second** returned argument (`cond_P_raw`), discarding `cond_P_equil` into `_`! The unscaled raw condition number was then recorded under the CSV column header `"cond_P_equil"`.

#### 3. Mathematical & Numerical Verification
Evaluating the true equilibrated modal matrix $P_{\text{equil}} = D_{\text{row}}^{-1} P D_{\text{col}}^{-1}$ across all production cases demonstrates:
- Conservative baseline (`S1_cons`): $\kappa(P_{\text{equil}}) \in [1.35, 22.72]$
- Active DPL baseline (`S1_dpl`): $\kappa(P_{\text{equil}}) \in [2.55, 9.39]$
- Extended relaxation lag (`S5_tauq_1ns`): $\kappa(P_{\text{equil}}) \in [2.55, 9.39]$
- Strong thermoelastic coupling (`S6_alpha20`): $\kappa(P_{\text{equil}}) \in [2.56, 9.39]$
- Classical elastic limit (`S3_classical`): $\kappa(P_{\text{equil}}) \in [129.15, 4648.99]$

Furthermore, the relative residual of the generalized interface eigenvalue problem:
$$
\text{Res} = \frac{\|\mathbf{A} \mathbf{c} - \lambda \mathbf{B} \mathbf{c}\|}{\|\mathbf{A}\| \|\mathbf{c}\| + |\lambda| \|\mathbf{B}\| \|\mathbf{c}\|}
$$
is strictly bounded by **$4.89 \times 10^{-9}$** across all modes, and achieves **$7.34 \times 10^{-16} - 3.84 \times 10^{-15}$ (machine precision)** for all propagating acoustic modes!

#### 4. Audit Table (Excerpts from `paper10/audit/PHASE3B_TARGETED_SCIENTIFIC_AUDIT.csv`)

| Case ID | $\Omega$ | $\kappa(P_{\text{raw}})$ | $\kappa(P_{\text{equil}})$ | $\kappa(T_{\text{cell}})$ | Max Relative Residual | Finite? | Physical Result Affected? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `S1_cons` | $0.05$ | $1.89 \times 10^{12}$ | **$22.72$** | $4.53 \times 10^{16}$ | $1.66 \times 10^{-14}$ | True | False |
| `S1_cons` | $0.50$ | $1.23 \times 10^{14}$ | **$2.46$** | $9.21 \times 10^{15}$ | $6.81 \times 10^{-15}$ | True | False |
| `S1_cons` | $1.00$ | $4.94 \times 10^{14}$ | **$1.35$** | $2.86 \times 10^{16}$ | $6.06 \times 10^{-15}$ | True | False |
| `S1_cons` | $1.80$ | $1.60 \times 10^{15}$ | **$1.73$** | $2.79 \times 10^{16}$ | $1.90 \times 10^{-14}$ | True | False |
| `S1_dpl` | $0.05$ | $4.07 \times 10^{15}$ | **$9.39$** | $7.99 \times 10^{16}$ | $3.99 \times 10^{-09}$ | True | False |
| `S1_dpl` | $0.50$ | $3.50 \times 10^{18}$ | **$2.81$** | $5.54 \times 10^{16}$ | $3.18 \times 10^{-11}$ | True | False |
| `S1_dpl` | $1.00$ | $2.21 \times 10^{19}$ | **$2.61$** | $1.66 \times 10^{17}$ | $7.05 \times 10^{-11}$ | True | False |
| `S1_dpl` | $1.80$ | $6.94 \times 10^{19}$ | **$2.55$** | $9.71 \times 10^{16}$ | $1.51 \times 10^{-12}$ | True | False |
| `S3_classical` | $0.05$ | $4.57 \times 10^{17}$ | **$4648.99$** | $1.89 \times 10^{17}$ | $2.11 \times 10^{-11}$ | True | False |
| `S3_classical` | $1.00$ | $7.15 \times 10^{17}$ | **$232.45$** | $1.39 \times 10^{17}$ | $8.31 \times 10^{-16}$ | True | False |
| `S3_classical` | $1.80$ | $2.55 \times 10^{18}$ | **$129.15$** | $6.01 \times 10^{16}$ | $1.96 \times 10^{-15}$ | True | False |
| `S5_tauq_1ns` | $1.00$ | $3.74 \times 10^{18}$ | **$2.61$** | $1.51 \times 10^{17}$ | $7.10 \times 10^{-11}$ | True | False |
| `S6_alpha20` | $1.00$ | $6.49 \times 10^{19}$ | **$2.59$** | $9.24 \times 10^{16}$ | $3.49 \times 10^{-10}$ | True | False |

---

### Section C: Audit of "0 Questionable Calculations" Claim (Issue C)
**Classification:** **QUALIFY**

#### 1. Audit Finding
The report stated:
> "Numerically questionable calculations: 0"

#### 2. Reassessment
1. **Classical Limit Filtering (`S3_classical`):**
   In Case `S3_classical`, 277 modes were stored instead of 500 (5 forward modes $\times$ 100 frequencies). The remaining 223 modes had Floquet multipliers $|\lambda| < 10^{-15}$ and were legitimately excluded by the safety threshold `abs(ev) > 1e-15`.
   *Physics:* As gradient length scales $c, d \to 0$, boundary layer thickness $\delta \sim \sqrt{c} \to 0$. Wavenumbers scale as $k \sim 10^5\text{ m}^{-1}$, producing spatial decay factors $\exp(-k a_j) < 10^{-200}$. These modes physically vanish from the transmission spectrum. This is not a numerical error, but it must be formally acknowledged as a truncation of infinitesimal boundary layers.
2. **Attenuation Numerical Floor:**
   In conservative cases, extracted pass-band attenuation is $\alpha a \approx 1.67 \times 10^{-5}$ rather than analytical zero ($0.0$). This floor is governed by the numerical conditioning of `scipy.linalg.eig` on the $20 \times 20$ generalized matrix pencil. It is numerically acceptable, but must be documented as the numerical noise floor of the eigensolver.

---

### Section D: Audit of Attenuation Interpretation (Issue D)
**Classification:** **PASS / QUALIFY**

#### 1. Verification of Three Separate Mechanisms
The audit confirms that the three wave attenuation and dispersion mechanisms are physically distinct:
1. **Bragg Stop Bands:** Arise solely from destructive spatial interference at periodic interfaces where $Z_A \ne Z_B$. Produces strong geometric evanescence ($\alpha a \sim 4.5 - 5.5$).
2. **Dipolar Gradient Elasticity:** Dispersive, conservative higher-order continuum mechanism altering wave phase velocity and branch curvature.
3. **DPL Thermoelastic Dissipation:** Irreversible entropy generation from thermal conduction with dual relaxation lags $\tau_q, \tau_\theta$. Produces complex Bloch wavenumbers ($k_i \ne 0$) and a finite attenuation floor across all propagating bands ($\alpha a \sim 2.2 \times 10^{-4} - 2.8 \times 10^{-2}$).

#### 2. Convention Verification
- Signed imaginary wavenumber $k_i a$ and absolute spatial attenuation magnitude $\alpha a = |k_i a|$ strictly follow the Phase-2 sign convention ($e^{i(k_r + i k_i)x} = e^{-k_i x} e^{i k_r x}$).
- Conservative symplecticity $\det(T) \equiv 1$ is never claimed for the dissipative 10-state DPL system.

---

### Section E: Audit of Gradient-Length Conclusions (Issue E)
**Classification:** **PASS (Physics) / QUALIFY (Visual Presentation)**

#### 1. Dispersive Softening vs Stiffening
The claim that:
- Micro-inertia $d_1/a$ induces **dispersive softening** (lowering high-frequency phase velocity and gap onsets), and
- Micro-stiffness $\sqrt{c_1}/a$ induces **dispersive stiffening** (raising high-frequency phase velocity and shifting gaps upward),
is **100% verified by the underlying multi-branch numerical data** in `S3_results.csv`:
- Low inertia ($d_1/a = 0.1$): Gap 1 opens at $\Omega_L = 0.7040$
- High inertia ($d_1/a = 1.0$): Gap 1 shifts downward to $\Omega_L = 0.4035$
- Low stiffness ($\sqrt{c_1}/a = 0.1$): Gap 1 opens at $\Omega_L = 0.2444$
- High stiffness ($\sqrt{c_1}/a = 0.8$): Gap 1 shifts upward to $\Omega_L = 0.8101$

#### 2. Visual Presentation Caveat (Figure 4)
In Figure 4, filtering on `branch_id == 0` inadvertently selected the evanescent gradient mode for `S3_d01` and `S3_c01`. This visual presentation defect must be corrected prior to manuscript synthesis by plotting the tracked propagating acoustic branch.

---

### Section F: Audit of the Identical-Layer Claim (Issue F)
**Classification:** **QUALIFY**

#### 1. Audit Finding
The report stated:
> "Complete gap suppression for identical layers."

#### 2. Necessary Qualification
In Case `S2_chi00` ($A = B$), material impedance contrast is identically zero ($Z_B/Z_A = 1.0$). Therefore, **material-contrast-induced Bragg band gaps disappear completely ($\Delta\Omega = 0.0000$)**. 

However, intrinsic gradient-elastic dispersion remains active throughout the homogeneous medium. The statement must be qualified to clarify that Bragg scattering is suppressed, not intrinsic gradient dispersion.

---

### Section G: Audit of Thermoelastic/DPL Physical Interpretation (Issue G)
**Classification:** **QUALIFY**

#### 1. Audit Finding
The report stated:
> "All findings obey continuum thermodynamics and phononic crystal wave mechanics."

#### 2. Necessary Qualification
Broad philosophical statements asserting thermodynamic proof must be replaced with precise statements reflecting the mathematical model:
- The DPL thermal model introduces a non-zero complex wavenumber whose imaginary part $\alpha = |k_i|$ is strictly non-negative for forward-propagating modes, consistent with positive entropy production.
- Thermal relaxation $\tau_q$ and retardation $\tau_\theta$ modulate the effective thermal conductivity $k_{\text{eff}}(\omega) = k_0 \frac{1 + i\omega\tau_\theta}{1 + i\omega\tau_q}$, transforming the sharp band-edge cusps of conservative systems into continuous, finite-attenuation transition zones.

---

### Section H: Audit of the 10 Publication Figures (Issue H)
**Classification:** **QUALIFY / CORRECT**

| Figure | Description | Audit Status | Specific Scientific Finding & Action Required |
| :---: | :--- | :---: | :--- |
| **Fig 1** | Baseline Bloch Dispersion | **PASS** | Scatter plot displays all 5 forward branches correctly; Bragg gap at $[0.67, 0.70]$ clearly resolved. |
| **Fig 2** | Baseline Attenuation | **CORRECT** | Filtered on `branch_id == 0`, which captured an evanescent mode ($\alpha a \sim 1.4$) in `S1_dpl`. Must be updated to plot the acoustic branch ($\alpha a \sim 2.2 \times 10^{-4}$). |
| **Fig 3** | Material Contrast Sweep | **PASS** | Scatter plot correctly displays gap opening from $\chi=0.0$ to $\chi=1.0$. |
| **Fig 4** | Gradient Length Scales | **CORRECT** | Filtered on `branch_id == 0`, plotting a flat vertical line at $k_r a/\pi = 0$ for `S3_d01`. Must be updated to plot the acoustic branch. |
| **Fig 5** | Filling Fraction Sweep | **PASS** | Scatter plot correctly displays geometric band-edge shifts across $\eta = 0.2, 0.5, 0.8$. |
| **Fig 6** | DPL Thermal Lags | **CORRECT** | Filtered on `branch_id == 0`, plotting evanescent modes ($\alpha a \sim 2 - 3.5$). Must be updated to plot the acoustic branch attenuation. |
| **Fig 7** | Thermoelastic Coupling | **CORRECT** | Line filtering on `branch_id == 0` must be replaced with acoustic branch filtering. |
| **Fig 8** | Combined Interaction | **PASS** | 6-panel factorial scatter plot displays complete band structures clearly and accurately. |
| **Fig 9** | Band-Gap Width Summary | **QUALIFY** | Subplots must add an explicit note/marker indicating that Gap 2 is truncated by the upper frequency boundary $\Omega = 1.80$. |
| **Fig 10** | Synthesis Map | **CORRECT** | Line filtering on `branch_id == 0` must be replaced with the propagating acoustic branch for all three mechanism curves. |

---

### Section I: Audit of Production Reproducibility (Issue I)
**Classification:** **PASS**

All numerical counts and metadata are 100% verified:
- 36 unique parameter cases across 7 sweep families.
- 100 uniformly spaced frequency points per case ($\Omega \in [0.05, 1.80]$).
- 17,747 modal records in CSV and JSON datasets (`paper10/production/results/`).
- 64 band gap records in `PRODUCTION_BANDGAP_SUMMARY.csv`.
- 36 attenuation records in `PRODUCTION_ATTENUATION_SUMMARY.csv`.
- Master metadata recorded in `PRODUCTION_METRIC_MANIFEST.json`.

---

## Required Concrete Actions Prior to Manuscript Synthesis

To advance from **CONDITIONAL PASS** to unconditional manuscript readiness, the following modular action items must be completed:

1. **Band-Gap Summary Qualification (`PRODUCTION_BANDGAP_SUMMARY.csv`):**
   Add a boolean column `is_boundary_truncated` to flag the 23 records where $\Omega_U = 1.8000$, and annotate them as open band gaps rather than closed physical band gaps.
2. **Production Report Calibration (`PHASE3B_PRODUCTION_REPORT.md`):**
   - Correct the condition number text to state that $\kappa(P_{\text{equil}})$ is between **$1.35$ and $22.72$** (and up to $4.65 \times 10^3$ in the classical limit), while $10^{15} - 10^{20}$ represents the unscaled SI raw condition number.
   - Clarify that in `S3_classical`, 223 evanescent boundary layer modes were legitimately filtered due to infinitesimal boundary layer decay ($|\lambda| < 10^{-15}$).
   - Qualify the identical-layer statement to distinguish Bragg gap suppression from intrinsic gradient dispersion.
   - Remove unproven thermodynamic generalizations.
3. **Line-Plot Figure Branch Filtering Calibration (Figures 2, 4, 6, 7, 10):**
   Update the plotting routines in `run_phase3b_production.py` to identify the propagating acoustic mode by tracking the mode with $k_r a / \pi > 0$ and lowest attenuation, rather than assuming `branch_id == 0`.
4. **Band-Gap Summary Figure (Figure 9):**
   Add an explicit dashed boundary annotation on Figure 9 indicating that Gap 2 remains open beyond the computed frequency ceiling $\Omega = 1.80$.

---

## Audit Sign-Off

**PHASE 3B SCIENTIFIC AUDIT STATUS:** **CONDITIONAL PASS**  
The underlying production dataset is verified, numerically stable, and physically sound. The required qualifications and figure filtering calibrations are strictly documented and isolated.

**HARD STOP:** Manuscript synthesis is paused awaiting user review and approval of this scientific audit.
