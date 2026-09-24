# PI decision package — P5 production-gate adoption + R-1 measured-adjudication acceptance

**Package state: `APPROVED / CLOSED` — both decisions authorised by the PI on 2026-09-24 (exact texts in the
two records' §6) and their minimal governance effect applied.** There is no P12-series phase number here and
no audit phase was created. The non-satisfaction statements of both records remain in force in full.

| field | value |
|---|---|
| prepared | 2026-09-24 |
| prepared at HEAD | `ca57a9d55774fadcbe1c5d17bf929fc8fa3ec516` (branch `phase-1-symbolic`, tri-equal verified before preparation) |
| records in this package | `paper9/audit/PI_DECISION_P5_GATE_ADOPTION.md`, `paper9/audit/PI_DECISION_R1_MEASURED_ADJUDICATION.md` |
| authorisation | recorded 2026-09-24 in **each** record's own signature block (PI instruction in the project
context; no wet signature claimed) |
| applied | 2026-09-24 — see each record's §7; **P5 = `PASS`, R-1 = `CLOSED`** |

---

## 1. What the PI is being asked to sign

| # | item | proposed one-line decision | record |
|---|---|---|---|
| 1 | **P5 production gate** — **AUTHORISED (Option A, adopt as written)** | adopt the Part A matrix + P11/P12C Case-C artifacts as the canonical Phase-5 production record and adopt the gate statement **P5 PASS / G5 PASS** (G5 = plan-level study completeness, not a validation gate); no number, Blueprint or validation status changes; B2/B3 remain NOT_VALIDATED | `PI_DECISION_P5_GATE_ADOPTION.md` §1, §6 |
| 2 | **R-1** — **AUTHORISED (Option A, accept and close without re-baseline)** | accept the executed measurement on the deployed 5i configuration under the frozen Rule R-fit (F = 3, unamended) as R-1's criterion of record and close R-1 **without** a re-baseline; governing artifact and all published numbers byte-identical; B2/B3 remain NOT_VALIDATED | `PI_DECISION_R1_MEASURED_ADJUDICATION.md` §1, §6 |

Both proposed decisions are **exactly one sentence each** and are quotable as the decision of record.

## 2. Status matrix — PROPOSED vs APPROVED/CLOSED, and the untouched items

| item | status in this package | basis |
|---|---|---|
| P5 gate adoption | **APPROVED / CLOSED (2026-09-24)** — `gate_state.P5` = `PASS` | PI authorisation, record 1 §6 |
| R-1 measured-adjudication acceptance | **APPROVED / CLOSED (2026-09-24)** — `gate_state.R-1` = `CLOSED` | PI authorisation, record 2 §6 |
| C-1 (5i criterion) | **CLOSED — unchanged**, per the A1 action recorded in `P12AD` §D / `P12AE` §E | nothing; **not reopened, not re-promoted by this package** |
| B1 | **GRAPHICAL_VALIDATION / PASS — unchanged** | — |
| B2, B3 | **NOT_VALIDATED — unchanged** (`quantitative_error` NULL ×3) | external authoritative source data only; no such data exists in-repo |
| PCR1 / G3 / G4 | **NOT PASS / NOT MET / NOT MET — unchanged** | B2/B3 validation, then the PI's signature (G4) |
| submission | **NOT AUTHORISED — unchanged** | — |
| Case-C 43.94 % | **no manuscript change** — it is explicitly the 4×4 result and labelled not-mesh-converged; the optional wording hardening was **not** applied | a separate, explicit authorisation; none sought here |
| historical records | untouched: `P12AB_*` matrix keeps its P12AB-era wording, `P5_TV_RESOLUTION.md` keeps its P5-era OPEN list, `P5_STATUS.md` stays byte-unchanged (`1a410f22…`) | — |

**Approved/closed items in this package: P5 and R-1** (2026-09-24, Option A each). C-1 was closed earlier, by
a different instrument (the A1 action, `P12AD` §D / `P12AE` §E), and is merely reported here.

## 3. Evidence basis (both records rest only on repository content + the executed measurements)

* **P5** — `P12AD` §B (retained-record decision), `P12AE` §C (preserved), the `LOCKED [S]` register entries, the
  S1–S9 completeness picture, and the executed common-point cross-check (bitwise-identical K, M; reduced Bloch
  K, M ≤ 7 × 10⁻¹⁶; spectra ≤ 4.9 × 10⁻¹⁵ outside the Γ zero cluster).
* **R-1** — the executed P12AB Part E measurement (5 realizations, 3 families, 0/5 fit-branch flips; admissible
  subset {4², 8², 16²} invariant in every realization) adjudicated by the frozen rule; the governing artifact is
  untouched.

**Measurement reproducibility.** Both measurements were executed from the repository's own frozen modules
(`paper9/solver/bfs_bloch_solver.py`, `paper9/verification/suite/p4b_5g_to_5i.py`, `p4a_5a_to_5f.py`) on
2026-09-24 at HEAD `ca57a9d…`. Supporting raw artifacts (scripts, logs, JSON) are held outside the repository as
working evidence and are **not** committed by this package; each record states the exact configuration, k-vector,
meshes, tolerances and verdicts, so the measurement can be reproduced from the record alone. If the PI wishes the
raw evidence to become part of the repository record, that is a separate instruction.

## 4. Mandatory non-satisfaction statement (applies to the whole package)

> **This package is a preparation-for-signature step.** It satisfies **none** of PCR1, G3 or G4; it does not
> authorise submission; it changes no scientific number, table, figure, threshold or gate definition; it does not
> amend the Blueprint or Rule R-fit; and **benchmarks B2 and B3 remain `NOT_VALIDATED`**. P13 remains blocked.
> Until the PI signs, P5 remains `NOT PASS/OPEN` and R-1 remains `OPEN`.

## 5. Scope discipline recorded for this package

Not done, by instruction: no new numerical analysis beyond the two specified comparisons; no solver rerun for
results; no manuscript or LaTeX edit; no reopening of C-1; no B2/B3 work, no literature hunt, no searches; no new
audit phase; no change to any historical audit record; no change to any status register. This package adds two
decision records and this index; nothing else.

## 6. Boundary

**Both authorisations have been recorded and applied; the package is closed.** No follow-up audit phase is
proposed and none was created. The standing prohibitions are unchanged: submission is not authorised, PCR1 is
`NOT PASS`, G3/G4 are `NOT MET`, and B2/B3 remain `NOT_VALIDATED`.

## 7. Recovery checkpoint (prepared-state record)

| field | value |
|---|---|
| previous verified checkpoint | `ca57a9d55774fadcbe1c5d17bf929fc8fa3ec516` (P12AI closure; tri-equal) |
| this package's records commit | `d7b985b` — adds exactly the three files of §5 (320 insertions), nothing else |
| working tree at preparation | clean except the pre-existing untracked `paper9/latex/ms.pdf` |
| sandbox `.git` recovery | repository `.git` was restored from the remote (clone → copy `.git` → `git reset HEAD` → `git checkout -- .`) before any edit; `local == origin == ls-remote == ca57a9d` re-verified after restore, and the restored tree was confirmed byte-clean against `HEAD` |
| guard check after adding the records | `pytest` record/consistency guards (`test_p12x`, `test_p12z`, `test_p12y`, `test_p12ad`, `test_p12ae`, `test_p12ab`, `test_p12af`) → **119 passed** |
| push | performed for `d7b985b` (`ca57a9d..d7b985b`) |
| status registers | unmodified: `P5_STATUS.md` `1a410f22…`, `benchmark_validation_record.json` `2fad2d92…`, `rule_rfit.py` `d4fed492…`, Blueprint v1.5 `b96c8e76…` |
