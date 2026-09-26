# Package Manifest — Paper 10 Journal & Reproducibility Package

**Manuscript Title:** Dual-Phase-Lag (DPL) Thermoelastic Band-Gap Tuning and Acoustic Dissipation in 1D Periodic Metamaterials with Dipolar Gradient Elasticity
**Governing Commit:** `f92e86462c42d9d4b7dce78309daac9ac53d7cef`
**Date:** 2026-09-26

---

## 1. Package Summary Statistics

- **Total Files in Package:** 74 (excluding symlinks)
- **Manuscript Pages:** 19 pages (`Paper10_Manuscript.pdf`)
- **Numbered Equations:** 37 equations
- **Embedded Figures:** 10 publication figures (300 DPI)
- **Summary Tables:** 3 formatted tables
- **Bibliography Entries:** 25 entries (29 in-text citations)
- **Production Datasets:** 18 files (7 sweep families CSV/JSON + summaries)
- **Validation Datasets:** 3 files
- **Source Code Files:** 14 files
- **Audit & Verification Records:** 6 files

---

## 2. Complete File Inventory & SHA-256 Checksums

| Relative Path | Size (Bytes) | SHA-256 Checksum | Purpose & Category |
| :--- | :---: | :--- | :--- |
| `00_README/PACKAGE_MANIFEST.md` | 4,178 | `53de5cc3323c626bc1006468049aaab2b2e67afebc37c5ccd99ef87648986787` | Documentation / Overview |
| `00_README/README.md` | 3,926 | `a6484aaf3ea9882c9d17bd7a8bcd9890d450754381158578519a20f7933c4871` | Documentation / Overview |
| `00_README/VERSION_AND_PROVENANCE.md` | 2,986 | `371a261ad274e07d4f2972bee498969dcaa208c67a56adf723fb1c65a2e5d311` | Documentation / Overview |
| `01_MANUSCRIPT/Paper10_Manuscript.pdf` | 3,414,879 | `0ab701ec5d95ab853b67957b87cc6a35c3df3596dd57602058ad6a0724888848` | Manuscript Deliverable |
| `01_MANUSCRIPT/Paper10_Manuscript.tex` | 54,531 | `f05a250082b30a004101ca13e2d169af09d80bd0022c0a54b8af32f43214ab2f` | Manuscript Deliverable |
| `01_MANUSCRIPT/compile_manuscript.sh` | 1,003 | `a4087e1f1f8c64ec46dc3f8407d608f5c6037e7d7850b3a04721c54b28ccb022` | Manuscript Deliverable |
| `01_MANUSCRIPT/references.bib` | 8,518 | `282dac52edb2ba18a6f4592ef7fc491d9b063da831fc57a67cee42ebd6789d3c` | Manuscript Deliverable |
| `02_FIGURES/FIGURE_MANIFEST.md` | 3,244 | `e5df3c0a3b641c2cce32d6f09596e731fa9de2733c94b36d9fe6ad1287ff50d6` | Publication Figures (300 DPI) |
| `02_FIGURES/fig10_synthesis_map.png` | 269,998 | `33d5396c46255913aea259465544f32ad729761e14c79c3a7212802a6b0b01db` | Publication Figures (300 DPI) |
| `02_FIGURES/fig1_baseline_dispersion.png` | 214,687 | `d2f1bf67669434983091e84ccfa8da629317862c4eabbea7a7fb692dfaa70dc2` | Publication Figures (300 DPI) |
| `02_FIGURES/fig2_baseline_attenuation.png` | 309,026 | `006754638291d22b89e6de36e8b43be52277c607adbe44b34dcb97327d7acd2f` | Publication Figures (300 DPI) |
| `02_FIGURES/fig3_material_contrast.png` | 228,983 | `a406eb2345ce487e2f31f49b6d1357c99d11e4e792abc1db2c2db19de211a293` | Publication Figures (300 DPI) |
| `02_FIGURES/fig4_gradient_lengths.png` | 329,671 | `33f169c7f57d4a13b804bcb5792642dfc2bef4aba7527047a2c6c6f8ef15ff52` | Publication Figures (300 DPI) |
| `02_FIGURES/fig5_filling_fraction.png` | 228,570 | `befd41ee416b3560256c68ba5dfa74d931419f7ce770fe7401127d84236959e7` | Publication Figures (300 DPI) |
| `02_FIGURES/fig6_dpl_lags.png` | 540,896 | `fb846c28340a78cc023e5125150751c30e1d7ca6c25d431d3e4b88660c85257e` | Publication Figures (300 DPI) |
| `02_FIGURES/fig7_thermoelastic_coupling.png` | 510,091 | `1c0b5cfeeca36bdc618bba6a892e4961144bf18785b37cfebef03909ab3c8e8d` | Publication Figures (300 DPI) |
| `02_FIGURES/fig8_combined_interaction.png` | 452,622 | `e3f3d31624a6ba7b42a0db307ec7df6fc8f817b2c23790d6730064ac793958b3` | Publication Figures (300 DPI) |
| `02_FIGURES/fig9_bandgap_summary.png` | 323,210 | `6407cfc32557e5a9d16c4550610530b906ac5fba3a216c6615e7b95897b67a4a` | Publication Figures (300 DPI) |
| `03_SOURCE_CODE/CODE_README.md` | 4,409 | `d7d8150216ad0cbea9c91dda47432eeb8fe466eeb1cb9679a88683c09f42abd6` | Computational Source Code |
| `03_SOURCE_CODE/analytical/PHASE1_DERIVATION.md` | 23,579 | `e7026078bc20a99623fad1c4a9302e936cc430092aacff4d85cdb299ceb7c6f9` | Computational Source Code |
| `03_SOURCE_CODE/analytical/PHASE1_SYMBOL_TABLE.md` | 5,267 | `9c62d79912618a417debed876f07ac9f21741c9128fc7c88473970d9c4b1a16e` | Computational Source Code |
| `03_SOURCE_CODE/production/regenerate_calibrated_figures.py` | 12,240 | `fde67850e8bf02c7f314eb1647e70335b29235c6e607721d2cdad968b09a718a` | Computational Source Code |
| `03_SOURCE_CODE/production/run_phase3b_production.py` | 49,363 | `79e73b70d67001edea9a0358b4edb39e3787632a7712795bd541c74ba7e6a0be` | Computational Source Code |
| `03_SOURCE_CODE/production/run_pilot_sweep.py` | 16,052 | `9446d1dc809ff2d26f637e7a4528529baf68cd060092a876b6ee619758dc7cd4` | Computational Source Code |
| `03_SOURCE_CODE/transfer_matrix/antiplane.py` | 15,556 | `00d62154d75cbc451f9532ffcb55e5e2483ae00fb816f527e5c1a869602e8ad6` | Computational Source Code |
| `03_SOURCE_CODE/transfer_matrix/coupled10.py` | 11,422 | `f08c25c1eea846145ba00e37b129ce718f7b7843fe4e98a660b0cc4db47062b2` | Computational Source Code |
| `03_SOURCE_CODE/transfer_matrix/parameters.py` | 5,274 | `089c01c6cddde8e01fb303f3b453e29a60390e6dc987a5e4458e4664b109e0f2` | Computational Source Code |
| `03_SOURCE_CODE/utilities/test_antiplane.py` | 3,370 | `20b13d9e49bd55927d29eb985731f456d533b24b450385ac324b2e96fe16a0a2` | Computational Source Code |
| `03_SOURCE_CODE/utilities/test_coupled10.py` | 4,708 | `5c50e2caac19fb99e6c20fa917b7de94c2e8ebe62a07bbd02d5b866df3ea1168` | Computational Source Code |
| `03_SOURCE_CODE/utilities/test_parameters.py` | 1,233 | `07b65f3ac1307addecabf290a17d3f8ca643ff57ea2c6b3f427c4badaa51700e` | Computational Source Code |
| `03_SOURCE_CODE/validation/run_benchmarks.py` | 11,047 | `362cd0f06c67516fcecfa4eed84cb39df1c002dafe7bff5ac69ab1f8341eb645` | Computational Source Code |
| `03_SOURCE_CODE/validation/run_periodic_pilot.py` | 5,525 | `45244e8661f9e40399c7b5d258a685168ab9bbe8f26f1b721e7255ca20150d85` | Computational Source Code |
| `03_SOURCE_CODE/validation/validate_benchmark_acta.py` | 6,226 | `c33d03ddfe034a7fa2f527540530a52f7bf8b961e8c75ad2524c044af69e71f6` | Computational Source Code |
| `04_PRODUCTION_DATA/DATA_DICTIONARY.md` | 7,122 | `e485dd0b726e7592a74f8b6f92b4ebc8dbf7c14bd52647e8c791cde4824d71d2` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/PHASE3_PARAMETER_MATRIX.json` | 1,926 | `d83e2b41eca72c9a8a04afee54eaf8fa8092ca93421c857e94ba1f169f93a452` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/PRODUCTION_ATTENUATION_SUMMARY.csv` | 5,105 | `4c459011b18242898ba88a153e018b3854cddc7a09851aa5073b197817758d4c` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/PRODUCTION_BANDGAP_SUMMARY.csv` | 6,215 | `c158dc110d289029e5a2a6ac214797ddcd415edbf1663e965960e0fcc5d0c8b4` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/PRODUCTION_METRIC_MANIFEST.json` | 10,371 | `37d152aef96f4dd9b52cfc27fddaa0429b4d91a8644a77ad8ea67a2601016cd9` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/S1_results.csv` | 271,355 | `b06e59badff2f54978d5881c3aa2a73d683d8f73d10fe3d2bf9bdcc20f3110fe` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/S1_results.json` | 86 | `a7739aa42f7b4ac4bcbf7cdf4cc3ebefdd1f54cccc9e611cb96ed931d92e27da` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/S2_results.csv` | 826,991 | `c7cee8f86846e5e63f79131b7d1287869e6cc553300a397d3cfe28a5051f3c83` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/S2_results.json` | 180 | `f4542959c5b0f9cf5101588431975d1b219abb936045a0b7598e6a34073ab58f` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/S3_results.csv` | 876,940 | `a6b83a081e1ecaa4f4e723f971475c6cf7f41edbbe5244656f029f2cba21961d` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/S3_results.json` | 161 | `6e740c596e0f0b099e8a8ae9b257e9401211e91d396c7fe48d090eee3117080b` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/S4_results.csv` | 826,828 | `87e7e5ef70ebc84271419870e718fa9c8bf097bcd56154ece5e72c2738fccd3d` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/S4_results.json` | 180 | `e081ac5fce7ce1b954265db10dc3497c7dbc799524779da5a41ca62213c64ace` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/S5_results.csv` | 692,074 | `e6edda34309a6ee58a83968598921dd9f22aa5064e9cc5ba2374dd3dc4144f10` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/S5_results.json` | 158 | `cb84875f456b9320bdf535b25331875530ac7a9ef8f79228277d7d39c1cda0c9` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/S6_results.csv` | 561,438 | `dc01400c9db6a15dfb4bceb9ea7167812882916ef9bf13bd381c33f8c162c039` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/S6_results.json` | 129 | `bfb5c943fdb5e2ae20e35fb7c664be573a16c8604dbc832e815d72065873f484` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/S7_results.csv` | 891,133 | `bf1819cdd2c30fa20c272ca90915c4033af8f0b48d9a0f0d717e74ab5e270623` | Frozen Production Dataset |
| `04_PRODUCTION_DATA/S7_results.json` | 153 | `895e822812c98a72a400352e8c45048cbe8442cbf5e588773ccb94451401ae13` | Frozen Production Dataset |
| `05_VALIDATION/PHASE2_BENCHMARK.md` | 6,548 | `26f995e02e7c08b2cfcdd5e13a01ab931a678c724aeafd5622e96009e5067bd7` | Independent Validation |
| `05_VALIDATION/PHASE2_REPRODUCIBILITY.md` | 2,941 | `46d0350de067d0f782fafe95b7ce928167ce3b61912db5fef534433900b494e8` | Independent Validation |
| `05_VALIDATION/PHASE2_TARGETED_VALIDATION_AUDIT.md` | 4,136 | `c07842a8b1b9559fd542d1eefb1df1428c007af2ef51415f86aa247ae9fd019c` | Independent Validation |
| `05_VALIDATION/VALIDATION_README.md` | 5,641 | `1379cc5c58f95c8de9611a70d4a612ad5940ae49df72d5c52b4cf37e5909c476` | Independent Validation |
| `05_VALIDATION/benchmark_papargyri_beskou_results.csv` | 8,635 | `2cf696e904d36d9ae80804a5c83830bf1ae59d60f1c7d002390ec513cc16eba7` | Independent Validation |
| `05_VALIDATION/benchmark_papargyri_beskou_results.json` | 21,934 | `988eb8e2a7bc55dc5e076fc0b9829ee703e5b2baced787fe387584ef0281da3d` | Independent Validation |
| `05_VALIDATION/periodic_pilot_results.json` | 435 | `2ac6aa2bca16f4a571ac122e6f45fbe331fd7dadf83bab81b8a7929a7ad0ee17` | Independent Validation |
| `05_VALIDATION/run_benchmarks.py` | 11,047 | `362cd0f06c67516fcecfa4eed84cb39df1c002dafe7bff5ac69ab1f8341eb645` | Independent Validation |
| `05_VALIDATION/run_periodic_pilot.py` | 5,525 | `45244e8661f9e40399c7b5d258a685168ab9bbe8f26f1b721e7255ca20150d85` | Independent Validation |
| `06_AUDIT_RECORD/FINAL_CORRECTION_VERIFICATION.md` | 6,867 | `b7c467b84d584e24de08d1f8002eb4a4572f033f348edcf08c4346fd4dd12cbf` | Scientific & Quality Audit |
| `06_AUDIT_RECORD/FINAL_PRE_SUBMISSION_AUDIT.csv` | 3,256 | `045f0d5212459db8f70000a4130ed44e2aa9a58e9268567236d30d8546cca8c3` | Scientific & Quality Audit |
| `06_AUDIT_RECORD/FINAL_PRE_SUBMISSION_AUDIT.md` | 29,459 | `b6695ec0b4c41d017cfd09aceacf38e408040e101384c333e43be18a2eaaa215` | Scientific & Quality Audit |
| `06_AUDIT_RECORD/PHASE4_MANUSCRIPT_AUDIT.md` | 7,680 | `752dd41c88bfe1a82c2f27227c0c51e93c126c81a3694b64f9f1cc96e2f377af` | Scientific & Quality Audit |
| `06_AUDIT_RECORD/PHASE4_MANUSCRIPT_SOURCE_AUDIT.md` | 11,827 | `0eabaa1887d779b3564020a334a2cb3ded2986bb27ba96e02babbbba29f109d2` | Scientific & Quality Audit |
| `06_AUDIT_RECORD/PHASE4_TRACEABILITY_MATRIX.md` | 7,134 | `114e4fd64b03d859f1a14f456759aac6282f022ac710535fc587c0070874aeef` | Scientific & Quality Audit |
| `07_REPRODUCIBILITY/ENVIRONMENT_INFO.txt` | 218 | `fa60679b8bce74490585baefb0bf63f43fbf6f9434c17f265e9c84e1b4b4921c` | Reproducibility Guide |
| `07_REPRODUCIBILITY/REPRODUCIBILITY_GUIDE.md` | 6,143 | `84dccabfbefd924a3e532fbb0c1447cc1c0858368caecf0de88c50c715f916a1` | Reproducibility Guide |
| `07_REPRODUCIBILITY/RUN_ORDER.md` | 939 | `7d24bc1fc779fea6b814522a9df5fbb47ad6fcf7e3365b4ce56960759bad1b66` | Reproducibility Guide |
| `08_GIT_PROVENANCE/FILE_INVENTORY.txt` | 10,599 | `b6602f742ed16b8686efdb08082085b59225bf8f6937f7ded66985d6092cdf08` | Git Milestone Tracking |
| `08_GIT_PROVENANCE/GIT_COMMIT.txt` | 41 | `22a11fc1bb43c0e148d55cbfe260392273a0b9149ab5ac15f6f7d00dd8ed3034` | Git Milestone Tracking |
| `08_GIT_PROVENANCE/GIT_LOG.txt` | 1,273 | `38fd5fe9e348494bc5d3c7096537ec2639498aa392c75f226edc10faeb86e152` | Git Milestone Tracking |
| `08_GIT_PROVENANCE/GIT_STATUS.txt` | 224 | `12399ad58b63511e39a2aeb8bfd3cc482c1510e1db069bac6c1901dc1bb65554` | Git Milestone Tracking |

---

## Phase-0 Addendum (2026-09-26)

The SHA-256 table above is the frozen v1.0 record and remains valid for all files unchanged since freezing. The following files were ADDED or MODIFIED by the Phase-0 scientific-depth expansion:

| Relative Path | Change | Purpose |
| :--- | :--- | :--- |
| `01_MANUSCRIPT/references.bib` | Modified (25 -> 47 entries; key `li2023thermoelastic` -> `li2026thermoelastic`) | Literature-depth expansion, all entries verified |
| `01_MANUSCRIPT/Paper10_Manuscript.tex` | Modified (additions only) | 3 new figures, renumbering, citation weaving in Results/Discussion/Conclusions |
| `01_MANUSCRIPT/Paper10_Manuscript.pdf` | Recompiled from updated source | Deliverable |
| `02_FIGURES/fig_unit_cell_schematic.png` | Added | Fig. 1 (schematic) |
| `02_FIGURES/fig_pb_benchmark_overlay.png` | Added | Fig. 2 (validation overlay) |
| `02_FIGURES/fig_chi_eta_heatmap.png` | Added | Fig. 12 (supplementary 2-D gap map) |
| `02_FIGURES/FIGURE_MANIFEST.md` | Updated | 13-figure manifest with renumbering note |
| `04_PRODUCTION_DATA/SUPP_CHI_ETA_GAP_SUMMARY.csv` | Added | 115 gap records over 11x11 (chi, eta) grid |
| `04_PRODUCTION_DATA/SUPP_CHI_ETA_CASE_METRICS.csv` | Added | 121 per-case metrics |
| `04_PRODUCTION_DATA/SUPP_CHI_ETA_GRID_META.json` | Added | Grid-run metadata (anchors PASSED) |
| `04_PRODUCTION_DATA/DATA_DICTIONARY.md` | Updated (Sec. 4) | Supplementary dataset documentation |
| `03_SOURCE_CODE/production/run_chi_eta_grid.py` | Added | Supplementary grid runner (frozen solver, verbatim) |
| `03_SOURCE_CODE/production/make_phase0_figures.py` | Added | Phase-0 figure generation script |
| `00_README/README.md`, `00_README/PACKAGE_MANIFEST.md` | Updated | This addendum |
