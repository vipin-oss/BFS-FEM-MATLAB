# RECOVERY CHECKPOINT — P12AF (pre-work)

**Phase:** P12AF — record the PI grant (P12AE decisions A–F) and perform the scoped manuscript edit
authorised by P12AE §B. **Branch:** `phase-1-symbolic`. This is the **pre-work** checkpoint; the final
form is written at phase exit.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| **Entry (verified tri-equal, clean)** | `8fc80cee5315825ca92c944347c787e053653dd9` (P12AE phase head) |
| Entry P12AE final checkpoint | `a944ac856c05ed54376025c2b6a8fba0020e5e0f` |
| Entry immutability baseline | `/home/user/p12af_baseline_hashes.txt` (tracked files, content sha256) |
| Manuscript hash at entry | set `5ba2c22e…` (12 `.tex` under `paper9/latex/`) |
| Governing Blueprint | v1.5 `b96c8e76…` — must remain byte-identical |
| Rule R-fit | `d4fed492…` — must remain byte-identical |
| Machine record | `benchmark_validation_record.json` `2fad2d92…` — must remain byte-identical |
| `P5_STATUS.md` | `1a410f22…` — must remain byte-identical |
| Source PDFs | must remain byte-identical |

## Scope declared before the work

1. Record the PI grant of P12AE decisions A–F in the P12AE signature block as an explicit internal act,
   using only PI identity/date/recording information available in the project context; mark
   genuinely-unavailable metadata as an explicit field rather than inventing it.
2. Perform **only** the manuscript edit authorised by P12AE §B:
   (i) insert the P12AD §E limitation statement in `paper9/latex/sections/sec05_verification.tex`;
   (ii) the A2 re-tiering required by Blueprint v1.5 §A2.8 and `P12S_MANUSCRIPT_IMPACT.md` J.1–J.5 in the
   same file; (iii) the benchmark-status re-tiering in `paper9/tables/out/tab03_anchor_errors.tex`.
   Byte-minimal; no equation, figure, data, numeric, stylistic or reference change.
3. Preserve B1 `GRAPHICAL_VALIDATION`/PASS, B2/B3 `NOT_VALIDATED`, B3 formulation
   `ESTABLISHED / SOURCE-EQUIVALENT`, `quantitative_error` NULL, and all gate states
   (PCR1 NOT PASS · G3 NOT MET · G4 NOT MET · P5 NOT PASS/OPEN · R-1 OPEN · C-1 closed as criterion item ·
   submission NOT AUTHORISED). No promotion wording.
4. Compile the manuscript and report errors / overfull boxes / cross-references / numbering.
   **Pre-existing compile blockers found at entry** (must be reported, not fixed — outside the authorised
   file list): (a) `paper9/latex/ms.tex` uses `\RaggedRight` in its column-type definitions without
   loading `ragged2e`; (b) `paper9/tables/out/tab06_convergence_floor.tex` has two malformed
   `\multicolumn` column specs (`{@{l@{}}` at its lines 13 and 15) that raise `\GenericError` inside
   `tabularx` and abort the run. The compile check therefore uses a **build-only harness** in `/tmp`
   (loader shim + temp-copy correction of those two specs); **no repo byte is changed by the harness**.
5. Run the existing manuscript/traceability/immutability guards; re-point only the pins that the
   authorised edit legitimately invalidates, and record every such re-pointing.
6. Commit → push → fetch → verify local = origin = ls-remote; final recovery checkpoint.

## Planned artefacts

* P12AE signature block completion (grant recorded) — edit of the existing record, no new layer.
* The two edited manuscript files (`sec05_verification.tex`, `tab03_anchor_errors.tex`).
* `paper9/audit/P12AF_MANUSCRIPT_RETIERING_RECORD.md` — the traceability record of the edit (before/after
  hashes, exact edits, compile result, guard result).
* Re-pointed guard pins (only where the authorised edit invalidates them).
* this checkpoint (final form) at phase exit.
