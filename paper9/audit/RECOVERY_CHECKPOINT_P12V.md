# RECOVERY CHECKPOINT — P12V (pre-work)

**Purpose:** recovery point created **before any P12V work** — independent forensic audit of the two
remaining external-validation blockers (B2 = Li et al. 2024 Fig. 2(b) `l` vs `l̄ = l/b` ambiguity;
B3 = Li et al. 2023 Fig. 4(c) formulation/parameter/convention mismatch), to determine whether either
blocker can be resolved from the already available authoritative published sources **without** author data.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Starting local SHA** | **`2e2c0e8b80660f56cfa330e43ad83efaf6b08d0f`** |
| **Starting remote SHA** | `2e2c0e8b80660f56cfa330e43ad83efaf6b08d0f` (verified by fetch + `ls-remote`) |
| Tree at entry | **clean** (0 porcelain entries) |
| P12U content / final | `5864fd4fb3dbc74c7aa753f17f048be3a040595a` / `2e2c0e8b80660f56cfa330e43ad83efaf6b08d0f` |
| P12T audit / final | `d0fa5b538db1842b5923c201c1d7d93a69ccf594` / `9a71f6752e9b7f85e45b3aa81c3dbe1210b384a6` |
| Governing Blueprint | **v1.5** `b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91` (must stay unchanged) |
| Authoritative sources | li2024 `2ac5f45d77ee37569f69e8890b70200ae6982f669ecaccf6cb5aa162f0340513`; li2023 `3f5103380302609ef2dfe76c8ade09cae79b2ebbd4fdb4da228576c331191aa7` |
| **P12V pre-work checkpoint SHA (this file's own commit)** | recorded in the P12V delivery report (pushed + verified) |

## Status at entry (locked — P12V does not change these)

| Item | Status |
|---|---|
| B1 | `GRAPHICAL_VALIDATION` / PASS |
| B2 | `NOT_VALIDATED` (ambiguity UNRESOLVED) |
| B3 | `NOT_VALIDATED` (`SOURCE_UNAVAILABLE`) |
| `quantitative_error` | `[NULL, NULL, NULL]` |
| **PCR1 / G3 / G4** | **NOT PASS / NOT MET / NOT MET** |
| **P5 / R-1 / PCR5** | **NOT PASS, OPEN / OPEN / PASS** |
| **P13** | **BLOCKED** |
| Manuscript | unchanged; author contact NONE; author requests NOT SENT; PI decision PENDING |

## P12V scope (this phase)

Forensic source audit only (Parts A–K of the phase instruction): build a page→equation→notation→meaning
map for every B2-relevant symbol in Li et al. 2024 and for the whole Fig. 4(c) chain in Li et al. 2023;
classify each missing item as `EXPLICITLY PROVIDED` / `DERIVABLE FROM SOURCE` / `ONLY INFERABLE` /
`NOT PROVIDED`; produce a convention-difference matrix for B3; audit reference [34]; run a no-tuning test
(branch relabeling, unit/normalization conversions and mathematically equivalent formulations only); and
record B2/B3 verdicts from the enumerated decision sets.

**Explicitly NOT in scope:** reopening P12U findings F1–F4; modifying Blueprint v1.5 or the manuscript;
production numerical results; tuning B2/B3 parameters to obtain agreement; open-ended parameter searches;
author contact or sending/altering the author-data requests; changing gate definitions; P13.

**Commits allowed:** audit report, audit evidence, tests only.
