# P5 — scientific production runs (status)

**Phase order:** P4A → P3 → P4B done; **P5 active**; P6–P9 not started.
**Gate: P5 NOT PASS.** The pilot production case passed all 15 integrity checks; the remaining
frozen P5 cases (S1–S9) are blocked on open parameter decisions (TV4/TV6/TV7/TV14, see §6), so
the gate stays open. Downstream status is unchanged: **B6 PARTIAL / PCR1 NOT PASS / G3 NOT MET**.

Phase-B/phase-1 symbolic results are untouched by this phase; P5 does not revisit B6/LWZ, adds no
published validation, and does not modify the formulation frozen through P4B.

## 1. Pilot production case (required first step)

| item | value |
|---|---|
| run id | `P5-20260922T200303Z-H-pilot-48ea7f9e` |
| status | PILOT (machinery validation; **not** a paper result) |
| parameters | `params/p5_pilot_params.yaml` (hash `48ea7f9e92801dedb601262f6d9ebaf9916a9492b61516fc764ab8ef2eeab145`) |
| basis | Case H, θ = 30°, l1 = 0.30, l2 = 0.10 (generic orientation, actual group C2) |
| resolution | n_mesh = 32 (P4B floor), n_bands = 8 reported, path 3×20+1 = 61 k, zone 41×41 = 1681 k |
| outputs | `results/raw/P5-20260922T200303Z-H-pilot-48ea7f9e/` (+ byte-identical manifest at `runs/P5-20260922T200303Z-H-pilot-48ea7f9e/manifest.json`) |
| wall time | ≈ 1 h 54 min (path 290 s + zone 6426 s solves on 2 pinned workers; remainder checks + manifest) |

### 1.1 Integrity checks (15 PASS / 0 FAIL)

| check | verdict | measured value |
|---|---|---|
| C1 solver completion (1742 k, ndof = 8192, all bands) | PASS | non-finite solves 0 |
| C2a Hermiticity of the reduced pencil | PASS | max_rel 0.0 (tol 1e-12) |
| C2b Bloch phase `K̄(k+G) = K̄(k)`, `ω(k+G) = ω(k)` | PASS | matrix 3.94e-17, ω diff 1.09e-11 (tol 1e-8) |
| C3 resolution at/above the P4B floor | PASS | n_mesh 32 = floor; ε_Δ = 4.6318e-11 |
| C4 tracking (matched MAC, window adequacy) | PASS | min_mac 0.9278 @ step 59 (tol 0.90); 54/60 steps evaluable; drift ≤ 3; no guard risk |
| C9 eigenpair residuals (non-degenerate reported modes) | PASS | max 8.13e-16 (tol 1e-8); 456 modes gated, 32 degenerate excluded |
| C5 no NaN/Inf, no silent negative | PASS | non-finite 0, negative 0, null modes reported 6 |
| C6a frozen gap definition `Δ_path ≥ Δ_complete` | PASS | min slack −1.98e-11 (tol 1e-8) |
| C6b no complete gap where the model cannot have one | PASS | Case H; none claimed; max complete gap −0.4427 |
| C7a k-evenness `ω(−k) = ω(k)` | PASS | max diff 0.0 |
| C7b irreducible extrema = full-grid extrema | PASS | diffs 0.0; domain C2; 861 irreducible points |
| C7c actual group is a symmetry of the spectrum | PASS | C2 residual 0.0 |
| C7d C4v NOT imposed under anisotropy | PASS | R90 witness 0.2872 ≫ 1e-6 |
| C7e X and Y inequivalent (`l1 ≠ l2`) | PASS | \|Δ\| 0.2290; ωX 2.7504, ωY 2.6992 |
| C8 re-solve determinism | PASS | max\|Δω²\| 0.0 (tol 1e-10), 3 repeats |

## 2. What the pilot establishes

* **Solver/no-failure:** every sampled k solved; no NaN/Inf; no unphysical negative eigenvalue; the
  6 internal null modes (Γ rigid translations at the three Γ points) are reported, never dropped
  (TV7 rule: only non-finite/negative roots would be flagged, and they would fail the run).
* **Hermiticity / phase consistency:** `K̄ᴴ = K̄`, `M̄ᴴ = M̄` exactly; `K̄(k+G) = K̄(k)` to 3.9e-17 and
  `ω(k+G) = ω(k)` to 1.1e-11 on three reciprocal vectors.
* **Resolution:** n_mesh = 32 = the P4B-validated floor (ε_Δ = 4.6318154949690315e-11).
* **Branch continuity:** matched-mode MAC ≥ `mac_min = 0.90` on every evaluable step of the path
  (positions of index re-orderings through crossings are reported, M12.2); the tracking window is
  verified adequate (no reported mode matched in the guard band); steps at the high-symmetry
  endpoints Γ, X, M where the spectrum is degenerate by symmetry are reported as not evaluable
  (inside a degenerate cluster the modal basis is arbitrary), not silently skipped.
* **Gaps:** path, directional and complete quantities are computed with the frozen M12.3 definition
  from a single dataset; `Δ_path ≥ Δ_complete` holds to numerical noise because the zone grid
  contains the path nodes; **no complete gap is claimed** for Case H (dispersion only, M12 G6).
* **Zone coverage:** the required irreducible domain of the *actual* group (M10-a ruling (a)) is
  present: irreducible extrema equal full-grid extrema exactly, k-evenness holds pointwise
  (`ω(−k) = ω(k)`), and the actual group C2 is verified as a symmetry of the spectrum.
* **Symmetry discipline:** C4v is *not* imposed under anisotropy — R90 is verified to be a
  non-symmetry (witness residual ≫ tolerance) and Γ–X ≠ Γ–Y by an explicit witness.
* **Reproducibility:** identical re-solve of three path points (bitwise, `max|Δω²| = 0.0`);
  parameters, git state, environment, frozen-source hashes and output hashes are recorded in the
  manifest; raw outputs are written once and made read-only.

## 3. Datasets (pilot)

| file | content | dimensions |
|---|---|---|
| `bands_path.npz` | Γ–X–M–Γ path: k, leg ids, ω, ω², phase velocity | 61 × 8 |
| `zone_omega.npz` | full-BZ grid: k, ω, ω², irreducible mask, spacing | 1681 × 8 |
| `vg_zone.npz` | group velocity on the grid (central differences, M12 (51)) | 1681 × 8 × 2 |
| `gaps.json` | directional / path / complete gaps for 7 adjacent band pairs | 7 pairs |
| `checks.json` | 15 integrity checks with residuals | — |
| `manifest.json` | run id, git, params snapshot + hash, env, output hashes, gates | — |
| `run_log.txt` | full driver log | — |

## 4. Superseded run kept for the record

`results/raw/P5-20260922T170429Z-H-pilot-48ea7f9e/` (14 PASS / 1 FAIL, C4) is kept, not deleted:
it exposed that the P4B-era ARPACK shift `σ = −1e-6` sits on the Γ null cluster and degraded the
sparse eigensolver (cluster splits `4.5e-4`, residuals `5.3e-11`, `min_mac = 0.485`). The diagnosis
and the corrected setting (`σ = −1.0`) are recorded in `audit/P5_READINESS.md §2.4` and
`production/p5/P5_PARAMETER_LOCK_REQUEST.md §2.3`.

## 5. Tests and audits executed

* `python3 -m pytest production/p5/test_p5_integrity.py -q` → **28 passed**.
* `python3 production/p5/lint_p5_params.py --params params/p5_pilot_params.yaml` → **PASS**
  (0 violations; parameters-only rule for solver code).
* Pre-flight runs on a reduced mesh (n_mesh = 16) with the final pipeline → 14 PASS / 1 FAIL
  (C3 only, n_mesh < floor 32 — expected on a pre-flight grid; recorded in
  `audit/P5_READINESS.md §3`).

## 6. Blockers for the remaining frozen cases

1. **Case C (S2, and the gap claims of S3–S8):** inclusion radius/contrast and the `ω₀`, `v̄`
   normalisation phase are not established from the sources (TV6/TV14); the Case-C inclusion
   assembly is not implemented. Case C cannot start by inventing parameters.
2. **AR sweeps (S1, S3, S4, S5):** the frozen M14/M15 assembly has no unit-cell aspect parameter, so
   `AR` must first be defined as the microstructure anisotropy ratio (requested in
   `production/p5/P5_PARAMETER_LOCK_REQUEST.md §3.1`).
3. **S8 energy flux / S9 micro-inertia** drivers are not written yet (P5 scope, later cases).

## 7. Files created in this phase

```
production/p5/p5_core.py                 P5 core (frozen-assembly reuse, solver, MAC, gaps, manifest)
production/p5/p5_run.py                  production run driver (path + zone, 15 checks, raw outputs)
production/p5/lint_p5_params.py          parameters-only lint
production/p5/test_p5_integrity.py       integrity test suite (28 tests)
production/p5/P5_PARAMETER_LOCK_REQUEST.md  requested [S] locks with evidence
params/p5_pilot_params.yaml              pilot parameter file (status: PILOT, tagged + sourced)
audit/P5_READINESS.md                    readiness record, numerical issues, evidence trail
audit/P5_STATUS.md                       this file
results/raw/P5-20260922T200303Z-H-pilot-48ea7f9e/  pilot raw dataset (immutable)
runs/P5-20260922T200303Z-H-pilot-48ea7f9e/manifest.json  plan-specified manifest location (byte-identical copy)
```
