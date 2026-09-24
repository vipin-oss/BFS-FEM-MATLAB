# BLUEPRINT v1.5 — AMENDMENT A2: EXTERNAL-VALIDATION EVIDENCE ROUTES

**Phase:** P12R · **Date:** 24 September 2026 · **Blueprint delta:** v1.4 → **v1.5**
**Pre-work checkpoint:** `26dbcf88d2bab7292e77ea32307d61d42496d398` (pushed and verified before any edit)

| Artefact | sha256 |
|---|---|
| Blueprint v1.3 (unchanged, historical) | `ca71b91aba4ca4abe9f157eb595ac8c2f709d838957a08ea0dce7160685dbf9f` |
| Blueprint v1.4 (unchanged, byte-identical) | `2ae0b1e8f37e10a0685a0b0ffd94e695bd62e3b4da6a02052a76190fc0acb638` |
| **Blueprint v1.5 (new)** | **`b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91`** |
| Reference classifier | `paper9/verification/suite/benchmark_validation_route.py` |
| Synthetic tests | `paper9/verification/suite/test_p12r_graphical_validation_route.py` |

**Authority and honest framing.** A2 was directed by the PI in the P12R brief (24 September 2026). It is
a **deliberate, documented change of the validation-governance tier**: where the source publishes only a
graph, a benchmark can now satisfy the external-validation requirement (G3/PCR1) by an explicitly
labelled *graphical* route instead of the ≤ 2 % quantitative one. It **supersedes, by explicit PI
instruction, the earlier standing constraint "do not modify the Blueprint merely to accommodate missing
data"** — while retaining every integrity rule that constraint protected: no fabricated percentages, no
digitised error numbers, no presentation of graphical evidence as quantitative, no silent promotion of
any gate, and no change to the quantitative thresholds.

---

## 1. Audit — where v1.4 made numerical source data mandatory

Read from the authoritative file (line numbers in `Paper9_Blueprint_v1.4.tex`, 1082 lines):

| v1.4 line | Statement | Mandate it imposes |
|---|---|---|
| 95 | Version row (v1.4 = v1.3 + §5.7 Rule R-fit + PCR5 wording) | identity only |
| 442 | §5.1 row: "reference values are recomputed from the anchors' own equations, parameters and interface conditions with an independently written transfer-matrix code; digitised curves are used only to draw overlays, never to compute errors" | **compatible** with A2 — examined, **not amended** |
| 457 | G3 hard gate: "band-gap edges and the first four branch frequencies must agree with the published values to ≤ 2 %" | **decisive** — mandates quantitative agreement |
| 458 | G3 evidence row: "relative error per quantity; maximum relative error; explicit PASS/FAIL per benchmark" | **re-scoped by A2** (no relative error can exist on the graphical route) |
| 469 | Independent reproduction protocol: "Recompute each anchor's dispersion from its published equations…; curve digitisation is permitted only to draw overlay figures, never to compute error numbers" | **compatible** with A2 (it is exactly the graphical route's reconstruction step) — examined, **not amended** |
| 471 | Error definition: "PASS iff ≤ 2 %" | **decisive** |
| 803 | Week-8 schedule: "GATE G3 — ≤ 2 % on all three gates" | **decisive** |
| 886–888 | **PCR1**: "All mandatory published benchmarks (Layers 1, 2a, 2b) PASS with maximum relative error ≤ 2 %" | **decisive** |
| 1027–1030 | Section 12 record ("G3/PCR1 untouched in substance") | **historical record** — deliberately not amended (see §5) |
| 1046 | v1.1-consistency bullet: "G3/PCR1 require … ≤ 2 %" | **decisive** (summary statement) |

**Conclusion of the audit:** the numerical-data mandate is carried by exactly six line-blocks
(95, 457, 471, 803, 886–888, 1046). Lines 442 and 469 were examined and require **no** change — they
already describe independent reconstruction and forbid using digitised curves for error numbers, which
is precisely the graphical route's discipline.

---

## 2. Versioning question and the exact Delta (v1.4 → v1.5)

**Question:** did v1.3 → v1.4 already introduce a locked amendment structure? **Yes.** v1.4 is v1.3 plus
**exactly four** changed single-line blocks (verified in this phase by `difflib` opcodes):

```
replace  v1.3[95:95]   -> v1.4[95:95]     (version row)
replace  v1.3[446:446] -> v1.4[446:446]   (§5.7 Rule R-fit)
replace  v1.3[618:618] -> v1.4[618:618]   (figure register — PCR5 wording)
replace  v1.3[895:896] -> v1.4[895:895]   (PCR5 item)
```

**Consequence, and the decision taken:** v1.4 is preserved **byte-identical** (never rewritten, never
re-edited) and the amendment is carried by a **new** file, `Paper9_Blueprint_v1.5.tex` = v1.4 + the
smallest possible new delta. Versioning therefore follows the established pattern — a frozen copy per
revision plus a frozen amendment record — and the v1.6-style chain stays auditable:
`v1.3 → v1.4 (A1: Rule R-fit) → v1.5 (A2: evidence routes)`.

**Delta v1.4 → v1.5 — exactly 8 blocks (6 replacements + 2 insertions), verified by opcode comparison:**

| # | Type | v1.4 lines | v1.5 lines | Content |
|---|---|---|---|---|
| 1 | replace | 95 | 95 | version row → 1.5, A2 named, v1.4/v1.3 provenance recorded, §5.7 untouched |
| 2 | replace | 457 | 457 | G3 criterion → two admissible routes (quantitative / graphical), "not validated" fails |
| 3 | replace | 471 | 471 | error definition → quantitative route only; no error on the graphical route |
| 4 | replace | 803 | 803 | Week-8 gate row → each gate met quantitatively **or** by the labelled graphical route |
| 5 | replace | 886–888 | 886–891 | PCR1 → three-state item (quantitative ≤ 2 % / graphical labelled / not validated) |
| 6 | replace | 1046 | 1049 | v1.1-consistency bullet → route-aware wording, thresholds unchanged |
| 7 | insert | before 1052 | 1055–1158 | **new Section 13 — AMENDMENT A2** (routes, hierarchy, B2 rule, A2.5, classification contract, decision table, non-promotion) |
| 8 | insert | before 1082 | 1189–1190 | additive note appended to the footer revision banner (historical lines untouched) |

Nothing else in v1.4 was altered: no equation, parameter, mesh, gate G1/G2/G4 meaning, benchmark card,
figure/table register, schedule item or scientific requirement. Brace balance holds (1245/1245).

---

## 3. The three routes (as enacted in v1.5, Section 13)

* **A2.1 (a) Quantitative validation** — source numerical values exist → the *existing* comparison and
  the *existing* thresholds (≤ 2 %; ≤ 0.5 % classical target), prescribed error reported.
* **A2.1 (b) Graphical validation** — no machine-readable source values, but a sufficiently detailed
  graph **and** the material/geometric/normalisation/boundary-interface information needed to
  reconstruct the case → reproduce, compare directly with the published curve, preserve the figure
  identification and axes, document branch identity / ranges / turning points / gap features, provide an
  overlay where technically possible, and label the result **GRAPHICAL VALIDATION**.
* **A2.1 (c) Not validated** — insufficient graph or insufficient accompanying information (or an
  unresolved source ambiguity) → **no claim**, G3/PCR1 item fails for that benchmark.
* **A2.3 hierarchy** — numerical > graphical-with-sufficient-parameters > insufficient; the lower route
  may never be presented as stronger, and where source numerics exist the graphical route is unavailable.
* **A2.4 (B2 rule)** — the 2024 Fig. 2(b) `l` vs `l̄` ambiguity must be resolved from authoritative source
  information before B2 is accepted under *either* route; no silent interpretation.
* **A2.5 (no fabricated precision)** — graphical agreement is never converted into a percentage
  ("1.x %", "<2 %", or any bound) unless source numerics exist or a separately governed, explicitly
  declared digitisation protocol is approved — **A2 approves none**.

---

## 4. Decision table (as enrolled in the Blueprint, A2.7)

| Evidence situation | Route and required treatment |
|---|---|
| Source numerical values available | **Quantitative route** — existing comparison, existing thresholds (≤ 2 %; ≤ 0.5 % classical), prescribed error reported |
| Graph only, parameters sufficient | **Graphical route** — reproduce, overlay, document observables, classify GRAPHICAL VALIDATION; **no percentage** |
| Graph only, parameters ambiguous or insufficient | **Not validated** — no claim; the G3/PCR1 item fails for that benchmark |

Machine-readable contract (A2.6): `QUANTITATIVE_VALIDATION` · `GRAPHICAL_VALIDATION` ·
`NOT_VALIDATED`; a graphical record carries **no** numerical error field. Implemented in
`paper9/verification/suite/benchmark_validation_route.py` and tested synthetically in
`paper9/verification/suite/test_p12r_graphical_validation_route.py` (cases 1–6 as required: numerical →
quantitative; graph-only sufficient → graphical; ambiguous parameter → not validated; insufficient
source → not validated; look-alike curve with a different parameter set → **not PASS**; graphical
agreement → stays graphical, never quantitative; plus a fabricated-precision guard).

---

## 5. Historical records and stale statements — classified, not rewritten

* Sections 11–12 of the Blueprint (revision records for v1.0→1.1 and 1.1→1.2, including the sentence
  "G3/PCR1 untouched in substance") are **historical records of earlier revisions**; they are left
  byte-identical and do not state current acceptance policy. A2.8 says so explicitly in the document.
* The footer banner still reads "Blueprint LOCKED v1.2" — a **pre-existing** staleness (already false at
  v1.3/v1.4, deliberately not rewritten); A2 appends a one-line revision note instead of editing history.
* `paper9/plan/blueprint/PROVENANCE.md` lists only v1.2/v1.3 and calls v1.3 "CURRENT governing
  specification", which has been stale since v1.4; a purely **additive** v1.4/v1.5 provenance block is
  appended below the existing rows (nothing above it is altered).
* `P12K_PCR1_G3_BLOCKER_FORENSIC_AUDIT.md`, `P12L_*`, `P12M_*`, `P12N_*`, `P12O_*`, `P12P_*`, `P12Q_*`
  remain valid as statements of the state *at their time*; the author-data route they describe is
  retained as the **higher-tier (quantitative) fallback**. Nothing was deleted.

---

## 6. Promotion status — no gate moves because A2 exists

| Item | Before P12R | After the A2 amendment |
|---|---|---|
| PCR1 | NOT PASS | **NOT PASS** (unchanged) |
| G3 | NOT MET | **NOT MET** (unchanged) |
| G4 | NOT MET | **NOT MET** (unchanged) |
| P5 | NOT PASS/OPEN | **NOT PASS/OPEN** (unchanged) |
| R-1 | OPEN | **OPEN** (unchanged) |
| PCR5 | PASS | **PASS** (unchanged) |
| P13 | BLOCKED | **BLOCKED** (unchanged) |
| B1/B2/B3 `quantitative_error` | NULL | **NULL** (unchanged) |

Promotion requires an actual, audited benchmark reproduction under A2 — a later, separately authorised
phase. A2 supplies the rule; it supplies no evidence.

---

## 7. Non-modification record (immutability verified in this phase)

| Artefact | Requirement | Result |
|---|---|---|
| Blueprint v1.3 | byte-identical | `ca71b91a…` ✔ |
| Blueprint v1.4 | byte-identical (frozen prior amendment) | `2ae0b1e8…` ✔ |
| Rule R-fit `rule_rfit.py` | unchanged | `d4fed492…` ✔ |
| Governing JSON / historical TXT / P4B script | unchanged | `38384363…` / `1daf0f32…` / `b1c8d996…` ✔ |
| `benchmark_evidence.json` | unchanged; B1/B2/B3 still NULL | `e9191506…` ✔ |
| Manuscript (latex/, tables/out, figures/out) | untouched | ✔ (no diff) |
| P12M author-request drafts | not deleted, not modified | sha `2f68e66f…` ✔ |
| Thresholds (2 % / 0.5 %) | unchanged | ✔ (code + Blueprint) |

---

## 8. Downstream obligations created by A2 (not executed here)

1. **Manuscript re-tiering (separately authorised):** every validation sentence must state the tier
   actually achieved; a graphically validated benchmark may not be described with a percentage or as
   "quantitative agreement", and Table 3's error columns cannot be filled for such benchmarks.
2. **Submission-gate consequence:** G3 can now be satisfied on the graphical route, but only with the
   label, the overlay and the documented observables in the main text — the evidence-in-manuscript rule
   is unchanged.
3. **Author-data request package (P12M/P12L):** retained; if data ever arrive, the benchmark moves to
   the quantitative route and must then meet ≤ 2 % (B1 ≤ 0.5 %) as before.

## 9. Reproduction

```
python3 - <<'EOF'
import hashlib, difflib
from pathlib import Path
a = Path("paper9/plan/blueprint/Paper9_Blueprint_v1.4.tex").read_text().splitlines(keepends=True)
b = Path("paper9/plan/blueprint/Paper9_Blueprint_v1.5.tex").read_text().splitlines(keepends=True)
print(len([o for o in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes() if o[0]!="equal"]), "blocks (expect 8)")
print(hashlib.sha256(Path("paper9/plan/blueprint/Paper9_Blueprint_v1.4.tex").read_bytes()).hexdigest())
EOF
python3 -m pytest paper9/verification/suite/test_p12r_graphical_validation_route.py -q
```
