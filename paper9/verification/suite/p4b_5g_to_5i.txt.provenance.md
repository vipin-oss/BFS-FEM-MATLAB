# Provenance label — `p4b_5g_to_5i.txt`

**This file is a historical stdout log (run 1 of 2), not the governing P4B record.**

| field | value |
|---|---|
| artifact | `paper9/verification/suite/p4b_5g_to_5i.txt` |
| sha256 | `1daf0f322260327919ee321f0a88d308f637a1c0e6473af5fcccbc56c69b2263` |
| added | commit `1581497` ("P4B: add 5g-5i suite (21/21 PASS, exit 0) + record"); unchanged since |
| identity | stdout capture of **run 1** of `p4b_5g_to_5i.py` (footer: `wrote /tmp/bfs-repo/…/p4b_5g_to_5i.json` — a foreign clone path) |
| 5i block | `observed slope=5.4857 95% CI [2.2301,8.7413] se=0.7566 nfit=4 floor=False`, `eps_Delta=4.626173e-11` |
| governing record | `paper9/verification/suite/p4b_5g_to_5i.json` (**run 2**): slope `4.173919246515192`, CI95 `[3.1453687594104447, 5.202469733619939]`, `eps_Delta = 4.6318154949690315e-11`, `note = "no theoretical order claimed"` |

**Why the two differ (one-line cause).** Same script, same frozen `[S-P4A]` inputs, two executions:
the ARPACK solve at 32² (called without a start vector) is not reproducible per call, so the 32²
relative error landed above the script's fixed `err > 1e-14` fit-subset cut in run 1
(1.2009e-13 → 4-point fit, slope 5.4857) and below it in run 2 (2.4781e-15 → 3-point fit, slope
4.173919). Full evidence: `paper9/audit/P4B_B1_PROVENANCE_RECONCILIATION.md`.

**Usage rules.**
1. The governing values for the P4B 5i row are the JSON's. The values in this log must **not** be
   quoted as the suite's result (in particular `slope = 5.4857`); they belong to the unstable
   4-point estimator family (spread 49 % across 21 realizations, vs 0.22 % for the governing
   3-point estimator).
2. This file is evidence and must not be edited, regenerated or deleted. Its byte hash is pinned by
   `test_p4b_b1_json_txt_consistency.py`.
3. Downstream consumers (tables, figures, `p5_core`, manuscript) must read only the JSON.
