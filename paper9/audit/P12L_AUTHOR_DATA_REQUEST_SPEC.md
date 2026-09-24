# P12L — Author-Data Request Specification (prepared, NOT sent)

**Purpose:** the minimum machine-readable external evidence required to close **PCR1** (and therefore
unblock **G3**), stated precisely enough that the PI can send it unchanged to the source authors.
**Status:** prepared under P12L; **no contact has been initiated, no message has been sent, and no
author has been approached.** Sending is a PI act under Decision A of
`P12L_PCR1_G3_FORMAL_BLOCKER_RECORD.md`.

**Accepted formats:** CSV, TXT (delimited or fixed-width), XLSX/XLS, MAT, JSON, or any equivalent
machine-readable format. Figures, screenshots or re-plots are **not** usable for the ≤2 % comparison;
plain numeric values in a message body are acceptable **only if** every quantity and unit below is
stated.

---

## 0. Common requirements (all three datasets)

For every requested dataset, please state:

1. **Figure/table identification** — which published item the dataset corresponds to (journal, volume,
   article number/DOI, figure and panel).
2. **Exact parameter set used to generate it** — every material, geometric and length-scale parameter,
   with values **and units**.
3. **Normalisation definitions** — how each plotted/normalised quantity is defined. In particular: the
   normalising frequency $\omega_0$ used for $\bar{\omega}$; how the wavenumber $\bar k$ is
   non-dimensionalised; and whether any length is normalised by a cell dimension, a layer thickness, or
   left dimensional.
4. **Boundary/interface conditions** — only where they are not already unambiguous in the paper (e.g.
   the set of continuity conditions applied at the layer interface for the requested case).
5. **Numerical precision and source format** — the precision as generated (double precision or as
   printed), and what tool produced the file.
6. **Coordinates/quantities expected** — for a dispersion dataset: the (wavenumber, frequency) pairs
   used to draw the curves; for gap data: the lower and upper edges of each band gap, in the same
   normalisation as the published plot.
7. **Branch indexing** — which branch is which, if the dataset contains several branches (needed for
   the "first four branch frequencies" comparison).

---

## 1. B1 — Layer 1, classical limit (Li et al. 2024, Fig. 2(a))

**Published anchor:** Li, Y.; Li, Y.; Guo, Z.; Wang, H.; Wang, C., *Scientific Reports* **14**:24035
(2024), DOI `10.1038/s41598-024-75049-1`, **Fig. 2(a)** (classical elasticity: $l=0,\ l_1=0,\ f=0$,
$L=0,\ L_1=0$; AlN/BaTiO₃ bilayer, normal incidence).

**Required numerical data:**

- the **(wavenumber, frequency) pairs** underlying the dispersion curves of Fig. 2(a) — or, if easier,
  the exact values at the plotted sampling used to draw the curves;
- the **band-gap edges** (lower/upper $\bar\omega$) of the first three stop bands of that panel;
- the **first four branch frequencies at two stated non-dimensional wavenumbers** (the paper defines
  its own $\bar k$; please name them), so the four lowest branches can be compared at fixed $\bar k$;
- confirmation of the **normalisation** used in the panel (definition of $\bar\omega$ and $\bar k$ for
  this figure), and the **parameter set** actually used (AlN: $\rho$, $c_{33}$, $a_A$; BaTiO₃: $\rho'$,
  $c'_{33}$, $a_B$; cell arrangement).

*Note: the criterion's classical-limit target is 0.5 % (mandatory bound 2 %); the smallest gaps plotted
in the panel are the decisive quantities, so please include the gap-edge values explicitly rather than
only the curve traces.*

## 2. B2 — Layer 2a, gradient elasticity with flexoelectricity suppressed (Li et al. 2024, Fig. 2(b))

**Published anchor:** same source, **Fig. 2(b)** ($f = 0$, $F = 0$; AlN/BaTiO₃ bilayer with internal
length scales).

**Required numerical data:**

- the **(wavenumber, frequency) pairs** and **band-gap edges** underlying Fig. 2(b), with the same
  completeness as §1;
- **the length-scale parameterisation — this is the blocking question.** The panel annotates a bare
  "`l = 1e-5`" while the paper's text defines a barred length. Please state, for the plotted case:
  - is the plotted quantity the **dimensional** $l$ (unit: m) or the **normalised** $\bar l$?
  - if normalised: **by what** is it normalised (cell dimension $b$, layer thickness $a_i$, or other),
    and what is the numerical value of that normalising length for this figure?
  - the corresponding definitions of $l_1$ (and $\bar l_1$), and of the material coefficients
    ($\mu_0 = c_{33}l^2$ prefactor or equivalent) actually used;
- the **parameter set** ($l_A, l_{1,A}, l_B, l_{1,B}$ and the cell dimensions $a_A, a_B$ or $b$) with
  units, as used for the plotted panel.

*Why this is mandatory: three internally consistent interpretations of the published text have been
run and produce different curves; without this clarification a numerical comparison cannot be
defined, regardless of the data supplied.*

## 3. B3 — Layer 2b, dipolar gradient Pb/brass bilayer (Li et al. 2023, Fig. 4(c))

**Published anchor:** Li, Y.; Askes, H.; Gitman, I. M.; Krynkin, A.; Wei, P., *Waves in Random and
Complex Media* **36**(4):5715–5735 (2023), DOI `10.1080/17455030.2023.2222189`, **Fig. 4(c)** (gradient
elasticity, comparison with the source's literature reference, thermoelastic coupling ignored; SH
waves in a periodic Pb/brass layered composite).

**Required numerical data:**

- the **(wavenumber, frequency) pairs** and **band-gap edges** underlying the Fig. 4(c) curves (the
  first two acoustic-optical branches shown in that panel);
- the **non-dimensional coefficients** actually used for the panel ($\bar c_1$, $\bar d_1$ and their
  ratios $\bar c_1/\bar c_2$, $\bar d_1/\bar d_2$; the \(\tau_R\) value, if the plotted case is
  isothermal please confirm it), with the definitions of $\bar c$ and $\bar d$ (including which length
  scale ($a_1$) normalises them);
- the **material and geometric parameters** for Pb and brass ($\mu$, $\rho$, layer thicknesses) as used
  for the plotted panel, with units.

*Note: the repository's evaluated case inherits the $\bar c_1 = 0.15$, $\bar d_1 = 0.25$,
$c_R = d_R = 1.5$ values from the source's **Fig. 3(b)** because the Fig. 4(c) panel annotates no
coefficients; if the plotted Fig. 4(c) case in fact uses different values, please state which.*

---

## 4. What is explicitly NOT requested

To keep the request narrow and purposeful, the following are **not** needed and are not being asked
for:

- source code, meshes, solver settings or implementation details;
- any unpublished model extensions, additional physics, or results not shown in the published figures;
- any figure files (images) — numeric values are what the criterion requires;
- any data beyond the three panels named above (e.g. Fig. 3, Fig. 5 or the thermoelastic cases are not
  part of the mandatory PCR1 set).

## 5. What acceptable data enables (acceptance test, no threshold changes)

Once received, the data are used exactly as follows, with the **existing** criteria (no new thresholds
are introduced):

| Step | Action | Artefact produced |
|---|---|---|
| 1 | Verify the supplied **parameter set + normalisation** against the published text and against the repository's recorded interpretation (especially B2's $l/\bar l$ question) | parameter-verification note |
| 2 | Re-run the **existing** solver configuration for that benchmark (no parameter tuning beyond the author-stated values) | numerical output (JSON) archived under `paper9/results/raw/` |
| 3 | Compare **gap edges** and the **first four branch frequencies at the stated $\bar k$** against the supplied values | comparison table |
| 4 | Compute the **relative error per quantity** and the **maximum relative error** | Table 3 extension (per-quantity + max) |
| 5 | Apply the **existing PCR1/G3 criterion**: mandatory **≤ 2 %** relative for all quantities; the **≤ 0.5 %** target applies to the classical limit (B1) | explicit PASS/FAIL per benchmark |
| 6 | Publish the same material in the **main manuscript** (per PCR2/G3 evidence rule), with per-benchmark PASS/FAIL | §5.1 revision + Fig. 4 if the overlays are updated |
| 7 | Re-assess **G3** (which additionally requires Layer 2c executed and the complete error table) and only then consider **G4**, which remains a PI signature after PCR1–PCR8 are checked | gate records |

No gate is closed by the mere receipt of data: closure requires steps 1–6 to produce agreement within
the existing thresholds, **and** the G3 completeness conditions of
`P12L_PCR1_G3_FORMAL_BLOCKER_RECORD.md` §2. Receipt of this data would **not** affect P5 (parallel-
pipeline reconciliation) or R-1 (pipeline-level reproducibility), both of which remain open
independently.
