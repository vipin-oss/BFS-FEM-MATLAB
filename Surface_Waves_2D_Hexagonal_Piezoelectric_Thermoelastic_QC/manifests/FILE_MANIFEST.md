# FILE_MANIFEST.md — Surface_Waves_2D_Hexagonal_Piezoelectric_Thermoelastic_QC (GitHub archival)

Shipped files: 141 (incl. this file and CHECKSUMS.sha256). Verify:
`sha256sum -c manifests/CHECKSUMS.sha256` from this directory.
Differences vs the FINAL_QC_SURFACE_WAVES_RESEARCH_ARCHIVE ZIP
(126 files): +11 EPS figures, +.gitignore, +GitHub README additions,
+MISSING_REFERENCE_PAPERS.md, +NOVELTY_MAP.md, +REVIEWER_RISK_AUDIT.md,
+CLEAN_ROOM_REPRODUCTION_REPORT.md, archive/ ZIPs replaced by README
(LFS/duplication policy — SHAs recorded), 4 historical audits renamed to
their FINAL_* names.

## Root (12)
README.md (GitHub guide, 18 sections) · PROJECT_STATUS.md · REPRODUCE.md ·
CHANGELOG.md · requirements.txt · environment.yml · run_all.py ·
params.json · grids.json · REPRODUCTION_REPORT.md (generated) ·
run_all.sh.orig (upstream blueprint, provenance) · .gitignore

## manuscript/ (3 + 11 + 1)
FINAL_MANUSCRIPT.tex / .bib / .pdf (29 pp, 0 err/warn/undefined) ·
figures/ (11 journal-source PDF copies, auto-synced) ·
supplementary/README.md

## figures/ (2 + 2 + 22 + 1)
style.py · make_all_figures.py · scripts/{make_figures_original_package.py,
README.md} · source/README.md · output/ (fig1–fig11.pdf authoritative +
Fig01–Fig11.eps companions)

## solver/ (10) · drivers/ (5) · tests/ (6, one per V0…V5)
As in the accepted package (unmodified science).

## results/ (16 + 2 + 6 + 1)
raw/ (13 CSV + 2 NPZ + MANIFEST.md + chain_log.txt, read-only) ·
manifests/{RAW_DATA_MANIFEST.md, RAW_DATA_CHECKSUMS.sha256} ·
validation/ (V0–V5 logs) · processed/README.md (empty by design)

## verification/ (2 + 5)
verify_invariants.py · reports/INVARIANT_CHECK.md ·
{branch_identity, symbolic, model_limits, two_path}/README.md

## audits/ (13)
SCIENTIFIC_SUFFICIENCY · FINAL_MANUSCRIPT · FINAL_PRODUCTION_REPORT ·
FIGURE_REDESIGN · FIGURE_DATA_TRACEABILITY · SPIKE_AND_ANOMALY ·
FINAL_REFERENCE_AUDIT · FINAL_FIGURE_AUDIT · FINAL_SUBMISSION_CHECKLIST ·
FINAL_TASK14_PRODUCTION_REPORT · NOVELTY_MAP · REVIEWER_RISK_AUDIT ·
CLEAN_ROOM_REPRODUCTION_REPORT

## literature/ (3 + 7 + 2)
README.md · all_references.bib (47) · MISSING_REFERENCE_PAPERS.md ·
7 category REFERENCES.md · sample_papers/{GK_Heat_style_reference.pdf,
README.md}

## provenance/ (4) · manifests/ (4)
PARAMETER/REFERENCE/DATA/FIGURE provenance · FILE_MANIFEST ·
FIGURE_MANIFEST · LITERATURE_MANIFEST · CHECKSUMS.sha256

## archive/ (1)
README.md — the three historical ZIPs are excluded from git (repo *.zip
LFS policy; byte duplicates of this tree); SHA-256s recorded therein.
