# RECOVERY CHECKPOINT — P12AE (pre-work)

**Phase:** P12AE — PI authorisation and manuscript transition (preparation of the authorisation record
only). **Branch:** `phase-1-symbolic`. This is the **pre-work** checkpoint; the final form is written at
phase exit.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| **Entry P12AD final checkpoint** | `8d93d3fd6c37bb5f39facad6254d51ec87df6de5` (as named in the P12AE brief) |
| **Entry HEAD (verified tri-equal)** | `cd5fa0c229807a2a3e7e45efcb7e0aac8f967b23` (P12AD bookkeeping commit; local = origin = ls-remote) |
| Tree at entry | **clean** (`git status --porcelain` empty) |
| Entry immutability baseline | `/home/user/p12ae_baseline_hashes.txt` (all tracked files, content sha256) |
| Governing Blueprint | v1.5 `b96c8e76…` — must remain byte-identical |
| Rule R-fit | `d4fed492…` — must remain byte-identical |
| Machine record | `paper9/audit/benchmark_validation_record.json` `2fad2d92…` — must remain byte-identical |
| Manuscript | byte-identical (set `5ba2c22e…`) — **no manuscript edit in this phase** |
| P5 record | `paper9/audit/P5_STATUS.md` `1a410f22…` — must remain byte-identical |

## Scope declared before the work

1. Read the P12AD decision record, `P5_STATUS.md`, the P13/preparation status records, the A2 manuscript
   re-tiering records and the manuscript governance/traceability records for PCR1/G3/G4.
2. Prepare **one** concise PI-authorisation record containing exactly decisions **A–F** (P13
   preparation-only transition; the scoped manuscript editing; P5 preserved as P12AD recorded; R-1
   preserved; C-1 preserved; and the non-satisfaction statement).
3. **Do not edit the manuscript.** Do not mark the authorisation approved: no explicit PI approval for
   this transition exists in the repository, so the record is prepared as **PROPOSED / ready-to-sign**.
4. Do not modify Blueprint v1.5, Rule R-fit, PCR1/PCR2–PCR8, G1–G4, `P5_STATUS.md`, numerical results,
   benchmark classifications, source files or manuscript bytes.
5. Targeted guards only (no new audit, no literature search, no benchmark hunt, no numerical rerun, no
   gate analysis).
6. Commit → push → fetch → verify local = origin = ls-remote; final recovery checkpoint.

## Standing status at entry (unchanged by this phase, must remain unchanged)

B1 `GRAPHICAL_VALIDATION`/PASS · B2 `NOT_VALIDATED` · B3 `NOT_VALIDATED` (formulation
`ESTABLISHED / SOURCE-EQUIVALENT`) · `quantitative_error` NULL ×3 · PCR1 **NOT PASS** · G3 **NOT MET** ·
G4 **NOT MET** · P5 **NOT PASS/OPEN** · R-1 **OPEN** · C-1 closed as a criterion item (frozen Rule R-fit,
unamended) · PCR5 PASS · P13 **BLOCKED** until authorised · author-data route **NOT SENT / NOT
AUTHORISED** · external benchmark hunt **permanently CLOSED**.

## Planned artefacts

* `paper9/audit/P12AE_PI_AUTHORISATION_MANUSCRIPT_PREPARATION.md` — the authorisation record (decisions A–F;
  status: proposed / ready-to-sign).
* `paper9/verification/suite/test_p12ae_authorisation_record.py` — targeted guards.
* this checkpoint (final form) at phase exit.
