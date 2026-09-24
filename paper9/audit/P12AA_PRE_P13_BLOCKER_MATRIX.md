# P12AA — pre-P13 blocker matrix (human-readable)

**Phase:** P12AA (traceability-metadata remediation + pre-P13 readiness audit)
**Date:** 2026-09-24 · **Branch:** `phase-1-symbolic`
**Governing spec:** `Paper9_Blueprint v1.5` (amendment A2, PI-directed, P12R)
**Status source:** `paper9/audit/benchmark_validation_record.json` (`gate_state` + `benchmarks`) and
`paper9/audit/P12L_PCR1_G3_FORMAL_BLOCKER_RECORD.md`
**Machine-readable twin:** `paper9/audit/P12AA_PRE_P13_BLOCKER_MATRIX.json`

This is a **readiness record**. It changes no gate definition, no threshold, no numerical result and no
validation route, and it closes nothing.

## Matrix

| Blocker | Current status | Exact reason | Required evidence | Available internally? | Author data required? | Can close now? |
|---|---|---|---|---|---|---|
| **B2** (Layer 2a gradient — Li 2024 Fig. 2(b)) | `NOT_VALIDATED` | No numerical values published for Fig. 2(b) (raster only), **plus** a dimensionally ambiguous length scale: caption gives a bare `l = 1e-5` while Eq. 55 defines `l̄ = l/b`; three admissible interpretations produce different curves and none may be adopted silently (A2.4). | The (wavenumber, frequency) pairs / band-gap edges underlying Fig. 2(b) **and** the plotted parameter set, units and exact length-scale definition/normalisation (P12L spec §2). | NO | YES | NO |
| **B3** (Layer 2b dipolar gradient — Li 2023 Fig. 4(c)) | `NOT_VALIDATED` (formulation `ESTABLISHED / SOURCE-EQUIVALENT`) | No numerical values published for Fig. 4(c) (raster only) and the panel's parameter set/normalisation is unstated. The reproduction **is** source-formulation-equivalent (layer matrix ≡ source Appendix 3 to ~1e-16), so the residual is source-side data, not a formulation defect. | Values underlying Fig. 4(c) (gap edges, first four branch frequencies at stated `k̄`) plus the Fig. 4(c) parameter set and normalisation. | NO | YES | NO |
| **PCR1** | `NOT PASS` | The `≤ 2 %` criterion is written against **published numerical values**; for the mandatory set (Layers 1, 2a, 2b) the public record holds zero tables, zero supplementary data and no numeric values in the text, so the criterion's quantity does not exist. The three `quantitative_error` entries are `null` by design. | Published/author-released reference values for Layers 1, 2a, 2b with the exact parameters, units and normalisation. | NO | YES | NO |
| **G3** | `NOT MET` | Consumes PCR1's quantity and adds completeness conditions (tabulated first four branch frequencies at stated `k̄`, gap-edge comparison, per-quantity and maximum relative error, explicit PASS/FAIL per benchmark in the main text). | PCR1 quantities plus the complete in-manuscript comparison block. | PARTLY (the manuscript block is internal work but is conditioned on unavailable reference values) | YES | NO |
| **G4** | `NOT MET` | PI signature is available only after PCR1–PCR8 all pass; a failed PCR blocks exactly as G3 does, and PCR1 is `NOT PASS`. | A complete PCR1–PCR8 pass set. | NO | YES (via PCR1) | NO |
| **P5** | `NOT PASS/OPEN` | Two parallel P5 pipelines with no numeric cross-validation (different solver lineage, sampling, band count, AR definition/scale, pilot orientation, TV values); branch-level gate contested (Part A `PASS` vs Part B `NOT PASS`). | One reconciled production record — at most one `[S]` set and one gate statement — supported by a numeric cross-validation at a common `(θ, AR, l-scale)` point. | YES | NO | NO — needs a PI/user reconciliation decision and an authorised run |
| **R-1** | `OPEN` | Pipeline-level reproducibility of the governing artifact is not established; determinism of the estimator rule (frozen Rule R-fit, `F = 3` strict) is **not** pipeline reproducibility, so R-1 is deliberately left open rather than forced. | An independent-pipeline re-execution under the frozen protocol, **or** an explicit PI decision that R-1 remains open at submission. | YES | NO | NO — needs an authorised re-run or an explicit decision; no re-baseline is undertaken here |
| **P13** | `BLOCKED` | Blocked by the upstream gates: PCR1 `NOT PASS`, G3/G4 `NOT MET`, P5 and R-1 open. The Blueprint's own rule forbids submission while these stand. | Closure of PCR1 → G3 → G4 plus P5 reconciliation and R-1 evidence. | NO | YES (for the PCR1/G3/G4 chain) | NO |

**Not a blocker (context):** **B1** (Layer 1, classical limit) stands at `GRAPHICAL_VALIDATION / PASS`
under amendment A2, with its own audit trail; it is not a submission blocker.

## What can move what

* **Author-released numerical data** can move the chain **PCR1 → G3 → G4** only, and only after the B2
  length-scale question is answered alongside it (P12L spec §2). It cannot move **P5** or **R-1**, and
  it does not by itself close PCR1: "data receipt alone does not close PCR1 or G3" (P12O §4).
* **P5** and **R-1** are internal matters (reconciliation and independent reproduction). They need a
  decision plus an authorised run, not external data.
* **No blocker** can be closed by changing a gate definition, a threshold, a numerical result or a
  validation route. Amendment A2 already fixed the admissible routes (numerical and graphical); this
  matrix adds none and relaxes none.
* Author-request status is unchanged: the three scoped requests are **prepared, NOT SENT**; no author
  has been contacted; the PI decision is **PENDING** and does not authorise sending at this stage.

## Readiness verdict (pre-P13)

**No blocker in this matrix is closable now**, and none is closable by a gate redefinition, a threshold
change or a route change. The internally obtainable blockers (P5, R-1) need an authorised internal
decision (and, for R-1, an authorised re-execution) with **no** author contact; the externally dependent
blockers (B2, B3, PCR1, G3, G4, P13) need reference numbers that exist only in the authors' hands, and
the requests for them remain unsent and unauthorised. This is a readiness audit, not a gate change:
every status above is exactly the status recorded by the active machine record.
