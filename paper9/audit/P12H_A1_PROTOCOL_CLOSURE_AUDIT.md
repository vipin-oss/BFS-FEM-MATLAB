# P12H — A1 Authorization, Blueprint v1.4 / Plan Amendment, and Protocol Closure Audit

**Phase:** P12H (branch `phase-1-symbolic`; `main` untouched) · **Date:** 2026-09-24
**Start SHA:** `2225cdc5c3189e056264229a0c3498f98207f344` (P12G; clean tree at entry)
**End SHA:** this commit — a file cannot embed its own commit hash; the SHA is printed in the final
P12H report and recorded in `paper9/audit/SANDBOX_GIT_RECOVERY_20260924.md` if a recovery occurs.
**Authorization in force:** **A1** — retain the governing numerical artifact; adopt the frozen P12G
**Rule R-fit** as the governing admissibility rule; apply the minimal Blueprint **v1.4** §5.7
amendment and the minimal plan 5i/PCR5 amendment.
**Explicitly NOT authorized (and not done):** the Route-F re-baseline (`4.180559`), any change to the
governing JSON/TXT numerical baseline, importing lost P12E values, P13, push.
**Environment:** python 3.13.14 · numpy 2.3.5 · scipy 1.17.1 · matplotlib 3.10.9 (unchanged from the
Part A manifest).
**Rule in force:** every claim traceable to an actual calculation; each gate status re-derived from
evidence, never promoted by assertion.

The governing numbers this audit preserves **unchanged**:

```
p  = 4.173919246515192
CI = [3.1453687594104447, 5.202469733619939]
ε_Δ = 4.6318154949690315e-11          "no theoretical order claimed"
```

---

## 1. Scope, decision record, and what this audit refuses to do

| Item | Status |
|---|---|
| Governing numerical artifact | **retained byte-identically** (`p4b_5g_to_5i.json` `38384363…`, `.txt` `1daf0f32…`, `.py` `b1c8d996…`, provenance `6154a23b…`) |
| Governing admissibility rule | **Rule R-fit** (frozen P12G; F = 3, strict; declared numerical zero 1e-15) — adopted as governing |
| Blueprint | **v1.4** created from v1.3 (4 edited blocks); **v1.3 preserved byte-identically** (`ca71b91a…`) |
| Plan | row 5i + PCR5 wording amended; one tautological sub-check removed |
| Manuscript | wording only — **no numerical change** |
| Floats | Table 6 extended (reproducibility/admissibility columns); Fig. 5 distinguishes fitted and excluded levels |
| R-1 | **OPEN** (§10) — closure was not forced |
| C-1 | **OPEN** (§9, §12) — criterion unchanged, now discriminant-tested |
| PCR1 / G3 / G4 / P5 | **NOT MET / NOT PASS** — unchanged (§11) |
| Route-F values in governed artifacts | **none** (§13) |
| Push | **not performed** |

This phase deliberately does **not** claim that the governing number became reproducible, that the
mesh sequence converged to fourth order, or that any previously unmet gate was met.

## 2. Part A — pre-change immutability manifest

`/home/user/p12h_logs/pre_change_manifest.json` (generator `manifest.py`, log `manifest_output.txt`):
HEAD `2225cdc`, branch `phase-1-symbolic`, empty `git status --porcelain` at entry; **20 protected
assets** with sha256, **3 tree hashes** (`paper9/latex` `a0f4fb8c…`, `paper9/tables/out` `eda2a0e2…`,
`paper9/figures/out` `2e21a83b…`), **46 audit-evidence files** across six evidence groups
(`p12d` 4, `p12e` 22, `p12f` 3, `p12g` 3, `p4b_b1` 7, `p4b_remediation` 7), and the host fingerprint.
Two pre-conditions were recorded and are re-verified post-change: the Route-F re-baseline is **not
installed**, and `4.180559` appears in **no** governed artifact.

## 3. Part B — Blueprint v1.4 (minimal §5.7 amendment)

`paper9/plan/blueprint/Paper9_Blueprint_v1.4.tex` (sha256 `0089754b076ff9e3…`) is derived from v1.3
by exactly **four** line-block edits, verified by opcode diff:

| # | v1.3 line | v1.4 content |
|---|---|---|
| 1 | 95 | version row → `1.4 --- LOCK; single amendment to §5.7 (… Rule R-fit …)` + provenance `sha256 ca71b91aba4ca4ab…` |
| 2 | 446 | §5.7 `[STR]` sentence → all four levels computed and reported; per-level admission by `e_i > F·max(s_i, 1e-15)`, `F = 3` strict, fixed **before** the calculation; excluded levels reported with `e_i`, `s_i`, ratio; identity of the excluded level stated in text, table and figure caption; 95 % CI reported; no theoretical order unless justified; **if fewer than three levels satisfy the criterion, no rate is reported** |
| 3 | 618 | verification-matrix row 5 → rate fitted from the levels that exceed the pre-declared criterion; number of fitted levels and any excluded level stated |
| 4 | 895–896 | PCR5 item → fit over the admissible levels; every excluded level reported with its error, reproducibility and ratio |

Preserved verbatim: the observed-LS-rate intent, the allocation bands at `4×4 … 32×32`, the
resolution-floor definition ("smallest gap width distinguishable from noise … allows weak anisotropy
effects to be claimed as real"), the CI requirement, and the no-theoretical-order clause. Removed:
the phrase "fitted by least squares **from the four refinement levels**", which A1 supersedes.
`v1.3` is byte-identical (`ca71b91a…`), so the historical specification is intact for audit.

## 4. Part C — plan amendment (row 5i and PCR5)

`paper9/plan/CALC_MASTER_PLAN.md` (`a45a5448a76764d5…`, pre-amendment `0e2c3a3a0e47d435…`):

- **Row 5i** now names per-level `e_i` and measured reproducibility `s_i` (two pre-registered start
  vectors, frozen configuration), the rule `e_i > F·max(s_i, 1e-15)` with pre-declared `F = 3`, the
  `< 3 admissible ⇒ no rate reported` clause, and states that ε_Δ is reported as the **operational
  mesh-change floor, distinct from the measurement resolution**.
- The former sub-check "16²→32² change ≤ ε_Δ" is **removed from the row**: it was satisfied by
  construction of `ε_Δ = max(that change, err32)` and verified nothing. It is replaced by the Rule
  R-fit admissibility record; the deletion is documented in the amendment note below the row (the
  original sentence survives only as a quotation of what was removed).
- The five now-distinct quantities are enumerated: (1) FE discretization trend, (2) measurement
  resolution `s_i`, (3) reproducibility spread as reported uncertainty, (4) observed convergence rate
  with 95 % CI and fitted subset, (5) reported ε_Δ.
- **PCR5** now reads: verify the reported rate is the LS fit of exactly the admissible levels; every
  excluded level is reported with `e_i`, `s_i` and the ratio; ε_Δ is reported as the operational
  mesh-change floor and is **not** presented as a measurement-resolution measure; no theoretical order
  is claimed. No other PCR definition was touched.

## 5. Part D — governance and traceability updates

- `paper9/verification/suite/P4B_5g_5i.md` — append-only **P12H addendum**; the original record text
  is untouched (`3ac49962…` → `8007a1bd…`). It states: the numerical result is unchanged; the
  *protocol* by which the fit subset is determined changed; the rule selects `{4², 8², 16²}` and
  reproduces the reported slope exactly; the former tautological sub-check is removed; Route-F values
  remain audit evidence only.
- `paper9/audit/traceability_matrix.csv` — four appended registry rows: `BP-v1.4`, `PLAN-5i`,
  `RFIT-1`, `RNAME-1` (no existing row edited).
- `paper9/audit/traceability_matrix.json` — metadata-only `p12h_amendment` block (blueprint/plan
  sha256 + pre-amendment plan sha256, the unchanged governing numbers, the Route-F disclaimer).
  `technical_variations` is untouched; `check_traceability.py` still reports 100 % of TVs closed.
- PCR5 **evidence pointers** now include the rule record, the rule module and the two new guard
  files; no numerical evidence was edited (46/46 evidence files byte-identical, §13).

## 6. Part E — baseline preservation and provenance statement

Recorded in `paper9/audit/evidence/p12h/rule_rfit_governing.json` (`provenance_statement`) and
repeated here as the authoritative statement:

> The governing JSON is the **numerical baseline** and is retained unchanged. Rule R-fit
> independently determines, from that artifact's own per-level errors and the era-matched
> reproducibility evidence, that its admissible subset is `{4, 8, 16}`; the resulting fit reproduces
> the governing value **bit-exactly**. The historical TXT output is retained as **historical
> evidence** and is not the numerical baseline. The Route-F configuration and its values
> (`4.180559`, ε_Δ `4.585037e-11`) are **audit evidence only** and appear in no governed artifact.

Consequently the reported `p` is neither re-derived from Route-F nor adjusted to any target: it is the
value that the retained artifact produces under the frozen rule.

## 7. Part F — manuscript wording (no numerical change)

| Location | Change | Numbers |
|---|---|---|
| `sec05` fit sentence (l. 106) | fit stated to run over the levels admissible under the pre-declared measurement-resolution rule; `4²`, `8²`, `16²` admissible, `32²` reported as resolution-limited | unchanged |
| `sec05` after the ε_Δ equation | added the distinction between the operational mesh-change floor and the finest-level measurement resolution | unchanged |
| `sec05` Fig. 5 caption | panel (a) distinguishes fitted levels (filled, dashed line) from the $32^2$ level (open marker, excluded because its error does not exceed three times its own reproducibility); floor described as operational and distinct | unchanged |
| `sec09` conclusion bullet | "confirmed … rate" → "supports an observed least-squares rate … fitted over the three admissible levels; the $32^2$ level is reported as resolution-limited and is not part of the fit" | unchanged |
| `ms.tex` abstract | rate qualified as fitted over the levels admissible under a pre-declared measurement-resolution rule | unchanged |

The wording never attributes the exclusion to how the rate changes, never claims a four-level fit,
never invokes a theoretical order or fourth-order convergence, and keeps `p = 4.17`,
CI `[3.15, 5.20]` and `ε_Δ = 4.63 × 10^{-11}` verbatim.

## 8. Part G — regenerated floats

**Table 6** (`tables/out/tab06_convergence_floor.tex` `343d93461eacf39c…`, generator
`5ee538589dcbe96c…`) — eight columns: mesh, elements, $h$, $\bar\omega_T$, relative error, step
variation, **reproducibility $s_i$**, **in rate fit?**; four rows of errors plus footers for the
closed-form frequency, the observed rate `p = 4.17` (CI, "no theoretical order claimed") with the
fitted subset named, and ε_Δ labelled "operational resolution floor (mesh change) — distinct from the
measurement reproducibility $s_i$".

| mesh | $e_i$ | $s_i$ | ratio | in fit |
|---|---|---|---|---|
| 4² | 1.51e-08 | 2.90e-14 | 5.208e+05 | yes |
| 8² | 7.59e-10 | 1.06e-13 | 7132 | yes |
| 16² | 4.63e-11 | 5.92e-13 | 78.24 | yes |
| 32² | 2.48e-15 | 1.26e-12 | 0.00196 | **no** (resolution-limited) |

**Figure 5** (`figures/out/fig05_mesh_convergence.pdf` `0b061d958ea62ed2…`, generator
`d1209c7dc6ad9dcb…`) — panel (a) plots the three admissible levels joined with the empirical fit and
shows the $32^2$ level as a distinct open marker labelled resolution-limited (excluded from the fit);
the operational floor and the measurement resolution are drawn as separate guide lines. Panel (b)
marks the finest step with hatched styling and a legend entry as the resolution-limited step. The
generator reads the rule record, so the displayed subset cannot drift from the governing decision.

## 9. Part H — C-1 validation and mutation coverage

**C-1 criterion (unchanged, P12E-authorized):** P1 strict monotone decrease; P2 `CI-lo ≥ 1.0`;
P3 `max |log-residual| ≤ ln 1.5`; P4 floor datum ≤ `1e-9`; ε_Δ reported, not an acceptance gate.

New permanent test file `verification/suite/test_p12h_c1_synthetic.py` (**23 tests**, all pass):
six required case classes — synthetic convergent (4th- and 2nd-order), flat plateau, oscillatory,
random noise, anti-convergent — each classified as required; each of P1–P4 individually shown able to
fail on its own falsifying case; three accepted sequences (incl. the marginal $p \approx 1.06$ and
the P4-exact boundary) keep all predicates true; the strictness of P1 pinned directly (an exactly
repeated error is not convergence). The known finding is preserved as a guard: the **four-level**
sequence still fails P3, which is the measured fact that motivates the rule.

**Rule R-fit adversarial set (P12G, frozen expectations):** B1–B8 classified exactly as
pre-declared, including the coupled pair B3/B4 whose inclusion CI-width NARROWS (28.55 → 4.33) in one
case and WIDENS (0.3475 → 5.07) in the other while **both are excluded** — the rule cannot be reading
the fit. A further test pins that the verdict is invariant to the surrounding trend.

**Mutations:** `paper9/verification/suite/rule_rfit.py` mutations **13/13 DETECTED**
(`/home/user/p12h_logs/mutation_rfit_output.txt`): F→2, F→4, floor→1e-12, strict→non-strict,
floor removed, `MIN_ADMISSIBLE`→2, seeds re-assigned, tol→1e-12, sets swapped, P2/P3/P4 thresholds
weakened, P1 made non-strict. Mutation R13 initially survived and exposed a **real coverage gap**
(nothing pinned P1's strictness directly); a direct strictness assertion was added — the gap was
closed by adding a test, **not** by weakening the criterion. The legacy staged matrix
(`audit/evidence/p12e/mutation_harness.py`) still reports **12/12 DETECTED**
(`/home/user/p12h_logs/p12e_mutation_rerun.txt`). No criterion constant was tuned in this phase.

## 10. Part I — R-1 assessment (stays OPEN; closure not forced)

Three distinct properties are separated (`/home/user/p12h_logs/r1_branch_stability.txt`):

| Property | Verdict | Basis |
|---|---|---|
| **A. solver-level reproducibility** (Route-F configuration) | established **for that configuration only** | P12E run1 ≡ run2 except the UTC stamp; audit evidence, not the governing configuration |
| **B. governing-artifact reproducibility** | **NOT established** | the governing artifact is one realization of an unpinned start vector at `tol = 1e-12`; its $32^2$ datum (2.478e-15) is **0.00196 ×** its own reproducibility (1.262e-12) — a fresh nominal run returns a different $32^2$ eigenvalue |
| **C. estimator-rule protocol determinism** | established | the rule maps recorded $(e_i, s_i)$ to a unique verdict, is applied identically to every k, reproduces the governing rate bit-exactly, and gives identical verdicts across a 273×-wide F-window |

R-1's recorded failure mode — the fit branch flipping with the solver realization under the deployed
`err > 1e-14` cut (21 documented realizations: 20 four-level, 1 three-level) — **is closed by
protocol**: replayed on that same family with the era-matched reproducibility, admission of the
$32^2$ level would require `e32 > 3.786e-12`, while the largest recorded realization gives
`e32 = 8.43e-13`; **no recorded realization admits it** (worst-case family margin 4.49×; at the
governing artifact itself the margin is 1527×). A counter-check preserves honesty: under the
*narrower, different-configuration* Route-F two-seed reproducibility (1.603e-13) the largest recorded
realization **would** be admitted, and a two-seed protocol has never been measured on the deployed
configuration — that absence *is* R-1.

**Verdict: R-1 remains OPEN.** Property B is unachieved and closing it requires the explicitly
unauthorized re-baseline. The estimator-branch closure must never be restated as solver or pipeline
determinism.

## 11. Part J — PCR and gate reassessment (re-derived, not promoted)

| Item | Status after P12H | Basis |
|---|---|---|
| **PCR5** | **PASS** (re-verified under the amended definition) | the reported rate is the LS fit of exactly the admissible levels (`{4²,8²,16²}`, rule re-derivation bit-exact); the excluded $32^2$ level is reported with `e_i`, `s_i` and ratio in text, Table 6 and Fig. 5; ε_Δ is reported as the operational mesh-change floor and is explicitly distinguished from the measurement resolution; no theoretical order is claimed (guard-enforced) |
| **PCR1** | **NOT PASS** | unchanged: external ≤ 2 % relative error remains uncomputable without author-released tables (G3) |
| **G1 / G2** | MET / MET | unchanged (symbolic evidence; suite green) |
| **G3** | **NOT MET** | unchanged hard gate — no author float tables; B2 length-scale ambiguity preserved, not resolved |
| **G4** | **NOT MET** | cannot be signed while G3/PCR1 are unmet; no file signs it |
| **P5** | **NOT PASS / OPEN** | unchanged — two parallel pipelines, no numeric cross-validation between them; the manuscript contains no P5-production claims |

Manuscript internal consistency was checked mechanically (§12, checks 1–4): Table 6, Figure 5 and
§5.3/§9/abstract now tell one story about the same three admissible levels and the single excluded
level, with identical numbers.

## 12. Part K — full regression (exact counts)

| Check | Command / artefact | Result |
|---|---|---|
| Full suite, run 1 | `pytest paper9/verification/suite -q` | **125 passed, 1 skipped in 6.57 s** |
| Full suite, run 2 | same | **125 passed, 1 skipped in 6.48 s** |
| New governance guards | `test_p12h_rule_rfit_governance.py` | **10 passed** |
| New C-1 / adversarial suite | `test_p12h_c1_synthetic.py` | **23 passed** |
| Legacy mutation matrix | `audit/evidence/p12e/mutation_harness.py` | **12/12 detected**, control PASS |
| Rule-module mutation matrix | `/home/user/p12h_logs/mutation_rfit.py` | **13/13 detected**, rule file restored byte-identically |
| Numerical cross-check + float/manuscript/Blueprint consistency | `/home/user/p12h_logs/final_verification.py` | **43/43 checks passed** (rule re-derivation bit-exact; tab06/fig05/Blueprint/plan/manuscript checks) |

Suite growth is exactly the 33 new tests (92 → 125 passed; the single skip is pre-existing and
unrelated). Logs: `/home/user/p12h_logs/suite_run{1,2}.txt`,
`paper9/audit/logs/p12h_suite_run{1,2}.txt`.

## 13. Part L — immutability verification

`/home/user/p12h_logs/immutability_check.py` → `immutability_output.txt`:

- 20 protected assets: **11 byte-identical**, **9 changed and all 9 authorized** (plan, ms.tex,
  sec05, sec09, tab06 generator/output, fig05 generator/output, P4B record addendum), **0 unexpected**.
- **46/46** audit-evidence files byte-identical (P12C raw, P12E staged patch and evidence intact).
- Anchors re-verified: Blueprint **v1.3** `ca71b91a…` (untouched), governing JSON `38384363…`,
  historical TXT `1daf0f32…`, script `b1c8d996…`, provenance `6154a23b…`, P12C 32²/64² raw
  `5547bae4…`/`c8910c0d…`, P11D `1d4476f1…`/`7dbabbd3…`, P12E patch `03b902d2…` → 0 failures.
- Three tree hashes changed, which is expected and confined to the authorized manuscript/float edits
  inside `paper9/latex`, `paper9/tables/out`, `paper9/figures/out`; the 24 generated `out/` artifacts
  required by the suite are present (7 tables + 17 figures).
- `4.180559` and `4.585037e-11` appear in **no** governed artifact (plan, v1.4, manuscript, Table 6,
  Fig. 5 generator, rule module, rule record).

## 14. Part N/O — final diff audit, commit, and remaining blockers

**Diff audit.** The change set is 11 modified + 6 added paths; each was reviewed against the A1 scope
and no unintended change was found: no numerical value in any governed artifact changed (JSON, TXT
and script untouched; `p`, CI, ε_Δ identical); no solver parameter, tolerance, seed or thread setting
changed anywhere outside the rule module's frozen constants; no subset selection logic was introduced
outside the rule; no Blueprint scope was broadened (v1.4 differs from v1.3 by exactly four blocks, all
inside §5.7, the matrix row and PCR5); language polishing is limited to the sentences listed in §7.

**Remaining blockers (unchanged by this phase):** PCR1 / G3 (author-released external numerical
tables), G4 (consequence of G3/PCR1), P5 (parallel-pipeline reconciliation), R-1 (pipeline-level
reproducibility — requires the unauthorized re-baseline), C-1 (criterion remains OPEN as a *gate*;
the discriminant predicate set is validated, not promoted).

**Five confirmations.**

1. **No Route-F re-baseline** was performed: the governing JSON/TXT/script are byte-identical and
   `4.180559` appears in no governed artifact.
2. **No P13** work was started.
3. **No P12E values were imported**: nothing was reconstructed, and the staged mirror remains
   non-governing audit evidence.
4. **Blueprint v1.3 is unmodified** (`ca71b91a…`); v1.4 carries explicit provenance.
5. **Nothing was pushed**; one focused commit on `phase-1-symbolic` only.
