# P12K — PCR1/G3 Blocker Forensic Audit (+ Remote Recovery Checkpoint)

**Phase:** P12K (forensic, read-only on science; branch `phase-1-symbolic`; `main` untouched)
**Date:** 2026-09-24 · **Baseline HEAD at entry:** `876213a8c4211ed4971735f6291a9a943f2dda24` (P12J), clean tree
**Repository:** `https://github.com/vipin-oss/BFS-FEM-MATLAB` · **Branch:** `phase-1-symbolic`
**Rule in force:** verify from source evidence; never fabricate or estimate missing external data;
never convert a graphical comparison into a numerical PASS; do not reopen closed issues without cause.

> **Remote checkpoint status — COMPLETE.** The push was performed with the same one-shot access
> point supplied for this phase (used inline only; never stored). `0d98502..476cac0` was delivered,
> then fetched and verified: **`origin/phase-1-symbolic = 476cac0c0b788b805563c766e3992ce2271b108b`**.
> All phases P12G–P12K are now recoverable from the remote branch alone. The anon-read-only
> constraint described in the first issue of this document no longer applies.

---

## 1. Verified remote recovery SHA

| Item | Value |
|---|---|
| Remote URL (authoritative recovery point) | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| Remote SHA at P12K entry (fetched, verified) | `0d9850290b63a5da81b098d999714ab621684c77` |
| **Remote SHA after the P12K push (verified)** | **`476cac0c0b788b805563c766e3992ce2271b108b`** |
| Local HEAD at P12K entry | `876213a8c4211ed4971735f6291a9a943f2dda24` (verified, tree clean) |
| Local commits not yet on the remote | P12G `2225cdc`, P12H `dd42e81`, P12I `1c6b2e3`, P12J `876213a`, P12K (this commit) |
| Remote recovery sufficiency | **MET** — remote equals local HEAD; no commit exists only in the sandbox |

## 2. Current baseline (locked; unchanged by this audit)

```
p        = 4.173919246515192
CI       = [3.1453687594104447, 5.202469733619939]
ε_Δ      = 4.6318154949690315e-11
admissible subset = {4², 8², 16²};  excluded = {32²};  "no theoretical order claimed"
```

Hash-verified at entry **and** after all work: Blueprint v1.3 `ca71b91a…` (byte-identical), Blueprint
v1.4 `2ae0b1e8…` (post-P12J), `rule_rfit.py` `d4fed492…`, governing JSON `38384363…`, historical TXT
`1daf0f32…`, P4B script `b1c8d996…`, P12E staged patch `03b902d2…`, P12C 32²/64² raw `5547bae4…` /
`c8910c0d…`. No Route-F value and no P12E numerical value appears in any governed artifact. Nothing
in this phase modified any of them.

## 3. PCR1 — exact authoritative definition

**Blueprint v1.4 §10.4, item 1** (enforcement point; "cannot be submitted until every line below is
true and evidenced in the computation log"):

> "All mandatory published benchmarks (Layers 1, 2a, 2b) PASS with maximum relative error $\le 2\%$;
> the $\le 2\%$ criterion is retained (the $0.5\%$ target applies only to the classical limit)."

Read with the §5.2 layer table, the quantities to be compared are **the band-gap edges and the first
four branch frequencies** (Blueprint §7.7/G3 row), for **Layer 1** (classical limit, anchor Li et al.
2024 Fig. 2(a)), **Layer 2a** (gradient elasticity with flexoelectricity suppressed, anchor Li et al.
2024 Fig. 2(b)) and **Layer 2b** (dipolar gradient elasticity, isothermal, Pb/brass, anchor Li et al.
2023 Fig. 4(c)). Layer 2c is marked *optional* in the layer table and is therefore outside PCR1's
mandatory set.

## 4. G3 — exact authoritative definition

**Blueprint v1.4, hard-gate box (HARD GATE G3 — non-negotiable):**

> "Layers 1, 2a and 2b band-gap edges and the first four branch frequencies must agree with the
> published values to **≤ 2 %** relative (target ≤ 0.5 % in the classical limit)."
> Evidence in manuscript: overlay/side-by-side dispersion plots; **tabulated first four branch
> frequencies at stated $\bar k$; band-gap edge comparison; relative error per quantity; maximum
> relative error; explicit PASS/FAIL per benchmark** — all in the main text.
> "If it fails: **Do not submit.**"

Layered gate structure: the roadmap places **G3** at week 8 (Layers 1/2a/2b/2c executed, error table
produced) and **G4** at week 14 ("submission-ready", signed by the PI **only after PCR1–PCR8 are
checked**; "a failed PCR blocks submission exactly as G3 does").

## 5. Benchmark inventory (Part C)

Sources: `audit/benchmark_evidence.json`, `p11d_regenerate_evidence.py`, `audit/P3_SOURCE_AUDIT.md`,
`audit/P11_SOURCE_PACKAGE_INVENTORY.md`, `analytic/`, `tables/out/tab03_anchor_errors.tex`,
`latex/sections/sec05_verification.tex`, plus first-hand re-extraction of the archived source PDFs
performed for this audit.

| # | Benchmark | Source PDF present? | Source equations? | Required parameters? | Boundary/interface conditions? | Author numerical table? | Machine-readable reference? | Reproduced by current solver? | Comparison type | Independent error % computable? | Satisfies PCR1? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **B1** — Layer 1 classical AlN/BaTiO₃ bilayer | **yes**, `analytic/li2024/s41598-024-75049-1.pdf` | yes (classical limit; Rytov exact dispersion implemented) | yes (in-text narrative; paper has **no tables**) | yes (source model; cell trace T = T_B T_A) | **no** | **no** | yes: Level 1/2 internal residuals `6.47e-16` / `7.22e-16`; genuine numerical gap bands computed | **graphical only** (qualitative overlay; raster) | **no** | **no** |
| 2 | **B2** — Layer 2a gradient AlN/BaTiO₃ (f = 0, F = 0) | **yes** (same file) | yes (gradient/bilinear transfer matrices) | yes, **but source `l` vs `l̄` is dimensionally ambiguous** (three labelled interpretations run, none adopted) | documented; ambiguity remains open | **no** | **no** | yes: three configurations run; internal residuals `4.10e-57`; genuine numerical gap bands computed | **graphical only** | **no** | **no** |
| 3 | **B3** — Layer 2b dipolar gradient Pb/brass SH bilayer | **yes**, `analytic/li2023/17455030.2023.2222189.pdf` | yes (dipolar gradient form; LWZ 2016 analytic reference) | yes (inherited Fig. 3(b) values: c̄₁ = 0.15, d̄₁ = 0.25, c_R = d_R = 1.5) | documented (SH interface conditions; pinned run P11D-B3-R1, 720 points) | **no** | **no** | yes: Level 1/2 residuals `1.37e-13` / `4.19e-14`; multiple acoustic-optical branches computed | **graphical only** (P12A-corrected overlay) | **no** | **no** |
| 4 | **B5** — micro-beam pure bending (Papargyri-Beskou & Beskos 2009) | **yes**, `analytic/pb2009/` | yes | yes | yes | n/a (exact source equations) | yes (equations) | yes | **numerical** | **yes** (`< 1e-15`) | PASS via **Layer 3** (analytic), not an external numerical benchmark |
| 5 | **TV9 / Layer 4** — Mishra, Kumar & Sharma 2026 homogeneous-lattice limit (independent method: dynamic stiffness + Wittrick–Williams) | referenced in TV registry (CLOSED [C], first-hand retrieval recorded) | yes | yes | yes | — | — | yes (homogeneous limit cross-check) | analytical/numerical cross-check | yes | **not a PCR1 item** (Layer 4 is *optional* in the layer table) |
| 6 | **Layer 2c** — classical/gradient band gaps (Li et al. 2023 Fig. 3) | yes | yes | yes | yes | **no** | **no** | — | graphical | no | **not a PCR1 item** (marked *optional*) |

**First-hand source check performed for this audit (independent of the registry):** text extraction
from the two archived PDFs gives, for **Li et al. 2024**: *"Data availability — The datasets used and
analysed during the current study can be obtained from the corresponding author. The email address of
the corresponding author is liyueqiu2004@163.com."*; the paper contains **0** occurrences of "Table N"
and **0** occurrences of "supplementary"; no numeric band-gap-edge or frequency values are stated in
the running text. For **Li et al. 2023**: **no** data-availability statement, **no** supplementary
material, **0** table labels, and no numeric gap-edge values in the text.

## 6. B1 / B2 / B3 status (Part F)

| | Status (registry) | Honest description | What would be needed to promote |
|---|---|---|---|
| **B1** | `PARTIAL / GRAPHICAL_ONLY` | The present calculation genuinely reproduces the classical-limit physics (Rytov analytical dispersion verified to `< 10⁻¹⁵`; internal Level 1/2 identities at machine precision) and the published *figure* is qualitatively matched. It is **not** numerically compared with published values, because none exist. | author-released first-four-branch frequencies and gap edges at stated $\bar k$ (or written numeric values), or an authorized digitisation protocol change (a governance act, not an audit act) |
| **B2** | `NOT_VALIDATED / GRAPHICAL_ONLY (l/l̄ AMBIGUITY)` | Same as B1 **plus an unresolved source-parameterisation ambiguity**: the Fig. 2(b) panel annotates a bare `l = 1e-5` while the source text defines a barred length; three interpretations are run and none adopted. **Not externally validated** — stated explicitly in the manuscript and Table 3. | resolved `l`/`l̄` semantics *and* published numerical values |
| **B3** | `GRAPHICAL_ONLY / PARTIAL` | The genuine Pb/brass heterogeneous gradient case is computed (pinned run, 720 points) and qualitatively compared; the Fig. 4(c) provenance question was corrected in P12A (the raster previously treated as Fig. 4(c) is the source's Fig. 7; the true panel annotates no c̄/d̄ values, and the evaluated parameters are **inherited** from Fig. 3(b), tagged [S]). | published numerical values for the dipolar-gradient panel |

No closed issue was reopened: TV1/TV2/TV12/TV9 stay as recorded, B2's ambiguity stays **preserved,
not resolved**, and no PARTIAL or GRAPHICAL status was silently promoted.

## 7. The three null external-error entries (Part D)

Trace of each `quantitative_error = null`:

`latex/sections/sec05_verification.tex` / `tables/out/tab03_anchor_errors.tex` (footnotes c–f)
→ `audit/benchmark_evidence.json` (B1/B2/B3 `quantitative_error: null`,
`reference_data_available: false`, `quantitative_error_allowed: false`)
→ `audit/p11d_regenerate_evidence.py` (single authoritative generator, no hand-edited numbers)
→ the archived source PDFs in `analytic/li2024/`, `analytic/li2023/`
→ the published record (no tables, no supplementary data).

| Null | Provenance chain verified | Category |
|---|---|---|
| **B1** `quantitative_error = null` | table footnote → registry → generator → PDF → paper | **genuinely unavoidable** — the reference quantity does not exist in the public record |
| **B2** `quantitative_error = null` | same, plus the `l`/`l̄` ambiguity record and three interpretation runs | **genuinely unavoidable**, with a **second, independent** blocker (parameterisation ambiguity) |
| **B3** `quantitative_error = null` | table footnote → registry → generator → PDF → paper | **genuinely unavoidable** — same reason |

This is **not** an evidence-collection gap in the repository: both source PDFs are present and
archived; the deficiency is in the *published record*. It is not an implementation gap (the solver
computes the quantities and passes every internal identity), and not a documentation gap (the
limitation is stated in the main text, in Table 3, and in the registry). The nulls are correctly
represented and must stay **NULL**.

The governing policy is explicit and is being followed:
> "Curve digitization is permitted ONLY to draw overlay figures, NEVER to compute solver-error
> percentages. If author raw numerical tables are unreleased, benchmark status is formally
> GRAPHICAL_ONLY / PARTIAL." — `audit/benchmark_evidence.json` metadata

and `audit/P11_SOURCE_PACKAGE_INVENTORY.md`: *"raw numerical tables were not published online as
supplementary data"*.

## 8. Exact missing evidence (per benchmark)

| Benchmark | Exact missing artifact | Where it could come from |
|---|---|---|
| **B1** | numeric values for the band-gap edges and the first four branch frequencies at the stated $\bar k$ of Li et al. 2024 Fig. 2(a) | the source's own datasets, **obtainable on request from the corresponding author** (the paper's Data-availability statement names an address); or any future author-deposited data |
| **B2** | the same for Fig. 2(b), **plus** an authoritative statement of whether the annotated `l = 1e-5` means `l` or `l̄` | same source/author channel; the ambiguity cannot be resolved from the published text alone |
| **B3** | numeric values for the dipolar-gradient dispersion/gap edges of Li et al. 2023 Fig. 4(c) | the source's datasets (no data-availability statement is published); author request |

No such artifact exists in this repository (verified: no author CSV/MAT/TXT/XLSX/archive anywhere in
the workspace; `bench/` contains no reference tables; the only numerical references present are the
repository's own computed outputs and the two source PDFs).

## 9. Can the available sources legitimately close PCR1? (Part E)

**No.** The mandatory evidence is `≤ 2 %` agreement with **published values** for Layers 1/2a/2b.
For all three, the published record contains **no numeric values** — only raster dispersion curves —
and the governing policy forbids computing error percentages from digitised curves. Promoting the
graphical overlays, the internal Level 1/2 identities, or the analytical Rytov agreement would be
exactly the silent GRAPHICAL→NUMERICAL conversion the protocol prohibits. The honest position is
unchanged: **PCR1 NOT PASS, G3 NOT MET.**

## 10. G3 / G4 dependency graph (Part G)

```
PCR1 (published-benchmark ≤2% relative error, Layers 1/2a/2b)
   └──> G3  (hard gate: same criterion + evidence-in-manuscript rule; "do not submit" if unmet)
            └──> G4  (PI signs a submission-ready release ONLY after PCR1–PCR8 pass;
                      "a failed PCR blocks submission exactly as G3 does")
                     └──> release readiness

independent blockers (not downstream of PCR1/G3):
   P5  (two parallel pipelines, reconciliation outstanding)
   R-1 (pipeline-level reproducibility; OPEN)
   C-1 (discriminant criterion validated but not deployed in the production script)
```

Closing PCR1 **would not by itself** close G3: G3 additionally requires the complete evidence package
(tabulated first four frequencies at stated $\bar k$, gap-edge comparison, per-quantity and maximum
relative error, explicit PASS/FAIL per benchmark, published in the main text) *and* Layer 2c. Closing
PCR1+G3 would still leave **G4 unsigned**: G4 is a PI procedural act performed after **PCR1–PCR8** all
pass — and G4 remains independently blocked while any PCR fails. P5 and R-1 are **independent** of
this chain and would remain open regardless. No automatic promotion is claimed anywhere in this
document.

## 11. P5 status (Part H)

**P5 = NOT PASS / OPEN (unchanged).** Two parallel P5 pipelines exist (`P5_STATUS.md`: Part A pilot
12/12 + studies, Part B NOT PASS), with **no numeric cross-validation between them**; the branch-level
gate is CONTESTED, and the manuscript contains no P5-production claims. No new P5 scientific work was
performed in P12K.

## 12. R-1 status (Part H)

**R-1 = OPEN (unchanged).** The three properties stay distinct: (A) solver-level reproducibility —
established for the Route-F configuration only (audit evidence, not governing); (B) governing-artifact
reproducibility — **not** established (one realization of an unpinned ARPACK start vector at
`tol = 1e-12`; the 32² datum sits 0.00196× below its own reproducibility); (C) estimator-rule
determinism — established (Rule R-fit is a pure function of `(e_i, s_i)` and reproduces the governing
rate bit-exactly). **(D) pipeline-level reproducibility remains unachieved.** Rule R-fit being
deterministic does **not** make the governing artifact reproducible, and this audit makes no such
claim.

## 13. Stale-claim inventory (Part I)

Sweep over all tracked `.md/.tex/.py/.json/.csv/.txt` for `PCR1 PASS`, `G3 PASS/MET`, `G4 PASS/MET`,
"externally validated", "fully validated", "release ready", "all benchmarks validated",
"convergence confirmed", "pipeline reproducible".

| Finding | Assessment |
|---|---|
| 92 `PCR1`-context, 128 `G3`-context, 49 `G4`-context hits | **All correct in context** — every one states NOT PASS / NOT MET, or is a *proposal* record. No live document asserts a passing gate. |
| `audit/P6_FORENSIC_AUDIT.md` — "Monotone convergence confirmed ($e_{32}<e_{16}<e_8<e_4$)" | **Not stale** — the strict monotonicity is a true, still-verified property of the 5i sequence and makes no fit-subset or theoretical-order claim. |
| `audit/P6_FINAL_GATE_AUDIT.md`, `audit/P9_FINAL_RELEASE_AUDIT.md` | **Superseded historical PCR numbering** (already catalogued by P12C Part I as unusable for current statuses). Keep as historical record. |
| `audit/P10B…P10G_*` (governance hold period) | These **propose** de-scoping amendments ("G3-H", "G4-H") that were **never adopted** (Blueprint v1.3/v1.4 retain the hard gate; P11D reversed the de-scoping). They are historical decision inputs, not current policy — flagged as *potentially misleading if read out of context*; a one-line "NOT ADOPTED / superseded" banner would be a documentation improvement **only if authorized**. |
| "fully validated" / "all benchmarks validated" | **Zero** live occurrences (the single hit is a negation audit in P10B). |
| "convergence confirmed" | Only the true monotonicity statement above. |
| "release ready", "pipeline reproducible", "externally validated" | All occurrences are **negations or explicit disclaimers** (P12C, P12I, P11D, P3_TV_RESOLUTION). |

**No stale achievement claim was found; nothing was rewritten** (corrections are only made when
demonstrably stale, and none is).

## 14. Final decision (Part J) — outcome 3, with a named external route

**PCR1 / G3 cannot currently be closed.** The evidence is *insufficient*, and the shortfall is in the
**published record**, not in this repository:

- the three null entries correspond to **genuinely unavailable author-released numerical data**
  (no tables, no supplementary files, no numeric values in the text; Li et al. 2024 states its
  datasets are available **only from the corresponding author**);
- no legitimate **repository-only** closure path exists — there is no machine-readable external
  reference anywhere in the workspace, and the governing policy forbids manufacturing error
  percentages from digitised curves;
- the only concrete route that does not fabricate data is an **external author-data request** for
  B1/B2 (and, additionally, an authoritative `l`/`l̄` clarification for B2) and for B3. This is an
  external action requiring PI authorization; it is **not** performed or initiated by this audit.

Accordingly: **PCR1 = NOT PASS, G3 = NOT MET, G4 = NOT MET** — preserved, not weakened, not promoted.

## 15. Regression and immutability (Part L)

| Check | Result |
|---|---|
| Full suite, run 1 | **126 passed, 1 skipped in 8.42 s** |
| Full suite, run 2 | **126 passed, 1 skipped in 6.71 s** |
| Gate/PCR guard sub-suites (P12C post-closeout, P11D remediation, P12A remediation, P8 remediation) | **33 passed in 0.46 s** |
| Numerical / manuscript / Blueprint cross-check (P12J copy) | **43/43 passed** |
| Immutability anchors (v1.3, v1.4, rule, JSON, TXT, script, P12E patch, P12C raws) | **9/9 verified**, 0 failures, before and after |
| Route-F / P12E values in governed artifacts | **none** |
| No scientific test changed to make a status pass | confirmed — this phase modified **no** scientific file |

## 16. Exact next authorized action

1. **Immediate (DONE 2026-09-24):** push of `876213a` + the P12K commit to
   `https://github.com/vipin-oss/BFS-FEM-MATLAB` branch `phase-1-symbolic` using the **same** access
   point as before; fetch; verify `origin/phase-1-symbolic` == the P12K commit; update
   `RECOVERY_CHECKPOINT_P12K.md` with the verified SHA and push that too. *(Exact commands in the
   checkpoint file.)*
2. **Then, still without starting P13:** decide the G3/PCR1 disposition — either
   (a) authorize a PI-led **author-data request** to the Li et al. authors (the only non-fabricating
   path to published numerical values), or (b) formally record PCR1/G3 as unmet external-evidence
   blockers for the submission decision. Either way, **P13 remains blocked** and no gate status may be
   promoted without the missing data.
3. Continue the standing rule: after every major block, push a recovery checkpoint **before** starting
   the next risky block.

---

**Status summary (all preserved, none promoted):** PCR1 NOT PASS · PCR5 **PASS** · G3 NOT MET ·
G4 NOT MET · P5 NOT PASS/OPEN · R-1 **OPEN** · C-1 OPEN · G-1 CLOSED · **P13 blocked**.
