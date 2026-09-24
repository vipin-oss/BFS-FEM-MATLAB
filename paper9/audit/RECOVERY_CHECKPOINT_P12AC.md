# RECOVERY CHECKPOINT — P12AC (final)

**Phase:** P12AC — final scientific literature-resolution pass: candidate classification and the formal
recording of **Decision B** for the external benchmarks B2/B3.
**Outcome:** the search for a *published* replacement or augmentation of B2/B3 is closed permanently; no
admissible candidate exists; B2/B3 remain `NOT_VALIDATED` for a **source-side** reason, established with the
solver verified *against* the source's own printed formulation to machine precision. No gate, threshold,
validation route, Blueprint byte, manuscript byte, numerical result or benchmark status moved.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Entry SHA (verified)** | **`5093c587a20d643c16f533f1458e8b52129265d6`** (P12AB final; local = origin = ls-remote, clean tree) |
| **P12AC pre-work checkpoint** | **`33ce5ecda32bd2fcf605fb7593426e1f4b87d226`** (pushed + verified before the audit edits) |
| **P12AC main commit** | **`9858fde1ffcf0d58501dd7a5910fcb8a0d64a9fb`** — Decision B record + evidence script/JSON + 11 guards |
| **P12AC final checkpoint** | the commit carrying this file (a commit cannot contain its own hash; it is stated in the P12AC delivery report) |
| **Verified remote SHA** | pushed and re-verified: local = `origin/phase-1-symbolic` = `ls-remote` |
| Tree at exit | clean (`git status --porcelain` empty) |
| Baseline for immutability | `/home/user/p12ac_baseline_hashes.txt` — **541** tracked files at entry (content sha256) |
| Governing Blueprint | **v1.5** `b96c8e76…` CURRENT (unchanged); v1.4 `2ae0b1e8…` FROZEN / superseded (unchanged) |
| Active machine record | `paper9/audit/benchmark_validation_record.json` `2fad2d92…` (unchanged) |
| Register | CSV `8d86528f…`; JSON `83ff8723…` (unchanged; 46 rows / 18 TVs) |
| Manuscript | 12 `.tex` under `paper9/latex/`, set hash `5ba2c22e…` — **byte-unchanged** |

## Decision recorded (Part 5 of the record)

> **Decision B.** *B2/B3 remain source-limited and NOT_VALIDATED because the published sources do not provide
> sufficient authoritative parameter/curve information.* — a property of the published record, **not** a
> solver defect; the benchmark hunt is closed permanently.

## Key substantive result (Part 3 of the record)

The repository anti-plane dipolar-gradient solver is a faithful implementation of LWZ2016 **as printed**:

| comparison (5 parameter points) | maximum discrepancy |
|---|---|
| printed Appendix 3 − repository solver | **3.6e-15** |
| printed Appendix 3 − first principles (Eqs. 12–14, 41.1–41.4) | **3.6e-15** |
| first principles − repository solver | **1.8e-15** |
| homogeneous cell vs the paper's own dispersion relation (14.1) | **1.4e-15** (relative) |

The earlier P12AB-family note that the implementation *differs* from the printed Appendix 3 is **retracted**
(defective hand-reconstruction; no member of a 96-member variant family reproduces it). LWZ2016 Fig. 3
(`ξ̄ = 0`) nevertheless remains **not reproducible** from its stated parameter set
(computed stop bands `[0.6675, 0.6937] · [1.2946, 2.2617] · [2.6098, …]` versus digitised grey bands
`[0.6036, 0.6627] · [0.8718, 1.1637] · [1.3136, 1.7120]`; no source-conforming convention variant
reproduces the digitised bands; layer order is provably irrelevant) ⇒ LWZ2016 = **SUPPORTING ONLY**,
not an admissible Layer-2 benchmark.

## Statuses at exit (all unchanged)

| Item | Status |
|---|---|
| B1 | `GRAPHICAL_VALIDATION` / `PASS` |
| B2 | `NOT_VALIDATED` (ambiguity `UNRESOLVED`; `quantitative_error` NULL) |
| B3 | `NOT_VALIDATED`; formulation `ESTABLISHED / SOURCE-EQUIVALENT`; `quantitative_error` NULL |
| PCR1 | `NOT PASS` (item 1 only) |
| G3 / G4 | `NOT MET` / `NOT MET` |
| P5 | `NOT PASS / OPEN` (authorisation-gated; independent of B2/B3) |
| R-1 | `OPEN` (independent of B2/B3; authorisation-gated) |
| C-1 | `OPEN` as a gate (independent; PI decision) |
| PCR5 | `PASS` |
| P13 | `BLOCKED` (now closable only by an explicitly authorised internal decision, without lowering any gate) |
| Author-data requests | **NOT SENT / NOT AUTHORISED** (P12L/P12M/P12Q unchanged) |
| Blueprint / manuscript | unchanged (`b96c8e76…` / `5ba2c22e…`) |

## Regression at exit (exact counts)

| Run | Result |
|---|---|
| P12AC guard suite (new) `test_p12ac_decision_b.py` | **11 passed** |
| Full suite `paper9/verification` | **282 passed, 1 skipped** (P12AB-era: 271P/1S) |
| `check_traceability.py` | 18 CLOSED/LOCKED, 0 open (100 %) |
| `check_register_provenance.py` | PASS — A = 0, B = 3, C = 2, D = 0 |
| `evidence/p12j/final_verification_p12j.py` | **43 passed / 0 failed** |
| Immutability vs `/home/user/p12ac_baseline_hashes.txt` (541 files) | **0 changed, 0 removed, 5 added** |

## Files added (the complete change set of this phase)

1. `paper9/audit/P12AC_LITERATURE_RESOLUTION_DECISION_B.md`
2. `paper9/audit/evidence/p12ac/lwz_tm_equivalence_check.py`
3. `paper9/audit/evidence/p12ac/lwz_tm_equivalence_results.json`
4. `paper9/verification/suite/test_p12ac_decision_b.py`
5. `paper9/audit/RECOVERY_CHECKPOINT_P12AC.md` (this file; pre-work form committed at `33ce5ec`)

Nothing else in the repository changed — no source PDF, no solver, no manuscript, no register row, no
production artefact, no historical audit record.
