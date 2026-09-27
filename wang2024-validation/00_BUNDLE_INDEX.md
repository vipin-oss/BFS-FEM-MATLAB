# Bundle index: Plan B and Wang (2024) validation work

This folder collects the work completed so far for the thermal-shock validation audit and Plan B.

## Main documents

- `plan_b_blueprint.md` — proposed validation-first, Q1-targeted research plan, hypotheses, validation protocol, go/no-go gates, and limits.
- `plan_b_execution_log.md` — actions actually run, numerical results, source-input discrepancies, and work still blocked/pending.
- `technical_note_draft.md` — preliminary technical note describing the completed Wang algebra and Shao sphere analytical checks.
- `README.md` — entry point and detailed source/model distinctions.

## Code and reproducible checks

- `single_element_limit.py` — independent Wang (2024) Appendix A algebra/limiting-case check; not a FEM solver validation.
- `shao2014_sphere_threshold.py` — standard-library Shao (2014) sphere-threshold analytical calculation.
- `papsik_input_audit.py` — source-input unit and thermal-scale checks; not an FEM run.
- `papsik_radial_thermal.py` — reduced radial finite-volume thermal baseline for alumina, ZTA, and an article-geometry core-shell case; not fracture simulation or reproduction of ANSYS outputs.
- `make_progress_pdf.py` and `render_pdf_previews.py` — scripts used to generate the progress PDF and its PNG page previews.

## Readable progress outputs

- `PlanB_Progress_Report.pdf` — three-page Hinglish summary.
- `preview/PlanB_Progress_Page1.png`, `Page2.png`, `Page3.png` — readable image previews for environments where PDF preview is unavailable.

## Explicitly not included / not done

- The Zenodo ZIP and its material CSV were not downloaded/verified in this environment; only official record metadata, archive listing, and accessible APDL text files were inspected.
- No ANSYS run, full independent rod fracture FEM, 3D simulation, new experiment, or experimental validation is included.
- No result in this bundle validates Wang (2024)'s PF-CZM/FEM solver.
- The existing `image-search/` folder is outside this bundle because it was pre-existing and is unrelated to this Plan B execution package.
