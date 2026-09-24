# P12I — Independent Post-P12H Release-Readiness Audit

**Phase:** P12I (independent verification; branch `phase-1-symbolic`; `main` untouched)
**Date:** 2026-09-24 · **Audited object:** commit `dd42e81b946a9ae3bee84d09d90f7440f88559c8` (P12H)
**Baseline:** `2225cdc5c3189e056264229a0c3498f98207f344` (P12G) · **Remote:** `0d985029…` (unchanged)
**Posture:** the P12H report was treated as a *claim set*. Every material claim was re-verified from
repository artifacts, git objects, source code, archived evidence and freshly executed tests. No
scientific result, Rule R-fit constant, Blueprint v1.4 text or manuscript number was modified.
**Evidence bundle:** `paper9/audit/evidence/p12i/` (independent rule re-implementation + output, both suite logs, cross-check re-run).
**Independent scripts:** `/home/user/p12i_logs/rule_rfit_forensic.py` (re-implements Rule R-fit from
its frozen statement, without importing the repository module), `suite_run{1,2}.txt`,
`numerical_crosscheck_rerun.txt`, figure renders.

**Audit verdict in one line:** the governing science, the rule's behaviour, every gate status and
every numerical claim verify as reported; **three documentation/cosmetic corrections are required**
(§12), none of which touches the governing baseline, the rule's behaviour, or any gate status.

---

## 1. State verification (Part A)

| Check | Result |
|---|---|
| HEAD | `dd42e81b946a9ae3bee84d09d90f7440f88559c8` — exact |
| Working tree | `git status --porcelain` empty at audit start and at every checkpoint |
| Remote | `git ls-remote` → `phase-1-symbolic = 0d9850290b63a5da81b098d999714ab621684c77` (unchanged); `git status -sb` = *ahead 3*, i.e. nothing pushed |
| P12H commit shape | `git rev-list --count 2225cdc..HEAD` = **1**; parent = `2225cdc`; author/identity as configured |
| Uncommitted scientific/manuscript changes | none (`git diff HEAD`, `git diff --cached` empty) |
| Change set | `git diff --name-status 2225cdc HEAD` = 19 paths: 11 modified + 8 added, all inside the authorized scope (§9) |

## 2. Blueprint v1.3 / v1.4 comparison (Part B)

- **v1.3 sha256 = `ca71b91aba4ca4abe9f157eb595ac8c2f709d838957a08ea0dce7160685dbf9f`** — byte-identical
  to the protected hash; blob identical across `2225cdc` and `HEAD` (git object comparison).
- **v1.4 = `0089754b076ff9e390c6aa5f6b2b97ca27dd8d38c7d14de8a0e80d6e2c752c62`**, 87 490 bytes,
  derived from v1.3 by **exactly four replaced blocks** (`difflib` opcode diff, character similarity
  98.08 %): version/provenance row (l. 95), §5.7 `[STR]` sentence (l. 446), verification-matrix row 5
  (l. 618), PCR5 item (l. 895). No other line differs; braces balanced.

| Requested check | Result |
|---|---|
| F = 3 unchanged | ✓ present once, `$F = 3$`, identical to the frozen constant |
| Strict inequality | ✓ "greater than", "if and only if" (strict bi-conditional) |
| ≥ 3 admissible levels explicit | ✓ "If fewer than three levels satisfy the criterion, no rate is reported." |
| All levels computed and reported | ✓ "All four prescribed refinement levels are computed and reported with their eigenvalues, relative errors and step-to-step changes." |
| No theoretical order introduced | ✓ unchanged clause "a theoretical order is claimed only if justified … otherwise the observed rate is reported as-is" |
| ε_Δ distinct from measurement resolution | ✓ ε_Δ definition unchanged; "resolution-limited data" introduced for excluded levels; distinctness also stated in the plan, Table 6, §5.3 and the Fig. 5 caption |
| CI requirement unchanged | ✓ "The 95\% CI of the fit is reported" |
| Declared numerical zero `max(s_i, 1e-15)` | **NOT in v1.4** — see correction **C1** (§12). It is stated in the plan row 5i and implemented in `rule_rfit.py`; the omission is decision-inactive for every recorded case (verified in §4). |
| Silent scope changes | none found: the four blocks are confined to §5.7, the matrix row and PCR5; the fixed four-level-fit phrase is gone (intended), no scientific value or band allocation was touched |

## 3. Rule R-fit verification from source (Part C)

Re-implemented from the frozen statement (`admitted = e > 3 · max(s, 1e-15)`), independent of the
repository module, and re-applied to archived evidence:

| Property | Verification |
|---|---|
| Strictness | `e = 3s` exactly → **not admitted**; one ulp above → admitted (executed) |
| Independence from slope/CI/PASS-FAIL | the admission path reads only `(e, s)`; the same `(e32, s32)` yields the same verdict under a steep and a shallow surrounding trend; the B3/B4 pair (identical `e32 = 2.44140625e-12`, `s32 = 5e-12`, opposite effects on the fit) gives identical verdicts → the rule cannot be reading the estimate |
| No post-hoc subset selection | module source: `spread_used`/`is_admissible`/`decide`/`admissible_subset` contain no reference to slope, CI, residual or pass/fail; selection is a pure function of the frozen constants and the two measured inputs |
| Deterministic handling of missing levels | `None` error → level skipped from the record but counted in the mesh list; `None` spread → declared numerical zero (1e-15); `fit_admissible` requires `len(admissible) ≥ 3` else `fit = None` and `reportable = False` |
| ≥ 3-level minimum | `MIN_ADMISSIBLE = 3`, pinned by a guard test |

**Recomputed verdicts (all from archived evidence, independent implementation):**

| Evidence | Subset | Excluded | Recomputed slope | Recorded | Match |
|---|---|---|---|---|---|
| governing JSON | `{4², 8², 16²}` | `{32²}` | `4.173919246515192`, CI `[3.1453687594104447, 5.202469733619939]` | same | **bit-exact** |
| historical TXT (full-precision archive) | `{4², 8², 16²}` | `{32²}` | `4.176712221457638` | `4.176712` (printed to 6 dp) | ✓ |
| historical TXT (printed values parsed from the file) | `{4², 8², 16²}` | `{32²}` | `4.176679543252895` | — (4-s.f. input) | subset ✓ |
| Route-F evidence (audit only) | `{4², 8², 16²}` | `{32²}` | `4.180558982889443`, CI `[3.2014, 5.1598]` | `4.180559` | ✓ |
| control-k evidence | `{8², 16², 32²}` | — | `4.195543296186137`, CI `[3.2947, 5.0964]` | `4.195543` | ✓ |
| historical 21-realization spreads | recomputed `(max−min)/min`: `2.8974e-14 / 1.0637e-13 / 5.9207e-13 / 1.2619e-12` | — | documented `2.897e-14 / 1.064e-13 / 5.921e-13 / 1.262e-12` | ✓ | — |

The governing case is the decisive one: the rule, applied to the artifact's own errors and to
reproducibility evidence of the artifact's own era, reproduces `p` **and** the CI **bit-exactly**.

## 4. The 32² exclusion (Part D)

- `e_32 = 2.4780585559967227e-15` (governing JSON), `s_32 = 1.261904e-12` (era spread, recomputed),
  `ratio = e_32/s_32 = 0.00196375`, threshold `F·s_32 = 3.785711e-12`.
- Decision: **excluded**; margin `F/ratio = 1527.7×` below the threshold. P12H's "1527×" is a
  truncation of that computed ratio (no discrepancy).
- **Uniform application:** the same rule on the same-era evidence applied to the control k
  (`0.37, 0.19)π/L`) **retains** the finest level → `{8², 16², 32²}`, ratio 940.1. The rule therefore
  discriminates on measurement resolution, not on which side of an answer a level falls.
- **Replay over the 21 documented realizations** (independent): with the era spread, admission
  requires `e32 > 3.7857e-12`; the largest recorded `e32 = 8.4349e-13`; **0/21 realizations admit**,
  worst-case family margin **4.49×**.
- **The declared-zero floor is decision-inactive in every recorded case**: removing it
  (`max(s,0)`) changes no verdict here, because the only unmeasurable spread (Route-F 4²) has
  `e = 1.51e-8 ≫ 3e-15`. It matters only in the hypothetical `e_i < 3e-15` band (hence C1, §12).

## 5. C-1 verification (Part E)

- C-1 suite executed: **23 passed** (`test_p12h_c1_synthetic.py`). Source inventory confirms the
  required contents: 6 case classes (convergent 4th/2nd order → PASS; flat, oscillatory, random,
  anti-convergent → FAIL), a falsifier for each of P1/P2/P3/P4, three accepted sequences
  (incl. `p ≈ 1.06` and the P4 boundary), B1–B8 adversarial cases, trend-invariance, and the
  strict-P1 predicate pin.
- Governance guards: **10 passed**.
- **13/13 mutation matrix re-run independently**: control passes; R1–R13 all DETECTED; R13
  (P1 strict → non-strict) is detected by the dedicated strictness test (`1 failed, 32 passed`), so the
  earlier coverage gap is genuinely closed; `rule_rfit.py` restored byte-identically
  (`d4fed49241bc3f74…`).
- Legacy staged matrix re-run: **12/12 DETECTED**, cleanup complete.
- **Four-level sequence still fails P3** (independently recomputed: 4-level slope `7.164770`,
  `resid_max = 2.7965 > ln 1.5 = 0.4055`) — the measured fact that motivates the rule.
- No criterion constant was changed anywhere in the tree (`P_MIN`, `R_MAX`, `FLOOR_MAX`, `F`, floor all
  as frozen).

## 6. Manuscript / figure / table (Part F)

Independent numeric cross-check (values parsed from the files, compared with the governing JSON and
the rule record):

- **Table 6:** 4 rows, `e_i = 1.51e-08 / 7.59e-10 / 4.63e-11 / 2.48e-15` and
  `s_i = 2.90e-14 / 1.06e-13 / 5.92e-13 / 1.26e-12` — **all identical to the sources**; `ω` values
  identical to the JSON; only 32² marked out of the fit with `no (ratio 0.00196)`; footer states
  `p = 4.17`, CI `[3.15, 5.20]`, "no theoretical order claimed", the fitted subset `{4², 8², 16²}`,
  the resolution-limited 32² level and the operational mesh-change floor "distinct from the
  measurement reproducibility $s_i$".
- **Sec. 05:** the fitted subset and the exclusion are stated in the text; `p = 4.17`, CI, and
  `ε_Δ = 4.63 × 10^{-11}` unchanged; the two-floor distinction is stated; no four-level-fit claim.
- **Sec. 09, abstract:** wording changed only ("supports an observed least-squares rate … fitted over
  the three admissible levels"; abstract adds the pre-declared measurement-resolution rule);
  numbers unchanged; the abstract's CI statement is intact.
- **Forbidden-claim sweep** across sec05, sec09, ms.tex, tab06 (gen+out), fig05 gen, plan, v1.4,
  traceability registry: no "four-level fit", no "fourth-order convergence", no `O(h^4`, no
  "solver floor"; the only `Babu\v{s}ka` occurrence is v1.4's unchanged *condition* under which a
  theoretical order could be claimed—not a claim. Route-F values appear only inside the traceability
  registry's explicit negative disclaimer (see observation O3, §12).
- **Figure 5, visual check** (rendered from the committed generator): panel (a) shows the three
  admissible levels joined with the empirical fit and 32² as a distinct open red square labelled
  "resolution-limited (1 level, excluded from fit)", with separate lines for the operational floor
  and the measurement resolution; panel (b) marks the finest step with a hatched bar and its own
  legend entry. Text, caption and plotted distinction agree.
  **Cosmetic defects found:** the new panel-(b) legend (lower right) overlaps the finest-step bar and
  its value label (introduced by P12H), and the tallest bar's annotation collides with the "(b)"
  subplot title (pre-existing — reproduced from the `2225cdc` generator as well). See C3 (§12).

## 7. PCR / gate reassessment (Part G)

Verified against the **authoritative definitions in Blueprint v1.4 §10.4**, not against the P12H
status table:

| Item | Independently determined status | Basis (re-verified) |
|---|---|---|
| **PCR5** | **PASS — justified** | the definition's six elements all hold: observed rate (present in text/table/figure), LS fit over exactly the admissible levels (bit-exact recomputation), 95 % CI reported, every excluded level reported with `e_i`, `s_i` and ratio, ε_Δ reported and correctly interpreted as the operational mesh-change floor, no theoretical order claimed (guard-enforced), traceability rows present. Note the definition was itself amended by v1.4 (one of the four authorized blocks) and the amendment **strengthens** it (adds the subset rule and the disclosure duty) — so PASS is not obtained by relaxing the criterion |
| **PCR1** | **NOT PASS** (unchanged) | `benchmark_evidence.json` still carries 3 null `quantitative_error` entries; external ≤ 2 % relative error remains uncomputable without the author tables |
| **G1 / G2** | MET / MET (unchanged) | symbolic evidence intact; suite green (125/1) |
| **G3** | **NOT MET** (unchanged) | same blocker as PCR1; no new external data was added anywhere in P12H |
| **G4** | **NOT MET** (unchanged) | no file signs it; blocked by G3/PCR1 |
| **P5** | **NOT PASS / OPEN** (unchanged) | two parallel pipelines, reconciliation outstanding; grep confirms the manuscript contains no P5/production claims |
| **C-1** | **OPEN** (unchanged, correctly) | the criterion the audit is named for is **not deployed**: `p4b_5g_to_5i.py` (`b1c8d996…`) still contains the tautological acceptance ("16→32 change ≤ ε_Δ by construction of max(…)"), so the production acceptance path is unchanged |
| **G-1** | **CLOSED** (unchanged) | environment guard closed at `bb32253`; guards green |
| **R-1** | **OPEN** (§8) | pipeline-level reproducibility unachieved |

No gate was promoted in P12H or in this audit. PCR5's PASS is a *re-derivation under an amended
definition*, and the amendment is the one A1 authorized.

## 8. R-1 forensic assessment (Part H)

The four-way distinction P12H asserted is present and correct:

| Layer | Status | Independently verified evidence |
|---|---|---|
| **A. solver-level reproducibility** | established **for the Route-F configuration only** | P12E run1 ≡ run2 except the timestamp; the Route-F patch (`routeF_patch.diff`) shows exactly what that configuration adds: thread pinning, `tol = 1e-14`, `v0 = default_rng(20260924)` |
| **B. governing-artifact reproducibility** | **NOT established** | the deployed call is `eigsh(…, tol=1e-12, maxiter=10000)` with **no `v0`** → ARPACK draws an unpinned start vector; the 32² eigenvalue then varies by `1.603e-13` relative between seeds while its distance to the exact value is `2.478e-15` (0.00196× its own reproducibility) |
| **C. estimator-rule determinism** | established | §3: pure function `(e_i, s_i) → verdict`, identical for every k, reproduces the governing rate bit-exactly, invariant over a 273×-wide F-window |
| **D. pipeline-level reproducibility** | **NOT established** | a fresh identical nominal run of the deployed path would return a different 32² eigenvalue and therefore a different 32² datum (though not a different *fit subset* — see below) |

**Is "branch-flip failure mode closed by protocol" supported?** Yes, with a precise scope:
replaying the 21 documented realizations under the rule with era-matched reproducibility gives
**0/21 admission** of the finest level (worst-case margin 4.49×, governing-artifact margin 1527.7×),
whereas the recorded legacy branch flipped (1/21 three-level, 20/21 four-level). So the *estimator
branch* is stable across every documented realization **for the governing era's reproducibility
evidence**. Two honest qualifications, both of which P12H's text anticipated and which this audit
sharpens:

- the stability is a property of that era's (wider) reproducibility estimate; under the narrower,
  different-configuration Route-F two-seed spread (`1.603e-13`) **7 of 21** realizations would admit
  the finest level (P12H's Part I note cited only the largest) — the branch is therefore **not**
  robust to every plausible measurement protocol;
- estimator-rule determinism (C) must not be restated as pipeline reproducibility (D).

**Determination: R-1 remains OPEN under its authoritative definition** ("pipeline-level
reproducibility — the estimator branch flips with solver realization"). The branch-flip *symptom* is
closed by protocol; the *property* is not achievable while the governing artifact is one realization
of an unpinned start vector, which only the explicitly unauthorized re-baseline would change.

## 9. Immutability, recomputed from git objects (Part I)

Manifest-independent: every protected asset was compared **across the two commits** (blob identity),
not against the P12H manifest alone.

- `git diff --name-status 2225cdc HEAD` = **19 paths, exactly the authorized set** (11 modified, 8
  added); **0 unexpected** paths anywhere in the repository.
- Protected assets: **11 byte-identical** across the commits (Blueprint v1.3, governing JSON,
  historical TXT, P4B script, P4B provenance, P12C 32²/64² raw, P11D convergence/ΔX, B1 guard,
  P12E staged patch); **9 changed, all authorized** (plan, ms.tex, sec05, sec09, tab06 gen+out,
  fig05 gen+out, P4B record addendum).
- **v1.3 blob identical** between commits; P12E staged evidence and P12C raw evidence: **0 changed
  paths**; all six evidence groups (`p12d`, `p12e`, `p12f`, `p12g`, `p4b_b1`, `p4b_remediation`)
  untouched — the P12H "46/46 byte-identical" claim holds.
- The P12E mirror directory contains only compiled caches (`__pycache__/_mut_*.pyc`) from the mutation
  runs; no mirror source file changed (observations O1, §12).
- P12H's own immutability summary ("11 unchanged, 9 changed, all authorized, 0 unexpected") is
  therefore **confirmed by an independent method**.

## 10. Regression (Part J)

| Run | Command | Result | Runtime |
|---|---|---|---|
| Suite, run 1 | `pytest paper9/verification/suite -q -rs` | **125 passed, 1 skipped** | 6.64 s |
| Suite, run 2 | `pytest paper9/verification/suite -q` | **125 passed, 1 skipped** | 6.41 s |
| Governance guards | `test_p12h_rule_rfit_governance.py` | 10 passed | 0.02 s |
| C-1 suite | `test_p12h_c1_synthetic.py` | 23 passed | 0.03 s |
| Rule-module mutations | `/home/user/p12h_logs/mutation_rfit.py` | **13/13 detected**, rule restored byte-identically | 5.7 s |
| Legacy staged mutations | `audit/evidence/p12e/mutation_harness.py` | **12/12 detected** | 3.9 s |
| Numerical / float / manuscript / Blueprint cross-check | `/home/user/p12h_logs/final_verification.py` | **43/43 passed** | 0.2 s |
| Rule re-derivation (this audit, independent implementation) | `/home/user/p12i_logs/rule_rfit_forensic.py` | governing slope **and** CI bit-exact; 4/4 subsets as recorded | 0.2 s |

**The single skip is investigated, not tolerated:** `test_p4b_b1_json_txt_consistency.py:237` is an
**opt-in** end-to-end rerun gated on `P4B_B1_FULL_RERUN=1`; the test file is byte-identical to
`2225cdc`, so the skip is pre-existing. The audit ran it anyway with the flag: **10 passed in 67.02 s**
— the deployed pipeline reproduces its own historical artifact (TOTAL 21 PASS 21) in a temporary
directory, and `git status` stayed clean afterwards. Suite growth 92 → 125 is exactly the 33 new
tests (10 governance + 23 C-1).

## 11. Claim-by-claim verification table (Part K)

| # | P12H claim | Evidence source | Independently verified? | Result | Notes |
|---|---|---|---|---|---|
| 1 | Governing `p = 4.173919246515192`; CI `[3.1453687594104447, 5.202469733619939]`; `ε_Δ = 4.6318154949690315e-11` unchanged | JSON vs git blobs vs §3 recomputation | yes | **CONFIRMED (bit-exact)** | artifact blobs identical; rule re-derives slope and CI without importing the module |
| 2 | Rule R-fit: `e_i > F·max(s_i,1e-15)`, F = 3 strict, ≥3 levels, applied uniformly, independent of slope/CI/PASS-FAIL | module source, plan row, executed boundary/trend tests | yes | **CONFIRMED** | floor stated in plan + code, **not** in v1.4 → C1 |
| 3 | 32² excluded because `e = 0.00196× s`, 1527× below threshold | JSON, era spreads, replay | yes | **CONFIRMED** (1527.7×) | family replay 0/21; counter-check 7/21 under the Route-F spread |
| 4 | The same rule retains the finest level at the control k | archived control-k evidence | yes | **CONFIRMED** | `{8²,16²,32²}`, ratio 940.1 |
| 5 | v1.4 = v1.3 + exactly four authorized blocks; v1.3 byte-identical | digests + opcode diff + git blob identity | yes | **CONFIRMED** | 4 blocks, no other line differs |
| 6 | 23 C-1 tests (6 classes, 4 falsifiers, B1–B8, trend invariance, strict-P1) | source inventory + execution | yes | **CONFIRMED** | four-level sequence still fails P3 |
| 7 | Rule mutations 13/13, incl. R13 | matrix re-run | yes | **CONFIRMED** | R13 detected by the strictness test |
| 8 | Legacy staged mutations 12/12 | matrix re-run | yes | **CONFIRMED** | cleanup complete |
| 9 | Suite 125 passed / 1 skipped | two runs | yes | **CONFIRMED** | 6.64 s / 6.41 s; skip pre-existing, opt-in test run separately and passes |
| 10 | 43/43 numerical/float/manuscript/Blueprint checks | script re-run | yes | **CONFIRMED** | reproduced identically |
| 11 | Immutability: 11 unchanged / 9 authorized / 0 unexpected; 46/46 evidence files | git object comparison (manifest-independent) | yes | **CONFIRMED** | 19-path change set exactly as authorized |
| 12 | PCR5 PASS re-verified under the amended definition | Blueprint §10.4 + artifacts | yes | **CONFIRMED** | PASS justified; amendment strengthened the criterion |
| 13 | PCR1 / G3 / G4 / P5 unchanged | evidence files, grep | yes | **CONFIRMED** | 3 null external-error entries; no P5 claims in the manuscript |
| 14 | C-1 OPEN | deployed script source | yes | **CONFIRMED** | tautological acceptance still deployed |
| 15 | R-1 OPEN; branch-flip closed by protocol only | replay + solver source | yes | **CONFIRMED**, with a sharpened figure (7/21) | see §8 |
| 16 | No Route-F re-baseline | blob identity + value sweep | yes | **CONFIRMED** | values occur only in the registry's negative disclaimer (O3) |
| 17 | No P12E import / staged evidence untouched | git diff on evidence dirs | yes | **CONFIRMED** | 0 changed paths |
| 18 | No push; one commit | `git ls-remote`, `rev-list --count` | yes | **CONFIRMED** | remote `0d985029…`; 1 commit |

## 12. Final decision (Part L) — **P12H VERIFIED WITH CORRECTIONS REQUIRED**

P12H is **internally consistent and evidentially supported on every material scientific claim**: the
governing baseline is unchanged and bit-exactly re-derivable, Rule R-fit behaves exactly as frozen,
the 32² exclusion is correct and uniformly applied, the C-1/adversarial/mutation evidence is
reproducible, the manuscript and floats agree with the artifacts, no gate was improperly promoted,
R-1 is correctly left OPEN, and nothing was pushed.

The corrections required are documentation-level (no numerical, solver, subset, gate or scope
impact):

- **C1 — v1.4 §5.7 does not state the declared numerical zero.** The Blueprint states
  `e_i > F·s_i` (F = 3 strict) but not `max(s_i, 1e-15)`. *File:*
  `paper9/plan/blueprint/Paper9_Blueprint_v1.4.tex`, line 446. *Required text (one clause, to be
  applied only in a future authorized change — not in this audit):* after "…times the reproducibility of
  that level's eigenvalue,", insert "where a level whose reproducibility is not measurable at the
  frozen configuration is treated as having the declared numerical zero $10^{-15}$,".
  *Impact:* none on any recorded verdict (verified in §4: the floor is decision-inactive for all four
  evidence cases); it closes a specification-completeness gap for the `e_i < 3·10^{-15}` band.
- **C2 — the P12H audit's description of that block is imprecise.** *File:*
  `paper9/audit/P12H_A1_PROTOCOL_CLOSURE_AUDIT.md`, §3, table row 2, which reads "per-level admission
  by `e_i > F·max(s_i, 1e-15)`". *Correction of record (this audit, §3 and §11 row 2):* v1.4 states
  `e_i > F·s_i` with F = 3 strict; the floor appears in the plan row 5i and in `rule_rfit.py`. The P12H
  document was deliberately **not** edited (an audit must not amend the object it audits); this P12I
  section is the correction of record.
- **C3 — cosmetic float defects.** *File:* `paper9/figures/out/fig05_mesh_convergence.pdf` /
  `figures/gen/fig05_mesh_convergence.py`. (i) The panel-(b) legend placed by P12H overlaps the
  finest-step bar and its `4.6e-11` label; (ii) the tallest bar's value annotation collides with the
  "(b)" subplot title (pre-existing, reproduced from the `2225cdc` generator). *Required action:*
  reposition the legend and place the bar annotations inside the axes in a future authorized float
  regeneration. *Impact:* presentation only; the plotted quantities and the fitted/excluded
  distinction are correct and agree with the caption.

Observations requiring no correction:

- **O1** — the P12E mirror retains `__pycache__/_mut_*.pyc` caches from the mutation harness; no
  mirror source file changed, so evidence immutability is intact.
- **O2** — `tables/gen/tab06_convergence_floor.py` guards `None` spreads in the *display* string but
  not in the ratio computation; latent only (its data source is the governing era, where all four
  spreads are measurable).
- **O3** — `audit/traceability_matrix.json` metadata quotes the Route-F values inside an explicit
  negative disclaimer; P12H's enumeration of artifacts free of Route-F values does not list this
  registry, so its statement is accurate as scoped but should be read with this note.
- **O4** — §8's sharpening: 7/21 (not 1) realizations would admit the finest level under the Route-F
  two-seed spread; this strengthens, not weakens, the OPEN verdict.

**Consequences explicitly NOT implied:** P12H verified does not mean release-ready. A1 remains the
governing choice (nothing in this audit gives evidence for the Route-F re-baseline); the v1.4
amendment is supported by the evidence; the governing numerical baseline is unchanged; R-1 remains
OPEN; PCR5 PASS is independently justified; and **no P13 work is authorized by this audit**.

## 13. Remaining blockers (unchanged by P12H and P12I)

1. **PCR1 / G3** — external ≤ 2 % relative error on benchmark Layers 1/2a/2b is uncomputable without
   author-released numerical tables; G4 cannot be signed while these are unmet.
2. **P5** — the two parallel P5 pipelines remain unreconciled; the manuscript claims nothing from them.
3. **R-1** — pipeline-level reproducibility requires the (unauthorized) Route-F re-baseline; meanwhile
   the estimator-branch failure mode is closed by protocol only.
4. **C-1** — the production acceptance path still contains the tautological sub-check; adopting the
   validated discriminant criteria in the deployed script is not authorized.
5. **C1–C3** above — documentation and float cosmetics, to be applied in a future authorized change
   (this audit makes no such change).
