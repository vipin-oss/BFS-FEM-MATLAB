# P12C Post-Closeout Forensic Audit — Part A: Scientific Evidence

**Scope:** independent, read-only re-audit of the P12C Case-C complete-gap evidence at
`phase-1-symbolic = 0d9850290b63a5da81b098d999714ab621684c77`.
**Date:** 2026-09-24 · **Method:** evidence files re-read from disk and re-derived (no new
production calculations, no file modifications).

---

## A1 — Five-mesh complete-gap series (21×21 zone grid)

Values re-read from `p11d_caseC_gap_convergence.json` (4²/8²/16²) and the two P12C JSONs (32²/64²):

| FE mesh | dofs 8(N+1)² | Δ_complete (recorded) | task-spec value | match (≤5e-11) |
|---|---|---|---|---|
| 4×4 | 200 | 2.5731869148388 | 2.5731869148 | ✔ |
| 8×8 | 648 | 2.2503884154045 | 2.2503884154 | ✔ |
| 16×16 | 2312 | 2.0722484270604 | 2.0722484271 | ✔ |
| 32×32 | 8712 | 1.9736363149301 | 1.9736363149 | ✔ |
| 64×64 | 33800 | 1.9178891171692 | 1.9178891172 | ✔ |

All five values reproduce the task specification to the stated digits. Series is strictly
monotonically decreasing.

## A2 — Decrements and ratios (recomputed from A1, never re-typed)

| quantity | recomputed | JSON-recorded | task-spec |
|---|---|---|---|
| d₁ = Δc₄−Δc₈ | 0.3227984994 | — | — |
| d₂ = Δc₈−Δc₁₆ | 0.1781399883 | 0.178140 (`d2_16vs8`) | — |
| d₃ = Δc₁₆−Δc₃₂ | **0.0986121121** | 0.09861211213033805 (`d3_32vs16`) | 0.098612… ✔ |
| d₄ = Δc₃₂−Δc₆₄ | **0.0557471978** | 0.05574719776087367 (`d4_64vs32`) | 0.054359… **✘ MISMATCH** |
| r_trigger = d₃/d₂ | **0.5535652777739** | 0.5535652777739338 | ≈ 0.553565 ✔ |
| r₄ = d₄/d₃ | **0.5653179569584** | 0.5653179569583828 (`d4_over_d3`) | ≈ 0.565318 ✔ |

**FINDING A-F1 (task-spec erratum, no repository impact).** The task prompt lists
`d4 = 0.054359…`; the evidence and the JSON both give **d₄ = 0.0557471978**. The prompt's
`r₄ ≈ 0.565318` is inconsistent with its own d₄ (0.054359/0.098612 = 0.5512), confirming the
prompt value is a transcription slip. The repository is correct everywhere: the JSON
`post_64_report.successive_decrements.d4_64vs32` = 0.0557471978 and `sec06_results.tex` states
`d_4 = 0.05575`. **No corrective action required** — recorded so the discrepancy is not silently
repeated.

## A3 — Non-convergence confirmation

- Successive-decrement ratios: 0.552, 0.554, 0.565 — **no ratio approaches ≪0.5**; the
  pre-registered trigger (≥0.5) fired at both decision points (32², then 64²).
- d₄ is still 17.3 % of d₁ and 31 % of d₂: the successive differences are not decaying
  geometrically toward zero at an accelerating rate.
- Verdict: **Case-C complete gap is NOT mesh-converged at the computed resolutions.** Confirmed.

## A4 — No converged width claimed

- `p12c_caseC_32_gap_convergence.json` and `…_64_…json`: unnegated use of “mesh-converged”
  = **0 occurrences** in both.
- `sec06_results.tex`: contains “**not mesh-converged**” (verbatim) and “**no mesh-converged
  complete-gap width is claimed**”; the 2.5732 value is explicitly labelled the 4×4-mesh result.
  Guard test `test_no_false_converged_claim_and_manuscript_honesty`
  (`test_p12c_caseC_32.py:145-155`) asserts all three of these strings; the 64² guard asserts
  the JSON-side absence (`test_p12c_caseC_64.py:114-121`).
- `sec08_discussion.tex`: “not mesh-converged at the resolutions computed to date …
  rather than a converged continuum value.”
- `sec09_conclusions.tex`: series extended to 64×64 with “not mesh-converged” and the 4×4
  attribution of 2.5732.
Confirmed with no exceptions.

## A5 — Raw JSON + SHA-256 sidecar integrity

| file | sha256 (recomputed) | sidecar | match |
|---|---|---|---|
| `p12c_caseC_32_gap_convergence.json` | `5547bae453964946c840…` | `…json.sha256` | ✔ |
| `p12c_caseC_64_gap_convergence.json` | `c8910c0de2188b49cc75…` | `…json.sha256` | ✔ |

Both sidecars are byte-exact matches of the current files.

## A6 — Production scripts ↔ recorded results

- Both scripts are present at HEAD: `production/p12c_caseC_gap_convergence.py` (32², staged),
  `production/p12c_caseC_gap_convergence_64.py` (64²), plus `p12c_64_feasibility_probe.py`.
- Recorded run metadata (`metadata`): `git_sha_at_run_start` = `1154315…` (correct: the scripts
  ran before the P12C commit); `parameter_hash_sha256` = `bb112a522e094b2b…`; top-level
  `environment` block: Python 3.13.14 / NumPy 2.3.5 / SciPy 1.17.1 (Linux-6.1.158). Guard tests
  assert these fields exist (`test_p12c_caseC_32.py:34-37,55`) and that the dense→sparse engine
  deviation is disclosed (`assert "OOM" in engine_disclosure`, `"sparse" in …`, lines 38-39).
- Script constants match the recorded engine: `EIGSH_SIGMA = −0.25`, `EIGSH_SIGMA_ALT = −0.5`,
  `EIGSH_TOL = 1e-12`, `N_SEG_PATH = 20`, `LU_PERM_SPEC = "COLAMD"`, and in the 64² script
  `PERM64 = "MMD_ATA"`; the recorded JSONs name those same settings in their disclosures.
- Cell identities, dof counts (8712 / 33800) and wall times in the JSONs correspond to the
  script’s outputs (11²/21² cells and the Γ–X–M–Γ path of 20 segments per leg).
- **FINDING A-F2 (minor, inert):** `p12c_caseC_gap_convergence_64.py` hard-codes
  `d2 = 0.178140` in `finalize`. It is used only for the reported context field
  `successive_decrements.d2_16vs8`; the reported r₄ uses the **measured** d₃ = Δc₁₆−Δc₃₂.
  No scientific effect; flagged for a future revision to read d₂ from the registry. The 32²
  script contains only a rounded `0.0986` inside a descriptive `gate_note` string.
  Per the standing rule the scripts were **not modified**.

## A7 — P11D 4²/8²/16² evidence not overwritten

- `git diff 1154315 HEAD -- results/raw/p11d_caseC_gap_convergence.json` → **empty**.
- Last commit touching it: `6b4ca8b` (P11D-C2). Content sha256:
  `1d4476f12d0b8ae9096e870436fbe0cd004dcd15e5edbb3663d827e8bedaf6ff`.
- P11D still holds 4²/8²/16² at 11², 21² and 41² grids (9 cells) plus `per_mesh_gaps` and
  `p11d_deltaX_check.json`. Unmodified. ✔

## A8 — Brillouin-zone resolution

| FE | 11×11 | 21×21 | |Δ| |
|---|---|---|---|
| 32×32 | 1.973636314301 | 1.973636314930 | 6.3e-10 |
| 64×64 | 1.917889115331 | 1.917889117169 | 1.8e-9 |

- Both meshes: grid-to-grid change ≤ 2e-9 (identical to ≥9 decimals; the manuscript’s
  “identical to 6 decimals” is true and conservative).
- Preserved 41×41 evidence (P11D, available meshes only): 4² → 2.5728033505, 8² → 2.2503884154,
  16² → 2.0722484271; the 21²→41² shift at 4² is 3.8e-4, matching the manuscript’s
  “~4×10⁻⁴” BZ-sampling accuracy statement.
- 41×41 was **not** required or run at 32²/64² (mandated grids were 11² and 21²); the
  ≤5e-4 BZ-error claim therefore rests on the P11D evidence and the 11²↔21² agreement above.
  Recorded, not overstated.

## A9 — Δ_X vs Δ_complete separation

| FE | Δ_X (X-point) | Δ_complete | difference |
|---|---|---|---|
| 4×4 | 2.7563016535473004 | 2.5731869148388 | **0.1831 (material)** |
| 8×8 | 2.25038841540496 | 2.2503884154045 | 5e-13 (solver noise) |
| 16×16 | 2.07224842705028 | 2.0722484270604 | 1e-11 (solver noise) |
| 32×32 | 1.9736363157 | 1.9736363149 | 8e-10 (solver noise) |
| 64×64 | 1.9178891171 | 1.9178891172 | 1e-9 (solver noise) |

- At 4×4 they differ materially (the ω̄₄ minimum sits off-X on Γ–M).
- At ≥8² they coincide **only to solver noise**, because both band edges sit at X corners.
- The manuscript states this distinction explicitly (“Δ_X and Δ_complete remain distinct
  quantities despite this coincidence”) and never equates them. **No manuscript statement
  equates the two.** ✔

## A10 — Extrema locations

- 32×32 (both grids): max ω̄₃ = 4.202670 at (0, π); min ω̄₄ = 6.176307 at (π, 0).
- 64×64 (11×11): max ω̄₃ = 4.1593048216 at (π, 0); min ω̄₄ = 6.0771939388 at (0, π)
  (21×21: same values, both at (π, 0)).
- All extrema are recorded per cell (`omega3_max_at_k`, `omega4_min_at_k` — keys verified) and
  all lie at X corners; guard tests assert the X-corner property at 32²/64²
  (`test_p12c_caseC_32.py:120-121`). The 0↔π corner tie is broken by solver noise (degenerate
  X-corner pair), consistent with A9. Recorded, no inconsistency.

## A11 — Actual calculations, not copied/interpolated

- Wall times recorded per cell: 32² 11²/21² = 759.5 s / 2813.5 s, path 403.0 s; 64² = 164.9 s /
  6439.7 s, path 896.9 s; totals 3976.1 s / 7501.5 s — inconsistent with any copy of the
  4²–16² results (those cost 0.39–1617 s total).
- 32² and 64² values are not midpoints of their neighbours: ½(2.0722+1.9736) = 2.0229 ≠ 1.9736;
  ½(1.9736+1.9179) = 1.9458 ≠ 1.9179.
- Independent re-derivation: gate **v2** regenerated the 4²/8²/16² gaps from scratch with the
  P12C engine and reproduced the authoritative P11D values in all 6 cells (≤3.4e-12), i.e. the
  engine demonstrably computes rather than replays values.
- Row-level checkpointing was used during the scans (disclosed in the staged-execution note).
  No checkpoint files are committed or present in the working tree (verified). This is expected
  once a scan completes and is **not** an evidence gap, because each cell's final extrema and
  timings are recorded in the JSONs.
- Staged-subprocess execution is disclosed in `metadata.staged_execution_note`; `wall_time_total_s`
  is the sum of per-stage times (32²: 3976.08 s = 759.5+2813.54+403.04 ✔; 64²: 7501.48 s =
  164.89+6439.69+896.9 ✔).

## A12 — Precision and deterministic repeatability

- **Assembly equivalence (v3):** sparse mirrored assembler vs the locked dense assembler,
  repeated at 4²/8²/16² in every run: max|ΔK| ≤ 9.1e-13, max|ΔM| ≤ 1.1e-16.
- **Eigenpair certification (v5):** shift-independent residuals ‖(K−λM)v‖/(|λ|‖Mv‖):
  32² ≤ 4.1e-9; 64² ≤ 1.08e-7 (gates 1e-8 / 1e-6). Solver noise floor is ≥5 orders of magnitude
  below the smallest mesh decrement of interest (d₄ = 0.0557).
- **Cross-engine agreement (v1):** 15 records (5 spot-k points × 4²/8²/16², Γ included);
  per-mesh maxima 2.98e-13 (4²), 2.07e-12 (8²), 6.36e-10 (16²).
- **Repeatability witness (recorded, not re-run):** the evidence JSONs contain *repeated*
  validation records accumulated over staged/re-invoked processes — v1: 15 records,
  v2: 24 records, v3: 15 records — every one within its gate, i.e. independent process
  invocations reproduced the same quantities to ≤1e-9. Additionally the P4B record documents
  two consecutive P4B executions agreeing to max|Δω| = 2.1e-13.
- ARPACK tolerance 1e-12 recorded; engine disclosed (OPinv-managed SuperLU shift-invert).
- No determinism counter-evidence found (no conflicting duplicate values among repeated records).

## A-Blockers

1. **None of the A-items failed.** No P12C scientific value, sidecar, script, or claim was found
   incorrect or unsupported.
2. **A-F1** task-spec erratum (d₄) — informational only.
3. **A-F2** inert hard-coded `d2` in the 64² script — informational; scripts deliberately not
   modified.
4. Residual provenance nuance: the 41×41 BZ evidence exists only for 4²/8²/16² (documented,
   by design).
