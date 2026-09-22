# eqs/phase1/ — Phase-1 symbolic formulation package

Purpose: reproduce the complete Phase-1 mathematical/symbolic formulation (modules M1–M17
of `paper9/plan/CALC_MASTER_PLAN.md` §A) from Blueprint v1.3 (`paper9/plan/blueprint/`).

Layout (deterministic naming; every artifact states purpose + provenance + units):
- `PHASE1_FORMULATION_PLAN.md` — module map M1–M17 -> scripts/equations/status.
- `derivations/` — narrative derivations with per-equation audit ([C]/[A]/[S] tags,
  assumptions, index/sign/dimension/symmetry checks, blueprint equation numbers).
- `scripts/` — SymPy derivation/verification scripts (exact rational arithmetic where
  possible). Run: `python3 scripts/<name>.py` from this directory. Deterministic output.
- `checks/` — captured stdout logs of script runs (generated, never hand-edited).
- `PHASE1_MANIFEST.md` — commit hashes, file hashes, software versions, TV dependencies.

Rules for this phase (user-locked): symbolic/formulation work only; no numerical
parameters invented; no TV item resolved by guessing; no benchmark validation (Phase 3),
no acceptance tests 5a–5h (Phase 4A), no final scientific results; blueprint notation
preserved unless a documented correction is mathematically necessary; ambiguities are
recorded as unresolved, never silently decided.

Status: IN PROGRESS (Phase 1). Phase 0 is LOCKED (main @ 175ea9e).
