# P12AF — MANUSCRIPT RE-TIERING RECORD (PI grant recorded 2026-09-24; scoped A2 edit performed)

**Phase:** P12AF · **Branch:** `phase-1-symbolic` · **Entry:** P12AE final checkpoint `8fc80cee`, HEAD
`8fc80cee` (verified tri-equal, clean tree) · **Pre-work checkpoint:** `73c7cec3`.
**Authorisation basis:** `P12AE_PI_AUTHORISATION_MANUSCRIPT_PREPARATION.md` (grant recorded in this phase,
signature block) — decision B; `P12AD_INTERNAL_RECONCILIATION_DECISION.md` §E (limitation text);
`Paper9_Blueprint_v1.5.tex` §13 / amendment A2 (`BLUEPRINT_V1_5_GRAPHICAL_VALIDATION_AMENDMENT.md`);
`P12S_MANUSCRIPT_IMPACT.md` J.1–J.5.
**Scope:** the authorised edit only. No new audit, no literature search, no benchmark hunt, no numerical
rerun, no P5 reconciliation, no R-1 rerun, no C-1 amendment, no gate modification.

---

## 1. Step 1 — the PI grant, recorded as an internal act

`paper9/audit/P12AE_PI_AUTHORISATION_MANUSCRIPT_PREPARATION.md`:

| Element | Change |
|---|---|
| Status line | `PROPOSED — READY TO SIGN — NOT SIGNED — NOT IN FORCE` → **`GRANTED — decisions A–F — recorded 2026-09-24`**, in force from the recording date |
| Pre-grant paragraph | retitled "Recording history"; the pre-grant record of the absence of approval is retained verbatim in substance and marked as the pre-grant history |
| Signature block | `GRANTED` — **☒ GRANT decisions A–F** (in full; partial-grant branch unused) · PI name **Vipin Gupta** · date **2026-09-24** (UTC) · recorded as **☒ internal act recorded in this file by the agent under the PI's explicit instruction conveyed in the project context (P12AF), committed to this repository**; ☐ wet/electronic signature **not supplied, not claimed** |
| Order of operations | step 1 marked **DONE 2026-09-24**; step 2 marked **IN PROGRESS (P12AF)** |

**No signature metadata was fabricated.** The PI-name field carries its provenance in full: the repository
owner account `vipin-oss` and the commit-author identity `Vipin Gupta <vipin@gurugramuniversity.ac.in>`
recorded in this repository's own history. The repository contains **no separate PI signature record** and
the manuscript author block names only "Phase-1/P7 Collaborative Research Team"; nothing beyond that
repository metadata was inferred, and the record states that the field **must be corrected by the PI** if
the formal name differs. The record is not a PI-signed artefact and does not claim to be one.

## 2. Step 2 — the scoped manuscript edit (P12AE decision B), exactly two files

### 2.1 `paper9/latex/sections/sec05_verification.tex` (1 file, 7 substitutions + paragraph placement)

1. **B1 (classical limit)** — now validated under the Blueprint's labelled graphical route (v1.5 §13,
   amendment A2) and **classified `Graphical Validation`**; quantitative solver error stays N/A and **no
   numerical percentage is asserted**.
2. **B2 (Layer 2a)** — **`Not Validated`** under the A2 routes; the length-scale definition remains
   unresolved; no claim is made and the corresponding verification-gate item is not met; **no numerical
   agreement value or error percentage** is claimed; the limitation is a limitation of the published
   parameter/normalisation information, **not** a deficiency of the solver or its verification suite.
3. **B3 (Layer 2b)** — the dipolar-gradient layer matrix is **formulation-equivalent to the source's own
   Appendix 3 form to machine precision**, but that is "a formulation-consistency check and explicitly
   *not* a benchmark validation"; in the absence of published author tables and because the Fig. 4(c)
   parameter set/normalisation are not stated, **B3 is `Not Validated`**; no agreement value or percentage.
4. **New limitation paragraph** — `\paragraph{External Benchmark Coverage.}` inserted in the Layer-2
   subsection **after `\end{enumerate}`** (outside the list), carrying the P12AD §E statement: B1 validated
   by the labelled graphical route with no percentage; B2/B3 **could not be quantitatively or
   authoritatively validated** (published parameter/normalisation information insufficient — Layer 2a
   length-scale definition/units ambiguous; Layer 2b parameter set/normalisation not stated); both reported
   as **not validated**; the corresponding verification gate is **not** claimed as met; **"No numerical
   agreement value and no error percentage is claimed for any of the three benchmarks."**; the
   formulation-consistency check is **not** a validation of the two benchmarks; the limitations reflect
   what the sources published, not any deficiency of the present solver or its verification suite.
5. **Evidence Hierarchy Declaration** — re-tiered: the labelled graphical route is admissible where the
   source supplies the needed information; **B1 satisfies it**; **B2 and B3 remain `Not Validated`**;
   **Gate G3 remains formally NOT MET**; the prepared author-data package is the higher-tier quantitative
   route that would close B2/B3.
6. **Figure 4 caption (a)** — "under the labelled graphical route, with no percentage asserted".
7. **Figure 4 caption (b)** — comparison with the source's Fig. 4(c) is now **`Not Validated`** (was
   "qualitative graphical only").

### 2.2 `paper9/tables/out/tab03_anchor_errors.tex`

| Cell / element | Before | After |
|---|---|---|
| B1 **Status** | `PARTIAL` | **`GRAPHICAL\_VALIDATION / PASS`** |
| B3 **Status** | `PARTIAL` | **`NOT VALIDATED$^g$`** (new footnote) |
| B2 **Status** | `NOT VALIDATED$^e$` | **byte-identical** |
| B5 row | `SOURCE\_EQUATIONS` / `PASS` | **byte-identical** |
| B1/B3 "Ref. Data Type" cells | `GRAPH\_ONLY / EQN$^c$`, `GRAPH\_ONLY$^d$` | **byte-identical** |
| All numerical cells (Level 1/Level 2 errors, computed gap 1) | — | **byte-identical** (guard-asserted) |
| Caption | "quantitative solver error … marked N/A (Graphical Only)" | "…(Blueprint v1.5 §13, amendment A2), quantitative solver error … marked N/A rather than manufactured from pixel digitization, **and no percentage is asserted for any graphically compared benchmark**" |
| Footnote *c* | qualitative graphical comparison, no tables | graphical comparison confirmed under the **labelled graphical route (A2), with no percentage asserted**; authors published no numerical tables |
| Footnote *d* (B3) | "qualitative graphical comparison only" | raster comparison **for audit only**; **NOT validated** (published parameter/normalisation information insufficient); percentage withheld per the evidence hierarchy |
| Footnote *f* | unchanged | **byte-identical** |
| Footnote *g* | — | **new**: B3 is NOT externally validated (source publishes no numerical curve data; Fig. 4(c) parameter set/normalisation not stated); the reproduction is formulation-equivalent to the source's own Appendix 3 form to machine precision, but that is a **formulation-consistency finding, not a validation**; no agreement value or percentage is claimed for B3 |

**No numeric value, no error figure, no percentage and no benchmark classification other than the
authorised A2 re-tiering was introduced or altered anywhere.**

## 3. Guard re-pointing (pins that asserted the pre-edit bytes)

The five guards below pinned the pre-edit manuscript set hash (`5ba2c22e…`). The authorised edit changes
it; each pin was **re-pointed to the post-edit value** (`a9342231…`), never deleted or loosened, and each
edit is annotated in the file. Assertions that stated a *historical* phase fact (e.g. the P12AC record
containing `5ba2c22e`) were left untouched, because those records were not edited:

* `test_p12x_governance_consistency.py` — pin re-pointed; the manuscript-scope test now asserts the
  re-tiered wording (B1 `Graphical Validation`, B2/B3 `Not Validated`, no `GRAPHICAL ONLY / PARTIAL`,
  G3 still `NOT MET`, no percentage).
* `test_p12y_traceability_cleanup.py` — pin re-pointed.
* `test_p12ad_decision_record.py` — pin re-pointed.
* `test_p12ae_authorisation_record.py` — pin re-pointed; the three pre-grant tests replaced by grant-state
  tests (granted/in force; **no signature or metadata fabricated**; the scoped edit performed by the
  recording phase).
* `test_p12ac_decision_b.py` — the git-based "untouched" check now asserts that the only manuscript path
  differing from HEAD is the P12AF-authorised file.

New phase guards: `paper9/verification/suite/test_p12af_manuscript_retiering.py` (17 guards) — scope of the
diff, table re-tiering, byte-identity of the B2/B5 rows and of every numerical cell, absence of any
percentage, limitation-paragraph placement outside the enumerate, absence of promotion wording, grant
recording, frozen artefacts/sources/author-request files, and that the pins moved rather than vanished.

## 4. Compilation verification (harness only — no repository byte changed for build repairs)

The repository does not compile as-is because of **pre-existing** defects that this phase is not
authorised to touch and did **not** touch: `paper9/latex/ms.tex` lines 14–15 use `\RaggedRight` without
loading `ragged2e`, several generated tables/sections contain text-mode `_`/`^`, and
`tab06_convergence_floor.tex` has malformed `\multicolumn` specs. A build harness was therefore assembled
**in `/tmp` only** (ms.tex preamble + `\RequirePackage{ragged2e}` + the two edited files, plus temporary
copies of the other generated files with escape-only repairs).

| Build | Errors | Overfull | Underfull | Pages |
|---|---|---|---|---|
| harness, **pre-edit** bytes (`/tmp/sec05.before`, `/tmp/tab03.before`) | 0 | 567 | 27 | 8 |
| harness, **post-edit** bytes (working tree) | 0 | 567 | 27 | 9 |

* **Zero LaTeX errors** in both builds; the edited files introduce **no new error**.
* **Overfull-box count unchanged (567 → 567): no new overfull box is attributable to the edit.** Two
  pre-existing overfull boxes in Table `tab:anchor_errors` (the fixed-width `tabular` already exceeds the
  text width in the pre-edit revision: 173.2 pt) widen to 243.3 pt because the mandated status identifiers
  (`GRAPHICAL_VALIDATION / PASS`, `NOT VALIDATED`) are longer than the superseded word `PARTIAL`. This is
  an unavoidable consequence of the authorised wording; it is disclosed here and is **not** a new box.
* Cross-references resolve: `\ref{fig:benchmark_validation}` and `\ref{tab:anchor_errors}` are unchanged;
  the label/numbering set of the edited document is identical (`figure.1`, `equation.2`, …) — only the
  figure-caption text and page positions differ.
* The limitation paragraph renders in the intended location (Layer-2 subsection, after the B1–B3 list);
  verified in the harness PDF text.

## 5. Verification performed (all counts exact)

| Check | Result |
|---|---|
| Full suite `paper9/verification/suite` | **334 passed, 1 skipped** (P12AE: 317 passed, 1 skipped; +17 P12AF guards; 0 failures) |
| New P12AF guards | 17 passed |
| Traceability audit (`check_traceability.py`) | **18/18 CLOSED/LOCKED, 0 open** |
| Register provenance (`check_register_provenance.py`) | **PASS** — A=0, B=3, C=2, D=0 (unchanged) |
| P12J final verification | **43/43 checks passed** |
| Immutability vs baseline `/home/user/p12af_baseline_hashes.txt` (552 files at `8fc80cee`) | **0 missing**; changed = exactly the 8 authorised files (grant record, sec05, tab03, 5 re-pointed guards); new = `RECOVERY_CHECKPOINT_P12AF.md`, this record, the P12AF guard file |
| Numerical results | unchanged (no solver, result, table-value or figure byte touched; guard-asserted) |
| Benchmark classifications | unchanged except the authorised A2 re-tiering (B1 → `GRAPHICAL_VALIDATION` / PASS; B2/B3 `NOT_VALIDATED`) |
| Blueprint v1.5 / v1.4 / v1.3, Rule R-fit, `P5_STATUS.md`, `p4b_5g_to_5i.json/.txt` | byte-unchanged |
| Source PDFs (7) and author-data request drafts (P12L/P12M/P12Q) | byte-unchanged; nothing sent, no author contacted |
| Machine record `benchmark_validation_record.json` | byte-unchanged (`2fad2d92…`): B1 `GRAPHICAL_VALIDATION`/PASS, B2/B3 `NOT_VALIDATED`, B3 formulation `ESTABLISHED / SOURCE-EQUIVALENT`, `quantitative_error` null ×3 |

## 6. Statuses preserved (explicitly — no promotion)

| Item | State after P12AF |
|---|---|
| PCR1 | **NOT PASS** |
| G3 | **NOT MET** |
| G4 | **NOT MET** |
| P5 | **NOT PASS / OPEN** |
| R-1 | **OPEN** |
| C-1 | closed as a criterion item under the frozen Rule R-fit |
| PCR5 | **PASS** |
| P13 / submission | **BLOCKED / NOT AUTHORISED** |
| B2, B3 | **NOT VALIDATED** |
| External benchmark hunt | **permanently CLOSED** |

No wording introduced by this phase claims that validation passed, that PCR1 passed, that G3 is met, that
G4 is cleared, or that submission is authorised. The re-tiering is disclosed transparently as a labelling
of evidence quality under the A2 routes, not as a gate promotion.

## 7. Hashes

| Artefact | Pre-edit | Post-edit |
|---|---|---|
| Manuscript set (`paper9/latex/**/*.tex`, sha256 of concatenated per-file sha256, sorted) | `5ba2c22e7e7db2f51ef76f56a1539ff170eb01cd0302c55fa724f7be180ca24b` | **`a934223187f6e78effe1a5caa93e307808f5958f99911c571ba929194022aaec`** |
| `sec05_verification.tex` | (pre-edit blob `8aeed62`) | `bfd45dd077e7cc4c542fef3fb3d24f89e1c1ea7958bf5052a97fb86b36d507c1` |
| `tab03_anchor_errors.tex` | (pre-edit blob, backup `/tmp/tab03.before`) | `77fd75844415869f0ce94c720af38b7370635b004640591f69ce42fa5de5c113` |

## 8. Outstanding (unchanged by this phase)

* Closing B2/B3 still requires the prepared author-data route (P12L/P12M) — **NOT SENT / NOT AUTHORISED**;
  the external benchmark hunt stays permanently closed.
* PCR1 remains the formal blocker; G3/G4 remain unmet; P5 remains not pass/open; R-1 remains open.
* Submission remains prohibited. Any further stage requires its own authorisation.
