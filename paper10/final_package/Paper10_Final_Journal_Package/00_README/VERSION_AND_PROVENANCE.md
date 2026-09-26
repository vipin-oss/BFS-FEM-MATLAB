# Version and Provenance Record — Paper 10

**Manuscript Title:** Dual-Phase-Lag (DPL) Thermoelastic Band-Gap Tuning and Acoustic Dissipation in 1D Periodic Metamaterials with Dipolar Gradient Elasticity  
**Target Journals:** *Applied Mathematical Modelling* / *Composite Structures*  
**Repository:** `vipin-oss/BFS-FEM-MATLAB`  
**Branch:** `arena/01a0dcde-bfs-fem-matlab`  
**Package Creation Date:** 2026-09-26  
**Final Verified Commit:** `f92e86462c42d9d4b7dce78309daac9ac53d7cef`  
**Remote Tracking SHA:** `f92e86462c42d9d4b7dce78309daac9ac53d7cef` (Verified match on `origin/arena/01a0dcde-bfs-fem-matlab`)  
**Package Status:** FINAL MANUSCRIPT — READY FOR JOURNAL PACKAGE PREPARATION  

---

## 1. Linear Milestone Provenance Chain

The research artifact was constructed strictly in accordance with Workflow v6, with each phase verified, audited, committed, pushed, and remote SHA-verified before advancing:

| Phase / Milestone | Commit SHA | Verification Status | Major Scientific Content Locked |
| :--- | :---: | :---: | :--- |
| **Stage 1: Research Blueprint** | `1ed2d54` | **LOCKED** | Model scope, novelty boundary, 5-level validation hierarchy, state vectors |
| **Phase 1: Analytical Derivations** | `e9ca21f` | **LOCKED** | Mindlin Form-II gradient elasticity + DPL heat conduction, boundary tractions |
| **Phase 2: Solver Implementation & Validation** | `ee61a02` | **LOCKED** | Papargyri-Beskou benchmark ($2.45 \times 10^{-15}$ error), symplecticity ($2.66 \times 10^{-13}$) |
| **Phase 3A: Parameter Matrix & Pilot Sweeps** | `505d9aa` | **LOCKED** | Locked 36-case matrix, Hungarian assignment continuous branch tracking |
| **Phase 3B: Full Production Sweeps** | `a21d4d6` | **LOCKED** | 36 cases, 100 frequencies, 17,747 modal records in 12.4 s |
| **Phase 3B: Targeted Scientific Audit** | `9ed2347` | **AUDITED** | Uncovered column unpack error, gap truncation, branch tracking filter flaws |
| **Phase 3B: Post-Correction Audit Baseline** | `5622c7b` | **LOCKED** | 23 open gaps flagged `is_boundary_truncated=True`, Figs 2/4/6/7/9/10 calibrated |
| **Phase 4: Manuscript Synthesis & Audit** | `a709ff5` | **LOCKED** | Initial 19-page manuscript in LaTeX & PDF, traceability matrix, source audit |
| **Phase 4: Pre-Submission Audit** | `82bca96` | **AUDITED** | 15-dimension audit, 4 minor actionable items cataloged in CSV (0 CRITICAL) |
| **Phase 4: Final Corrected Baseline** | `f92e864` | **FROZEN** | Applied AUD-01 to AUD-04, recompiled 19 pp PDF, final verification PASS |

---

## 2. Immutability Guarantee

The following core components are **100% frozen** and must not be altered:
- Governing continuum mechanics equations and variational boundary conditions (`PHASE1_DERIVATION.md`);
- Modular solvers (`coupled10.py`, `antiplane.py`, `parameters.py`);
- Numerical production datasets (`04_PRODUCTION_DATA/*.csv`, `*.json`);
- Calibrated publication figures (`02_FIGURES/*.png`);
- Verified manuscript source and PDF (`01_MANUSCRIPT/`).
