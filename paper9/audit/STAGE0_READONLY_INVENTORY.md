# Stage 0 — Initial State & Authoritative Read-Only Inventory

**Date of Inventory:** 2026-09-22  
**Branch:** `phase-1-symbolic`  
**Working Tree:** Clean  
**Local HEAD:** `b9c0b17571ca95e14241bd3a43cf85e414b79a55`  
**Remote Tracking HEAD (`origin/phase-1-symbolic`):** `b9c0b17571ca95e14241bd3a43cf85e414b79a55`  
**Main Branch (`origin/main`):** `1de47a4d111260ffb9b48d7c99e9db45102367c7` (untouched)

---

## 1. Project Phase & Gate Status Matrix

| Phase / Gate | Level | Status | Notes / Reference |
|---|---|---|---|
| **Phase 0** | Plan | **LOCKED** | `CALC_MASTER_PLAN.md` v1.1 |
| **Phase 1** | Mathematical Formulation | **PASS** (G1) | M1–M17 symbolic derivations verified (244+ checks) |
| **Phase 2** | Analytical Calculations | **PASS** (G1b) | Case H closed forms, PB2009 & LWZ2016 formulations |
| **Phase 4A** | Solver Acceptance | **PASS** (G2a) | Tests 5a–5f pass (34/34 PASS) |
| **Phase 3** | Published Validation | **NOT PASS** (G3 NOT MET) | B1/B2/B3 blocked; B6 PARTIAL; PCR1 NOT PASS |
| **Phase 4B** | Verification & Convergence | **PASS** (G2) | Tests 5g–5i pass (21/21 PASS); $\varepsilon_\Delta \approx 4.63 \times 10^{-11}$ |
| **Phase 5** | Main Scientific Production | **PASS** (G5) | Pilot (12/12 PASS), 42-point matrix, S1, S3–S9 complete |
| **Phase 6** | Figures & Tables | **NOT READY** | G3 NOT MET (Fig 4/Tab 3 blocked); S2 unrun (Fig 7/Tab 5 Case C blocked) |
| **Phases 7–9**| Manuscript, Bib, Final Release| **NOT STARTED** | Gated on P6 completion |

---

## 2. Technical Verification (TV) Status Inventory

| TV ID | Item | Current Status | Blocker Effect on P6 |
|---|---|---|---|
| **TV1** | Anchor A (Li 2023) Fig 4(c) $\bar c, \bar d$ parameters | **OPEN** | Blocks Fig 4(c) validation overlay |
| **TV2** | Anchor B (Li 2024) unit-cell $b = a_A + a_B$ | **CLOSED [C]** | Closed from Li 2024 Eq. (51) |
| **TV4** | $k$-path sampling ($N_{\mathrm{seg}}=40$, 121 path nodes, 3321 2D nodes) | **LOCKED [S]** | Locked in P5 pilot and production |
| **TV6** | Production parameters (Case H vs Case C) | **PARTIAL [S]** | Case H locked; Case C parameters **OPEN** (blocks Fig 7, S2) |
| **TV7** | Reported bands ($N=4$) & spurious-mode filter | **LOCKED [S]** | Locked in P5 pilot and production |
| **TV8** | Anchor A (Li 2023) Fig 3 panels | **CLOSED [C]** | Closed from Li 2023 caption |
| **TV9** | Mishra 2026 homogeneous limit (Layer 4) | **OPEN** | Optional Layer 4 check |
| **TV10**| PB2009 Eqs (22)–(28) transcription | **CLOSED [C]** | Closed in Phase 2 |
| **TV11**| LWZ2016 closed forms & parameters | **CLOSED [C]** | Closed in Phase 2 |
| **TV12**| Overlay axis ranges/sampling for Fig 4(a)–(c) | **OPEN** | Blocks Fig 4 validation overlay |
| **TV13**| Numerical resolution floor $\varepsilon_\Delta = 4.63 \times 10^{-11}$ | **LOCKED [A]** | Locked in P4B test 5i |
| **TV14**| Case C reference phase non-dimensionalization | **OPEN** | Blocks Case C production (Fig 7, Table 2) |
| **TV15**| Phase velocity non-dimensionalization $\bar v_p$ | **LOCKED [A]** | Locked in M12 / P5 |
| **TV16**| Orientation angle unit & sensitivity $S_\theta$ scheme | **LOCKED [S]** | Locked in P5 / Table 5 |
| **TV17**| BFS Hermite element 32-DOF ordering & node numbering | **LOCKED [A]** | Locked in M13 / P4A |
| **TV18**| BFS circular inclusion representation | **OPEN** | Blocks Case C production (Fig 7, S2) |

---

## 3. Primary Archival Sources Present in Repository

* `paper9/analytic/li2024/s41598-024-75049-1.pdf` (Li et al., *Sci. Rep.* 14:24035, 2024) — 14 pp.
* `paper9/analytic/li2023/17455030.2023.2222189.pdf` (Li et al., *Waves Random Complex Media* 36:5715–5735, 2023) — 22 pp.
* `paper9/analytic/lwz2016/li2015.pdf` (Li, Wei & Zhou, *Acta Mech.* 227:1005–1023, 2016) — 19 pp.
* `paper9/analytic/pb2009/papargyri-beskou2009.pdf` (Papargyri-Beskou & Beskos, *Int. J. Solids Struct.* 46:3751–3758, 2009) — 8 pp.

---

## 4. Verification & Production Data Assets Present

* Solver core: `paper9/solver/bfs_bloch_solver.py`
* Master parameters: `paper9/params/params_master.yaml`
* P4A verification: `paper9/verification/suite/p4a_5a_to_5f.py` (34/34 PASS)
* P4B verification: `paper9/verification/suite/p4b_5g_to_5i.py` (21/21 PASS)
* Pytest test suite: `paper9/verification/suite/test_p5_production.py` & `test_p4b_5g_5h.py` (11/11 PASS)
* Raw production records:
  - `paper9/results/raw/p5_pilot_raw.json`
  - `paper9/results/raw/p5_production_raw.json`
* Processed production records:
  - `paper9/results/processed/p5_pilot_summary.json`
  - `paper9/results/processed/table5_gap_summary.json`
  - `paper9/results/processed/p5_production_highlights.json`
