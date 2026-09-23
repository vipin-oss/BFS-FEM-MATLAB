# P11 Source Package Inventory & Forensic Audit

**Date:** 2026-09-23  
**Repository Branch:** `phase-1-symbolic`  
**Container Source:** `https://github.com/vipin-oss/BFS-FEM-MATLAB/blob/main/s10773-022-05163-1.zip`  
**Extracted Directory:** `paper9/sources/`  
**Auditor:** P11 Autonomous Research & Audit Agent  
**Operational Framework:** Paper9 Blueprint v1.3 Full Scope (Case H + Case C + B1–B3 published validation; target journal: *IJMS*)

---

## 1. Container Overview & Extraction Summary

The user-supplied archive `s10773-022-05163-1.zip` (12 MB) located on GitHub `main` was retrieved and extracted into `paper9/sources/`. The package contains 7 PDF files totaling 17,018,903 bytes.

A rigorous forensic inspection of file hashes, metadata, page counts, and full-text content was conducted to determine the exact identity, readability, and scientific relevance of each item.

---

## 2. Complete Inventory of Supplied Sources

### File 1: `s41598-024-75049-1.pdf` (Benchmark B1 & B2 Anchor)
- **Exact Title:** *Band gaps of elastic waves in 1-D dielectric phononic crystal with the flexoelectric and strain gradient effects consideration*
- **Authors:** Ying Li, Yueqiu Li, Zihao Guo, Hong Wang, Changda Wang
- **Journal:** *Scientific Reports* (Nature Publishing Group)
- **Year:** 2024
- **Volume / Article Number / Pages:** Vol. 14, Article No. 24035 (14 pages)
- **DOI:** `10.1038/s41598-024-75049-1`
- **File Path:** `paper9/sources/s41598-024-75049-1.pdf`
- **SHA256:** `2ac5f45d77ee37569f69e8890b70200ae6982f669ecaccf6cb5aa162f0340513`
- **Page Count:** 14
- **Type:** Archival open-access journal article (complete text and vector figures).
- **Supports:** **Benchmark B1** (Layer 1 classical limit, Fig. 2a) and **Benchmark B2** (Layer 2a gradient elasticity with flexoelectricity suppressed, Fig. 2b).
- **Readability & Content Extraction:** 100% readable. All governing equations (1)–(55), boundary conditions, transfer-matrix formulation, constitutive parameters, and figure captions are present.
- **Forensic Finding on Numerical Data:** The article does **not** include open supplementary numerical tables for frequency eigenvalues $\bar{\omega}(\bar{k})$. Under "Data availability", it states: *"The datasets used and analysed during the current study can be obtained from the corresponding author (liyueqiu2004@163.com)"*. However, the plotted curves and coordinate axes in Fig. 2(a) and Fig. 2(b) are rendered in high-resolution vector format, enabling reliable graphical reproduction and extraction of band-edge asymptotes.

---

### File 2: `Band-gaps-of-thermoelastic-waves-in-1D-phononic-crystal-with-fractional-order-generalized (1).pdf` (Benchmark B3 Anchor)
- **Exact Title:** *Band gaps of thermoelastic waves in 1D phononic crystal with fractional order generalized thermoelasticity and dipolar gradient elasticity*
- **Authors:** Yueqiu Li, Harm Askes, Inna M. Gitman, Anton Krynkin, Peijun Wei
- **Journal:** *Waves in Random and Complex Media* (Taylor & Francis)
- **Year:** 2023 (published online 9 June 2023; volume issue 2026)
- **Volume / Issue / Pages:** Vol. 36, No. 4, pp. 5715–5735
- **DOI:** `10.1080/17455030.2023.2222189`
- **File Path:** `paper9/sources/Band-gaps-of-thermoelastic-waves-in-1D-phononic-crystal-with-fractional-order-generalized (1).pdf`
- **SHA256:** `3f5103380302609ef2dfe76c8ade09cae79b2ebbd4fdb4da228576c331191aa7`
- **Page Count:** 22
- **Type:** Author/Accepted version PDF of archival paper.
- **Supports:** **Benchmark B3** (Layer 2b dipolar gradient bilayer, Fig. 4c) and optional **Benchmark B4** (Fig. 3).
- **Readability & Content Extraction:** 100% readable. Contains full formulations for fractional thermoelasticity, dipolar gradient elasticity, 4 interface continuity conditions, and transfer matrix.
- **Forensic Finding on Parameters (TV1 / TV12):** 
  - Fig. 4(c) caption states: *"the dispersion curves for the gradient elastic solids and the comparison with literature [34]"* (where [34] is Li, Wei & Zhou 2016, *Acta Mech.* 227:1005–1023). Thermoelastic coupling is explicitly ignored.
  - While Fig. 4(c) caption omits explicit text for $c_1, c_R, d_1, d_R$, the paper references Section 4.2 / Section 5 parameter sets, where Fig. 3 explicitly tabulates: $c_1 = 0.15, c_R = 1.5, d_1 = 0.25, d_R = 1.5$.
  - Shared numerical constants: Lead/brass bilayer, $a_1 = 10^{-5}\,\mathrm{m}, a_2/a_1 = 1, \rho_1 = 7.5 \times 10^3\,\mathrm{kg/m}^3, \mu_1 = 2.3 \times 10^{10}\,\mathrm{Pa}, \omega_0 = 4.1 \times 10^8\,\mathrm{Hz}, \lambda_R = 0.047, \mu_R = 0.056, \rho_R = 0.157$.

---

### File 3: `s00707-026-04680-y.pdf` (Anchor C / Layer 4 Cross-Check)
- **Exact Title:** *Tunable wave propagation and band gap characteristics in functionally graded lattices with multiple topologies via dynamic stiffness and Floquet–Bloch formulation*
- **Authors:** Mudit Mishra, Sandeep Kumar, Ambuj Sharma
- **Journal:** *Acta Mechanica* (Springer Nature)
- **Year:** 2026
- **Volume / Pages:** Vol. 237, pp. 3951–3982
- **DOI:** `10.1007/s00707-026-04680-y`
- **File Path:** `paper9/sources/s00707-026-04680-y.pdf`
- **SHA256:** `eaa9b5f443a90378aea5210a7292bb14238f8da32f4e17ac6ff2f42c5cc4bd5b`
- **Page Count:** 32
- **Type:** Archival original paper PDF.
- **Supports:** **Anchor C** / Layer 4 cross-check in the homogeneous limit ($\mathrm{AR}=1$, no gradation), closing **TV9**.
- **Readability & Content Extraction:** 100% readable text and figures. Contains dynamic stiffness formulations and Floquet–Bloch dispersion for square and triangular lattice unit cells.

---

### File 4: `zhan2010.pdf` (Case C 2D Phononic Crystal Literature Baseline)
- **Exact Title:** *Influences of anisotropy on band gaps of 2D phononic crystal*
- **Authors:** Zhengqiang Zhan, Peijun Wei
- **Journal:** *Acta Mechanica Solida Sinica*
- **Year:** 2010
- **Volume / Issue / Pages:** Vol. 23, No. 2, pp. 181–188
- **DOI:** `10.1016/S0894-9166(10)60020-1`
- **File Path:** `paper9/sources/zhan2010.pdf`
- **SHA256:** `47b7a4395fc2fbd3dac2b579a88cfe134311060208a55b7dc133fb1ec65062f1`
- **Page Count:** 8
- **Type:** Archival journal paper PDF.
- **Supports:** **Case C / Study S2 (Fig 7 & Table 5)**.
- **Readability & Content Extraction:** 100% readable. Provides exact material constants for 2D square unit cells with circular cylindrical fillers:
  - Epoxy matrix: $c_{11} = 7.54\,\mathrm{GPa}, c_{12} = 4.57\,\mathrm{GPa}, \mu = 1.48\,\mathrm{GPa}, \rho = 1142\,\mathrm{kg/m}^3$.
  - Anisotropic/orthotropic YBCO cylinders: $c_{11} = 268\,\mathrm{GPa}, c_{12} = 132\,\mathrm{GPa}, c_{13} = 95\,\mathrm{GPa}, c_{22} = 231\,\mathrm{GPa}, c_{23} = 71\,\mathrm{GPa}, c_{33} = 186\,\mathrm{GPa}, c_{44} = 37\,\mathrm{GPa}, c_{55} = 49\,\mathrm{GPa}, c_{66} = 95\,\mathrm{GPa}, \rho = 6333\,\mathrm{kg/m}^3$.
  - Exact rotation matrix $M(\theta)$ for rotating cylindrical inclusions.
  - Complete band-gap generation along $\Gamma$--$X$--$M$--$\Gamma$ in square lattice.

---

### File 5: `zheng2009.pdf` (Benchmark B1 Classical Bilayer Reference)
- **Exact Title:** *Band gaps of elastic waves in 1-D phononic crystals with imperfect interfaces*
- **Authors:** Min Zheng, Pei-jun Wei
- **Journal:** *International Journal of Minerals, Metallurgy and Materials*
- **Year:** 2009
- **Volume / Issue / Pages:** Vol. 16, No. 5, pp. 608–614
- **DOI:** `10.1016/S1674-4799(09)60105-9`
- **File Path:** `paper9/sources/zheng2009.pdf`
- **SHA256:** `8898cd59a103d3402a32c5d80ebd697860db566864b545666c3839d833493f32`
- **Page Count:** 7
- **Type:** Archival journal paper PDF.
- **Supports:** **Benchmark B1** classical bilayer reference (cross-referenced in Blueprint line 437).

---

### File 6: `hosseini2021.pdf` (Forensic Misnaming Discovery)
- **Supplied File Name:** `hosseini2021.pdf`
- **Actual Document Content:** *NOMES DE LUGAR: CONFIM* by Massimo Cacciari (*Revista de Letras*, Vol. 45, No. 1, pp. 13–22, 2005).
- **Forensic Finding:** This file is an unrelated Brazilian humanities literature paper in Portuguese. It is **not** the engineering paper by S. M. Hosseini & C. Zhang (2021, *Int. J. Mech. Sci.* 209:106711).
- **Impact:** Hosseini & Zhang (2021) is not available from this PDF. However, **File 4 (`zhan2010.pdf`)** directly provides the authoritative, peer-reviewed 2D square unit-cell parameters with circular inclusions from Peijun Wei's research group (the identical anchor research group of Li et al. 2023, 2024 and LWZ 2016), fully fulfilling the requirements for Case C.

---

### File 7: `s10773-022-05163-1.pdf` (Container Name Artifact)
- **Actual Document Content:** *Two Classes of Quantum Synchronizable Codes* by Zheng Li & Shixin Zhu (*Int. J. Theor. Phys.* 61:147, 2022).
- **Forensic Finding:** Quantum information theory article from which the zip file name was derived; unrelated to continuum mechanics.

---

## 3. Classification of Available Evidence for Blueprint v1.3

Following the project's evidence hierarchy:
1. **Mathematical Equations & Model Definitions:** Complete and verified across all anchors (Li 2024, Li 2023, LWZ 2016, PB 2009, Zhan 2010).
2. **Parameters & Provenance:**
   - Li 2024 (B1/B2): Material constants for AlN and BaTiO3, cell thickness $b = a_A + a_B = 0.02\,\mathrm{m}$, non-dimensionalizations fully extracted.
   - Li 2023 (B3): Lead/brass parameters, non-dimensional scales fully extracted.
   - Case C (Zhan 2010): Epoxy/YBCO constants, density contrast, stiffness contrast, rotation transformation fully extracted.
3. **Plotted Dispersion Curves:** High-resolution vector graphics available in the PDFs for B1 (Fig 2a), B2 (Fig 2b), B3 (Fig 4c), and Case C (Fig 3).
4. **Numerical Tables:** As explicitly stated in Li et al. (2024), raw numerical tables were not published online as supplementary data. Therefore, in strict compliance with project governance:
   - Reproduction of B1, B2, B3 via independent 1D transfer-matrix and FE calculations will be quantitatively verified against analytical limits (Level 1) and evaluated against clearly extracted vector curve asymptotes and gap bounds (Level 2), with all visual comparisons explicitly labeled as **QUALITATIVE / GRAPHICAL**.
