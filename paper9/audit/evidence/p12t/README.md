# P12T evidence bundle — independent forensic audit of P12S

Pre-work checkpoint: `71e6049d88ec5a2ee26b65a5e088562d841c47bd` (pushed + verified before any audit work).
Entry SHA: `b80ff67348f5b0fbf4cce28aa2ff6ee288ca20df`.

| File | What it is |
|---|---|
| `independent_checks.py` / `independent_checks.json` | This audit's own code and results: source re-extraction from both PDFs (22 checks), own transfer-matrix band-edge root-finding for B1, own B2 interpretation arithmetic, own B3 ω₀ and classical-limit derivation, own panel digitisation, re-run of the audited B3 artifact, and governance probes on the classifier with synthetic inputs only. |
| `b2_registry_crosscheck.txt` | P12S micro-configuration gaps vs the pre-existing production registry `paper9/results/raw/p11d_b2_gap_registry.json` (adaptive precision, exact z-test) — agreement ≤ 0.005 in ω̄. |
| `overclaim_search.txt` | Tier/percentage/status phrase search across the P12S artifacts, the P12S support code and the manuscript (report only). |
| `immutability.txt` | 17/17 anchors unchanged (12 governing + 5 P12S artifacts), plus source-PDF hashes and empty diffs for the manuscript, production code, blueprint directory and P12S artifacts. |
| `suite_run1.txt`, `suite_run2.txt` | Full suite twice: **151 passed, 1 skipped** each. |
| `guards.txt` | P12S + P12R + P12C guard files: **36 passed**. |
| `crosscheck.txt` | P12J independent cross-check: **43/43**. |

**Outcome:** B1 `GRAPHICAL_VALIDATION`/PASS and B2/B3 `NOT_VALIDATED` are independently confirmed; the
gate consequences (PCR1 NOT PASS, G3/G4 NOT MET) follow from Blueprint v1.5 §13/A2.7. Two descriptive
defects were found and recorded without being fixed (F1: B1 vertex strings; F2/F3: the B3 "0.50" baseline
clause, also propagated into the manuscript-impact proposal). No scientific artifact, manuscript,
Blueprint, threshold, production result or author-request document was modified by this phase.
