# Plan B blueprint: a parameter-locked validation study of thermal-shock crack initiation

**Status:** research blueprint only. No new solver run, laboratory test, or validation claim is made here.  
**Q1 aim:** target a strong SCI Q1 fracture/ceramics journal if the mandatory validation gates below are met; publication tier and acceptance are not guaranteed.

## 1. Recommended research direction

### Working title

**Can thermal-shock crack-initiation criteria transfer across geometry and architecture without calibration? A historical sphere benchmark and prospective blind rod test**

### Core question

Given thermal, elastic, strength, and toughness inputs fixed independently of the observed cracks, how well do (i) a thermoelastic maximum-stress/size-effect baseline and (ii) a finite-fracture-mechanics coupled stress–energy criterion predict crack onset across two substantially different thermal-shock configurations: quenched alumina spheres and monolithic/core–shell ceramic rods?

The paper's contribution would be a **falsifiable, parameter-locked transferability test**, including an independently measured thermal boundary condition and a prospective hold-out experiment. It is not a claim that a new fracture law has already been developed or that an existing solver has been validated. The core scientific issue is whether thresholds and architecture rankings survive changes of geometry, material, and length scale when the model is denied crack-outcome tuning.

## 2. Why this is the best fit to the work already completed

This direction keeps the completed work useful without overstating it:

1. **Shao et al. (2014) sphere benchmark:** the existing `shao2014_sphere_threshold.py` is a reproducible analytical baseline and a useful cross-scale reference. Its current results and property-row sensitivity can be reused as the frozen historical benchmark, not re-labelled as validation of a rod FEM or of Wang's code.
2. **Papšík et al. (2024) rod study:** its open Zenodo archive supplies measured-material information, figures/photos of tested rods, and the authors' ANSYS APDL inputs for the finite-fracture-mechanics calculations. This is the most promising public bridge to a new independent rod analysis.
3. **Wang et al. (2024) audit:** the one-element Appendix A check and the Shao sphere comparison remain source-audit/analytical work. They motivate disciplined input provenance and define what the new study must test; they do **not** validate Wang's FEM/PF-CZM solver and are not to be presented as such.

The Plan B model will be the **stress–energy/finite-fracture-mechanics criterion**, not the unavailable Wang (2024) PF-CZM implementation. Wang (2020) AT2, Wang (2024) PF-CZM, Shao's sphere equations, and Papšík's criterion must remain separately identified throughout the paper.

## 3. Public evidence and its limits (audited so far)

### 3.1 Shao sphere-quench benchmark

Shao et al. report quenching of 99.5% alumina spheres with radii 0.11, 0.35, 0.56, 1.0, and 2.1 mm, six specimens per size group, and text/figure-described crack thresholds. The existing independent implementation predicts (using the 20–600 °C property row) critical drops of 219.3 K, 548.3 K, and 1291.0 K for radii 2.10, 0.35, and 0.11 mm. The paper's qualitative observations are approximately 240 K, above 620 K, and no cracks at 1280 K, respectively. The 20–400 and 20–600 °C property rows bracket those coarse limits, while broader property ranges move the predictions substantially.

**Use in Plan B:** a fixed historical size-effect check, with the already-documented property sensitivity. The reported experimental limits are not specimen-level machine-readable data, so this source alone cannot support a precision statistical validation.

### 3.2 Papšík et al. (2024) rod benchmark and archive

The article concerns 5 mm diameter, 50 mm long alumina and ZTA monoliths and core–shell rods with a 400 μm alumina surface layer. Public crack observations are for 3D-printed ZTA rods at initial temperature differences of 250 °C and 400 °C. The article reports that at 250 °C one of three specimens cracked and two did not; its calculated monolithic-ZTA threshold is about 280 °C. The paper's other rod/architecture results are numerical predictions, not experimental validations of those architectures.

The Zenodo record is open under **CC BY 4.0** and its archive API manifest lists 34 entries: one material CSV, 13 ANSYS input files, figure-description/readme text, and image assets including the no-shock/250 °C/400 °C rod images. The relevant APDL inputs were inspected through the archive API. The thermal input specifies a 50,000 W m⁻² K⁻¹ convection coefficient on the lateral surface and leaves the rod bases unexposed; the material inputs specify measured/assigned properties and a 1470 °C stress-free reference temperature. The archive is useful for reconstruction, but it does **not** provide a rich set of per-specimen crack measurements, raw temperature histories, or experimental crack data for the multilayer designs.

**Important data-quality gates before any reproduction claim:**

- The archive readme says `Material_data.xlsx`, whereas the archive manifest lists `Data/Material_data.csv`; the CSV is listed but its contents were not retrievable through the current file-preview route. The article tables and APDL input files therefore remain the presently inspected parameter sources; verify the CSV directly when preparing the study.
- The ZTA APDL file assigns a characteristic strength of 902 MPa and Weibull modulus 13.6. The article's Table 1 reports a ZTA biaxial characteristic strength of 1025 MPa and Weibull modulus 5.3 (with a separately reported tensile-strength estimate). This may reflect a conversion or a different parameter definition, but the source material inspected so far does not resolve it. **Do not silently choose one.** Reconcile the quantity, size/area correction, and provenance before freezing the model inputs. If the discrepancy cannot be resolved from public documentation, report both as preregistered sensitivity cases and downgrade any claim that depends on the choice.
- The archive's supplied scripts are ANSYS Mechanical Classic APDL. Their availability does not mean they have been executed or that the figures have been reproduced. Do not use a commercial license without authorization; an independent implementation is an acceptable alternative.

**Consequence:** this public rod dataset is a valuable historical reproduction/consistency check, but it is too sparse to serve as the sole confirmatory validation for a Q1-targeted predictive paper. In particular, the composite-architecture predictions are not experimentally validated by the public photos.

### 3.3 Wang (2024)

The existing Wang audit identifies the Appendix A Eq. (A7) inconsistency and missing inputs/source needed for a solver reproduction. Those findings remain unchanged. The audit is not evidence for or against the full 3D solver and is not the Plan B validation set.

## 4. Preregistered claims and hypotheses

The final claims must be limited to what the tests actually support. Before viewing new crack outcomes, state these hypotheses and publish/freeze the prediction files:

- **H1 — sphere size effect:** for fixed material/boundary inputs, the predicted critical quench drop rises as sphere radius falls over the tested range; uncertainty intervals should account for the independently reported property ranges.
- **H2 — rod onset:** the stress–energy criterion predicts the crack-onset interval for the ZTA monolith without tuning to the published 250/400 °C photos. The historical result is a sparse consistency check, not a blind test.
- **H3 — architecture effect:** the predicted threshold ranking between the alumina monolith, ZTA monolith, and alumina-shell/ZTA-core rod is preserved under measured-property and thermal-boundary uncertainty. This is a **prospective prediction** until corresponding experiments are performed; the 2024 paper's simulations cannot count as experimental validation.
- **H4 — criterion comparison:** on prospective held-out tests, the coupled stress–energy model improves preregistered onset prediction over a maximum-stress-only baseline. If it does not, that is a reportable negative result, not a reason to tune the coupled criterion.

## 5. Study design and methods

### WP1 — public-source and input lock

Create a provenance ledger with one row per input: value, units, source table/file/equation, uncertainty, and whether measured, inferred, or assumed. Retrieve and checksum the public archive; inspect the material CSV and every APDL file used in the analysis. Resolve the 902 MPa/13.6 versus Table 1 discrepancy before the primary model run.

For the historical Papšík reproduction, start with the authors' stated thermal boundary condition (50 kW m⁻² K⁻¹ on the curved/lateral surface, bases insulated) and dimensions. Do not adjust the coefficient against crack images. Run a clearly labelled two-case parameter sensitivity if an input discrepancy remains unresolved; do not call either case a reproduction of the unique published baseline.

For Shao, reuse the existing implementation and preserve all five property rows. Do not use the Wang 2024 property set as a substitute for Shao's measured alumina data.

### WP2 — independent solver and verification

Implement or independently reconstruct an axisymmetric transient heat-transfer/thermoelastic model for the rod and the finite-fracture stress–energy evaluation. Keep the sphere solution separate. A MATLAB implementation is compatible with this repository; a different open implementation is acceptable if its dependencies and version are pinned.

Required verification before comparison with experiments:

- recover the appropriate uniform-temperature/no-stress and one-dimensional limits;
- test stress sign, energy-release sign, units, axisymmetric boundary conditions, and the stress-free reference-temperature implementation;
- demonstrate mesh, crack-depth-increment, time-step, and time-window convergence on prespecified outputs;
- compare an independent calculation of the thermal field/stress in at least one no-crack case;
- archive code, input tables, and machine-readable predictions with a checksum before new test outcomes are opened.

Reproducing a published APDL input is useful for source verification but is not independent validation. The independent implementation should be compared with the APDL outputs only if a licensed solver is lawfully available; otherwise document that part as not run.

### WP3 — historical-data checks

1. Re-run the existing Shao threshold code from a clean environment and include the existing output table and sensitivity analysis. Preserve its classification as an analytical benchmark with coarse experimental threshold bands.
2. Re-score the Papšík 250/400 °C rod images using a written image-scoring protocol (crack present/absent; circumferential vs other visible cracking; ambiguous image category). Keep the original specimen count and image limitations visible. Do not infer unreported quantitative crack depth or crack spacing from a photograph.
3. Predict the ZTA rod result before image scoring. Report its agreement or disagreement; no parameter change is permitted after comparison.
4. Do not use Papšík's own numerical composite outputs as experimental observations or as independent validation targets.

### WP4 — mandatory prospective experimental validation

A prospective hold-out experiment is required for the paper's central predictive claim. Use the public benchmarks to set up the method, but do not claim a validated architecture ranking until tests on that architecture exist.

**Minimum material/architecture set:**

- monolithic alumina rod;
- monolithic ZTA rod;
- ZTA core with the 400 μm alumina outer layer represented in the public model.

Use 5 mm diameter × 50 mm long specimens to match the published rod design. If reproducing the core–shell manufacturing route is infeasible, explicitly narrow the central claim to the two monoliths and design a different held-out geometry before testing; do not retain untested multilayer claims.

**Inputs and measurements fixed independently of fracture outcomes:**

- characterize sister specimens for density, `E(T)`, Poisson ratio, thermal expansion, conductivity, heat capacity, toughness, and tensile/biaxial strength distributions;
- measure the quench-bath temperature and initial specimen temperature;
- determine the transient boundary heat-transfer condition from instrumented thermal-witness rods/temperature histories, not by adjusting it to match crack onset or crack morphology;
- use the measured thermal condition in the forward model, and publish raw thermal traces and calibration uncertainty;
- randomize specimen order and keep crack-image scorers unaware of model predictions.

Test at five prespecified temperature-difference levels per architecture, centered on the frozen model prediction and spanning its input-uncertainty interval. Use at least 10 independent rods per level (150 rods for three architectures); perform a prospective power/sample-size calculation from the independent strength variability and increase the count if that calculation requires it. The experimental plan may use acoustic emission/high-speed imaging for onset time and post-quench optical or tomographic inspection for crack presence/depth. The exact threshold definition and observation window must be frozen before testing.

**No-fit rule:** no post-shock fitting of heat-transfer coefficients, strength, toughness, phase-field length, viscous parameters, or fracture-model constants. No outcome-informed parameter selection, no author data requests, and no filling missing model parameters from a related Wang paper. Statistical intervals on observed proportions are allowed for validation, but cannot be fed back into the model.

### WP5 — preregistered evaluation and falsification

- Primary output: per-architecture predicted onset interval and the observed onset bracket, with sensor/material/input uncertainties propagated into the model's prediction interval.
- Primary comparison: whether each observed transition bracket overlaps the model's frozen 90% predictive interval. Report every architecture, including failures; do not refit a missed interval.
- Secondary comparison: specimen-level binary crack/no-crack predictions and Brier score for the coupled stress–energy model versus the maximum-stress baseline. Probabilities must come from independently measured pre-test input distributions, not a fit to quench outcomes.
- Report exact binomial intervals for observed crack proportions at each test level. Do not estimate a new model parameter or choose the “best” property row from these outcomes.
- Report the historical sphere limits and Papšík photos separately from the prospective confirmatory results so that reused data are not misrepresented as blind validation.

A meaningful negative result is that the criterion misses the new onset intervals, loses its architecture ranking under plausible measured-property uncertainty, or fails to outperform the baseline. Any of these is publishable as a falsification/transferability result if the experimental and verification protocols are sound.

## 6. Mandatory go/no-go gates

| Gate | Pass condition | If it fails |
|---|---|---|
| **G1 — data traceability** | Zenodo archive and license confirmed; material CSV and APDL inputs read; ZTA strength/Weibull discrepancy resolved or bounded in a declared sensitivity analysis. | Stop claims of exact Papšík reproduction; use the public images only as qualitative historical evidence. Do not hide the mismatch. |
| **G2 — numerical verification** | Independent code passes limiting-case tests and demonstrated mesh/time/crack-increment convergence. | Do not compare the model to experiments or write a prediction claim. |
| **G3 — boundary condition** | Thermal boundary history is independently measured for the new tests; historical fixed-h case is kept separate. | No validation claim for new rod thresholds; do not estimate h from cracks. |
| **G4 — held-out evidence** | Prospective tests include the architecture/material represented by each central claim, with blinded scoring and enough independent specimens. | Narrow the claims to tested cases. If no prospective validation is possible, reposition the work as a reproducibility/analytical benchmark, not a validated Q1-level predictive study. |
| **G5 — no leakage** | Predictions and analysis plan are frozen before hold-out outcomes are opened. | Label the analysis exploratory; it cannot count as blind validation. |

**Hard stop:** if the ZTA input discrepancy cannot be resolved and no new independent rod validation can be conducted, the Papšík dataset alone does not support the proposed central Q1-targeted predictive claim. Do not compensate by fitting, requesting author data, or treating simulations as experiments.

## 7. How the paper connects to the existing audit

The manuscript should include a short “relationship to prior checks” paragraph:

- The Wang (2024) Appendix A calculation is an algebraic limiting-case audit only; Eq. (A7) is inconsistent as printed with its stated traction-free side faces.
- The Shao (2014) script is an independent analytical sphere-threshold reproduction with coarse threshold-band comparison and property sensitivity.
- The Plan B rod analysis is a separate criterion/source and must be independently implemented and verified.
- No result in this Plan B validates Wang (2024)'s 3D PF-CZM/FEM implementation. Its missing inputs/source, the sphere-condition discrepancy, and other audit limitations remain open.

This separation is central to the paper's credibility and must also be reflected in figure captions, code comments, and the repository README.

## 8. Proposed manuscript structure and deliverables

1. Motivation and falsifiable hypotheses; distinguish stress-only, stress–energy, and phase-field formulations.
2. Source/data audit and preregistered parameter provenance.
3. Governing equations and independent numerical implementation.
4. Verification and convergence.
5. Historical sphere and public-rod checks, with their data limits.
6. Prospective blind rod validation and uncertainty-aware model comparison.
7. Architecture ranking, failure cases, limitations, and reproducibility.

**Required outputs:** source/input provenance table; checksummed prediction file frozen pre-test; code and environment lockfile; open thermal-witness traces and specimen-level crack labels; convergence tables; uncertainty/sensitivity tables; figure scripts; and a short data-license/citation note for the CC BY Zenodo material.

**Potential journal direction:** *Engineering Fracture Mechanics* or *Journal of the European Ceramic Society*, depending on whether the final contribution is led by fracture-mechanics transferability or ceramic testing/material behavior. This is a targeting recommendation, not a prediction of acceptance or quartile at submission time.

## 9. Source references

- Shao, Y. F. et al. (2014), “Dimension limit for thermal shock failure,” *Philosophical Magazine* 94, 2647–2655. [https://doi.org/10.1080/14786435.2014.926408](https://doi.org/10.1080/14786435.2014.926408).
- Papšík, R. et al. (2024), “Prediction of thermal shock induced cracking in multi-material ceramics using a stress-energy criterion,” *Engineering Fracture Mechanics* 303, 110121. [https://doi.org/10.1016/j.engfracmech.2024.110121](https://doi.org/10.1016/j.engfracmech.2024.110121).
- Papšík et al. public dataset, Zenodo record 13970234, CC BY 4.0. [https://doi.org/10.5281/zenodo.13970234](https://doi.org/10.5281/zenodo.13970234).
- Wang, T. et al. (2024), “Phase field modeling of crack propagation in three-dimensional quasi-brittle materials under thermal shock,” *Engineering Fracture Mechanics* 302, 110070. [https://doi.org/10.1016/j.engfracmech.2024.110070](https://doi.org/10.1016/j.engfracmech.2024.110070).
- Existing audit and reproducible scripts: [`README.md`](README.md), [`shao2014_sphere_threshold.py`](shao2014_sphere_threshold.py), [`single_element_limit.py`](single_element_limit.py).
