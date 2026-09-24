# P12S — proposed manuscript-impact list (PROPOSAL ONLY — the manuscript is NOT modified)

**Status of the manuscript in this phase:** untouched. `paper9/latex/`, `paper9/tables/`,
`paper9/figures/` are byte-unchanged vs the pre-work checkpoint `270b8ab`
(`git diff --stat 270b8ab -- paper9/latex paper9/tables paper9/figures` → empty).
**No manuscript change is committed by P12S.** The items below are proposals for a future,
separately authorised editing phase; they are *not* applied here.

Route vocabulary per Blueprint v1.5 / A2: `GRAPHICAL_VALIDATION` (labelled overlay, never a
percentage), `NOT_VALIDATED`, `QUANTITATIVE_VALIDATION` (≤ 2 %, ≤ 0.5 % classical — unchanged).

---

## J.1 — `paper9/latex/sections/sec05_verification.tex` (Benchmark B1 paragraph, ~line 29)

| | |
|---|---|
| **Old claim** | "…Figure~\ref{fig:benchmark_validation}(a) presents the computed dispersion branches alongside the visual overlay against Figure~2(a) of Li et al. … Because the source publication released graphical plots without floating-point tables, quantitative solver error is classified as N/A (Graphical Only) per Table~\ref{tab:anchor_errors}." |
| **New wording (proposed)** | "…the independent classical Rytov solution reproduces the four lowest branches of Figure~2(a) of Li et al. branch-by-branch under the source-stated parameters and the source's own normalisation (Eq. 55), satisfying the labelled graphical-validation route of the Blueprint (§13, amendment A2); quantitative solver error remains N/A because the source released no floating-point tables." |
| **Figure/table impact** | none structurally; `tab03_anchor_errors.tex` B1 status cell `PARTIAL` → proposed `GRAPHICAL PASS (A2 route)`. |
| **Evidence** | `paper9/audit/evidence/p12s/B1_overlay.png`; `paper9/audit/benchmark_validation_record.json` → `benchmarks.B1`. |

## J.2 — same file (Benchmark B2 paragraph, ~line 35)

| | |
|---|---|
| **Old claim** | "…the stabilized adaptive-precision transfer-matrix engine achieves Level 1 and Level 2 identical-material residuals of 4.10 × 10⁻⁵⁷ … Stop bands of the dimensional-micro (published-axis) configuration open at ω̄ ∈ [0.078, 0.242] … Benchmark B2 is classified as NOT VALIDATED / GRAPHICAL ONLY (external quantitative validation unavailable)." |
| **New wording (proposed)** | keep `NOT VALIDATED` (strengthened): "…under the source-stated cell geometry (a_A = a_B = 0.01 m) the gradient correction is O((lk)²) ≈ 4 × 10⁻⁶ and the reproduction coincides with the classical panel (a), whereas the published panel (b) deviates strongly; the alternative barred reading of the source's own l̄ = l/b definition would require an adaptive precision of ≈ 5 × 10⁴ decimal digits (numerically infeasible), and the micro-geometry reading contradicts the stated cell size. The ambiguity is therefore recorded as unresolved and Benchmark B2 is NOT VALIDATED (route A2.4: no silent choice)." |
| **Figure/table impact** | `tab03_anchor_errors.tex` B2 row unchanged in status (`NOT VALIDATED`); footnote (e) may be extended with the two new quantitative statements. |
| **Evidence** | `paper9/audit/evidence/p12s/B2_overlay_interpretations.png`; `benchmark_validation_record.json` → `benchmarks.B2`. |

## J.3 — same file (Benchmark B3 paragraph, ~line 36) **— the material change**

| | |
|---|---|
| **Old claim** | "As shown in Figure~\ref{fig:benchmark_validation}(b), the independent transfer matrix yields the multi-passband structure with stop bands at ω̄ ∈ [0.340, 1.024], [1.423, 1.867], and [2.477, 2.911]. … status is designated as GRAPHICAL ONLY / PARTIAL." |
| **New wording (proposed)** | "The independent transfer-matrix evaluation yields stop bands at ω̄ ∈ [0.339, 1.021], [1.419, 1.868], [2.474, 2.908] (reproduced here; unchanged numerically), but this implementation does not overlay Figure~4(c): its lowest branch reaches ω̄ ≈ 0.35 at k̄ = 1 whereas the source's own figure and the exact classical limit require 0.50. Because the source publishes no tables and its dipolar-gradient formulation/coefficient convention cannot be pinned down from the text, Benchmark B3 is recorded as **NOT VALIDATED** under the A2 routes; no parameter was tuned to force agreement." |
| **Figure/table impact** | `tab03_anchor_errors.tex` B3 status cell `PARTIAL` → `NOT VALIDATED`; gap-1 column value presumably unchanged (production numbers untouched); `fig04_benchmark_validation.pdf` panel (b) caption ("comparison … qualitative graphical only") to be re-labelled `NOT VALIDATED` for consistency. |
| **Evidence** | `paper9/audit/evidence/p12s/B3_overlay.png`; `benchmark_validation_record.json` → `benchmarks.B3`; blocker recorded in `P12S_GRAPHICAL_VALIDATION_AUDIT.md` §Phase F. |
| **Why this matters** | this is the only place where the P12S evidence would *weaken* a manuscript status; it must be surfaced, not buried. |

## J.4 — `paper9/latex/sections/sec05_verification.tex` (Evidence Hierarchy Declaration, ~line 48)

| | |
|---|---|
| **Old claim** | "…graphical alignment is preserved as qualitative evidence in repository audit artifacts … without claiming unsubstantiated numerical error tolerances from visual similarity alone. Consequently, Gate~G3 remains formally NOT MET until author-released floating-point datasets are made publicly available." |
| **New wording (proposed)** | "…under Blueprint v1.5 §13 (amendment A2) a labelled graphical-validation route is admissible for published benchmarks; B1 satisfies it (`paper9/audit/evidence/p12s/B1_overlay.png`), while B2 and B3 remain NOT VALIDATED for the source-side reasons recorded in `paper9/audit/benchmark_validation_record.json`. Consequently Gate~G3 remains formally NOT MET, and the author-data request package remains the higher-tier route that would close B2/B3 quantitatively." |
| **Figure/table impact** | none. |

## J.5 — items with **no** proposed change

- Abstract/introduction/conclusions: no number in them depends on the B1/B2/B3 route status (checked:
  no "2 %", "validation rate" or benchmark-status sentence outside §5 and Table 3).
- `tab04_consistency_suite.tex`, `tab02_parameters.tex`, `tab05_gap_summary.tex`,
  `tab06_convergence_floor.tex`, `tab07_steering_sweep.tex`: unaffected; no production result changed.
- The rejected 0.48 % pixel metric is **not** reintroduced anywhere; the P12S evidence supersedes it and
  keeps every `quantitative_error` NULL.
