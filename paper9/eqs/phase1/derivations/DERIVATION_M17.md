# DERIVATION M17 — Appendix B energy flux (blueprint (B.1)–(B.8))

Status: **checks PASSED (13/13)** · Script `scripts/m17_energy_flux.py` · Log `checks/m17_energy_flux.log`.
Independent of `m12_observables.py`. Locked: M8.7, M5, M6, M4 (26). Blueprint v1.3 not edited.
Register (lines 591–592): (B.1)–(B.4) balance/classical/double-stress/time-average;
(B.5)–(B.8) dimensions, `⟨S⟩/(⟨W⟩+⟨T⟩)=v_g`, numerical protocol.

**Discrepancy vs M12:** none. Independently derived `S_j` coincides with M12.2. Blueprint wording
“classical + double-stress” omits the micro-inertia slot; recorded, not amended.

## Mapping

| eq | content | type |
|---|---|---|
| **(B.1)** | `W = ½ σ:ε + ½ τ:η`, `T = ½ ρ (v·v + ℓ² v_{,j}·v_{,j})` | definition (M5/M6) |
| **(B.2)** | `∂_t(W+T) + ∂_j S_j = − v_i R_i` | identity, arbitrary fields |
| **(B.3)** | `S_j = −(σ_{ij}−τ_{ijk,k}) v_i − τ_{imj} v_{i,m} − ρ ℓ² ü_{i,j} v_i` | definition of flux (outward; Ė+div S=0 on-shell) |
| **(B.4)** | harmonic: `⟨ab⟩=½ Re(A conj B)` for `e^{-iωt}` | convention |
| **(B.5)** | `[W]=[T]=J/m³`, `[S]=W/m²` | dimensional check |
| **(B.6)** | on-shell `⟨S⟩/(⟨W⟩+⟨T⟩)=v_g` (energy velocity) | consequence |
| **(B.7)** | Case-H 1-D shear/extension: (B.6) exact | specialization / M12 cross-check |
| **(B.8)** | test 5h protocol; power `−S·n` = reduced-traction + double-traction + micro-inertia surface power | protocol; M8-a not re-derived |

## Independent algebra `[A]`

EOM residual `R_i = σ_{ij,j} − τ_{ijk,jk} − ρ(ü_i − ℓ² ü_{i,jj})`. Multiply by `v_i=ú_i`, product rule:

- `v_i σ_{ij,j} = ∂_j(σ_{ij} v_i) − σ:ε̇`
- `−v_i τ_{ijk,jk} = −∂_j(τ_{ijk,k} v_i) + ∂_j(τ_{imj} v_{i,m}) − τ:η̇`
- `ρ v·ü = ∂_t T_class`
- `−ρ ℓ² v_i ü_{i,jj} = −∂_j(ρ ℓ² v_i ü_{i,j}) + ∂_t T_micro`

Linear hyperelasticity: `Ẇ = σ:ε̇ + τ:η̇`. Hence (B.2)–(B.3). No volumetric source on-shell.
Sign: `S` is **outward** energy flux (`Ė + div S = 0`).

Micro-inertia flux `−ρ ℓ² ü_{i,j} v_i` is required (E5). Double-stress slots required (E3).

## Checks

1-D generic polynomial-trig shear (not an eigenwave): (B.2) exact.  
2-D polynomial-trig, `L=l₁² I`: (B.2) exact.  
Case-H 1-D shear and extension: `⟨W⟩=⟨T⟩`, `⟨S⟩/(⟨W⟩+⟨T⟩)=dω/dk` independently averaged.  
M12.2 index form recovered. Units (B.5). Positivity from M6, no new hypothesis.

## TV

TV4, TV6, TV7, TV14, TV15, TV17, TV18 OPEN. (B.8) numerical 5h not executed (Phase 4).
