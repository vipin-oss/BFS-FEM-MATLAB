# RECOVERY CHECKPOINT — P12T (final)

**Purpose:** final recovery point for the P12T independent audit of the P12S graphical-validation
evidence. Audit only: no Blueprint, manuscript, scientific, production or author-request artifact was
modified.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Starting SHA (phase entry)** | **`b80ff67348f5b0fbf4cce28aa2ff6ee288ca20df`** (local = remote = `ls-remote`; clean tree) |
| P12T pre-work checkpoint | `71e6049d88ec5a2ee26b65a5e088562d841c47bd` (pushed `b80ff67..71e6049`; verified) |
| **P12T audit commit** | **`d0fa5b538db1842b5923c201c1d7d93a69ccf594`** (pushed `71e6049..d0fa5b5`; verified by fetch **and** `ls-remote`) |
| P12T final checkpoint | this file's own commit (SHA recorded in the delivery report; pushed + verified the same way) |
| Governing Blueprint | **v1.5** `b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91` — **unchanged** |
| Tree at exit | checked clean after the checkpoint push; no history rewrite; no new branch |

## Audit verdicts

| Item | Verdict |
|---|---|
| **B1** (Li 2024 Fig. 2(a), p. 9) | **VERIFIED WITH CORRECTION REQUIRED** — route `GRAPHICAL_VALIDATION`/PASS independently confirmed (own transfer-matrix root-finder; own digitisation, max \|Δω̄\| ≈ 0.006 ≈ 1.6 px); finding **F1**: the vertex strings in the machine-readable record are descriptive-only errors |
| **B2** (Li 2024 Fig. 2(b), p. 9) | **VERIFIED** — ambiguity genuinely unresolved in the source; (lk)² = 4.1639×10⁻⁶ and 1.6655×10⁻⁹; barred requirement `required_dps = 52131` reproduced exactly via `ceil(0.4343·Λ)+15`; micro-configuration gaps cross-checked against the pre-existing production registry (≤ 0.005 ω̄); no interpretation matches the published panel |
| **B3** (Li 2023 Fig. 4(c), p. 15) | **VERIFIED WITH CORRECTION REQUIRED** — ω₀ = 4.114×10⁸ Hz reproduced; reproduced 0.339 vs the source's own **solid "Present"** curve **0.436** at k̄ = 1 (98 % column presence); findings **F2/F3**: the "0.50" baseline clause misstates the figure (0.50 is the classical limit / the dashed literature curve) and is propagated into the manuscript-impact proposal |
| Graphical-validation governance | **VERIFIED** — synthetic classifier probes: thresholds 2.0/0.5 unchanged, graphical route never carries a number, `FabricatedPrecisionError` on any percentage without source numerics, hierarchy ranks 3/2/1 |
| Gate logic (v1.5 §13/A2.7) | **VERIFIED** — B1 graphical + B2/B3 not validated ⇒ PCR1 NOT PASS, G3 NOT MET, G4 NOT MET; definitions unchanged |

## Evidence, immutability, regression

| Check | Result | Log |
|---|---|---|
| Independent checks | 22 source checks + own recomputations of every checkable P12S scalar | `paper9/audit/evidence/p12t/independent_checks.json` |
| Overclaim search | no overclaim found in the P12S artifacts; manuscript-side tier wording differences already documented in the P12S impact proposal | `…/overclaim_search.txt` |
| Immutability | **17/17** anchors (12 governing + 5 P12S artifacts); source PDFs match the recorded hashes; manuscript/production/blueprint/P12S diffs empty | `…/immutability.txt` |
| Regression | suite **151 passed, 1 skipped** ×2; guards **36 passed**; cross-check **43/43** | `suite_run1.txt`, `suite_run2.txt`, `guards.txt`, `crosscheck.txt` |

## Findings (recorded, NOT fixed — per the phase rule)

* **F1** (LOW–MEDIUM, descriptive): `paper9/audit/benchmark_validation_record.json:30` and
  `paper9/audit/P12S_GRAPHICAL_VALIDATION_AUDIT.md:84` — B1 vertex strings.
* **F2** (MEDIUM, misstated baseline): `paper9/validation/p12s_run.py:184–185`,
  `paper9/audit/benchmark_validation_record.json:165`,
  `paper9/audit/P12S_GRAPHICAL_VALIDATION_AUDIT.md:111–112`,
  `paper9/audit/RECOVERY_CHECKPOINT_P12S.md:27`, and the proposal
  `paper9/audit/P12S_MANUSCRIPT_IMPACT.md:37`.
* **F3** (LOW, internal inconsistency): `paper9/validation/p12s_run.py:178` vs `:184–185`.
* **F4** (INFO): the "numerically infeasible" wording is correctly qualified.

No defect was found in any route decision, gate consequence, classifier rule, threshold, production
numerical result, or governing artifact.

## Status at exit (unchanged)

PCR1 **NOT PASS** · G3 **NOT MET** · G4 **NOT MET** · P5 **NOT PASS / OPEN** · R-1 **OPEN** ·
PCR5 **PASS** · P13 **BLOCKED** · B1/B2/B3 `quantitative_error` **NULL** · manuscript **unchanged**
(0 diffs) · author requests **NOT SENT**, no contact, no data received · Blueprint v1.5 not reopened.

## Chain (most recent)

`… → b80ff67` (P12S final) `→ 71e6049` (**P12T pre-work**) `→ d0fa5b5` (P12T audit) `→` *this checkpoint*.
