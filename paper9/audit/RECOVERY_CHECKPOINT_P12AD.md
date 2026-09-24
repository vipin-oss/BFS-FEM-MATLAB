# RECOVERY CHECKPOINT — P12AD (final)

**Phase:** P12AD — internal reconciliation and transition decision. **Branch:** `phase-1-symbolic`.
**Status:** complete; all P12AD artefacts committed and pushed; manuscript and every frozen artefact
byte-unchanged.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| **Entry SHA (verified tri-equal at start)** | `37f71865b9414a25d915524bae2c32060c5536ae` (P12AC final) |
| **P12AD pre-work checkpoint** | `a80d96c2ebd3e326ada8d10d70fd7b7bced9293e` |
| **P12AD main commit** | `5e574febc603ba942ff6558737146f0069247e58` |
| **P12AD final checkpoint** | *(this file's commit — see the phase report / `git log -1`)* |
| Entry immutability baseline | `/home/user/p12ad_baseline_hashes.txt` — 546 tracked files at entry |
| Immutability result | **changed = 0, removed = 0**; added = this record + guard suite + this checkpoint |
| Governing Blueprint | **v1.5** `b96c8e76…` — byte-identical |
| Manuscript | **byte-identical** (set `5ba2c22e…`; 12 `.tex` files under `paper9/latex/`) — no edit made |
| Governing 5i artefact | `p4b_5g_to_5i.json` `38384363…`; rate `4.173919246515192`, CI `[3.1453687594104447, 5.202469733619939]`, `ε_Δ 4.6318154949690315e-11` — byte-identical |
| Machine record | `paper9/audit/benchmark_validation_record.json` `2fad2d92…` — byte-identical |
| Register | JSON `83ff8723…`; CSV `8d86528f…`; 18/18 closed-locked; provenance A=0 / B=3 / C=2 / D=0 |
| P5 record | retained: `results/raw/p5_production_raw.json` `0af7445a…` + `results/processed/p5_production_highlights.json` `ce28df21…` (commit `15814972…`, `param_hash 09dd73f4…`) |

## What P12AD decided (all recorded in `P12AD_INTERNAL_RECONCILIATION_DECISION.md`)

* **§A — statuses unchanged, nothing relabelled:** B1 `GRAPHICAL_VALIDATION`/PASS; B2 `NOT_VALIDATED`
  (source-limited); B3 `NOT_VALIDATED` + formulation `ESTABLISHED / SOURCE-EQUIVALENT`;
  `quantitative_error` NULL ×3; PCR1 `NOT PASS`; G3 `NOT MET`; G4 `NOT MET`; P5 `NOT PASS/OPEN`;
  R-1 `OPEN`; PCR5 `PASS`; P13 `BLOCKED`; author-data route NOT SENT / NOT AUTHORISED.
* **§B — P5:** the retained numerical production record is the Part A matrix (only complete matrix; its
  conventions are the registered ones; no manuscript claim depends on it; Rule R-fit untouched). The
  Part-A *gate statement* is **not** adopted — that sentence remains a PI act; P5 therefore stays
  `NOT PASS/OPEN` and `P5_STATUS.md` stays byte-unchanged. PCR1/G3/G4 preserved exactly.
* **§C — R-1:** the authorised rerun is **not necessary for the manuscript**; the governing artefact is
  retained, R-1 stays open as an internal governance item, and the specified P12AB Part E rerun remains
  the minimum action that would establish property B. **No numerics run; no re-baseline.**
* **§D — C-1:** criterion item closed under the governing frozen Rule R-fit (adopted under A1); the
  residual estimator/Blueprint model defect is documented as a limitation the manuscript already carries.
  Rule R-fit unchanged; the P1–P4 proposal stays non-governing.
* **§E — limitation text:** exact publication-appropriate statement for B2/B3 (B1 graphical; B2/B3 not
  quantitatively/authoritatively validated because required parameter/curve information is unavailable or
  ambiguous; B3 formulation independently established as source-equivalent; source-data limitations, not
  solver failure; no quantitative error percentage) — text delivered, **manuscript not edited**.
* **§F — P13:** a final manuscript-preparation stage is not itself a gate; it may begin only under an
  explicit PI authorisation recorded as an internal preparation act, with no gate promoted, submission
  still prohibited while PCR1 fails, the §E limitation carried, the A2 re-tiering included, and §§B–D
  dispositions recorded.
* **§G — minimum remaining authorisations:** (1) P13 transition; (2) manuscript editing (limitation text +
  A2 re-tiering); (3) P5 gate sentence; (4) R-1 accept-as-open or authorise the rerun; (5) C-1 disposition;
  (6) author-data route maintenance (no action). Nothing else.
* **§H — the external benchmark hunt is CLOSED PERMANENTLY** (Decision B carried forward; no admissible
  replacement or augmentation exists; no further search, hunt phase, literature pass or metadata-only audit
  loop is authorised on this question).

## Verification (exact counts)

| Check | Result |
|---|---|
| `test_p12ad_decision_record.py` (new guards) | 18 passed |
| Full suite `paper9/verification/suite` | **300 passed, 1 skipped, 0 failed** |
| `check_traceability.py` | 18/18 CLOSED/LOCKED, 0 open |
| `check_register_provenance.py` | PASS — A=0 / B=3 / C=2 / D=0 |
| Immutability vs entry (546 files @ `37f7186`) | 0 changed / 0 removed / 3 added (all P12AD) |
| Manuscript | 0 bytes changed |

## State after P12AD

Local = origin = ls-remote (verified at every push). Working tree clean. No gate, threshold, route,
gate definition, numerical result, Blueprint byte or manuscript byte was changed. PCR1/G3/G4 remain
unmet; the project's entry into final manuscript preparation is now a single authorised PI decision away,
and no part of it requires reopening the closed benchmark hunt.
