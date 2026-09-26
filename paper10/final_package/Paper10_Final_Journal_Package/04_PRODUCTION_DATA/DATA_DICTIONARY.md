# Data Dictionary — Paper 10 Production Datasets

**Manuscript:** Dual-Phase-Lag (DPL) Thermoelastic Band-Gap Tuning and Acoustic Dissipation in 1D Periodic Metamaterials with Dipolar Gradient Elasticity  
**Dataset Location:** `04_PRODUCTION_DATA/`  
**Total Cases:** 36 parameter cases across 7 sweep families (S1–S7)  
**Frequency Sampling:** 100 uniformly spaced points across $\Omega \in [0.05, 1.80]$ ($\Delta\Omega = 0.01768$)  
**Total Modal Records:** 17,747 records  

---

## 1. Dataset Overview

| File Name | Sweep Family & Focus | Cases Included | Records | Primary Sweep Parameter(s) |
| :--- | :--- | :---: | :---: | :--- |
| `S1_results.csv` | Baseline Dispersion & DPL | 2 | 1,000 | Conservative ($\beta \to 0$) vs Active DPL Baseline |
| `S2_results.csv` | Material Contrast | 6 | 2,985 | Contrast parameter $\chi \in \{0.0, 0.5, 1.0\}$ |
| `S3_results.csv` | Gradient Length Scales | 7 | 3,275 | Micro-inertia $d_1/a$, micro-stiffness $\sqrt{c_1}/a$, classical limit ($c,d\to 0$) |
| `S4_results.csv` | Geometric Asymmetry | 6 | 3,000 | Layer A filling fraction $\eta = a_1/a \in \{0.2, 0.5, 0.8\}$ |
| `S5_results.csv` | Non-Fourier Thermal Lags | 5 | 2,500 | Relaxation lag $\tau_q \in [1\text{ ps}, 1\text{ ns}]$, retardation lag $\tau_\theta \in [0.1\text{ ps}, 100\text{ ps}]$ |
| `S6_results.csv` | Thermoelastic Coupling | 4 | 2,000 | Coupling scaling $\alpha_t / \alpha_{t,\text{base}} \in \{0.0, 0.5, 1.0, 2.0\}$ |
| `S7_results.csv` | Combined Factorial Interactions | 6 | 2,987 | Factorial pairings of Bragg, gradient, and DPL mechanisms |
| `PRODUCTION_BANDGAP_SUMMARY.csv` | Extracted Bragg Stop Bands | 36 | 64 | Authoritative lower/upper gap edges, widths, and truncation flags |
| `PRODUCTION_ATTENUATION_SUMMARY.csv`| Pass/Stop Band Attenuation | 36 | 36 | Min, mean, max pass-band attenuation and peak stop-band attenuation |
| `PRODUCTION_METRIC_MANIFEST.json` | Master Campaign Manifest | 36 | --- | Runtime, hardware, environment, and numerical health metrics |
| `PHASE3_PARAMETER_MATRIX.json` | Parameter Specifications | 36 | --- | Master locked parameter configurations |

---

## 2. Record Field Definitions (`S1_results.csv` through `S7_results.csv`)

Each row in the family result CSVs represents one forward-propagating or evanescent mode at a discrete frequency $\Omega$:

| Column Header | Data Type | Physical Meaning | Physical Units | Valid Range / Interpretation |
| :--- | :---: | :--- | :---: | :--- |
| `family_id` | String | Sweep family identifier | --- | `S1` to `S7` |
| `case_id` | String | Unique parameter case identifier | --- | e.g., `S1_cons`, `S1_dpl`, `S3_classical` |
| `case_name` | String | Descriptive case name | --- | e.g., `Active DPL Thermoelastic Baseline` |
| `freq_index` | Integer | Frequency grid index | --- | `0` to `99` |
| `Omega` | Float | Normalized frequency | Dimensionless | $\Omega = \omega a / (2\pi v_m) \in [0.05, 1.80]$ |
| `omega_rad_s` | Float | Circular frequency | $\text{rad/s}$ | $\omega = 2\pi v_m \Omega / a \approx 2.72 \times 10^4$ to $9.79 \times 10^5\text{ rad/s}$ |
| `branch_id` | Integer | Hungarian branch tracking index | --- | `0` to `4` (5 forward modes extracted from 10-state pencil) |
| `lambda_real` | Float | Real part of Bloch multiplier $\lambda$ | Dimensionless | $\lambda = e^{i k_x a}$ |
| `lambda_imag` | Float | Imaginary part of Bloch multiplier $\lambda$| Dimensionless | $\lambda = e^{i k_x a}$ |
| `kr_a_over_pi`| Float | Real normalized Bloch wavenumber | Dimensionless | $k_r a / \pi \in [0.0, 1.0]$ (First Brillouin zone) |
| `ki_a` | Float | Signed imaginary Bloch wavenumber | Dimensionless | Negative for forward spatial decay |
| `alpha_a` | Float | Spatial attenuation magnitude | Dimensionless | $\alpha a = \|k_i a\| \ge 0.0$ |
| `phase_vel_m_s`| Float | Acoustic phase velocity | $\text{m/s}$ | $v_p = \omega / k_r$ |
| `is_pass_band`| Boolean | Automated pass-band flag | --- | `True` if $\alpha a < 0.1$ and $k_r a / \pi > 0.001$; `False` otherwise |
| `cond_P_raw` | Float | Modal matrix condition number | Dimensionless | Evaluated via canonical two-sided equilibration ($\kappa \le 22.72$ baseline) |

---

## 3. Band-Gap Summary Table (`PRODUCTION_BANDGAP_SUMMARY.csv`)

| Column Header | Data Type | Physical Meaning | Interpretation |
| :--- | :---: | :--- | :--- |
| `case_id` | String | Parameter case ID | Maps to simulation sweep |
| `case_name` | String | Descriptive name | Maps to production matrix |
| `gap_index` | Integer | Gap sequential index | `1`, `2`, `3`, etc. within case |
| `Omega_L` | Float | Lower band-gap edge frequency | Onset of stop band |
| `Omega_U` | Float | Upper band-gap edge frequency | Termination of stop band |
| `delta_Omega` | Float | Band-gap frequency width | $\Delta\Omega = \Omega_U - \Omega_L$ |
| `Omega_mid` | Float | Mid-gap central frequency | $\Omega_c = (\Omega_L + \Omega_U)/2$ |
| `gap_to_midgap_ratio` | Float | Relative gap width ratio | $\Delta\Omega / \Omega_c$ |
| `is_boundary_truncated`| Boolean | Boundary truncation flag | **Crucial:** `True` indicates the stop band remains **open** at the frequency ceiling $\Omega = 1.8000$, with its upper physical edge lying outside the investigated window. Exactly 23 records are flagged `True`. `False` indicates a fully closed internal stop band. |

---

## 4. Attenuation Summary Table (`PRODUCTION_ATTENUATION_SUMMARY.csv`)

| Column Header | Data Type | Physical Meaning | Interpretation |
| :--- | :---: | :--- | :--- |
| `case_id` | String | Parameter case ID | Maps to simulation sweep |
| `case_name` | String | Descriptive name | Maps to production matrix |
| `pass_alpha_min` | Float | Minimum pass-band attenuation | Governed by eigensolver numerical noise floor in conservative limit ($\sim 10^{-9}$) |
| `pass_alpha_mean`| Float | Mean pass-band attenuation | Average dissipation across modes satisfying `is_pass_band == True` |
| `pass_alpha_max` | Float | Maximum pass-band attenuation | Peak dissipation near band edges |
| `stop_alpha_peak`| Float | Peak stop-band attenuation | Maximum geometric evanescence inside Bragg gaps ($\alpha a \approx 4.915$) |

---

## 5. Critical Physical Distinctions Preserved in Data

1. **Bragg Stop Bands vs. DPL Dissipation:**
   In conservative cases (`S1_cons`), $\alpha a \approx 1.67 \times 10^{-5}$ across pass bands and surges to $4.915$ inside Bragg gaps (pure geometric reflection). In active DPL cases (`S1_dpl`), thermoelastic entropy generation establishes a non-zero attenuation baseline ($\alpha a_{\text{mean}} = 2.21 \times 10^{-4}$) across all propagating frequencies.
2. **Open Boundary Gaps:**
   All 23 records terminating at $\Omega_U = 1.8000$ (e.g., `S1_dpl` Gap 2, $\Omega_L = 1.3051$) are explicitly designated with `is_boundary_truncated = True`. They are **open attenuation bands**, not closed physical band gaps.
3. **Identical Layers Limit:**
   In case `S2_chi00_dpl` ($\chi = 0$), acoustic impedance mismatch is zero, yielding $\Delta\Omega \equiv 0.0000$ (no Bragg gaps). Intrinsic dipolar gradient dispersion and thermal attenuation remain active throughout the homogeneous medium.
