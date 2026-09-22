# Phase 0 audit / change record (2026-09-22)

Scope: final Phase 0 consistency-fix pass on paper9/plan/CALC_MASTER_PLAN.md (v1.0 -> v1.1).
Authoritative sources used: locked Blueprint v1.2 (femcheck/blueprint/Paper9_Blueprint.tex,
outside this repository) and the repository contents. No blueprint file was modified.

## 1. Internal verification test count
Finding (from Blueprint v1.2): suite = EIGHT automated tests 5a-5h (S5.6, Table 4 register
"Eight rows", checklist "eight"); matrix row 5i = mesh-convergence/resolution-floor study
(S5.7, Fig 5, Table 6), "part of Layer 5, not a sixth layer". Layer 5 = nine verification
rows 5a-5i = eight-test suite + convergence study.
Action: CALC_MASTER_PLAN Section F note added (definitive wording); checklist item corrected.
5i RETAINED (blueprint genuinely contains it) and precisely documented. No "nine tests" claim anywhere.

## 2. G3 / G3b gate naming
Finding: Blueprint locks G1, G2, G3, G4; G3 = published-validation HARD gate (<=2%, 0.5%
classical). Plan v1.0 introduced "G3b" for Phase-5 completeness, colliding in appearance with G3.
Action: G3b renamed to G5 (plan-level Phase-5 completeness gate); gate terminology map added to
Section B listing blueprint-locked vs plan-level gates. G3 meaning untouched; no blueprint gate renamed.

## 3. Phase order 4A -> 3 -> 4B
Action: explicit execution order line added to Section B:
P0 -> P1 -> P2 -> P4A -> P3 -> P4B -> P5 -> P6 -> P7 -> P8 -> P9, with rationale (cheap solver
acceptance before expensive validation; mirrors blueprint G2-before-G3 order). Blueprint
validation framework unchanged.

## 4. Benchmark card mapping B1-B7
Action: mapping table added to Section E, verified against the Blueprint v1.2 validation matrix:
B1=row1/L1/SciRep2024 Fig2(a)/published/GATE; B2=row2a/L2/SciRep2024 Fig2(b)/published/GATE;
B3=row2b/L2/WRAM2023 Fig4(c)/published/GATE; B4=row2c/L2/WRAM2023 Fig3/published/optional;
B5=row3/L3/PB2009/analytical/mandatory non-gate; B6=row3b/L3/LWZ2016/analytical/mandatory non-gate;
B7=row4/L4/Mishra2026/published independent method/optional. Layer 5 rows carry no B-card.
No mapping invented; unextracted panel parameters remain in the TV register.

## 5. Blueprint residual (recorded, not edited)
Blueprint v1.2 schedule week-6 row still says "GATE G2 --- all 7 internal tests pass"
(v1.0 leftover; contradicted by S5.6/Table 4/checklist "eight"). Authoritative count = 8 (+5i).
Recommendation: editorial fix in a future blueprint revision (v1.3) with explicit user approval.

## Files changed in this pass
- paper9/plan/CALC_MASTER_PLAN.md (v1.0 -> v1.1)
- paper9/plan/README.md (status line)
- paper9/audit/phase0_change_record.md (this file, new)
No other repository files touched; legacy zips/docx untouched; no scientific content deleted.
