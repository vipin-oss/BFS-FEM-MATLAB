# P12B — S7 steering θ-sweep extension and figure of merit M_s (provenance record)

**Phase:** P12B (branch `phase-1-symbolic`; `main` untouched; Blueprint v1.3 untouched)
**Date:** 2026-09-23
**Authority:** P12 post-P11D gate audit recommendation (b) + explicit user instruction
"Start P12B now" (this chat). Target: PCR7 → full PASS (steering figure of merit
defined, computed, published, pinned).
**Rule in force:** locked methodology only — no change to model, mesh, tolerances,
or definitions; evidence registry-first (every manuscript number generated from
`results/raw/p12b_s7_theta_sweep.json` by committed generators; nothing hand-entered).

---

## 1. Scope executed (exactly the audited P12B extension)

- θ sweep θ ∈ {0°, 15°, 30°, 45°, 60°, 75°, 90°} (the locked P5 grid,
  `master_params.theta_sweep_deg`) × AR ∈ {5, 10} — 14 configurations.
- Locked S7 definitions verbatim: Case-H single-cell assembly
  (`assemble_KM(hx=L, hy=L)`, volume-equivalent semi-axes from AR, l_iso = 0.20,
  ell2 = 0.04, λ = μ = ρ = L = 1.0 — all loaded from
  `results/raw/p5_production_raw.json::master_params`, cross-asserted equal to
  the P5 production driver), ring |k̄| = k_rad = 0.5 π/L, S7 sampling
  φ = linspace(0, 2π, 73) (5° steps), branch 0 (first acoustic branch),
  unsigned group-velocity deviation δ via `compute_group_velocity_2d`
  (central differences, h = 1e-4) — the unmodified locked P5 code path.
- **Pipeline-identity anchor:** the (AR=5, θ=45°) and (AR=10, θ=45°)
  configurations existed in the locked P5 evidence
  (`study_S7_ifc_steering`); the P12B run reproduces their δ_max to
  **rel diff = 0.0**. Recorded in the evidence JSON (`legacy_anchor_check`).

Cost: 0.6 s wall time (single-cell Case-H assembly; no mesh study — nothing
remotely comparable to the Case-C 5016 s runs; P12C untouched).

## 2. Figure-of-merit definition (as audited, locked conventions)

> φ*(θ, AR) = (argmax_φ δ(φ; θ, AR)) mod 90°, in degrees, on the locked ring;
> **M_s(AR) = φ*(90°, AR) − φ*(0°, AR)**.

Declared tie-break and post-processing (recorded verbatim in the evidence
`definitions` block): smallest representative among co-equal maxima (1e-12
relative); a 3-point parabolic refinement is stored separately
(`phi_star_refined_deg`) for transparency; the published FoM uses the discrete
locked-grid value.

## 3. Computed results (from the evidence — no estimates)

δ_max(θ) [deg] / φ*(θ) [deg] on the locked grid:

| θ | AR=5 δ_max | AR=5 φ* | AR=10 δ_max | AR=10 φ* |
|---|---|---|---|---|
| 0°  | 1.4248 | 45 | 2.8008 | 45 |
| 15° | 1.4425 | 30 | 2.8227 | 30 |
| 30° | 1.4303 | 15 | 2.8128 | 20 |
| 45° | 1.4135 | 0  | 2.7866 | 5  |
| 60° | 1.4303 | 75 | 2.8128 | 70 |
| 75° | 1.4425 | 60 | 2.8227 | 60 |
| 90° | 1.4248 | 45 | 2.8008 | 45 |

- **M_s(AR=5) = +0.0000°; M_s(AR=10) = +0.0000°** (φ*(90°) = φ*(0°) = 45.00°;
  parabolic-refined values identical to shown precision).
- δ_max spans [1.4135°, 1.4425°] (AR=5) and [2.7866°, 2.8227°] (AR=10):
  minima at θ = 45°, maxima at θ = 15° and 75°; relative spans 2.1 % / 1.3 %.
- The pinned §7.1 values (1.41° / 2.79° at θ = 45°, AR = 5 / 10) match the
  θ = 45° row exactly — full consistency with the pre-P12B manuscript.

**Verified field symmetries (max residuals over the whole sweep):**
- headless periodicity δ(φ+180°; θ) = δ(φ; θ): **≤ 8.6×10⁻⁷ deg** (worst case
  at δ ≈ 0 points; arccos rounding — reported honestly as < 10⁻⁶ deg, not 10⁻⁸);
- mirror co-symmetry δ(φ; θ) = δ(90° − φ; 90° − θ): **≤ 6.8×10⁻⁹ deg**;
- δ_max(θ) = δ_max(90° − θ): **≤ 2.0×10⁻⁹ deg**.
The θ = 90° field is the exact φ → 90° − φ mirror of the θ = 0° field, not its
pointwise equal (max direct deviation 0.031° / 0.211°) — this is WHY
φ*(90°) ≡ φ*(0°) (= 45°, on the mirror plane) and M_s = 0 is a symmetry
statement, not a triviality. Manuscript mechanism sentence ties the mirror law
to the L-tensor rotation–swap symmetry of §2 (L12(θ + 90°, l1, l2) =
−L12(θ, l2, l1)).

Physical statement published in §7/§9: orientation tuning repositions the
steering lobes as φ* ≈ (45° − θ) mod 90° (exact on the grid at AR = 5;
≤ 5° excursions at AR = 10) while the attainable deviation amplitude varies by
< 2.1 % — the steering axis is repositionable within the fundamental sector,
and M_s = 0 quantifies the exact mod-90° return of the principal axis.

## 4. Provenance chain (registry-first)

```
production/p12b_s7_theta_sweep.py      (locked solver imports; no redeclared constants)
  → results/raw/p12b_s7_theta_sweep.json   (immutable evidence; master_params + sha256,
      git commit, env, legacy anchor, symmetry diagnostics, definitions verbatim)
  → tables/gen/tab07_steering_sweep.py   → tables/out/tab07_steering_sweep.tex   (Table 7)
  → figures/gen/fig14_s7_steering_sweep.py → figures/out/fig14_s7_steering_sweep.{pdf,png} (Fig. 14)
  → latex/sections/sec07_steering.tex    (new subsection: definition eqs. (Ms_def), (Ms_value),
      quantitative sweep paragraph, Fig. 14 + Table 7)
  → latex/ms.tex                         (abstract clause: range + M_s = 0.0000° + mirror co-symmetry)
  → latex/sections/sec09_conclusions.tex (steering bullet: sweep ranges, axis law, M_s)
```

Guard tests: `verification/suite/test_p12b_steering_fom.py` (5 tests): locked
conventions + registry params; M_s definition/values; symmetries + legacy
anchor; manuscript/table integration (exact strings + table rows regenerated
from evidence); **live recompute** of φ*/M_s from the locked solver path
matching the stored evidence.

## 5. Color/evidence-presentation item (user requirement #0)

- Manuscript Figure 4 (`fig04_benchmark_validation.pdf`): already color-coded
  (navy B1 / crimson B3; tinted gap bands; labeled) — verified from rendered
  PNG.
- `audit/evidence/fig4c_overlay.png`: source raster kept **untouched grayscale**
  (fidelity); present calculation now color-coded by continuous dispersion
  segment (crimson/navy/green/orange, legend labels; point set unchanged —
  coloring is a continuity grouping of the same computed (k̄, ω̄) points), stop
  bands shaded, two-line banner (qualitative-comparison caveat + source-fidelity
  note). Regenerated via `p11d_regenerate_evidence.py`; B2 authoritative gaps
  reproduced identically on regen.

## 6. PCR/gate status claim (documentation; definitions unchanged)

- **PCR7 → PASS**: steering FoM M_s defined (locked S7 conventions), computed
  from evidence, published in §7/abstract/§9, pinned by a live-recompute guard
  test — matching the audited acceptance ("extending S7 to the missing angles
  costs ~5–15 min and closes it").
- PCR2/3/6/8: unchanged (green; P12A state). PCR1: NOT MET (unchanged).
- **G3: NOT MET (unchanged). G4: NOT MET (unchanged)** — no external anchor
  data appeared; no redefinitions. G1/G2 MET (suite green incl. new tests).
- Remaining blockers unchanged: G3/PCR1 external ≤2%; B2 l/l̄ ambiguity
  (author clarification); Case-C Δ_complete mesh convergence → **P12C**
  (separate authorization); P12D Layer-1 FE. P12B does not touch them.
