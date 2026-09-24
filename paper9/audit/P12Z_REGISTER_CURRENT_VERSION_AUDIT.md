# P12Z — TRACEABILITY REGISTER CURRENT-VERSION / A2 GOVERNANCE AUDIT

**Phase:** P12Z · **Decision: A — `NO CORRECTION — CURRENT TRACEABILITY SUFFICIENT`.**
No register row was added, no existing row was edited; the register files are byte-identical to the
P12Z entry state. Deliverables: this record + `paper9/verification/suite/test_p12z_register_current_version.py`.

| Field | Value |
|---|---|
| Entry SHA (verified) | `cb6a4c61041716345381e988c337290b85b5640a` (local = origin = ls-remote; clean tree) |
| Pre-work checkpoint | `316f0d68556ae8709acf2f87bf697c19c754378c` (pushed + verified before any edit) |
| Audit commit | recorded in the delivery report |
| Register at entry and exit | `traceability_matrix.csv` `4ce06f024bf41f12688998fd26c2861cf04dd9adaefbab93213d48698e573b04`; `traceability_matrix.json` `f332e03117b60643ecd901d64c585d3accac401b55c7bca54054d5bff1118b6f` |

## Part A — recovery

`git fetch` → local `HEAD` = `origin/phase-1-symbolic` = `ls-remote` = `cb6a4c6…`; porcelain empty;
baseline `/home/user/p12z_baseline_hashes.txt` (527 tracked files); pre-work checkpoint `316f0d6`
pushed and re-verified before any edit.

## Part B — traceability schema audit

**What a Blueprint row represents.** The register is a *claim ledger*: `paper9/audit/README.md`
defines it as “claim → figure/table → processed → raw → run manifest → code → equation → parameters”,
and master plan §K fixes the row mapping as `MS claim → FIG/TAB → RES → RUN → EQ → params` with the
ID scheme `EQ-n / RUN-id / RES-id / FIG-n / TAB-n / MS-§x.y`. Every row carries the **phase that
locked the claim** and a status; rows are appended, never re-edited (P11D retag kept history via an
addendum; P12H appended four rows “no existing row edited”; P12C explicitly recorded that the matrix
“was not modified”). The two `BP` rows are therefore *revision events*: `BP-v1.3` (phase `P0`,
“governing specification (blueprint v1.3 editorial-only revision)”, `derivation_doc` =
`paper9/plan/blueprint/PROVENANCE.md`) and `BP-v1.4` (phase `P12H`, the A1 amendment, `derivation_doc`
= `P12H_A1_PROTOCOL_CLOSURE_AUDIT.md`).

**Determinations.**

| # | Question | Answer (evidence) |
|---|---|---|
| 1 | What a Blueprint row represents | A phase-stamped record of a *locked revision event*: the revision identity, its delta, its hash and its locking audit — not a live “current version” pointer |
| 2 | Must every governing Blueprint version have a row | **No rule requires it.** The register's documented schema is claim/equation/element-level traceability (README; master plan §K). Version governance is carried by `paper9/plan/blueprint/PROVENANCE.md` — “version-controlled frozen snapshots for traceability” — which is the file the register's own `BP-v1.3` row cites as its derivation document |
| 3 | Do amendments such as A2 require a separate row | **No standing requirement.** The A1 precedent (P12H) appended rows because A1 created *new governed artifacts* (a plan amendment, the Rule R-fit module + guards, terminology) — an amendment-time registration choice. A2's new governed artifacts are registered in its own amendment record, the frozen v1.5 file, the route classifier/guards and the machine record (Part C) |
| 4 | Is the graphical-validation route already represented | Yes — by the **frozen v1.5 file §13** (\`\\section{AMENDMENT A2\` … A2.1–A2.8), the A2 amendment record, \`benchmark_validation_route.py\` (fixed identifiers \`QUANTITATIVE_VALIDATION\` / \`GRAPHICAL_VALIDATION\` / \`NOT_VALIDATED\`), its synthetic guard, and B1's route label in the active machine record. The register's row types cover TVs/equations/benchmarks; the validation *tier* has never been a register row type (nor was A2.4/A2.5-style governance) |
| 5 | Is the existing `BP-v1.4` row intentionally historical only | Yes — phase `P12H`, consistent with the P12H audit it cites, and with the project's own point-in-time convention that `PROVENANCE.md` states explicitly (“the rows above this block still describe v1.3 as current; that was true when they were written and they are deliberately left unedited”). P12Y classified it as a historical registry row; P12Z re-verified that (no active record treats it as current) |
| 6 | Is `governing_spec = Paper9_Blueprint v1.5` sufficient | **Yes.** The machine-readable pointer exists (\`benchmark_validation_record.json\` → \`\"governing_spec\": \"Paper9_Blueprint v1.5 (A2 graphical-validation route)\"\`) and the authoritative file/hash registry exists (\`PROVENANCE.md\` additive P12R block: v1.5 \`b96c8e76…\` **CURRENT governing specification**; v1.4 \`2ae0b1e8…\` **FROZEN, superseded by v1.5; byte-identical since creation**). The repository's traceability rules require claims to trace to evidence; they do not require the register to restate the version ledger |

## Part C — A2 traceability chain

`Blueprint v1.5 §13 (A2)` → `BLUEPRINT_V1_5_GRAPHICAL_VALIDATION_AMENDMENT.md` (`c008a00e…`, eight-block
delta, routes, hierarchy, B2 rule, no-fabricated-precision, decision table, non-promotion table) →
`benchmark_validation_route.py` (`c5b26190…`) + `test_p12r_graphical_validation_route.py`
(`8e83d16e…`) → `benchmark_validation_record.json` (`governing_spec`, per-benchmark `route`) → gate
state. **No entry needed for the chain to be closed:**

| Required traceability | Where it is carried | Verdict |
|---|---|---|
| B1 graphical validation | machine record `B1.route = GRAPHICAL_VALIDATION`, `B1.graphical_validation = PASS`; route definition v1.5 A2.1(b); evidence P12S/P12T/P12V (`evidence/p12v/…`, P12V audit) | ✓ traceable |
| B2 source ambiguity | machine record `B2.ambiguity_status = UNRESOLVED (dimensional vs barred reading of l; A2.4 forbids silent choice)`, `B2.route = NOT_VALIDATED`; v1.5 A2.4; `P12L`/`P12N` historical record; P12V audit §B2 | ✓ traceable |
| B3 source-data insufficiency | machine record `B3.route = NOT_VALIDATED`, `parameter_completeness`, `ambiguity_status`, `formulation_status = ESTABLISHED / SOURCE-EQUIVALENT`; P12U/P12V/P12W/P12X records | ✓ traceable |
| `quantitative_error` NULL policy | v1.5 A2.5 + A2.6 (a graphical record carries no numerical error field); machine record `quantitative_error = null` ×3; `benchmark_evidence.json` | ✓ traceable |
| A2's distinct graphical evidence tier | v1.5 A2.1(b)/A2.3/A2.6/A2.7; amendment record §3–§4; classifier identifiers; P12R synthetic guards | ✓ traceable |
| Current governing specification machine-identifiable | `benchmark_validation_record.json.governing_spec`; `PROVENANCE.md` (file + sha256 + CURRENT/FROZEN status) | ✓ machine-identifiable |

**Loss of traceability from the missing row: none identified.** No claim, gate, benchmark, number or
evidence pointer becomes untraceable; the register simply does not restate a ledger that is kept, by
design, in `PROVENANCE.md` and the machine record.

## Part D — CSV / JSON consistency

| Check | Result |
|---|---|
| Same active TV statuses | **Provenance class agrees for every shared TV row** (10 shared of 11 CSV TV rows; `TV6-CaseC` is a CSV-only row). Three rows differ **only in the state word**: `TV6` CSV `PARTIAL [S]` vs JSON `LOCKED [S]`, `TV14` and `TV18` CSV `CLOSED [S]` vs JSON `LOCKED [S]` — the CSV rows are phase-stamped P5/P11 point-in-time entries while the JSON is the consolidated P11 snapshot; class (`[S]`) is identical in all three, so no provenance claim conflicts. Observed by P12X/P12Y as well; **not rewritten** (Part D: do not rewrite historical rows) |
| Same governing specification | **Both registers are silent** about the governing blueprint version (neither contains \`v1.5\` or \`A2\`): the CSV's latest `BP` row is the P12H `BP-v1.4` revision event and the JSON's `metadata.p12h_amendment.blueprint` block is the same A1 registration. Their silence is *identical*, so no divergence exists between the two representations; the current version is registered in `PROVENANCE.md` + the machine record |
| Same historical Blueprint information | Yes — `BP-v1.4` row and JSON metadata both cite `0089754b…` (the P12H-time v1.4 hash) and `ca71b91a…` (v1.3); the plan amendment is recorded identically (post `a45a5448…`, pre `0e2c3a3a…`) |
| No hidden divergence | Verified mechanically: column schema (9 documented columns, 46 data rows), unique claim ids, the `BP`/`PLAN`/`M`/`F`/`TV`/`RFIT`/`RNAME` row families, the TV class comparison above, and the plan/blueprint hash citations — all cross-checked. No `BP-v1.5` row, no duplicate governing row, no conflicting governing row |
| No stale v1.4 row incorrectly treated as current | The `BP-v1.4` row is a phase-stamped P12H revision record; **no active record** treats it as the governing specification (machine record `governing_spec` = v1.5; `PROVENANCE.md` marks v1.4 FROZEN/superseded; the P12Y guard suite asserts **no** `BP-v1.5` row and keeps the F3 disposition). Two P12H-era *hash citations* in that row family no longer match the artifacts as they now stand and are **reported, not rewritten** (below) |

### Reported, not corrected

* **P12Z-O1** — the `BP-v1.4` row (and the JSON `p12h_amendment.blueprint.v1.4_sha256`) cite
  `0089754b076ff9e3…`, the **P12H-time** v1.4 hash; the frozen v1.4 file is now `2ae0b1e8f37e10a0…`
  after the P12J C1 correction (v1.4 §5.7 declared-zero clarification). The authoritative current
  v1.4 hash is registered in `PROVENANCE.md`; the row is consistent with the P12H audit it cites.
* **P12Z-O2** — the `PLAN-5i` row (and JSON `p12h_amendment.plan.sha256`) cite the plan's
  post-amendment sha256 `a45a5448a76764d5…`. That value matches **no reachable revision** of
  `paper9/plan/CALC_MASTER_PLAN.md`: the pre-amendment value `0e2c3a3a…` is verified (commit
  `fb9bd5d`), the amended file hashes to `1f1c080b…` at `dd42e81` (its only modifier) and at HEAD, and
  neither CRLF/LF/newline variants nor any progressive reconstruction of the P12H hunk reproduces it.
  The artifact itself is intact (the A1 amendment is present and its own note records the correct
  pre-amendment hash); the recorded *post-amendment* hash is a P12H-era bookkeeping error in an
  additive citation. Not corrected here (historical row; outside the A2 decision; Part D forbids
  rewriting historical rows). Recorded for a separately authorised cleanup.
* **P12Z-O3** — the three state-word-only TV divergences in Part D (no provenance-class conflict; no
  gate or numerical implication).

## Part E — decision

**A — `NO CORRECTION — CURRENT TRACEABILITY SUFFICIENT`.**

1. The governing schema does not require a register row per governing blueprint revision (Parts B.2–B.3);
   version governance is carried by `PROVENANCE.md`, the file the register's own `BP-v1.3` row cites.
2. The v1.5/A2 chain is fully traceable and machine-identifiable through current records (Part C), with
   **no** loss of traceability in any of the six required links.
3. The absence is consistent with the register's design (append-only, phase-stamped claim ledger;
   historical rows deliberately unedited) and is identical in the CSV and the JSON, so it is a
   register-design/practice choice, **not** a hidden divergence or a false current-version claim.
4. Adding a `BP-v1.5/A2` row would be a *content addition for completeness* — explicitly out of scope
   unless a schema requirement or genuine gap exists; neither does here. No cosmetic row was added.
5. No scientific status, gate, threshold, route or number was touched; the two register files are
   byte-identical to their entry state (guarded).

## Part F/G — no correction; audit record + guards only

Guards added (`test_p12z_register_current_version.py`): exactly one *current* governing blueprint
(v1.5, in the additive `PROVENANCE.md` block; the older `CURRENT` label is above the amendment marker
and marked stale by the file itself); v1.4 historical/frozen; A2 traceable (v1.5 §13 + amendment
record + classifier + guards + B1 route label); no duplicated or conflicting governing row; all
existing TV provenance classes unchanged; the two register files byte-identical (proving no row was
added); gate states and `quantitative_error` pinning; immutability anchors. No existing test weakened.

## Part H — gate / scientific immutability

B1 `GRAPHICAL_VALIDATION`/PASS · B2 `NOT_VALIDATED`/`UNRESOLVED` · B3 `NOT_VALIDATED` with
`formulation_status = ESTABLISHED / SOURCE-EQUIVALENT` · `quantitative_error = [NULL, NULL, NULL]` ·
PCR1 NOT PASS · G3 NOT MET · G4 NOT MET · P5 NOT PASS/OPEN · R-1 OPEN · PCR5 PASS · P13 BLOCKED —
all re-verified unchanged.

## Part I/J/K — regression, immutability, commit

See the final checkpoint (`paper9/audit/RECOVERY_CHECKPOINT_P12Z.md`) for the exact regression counts,
the immutability result against `/home/user/p12z_baseline_hashes.txt` and the commit/push/recovery
chain. Only P12Z artifacts (this record, the guard suite, the checkpoint) are added; no other file
changed.
