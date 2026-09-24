# P12I evidence bundle — independent verification of P12H

Audited commit: `dd42e81b946a9ae3bee84d09d90f7440f88559c8` (P12H); baseline `2225cdc…` (P12G).

| File | What it is |
|---|---|
| `rule_rfit_forensic.py` | Independent re-implementation of Rule R-fit (does **not** import `verification/suite/rule_rfit.py`); re-derives every subset, slope and CI from archived evidence, plus strictness/floor/independence probes |
| `rule_rfit_forensic_output.txt` | Its output: governing slope **and** CI bit-exact; TXT / Route-F / control-k subsets and slopes as recorded; 21-realization replay 0/21 admission |
| `suite_run1.txt` | Full suite with `-rs` (125 passed, 1 skipped) and the investigated skip reason |
| `suite_run2.txt` | Second full suite run (125 passed, 1 skipped) |
| `numerical_crosscheck_rerun.txt` | Re-run of the P12H numerical/float/manuscript/Blueprint cross-check (43/43) |

Non-repo working files used by the audit (hashes not pinned): figure renders under
`/home/user/p12i_logs/` (post-P12H and `2225cdc`-era generators) and the opt-in end-to-end run
(`P4B_B1_FULL_RERUN=1 pytest … -q` → 10 passed in 67.02 s, repo clean afterwards).

Run from the repository root, e.g. `python3 paper9/audit/evidence/p12i/rule_rfit_forensic.py`.
