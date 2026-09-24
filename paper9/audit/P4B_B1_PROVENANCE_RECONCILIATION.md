# P4B B1 — JSON↔TXT Provenance Reconciliation (forensic)

Audit date 2026-09-24. Base HEAD `410f4537b548a3dea45d4891e9c70cf4818310be` (branch
`phase-1-symbolic`), P12C base `0d9850290b63a5da81b098d999714ab621684c77`.
No push. No P12E values imported. P12C results, production scripts and Blueprint v1.3 untouched.

**Artifacts under investigation** (all added in one commit, `1581497` "P4B: add 5g-5i suite
(21/21 PASS, exit 0) + record"; `git log --follow` shows no later commit touching any of them):

| file | sha256 | size |
|---|---|---|
| `paper9/verification/suite/p4b_5g_to_5i.json` | `383843632e317c219b4df68fdf8fd875a117cf3cde35babf14b75f6c6a8ee185` | 8747 B |
| `paper9/verification/suite/p4b_5g_to_5i.txt` | `1daf0f322260327919ee321f0a88d308f637a1c0e6473af5fcccbc56c69b2263` | 5655 B |
| `paper9/verification/suite/p4b_5g_to_5i.py` | `b1c8d9963b14a19e0f62b29434811635f9a8d721133987b87d8e25882516f6a0` | 20221 B |
| `paper9/verification/suite/P4B_5g_5i.md` | `5ce552ba88b5617435d041e568b93050f3c6794ea87cd8a7314cc9b59d954fc3` | 4096 B |

## 1. Which calculation produced which number

**1.1 The script is one and the same.** `p4b_5g_to_5i.py` prints the log to stdout and writes
`p4b_5g_to_5i.json` next to itself (`dest = HERE / "p4b_5g_to_5i.json"`, tail of `main()`). The
committed JSON carries exactly the script's schema, including the suite-annotation keys the script
appends (`"PCR1": "NOT PASS"`, `"G3": "not met"`, `"B6": "PARTIAL (unchanged)"`, `"P4B": "PASS"`),
the declared tolerances (`tol_5g`, `tol_5h_identity`, `tol_5h_vg`), the `rows` ledger and the
`note: "no theoretical order claimed"`. **No field was added or edited by hand** — every key/value
is reproducible from the script source.

**1.2 JSON provenance = "run 2".** The record file `P4B_5g_5i.md` states: *"Repeat run agreement:
max |Δω| = 2.1e-13"* and, in the 5i section, *"observed slope 4.17, 95% CI [3.15, 5.20] (run 2 of
the same suite; runs vary with solver roundoff, 16→32 change ≈ 4.6e-11)"*. Measured here: the two
committed 5i ω-vectors differ by max |Δω| = **2.084998840246044e-13** (at n=16), and the committed
JSON is the only one of the pair whose slope is 4.17 with 16→32 change 4.6318e-11. Hence the
committed **JSON is the output of run 2**, the run the record designates as the reported one.

**1.3 TXT provenance = "run 1" (stdout log).** The TXT is a captured stdout log
(`P4B 5g-5i  python 3.13.14 numpy 2.3.5`, same `params [S-P4A]` line, `TOTAL 21  PASS 21  FAIL 0`)
whose last line is `wrote /tmp/bfs-repo/paper9/verification/suite/p4b_5g_to_5i.json` — a *different
clone path*. It reports `observed slope=5.4857 ... se=0.7566 ... nfit=4 floor=False`, i.e. the 5i
block of run 1. (The `/tmp/bfs-repo` footer is the known foreign-path quirk of this baseline, not a
defect to "fix".)

**1.4 Same inputs, same script revision.** Evidence that the two runs are the same calculation:
ω(4×4) = `1.164855406907999` is **bit-identical** in both artifacts *and* in all 21 sandbox
realizations (§3); the whole 5g block matches (v_∞ = 0.31622777, ratios 1.730 → 2.849e-4, FE
sequence), and the 5h block matches **exactly to full precision** (max energy-velocity deviation
`6.911715833981807e-10` and FE v_g deviation `3.6474033598987756e-07` appear verbatim in both).
Only the 5i ω values at n = 16 and n = 32 differ (2.1e-13 / 1.4e-13), which is precisely what the
record already flagged as "solver roundoff between runs".

**1.5 Neither artifact was manually edited.** Both are internally consistent with the script's own
arithmetic: recomputing the LSQ from each artifact's own ω-vector reproduces its slope and CI
exactly (§2.1). A hand edit would not survive that check.

## 2. The actual cause of the numeric divergence

**2.1 Both reported slopes are exact functions of their own evidence.**

| quantity | run 1 (TXT) | run 2 (JSON) |
|---|---|---|
| ω(4×4) | 1.164855406907999 | 1.164855406907999 |
| ω(8×8) | 1.164855390212705 | 1.1648553902126322 |
| ω(16×16) | 1.1648553893826616 | 1.1648553893828701 |
| ω(32×32) | 1.1648553893287734 | 1.1648553893289162 |
| rel err (4,8,16,32) | 1.5091e-8, 7.5871e-10, 4.6142e-11, **1.2009e-13** | 1.5091e-8, 7.5865e-10, 4.6321e-11, **2.4781e-15** |
| fit points used (`e > 1e-14`) | **4** | **3** (32² dropped) |
| reported slope | **5.4857096…** (TXT: 5.4857) | **4.173919246515192** |
| 95% CI | [2.2301413, 8.7412779] (TXT: [2.2301, 8.7413]) | [3.1453687594, 5.2024697336] |
| ε_Δ = max(\|ω32−ω16\|/ω32, err32) | 4.626173146257483e-11 (TXT: 4.626173e-11) | 4.6318154949690315e-11 |
| `floor_flag` | False | True |
| PASS/FAIL | 21/0 | 21/0 |

Both slopes and CIs were independently recomputed here from the printed ω values and match the
artifacts to all printed digits (run 1: slope 5.4857096102, se 0.756581; run 2: slope
4.1739192465152, se 0.080950).

**2.2 The switch is the script's own fit-subset cut.** In the 5i section the script does:

```python
floor_flag = errs[-1] < 1e-12 or (...)          # reported only, NOT used for the fit
use = [(h, e, n) for n, h, e in zip(meshes, hs, errs) if e > 1e-14]   # fixed 1e-14 cut
slope = lsq_loglog_slope([u[0] for u in use], [u[1] for u in use])
```

Run 2's 32² datum (2.4781e-15) fell **below** the fixed `1e-14` cut → 3-point fit (meshes
4, 8, 16) → slope 4.1739. Run 1's 32² datum (1.2009e-13) stayed **above** the cut → 4-point fit →
slope 5.4857. Nothing else changed: same script, same meshes, same k, same tolerance, same
acceptance predicate, same observable; the ε_Δ values differ only in the 5th digit *because* they
are built from the same slightly different ω(32²)/ω(16²).

**2.3 Why the 32² datum lands on either side: the iterative solve is not reproducible per call.**
The 5i section solves `eigsh(Kh, k=4, M=Mh, which="SM", tol=1e-12, maxiter=10000)` with **no start
vector**. Probes executed in an out-of-tree copy (`audit/evidence/p4b_b1/nondeterminism_probes.txt`):

- two consecutive calls on the **identical matrices in one process** differ: n=16 → 9.86e-14,
  n=32 → 5.46e-13;
- the same call with an **explicit start vector `v0`** is bit-reproducible: three consecutive n=16
  calls returned 1.16485538938230948 with max |diff| = **0.0**;
- an out-of-tree wrapper that seeded scipy's `rng` parameter (`default_rng(4)`) did **not**
  stabilise the result (three calls differed by 1.3e-13), whereas passing `v0` did.

So the per-call ARPACK start vector (drawn when `v0` is omitted; `scipy/…/arpack.py`:
`self.rng = np.random.default_rng(rng)` with `rng=None` ⇒ entropy-seeded, resid filled on ARPACK's
`ido == 4` request) is the sole source of variation, and at n = 32 the eigenvalue is only
determined to ~1e-13…1e-15 depending on the draw.

**2.4 Classification of the difference (task §1.7).** Changed frequency subset — no. Changed mesh
subset — no. Changed floor handling — no (the `floor_flag` branch is reported only). Changed
regression points — **yes, indirectly**: the fixed 1e-14 cut selected a different point set.
Changed acceptance subset — no. Different ε_Δ — only as a downstream 5th-digit effect. Different
rounding — no. Different script revision — no. Actual solver difference — **yes, in the sense of
solver *realisation*, not of solver configuration**: the same iterative eigensolver call returns a
slightly different smallest eigenvalue per invocation.

## 3. Reproduction records (task Part 2 / Part 5)

All reproduction ran in out-of-tree copies (`/tmp/p4b_repro`, `/tmp/p4b_seed`); the repository was
not written to. Evidence bundle: `paper9/audit/evidence/p4b_b1/`
(`repro_realizations_summary.json`, `formal_A.json/.txt`, `formal_B.json/.txt`, `run1.txt`,
`nondeterminism_probes.txt`).

- **JSON result**: recomputed exactly from the committed ω-vector (3-point subset by the script's
  own rule) → slope 4.173919246515192, CI [3.1453687594104447, 5.202469733619939],
  ε_Δ 4.6318154949690315e-11. ✔
- **TXT result**: recomputed exactly from run-1's ω-vector (4-point subset) → slope 5.4857096,
  CI [2.2301413, 8.7412779], ε_Δ 4.626173146257483e-11. ✔
- **Fresh executions** (all exit 0, `TOTAL 21 PASS 21 FAIL 0`): 5 unseeded (slopes 4.7891, 4.9902,
  5.3343, 4.8289, 5.2395; e₃₂ = 1.70e-13…6.01e-13), 12 RNG-seeded (slopes 4.7146…5.4979;
  e₃₂ = 1.17e-13…7.14e-13), 2 formal runs A/B (slope 4.8133 @ 72.5 s; slope 4.6426 @ 77.1 s;
  ε_Δ 4.6392e-11 / 4.6790e-11) — **19/19 fresh realizations took the 4-point branch; none produced
  e₃₂ < 1e-14.** Consequently: *the value 5.4857 is reproducible in kind* (every fresh run lands in
  its 4-point family) *and exactly computable from the TXT's own ω*; *the value 4.1739 is
  reproducible exactly from the JSON's own ω*, but a bit-exact end-to-end regeneration is not
  attainable because it requires a specific lucky 32² draw.
- **Run-to-run statistics over all 21 realizations** (19 fresh + 2 committed):

| estimator | range | spread |
|---|---|---|
| 3-point slope (4, 8, 16) — the JSON's fit | 4.173919 … 4.183199 | **0.22 %** |
| 4-point slope (4, 8, 16, 32) — the TXT's fit | 4.6426 … 7.1648 | **49.2 %** |
| ε_Δ | 4.5505e-11 … 4.6790e-11 | 2.6 % |
| ω(4×4) | 1.164855406907999 | **bit-identical in all 21** |

- **Two formal runs are not byte-identical and not numerically identical** (txt sha
  `56076a7a…` vs `b4c87870…`; json sha `8273f6cc…` vs `865f2846…`). This is expected and is now a
  documented property of the 5i block, not a defect of the pair.

## 4. Governing value — decision by provenance and evidence (task Part 3, policy A)

**Policy A applies**: JSON and TXT are produced by the same current authoritative script from the
same frozen inputs; the divergence is a generation/reporting inconsistency (two different
executions were committed as a pair, and the fit-subset rule is sensitive to a nondeterministic
datum).

**Governing artifact: the JSON** — `slope = 4.173919246515192`, `CI95 = [3.1453687594104447,
5.202469733619939]`, `ε_Δ = 4.6318154949690315e-11`, `note = "no theoretical order claimed"`.
This is *not* a preference for JSON; it is established by three independent pieces of evidence:

1. **Provenance**: the committed record `P4B_5g_5i.md` designates the reported observed slope
   (4.17, CI [3.15, 5.20]) and 16→32 change 4.6e-11 as "run 2", and only the JSON matches run 2
   (max |Δω| = 2.1e-13 against the other committed run).
2. **Consumption**: the JSON is the machine-readable artifact every downstream consumer reads —
   `tables/gen/tab04_consistency_suite.py`, `tables/gen/tab06_convergence_floor.py`,
   `figures/gen/fig05_mesh_convergence.py`, `production/p5/p5_core.py`, the P4A/P4B guards and the
   manuscript tables/figures. Nothing in the repository consumes the TXT; it is prose evidence.
3. **Reproducibility of the quantity**: the JSON reports the **3-point fit**, whose value across 21
   realizations varies by 0.22 % (4.1739–4.1832) and is therefore a reproducible metric. The TXT
   reports the **4-point fit**, which includes the noise-limited 32² datum and whose value varies by
   49 % across the same realizations — it is not a reproducible metric and must not be cited.

**The TXT is preserved, byte-identical, as historical run-1 stdout evidence** and is now explicitly
labelled (`p4b_5g_to_5i.txt.provenance.md`); its 5.4857 / 4.626e-11 remain on record as the run-1
output. No file was rewritten, no number was changed, and the P4B script was not modified.

## 5. P4B 5i criterion audit (task Part 4)

| question | finding |
|---|---|
| exact sequence | homogeneous Case-H acoustic ω_T at k̄ = (0.31π/L, 0.22π/L), meshes n = 4, 8, 16, 32 (h = 1/n); closed form ω_ex = 1.164855389329 (M11.3) |
| genuinely monotonic? | **yes** in every one of the 21 realizations (errs strictly decreasing); note the script does **not** *test* monotonicity, it is an observed property (plan row 5i lists "monotone convergence" as the expected outcome) |
| fitted quantity | log(relative error in ω_T) vs log(h); ordinary least squares; 95 % CI via Student-t with dof = n−2 |
| mesh levels included | all four are *computed*; the *fit* uses the subset with rel err > 1e-14 (3 or 4 points depending on the draw) |
| floor as threshold or derived? | **derived from the same data**: ε_Δ := max(\|ω₃₂−ω₁₆\|/ω₃₂, err₃₂). (The plan's *candidate* definition was max over IBZ of \|ω(32²)−ω(extrapolated)\| with "final wording fixed when computed"; ω(16²) is the locked stand-in for the extrapolation, justified because the 16²→32² change ≈ 4.6e-11 is orders below the reported gap quantities.) |
| tautological acceptance? | **yes, one of the three 5i checks**: "16²→32² relative change ≤ ε_Δ" cannot fail, because ε_Δ is defined as the max that includes that very change (d16_32 = ε_Δ in both runs). This is inherited from the plan's own row-5i wording, faithfully implemented by the script — documented here, **not silently modified** (criterion changes require authorisation). The other two 5i checks (`slope` finite; `ε_Δ` finite) are sanity checks, not scientific discriminators; P4B's PASS/FAIL never depended on the disputed slope value (21/21 PASS in both runs and in all 19 fresh runs). |
| slope descriptive only? | yes — the JSON/record explicitly carry `note = "no theoretical order claimed"` |
| theoretical order claimed? | **no** anywhere: the script, the JSON, the record, Table 6 and the manuscript all state the empirical rate with its CI and the explicit disclaimer; the manuscript's Figure 5/Table 6 use the corresponding **ε_Δ = 4.63e-11**. |

## 6. Manuscript cross-check (task Part 7)

- "5.4857" / "5.485" occurs **nowhere** in `latex/`, `tables/out/`, `figures/` (checked).
- The manuscript states p = 4.17 with CI [3.15, 5.20] (`ms.tex` abstract, `sec05_verification.tex`
  eq. line 108, `sec09_conclusions.tex`), i.e. exactly the governing JSON values; `tables/out/tab06`
  uses the governing ω/rel-err rows and the ε_Δ footer 4.63e-11; `tables/out/tab02_parameters.tex`
  cites "[A] P4B 5i mesh convergence study (commit 1581497)" for ε_Δ = 4.63e-11.
- "no theoretical order claimed" is present in the abstract (Part C fix) and in the JSON note.
- ΔP4B related hidden dependencies: `production/p5/p5_core.py` reads the JSON (not the TXT) ✓.

**Conclusion of the cross-check**: all active manuscript claims correspond to the governing JSON;
the divergent TXT value appears only inside the labelled historical TXT itself and in the audit
documents that discuss this blocker.

## 7. Explicitly not done

- `p4b_5g_to_5i.py` **not modified** (scientific engine; the changes below are *recommendations*
  requiring authorisation): (a) pass an explicit `v0` (or otherwise pin the start vector) so that
  runs are reproducible; (b) make the fit-subset cut self-documenting — the inline comment says
  "points above 10*min_err" while the code applies a fixed `e > 1e-14`; (c) decide whether the
  definitional check "d16→32 ≤ ε_Δ" should be replaced by a non-tautological criterion.
- `p4b_5g_to_5i.json` and `p4b_5g_to_5i.txt` **not modified** (byte-identical to `1581497`).
- No new P4B calculation was added to the repository as evidence-of-record; the reproduction runs
  live only in `audit/evidence/p4b_b1/` with their hashes.
- No P12E artifact was reconstructed, imported or invented.

## 8. Evidence hashes

```
p4b_5g_to_5i.json   383843632e317c219b4df68fdf8fd875a117cf3cde35babf14b75f6c6a8ee185 (unchanged)
p4b_5g_to_5i.txt    1daf0f322260327919ee321f0a88d308f637a1c0e6473af5fcccbc56c69b2263 (unchanged)
p4b_5g_to_5i.py     b1c8d9963b14a19e0f62b29434811635f9a8d721133987b87d8e25882516f6a0 (unchanged)
formal_A.txt        56076a7a54aab825fd5701855f9dbc348c61b1747e8bbc85815dae7c221cc700
formal_B.txt        b4c87870cbeb32aa3377bb27e7405d71ff849f5d6c371d3c2acd930701765ff8
formal_A.json       8273f6cce6dd8ad893d9afd65364a678174ee45124eee33cd9ecee36d79ae844
formal_B.json       865f2846b7eba0ac1ee412ae7dd489fcd4cf3120c9cd6c00977d9adf5a3b2c2c
```
