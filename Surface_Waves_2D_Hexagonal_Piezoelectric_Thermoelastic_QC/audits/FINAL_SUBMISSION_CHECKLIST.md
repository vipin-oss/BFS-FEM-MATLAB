# FINAL_SUBMISSION_CHECKLIST.md — updated for Task 13 (2026-09-07)

## Manuscript package (submission/)

- [x] FINAL_MANUSCRIPT.tex — 30 pp source, 0 errors / 0 LaTeX warnings
- [x] FINAL_MANUSCRIPT.pdf — 30 pages (target 26–30), all figures embedded
- [x] FINAL_MANUSCRIPT.bib — 47 entries (mirrors the tex thebibliography)
- [x] figures/fig1_schematic.pdf — reused (conceptual schematic)
- [x] figures_pub/*.pdf — 12 regenerated publication figures (caption-free)
- [x] make_figures_publication.py — regeneration script (raw data read-only)
- [x] FINAL_REFERENCE_AUDIT.md — 47-entry audit with verification tiers
- [x] FINAL_FIGURE_AUDIT.md — lineage table, automated scan, F1–F7 disposition
- [x] FINAL_MANUSCRIPT_CHANGELOG.md — Task-12 → Task-13 delta record
- [x] FINAL_SUBMISSION_CHECKLIST.md (this file)
- [x] FINAL_PRODUCTION_REPORT.md — 13-section format, verdict

## Content requirements (Task 13 P-items)

- [x] P2 length 26–30 pp (30)
- [x] P3 Introduction subsectioned 1.1–1.5; 15-point progression; each
      paragraph answers "what does it establish + why does it matter"
- [x] P4 47 verified refs (target ≈55 not padded; every entry supports a
      specific statement; audit maintained)
- [x] P5 key references positioned (Shechtman, Levine–Steinhardt, Bak,
      Lubensky–Ramaswamy–Toner, de Boissieu, A&L 2014×2, A&L 2023, Lord–
      Shulman, Chadwick–Seet, 2D-hex statics/fracture/piezoelectric set,
      1D-hex wave cluster); 1D vs 2D hex explicitly distinguished
- [x] P6 novelty wording "To the best of our knowledge, within the literature
      surveyed…" (framework-combination framing, moderate)
- [x] P7/P8 interpretation paragraph around every figure placement
- [x] P9 Discussion physical (mechanisms, not trend reporting); numerical
      trend / mechanism / modelling implication separated
- [x] P10 every curve scanned; 7 flagged features classified (F1–F7); no
      hiding/smoothing/deletion
- [x] P11/P12 figures caption-free, serif, panel letters, traceable lineage
- [x] P13 figure-by-figure content matches ACTUAL plotted quantities; Fig. 9b
      boundary = resolution boundary, not a phase transition
- [x] P14 Results structure: question → figure → observation → interpretation
- [x] P15 A/B/C physical interpretation in §7.2–7.4
- [x] P16 thermal smallness explained (T0β1*, τ0*Ω*, LS structure) in §7.5
- [x] P17 phason BC physics (free vs clamped; A degeneracy) in §7.6
- [x] P18 Ω_c/ω0≈11467.5 preserved; no crossover claim in baseline window;
      material crossover vs sweep/resolution boundary distinguished (§7.4)
- [x] P19 Discussion 7.1–7.9 structure
- [x] P20 limitations list (10 items incl. 2D-hex scope, parameter ranges)
- [x] P21 abstract: problem/method/A-B-C/numbers/interpretation/limitation
- [x] P22 conclusions = result + physical meaning + modelling implication
- [x] P23 citation audit: 0 orphans, 0 undefined, 0 duplicates; count 47
- [x] P24 tables: params+provenance (T1), A/B/C comparison (T2),
      nondimensional groups+ranges (T3)
- [x] P25 language audit clean (grep: 0 forbidden hits)
- [x] P26 figure QC: no embedded captions; consistent typography/weights;
      no unexplained spike (audit F1–F7)
- [x] P27 build 26–30 pp
- [x] P28 all deliverables present
- [x] P29 final report in required format

## Standing constraints re-verified

- [x] No new simulations; science closed; package ZIP sha256 unchanged
- [x] Figures regenerated with identical underlying data; captions only in tex
- [x] Fig. 9b not called a transition; Ω_c reference line only
- [x] 1D vs 2D hexagonal formulations distinguished at every use
- [x] Every new reference web-verified; unverified fields flagged, not guessed
- [x] No experimental-observability claims
- [x] Guyer–Krumhansl content NOT imported (sample paper = style only)

## Remaining author inputs before submission (placeholders in tex)

- [ ] Author names, affiliations, ORCIDs, corresponding-author email
- [ ] Funding statement; conflict-of-interest statement; author contributions
- [ ] Public archive identifier (if/when the reproducibility package is
      deposited); publisher class file applied at portal submission
