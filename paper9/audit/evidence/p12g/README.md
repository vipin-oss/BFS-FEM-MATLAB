# P12G evidence bundle (design freeze only)

| file | content |
|---|---|
| `rfit_freeze.py` | the frozen Rule R-fit definition (constants F=3, SPREAD_FLOOR=1e-15, seeds 20260924/7, tol 1e-14, threads=1, meshes 4/8/16/32) + Part B adversarial circularity audit + Part C application to four archived datasets + the F-robustness window computation |
| `rfit_freeze_output.txt` | its output (rule text, 10 adversarial cases, 4 dataset applications, robustness window) |

Spread inputs are read from `audit/evidence/p12e/*` and `audit/evidence/p4b_b1/repro_realizations_summary.json`,
and the script asserts that every 5i-k and control-k spread value appears verbatim in those archived
outputs. No solver was run; no production file, manuscript, plan or Blueprint was modified.

Adversarial cases B3/B4 were located by a declared seeded search (400k random cases to establish that
SSE cannot improve; a seeded CI-width search for the improving/worsening pair) and then frozen as
literals. The rule itself was not changed after any outcome was observed.
