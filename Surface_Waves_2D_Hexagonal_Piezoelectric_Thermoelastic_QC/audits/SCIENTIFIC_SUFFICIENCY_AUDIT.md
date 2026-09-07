# SCIENTIFIC_SUFFICIENCY_AUDIT.md

Carried from the accepted-task audit (renamed for this package; content unchanged):

# FINAL_ACCEPTANCE_AUDIT.md
## QC Surface-Wave Research Package — Final Acceptance Audit

Audit date: 2026-09-07 (Asia/Calcutta). Auditor: independent re-verification
performed entirely from the final ZIP in a fresh temporary directory
(`/tmp/qc_accept_nO9z`); the working repository was not used as the
verification environment. Every number below was recomputed this audit;
no prior log was trusted as evidence.

## 1. Executive Verdict

**GO.** The final ZIP is complete, clean, self-contained, and reproducible:
all six validations were re-executed from the clean extraction and pass
with the documented values; both prior audit findings (E1 branch-tracking
artifact, E2 resolution-count convention) are verified fixed; Study-1 data
regenerate cell-identical; all figures regenerate from the included raw
data; no stale, secret, or unrelated content was found.

## 2. Final ZIP Identity

- File: `QC_First_Paper_FINAL_REPRODUCIBLE_PACKAGE_2026-09-06.zip`
- Size: 1,114,047 bytes; mtime 2026-09-07 02:01:35 +0000 (post-fix rebuild)
- Only other ZIP present: `QC_First_Paper_INDEPENDENT_AUDIT_PACKAGE.zip`
  (34 MB) — the earlier Task-4 documentation-audit deliverable, a different
  artifact class, explicitly excluded from the final package by design.
  No pre-fix/post-fix ambiguity exists: a single research ZIP is present,
  and its contents are demonstrably post-fix (§7).
- `PACKAGE_MANIFEST.md` (repository level; it records the ZIP's own SHA and
  therefore lives beside, not inside, the ZIP) agrees with the actual ZIP:
  size, SHA-256, 70 files, contents table — all confirmed.

## 3. Exact SHA-256

`b817860569293e4dfec88419068d83b59976e3d875095e698cb13ae0c4244ec2`
(recomputed this audit; matches PACKAGE_MANIFEST.md). `unzip -t`: no errors.

## 4. Package Contents

70 files: README (1) · formulation (3: tex, 19-pp pdf, error ledger) ·
blueprint (2) · audit (3: IMPLEMENTATION_AUDIT, REPORT,
ARENA_POST_CLAUDE_FIX_AUDIT) · implementation (61: solver 10, tests 6,
drivers 5, figures 12 PDF + generator + manifest, results 16 + MANIFEST +
chain_log, logs 6, params.json, grids.json, requirements.txt, run_all.sh).
Solver-hash lineage recorded throughout: studies `7cfda8cdc7345f93`,
post-fix `8c0abbabe66776dd` (recomputed from the extracted tree:
`8c0abbabe66776dd`).

## 5. Clean Extraction Verification

Fresh temp dir; 70 files extracted (matches manifest). Stale-file scan
(__pycache__, .pytest_cache, *.pyc, *.tmp, *.ipynb, *~, *.bak, *.swp,
.DS_Store, *.aux, *.orig): **0 hits**. No duplicate figures; no pre-fix
CSVs (shipped `v3_model_limits.csv` carries the post-fix Ω=1000 value).

## 6. V0–V5 Results (executed from the clean extraction)

| Test | Exit | Result | Key numbers (this audit's logs) |
|---|---|---|---|
| V0 integrity | 0 | PASS | — |
| V1 two-path | 0 | PASS | 15/15 anchors ≤1e-8; worst |dV|/V ≈ 9.4e-10 (A, Ω=0.01) |
| V2 elastic limit | 0 | PASS | v_P/v0=1, v_S/v0=0.5 exact; V_R/v_S num 0.932525905921 vs analytic ...931; coupled anchors V*/v_S=0.62145378 (A), 0.93260276→0.93260246 (B,C) |
| V3 model limits | 0 | PASS | gates 1.110e-9 / 3.266e-9 (121/121); evidence max 3.107e-2; 71/121 ≤1e-6 (Ω≥0.3162); seed branch-verified 0.31072662 |
| V4 symbolic | 0 | PASS | p-degree 10 all; Ω-degree 10/8/10; det M(Ω=0)=410478057/25600000000000·(k²+p²)⁵ (sympy, all models) |
| V5 nondimensional | 0 | PASS | frozen table reproduced |

Zero warnings/errors in any fresh log. Determinism: the V3 CSV and both
Study-1 CSVs regenerated in the extraction are byte-identical to the
shipped copies.

## 7. E1 Branch-Tracking Verification (recomputed from shipped data)

1. Ω=1000 C(D_w*→1e-8) seed: V*=**0.31072662**, status `seed_verified`,
   deviation vs A = 7.595e-11 — on the intended A/phason branch.
2. Matches the reported 0.31072662.
3. Phonon value 0.467316 not selected; **no** C_Dw0 point lies within
   1e-3 of 0.4673 anywhere on the grid.
4. Branch identity explicitly enforced in the shipped test:
   `refine_branch_near` anchoring + `BRANCH_MATCH_REL=1e-2` acceptance +
   `seed_verified` assertion; the old `isfinite`-only check is absent
   (grep: 0 occurrences).
5. Continuity diagnostic active: `flag_discontinuities` present in the
   shipped `branch.py` and wired as a hard failure in the shipped test.
6. No comparable jump elsewhere: max adjacent |ΔV|/V on the C_Dw0 sweep =
   **5.422e-3** (matches reported ~5.4e-3); sub-crossover deviation is
   monotone as Ω decreases; 121/121 resolved.
7. Fig. 2b regenerated from the post-fix CSV; its data contain no spike
   (the curve it plots is the verified CSV).
8. Max adjacent jump: 5.422e-3 ✓.
9. Singular-limit max deviation: **3.1070e-2 at Ω=1e-3** ✓.
10. 1e-6 agreement: **71/121 for Ω≥0.3162** ✓.
11. Gates: **1.110e-9** and **3.266e-9** ✓ (unchanged by the fix).

## 8. E2 Resolution-Convention Verification

- Source: `study1_baseline.py` line 60 — `dBC = |V_B−V_C|/|V_C|` (relative,
  per the frozen blueprint).
- Shipped `fig4_deltas.csv` internally consistent with that definition
  (max discrepancy 2e-13, print precision).
- Recomputed counts: |V_B−V_C| < ε_Δ → **95/121**; Δ_BC < ε_Δ/V_C
  (pointwise relative equivalent, same inequality) → **95/121**;
  Δ_BC < 1.13e-8 treated as dimensionless → **91/121**.
- All "95/121" statements in README/REPORT/audit state the
  absolute-equivalent criterion explicitly; every "91/121" occurrence is
  explicitly labeled as the non-equivalent dimensionless reading
  ("would give 91/121", "alternative reading"). No statement implies the
  two are the same criterion.
- Fig. 4 plots the floor as ε_Δ/V ≈ 2.4e-8 — same convention.
- No data were altered to obtain 95/121: the count follows arithmetically
  from the shipped raw V columns (recomputed above), and Study-1
  regenerates identically (§9).

## 9. Study-1 Regression Check

- Study-1 re-executed from the clean extraction: `study1_baseline.csv`
  (21 value columns × 363 rows) and `fig4_deltas.csv` (7 × 121) are
  **cell-identical** to the shipped copies (only run metadata refreshed).
- Documented headline values confirmed at their stated frequencies:
  V_A=0.310727; V_B(Ω=1e-3)=0.46630123 (= V2 anchor 0.466301229975);
  V_C(Ω=1e2)=0.466263829; max Δ_BC=9.4829e-6 at Ω=1e3; max Δ_AC=0.3336.
- S3 (max Δ_T=7.8794e-5) and BC (max ΔV/V=8.0609e-6) shipped data match
  documented values. S2 npz: max Δ_BC=4.9976e-3, 2377/3721 above the
  per-point relative floor, V_B≥0.4650, V_C≥0.4663 — all as documented.
- Note: a byte-level diff against *pre-fix* files cannot be repeated this
  audit (no pre-fix copy persists; the git history has a single post-fix
  commit). Regression is instead established three ways: deterministic
  regeneration, documented-value agreement, and the fix's provable
  unreachability from production code paths (additive functions only,
  called solely by the V3 test). **No changed numerical cells found.**

## 10. Figure/Data Consistency

- 12 figure PDFs present, each 1 page, readable (pypdf); formulation PDF
  19 pp readable.
- All 12 figures regenerated from the included raw data inside the clean
  extraction (full `make_figures.py` run) — the figure pipeline is
  executable and current; fig2b's source is the post-fix v3 CSV.
- `FIGURES_MANIFEST.md` maps every figure to its exact CSV/NPZ and
  producing driver; all references exist. Fig. 7 manifest documents the
  honest exclusion of model A (no comparable branch under clamped
  phason). Fig. 9b documentation retains the cautious wording:
  "Ω_c appears … as a reference line only", "no claimed transition" —
  preserved, not reinterpreted.

## 11. Mathematical Consistency (direct inspection of shipped code)

- Frozen constant relations in `params.json`/Material: C66=(C11−C12)/2 ✓,
  K6=K1−K2−K3 ✓, R6=(R1−R2)/2 ✓.
- Pencil coefficients extracted numerically from `M_matrix` (3-point
  sampling in p): A1(3,4)=A1(4,3)=−(K2+K6)k=−0.255 for all three models ✓;
  det(A2)>0 with det(A2)=(C11K1−R1²)(C66K3−R6²)k11·k⁴ exactly (ratio
  1.000000) ✓.
- V4 (sympy, shipped log + re-executed): p-degree 10 all models;
  Ω-degree 10 (A), 8 (B), 10 (C); det M(Ω=0) =
  410478057/25600000000000·(k²+p²)⁵ for all models ✓. (A purely numeric
  probe of the ω=0 determinant constant differs at ~8e-7 relative because
  the numerical M carries the thermal-row normalization; the sympy check
  is the authoritative frozen identity and is exact.)
- Formulation unchanged; this was a consistency audit only.

## 12. Boundary and Nondimensionalization Consistency

Verified verbatim in shipped code: half-space z>0 with n=−e_z and
t_z=−σ_zz=P0 (`boundary.py` docstring/rows); rows σ_zz=0 (free), σ_xz,
H_xz/H_zz or clamped w_x=w_z=0; thermal isothermal θ=0 or insulated
∂θ/∂z=0; admissibility Im p>0 with near-real roots excluded and flagged
(`roots.py`); nondimensionalisation v0=√(C11/ρ), ω0=v0·k0,
U0=β1T0/(C11k0), stresses /C11 (`material.py`); V5 reproduces the frozen
table. No accidental changes.

## 13. Reproducibility Assessment

A fresh researcher with only this ZIP can reproduce everything: README
documents every command (run_all.sh + per-component); requirements.txt
pins numpy/scipy/sympy/matplotlib at the versions used; imports in the
tree are exactly stdlib + those four + the local `solver` package (no
undocumented dependency); no absolute paths in any script/module/doc
(the only `/home/user` mentions are inside `results/chain_log.txt`, a
verbatim provenance record, documented as such). Verified by execution:
V0–V5, Study 1, V3, and the complete figure regeneration all ran from the
clean extraction with no access to the working repository. Not re-executed
in this audit (documented scoping, not a defect): Study 2 (~2 h),
Study 3, BC study, roots driver — their drivers ran in the final chain,
their shipped data match all documented values, and their figures were
regenerated from that data during this audit.

## 14. Packaging/Cleanliness Assessment

Secrets/credentials/API-key patterns: 0 hits. VCS metadata: none.
Unrelated project material: none. Caches/temp/editor/notebook files: none.
Stale pre-fix artifacts: none (v3 CSV and fig2b are post-fix; all other
data provingly unchanged). Duplicate figures: none.

## 15. Remaining Risks/Caveats (non-blocking, all documented in-package)

1. The resolution benchmark carries its own older solver hash
   (`ae77e8a76333617a`, run `20260906-resolution`) — documented in README
   §6 and the MANIFEST; the fix it predates affected branch selection
   only, and ε_Δ's definition (refinement-based u_V) is unaffected.
2. The 95-vs-91 count duality is retained deliberately (both readings
   recorded in ARENA §7–8); the manuscript should quote the
   absolute-equivalent convention (95/121) with the floor stated as
   ε_Δ/V* ≈ 2.42e-8.
3. `PACKAGE_MANIFEST.md` lives beside the ZIP (it records the ZIP's own
   SHA-256 and cannot live inside it).
4. Study 2/3/BC/roots drivers were not re-executed in this audit
   (scoping; see §13) — their outputs are shipped, hash-identified, and
   value-verified against the documentation.

## 16. Final GO/NO-GO for Manuscript Drafting

**GO.** No blocking reproducibility, scientific-consistency,
stale-artifact, or packaging defect remains.

The final QC package is accepted as the reproducibility baseline for
manuscript drafting.
