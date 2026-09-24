# Recovery checkpoint — P12AH (table-layout repair and generator reconciliation)

**Phase:** P12AH · **Date:** 2026-09-24 · **Entry commit:** `b45ea785cadfc0ae09ffcba0c0d11153c6144bd4`
**Branch:** `phase-1-symbolic` · **Remote:** `https://github.com/vipin-oss/BFS-FEM-MATLAB`

## Commits in this phase

| # | commit | content |
|---|---|---|
| 1 | `2bb91f8` | seven table generators + seven generated tables: layout repair, generators own their outputs |
| 2 | `eca80da` | new `test_p12ah_generator_and_layout.py`; P12AG/P12AF/P6 guard updates; `P12AH_FIGURE_FRESHNESS.json` |
| 3 | `3fba402` | P12AF phase guards re-anchored on the pre-phase commit; allowlist extended |
| 4 | (this file) | phase record + recovery checkpoint |

## State at checkpoint

* Working tree clean except the untracked in-repo build product `paper9/latex/ms.pdf` (as before this phase).
* Full suite: **369 passed, 1 skipped** (`pytest paper9/verification/suite`).
* Repo-only manuscript build (clean scratch tree, `pdflatex ×2 → bibtex → pdflatex ×3`): **0 errors, 0 undefined
  citations/references, 5 overfull boxes (body prose only), 34 pages**, PDF 905 012 B —
  copied to `/home/user/p12ah_manuscript_build.pdf`.
* Every repaired table compiles alone with **zero** overfull boxes and **zero** LaTeX errors
  (`test_p12ah_generator_and_layout.py::test_table_compiles_without_overfull_box`).
* Content neutrality proved per table: undoing the documented layout edits returns each file byte-for-byte to
  its pre-phase state (sha256 pins inside the guard; `tab03` → `77fd7584…`, the P12AF bytes).

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
2. `python3 -m pytest paper9/verification/suite -q` — expect **369 passed, 1 skipped**.
3. Rebuild from the repo only: scratch tree with `paper9/latex/`, `paper9/tables/out/`,
   `paper9/figures/out/`, `paper9/bib/paper9.bib`; `pdflatex ×2 → bibtex ms → pdflatex ×3`;
   expect 0 errors, 34 pages, 5 prose-level overfull boxes.
4. Do **not** regenerate `figures/out/fig05_mesh_convergence.pdf` for freshness checks: it regenerates
   pixel-identically but with different bytes; freshness is asserted by input hashes in
   `paper9/audit/P12AH_FIGURE_FRESHNESS.json`.
5. Do not run any table generator expecting a *content* change: every table file is now a byte-reproducible
   product of its generator, and the guard suite asserts it.
