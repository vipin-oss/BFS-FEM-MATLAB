# P12O — Author-Data Blocker Decision Record (final for the preparation stage)

**Phase:** P12O — final blocker decision record.
**Scope:** formally closes the author-data **preparation** stage. No request is sent, no author is
contacted, and **no new scientific validation, calculation, digitisation or measurement is performed.**
**Entry state:** remote HEAD `4dcf91d51d126a165b02d0520d2d2638edf56c33` (verified), tree clean,
pre-work checkpoint `66a46594c117f9ce065b49f0129c71dee6220805` committed, pushed and verified before
this file was written.

This record adds no new governance rule. It states the current state and the permitted future actions.
The governing records remain: `P12L_PCR1_G3_FORMAL_BLOCKER_RECORD.md` (rationale),
`P12L_AUTHOR_DATA_REQUEST_SPEC.md` (data specification), `P12N_AUTHOR_DATA_HANDOFF.md` (handoff,
sequence and checklist).

---

## 1. Required statements

1. **P12M and P12N are complete.**
   P12M content `88961608524d8de51e29ee1662051efdedb3b9df`, final checkpoint
   `3ea85e36c85b22520e263dc58c6fca8cc0693720`; P12N content
   `dbaf1e92d51926adfa9b52873b61712e405c0e1f`, final checkpoint
   `4dcf91d51d126a165b02d0520d2d2638edf56c33`. Both pushed and remote-verified.
2. **Three author-data requests are prepared but NOT SENT** — B1 (Li et al. 2024, Fig. 2(a)),
   B2 (Li et al. 2024, Fig. 2(b)), B3 (Li et al. 2023, Fig. 4(c)), in
   `paper9/audit/P12M_AUTHOR_REQUEST_DRAFTS.md`.
3. **No author has been contacted** by any channel.
4. **No author-supplied numerical benchmark data have been received** for any of B1/B2/B3.
5. **B1/B2/B3 `quantitative_error` remain NULL** in `audit/benchmark_evidence.json`
   (verified in this phase: `B1 = None`, `B2 = None`, `B3 = None`).
6. **B1 = `PARTIAL / GRAPHICAL_ONLY`.**
7. **B2 = `NOT_VALIDATED / GRAPHICAL_ONLY`**; the **`l` vs `l̄` ambiguity is unresolved** — no
   source-authoritative answer has been obtained.
8. **B3 = `GRAPHICAL_ONLY / PARTIAL`.**
9. **PCR1 = NOT PASS.**
10. **G3 = NOT MET.**
11. **G4 = NOT MET.**
12. **P5 = NOT PASS / OPEN.**
13. **R-1 = OPEN.**
14. **PCR5 = PASS.**
15. **P13 = BLOCKED.**

---

## 2. Decision

> ## `AUTHOR-DATA REQUESTS PREPARED — AWAITING PI/AUTHOR ACTION`

**Interpretation limits (binding):**

- Preparation is **not** authorization to send. Sending the three requests is a **PI act**; the agent
  neither sends nor contacts anyone.
- No recipient name, address or channel may be invented; contact details come only from each
  publication's own record.
- No digitisation of published curves and no substitute, estimated, interpolated or reconstructed
  numerical values may be used at any point.
- **Acceptance thresholds are unchanged and unchanged-able**: ≤ 2 % mandatory; ≤ 0.5 % classical-limit
  target for B1 only. No new threshold may be introduced.
- The manuscript and Blueprint are **not** modified beyond what has already been formally incorporated
  (Blueprint v1.4 `2ae0b1e8…`, with the P12J correction already recorded). No estimated benchmark
  errors, no external-validation claims and no "author data received" claims may be inserted.
- **P13 stays blocked.**

---

## 3. Future-state decision table (permitted next actions only)

| Event | Permitted next action |
|---|---|
| No author response | **Preserve PCR1/G3/G4/P5/R-1 blocked statuses**; no proxy, surrogate or substitute evidence |
| Author data received for **B1** | Run provenance / normalisation / integrity checks **first** (hash, re-read, units, conventions, figure correspondence) — before any comparison |
| Author data received for **B2** | **Resolve `l` vs `l̄`** by source-authoritative information **before** numerical validation; unresolved ⇒ B2 stays blocked regardless of data quality |
| Author data received for **B3** | Verify the **actual `c̄₁`, `d̄₁`, `c_R`, `d_R`** parameter set used for Fig. 4(c) **first** (the panel annotates none) |
| Complete acceptable data for all required benchmarks | Reassess **PCR1**, then **G3** (completeness: full error table, per-benchmark PASS/FAIL, manuscript evidence, Layer 2c); **only then** downstream gates (G4 = PI act; P5 and R-1 remain independent) |
| Incomplete / ambiguous data | **Keep the corresponding benchmark blocked**; record the gap; do not extrapolate, digitise or substitute |

**Explicit statement: "Data receipt alone does not close PCR1 or G3."**
Closure requires the full check-and-comparison sequence plus agreement within the existing thresholds,
and for G3 additionally its completeness conditions.

---

## 4. Closing state of the preparation stage

| Question | Answer |
|---|---|
| Requests prepared? | Yes — three scoped, ready-to-send messages |
| Requests sent? | **No** |
| Author contacted? | **No** |
| Data received? | **No** |
| Gates moved? | **No** — PCR1 NOT PASS · G3 NOT MET · G4 NOT MET · P5 NOT PASS/OPEN · R-1 OPEN · PCR5 PASS |
| P13? | **BLOCKED** |
| What happens next? | PI/author action. On arrival of actual data, resume at `P12N_AUTHOR_DATA_HANDOFF.md` §3–§4 with the templates in `paper9/audit/author_data/` |

**Regression at the time of this record:** suite 126 passed / 1 skipped; PCR/gate guard sub-suites
33 passed; manuscript/Blueprint cross-check 43/43; immutability 8/8 anchors. No scientific test changed.
