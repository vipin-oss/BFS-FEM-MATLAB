# PHASE-1 DERIVATION AND MATHEMATICAL-AUDIT RECORD — MODULE M10
## Irreducible Brillouin zone, the Γ–X–M–Γ path and its sampling (blueprint §3.3, eq. (44))

Status: **M10 symbolic derivation COMPLETE — 23 checks PASSED; one forward-scope item FLAGGED
(M10-a), NOT repaired, ruling required.** M1–M9 and the M15-a ruling unchanged. M11–M17 NOT
STARTED. Blueprint v1.3 unchanged (sha256 `ca71b91a…dbf9f`). No numerical value, no k-point
count (TV4 not resolved, not guessed), no band, no solver, no benchmark.

Inputs (read-only): Blueprint v1.3 §3.3 (line 379), §3.5 (381: complete gap "over the whole
IBZ"), §4.6 (404), §6.4 (headline Γ–X → Γ–M migration), register (44) (576), Fig. 2, tests 5b/5c/5e;
`CALC_MASTER_PLAN.md` §A row M10 (TV4), TV table; M1–M9 records; `AUDIT_M15a_*` (locked pair
`K̄ᴴ = K̄`, `K̄(−k) = conj K̄(k)`, test structure T1–T4); M7 note M7-b.

Script: `scripts/m10_ibz_path.py` (deterministic, SymPy exact, writes no files); log
`checks/m10_ibz_path.log`; sha256 recorded in the log (pre-run = post-run).

---

## M10.0 Scope `[S]`

Blueprint §3.3: "Irreducible Brillouin zone for the square lattice: Γ(0,0) → X(π/L,0) →
M(π/L,π/L) → Γ. Discretisation of the path and the number of k-points per segment." → (44).
Plan row M10: input square lattice; output sampled path; k-points/segment = TV4 **[S]-pending**.

M10 therefore owns: (i) the path parametrisation and its sampling *structure*; (ii) the
*justification* of the path as the IBZ boundary, which requires the symmetry group of the locked
operator; (iii) consistency with M9 phases and the M15-a identities. It does **not** own the
non-dimensionalisation (M11), observables (M12), or any matrix (M13–M15).

---

## M10.1 The path (44), derived `[A]` (checks P1–P6)

- Three affine legs `k(t) = A + (B−A)t`, `t∈[0,1]`, continuous and closed; endpoints are the M9
  points `Γ, X = b₁/2, M = (b₁+b₂)/2`.
- Arc lengths `π/L, π/L, √2π/L`; total `(2+√2)π/L`; in `k̄ = kL/π` the abscissa breakpoints are
  `0, 1, 2, 2+√2` (dimensionless; M11 consistency only).
- Containment: every leg in the closed first BZ; X–M and M on the BZ boundary `k₁ = π/L`.
- Sampling structure with **symbolic** `N_seg` (TV4): `k_j = A + (B−A) j/N_seg`, `j = 0…N_seg`;
  `3N_seg+1` nodes, `3N_seg` distinct k; spacing `π/(L N_seg)` on the two straight legs and
  `√2π/(L N_seg)` on the diagonal — uniform *within* a leg, not *across* legs unless `N_seg` is
  scaled by leg length (a TV4 design option, recorded, not chosen).
- Phases along the path (M9): Γ–X `μ_y = 1, μ_x = e^{iπt}`; X–M `μ_x = −1, μ_y = e^{iπt}`; M–Γ
  `μ_x = μ_y = e^{iπ(1−t)}`. Unimodular everywhere ⇒ the M15-a pair holds at every sample; the
  tying is real only at Γ, X, M (consistent with M8-a-1 and M15-a: the literal (68) "passes" only
  there).

## M10.2 Case-H dispersion of the locked operator, derived `[A]` (S1–S3, T4–T5)

From the M8 strong form (O1) with the M9 ansatz `u = a e^{i(k·x−ωt)}` and the anisotropic (26):

```
H(k) a = 0 ,   H(k) = (1 + k·L·k/10) Γ_cl(k) − ρω²(1 + ℓ²|k|²) I
k·L·k = L₁₁k₁² + 2L₁₂k₁k₂ + L₂₂k₂²   (L = Rᵀdiag(l₁²,l₂²)R, blueprint (6)–(8); M2 mixed term 2L₁₂)
ω_L² = (λ+2μ)/ρ · |k|² (1 + k·L·k/10)/(1 + ℓ²|k|²) ,   ω_T² = μ/ρ · |k|² (1 + k·L·k/10)/(1 + ℓ²|k|²)
```

Polarisations `k` (L) and `k⊥` (T) exactly as classically: `L` scales both branches by the same
direction-dependent factor and does not rotate polarisation. Dimensions: `k·L·k`, `ℓ²|k|²`
dimensionless; `ω²` in s⁻². Envelope route with `∂→+ik` on the uniform envelope reproduces `H`
(M9 [B9a]); the sign is unobservable there (M9 [B9b]) — the discrete sign test is M15-a T3.
The 1D reduction reproduces the M7 structural check and contains the M15-a Hermite-cell reference.

## M10.3 Symmetry group and the irreducible zone, derived `[A]` (S4–S9, T1)

Criterion (proved): `ω(Qk) = ω(k) ∀k ⇔ Q L Qᵀ = L` (all other factors are O(2)-invariant).
Over the lattice point group C4v:

| case | group G | \|G\| | irreducible zone |
|---|---|---|---|
| AR = 1 | C4v | 8 | triangle Γ–X–M = \|BZ\|/8 (M9 [L10]) |
| θ = 0° or 90°, AR ≠ 1 | {I, −I, σ_x, σ_y} | 4 | quarter square = \|BZ\|/4 |
| θ = 45°, AR ≠ 1 | {I, −I, σ_d, σ_d′} | 4 | \|BZ\|/4 |
| generic θ, AR ≠ 1 | {I, −I} | 2 | half BZ = \|BZ\|/2 |

Inversion `−I` is always present: `ω(−k) = ω(k)` is exactly the spectral content of the M15-a pair
(T1), so the half-BZ reduction is guaranteed by the operational formulation and needs no
appeal to (68). Explicit inequivalences (S8): at θ = 0, `ω(X) ≠ ω(Y)` with difference ∝ `(l₁²−l₂²)`;
at θ = 45°, `ω(M) ≠ ω(M′)`, `M′ = (π/L,−π/L)`; at generic θ both.

## M10.4 M7-b re-check `[A]` (Q1)

Case H: (a) `ω(θ+90°; l₁,l₂)(k) = ω(θ; l₂,l₁)(k)` exactly — material identity (30), no cell
symmetry needed; (b) `ω(θ+90°; l₁,l₂)(k) = ω(θ; l₁,l₂)(R₉₀k)` exactly — for Case C this needs the
cell to be C4-invariant (true for the square cell with a centred circular inclusion). `R₉₀`
maps Γ–X–M–Γ to Γ–Y–M′–Γ. **Test 5e must be formulated as (a) on the same path or (b) on the
rotated path**, never as "same path, same L". M7-b is discharged for Case H; for Case C it is
discharged conditional on the C4-invariant cell geometry (a TV6 geometry statement).

## M10.5 T4 reference role (T6) `[A]`

The closed forms of M10.2 are the Layer-3 analytic reference for Case H at interior k (M15-a T4).
They are k-even but **not** G-periodic, while the discrete Bloch problem is G-periodic (M9 [L11]);
the discrete bands are the *folded* continuum branches — fold before comparing (for P2.1/M15).

---

## M10.6 FLAGGED ITEM M10-a — the path (44) is the IBZ boundary only for AR = 1 `[A]`,`[S]`
### (recorded, NOT repaired; ruling required before M12 and M15)

**Finding.** Blueprint §3.3 calls Γ–X–M–Γ the irreducible Brillouin zone "for the square lattice".
That is correct for the *lattice* (C4v) and for the *operator* only when AR = 1. The paper's
novelty (D4, §6.4, §6.6) is precisely AR ≠ 1 with θ swept over 0°…90°: there the symmetry group
of the locked operator is C2v (θ = 0°, 45°, 90°) or {I, −I} (generic θ), the irreducible zone is
¼ or ½ of the BZ, and the path omits inequivalent legs (Γ–Y, Y–M, Γ–M′, …). Established
exactly in [S5]–[S8] from the locked formulation; no numerics involved.

**What is and is not affected.**
- Not affected: the path is a valid k-set for every (θ, AR); *partial* gaps "along one path"
  (§3.5) and the §6.4 headline (gap edge along Γ–X vs Γ–M) are well defined on it; M9, M15-a,
  the eigenproblem, tests 5a/5b/5d/5f/5g/5h.
- Affected: (i) the *complete-gap* definition "over the whole IBZ" (§3.5, eq. (49); M12) — a
  minimum/maximum taken over Γ–X–M–Γ alone is **not** the extremum over the irreducible zone for
  AR ≠ 1 and can over-report complete gaps; (ii) the design map §6.6 / Fig. 10–11 ("first complete
  gap width") and Table 5 ("complete/partial"); (iii) Fig. 2(b) caption; (iv) test 5e wording
  (M10.4); (v) test 5c (rotational invariance at AR = 1) is unaffected and in fact is the case
  where the path *is* the IBZ.

**Options (not chosen here).**
(a) Keep the path (44) for band plots and *partial* gaps; define *complete* gaps over the
    irreducible zone of M10.3 (half BZ for generic θ; quarter for θ ∈ {0°,45°,90°}) by an
    area sampling or an extended boundary path (e.g. Γ–X–M–Γ–Y–M′–Γ, or the full BZ boundary
    plus both diagonals) — amendment to §3.3/§3.5/(44)/(49) and to M12.
(b) Keep (44) literally and relabel complete gaps as "complete along Γ–X–M–Γ" (a path-restricted
    quantity, not an IBZ extremum) — weaker claim, must be stated in the manuscript.
(c) Restrict the complete-gap claims to the C2v-symmetric orientations θ ∈ {0°,45°,90°} with an
    enlarged path covering the quarter BZ, and report only partial gaps at generic θ.
Interacts with TV4 (k-sampling) and with Phase-5 production cost (42 analyses). **M10 does not
decide.**

---

## M10.7 Consistency table `[A]`

| Requirement | Where verified |
|---|---|
| M8 strong form (O1) | S1 (dispersion derived from it) |
| M8-a reduced boundary model | no boundary term enters Case H; periodic cell — unchanged |
| M9 phase rules / covariance | P6, T5 |
| anisotropic (26) | S1, S1b, S6 (only `k·L·k` breaks symmetry) |
| M15-a pair (T1/T2) | T1 (k-evenness), P6 (unimodular on path) |
| M15-a T3 | T5 (sign unobservable in Case H at q = 0 ⇒ T3 remains necessary) |
| M15-a T4 | T6 (fold before compare) |
| dimensions | S3, P2 |
| M7 ladder (27)–(30) | T3, T4 |
| M7-b | Q1 |

## M10.8 Checks (23, all PASSED)

P1–P6 path/sampling/phases; S1, S1b, S2, S3 dispersion and dimensions; S4–S9 symmetry group,
irreducible zone, path inequivalences; T1–T6 evenness, ladder, 1D reduction, covariance,
reference role; Q1 M7-b. Log `checks/m10_ibz_path.log`.

Failures encountered: none in the final run (development iterations: none recorded beyond the
first complete run).

## M10.9 Not done (deliberate)

TV4 not resolved; no k-point value; no M11 (non-dimensionalisation used only as `k̄ = kL/π`
consistency); no M12 observables; no blueprint edit; M10-a options not selected.
