# P12J evidence bundle — closure of the P12I corrections C1/C2/C3

Audited baseline: `1c6b2e3e793ab7a9e60bef09c347e5f91bc748fb` (P12I).

| File | What it is |
|---|---|
| `final_verification_p12j.py` | P12J copy of the P12H-era numerical/float/manuscript/Blueprint cross-check. One assertion anchor was extended because C1 reworded the v1.4 clause it quoted; the check's intent (the rule text must be measurement-only) is unchanged and the added form is stricter. The P12H-era script itself was not modified (`sha256 e5ae5ee0604a6e45…`). |
| `final_verification_p12j_output.txt` | Its output: 43/43 checks passed (four edited blocks vs v1.3, floor present, forbidden-claim sweep clean). |
| `suite_run1.txt` / `suite_run2.txt` | Full suite twice: **126 passed, 1 skipped** (7.34 s / 6.66 s). The +1 over P12I's 125 is the new P12J traceability guard. The single skip remains the pre-existing opt-in rerun, executed separately (`P4B_B1_FULL_RERUN=1` → 10 passed, 72.01 s) and deliberately kept out of the normal-suite count. |

Figure check: `figures/out/fig05_mesh_convergence.pdf` regenerated from the amended generator and
inspected visually — both panel titles clear, value labels inside the tall bars, panel-(b) legend in
the free upper-right corner; plotted data, fitted/excluded classification, regression line, axes,
limits and mesh values unchanged.
