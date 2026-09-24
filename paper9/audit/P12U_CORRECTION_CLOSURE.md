# P12U — correction closure for the P12T findings F1–F3

**Phase entry (verified):** `9a71f6752e9b7f85e45b3aa81c3dbe1210b384a6` — local = `origin/phase-1-symbolic`
= `ls-remote`, clean tree. **Pre-work checkpoint:** `6937f5f61f9f054ce0c50db99db60b20430a16f8`
(pushed + verified before any edit).

**Scope:** correct **only** the factual/descriptive inconsistencies documented by the P12T independent
audit (F1, F2, F3) and pin them with regression tests. P12T is accepted as the audit baseline; the
substantive B1/B2/B3 route conclusions are **not** reopened, and no numeric, route, gate, threshold,
model, parameter or production artifact was changed.

---

## 1. F1 — B1 vertex strings corrected

| | |
|---|---|
| **Correction** | the vertex lists were replaced with the P12T-verified values: **k̄ = 0 → 0.0000 / 0.9795 / 1.0210 / 1.9809**; **k̄ = ±1 → 0.4799 / 0.5196 / 1.4998 / 1.9809** |
| **Locations** | `paper9/audit/benchmark_validation_record.json` (`benchmarks.B1.reproduction_status`) · `paper9/audit/P12S_GRAPHICAL_VALIDATION_AUDIT.md` (§Phase D) |
| **Also removed** | the defective strings `1.4799` / `0.5099` from the whole corrected corpus (verified: absent from all six corrected files) |
| **No new precision** | only P12T-established values were used; the audit file additionally cites the P12T-measured digitised published reference (k̄ = 1: 0.4803 / 0.5253 / 1.4991) |

## 2. F2 — baseline wording corrected everywhere

The statement "the source's own figure … require 0.50" was replaced by wording that clearly separates
the three quantities: **the source's own gradient ("Present", solid) curve ≈ 0.436** at k̄ = 1 ·
**the classical limit 0.500** · **the dashed literature [34] curve ≈ 0.50**. The value 0.500 is no longer
attributed to the source's gradient result anywhere.

| Location | Correction |
|---|---|
| `paper9/validation/p12s_run.py` (B3 `reason`) | "…the source's own gradient ('Present', solid) curve lies at ~0.436 there (P12T measurement, consistent with the digitised reading (1, ~0.45) recorded above); the classical limit is 0.500 and the dashed literature [34] curve is ~0.50…" |
| `paper9/audit/benchmark_validation_record.json` (`benchmarks.B3.reason`) | same string as the corrected script output (aligned verbatim) |
| `paper9/audit/P12S_GRAPHICAL_VALIDATION_AUDIT.md` (§Phase F) | "…the source's own gradient ("Present", solid) curve lies at **≈ 0.436** there (P12T measurement: present in 98 % of the last 60 pixel columns), the **classical limit is 0.500** and the dashed literature [34] curve is ≈ 0.50…" |
| `paper9/audit/RECOVERY_CHECKPOINT_P12S.md` (B3 row) | "…(lowest branch ≈ 0.35 vs the source's own gradient curve ≈ 0.436 at k̄ = 1; classical limit 0.500; dashed literature [34] curve ≈ 0.50)…" |
| `paper9/audit/P12S_MANUSCRIPT_IMPACT.md` (proposed B3 wording) | "…whereas the source's own gradient ("Present") curve lies at ≈ 0.436 (classical limit 0.500; dashed literature [34] curve ≈ 0.50)." |
| **Additional propagated copy** (found by this phase, same sentence) | `paper9/audit/evidence/p12s/p12s_validation_record.json` (`benchmarks.B3.reason`) — corrected, and **verified byte-equal to a fresh run of the corrected script** (only the `overlay` path field differs) |

## 3. F3 — internal consistency restored

`p12s_run.py` line 178 ("(1,~0.45)") is the accepted reading and was **not** altered. Lines 184–185 now
state the same curve with the P12T measurement (≈ 0.436) and explicitly note that it is consistent with
that digitised reading, so the file no longer contains two contradictory baselines.

**F4** (INFO — "numerically infeasible" is a practical statement) was **not** changed: P12T already
considered the wording qualified.

## 4. Verification performed

| Check | Result | Log |
|---|---|---|
| **Integrity re-run** of the corrected script into `/tmp` (committed evidence untouched) | runs end-to-end; **all six PNGs regenerate byte-identical**; the only JSON difference was the corrected B3 reason string and the redirected path field; all numeric fields identical | `evidence/p12u/corrected_text_inspection.txt` |
| Targeted tests (P12U closure + P12S anti-fabrication + P12R route) | **42 passed** | `evidence/p12u/targeted.txt` |
| Full regression ×2 | **168 passed, 1 skipped** each (151 before + 17 new P12U guards; no test weakened, removed or modified) | `evidence/p12u/suite_run1.txt`, `suite_run2.txt` |
| Guards (P12C post-closeout, P12H rule-R-fit, P12H C1, P12R, P12S, P12U) | **87 passed** | `evidence/p12u/guards.txt` |
| Numerical / manuscript / Blueprint cross-checks | **43 / 43** | `evidence/p12u/crosscheck.txt` |
| Immutability | **12/12** governing anchors unchanged; overlays, panels, P12T audit + evidence, `benchmark_evidence.json`, the P12S/P12R guard files byte-identical; blueprint dir, manuscript, production + results, source PDFs, author-request drafts **unchanged** | `evidence/p12u/immutability_and_correction.txt` |
| Independent re-inspection of the corrected text | defective strings absent from all six corrected files; every corrected file distinguishes 0.436 / 0.500 / dashed literature; F1 vertex values present in both locations; corrected raw record equals the corrected script output | `evidence/p12u/corrected_text_inspection.txt` |

**Two internal-consistency items were found and closed during the re-inspection** (both consequences of
the F2 correction, not new defects): the machine record's B3 reason was aligned verbatim with the
corrected script output, and the `evidence_path_sha256` fields (which pointed at the pre-correction raw
record `b1e7c17d…`) were refreshed to the corrected raw record `cffc0c88…`.

## 5. New regression guards (17 tests)

`paper9/verification/suite/test_p12u_correction_closure.py`:
* **F1** — the two corrected locations carry the P12T-verified k̄ = 0 and k̄ = ±1 vertex values and none
  of the defective strings; no defective vertex string survives in the corrected corpus.
* **F2** — each corrected file states the source's own gradient value **0.436**, the **classical limit
  0.500** and names the **dashed** literature curve; the three defective phrasings are asserted absent.
* **F3** — `p12s_run.py` keeps the accepted digitised reading `(1,~0.45)`, carries 0.436/0.500, and the
  two B3 readings agree within 0.02; no `require 0.50` baseline remains in any corrected file.
* **Closure invariants** — routes (`GRAPHICAL_VALIDATION` / `NOT_VALIDATED` / `NOT_VALIDATED`),
  `quantitative_error` `[NULL, NULL, NULL]`, gate states (PCR1 NOT PASS; G3/G4 NOT MET; P5; R-1; PCR5
  PASS; P13 BLOCKED), the numerical fields (B1 gaps 0.4801/0.5199, B2 `barred_required_dps` 52131,
  B3 gaps 0.3391/1.0213, ω₀ 411423336.09829) and the three overlay hashes are asserted unchanged, plus
  the record-to-raw-record evidence-hash consistency.

## 6. Statements (all verified)

* Blueprint v1.3/v1.4/v1.5, Rule R-fit, governing P4B artifacts, `benchmark_evidence.json`, P12M drafts
  and `PROVENANCE.md` — **unchanged**.
* Manuscript, production code and results, source PDFs, author-request drafts — **unchanged**.
* B1 `GRAPHICAL_VALIDATION`/PASS · B2 `NOT_VALIDATED` · B3 `NOT_VALIDATED` · `quantitative_error`
  `[NULL, NULL, NULL]` — **unchanged**.
* PCR1 **NOT PASS** · G3 **NOT MET** · G4 **NOT MET** · P5 **NOT PASS / OPEN** · R-1 **OPEN** ·
  PCR5 **PASS** · P13 **BLOCKED** — **unchanged**.
* No author contact, nothing sent, no P13 work, no benchmark tuning. Diff of this phase: 6 text files
  (+20/−14) plus the new guards, evidence and this record.
