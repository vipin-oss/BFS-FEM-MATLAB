# P5 — readiness record (Case H pilot basis)

Purpose: state, from executed evidence only, what the P5 pipeline *is* ready to do, what it is
**not** ready to do, and which numerical issues are known and how they are handled.
Gate status remains **P5 NOT PASS** (see `audit/P5_STATUS.md`); downstream statuses unchanged
(B6 PARTIAL, PCR1 NOT PASS, G3 NOT MET).

## 1. Pipeline components (all executed)

| component | path | state |
|---|---|---|
| core (frozen assembly reuse, reduction, solver, MAC, gaps, manifest) | `production/p5/p5_core.py` | executed; lint-clean (parameters-only rule) |
| run driver (path + zone solves, checks C1–C9, immutable raw outputs, manifest) | `production/p5/p5_run.py` | executed on smoke, pre-flight and pilot grids |
| pilot parameter file | `params/p5_pilot_params.yaml` | `status: PILOT`; every entry carries tag + source |
| parameters-only lint | `production/p5/lint_p5_params.py` | PASS (0 violations; R1 allowlist, R2 no scientific literal, R3 frozen assembly called only with `conf[...]` arguments) |
| integrity test suite | `production/p5/test_p5_integrity.py` | 28/28 PASS |

Checks executed per run (15 named checks covering the eight required acceptance areas):
C1 solver completion/ndof/all bands · C2a Hermiticity · C2b `K̄(k+G)=K̄(k)`, `ω(k+G)=ω(k)` ·
C3 resolution ≥ P4B floor · C4 tracking (MAC, window adequacy) · C5 filter/NaN accounting ·
C6a gap ordering · C6b no complete gap where the model cannot have one · C7a k-evenness ·
C7b irreducible extrema = full-grid extrema · C7c actual group is a symmetry · C7d C4v not imposed ·
C7e X ≠ Y witness · C8 re-solve determinism · C9 per-mode residuals.

## 2. Numerical issues found and how they are handled (nothing hidden)

1. **Tracking window truncation (C4).** The continuation partner of a reported band can sit several
   sorted-band indices away from it at the next k (measured: 4 indices). With a 2-column buffer the
   match was truncated and the run reported `min_mac = 2e-22` — a *window* artefact, not a physics
   failure. Handling: request `n_bands + 8` Ritz pairs (tracking only, never reported) plus a
   `track_guard` adequacy sub-check that fails C4 if a reported mode is matched in the last two
   columns of the window. Diagnosed first as "possible ARPACK/buffer artefact": **refuted** —
   buffers 0/2/4/8 and tolerances 1e-10/1e-12, and the dense path, all gave the same value.
2. **Low-k mode rotation (C4).** With 10 points per leg the two lowest branches rotate enough in
   shape that matched MAC = 0.863 < 0.90 over one M–Γ step; identical with dense and sparse solvers.
   Handling: refine the path (20 points/leg ⇒ 0.962) — the criterion is met by resolution, never by
   relaxing `mac_min`.
3. **Zone/path sampling mismatch (C6a).** `Δ_path ≥ Δ_complete` is a statement about the *true*
   continuous sets; on discrete samples a coarser zone grid can miss the path extremum and produce a
   spurious negative slack (measured `−0.184` with a 5×5 grid at n_mesh=16). Handling: zone grid
   spacing = path spacing (`41×41` full BZ), so the path nodes are grid nodes; residual slack is
   `0…−2.3e-10`, i.e. numerical.
4. **Shift on the null cluster (C4, data accuracy).** The P4B-era `σ = −1e-6` is effectively *on*
   the Γ null cluster (`ω² ≈ 0`). With it, the sparse path returned symmetry-degenerate doublets
   split by up to `4.5e-4` (so the degeneracy mask missed them and per-mode MAC was evaluated inside
   a basis-arbitrary cluster, giving `min_mac = 0.485` at pilot step 1) and residuals of `5.3e-11`.
   Handling: `σ = −1.0`, separated from the spectrum by O(1) — splits collapse to `1e-10`, residuals
   to `5.5e-16`, centroids unchanged. The dense path never used `σ`, which is why the same operator
   at n=16/n=24 showed exact degeneracies and exposed the artefact.
5. **Re-solve determinism (C8).** ARPACK's random start vector perturbs the *members* of a
   symmetry-degenerate cluster at the level of its tolerance (measured `max|Δω²| = 7.7e-6` at Γ,
   which is 3.1e-6 in ω). Handling: fixed start vector (`arpack_v0_seed = 0`) ⇒ `max|Δω²| = 0.0`.
   The gate is applied to `ω²`, because `ω = √(ω²)` is ill-conditioned at the Γ null modes; the ω
   difference is reported for information.
6. **Residual normalisation at soft/null modes (C9).** `‖Kv−λMv‖/‖Kv‖` diverges for the Γ internal
   null modes (`‖Kv‖ ≈ 1e-11`), which produced a bogus `max_residual = 0.999`. Handling: residuals are
   scale-normalised, `‖Kv−λMv‖/(‖K‖_F‖v‖)`, and gated only for modes outside symmetry-degenerate
   clusters (inside a cluster the eigenvectors are basis-arbitrary, so neither MAC nor per-mode
   residual is defined).
7. **Degenerate clusters are real in this operator.** ω² is degenerate at Γ, X, M and along symmetry
   lines (Γ null doublet + orthogonal two-fold pairs); modal bases there are arbitrary. This is why
   the documented rule is Hungarian matching + `deg_tol` + cluster reporting, and not per-mode
   diagonal MAC, which is meaningless here.
8. **Mass-metric conditioning (recorded; not a defect).** The mass matrix has diagonal entries spanning
   ~6e-9…1.4e-1, so M-orthonormality of ARPACK vectors reaches only ~3e-8 (dense path ~3e-15).
   Consequence: MAC values are trustworthy to ~1e-7, far below the 0.90 gate and the observed
   margins; cross-checks gave identical MAC to 4 decimals between dense and sparse paths.
9. **Thread oversubscription (recorded).** With 2 workers × 2 BLAS threads the box ran 5.2× slower
   per k-point than with 1 thread per worker; the driver pins BLAS/OMP threads to 1 (spectrum
   unchanged, `max|Δω²| = 0.0` between settings).

## 3. Evidence trail (executed)

| run | grid | result |
|---|---|---|
| smoke, n_mesh=8, `…-dbb49a67` | reduced | 12 PASS / 2 FAIL (C3 8<32 expected; C4 all steps degenerate — a reduced grid cannot validate C4) |
| pre-flight, n_mesh=16, 5×5 zone | 31+25 | 11 PASS / 4 FAIL (C3, C4 window, C6a sampling, C8 determinism) — all four diagnosed, see §2 |
| pre-flight, n_mesh=16, 21×21 zone aligned, buffer 8 | 31+441 | 13 PASS / 2 FAIL (C3, C4 0.863) → path refined |
| pre-flight, n_mesh=16, 41×41 zone aligned, `N_seg=20` | 61+1681 | **14 PASS / 1 FAIL (C3 only, n_mesh=16 < floor 32; expected on a pre-flight grid)** |
| pre-flight, n_mesh=16, 41×41 zone, corrected shift | 61+1681 | **14 PASS / 1 FAIL (C3 only)**; C4 `min_mac=0.9618`, C9 `3.7e-16`, C6a slack `−1.7e-13` |
| pilot, n_mesh=32, run 1 (`…-48ea7f9e`, `σ=−1e-6`) | 61+1681 | 14 PASS / 1 FAIL (C4 `min_mac=0.485` at step 1) → diagnosed as the shift artefact of §2.4; kept as superseded raw output, not deleted |
| pilot, n_mesh=32, run 2 (`P5-20260922T200303Z-H-pilot-48ea7f9e`, corrected shift) | 61+1681 | **15 PASS / 0 FAIL**; C4 `min_mac=0.9278`, C9 `8.1e-16`, C6a slack `−2.0e-11` (details in `audit/P5_STATUS.md`) |

Reduced-grid smoke runs are machinery validation only and are never reportable as paper results
(they are kept under scratch paths, not in `results/`).

## 4. Not ready / blocked

1. **Case C (S2, S3–S8 gap claims): blocked.** Inclusion radius/contrast and the `ω₀`, `v̄`
   normalisation phase are not established from sources (TV6/TV14); the Case-C inclusion assembly does
   not exist yet. No complete-gap claim is possible for Case C until then, and Case H can never claim
   one (C6b).
2. **AR sweeps (S1, S3, S4, S5): blocked on the `AR` definition.** The frozen assembly has no
   unit-cell aspect parameter, so `AR` must be defined as the microstructure anisotropy ratio; see
   `production/p5/P5_PARAMETER_LOCK_REQUEST.md` §3.1.
3. **Energy flux (S8) and micro-inertia study (S9) drivers** are not written yet (P5 scope, later
   cases); the flux partition requires the P4B kinetic/potential split, which exists and is frozen.
4. **Manifest location**: the master plan specifies `runs/<run_id>/manifest.json`; the driver writes
   the run directory under `results/raw/<run_id>/` (per `results/raw/README.md`). Reconciliation is
   requested in the lock request; until decided, both the run directory and the plan path are treated
   as the manifest home (byte-identical copy).

## 5. Claims boundary (applies to every P5 dataset)

* No complete band gap is claimed for Case H — dispersion only (M12 G6).
* Path gaps and directional gaps are never called complete gaps; a complete gap requires the 2D zone
  sample, never Γ–X–M–Γ alone.
* The symmetry used is the actual point group of the operator (here C2 at a generic orientation);
  C4v is never imposed under anisotropy.
* Branch numbering is the sorted-eigenvalue label; index re-orderings through crossings are reported
  with their k-position, and no data are smoothed, interpolated or manually edited.
* The pilot dataset is a declared machinery-validation run and must not be reported as a paper result.
