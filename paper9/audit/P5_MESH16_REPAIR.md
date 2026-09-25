# P5 n = 16 production repair — record

**Scope:** replace the contaminated N = 1 production discretisation of the P5 production pass with a
defensible n = 16 production discretisation, and reduce every printed number to a precision that
survives the mesh comparison. Authorised by the PI on 2026-09-24 (P5-A + R-1-A decision package,
`paper9/audit/PI_DECISION_PACKAGE_P5_R1.md`); the earlier P5 `PASS` was a production-*completeness*
decision, not a numerical-correctness claim, which is precisely the gap this repair closes. R-1 stays
`CLOSED`, C-1 is not reopened, B1/B2/B3 statuses are untouched, and no submission is authorised by
this record.

**Historical record (append-only, never rewritten):** the N = 1 production artefacts remain
byte-identical and are still the evidence for every earlier audit phase:

| artefact | sha256 (unchanged) |
|---|---|
| `results/raw/p5_production_raw.json` | `0af7445a4c5e502942b451ed8f214d7191ebfe23cb97b3d65b6a0d39f81eb3d0` |
| `results/processed/table5_gap_summary.json` | `f0e1c2001fab8c8dcfc278717daaba390da8694cc144af12f06cff378d31f784` |
| `results/raw/p12b_s7_theta_sweep.json` | `9d645ce98bc2c1b6776b40bbcf602a11953ec059e2e6ca2b1503047bcbce84d1` |

## 1. What was run

The frozen Part-A formulation, unchanged except for the element count per unit cell:

* 16 x 16 BFS elements per unit cell, `h = 0.0625`, **2048** dof per cell, frozen n-order assembly.
* Same 42-point `(theta, AR)` matrix: `theta in {0, 15, 30, 45, 60, 75, 90} deg`,
  `AR in {1, 2, 3, 5, 7, 10}`.
* `N_seg = 40`, `N_kx = 41`, `N_ky = 81`, `N_bands = 4`, `tol_herm = 1e-12`, `eps_Delta = 4.63e-11`,
  same materials (`L = lam = mu = rho = 1`), `ell2 = 0.04`, `l_iso = 0.20`, same k-path and grid.
* Deterministic eigensolve only: shift-invert ARPACK (tol 1e-11, `ncv = 16`, `k = 8`,
  `sigma = 1e-3`) from a fixed analytic start basis. No stochastic `which="SM"` start, no correction
  factor, no rescaling, no warm starts.

**Execution result (n = 16, the production mesh).** 42/42 cases, **145 659 solves**, compute wall
**5266.2 s** (2 workers; summed per-case time 26 962 s), worst backward error **5.53e-13**, dense
fallbacks **0**.

**Comparison leg (n = 8).** The same driver, assembly and post-processing at 8 x 8 elements per cell
(512 dof): 42/42 cases, 145 659 solves, **2081.7 s**, worst backward error **2.60e-13**, 0 fallbacks.
It exists solely to bound the mesh sensitivity of every printed quantity; nothing in the manuscript
is taken from it.

**Reproducibility record.** Each result JSON carries `git_commit`, `param_hash`, `environment`
(python 3.13.14, numpy 2.3.5, Linux x86_64), `utc`, `timing_seconds`, `n_solves_total`,
`worst_backward_error`, `n_dense_fallbacks` and a `provenance` block naming the artefact it
supersedes. Run logs: `audit/evidence/p5_mesh16/run_log_mesh16.txt`,
`audit/evidence/p5_mesh8/run_log_mesh8.txt`; stage log `audit/evidence/p5_mesh16/pipeline.log`.

## 2. Superseding artefact sets (authoritative = n = 16; n = 8 = comparison only)

| n = 16 artefact | sha256 |
|---|---|
| `results/raw/p5_production_raw_mesh16.json` | `2a8267b4f3f9bfc209597c54e53c26afc261e220669ccdbbad4b194038376e69` |
| `results/raw/p5_production_mesh16_grid.npz` | `91963453f8c8a7472325154719b3339aa483317b705b3d4a64b2367a509ff81c` |
| `results/processed/table5_gap_summary_mesh16.json` | `d3d633c337a37b3443930d99ce9217e1f5734064201611da2c2823688894f9e4` |
| `results/processed/p5_production_highlights_mesh16.json` | `c3ae8f3e79728cceeb4c905d2e4f0ace2077219758a9b1ddb5c70d6668a5ce47` |
| `results/raw/p12b_s7_theta_sweep_mesh16.json` | `75428b7ca8271818dab2e69ef03db8f2245c2e8585be0e3fbc32edd6e470867e` |

| n = 8 comparison artefact | sha256 |
|---|---|
| `results/raw/p5_production_raw_mesh8.json` | `d69cd6b6d0ea75b1a0d5c39ca231e9a13d260a2ac7a71bf6b96479772092a9e9` |
| `results/raw/p5_production_mesh8_grid.npz` | `33069aada0ddbdba0c5925cde3171a6801e9970b9e8fd29a34002c889f0bc0d5` |
| `results/processed/table5_gap_summary_mesh8.json` | `dfd0150ef794574379df94dce2a143655e1e18a036b1b00bb2b2e3b465b19dc2` |
| `results/processed/p5_production_highlights_mesh8.json` | `5cf5702d8d3e31d9577fc852e39bf60caf8ec923a398ccec787cdc4cbf2e00d9` |
| `results/raw/p12b_s7_theta_sweep_mesh8.json` | `6e737cf6a10c0e7fe8409524f06b570b2ef1299ce1ed655733e19d3d08b2eba4` |

`verification/suite/test_p5_mesh16_repair.py` pins both tables, pins the N = 1 table above as
untouched, and checks the manuscript literals against the n = 16 JSON.

## 3. Gap classification (Table 5) — recomputed at both meshes

126 rows at every mesh; classes were recomputed from data, never carried over.

* N = 1: 70 `none` / 56 `directional`; **n = 16: 84 `none` / 42 `directional`**;
  **n = 8: 84 `none` / 42 `directional`**.
* **N = 1 -> n = 16: 14 rows change**, every one of them the `(3, 4)` pair,
  `directional -> none`: `(AR, theta)` = (2, 75), (2, 90), (3, 60), (3, 75), (3, 90), (5, 60),
  (5, 75), (5, 90), (7, 60), (7, 75), (7, 90), (10, 30), (10, 75), (10, 90).
* **n = 8 -> n = 16: 0 rows change** (`mesh_comparison.json` summary
  `classification_changes = 0` of 126). The classification is therefore converged between the two
  finer meshes, and the 14-row movement is a coarse (N = 1) artefact.
* Sign changes N = 1 -> n = 16: `delta_GX` 14, `delta_XM` 2, `delta_MG` 5, `delta_complete` 0.
* No row becomes a complete gap at any mesh: the design-map maximum of `delta_complete` is
  **-0.3234978** (n = 8: -0.3235097; N = 1: -0.3758), so `Delta_complete <= -0.3235` stands.

## 4. Printed-precision reduction (the mesh-stability rule)

Mesh-to-mesh movement of each printed quantity (n = 8 vs n = 16):

| quantity | movement | printed precision adopted |
|---|---|---|
| Table 5 `delta_GX` | 28/126 cells move at 4 dp; 16 at 3 dp; 0 at 2 dp | 3 dp (the 12 printed rows are unchanged; 2 dp would print the +0.0043 directional gap as `+0.00`) |
| Table 5 `delta_path`, `delta_complete`, `norm_gap_width` | 47/55/27 cells at 4 dp; 21/21/6 at 3 dp; 2/2/2 at 2 dp | 2 dp |
| Table 5 `S_theta` footer | AR = 3, 5, 7, 10 move at 3 dp (e.g. 2.3423 -> 2.3372) | 2 dp |
| `delta_max` (Figures 6/8/14, Table 7, text) | all 14 sweep rows identical at 4 dp | unchanged (4 dp in Table 7, 2 dp in text) |
| `delta_max` theta-invariance span | 7.55e-6 deg (n = 8) vs 3.96e-7 (n = 16) | text bound **1e-5 deg** (was 5e-7), relative variation **5e-4 %** (was 3e-5 %) |
| `delta_max(theta) = delta_max(90 - theta)` | 2.25e-8 vs 8.03e-8 deg | text bound **1e-7 deg** (was 8e-8, which the n = 16 measurement itself violated) |
| `M_s` on the locked 5 deg grid | 0 deg / 10 deg at both meshes | unchanged |
| parabolic-refined `M_s` | not resolved: -0.00 vs -2.67 deg at AR = 5 | reduced to a qualitative statement in Table 7 (no refined digit printed) |
| `phi*` at (AR = 10, theta = 45 deg) | exact four-fold tie of the ring sampling: 85 deg (n = 8) vs 5 deg (n = 16) | grid-tie, stated as such; the tabulated value is the n = 16 one |

Table 5 carries a footnote naming the precision basis and the worst-case mesh-to-mesh changes
(5.5e-3 `delta_GX`, 5.8e-3 `delta_path`, 5.7e-3 `delta_complete`); full-precision values stay in the
n = 16 result set. `S_theta` is quoted as 2.34 rad^-1 in the abstract, Section 6 and Section 9.

Two bound corrections came out of the guards rather than the prose: Section 7's theta -> 90 - theta
bound (8e-8 -> 1e-7) and the anchor-comparison tier (see 5). No other language was touched and no new
claim was introduced; the only factual caption correction is Figure 10's "monotonic gap opening with
increasing aspect ratio", which the regenerated data contradicts (the maximum sits at AR = 7).

## 5. Steering sweep (S7) at both meshes

`production/p12b_s7_theta_sweep_mesh16.py` gained optional `--n-elem / --registry / --out` arguments
(defaults unchanged, so the n = 16 invocation is bit-identical in definition); the n = 8 leg is the
same measurement on the coarser mesh. Cross-mesh result: all 14 `delta_max` rows identical at 4 dp,
`M_s` = 0 deg (AR = 5) and 10 deg (AR = 10) at both meshes, symmetry residuals within 1.3e-6 deg at
both meshes.

Anchor check against the matching P5 production `study_S7_ifc_steering` row: the two runs share the
formulation but not the eigensolver iteration path, so the comparison is tiered — at n = 16,
(AR = 10, theta = 45) reproduces to 7.0e-10 relative and (AR = 5, theta = 45) to 8.6e-8; at n = 8 both
reproduce to 5.5e-9 and 4.4e-9. `test_p5_mesh16_repair.py` holds every case to 1e-6 and the
strictest tier to 1e-9 where it holds.

## 6. Figures, tables and manuscript text re-emitted

Re-emitted from the n = 16 authoritative data: Figures 6, 8, 9, 10, 11, 12, 14 and Tables 2, 5, 7.
Every other figure is byte-identical to `HEAD` in content (differences in embedded creation dates
were normalised away, and the files were restored from `HEAD`); Table 6 and Figures 1-5, 7, 13 are
similarly untouched. Manuscript files edited: `ms.tex` (abstract) and `sections/sec01`, `sec04`,
`sec05`, `sec06`, `sec07`, `sec08`, `sec09` — production-dependent numbers plus the element-order
statement (Section 4) and the Section 5 epsilon-Delta sentence re-anchored on the measured margin
(smallest quoted gap 4.3e-3 = 9e7 eps_Delta, seven orders; smallest positive design-map gap 1.32e-3,
7.5 orders).

## 7. Guard pins superseded by this repair (historical values retained)

| guard | constant | value chain |
|---|---|---|
| `test_p12ad`, `test_p12ae`, `test_p12x`, `test_p12y` | `MANUSCRIPT_TEX_SET_SHA256` | `243bb4d3...` (P12AG) -> `4843ef7e...` (n = 16 repair) -> **`8b45db33...`** (precision reduction) |
| `test_p12af_manuscript_retiering.py` | `MANUSCRIPT_TEX_SET_SHA256_P5REPAIR` | `4843ef7e...` -> **`8b45db33...`** |
| `test_p12ac_decision_b.py` | `AUTHORISED_MANUSCRIPT_FILES` | union of the P12AF set and the seven paths this repair edits |
| `test_p12ag_clean_build.py` | `NUMERIC_TOKEN_SHA256[tab02]` | `545cf787...` -> `af741826...` (unchanged by the precision step) |
| `test_p12ag_clean_build.py` | `NUMERIC_TOKEN_SHA256[tab05]` | `75bb31b6...` -> `8edafe0d...` -> **`e481f264dca7dfa5...`** |
| `test_p12ag_clean_build.py` | `PINNED_VALUES[tab05]` | `1.155/1.343/1.542/3.946` -> `+0.0406/-0.3235/1.415/1.757/1.863/1.398/2.337` -> **`+0.044/-0.32/1.40/1.42/1.76/1.86/2.34`** |
| `test_p12ag_clean_build.py` | `P12AF_CONTENT[SEC05]` | `bfd45dd0...` kept as history; current content pinned separately |
| `test_p12ah_generator_and_layout.py` | `AUTHORISED_REPAIR` | tab02 pinned; tab05 content + raw and tab07 content re-pinned after the precision step; tab06 unchanged |
| `test_p12b_steering_fom.py` | manuscript/table integration | reads `p12b_s7_theta_sweep_mesh16.json`; `M_s` 0 deg / 10 deg; symmetry bound 1.3e-6 |
| `test_p8_remediation.py` | FIND-01 / FIND-02 | `0.0431 -> 0.0043`, `0.0896 -> 0.0677` |
| `test_p5_mesh16_production.py` | manuscript literals | `S_theta` checked at its printed 2 dp |
| `test_p5_mesh16_repair.py` | new, this repair | both artefact sets pinned; Table-5 reclassification (N = 1 -> n = 16) = the 14 named rows; `classification_changes` (n = 8 -> n = 16) = 0; S7 comparison legs; printed-precision checks for Table 5, `S_theta` and both steering bounds |

## 8. Verification

`verification/suite/verify_p5_mesh16.py` (pipeline stage 5) writes
`audit/evidence/p5_mesh16/verification_mesh16.{json,txt}` (phases A-D: assembly equivalence against
the frozen reference at both meshes, mode-resolved dense-subset agreement along path and grid, extrema
verification, classification-critical rows) and `mesh_comparison.{json,txt}` (phase E, n = 8 vs n = 16
for every claim-bearing quantity). The Table-5 classification guard asserts the phase-E
`classification_changes` count is exactly 0.

**Stage-5 run completed (2026-09-25).** All 42 n = 16 cases were cross-checked against the
independent dense reference; every case is recorded individually in
`audit/evidence/p5_mesh16/verification_mesh16_cases.jsonl` (interrupted once by a sandbox teardown,
resumed from the cache without recomputing completed cases). Headline result: assembly equivalence
1.137e-13 (n = 16) / 2.842e-14 (n = 8); design-map grid agreement max 2.76e-12 (median 9.4e-13);
672 extrema verified with max |production - dense| 1.39e-12; 18 classification-critical rows;
0 unmatched modes in every case; 2387 dense reference solves. The largest path deviation over the
lowest four bands, 2.13e-06 (median 5.8e-07), occurs in every instance at the Gamma point in the
near-zero acoustic modes (omega ~ 0 - 3e-06), which are outside the accuracy claims; the
claim-bearing bands agree to ~5e-13. Mesh comparison: 0 of 126 gap-classification rows change
between n = 8 and n = 16. Wall time 5229.9 s.

**Known inherited layout warning:** the manuscript build has always emitted one
"Float too large for page" warning for the master-parameter table float (1197 pt at `HEAD`; 1254 pt
after the required element-order row was added). It is a warning, not an error: the build reports
0 LaTeX errors, 0 undefined references and 0 missing files, and the table renders in full.

## 9. Final closure: two unsupported Section 6 statements removed (2026-09-25)

The n = 16 repair commit `f4711ac` recorded in its message that Figure 10 "no longer claims
monotonic gap opening with aspect ratio", but the diff shows the caption was re-pointed only for its
numbers and the clause was left in place. Re-inspection against the authoritative n = 16 result set
(`results/raw/p5_production_raw_mesh16.json`, `study_S5_design_map`) found two statements in
`latex/sections/sec06_results.tex` that the production data contradicts. Both are corrected here; no
other file, number, figure, table, gate, status or decision is touched.

| # | Statement as committed | Evidence from the n = 16 production set | Correction |
|---|---|---|---|
| 1 | Figure 10 caption: "Three-dimensional response surface showing monotonic gap opening with increasing aspect ratio" | `Delta_GX` (bands 2--3) is non-monotonic in `AR` at every `theta`; e.g. `theta = 0 deg`: `+0.0406, +0.0281, +0.0445, +0.0013, +0.0677, -0.0018` for `AR = 1, 2, 3, 5, 7, 10`. The same caption states the maximum is at `AR = 7`, so it was internally contradictory | "(a) Three-dimensional response surface of $\Delta_{GX}$; the dependence on $\mathrm{AR}$ is not monotone." |
| 2 | Section 6 (aspect-ratio sweep): "At `AR = 1`, the microstructure is isotropic and no directional gap opens along `Gamma`--`X`" | `Delta_GX = +0.040568` at `AR = 1` for all seven `theta` (identical, as isotropy requires); it is positive at every mesh (`N = 1`: `+0.0447`; `n = 8`: `+0.0406`). Table 6 of the manuscript therefore lists the `AR = 1` rows as `+0.041`, class *Directional* | "At `AR = 1` the microstructure is isotropic, yet a directional stop band along `Gamma`--`X` is already present and orientation-independent (`Delta_GX = +0.041` at every `theta`)." |

The trailing clause of the same Section 6 sentence ("progressively driving the divergence between the
upper and lower acoustic branches at the zone boundary") is removed with it: at the `theta = 45 deg`
sweep the two acoustic branches stay degenerate at `X` for every `AR` (`study_S4`), and the
lower-to-upper doublet separation at `X` *decreases* with `AR` (`1.7454` at `AR = 1` to `1.5773` at
`AR = 10`), so it is not a progressive divergence.

**What is not changed.** The Section 5 margin sentence is left as written: "All computed band gaps and
frequency shifts quoted in the text of subsequent sections exceed `eps_Delta` by at least seven orders
of magnitude (the smallest, `|Delta_GX| = 4.3e-3`, is `9e7 eps_Delta`)". This is true as stated
(`4.3e-3 / 4.63e-11 = 9.3e7`, i.e. 7.97 orders) and `4.3e-3` is the smallest `Delta_GX` quoted in prose.
The smallest *tabulated* value, `+0.001` at (`AR = 5`, `theta = 0 deg`) i.e. `1.3238e-3`, is
`2.86e7 eps_Delta` = 7.46 orders, so the general seven-order claim also holds for it.

**Verification after the correction.**

| Check | Result |
|---|---|
| Build `cd paper9/latex && pdflatex -> bibtex -> pdflatex x2` | 0 LaTeX errors, 0 undefined citations/references, 0 missing files, no rerun request, 14/14 figures and 7/7 tables present, 34 pages |
| Full suite `paper9/verification/suite` | **395 passed, 4 skipped, 0 failed** (the 4 skips are the three pre-existing P12AH numeric-content skips and the opt-in P4B-B1 full rerun) |
| `test_p12ag_clean_build.py` | 11 passed, including a real `pdflatex -> bibtex -> pdflatex x2` build in a scratch tree with zero errors |
| `test_statuses_and_gates_are_unchanged` | B1 `GRAPHICAL_VALIDATION`/PASS, B2/B3 `NOT_VALIDATED`, PCR1 `NOT PASS`, G3/G4 `NOT MET`, P5 `PASS`, R-1 `CLOSED` |

**Guard pins superseded by this correction (historical values retained):**

| guard | constant | value chain |
|---|---|---|
| `test_p12ad`, `test_p12ae`, `test_p12x`, `test_p12y` | `MANUSCRIPT_TEX_SET_SHA256` | `243bb4d3...` (P12AG) -> `4843ef7e...` (n = 16 repair) -> `8b45db33...` (precision reduction) -> **`bac1425c...`** (Section 6 correction) |
| `test_p12af_manuscript_retiering.py` | `MANUSCRIPT_TEX_SET_SHA256_P5REPAIR` | `4843ef7e...` -> `8b45db33...` -> **`bac1425c...`** |

## 10. Final closure: Table 5 caption corrected to the tabulated aspect-ratio subset (2026-09-25)

`latex/sections/sec06_results.tex` carried the Table 5 caption "across aspect ratios
$\mathrm{AR} \in \{1, 2, 5, 10\}$", but the regenerated table tabulates $\mathrm{AR} \in \{1, 3, 5, 10\}$.
The mismatch predates the n = 16 repair and is not a repair artefact: the caption was written in the
original draft commit `bd0fcfb`, while the generator `tables/gen/tab05_gap_summary.py` has selected
`selected_ar = [1.0, 3.0, 5.0, 10.0]` since it was first written in `98d9ac0`. The caption has
therefore never described the table it introduces.

The generated table is the authoritative artefact: its content is recomputed from
`results/processed/table5_gap_summary_mesh16.json` and is pinned by `test_p12ah_generator_and_layout.py`
and `test_p12ag_clean_build.py`. The caption is prose describing it, so the caption is the element
corrected. No number, figure, table, gate, status or decision is changed; the twelve tabulated rows,
the $S_\theta$ footer and the printed-precision footnote are untouched.

**Verification after the correction.**

| Check | Result |
|---|---|
| Build `cd paper9/latex && pdflatex -> bibtex -> pdflatex x2` | 0 LaTeX errors, 0 undefined citations/references, 0 missing files, no rerun request, 14/14 figures and 7/7 tables present, 34 pages |
| Full suite `paper9/verification/suite` | **395 passed, 4 skipped, 0 failed** (the 4 skips are the three pre-existing P12AH numeric-content skips and the opt-in P4B-B1 full rerun) |
| `test_statuses_and_gates_are_unchanged` | B1 `GRAPHICAL_VALIDATION`/PASS, B2/B3 `NOT_VALIDATED`, PCR1 `NOT PASS`, G3/G4 `NOT MET`, P5 `PASS`, R-1 `CLOSED` |

**Guard pins superseded by this correction (historical values retained):**

| guard | constant | value chain |
|---|---|---|
| `test_p12ad`, `test_p12ae`, `test_p12x`, `test_p12y` | `MANUSCRIPT_TEX_SET_SHA256` | `243bb4d3...` (P12AG) -> `4843ef7e...` (n = 16 repair) -> `8b45db33...` (precision reduction) -> `bac1425c...` (Section 6 correction) -> **`a1a450aa...`** (Table 5 caption correction) |
| `test_p12af_manuscript_retiering.py` | `MANUSCRIPT_TEX_SET_SHA256_P5REPAIR` | `4843ef7e...` -> `8b45db33...` -> `bac1425c...` -> **`a1a450aa...`** |

**Precision note recorded, not changed.** The abstract, Section 6, Section 8 and Section 9 quote the
no-complete-gap margin as $\Delta_{\mathrm{complete}} \le -0.3235$. The design-map maximum in the
authoritative n = 16 set is $-0.3234978237$, which rounds to $-0.3235$ at the four decimals quoted but
is strictly greater than $-0.3235$ by $2.2\times10^{-6}$. This is correct rounding of the quoted value
rather than an error, and it is far inside the mesh-to-mesh movement of this quantity
($5.7\times10^{-3}$ between $n = 8$ and $n = 16$, recorded in the Table 5 footnote), so no scientific
conclusion depends on it. It is recorded here for traceability; no manuscript number is changed.
