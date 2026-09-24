# P4B B1 — Resolution Closeout

Date 2026-09-24 · branch `phase-1-symbolic` · base HEAD `410f4537b548a3dea45d4891e9c70cf4818310be`
(P12C base `0d9850290b63a5da81b098d999714ab621684c77`). No push. P12C results/scripts and
Blueprint v1.3 untouched; no P12E value imported or invented.

## 1. Exact cause of the conflict

`p4b_5g_to_5i.txt` and `p4b_5g_to_5i.json` are **two executions of the same committed script
`p4b_5g_to_5i.py` with identical frozen `[S-P4A]` inputs** — run 1 (stdout log → TXT) and run 2
(the record's reported run → JSON), committed together in `1581497`.

They differ only in the 5i block, and only because of one datum:

- the 5i eigensolve is `eigsh(…, which="SM", tol=1e-12)` **without a start vector**, so each call
  draws a fresh random start vector; two consecutive calls on the *identical matrices in one
  process* differ by 9.9e-14 (n=16) and 5.5e-13 (n=32), while the same call with an explicit `v0` is
  bit-reproducible (max |Δω| = 0.0);
- hence ω(32²) was 1.1648553893287734 in run 1 (relative error 1.2009e-13) and 1.1648553893289162
  in run 2 (2.4781e-15);
- the script admits a fit point only when `err > 1e-14` (fixed cut), so run 1 fitted
  **4 points** (slope 5.4857096) and run 2 fitted **3 points** (slope 4.173919246515192).

Nothing else changed: same meshes 4/8/16/32, same k, same observable, same tolerance, same
acceptance predicate, same script revision. ω(4×4) is bit-identical in both artifacts and in all 21
realizations, and the entire 5g/5h content matches to full precision — proving the two runs are the
same calculation.

## 2. Provenance of the JSON

Machine-readable suite output written by the script itself (`dest = HERE / "p4b_5g_to_5i.json"`), with
the script's schema and annotation keys (`PCR1`, `G3`, `B6`, `P4B`, tolerances, `rows` ledger, `note`).
`utc = 2026-09-22T15:00:35.535905+00:00`, python 3.13.14, numpy 2.3.5, 21/21 PASS. It is **run 2**:
the record `P4B_5g_5i.md` designates the reported observed slope (4.17; CI [3.15, 5.20]) and the
16→32 change ≈ 4.6e-11 as "run 2", and only the JSON matches that run (max |Δω| = 2.085e-13 against
the other committed run, exactly the "2.1e-13" of the record). Not hand-edited — every field is
reproducible from the script's arithmetic. sha256 `383843632e317c219b4df68fdf8fd875a117cf3cde35babf14b75f6c6a8ee185`.

## 3. Provenance of the TXT

Captured stdout of **run 1** (`P4B 5g-5i  python 3.13.14 numpy 2.3.5`, same params line,
`TOTAL 21  PASS 21  FAIL 0`, footer `wrote /tmp/bfs-repo/…/p4b_5g_to_5i.json` — foreign clone path).
5i block: `observed slope=5.4857 CI [2.2301,8.7413] se=0.7566 nfit=4 floor=False`,
`eps_Delta=4.626173e-11`. **Preserved byte-identical**; now labelled by
`paper9/verification/suite/p4b_5g_to_5i.txt.provenance.md`.
sha256 `1daf0f322260327919ee321f0a88d308f637a1c0e6473af5fcccbc56c69b2263`.

## 4. Is 5.4857 reproducible?

- **Exactly, from the run-1 evidence**: yes — recomputing the LSQ from the TXT's own ω-vector
  (4-point subset) gives 5.4857096102 / CI [2.2301413, 8.7412779] / se 0.756581, matching the TXT to
  all printed digits.
- **End-to-end**: the *family* is reproducible — 19/19 fresh sandbox realizations produced the
  4-point branch (slopes 4.6426 … 7.1648); the specific value 5.4857 was not regenerated bit-exactly
  because that requires the exact run-1 draw of ω(16²)/ω(32²).
- **As a metric**: **not reproducible** — the 4-point estimator (which includes the noise-limited 32²
  datum) has a 49 % spread across 21 realizations and must not be cited.

## 5. Is 4.173919246515192 reproducible?

- **Exactly, from the governing evidence**: yes — recomputing the LSQ from the JSON's own ω-vector
  under the script's own `err > 1e-14` rule gives 4.173919246515192, CI
  [3.1453687594104447, 5.202469733619939], ε_Δ = 4.6318154949690315e-11 — bit-exact match.
- **End-to-end**: the *quantity* is reproducible — the 3-point (4², 8², 16²) estimator across all 21
  realizations spans 4.173919 … 4.183199, i.e. **0.22 %**; ε_Δ spans 4.5505e-11 … 4.6790e-11
  (2.6 %). A bit-exact end-to-end regeneration of the committed file is not attainable, because it
  needs a 32² draw below 1e-14 (0 of 19 fresh draws in this sandbox; the committed run 2 is one such
  draw).

## 6. Governing-source decision (evidence policy A → JSON governs)

The JSON governs, on three independent grounds — not on preference:
1. **provenance** — it is run 2, the run the committed record designates as the reported one;
2. **consumption** — it is the only artifact read downstream (Table 4, Table 6, Figure 5,
   `production/p5/p5_core.py`, guards); the TXT is prose evidence only;
3. **reproducibility of the reported quantity** — 3-point estimator spread 0.22 % vs 4-point 49 %.

Governing values: **slope 4.173919246515192; 95 % CI [3.1453687594104447, 5.202469733619939];
ε_Δ = 4.6318154949690315e-11; note "no theoretical order claimed"**.
The TXT keeps its run-1 values as labelled history. No file was rewritten; no scientific number was
changed; `p4b_5g_to_5i.py` was not modified.

## 7. Exact acceptance criterion (as implemented, unchanged)

5i acceptance = the three `check(...)` predicates: slope finite; ε_Δ finite; and
`|ω₃₂−ω₁₆|/ω₃₂ ≤ ε_Δ` — the third being **definitional/tautological by construction** of
ε_Δ := max(|ω₃₂−ω₁₆|/ω₃₂, err₃₂). This tautology is inherited from the plan's own row-5i wording
(`plan/CALC_MASTER_PLAN.md`: "ε_Δ = locked operational floor; 16²→32² change ≤ ε_Δ"), is faithfully
implemented, is now documented, and was **not modified** (criterion change = authorisation
required). The regression slope is descriptive only and no theoretical order is claimed. P4B's
PASS/FAIL never depended on which fit subset was used (21/21 PASS in both committed runs and in all
19 fresh runs).

## 8. Manuscript consistency

Checked `latex/ms.tex`, `latex/sections/*.tex`, `tables/out/`, `figures/`:
- "5.4857" / "5.485" / "4.626173e-11" appear **nowhere** in manuscript, tables or figures;
- the manuscript states p = 4.17 (CI [3.15, 5.20]) with the "no theoretical order claimed" caveat
  and ε_Δ = 4.63e-11 — exactly the governing JSON values;
- `tab02_parameters.tex` cites "[A] P4B 5i mesh convergence study (commit 1581497)" for ε_Δ;
- downstream generators read only the JSON. No manuscript edit was needed.

## 9. Guard result

New regression guard `paper9/verification/suite/test_p4b_b1_json_txt_consistency.py` (8 tests):
pins JSON/PY/TXT byte hashes; re-derives slope/CI/ε_Δ from the JSON's own evidence; enforces the
`err > 1e-14` fit-subset rule and the ε_Δ definition (incl. the documented definitional sub-check);
pins the TXT's run-1 values + provenance label so silent edits fail; asserts TXT↔JSON agreement on
5g/5h and ω(4×4); asserts no theoretical-order claim and no run-1 value in the manuscript; asserts
only the JSON is consumed; and (opt-in) re-runs the suite end-to-end checking 21/21 PASS, schema,
bit-identical ω(4×4) and the documented 3-point stability band.

Executed **twice** (both with the opt-in end-to-end rerun enabled):
run 1 → **8 passed, 0 failed, 0 skipped, exit 0, 73.41 s** (log
`audit/logs/p4b_b1_guard_run1.txt`, sha256 `39d32c1caae0949239e97331d53e98501888b927891ff071ce2a52509b941858`);
run 2 → **8 passed, 0 failed, 0 skipped, exit 0, 72.90 s** (log
`audit/logs/p4b_b1_guard_run2.txt`, sha256 `800b6be1c2781beb2a545a510f147794604161037b68ed8490af93aacbdb935d`).

## 10. Full-suite result

`python3 -m pytest paper9/verification/suite/ -q` (repo root), default environment:

| run | collected | passed | failed | skipped | exit | pytest time | log sha256 |
|---|---|---|---|---|---|---|---|
| 1 | 91 | 90 | 0 | 1 | 0 | 7.52 s | `39e58ef5f2121a396c17597ef3d8b587b3009c8b90d87f4124a891a34519b362` |
| 2 | 91 | 90 | 0 | 1 | 0 | 7.74 s | `eebddfb5102f9e93931cfc7ab1b3f6a533a9267fa4004ce7eb67619f7706a4cf` |

(1 skipped = the opt-in end-to-end rerun, exercised separately with `P4B_B1_FULL_RERUN=1`; suite grew
72 → 83 → 91 as Parts G and B1 added guards. Logs: `audit/logs/p4b_b1_suite_run{1,2}.txt`.)

## 11. B1 status

**B1: CLOSED.** Cause identified by executable provenance; governing value established on evidence
(not preference); the historical TXT preserved byte-identical and explicitly labelled; artifact
pairing documented in the record (append-only addendum); regression guard added and executed twice;
manuscript verified consistent; suite green twice. No scientific number was changed and no engine
file was touched.

**Recorded follow-ups (not applied; require authorisation — outside B1):**
1. pin the 5i start vector (`v0`) in `p4b_5g_to_5i.py` so the suite becomes bit-reproducible
   (this would change future outputs → would require re-baselining the JSON);
2. align the inline comment ("LSQ only on points above 10*min_err") with the implemented
   `err > 1e-14` cut, and document the fit-subset rule in the record;
3. decide whether the definitional 16²→32² ≤ ε_Δ check should be replaced by an independently
   bounded criterion.
4. Standing P12C-era blockers are unaffected: PCR1 / G3 / G4 remain NOT MET and P5 remains
   NOT PASS/OPEN (`P12C_RELEASE_READINESS.md`).
