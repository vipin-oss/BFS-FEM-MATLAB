# P12S evidence bundle — B1/B2/B3 graphical-validation reproduction (Blueprint v1.5 / A2)

Pre-work checkpoint: `270b8ab42246a2c20e0de8395aea8c8e5f068af4` (pushed + fetch/`ls-remote` verified
before any scientific work). Governing spec: `paper9/plan/blueprint/Paper9_Blueprint_v1.5.tex` §13 (A2).

| File | What it is |
|---|---|
| `B1_panel.png`, `B2_panel.png`, `B3_panel.png` | Panels split out of the **authoritative PDFs** in this repo (Li 2024 p. 9 Fig. 2(a)/(b); Li 2023 p. 15 Fig. 4(c)). Registration/plot-box geometry in the generator output. |
| `B1_overlay.png` | B1: published Fig. 2(a) + registration digits (left) and independent Rytov reproduction vs published (right). Reproduction lies on the published curve. |
| `B2_overlay_interpretations.png` | B2: the published Fig. 2(b) against all three labelled interpretations (source geometry / micro geometry / barred reading infeasibility). No interpretation reproduces the panel. |
| `B3_overlay.png` | B3: published Fig. 4(c) + registration digits (left) and the independent dipolar-gradient reproduction vs published (right). **The reproduction does not overlay the published curve** — see the audit §Phase F. |
| `p12s_validation_record.json` | Raw reproduction output written by `paper9/validation/p12s_run.py` (gap registries, ω₀ check, overlay hashes). |
| `suite_run1.txt`, `suite_run2.txt` | Full verification suite, two runs: **151 passed, 1 skipped** each (143 pre-existing + 8 new P12S anti-fabrication tests). |
| `guards.txt` | Named guard files (P12C post-closeout guards, P12H rule-R-fit governance, P12H C1 synthetic, P12R route, P12S anti-fabrication): **70 passed**. |
| `crosscheck.txt` | P12J independent cross-check script: **43/43**. |
| `immutability.txt` | 12 governing anchors unchanged (**12/12**) + manuscript/production/blueprint diffs vs `270b8ab` (all empty). |

**Digitisation policy actually applied:** panel pixels are used *only* to register the published curve
on the axes of the reproduction; no residual is converted into a percentage anywhere, and all three
`quantitative_error` fields remain **NULL** (`paper9/audit/benchmark_validation_record.json`).

**Routes:** B1 `GRAPHICAL_VALIDATION` (PASS) · B2 `NOT_VALIDATED` (parameter ambiguity unresolved) ·
B3 `NOT_VALIDATED` (reproduction does not overlay). Gates unchanged: PCR1 NOT PASS · G3 NOT MET ·
G4 NOT MET · P5 NOT PASS/OPEN · R-1 OPEN · PCR5 PASS · P13 BLOCKED. Manuscript untouched; no author
contact; nothing sent.
