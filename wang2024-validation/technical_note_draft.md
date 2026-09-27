# A reproducibility audit of the analytical and sphere-quench benchmarks in Wang et al. (2024)

**Draft status:** preliminary technical note; not a validation of the authors’ finite-element implementation. All numerical results below are reproducible with the accompanying standard-library Python scripts.

## Abstract

Wang et al. (2024) present a three-dimensional phase-field cohesive-zone model (PF-CZM) for ceramic-ball quenching and use a one-element cooling calculation and sphere experiments as validation evidence. We independently audited two bounded parts of that evidence. First, an isotropic thermoelastic calculation of the Appendix A one-element state shows that its printed Eq. (A7) is inconsistent with the stated traction-free lateral faces and with Eqs. (A5), (A6), and (A8): the compatible lateral strain is `(1+nu) alpha DeltaT`, rather than the printed `(1-nu) alpha DeltaT`. The PF-CZM strength-onset temperature-drop magnitude calculated from the reported material inputs is 60.8108 K. Second, we independently implemented the spherical heat-conduction and thermal-stress threshold equations in the cited Shao et al. (2014) paper. Using its 20–600 °C property row gives critical drops of 219.3 K for radius 2.10 mm, 548.3 K for radius 0.35 mm, and 1291.0 K for radius 0.11 mm. The first two are lower than the paper’s approximate textual onset markers (about 240 K and above 620 K); the small-sphere prediction is just above the reported no-crack test at 1280 K. Repeating the calculation for all five temperature-averaged property rows shows that the 20–400 °C and 20–600 °C rows bracket the two approximate larger-sphere markers and predict no cracking at 1280 K for the 0.11 mm sphere, consistent with Shao et al.’s stated property-range conclusion. Applying the same simplified analytical threshold equation to Wang et al.’s different Table 2 property set gives much lower thresholds; this is a property-traceability diagnostic, not a simulation of Wang’s PF-CZM. The checks do not verify the 2024 solver or reproduce its 3D fields. The reported baseline `l_c` and `eta`, executable source/input, and tabulated ball-comparison data are unavailable from the inspected public sources. The evidence supports a limited analytical/reproducibility note, not a claim that the 3D solver has been validated.

**Keywords:** thermal shock; phase-field cohesive-zone model; reproducibility; thermoelasticity; alumina spheres; verification

## 1. Scope and research question

This note asks whether the publicly reported analytical limiting case and the cited sphere-quench threshold data can be independently checked from the papers’ stated equations and inputs. It does not implement or test the Abaqus PF-CZM solver described by Wang et al. (2024), and it does not claim to reproduce the reported three-dimensional ceramic-ball calculations.

The distinction between checks is important:

1. **Equation/algebra check:** independently solve the 2024 Appendix A one-element thermoelastic limit.
2. **External benchmark check:** independently evaluate the Shao et al. (2014) spherical thermal-shock threshold equations and compare with that paper’s text-reported experimental limits.
3. **Solver verification and 3D reproduction:** not performed because the 2024 numerical baseline and executable implementation are not publicly specified in the inspected materials.

## 2. Sources and model distinction

### 2.1 Wang et al. (2024)

Wang et al. report `E=370 GPa`, `nu=0.22`, `f_t=180 MPa`, `G_c=0.0425 N/mm`, `k_0=12 W/(m K)`, and `alpha=8.0e-6/K` in Table 2 for the ceramic-ball modeling. The text reports a convection coefficient of `80 N/(mm s K)`, equivalent dimensionally to `80,000 W/(m^2 K)`. Table 2 does not state the baseline phase-field length `l_c` or viscosity `eta`; without `l_c`, Eq. (25) does not fix `a_1` for the PF-CZM degradation function.

Appendix B is titled as Python source for calculating the *analytical* one-element phase-field and stress solutions. The supplied article PDF gives a short description of that code but contains no listing or direct download link; it is not identified as the Abaqus 3D solver source. The article’s reference [11] is Shao et al. (2014), “Dimension limit for thermal shock failure.” Section 4.2 describes the R=1 mm case as a 780 K drop, whereas the Fig. 9 caption labels it as 380 K. This conflict must be resolved before that particular image is used as a reproduction target.

### 2.2 Wang et al. (2020) is a different model

Wang et al. (2020) uses an AT2-type crack-surface regularization, `d^2/(2 l_c) + l_c |grad d|^2/2`, and alternative energy splits. It is not the 2024 PF-CZM. Its one-element uniaxial test is described with a 1 mm cube, `E=210 GPa`, `nu=0`, `rho=7800 kg/m^3`, `G_c=0.01 kN/mm`, `eta=1e-7 kN s/mm^2`, and `l_c=1 mm`, loaded over 0.01 s. Although the article advertises supplementary Abaqus subroutines and an input file, the archived source/input could not be retrieved in this audit; the test description was not executed. This is a possible separate AT2 regression test, not evidence for the 2024 PF-CZM.

### 2.3 Wang et al. (2022) is closer but does not supply the 2024 baseline

The 2022 paper implements PF-CZM and gives a ceramic-plate example with `E=370 GPa`, `nu=0.22`, `G_c=0.0425 N/mm`, `f_t=180 MPa`, `rho=2450 kg/m^3`, `c=840 J/(kg K)`, `k_0=20 W/(m K)`, `alpha=6e-6/K`, `h=0.05 mm`, and `l_c=2h=0.10 mm`. Those are inputs to that plate example. They are not an explicit declaration of `l_c` or `eta` for the 2024 single-element or ball baseline and are not transferred here.

## 3. Methods

### 3.1 One-element thermoelastic limit

Let `e_th=alpha DeltaT`, with signed `DeltaT`; the cooling magnitude is `theta=-DeltaT>0`. The Appendix A kinematics are `epsilon_x=epsilon_y` and `epsilon_z=0`. Isotropic elasticity and zero lateral stress give

` sigma_x = lambda(2 epsilon_x - 3 e_th) + 2 mu(epsilon_x - e_th) = 0 `,

so

` epsilon_x = [(3 lambda + 2 mu)/(2 lambda + 2 mu)] e_th = (1+nu)e_th `.

This differs from Eq. (A7) as printed, `(1-nu)e_th`. Substituting the compatible strain gives zero lateral stress and axial tensile-stress magnitude `E alpha theta`. The reported PF-CZM onset occurs when that stress reaches `f_t`, hence

` theta_c = f_t/(E alpha) `.

At onset, the effective energy release rate is `H=f_t^2/(2E)`. Table 2 gives `theta_c=60.810810811 K` and `H=43,783.783784 J/m^3`. At the onset, Eq. (A11) reduces to the same condition at `d=0`; this does not determine the post-onset `d(theta)` curve without `l_c` (through `a_1`).

For the printed Eq. (A7), the independent isotropic constitutive calculation gives a lateral stress of 115.925 MPa at the stated onset; Eq. (A6) then gives 231.007 MPa axially, inconsistent with Eq. (A8)’s 180 MPa. This is an algebraic inconsistency in the printed limiting-case derivation, not evidence by itself that the numerical solver is wrong.

### 3.2 Independent implementation of the Shao sphere-threshold equations

Shao et al. (2014), Eqs. (5)–(15), give a series solution for a sphere initially at uniform temperature and suddenly exposed to a convective medium. For each radius, the Biot number is `Bi=hR/k`; the positive eigenvalues solve `beta_n cot(beta_n)=1-Bi`. The dimensionless surface-hoop-stress history is evaluated as a series in Fourier number `F=a t/R^2` and maximized over `F`. Writing the maximum dimensionless stress factor as `q_max(Bi)`, the threshold is

` DeltaT_c = sigma_0(1-nu) / [E alpha q_max(Bi)] `.

The maximum over Fourier number removes the need for `rho c_p` for this threshold-only calculation; those data would be needed to convert the maximizing Fourier number to physical time. Roots are bracketed and solved by bisection; the Fourier-number maximum is found by a logarithmic scan followed by golden-section refinement. The result is checked for monotonicity with radius and convergence between 80- and 120-mode series truncations (relative threshold change below `1e-6` for the reported rows).

The primary calculation uses Shao et al.’s Table 1 average parameters for 20–600 °C: `E=380 GPa`, `nu=0.22`, `sigma_0=358 MPa`, `h=80,000 W/(m^2 K)`, `k=18.4 W/(m K)`, and `alpha=7.7e-6/K`. The same calculation is repeated for each of the five property-range rows in Table 1. No digitization of figures is used.

## 4. Results

### 4.1 Appendix A one-element result

The independent onset drop is **60.8108 K**. The compatible strain is `(1+nu)alpha DeltaT`; the printed Eq. (A7) does not satisfy the traction-free lateral boundary condition. The detailed reproducible output is in `single_element_limit.py`.

### 4.2 Shao sphere-quench threshold

Using the 20–600 °C property row gives:

| Radius (mm) | Bi | `q_max` | Fourier number at peak | Predicted `DeltaT_c` (K) |
|---:|---:|---:|---:|---:|
| 2.10 | 9.1304 | 0.435231 | 0.016006 | 219.3 |
| 1.00 | 4.3478 | 0.316904 | 0.028886 | 301.1 |
| 0.56 | 2.4348 | 0.232719 | 0.043426 | 410.1 |
| 0.35 | 1.5217 | 0.174047 | 0.058170 | 548.3 |
| 0.11 | 0.4783 | 0.073925 | 0.103525 | 1291.0 |

Shao et al. report that R=2.1 mm spheres crack only above about 240 K, R=0.35 mm spheres require more than 620 K, and R=0.11 mm spheres remain uncracked even at 1280 K. These statements are inequalities/round conditions, not tabulated critical points. The 20–600 °C row predicts onset 8.6% below 240 K for R=2.1 mm and 11.6% below 620 K for R=0.35 mm, while it predicts a 1291 K threshold for R=0.11 mm.

Shao et al. explicitly compare average-property rows from 20–300 through 20–1300 °C and state that the 20–400 and 20–600 °C curves are consistent with their experiments. The independent recalculation gives:

| Property range | R=2.10 mm (K) | R=0.35 mm (K) | R=0.11 mm (K) |
|---|---:|---:|---:|
| 20–300 °C | 290.7 | 792.4 | 1953.7 |
| 20–400 °C | 258.4 | 681.7 | 1652.4 |
| 20–600 °C | 219.3 | 548.3 | 1291.0 |
| 20–800 °C | 194.2 | 464.4 | 1065.4 |
| 20–1300 °C | 165.7 | 367.7 | 805.7 |

The 20–400 and 20–600 °C rows bracket the two round-number larger-sphere onset markers and both keep the 0.11 mm sphere below onset at 1280 K. The wider property intervals depart significantly. This supports the published analytical trend and its sensitivity statement, with threshold-level disagreement for the 20–600 °C row; it is not an exact validation against raw experimental observations.

### 4.3 Material-property traceability diagnostic

Applying the same **simplified Shao analytical threshold equation** to Wang et al.’s Table 2 properties (`E=370 GPa`, `nu=0.22`, `f_t=180 MPa`, `k_0=12 W/(m K)`, `alpha=8e-6/K`, `h=80,000 W/(m^2 K)`) gives thresholds of 94.1, 123.4, 161.5, 208.9, and 457.8 K for radii 2.1, 1.0, 0.56, 0.35, and 0.11 mm, respectively. In particular, this static fully exposed sphere formula with the 2024 material set would predict a much lower onset than Shao’s reported 0.35 mm and 0.11 mm observations. This is **not** a prediction from Wang’s PF-CZM, whose moving-ball thermal history and damage coupling differ. It identifies a material/protocol mismatch requiring explanation before treating the 2024 experimental comparison as an independent quantitative validation.

## 5. Discussion

Three levels of evidence must not be conflated. The one-element algebra calculation checks a limiting-case derivation. The Shao calculation reproduces a cited analytical benchmark and evaluates whether its stated trends and threshold bands align with the experiment. Neither runs the 2024 numerical solver. Wang et al. report that their one-element numerical histories match an analytical solution, but the full numerical curves are not tabulated and the baseline `l_c` and `eta` needed for an independent post-onset reconstruction are not specified in the inspected paper. The 2024 ball comparison likewise lacks tabulated crack-block counts, and its data statement says “Data will be made available on request.” No author request was made.

The cited methods papers are not interchangeable: Wang et al. (2020) is an AT2-type gradient-damage implementation, whereas Wang et al. (2022) contains PF-CZM examples. Neither supplies confirmed 2024 baseline values. The experiment source further documents different strength and thermal-property values from the 2024 Table 2. These gaps do not prove that the 2024 3D results are incorrect; they limit independent reproducibility and the strength of the validation claim.

## 6. Conclusions

1. The 2024 Appendix A Eq. (A7) is inconsistent with its stated traction-free lateral condition; the compatible factor is `1+nu`.
2. The PF-CZM onset drop from the reported Table 2 inputs is 60.8108 K. This verifies the onset algebra only.
3. An independent implementation of Shao et al.’s analytical sphere threshold reproduces the reported size effect. The 20–400 and 20–600 °C property rows bracket the paper’s approximate larger-sphere markers and predict no crack at 1280 K for the 0.11 mm sphere.
4. Substituting Wang et al.’s Table 2 properties into that different analytical model gives much lower onset thresholds; this is a traceability diagnostic, not a PF-CZM result.
5. The evidence supports a bounded analytical/reproducibility audit. **The 2024 FEM/PF-CZM solver, its transient numerical histories, and its 3D ball predictions remain unvalidated by this work.**

## Reproducibility

From the repository root:

```bash
python wang2024-validation/single_element_limit.py
python wang2024-validation/shao2014_sphere_threshold.py
```

Both scripts use only Python’s standard library. The second script includes the Shao Table 1 temperature-range sensitivity and the clearly labeled Wang Table 2 diagnostic.

## References

1. T. Wang, Y. Zhang, H. Han, L. Wang, X. Ye, and Z. Zhuang, “Phase field modeling of crack propagation in three-dimensional quasi-brittle materials under thermal shock,” *Engineering Fracture Mechanics* 302 (2024), 110070. https://doi.org/10.1016/j.engfracmech.2024.110070
2. Y. F. Shao, Q. N. Liu, H. J. Tian, Z. K. Lin, X. H. Xu, and F. Song, “Dimension limit for thermal shock failure,” *Philosophical Magazine* 94 (2014), 2647–2655. https://doi.org/10.1080/14786435.2014.926408
3. T. Wang, H. Han, Y. Wang, X. Ye, G. Huang, Z. Liu, et al., “Simulation of crack patterns in quasi-brittle materials under thermal shock using phase field and cohesive zone models,” *Engineering Fracture Mechanics* 276 (2022), 108889. https://doi.org/10.1016/j.engfracmech.2022.108889
4. T. Wang, X. Ye, Z. Liu, X. Liu, D. Chu, and Z. Zhuang, “A phase-field model of thermo-elastic coupled brittle fracture with explicit time integration,” *Computational Mechanics* 65 (2020), 1305–1321. https://doi.org/10.1007/s00466-020-01820-6
