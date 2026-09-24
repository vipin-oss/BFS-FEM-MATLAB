# RECOVERY CHECKPOINT — P12U (final)

**Purpose:** final recovery point for the P12U correction closure (P12T findings F1–F3). Text-only
corrections plus new regression guards; no scientific, production, manuscript, Blueprint or gate change.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Starting SHA (phase entry)** | **`9a71f6752e9b7f85e45b3aa81c3dbe1210b384a6`** (local = remote = `ls-remote`; clean tree) |
| P12U pre-work checkpoint | `6937f5f61f9f054ce0c50db99db60b20430a16f8` (pushed `9a71f67..6937f5f`; verified) |
| **P12U correction commit** | **`5864fd4fb3dbc74c7aa753f17f048be3a040595a`** (pushed `6937f5f..5864fd4`; verified by fetch **and** `ls-remote`) |
| P12U final checkpoint | this file's own commit (SHA recorded in the delivery report; pushed + verified the same way) |
| Governing Blueprint | **v1.5** `b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91` — **unchanged** |
| Tree at exit | checked clean after the checkpoint push; no history rewrite; no new branch |

## Closures

| Finding | Status | Where |
|---|---|---|
| **F1** B1 vertex strings | **CLOSED** | machine record `benchmarks.B1.reproduction_status` and P12S audit §Phase D now carry k̄ = 0 → 0.0000/0.9795/1.0210/1.9809 and k̄ = ±1 → 0.4799/0.5196/1.4998/1.9809; `1.4799` / `0.5099` absent from the corrected corpus |
| **F2** "source's own figure … require 0.50" | **CLOSED** | corrected in `p12s_run.py`, the machine record, the P12S audit file, the P12S recovery checkpoint, the manuscript-impact proposal **and** the raw run record (propagated copy found in this phase); wording now separates the source's own gradient ("Present", solid) curve ≈ 0.436 · the classical limit 0.500 · the dashed literature [34] curve ≈ 0.50 |
| **F3** internal inconsistency in `p12s_run.py` | **CLOSED** | line 178 unchanged (accepted reading); lines 184–185 now consistent with it |
| F4 | **UNCHANGED** | INFO, wording already qualified |

Two consequences of the correction were also closed: the machine record's B3 reason is verbatim the
corrected script output, and the `evidence_path_sha256` fields were refreshed from the pre-correction raw
record `b1e7c17d…` to the corrected raw record `cffc0c88…`.

## Verification at exit

| Check | Result |
|---|---|
| Corrected script re-run into `/tmp` (committed evidence untouched) | runs clean; all six PNGs byte-identical; only the corrected B3 reason string and the redirected path differ; numeric fields identical |
| Targeted tests | **42 passed** (`evidence/p12u/targeted.txt`) |
| Full regression ×2 | **168 passed, 1 skipped** each (`suite_run1.txt`, `suite_run2.txt`) |
| Guards | **87 passed** (`guards.txt`) |
| Cross-checks | **43 / 43** (`crosscheck.txt`) |
| Immutability | **12/12** governing anchors unchanged; overlays, panels, P12T audit + evidence, `benchmark_evidence.json` and the P12S/P12R guard files byte-identical; blueprint, manuscript, production, results, PDFs, drafts unchanged (`immutability_and_correction.txt`) |
| Corrected-text re-inspection | defective strings absent; three baselines distinguished in every corrected file (`corrected_text_inspection.txt`) |
| New guards | `paper9/verification/suite/test_p12u_correction_closure.py` — 17 tests pinning F1/F2/F3 plus the closure invariants and the record↔raw-record hash consistency |

## Status at exit (unchanged)

B1 `GRAPHICAL_VALIDATION`/PASS · B2 `NOT_VALIDATED` (ambiguity UNRESOLVED) · B3 `NOT_VALIDATED` ·
`quantitative_error` `[NULL, NULL, NULL]` · PCR1 **NOT PASS** · G3 **NOT MET** · G4 **NOT MET** ·
P5 **NOT PASS / OPEN** · R-1 **OPEN** · PCR5 **PASS** · P13 **BLOCKED** · manuscript **unchanged** ·
author requests **NOT SENT**, no contact, no data received · Blueprint not reopened.

## Chain (most recent)

`… → d0fa5b5` (P12T audit) `→ 9a71f67` (P12T final) `→ 6937f5f` (**P12U pre-work**)
`→ 5864fd4` (P12U correction) `→` *this checkpoint*.
