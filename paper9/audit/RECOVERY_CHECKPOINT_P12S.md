# RECOVERY CHECKPOINT — P12S (final)

**Purpose:** final recovery point for the P12S graphical-validation phase (B1/B2/B3 reproduction under
Blueprint **v1.5** / amendment **A2**). The pre-work checkpoint for this phase is `270b8ab`.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Starting SHA (phase entry)** | **`70b7b0e9bf28cbb3d103770e68b9147b7bab68ff`** (verified by fetch + `ls-remote`; tree clean) |
| P12S pre-work checkpoint | `270b8ab42246a2c20e0de8395aea8c8e5f068af4` (pushed `70b7b0e..270b8ab`; verified) |
| **P12S content commit** | **`a1816a946f2cf059eaa16144caa529f4f856502f`** (pushed `270b8ab..a1816a9`; verified by fetch **and** `ls-remote`) |
| P12S final checkpoint | **this file's commit** (SHA recorded in the delivery report; pushed + verified the same way) |
| Governing Blueprint | **v1.5** `b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91` (unchanged by P12S) |
| Tree at exit | **clean**; no history rewrite; no new branch; no new auth endpoint |

## Benchmark outcomes (P12S)

| | B1 | B2 | B3 |
|---|---|---|---|
| Source | Li 2024, *Sci. Rep.* 14:24035 | Li 2024, *Sci. Rep.* 14:24035 | Li & Wei 2023, doi 10.1080/17455030.2023.2222189 |
| Figure (page) | Fig. 2(a) (p. 9) | Fig. 2(b) (p. 9) | Fig. 4(c) (p. 15) |
| Observable | 4 lowest branches, ω̄ vs k̄ | dispersion with band gaps | dispersion without thermoelastic coupling |
| **Route** | **GRAPHICAL_VALIDATION** | **NOT_VALIDATED** | **NOT_VALIDATED** |
| **graphical_validation** | **PASS** | **NOT_APPLICABLE** | **NOT_APPLICABLE** |
| **quantitative_error** | **NULL** | **NULL** | **NULL** |
| Reason (one line) | independent Rytov reproduction lies on the published curve branch-by-branch; source publishes no tables | the caption's `l` is dimensionally ambiguous: at the stated a = 0.01 m the gradient correction is O(1e−6) (reproduction collapses onto the classical panel (a)), the barred reading needs ≈ 5.2×10⁴ adaptive digits, the micro reading contradicts the stated cell size | parameters available (ω₀ reproduced 4.115×10⁸ vs 4.1×10⁸ Hz) but the independent dipolar-gradient reproduction does **not** overlay the published panel (lowest branch ≈ 0.35 vs the source's own gradient curve ≈ 0.436 at k̄ = 1; classical limit 0.500; dashed literature [34] curve ≈ 0.50); no tuning performed |
| Ambiguity status | NONE | UNRESOLVED | SOURCE_UNAVAILABLE (formulation/convention) |
| Evidence | `paper9/audit/evidence/p12s/B1_overlay.png` | `…/B2_overlay_interpretations.png` | `…/B3_overlay.png` |

Machine-readable record: **`paper9/audit/benchmark_validation_record.json`**
(sha256 `a53ee7c7fe4609c76569345f07420a2ef58e8e6c0c6bf741dfef7060d07efedd`);
raw run output: `paper9/audit/evidence/p12s/p12s_validation_record.json`.

## Gate state at exit (no promotion, no definition change)

| Item | Status |
|---|---|
| **PCR1** | **NOT PASS** |
| **G3** | **NOT MET** |
| **G4** | **NOT MET** |
| **P5** | **NOT PASS / OPEN** |
| **R-1** | **OPEN** |
| **PCR5** | **PASS** |
| **P13** | **BLOCKED** |

**Exact blocker for PCR1/G3:** B2 remains `NOT_VALIDATED` because the single parameter defining the
source's Fig. 2(b) is dimensionally ambiguous (`l` vs `l̄ = l/b`) and A2.4 forbids a silent choice, and
B3 remains `NOT_VALIDATED` because the source's dipolar-gradient formulation/coefficient convention
cannot be pinned down from the published text (source publishes no tables; data "on reasonable
request"). The author-data request package prepared in P12M/P12L remains the higher-tier route that
would close them quantitatively; **nothing was sent and no author was contacted**.

## Regression and immutability (evidence in `paper9/audit/evidence/p12s/`)

| Check | Result | Log |
|---|---|---|
| Full verification suite ×2 | **151 passed, 1 skipped** each (143 pre-existing + 8 new P12S anti-fabrication tests) | `suite_run1.txt`, `suite_run2.txt` |
| Named guard files (P12C guards, P12H rule-R-fit, P12H C1, P12R route, P12S anti-fabrication) | **70 passed** | `guards.txt` |
| P12J independent cross-check | **43 / 43** | `crosscheck.txt` |
| Immutability anchors | **12 / 12** (v1.3, v1.4, v1.5, rule R-fit, governing JSON, historical TXT, P4B script, provenance anchor, P12E staged patch, `benchmark_evidence.json`, P12M drafts, `PROVENANCE.md`) | `immutability.txt` |
| Manuscript / production / blueprint diffs vs `270b8ab` | **empty** — no production numerical result changed | `immutability.txt` |

## Compliance statements

- **Manuscript: UNCHANGED** (`paper9/latex`, `paper9/tables`, `paper9/figures` byte-identical vs the
  pre-work checkpoint). The Phase J output is a **proposal only**: `paper9/audit/P12S_MANUSCRIPT_IMPACT.md`.
- **Source PDFs: UNCHANGED** — Li 2024 `2ac5f45d77ee37569f69e8890b70200ae6982f669ecaccf6cb5aa162f0340513`,
  Li 2023 `3f5103380302609ef2dfe76c8ade09cae79b2ebbd4fdb4da228576c331191aa7` (as recorded in
  `paper9/audit/benchmark_validation_record.json → source_immutability`; PDFs read-only, figures
  extracted into a separate directory).
- **Digitisation** used only as a graphical-registration intermediate; no residual became an error, no
  percentage was produced, and the rejected 0.48 % claim is not restated anywhere.
- **Author contact:** NONE. **Requests sent:** NONE. **Substitute values:** NONE. **Thresholds:** unchanged.
- Blueprint v1.5 not reopened or rewritten; no gate definition altered; no P13 work started.

## Chain (most recent)

`… → 1b05236` (P12Q final) `→ 26dbcf8` (P12R pre-work) `→ 53d40c3` (P12R amendment) `→ 70b7b0e`
(P12R final) `→ 270b8ab` (**P12S pre-work**) `→` **`a1816a9` (P12S content)** `→` *this checkpoint*.
