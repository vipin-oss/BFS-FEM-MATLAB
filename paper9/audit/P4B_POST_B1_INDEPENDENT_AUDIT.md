# P4B Post-B1 — Independent Reproducibility + 5i Criterion Audit

Date 2026-09-24 · branch `phase-1-symbolic` · P12C base `0d9850290b63a5da81b098d999714ab621684c77` ·
B1 closeout HEAD at audit start `b6f372f4b4d775d1489407a4237da65d49d2eac4`.
No push · no P12E reconstruction · no P12C calculation · no Blueprint/main change ·
B1 evidence not modified · TXT and JSON neither regenerated nor reconciled · v0 not pinned ·
5i criterion not changed.

> **Environment note (procedural, not scientific).** On starting this task the sandbox had been
> re-provisioned: `paper9` content was intact and hash-verified, but `.git` **and every directory
> named `out/`** (i.e. `paper9/tables/out/`, `paper9/figures/out/`) had been dropped by the
> workspace snapshot. The 24 dropped files were restored **byte-identically** from an anonymous
> clone of the public remote at the exact base `0d985029` (no audit commit had ever touched them);
> `.git` ancestry was re-materialised afterwards (see §10–§11 and the closeout report). All audit
> content below comes from hash-verified files.

## 1. Scope

Independent verification of the B1 resolution (P4B `p4b_5g_to_5i.json` vs `p4b_5g_to_5i.txt`),
critical audit of the "JSON is authoritative" decision, mechanism audit of the 5i nondeterminism,
audit of the `err > 1e-14` fit cutoff and of the definitional 5i sub-check, a v0 recommendation,
manuscript cross-check, regression runs and immutability verification. No new scientific production;
no change to any evidence file; no test modified.

**Terminology used throughout (as required).**
*Artifact-level reproducibility* — the committed artifact's values can be re-derived from its own
data and its provenance is established. *Solver-level deterministic reproducibility* — independent
executions return bit-identical numbers. *Scientific validation* — independent physical/analytical
evidence confirms that the reported quantity measures what it claims. This audit finds the first
**established**, the second **not achieved** (per-call and per-configuration variation documented),
and the third **not claimed and not available from the 5i design**.

## 2. Evidence inspected

B1 documents (`P4B_B1_PROVENANCE_RECONCILIATION.md`, `P4B_B1_RESOLUTION_CLOSEOUT.md`,
`verification/suite/P4B_5g_5i.md` + its append-only addendum, `p4b_5g_to_5i.txt.provenance.md`);
`verification/suite/p4b_5g_to_5i.{py,json,txt}`; the B1 guard
(`test_p4b_b1_json_txt_consistency.py`); the evidence bundle
(`audit/evidence/p4b_b1/`, incl. 21 realizations, formal runs A/B, nondeterminism probes);
P4A module `p4a_5a_to_5f.py`; `P4A_5a_5f.md`; plan row 5i (`plan/CALC_MASTER_PLAN.md`);
manuscript (`latex/ms.tex`, `latex/sections/*.tex`, `tables/out/*.tex`, `figures/gen/*.py`);
consumers (`tab04`, `tab06`, `fig05`, `production/p5/p5_core.py`); and — because `.git` was lost —
an anonymous clone of the public remote at the exact pushed base `0d985029` as the parent reference.

All verification was executed with freshly written code (`/home/user/p4b_post_b1_logs/
independent_verify.py`), not by re-importing the guard or any repository helper.

## 3. B1 provenance verification (claims A–H, independently re-derived)

| # | claim | method | result |
|---|---|---|---|
| A | TXT = run 1 | `git log --follow` (single commit `1581497`); TXT footer `wrote /tmp/bfs-repo/…`; record's "two consecutive executions · max \|Δω\| = 2.1e-13" vs measured TXT↔JSON max \|Δω\| = **2.085e-13** | **consistent** — TXT is the companion execution of the pair. *Residual:* the label "run 1" is a convention (the TXT carries no timestamp; "run 1" vs a hypothetical later run cannot be distinguished from the artifact alone). |
| B | JSON = run 2 | record designates the reported slope (4.17; CI [3.15, 5.20]) and 16→32 change ≈ 4.6e-11 as "run 2"; only the JSON matches (slope 4.173919246515192, d16_32 = 4.6318154949690315e-11) | **confirmed** |
| C | same committed script | JSON key set ≡ the script's `out` dict keys exactly (19 keys, no extras/missing); 5 full-precision 5g/5h tokens appear verbatim in the TXT and equal the JSON values; `params [S-P4A]` dicts identical; single P4B script in the repo (one commit) | **confirmed** |
| D | frozen inputs identical | params dicts equal; `omega_exact = 1.164855389329` identical in both; ω(4×4) identical; all differences confined to ν = 8/16/32 digits at 7e-14…2e-13 | **confirmed** |
| E | cause = unpinned solver start vector | rel_err[3] = 1.2009e-13 (TXT) vs 2.4781e-15 (JSON) straddles the fixed `e > 1e-14` cut; `eigsh(..., which="SM", tol=1e-12)` is called **without v0** for nd > 128 (confirmed in code); v0-pinned calls are bit-identical (probe file) | **confirmed, with refinement** — see §4 |
| F | both slopes reproduce from their own arrays | fresh OLS (independent implementation): TXT → 5.4857096102, CI [2.2301413, 8.7412779], se 0.756581 (printed 5.4857 / [2.2301, 8.7413] / 0.7566); JSON → 4.173919246515192, CI [3.1453687594104447, 5.202469733619939] (stated values identical to the last digit) | **confirmed exactly** |
| G | JSON's 3-point fit stable | recomputed over all 21 documented realizations: **4.173919 … 4.183199 (0.222 %)**; unchanged (0.222 %) when the one thread-pinned realization is excluded | **confirmed** |
| H | TXT's 4-point fit is the unstable branch | same 21 realizations: **4.6426 … 7.1648 (49.2 %)**; the committed TXT (5.4857) sits inside that family | **confirmed** |

**Two corrections to the B1 documents (recorded here; B1 files left unmodified per instruction).**

1. **ω(4×4) bit-identity is overstated.** Both B1 documents state ω(4×4) = `1.164855406907999` is
   "bit-identical … in all 21 sandbox realizations". It is bit-identical in the **committed TXT,
   the committed JSON and the 20 default-configuration realizations**; the 21st realization
   (`seeded_s04`, = the `OMP_NUM_THREADS=1` probe run of the B1 session) has
   `1.1648554069080328`. This audit reproduced that exact value bit-for-bit by running the n = 4
   solve with `OMP_NUM_THREADS=1` (3/3), while the default configuration reproduces
   `…607999` (3/3) even though the sandbox instance is different from the B1 session's. Correct
   statement: *ω(4×4) is bit-identical within a fixed thread configuration and identical across
   sandbox instances under the default configuration; it is last-bit sensitive to BLAS thread
   configuration.* Impact: none on B1 (ω(4×4) carries rel. error 1.5e-8 and never approaches the
   cut).
2. **Consumer list wording.** The B1 audit lists "the P4A/P4B guards" among JSON consumers. The
   P4A/P4B pytest file imports the **module** (`p4b_5g_to_5i.py`), not the JSON. Actual JSON
   readers: `figures/gen/fig05_mesh_convergence.py`, `production/p5/p5_core.py`,
   `tables/gen/tab04_consistency_suite.py`, `tables/gen/tab06_convergence_floor.py`, the script
   itself, and the new B1 guard (which additionally pins its hash). The conclusion is unaffected —
   three substantive scientific consumers remain.

*A third observation from this audit (not a B1 error):* a one-ulp input difference changes the
answer at the same scale as the effects under discussion. My first probe passed `ell2 = 0.04`
directly, whereas the script passes `ell**2 = np.sqrt(0.04)**2` (1 ulp apart); the probe returned
`1.164855406908048`, a value that does not occur in any real run. Bit-level comparisons require
bit-level input fidelity.

## 4. JSON/TXT divergence mechanism (independent verification)

Verified chain: same script → same frozen inputs → 5i eigenproblem at n = 8, 16, 32 solved by
`eigsh(which="SM", tol=1e-12)` **without a start vector** (n = 4 takes the dense LAPACK branch,
nd = 128 ≤ 128) → per-call variation of ω(32²) at the 1e-13–1e-15 level → the fixed
`err > 1e-14` fit-subset predicate flips between 4 points and 3 points → slope 5.4857 vs
4.173919246515192.

Supporting facts, all re-derived here: the matrix/operator is unchanged (identical code path, params
and every shared output digit); the eigenvalue differences are at solver-numerical level
(7.3e-14 … 2.1e-13); the identified branch is unchanged (all values agree with the M11.3 closed form
to ≤8.4e-13 relative; no swap, no physical eigenbranch change — ω̄_T stays 1.1648553893xx in every
run); and only the fit-selection predicate differs.

Refinement from §3.1: within one environment the iterative solver's start vector is the demonstrated
source of run-to-run variation, but last bits are also **configuration-dependent** (dense n = 4
differs between default and thread-pinned runs, bit-reproducible within each configuration). The
divergence between the committed TXT and JSON is fully explained by the start-vector mechanism; the
global E–H mechanism claim of the B1 audit is thereby substantiated, not weakened.

## 5. "JSON is authoritative": artifact governance vs scientific preference

**What the three grounds actually establish.**

1. *Provenance (JSON = documented run 2)* — establishes **artifact governance**: within the project's
   evidence record, the JSON is the artifact designated as the reported run of row 5i.
2. *Consumption (tab04/tab06/fig05/p5_core/B1 guard read only the JSON)* — establishes **artifact
   governance** as well: the JSON is the operative record; the TXT is historical stdout.
3. *Stability (3-point estimator 0.22 % vs 4-point 49.2 %)* — establishes a **reproducibility
   property of the estimator**, not of the physical claim.

**Determination.** Grounds 1–2 are governance-valid and sufficient for the decision "the JSON is the
current authoritative artifact". Ground 3 does **not** upgrade this to "scientifically preferred
estimate" in the sense of scientific validation, but it does support a *methodological* preference:

- the datum excluded by the 3-point fit is demonstrably **not a discretization-error sample**:
  with *identical inputs* it ranges over 2.48e-15 … 8.43e-13 (×340) across realizations, and the
  governing value sits **1000× below** the error the 3-point fit itself predicts at that mesh
  (3-pt fit → 2.484e-12; observed 2.478e-15). A deterministic discretization error cannot vary with
  the RNG; this datum is solver-accuracy-limited;
- hence the 3-point estimate is the one that rests entirely on the discretization-dominated part of
  the sequence, and the 4-point estimate mixes a trend with a solver-noise dato.

**But the honest limits must be stated:**

- "scientifically preferred" here means "more defensible as a *descriptive* statistic under the
  current solver" — it is **not** evidence about the true convergence behaviour, and it is **not**
  scientific validation of p = 4.17;
- the governing artifact is the **rare branch** (1 of 21 documented realizations took the 3-point
  branch — the committed run 2 itself). A fresh end-to-end run normally reports the unstable 4-point
  value (4.64 … 7.16). **Pipeline-level reproducibility of the manuscript's 4.17 is therefore not
  achieved**; what is reproducible is (i) the JSON's value from its own arrays and (ii) the stable
  3-point estimator (0.22 %) when computed by the script's own rule;
- with dof = 1 the 3-point CI [3.15, 5.20] is very wide; both competitor values (4.17, 5.49) lie
  within it. The number is descriptive; the manuscript's "no theoretical order claimed" caveat
  (abstract) is the correct framing.

**Consequence for the B1 decision:** *governance-valid*; additionally *supported* by an
estimator-stability argument that is documented, not validated. No re-decision is required; the
residual reproducibility exposure is recorded as blocker R-1 (§12).

## 6. The `err > 1e-14` fit cutoff

**Purpose and character.** The cut excludes fit points that sit at the solver/resolution floor from
the log-log LSQ — scientifically reasonable *in intent* (rate fits should not be dominated by
roundoff-limited points). Its **value** is not derived from anything in the project: it is not
machine-epsilon (2.2e-16), not tied to the solver tolerance declared in the same section
(`tol=1e-12` on λ = ω², i.e. ≈5e-13 at ω level), not resolution-dependent and not documented in the
plan (row 5i specifies the meshes, the fit and ε_Δ, but no fit-subset rule). Introduced with the
single `1581497` commit, never adjusted. Classification: **inherited arbitrary constant that acts as
a solver-noise threshold** — and precisely because the 32² noise straddles it, it silently controls
which estimator is reported.

**Documentation drift — and it is not inert.** The comment above the code says
*"LSQ only on points above 10*min_err"*; the code implements a fixed `e > 1e-14`. Counterfactual
computed here:

| run | min err | 10·min err | points under code rule | slope | points under the commented rule | slope |
|---|---|---|---|---|---|---|
| TXT (run 1) | 1.2009e-13 | 1.2009e-12 | 4 | 5.4857 | **3** | **4.1767** |
| JSON (run 2) | 2.4781e-15 | 2.4781e-14 | 3 | 4.1739 | 3 | 4.1739 |

Had the code implemented the rule its own comment names, **both runs would have fitted 3 points**
(4.1767 and 4.1739) and the B1 divergence would never have occurred. The drift is therefore
execution-relevant, not merely cosmetic. Not modified (criterion change requires authorisation).

## 7. The definitional 5i sub-check — classification

**Classification: C — tautological/derived.** Formally, the check is
`d16_32 ≤ ε_Δ + 1e-30` with `ε_Δ ≡ max(d16_32, err32)`, i.e. `d16_32 ≤ max(d16_32, err32)` — true for
any finite data; verified empirically that `d16_32 == ε_Δ` to the last bit in both runs
(4.6261731462574832e-11 / 4.6318154949690315e-11). Its only failure mode is non-finite input.

Block-level consequence (recorded, not changed): the other three 5i checks assert only finiteness
(the four ω values exist and are finite; the slope is finite; ε_Δ is finite — the last two fail only
if fewer than three points survive the cut). `floor_flag` is computed and reported but used in no
assertion. **Row 5i therefore has no non-trivial acceptance predicate; P4B's PASS for 5i is
structural.** Its scientific value lies in the recorded numbers and in ε_Δ being definition-locked,
not in a discriminating test. The plan's expectation "monotone convergence" is *not* tested by the
script (it is, however, factually true in all 21 realizations — verified here).

## 8. Should v0 be pinned? — recommendation only

| question | assessment |
|---|---|
| improves reproducibility? | Yes, **per configuration**: identical matrices and an explicit `v0` reproduced bit-identical results in three consecutive calls (0.0 difference), and the default configuration reproduced the committed bits across sandbox instances. |
| alters the scientific estimator? | Not its definition; it changes **which realization is reported**. If the pinned draw lands above the 1e-14 cut, the reported slope becomes a 4-point value (≈4.6–7.2) and the manuscript's 4.17/CI would have to be re-baselined. |
| removes the fit-branch ambiguity? | Only for the pinned configuration. It freezes *this* draw; it does not remove the data-dependent subset selection. Thread configuration also matters (demonstrated for the dense path), so cross-environment bit-stability cannot be promised by v0 alone. |
| requires a Blueprint change? | No — implementation detail; no gate or definition changes. |
| requires regeneration / re-baselining? | **Yes** if adopted: new governing JSON, new guard hash pins, record update, manuscript CI re-check. The historical run-1/run-2 pair remains valid as (unpinned) history. |
| invalidates run1/run2 provenance? | No. It makes future runs non-comparable bit-wise with the historical pair, which the record must note. |

**Recommendation (deferred, needs authorisation).** Treat v0 pinning and the subset rule as **one**
hardening package, in this order: (1) pre-declare the fit-subset rule (a principled rule — e.g. fit
4², 8², 16² and report 32² as the floor datum, or a noise-threshold rule derived from `tol`), so the
reported estimator no longer depends on a noisy predicate; (2) then optionally pin `v0` (and, if
bit-identity is wanted, the thread count) for bit-reproducibility; (3) re-baseline once: regenerate
the governing artifact, update the record and guard pins, re-check the manuscript's p/CI; (4) only
then may "pipeline-level reproducibility" be claimed. Doing (2) alone would be cosmetic and would
change the reported number without fixing the design.

## 9. Manuscript cross-check

Terms scanned in `latex/`, `tables/out/`, `figures/`:

| term | hits | assessment |
|---|---|---|
| `4.173919246515192`, `4.1739` | 0 / 0 | full precision not quoted (fine) |
| `3.145`, `5.202` | 0 / 0 | CI quoted only as [3.15, 5.20] = correct rounding of [3.1454, 5.2025] |
| `4.6318154949690315`, `4.63` | 0 / 4 | ε_Δ quoted as 4.63e-11 (ms.tex abstract, sec05 eq. (5.7), fig. 5 caption, sec09, Table 2 row, Table 6 footer) — matches the JSON |
| `5.4857`, `5.485`, `4.626…e-11` | 0 / 0 / 0 | **historical run-1 values never quoted** |
| `convergence order` | 0 | — |
| `fourth-order` | 1 | `sec03_bloch.tex:30` — "fourth-order gradient elasticity discretizations" (the *model/discretization*, not a convergence-order claim). No finding. |
| `empirical slope` | 0 | wording used: "observed empirical convergence rate" / "empirical least-squares rate" (sec05:106, sec09:8) — acceptable |
| `resolution floor` | 7 | ms.tex, sec05 (twice incl. Table 6 caption), sec09 — consistent with the JSON |

Additional verifications: the "no theoretical order claimed" caveat is present in the abstract
(ms.tex); sec05 states the rate as "observed empirical … of p = 4.17 (95 % CI [3.15, 5.20])" and
does not itself repeat the caveat (acceptable: the claim language is empirical throughout);
"Monotone mesh convergence across 4² to 32²" (sec09:8) is factually supported — rel. errors are
strictly decreasing in **21/21** documented realizations; the sec05 claim that reported gaps exceed
ε_Δ "by at least eight orders of magnitude" checks out (smallest gap quoted in text, 0.0431, gives
log₁₀ = 8.97).

**One non-blocking wording note (no edit made).** sec05 writes the fit model as
`Δω̄(h) − Δω̄(h_min) = C h^p` (finest-mesh reference), while the implemented estimator fits the
relative error against the **closed-form** M11.3 value with no offset. Because the finest mesh
resolves the closed form to 2.5e-15 relative, the two conventions differ by only 3.9e-5 in p
(4.173919 vs 4.173958) — i.e. numerically equivalent at the quoted precision, but the wording is
imprecise. Recommended (deferred): align the wording in a future editorial pass. No inconsistency
in any quoted number; nothing rewritten.

## 10. Regression results

Logs: `/home/user/p4b_post_b1_logs/` (kept **outside** the repository so the single focused commit
contains only the audit document; sha256 of each log recorded in the session report).

**B1 guard, default mode (opt-in rerun skipped) — twice:**

| run | collected | passed | failed | skipped | exit | time |
|---|---|---|---|---|---|---|
| 1 | 8 | 7 | 0 | 1 | 0 | 0.10 s |
| 2 | 8 | 7 | 0 | 1 | 0 | 0.07 s |

**B1 guard, opt-in end-to-end rerun (`P4B_B1_FULL_RERUN=1`, default environment) — twice:**

| run | passed | failed | exit | time | note |
|---|---|---|---|---|---|
| 1 | 8 | 0 | 0 | 52.38 s | fresh run: 21/21 PASS, schema match, slope = its own fit, 3-pt estimator in band, ω(4×4) bit-equal |
| 2 | 8 | 0 | 0 | 59.69 s | same |

**B1 guard, opt-in rerun under a pinned-thread environment (`OMP_NUM_THREADS=1`) — fragility probe:**

| run | passed | failed | exit | failing assertion |
|---|---|---|---|---|
| 1 | 7 | 1 | 1 | `d["omega"][0] == rec["5i"]["omega"][0]` → 1.1648554069080328 vs 1.164855406907999 |

This is finding **G-1** (§12): the exact-bit cross-run assertion is configuration-sensitive (the
other seven assertions pass). Under the default configuration it passes — including in this
re-provisioned sandbox, which is itself evidence of cross-instance reproducibility at default
settings. Not modified (test changes require authorisation).

**Authoritative suite, `python3 -m pytest paper9/verification/suite/ -q`, twice.** Collection: **91
tests**. Two stages were measured because of the snapshot incident (§Environment note):

| stage | run | collected | passed | failed | skipped | exit | time | log sha256 |
|---|---|---|---|---|---|---|---|---|
| as-restored (before artifact restore) | 1 | 91 | 79 | **11** | 1 | 1 | 7.79 s | `9c0f23eb…` |
| as-restored | 2 | 91 | 79 | **11** | 1 | 1 | 6.92 s | `262da762…` |
| after byte-identical restore of the 24 dropped `*/out/` artifacts | 1 | 91 | **90** | 0 | 1 | 0 | 6.51 s | `678e7017…` |
| after restore | 2 | 91 | **90** | 0 | 1 | 0 | 6.66 s | `be95a19e…` |

All 11 failures were `FileNotFoundError`/missing-file assertions on generated outputs
(`figures/out/*.pdf`, `tables/out/*.tex`) — i.e. the snapshot-dropped files, not content errors. No
test was changed, skipped or weakened at any point. The 1 skip is the opt-in rerun (exercised
separately above).

**Guard efficacy (mutation testing, isolated copy tree — independent of any claim in the B1 docs):**

| variant | result |
|---|---|
| baseline copy | 7 passed, 1 skipped |
| JSON `slope` field tampered (4.173919… → 4.17) | **2 failed** |
| TXT byte-tampered (`5.4857` → `5.4858`) | **1 failed** |
| manuscript leaks run-1 value (append `5.4857` to a copy of ms.tex) | **1 failed** |
| reconciliation doc loses its "cannot fail" note | **1 failed** |

The guard detects every class of tampering it claims to detect. (Wart, recorded only: one assertion
depends on prose in `P4B_B1_PROVENANCE_RECONCILIATION.md`, and one line contains a vacuously
redundant `repr(...) in txt.replace(...)` expression — both harmless.)

## 11. Immutability results

`.git` loss meant no parent diff was possible; the parent reference used instead is an anonymous
clone of the public remote at the **exact pushed base `0d985029`**, compared file-by-file by SHA-256
(312 base files vs 345 working-tree files).

| check | result |
|---|---|
| files present in base but missing from the working tree | 24 — all under `paper9/figures/out/` (17) and `paper9/tables/out/` (7), dropped by the snapshot's `out/`-exclusion; **restored byte-identically** (24/24 hash match) |
| files differing from base | exactly **6**: `latex/ms.tex`, `sections/{sec04,sec05,sec06,sec08}.tex`, `verification/suite/P4B_5g_5i.md` — all previously committed audit content (Parts C/E corrections + the B1 append-only addendum) |
| everything else | byte-identical to base, including every protected item: |
| Blueprint v1.3 | `ca71b91aba4ca4ab…` ✔ identical |
| P12C raw JSONs | 32² `5547bae453964946…` ✔, 64² `c8910c0de2188b49…` ✔; sidecars verify (manual check; note the 64² sidecar is hash-only, hence not `sha256sum -c`-formatted) |
| P12C production scripts | `p12c_caseC_gap_convergence.py` `1b577c7e…`, `…_64.py` `160641da…`, `p12c_64_feasibility_probe.py` `e0b57706…` ✔ all identical |
| P11D raw evidence | `p11d_caseC_gap_convergence.json` `1d4476f1…` ✔, `p11d_deltaX_check.json` `7dbabbd3…` ✔ |
| historical P4B TXT | `1daf0f3222603279…` ✔ untouched; JSON `383843632e317c21…` ✔; script `b1c8d9963b14a19e…` ✔ |

No protected file changed.

## 12. Remaining scientific/governance blockers

- **R-1 (new; reproducibility exposure).** The manuscript's p = 4.17 is the value of the recorded run
  (the rare 3-point branch, 1/21); fresh default-configuration runs usually report an unstable
  4-point value (4.64–7.16). The value is artifact-reproducible and the estimator is stable
  (0.22 %), but the *pipeline* is not reproducible. Mitigation options in §8; no change made.
- **G-1 (new; guard fragility).** The opt-in guard's exact-bit ω(4×4) assertion fails under a
  pinned-thread environment (demonstrated: 1 failed / 7 passed with `OMP_NUM_THREADS=1`). Default
  configuration passes (×2 in this sandbox, ×2 in the previous one). Fix = relative tolerance or
  explicit thread pinning; requires authorisation.
- **C-1 (new; criterion design).** Row 5i has no non-trivial acceptance predicate (definitional
  sub-check + finiteness checks); the `1e-14` cut is an undocumented arbitrary constant whose
  comment names a different rule and whose behaviour decides which estimator is reported. The
  counterfactual shows the commented rule would have suppressed the B1 divergence entirely. No
  change made.
- **B1-E1/E2 (corrections to B1 documents, recorded here, documents unmodified):** ω(4×4)
  bit-identity overstated (20/21 realizations, configuration-dependent); consumer list wording.
- **Pre-existing and unchanged:** PCR1, G3, G4 **NOT MET**; P5 **NOT PASS/OPEN** (no release/final
  language permissible); P12E artifacts unverifiable in this sandbox.
- **Procedural (not scientific):** the workspace snapshot drops `.git` and every `*/out/` directory
  on re-provisioning; both were recovered here (byte-identical file restore from the public remote +
  local re-materialisation of the audit history). Downstream tasks should re-verify `git rev-parse`
  and the presence of `out/` artifacts at start.

**Bottom line.** B1's conclusion stands under independent verification — but it is an
**artifact-governance** resolution supported by a **reproducibility** argument, not a scientific
validation; the underlying 5i design remains non-discriminant and pipeline-level reproducibility of
the reported rate is not achieved. Two B1 statements are corrected above; no B1 evidence file, test,
criterion, or scientific source was modified.
