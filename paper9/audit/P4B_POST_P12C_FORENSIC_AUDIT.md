# P4B Post-P12C Forensic Audit (Part E)

Base `phase-1-symbolic @ 0d985029` · 2026-09-24 · **sandbox state: pre-P12E**.
Question set: is the P4B 5g–5i evidence set internally consistent, which artefact governs
each downstream number, and are the task-prompt's quoted values verifiable here?

## 1. Files present vs absent

| artefact | sha256 | status |
|---|---|---|
| `verification/suite/p4b_5g_to_5i.py` | `b1c8d9963b14a19e…` | present (generator; writes json + txt) |
| `verification/suite/p4b_5g_to_5i.json` | `383843632e317c21…` | present — **governs** tables 4/6, fig 5, manuscript |
| `verification/suite/p4b_5g_to_5i.txt` | `1daf0f3222603279…` | present — run log (older execution) |
| `verification/suite/P4B_5g_5i.md` | `5ce552ba88b56174…` | present (P4B record; equals the recovery-report's *pre-P12E archive* hash) |
| `archive/P4B_5g_5i_pre_P12E.md`, `archive/p4b_5g_to_5i_committed_conflict_20260923.*`, `test_p12e_remediation.py` | — | **absent** (P12E artefacts not in this tree) |

## 2. Task-prompt P12E values — verifiability

Strict full-literal search (`grep -rl`) for `4.71578752682248`, `3.377399590254491`,
`6.054175463390468`, `4.6619906233888485e-11`: **0 files each**.
⇒ The prompt's claimed P12E remediation values (slope ≈ 4.71578752682248; CI
[3.377399590254491, 6.054175463390468]; ε ≈ 4.6619906233888485e-11) **cannot be verified in
this sandbox and were not used anywhere in this audit**. Whatever P12E did remains outside
this tree; no value was imported.

## 3. The in-tree P4B numbers and the json↔txt conflict (open)

| quantity | JSON (governing) | TXT run log | manuscript |
|---|---|---|---|
| LSQ slope | **4.173919246515192** | 5.4857 | 4.17 ✓ (json) |
| 95 % CI | **[3.1453687594104, 5.2024697336199]** | [2.2301, 8.7413] | [3.15, 5.20] ✓ (json) |
| ε_Δ | **4.6318154949690315e-11** | 4.626173e-11 | 4.63e-11 ✓ (json) |
| 16²→32² rel change | 4.6318154949690315e-11 | 4.626173146257483e-11 | — |
| rel err series (4,8,16,32) | 1.5091e-8, 7.5865e-10, 4.6321e-11, 2.4781e-15 | (journaled similarly) | Table 6 rows ✓ |
| ω_T series | 1.164855406908, 1.164855390213, 1.164855389383, 1.164855389329 | — | Table 6 ✓ |
| floor_flag | true | true (`floor=True`) | — |

**E-F1 (open conflict; RESOLVED 2026-09-24 — see the resolution addendum below and
`P4B_B1_RESOLUTION_CLOSEOUT.md`).** The two committed artefacts are executions of the same suite that
disagree in the near-floor regime (ω values differ at ~1e-15 roundoff; the *differences* of
interest are ~5e-11, so the derived slope/ε_Δ differ: 4.17 vs 5.49; 4.6318e-11 vs 4.6262e-11).
This is precisely the pre-P12E "committed conflict" that P12E was created to reconcile; it
remains **unresolved in this tree**. Resolution is **not attempted here** (no P12E context, no
new runs permitted; raw logs are history). Downstream consumers (`tab04`, `tab06`, `fig05`)
read **only the JSON**, so the manuscript/table/figure set is internally consistent with the
JSON; the TXT is a divergent log.

## 4. Definitional audit of ε_Δ (E-F2 → corrected)

- Definition in the JSON/Table 6/P4B md: ε_Δ := max(|ω_T(32)−ω_T(16)|/ω_T(32), rel-err₃₂)
  = **4.6318e-11** (it equals the *relative* change; rel-err₃₂ = 2.4781e-15 is smaller). ✓
- The manuscript's display equation wrote the **absolute** difference formula as if it gave
  4.63×10⁻¹¹ (the absolute difference is 5.40×10⁻¹¹). **Corrected** to
  `ε_Δ = |ω̄_T^(32) − ω̄_T^(16)| / ω̄_T^(32) = 4.63×10⁻¹¹` (guard
  `test_p8_remediation.py::test_find08_operational_resolution_floor_notation` still passes).
- All other manuscript uses of ε_Δ are relative-quantity comparisons ✓ (8-orders-of-magnitude
  claim: smallest reported gap 0.0431 ≫ 4.63e-11 by ~9.3 orders).

## 5. 5g acceptance subset (prompt claim: k̄ = {0.2, 0.5})

- Script: `ks_fe = [0.2π/L, 0.5π/L, 0.8π/L, π/L]`; `ks_fe_tol = ks_fe[:2]` → criterion subset
  **{0.2, 0.5}** ✓ (matches the prompt claim; present already pre-P12E).
- JSON 5g block stores `FE_max_rel = 1.6219e-3` — that is the **all-κ maximum** (κ=0.8), *not*
  the criterion value (criterion max = 1.63e-4 < 1e-3). Documented (E-F3, inert) so the two
  numbers are not confused in future audits.
- Other 5g evidence (json): `vinf_T = 0.3162277660168379`; `ellbar_gt0_monotone = true`;
  bounded-branch ratios 1.730 → 2.849e-4; ℓ̄=0 branch |ratio−1| = 3.17e-4; FE ℓ̄=0 monotone
  (1.00079 → 1.02046) ✓ consistent with `P4B_5g_5i.md`.

## 6. 5i criterion audit

- Observable: acoustic ω_T at fixed k = (0.31π/L, 0.22π/L) vs the M11.3 closed form
  (k recorded in JSON `5i.k`; script lines confirmed; Part C fixed the manuscript's
  previously wrong configuration description).
- Monotonic criterion: `16²→32² relative change ≤ ε_Δ` — check present and PASS
  (rel = 4.631815e-11 = ε_Δ, equality by construction).
- `floor_flag` heuristic (`errs[-1] < 1e-12 or (ratio>0.5 and errs[-1]<1e-8)`) governs the LSQ
  fit set ("use" list); residual observation: 4 points / 3 mesh gaps, nfit = 4 in the txt.
  Heuristic nature is documented in the P4B record and remains as-is.
- CI and slope are reported as *observed*, with “no theoretical order claimed” in JSON note,
  Table 6 footer, and (after Part C) the abstract.

## 7. Table 6 availability

`tables/out/tab06_convergence_floor.tex` is present and git-tracked; generated by
`tables/gen/tab06_convergence_floor.py` from the JSON. Values verified line-by-line against the
JSON (ω_T series, relative errors, ε_Δ definition, p = 4.17 CI [3.15, 5.20], “no theoretical
order claimed”). ✓

## 8. Verdict for Part E

- Manuscript numbers are consistent with the governing JSON; one definitional display equation
  corrected; no edits to `p4b_5g_to_5i.{json,txt,py,md}`.
- **Blocker (carried to Part K):** the json↔txt divergence (E-F1) is an unresolved P4B
  evidence-quality issue in this tree; it predates P12C (P12E-era work was to resolve it and is
  out of scope here). Release-readiness cannot treat the P4B record as fully reconciled.


---

## Resolution addendum — E-F1 / B1 (appended 2026-09-24; no earlier text altered)

B1 has been **resolved** by executable provenance (`P4B_B1_PROVENANCE_RECONCILIATION.md`,
`P4B_B1_RESOLUTION_CLOSEOUT.md`, evidence in `audit/evidence/p4b_b1/`):

- the TXT and the JSON are **two executions of the same committed script** (`p4b_5g_to_5i.py`) with
  identical frozen `[S-P4A]` inputs — TXT = run 1 stdout, JSON = run 2 (the run the record
  `P4B_5g_5i.md` designates as the reported slope);
- the 5i eigensolve is called without a start vector, so ω(32²) lands unpredictably on either side
  of the script's fixed `err > 1e-14` fit-subset cut: 1.2009e-13 in run 1 (4-point fit → slope
  5.4857) vs 2.4781e-15 in run 2 (3-point fit → slope 4.173919246515192);
- **the JSON governs** (provenance: it is run 2; consumption: every generator/test/p5 module reads
  it; reproducibility: its 3-point estimator spans 0.22 % across 21 realizations vs 49 % for the
  TXT's 4-point estimator). The TXT is preserved byte-identical and labelled
  (`p4b_5g_to_5i.txt.provenance.md`); no file or number was changed;
- guard added: `verification/suite/test_p4b_b1_json_txt_consistency.py` (8 tests, executed twice,
  both runs 8 passed with the opt-in end-to-end rerun). Manuscript verified to quote only the
  governing JSON values (no occurrence of 5.4857 / 4.626e-11 anywhere in `latex/`, `tables/out/`,
  `figures/`).

Consequently the E-F1 "do not quote the txt" caution remains in force for the *historical* TXT, but
B1 is no longer an open reconciliation blocker.
