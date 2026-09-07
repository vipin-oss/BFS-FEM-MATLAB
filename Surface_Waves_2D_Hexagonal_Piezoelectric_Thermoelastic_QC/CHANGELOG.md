# CHANGELOG.md

## Archive closure (final archival packaging, 2026-09-07)

- Built self-contained long-term archive FINAL_QC_SURFACE_WAVES_RESEARCH_ARCHIVE
  from the accepted Task-15 package (science untouched; packaging only).
- Restructured per archive spec: tests/V0…V5 subdirs; figures/style.py and
  figures/make_all_figures.py at figures/ level (paths updated);
  results/manifests/ (raw checksums); verification/{branch_identity,symbolic,
  model_limits,two_path,reports}/; manuscript/{supplementary,figures}/;
  literature/ (metadata-only, 47-entry bib, 8 categories); provenance/ (4
  documents); archive/ (both historical packages).
- run_all.py: manuscript/figures/ journal copies auto-synced before compile.
- Pipeline re-verified in place: invariants 22/22 PASS; figures regenerated
  content-identical; manuscript 29 pp, 0 errors.

## Task 15 (figure polishing + reproducible package closure, 2026-09-07)

- Baseline frozen: upstream ZIP sha256 b8178605…c4244ec2; git ea257c9;
  solver record hash 8c0abbabe66776dd. No science reopened.
- Built FINAL_RESEARCH_PAPER_PACKAGE/: solver, drivers, tests, raw data
  (byte copies), figures pipeline (style.py + make_all_figures.py →
  fig1..fig11.pdf), manuscript (graphicspath-adapted), 6 audits,
  verification/verify_invariants.py (22 checks incl. branch identity at
  Ω*=1000: V_C(D_w*→0)=0.3107266158, |ΔV|=2.4e-11, NOT the 0.467 branch),
  run_all.py (default / --check-only / --from-scratch).
- Fig2a annotations made data-driven (formatted from CSV; grep-verified
  zero hand-typed result values).
- Compile loop fixed to rerun until cross-references stabilise (0 warnings).
- Clean-room reproduction test PASS (fresh dir, artifacts deleted, all
  figures stream-identical, manuscript 29 pp / 0 err / 0 warn).
- Task-15 package archived verbatim at
  archive/FINAL_QC_SURFACE_WAVES_PAPER_PACKAGE_2026-09-07.zip
  (sha256 1c7c55d7672ecf8d9229a44a2b68b0dfe2348e7305042f11a9e87036e8042fe6).


## Task 14 (figure redesign, 2026-09-07) — delta over Task 13

- Figures: 13 → 11. New generation script `figures_v2/make_figures_v2.py`;
  outputs in `figures_v2/`. Old Task-13 script retained for provenance.
- Fig. 1 fully redrawn (embedded title/paragraph removed; continuum-style
  schematic with decay envelope, δ* bracket, BC line, fields/model box).
- Fig. 2 = merged old 2a+2b (2 panels; de-cluttered labels; roundoff band).
- Fig. 3 = 3 panels (branches; |V_B−V_C| vs absolute floor; P_w).
- Fig. 4 = 3 panels (ΔBC; ΔBC/floor with unity criterion; ΔAC).
- Fig. 5 = 3 panels (B/C V* slices at D_w*=1e-2,1,1e2,1e4; ΔBC; χ=Ω*/Ω_c
  master-curve collapse).
- Fig. 6 = 2 panels (Δ_T(Ω*); Δ_T(τ0*Ω*) with merged relaxation branch).
- Fig. 7 = 2 panels (ΔV/V; δ* change) + model-A note; degenerate A values
  never plotted.
- Fig. 8 = enlarged 3×3 roots, per-panel scaling.
- Fig. 9 = NEW genuine 3D: V_B, V_C, log10 Δ_BC surfaces with base-plane
  contour projections; z-ranges exactly the data ranges; Ω_c reference line
  on base plane labelled reference-only.
- Fig. 10 = old 9c as exact-cell heatmap with sample dots (no interpolation).
- Fig. 11 = old 8b upgraded to 121-pt δ*(Ω*) + Ω*δ* scaling panel.
- Captions rewritten in sample-paper style; all cross-references remapped
  (fig2a/2b→2, 9a/9b→9, 9c→10, 8b→11); surrounding interpretation paragraphs
  extended per panel (question→figure→observation→mechanism→implication).
- Science frozen: no number, equation, parameter, gate, floor, branch
  identity, or conclusion changed; raw data read-only; no new simulations.
- New/updated deliverables: FIGURE_REDESIGN_AUDIT.md,
  FIGURE_DATA_TRACEABILITY.md, SPIKE_AND_ANOMALY_AUDIT.md, this changelog,
  FINAL_PRODUCTION_REPORT.md.
- Build: 30 pp, 0 errors / 0 LaTeX warnings / no overfull ≥10 pt; figures
  within one page of first citation.

---

# FINAL_MANUSCRIPT_CHANGELOG.md — Task 13 (presentation upgrade, 2026-09-07)

Baseline: Task-12 FINAL_MANUSCRIPT (21 pp, 18 refs, 13 figures).
Output: 30 pp, 47 refs, 13 figures. **Science frozen throughout: no equation,
parameter, number, gate, threshold, or claim was changed.** All numerical
values in the rewritten manuscript were carried over verbatim from the Task-12
text; figures were regenerated from the same raw data files.

## 1. Structure

- Introduction expanded from ~1.5 pp of unnumbered prose to ~3 pp with
  numbered subsections 1.1–1.5 (sample-paper style): QC/phason foundations →
  phason dynamics classes → surface waves in anisotropic/piezoelectric/
  thermoelastic media → 1D vs 2D hexagonal QC literature → gap, RQ1–RQ4,
  contributions, roadmap. Note: ~3 pp rather than ~2 pp because the verified
  literature base grew from 18 to 47 references; each paragraph states what it
  establishes and why it matters for this study (no citation dumping).
- §5–§6 split: "Verification and benchmarks" (§5) and "Results" (§6) with a
  per-figure interpretation paragraph immediately after each figure
  (what is plotted / what changes / what does not / mechanism / what it
  supports for the RQs / limitations).
- New §7 Discussion with subsections 7.1–7.9 (branch selection; model A
  physics; model B physics; model C and Ω/Ω_c; why the thermal effect is
  small; phason BC physics; penetration structure; relation to 1D hexagonal
  literature; limitations incl. new items 2D-hex scope and parameter ranges).
- §8 Conclusions rewritten as 6 items, each with result + physical meaning +
  modelling implication.
- Nomenclature, Data-availability, Declarations unchanged (placeholders kept).

## 2. Bibliography: 18 → 47 entries

- 29 new entries, all verified by web search on 2026-09-06/07 (see
  FINAL_REFERENCE_AUDIT.md tiers V1/V2). Notable corrections during
  verification: Fan & Mai review is AMR **57**:325–343 (**2004**), not
  AMR 56:549 (2003) as memory suggested; Lubensky–Ramaswamy–Toner
  hydrodynamics paper is PRB **32**:7444 (1985), not PRL.
- Rejected (metadata could not be verified): Socolar 1991 dodecagonal
  elasticity; Abe 2000 PRL; Results-in-Physics 60 (2024) Lamb-wave paper
  (conflicting article numbers 107674/107464); Crystals 14:170 (2024)
  (authors not confirmed); Chadwick & Windle 1964 (not found; replaced by the
  verified Chadwick & Seet 1970 Mathematika thermoelastic-surface-wave paper).
- All 1D hexagonal wave references are labelled 1D at every use; no 1D result
  supports a 2D claim.
- Orphan/undefined/duplicate checks: 0/0/0 (script-verified).

## 3. Figures

- New script `submission/make_figures_publication.py` regenerates 12 PDFs into
  `submission/figures_pub/` from the accepted raw data (read-only):
  identical datasets and plotted quantities to the accepted figures;
  **no embedded titles or caption text** (all captions now live only in the
  tex); serif typography, panel letters (a)/(b)/(a)–(i), compact legends,
  consistent colours (Okabe-Ito) and line weights.
- fig1_schematic.pdf reused unchanged (conceptual drawing, no embedded
  caption).
- The legacy coarse-scan record point (0.934208) in fig2a is **kept** and
  relabelled neutrally ("coarse-scan record, excluded"); the fig6 reference-τ
  flat line and the fig2b frozen 1e-8 evidence curve are kept and explained in
  captions (see FINAL_FIGURE_AUDIT.md items F1–F7).
- Lineage: raw CSV/NPZ (study1_surface_waves/results) → script → figures_pub
  PDF → tex caption; table in FINAL_FIGURE_AUDIT.md §1.

## 4. Suspicious-feature inspection (Part 10)

- Automated scan of every plotted curve (step sizes, NaN census, root counts,
  conditioning, map smoothness) — results and classification of the seven
  flagged features in FINAL_FIGURE_AUDIT.md. No data hidden, smoothed,
  deleted, or cropped; nothing required a fix in the data.

## 5. Language and claim discipline

- Removed the single borderline word ("dramatic" → "change only marginally");
  grep audit for obviously/remarkable/clearly seen/excellent agreement/
  striking/groundbreaking/first-ever: 0 hits.
- Preserved: Ω_c/ω0≈11467.5 reference-line-only treatment; no crossover claim
  in the baseline window; Fig. 9b "reference line only"; 95/121 with the
  91/121 footnote; model-A clamped degeneracy honest handling; k11 6 vs 5.3
  disclosure; surrogate labels; "to the best of our knowledge, within the
  literature surveyed"; no experimental-observability claims; FEM mentioned
  only to state it is out of scope.

## 6. Build

- pdflatex ×2, rc=0, **0 errors, 0 LaTeX warnings**, no overfull boxes ≥10 pt,
  30 pages (within the 26–30 target), all 13 figures embedded, all citations
  resolved.

## 7. Not changed (deliberately)

- All equations, parameter tables, verification gates, sweep results, floor
  conventions, E2 footnote, limitations content (extended, not weakened).
- The accepted reproducibility package ZIP (sha256 unchanged) and the git
  history.
