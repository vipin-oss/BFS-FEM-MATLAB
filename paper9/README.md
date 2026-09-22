# Paper 9 - Direction-dependent band gaps in 2D anisotropic strain-gradient elastic media

Bloch-Floquet C1 finite-element study of Mindlin Form-II strain-gradient elasticity with an
anisotropic ellipsoidal characteristic-length tensor and micro-inertia. Primary target:
Int. J. Mechanical Sciences (Q1). Governing specification: `plan/CALC_MASTER_PLAN.md` and the
locked blueprint (v1.2, maintained outside this repository during Phase 0).

## Scientific scope (locked)
Dynamics + periodicity + micro-inertia on the existing constitutive family. Explicitly
excluded: fractional/memory models, thermal coupling, piezoelectricity, flexoelectricity,
functionally graded materials, geometric nonlinearity, 3D, damping.

## Repository structure
plan/ eqs/ params/ bench/ analytic/ solver/ validation/ verification/ production/
results/{raw,processed} figures/{gen,out} tables/{gen,out} latex/ bib/ audit/ release/
(see each folder README for its purpose).

## Current status (2026-09-22)
- Phase 0: calculation master plan DRAFT, awaiting user lock. Directory structure created.
- Phases 1-9: NOT STARTED.
- Validation status: NOT STARTED (no benchmark run exists; no validation claim is made).
- Verification status: NOT STARTED.
- Release status: EMPTY (no release candidates).

## Reproduction
Every computational run records a manifest (run id, git commit, parameter snapshot with
provenance tags, library versions, output hashes) under audit/. Figures and tables are
regenerated only by version-controlled scripts from results/processed/.

## Working rules
Sequential phases with lock gates (G1, G1b, G2a, G3, G2, G3b, G-F, G-B, G4); published-paper
validation (Layers 1, 2a, 2b at <=2%) is a hard submission gate and must appear in the final
manuscript; raw data is never edited; failed runs are kept as audit trail.
