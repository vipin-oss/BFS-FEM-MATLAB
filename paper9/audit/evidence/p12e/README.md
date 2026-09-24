# P12E evidence bundle (audit trail — staged implementation, NOT installed in the repo)

| file | content |
|---|---|
| `pre_change_snapshot.json` / `snapshot_output.txt` | Part A snapshot: HEAD, env, protected hashes, tree hashes, P12E-absence check |
| `routeF_patch.diff` | the exact Route-F + C-1 patch applied to the **staged copy** of `p4b_5g_to_5i.py` (the repository copy is byte-identical to the original `b1c8d996…`) |
| `p12e_synthetic_discrimination.py` | Part D synthetic discrimination suite (runs against any module path) |
| `synthetic_discrimination_output.txt` | Part D result — ALL CHECKS: PASS |
| `mutation_harness.py` / `mutation_harness_output.txt` | Part H mutation matrix — 12/12 detected, control passes |
| `production_run1_stdout.txt`, `production_run1.json` | Part E controlled re-baseline run 1 (exit 1: P3 FAIL) |
| `production_run2_stdout.txt`, `production_run2.json` | Part I reproducibility run 2 (JSON identical to run 1 except `utc`) |
| `partI_and_band.py` / `partI_and_band_output.txt` | reproducibility comparison, P3 failure envelope, criterion on historical data |
| `certify32_fixed.py` / `_output.txt` | ARPACK convergence certification at the 5i k (tol 1e-12/1e-14/1e-15) |
| `discriminate.py` / `_output.txt` | control experiment at a different k (solver resolves 6.1e-12 with 6.5e-15 seed spread) |
| `verify_convergence.py`, `preflight_probe.py` (+outputs) | seed-variation and pre-flight feasibility probes |

**Nothing in this bundle is installed**: no repository scientific artifact was modified, no new
governing JSON was created, no manuscript/table/figure/plan change was made. The re-baseline was
stopped at the authorized P1–P4 gate (P3 FAIL).
