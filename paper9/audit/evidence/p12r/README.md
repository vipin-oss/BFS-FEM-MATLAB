# P12R evidence bundle — Blueprint v1.5 amendment A2 (external-validation evidence routes)

Pre-work checkpoint: `26dbcf88d2bab7292e77ea32307d61d42496d398` (pushed + fetch/`ls-remote` verified
before any edit).

| File | What it is |
|---|---|
| `suite_run1.txt` / `suite_run2.txt` | Full suite twice: **143 passed, 1 skipped** (6.87 s / 6.39 s). 126 pre-existing + **17 new** A2 tests; the skip is the pre-existing opt-in rerun. |

**What A2 does.** Introduces the three external-validation evidence routes — QUANTITATIVE (existing
thresholds, unchanged), GRAPHICAL (labelled overlay comparison, no percentage), NOT VALIDATED
(insufficient source or unresolved ambiguity) — with the evidence hierarchy, the B2 `l` vs `l̄` rule, the
no-fabricated-precision prohibition, a machine-readable classification contract and a decision table.
**Nothing is promoted**: PCR1 NOT PASS · G3 NOT MET · G4 NOT MET · P5 NOT PASS/OPEN · R-1 OPEN ·
PCR5 PASS · P13 BLOCKED; B1/B2/B3 `quantitative_error` still NULL.

**Delta:** v1.5 = v1.4 + exactly **8 blocks** (6 single-line replacements at v1.4 lines 95, 457, 471,
803, 886–888, 1046; 2 insertions — new Section 13 and a footer revision note), verified by opcode
comparison. v1.4 remains byte-identical `2ae0b1e8…`; v1.3 `ca71b91a…`. New v1.5 sha256
`b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91`.

**Immutability (10/10 anchors):** v1.3, v1.4, `rule_rfit.py`, governing JSON, historical TXT, P4B
script, provenance anchor, P12E patch, `benchmark_evidence.json`, P12M request drafts — all unchanged;
manuscript (`latex/`, `tables/`, `figures/`) untouched; `PROVENANCE.md` additive only (24 insertions,
0 deletions).

**Tests:** 17 new governance/synthetic tests incl. the six required synthetic cases and the
fabricated-precision guard; PCR/gate guard sub-suites 44 passed; numerical/manuscript/Blueprint
cross-check 43/43. No existing test modified.

**Not done (out of scope):** B1/B2/B3 revalidation, curve digitisation, threshold changes, model/
production changes, manuscript edits, author contact, P13.
