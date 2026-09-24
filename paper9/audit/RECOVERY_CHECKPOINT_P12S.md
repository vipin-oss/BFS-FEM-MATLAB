# RECOVERY CHECKPOINT — P12S (pre-work)

**Purpose:** recovery point created **before any P12S work** (graphical-validation implementation and
B1/B2/B3 reproduction under Blueprint v1.5/A2).

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| Starting local SHA | `70b7b0e9bf28cbb3d103770e68b9147b7bab68ff` |
| Starting remote SHA | `70b7b0e9bf28cbb3d103770e68b9147b7bab68ff` (verified by fetch + `ls-remote`) |
| Tree at entry | **clean** |
| P12R amendment SHA | `53d40c30480b20c71368870d3a29e8a885b8bd1e` (v1.5 = v1.4 + 8 declared A2 blocks) |
| P12R content / final checkpoint | `53d40c30480b20c71368870d3a29e8a885b8bd1e` / `70b7b0e9bf28cbb3d103770e68b9147b7bab68ff` |
| P12Q content / final checkpoint | `379abcaf0f5a4a84c73617f24ad1d68542820da4` / `1b0523606a0545121c8ffb807b7a2203fe548a9a` |
| P12P content / final checkpoint | `c5138a591aba19fd2a29b017011d21782ff8306d` / `059239efb15068b2477a3cf9a486738c3b7d88ec` |
| **Governing rule** | **Blueprint v1.5 §13 (amendment A2)** — quantitative / graphical / not-validated routes; thresholds unchanged (≤ 2 %; ≤ 0.5 % classical) |
| P12S pre-work checkpoint SHA (this file) | recorded in the P12S session report after the verified push |
| P12S commit SHAs | recorded in the P12S session report after the verified pushes |

## Status at entry (locked)

| Item | Status |
|---|---|
| **PCR1** | **NOT PASS** |
| **G3** | **NOT MET** |
| **G4** | **NOT MET** |
| **P5** | **NOT PASS / OPEN** |
| **R-1** | **OPEN** |
| **PCR5** | **PASS** |
| **P13** | **BLOCKED** |

External-evidence state: author requests **NOT SENT**; **no author contacted**; **no author data
received**; B1/B2/B3 `quantitative_error` **NULL**; B2 `l` vs `l̄` unresolved.

## P12S scope

Phase A forensic extraction from the authoritative PDFs (`paper9/analytic/li2024/`, `li2023/`);
Phase B route classification; Phase C reproduction and overlay for benchmarks qualifying under A2;
Phase D–F per-benchmark treatment (B1 classical, B2 ambiguity, B3 parameter provenance); Phase G
machine-readable validation record; Phase H anti-fabrication tests; Phase I PCR1/G3 evaluation strictly
under A2; Phase J manuscript-impact list (no manuscript change); Phase K regression + immutability;
Phase L commit/push/checkpoint.

**Not performed:** author contact, request sending, fabricated percentages, threshold changes, gate
changes merely to obtain PASS, manuscript edits, P13.
