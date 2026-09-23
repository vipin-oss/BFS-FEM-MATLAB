# P12A Close-out — source-figure correction, PCR6 registry completion, hygiene

**Phase:** P12A (branch `phase-1-symbolic`; `main` untouched; Blueprint v1.3 untouched)
**Date:** 2026-09-23
**Authority:** P12 post-P11D gate audit (this chat) + explicit user authorization
("Implement P12A fully — local commits + push") recorded in the conversation.
**Rule in force:** evidence-first; registry-first regeneration (no hand-edited
numbers); historical audit documents preserved (corrections via dated addenda);
no gate/PCR/Blueprint redefinition; test suite green at every commit.

---

## 1. Findings that P12A corrects

### F1 (factual, submission-class): Li et al. (2023) Fig. 4(c) misidentification
The raster archived in P11 as "Fig. 4(c)" (`paper9/audit/evidence/fig4c_raw.png`,
three panels annotated tau_R = 1 / 0.1 / 0.05) is **pixel-identical
(mean |diff| = 0.0000) to FIGURE 7** of the source (gradient *thermo-elastic*
model), printed page 16 — verified by byte-level comparison against the PDF's
embedded images (PyMuPDF) in the P12 audit.  The genuine Figure 4 is the
1500×437 image on printed page 15, in-repo as
`paper9/audit/evidence/li2023_p15_img1_Im1.png`: panel (c) "Gradient
elasticity" (present vs Li and Wei [34]), no tau_R sweep, no c_bar/d_bar
annotation.  The false claim "Fig. 4(c) sweeps tau_R" propagated to
`sec05_verification.tex` (2 places), `tab03_anchor_errors.tex` footnote f,
`traceability_matrix.json` TV1, `benchmark_evidence.json` B3,
`fig04_benchmark_validation.py`, `p11d_regenerate_evidence.py`, and the P11D
addendum of `P3_TV_RESOLUTION.md`.

**What survives:** TV1's verdict — Fig. 4(c)'s caption annotates **no**
c_bar/d_bar (re-verified from the PDF text layer), so c_bar_1 = 0.15,
c_R = 1.5, d_bar_1 = 0.25, d_R = 1.5 remain **inherited from Fig. 3(b)**,
provenance **[S]**.  All B3 numbers (pinned run P11D-B3-R1) are unaffected.
Only the rationale sentence and the overlay basis were wrong.

### F2 (documentation): B2 l_bar normalization wording
The source (Li et al. 2024, Eq. (55) context, P12-verified) defines
**l_bar = l/b, b = a_A + a_B = 0.02 m**.  Pre-P12A registry/engine prose said
"l_bar = l/a (layer width)" — an engine-side convention, not the source.
Also: `b2_stable_tm.py` comment "l = l_bar * a = 2e-7 m" was arithmetically
inconsistent (l_bar·a = **1e-7** m, which is what the engine actually used and
what P11D reported; under the source's l/b the same l_bar would give 2e-7 m).
And `benchmark_evidence.json` B1 cited a non-existent "Section 4.1 & Table 1"
(the paper contains **no tables**; parameters are in the unnumbered
"Numerical results and discussions" narrative; the year "Li et al. (2023)"
in the B2 ambiguity text was also wrong → 2024).  The B2 l/l̄ **ambiguity
itself remains OPEN and unresolved** — P12A changes wording, not status.

### F3 (PCR6): B1/B2/B3 rows absent from the Table-2 registry
Every material/geometric/microstructural parameter of B1/B2/B3 that reaches
the results is now registered in `params/params_master.yaml` (32 new rows,
all tagged) and regenerated into `tables/out/tab02_parameters.tex`
(25 → 57 parameters).  Exact field→tag→evidence mapping: see §3.

**Tag-convention note (documented drift; PI decision pending; NO gate
change):** the legacy YAML header reads "[C] canonical/published,
[A] analytical derivation, [S] study/design", while the manuscript legend
(sec05 line 119) and existing rows use "[A]" for anchor-published *and*
derived values, "[S]" for study/inherited.  The new rows follow the **live**
convention (consistent with the Zhan & Wei rows and the manuscript text);
the note is recorded in the YAML header comment added in P12A.  PCR6 requires
a [C]/[A]/[S] tag per parameter; the letter-per-class choice is a
documentation convention, flagged rather than silently settled.  The B3
inherited values were additionally pinned to **[S]** in the pinned-run
registry and manuscript since P11D — unchanged.

### F4 (governance freshness): B5 provenance
Table-3's B5 row traces to `validation/L3/p3_layer3_pb2009.py` (P3 vintage,
not regenerated in P11D).  P12A executed a **freshness re-run**: 11/11 PASS,
max rel err 5.466e-16 (< 1e-15 claim unchanged), deterministic — fresh output
byte-identical to the committed evidence file.  Scientific impact: none;
provenance note updated in `benchmark_evidence.json`.

### F5 (governance hygiene): legacy parallel engine
`validation/p11_b1_b2_b3_validation.py` has **no `.py` consumer**
(full-tree grep, P12 audit).  Its statuses are derived but its tolerances
(1e-6/1e-8) and 0.05-modulus edge rule differ from the authoritative engine.
P12A adds a DEPRECATED header (no code change, no refactor).

---

## 2. Corrections applied (all edits)

| # | File | Change |
|---|---|---|
| 1 | `production/p11d_b2_registry.py` | PARAMETER_SEMANTICS prose corrected (source l_bar = l/b; engine l/a recorded separately; dimensional/barred readings; year 2023→2024) |
| 2 | `results/raw/p11d_b2_gap_registry.json` | the SAME 3 prose fields mirrored + `p12a_note` added — **scripted prose-only edit; numeric identity vs pre-edit backup asserted programmatically (all configs/scans/residuals unchanged)**; no registry re-run (adaptive-precision cost) |
| 3 | `validation/b2_stable_tm.py` | class docstring + CFG-BAR-MACRO comment corrected (l/b source vs l/a engine; 2e-7→1e-7 arithmetic note; simulated geometry unchanged) |
| 4 | `audit/p11d_regenerate_evidence.py` | docstring (P12A correction record); B1 `parameter_source` (no-table citation); B3 `parameter_source` + overlay note (Fig. 7-vs-4(c) truth; keeps "3(b)"/"[S]"); B5 `provenance_note` (P12A freshness); tab03 footnote f; overlay now embeds the GENUINE Fig. 4 raster `li2023_p15_img1_Im1.png` rendered with `cmap="gray"` (mode-L raster) |
| 5 | `figures/gen/fig04_benchmark_validation.py` | docstring + in-figure annotation corrected ("NO c̄/d̄ annotation; τ_R sweep is source Fig. 7"); "no error"/"no source-curve overlay" honesty strings preserved |
| 6 | `latex/sections/sec05_verification.tex` | B3 item + Fig. 4 caption corrected; [S]/inherited/3(b)/4(c)/"no error percentages" preserved; cites \cite{liweizhou2016} (exists in bib) |
| 7 | `audit/traceability_matrix.json` | TV1 resolution text corrected (rationale; verdict "CLOSED [S]" unchanged); evidence pointer updated to the genuine raster + identification note |
| 8 | `audit/P3_TV_RESOLUTION.md` | **appended** dated P12A addendum (history preserved; supersedes only the tau_R sentence; B2 l/b fact added; TV1 stays CLOSED [S]) |
| 9 | `audit/evidence/fig4c_raw_IS_FIGURE7.md` | **new** identification note beside the retained (mislabelled) raster |
| 10 | `params/params_master.yaml` | +32 B1/B2/B3 rows (tags: anchor-published/derived [A]; inherited/labelled-interpretations [S]) + tag-convention comment |
| 11 | `tables/gen/tab02_parameters.py` | LaTeX symbol mapping for the 32 new keys |
| 12 | `tables/out/tab02_parameters.tex` | regenerated (57 parameters) |
| 13 | `validation/L3/p3_layer3_pb2009.txt` | freshness re-run output (byte-identical to previous — deterministic) |
| 14 | `validation/p11_b1_b2_b3_validation.py` | DEPRECATED header comment |
| 15 | `verification/suite/test_p12a_remediation.py` | **new**: 4 guard tests G1–G4 (tau_R regression guard; l/b semantics; genuine-raster/colormap; PCR6 rows+tags) |
| 16 | `audit/P12A_CLOSEOUT.md` | this document |

**Preserved untouched (governance):** `main` (98176e8); Blueprint v1.3;
historical P11/P11A–P11D audit documents (their tau_R sentences stand as
history; the P3_TV_RESOLUTION P12A addendum is the correction record);
`fig4c_raw.png` (retained with identification note); all scientific numbers
(gaps, residuals, timings); all gate logic.

## 3. Regeneration commands (registry-first)

```
python3 paper9/validation/L3/p3_layer3_pb2009.py            # B5 freshness (11/11 PASS, 5.466e-16)
python3 paper9/audit/p11d_regenerate_evidence.py            # evidence JSON + Table 3 + fig4c overlay
python3 paper9/figures/gen/fig04_benchmark_validation.py    # Fig. 4 pdf/png
python3 paper9/tables/gen/tab02_parameters.py               # Table 2 (57 params)
```

Numeric-integrity checks: regenerated `benchmark_evidence.json` diff contains
**zero** changed level-error/gap lines (verified by `git diff` grep);
registry JSON numeric content asserted identical to pre-edit backup;
B1 fresh run in regen reproduced its recorded Level-1/2 residuals and gaps.

## 4. PCR / gate status after P12A (Blueprint v1.3 definitions authoritative)

| Item | Before P12A | After P12A | Basis |
|---|---|---|---|
| PCR1 | NOT MET | **NOT MET (unchanged)** | external ≤2% still uncomputable (P12 audit §A); no redefinition |
| PCR2 | PASS | **PASS** | honesty strings preserved; claim wording now factually correct |
| PCR3 | PASS | **PASS** | B5 freshness re-run adds current evidence |
| PCR4 | PASS | **PASS** | unchanged |
| PCR5 | PASS | **PASS** | unchanged (Case-H Layer-5 scoping per P11D mapping) |
| PCR6 | PARTIAL | **PASS** | every B1/B2/B3 parameter registered + tagged (Table 2); convention documented |
| PCR7 | PARTIAL | **PARTIAL (unchanged)** | steering figure-of-merit pending P12B |
| PCR8 | PASS | **PASS** | unchanged |
| G1 | MET | **MET** | unchanged |
| G2 | MET | **MET** | unchanged (suite green incl. new guards) |
| G3 | NOT MET | **NOT MET (unchanged)** | no author tables; B2 ambiguity open |
| G4 | NOT MET | **NOT MET (unchanged)** | G3/PCR1 not met; PCR7 partial |

## 5. Tests

Suite after all P12A edits: **57/57 PASS** (53 pre-existing + 4 new P12A
guards).  Historical P11D practice (suite run at every commit) followed.

## 6. Git

Commit chain (titles): **P12A-C1** source-figure correction (F1), regenerated
evidence/Fig. 4/Table 3; **P12A-C2** PCR6 registry rows + Table 2; **P12A-C3**
hygiene (F2/F4/F5), guard tests, this close-out.  SHAs: see `git log` (a file
cannot embed its own hash; P11D convention).  `main` never touched; Blueprint
never touched; history never rewritten.

## 7. Remaining blockers after P12A (unchanged from P12 audit)

1. G3/PCR1 external ≤2% — class C/D (author evidence needed for Layer 2a;
   antiplane decision + run for 2b; P12D can close Layer 1).
2. B2 l/l̄ ambiguity — OPEN (P12A corrected wording only; source defines
   l̄ = l/b; three labelled interpretations stand).
3. Case-C Δ_complete not mesh-converged — P12C (32² minimum; 64² conditional;
   separate authorization).
4. PCR7 steering figure-of-merit — P12B (cheap S7 θ-sweep extension).
5. PI-level: author contact; Blueprint v1.4 decisions.
