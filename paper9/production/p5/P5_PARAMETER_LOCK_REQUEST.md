# P5 — parameter lock request (Case H pilot basis)

Status: **REQUESTED** (nothing in this file is locked yet; no value has been changed silently).
Scope: `[S]`-tagged production choices that the frozen `[P4A]`/`[P4B]` formulation does not fix.
This file requests a decision; it does **not** modify Blueprint v1.3, the M10-a ruling, the M12 gap
definitions, the M13/M15 assembly, or any committed P4A/P4B artefact.

## 1. Reused unchanged — no decision requested

| item | value | source / evidence |
|---|---|---|
| material set (Case H, homogeneous BFS) | `L=1, λ=1, μ=1, ρ=1, ℓ²=0.04` | `[S-P4A]`, frozen in P4A/P4B artefacts |
| length tensor (anisotropic) | `l1=0.30, l2=0.10` via frozen `L_plane(l1,l2,θ)` (M2) | `[S-P4A]`; rotation is the frozen M2 map |
| assembly | `assemble_nxn_bloch(n,kx,ky,L,λ,μ,ρ,ℓ²,L11,L22,L12)` (M14/M15) | validated in P4B 5i; DOF `8*node+4*comp+typ` (M13) |
| gap taxonomy | path / directional / complete; `Δ_path ≥ Δ_complete`; complete-gap claims need 2D zone sampling | M12.3, Blueprint §3.5 |
| mode tracking | MAC, sorted-band indexing, reorderings reported (M12.2) | frozen |
| symmetry | point group of the ACTUAL operator (M10.3): C4v(AR=1) → C2v(θ=0/90°) → C2v′(θ=45°) → C2 (generic) | M10/M10-a; M10-a v1.4 **not** applied |
| resolution floor | `ε_Δ = 4.6318154949690315e-11` ⇒ `n_mesh ≥ 32` | P4B 21/21 PASS |
| reduction / solver API | `p4a`-reused `assemble_KM`, `T_impl`, `reduce_mat`, `L_plane`, `omega2` | frozen in P4B |

## 2. Requested locks, with the measurement that fixes each one

### 2.1 TV4 — k-sampling

* **TV4a path sampling: `path_N_seg = 20` per leg (Γ–X, X–M, M–Γ) ⇒ 3×20+1 = 61 k-points.**
  Evidence (pilot operator, θ=30°, l1/l2 = 0.30/0.10): matched-mode MAC of the two lowest branches
  over a single M–Γ step is **0.863 at `N_seg=10`** (Δk = 0.1π/L) and **0.962 at `N_seg=20`**
  (Δk = 0.05π/L), i.e. the tracking criterion is met by *resolving* the path (quadratic in Δk),
  not by relaxing `mac_min = 0.90`. The 0.863 value was reproduced identically with the dense
  eigensolver and with shift-invert, so it is a physical mode-shape rotation of the low branches
  at small k, not a solver artefact.
* **TV4b zone sampling: uniform full-BZ grid `41×41` (spacing `2π/40 = π/20`).**
  The grid spacing equals the path spacing, so the path node set is a **subset** of the grid node
  set; the ordering invariant `Δ_path ≥ Δ_complete` is then sharp on the discrete sets rather than
  sampling-limited (a `5×5` grid produced a spurious slack of `−0.184` at n_mesh=16 because the
  coarse grid missed the path extremum; the aligned grid gives `−2.3e-10…0`, i.e. numerical noise).
  41×41 = 1681 points, 861 of which are in the C2 irreducible domain.

### 2.2 TV7 — reported bands and the spurious-mode / filter documentation

* **Reported bands `n_bands = 8`** (lowest eight of the reduced pencil).
* **No spurious-branch filter is applied, because nothing is discarded.** `mode_filter` counts
  (i) non-finite eigenvalues, (ii) `ω² < neg_tol` roots and (iii) `|ω²| ≤ null_tol` internal null
  modes; (i) and (ii) make the run FAIL (never silently dropped), (iii) are reported as physical
  low-frequency internal modes (Γ rigid translations, M15-a / P4A 5f). No smoothing, interpolation,
  re-ordering of data or manual editing anywhere.

### 2.3 Solver settings (numerical, not observable)

| setting | requested value | evidence |
|---|---|---|
| shift `σ` | **`−1.0`** (P4B-era value was `−1e-6`) | the lowest eigenvalues are the internal null modes at `ω² ≈ 0`; a shift sitting on them (`−1e-6`) degrades the sparse eigensolver by 5 orders. Measured at Γ, n_mesh=32: symmetry-degenerate cluster splits `4.5e-4` and reported-mode residuals `5.3e-11` at `σ=−1e-6` versus `1e-10` and `5.5e-16` at `σ=−1.0` (cluster centroids identical to 12 digits). `−1.0` is separated from the whole spectrum (`ω² ≥ 0`) by O(1). Any new parameter set re-runs this check before production |
| ARPACK `tol` / `maxiter` | `1e-10` / `20000` | reported-mode residual gate C9 ≤ `1e-8`, actual ≤ `5.5e-16` with the corrected shift |
| ARPACK start vector | fixed, `arpack_v0_seed = 0` | without it a random start perturbs the members of a symmetry-degenerate cluster at the level of the convergence tolerance, which broke the re-solve determinism gate C8 (`3.1e-6`); with it C8 is exact (`0.0`) |
| dense path | only for `ndof ≤ 512` (n ≤ 8) | dense is bitwise deterministic and is kept as the cross-check in the test suite; production n=32 is sparse |
| tracking buffer | `n_bands_buffer = 8` extra Ritz pairs, **tracking only, never reported** | measured maximum band-index drift over one path step is 4 indices (band 7 at k_A matches band 10 at k_B); a 2-column buffer truncated the match and produced a spurious `min_mac = 0` |
| window guard | `track_guard = 2` | a reported mode matched in the last two columns of the tracking window fails check C4 as a possible truncation artefact |
| degeneracy rule | `deg_tol = 1e-6` (relative to `max|ω²|`) | inside a symmetry-degenerate cluster the eigenvector basis is arbitrary, so neither per-mode MAC nor per-mode residual is defined there; the cluster is reported, never averaged away |
| MAC gate | `mac_min = 0.90` (unchanged) | not relaxed at any point of the diagnosis |
| parallel setting | `n_proc = 2`, BLAS threads pinned to 1 | measured 4.30 s/k-point vs 8.41 (sequential) and 22.27 (2 workers × 2 BLAS threads); spectrum identical between settings (`max|Δω²| = 0.0`) |

## 3. Blocking gaps — no value can be locked yet

1. **`AR` vocabulary (blocks S1, S3, S4, S5).** The frozen M14/M15 assembly has **no unit-cell
   aspect-ratio parameter** (square cell of side `L`; verified: `AR` appears in the params schema and
   the manifest only, it does not enter `assemble_nxn_bloch`). Therefore the S1–S9 `AR` sweeps
   (`AR ∈ {1,2,3,5,7,10}`) can only act through the frozen length tensor, i.e. `AR` must be defined as
   the **microstructure anisotropy ratio** (e.g. `AR = l1/l2` with a locked scale). Decision requested
   before any AR sweep is launched.
2. **Case C materials (blocks S2, TV6/TV14).** Inclusion radius and contrast, and which phase's
   `μ, ρ` define `ω₀` and `v̄`, are not found in the available sources. No value is invented; the
   Case-C baseline cannot run until this is locked. The pilot (Case H) is unaffected.
3. **Pilot orientation.** The pilot uses `θ = 30°`, `l1 = 0.30`, `l2 = 0.10` (generic orientation,
   actual group C2) as the "one anisotropic orientation" required for the pilot. It is deliberately
   *not* an S1–S9 baseline point (S1 is `AR=1` vs `10`); it is a machinery-validation basis.

## 4. Explicitly not requested

No change to the frozen formulation, no C4v assumption under anisotropy, no tolerance relaxation
(`mac_min`, `deg_tol`, `residual_tol`, `ε_Δ` floor), no new published validation, no benchmark/source
data change, no digitisation-based error metric.

## 5. Decision

Requested by: P5 pilot execution (run `P5-20260922T170429Z-H-pilot-48ea7f9e`).
Requested decision: lock `path_N_seg = 20`, zone grid `41×41` full-BZ, `n_bands = 8` with the
"nothing is discarded" filter statement, the solver settings of §2.3, and the `AR = l1/l2` definition
of §3.1 (or an alternative explicit definition).
Until then the pilot stands as **PILOT** (`status: PILOT` in `params/p5_pilot_params.yaml`) and
**P5 remains NOT PASS**.

Update 2026-09-22: pilot run 2 (`P5-20260922T200303Z-H-pilot-48ea7f9e`, executed with the §2
settings: `σ = −1.0`, `N_seg = 20`, `41×41` zone, 8 reported bands) passed all 15 integrity
checks (C4 `min_mac = 0.9278 ≥ 0.90` at n_mesh = 32; C9 `8.1e-16`), confirming the requested
values. The requested decisions themselves remain open.
