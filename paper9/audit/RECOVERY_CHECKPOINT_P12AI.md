# Recovery checkpoint — P12AI (final manuscript closure)

**Phase:** P12AI · **Date:** 2026-09-24 · **Entry:** `e986a13fdd82e8df1e2c93a534aa6ae4163bd8e6` (P12AH final)
**Branch:** `phase-1-symbolic` · **Remote:** `https://github.com/vipin-oss/BFS-FEM-MATLAB`

## What this phase closed

Inspection of the rendered PDF (not the TeX log) showed that **five** of the six tables P12AH left untouched
printed content outside the physical page, so the minimum content-neutral layout fix was applied to exactly
those five and to nothing else. **Table 6 (tab05) was left untouched** — it is fully readable.

* repaired: tab01 (Table 1), tab02 (Table 5), tab04 (Table 3), tab06 (Table 4), tab07 (Table 7)
* deliberately unchanged: tab05 (Table 6) — asserted byte-identical to the entry commit
* Table 2 (tab03) unchanged since P12AH — still `8b7de407…`, undo → P12AF bytes `77fd7584…`

Each repair is layout only and is proved content-neutral byte-for-byte by undoing it and comparing with the
pinned pre-layout content (see `P12AI_FINAL_CLOSURE_RECORD.md` §3).

## State at checkpoint

* Final build from repository sources: **0 LaTeX errors, 0 missing files, 0 undefined citations/references,
  6 overfull boxes (five prose paragraphs + the harmless Table 6 alignment box), 3 underfull, 34 pp,
  904 992 B**, per-page content streams reproducible from a second independent build.
* Every table lies inside the text block; no text anywhere in the document starts beyond the page edge
  (measured with the extraction clip widened to x = 4000 pt).
* Full suite: **375 passed, 1 skipped**.
* Working tree clean apart from the untracked build product `paper9/latex/ms.pdf`.

## Frozen scientific status (unchanged, not to be relabelled)

B1 GRAPHICAL_VALIDATION / PASS · B2/B3 NOT VALIDATED · B3 ESTABLISHED / SOURCE-EQUIVALENT ·
`quantitative_error` NULL ×3 · PCR1 NOT PASS · G3/G4 NOT MET · P5 NOT PASS / OPEN · R-1 OPEN ·
C-1 closed as a criterion item · PCR5 PASS · author-data route NOT SENT / NOT AUTHORISED ·
external benchmark hunt CLOSED · **submission NOT AUTHORISED**.

## Governing hashes (unchanged)

Blueprint v1.5 `b96c8e76…` · v1.4 `2ae0b1e8…` · v1.3 `ca71b91a…` · Rule R-fit `d4fed492…` ·
active record `2fad2d92…` · P5_STATUS `1a410f22…` · register `83ff8723…` / `8d86528f…` ·
A2 amendment `c008a00e…` · `p4b_5g_to_5i.json` `38384363…` · `fig05_mesh_convergence.pdf` `3d309eaa…` ·
`sec05_verification.tex` `bfd45dd0…` · drafts P12L `8acb70f1…` / P12M `2f68e66f…` / P12Q `1f060350…`.

## How to resume

1. `git fetch origin && git rev-parse HEAD origin/phase-1-symbolic` and `git ls-remote` — expect all three
   equal to the final commit in the phase report.
2. `python3 -m pytest paper9/verification/suite -q` — expect **375 passed, 1 skipped**.
3. Rebuild from the repo only (scratch tree with `paper9/latex/`, `tables/out/`, `figures/out/`, `bib/`);
   `pdflatex ×2 → bibtex ms → pdflatex ×3`; expect 0 errors, 34 pp, 6 overfull boxes, all tables inside
   the text block.
4. Do not regenerate figures to refresh timestamps: `fig05_mesh_convergence.pdf` regenerates
   pixel-identically but with different bytes; freshness is asserted by input hashes in
   `P12AH_FIGURE_FRESHNESS.json`.
5. Table files are byte-reproducible products of their generators; the guard suite asserts it.
