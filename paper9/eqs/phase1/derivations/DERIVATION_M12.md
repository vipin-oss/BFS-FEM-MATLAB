# DERIVATION M12 — Observables (blueprint §3.5, eqs. (48)–(52)) — PARTIAL under locked v1.3

Status: **PASS for the executable scope (22/22 checks); (49) sampling protocol BLOCKED (no authorisation
for the M10-a amendment found in the repository).** Script `scripts/m12_observables.py` · Log
`checks/m12_observables.log`.

## M12.0 Authorisation audit `[A]`

Searched `paper9/` for "authoris/authoriz/v1.4": the only authorisations on record are the Phase-0 editorial
v1.2→v1.3 revision (`audit/phase0_change_record.md` item 6, `plan/blueprint/PROVENANCE.md`). The M10-a
amendment (`AUDIT_M10a_ibz_scope.md` §7) and the M15-a amendment (`AUDIT_M15a_hermiticity_test.md` §7)
are recorded as *proposed, NOT applied, authorisation pending*. **No authorisation exists ⇒ Blueprint v1.3
untouched (sha `ca71b91a…`).** M12 is therefore audited against the literal v1.3 text.

## M12.1 Exact M12 scope (repository text) `[L]`

§3.5 (line 381): band `ω̄_n(k)` (48); band gap `Δω̄_g = ω̄_{n+1}^{min} − ω̄_n^{max}` "over the whole IBZ
(complete) or along one path (partial)", mid-frequency, aspect ratio, normalised width `Δω̄/ω̄_mid`,
orientation sensitivity `S_θ = max|∂Δω̄/∂θ|/maxΔω̄` (49); "gaps exist only with periodic contrast (Case C)";
phase velocity (50); group velocity `v_g = ∇_k ω` (51); time-averaged energy flux from the energy balance
(classical + double-stress, dimensional check) with `v_g = ⟨S⟩/⟨W+T⟩` verified numerically in §7.3 (52);
plan row M12 (line 47), F11 "identity matches Appendix B result"; reviewer box (386–388) "extra double-stress
Poynting term". Dependencies: M9, M11 (plan); M17 (B.1)–(B.8) shares the flux derivation.

### Classification

| component | status |
|---|---|
| (48) band-function properties | derivable now — done |
| (49) gap **definitions**, monotonicity, scale invariances | derivable now — done |
| (49) sampling protocol realising "whole IBZ" for AR≠1 | **blocked — missing authorisation (M10-a amendment items 1–2)** |
| (49) any gap value, complete/partial classification, S_θ values | later numerical production (Phase 5); also TV4, TV6 |
| (49) S_θ angle unit / difference scheme | ambiguity → **TV16** |
| (50) phase velocity structure | derivable now — done; exact manuscript definition stays **TV15** |
| (51) group velocity, deviation angle | derivable now — done |
| (52) energy balance, flux, time average, identity | derivable now — **done exactly** (also discharges the symbolic part of M17/F11; M17 record itself not written) |
| barred reporting of all of the above | done via M11; reference μ, ρ, L for Case C stays **TV14** |

## M12.2 (48) Band functions `[A]` (B1–B5)

With the M15-a pair `K̄ᴴ = K̄`, `K̄(−k) = conj K̄(k)` and `M̄ = M̄ᴴ > 0`: eigenvalues real (B1); `K̄(k+G) = K̄(k)`
for `G ∈ (2π/L)ℤ²` because `e^{iG·a_α} = 1` (M9 phases) ⇒ bands are functions on the torus (B2); spectrum
even in k (B3; the invalid `K̄(k) = K̄(−k)ᴴ` is not used). Definition adopted (literal §3.5): `ω̄_n` = n-th
smallest eigenvalue, multiplicity counted — continuous on the torus, so the extrema in (49) exist; at
crossings the sorted labels are continuous but not smooth (MAC continuation of §4.6 is a tracking device,
not part of the definition). Case H has no crossing: `ω_L/ω_T = √((λ+2μ)/μ)` constant (B4). Barred form =
M11 [D2]/[D4] (B5).

## M12.3 (49) Gap definitions `[A]` (G1–G6) — definitions only, no values

For a compact k-set `S`: `Δ_g[S] := min_S ω̄_{n+1} − max_S ω̄_n`. Three instances, to be used verbatim:
- **directional / partial** — `S` = one leg (Γ–X, Γ–M, …) — §3.5 "along one path";
- **path gap** — `S` = Γ–X–M–Γ;
- **complete** — `S` = irreducible zone of the *actual* symmetry group (M10-a), equivalently the full BZ
  (G2: symmetry + periodicity make the two extrema equal).

Monotonicity `S₁ ⊂ S₂ ⇒ Δ[S₁] ≥ Δ[S₂]` verified on nested BZ-boundary sets (G1); the path is a strict
subset of the zone boundary for AR≠1 and its minimum is strictly larger in the exact Case-H model (G3) ⇒
**no complete gap may be claimed from Γ–X–M–Γ; the path gap is an upper bound.** Under v1.3 the complete
gap has a correct *definition* but no locked *sampling*; that is the pending amendment — not executed.
Width/mid/normalised width: `Δ/ω̄_mid` is ω₀-scale-invariant; `Δ`, `ω̄_mid` scale as 1/ω₀ (G4) — hence
TV14 (reference μ, ρ, L) affects `Δ`, `ω̄_mid`, all `ω̄` but not `Δ/ω̄_mid`. `S_θ` is scale-invariant but its
value depends on the angle unit (factor 180/π) and on the finite-difference scheme on the 7-point θ grid
(G5) → **TV16 (new)**. Case H: no gap (monotone branches, folding gives boundary degeneracies only) (G6),
consistent with the §3.5 statement.

## M12.4 (50)–(51) Velocities `[A]` (P1–P2, V1–V4)

- Phase velocity is branch- and direction-dependent: `v_{p,n}(k) = ω_n(k)/|k|`, vector `v_p k̂`; anisotropy
  enters via `k̂·L·k̂ = l₁²cos²(φ−θ) + l₂²sin²(φ−θ)` (P1). A scalar `k` alone is insufficient for Case C
  → the manuscript definition of `v̄` remains **TV15** (no choice made). Units m/s; `v̄_p = ω̄/(πk̄)`; classical
  limits 1 and √(λ/μ+2) (P2).
- `v_g = ∇_k ω`: odd in k, covariant `v_g(Qk) = Q v_g(k)` for Q in the M10-a group (V1). Polar identities
  `k̂·v_g = ∂ω/∂|k|`, `k̂×v_g = |k|⁻¹∂ω/∂φ` (V2–V3): deviation angle δ vanishes identically for AR=1 and is
  non-zero for l₁≠l₂ — δ is a pure anisotropy observable. Barred: `v_g = √(μ/ρ)π⁻¹∇_k̄ω̄`, δ scale-invariant
  (V4). Note for §7.2: "central differences on the band surface" require the 2-D k-grid (same grid as the
  blocked (49) protocol; grid size is part of TV4).

## M12.5 (52) Energy balance and flux — derived `[A]` (F1–F5)

Locked inputs: `σ_ij = C_ijpq ε_pq`, `τ_ijk = (1/10)L_kn C_ijpq η_pqn` (M4 (26)), `W = ½σε + ½τη` (M6, C4),
`T = ½ρ(u̇_i u̇_i + ℓ² u̇_i,j u̇_i,j)` (M5), residual `R_i = σ_ij,j − τ_ijk,jk − ρ(ü_i − ℓ²ü_i,jj)` (M8.5).

Derivation: `Ẇ = σ_ij ε̇_ij + τ_ijk η̇_ijk` (verified), integrate by parts twice on the τ term and once on the
micro-inertia term:

```
(M12.1)  ∂(W+T)/∂t + ∂S_j/∂x_j = − u̇_i R_i          (identity for ARBITRARY fields, verified exactly, F1)
(M12.2)  S_j = −[ (σ_ij − τ_ijk,k) u̇_i  +  τ_imj u̇_i,m  +  ρℓ² ü_i,j u̇_i ]
```

On solutions (R = 0): `∂(W+T)/∂t + div S = 0`. Three flux contributions: classical `−σ_ij u̇_i`; the
**double-stress terms** `+τ_ijk,k u̇_i − τ_imj u̇_i,m` (the extra Poynting term of the reviewer box; note
the total-stress combination `Σ_ij = σ_ij − τ_ijk,k` of M8.6 appears naturally); and a **micro-inertia
flux** `−ρℓ² ü_i,j u̇_i`, absent from the blueprint wording "classical + double-stress" — dropping either
non-classical term breaks the identity (F2). Units: every term W m⁻²; `⟨S⟩/⟨W+T⟩` in m s⁻¹ (F3).

Time average on the locked Case-H transverse plane wave `u = A a_T cos(k·x − ωt)`, generic (θ, l₁, l₂, ℓ, k):

```
(M12.3)  ⟨S⟩ / ⟨W+T⟩ = ∇_k ω_T      exactly, both components          (F4)
(M12.4)  ⟨T⟩ = ⟨W⟩ on-shell;  ⟨W_g⟩/⟨W⟩ = (k·L·k/10)/(1 + k·L·k/10);  ⟨T_g⟩/⟨T⟩ = ℓ²|k|²/(1 + ℓ²|k|²)   (F5)
```

(M12.3) is the symbolic content of plan F11 and of test 5h; the numerical verification protocol (B.8) is
Phase 4. Sign/convention: fields real, `e^{i(k·x−ωt)}` real part; the sign of S is fixed by (M12.1) (energy
flows along +v_g), no wrong-sign variant satisfies F1/F4.

## M12.6 Hidden assumptions surfaced `[S]`

| id | item |
|---|---|
| blocked (auth.) | (49) "over the whole IBZ" has no v1.3 sampling protocol valid for AR≠1; M10-a amendment items 1–2 required |
| TV4 | N_seg (path) and N_k (2-D grid for complete gaps, IFCs, central-difference v_g) — not guessed |
| TV6 / TV14 | reference phase μ, ρ, L for ω₀ and v̄ in Case C — affects Δ, ω̄_mid, all ω̄; not Δ/ω̄_mid, δ, S_θ |
| TV15 | v̄ per branch and direction; scalar k insufficient (P1) |
| **TV16 (new)** | S_θ: angle unit (rad⁻¹ vs deg⁻¹) and difference scheme on the θ grid; also whether Δ in S_θ is the complete or a directional gap (follows the (49) ruling) |
| notation | blueprint (52) text says "classical + double-stress"; the derived flux also carries a micro-inertia term (M12.2) — Appendix B wording must include it (no model change; record for M17 and the pending amendment list) |
| bar notation | (45)–(47) vs (66)–(68) clash recorded in M11; unchanged |

## M12.7 Proposed amendment additions (NOT applied)

Add to the M10-a v1.4 proposal: (52)/App. B wording "classical + double-stress + micro-inertia flux
terms, eq. (M12.2)"; (49) explicit three-way gap taxonomy (already item 2 of the M10-a proposal); S_θ unit
and scheme (TV16) once decided.
