# P12C Post-Closeout Suite Run Record (Part H)

Base: `phase-1-symbolic @ 0d985029` + audit commits `75d2eb9` (Parts A–C), `3138584` (Parts D–E) and
the Part G guard suite (committed with this record in `355c660`). Host: sandbox, Linux-6.1.158, Python 3.13.14, pytest 9.0.3
(NumPy 2.3.5 / SciPy 1.17.1 as recorded in the P12C evidence).

## Authoritative suite — two independent runs

**Command (run from repo root):**
```
python3 -m pytest paper9/verification/suite/ -q
```

| Run | total | passed | failed | skipped | exit | duration (pytest) | log | log sha256 |
|---|---|---|---|---|---|---|---|---|
| 1 | 83 | 83 | 0 | 0 | 0 | 6.84 s | `paper9/audit/logs/p12c_post_closeout_suite_run1.txt` | `0553ecd7c6ad390ce3572db98294e7d883aaa8485a70edc52551c7d2447048e4` |
| 2 | 83 | 83 | 0 | 0 | 0 | 7.10 s | `paper9/audit/logs/p12c_post_closeout_suite_run2.txt` | `8b95eccadbf8a4e413273c3634e72c5346b0c97327205891ea2d085915258b36` |

Both runs are byte-different (timings/pytest footer) but report identical results; exit code 0.

Count reconciliation: the suite held **72** tests at P12C close-out; the Part G guard file adds
**11** tests → **83**. No test was deleted or skipped.

## Supplementary — non-suite tests in `paper9/` (whole-repo collection = 113)

**Command:**
```
python3 -m pytest paper9/production/p5/test_p5_integrity.py \
  paper9/validation/b6_lwz_tm/test_lwz_tm.py \
  paper9/eqs/phase1/scripts/audit_m15a_hermiticity_test.py -q
```
→ **30 passed, 0 failed, exit 0, 52.44 s**, log
`paper9/audit/logs/p12c_post_closeout_nonsuite.txt`, sha256
`8f9ad089ad788ed6c5de20be4ad6f83428c568190f598d652d2bef36aa449601`.
Repo-wide collection: `python3 -m pytest paper9 --collect-only -q` → **113 tests**
(83 suite + 30 non-suite) ✓.

## Notes

- Logs are committed verbatim under `paper9/audit/logs/`; hashes above are of those files.
- “passed” counts were taken from the pytest summary lines in the logs; no claim of success is
  made beyond those recorded outputs.
- The Part G guards were additionally executed twice on their own (11 passed both times,
  0.05 s / 0.02 s) before this record.
