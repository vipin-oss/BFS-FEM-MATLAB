# PARAMETER_PROVENANCE.md

Single source of truth: `params.json` (root). Starred (nondimensional)
values are DERIVED from the dimensional set by the frozen
nondimensionalisation and must never be edited directly. The parameter set
is composite and partly surrogate — this is declared in the manuscript
(Section 7.9) and is part of the accepted baseline.

## Dimensional (SI) values and their provenance labels (from params.json)

| Parameter | Value | Provenance |
|---|---|---|
| C11, C12, C13, C33, C44, K1, K2, K3, R1, R2 | 200, 100, 100, 150, 50, 50, 20, 20, 10, 5 GPa | composite table (wang2015 = wang2020 = li2017 Table 1) |
| C66, K6, R6 | derived | frozen symmetry relations 2C66=C11−C12, K6=K1−K2−K3, 2R6=R1−R2 |
| ρ | 4180 kg/m³ | SURROGATE (declared) |
| ρ_w | 4180 kg/m³ | DECLARED identification ρ_w = ρ (no independent phason mass density in literature) |
| β1 | 1.798e6 | composite table |
| k11 | 6.0 W/(m K) | DECLARED choice; li2017 reports 5.3 — discrepancy genuine and unresolved (declared) |
| c_e | 500 J/(kg K) | SURROGATE (declared); nondimensionally c_e* = 1 exactly (absorbed into thermal-row normalisation) |
| T0 | 298 K | standard reference temperature |
| τ0 | 1e-13 s | DECLARED computational parameter (design sweep 1e-13…1e-11 s; production uses τ0* values) |
| D_w | 2.0833e18 | literature-derived: D_w = 1/C_w, C_w = 4.8e-19 m³ s/kg from chellappan2015 eq.(3)+p.8; mobility/friction distinction enforced |
| C_w | 4.8e-19 m³ s/kg | chellappan2015 |
| k0 (scale) | 2π×1e6 m⁻¹ | DECLARED nondimensionalisation scale (reference wavelength 1 µm); NEVER a working wavenumber |

## Frozen derived values (verification gates)

v0 = 6917.1446 m/s; D_w* = Ω_c = 11467.5; τ0* = 4.3462e-3; k11* = 2.6077e-3;
T0β1s = 2.3047e-3; starred elastic targets exactly {1, 0.5, 0.25} and phason
{0.25, 0.1, 0.1, 0.05}, coupling {0.05, 0.025, 0.0125} (see
`frozen_starred_targets` in params.json). Polynomial degree p = 10.

All of the above are re-checked at runtime by
`verification/verify_invariants.py`; any change stops the pipeline.
