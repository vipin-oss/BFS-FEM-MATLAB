# PI decision record — R-1 measured-adjudication acceptance

**Status: `APPROVED / CLOSED` — PI authorisation recorded 2026-09-24 (§6). R-1 is now `CLOSED`, without a
re-baseline.** The authorisation was conveyed by the PI as an explicit instruction in the project context
and is recorded below with its exact text; no wet signature is claimed.

| field | value |
|---|---|
| prepared | 2026-09-24 |
| prepared at HEAD | `ca57a9d55774fadcbe1c5d17bf929fc8fa3ec516` (branch `phase-1-symbolic`, tri-equal verified) |
| prepared by | repository-side preparation; the PI authorisation of §6 was recorded on 2026-09-24 |
| phase numbering | **none** — this is a decision record, not an audit phase, and it authorises no work |
| came into force | **2026-09-24**, on the PI's authorisation recorded in §6 |
| companion record | `paper9/audit/PI_DECISION_P5_GATE_ADOPTION.md` (same package) |

---

## 1. The decision — as adopted (one line, quotable)

> **PI DECISION (R-1), adopted 2026-09-24.** *I accept the executed reproducibility measurement on the deployed 5i
> configuration (`paper9/verification/suite/p4b_5g_to_5i.py`: tol = 1e-12, unpinned §5.7 start vector, meshes
> 4²–32²; five independent realizations across three families) adjudicated by the frozen **Rule R-fit** (F = 3
> strict, unamended) as R-1's criterion of record, and I close R-1 **without** a re-baseline, the admissible
> subset {4², 8², 16²} being invariant in all five realizations (0/5 fit-branch flips); the governing 5i artifact,
> its rate 4.173919246515192, its 95 % CI and ε_Δ remain byte-identical, no scientific number changes, the
> Blueprint and Rule R-fit are unamended, and benchmarks B2 and B3 remain NOT_VALIDATED.*

**The alternative not taken** (recorded for the record): authorise the **re-baseline** — regenerate the governing 5i
artifact under the frozen rule. `P12AB` Part E classifies R-1 as *"CLOSED only after an authorised numerical
rerun"*; the measurement above **is** that rerun's specified content, executed without touching any stored
artifact. A re-baseline is the only route that would change published numbers and is therefore the more
expensive option; the PI authorisation of 2026-09-24 **did not take it** (option C not selected).

**Signature options (recorded as presented).** (A) accept, close R-1 without re-baseline; (B) accept with
amendments; (C) do not accept; authorise the re-baseline. **Selected: A — accept and close R-1 without
re-baseline.**

## 2. Why this decision is evidence-complete

**What R-1 is.** `P12H` §10 / `P12AB` Part E separate three properties: **A** solver-level reproducibility
(established, Route-F configuration only), **B** governing-artifact reproducibility (not established — the
governing artifact is one realization of an unpinned start vector), **C** estimator-rule protocol determinism
(established). R-1's *recorded failure mode* is the **fit branch flipping with the solver realization** under the
deployed `err > 1e-14` cut (21 documented realizations: 20 four-level, 1 three-level).

**The measurement executed (exact P12AB Part E specification).** On the deployed configuration as shipped —
`verification/suite/p4b_5g_to_5i.py`, k = (0.31π, 0.22π)/L, ω̄_exact = 1.1648553893289133, meshes 4², 8², 16², 32²,
`tol = 1e-12`, **unpinned** start vector, threads unpinned, single process — the frozen Rule R-fit (F = 3 strict,
SPREAD_FLOOR 1e-15, ≥ 3 admissible levels, per-level spread s = (max − min)/min of ω) was applied to five
independent realizations. The deployed `err > 1e-14` cut, which the flip was defined against, is **not taken
anywhere**.

**Family 1 — deployed path as shipped (unpinned), 3 realizations**

| level | measured spread s | max error e | threshold 3·max(s, 1e-15) | e / threshold | verdict |
|---|---|---|---|---|---|
| 4² | 0 (dense path, deterministic) | 1.509122 × 10⁻⁸ | 3.0 × 10⁻¹⁵ | 5.03 × 10⁶ | admissible |
| 8² | 3.431158 × 10⁻¹⁴ | 7.586734 × 10⁻¹⁰ | 1.029347 × 10⁻¹³ | 7 370 | admissible |
| 16² | 1.164688 × 10⁻¹³ | 4.602346 × 10⁻¹¹ | 3.494063 × 10⁻¹³ | 131.6 | admissible |
| 32² | 4.064016 × 10⁻¹³ | 5.686191 × 10⁻¹³ | 1.219205 × 10⁻¹² | **0.4664** | **excluded** |

Fit slopes per realization: **4.1789475735 / 4.1803898441 / 4.1785620603** — admissible subset {4², 8², 16²} in
all three.

**Family 2 — Route-F two-seed protocol (PCG64 seeds 20260924, 7) at the deployed tolerance, 2 realizations**

| level | measured spread s | max error e | threshold | e / threshold | verdict |
|---|---|---|---|---|---|
| 4² | 0 | 1.509122 × 10⁻⁸ | 3.0 × 10⁻¹⁵ | 5.03 × 10⁶ | admissible |
| 8² | 1.219967 × 10⁻¹⁴ | 7.586986 × 10⁻¹⁰ | 3.659902 × 10⁻¹⁴ | 20 730 | admissible |
| 16² | 3.831460 × 10⁻¹⁴ | 4.593387 × 10⁻¹¹ | 1.149438 × 10⁻¹³ | 399.3 | admissible |
| 32² | 5.276359 × 10⁻¹³ | 3.739962 × 10⁻¹³ | 1.582908 × 10⁻¹² | **0.2363** | **excluded** |

Fit slopes: **4.1805695819 / 4.1799676366** — admissible subset {4², 8², 16²} in both.

**Result.** **0 / 5 realizations flip the fit branch**; the admissible subset is invariant; the reported rate
spans 4.1786 – 4.1806 across realizations (and 4.1765 – 4.1848 over the realized spread envelope), so the
manuscript's two-decimal `p = 4.17` is invariant. Margins: the largest measured 32² error (5.686 × 10⁻¹³) against
the smallest admitted threshold (1.219 × 10⁻¹²) is **2.14×** in the deployed family and **4.2×** in the two-seed
family; the verdict is unchanged for any F ≳ 1.40 (deployed family) — the register's F-robustness window for the
governing family was (0.2866, 78.24). The 32² level is excluded *because its measurement sits at or below its own
reproducibility* (in the governing artifact its error is 0.00196× its own threshold): it is not admissible at any
F, i.e. unmeasurable in principle at that level rather than merely unmeasured.

**Cross-era consistency check.** This era's 16² errors (4.590 – 4.602 × 10⁻¹¹) agree with the governing
artifact's 4.6321 × 10⁻¹¹ to ≤ 1.6 %, and the 32² level is on the same scale (1.5 – 5.7 × 10⁻¹³) in both eras.

## 3. What this authorisation changes — exact and minimal (applied 2026-09-24)

On authorisation the following governance effect exists (and has been applied — see §7):

1. **R-1 becomes CLOSED** (by the PI's recorded decision, without a re-baseline), on the criterion: two
   independent realizations on the deployed configuration, adjudicated by the frozen Rule R-fit (F = 3, unchanged)
   — measured this phase with five realizations, 0/5 flips;
2. the text of the achievement is recorded as *"Adjudicated by the measured reproducibility of the deployed
   configuration under the frozen rule; no re-baseline performed."* — and **never** as solver-wide or
   pipeline-wide determinism (the `P12H` §10 caution: the estimator-branch closure must not be restated as solver
   or pipeline determinism);
3. the active record `paper9/audit/benchmark_validation_record.json` now carries `gate_state.R-1` = `CLOSED`
   and a `pi_authorisations_2026_09_24` provenance block citing this record. `paper9/audit/P5_STATUS.md` and
   every historical record stay byte-unchanged.

**No stored artifact changes:** the governing 5i JSON (`paper9/verification/suite/p4b_5g_to_5i.json`) keeps its
rate `4.173919246515192`, its 95 % CI [3.1453687594, 5.2024697336] and ε_Δ = 4.6318154949690315 × 10⁻¹¹, byte for
byte; Table 6 and Figure 5 are untouched.

## 4. Mandatory non-satisfaction statement (applies to any granting)

> **This acceptance is a reproducibility-adjudication item only.** It does **not** constitute satisfaction of
> PCR1, G3 or G4; it does **not** authorise submission; it changes **no** scientific number, threshold or gate
> definition; it does not amend the Blueprint and does not amend Rule R-fit; it establishes **no** external
> benchmark validation; and **benchmarks B2 and B3 remain `NOT_VALIDATED`** with `quantitative_error` NULL. P13
> remains blocked.

## 5. Disclosed limits of the measurement (recorded honestly)

* Property **B** in its strict sense (the *stored* artifact being reproducible) is **not** established by this
  measurement and is not claimed: the measurement adjudicates the deployed *configuration* and shows the fit
  verdict is invariant across realizations, including the family in which the governing artifact was produced.
* Thread pinning was not enforced in this measurement (Route-F pinned threads); the spread this produces is
  *larger* than a pinned run's, i.e. the margins above are conservative.
* The Γ-point spectral comparison in the companion P5 record is √-amplified in the zero/rigid cluster and is
  quoted there with that caveat.

## 6. Signature block

```
R-1 MEASURED-ADJUDICATION ACCEPTANCE

State:  [ ] PROPOSED / READY FOR PI SIGNATURE        [x] APPROVED / CLOSED
        (approved and closed on 2026-09-24)

Decision (selected):     [x] A — accept, close R-1 without re-baseline
                         [ ] B — accept with amendments     [ ] C — authorise the re-baseline

PI decision text (verbatim, as conveyed 2026-09-24):
    "OPTION A — accept and close R-1 without re-baseline.
     Accept the executed P12AB Part-E measurement on the deployed 5i configuration as the
     criterion of record and close R-1 without re-baselining the governing 5i artifact or
     changing any published numerical result."

Amendments / conditions: none. No re-baseline was performed and none is authorised by this record.

PI: Vipin Gupta (name per repository metadata; PI-correctable)   Date: 2026-09-24
    (authorisation conveyed as an explicit PI instruction in the project context; no wet signature claimed)

Recorded by: P12C Post-Closeout Audit Agent (repository-side recording of the PI's instruction)
    Date: 2026-09-24
```

**Explicit distinction (state at closure).** The `PROPOSED / READY FOR PI SIGNATURE` state ended when the PI
issued the authorisation above; `APPROVED / CLOSED` exists **only** by that authorisation and was applied by the
minimal governance change listed in §7.

## 7. Applied governance effect (2026-09-24, minimal)

| file | change |
|---|---|
| `paper9/audit/benchmark_validation_record.json` | `gate_state.R-1`: `OPEN` → `CLOSED`; provenance block `pi_authorisations_2026_09_24.R-1` added (decision text pointer, effect, record path, non-satisfaction). **All other fields, values, hashes and reason strings byte-identical**; the governing 5i JSON is untouched |
| `paper9/audit/PI_DECISION_R1_MEASURED_ADJUDICATION.md` | this record: state → `APPROVED / CLOSED`, PI authorisation recorded with date and exact text |
| `paper9/audit/PI_DECISION_PACKAGE_P5_R1.md` | package state and status matrix updated to the authorised closures |
| `paper9/verification/suite/` governance guards | as listed in the companion P5 record §7 (the two closures share one guard update); every other gate, benchmark field, number, reason string and historical assertion unchanged |

**Not changed by this authorisation:** the governing 5i artifact (`paper9/verification/suite/p4b_5g_to_5i.json`:
rate `4.173919246515192`, 95 % CI, ε_Δ = 4.6318154949690315 × 10⁻¹¹, byte-identical), Table 6, Figure 5, Rule
R-fit, the Blueprint (all versions), the manuscript and all LaTeX, all figures and tables, all results
artifacts, and every benchmark classification. **No re-baseline was performed.** B2 and B3 remain
`NOT_VALIDATED`; PCR1 `NOT PASS`; G3/G4 `NOT MET`; submission not authorised.
