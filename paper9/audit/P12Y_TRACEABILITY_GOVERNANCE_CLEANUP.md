# P12Y — TRACEABILITY / GOVERNANCE CLEANUP AUDIT

**Phase:** P12Y. **Scope:** audit the two P12X follow-up findings — **P12X-F1** (`traceability_matrix.csv`
row TV1 reads `CLOSED [C]` while the authoritative JSON reads `CLOSED [S]`) and **P12X-F2** (`P12N`
cites Blueprint v1.4 line numbers while v1.5 governs) — and decide for each whether it is a genuine
active inconsistency requiring the smallest byte-minimal correction, a historical record, or a
harmless reference. No scientific state, gate, threshold or numerical result may change; the
Blueprint, manuscript, source PDFs and author-request drafts are off-limits.

| Field | Value |
|---|---|
| Entry SHA (verified) | `7e74063aa452ef6275a1493e5a85cc06b276dcdb` (local = origin = ls-remote; clean tree) |
| Pre-work checkpoint | `798c0132c456f190349b3e84a63b509e2c1e3961` (pushed + verified before any edit) |
| Audit/correction commit | recorded in the P12Y delivery report |
| Final checkpoint | `paper9/audit/RECOVERY_CHECKPOINT_P12Y.md` (final form) |
| Register before / after | `0b508bf7f15dc532b553b951382deaf315e38ebd33ecd5b5d765163bd3f49d38` → `4ce06f024bf41f12688998fd26c2861cf04dd9adaefbab93213d48698e573b04` |

## Part A — recovery

`git fetch` → local `HEAD` = `origin/phase-1-symbolic` = `ls-remote` = `7e74063…`; porcelain empty;
pre-work checkpoint `798c013` pushed and re-verified before any edit; baseline hash snapshot of 524
tracked files taken at entry (`/home/user/p12y_baseline_hashes.txt`).

## Part B — P12X-F1 (TV1 `CLOSED [C]` vs `CLOSED [S]`)

**What the brackets mean (from the governing documentation, not assumed).** Blueprint **v1.5**
(§PCR6 / writing conventions / checklist) defines exactly three parameter-provenance tags:
“[C] cited / [A] analytically defined / [S] assumed-with-justification”, with “Every parameter
carries a provenance tag [C]/[A]/[S]”. The traceability register uses the same three classes in its
`status` column (`CLOSED [C]`, `LOCKED [S]`, `LOCKED [A]`, `PARTIAL [S]`, …), i.e. the bracket is the
**provenance/basis class** of the claim, not a second state word.

**Is the register active?** Yes. `traceability_matrix.csv` is cited as the project's traceability
register by the master plan (`CALC_MASTER_PLAN.md` lines 327/352), the stage-1 blocker audit
(`STAGE1_BLOCKERS_AUDIT.md`), the P10 governance records (`P10_GOVERNANCE_SCOPE_DECISION.md` line 54
— “Complete traceability register tracking 71 blueprint equations, matrices, and paragraphs”;
`P10B`/`P10C`/`P10D`), the P8/P9 release audits and the P11 run record (“Synchronized
`traceability_matrix.json` and `traceability_matrix.csv`”). It was maintained as recently as P12H
(commit `dd42e81`, which appended the A1 registry rows).

**Chronology (git evidence).** The CSV's TV rows were written at `c150c0d` (2026-09-23 06:13:37,
`CLOSED [C]`). The retag to `[S]` was executed by P11D at `df7e26c` (2026-09-23 09:12:21) in the
**JSON** matrix, the TV-resolution addendum (`P3_TV_RESOLUTION.md`: “TV1 is CLOSED with provenance
[S] (inherited / source-derived), NOT [C]”), the P11D remediation audit (“`traceability_matrix.json`
TV1: **CLOSED [C] → CLOSED [S]**”; the listed retag targets are “matrix + addendum + manuscript”)
and the manuscript (“TV1, retagged [C] → [S]”). `git log -S` shows the CSV's TV1 row was never
re-synced.

**Disposition — `CORRECTION REQUIRED` (applied).** The CSV row is a genuine **stale active register
value**: it carries the pre-retag class, contradicting the authoritative JSON, the retag records and
the manuscript. The authoritative current state is `CLOSED [S]` (the Fig. 4(c) panel annotates no
c̄/d̄ values, so the evaluated c̄₁/d̄₁ are *inherited* from Fig. 3(b) — assumed-with-justification —
and “must never be described as author-specified Fig. 4(c) parameters ([C])”).

**Correction (smallest possible): the status cell only** —
`checks PASSED,CLOSED [C],"Section 4.2 …` → `checks PASSED,CLOSED [S],"Section 4.2 …`.
The note cell is left byte-identical: it names the *justification* of the inherited values (source
§4.2 text and Fig. 3(b) caption), which remains true under `[S]`; the full retag rationale lives in
the JSON resolution text. One line changed in the file.

**Post-correction verification**

* no unrelated row changed — hash of the file with the TV1 line removed is unchanged
  (`0407f460…`), and the TV-row class tally is `CLOSED [C]` 3, `CLOSED [S]` 4, `LOCKED [S]` 2,
  `LOCKED [A]` 1, `PARTIAL [S]` 1 (TV1 moved from the first to the second bucket);
* every TV claim shared with the authoritative JSON now carries the same provenance class;
* no benchmark status changed (B1 `GRAPHICAL_VALIDATION`/PASS · B2 `NOT_VALIDATED`/`UNRESOLVED` ·
  B3 `NOT_VALIDATED` with `ESTABLISHED / SOURCE-EQUIVALENT`);
* no gate changed (PCR1 NOT PASS · G3/G4 NOT MET · P5 NOT PASS/OPEN · R-1 OPEN · PCR5 PASS ·
  P13 BLOCKED);
* no numerical field changed; no source-evidence classification was silently *upgraded* — the
  correction moves the row **down** to the class the P11D retag established;
* the other CSV rows that differ from the JSON do so only in the state word (`CLOSED`/`PARTIAL` vs
  `LOCKED`), never in the provenance class → no conflict, not corrected.

## Part C — P12X-F2 (Blueprint v1.4 references)

Every v1.4 occurrence in the live chain, classified with the mandate's categories
(A historical statement of what was audited then / B operative reference that must now point to v1.5
/ C stale wording, valid meaning / D other):

| Location | Text | Class |
|---|---|---|
| `P12N_AUTHOR_DATA_HANDOFF.md` §2 (line 66) | “Threshold wording agrees with the authoritative Blueprint v1.4 (line 457 …; line 471 …; line 803 G3) … agrees — **no threshold introduced or changed**”, inside the section headed “Package consistency audit (read-only; **performed in this phase**)” | **A** (historical check statement) + **C** (the version label is stale, the cited content is unchanged) |
| `P12L_PCR1_G3_FORMAL_BLOCKER_RECORD.md` lines 16/28/174 | quotes “Blueprint v1.4 §10.4, item 1”, the “hard-gate box”, and the path `Paper9_Blueprint_v1.4.tex` as the source of the PCR1/G3 text | **A/C** — the record documents the text in force when the blocker record was written; v1.5 preserves that text |
| `P12O_AUTHOR_DATA_BLOCKER_DECISION.md` line 60 | “Blueprint v1.4 `2ae0b1e8…`, with the P12J correction already recorded” | **A** — historical provenance statement about what was unmodified at that time |
| `traceability_matrix.csv`/`json` row `BP-v1.4` (P12H) | records the A1 amendment as an event (“v1.4 = v1.3 + ONE amendment in section 5.7 …”) | **A** — historical registry row, exactly like `BP-v1.3` |
| `PROVENANCE.md`, `P12R` amendment record, active machine record | v1.5 declared | **current** (below) |

**Governing-version verification.** `paper9/plan/blueprint/PROVENANCE.md` (additive P12R block)
declares `Paper9_Blueprint_v1.5.tex` … **CURRENT governing specification** and v1.4 … **FROZEN,
superseded by v1.5; byte-identical since creation**; the active machine record's `governing_spec`
reads `Paper9_Blueprint v1.5 (A2 graphical-validation route)`. The A2 amendment record states the
thresholds are unchanged (`≤ 2 %`; `0.5 %` classical target) and lists the eight edited blocks
(95, 457, 471, 803, 886–888, 1046 + two insertions); comparing the two frozen copies, the *set* of
percent-values in v1.5 equals v1.4's (`{0.5, 2, 40, 95}` — A2 only adds occurrences of the same
thresholds in its new Section 13). No gate moved: PCR1/G3/G4/P5/R-1/PCR5/P13 are identical before
and after A2 (A2 §6).

**Disposition — `HISTORICAL-ONLY` (no correction).** The occurrences are statements of the state at
their time. The governing amendment itself explicitly classifies them so: A2 §5 —
“`P12K…Q*` remain valid as statements of the state *at their time*; the author-data route they
describe is retained as the higher-tier (quantitative) fallback. Nothing was deleted.” Rewriting
them would falsify history and is forbidden by the mandate. No occurrence is used as an operative
governing pointer for a *current* rule: the live records (`P12P` action gate, `P12Q` PI handoff)
state the gate table and the send authorisation without citing a Blueprint version, and the only
record that *is* authoritative about the current version (PROVENANCE.md + the machine record)
already declares v1.5.

**P12Y-F3 (new observation, reported, not corrected).** The claim register's latest blueprint row is
the P12H A1 row `BP-v1.4`; there is no A2/`v1.5` row (the A1 amendment received four registry rows —
`BP-v1.4`, `PLAN-5i`, `RFIT-1`, `RNAME-1`). This is a *completeness gap*, not a false statement:
v1.5 is registered authoritatively in `PROVENANCE.md`, in the P12R amendment record, and in the
machine record's `governing_spec`. Adding amendment rows is a content addition beyond this phase's
minimal-correction rule, so it is recorded here and left for a separately authorised cleanup.
`paper9/audit/traceability_matrix.csv` row `BP-v1.4` itself is a historical A1 row and was not
altered.

## Part D — active governance consistency

| Record | Blueprint version | Statuses | Gates |
|---|---|---|---|
| active machine record | `governing_spec` = v1.5 (A2) | B1 PASS / B2 `NOT_VALIDATED` + `UNRESOLVED` / B3 `NOT_VALIDATED` + `ESTABLISHED / SOURCE-EQUIVALENT`; `quantitative_error` `[NULL, NULL, NULL]` | PCR1 NOT PASS · G3/G4 NOT MET · P5 NOT PASS/OPEN · R-1 OPEN · PCR5 PASS · P13 BLOCKED |
| `benchmark_evidence.json` | P11D-era registry, no version claim | B1/B2/B3 `quantitative_error = null`; B3 `GRAPHICAL_ONLY / PARTIAL`, provenance `[S] (inherited), never [C]` | — |
| `PROVENANCE.md` | v1.5 CURRENT; v1.4 FROZEN/superseded | — | — |
| A2 amendment record | v1.5 = v1.4 + 8 blocks | “no gate moves because A2 exists” | same as record |
| `P11D_PCR_MAPPING.md` | v1.3-era mapping | PCR1 NOT MET · G3/G4 NOT MET | unchanged |
| `P12N/P12O/P12P/P12Q` | v1.4-era historical (classified A2 §5) | author-data chain unchanged | same gate table |
| traceability register | latest blueprint row `BP-v1.4` (A1, historical) | TV classes now agreed with the JSON | — (P12Y-F3) |

No contradiction: all operative records state B1 PASS, B2 `NOT_VALIDATED`/unresolved, B3
`NOT_VALIDATED` with the formulation established, and the frozen seven-state gate set.

## Part E — source / status hierarchy

No active record confuses: source evidence (raster figures only — Li 2024/2023 release no tables),
analytical validation (Level-1/2 residuals), graphical validation (B1 PASS, on the labelled A2
graphical route), the author-data requirement (B2 `l`/`l̄` + panel geometry; B3 Fig. 4(c) parameter
set/normalisation + curve data — drafts, unsent), historical audit status (P12K–P12W records) and
current gate status. B1 remains graphical validation only; B2 remains unresolved; B3's formulation
is established while its **validation** remains `NOT_VALIDATED`; `quantitative_error` stays
`[NULL, NULL, NULL]` and no percentage error was introduced anywhere (asserted mechanically).

## Part F — correction policy compliance

One byte-minimal correction (the TV1 status cell), no historical record rewritten, no scientific
content touched, Blueprint v1.5 / manuscript / drafts untouched, targeted guards added
(`test_p12y_traceability_cleanup.py`), and the correction recorded here and in the checkpoint.

## Part G — regression (exact counts)

| Run | Result |
|---|---|
| P12Y guards (new file) | **15 passed** |
| targeted set (P12Y + X + W + V + U + S + R) | **105 passed** |
| P12T independent-checks script (standalone; P12T has no pytest file) | 24 boolean assertions: **15 True / 9 False**, output **identical to the committed P12T record**; the 9 are the eight source-extraction artefacts P12T itself documented (whitespace/glyph postfixes in a naive extractor) plus their aggregate flag — the strings are verified present by the normalised-text guards in P12S/P12V |
| named governance guards (P12C + P12H ×2 + P12R + P12S + P12U + P12V + P12W + P12X + P12Y) | **150 passed** (135 before P12Y) |
| full suite `paper9/verification/suite` | **231 passed, 1 skipped** (216P/1S before P12Y) |
| P12J cross-check | **43 checks passed, 0 failed** |

No existing test was weakened; no test deleted.

## Part H — immutability

524 tracked files compared against the entry snapshot → exactly one file changed by this phase
(`traceability_matrix.csv`) plus the new P12Y artifacts. Blueprint v1.4/v1.5, `PROVENANCE.md`, Rule
R-fit, manuscript, production, results, tables, analytic sources, source PDFs, P12S/T/U/V evidence,
the raw P12S/P12U record and the author-request drafts/specification are byte-identical.

## Part I — commit / push / recovery

Audit + correction + guards committed together, pushed, fetched, verified
(local = origin = ls-remote), final checkpoint written, pushed and re-verified; clean tree.
