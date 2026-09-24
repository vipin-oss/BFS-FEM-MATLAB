# RECOVERY CHECKPOINT — P12AE (final)

**Phase:** P12AE — PI authorisation and manuscript transition (authorisation record prepared; no
manuscript edit). **Branch:** `phase-1-symbolic`. **Status:** complete.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Entry: P12AD final checkpoint | `8d93d3fd6c37bb5f39facad6254d51ec87df6de5` |
| Entry HEAD (verified tri-equal) | `cd5fa0c229807a2a3e7e45efcb7e0aac8f967b23` |
| **P12AE pre-work checkpoint** | `347ef731957176be818f7a2e77a25f8c2def8d84` |
| **P12AE main commit** | `29270ab189181a74a537675cf821a2aa480373fb` |
| **P12AE final checkpoint** | `a944ac856c05ed54376025c2b6a8fba0020e5e0f` — the commit that first committed this file (a later bookkeeping commit updating this row is not a change of state); the phase head SHA is reported in the P12AE phase report and is verified tri-equal |
| Entry immutability baseline | `/home/user/p12ae_baseline_hashes.txt` (549 tracked files at entry) |
| Immutability result | **changed = 0, removed = 0**; added: the authorisation record, its guard suite, this checkpoint |
| Manuscript | **byte-identical** (set `5ba2c22e…`) — **no manuscript edit was made in this phase** |
| Blueprint v1.5 | `b96c8e76…` byte-identical |
| Rule R-fit | `d4fed492…` byte-identical |
| Machine record | `benchmark_validation_record.json` `2fad2d92…` byte-identical |
| Register | JSON `83ff8723…` / CSV `8d86528f…`; 18/18 closed; provenance A=0/B=3/C=2/D=0 |

## What P12AE produced

One instrument: `paper9/audit/P12AE_PI_AUTHORISATION_MANUSCRIPT_PREPARATION.md` — **status PROPOSED /
READY TO SIGN / NOT SIGNED / NOT IN FORCE**, containing exactly:

* **A** — `AUTHORISE P13 MANUSCRIPT-PREPARATION TRANSITION ONLY`; not a PCR1/G3/G4 pass; no submission;
* **B** — the scoped manuscript editing (insert the P12AD §E limitation statement; perform the A2
  re-tiering per `P12S_MANUSCRIPT_IMPACT.md` J.1–J.5; preserve B2/B3 `NOT_VALIDATED`; preserve B3
  `ESTABLISHED / SOURCE-EQUIVALENT`; state no numerical agreement/error percentage for B2/B3; state the
  limitation is source-data/parameter availability, not solver failure), bounded to
  `paper9/latex/sections/sec05_verification.tex` + the `tab03_anchor_errors.tex` status cells, with the
  no-percentage and byte-minimal bounds;
* **C** — P5 preserved exactly as P12AD recorded (retained record = Part A matrix; P5 PASS gate sentence
  **not** adopted; P5 remains `NOT PASS/OPEN`; `P5_STATUS.md` untouched);
* **D** — R-1 preserved (`OPEN` as an internal governance item; **no rerun, no re-baseline**);
* **E** — C-1 preserved (closed as a criterion item under the frozen Rule R-fit; **no amendment**);
* **F** — the exact non-satisfaction sentence.

The instrument is **inert** until the PI records a granting (signature block or an equivalent PI-authored
decision entry); the agent did not sign it, complete it or infer consent. No explicit PI approval for this
transition exists in the repository (`P12Q` Option A/B neither selected; `P12P` "no explicit PI
authorization"; `P12AD` §F).

## Verification (exact counts)

| Check | Result |
|---|---|
| `test_p12ae_authorisation_record.py` (new guards) | **17 passed** |
| Full suite `paper9/verification/suite` | **317 passed, 1 skipped, 0 failed** |
| `check_traceability.py` | 18/18 CLOSED/LOCKED, 0 open |
| `check_register_provenance.py` | PASS — A=0 / B=3 / C=2 / D=0 |
| Immutability vs entry (549 files) | 0 changed / 0 removed / 3 added (all P12AE) |
| Manuscript | 0 bytes changed |

## State after P12AE

Local = origin = ls-remote (verified at every push); working tree clean. Nothing scientific moved:
benchmark classifications, PCR1/G3/G4, P5, R-1, C-1, thresholds, routes, gate definitions and numerical
results are exactly as P12AD left them. **The next phase — and only if the PI grants decisions A–F — is
the scoped manuscript editing; it is not this phase.** Submission remains prohibited while PCR1 fails and
G3 is unmet.
