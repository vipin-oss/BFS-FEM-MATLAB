# PI DECISION — AMENDMENT A3 (Blueprint v1.5 → v1.6)

**Status:** **AUTHORISED (OPTION A)** — recorded 2026-09-25
**Repository:** `vipin-oss/BFS-FEM-MATLAB` · **Branch:** `phase-1-symbolic`
**Entry HEAD:** `170fd1d15d74fa21e32da2b0ed06ccb26adb8bc8` (verified; tree clean)
**Governing specification at entry:** `Paper9_Blueprint v1.5 (A2 graphical-validation route)`
**Blueprint v1.5 sha256:** `b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91`
**Authorising instrument:** `PI_AUTHORISATION_A3_DRAFT.md` (decision package, §0–§7)

---

## 1. Authorisation text (recorded verbatim)

> "I authorise Blueprint amendment A3, creating a new frozen version v1.6 from v1.5, with the scope of
> §2 and subject to the five mandatory conditions of §3 and the preservation clauses of §4. B2 and B3
> remain `NOT_VALIDATED`. This is a governance/Blueprint-tier act only: it changes no numerical result,
> no threshold, no evidence hierarchy, no production artefact and no scientific claim, and **it does not
> by itself promote any gate or authorise journal submission** — G4 remains a separate PI signature act
> under §10.3, and P13/submission remains a separate PI decision."

**Minimum recordable sentence (P12AD §G item 1 form):**

> *"PI authorises Blueprint amendment A3 (v1.5 → frozen v1.6), re-scoping the consequence of the
> source-insufficient and disclosed `NOT_VALIDATED` state, subject to conditions A3.1–A3.5; B2 and B3
> remain `NOT_VALIDATED`; no threshold, route definition, numerical result, figure, table or scientific
> claim changes; no gate is promoted by this act; G4 and P13/submission remain separate PI decisions."*

No wet or electronic signature is claimed; this record records the PI's decision as given.

## 2. Scope actually implemented (exhaustive)

A3 changes **only the consequence** of the already-defined evidence state (c) `NOT_VALIDATED`, and
**only for the sub-case in which the insufficiency is source-side and disclosed**, from "fails G3/PCR1"
to "does not of itself fail PCR1 item 1 / G3, subject to A3.1–A3.5".

| # | Location in v1.5 | Change |
|---|---|---|
| 1 | §13 A2.1(c), L1077–1079 | State (c) retained verbatim with its general consequence; an *unless* clause added for a benchmark satisfying all of §13 A3, retained in the same `Not validated` state and not of itself failing the item. |
| 2 | §13 A2.7, row 3, L1137 | Split: *source-insufficient with all A3 conditions satisfied* (item not failed by that benchmark alone) versus *not attempted, or not reproduced for a reason other than source insufficiency* (retains the original consequence). |
| 3 | G3 hard-gate criterion row, L457 | One conditional sentence appended after "…and fails this gate". |
| 4 | PCR1 item 1, L886–890 | The same conditional inserted after "…and this item fails". |
| 5 | New §13 A3 | The five mandatory conditions A3.1–A3.5 and an express "No automatic promotion" clause. |

Implementation form follows the A2 precedent (`BLUEPRINT_V1_5_GRAPHICAL_VALIDATION_AMENDMENT.md` §2):
a new frozen file `paper9/plan/blueprint/Paper9_Blueprint_v1.6.tex`; **v1.5 preserved byte-identical**;
a frozen amendment record; and a new row in `plan/blueprint/PROVENANCE.md`.

**A3 introduces no new evidence route, no new benchmark and no new validation requirement.**

## 3. The five mandatory conditions (all must hold; none may be waived)

- **A3.1 — A validated benchmark exists.** At least one mandatory external benchmark (Layers 1, 2a, 2b)
  is validated by an admissible higher route. *Satisfied: B1 = `GRAPHICAL_VALIDATION` / PASS.*
- **A3.2 — Explicit, everywhere.** The `NOT_VALIDATED` state is stated explicitly, per benchmark, in the
  main manuscript **and** in every active artefact. No artefact may imply that B2 or B3 is validated.
- **A3.3 — No numerical claim.** No relative error, percentage, bound, digitised value or inferred
  number is claimed. The three `quantitative_error` fields remain `null`. A2.5 unchanged.
- **A3.4 — Source-side attribution recorded.** Reason recorded as source-side, with the
  formulation-consistency evidence retained: **B3** — layer matrix ≡ source Appendix 3
  (`ESTABLISHED / SOURCE-EQUIVALENT`); **B2** — the `l` versus `l̄` ambiguity stands unresolved and is
  **not** silently resolved. A2.4 unchanged.
- **A3.5 — Higher-tier route retained.** The P12L/P12M author-data request package is retained as the
  higher-tier quantitative route; if data arrive, the benchmark must then meet ≤2 % (B1: ≤0.5 %
  classical) exactly as before. Authorising A3 does **not** authorise sending anything.

## 4. Preservation clauses (unchanged by A3; violation voids the authorisation)

1. **B2 and B3 remain `NOT_VALIDATED`**; `quantitative_error` stays `null`. B1 stays
   `GRAPHICAL_VALIDATION` / PASS. No benchmark is promoted.
2. **Thresholds unchanged:** ≤2 % mandatory; ≤0.5 % classical-limit target.
3. **Evidence hierarchy unchanged** (A2.3). No route definition changes; no evidence is added.
4. **A2.4, A2.5, A2.6 unchanged**, including the fixed route identifiers.
5. **Rule R-fit unchanged:** `rule_rfit.py` sha256
   `d4fed49241bc3f741fead6d615d966e41f8690f82c07d0ae25705aedc51bd0d8`.
6. **ε_Δ unchanged:** `4.63e-11` (frozen `4.6318154949690315e-11`).
7. **All numerical results and artefacts unchanged:** the n = 16 production set and its pinned
   sha256 values; the n = 8 comparison leg; Figures 1–14; Tables 1–7; every manuscript number.
8. **Source immutability unchanged:** Li 2024 PDF `2ac5f45d…`, Li 2023 PDF `3f510338…`,
   `manuscript_modified: false`, `author_contact: NONE`.
9. **Author-data route:** NOT SENT / NOT AUTHORISED. A3 neither sends nor authorises sending.
10. **Historical records are not rewritten:** P12AA/P12AB matrices and P12N/P12O/P12P/P12Q keep their
    own values verbatim.

## 5. Machine-record effect

| Record | Field | Before | After implementation |
|---|---|---|---|
| `audit/benchmark_validation_record.json` | `governing_spec` | v1.5 (A2 route) | v1.6 (A2 route; A3 source-insufficient disposition) |
| idem | `gate_state.PCR1` | `NOT PASS` | `PASS` (reassessed under v1.6 §13 A3) |
| idem | `gate_state.G3` | `NOT MET` | `MET` (reassessed under v1.6 §13 A3) |
| idem | `gate_state.G4` | `NOT MET` | **`NOT MET` — unchanged** |
| idem | `gate_state.P13` | `BLOCKED` | **`BLOCKED` — unchanged** |
| idem | `benchmarks.B2.route`, `B3.route` | `NOT_VALIDATED` | **`NOT_VALIDATED` — unchanged** |
| idem | `quantitative_error` (B1/B2/B3) | `[null, null, null]` | **`[null, null, null]` — unchanged** |
| Manuscript | two "Gate~G3 remains formally NOT MET" sentences | true | corrected (bookkeeping only) |

## 6. Separate decisions — NOT made by this authorisation

| Decision | State |
|---|---|
| **A3 (Blueprint amendment)** | **AUTHORISED** — this record |
| **G4 (PI signature under §10.3)** | **NOT MADE** — G4 remains `NOT MET` |
| **P13 / journal submission** | **NOT MADE** — P13 remains `BLOCKED`; submission is not authorised |

**This record is not a submission authorisation and must never be cited as one.**
