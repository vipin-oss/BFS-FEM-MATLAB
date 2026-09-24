# RECOVERY CHECKPOINT — P12W (final)

**Phase:** P12W — correction closure for the two residual P12V text findings
(**P12V-F1** `benchmarks.B3.reproduction_status`; **P12V-F2** `benchmarks.B3.ambiguity_status`),
plus the one consequential span inside `gate_state.blocker` (Part C internal-contradiction rule).
Text-only correction: no route, gate, number, hash or scientific status changed.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Entry SHA (verified)** | **`cbb26b52b7abeeb9cfc247bc6ba10978c96d697f`** (P12V final; local = origin = ls-remote, clean tree) |
| **P12W pre-work checkpoint** | **`1f5cd5f4116a9793c05b1329afeaf6d81be2842c`** (pushed + verified before any edit) |
| **P12W correction commit** | **`186374f12fbee915fcbacaad2a4ce38c6822599c`** — “P12W: correction closure for P12V-F1/F2 (B3 record wording) with 12 targeted guards” |
| **P12W final checkpoint (this file)** | recorded in the P12W delivery report |
| **Verified remote SHA** | pushed and re-verified (local = `origin/phase-1-symbolic` = `ls-remote`) |
| Tree at exit | clean (`git status --porcelain` empty) |
| Governing Blueprint | **v1.5** `b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91` (unchanged) |
| Active machine record | before `cdbfe6c2d7e0e19b98940815e4478c1c9a1a432f3ad1d4b4698b00349d451df3` → after `9ea0d4c8039b42c2644db3c679e3ff4b42b2a8a72b3977f6e54c1d301b718b51` |
| Frozen raw P12S/P12U record | `cffc0c889c79186b34b0d3775191e181e040dfb358e4c61f6c06a7f22f5c3a21` (byte-identical, untouched) |
| Authoritative sources | li2024 `2ac5f45d…`; li2023 `3f510338…` (both byte-identical) |

## Exact files changed by P12W

| File | Change |
|---|---|
| `paper9/audit/benchmark_validation_record.json` | 3 text spans: `benchmarks.B3.reproduction_status` (F1), `benchmarks.B3.ambiguity_status` (F2), `gate_state.blocker` (Part C; dropped “unverifiable formulation”). All other fields, numbers, hashes, reasons and gates identical |
| `paper9/verification/suite/test_p12v_source_audit.py` | content pin re-pointed to the intentionally corrected record (same exact-content strictness; documented in the docstring) |
| `paper9/verification/suite/test_p12w_correction_closure.py` | **new** — 12 targeted F1/F2/Part-C guards |
| `paper9/audit/P12W_CORRECTION_CLOSURE.md` | **new** — closure record |
| `paper9/audit/RECOVERY_CHECKPOINT_P12W.md` | **new** — pre-work version (`1f5cd5f`), now final |

## Findings closed

| Finding | Status | Basis |
|---|---|---|
| **P12V-F1** | **CLOSED** | `reproduction_status` now separates the source-formulation reproduction (~0.3391; P12T's reading 0.35) · the published solid “Present” gradient curve (~0.433–0.436) · the classical limit 0.500 / dashed literature [34] (~0.50); “source's own 0.50” deleted (repo-wide search: the string survives only as the historical finding quoted in the P12V audit) |
| **P12V-F2** | **CLOSED** | `ambiguity_status` now states the formulation is established as the source's own (Appendix 3 `[P0][G][P0]^-1` to ~1e-16 at 60 digits; recorded bands reproduced), that the residual is the unstated Fig. 4(c) parameter set/normalisation and curve data with no Fig. 3(b) inheritance assumed, and that B3 remains `NOT_VALIDATED`; the frozen P12S-era `reason` clause is flagged as historical text, not the operative status |
| (Part C consequential span) | **CLOSED** | `gate_state.blocker` no longer calls the formulation unverifiable; still records “B2 and B3 remain NOT_VALIDATED” and “gate definitions unchanged” |

Not reopened: P12U F1–F4. Not corrected (by rule): the frozen P12S/P12U `reason` strings, pinned
byte-identical by the P12U guards; historical P12S/T/U/V audit documents remain faithful to what
they recorded at the time.

## Status at exit (unchanged)

| Item | Status |
|---|---|
| B1 | `GRAPHICAL_VALIDATION` / PASS |
| B2 | `NOT_VALIDATED` / ambiguity `UNRESOLVED` |
| B3 | `NOT_VALIDATED` |
| `quantitative_error` | `[NULL, NULL, NULL]` |
| **PCR1 / G3 / G4** | **NOT PASS / NOT MET / NOT MET** |
| **P5 / R-1 / PCR5** | **NOT PASS, OPEN / OPEN / PASS** |
| **P13** | **BLOCKED** |
| Manuscript | unchanged (0 diffs) |
| Author requests | **NOT SENT**; drafts unmodified; no author contact; PI decision PENDING |

## Verification performed

* new P12W guards → **12 passed**; P12W + P12V → 23 passed;
* targeted (P12W + P12V + P12U + P12S + P12R) → **65 passed**;
* named guard files → **110 passed** (98 before P12W: P12C + P12H ×2 + P12R + P12S + P12U + P12V);
* full regression suite `paper9/verification/suite` → **191 passed, 1 skipped** (179P/1S at P12V);
* P12J cross-check → **43 checks passed, 0 failed**;
* immutability → 518 tracked files compared against the pre-work hash baseline: **exactly 2 changed**
  (the active record and the P12V test pin); `git status --porcelain` at exit empty; Blueprint v1.5,
  Rule R-fit, manuscript (`paper9/latex/`), production, results, tables, validation, `paper9/analytic/`
  sources, P12S/T/U/V evidence and all P12 audit documents byte-identical; raw P12S/P12U record
  untouched;
* no production numerical result changed; no gate, route or status altered; no parameter tuned.
