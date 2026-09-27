# Literature Search Log: Paper 11 Novelty Audit

**Search Window:** September 2026  
**Auditor:** Independent Scientific Audit Agent  
**Databases / Engines Searched:** Crossref, Google Scholar, ScienceDirect (Elsevier), SpringerLink, Wiley Online Library, Taylor & Francis, AIP Publishing, OSTI / DOE, arXiv.

---

## 1. Search Queries and Strategy

### Query Group 1: Guyer–Krumhansl and Boundary Heat Loss / Robin Conditions
- `"Guyer-Krumhansl" AND ("Robin" OR "convective boundary" OR "heat loss" OR "Biot")`
- `"Guyer Krumhansl" AND "laser flash" AND ("heat loss" OR "cooling")`
- `"Guyer-Krumhansl" AND "thermal boundary resistance"`
- *Objective:* Determine if any analytical or numerical solution of the Guyer–Krumhansl equation incorporates Robin boundary conditions in laser flash testing.

### Query Group 2: Guyer–Krumhansl Parameter Identifiability and Sensitivity
- `"Guyer-Krumhansl" AND ("identifiability" OR "parameter estimation" OR "inverse problem")`
- `"Guyer-Krumhansl" AND ("Fisher information" OR "sensitivity analysis" OR "Jacobian")`
- `"Guyer-Krumhansl" AND ("relaxation time" AND "nonlocal" AND "singularity")`
- *Objective:* Identify if previous inverse problem or sensitivity analyses evaluated the simultaneous determination of $(\tau_q, \kappa^2)$ or encountered rank deficiency.

### Query Group 3: Fourier Resonance and Degeneracy
- `"Fourier resonance" AND "Guyer-Krumhansl"`
- `"Guyer-Krumhansl" AND ("kappa^2/tau = alpha" OR "kappa2/tau = alpha" OR "B = 1")`
- `"Guyer-Krumhansl" AND ("degeneracy" OR "collinear" OR "singular")`
- *Objective:* Trace the exact origin and scope of the $B=1$ resonance condition across existing literature.

### Query Group 4: Classical Laser Flash Heat Loss Foundations
- `"Cowan" AND "laser flash" AND "thermal diffusivity"`
- `"Cape" AND "Lehman" AND "laser flash" AND "finite pulse"`
- `"Parker" AND "flash method" AND "heat loss"`
- *Objective:* Verify original classical benchmarks and heat-loss correction methodologies.

---

## 2. Records Examined & Bibliographic Verification

### Record 1: Kovács (2018)
- **Title:** *Analytic solution of Guyer-Krumhansl equation for laser flash experiments*
- **Authors:** Róbert Kovács
- **Journal:** *International Journal of Heat and Mass Transfer*, Vol. 127, pp. 631–636 (2018)
- **DOI:** [`10.1016/j.ijheatmasstransfer.2018.07.039`](https://doi.org/10.1016/j.ijheatmasstransfer.2018.07.039)
- **Verification:**
  * Examined governing equations: 1D linear Guyer–Krumhansl equation with thermal relaxation $\tau$ and nonlocality $\kappa^2$.
  * Boundary conditions: Front surface pulsed heat flux $q(0, t) = q_0$ for $t \in [0, t_p]$; rear surface adiabatic $q(L, t) = 0$.
  * Heat loss: Explicitly omitted. Convective and radiative cooling are NOT included ($Bi = 0$).
  * Content on resonance: Notes that when $B \equiv \kappa^2 / (\alpha \tau) = 1$, the analytical solution recovers the Fourier temperature rise. Does NOT perform sensitivity analysis, does NOT evaluate Fisher information, and does NOT investigate boundary heat loss.
- **Classification:** **Category B (Partial Prior Art / Baseline Anchor)**.

### Record 2: Both et al. (2016)
- **Title:** *Deviation from the Fourier law in room-temperature heat pulse experiments*
- **Authors:** S. Both, B. Czél, T. Fülöp, G. Gróf, Á. Gyenis, R. Kovács, P. Ván, J. Verhás
- **Journal:** *Journal of Non-Equilibrium Thermodynamics*, Vol. 41, No. 1, pp. 41–48 (2016)
- **DOI:** [`10.1515/jnet-2015-0038`](https://doi.org/10.1515/jnet-2015-0038)
- **Verification:**
  * Experimental heat pulse testing on room-temperature materials (basalt, metal foams).
  * Notes that Guyer–Krumhansl model captures non-Fourier effects. Mentions that the algebraic parameter combination $\kappa^2 / \tau = \alpha$ corresponds to "hierarchical resonance" / "Fourier resonance".
  * Boundary conditions: Modeled as adiabatic pulse excitation.
  * Inverse analysis: Curve fitting via non-linear least squares, but NO structural identifiability or sensitivity collinearity analysis, and NO boundary heat loss.
- **Classification:** **Category B (Partial Prior Art)**.

### Record 3: Ván et al. (2017)
- **Title:** *Guyer-Krumhansl–type heat conduction at room temperature*
- **Authors:** P. Ván, A. Berezovski, T. Fülöp, Gy. Gróf, R. Kovács, Á. Lovas, J. Verhás
- **Journal:** *EPL (Europhysics Letters)*, Vol. 118, No. 5, Art. 50005 (2017)
- **DOI:** [`10.1209/0295-5075/118/50005`](https://doi.org/10.1209/0295-5075/118/50005)
- **Verification:**
  * Demonstrates room-temperature GK behavior in rocks and composites.
  * Mentions Fourier resonance as a reference boundary between over-diffusive and under-diffusive regimes.
  * Treats only forward pulse response under adiabatic boundaries.
- **Classification:** **Category C (Background)**.

### Record 4: Cowan (1963)
- **Title:** *Pulse method of measuring thermal diffusivity at high temperatures*
- **Authors:** R. D. Cowan
- **Journal:** *Journal of Applied Physics*, Vol. 34, No. 4, pp. 926–927 (1963)
- **DOI:** [`10.1063/1.1729335`](https://doi.org/10.1063/1.1729335)
- **Verification:**
  * Formulates classical Fourier heat loss correction for laser flash experiments using symmetric and asymmetric surface radiation/convection.
  * Establishes the transcendental eigenvalue equation $\tan \mu_n = \frac{2Bi \mu_n}{\mu_n^2 - Bi^2}$.
  * Does not contain Guyer–Krumhansl, thermal relaxation, or spatial nonlocality.
- **Classification:** **Category B (Classical Foundation / Benchmark Anchor)**.

### Record 5: Cape & Lehman (1963)
- **Title:** *Temperature and finite pulse-time effects in the flash method for measuring thermal diffusivity*
- **Authors:** J. A. Cape, G. W. Lehman
- **Journal:** *Journal of Applied Physics*, Vol. 34, No. 7, pp. 1909–1913 (1963)
- **DOI:** [`10.1063/1.1729711`](https://doi.org/10.1063/1.1729711)
- **Verification:**
  * Derives dual corrections for finite laser pulse width and radiative cooling in 2D cylindrical geometry.
  * Based strictly on classical Fourier diffusion.
- **Classification:** **Category C (Background)**.

### Record 6: Parker et al. (1961)
- **Title:** *Flash method of determining thermal diffusivity, heat capacity, and thermal conductivity*
- **Authors:** W. J. Parker, R. J. Jenkins, C. P. Butler, G. L. Abbott
- **Journal:** *Journal of Applied Physics*, Vol. 32, No. 9, pp. 1679–1684 (1961)
- **DOI:** [`10.1063/1.1728417`](https://doi.org/10.1063/1.1728417)
- **Verification:**
  * Foundational laser flash paper. Establishes $\alpha = 0.1388 L^2 / t_{1/2}$. Assumes adiabatic conditions and classical Fourier diffusion.
- **Classification:** **Category C (Foundational Background)**.

### Record 7: Sellitto et al. (2025)
- **Title:** *Nonlinear Guyer–Krumhansl equation and boundary conditions in nanolayers with heat-flux dependent mean free path*
- **Authors:** Antonio Sellitto, Ilaria Carlomagno, Vito Antonio Cimmelli
- **Journal:** *Zeitschrift für angewandte Mathematik und Physik*, Vol. 76, Art. 52 (2025)
- **DOI:** [`10.1007/s00033-025-02481-2`](https://doi.org/10.1007/s00033-025-02481-2)
- **Verification:**
  * Examines nonlinear boundary slip in nanolayers with flux-dependent mean free path.
  * Treats microscopic boundary slip laws, but does NOT treat laser flash macro-scale convective/radiative heat loss, does not treat Fourier resonance, and does not study inverse problem identifiability.
- **Classification:** **Category C (Background)**.

---

## 3. Rejected False-Positive Records

1. **"Identifiability of heat-exchange parameters" (Tanana & Danilin 2003)**:
   * Studied simultaneous identification of heat transfer coefficient and ambient temperature in classical 1D/2D Fourier conduction.
   * *Reason for rejection:* Purely classical Fourier; zero connection to Guyer–Krumhansl transport or non-Fourier resonance.
2. **"Machine learning-assisted analytical modeling of nonlocal biothermoelastic response... using GK model" (2026)**:
   * Studied coupled thermoelastic skin response using GK bioheat equation.
   * *Reason for rejection:* Forward biothermoelastic solver with machine learning surrogate; no study of laser flash heat-loss invariance or sensitivity singularity.
3. **"A Bayesian inference approach to the inverse heat conduction problem" (Wang & Zabaras 2004)**:
   * Focused on heat flux estimation in classical Fourier IHCP.
   * *Reason for rejection:* Classical Fourier model; no GK terms.

---

## 4. Prior-Art Summary

- **Total Category A Records (Direct Overlap):** **0**
- **Total Category B Records (Partial Overlap):** **3** (Kovács 2018, Both et al. 2016, Cowan 1963)
- **Total Category C Records (Background):** **4** (Parker 1961, Cape & Lehman 1963, Ván 2017, Sellitto 2025)

**Conclusion:** No published work has investigated, derived, or stated that boundary convective/radiative heat loss preserves the Guyer–Krumhansl Fourier-resonance sensitivity singularity.
