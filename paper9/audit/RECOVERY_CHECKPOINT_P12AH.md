# Recovery checkpoint — P12AH (Table-2 layout repair and generator reconciliation)

**Phase:** P12AH · **Date:** 2026-09-24 · **Entry commit:** `b45ea785cadfc0ae09ffcba0c0d11153c6144bd4`
**Branch:** `phase-1-symbolic` · **Remote:** `https://github.com/vipin-oss/BFS-FEM-MATLAB`

## Authorised scope (P12AG report §6, items 1–2; item 3 resolved in §3 below)

1. `paper9/tables/gen/tab03_anchor_errors.py` reconciled so it can be run at all — it now embeds the
   P12AF-authorised Table 2 plus the layout correction.
2. Table 2 layout repaired so its Status column is no longer pushed off the printed page. Layout only:
   undoing the edits returns the file byte-for-byte to the P12AF bytes (`77fd7584…`).
3. Figure 5: the content re-scope option was taken — the committed figure PDF is byte-unchanged
   (`3d309eaa…`) and its derivation inputs are hashed in `P12AH_FIGURE_FRESHNESS.json`.

## Commits in this phase

| # | commit | content |
|---|---|---|
| 1 | `2bb91f8` | first pass: layout repair applied to seven tables (superseded — see #4) |
| 2 | `eca80da` | guards + `P12AH_FIGURE_FRESHNESS.json` (P12AH guard later narrowed) |
| 3 | `3fba402` | P12AF phase guards re-anchored on the entry commit; allowlist extended |
| 4 | `8bc1544` | **scope correction:** tab01/tab02/tab04/tab05/tab06/tab07 restored byte-for-byte to `b45ea78`; guards narrowed to Table 2 |
| 5 | (this file) | record + checkpoint corrected to the authorised scope |

`git diff b45ea78…HEAD` touches only: `gen/tab03_anchor_errors.py`, `out/tab03_anchor_errors.tex`,
`test_p12af_manuscript_retiering.py`, `test_p12ag_clean_build.py`, `test_p12ah_generator_and_layout.py`,
`P12AH_FIGURE_FRESHNESS.json` and the two P12AH audit records.

## State at checkpoint

* Working tree clean except the untracked in-repo build product `paper9/latex/ms.pdf`.
* Full suite: **351 passed, 1 skipped** (`pytest paper9/verification/suite`).
* Repo-only build (clean scratch tree, `pdflatex ×2 → bibtex → pdflatex ×3`): **0 errors, 0 undefined
  citations/references, 611 overfull boxes, 35 pages**, PDF 888 647 B — copied to
  `/home/user/p12ah_manuscript_build.pdf`. Table 2 (page 32) is fully readable:
  `/home/user/p12ah_table2_fixed.png`.
* The manuscript's remaining large boxes are the pre-existing ones listed in the phase record §7; they are
  **not applied** and would need a fresh authorisation.

## Frozen statuses (unchanged, not to be relabelled)

B1 GRAPHICAL_VALIDATION / PASS · B2/B3 NOT VALIDATED · B3 ESTABLISHED / SOURCE-EQUIVALENT ·
`quantitative_error` NULL ×3 · PCR1 NOT PASS · G3/G4 NOT MET · P5 NOT PASS / OPEN · R-1 OPEN ·
C-1 closed as a criterion item · PCR5 PASS · author-data route NOT SENT / NOT AUTHORISED ·
external benchmark hunt CLOSED · **submission NOT AUTHORISED**.

## Governing hashes (unchanged)

Blueprint v1.5 `b96c8e76…` · v1.4 `2ae0b1e8…` · v1.3 `ca71b91a…` · Rule R-fit `d4fed492…` ·
active record `2fad2d92…` · P5_STATUS `1a410f22…` · register `83ff8723…` / `8d86528f…` ·
A2 amendment `c008a00e…` · `p4b_5g_to_5i.json` `38384363…` · drafts P12L `8acb70f1…` /
P12M `2f68e66f…` / P12Q `1f060350…`.

## How to resume

1. `git fetch origin && git rev-parse HEAD origin/phase-1-symbolic` — expect all three (plus
   `git ls-remote`) equal to the final commit recorded in the phase report.
2. `python3 -m pytest paper9/verification/suite -q` — expect **351 passed, 1 skipped**.
3. Rebuild from the repo only: scratch tree with `paper9/latex/`, `paper9/tables/out/`,
   `paper9/figures/out/`, `paper9/bib/paper9.bib`; `pdflatex ×2 → bibtex ms → pdflatex ×3`; expect
   0 errors, 35 pages, 611 overfull boxes, Table 2 readable on page 32.
4. Do **not** regenerate `figures/out/fig05_mesh_convergence.pdf` for freshness checks: it regenerates
   pixel-identically but with different bytes; freshness is asserted by input hashes in
   `paper9/audit/P12AH_FIGURE_FRESHNESS.json`.
5. Do not run a table generator expecting a content change: each table file is a byte-reproducible product
   of its generator, and the guard suite asserts it (Table 2's generator was the stale one — now fixed).
