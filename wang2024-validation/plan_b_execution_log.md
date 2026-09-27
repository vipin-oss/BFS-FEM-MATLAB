# Plan B execution log

**Execution state:** started. Source/parameter reconnaissance, existing-check reruns, and an independent reduced radial thermal calculation are complete. The full Plan B is **not** complete: no independent rod fracture FEM, no new laboratory tests, and no experimental validation have been performed.

## Actions actually executed

### WP1 — source and parameter audit (partial; gate G1 not passed)

- Confirmed from the official Zenodo API metadata that record `10.5281/zenodo.13970234` is public and marked CC BY 4.0. The manifest reports one 2,528,002-byte ZIP (listed MD5 `f32bf0929f08dcef912e102e468a958d`) with 34 members, including a 586-byte material CSV, 13 APDL input files, figure descriptions, and figures/photos.
- Read the archive README, figure descriptions, and the accessible APDL setup, material, geometry, thermal, mesh, stress, crack-loop, energy, and export inputs through the official archive-container API. The ZIP itself was not downloaded, so the record's MD5 has **not** been independently verified.
- The README calls the data file `Material_data.xlsx`, but the archive manifest lists `Data/Material_data.csv`. The CSV preview endpoint returned HTTP 500 on repeated official-endpoint attempts; its contents remain unread. No author contact or access-control workaround was attempted.
- The APDL thermal input uses 50,000 W m⁻² K⁻¹ on the lateral surface; the end-face convection commands are commented out. It uses a 100 ms thermal run with adaptive steps from 1 μs to 1 ms.
- Source-configuration issues requiring resolution before a reproduction:
  1. The geometry input defaults the rod height to **5 mm** when no `rod_height` parameter is supplied; the article describes 50 mm long specimens. The top-level input/readme does not document a complete parameter-initialization command.
  2. The geometry input sets `layer_thickness=0 μm`; a core–shell calculation therefore requires an undocumented override or source edit.
  3. The material files activate the 20 °C property row; the shown 320/620 °C E and thermal-expansion entries are commented out.
  4. The ZTA APDL file assigns `902 MPa`, `m=13.6`; the article Table 1 reports ZTA biaxial characteristic strength `1025 MPa`, `m=5.3`, and also gives a distinct tensile-strength estimate. The conversion/provenance is unresolved.
- These are not automatically proof of errors in the published calculations: some may rely on an undocumented interactive setup or parameter convention. They do mean the archived inputs are not yet a unique, traceable reproduction recipe.

### WP2 — independent thermal/arithmetic checks (partial)

Added `papsik_input_audit.py`, a standard-library audit of unit conversions and thermal scales from the APDL input values. It does **not** solve the heat equation or fracture problem. Verified outputs include:

| APDL material | Thermal diffusivity (m²/s) | Radial Biot number, R=2.5 mm | R²/α (s) | Fo at 100 ms | `G_c` from APDL `K_Ic` (J/m²) |
|---|---:|---:|---:|---:|---:|
| Alumina | 1.020237×10⁻⁵ | 3.6765 | 0.6126 | 0.1632 | 25.403 |
| ZTA | 7.613972×10⁻⁶ | 5.6818 | 0.8209 | 0.1218 | 46.181 |

The derived ZTA `G_c` agrees with the APDL value to rounding. These checks do not establish FEM convergence or validate the thermal/fracture implementation.

Added and ran `papsik_radial_thermal.py`, a standard-library, homogeneous-cylinder radial finite-volume baseline using the APDL thermal constants and its 100 °C default shock. It is explicitly a reduced thermal component—not the paper's finite-length axisymmetric ANSYS model and not a fracture simulation. It separately varied radial mesh (50/100/200 cells at fixed time step) and time step (1/0.5/0.25 ms at fixed mesh); each refinement changed the 100 ms center/surface temperatures by less than 0.15 °C. The discrete energy-balance residual remained below 7.4×10⁻¹⁴, and the adiabatic (`h=0`) uniform-temperature limit passed. At the finest grid, the calculated temperatures were 99.685 °C center / 45.068 °C surface for alumina and 106.703 °C / 40.180 °C for ZTA. I then added the article-reported ZTA-core / 0.4 mm alumina-shell thermal case (the supplied geometry input itself resets shell thickness to zero); the 200-cell / 0.25 ms result was 105.458 °C center / 41.794 °C surface, with energy residual below 6×10⁻¹⁴. This layered case uses the published article geometry as an explicit input and is not a reproduction of the archived APDL run. These are predictions of the reduced thermal model only, not reproduction values from the article.

Environment probe found no `ansys`, `matlab`, or `octave` executable and no installed NumPy/SciPy/FEniCS/scikit-fem packages. The reduced thermal model uses the standard library. A full independent axisymmetric fracture FEM remains **deferred** until the geometry/material inputs are resolved; it should not be built against guessed parameters.

### WP3 — rerun of existing historical checks

- `python wang2024-validation/shao2014_sphere_threshold.py` ran successfully. Its built-in 80/120-mode convergence and property-range assertions passed. Output reproduces the existing values: 219.27 K, 548.32 K, and 1290.95 K for radii 2.10, 0.35, and 0.11 mm with the 20–600 °C property row. The output remains a qualified comparison with prose/figure threshold bands, not exact experimental validation.
- `python wang2024-validation/single_element_limit.py` ran successfully. It reproduced the Appendix A onset algebra and the Eq. (A7) traction-free-face inconsistency already recorded in `README.md`. This remains a single-element analytical check, not a numerical solver test.
- Public Papšík images have not been re-scored, and no outcomes have been reclassified from figure images.

## Mandatory work still outstanding

| Blueprint item | Status | Reason / required next action |
|---|---|---|
| Read/checksum the full Zenodo archive and inspect the material CSV | **Blocked** | Official archive file-preview/download was unavailable in this environment; the CSV endpoint returned HTTP 500. A direct authorized public download is needed to verify it and the listed checksum. |
| Resolve Papšík material/geometry configuration | **Blocked** | Need the CSV and a documented input setup that recovers the 50 mm height, core–shell layer thickness, and strength/Weibull definitions. Do not infer them. |
| Independent axisymmetric thermal/fracture FEM and convergence | **Not started** | No numerical solver dependencies are installed; more importantly, G1 inputs are not locked. |
| Predictive comparison against public rod images | **Not started** | Do not score after-the-fact images as blind validation; image data are sparse and no unique reproduced parameter set is yet established. |
| Prospective, blinded validation experiment | **Not performed** | Requires physical specimens, independent material/thermal measurements, instrumentation, and a lab campaign. It cannot be completed by code changes in this repository. |
| Q1-level predictive claim | **Not authorized by current evidence** | Public Papšík data alone do not validate the composite predictions; the mandatory prospective experiment remains outstanding. |

## Guardrails maintained

- No post-shock fitting, author data request, or use of unverified Wang inputs.
- No 3D simulation was run.
- No result here validates Wang (2024)'s PF-CZM/FEM solver.
- No experimental, statistical, or Q1 acceptance claim is made.
