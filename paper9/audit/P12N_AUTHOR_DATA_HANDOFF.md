# P12N — Author-Data Handoff (authoritative statement of the external-evidence blocker)

**Phase:** P12N — author-data request handoff / blocker preservation. **No new scientific work.**
**Statuses in this file are exactly the statuses at remote HEAD `3ea85e36c85b22520e263dc58c6fca8cc0693720`
(= entry state of P12N); nothing was promoted while producing this handoff.**

This file is the single authoritative summary of the external-evidence state. It supersedes nothing:
the governing records remain `P12L_PCR1_G3_FORMAL_BLOCKER_RECORD.md` (rationale) and
`P12L_AUTHOR_DATA_REQUEST_SPEC.md` (data specification). Where this file restates a status, it repeats
the locked value; it does not create one.

---

## 1. Required statements (numbered as required)

1. **Three author requests are prepared but NOT SENT** — B1 (Li et al. 2024, Fig. 2(a)), B2 (Li et al.
   2024, Fig. 2(b)), B3 (Li et al. 2023, Fig. 4(c)), in `paper9/audit/P12M_AUTHOR_REQUEST_DRAFTS.md`.
2. **No author has been contacted** — no message was sent by any channel; recipient identity/contact
   channel is left as a placeholder in each draft.
3. **No benchmark numerical data has been received** for any of B1/B2/B3 — no author-supplied file
   exists in the repository, and `paper9/audit/author_data/` contains **templates with placeholders
   only** (verified: zero numeric values entered).
4. **B1/B2/B3 `quantitative_error` remain NULL** in `audit/benchmark_evidence.json`
   (`B1 = None`, `B2 = None`, `B3 = None`; only `B5` carries a value from source equations).
5. **B1 remains `PARTIAL / GRAPHICAL_ONLY`.**
6. **B2 remains `NOT_VALIDATED / GRAPHICAL_ONLY (l/l_bar AMBIGUITY)`** and the **`l` vs `l̄` ambiguity
   remains unresolved** — no source-authoritative answer has been obtained.
7. **B3 remains `GRAPHICAL_ONLY / PARTIAL`.**
8. **PCR1 = NOT PASS.**
9. **G3 = NOT MET.**
10. **G4 = NOT MET.**
11. **P5 = NOT PASS / OPEN.**
12. **R-1 = OPEN.**
13. **PCR5 = PASS.**
14. **P13 remains BLOCKED.**
15. **No data receipt itself closes any gate** — receipt is an input to a verification sequence, not a
    result; closure requires agreement within the existing thresholds *and* the G3 completeness
    conditions.
16. **Once data are actually received, they must first pass the existing receipt / provenance /
    parameter / normalisation checks before any ≤ 2 % (and, for B1, ≤ 0.5 % classical-limit) numerical
    comparison is performed.**
17. **B2 cannot proceed to numerical acceptance until the `l` vs `l̄` ambiguity is explicitly resolved
    by source-authoritative information** — unresolved ⇒ B2 stays blocked regardless of any data
    supplied.
18. **Do not invent substitute values and do not digitise curves under the current policy** — the
    standing rule (`audit/benchmark_evidence.json`) permits curve digitisation only for overlay
    figures, never for error percentages; no estimation, interpolation or reconstruction of missing
    author tables is admissible.

**Independence note (preserved):** author data can move only the **PCR1 → G3 → G4** chain. It cannot
resolve **P5** (internal parallel-pipeline reconciliation) or **R-1** (pipeline-level reproducibility),
and it does not touch **PCR5** (already PASS) or the governing numerical baseline
(`p = 4.173919246515192`, CI `[3.1453687594104447, 5.202469733619939]`, ε_Δ `4.6318154949690315e-11`).

---

## 2. Package consistency audit (read-only; performed in this phase)

The existing P12M/P12L package was audited against the fourteen required request items and the
eighteen required receipt items. **Result: internally consistent — one note, no correction required.**

| Check | Result |
|---|---|
| All package files present (drafts, spec, blocker record, forensic audit, 3 templates, evidence bundles, P12K/P12M checkpoints, `benchmark_evidence.json`) | 12/12 present |
| Threshold wording agrees everywhere (drafts §4, spec §5, all three templates) | agrees: mandatory **≤ 2 %**, **≤ 0.5 %** classical-limit target for B1 only |
| Threshold wording agrees with the authoritative Blueprint v1.4 (line 457: "≤ 2 % relative (target ≤ 0.5 % in the classical limit)"; line 471 error definition; line 803 G3) | agrees — **no threshold introduced or changed** |
| Request scope per benchmark: draft asks ⊇ P12L spec asks (B1: (x,y) points, first three gap edges, first-four branch frequencies at stated k̄, parameters, normalisation; B2: same + `l`/`l̄`, normalising length, `l₁` convention, coefficient convention, parameter set; B3: (x,y) points, gap edges, `c̄₁`/`d̄₁`/`c_R`/`d_R` actually used, parameters with units, normalisation) | consistent (drafts add "with units" and the Fig. 3(b)-vs-Fig. 4(c) coefficient question — strengthening only, no scope expansion) |
| Receipt templates carry all 18 required items (source identity, date, file name + SHA-256, attribution, figure correspondence, units, normalisation, parameters, boundary/interface conditions, data checksum, solver configuration, comparison result, relative error, acceptance threshold, PCR1 status, + attestation) | 18/18 in each of B1/B2/B3 |
| Templates contain placeholders only (no hypothetical values) | verified: 0 numeric values |
| Acceptance-protocol step order (receipt → provenance → parameter/normalisation → solver run → point comparison → error calculation → criterion → evidence artifact → PCR1 → G3) monotonic in drafts §4 | verified |
| Forbidden content: e-mail addresses, invented recipient names, claims of prior validation, claims of having sent/contacted | none present |
| Explicit "NOT SENT" statement inside the drafts | present |
| Formatting note (non-substantive): drafts phrase B1's first item as "numerical points" where the spec says "(wavenumber, frequency) pairs", and B2's item list says "same completeness as §1" rather than repeating the clause | wording only; meaning identical — the drafts were **not** rewritten (per this phase's instruction) |

---

## 3. Future receipt sequence — DEFINED ONLY, NOT EXECUTED

```
receipt
  → provenance check
  → parameter / normalisation resolution        (B2: l vs l̄ must be resolved here, and only by
                                                 source-authoritative information)
  → machine-readable data integrity check       (hash, re-read, units, conventions)
  → benchmark reconstruction                    (existing solver configuration; author-stated
                                                 parameters only; no tuning)
  → prescribed error calculation                (per-quantity + maximum, relative, existing definition
                                                 e = |ω̄_ours − ω̄_ref| / ω̄_ref)
  → PCR1 reassessment                           (all three mandatory benchmarks)
  → G3 reassessment                             (+ completeness: full error table, per-benchmark
                                                 PASS/FAIL, manuscript evidence, Layer 2c)
  → G4 / P5 downstream reassessment             (G4 = PI act after PCR1–PCR8; P5 and R-1 are
                                                 independent of author data)
```

**Not executed. No step of this sequence has been started or simulated.** Execution requires actual
author-supplied machine-readable data in hand.

---

## 4. Strict NOT RECEIVED / NOT EXECUTED checklist

A future run may change a row **only** when the stated condition is met with actual author-supplied
data. Until then every row stays as recorded below. No row may be changed by inference, estimation,
digitisation or re-reading of published figures.

### B1 — Li et al. 2024, Fig. 2(a) (Layer 1, classical limit)

| # | Item | State |
|---|---|---|
| 1 | Request sent | **NOT SENT** |
| 2 | Author response received | **NOT RECEIVED** |
| 3 | Machine-readable file archived + hashed | **NOT RECEIVED** |
| 4 | Provenance verified | **NOT EXECUTED** |
| 5 | Parameters / normalisation verified | **NOT EXECUTED** |
| 6 | Independent solver run for B1 | **NOT EXECUTED** |
| 7 | Point/gap-edge comparison | **NOT EXECUTED** |
| 8 | Error calculation + criterion (≤ 2 %; ≤ 0.5 % classical target) | **NOT EXECUTED** |
| 9 | `quantitative_error` value | **NULL** |
| 10 | Receipt template completed | **NOT EXECUTED** (placeholders only) |
| 11 | Status | **PARTIAL / GRAPHICAL_ONLY** |

### B2 — Li et al. 2024, Fig. 2(b) (Layer 2a, strain gradient)

| # | Item | State |
|---|---|---|
| 1 | Request sent | **NOT SENT** |
| 2 | Author response received | **NOT RECEIVED** |
| 3 | Machine-readable file archived + hashed | **NOT RECEIVED** |
| 4 | `l` vs `l̄` ambiguity resolved by source-authoritative information | **NOT RESOLVED** (blocking) |
| 5 | Provenance verified | **NOT EXECUTED** |
| 6 | Parameters / normalisation verified | **NOT EXECUTED** |
| 7 | Independent solver run for B2 | **NOT EXECUTED** |
| 8 | Point/gap-edge comparison | **NOT EXECUTED** |
| 9 | Error calculation + criterion (≤ 2 %) | **NOT EXECUTED** |
| 10 | `quantitative_error` value | **NULL** |
| 11 | Receipt template completed | **NOT EXECUTED** (placeholders only) |
| 12 | Status | **NOT_VALIDATED / GRAPHICAL_ONLY (l/l_bar AMBIGUITY)** |

### B3 — Li et al. 2023, Fig. 4(c) (Layer 2b, dipolar gradient)

| # | Item | State |
|---|---|---|
| 1 | Request sent | **NOT SENT** |
| 2 | Author response received | **NOT RECEIVED** |
| 3 | Machine-readable file archived + hashed | **NOT RECEIVED** |
| 4 | Provenance verified | **NOT EXECUTED** |
| 5 | Parameters / normalisation verified (incl. `c̄₁`/`d̄₁` actually used for Fig. 4(c)) | **NOT EXECUTED** |
| 6 | Independent solver run for B3 | **NOT EXECUTED** |
| 7 | Point/gap-edge comparison | **NOT EXECUTED** |
| 8 | Error calculation + criterion (≤ 2 %) | **NOT EXECUTED** |
| 9 | `quantitative_error` value | **NULL** |
| 10 | Receipt template completed | **NOT EXECUTED** (placeholders only) |
| 11 | Status | **GRAPHICAL_ONLY / PARTIAL** |

**Blanket rule applying to all three:** a row may move only on evidence of the kind named in the row —
"NOT RECEIVED" → "RECEIVED (file, SHA-256)" requires the actual file; "NOT EXECUTED" → "EXECUTED"
requires the archived artefact of that step. Receipt alone moves nothing in §1's gate statuses.

---

## 5. Handoff summary

| Question | Answer |
|---|---|
| Are the requests ready to send? | Yes — three separate scoped messages in `P12M_AUTHOR_REQUEST_DRAFTS.md` |
| Have they been sent? | **No.** Sending is a PI act |
| Has any author been contacted? | **No** |
| Has any benchmark data arrived? | **No** |
| Can any gate move now? | **No.** PCR1 NOT PASS · G3 NOT MET · G4 NOT MET · P5 NOT PASS/OPEN · R-1 OPEN · PCR5 PASS |
| What unblocks the chain? | Actual author-supplied machine-readable data for B1, B2, B3 (B2 also requiring the `l`/`l̄` resolution), then the §3 sequence |
| What stays blocked regardless? | **P13** — blocked until the gates it depends on are satisfied |

**Exact next action:** the PI sends the three prepared requests (or decides otherwise). Nothing in
P12N authorises numerical validation, gate reassessment, manuscript edits or P13.
