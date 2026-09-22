# AUDIT M10-a — scope of the path Γ–X–M–Γ (blueprint (44)) as "the IBZ boundary"

Status: **RESOLVED — ruling (a)** (blueprint amendment required, **NOT applied**; see §7).
Script: `scripts/audit_m10a_ibz_scope.py` · Log: `checks/audit_m10a_ibz_scope.log` · 26 checks, 26 PASS.
Inputs (read from the repository, not from the M10 summary): Blueprint v1.3 lines 263–269 (claims table),
328 (§1.3), 379 (§3.3), 381 (§3.5), 385 (Fig. 2 plan), 404 (§4.6), 485–489 (§6.3–6.7), 500–502 (§7.1–7.3),
576/579 (register (44)/(49)), 615–625 (figure list), 658 (Table 5 spec), 1062–1064 (summary box);
`DERIVATION_M10.md` §M10.3/§M10.6; `DERIVATION_M09*.md`; `AUDIT_M15a_hermiticity_test.md`;
`CALC_MASTER_PLAN.md` rows M10/M12, TV4 (line 359); `PHASE1_MANIFEST.md`; `traceability_matrix.csv`.
Tags: `[A]` derived here, `[L]` locked earlier, `[S]` still to be specified.

---

## 1. Independent re-derivation of the symmetry / IBZ argument `[A]` (G1–G4, Z1–Z9)

**Objects.**
- Lattice: square, a₁ = L e₁, a₂ = L e₂; BZ = [−π/L, π/L]²; lattice point group C4v (8 elements, all map
  the BZ onto itself, G1).
- Material: locked length tensor (M2, (6)) L(θ) = Rᵀ diag(l₁², l₂²) R with L₁₂ = (l₁²−l₂²) sinθ cosθ,
  L₁₁−L₂₂ = (l₁²−l₂²) cos2θ (G4).
- Spectrum (Case H, from M10 [S2], itself derived from (O1)+(26)+M9):
  ω²_{T,L} = c²|k|²(1 + k·L·k/10)/(1 + ℓ²|k|²). Only `k·L·k` is not O(2)-invariant.

**Criterion (proved independently).** For orthogonal Q: ω(Qk) = ω(k) ∀k ⇔ k·(QᵀLQ)·k = k·L·k ∀k ⇔
QᵀLQ = L ⇔ QLQᵀ = L. Hence the *material point group* is Stab_{O(2)}(L); the symmetry group of the
Bloch problem is G = Stab(L) ∩ C4v (the lattice must also be respected; for Case C the inclusion must
be G-invariant too — a centred circular inclusion is C4v-invariant, so it never lowers G further).

**Result (G2, G3), verified by exact spectral invariance for each of the 8 elements:**

| case | G | \|G\| | irreducible zone (fundamental domain of G on the BZ torus) | area |
|---|---|---|---|---|
| AR = 1 (l₁ = l₂), any θ | C4v | 8 | triangle Γ–X–M | \|BZ\|/8 |
| θ = 0°, 90°, AR ≠ 1 | C2v = {I, −I, σ_x, σ_y} | 4 | quarter square [0,π/L]² | \|BZ\|/4 |
| θ = 45°, AR ≠ 1 | C2v′ = {I, −I, σ_d, σ_d′} | 4 | wedge \|k₂\| ≤ k₁ ≤ π/L | \|BZ\|/4 |
| generic θ (sin4θ ≠ 0), AR ≠ 1 | C2 = {I, −I} | 2 | half BZ [0,π/L]×[−π/L,π/L] | \|BZ\|/2 |

Inversion −I is always in G (k-evenness = spectral content of the M15-a pair K̄ᴴ = K̄, K̄(−k) = conj K̄(k);
no appeal to the invalid (68)). Each listed domain was verified to be a fundamental domain by an
orbit-cover test on a 17×17 rational BZ grid, and the triangle was verified **not** to cover for
C2v, C2v′, C2 (Z9). Torus care: M′ = (π/L, −π/L) ≡ M mod reciprocal lattice, whereas Y ≢ X (Z3); the
explicit non-equivalent witnesses are Y and interior points q₁ = (π/4L, π/2L), q₂ = (π/2L, −π/4L)
(Z4–Z7).

## 2. Can "Γ–X–M–Γ is the IBZ boundary" be retained globally? `[A]` (Z2, Z8) — **NO**

Necessary condition for the triangle to be a fundamental domain: |G|·area(triangle) = |BZ|. This holds
iff |G| = 8 iff AR = 1 (or l₁ = l₂). For AR ≠ 1 the triangle covers only ½ (C2v) or ¼ (C2) of the
required area, and Y (θ = 0°/90°, generic θ) or the k₂ < 0 wedge (θ = 45°) are not reachable from it.
The statement is therefore **false for the paper's own novelty regime** (AR = 5, θ swept 0°…90°,
§6.4; 42-point (θ, AR) map, §6.6) and cannot be retained or "softened" into a global statement.
What *is* true globally: the path lies in the closed BZ for all (θ, AR) and is a valid dispersion path
(R2).

## 3. Downstream blueprint locations affected (actual text) `[A]`

| location (v1.3 line) | text | impact |
|---|---|---|
| claims table row 4 (263) | "Hermitian reduced eigenproblem over the irreducible Brillouin zone" | wording OK only if the IBZ is that of the actual G; must not be equated with Γ–X–M–Γ |
| row 6 (265) | "first **complete** gap opens along Γ–X at θ = 0° and migrates to Γ–M" | internally inconsistent: a gap "along Γ–X" is *partial/directional*; "complete" requires the zone extremum. Reword (see §7) |
| §1.3 (328) | "irreducible Brillouin zone, complete vs. partial gaps" | fine; the paper must then honour the distinction |
| **§3.3 (379), (44) (576)** | "Irreducible Brillouin zone for the square lattice: Γ→X→M→Γ" | correct for the lattice / AR = 1 only; needs the G-dependent statement of §1 |
| **§3.5 (381), (49) (579)** | "Δω̄_g … over the whole IBZ (complete) or along one path (partial)" | definition is right; **the sampling that realises "whole IBZ" is missing** and, for AR ≠ 1, cannot be the path |
| Fig. 2 (385, 615) | "IBZ with Γ-X-M-Γ path" | caption must say "lattice IBZ (AR = 1); irreducible zone for AR ≠ 1 shown as quarter/half BZ" |
| §4.6 (404) | "branch tracking along the IBZ path by MAC" | unaffected (path-based tracking is still needed for Fig. 6–8) |
| §6.3 (485) | "Case C bands along Γ-X-M-Γ; first three complete and partial gaps" | complete gaps must come from the zone sampling, partial ones from the path |
| §6.4 (486), Fig. 8 (621) | orientation sweep; "gap edge along Γ–X vs θ; same along Γ–M" | **unaffected** — these are path/directional quantities. Headline survives as *directional* migration |
| **§6.6 (488), Fig. 10** | "first complete gap width, 42 points" | requires zone sampling at each of 42 (θ, AR) points |
| **§6.7 (489), Fig. 11, Table 5 (658)** | "complete-vs-partial regime classification", column "type (complete/partial)" | classification only meaningful with zone-based complete gaps |
| §7.1–7.2 (500–501) | iso-frequency contours; v_g = ∇_k ω by central differences "on the band surface" | already require a **2-D k-grid**: the zone sampling of option (a) is *not* new cost; it is the same data |
| summary box (1062–1064) | "Hermitian reduced eigenproblem over Γ-X-M-Γ"; "migrates the stop band from Γ–X to Γ–M" | first phrase: replace by "over the irreducible zone (path for band diagrams)"; second is directional — fine with the reworded row 6 |
| Table 1 column (654, 947) | "partial gap / complete gap / IFC" | literature comparison must use the same distinction |
| test 5e (plan) | 90° symmetry | must be phrased as in M10 §M10.4 (same path with l₁↔l₂, or rotated path Γ–Y–M′–Γ) |
| test 5c | rotational invariance at AR = 1 | unaffected (path *is* the IBZ boundary there) |

Blueprint occurrences of "irreducible"/"IBZ": lines 263, 328, 379, 385, 404, 576, 615 — all listed above.

## 4. Evaluation of options against the actual design `[A]` (O1, O2)

| requirement (locked text) | (a) zone sampling for complete gaps | (b) path-restricted relabel | (c) restrict to C2v orientations |
|---|---|---|---|
| §6.4 sweep θ = 0…90° step 15° at AR = 5 (headline) | ✔ | ✔ | ✘ (drops 15°, 30°, 60°, 75° from complete-gap statements; sweep loses its map) |
| §6.6 42-point *complete*-gap design map | ✔ | ✘ (quantity is no longer a complete gap; map would be mislabelled) | ✘ (only 3 of 7 θ values) |
| §3.5/(49) "over the whole IBZ" | ✔ | ✘ (needs redefinition of the observable) | ✔ |
| §6.7 / Table 5 complete-vs-partial classification | ✔ | ✘ (no genuine complete class) | ✘ (incomplete map) |
| §7.1–7.2 already need band surfaces on a 2-D grid | ✔ (same data) | ✔ | ✔ |
| no change to the physical model | ✔ | ✔ | ✔ |

(b) preserves the literal (44) but demotes the paper's central quantitative claim (Fig. 10–11, Table 5,
claims rows 6 and 10) to a path-restricted quantity that reviewers in phononics will not accept as a
"complete gap" — and it would leave the manuscript over-reporting complete gaps (E1–E3 show the path
extremum is only an upper bound). (c) deletes the orientation sweep's interior points, i.e. the novelty.
(a) is the only option under which every locked statement remains true; its cost is a 2-D k-grid per
(θ, AR) point that §7.1–7.2 require anyway. **Ruling: (a).** Scientific model unchanged (O2).

## 5. Three distinct notions (must be used consistently from M12 on) `[A]`

1. **Gap along Γ–X–M–Γ** (path gap): min over the path of band n+1 minus max over the path of band n.
   Well defined for every (θ, AR); equals the complete gap **only** when the path is the IBZ boundary
   *and* all band extrema lie on that boundary (the latter is a heuristic, not a theorem).
2. **Directional / partial gap** (§3.5 "along one path"): the same on a single leg (e.g. Γ–X, Γ–M).
   This is what §6.4 / Fig. 8(b,c) and claims row 6 actually measure.
3. **Complete gap** (§3.5/(49) "over the whole IBZ"): min/max over the irreducible zone of the actual
   G (equivalently over the full BZ, by symmetry). Subset inequalities (E3): Δ_path ≥ Δ_complete, with
   strict inequality possible (E2: θ = 0, AR = 3 exact-rational example, band minimum at Y, off the path;
   E4: the discrepancy vanishes at AR = 1).

## 6. Sampling mathematically required for a complete-gap claim `[A]` (R1) and TV4 `[S]` (R3)

| case | minimal domain to sample | remark |
|---|---|---|
| AR = 1 | triangle Γ–X–M (area, or boundary path as heuristic) | path (44) is the boundary |
| θ ∈ {0°, 90°}, AR ≠ 1 | quarter square [0, π/L]² | boundary heuristic: Γ–X–M–Y–Γ (+ diagonal Γ–M if desired) |
| θ = 45°, AR ≠ 1 | wedge \|k₂\| ≤ k₁ ≤ π/L | boundary heuristic: Γ–M–X–M′–Γ |
| generic θ | half BZ [0, π/L]×[−π/L, π/L] | boundary heuristic: Γ–X–M–Y–Γ–Y′–M′–X–Γ … ; area grid recommended |

A uniform half-BZ grid is valid for *all* cases (superset), which is the simplest protocol for the
42-point map and is exactly the grid §7.1–7.2 need for IFCs and ∇_k ω.

**TV4 stays open.** The blueprint specifies neither N_seg (path) nor a zone grid. After M10-a TV4 must
eventually fix **two** resolution parameters: (i) N_seg per path segment for band diagrams/partial gaps,
(ii) the 2-D zone grid N_k × N_k (or equivalent) for complete gaps, IFCs and central-difference v_g,
both justified by the resolution-floor study 5i (mesh + k-refinement) — nothing is chosen here.

## 7. Proposed Blueprint v1.3 → v1.4 amendment (NOT APPLIED; authorisation required) `[S]`

Nature: **terminology + sampling protocol only; no change to the scientific model, the operator,
the eigenproblem, or any of (1)–(43), (45)–(68).**

1. §3.3 / (44) (line 379): "Irreducible Brillouin zone of the square lattice (C4v): Γ(0,0)→X(π/L,0)→
   M(π/L,π/L)→Γ, used for band diagrams and partial (directional) gaps at all (θ, AR). For AR ≠ 1 the
   symmetry group of the operator reduces to C2v (θ ∈ {0°,45°,90°}) or C2 = {I,−I} (generic θ) and the
   irreducible zone is one quarter or one half of the BZ; complete gaps are evaluated on a uniform grid
   over the half BZ [0,π/L]×[−π/L,π/L] (valid for all cases). Path resolution N_seg and grid resolution
   N_k: TV4."
2. §3.5 / (49) (line 381): after "over the whole IBZ (complete)" add "(irreducible zone of the actual
   symmetry group, §3.3, sampled on the 2-D grid)"; after "along one path (partial)" add "(directional
   gap; along Γ–X–M–Γ it is called the *path gap* and is an upper bound of the complete gap)".
3. Claims row 6 (line 265) and summary box (1064): "the first **directional** gap along Γ–X at θ = 0°
   migrates to Γ–M as θ → 90°; complete-gap width mapped on (θ, AR)".
4. Summary box (1062): "Hermitian reduced eigenproblem over the irreducible zone (Γ-X-M-Γ for band
   diagrams; 2-D k-grid for complete gaps and IFCs)".
5. Fig. 2 (385, 615): panel (b) "BZ with Γ-X-M-Γ path and the irreducible zones for C4v, C2v, C2".
6. §6.3, §6.6, §6.7, Table 5 (485, 488, 489, 658): add "complete gaps from the 2-D zone grid, partial
   gaps from the path"; Table 5 column "type" gets the three-way label {complete, path, directional}.
7. Verification 5e (plan): "ω(θ+90°; l₁,l₂) on Γ–X–M–Γ equals ω(θ; l₂,l₁) on the same path, or
   ω(θ; l₁,l₂) on Γ–Y–M′–Γ" (from M10 §M10.4).
8. Traceability: rows (44), (49), Fig. 2, Fig. 10–11, Table 5, TV4 updated accordingly.

## 8. Downstream consequences for M11 onward (not implemented) `[A]`

- **M11 (non-dimensionalisation (45)–(47)) — can proceed now.** It depends on M9 only; no k-sampling
  or gap definition enters. No further ruling needed for M11.
- **M12 (observables (48)–(52)) — blocked on authorisation of amendment items 1–2** (definition of the
  complete gap over the zone grid; three-way gap taxonomy; S_θ and normalised width then defined on the
  zone-based complete gap). Phase velocity/v_g/energy flux parts of M12 are unaffected.
- **M15 (Bloch reduction)** — unaffected mathematically (M15-a pair already gives ω(−k) = ω(k)); its
  driver must accept arbitrary k in the half BZ, not only path k.
- **Phase 5 production**: per (θ, AR) point, one path run + one zone-grid run (the latter shared with
  §7.1–7.2); cost change is bounded by the IFC grid already planned.
- **Tests**: 5c unchanged; 5e rephrased (item 7); a new consistency test is advisable — at AR = 1 the
  zone-grid complete gap must equal the path gap within ε_Δ (E4).
- **TV4**: two parameters (§6), remains `[S]`.

## 9. What was NOT changed

M1–M10 equations and scripts; Blueprint v1.3 (sha unchanged); the M15-a ruling; N_seg/N_k (TV4).
The path (44) is retained as the primary dispersion figure for all (θ, AR) (R2).
