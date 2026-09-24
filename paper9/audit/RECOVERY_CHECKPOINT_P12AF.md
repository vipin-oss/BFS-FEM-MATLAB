# RECOVERY CHECKPOINT — P12AF (final)

**Phase completed:** P12AF — the PI grant of P12AE decisions A–F recorded as an explicit internal act
(2026-09-24), and the scoped manuscript edit authorised by P12AE decision B performed in exactly the two
authorised files. **Branch:** `phase-1-symbolic`. No gate was promoted; no numerical result and no
classification other than the authorised A2 re-tiering changed.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Entry (verified tri-equal, clean) | `8fc80cee5315825ca92c944347c787e053653dd9` (P12AE phase head) |
| Entry P12AE final checkpoint | `a944ac856c05ed54376025c2b6a8fba0020e5e0f` |
| **P12AF pre-work checkpoint** | **`73c7cec3bb181cd50184423b83bb00d10cb429e3`** |
| **P12AF main (audit + correction) commit** | **`7899102c5c41120bf31ec60087582214a13b9ec0`** |
| Immutability baseline | `/home/user/p12af_baseline_hashes.txt` (552 tracked files at `8fc80cee`) |
| Manuscript set hash — entry | `5ba2c22e7e7db2f51ef76f56a1539ff170eb01cd0302c55fa724f7be180ca24b` (12 `.tex`) |
| **Manuscript set hash — after the authorised edit** | **`a934223187f6e78effe1a5caa93e307808f5958f99911c571ba929194022aaec`** |
| Governing Blueprint v1.5 | `b96c8e76…` — **byte-identical** |
| Rule R-fit | `d4fed492…` — **byte-identical** |
| Machine record `benchmark_validation_record.json` | `2fad2d92…` — **byte-identical** |
| `P5_STATUS.md` | `1a410f22…` — **byte-identical** |
| Source PDFs (7) / author-request drafts (P12L, P12M, P12Q) | **byte-identical** |
| Phase record | `paper9/audit/P12AF_MANUSCRIPT_RETIERING_RECORD.md` |

## What changed (exactly)

1. `paper9/audit/P12AE_PI_AUTHORISATION_MANUSCRIPT_PREPARATION.md` — grant recorded: status
   **GRANTED — decisions A–F — recorded 2026-09-24**, in force from the recording date; signature block
   completed as an **internal act by the agent under the PI's explicit instruction conveyed in the project
   context (P12AF), committed to this repository**; PI-name field `Vipin Gupta` with its full provenance
   caveat (owner `vipin-oss` + commit-author identity; no separate PI signature record exists; field
   PI-correctable); ☐ wet/electronic signature **not supplied and not claimed**; pre-grant history retained
   verbatim; order of operations updated (step 1 done, step 2 performed).
2. `paper9/latex/sections/sec05_verification.tex` — the authorised A2 re-tiering (7 substitutions plus the
   limitation paragraph placed after `\end{enumerate}`).
3. `paper9/tables/out/tab03_anchor_errors.tex` — B1 `GRAPHICAL\_VALIDATION / PASS`
   (was `PARTIAL`), B3 `NOT VALIDATED$^g$` (was `PARTIAL`) with new footnote *g*, footnotes *c*/*d*
   re-tiered, caption declares that no percentage is asserted for any graphically compared benchmark;
   B2/B5 rows and all numerical cells byte-identical.
4. Five legacy guards re-pointed to the post-edit manuscript hash (**not** loosened, each annotated):
   `test_p12x_governance_consistency.py`, `test_p12y_traceability_cleanup.py`,
   `test_p12ad_decision_record.py`, `test_p12ae_authorisation_record.py` (pre-grant tests replaced by
   grant-state + no-fabrication tests), `test_p12ac_decision_b.py` (git-scope check).
5. New guards: `paper9/verification/suite/test_p12af_manuscript_retiering.py` (17 guards).
6. `paper9/audit/P12AF_MANUSCRIPT_RETIERING_RECORD.md` (this phase's traceability record) and this
   checkpoint.

## Verification at exit (exact)

| Check | Result |
|---|---|
| Full suite | **334 passed, 1 skipped, 0 failed** (P12AE: 317/1) |
| Traceability (`check_traceability.py`) | **18/18 closed, 0 open** |
| Register provenance | **PASS** — A=0, B=3, C=2, D=0 |
| P12J final verification | **43/43** |
| Compile (build harness in `/tmp` only) | **0 LaTeX errors** pre- and post-edit; overfull 567 → 567 (**no new overfull box**); limitation paragraph renders in the intended location; cross-references and label numbers unchanged |
| Immutability vs `8fc80cee` baseline | **0 files missing; 0 unintended changes** — changed set = exactly the 8 authorised files above; new = this checkpoint, the phase record, the P12AF guard file |
| Pre-existing compile blockers (reported, not fixed) | `ms.tex` `\RaggedRight` without `ragged2e`; text-mode `_`/`^` in generated tables/sections; malformed `\multicolumn` specs in `tab06_convergence_floor.tex` |

## Statuses after P12AF (no promotion)

PCR1 **NOT PASS** · G3 **NOT MET** · G4 **NOT MET** · P5 **NOT PASS / OPEN** · R-1 **OPEN** ·
C-1 closed as a criterion item (Rule R-fit frozen) · PCR5 **PASS** · P13/submission **BLOCKED** ·
B2, B3 **NOT VALIDATED** · B3 formulation **ESTABLISHED / SOURCE-EQUIVALENT** ·
`quantitative_error` null ×3 · external benchmark hunt **permanently CLOSED** ·
author-data route **NOT SENT / NOT AUTHORISED**.

## Next step

Closing B2/B3 still requires the prepared author-data route (P12L/P12M); the hunt stays closed; PCR1
remains the formal blocker; any further stage — including any submission decision — needs its own
authorisation.
