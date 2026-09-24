# P12J — Correction-Only Closure of the P12I Findings

**Phase:** P12J (correction-only; branch `phase-1-symbolic`; `main` untouched) · **Date:** 2026-09-24
**Baseline:** `1c6b2e3e793ab7a9e60bef09c347e5f91bc748fb` (P12I), clean tree · **Remote:** `0d985029…`
(unchanged; nothing pushed) · **Verdict being acted on:** P12I = *P12H VERIFIED WITH CORRECTIONS
REQUIRED*.
**Scope:** resolve **only** C1, C2, C3. No scientific result, governing number, Rule R-fit constant,
admissible subset, PCR definition, gate status, Blueprint scope or solver setting was changed; no
Route-F re-baseline; no P12E value imported; no P13; no push.
**Evidence bundle:** `paper9/audit/evidence/p12j/`.

---

## 1. P12I baseline

P12I verified P12H's material claims from artifacts, git objects, source and fresh execution
(independent Rule R-fit re-implementation reproduced `p` and the CI bit-exactly; 32² exclusion
1527.7× below threshold with the same rule retaining the finest level at the control k; 19-path change
set exactly as authorized; gates re-derived), and required three corrections, none of which touched
the governing baseline or any gate status. P12J closes them and re-verifies the invariants that P12I
established. The P12H and P12I documents remain auditable as historical records: the P12H text is
preserved and amended only by an additive note; the P12I verdict text is unchanged and amended only
by an additive status block.

## 2. C1 — Blueprint v1.4 §5.7 states its declared numerical zero

**File:** `paper9/plan/blueprint/Paper9_Blueprint_v1.4.tex` (sha256 before `0089754b076ff9e3…`,
after **`2ae0b1e8f37e10a0…`**), two line-blocks edited (l. 95 version/provenance row, l. 446 §5.7):

- the rule clause now reads: "…greater than the pre-declared factor $F = 3$ times the larger of that
  level's measured reproducibility and the declared numerical zero $10^{-15}$:
  $e_i > F \cdot \max(s_i, 10^{-15})$, $F = 3$ --- the reproducibility $s_i$ being measured from two
  pre-registered start vectors at the frozen solver configuration (the protocol, $F$ **and the declared
  zero** are fixed before the calculation is run and recorded with it)."
- the version row records the clarification: "P12J (2026-09-24) clarification: the §5.7 rule now
  states its declared numerical zero explicitly, $e_i > F \cdot \max(s_i, 10^{-15})$ with $F = 3$,
  decided inactive for every recorded result".

**Criterion unchanged:** the comparison is identical to the frozen rule and to
`verification/suite/rule_rfit.py` (`F = 3.0`, `SPREAD_FLOOR = 1e-15`, strict `>`, declared zero where
no spread is measurable); the clarification is decision-inactive for all four recorded cases
(P12I §4). All other §5.7 content — all-levels-reported, excluded-level disclosure, CI requirement,
no-theoretical-order clause, the ≥3-level minimum, the resolution-floor sentence and the
weak-anisotropy sentence — is preserved verbatim.

**Structural integrity re-verified after the edit:** v1.3 still differs from v1.4 by **exactly the
same four blocks** (lines 95 / 446 / 618 / 895); v1.4 brace-balanced; no other line changed.

## 3. C2 — P12H audit description corrected by additive note

**File:** `paper9/audit/P12H_A1_PROTOCOL_CLOSURE_AUDIT.md` — **additive only (+13 lines, 0 removed)**.
An explicit "P12J correction note (2026-09-24)" was placed ahead of §1 stating: the §3 table's row 2
described per-level admission as `e_i > F·max(s_i, 1e-15)` while the v1.4 text at that commit read
`e_i > F·s_i`; the floor lived in the plan row 5i and in `rule_rfit.py`; the row anticipated the
rule's operational form rather than quoting the specification text; the correction was independently
recorded as C2 in P12I §12 and is closed by C1, since the current §5.7 text makes the row-2
description an exact quotation.

All 14 sections, every scientific conclusion and the original text are intact (verified: the §3 row,
the section count and the governing numbers are unchanged). P12I's correction record remains
traceable — the note cites `P12I_INDEPENDENT_P12H_VERIFICATION.md` §12 and this document.

## 4. C3 — Figure 5 cosmetics

**Files:** `figures/gen/fig05_mesh_convergence.py` and the regenerated
`figures/out/fig05_mesh_convergence.pdf` (31 297 → 35 165 bytes; the committed generator was run, no
manual editing of the PDF).

| Defect (P12I §6) | Fix |
|---|---|
| Panel-(b) legend (P12H-added) overlapped the finest-step bar and its value label | legend moved to the free **upper-right** corner of panel (b) |
| The tallest bar's value annotation collided with the "(b)" subplot title (pre-existing, reproduced from the `2225cdc` generator) | value labels are now drawn **inside** the two tall bars (white, centred); the smallest bar keeps its label just above itself |

**Nothing scientific changed:** plotted arrays are the same JSON values (`omega`, `rel_err`), the
fitted/excluded classification still comes from the Rule R-fit record, the regression line, axes,
log scales, limits, mesh values and the panel titles' wording are untouched, and the caption
unchanged. Visual verification of the regenerated figure: both titles fully legible, no overlap
between the legend and any bar, labels readable, the resolution-limited (hatched) finest step and the
operational-floor line still clearly distinguished.

## 5. Regression results (Part D)

| Check | Result |
|---|---|
| Full suite, run 1 | **126 passed, 1 skipped in 7.34 s** |
| Full suite, run 2 | **126 passed, 1 skipped in 6.66 s** |
| Governance guards (incl. new C1 assertions + P12J traceability guard) | 11 passed |
| C-1 synthetic suite | 23 passed |
| P4B consistency + P6 remediation/generators (the guards touching v1.4 / fig05 / tab06) | 20 passed, 1 skipped |
| Opt-in end-to-end rerun (separate, **not** merged into the normal count) | `P4B_B1_FULL_RERUN=1` → **10 passed in 72.01 s**, repo clean |
| Numerical / float / manuscript / Blueprint cross-check (P12J copy) | **43/43 passed** |

The baseline move 125 → 126 passed is exactly the **one** new guard added for C1/C2/C3 traceability;
the single skip is the pre-existing opt-in rerun, unchanged. **One affected check was found and
handled correctly:** the P12H-era cross-check asserted the literal phrase "reproducibility of that
level's eigenvalue", which C1 reworded; the P12J copy extends the anchor to accept both wordings (the
intent — the rule text must be measurement-only — is unchanged and the added form is stricter). The
P12H-era working script was left untouched (`sha256 e5ae5ee0604a6e45…`), so the P12H record stays
reproducible as written.

## 6. Mutation results

| Matrix | Result |
|---|---|
| Rule-module mutations (`mutation_rfit.py`) | **13/13 detected**, rule file restored byte-identically (`d4fed49241bc3f74…`) |
| Legacy staged mutations (`audit/evidence/p12e/mutation_harness.py`) | **12/12 detected**, cleanup complete |

No criterion constant was touched, so the mutation coverage is unchanged by P12J.

## 7. Immutability results

| Asset | Expected | Verified |
|---|---|---|
| governing JSON `p4b_5g_to_5i.json` | `38384363…` | ✓ unchanged |
| historical TXT `p4b_5g_to_5i.txt` | `1daf0f32…` | ✓ unchanged |
| P4B production script `p4b_5g_to_5i.py` | `b1c8d996…` | ✓ unchanged |
| TXT provenance | `6154a23b…` | ✓ unchanged |
| **Blueprint v1.3** | `ca71b91a…` | ✓ byte-identical (also blob-identical across commits) |
| **Rule R-fit implementation** `rule_rfit.py` | `d4fed492…` | ✓ unchanged |
| P12E staged patch | `03b902d2…` | ✓ unchanged; no P12E value imported |
| P12C 32²/64² raw evidence | `5547bae4…` / `c8910c0d…` | ✓ unchanged |
| Route-F values in governed artifacts | none | ✓ sweep over v1.4, plan, manuscript, sec05, sec09, Table 6, fig05 generator, `rule_rfit.py` finds none |

The P12J change set is confined to the six files in §8 of the diff audit; no manuscript source, plan
row, table, traceability registry, gate document or evidence bundle was touched.

## 8. Governing-number verification

```
p        = 4.173919246515192                     (unchanged)
CI       = [3.1453687594104447, 5.202469733619939]   (unchanged)
ε_Δ      = 4.6318154949690315e-11                (unchanged)
admissible subset = {4², 8², 16²};  excluded = {32²};  "no theoretical order claimed"
```

Read directly from the governing JSON (whose hash is unchanged) after all edits. The C1 clarification
does not alter the rule's behaviour: re-running the independent re-derivation and the guard suite
reproduces the bit-exact fit and every recorded verdict.

## 9. Gate / status preservation

| Item | Status | Basis |
|---|---|---|
| **PCR5** | **PASS** (unchanged) | definition and evidence untouched; the C1 clarification adds no requirement |
| **R-1** | **OPEN** (unchanged) | pipeline-level reproducibility unachieved; the C1–C3 changes do not touch the solver configuration or the reproducibility evidence |
| **C-1** | OPEN (unchanged) | production acceptance path untouched |
| **G-1** | CLOSED (unchanged) | — |
| **G3** | **NOT MET** (unchanged) | no external author tables exist |
| **G4** | **NOT MET** (unchanged) | cannot be signed while G3/PCR1 unmet |
| **PCR1** | NOT PASS (unchanged) | 3 null external-error entries remain |
| **P5** | **NOT PASS / OPEN** (unchanged) | parallel pipelines still unreconciled |
| **P13** | **blocked** | not authorized by P12H, P12I or P12J |

No gate was promoted, demoted or reinterpreted in this phase.

## 10. Confirmation: no scientific result or protocol criterion changed

Explicitly confirmed by the diff audit (Part H):

- the **protocol criterion** is `e_i > F·max(s_i, 1e-15)`, `F = 3` strict, exactly as frozen in
  P12G and implemented in `rule_rfit.py` (unchanged, hash-verified); C1 only made the Blueprint text
  state the declared zero that the protocol already contained;
- the **admissible subset** for the governing artifact remains `{4², 8², 16²}` with `32²` excluded;
- **no** scientific, numerical, solver, parameter, manuscript-content, governance-criterion or scope
  change is present in the diff;
- the diff contains exactly six files: v1.4 (2 line-blocks, C1), the P12H record (+13 additive lines,
  C2), the P12I record (+14 additive lines, correction status), the fig05 generator (legend/labels,
  C3), the regenerated fig05 PDF, and the governance guard file (+16 lines: C1 assertions + the P12J
  traceability test). No other path in the repository differs from `1c6b2e3`.

## 11. Commit and closure state

One focused commit on `phase-1-symbolic`; working tree clean afterwards; **nothing pushed** — the
remote remains `0d9850290b63a5da81b098d999714ab621684c77`.

**Correction status: C1 = CLOSED, C2 = CLOSED, C3 = CLOSED.** P12H's verdict (verified, corrections
required) and P12I's verification record are preserved; both now point to this closure.
