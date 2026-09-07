# NOVELTY_MAP.md

What is new in this work relative to the cited literature (no claim beyond
what the manuscript and audits establish).

## Novel contributions

1. **First semi-analytical surface-wave treatment of a 2D-hexagonal
   PIEZOELECTRIC THERMOELASTIC quasicrystal half-space with three phason
   dynamic models side by side.** Existing QC surface-wave literature
   (zhang2023cryst, zhang2024amm, zhang2025zamm, zhang2021amss/acta,
   feng2024amm, ma2023zamp) covers 1D-hex QCs/PQCs, layered media, or
   isothermal elasticity; thermoelastic phason dynamics with Lord–Shulman
   relaxation in the half-space surface-wave setting is not treated there.
2. **Model ladder A/B/C (inertial / diffusive / telegraph phason dynamics)**
   implemented in one dispersion pencil with documented exact limits
   (gates 1.11e-9 / 3.27e-9) — agiasofitou2014 motivates the telegraph
   model but does not perform this comparative surface-wave analysis.
3. **Resolution-floor methodology.** A benchmarked relative-resolution
   floor ε_Δ/V ≈ 2.42e-4 converts "model differences are small" into a
   quantitative statement: Δ_BC is below the floor on 95/121 production
   points (71/121 as evidence at Ω* ≥ 0.31622776602) — a
   resolution-resolvable-region statement, not a physical identity claim.
4. **Systematic sensitivity triad** — phason friction D_w (61×61 map),
   thermal relaxation τ0, phason boundary condition (clamped vs free,
   ≤8.06e-6) — mapped against the resolution floor; no prior QC
   surface-wave paper reports this triad.
5. **Fully programmatic, checksummed reproduction chain** (solver → raw
   data → figures → manuscript) with a 22-check invariant gate including
   the Ω*=1000 branch identity.

## Explicitly NOT claimed

- No new physics beyond the cited constitutive/dynamical frameworks.
- No experimental validation; parameters are composite/partly surrogate
  (declared, §7.9 of manuscript).
- No FEM; no phase-transition interpretation of sub-floor differences.
- 2D-hex QC surface waves exist in the literature (isothermal/elastic);
  novelty is the piezoelectric-thermoelastic + phason-dynamics-model
  comparison + resolution-floor framing.
