# eqs/
Symbolic equations, derivations, equation-generation scripts, symbolic verification and
equation audit records (SymPy, exact rational arithmetic). Maps to blueprint eq register (1)-(71), (A.1)-(A.6), (B.1)-(B.8).

## Phase-1 package: `phase1/`
Phase-1 symbolic formulation (modules M1–M17 of `paper9/plan/CALC_MASTER_PLAN.md` §A),
on branch `phase-1-symbolic`. Structure: `phase1/README.md` (rules),
`phase1/PHASE1_FORMULATION_PLAN.md` (module map + status), `phase1/derivations/`
(per-equation audit: provenance tags, assumptions, checks, units),
`phase1/scripts/` (deterministic SymPy derivation/verification scripts),
`phase1/checks/` (captured run logs), `phase1/PHASE1_MANIFEST.md` (commit/file hashes,
software versions, TV dependencies).

Milestone 1 (M1–M7, blueprint eqs (1)–(30)): 76 symbolic checks PASSED; see
`phase1/derivations/DERIVATION_M01_M07.md`. M8–M17 NOT STARTED.
Status labels used: DRAFT / IN PROGRESS / TO BE VERIFIED / PASSED / FAILED / LOCKED.
No numerical verification (5a–5i), no published-benchmark validation, no scientific
results are produced by this package.
