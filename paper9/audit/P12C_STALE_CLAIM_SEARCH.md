# P12C Repo-Wide Stale-Claim Search (Part I)

Scope: all git-tracked files (240), read-only, executed at the post-Parts-C/E fix state
(commits `75d2eb9`, `3138584`, `355c660`). No historical record was deleted or rewritten.

**Classification key**
- **ACTIVE** — current manuscript / current status documents; must be true today.
- **HISTORICAL** — dated audit-phase records of past states (P6–P12B). Retained by design;
  they describe the phase in which they were written.
- **EVIDENCE** — raw/processed data and run logs. Immutable; string hits inside JSON are data
  (often digit substrings of longer literals), not claims.
- **FIXED** — was stale in active text, corrected in this audit (commit recorded).
- **STALE** — contradicts current state while presented as current. **Post-fix count: 0.**

## 1. Headline terms (task-mandated)

| term | active-manuscript hits | where | verdict |
|---|---|---|---|
| “fully solved” | **0** (was 1) | — | **FIXED** (`75d2eb9`; sec08 wording) |
| “quadrature invariance” | **0** (was 1) | — | **FIXED** (`75d2eb9`; sec06 re-scoped to X-gap at 4×4) |
| “exact interface” | **0** | — | clean |
| “exact curved” | **0** (1 historical) | `P11_CASE_C_IMPLEMENTATION_AUDIT.md` (says the interface is *not* exactly represented) | HISTORICAL, honest |
| “converged complete gap” | **0** (guards + 1 historical) | `test_p12c_caseC_64.py` (asserts its absence), `P11D_REMEDIATION_AUDIT.md` (shows it is not produced) | guards/HISTORICAL |
| “mesh-converged” | **5, all negations** | sec06 (43), sec08 (8, 16), sec09 — “not mesh-converged” / “no mesh-converged … claimed” | ACTIVE, correct (asserted by guards) |
| “P5 PASS” | **0 anywhere** | — | clean |
| “P5 NOT PASS” | 2 | `audit/P5_STATUS.md`, `audit/P5_READINESS.md` | ACTIVE-status, correct |
| “NOT PASS” | 0 in manuscript; 64 audit-docs | status/history docs | HISTORICAL/status |

## 2. Case-C series numbers

| term | active-manuscript | audit-docs | evidence+guards | verdict |
|---|---|---|---|---|
| 2.5732 | 18 (sec06/08/09) | 52 | 4 + 4 | ACTIVE (correct, 4×4-mesh attribution present) |
| 2.2504 | 5 | 20 | 1 | ACTIVE |
| 2.0722 | 5 | 22 | 16 + 1 | ACTIVE |
| 1.9736 | 6 | 4 | 7 + 2 | ACTIVE |
| 1.9179 | 6 | 2 | 1 + 1 | ACTIVE |

(Historical audit-doc hits are the P11A–P12C records of how the series evolved; evidence-file
hits are data. No active occurrence claims a converged width — verified in Part A/B.)

## 3. Mesh-size tokens

| term | manuscript | guards | evidence | notes |
|---|---|---|---|---|
| `4x4`/`8x8`/`16x16`/`32x32`/`64x64` (unspaced) | **0** (all manuscript forms use `\times`) | 43/28/31/43/32 | 40/30/25/13/13 | legacy token in code/guards/evidence only — no active prose |
| `4\times4` … `64\times64` | present in sec06/08/09 series context | — | — | ACTIVE, correct |

## 4. Gates (PCR1 / G3 / G4)

| term | manuscript | plan+blueprint | audit-docs | verdict |
|---|---|---|---|---|
| PCR1 | 1 (sec08: “Gate G3 remains formally NOT MET”) | 20 | 144 | ACTIVE statement = NOT MET ✓ |
| G3 | 3 (sec05, sec08×2: NOT MET) | 37 | 243 | ACTIVE statements = NOT MET ✓ |
| G4 | 0 | 12 | 127 | no manuscript claim; audit-docs historical |

**Historical-numbering warning (recorded, not edited):** `P6_FINAL_GATE_AUDIT.md` and
`P9_FINAL_RELEASE_AUDIT.md` use a pre-P11 PCR numbering (“PCR1 = Layer-1 classical limit”).
They are HISTORICAL; the authoritative mapping is `P11D_PCR_MAPPING.md` + P12A/P12B updates.

## 5. FIXED items (this audit) — before/after

1. sec08 “Case C is **fully solved**” → “Case C is documented …” (`75d2eb9`).
2. sec08 “circular inclusion geometry is **resolved** … (TV18)” → “treated with the locked
   immersed Gauss–Legendre quadrature of TV18 (sub-cell sampling; boundary approximated …)”.
3. sec08 “All 18 TVs are **resolved and closed**” → “carry a definitive recorded status
   (closed or locked …)” (matrix: 8 CLOSED / 10 LOCKED).
4. sec06 quadrature item “stop-band widths … **quadrature invariance to within 1.22 %**” →
   “X-point directional gaps Δ_X at the fixed 4×4 mesh … deviations −1.22 % / +1.08 % …”.
5. sec04 degree claim (“quartic”/“quadratic” products) → degree-six per coordinate + cut-element
   O(h) caveat (M14).
6. sec05 fig. 5 description + caption, 5i configuration, 5a–5h test list, Level-1 tolerance,
   ε_Δ display equation; ms.tex abstract “no theoretical order claimed” (`75d2eb9`,`3138584`).

## 6. Retained by design (no edits)

- **HISTORICAL audits** P6/P9/P10/P11A/P11B/P11D/P12A/P12B: contain the era's wording, including
  “invariant to within 1.22 %” (P11B) and the Δ_X/Δ_complete conflation analysis (P11D). They
  document how the current state was reached and are referenced as provenance.
- **EVIDENCE**: `results/raw/p11_caseC_convergence.json` metadata still carries the P11B-era
  string “TV18 resolved … smooth indicator function”. It is preserved raw output (README:
  “superseded runs are kept, not deleted”); the active manuscript no longer repeats it (Part C).
- **Traceability master** already distinguishes P11D-era statuses; Part B added a separate
  number-level artefact rather than rewriting it.

## 7. Residual watchlist

| item | why it matters | action if context changes |
|---|---|---|
| `p11_caseC_convergence.json` metadata “TV18 resolved” wording | could be quoted as current TV18 status | quote TV18 from `traceability_matrix.json` (LOCKED [S]) instead |
| P11B “quadrature errors negligible” | one-observable, one-mesh statement | cite Part D scope if ever quoted |
| P12A table “PCR7 PARTIAL … pending P12B” | superseded by P12B §6 (PCR7 PASS) | use P12B as the newer authority (both retained) |
| P4B `txt` vs `json` divergence (Part E F-1) | the txt log reports slope 5.4857 / ε 4.626e-11 | do not quote the txt; quote the JSON (governing) |
