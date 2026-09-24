# RECOVERY CHECKPOINT — P12U (pre-work)

**Purpose:** recovery point created **before any P12U work** (correction closure for the P12T findings
F1–F3: two factual/descriptive defects and one internal inconsistency found by the independent audit).

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Starting local SHA** | **`9a71f6752e9b7f85e45b3aa81c3dbe1210b384a6`** |
| **Starting remote SHA** | `9a71f6752e9b7f85e45b3aa81c3dbe1210b384a6` (verified by fetch + `ls-remote`) |
| Tree at entry | **clean** (0 porcelain entries); 24/24 tracked `*/out/` artifacts present |
| P12T audit commit | `d0fa5b538db1842b5923c201c1d7d93a69ccf594` |
| P12S content / final | `a1816a946f2cf059eaa16144caa529f4f856502f` / `b80ff67348f5b0fbf4cce28aa2ff6ee288ca20df` |
| Governing Blueprint | **v1.5** `b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91` (must stay unchanged) |
| **P12U pre-work checkpoint SHA (this file's own commit)** | recorded in the P12U delivery report (pushed + verified) |

## Status at entry (locked — P12U does not change these)

| Item | Status |
|---|---|
| B1 | `GRAPHICAL_VALIDATION` / PASS |
| B2 | `NOT_VALIDATED` (ambiguity UNRESOLVED) |
| B3 | `NOT_VALIDATED` |
| `quantitative_error` | `[NULL, NULL, NULL]` |
| **PCR1 / G3 / G4** | **NOT PASS / NOT MET / NOT MET** |
| **P5 / R-1 / PCR5** | **NOT PASS, OPEN / OPEN / PASS** |
| **P13** | **BLOCKED** |

## P12U scope (this phase) — F1–F3 only

* **F1**: replace the B1 vertex strings with the P12T-verified values (k̄ = 0 → 0.0000/0.9795/1.0210/1.9809;
  k̄ = ±1 → 0.4799/0.5196/1.4998/1.9809) in
  `paper9/audit/benchmark_validation_record.json` and `paper9/audit/P12S_GRAPHICAL_VALIDATION_AUDIT.md`.
* **F2**: replace the "the source's own figure … require 0.50" wording with wording that distinguishes the
  source's own gradient ("Present") curve ≈ 0.436 · the classical limit 0.500 · the dashed literature [34]
  curve ≈ 0.50, in `paper9/validation/p12s_run.py`, `paper9/audit/benchmark_validation_record.json`,
  `paper9/audit/P12S_GRAPHICAL_VALIDATION_AUDIT.md`, `paper9/audit/RECOVERY_CHECKPOINT_P12S.md`,
  `paper9/audit/P12S_MANUSCRIPT_IMPACT.md`.
* **F3**: make `p12s_run.py` lines 184–185 consistent with line 178 (the accepted reading).
* Add regression tests pinning F1/F2/F3 so the defects cannot silently return.

**Explicitly NOT in scope:** any change to the Blueprint, Rule R-fit, the manuscript, production
numerical results, the B1/B2/B3 routes and statuses, the gates, the author-request package, or any new
benchmark tuning; no author contact; no P13 work. F4 stays as recorded (INFO, wording already qualified).
