# Wang et al. (2024): defensible limiting-case check

## Source inspected

T. Wang et al., “Phase field modeling of crack propagation in three-dimensional quasi-brittle materials under thermal shock,” *Engineering Fracture Mechanics* 302 (2024), 110070. DOI: [10.1016/j.engfracmech.2024.110070](https://doi.org/10.1016/j.engfracmech.2024.110070). The full 16-page PDF supplied by the user is also available at the [repository PDF URL](https://raw.githubusercontent.com/vipin-oss/BFS-FEM-MATLAB/main/1-s2.0-S0013794424002339-main.pdf).

The independent check is deliberately limited to the paper’s one-element thermoelastic limiting case in Appendix A (publisher PDF p. 14), at the PF-CZM tensile-strength onset. It is **not** an Abaqus, finite-element, or 3D-ball reproduction.

## Reproducible run

From this directory’s parent:

```bash
python wang2024-validation/single_element_limit.py
```

The script uses only the Python standard library. It builds the isotropic 3D normal stiffness from the reported `E` and `nu`, imposes zero normal strain in z, leaves the other four faces traction-free, and independently checks the printed Appendix A relations.

## Inputs and result

Table 2 (publisher PDF p. 6) gives `E = 370 GPa`, `nu = 0.22`, `ft = 180 MPa`, and `alpha = 8.0e-6 K^-1`. For signed temperature change `DeltaT = T - T_ref`, cooling has `DeltaT < 0`; the plotted “temperature drop” is its positive magnitude `theta = -DeltaT`.

At the PF-CZM onset, `E alpha theta_c = ft`, so the independently calculated limit is:

- `theta_c = 60.810810811 K`;
- tensile `sigma_z = 180 MPa`;
- `H = ft^2/(2E) = 43,783.783784 J/m^3`;
- `l_ch = E G_c / ft^2 = 0.485339506 mm`, using Table 2’s `G_c = 0.0425 N/mm` and Eq. (25).

## Defensible finding: Appendix A Eq. (A7) is inconsistent as printed

Appendix A states `epsilon = [epsilon_x, epsilon_x, 0, ...]`, uses the isotropic constitutive law, and says the four side faces are free. Its Eq. (A5) is

`(1-nu)(epsilon_x-alpha DeltaT) + nu(epsilon_x-alpha DeltaT) - nu alpha DeltaT = 0`.

Solving that equation gives `epsilon_x = (1+nu) alpha DeltaT`, not the printed Eq. (A7), `epsilon_x = (1-nu) alpha DeltaT`. The `1+nu` result also makes Eqs. (A6) and (A8) mutually consistent and gives zero lateral stress, as required by the stated free-face boundary condition.

At the reported PF-CZM onset, using Eq. (A7) literally instead gives a lateral stress of **115.925 MPa** and an Eq. (A6) axial stress of **231.007 MPa**, while Eq. (A8) gives **180 MPa**. Using `1+nu` gives zero lateral stress and 180 MPa axial tension. The script asserts both the consistent result and the nonzero residual from the printed Eq. (A7). This is a clear algebraic inconsistency in the published limiting-case derivation; it is most consistent with a typographical error in Eq. (A7), and by itself does not prove that the 3D solver results are wrong.

## What this does and does not validate

**Pass:** an independent thermoelastic one-element algebra check at the PF-CZM onset, after correcting the apparent Eq. (A7) typo. Eq. (A11) also reduces at `d=0` to the same onset condition `E alpha theta = ft`.

**Not validated:** the paper’s plotted full phase-field/stress curves, transient numerical integration, Abaqus implementation, or 3D ceramic-ball predictions. Table 2 does not give the base-case phase-field length `l_c`; Eq. (25) therefore leaves `a_1 = (4/pi) l_ch/l_c` undetermined. The viscous parameter `eta` in Eq. (23) is discussed but not reported numerically. The paper’s Appendix B says Python source code is provided, but the supplied 16-page PDF contains only a description—not a code listing. The Data availability statement (p. 13) says data will be made available on request, which is not public data.

There is also a traceability conflict in the ball comparison: Section 4.2 (p. 7) describes the `R = 1.00 mm` case as `DeltaT = -780 K`, while the Fig. 9 caption on p. 9 says `DeltaT = -380 K`. The paper does report experimental comparisons of surface morphology and statistical observables (Sections 4.2–4.3; Figs. 9, 12–15), but that condition mismatch must be resolved before claiming reproduction of that particular case.

## Correction to the benchmark citation previously suggested

The 2024 paper’s reference [11] is **not** the 2016 Springer paper previously suggested. Its actual reference [11] is:

Y. F. Shao, Q. N. Liu, H. J. Tian, Z. K. Lin, X. H. Xu, and F. Song, “Dimension limit for thermal shock failure,” *Philosophical Magazine* 94 (2014), 2647–2655. DOI: [10.1080/14786435.2014.926408](https://doi.org/10.1080/14786435.2014.926408).

The cited experiment has now been inspected independently. The earlier suggested “Fracture characteristics of silicon nitride ceramic ball subjected to thermal shock” (DOI `10.1007/s10853-016-9855-1`) is a different paper and should not be substituted for Wang’s ref. [11].

## Related-source audit: keep the models distinct

**Wang et al. (2020) is not the 2024 PF-CZM.** T. Wang et al., “A phase-field model of thermo-elastic coupled brittle fracture with explicit time integration,” *Computational Mechanics* 65 (2020), 1305–1321, [DOI: 10.1007/s00466-020-01820-6](https://doi.org/10.1007/s00466-020-01820-6). Its regularized crack-surface term is the standard AT2-type gradient-damage form, proportional to `d^2/(2 l_c) + l_c |grad d|^2/2`; it does not use the 2024 cohesive degradation function calibrated by `f_t` and `a_1`. The 2020 paper also considers alternative tensile/compressive energy splits, but that does not make it PF-CZM. It documents a useful separate one-element uniaxial test: a 1 mm cube, `E=210 GPa`, `nu=0`, `rho=7800 kg/m^3`, `G_c=0.01 kN/mm`, `eta=1e-7 kN s/mm^2`, and `l_c=1 mm`, with linear displacement loading over 0.01 s. The paper says its supplementary material includes Abaqus subroutines and the one-element `.inp` file. The Springer article page identifies that supplement as available to authorized users; an anonymous request to the corresponding official supplementary URL returned `AccessDenied`. Thus the published test description is inspected, but the archived source/input were not obtained or run. This can be a distinct AT2 implementation regression test if the artifact becomes lawfully accessible; it cannot validate the 2024 PF-CZM solver.

**Wang et al. (2022) is the closer PF-CZM source, but its example inputs do not fill the 2024 omissions.** T. Wang et al., “Simulation of crack patterns in quasi-brittle materials under thermal shock using phase field and cohesive zone models,” *Engineering Fracture Mechanics* 276 (2022), 108889, [DOI: 10.1016/j.engfracmech.2022.108889](https://doi.org/10.1016/j.engfracmech.2022.108889). Its ceramic-plate table reports `E=370 GPa`, `nu=0.22`, `G_c=0.0425 N/mm`, `f_t=180 MPa`, `rho=2450 kg/m^3`, `c=840 J/(kg K)`, `k_0=20 W/(m K)`, and `alpha=6e-6/K`; that plate example uses `h=0.05 mm`, `l_c=2h=0.10 mm`, and convection `55 N/(mm s K)`. These are inputs to the 2022 plate example, not an explicit declaration of the 2024 ball or one-element base-case `l_c` and `eta`. They must not be silently transferred.

**Shao et al. (2014) experimental conditions are now checked.** As-sintered 99.5% alumina spheres of radii 0.11, 0.35, 0.56, 1.0, and 2.1 mm (about 4.9% porosity) were used, with six specimens per size group. Specimens were heated at 10 °C/min, held 20 min, free-fall quenched into 20 °C water within five seconds, dried, dye-impregnated, and inspected microscopically. The paper states that the 2.1 mm spheres cracked only above a 240 K drop, 0.35 mm spheres required more than 620 K, and 0.11 mm spheres showed no cracks even at 1280 K. These text-reported observations are useful qualitative/threshold checks, not tabulated surface-block counts or digitized crack maps.

There is a material-input traceability difference between the experiment source and the 2024 simulation. Shao et al.’s Table 1 row for 20–600 °C reports `E=380 GPa`, `nu=0.22`, strength `358 MPa`, `k=18.4 W/(m K)`, and `alpha=7.7e-6/K` (with `h=80,000 W/(m^2 K)`). Wang et al. (2024) instead lists `E=370 GPa`, `nu=0.22`, `f_t=180 MPa`, `k_0=12 W/(m K)`, and `alpha=8.0e-6/K`; its convection value `80 N/(mm s K)` is dimensionally equivalent to `80,000 W/(m^2 K)`. These are not identical material-property sets. This is a provenance/quantitative-comparability gap to resolve, not by itself evidence that the numerical result is false. Shao’s individual experimental points and Wang’s crack-block count data are not tabulated in the inspected papers; the 2024 paper says data are available on request. No curve digitization or author contact/data request was performed.

## New independent benchmark: Shao et al. sphere-quench threshold

I added `shao2014_sphere_threshold.py`, a standard-library implementation of the spherical transient-conduction and thermoelastic surface-hoop-stress equations in Shao et al. (2014), Eqs. (5)–(15). It uses the paper’s Table 1 average properties for 20–600 °C: `E=380 GPa`, `nu=0.22`, strength `sigma_0=358 MPa`, `h=80,000 W/(m^2 K)`, `k=18.4 W/(m K)`, and `alpha=7.7e-6/K`. The series uses the Robin eigenvalues `beta_n cot(beta_n)=1-Bi`, with `Bi=hR/k`; the dimensionless surface-stress maximum is evaluated over Fourier number and Eq. (15) gives `DeltaT_c=sigma_0(1-nu)/(E alpha q_max)`. Because the calculation maximizes over Fourier number, missing `rho c_p` is not needed for this threshold-only check (it would be needed to convert peak Fourier number to physical time).

Run from the repository root:

```bash
python wang2024-validation/shao2014_sphere_threshold.py
```

Independent output:

| Sphere radius (mm) | Bi | `q_max` | `F` at peak | Predicted critical drop (K) |
|---:|---:|---:|---:|---:|
| 2.10 | 9.1304 | 0.435231 | 0.016006 | 219.3 |
| 1.00 | 4.3478 | 0.316904 | 0.028886 | 301.1 |
| 0.56 | 2.4348 | 0.232719 | 0.043426 | 410.1 |
| 0.35 | 1.5217 | 0.174047 | 0.058170 | 548.3 |
| 0.11 | 0.4783 | 0.073925 | 0.103525 | 1291.0 |

**Result: qualified agreement within the material-property range Shao reports.** With the 20–600 °C row alone, the thresholds increase as radius decreases, and the `R=0.11 mm` prediction (1291 K) is just above the reported no-crack test at 1280 K. The two larger-sphere predictions are lower than the prose onset markers: 219 K versus about 240 K at `R=2.10 mm` (−8.6%), and 548 K versus more than 620 K at `R=0.35 mm` (−11.6% relative to 620 K).

Shao et al. also tabulate averages over several temperature ranges and state that their 20–400 °C and 20–600 °C theoretical curves are the ones consistent with experiment. Recomputing all five property rows gives:

| Property range | `R=2.10 mm` (K) | `R=0.35 mm` (K) | `R=0.11 mm` (K) |
|---|---:|---:|---:|
| 20–300 °C | 290.7 | 792.4 | 1953.7 |
| 20–400 °C | 258.4 | 681.7 | 1652.4 |
| 20–600 °C | 219.3 | 548.3 | 1291.0 |
| 20–800 °C | 194.2 | 464.4 | 1065.4 |
| 20–1300 °C | 165.7 | 367.7 | 805.7 |

The 20–400 and 20–600 °C rows bracket the two round-number onset markers and both predict no cracking at 1280 K for the 0.11 mm sphere, consistent with Shao et al.’s stated property-range conclusion. The wider-range rows depart substantially. Since the experimental thresholds are reported as prose/figure observations rather than exact tabulated measurements, this is a **reproduced analytical benchmark with a qualified threshold-band check**, not a precision fit or exact experimental validation. No points were digitized.

As a **separate parameter-traceability diagnostic only**, I also evaluated the same linear-elastic sphere threshold equation with Wang (2024) Table 2’s values (`E=370 GPa`, `nu=0.22`, `f_t=180 MPa`, `k_0=12 W/(m K)`, `alpha=8e-6/K`, and the matching `h=80,000 W/(m^2 K)`). It gives predicted thresholds of 94 K, 123 K, 161 K, 209 K, and 458 K for radii 2.1, 1.0, 0.56, 0.35, and 0.11 mm, respectively. These are far below Shao’s textual limits, especially for the 0.11 mm sphere. This is **not** a simulation of Wang’s PF-CZM, and the moving-ball thermal history and differing material set prevent treating it as a direct falsification. It does show that the experimental material-property provenance matters materially; the 2024 paper needs a clear reconciliation of its `f_t=180 MPa` input with the cited experiment’s reported 358 MPa strength before quantitative comparisons can be independently assessed.

**Scope:** this independently checks the *Shao analytical sphere-quench benchmark* against its text-reported experiment. It does not execute or validate the 2024 PF-CZM/FEM solver. It is a new, reproducible physical-benchmark check beyond the prior Appendix A algebra audit, but does not close the full solver-validation gap.

## Validation status and unavailable inputs

- **Completed checks:** (1) the 2024 Appendix A one-element thermoelastic/PF-CZM onset algebra check; and (2) the independent Shao (2014) analytical sphere-quench threshold calculation compared with the paper’s text-reported experimental limits.
- **Not performed:** verification/validation of the 2024 solver or code, numerical reproduction of its one-element time histories, reproduction of its 3D FEM results, experimental validation of the 2024 crack-block statistics, or 3D simulation. The Shao benchmark validates neither Wang’s PF-CZM implementation nor its 3D predictions; the 2024 visual morphology comparison remains unreproduced.
- **UNAVAILABLE FROM PUBLIC SOURCE:** the 2024 baseline numerical values of `l_c` and `eta`, the 2024 source code/input files, and tabulated numerical values for the plotted crack-block comparisons. The 2020 supplementary AT2 source/input is cited by that article but was not anonymously retrievable in this audit. Related-paper values are not substitutes.

**WP1 STATUS: NOT STARTED** for full solver/benchmark validation. **3D SIMULATION: NOT AUTHORIZED. POST-SHOCK FITTING: NOT AUTHORIZED. AUTHOR DATA: NOT REQUESTED.**

## Plan B research blueprint

A separate Q1-targeted (not acceptance-guaranteed) blueprint proposes a parameter-locked, cross-geometry validation of thermal-shock initiation criteria, reusing the Shao sphere calculation and evaluating the open Papšík et al. rod archive without treating it as sufficient validation by itself. It requires a prospective blinded rod experiment before making a predictive architecture claim and preserves the boundary that none of this validates Wang (2024)'s PF-CZM solver. See [`plan_b_blueprint.md`](plan_b_blueprint.md) for the hypotheses and full protocol. Execution has begun: [`plan_b_execution_log.md`](plan_b_execution_log.md) records checks completed and blockers. [`papsik_input_audit.py`](papsik_input_audit.py) checks source-input scales, while [`papsik_radial_thermal.py`](papsik_radial_thermal.py) is a verified reduced radial heat-transfer baseline—not the published FEM or a fracture simulation.
