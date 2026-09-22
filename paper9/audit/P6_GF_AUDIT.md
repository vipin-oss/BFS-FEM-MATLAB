# Gate G-F Float Audit Record (Phase 6)

**Date of Audit:** 2026-09-22  
**Branch:** `phase-1-symbolic`  
**Base Commit:** `b9c0b17571ca95e14241bd3a43cf85e414b79a55`  
**Gate:** **G-F (Figure and Table Generation Audit)**  
**Gate Status:** **PARTIAL** (16/19 floats fully generated, verified, and locked; 3/19 floats legitimately blocked).

---

## 1. Executive Gate Decision

* **Permissible Floats Generated:** 11 figures (Figs 1, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13) and 5 tables (Tabs 1, 2, 4, 5-CaseH, 6) = **16 floats generated**.
* **Blocked Floats (Not Fabricated):**
  - **Fig 4 (Anchor overlays):** **BLOCKED** (Gate G3 = NOT MET, PCR1 = NOT PASS).
  - **Table 3 (Anchor error table):** **BLOCKED** (Gate G3 = NOT MET, PCR1 = NOT PASS).
  - **Fig 7 (Case C bands and modes):** **BLOCKED** (TV6 Case C, TV14, TV18 unresolved; Study S2 unrun).
* **Gate Verdict:** **G-F = PARTIAL**. In accordance with the project's strict non-fabrication policy, blocked floats are documented rather than faked. Full Gate G-F PASS cannot be awarded until G3 and Case C are resolved.

---

## 2. Float Traceability Matrix

Every generated float traces unambiguously to a version-controlled generator script, an immutable data source, a parameter hash, and a verification test.

### Figures (Vector PDF in `paper9/figures/out/`)

| Float | Title / Content | Generator Script | Primary Data Source | Param / Data Hash (prefix) | Relevant Phase / Study | Status |
|---|---|---|---|---|---|---|
| **Fig 1** | Microstructural ellipsoid & $\mathbf{L}(\theta)$ | `paper9/figures/gen/fig01_ellipsoid_tensor.py` | `params_master.yaml` | `5bf229bdaebf` | P1 (M1, M2) | **LOCKED** |
| **Fig 2** | Periodic lattice, BZ & IBZ path | `paper9/figures/gen/fig02_lattice_ibz.py` | `params_master.yaml` | `5bf229bdaebf` | P1 (M10, M10a) | **LOCKED** |
| **Fig 3** | BFS 32-DOF layout & Bloch phases | `paper9/figures/gen/fig03_bfs_dof_bloch.py` | Analytical specification | n/a | P1 (M9, M13) | **LOCKED** |
| **Fig 4** | Anchor comparison overlays | — | B1–B3 published curves | — | P3 (B1–B3) | **BLOCKED** (G3) |
| **Fig 5** | Mesh convergence & floor $\varepsilon_\Delta$ | `paper9/figures/gen/fig05_mesh_convergence.py` | `p4b_5g_to_5i.json` | `383843632e31` | P4B (Test 5i) | **LOCKED** |
| **Fig 6** | Case H bands along $\Gamma-X-M-\Gamma$ | `paper9/figures/gen/fig06_caseH_dispersion.py` | `p5_production_raw.json` | `0af7445a4c5e` | P5 (Study S1) | **LOCKED** |
| **Fig 7** | Case C baseline bands & modes | — | Study S2 | — | P5 (Study S2) | **BLOCKED** (Case C) |
| **Fig 8** | Orientation sweep $\theta \in [0, 90^\circ]$ | `paper9/figures/gen/fig08_theta_sweep.py` | `p5_production_raw.json` | `0af7445a4c5e` | P5 (Study S3) | **LOCKED** |
| **Fig 9** | Aspect-ratio sweep $\mathrm{AR} \in [1, 10]$ | `paper9/figures/gen/fig09_ar_sweep.py` | `p5_production_raw.json` | `0af7445a4c5e` | P5 (Study S4) | **LOCKED** |
| **Fig 10** | 3D design map $\Delta_{GX}(\theta, \mathrm{AR})$ | `paper9/figures/gen/fig10_design_map_3d.py` | `p5_production_raw.json` | `0af7445a4c5e` | P5 (Study S5) | **LOCKED** |
| **Fig 11** | Polar design map & sensitivity $S_\theta$ | `paper9/figures/gen/fig11_polar_map_regimes.py` | `p5_production_raw.json` | `0af7445a4c5e` | P5 (Study S6) | **LOCKED** |
| **Fig 12** | Iso-frequency contours & wave steering | `paper9/figures/gen/fig12_ifc_wave_steering.py` | `p5_production_raw.json` | `0af7445a4c5e` | P5 (Study S7) | **LOCKED** |
| **Fig 13** | Energy partition & micro-inertia speed | `paper9/figures/gen/fig13_energy_microinertia.py` | `p5_production_raw.json` | `0af7445a4c5e` | P5 (Study S8, S9) | **LOCKED** |

---

### Tables (LaTeX Fragments in `paper9/tables/out/`)

| Float | Title / Content | Generator Script | Primary Data Source | Param / Data Hash (prefix) | Relevant Phase / Study | Status |
|---|---|---|---|---|---|---|
| **Table 1** | Literature positioning table | `paper9/tables/gen/tab01_literature_positioning.py` | Blueprint §1.4 | n/a | P0 / Blueprint | **LOCKED** |
| **Table 2** | Parameter registry with tags | `paper9/tables/gen/tab02_parameters.py` | `params_master.yaml` | `5bf229bdaebf` | P0 / P4A / P5 | **LOCKED** |
| **Table 3** | Anchor error table | — | P3 validation results | — | P3 (B1–B3) | **BLOCKED** (G3) |
| **Table 4** | Eight-test internal consistency suite | `paper9/tables/gen/tab04_consistency_suite.py` | `p4b_5g_to_5i.json` | `383843632e31` | P4A / P4B (5a–5h) | **LOCKED** |
| **Table 5** | Gap summary & $S_\theta$ (Case H) | `paper9/tables/gen/tab05_gap_summary.py` | `table5_gap_summary.json` | `f0e1c2001fab` | P5 (S2/S6/S7) | **LOCKED [Case H]** |
| **Table 6** | Convergence rate & resolution floor | `paper9/tables/gen/tab06_convergence_floor.py` | `p4b_5g_to_5i.json` | `383843632e31` | P4B (Test 5i) | **LOCKED** |

---

## 3. Style and Quality Control (QC) Audit

Every generated file was checked against the locked style guidelines:
1. **Vector Output:** All figures are emitted as PDF vector files (`paper9/figures/out/*.pdf`). Zero raster screenshots.
2. **Typography & Legibility:** Font sizes strictly satisfy the journal minimum ($\ge 8\,\mathrm{pt}$; labels at $10\,\mathrm{pt}$, tick labels and legends at $8\,\mathrm{pt}$).
3. **Axis Conventions:** Non-dimensional barred variables ($\bar\omega, \bar k, \theta$) and physical units where appropriate ($L_{ij}$ in $\mathrm{m}^2$, $S_\theta$ in $\mathrm{rad}^{-1}$).
4. **Data Integrity:** No hardcoded numbers in generator scripts. All plotted data points and table rows are dynamically ingested from verified JSON/YAML files.
5. **LaTeX Syntax:** Table fragments in `paper9/tables/out/*.tex` utilize standard `tabularx` environments compatible with `elsarticle`.

---

## 4. Preservation of Unchanged Downstream Statuses

* **Phase 6 Status:** **PARTIAL** (permissible subset complete; full phase awaiting G3 & Case C).
* **Gate G-F Status:** **PARTIAL**.
* **Gate G3:** **NOT MET** (preserved).
* **PCR1:** **NOT PASS** (preserved).
* **B6:** **PARTIAL** (preserved).
* **Phases P7–P9:** **NOT STARTED**.
