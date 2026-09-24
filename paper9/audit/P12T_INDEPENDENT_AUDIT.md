# P12T — independent forensic audit of the P12S graphical-validation evidence

**Phase entry (verified):** `b80ff67348f5b0fbf4cce28aa2ff6ee288ca20df` — local = `origin/phase-1-symbolic`
= `ls-remote`, clean tree. **Pre-work checkpoint:** `71e6049d88ec5a2ee26b65a5e088562d841c47bd`
(pushed + verified before any audit work).
**Mode:** audit only. The Blueprint, the manuscript, the source PDFs and every P12S artifact were read
but **not modified**. No B1/B2/B3 parameter, formulation or configuration was changed or tuned; no
percentage was assigned to any benchmark; no author was contacted and nothing was sent.

**Independent tooling (this audit's own code):** `paper9/audit/evidence/p12t/independent_checks.py` →
`independent_checks.json`, plus `overclaim_search.txt`, `b2_registry_crosscheck.txt`,
`immutability.txt`, `suite_run1.txt`, `suite_run2.txt`, `guards.txt`, `crosscheck.txt`.

---

## 1. Verification ledger (everything re-derived, never trusted)

| # | P12S statement | Independent method (P12T) | Result |
|---|---|---|---|
| 1 | Fig. 2(a)/(b) are Li 2024 Fig. 2, p. 9; captions exactly as quoted | `pypdf` text extraction of `analytic/li2024/s41598-024-75049-1.pdf` | **confirmed** (caption on PDF index 8 = journal p. 9) |
| 2 | AlN: ρ = 3.23×10³, a₃ = 8.4×10⁻¹¹, c₃₃ = 3.9×10¹¹; **a_A = a_B = 0.01 m** | same, p. 7 | **confirmed** (literal: `ρ =3.23 × 103 kg/m3, a3 =8.4 × 10−11 C2/Nm2, c33 =3.9 × 1011 Pa, aA = aB =0.01 m`) |
| 3 | Normalisation: **l̄ = l/b**, l̄₁ = l₁/b, **k̄ = kb/π**, ω̄ = ω/ω₀, ω₀ = 2π/(a_A√(c₃₃/ρ) + a_B√(c₃₃′/ρ′)) | same, Eq. (55) region | **confirmed** (`¯l = l b`, `¯l1 = l1 b`, `¯k = kb π`, `¯ω = ω ω0`, `ω0 =2 π/(aA√c33/ρ + aB√c′33/ρ′)`) |
| 4 | b = a_A + a_B (cell = 0.02 m) | same, Eq. (51) text | **confirmed** |
| 5 | B1 reproduction: band edges | **own 2×2 transfer-matrix trace root-finding** (different method; order-commutation residual 0.0) | **confirmed**: edges 0.47987, 0.51959, 0.97946, 1.02102, 1.49817, 1.50193, 1.98090, 2.01853 vs P12S gaps (0.4799/0.5199, 0.9795/1.0209, 1.4977/1.5005, 1.9773/2.0164) — agreement inside the 7.5×10⁻⁴ scan grid |
| 6 | B1 graphical agreement with the published curve | **own digitisation** of `B1_panel.png` at k̄ = 0, 0.25, 0.5, 0.75, 1 | **confirmed**: published {0.0225, 0.9794, 1.0244, 1.9719} / {0.1313, 0.8743, 1.1295, 1.8687} / {0.2552, 0.7523, 1.2514, 1.7467} / {0.3790, 0.6266, 1.3771, 1.6210} / {0.4803, 0.5253, 1.4991} vs computed {0, 0.9795, 1.0210, 1.9809} / {0.1247, 0.8739, 1.1269, 1.8736} / {0.2494, 0.7501, 1.2509, 1.7495} / {0.3734, 0.6262, 1.3754, 1.6249} / {0.4799, 0.5196, 1.4998}: **max \|Δω̄\| ≈ 0.006 ≈ 1.6 px** |
| 7 | B2: (l k)² ≈ 4×10⁻⁶ at the stated geometry | own arithmetic with k_A = ω₀/V_A = 204.055 m⁻¹ | **confirmed**: 4.1639×10⁻⁶ (dimensional l = 10⁻⁵ m), 1.6655×10⁻⁹ (barred l = 2×10⁻⁷ m); l/b = 5×10⁻⁴; l/a = 10⁻³ |
| 8 | B2: barred reading needs ≈ 5.2×10⁴ digits | own re-run of `StableB2.required_dps()` + own derivation log₁₀(e)·Λ | **confirmed and explained**: required_dps = **52131**, Λ = 119999.99, log₁₀(e)·Λ = 52115.3, engine policy `ceil(0.4343·Λ)+15 = 52116+15 = 52131` — exactly the reported value |
| 9 | B2: reproduction at source geometry coincides with the classical panel | own classical edges vs the recorded CFG-DIM-MACRO edges | **confirmed**: differences ≤ 7×10⁻⁴ in ω̄ (below figure resolution) |
| 10 | B2: published Fig. 2(b) deviates strongly from 2(a) | own digitisation of both panels | **confirmed**: at k̄ = 0 (b) {0.867, 1.164, 1.776} vs (a) {0, 0.980, 1.021, 1.981}; at k̄ = 1 (b) {0.336, 0.645, 1.412, 1.513} vs (a) {0.480, 0.520, 1.500, 1.981} |
| 11 | B2: the micro reading also fails to match the published panel | production registry `p11d_b2_gap_registry.json` (pre-existing, adaptive-precision exact z-test) vs P12S grid scan | **confirmed**: registry CFG-DIM-MICRO bands [0.078, 0.2422], [0.3783, 0.383], [0.742, 0.7599], [0.7851, 1.1028], [1.1234, 1.4346]… vs P12S [0.0815, 0.2446], [0.382, 0.3863], [0.7425, 0.7639], [0.7854, 1.103], [1.1245, 1.4378] — ≤ 0.005 (grid resolution); the published (b) lowest branch at k̄ = 1 is 0.336, matching neither reading |
| 12 | B3: Fig. 4(c) on Li 2023 p. 15, caption quoted correctly | `pypdf`, `analytic/li2023/17455030.2023.2222189.pdf` | **confirmed** (caption on PDF index 14 = p. 15: "(c) the dispersion curves for the gradient elastic solids and the comparison with literature [34]") |
| 13 | B3: p. 15 text = dipolar gradient, thermoelastic coupling ignored | same | **confirmed** ("Figure 4(c) shows the dispersion and bandgap for the dipolar gradient elastic solids but ignoring the thermoelastic coupling") |
| 14 | B3: no parameters in the 4(c) caption; values from p. 14 + Fig. 3(b) caption | same (p. 14 = index 13 and p. 15 captions) | **confirmed**; the source contains **no explicit "Fig. 4(c) uses Fig. 3(b)'s values" sentence** (searched "same/identical/as in/refer to … Fig. 3 / Section 4.2") — the linkage is a **labelled inference**, which is how P12S records it ("inheritance is inferred from the case definition") |
| 15 | B3: ω₀ = 4.114×10⁸ vs stated 4.1×10⁸ Hz | own computation from the source's own formula, p. 14 | **confirmed**: 411 423 336.098 Hz (0.347 % above the stated rounded value) |
| 16 | B3: reproduced lowest branch ≈ 0.35 at k̄ = 1 | re-run of the audited artifact (`p12s_reproduce.b3_dispersion`, WORK redirected) | **confirmed**: first stop-band upper edge 0.3391 → lowest branch tops at ω̄ ≈ 0.339 |
| 17 | B3: the reproduction does not overlay the published panel | own solid/dashed family tracking on `B3_panel.png` (legend in the panel: **solid = "Present"**, **dashed = "Li and Wei [34]"**) | **confirmed**: the source's own *solid* curve reaches **ω̄ = 0.436** at k̄ = 1 (present in 98 % of the last 60 columns); reproduction 0.339 → mismatch −0.097 |
| 18 | Gates: B1 graphical + B2/B3 not validated ⇒ PCR1 NOT PASS, G3/G4 NOT MET | Blueprint v1.5 §13 (A2.7 decision table, lines 1129–1143; line 803; A2.8 lines 1153–1156) + classifier re-derivation | **confirmed** — A2.7: "Graph only, parameters ambiguous or insufficient → **Not validated**: no claim; the G3/PCR1 item fails for that benchmark" |

## 2. A — B1 (Li 2024 Fig. 2(a))

* Source figure/page, classical parameter set, normalisation, interface/BC and branch identities:
  **independently verified** (rows 1–4).
* Reproduction: **independently verified with a different numerical method** (row 5) and against the
  published curve by an independent digitisation (row 6): max deviation ≈ 0.006 in ω̄ (≈ 1.6 px), i.e.
  within the printed line width. The graphical claim is therefore supported.
* **No hidden quantitative percentage:** the record carries `quantitative_error: null`, the audit text
  says "no percentage asserted", and no error-like number appears anywhere in the P12S code or record
  (overclaim search §7). The rejected **0.48 %** metric is mentioned only in the form "not used /
  rejected" and is absent from the machine-readable record.
* **Not upgraded:** the verdict stays at the graphical tier; no route/status was promoted by this audit.

**B1 verdict: VERIFIED WITH CORRECTION REQUIRED** (descriptive fields only — finding **F1**; the route
`GRAPHICAL_VALIDATION`/PASS itself is verified and is **not** upgraded).

## 3. B — B2 (Li 2024 Fig. 2(b))

* **Exact source notation:** caption `b gradient elasticity (l = 10⁻⁵, l₁ = 2 × 10⁻⁵, f = 0, L = 5, L₁ = 5, F = 0)`;
  the panel image itself is labelled `l = 1×10⁻⁵`.
* **Exact definition of b:** `b = a_A + a_B` (Eq. 51 text) = 0.02 m with the stated a_A = a_B = 0.01 m.
* **Stated values:** only `l` and `l₁` in the caption; the source's body text does **not** give
  dimensional `l` values in metres for this example — the ℓ-family is dimensioned only through Eq. (55).
* **Is either interpretation justified by the paper?** *No.* The dimensional reading (l = 10⁻⁵ m) is
  arithmetically admissible but contradicts the published panel (b); the barred reading (l̄ = 10⁻⁵ ⇒
  l = 2×10⁻⁷ m) follows the paper's own normalisation but makes the evanescent exponent enormous. The
  source contains no sentence that resolves it. **The ambiguity is therefore genuinely unresolved in the
  source — the audit does not resolve it by outside assumption.**
* The O(10⁻⁶) statement is **correctly derived** (row 7) and the "coincides with the classical panel"
  consequence is **verified numerically** (row 9).
* The ≈ 5.2×10⁴-digit statement is **actually supported by the computation** (row 8) and its mechanism is
  exact: `ceil(0.4343·Λ) + 15`.
* "Micro reading contradicts the stated cell size" is **technically justified**: the micro configuration
  requires a = 1×10⁻⁵ m while the source states a_A = a_B = 0.01 m (the repository's own registry labels
  that configuration "dimensional-micro (a=l=1e-5 m, **modified-geometry scale**)").
* No interpretation matches the published panel (rows 10–11).

**B2 verdict: VERIFIED** (route `NOT_VALIDATED`, ambiguity `UNRESOLVED`, `quantitative_error` NULL). No
correction required; no promotion.

## 4. C — B3 (Li 2023 Fig. 4(c))

* Figure/page and caption: verified (rows 12–13).
* Parameter information: the material data are on p. 14; the gradient-case values (c̄₁ = 0.15, cR = 1.5,
  d̄₁ = 0.25, dR = 1.5) appear in the **Fig. 3(b) caption**. **No explicit inheritance sentence exists in
  the source** (row 14); P12S records the linkage as an inference, which is the correct treatment and is
  not an overclaim. The manuscript's own [S] provenance tag already states this.
* ω₀: verified (row 15).
* Independent dipolar-gradient formulation: **not independently reconstructible by this audit** — the
  source's convention cannot be pinned down from the text, and the repository implementation cannot be
  validated against its own classical limit (overflow of sinh(τa) as the gradient parameters → 0,
  reproduced by this audit). This is precisely the blocker P12S records.
* Reported discrepancy: reproduced 0.339 vs the source's own **solid "Present"** curve 0.436 at k̄ = 1
  (row 17) — a −0.097 mismatch. NOT_VALIDATED follows without any tuning (no parameter was changed
  between the recorded run and this re-run).
* **`SOURCE_UNAVAILABLE` is justified** for the formulation/coefficient convention of the source's
  dipolar-gradient model.
* **Defect:** the clause "the source's own figure … require 0.50" is **wrong** — the source's own gradient
  curve is at 0.436; 0.50 is the *classical* limit (exactly 0.500) and/or the dashed literature [34]
  curve. See finding **F2** (including the copy that P12S propagated into its manuscript-impact proposal).

**B3 verdict: VERIFIED WITH CORRECTION REQUIRED** (finding **F2**; the `NOT_VALIDATED` route itself is
verified).

## 5. D — graphical-validation governance standard

`paper9/verification/suite/benchmark_validation_route.py` was exercised with **synthetic** inputs only
(never with B1/B2/B3 outcomes to force a result):

| Probe | Result |
|---|---|
| genuine numerics, 1.4 % (general, ≤ 2 %) | `QUANTITATIVE_VALIDATION`, PASS, error 1.4, threshold 2.0 |
| genuine numerics, 2.6 % | FAIL against the same 2.0 threshold |
| genuine numerics, 1.4 % with `classical_limit=True` | FAIL against the 0.5 threshold (**both thresholds unchanged**) |
| graph-only + overlay | `GRAPHICAL_VALIDATION`, `quantitative_error = None`, no threshold attached |
| graph-only + unresolved ambiguity | `NOT_VALIDATED`, error None |
| insufficient parameters | `NOT_VALIDATED`, error None |
| **% supplied without source numerics** | **`FabricatedPrecisionError`** raised (A2.5) |

* No visual overlay is converted into a number (`quantitative_error` is `None` on the graphical route in
  every probe and in the committed record).
* No digitisation residual exists in the P12S code at all (grep for `residual`/`resid`: no hits), so no
  residual can be called solver error.
* No ≤ 2 % claim is assigned without reference data; the thresholds (2.0 / 0.5) are unchanged and the
  rejected 0.48 % value appears nowhere in the classifier.
* The hierarchy is enforced (`QUANTITATIVE=3 > GRAPHICAL=2 > NOT_VALIDATED=1`), and the eight P12S
  anti-fabrication guards pass.

**Governance verdict: VERIFIED.**

## 6. E — gate logic under Blueprint v1.5

Blueprint v1.5 §13/A2.7 (lines 1129–1143) states that a benchmark whose graph has ambiguous or
insufficient parameters is **not validated** and "the G3/PCR1 item fails for that benchmark"; line 803
requires G3 to be met "either quantitatively at ≤ 2 % or … by the graphical route of Section 13";
lines 1153–1156 (A2.8) forbid automatic promotion. Re-deriving the routes through the classifier from the
recorded facts reproduces B1 = `GRAPHICAL_VALIDATION`, B2 = `NOT_VALIDATED`, B3 = `NOT_VALIDATED`.

Therefore **PCR1 NOT PASS** (B2 and B3 anchors fail), **G3 NOT MET**, and **G4 NOT MET** (G4 is signed
only after PCR1–PCR8 are checked, line 909). The P12S conclusion is correct; the gate definitions were
**not** changed, and nothing was promoted by either phase. **Gate-logic verdict: VERIFIED.**

## 7. F — source-evidence traceability

Every substantive P12S conclusion maps to source + artifact + computation (ledger rows 1–18). Two
statements are flagged as **insufficiently evidenced**: the B1 vertex strings (F1) and the B3 "0.50"
baseline clause (F2). Both are *descriptive*; no route, gate or numerical production result depends on
them. The B3 parameter inheritance is correctly labelled as an inference rather than a source statement.
**Traceability verdict: TRACEABLE, with the two flagged statements.**

## 8. G — overclaim search

(`paper9/audit/evidence/p12t/overclaim_search.txt`)

* No P12S artifact claims B1 quantitative validation, B2 validation despite ambiguity, B3 validation
  despite the failed overlay, or "agreement within X %".
* No "validated against Li et al." phrasing without a tier: the only `validated against` occurrence is
  the correct negative statement about the B3 implementation's classical limit.
* No PCR1/G3 satisfaction claim: every mention is "NOT PASS"/"NOT MET"/"unchanged".
* The rejected 0.48 % appears only as "rejected / not restated".
* **Manuscript-side (report only, no change made):** `sec05_verification.tex` line 36 still records B3 as
  "GRAPHICAL ONLY / PARTIAL" and line 48 still says G3 remains NOT MET "until author-released
  floating-point datasets are made publicly available". Under A2 the second sentence is now narrower than
  current policy, and P12S's evidence changes B3's tier wording. Both are already listed in
  `paper9/audit/P12S_MANUSCRIPT_IMPACT.md` (J.3, J.4) — i.e. the discrepancy is documented, not hidden.
  **No manuscript edit was made or proposed as applied.**

## 9. H — independent reproduction (numbers)

Recomputed by audit code: B1 band edges (own TM method), B1/B2/B3 panel measurements (own digitisation),
B2 (l k)², B2 barred precision requirement, B3 ω₀, B3 k̄ = 1 branch comparison, B2 registry cross-check.
All values are in `independent_checks.json`. **Every P12S scalar that this audit could independently
recompute was confirmed** — except the two descriptive statements in F1/F2.

## 10. I — immutability

`paper9/audit/evidence/p12t/immutability.txt`: **17/17** — Blueprint v1.3 `ca71b91a…`,
v1.4 `2ae0b1e8…`, v1.5 `b96c8e76…`, Rule R-fit `d4fed492…`, governing P4B JSON `38384363…`,
historical TXT `1daf0f32…`, P4B script `b1c8d996…`, provenance anchor `6154a23b…`, P12E staged patch
`03b902d2…`, `benchmark_evidence.json` `e9191506ca0fb07a`, P12M drafts `2f68e66f…`, `PROVENANCE.md`
`f4ab0b71…`, plus the five P12S artifacts under audit. Source PDFs match the hashes P12S recorded
(Li 2024 `2ac5f45d…`, Li 2023 `3f510338…`). `git diff` vs `a1816a9` shows **no changes** to the P12S
artifacts, the manuscript, production code, the blueprint directory or the source-PDF directory; no
blueprint edit occurred during P12T.

## 11. J — regression (actual results, not assumed)

| Run | Result |
|---|---|
| full suite, run 1 | **151 passed, 1 skipped** (11.01 s) |
| full suite, run 2 | **151 passed, 1 skipped** (22.29 s) |
| P12S + P12R + P12C guard files (named) | **36 passed** (8 + 17 + 11) |
| P12J cross-check | **43 / 43** |

Baseline expectation (151P/1S) reproduced; no test was added, removed or modified by this phase.

## 12. Findings register (recorded, NOT fixed — per phase rule)

| ID | Severity | Location (exact) | Defect | Verified truth | Recommended correction (not applied) |
|---|---|---|---|---|---|
| **F1** | LOW–MEDIUM (descriptive) | `paper9/audit/benchmark_validation_record.json:30`; same string in `paper9/audit/P12S_GRAPHICAL_VALIDATION_AUDIT.md:84` | "branch vertices omega_bar(0)=0.0000/1.4799/1.9799; omega_bar(1)=1.4799/0.5099" does not match the actual branches | k̄ = 0: **0.0000 / 0.9795 / 1.0210 / 1.9809**; k̄ = ±1: **0.4799 / 0.5196 / 1.4998 / 1.9809**; published panel k̄ = 0: {0.0225, 0.9794, 1.0244, 1.9719}, k̄ = 1: {0.4803, 0.5253, 1.4991} | replace the vertex list with the verified values; the graphical verdict is unchanged |
| **F2** | MEDIUM (misstated baseline) | `paper9/validation/p12s_run.py:184–185`; `paper9/audit/benchmark_validation_record.json:165`; `paper9/audit/P12S_GRAPHICAL_VALIDATION_AUDIT.md:111–112`; `paper9/audit/RECOVERY_CHECKPOINT_P12S.md:27`; propagated into the proposal `paper9/audit/P12S_MANUSCRIPT_IMPACT.md:37` | "the source's own figure and the exact classical-limit value require 0.50" attributes 0.50 to the published figure | the source's own **solid ("Present")** curve reaches **0.436** at k̄ = 1 (98 % column presence); **0.500** is the exact classical limit; the dashed literature [34] curve is ≈ 0.504 | "…the lowest branch reaches ω̄ ≈ 0.34 at k̄ = 1 whereas the source's own gradient curve requires ≈ 0.44 (classical limit 0.50)…"; the route `NOT_VALIDATED` is unchanged |
| **F3** | LOW (internal inconsistency) | `paper9/validation/p12s_run.py:178` vs `:184–185` | the same file states the published branch reaches "(1, ~0.45)" and later that the figure "require[s] 0.50" | 0.436 measured → the ":178" reading is the correct one | align the two statements when correcting F2 |
| **F4** | INFO (no action) | `P12S_GRAPHICAL_VALIDATION_AUDIT.md` §Phase E | "numerically infeasible" is a practical statement (52 131-digit working precision), not a mathematical impossibility | `required_dps = 52131` reproduced exactly, mechanism `ceil(0.4343·Λ)+15` | none — the wording is already qualified |

No defect was found in the **route decisions**, the **gate consequences**, the **classifier**, the
**thresholds**, any **production numerical result**, or the **immutability** of any governing artifact.

## 13. Final decision categories

| Item | Verdict |
|---|---|
| **B1** | **VERIFIED WITH CORRECTION REQUIRED** (F1; route `GRAPHICAL_VALIDATION`/PASS verified, not upgraded) |
| **B2** | **VERIFIED** (`NOT_VALIDATED`, ambiguity genuinely unresolved in the source) |
| **B3** | **VERIFIED WITH CORRECTION REQUIRED** (F2/F3; route `NOT_VALIDATED` verified) |
| Graphical-validation governance | **VERIFIED** |
| **PCR1** | **NOT PASS** (unchanged) |
| **G3** | **NOT MET** (unchanged) |
| **G4** | **NOT MET** (unchanged) |
| **P5** | **NOT PASS / OPEN** (unchanged) |
| **R-1** | **OPEN** (unchanged) |
| **PCR5** | **PASS** (unchanged) |
| Manuscript | unchanged (0 diffs); P12S impact list remains a proposal |
| Author requests | NOT SENT; no contact; no data received |
| P13 | BLOCKED (not started) |
