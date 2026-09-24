# P4B Post-B1 — Remediation Readiness Report

Date 2026-09-24 · HEAD `6f7850dd4f6947ed001e9489d4d7f8217a4804df` → this commit · branch
`phase-1-symbolic` · P12C base `0d985029`. No push · no P12E · no new scientific production ·
no P12C calculation · Blueprint v1.3 and `main` untouched.

**Terminology (strict, never interchanged).**
*artifact-level reproducibility* — a committed artifact's values re-derive from its own data and its
provenance is fixed. *pipeline-level reproducibility* — re-executing the production path returns the
same reported quantity within a stated tolerance. *solver-level determinism* — executions return
bit-identical eigenvalues. *scientific validation* — independent physical evidence confirms the
quantity measures what it claims. *guard robustness* — a protective test fails on meaningful change
and passes across harmless environments.

## 1. R-1 result — OPEN

Cause localised to one interaction: the fixed `err > 1e-14` fit-subset predicate (stage 5) applied to
the n = 32 output of a non-deterministic eigensolve (stage 3). The predicate's decision window is
±1.165e-14 in ω (2.33e-14 wide) while the solver's own call-to-call jitter at n = 32 is
1e-13 … 5e-13 — i.e. **the cut resolves solver noise, not discretization**. Stages 1, 2, 4, 6 are
deterministic (matrix hashes identical on rebuild; post-processing bit-identical on identical
input; OLS reproduces both reported slopes exactly).

| characterisation | status |
|---|---|
| artifact-level reproducibility of the governing JSON | **established** |
| pipeline-level reproducibility of the reported slope | **NOT established** — 26.6 % spread over 21 realizations under the deployed rule (20/21 draws take the 4-point branch); the committed 4.17 is the 1/21 branch |
| solver-level determinism (iterative path) | **not established** (unpinned start vector; dense path deterministic per configuration only) |
| ε_Δ reproducibility | 2.78 % spread (4.5505e-11 … 4.6790e-11); quoted 4.63e-11 is the recorded realization |
| scientific validation | not attempted; no independent physical confirmation of p = 4.17 is claimed anywhere |

## 2. C-1 result — OPEN (criterion non-discriminant + drift)

Deployed acceptance replicates as: four finite ω values + finite slope + finite ε_Δ +
`d16_32 ≤ ε_Δ ≡ max(d16_32, err32)` (**tautology, class C**). Synthetic-sequence test: the logic
PASSES a flat plateau, an oscillating sequence, pure noise, and an **anti-convergent** sequence
(errors growing under refinement); the only failure mode is < 3 points above the cut. ε_Δ is
data-derived, not prescribed. `err > 1e-14` is an undocumented arbitrary constant; and the code
contradicts its own comment ("10·min_err"), where the commented rule would select 3 points in
**both** committed runs (4.176712 / 4.173919) instead of 4/3 — the drift is execution-relevant
(full analysis: `P4B_5i_CRITERION_AUDIT.md`).

## 3. G-1 result — CLOSED (guard-level, implemented)

The failing assertion was `d["omega"][0] == rec["5i"]["omega"][0]` — an **exact-bit equality on the
dense-path eigenvalue**. Investigation: it does not test a scientific invariant. The committed
evidence bundle itself records two bit-values for the same code and inputs
(`1.164855406907999` default, 20/21 realizations; `1.1648554069080328` under `OMP_NUM_THREADS=1`,
1/21) — a BLAS/thread last-bit effect (~3.4e-14). Material changes (mesh, k, parameters,
quadrature) move this value by ≥ 1e-8, i.e. four orders above the largest tolerance now used.

**Correct guard semantics chosen: B (numerical-tolerance determinism) + C (invariant/property
based).** Exact byte-hash pinning (semantics A) is retained **only for the committed artifacts**
(JSON, TXT, script, provenance label) — those are immutable evidence and *should* fail on any edit.

## 4. Comment/implementation drift — audited, not changed

Comment l.427 says "points above 10*min_err"; l.428-432 implement `floor_flag` (reported only) plus a
fixed `e > 1e-14`. Verified from committed data: commented rule ⇒ TXT 4.176712 (3 pts), JSON
4.173919 (3 pts); over 21 realizations the commented rule selects 3 points 21/21 times (spread
0.222 % vs 26.6 %). Changing only the comment is safe but insufficient; changing the logic is a
criterion change → §7.

## 5. Proposed remediation (precise; nothing below is implemented)

### R1 — make the P4B estimator rule-predetermined (+ optional v0 pinning)

| item | detail |
|---|---|
| files | `paper9/verification/suite/p4b_5g_to_5i.py` (fit-subset rule; optionally `v0` in `acoustic_omegas`); `paper9/verification/suite/test_p4b_b1_json_txt_consistency.py` (PY_SHA pin update); `P4B_5g_5i.md` (record note) |
| exact logic (recommended) | replace `use = [pts with e > 1e-14]` by a **pre-declared** subset: fit 4², 8², 16²; report 32² as the floor datum (equivalently: the comment's measured rule, since both select 3 points in 21/21 realizations). Optionally pin `v0` (and thread count if bit-identity is wanted) in the `eigsh` call |
| why required | removes solver-noise dependence of the reported estimator; makes the executed rule match its documented intent; makes the pipeline reproducible to 0.222 % |
| expected effect | committed artifact values **unchanged** (run 2 already uses the 3 points: slope 4.173919246515192, CI [3.1453687594104447, 5.202469733619939], ε_Δ 4.6318154949690315e-11); future runs stop taking the 26.6 %-wide 4-point branch; ε_Δ keeps its definition (its residual 2.78 % spread is solver-limited and would need v0 pinning to narrow) |
| numerical baseline changes? | **No for the recorded artifact** (verified); **yes for executed behaviour** → criterion change |
| new calculation required? | no new science; one verification re-run + record update if adopted |
| Blueprint change? | **No** |
| classification | *numerically non-baseline-changing for the committed artifact, criterion-changing for the pipeline* → **requires explicit re-baselining authorization**; not implemented |

### C1 — non-tautological 5i acceptance

| item | detail |
|---|---|
| file | `paper9/verification/suite/p4b_5g_to_5i.py` (check block, l.443-462), `P4B_5g_5i.md`/plan note |
| exact logic (options, pick one under authorization) | (i) assert the **fit residual** of the selected points to the power law is below a stated bound (e.g. max \|ln e − (a + p ln h)\| ≤ 0.05); (ii) assert **monotone decrease** of rel_err across the pre-declared meshes (true in 21/21 realizations); (iii) replace the definitional sub-check with an **externally motivated** bound, e.g. `d16_32 ≤ 10 · tol_ω²` where the solver tolerance is declared, or a prescribed floor like 1e-10 chosen *before* looking at data; (iv) reclassify "16²→32² ≤ ε_Δ" explicitly as a *definition lock* (documentation), not a test |
| why required | the current row cannot fail for any convergent, non-convergent or noisy sequence (demonstrated); a test that cannot fail provides no evidence |
| expected effect | row 5i gains discriminating power; recorded numbers unchanged |
| baseline/Blueprint impact | numbers unchanged; criterion text changes → **requires authorization**; no Blueprint change |

### G1 — environment-robust guard (IMPLEMENTED, see §6)

## 6. What was safely implemented in this task (guard-level only)

`paper9/verification/suite/test_p4b_b1_json_txt_consistency.py` (single file, no scientific artifact):

1. **G-1 fix** — opt-in re-run comparison changed from exact-bit equality to
   `|Δω(4×4)| ≤ 1e-12` (documented basis: thread jitter ≤ 5e-14; smallest material change ≥ 1e-8)
   **plus** a property band: ω(4×4) must lie inside the documented realization band from
   `audit/evidence/p4b_b1` padded by 5e-13;
2. **additional re-run assertions** — schema, `note == "no theoretical order claimed"`,
   `(PASS, FAIL) == (21, 0)`, mesh sequence `(4, 8, 16, 32)`, monotone decreasing ω_T, 4×4 within
   1e-7 of the closed form;
3. **hash-independent baseline freeze** — new test pinning the governing literals (slope, CI95,
   ε_Δ, d16_32, ω and rel_err vectors, meshes, note, floor_flag, utc, PASS/FAIL, P4B/PCR1/G3/B6,
   Case-H parameters). This closes the "tamper the JSON *and* update its hash pin" hole;
4. **documentation test** — a test that reads the committed evidence bundle and asserts its
   documented 4×4 spread (two bit-values, ≤1e-12) so the G-1 basis cannot silently disappear.

Commit-level statement: **no scientific baseline file changed** — in particular the authoritative
JSON, the historical TXT, `p4b_5g_to_5i.py`, the 5i criterion, P12C evidence and the Blueprint are
byte-identical (§11).

## 7. Changes requiring explicit authorization (NOT implemented)

1. **R1 rule change + optional v0 pinning** (§5 R1) — criterion/behaviour change, needs one
   verification re-run and a record note; classified *numerically non-baseline-changing for the
   committed artifact* but *criterion-changing for the pipeline*.
2. **C1 acceptance redesign** (§5 C1) — criterion change.
3. **Comment drift fix** — comment-only edit is safe but is only worth doing together with (1)/(2).
4. Any regeneration of the governing JSON or the historical TXT — none is needed for (1)/(2);
   the historical pair must stay as-is regardless.
5. Blueprint v1.3 or `main` changes — **not required by any option**.

## 8. Mutation testing (Part H) — all detected

**Fast mode** (isolated copy tree, committed files mutated; baseline 9 passed / 1 skipped):

| mutation | result |
|---|---|
| M1 `slope` → 4.20 | 3 failed ✔ |
| M1b `slope` → 4.20 **+ JSON_SHA constant updated** (coordinated tampering) | **2 failed ✔** (caught by the new literal freeze) |
| M2 `eps_Delta` → 4.9e-11 | 3 failed ✔ |
| M3 `rel_err[2]` → 5.1e-11 | 3 failed ✔ |
| M4 `utc` provenance altered | 2 failed ✔ |
| M5 `rel_err[3]` → 3.0e-13 (fit-subset change) | 4 failed ✔ |
| M6 ω(32²) shifted +3e-13 | 2 failed ✔ |
| M7 TXT provenance label inverted ("not the governing" → "now the governing") | 1 failed ✔ |
| M8 TXT bytes `5.4857` → `5.4859` | 1 failed ✔ |
| restore → baseline | 9 passed / 1 skipped ✔ |

**Opt-in end-to-end mode** (script mutated; baseline 10 passed, 58.8 s):

| mutation | result |
|---|---|
| S1 k changed (0.31π/L → 0.32π/L) | 2 failed ✔ (tolerance + band) |
| S2 fit rule takes all 4 points | 1 failed ✔ ("reported slope != its own fit") |
| S3 mesh sequence shortened to 4, 8, 16 | 2 failed ✔ |
| S4 note replaced by "theoretical order p = 4 claimed" | 2 failed ✔ |
| S5 restore control | 10 passed ✔ |

## 9. Default vs OMP_NUM_THREADS=1 (Part I)

| configuration | result |
|---|---|
| fast mode, default | 9 passed, 1 skipped (×2: 0.17 s / 0.09 s) |
| opt-in, default | **10 passed** ×2 (63.67 s / 66.01 s) |
| opt-in, `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1` | **10 passed** (67.86 s) — previously 1 failed (exact-bit assertion); **G-1 proven fixed in both environments** |

## 10. Complete suite (Part I)

`python3 -m pytest paper9/verification/suite/ -q`, twice, default environment:

| run | collected | passed | failed | skipped | exit | runtime | log sha256 |
|---|---|---|---|---|---|---|---|
| 1 | 93 | 92 | 0 | 1 | 0 | 6.92 s | `22771de392638dc370d4686f…` |
| 2 | 93 | 92 | 0 | 1 | 0 | 6.29 s | `e3cb05604a3c2c0fecaa17ac…` |

(93 = 91 previous + 2 new guard tests; the single skip is the opt-in re-run, exercised separately
above.) P4B 5g/5h guard: 3 passed ×2. Logs committed under `paper9/audit/logs/p4b_remediation_*`:
`5g5h_run{1,2}` (`c67e541fd068f1dc…`), `guard_fast_run{1,2}` (`5ac2fc038a52b8c7…` /
`372024a78cd26cba…`), `guard_full_run{1,2}` (`7ad747010dfe166a…` / `f0df3fe937b34aaf…`),
`guard_full_omp1` (`950440822aebb3b7…`), `suite_run{1,2}` as tabulated. Both suite runs were
executed on the final committed state (guard + audit files present).

## 11. Immutability (Part J) — all verified

| artifact | sha256 | status |
|---|---|---|
| `Paper9_Blueprint_v1.3.tex` | `ca71b91aba4ca4ab…` | identical to base |
| P12C 32² raw JSON (+sidecar) | `5547bae453964946…` | identical |
| P12C 64² raw JSON (+sidecar) | `c8910c0de2188b49…` | identical |
| P11D convergence / Δ_X | `1d4476f12d0b8ae9…` / `7dbabbd3676c33d0…` | identical |
| P4B historical TXT | `1daf0f3222603279…` | identical |
| P4B governing JSON | `383843632e317c21…` | identical (not regenerated) |
| P4B script | `b1c8d9963b14a19e…` | identical (criterion untouched) |

`git diff HEAD -- paper9/production paper9/results` is empty: no P12C production script and no raw
result changed. The only modified tracked file in this task is the guard.

## 12. Manuscript (Part K) — consistent, unchanged

- governing values present as printed: `p = 4.17`, `CI [3.15, 5.20]` (ms.tex, sec05 l.108, sec09),
  `ε_Δ = 4.63e-11` (ms.tex, sec05 l.113 + fig. 5 caption, sec09, Table 2, Table 6), and the
  "no theoretical order claimed" caveat (abstract);
- full-precision tokens (`4.173919246515192`, `3.1453687594104447`, `5.202469733619939`,
  `4.6318154949690315e-11`) appear **only in the governing JSON**, as designed;
- run-1 values (`5.4857`, `5.4857096`, `4.626173`) appear **nowhere** in `latex/`, `tables/out/`,
  `figures/`;
- no manuscript file was modified in this task.

## 13. Current blockers

| id | status | note |
|---|---|---|
| R-1 | **OPEN** | pipeline-level reproducibility not achieved; fix designed (§5 R1) and **awaiting explicit re-baselining authorization** |
| C-1 | **OPEN** | 5i criterion non-discriminant + arbitrary cut + comment drift; redesign options listed (§5 C1), criterion untouched |
| G-1 | **CLOSED** | guard revised to semantics B + C, proven in default and OMP=1 environments, mutation-verified |
| B1-E1/E2 | recorded | B1-document corrections already logged in `P4B_POST_B1_INDEPENDENT_AUDIT.md` |
| governing gates | unchanged | PCR1, G3, G4 **NOT MET**; P5 **NOT PASS/OPEN**; no release/final language permitted |
| P12E | absent | unverifiable in this sandbox; not reconstructed |
| procedural | standing | workspace snapshot drops `.git` and `*/out/` on re-provisioning — re-verify at task start |

**Bottom line.** G-1 is closed at guard level with evidence in both environments and full mutation
coverage. R-1 and C-1 remain open by design: both require changing the executed P4B rule, and this
task forbids that without explicit authorization. No scientific artifact, criterion, threshold,
number or manuscript value was altered.
