# Blueprint v1.6 — AMENDMENT A3: SOURCE-INSUFFICIENT BENCHMARKS

**Date:** 2026-09-25 · **Branch:** `phase-1-symbolic`
**Entry HEAD:** `170fd1d15d74fa21e32da2b0ed06ccb26adb8bc8`
**Authorisation:** `paper9/audit/PI_DECISION_A3_AMENDMENT.md` (Option A, PI-authorised)
**Frozen artefacts:** `Paper9_Blueprint_v1.6.tex`
`de46c3bb823bdd1472c07b6c96d4c4b39c967617823e667ebdce99101a8d58ff`
**Immutability:** `Paper9_Blueprint_v1.5.tex` `b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91`
(byte-identical), `Paper9_Blueprint_v1.4.tex` `2ae0b1e8f37e10a0685a0b0ffd94e695bd62e3b4da6a02052a76190fc0acb638`
(byte-identical).

---

## 1. Why A3 was needed

Under v1.5 a mandatory benchmark whose published information is insufficient to reproduce it stands in
evidence state (c) of §13 A2.1 and, by A2.1(c) and the third row of the A2.7 decision table, **fails PCR1
item 1 (v1.5 lines 886–890) and the G3 hard gate (v1.5 line 457)**. B2 (Layer 2a) and B3 (Layer 2b) are
in that state for **source-side** reasons only. The chain §10.4 → G3 ("If it fails: Do not submit") →
§10.3 ("A failed PCR blocks submission exactly as G3 does") therefore makes PCR1 unmeetable without data
that exist only in the authors' hands. A3 removes that unmeetable condition; it does not and cannot
supply the missing evidence.

## 2. The delta (v1.5 → v1.6) — five blocks, exhaustive

| # | Location | Change |
|---|---|---|
| 1 | §13 A2.1(c) | State (c) retained verbatim and its general consequence retained; an *unless* clause added for a benchmark satisfying all of Section 13 A3, which is retained in the same \textsc{Not validated} state and does not of itself fail the item. |
| 2 | §13 A2.7, third decision-table row | Split into two rows: *source-insufficient with all A3 conditions satisfied* (item not failed by that benchmark alone) and *not attempted, or not reproduced for a reason other than source insufficiency* (retains the original consequence). |
| 3 | G3 hard-gate criterion row (v1.5 line 457) | One sentence appended, conditional on Section 13 A3. |
| 4 | PCR1 item 1 (v1.5 lines 886–890) | One clause inserted, conditional on Section 13 A3. |
| 5 | New §13 A3 | The five mandatory conditions A3.1–A3.5 and an express "No automatic promotion" clause. |

A3 **creates no evidence route, admits no new kind of evidence, adds no benchmark and adds no validation
requirement.** It defines only the consequence, for PCR1 and G3, of a benchmark whose validating
information cannot be obtained from the published record.

## 3. Promotion status — no gate moves because A3 exists

| Item | Before A3 | On authorisation of A3 alone |
|---|---|---|
| PCR1 | NOT PASS | **unchanged** (reassessed only under §5 below) |
| G3 | NOT MET | **unchanged** (reassessed only under §5 below) |
| G4 | NOT MET | **NOT MET** — separate PI signature (§10.3) |
| P13 | BLOCKED | **BLOCKED** — separate PI decision |
| B1/B2/B3 `quantitative_error` | NULL ×3 | **NULL ×3** |
| B2 / B3 route | NOT_VALIDATED | **NOT_VALIDATED** |

## 4. Non-modification record (verified)

| Artefact | Requirement | Result |
|---|---|---|
| Blueprint v1.4 | byte-identical | `2ae0b1e8…` ✔ |
| Blueprint v1.5 | byte-identical | `b96c8e76…` ✔ (all v1.5 hash/immutability guards retained unchanged) |
| Rule R-fit `rule_rfit.py` | unchanged | `d4fed492…` ✔ |
| Thresholds (2 % / 0.5 %) | unchanged | ✔ (code and Blueprint) |
| `benchmarks.B2.route` / `B3.route` | `NOT_VALIDATED` | ✔ unchanged |
| `quantitative_error` (B1/B2/B3) | `null` ×3 | ✔ unchanged |
| `source_immutability` | `manuscript_modified: false`, `author_contact: NONE` | ✔ unchanged |
| Author-data package (P12L/P12M) | present, NOT SENT | ✔ unchanged; nothing sent, no author contacted |
| Historical records: P12AA / P12AB matrices, P12N / P12O / P12P / P12Q | not rewritten | ✔ unchanged |
| All production results, Figures 1–14, Tables 1–7, n = 16 artefacts | unchanged | ✔ |

## 5. Reassessment of PCR1 and G3 under A3 (recorded after v1.6)

Performed against A3.1–A3.5 with repository evidence. **All five conditions hold:**

| Condition | Evidence |
|---|---|
| **A3.1** — ≥1 mandatory benchmark validated by a higher route | B1 `route = GRAPHICAL_VALIDATION`, `graphical_validation = PASS` |
| **A3.2** — \textsc{Not validated} stated explicitly | Record routes B2/B3 = `NOT_VALIDATED`; §5 text "Benchmarks~B2 and B3 remain \textsc{Not Validated}"; Table 3 rows B2/B3 marked NOT VALIDATED with footnotes (d), (e), (g) |
| **A3.3** — no numerical claim | `quantitative_error = [null, null, null]`; §5 "no percentage is attached to any graphically compared benchmark"; Table 3 marks the quantitative error N/A |
| **A3.4** — source-side attribution recorded | B3 `formulation_status` = "ESTABLISHED / SOURCE-EQUIVALENT…"; B2 length-scale ambiguity recorded as unresolved (Table 3 footnote (e)); `author_contact = NONE` |
| **A3.5** — higher-tier route retained | `P12L_AUTHOR_DATA_REQUEST_SPEC.md` and `P12M_AUTHOR_REQUEST_DRAFTS.md` present; `P12O` records NOT SENT; nothing sent by this phase |

**Outcome recorded:** `gate_state.PCR1: NOT PASS → PASS` and `gate_state.G3: NOT MET → MET`, as a
reassessment under v1.6 §13 A3 and **not** as a promotion by the amendment itself (A3's own
"No automatic promotion" clause). The `gate_state.blocker` string continues to record that B2 and B3
remain `NOT_VALIDATED` for source-side data gaps.

**`gate_state.G4` remains `NOT MET`** (PI signature not given under §10.3) and **`gate_state.P13`
remains `BLOCKED`** (submission decision not made). **Submission is not authorised.**

## 6. Manuscript consequence (bookkeeping only)

Two sentences asserting "Gate~G3 remains formally NOT MET" (`sec05_verification.tex`,
`sec08_discussion.tex`) became stale once G3 was reassessed as MET. Both are corrected to the state
actually achieved. The §5 limitation wording for B2/B3 (P12AD §E) is **retained verbatim**; no other
manuscript text, number, figure or table is touched.

## 7. Reproduction

```python
import hashlib, difflib
from pathlib import Path
a = Path("paper9/plan/blueprint/Paper9_Blueprint_v1.5.tex").read_text().splitlines(keepends=True)
b = Path("paper9/plan/blueprint/Paper9_Blueprint_v1.6.tex").read_text().splitlines(keepends=True)
print(len([o for o in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes() if o[0]!="equal"]),
      "blocks (expect 5)")
print(hashlib.sha256(Path("paper9/plan/blueprint/Paper9_Blueprint_v1.5.tex").read_bytes()).hexdigest())
```
