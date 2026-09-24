# P12L — Formal PCR1 / G3 Blocker Record

**Phase:** P12L (documentation of an externally blocked gate; no science performed)
**Date:** 2026-09-24 · **Branch:** `phase-1-symbolic` · **Repository:** `https://github.com/vipin-oss/BFS-FEM-MATLAB`
**Basis:** P12K forensic audit (`paper9/audit/P12K_PCR1_G3_BLOCKER_FORENSIC_AUDIT.md`), whose findings
are treated here as **independently verified** and are locked unchanged.
**Status of this document:** a record of fact for the PI's decision. It performs no calculation,
asserts no new result, and promotes no gate. The two decisions it serves are *A* (PI-authorized
external author-data request, specification in `P12L_AUTHOR_DATA_REQUEST_SPEC.md`) or *B* (formal
acceptance that PCR1/G3 remain unmet).

---

## 1. The PCR1 requirement (authoritative text)

Blueprint v1.4 §10.4, item 1 — the enforcement point ("cannot be submitted until every line below is
true and evidenced in the computation log"):

> "All mandatory published benchmarks (Layers 1, 2a, 2b) PASS with maximum relative error $\le 2\%$;
> the $\le 2\%$ criterion is retained (the $0.5\%$ target applies only to the classical limit)."

The mandatory set is **Layers 1, 2a and 2b**; Layer 2c is marked *optional* in the §5.2 layer table.
Per §10.4 item 2 (PCR2) and the G3 evidence rule, the comparison must appear **in the main
manuscript**, not in supplementary or internal files only.

## 2. The G3 dependency

Blueprint v1.4, hard-gate box (**HARD GATE G3 — non-negotiable**):

> "Layers 1, 2a and 2b band-gap edges and the first four branch frequencies must agree with the
> published values to **≤ 2 %** relative (target ≤ 0.5 % in the classical limit)."

with the evidence-and-manuscript rule (overlay/side-by-side plots; **tabulated first four branch
frequencies at stated $\bar k$**; band-gap edge comparison; per-quantity and maximum relative error;
explicit PASS/FAIL per benchmark — all in the main text), the roadmap anchor at week 8 ("Layers 1,
2a, 2b, 2c executed. Error table produced."), and the instruction **"If it fails: __Do not
submit.__"**

G3 therefore consumes PCR1's quantity and adds its own completeness conditions (§6).

## 3. B1 / B2 / B3 evidence status (locked from P12K)

| Benchmark | Layer | Anchor | Solver evidence held | Reference evidence held | Status |
|---|---|---|---|---|---|
| **B1** | 1 (classical limit) | Li et al. 2024, Fig. 2(a) | genuine numerical dispersion and Bragg bands; Level 1 residual `6.47e-16`, Level 2 `7.22e-16`; Rytov analytic verified `<10⁻¹⁵` | **only a published raster figure** | **PARTIAL / GRAPHICAL_ONLY** |
| **B2** | 2a (gradient, $f=0$) | Li et al. 2024, Fig. 2(b) | genuine numerical bands; Level 1/2 residuals `4.10e-57`; three parameter interpretations run | **only a published raster figure; parameterisation ambiguous** | **NOT_VALIDATED / GRAPHICAL_ONLY** |
| **B3** | 2b (dipolar gradient, Pb/brass) | Li et al. 2023, Fig. 4(c) | genuine numerical bands (pinned run P11D-B3-R1, 720 points); Level 1 `1.37e-13`, Level 2 `4.19e-14` | **only a published raster figure** | **GRAPHICAL_ONLY / PARTIAL** |

Nothing here is new: these are the registry statuses (`audit/benchmark_evidence.json`) as locked by
P12K. No status is promoted or demoted by this record.

## 4. Why the three `quantitative_error` entries remain NULL

Each entry is `null` in `audit/benchmark_evidence.json` with `reference_data_available = false` and
`quantitative_error_allowed = false`. The chain was traced end-to-end in P12K — manuscript footnote →
Table 3 → registry → single authoritative generator (`p11d_regenerate_evidence.py`) → archived source
PDF → published record — and re-verified first-hand from the archived PDFs:

- **Li et al. 2024** (`analytic/li2024/s41598-024-75049-1.pdf`): **zero** tables, **zero**
  supplementary material, and **no numeric band-gap-edge or branch-frequency values in the running
  text**; the Data-availability statement reads that the datasets "can be obtained from the
  corresponding author".
- **Li et al. 2023** (`analytic/li2023/17455030.2023.2222189.pdf`): **zero** tables, **zero**
  supplementary material, **no** data-availability statement, and no numeric gap-edge values in the
  text.

A relative error is a ratio between a computed quantity and a **published numerical value**. With no
published numerical value for the gap edges or the first four branch frequencies, the quantity the
criterion is defined on does not exist. The NULLs are therefore the **correct and only honest
representation**: they record "not computable from the public record", not "computation failed".
**This is not a solver failure** (§10).

## 5. Why digitising the figures is not an admissible substitute

Governing policy, verbatim (`audit/benchmark_evidence.json`, metadata):

> "Curve digitization is permitted ONLY to draw overlay figures, NEVER to compute solver-error
> percentages. If author raw numerical tables are unreleased, benchmark status is formally
> GRAPHICAL_ONLY / PARTIAL."

The reasons are recorded in the same evidence chain: raster curves do not carry axis-anchored numeric
precision; the digitisation uncertainty is not characterised and cannot be propagated into a ≤2 %
claim; and the criterion is written against **published values**, which a pixel estimate is not.
Applying the policy, the manuscript states the N/A (Graphical Only) designation explicitly
(`sec05_verification.tex`; Table 3 footnotes), and the registry forbids the error computation
(`quantitative_error_allowed: false`). Any pixel-derived percentage would be a **fabricated**
pass/fail input and is excluded by the governing protocol, by P12K's mandate, and by the P12L stop
condition.

## 6. Why B2 has a second, independent blocker

Beyond the missing numerics, **B2's source parameterisation is dimensionally ambiguous**: the Fig.
2(b) panel annotates a bare `l = 1e-5` while the paper's text defines a barred length scale
($\bar l = l/b$ semantics; the mismatch with the panel annotation was flagged at the source-audit
stage and never resolvable from the published text). Three interpretations have been run separately
(`CFG-DIM-MICRO`, `CFG-DIM-MACRO`, `CFG-BAR-MACRO`), and **none was adopted as truth**, because the
source does not determine which one the published curve corresponds to.

Consequence: even if numerical data for Fig. 2(b) were obtained, a ≤2 % comparison would remain
**undefined** until the author states — or the data unambiguously fix — whether the plotted case uses
`l` or `l̄` (and with which normalisation). This is an independent condition that external data must
satisfy, not a by-product of §4.

## 7. Why no author-data file exists in the repository

Exhaustive repository/inventory checks (P12K Part E, re-run here):

- no author CSV / TXT / XLSX / MAT / JSON, no supplementary archive, and no reference-table file
  anywhere in the workspace;
- `bench/cards/`, `bench/reference_tm/`, `bench/overlays/` contain no reference tables;
- the only numerical references present are the repository's **own** computed outputs;
- the only publisher artefacts archived are the two source **PDFs** and figure rasters;
- `audit/P11_SOURCE_PACKAGE_INVENTORY.md` records the same conclusion ("raw numerical tables were not
  published online as supplementary data"), and the P12K first-hand PDF inspection confirms it.

There is therefore no machine-readable external reference in this repository to compare against — the
absence is in the **published record**, and no repository-side step can create it.

## 8. Why external author-released numerical data is required

To satisfy §1–§2 the comparison needs, for each of B1/B2/B3, the **numerical values underlying the
published curves** (or equivalent tabulated values) together with the exact parameters, units and
normalisation definitions used to produce them. Only the authors hold these; the papers themselves
state (Li 2024) that the datasets are obtainable from the corresponding author. Consequently:

- **Decision A** — a narrowly scoped, PI-authorized data request (specification prepared in
  `P12L_AUTHOR_DATA_REQUEST_SPEC.md`; **not sent**, no author contact initiated);
- **Decision B** — formal acceptance that PCR1/G3 remain unmet and the submission decision is made on
  that basis.

No third path exists that does not fabricate the missing numbers.

## 9. No numerical values were fabricated or inferred

Recorded as a standing attestation: **no** benchmark relative error, gap edge, branch frequency,
parameter value or normalisation was invented, estimated, digitised, interpolated or inferred from any
figure at any point in this audit chain. The three `quantitative_error` entries remain `null`; no new
number was introduced into `benchmark_evidence.json`, Table 3, the manuscript, or any registry by P12K
or P12L. Where values are quoted in this record (residuals, thresholds), they are copied from existing
artefacts with their provenance named.

## 10. PCR1 / G3 / G4 remain unmet — and this is not a solver defect

| Item | Status (unchanged) | Reason |
|---|---|---|
| **PCR1** | **NOT PASS** | the published ≤2 % comparison quantity does not exist in the public record |
| **G3** | **NOT MET** | same quantity, plus its completeness/manuscript conditions (§6) |
| **G4** | **NOT MET** | PI signature only after PCR1–PCR8 pass; a failed PCR blocks submission exactly as G3 does |

The blocker is **evidential, not computational**: the solver reproduces every internally checkable
quantity it can be tested against (Level 1/2 identities at machine precision, Rytov analytic
dispersion, analytic Layer 3 checks, the internal five-layer suite, mesh convergence with the
governing rate), and the missing input is the *published reference numbers*, which no solver run can
supply. No statement in this record should be read as a solver failure, nor as a claim that the
manuscript is unaffected: PCR1/G3 unmet **blocks submission** under the Blueprint's own rule.

## 11. Explicitly out of scope for external data (status preservation)

The requested external data can only move the PCR1/G3 chain. It would **not**:

- resolve **P5** (two parallel production pipelines, no numeric cross-validation between them) — an
  internal reconciliation matter;
- change **R-1** (pipeline-level reproducibility of the governing artifact; the estimator rule's
  determinism is not pipeline reproducibility);
- alter **PCR5** (already PASS under the amended definition and unchanged by this record);
- alter the **governing numerical baseline** (`p = 4.173919246515192`, CI
  `[3.1453687594104447, 5.202469733619939]`, `ε_Δ = 4.6318154949690315e-11`) or Rule R-fit;
- authorize **P13**, a Route-F re-baseline, or any manuscript release edit.

## 12. Reproduction of the P12K facts cited here

| Fact | Command / artefact |
|---|---|
| PCR1 and G3 text | `paper9/plan/blueprint/Paper9_Blueprint_v1.4.tex` (hard-gate box; §10.4 item 1) |
| Registry statuses and the digitisation policy | `paper9/audit/benchmark_evidence.json` |
| Table 3 N/A (Graphical Only) footnotes | `paper9/tables/out/tab03_anchor_errors.tex`; §5.1 of `sec05_verification.tex` |
| Source PDF findings (tables/supplement/data availability) | `paper9/analytic/li2024/s41598-024-75049-1.pdf`, `paper9/analytic/li2023/17455030.2023.2222189.pdf` — first-hand text extraction, P12K §5 |
| B2 ambiguity record | `P3_TV_RESOLUTION.md`; `benchmark_evidence.json` `parameter_semantics/ambiguity_status`; three interpretation runs |
| No author data in the package | `audit/P11_SOURCE_PACKAGE_INVENTORY.md`; P12K Part E searches |
| Gate/status matrix | `audit/P12C_GATE_PCR_FORENSIC_AUDIT.md` §2; `audit/P12K_PCR1_G3_BLOCKER_FORENSIC_AUDIT.md` §13 |

**Status summary (locked): PCR1 NOT PASS · PCR5 PASS · G3 NOT MET · G4 NOT MET · P5 NOT PASS/OPEN ·
R-1 OPEN · C-1 OPEN · G-1 CLOSED · P13 BLOCKED.**
