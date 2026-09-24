# P12C Case-C Number Traceability Artifact (Part B)

Audit date 2026-09-24 · repo `phase-1-symbolic @ 0d985029` · read-only pass.
Purpose: end-to-end trace for **every Case-C number appearing in the current manuscript**:
`raw JSON → production script → parameter snapshot → solver → guard/test → manuscript statement`.
This file is the new traceability artifact for Case-C numbers; the master
`paper9/audit/traceability_matrix.{csv,json}` was **not modified** (it is referenced by the
remediation guard tests and by PCR/G claims; its Case-C entries are issue-level (TV6-CaseC, TV14),
not number-level — that gap is closed here).

## 1. Source chain (files and roles)

| # | artefact | produced by | role |
|---|---|---|---|
| S1 | `results/raw/p11_caseC_raw.json` | `production/p11_caseC_run.py` | baseline dispersion + 5-point radius sweep (P11B era, preserved) |
| S2 | `results/raw/p11_caseC_convergence.json` | `production/p11_caseC_convergence.py` | **P11B-era** mesh (X-gap), quadrature, BZ + inequality blocks (preserved, partially superseded) |
| S3 | `results/raw/p11d_caseC_gap_convergence.json` | `production/p11d_caseC_gap_convergence.py` | **authoritative** Δ_complete for 4²/8²/16² on 11²/21²/41² + `per_mesh_gaps` |
| S4 | `results/raw/p11d_deltaX_check.json` | same as S3 | Δ_X for 4²/8²/16² (explicit separation from Δ_complete) |
| S5 | `results/raw/p12c_caseC_32_gap_convergence.json` (+`.sha256`) | `production/p12c_caseC_gap_convergence.py` | 32² cells + path, validation v1–v5 |
| S6 | `results/raw/p12c_caseC_64_gap_convergence.json` (+`.sha256`) | `production/p12c_caseC_gap_convergence_64.py` | 64² cells + path, `post_64_report` |
| P | `params/params_master.yaml` + `metadata.parameter_snapshot` in S5/S6 | — | parameter snapshot (`parameter_hash_sha256 = bb112a522e094b2b…`) |
| G | `verification/suite/test_p11_case_c.py`, `test_p11b_forensic_remediation.py`, `test_p11d_remediation.py`, `test_p12c_caseC_32.py`, `test_p12c_caseC_64.py` | — | guards |

Note on S2: `results/raw/README.md` declares “superseded runs are kept, not deleted”; S2 is
therefore historical evidence, still the sole source of the quadrature block (see F-1/F-2) and
the P11B-era `gap_at_X` series.

## 2. Number-level trace table (manuscript → source)

“Match” = manuscript rounding agrees with the raw value. All values below were re-read/re-derived
in this audit (P12C_POST_CLOSEOUT_FORENSIC_AUDIT.md, Part A).

| # | Manuscript location | Number | Quantity | Raw source (field) | Guard | Match |
|---|---|---|---|---|---|---|
| 1 | sec06 ¶baseline; Fig.8(a) caption | 4.5698 | max ω̄₃ (4², 21²) | S3 `4x4_FE_21x21_BZ.omega3_max` = 4.56979291726 | test_p12c_caseC_32 (via registry cell), S2 | ✔ |
| 2 | idem | 7.1430 | min ω̄₄ (4², 21²) | S3 `…omega4_min` = 7.14297983210 | idem | ✔ (7.14298) |
| 3 | idem | 2.5732 | Δ_complete (4², 21²) | S3 `4x4_FE_21x21_BZ.delta_complete` = 2.57318691483 | test_p11d_remediation, test_p11b (S2) | ✔ |
| 4 | idem | 2.5728 | Δ_complete (4², 41²) | S3 `4x4_FE_41x41_BZ.delta_complete` = 2.5728033505 | test_p11d_remediation | ✔ |
| 5 | idem | 43.94 % | Δ/ω̄_mid (4², 21²) | S2 `bz_refinement.21x21.norm_gap_pct` = 43.94; S3 `norm_gap_pct` 43.938 | idem | ✔ |
| 6 | idem | ~4×10⁻⁴ | BZ sampling accuracy (21²→41² at 4²) | S3 (2.5731869→2.5728034 = 3.84e-4) + P11D audit N_seg=40 path control | — | ✔ |
| 7 | sec06 inequality eq. | 2.6114 / 2.7563 / 3.2871 | Δ_ΓX / Δ_XM / Δ_MΓ (4², N_seg 20) | S2 `inequality_audit.delta_{GX,XM,MG}`; S3 `per_mesh_gaps.4x4` = 2.61137796314 / 2.75630165355 / 3.28711134211 | test_p11b (`test_caseC_hierarchy_inequalities`), test_p11d | ✔ |
| 8 | idem | 2.5732 = Δ_path = Δ_complete | path & complete gap (4²) | S2 `inequality_audit.delta_path/delta_complete`; S3 `per_mesh_gaps.4x4.delta_path` = 2.57318691484 | idem | ✔ |
| 9 | sec06 mesh series | 2.5732, 2.2504, 2.0722, 1.9736, 1.9179 | Δ_complete (21², 4²→64²) | S3 cells 4/8/16; S5 `cells_32[…21x21].delta_complete` = 1.973636314930; S6 `cells_64[…21x21]` = 1.917889117169 | test_p12c_caseC_32, _64 (pin series + monotone) | ✔ |
| 10 | idem | 200 / 648 / 2312 / 8712 / 33800 | global dofs | 8(N+1)²; S5/S6 `fe_dofs` = 8·33² / 8·65² | test_p12c_caseC_32 (8·33·33), _64 (8·65·65) | ✔ |
| 11 | idem | Δ_X = 2.7563, 2.2504, 2.0722, 1.9736, 1.9179 | X-point gaps | S4 `delta_X` = 2.75630165355 / 2.25038841540 / 2.07224842705; S5 `path_32.delta_XM` = 1.9736363157; S6 `path_64.delta_XM` = 1.9178891171 | test_p11d_remediation, test_p12c_32/64 | ✔ |
| 12 | idem | d₁ 0.3228, d₂ 0.17814, d₃ 0.09861, d₄ 0.05575 | successive decrements | recomputed from #9; S6 `post_64_report.successive_decrements` = {d2 0.17814 (hard-coded), d3 0.09861211213, d4 0.05574719776} | test_p12c_caseC_64 (recomputes r from cells) | ✔ |
| 13 | idem | 0.552 / 0.554 / 0.565 | decrement ratios | recomputed; trigger r = S6 `parent_rule_evaluation.r` = 0.55356527777 (rule text: `metadata.rule_64`) | test_p12c_caseC_64 (`assert abs(r − recompute) < 1e-9`, `r ≥ 0.5`) | ✔ |
| 14 | idem | “≥0.5 triggered 32² and 64²” | decision rule | S5 `metadata.rule_64` (pre-registered), S6 `trigger` + `parent_rule_evaluation.decision` (“RUN 64x64”) | test_p12c_caseC_64 (`"0.5" in trigger`, decision) | ✔ |
| 15 | sec06 quadrature item | 2.7563, 2.7226, 2.7862 | X-point gap at 4² for 16/36/64 Gauss pts | **S2** `quadrature_sensitivity.{4x4,6x6,8x8}.gap_at_X` (S2 = P11B-era, preserved) | test_p11b (`test_caseC_quadrature_sensitivity`) | ✔ value; label see F-1 |
| 16 | idem | 1.22 % | “quadrature invariance to within” | P11B_REMEDIATION_AUDIT table: −1.22 % / +1.08 % vs baseline; 1.22 % = max one-sided | idem | ✔ value; framing see F-2 |
| 17 | sec06 BZ item | < 5×10⁻⁴; 2.5732→2.5728; “identical to 4 dp at 8²/16²” | BZ-grid sensitivity | S3 cells 11²/21²/41² (8²: 2.25038841540 all grids; 16²: 2.07224842705/…42706) | test_p11d_remediation | ✔ |
| 18 | idem | “identical to 6 decimals at 32²/64² (11²↔21²)” | idem | S5/S6 cells: 32² 1.973636314301 vs …314930 (Δ6.3e-10); 64² 1.917889115331 vs …117169 (Δ1.8e-9); 6 dp agreement: 1.973636 vs 1.917889 ✔ | test_p12c_32/64 | ✔ |
| 19 | sec06 sweep ¶ Fig.8(b) | 0.8288 (16.61 %), 2.5732 (43.94 %), 2.4426 (37.00 %) | Δ_complete at r₀/a = 0.20/0.30/0.40 (4², 21²) | S1 `radius_sweep.r_20/r_30/r_40.gap_34.delta_complete` = 0.8288311899 / 2.5731869148 / 2.4425733578; `norm_gap_width` = 0.1661045687 / 0.4393813438 / 0.3700322929 | test_p11b (sweep + inequality) | ✔ |
| 20 | idem | f = 28.27 %; f ∈ [12.6 %, 50.3 %] | filling fractions | 0.2827433388230814; r_20/r_40 `filling_fraction` = 0.1256637061 / 0.5026548246 | test_p11b | ✔ |
| 21 | sec06 material ¶ | χ_μ = 25.0, χ_ρ = 5.546 | contrasts | S1 `metadata.contrast_mu/contrast_rho` = 25.0 / 5.546 | test_table2_parameter_provenance_tags | ✔ |
| 22 | idem | ρ_m 1142, μ_m 1.48 GPa, λ_m 4.57 GPa, ρ_i 6333, μ_i 37.0 GPa, λ_i 95.0 GPa; ℓ_m=0.10L, ℓ_i=0.20L | dimensional material data | Zhan & Wei (2010) Table 1 per Table 2 rows + nondimensional consistency: λ_m/μ_m = 3.088 = S1 `lam(m)`, λ_i/μ_i = 2.568 = 64.19/25, ℓ² = 0.01/0.04 | test_table2_parameter_provenance_tags | ✔ (tag audit = Part C) |
| 23 | sec06 material ¶ | c_{t,m} 1138.4 m/s; ω_{0,C} = πc_{t,m}/L | nondimensionalisation | derived: √(1.48e9/1142) = 1138.4 | — | ✔ |
| 24 | sec08 ¶2; sec09 ¶5 | series repeat + “2.5732 = 4×4-mesh width, not converged” | status statements | #3, #9; “not mesh-converged” asserted against S5/S6 & sec06 by guards | test_p12c_caseC_32/64 (manuscript honesty tests) | ✔ |

## 3. Flags (Part B findings)

**F-1 (C-class, manuscript).** The quadrature item (#15) reports S2’s **`gap_at_X`** values —
X-point directional gaps at the **4×4 mesh** — but calls them “stop-band widths” inside a section
otherwise about Δ_complete. The same paragraph uses 2.7563 one sentence earlier explicitly as
Δ_X (= Δ_XM at 4²). A reader can misread these as complete-gap sensitivities. The manuscript does
not say the quadrature study was performed on the 4×4 mesh. Recommended minimal fix (subject to
Part C edit rules): label as “X-point gap at the 4×4 mesh”. Not corrected in this pass.

**F-2 (B/C-class, manuscript).** “Demonstrating quadrature invariance to within 1.22 %” reproduces
the P11B audit’s one-sided framing (−1.22 % / +1.08 % vs the 4×4 baseline). Total spread is
2.31 % (2.7226→2.7862). The claim is defensible only as “max deviation from the 4×4 rule ≤1.22 %”;
as written it can be read as a 1.22 % band, understating the spread. Not corrected in this pass.

**F-3 (A-class, inert).** `p12c_caseC_gap_convergence_64.py` hard-codes `d2 = 0.178140`
(`finalize`); used only for the context field `successive_decrements.d2_16vs8`. The reported r₄
uses the measured d₃. Also `p12c_caseC_gap_convergence.py` embeds the rounded string “d3=0.0986”
in a descriptive note. Both are display-only; no impact on any manuscript number (#12 recomputed
from cells). Scripts deliberately not modified (standing rule).

**F-4 (B-class, source hygiene).** S2 (`p11_caseC_convergence.json`, P11B era) remains the source
for #15/#16 only; its `mesh_convergence` block holds the **X-gap** series (2.7563/2.2504/2.0722)
that was the historical source of the Δ_complete conflation remediated in P11D. Its
`metadata.inclusion_treatment` string still reads “TV18 resolved via Cartesian immersed
Gauss–Legendre quadrature with smooth indicator function” — P11B-era wording (see F-6). The file
is correctly declared preserved/historical by `results/raw/README.md` and is not cited as
authoritative anywhere in the active manuscript.

**F-5 (B-class, duplicates — documented so they are not confused in future audits).**
2.7563 = Δ_XM(4²) = Δ_X(4²) = quadrature baseline (S2 `gap_at_X`) — same value, three contexts.
2.5732 = Δ_path(4²) = Δ_complete(4²,21²) = sweep r₀/a=0.30 width. 2.2504 / 2.0722 appear as both
Δ_X and Δ_complete at 8²/16² **by coincidence** (band edges at X corners; agreement only to solver
noise, 5e-13 / 1e-11). All are legitimately distinct quantities; the manuscript (#11) states the
distinction explicitly.

**F-6 (B/C-class, leftover P11B/P11C strings).** (i) S2 metadata phrase “TV18 resolved … smooth
indicator function” and (ii) sec08 “TV18 is resolved via immersed Gauss quadrature” reuse the
pre-remediation framing; the frozen status is TV18 = LOCKED [S] “standard immersed Gauss-quadrature
indicator function on a regular mesh” (no exactness/“resolved” claim; and M14/TV18 documentation of
the **O(h)** cut-element integration error stands). Raw JSON is historical (F-4) and is not edited;
the sec08 wording is carried into Part C/I classification.

**F-7 (A-class).** No Δ_X/Δ_complete numeric confusion found in any active manuscript number:
Δ_X series (#11) traces to S4/path records; Δ_complete series (#9) traces to S3/S5/S6 cells.
No false “converged” language found (Part A4; guards assert the negative claims).

**F-8 (B-class, rounding).** Rounding is consistent per number (#1–#23); mixed decimal precision
(d₁ 4 dp vs d₂/d₃/d₄ 5 dp; legs 4 dp; series 4 dp) is cosmetic, all trailing digits round correctly
from raw values. “0.17814” is exact to the hard-coded literal F-3, not independently re-derived in
S6 — d₂ recomputes to 0.1781399883 from S3+canvas, which rounds to 0.17814 ✔.

**F-9 (A-class).** Variable naming in the manuscript is correct: “Δ_X” is only used where the raw
field is a X-point gap (`delta_X`/`delta_XM`); “Ω̄” path legs use Δ[Γ–X], Δ[X–M], Δ[M–Γ] matching
S2 `delta_GX/XM/MG`.

**F-10 (scope note).** Sweep values (#19/#20) are 4²-mesh-only — the manuscript says so explicitly
(“evaluated at the 4×4 mesh”) — and were not re-run at higher meshes by P11D/P12C (by design).
The “optimal maximum at 0.30” statement is correct over the five evaluated radii (0.20→0.40).
