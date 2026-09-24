# P12AB — Remaining-Blocker Forensic Audit and P13 Entry Decision

**Phase:** P12AB (integrated forensic audit of the remaining blockers under the current governing
Blueprint v1.5 / amendment A2)
**Date:** 2026-09-24 · **Branch:** `phase-1-symbolic` ·
**Repository:** `https://github.com/vipin-oss/BFS-FEM-MATLAB`
**Entry HEAD (verified):** `7028da06e74950f3867c3140e5780c15a28e540e` (P12AA final checkpoint)
**Pre-work checkpoint:** committed and pushed before any audit work (see
`RECOVERY_CHECKPOINT_P12AB.md`)

**Scope guard.** This phase audits; it closes nothing and promotes nothing. It changes no gate
definition, threshold, validation route, benchmark set or numerical result; it does not modify Blueprint
v1.5, the manuscript, the production outputs or any historical record; it contacts no author and sends
nothing; it re-runs no solver. Findings are reported against the **current** governing text — v1.5
§13 (A2) and the v1.5 G3/PCR1 wording — never against v1.3/v1.4 rules.

---

## Part A — recovery

`git fetch origin phase-1-symbolic`; local = `origin/phase-1-symbolic` = `git ls-remote` remote tip =
`7028da06…`; working tree clean; immutability baseline written to `/home/user/p12ab_baseline_hashes.txt`
(536 tracked files). Pre-work checkpoint pushed and remotely verified before the audit began.

## Part B — B2 / B3 author-data dependency audit

### B.1 The governing test (current text)

The three evidence states of A2.1 are **exhaustive and mutually exclusive** (A2.6 fixes them as
`QUANTITATIVE_VALIDATION`, `GRAPHICAL_VALIDATION`, `NOT_VALIDATED`). The graphical route is admissible
only when "no machine-readable source values exist, **but the published source provides a sufficiently
detailed benchmark graph together with the material, geometric, normalisation and boundary/interface
information needed to reconstruct the case**" (A2.1(b)); A2.2 then requires the reproduction to be built
from those source-reported parameters (G1) and compared **directly** with the published curve (G2), with
no parameter adjustment to improve the visual match. A2.1(c) places a case with an unresolved source
ambiguity, or with insufficient accompanying information, in `NOT_VALIDATED`; A2.7's decision table
routes "graph only, parameters ambiguous or insufficient" to **Not validated**; and A2.8 confirms that
"A2 does not mark PCR1 or G3 as PASS/MET" — the states must be earned by an actual reproduction.

### B.2 B2 (Layer 2a, Li et al. 2024 Fig. 2(b))

| # | Question | Finding |
|---|---|---|
| 1 | Which A2 evidence state applies? | **`NOT_VALIDATED`** — on two independent grounds: the source carries an **unresolved ambiguity** (A2.1(c), and A2.4 explicitly forbids acceptance under *either* route while it stands), and no admissible reproduction reproduces the published panel (A2.7 "parameters ambiguous or insufficient") |
| 2 | What source information is available? | The Fig. 2(b) raster (with panel (a) classical); the caption string "gradient elasticity (l = 10⁻⁵, l₁ = 2·10⁻⁵, f = 0, L = 5, L₁ = 5, F = 0)"; the body definition `l̄ = l/b` (p. 7); the source-stated cell geometry `a_A = a_B = 0.01 m`; the paper's equations (Eq. 55 normalisation) |
| 3 | What is genuinely missing? | (i) the **definition and units of the plotted length scale** (dimensional `l` in metres, or normalised `l̄ = l/b`, and against which normalising length), and (ii) the parameter set actually plotted in panel (b). Nothing else: the solver-side evidence is complete |
| 4 | Can the published graph + source equations/parameters support graphical / quantitative validation — or neither? | **Neither.** Quantitative: no source numerical values exist, and A2.5 forbids manufacturing a percentage from a raster. Graphical: A2.4 blocks acceptance while the ambiguity stands, and the repository's own three admissible readings all fail the direct comparison — under the source-stated geometry (`l/b = 5×10⁻⁴`) the gradient correction is `O((lk)²) ≈ 4.16×10⁻⁶` and the reproduction **coincides with the classical panel (a)**, contradicting the published panel (b); the barred reading is numerically infeasible at working precision (≈5×10⁴ decimal digits required; run at dps 52 131 it still shows classical structure); the micro reading contradicts the stated cell size |
| 5 | Does A2 permit B2 to be accepted as a source-limited graphical validation despite the `l`/`l̄` ambiguity? | **No.** A2.4: "That ambiguity must be resolved from authoritative source information before B2 can be accepted under *either* route … B2 may not be reported as validated while the ambiguity stands." "Source-limited" is not one of A2.1's three states |
| 6 | Would accepting it require changing Blueprint v1.5? | **Yes** — it would require amending or voiding A2.4 (and A2.7's third row). That is a governance change of the governing specification, which this phase may not make and which Part H classifies as **NOT PERMITTED** |
| 7 | Can any currently available evidence resolve the ambiguity without author input? | **No.** The caption carries no unit and no definition; the body defines only the barred quantity; the source releases no supplementary material; and the repository has already exercised every admissible reading. Moreover, resolving the *definition* is **necessary but not shown to be sufficient**: for the two readings that can be evaluated, the reproduction contradicts panel (b), so the panel's actual parameter values may also be needed |

**B2 dependency classification: `AUTHOR DATA REQUIRED`** (authoritative source clarification; the
governing rule itself requires it). **B2 remains `NOT_VALIDATED`.**

### B.3 B3 (Layer 2b, Li et al. 2023 Fig. 4(c))

| # | Question | Finding |
|---|---|---|
| 1 | Formulation identity | **Established** (P12V, unchanged): the repository layer matrix equals the source's own Appendix 3 composition `[P0][G][P0]⁻¹` to ≈1e-16 at 60 digits, and the recorded band edges are reproduced. The formulation is *not* the blocker |
| 2 | Exact source-side missing information | The **Fig. 4(c) parameter set and normalisation** (its caption states no values; the gradient values `c̄₁ = 0.15, d̄₁ = 0.25` with ratios `c_R = d_R = 1.5` come from the **Fig. 3(b)** caption and are inherited **by inference only**), the `ω₀`/scaling actually used for that panel (reproduced 4.115e8 Hz vs stated 4.1e8 Hz), and the source's numerical curve data if a quantitative comparison were ever required |
| 3 | Does A2 permit graphical validation with the existing source evidence? | **No.** G1 requires the case to be reproduced from **source-reported** parameters; for panel (c) the parameter set is *not* source-reported, and the inheritance from Fig. 3(b) may not be treated as authoritative (P12S/P12T rulings). G2 then requires the direct comparison to be a validation — the reproduction (lowest branch ω̄ ≈ 0.3391) does **not** overlay the published solid curve (≈0.433–0.436) |
| 4 | Does the published Fig. 4(c) contain sufficient visual information and parameters for a defensible graphical comparison? | The **graph** is adequate; the **accompanying information is not**. A2.1(b) requires both. Per A2.1(c)/A2.7 the case is therefore `NOT_VALIDATED` |
| 5 | Can the mismatch be documented as source-side parameter/normalisation insufficiency? | **Yes — and it is.** The record documents the residual as the source's unstated Fig. 4(c) parameter set/normalisation; the formulation-equivalent reproduction, the classical Rytov limit and the independent [34] reference are mutually consistent, so the residual is source-side. Documentation is *not* validation: A2 provides no route that converts it into one |
| 6 | Does quantitative validation remain impossible? | **Yes.** No source numerical values exist; A2.5 forbids attaching any percentage; the digitisation policy permits curves **only** for overlay drawing |
| 7 | Are author data genuinely required for the CURRENT A2 route? | **Yes.** The minimum for B3's graphical route is the source-reported Fig. 4(c) parameter set and normalisation (and, if that reproduction also mismatches, the source's numerical data to adjudicate). No repository-side step can supply it |

**B3 dependency classification: `AUTHOR DATA REQUIRED`.** **B3 remains `NOT_VALIDATED`**, with
`formulation_status = ESTABLISHED / SOURCE-EQUIVALENT` unchanged.

**Negative control (mandate):** the availability of the graphs is **not** converted into a PASS. B2 and
B3 remain in the not-validated state precisely because A2's graphical route has its own mandatory
information requirement (A2.1(b)/A2.2 G1) and A2.4's B2-specific bar.

## Part C — PCR1 / G3 / G4 chain audit

Governing text used (v1.5 only): the G3 box at line 457 ("Layers 1, 2a and 2b must each be validated by
one of the two admissible evidence routes of Section 13 … a benchmark met by neither route is **not
validated** and fails this gate"), the G3 evidence row (re-scoped by A2.8 for graphically validated
benchmarks), PCR1 item 1 (lines 886–888) and PCR1 item 2, and the G4 ownership rule ("the PI signs G4
only after PCR1–PCR8 are checked against the computation log. A failed PCR blocks submission exactly as
G3 does.").

### C.1 Gate dependency table

| Item | Current evidence | Governing requirement (v1.5) | Satisfied? | Missing item |
|---|---|---|---|---|
| **B1** (Layer 1) | Labelled overlay + documented observables; classical Rytov reproduction branch-by-branch under source-stated parameters; Level 1/2 identities | A2.1(b) + A2.2 G1–G6 (graphical route) | **YES** (route = `GRAPHICAL_VALIDATION`) | none for the A2 route; the A2 manuscript re-tiering edit is a separate, separately authorised task |
| **B2** (Layer 2a) | Solver-side complete; three admissible interpretations; no admissible reproduction | A2.1(b); **A2.4**; A2.7 | **NO** (`NOT_VALIDATED`) | authoritative `l`/`l̄` definition (+ possibly the plotted parameter set) |
| **B3** (Layer 2b) | Formulation identity; reproduction mismatch documented; no source numeric values | A2.1(b); A2.2 G1/G2; A2.7 | **NO** (`NOT_VALIDATED`) | Fig. 4(c) parameter set + normalisation (authoritative) |
| **PCR1** | item 1: B1 only; item 2: main-manuscript presentation exists for the achieved states | "All mandatory published benchmarks (Layers 1, 2a, 2b) are validated by an admissible evidence route" | **NO** | B2 and B3 validation (either route) |
| **PCR2–PCR8** | P12C status matrix: PCR2–PCR8 PASS (evidence in main text, analytics, Table 4, Fig. 5/Table 6, provenance tags, quantitative claims, novelty hedging) | items 2–8 | **YES** | — |
| **G1 / G2** | symbolic/analytic evidence; internal suite green | hard gates G1/G2 | **YES** | — |
| **G3** | consumes PCR1's quantity; A2 relief on its evidence row | G3 box (line 457) | **NO** | same as PCR1's items, plus the in-manuscript evidence rows once available |
| **G4** | — | PI signature after PCR1–PCR8 | **NO** | a complete PCR pass set |
| **P5** | one complete production matrix (Part A conventions, which are the locked ones); parallel record pilot-only; no manuscript claims | production gate; `P5_STATUS.md`: "at most one [S] set and one gate statement can stand" | **NO** (`NOT PASS/OPEN`) | PI reconciliation decision (evidence basis exists) |
| **R-1** | properties A (Route-F config) and C established; property B not | pipeline-level reproducibility | **NO** (`OPEN`) | authorised run/re-baseline |
| **C-1** | discriminant rule validated and applied, not promoted | 5i criterion gate | **NO** (`OPEN` as a gate) | PI decision |
| **G-1** | closed in `bb32253` (tolerance + property semantics) | environment-sensitive guard | **YES** | — |
| **P13** | — | submission | **BLOCKED** | all of the above |

### C.2 Answers

1. **Is PCR1 blocked solely because B2/B3 are `NOT_VALIDATED`?** Yes for its substance: PCR1 item 1
   fails **only** on Layers 2a and 2b, each in the `NOT_VALIDATED` state. PCR1 is **not** blocked by a
   requirement that every benchmark carry a quantitative error — v1.5 explicitly permits a mixture
   (quantitative where source values exist, graphical where they do not), and B1's graphical item is
   satisfied. Item 2's evidence-in-manuscript requirement is separately subject to the A2 re-tiering
   edit, which does not change PCR1's substance.
2. **Could graphical B1 + source-limited B2/B3 satisfy any part of PCR1?** Only B1's item. "Source-
   limited" is not an admissible state (A2.1 is exhaustive and mutually exclusive), so B2's and B3's
   items remain unsatisfied by construction.
3. **If not, why exactly?** A2.4 forbids B2's acceptance under either route while the ambiguity stands;
   B3 fails G1 (parameters not source-reported for panel (c)) and G2 (the reproduction does not overlay
   the published curve); A2.7 maps both to **Not validated**; G3/PCR1 then fail those items.
4. **Is G3 independently blocked by PCR1?** No — G3 *consumes* the same quantity. Its additional
   conditions (evidence rows, completion) become decidable only once the benchmarks are validated, so
   G3 has no independent blocker beyond PCR1's, plus its own manuscript-evidence obligation.
5. **Is G4 independently blocked by G3?** No. G4 is blocked by the **PCR set** (PCR1 fails) and, in
   parallel, by G3; it has no evidence requirement of its own. Any failed PCR blocks exactly as G3 does.
6. **Circularity or redundant blockers?** No circularity: `B2/B3 → PCR1 → G3 → G4 → submission` is
   acyclic, and P5, R-1, C-1 are parallel items. There is deliberate **redundancy** — B2/B3 surface in
   PCR1, G3 and G4 — which is the Blueprint's own enforcement design, not a defect; and P13 BLOCKED is a
   **consequence** of the others, not an independent blocker.

## Part D — P5 final audit

**What remains unresolved.** Two P5 records exist (P5_STATUS.md preserves both verbatim): the Part A
pipeline (pilot 12/12; studies S1, S3–S9 on the 42-point (θ, AR) grid; TV locks; P6 floats; gate PASS)
and the Part B pipeline (pilot 15/15; a parameter lock **request**; gate NOT PASS). They differ in solver
lineage, sampling, reported band count, AR definition/scale, pilot orientation and the TV values; no
numeric cross-validation at a common point has ever been executed.

**What the audit establishes from existing evidence.**

* **Exactly one production matrix exists in the repository** — the Part A one
  (`results/raw/p5_production_raw.json`, `git_commit 15814972…`, `param_hash 09dd73f4…`;
  `results/processed/p5_production_highlights.json` listing S1, S3–S9). The Part B pipeline never ran its
  production set: its record states the frozen cases "are blocked on open parameter decisions
  (TV4/TV6/TV7/TV14)".
* **Those parameter decisions are no longer open**, and they were locked in favour of the Part A
  conventions: `P5_TV_RESOLUTION.md` locks TV4 (`N_seg = 40`, 121 path nodes, 41×81 half-BZ),
  TV6-Case-H (frozen P4A/P4B set, area-preserving `l_iso` scaling), TV7 (`N = 4` reported branches) and
  TV15/TV16 — and those are exactly the values the traceability register carries as `LOCKED [S]`.
* **The manuscript contains no P5-production claims** (P12C §2: zero `production/P5` hits in
  `latex/sections/`), so no published claim depends on the contested gate.
* **Rule R-fit is unaffected**: it governs the 5i estimator, not the P5 production matrix.

**Conclusion.** The *evidence* needed to reconcile P5 exists in-repo; what is missing is the **PI/user
reconciliation decision** — one production record and one gate statement must be adopted, with the other
retained as history. This is not an author-data matter and does not require a re-run; a numeric
cross-validation at a common point would only be needed if the PI prefers a numeric basis for the
decision, and it would be an internal, authorised run. **No solver was re-run in this phase; the
governing `4.173919246515192` result was not touched.** P5 remains `NOT PASS/OPEN`.

*Specified (not executed) cross-validation run, if the PI wants one:* Case H, θ = 45°, AR = 3, `n_mesh`
= 32, area-preserving `l_iso` scaling, the locked 121-node Γ–X–M–Γ path; run both pipelines' solvers on
that single configuration; compare branch frequencies and gap edges at the identical k-points; report
the differences with no threshold attached (a diagnostic, not a gate).

## Part E — R-1 final audit (pipeline-level reproducibility)

Five concerns are separated, per the P12D terminology and P12H §10:

| Concern | Status | Basis |
|---|---|---|
| **1. Scientific reproducibility** (does the physics reproduce?) | Established where it can be tested | independent transfer-matrix / Rytov reproductions; Layer 1–3 analytics; internal suite; Case-C convergence |
| **2. Solver determinism** | Established **for the Route-F configuration only** | `v0` pinned + `tol = 1e-14` + pinned threads ⇒ bit-identical reruns (P12E §10); the **deployed** configuration leaves `v0` unpinned at `tol = 1e-12` |
| **3. Environment sensitivity** | Closed | G-1 CLOSED in `bb32253` (tolerance + property semantics verified for default and `OMP_NUM_THREADS=1`) |
| **4. Fit-subset reproducibility** | Established | frozen Rule R-fit is deterministic and stable: unique verdict for every k, identical verdicts across a 273×-wide F window, reproduces the governing rate bit-exactly, and no recorded realization admits the 32² level (worst-case family margin 4.49×; 1527× at the governing artifact) |
| **5. Governing-artifact reproducibility** | **NOT established** | the governing artifact is one realization of an unpinned start vector; its 32² datum (2.478e-15) is 0.00196× its own reproducibility (1.262e-12) — a fresh nominal run returns a different 32² eigenvalue. P12H §10: "Property B is unachieved and closing it requires the explicitly unauthorized re-baseline" |

**Classification: `B` — CLOSED only after an authorised numerical rerun.**
(`A` is excluded: the missing property is empirical. `C` is excluded as *insufficient*: a governance
decision can only choose to *leave R-1 open* — which is the legitimate status quo — it cannot establish
property B. `D` is excluded: the gap is a specific, executable measurement, not an impossibility.)

*Exact run required (specified, **not executed**):* on the **deployed** 5i configuration
(`tol = 1e-12`, unpinned §5.7 start vector, `n_mesh ∈ {4, 8, 16, 32}`), execute two independent
realizations — equivalently, apply the Route-F two-seed protocol **without** pinning seed or tolerance —
and record, for each level, the relative error `e_i` together with its measured reproducibility `s_i`;
then apply frozen Rule R-fit (unchanged, `F = 3` strict) and report whether the admissible subset and the
fit verdict are invariant across realizations. If instead the PI authorises a **re-baseline**, the
governing artifact would be regenerated under the frozen rule, which would change the published numbers
— an action expressly outside this phase.

## Part F — author-data decision classification

| Item | Classification | Note |
|---|---|---|
| **B2** | **AUTHOR DATA REQUIRED** | the governing rule (A2.4) itself requires authoritative source resolution; no internal route |
| **B3** | **AUTHOR DATA REQUIRED** | the Fig. 4(c) parameter set/normalisation exists only with the authors; no internal route |
| **P5** | **AUTHORISATION REQUIRED** | internally resolvable on existing evidence; the missing item is the PI reconciliation decision (optionally preceded by an authorised, internal cross-validation run) |
| **R-1** | **AUTHORISATION REQUIRED** | the required action is an internal numerical run (or a re-baseline) that only the PI can authorise |

**Author-request status verified unchanged:** `P12M_AUTHOR_REQUEST_DRAFTS.md` (`2f68e66f…`) header
"PREPARED, NOT SENT"; `P12L_AUTHOR_DATA_REQUEST_SPEC.md` (`8acb70f1…`) "no contact has been initiated";
`P12Q_PI_DECISION_HANDOFF.md` "NOT AUTHORIZED / NOT SENT", PI decision pending, no option selected;
`paper9/audit/author_data/` holds only the three unfilled receipt templates. **Nothing was sent; no
author was contacted.**

## Part G — P13 entry criteria (audit only; the gate state is unchanged)

| # | Prerequisite | Governing basis | State |
|---|---|---|---|
| 1 | PCR1 — all three mandatory benchmarks validated by an admissible route | v1.5 PCR1 item 1 | **NOT PASS** |
| 2 | PCR2 — configurations/parameters/curves/errors in the main manuscript | PCR item 2 | **PASS** (A2 re-tiering edit separately unauthorised) |
| 3 | PCR3 — analytical checks | PCR item 3 | **PASS** |
| 4 | PCR4 — eight-test internal suite tabulated | PCR item 4 | **PASS** |
| 5 | PCR5 — mesh convergence with the observed rate + ε_Δ reported | PCR item 5 | **PASS** |
| 6 | PCR6 — parameter provenance tags | PCR item 6 | **PASS** |
| 7 | PCR7 — quantitative support for major claims | PCR item 7 | **PASS** |
| 8 | PCR8 — hedging + research-gap visibility | PCR item 8 | **PASS** |
| 9 | Hard gate G1 | v1.5 gates | **MET** |
| 10 | Hard gate G2 | v1.5 gates | **MET** |
| 11 | Hard gate G3 | v1.5 line 457 | **NOT MET** |
| 12 | Hard gate G4 — PI signature after PCR1–PCR8 | v1.5 gate owner | **NOT MET** |
| 13 | P5 production gate | `P5_STATUS.md` | **NOT PASS / OPEN** |
| 14 | R-1 pipeline-level reproducibility | P12D/E/H | **OPEN** |
| 15 | C-1 5i criterion (as a gate) | P12D/P12H §14 | **OPEN** |
| 16 | G-1 environment-sensitive guard | `bb32253` | **CLOSED** |
| 17 | Author-data decision (route A vs B) | P12L/P12N/P12O/P12P/P12Q | **PENDING** |
| 18 | A2 manuscript re-tiering edit | A2.8 | **NOT DONE** (requires separate authorisation) |
| 19 | PI submission (P13) decision | Blueprint + P12-series register | **NOT MADE** |
| 20 | **P13** | — | **BLOCKED** |

## Part H — no-gate-lowering test

| Proposed closure route | What it would require | Verdict |
|---|---|---|
| Accept B2 as graphical validation with the ambiguity standing | amending/voiding A2.4 and A2.7's third row | **NOT PERMITTED** |
| Accept B3 as graphical validation despite the non-overlaying curve | asserting agreement the evidence does not support; weakening A2.2 G2 | **NOT PERMITTED** |
| Attach any percentage (`<2 %`, `≈1.x %`, any bound) to a graphical result | A2.5 prohibits fabricated precision | **NOT PERMITTED** |
| Digitise the published curves to compute solver errors | digitisation policy (overlay drawing only) + A2.5 | **NOT PERMITTED** |
| Remove/relabel a benchmark (e.g. treat Layer 2a as optional) | changing the mandatory set in the Blueprint | **NOT PERMITTED** |
| Change the ≤ 2 % / ≤ 0.5 % thresholds | A2 leaves all thresholds unchanged; the register records them as invariant | **NOT PERMITTED** |
| Relax Rule R-fit (`F < 3`) to admit the 32² level | altering the frozen pre-declared admissibility rule | **NOT PERMITTED** |
| Close R-1 by restating the estimator-branch closure as solver/pipeline determinism | P12H §10 expressly forbids this restatement | **NOT PERMITTED** |
| Treat the deployed artifact as reproducible although property B is unmeasured | declaring an unmeasured property satisfied | **NOT PERMITTED** |
| Adopt one P5 record without the PI reconciliation decision | performing a governance decision this phase is not authorised to make | **PERMITTED ONLY WITH AUTHORISATION** (no threshold/route change involved) |
| Re-tier the manuscript to the A2 route vocabulary | A2.8 declares this a separately authorised manuscript edit | **PERMITTED ONLY WITH AUTHORISATION** |
| Send the author requests | P12Q: sending is not authorised | **NOT PERMITTED** |

**Result:** every route that would make a blocked gate pass under the current framework requires either
a threshold/route/gate change or the declaration of unmeasured properties, and is therefore **not
permitted**. The only admissible movements are the separately authorised governance/decision actions
listed in Part F.

## Part I — consolidated remaining-blocker matrix

Delivered as `paper9/audit/P12AB_REMAINING_BLOCKER_MATRIX.json` (machine-readable) and
`paper9/audit/P12AB_REMAINING_BLOCKER_MATRIX.md` (human-readable), with the columns
`Blocker | Evidence available | Governing rule | Exact missing item | Who/what supplies it | Can close now? |
Next legitimate action`, covering B2, B3, PCR1, G3, G4, P5, R-1, C-1 and P13. It supersedes the P12AA
matrix, which remains on record as that phase's artifact.

## Part J — decision on the next phase

**`P13 BLOCKED — BOTH EXTERNAL AND INTERNAL BLOCKERS`.**

* **External:** B2 and B3 cannot reach either admissible A2 route without authoritative source
  information; their failure propagates to PCR1 → G3 → G4.
* **Internal:** P5 needs a PI reconciliation decision; R-1 needs an authorised run (or an authorised
  re-baseline); C-1 needs a PI decision promoting the validated predicate set; the A2 manuscript
  re-tiering edit and the submission decision are separately unauthorised.
* P13 is **not** started, and no route exists to start it without those actions. This decision does not
  alter any gate state.

## Parts K–M — tests, regression, immutability

See the final checkpoint (`RECOVERY_CHECKPOINT_P12AB.md`) for the exact counts, the immutability result
and the byte-identity groups.
