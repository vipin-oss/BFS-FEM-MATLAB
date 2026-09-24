# RECOVERY CHECKPOINT — P12V (final)

**Phase:** P12V — forensic source audit of the two remaining external-validation blockers
(B2 = Li et al. 2024 Fig. 2(b) `l` vs `l̄ = l/b`; B3 = Li et al. 2023 Fig. 4(c)
dipolar-gradient formulation/parameter/convention). Audit only.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Starting SHA (entry)** | **`2e2c0e8b80660f56cfa330e43ad83efaf6b08d0f`** (P12U content `5864fd4fb3dbc74c7aa753f17f048be3a040595a`) |
| **P12V pre-work checkpoint** | **`4f373f0408dfa3435e5f1c7ea636a623199dbb38`** (pushed + verified before any editorial work) |
| **P12V audit commit** | **`9b1eff8f42430280aecb6689ed99182c057f56c2`** — “P12V: B2/B3 blocker source audit (Parts A-H), evidence and 11 source-audit guards” |
| **P12V final checkpoint (this file)** | recorded in the P12V delivery report |
| Tree at exit | audit artifacts only; no tracked file modified by this phase |
| Governing Blueprint | **v1.5** `b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91` (unchanged) |
| Authoritative sources | li2024 `2ac5f45d77ee37569f69e8890b70200ae6982f669ecaccf6cb5aa162f0340513`; li2023 `3f5103380302609ef2dfe76c8ade09cae79b2ebbd4fdb4da228576c331191aa7` (both re-verified, byte-identical) |

## Verdicts (this phase)

| Benchmark | Decision (from the permitted sets) | Status |
|---|---|---|
| **B2** | **`SOURCE-AMBIGUOUS — DATA REQUIRED`** | remains `NOT_VALIDATED` (ambiguity `UNRESOLVED`), `quantitative_error` NULL |
| **B3** | **`SOURCE-AMBIGUOUS — DATA REQUIRED`** | remains `NOT_VALIDATED`, `quantitative_error` NULL |

Key B3 result: the repository's transfer matrix was **independently reconstructed from the
source's own Appendix 3** (`[T] = [P0][G][P0]⁻¹`, 60-digit arithmetic) and equals the repository's
closed-form matrix to ~10⁻¹⁶; the 60- and 120-digit Bloch evaluations reproduce the recorded band
edges (gap from ω̄ = 0.3391, second band from ω̄ = 1.021) exactly. The residual mismatch with the
published Fig. 4(c) solid curve (ω̄ ≈ 0.433–0.436 at k̄ = ±1) is therefore **source-side**, not an
implementation defect. Key B2 result: the caption value is an **unbarred, unit-less** number, the
normalisation `l̄ = l/b` is printed only for the barred symbol, no sentence links the caption to
Eq. (55), no erratum/supplementary exists, and no admissible interpretation reproduces the
published Fig. 2(b).

## Findings (reported, not fixed)

* **P12V-F1** `paper9/audit/benchmark_validation_record.json` → `benchmarks.B3.reproduction_status`
  still attributes “0.50” to “the source's own” curve (the P12T/P12U conflation); the source's own
  gradient curve is 0.436 (classical limit 0.500, dashed [34] ≈ 0.50).
* **P12V-F2** same record → `benchmarks.B3.ambiguity_status` wording (“formulation/coefficient
  convention not pinned down”) is superseded: the formulation is now verified.

Neither changes a route, gate or number.

## Status (unchanged — P12V did not promote anything)

| Item | Status |
|---|---|
| B1 | `GRAPHICAL_VALIDATION` / PASS |
| `quantitative_error` | `[NULL, NULL, NULL]` |
| **PCR1 / G3 / G4** | **NOT PASS / NOT MET / NOT MET** |
| **P5 / R-1 / PCR5** | **NOT PASS, OPEN / OPEN / PASS** |
| **P13** | **BLOCKED** |
| Manuscript | unchanged (0 diffs); author contact NONE; author requests NOT SENT and unmodified; PI decision PENDING |

## Verification performed (this phase)

* full suite `paper9/verification/suite` → **179 passed, 1 skipped** (was 168P/1S before P12V);
* targeted (P12V + P12U + P12S + P12R) → **53 passed**;
* named guard files (P12C + P12H ×2 + P12R + P12S + P12U + P12V) → **98 passed** (87 before P12V);
* P12J cross-check → **43 checks passed, 0 failed**;
* immutability → `git status --porcelain` shows only the three new P12V artifacts; **no tracked file
  modified** (Blueprint v1.5, manuscript, production, sources and the corrected P12U record all
  unchanged); source PDFs byte-identical to their recorded hashes;
* no production numerical result changed; no gate, route or status was altered.

## Scope carried out

Parts A–H of the phase instruction (B2 source map and the eight enumerated questions; the B3
Fig. 4(c) chain and the nine enumerated questions; the 15-row convention-difference matrix;
reference auditing; the classification table; the no-tuning statement; verdicts; the precise
missing-information record, unsent). No author contact; no requests sent or altered; no tuning;
no gate/definition/Blueprint/manuscript change; P13 untouched; P12U F1–F4 not reopened.
