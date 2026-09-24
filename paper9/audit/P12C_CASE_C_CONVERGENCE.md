# P12C Case-C Complete-Gap Convergence — Remediation Audit

**Phase:** P12C (branch `phase-1-symbolic`; `main` untouched at `98176e8`)
**Governing document:** Paper9 Blueprint v1.3 — unmodified
**Entry SHA:** `11543157541c1b9bf9ec4106e1b68f468da9f4a2` (P12B closeout; `origin/phase-1-symbolic` verified at entry)
**Date:** 2026-09-23
**Rule in force:** every claim traceable to an actual calculation; nothing made to "look ready"; no post-hoc reinterpretation of pre-registered rules.

---

## 1. Scope

Execute the mandated Case-C complete-gap convergence extension on the exact
locked P11D Case-C model, with no scientific-model change to cut runtime:

1. FE `32x32` (dofs 8712) at BZ `21x21` — mandatory;
2. apply the pre-registered `64x64` rule EXACTLY once the 32x32 data existed;
3. compare against the authoritative P11D `4x4/8x8/16x16` series;
4. report Δ_X, Δ_path and Δ_complete separately (never conflated);
5. check BZ sampling consistently with the existing 11/21/41 evidence;
6. update only the genuinely required numerical statements;
7. add regression guards; full suite green; ONE atomic commit; push only
   `phase-1-symbolic` with a fresh user-supplied PAT.

Authority for the run: explicit user authorization in the P12C brief.

## 2. Result — complete gap Δ_complete (direct min/max over the 21x21 zone)

Definition (locked, unchanged): Δ_complete = min_{BZ} ω̄₄ − max_{BZ} ω̄₃,
evaluated directly on the quarter-zone grid (Γ, X, M included); never
inferred from Δ_X.

| FE mesh | dofs 8(N+1)² | Δ_complete (21x21) | Δ_X | Δ_path |
|---|---|---|---|---|
| 4×4  | 200   | 2.5731869148 | 2.7563 | 2.5732 |
| 8×8  | 648   | 2.2503884154 | 2.2504 | 2.2504 |
| 16×16| 2312  | 2.0722484271 | 2.0722 | 2.0722 |
| **32×32** | **8712** | **1.9736363149** | **1.9736** | **1.9736** |
| **64×64** | **33800** | **1.9178891172** | **1.9179** | **1.9179** |

- Successive decrements per mesh doubling: d₁ = 0.3228, d₂ = 0.17814,
  d₃ = 0.09861, d₄ = 0.05575.
- Successive-decrement ratios (all computed from the measured values above):
  d₂/d₁ = 0.552, d₃/d₂ = 0.554, d₄/d₃ = 0.565. Effective observed refinement
  rate ≈ 0.55 per mesh doubling (p_obs = log₂(1/ratio) ≈ 0.82–0.86).
- Δ_X equals Δ_complete from 8×8 upward because **both** band edges sit at the
  X corners (an observed geometric fact, not a definitional identity); the two
  quantities remain distinct and are reported separately.
- Test-set/grid provenance: BZ extrema at 32×32 — max ω̄₃ = 4.2027 at
  (0, π); min ω̄₄ = 6.1763 at (π, 0). At 64×64 — 4.1593 and 6.0772 at
  (π, 0). Gaps are open at every mesh and grid.

**Extrapolation remark (explicitly NOT a computed result):** if the ≈0.55
decrement ratio persisted, the geometric tail from d₄ would sum to
d₄·r/(1−r) ≈ 0.068, implying a limiting width of order 1.85. This estimate is
recorded for orientation only; it is not used in the manuscript, and no
mesh-converged value is claimed.

## 3. Pre-registered 64×64 decision (applied exactly, recorded before the run)

Locked rule: run `64x64` iff r = d₃/d₂ ≥ 0.5, where d₃ = Δc(16²)−Δc(32²),
d₂ = Δc(8²)−Δc(16²) (both from measured data).

Evaluated after the 32×32 cells (recorded in
`results/raw/p12c_caseC_32_gap_convergence.json :: rule_64_evaluation`):

> r = 0.098612 / 0.178140 = **0.5535652777739338 ≥ 0.5 → RUN 64x64 (trigger met)**

The 64×64 level was then run; the post-64 ratio d₄/d₃ = 0.5653 is reported as
data only (the locked rule chain specified 64×64 as its end level; if the same
criterion were extended to a further level it would trigger again).

## 4. Brillouin-zone resolution finding

- At fixed FE mesh, 11×11 and 21×21 grids give **identical** Δ_complete to
  6 decimals at 32×32 (1.973636 both) and 64×64 (1.917889 both).
- Historical P11D evidence: 21×21 vs 41×41 at 4×4 differ by 4×10⁻⁴
  (2.5732 vs 2.5728); at 8×8 and 16×16 identical to 4 decimals.
- BZ-sampling convergence (≈≤5×10⁻⁴) is therefore cleanly separated from the
  FE-mesh error, which is two orders larger and still decreasing at 64×64.

## 5. Engine and deviations (all disclosed in the evidence JSON metadata)

Methodology, model, parameters, boundary/interface treatment, immersed
TV18 quadrature (ngauss=4), branch tracking (ascending-sqrt indices [2],[3]),
tolerances (ARPACK tol 1e-12) and gap definitions are **identical** to the
locked P11D engine. The linear-algebra backend differs of necessity, and each
difference is disclosed and gated:

1. **Sparse mirrored assembler** — element values bit-identical to the locked
   dense `assemble_mesh_KM_ngauss` (gate v3: max|dK| ≤ 9.1e-13, max|dM| ≤
   1.1e-16 in all runs). The locked dense engine needs ≈5 GB at 32×32 and was
   OOM-killed in this 2 GB sandbox (measured, `dmesg`-verified).
2. **Continuous selection σ = −0.25** (alt −0.5 in the cross-check), ARPACK
   shift-invert with explicit externally-managed `splu` via `OPinv`. scipy's
   built-in σ-mode leaked ≈LU-size per `eigsh` call in this build
   (root-caused via dmesg-verified OOM kills and RSS-drift experiments);
   raw `splu` create/destroy cycles showed zero drift. Same ARPACK mode, same
   σ, same tolerance, same eigenpair selection.
3. **Sparse-native Bloch T** — bit-identical entries to
   `solver.build_mesh_bloch_T` (verified at 8×8/16×16 × 3 k before use);
   avoids a 1.14 GB dense transient per k at 32×32.
4. **64×64 only:** SuperLU `permc_spec="MMD_ATA"` for the shifted operator.
   Default ordering exceeded the memory cap at 64×64 (measured kills; probe
   script `production/p12c_64_feasibility_probe.py`); the
   adopted factorization measured nnz = 42 895 861 (≈1.03 GB), 7.8 s,
   solve 0.12 s, peak RSS 1.12 GB including a full eigensolve. Ordering does
   not alter the mathematical problem.
5. **Staged subprocess execution with row-level checkpoints** (sandbox
   memory-cap discipline): wall times recorded per cell; `wall_time_total_s`
   is the sum of the 32×32 (resp. 64×64) cell and path times.

## 6. Validation gates (all PASS; recorded in the evidence JSONs)

| Gate | Content | Result |
|---|---|---|
| v1 | spot-k vs both P11D engines (`gvx`, `solve_bloch_mesh`) at 4/8/16² | ≤ 4.6e-10 (Γ included; gate 1e-9) |
| v2 | reproduce authoritative P11D Δc at 4/8/16² × {11²,21²} (values read from the P11D JSON registry) | all 6 cells ≤ 3.4e-12 |
| v3 | sparse- vs dense-assembled K, M equality | ≤ 9.1e-13 (gate 1e-12) |
| v4 | cross-σ coherence at spot-k (32², 64²) | non-Γ ≤ 9.4e-10 (gate 1e-9); Γ recorded ≤ 9.7e-9/3.8e-9 with calibrated catastrophic-flag gate 1e-7 / 3e-7 |
| v5 | **shift-independent eigenpair residuals** ‖(K−λM)v‖/(|λ|‖Mv‖) | 32²: ≤ 4.1e-9; 64²: ≤ 1.08e-7 (gate 1e-6); solver noise floor ≥ 3 orders below d₄ = 0.0557 |

## 7. Evidence provenance

| Artifact | Content | Integrity |
|---|---|---|
| `results/raw/p12c_caseC_32_gap_convergence.json` (+`.sha256`) | 32×32 cells (11², 21²), path (N_seg=20), comparison, rule evaluation, validation v1–v5, environment, git SHA, parameter snapshot + hash | sha256 sidecar |
| `results/raw/p12c_caseC_64_gap_convergence.json` (+`.json.sha256`) | 64×64 cells, path, post-64 report, disclosures, validation | sha256 sidecar |
| `results/raw/p11d_caseC_gap_convergence.json` | authoritative 4/8/16² series | **unmodified** |

Wall times: 32×32 — 11² 760 s, 21² 2814 s, path 407 s. 64×64 — 11² 165 s,
21² 6440 s, path 911 s.

## 8. Manuscript updates (numerical statements only)

`sec06_results.tex` (mesh-refinement and BZ items of the Discretization
paragraph), `sec08_discussion.tex`, `sec09_conclusions.tex`: series extended
to 32×32/64×64 with the decrements and ratios above. The honest verdict is
**unchanged — the complete gap is not mesh-converged**, no mesh-converged
width is claimed, and Δ_X ≠ Δ_complete wording is preserved. No language
polishing.

## 9. Tests

New guards: `verification/suite/test_p12c_caseC_32.py` (presence/provenance,
definitions & separation, rule decision recomputed from evidence, no false
"converged") and `verification/suite/test_p12c_caseC_64.py` (presence/
provenance incl. MMD_ATA and measured-infeasibility disclosures, cell
definitions, report consistency, certification, manuscript honesty).
Full-suite status recorded in the P12C closeout.

## 10. PCR / gates

PCR5's Case-C note (honest decreasing trend, not mesh-converged) remains
accurate and is now backed by five meshes instead of three; no PCR status
changes. G3 / G4 remain **NOT MET** (unchanged, per P11D mapping).

## 11. Sandbox re-provisioning and commit re-creation (provenance record)

Between the creation of the P12C commit and its push, the execution sandbox was
re-provisioned: the local `.git` directory was lost (the workspace snapshot is
files-only), so the local commit `74e450e` no longer existed anywhere — remote
`phase-1-symbolic` was still at `1154315` (P12B). Recovery, none of which
changed any result:

1. The repository was re-cloned anonymously (public remote) at
   `phase-1-symbolic = 11543157541c1b9bf9ec4106e1b68f468da9f4a2`; verified `HEAD`
   == `1154315` == `origin/phase-1-symbolic`.
2. All P12C work-product files survived the re-provision and were overlaid onto
   the clone; `git status` reproduced **exactly** the original 13-path change
   set. The two tracked `out/` directories absent from the restored tree are
   workspace-snapshot exclusions (present in git) and were restored from the
   clone.
3. sha256 sidecars of both evidence JSONs re-verified against their files.
4. Full suite re-run on the rebuilt tree: **72/72 PASS**.
5. The commit was re-created with the identical message; its SHA therefore
   differs from the lost `74e450e` (the SHA of record is the one in the pushed
   remote verified after this push). No git history was rewritten — the lost
   commit never left the sandbox; this section documents the re-creation rather
   than hiding it.
