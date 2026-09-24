# P12M — Author-Data Request Drafts (three scoped messages, PREPARED, NOT SENT)

**Status:** prepared under PI authorization (P12M). **No message has been sent; no author has been
contacted.** Sending is a PI act. Recipient identity/contact channel is deliberately left as a
placeholder to be filled from each publication's own record — no recipient name or address is invented
here. (For the Li et al. 2024 article, the source PDF's own data-availability statement names the
corresponding author's contact channel; that is the intended route. For the Li et al. 2023 article no
such statement is published, so the publisher-listed corresponding-author channel applies.)

**Scope of each request:** only the missing numerical benchmark data needed to compare published
quantities against our independent calculations for validation/reproducibility purposes. **No source
code, no unpublished material, no unrelated figures.** Machine-readable files are preferred; CSV, TXT,
XLSX/XLS, MAT, JSON or equivalent are all acceptable. Naming the datasets does not imply any result:
**no claim is made in these messages, or anywhere in this repository, that the benchmark has already
been validated against the requested data.**

The technical minimum behind each message is `P12L_AUTHOR_DATA_REQUEST_SPEC.md` §0–§3. If shorter
messages are preferred, the numbered asks below are the irreducible minimum; the "detail" lines can be
dropped only if the corresponding file self-describes its units and normalisation.

---

## 1. Request B1 — Li et al., *Sci. Rep.* **14**:24035 (2024), Fig. 2(a)

**Subject:** Request for the numerical data underlying Fig. 2(a) of *Scientific Reports* 14:24035 (2024) — for independent validation

**Recipient:** `[corresponding author / contact channel as stated in the article's data-availability
statement]`

> Dear Dr. Li and co-authors,
>
> I am carrying out an independent implementation of the strain-gradient / flexoelectric phononic-crystal
> dispersion problem and would like to validate it against your published benchmark. I am writing to ask
> whether you could share the numerical data behind **Fig. 2(a)** of your *Scientific Reports* 14:24035
> (2024) article — the classical-elasticity panel (l = 0, l₁ = 0, f = 0, L = 0, L₁ = 0) for the AlN/BaTiO₃
> bilayer.
>
> Specifically, for that panel:
>
> 1. the **numerical points** underlying the plotted dispersion curves (wavenumber–frequency pairs, in
>    the same normalisation as the panel);
> 2. the **lower and upper edges of the first three stop bands** (normalised frequency);
> 3. the **first four branch frequencies at a stated normalised wavenumber** (please name the
>    wavenumber(s) you would like used, or state the values at, say, two representative values);
> 4. the **exact parameter set used for that figure** (layer materials and their ρ, c₃₃, layer
>    thicknesses / cell size, and any length-scale parameter set to zero), with units;
> 5. the **normalisation definitions** used in the panel (how ω̄ and k̄ are defined for that figure).
>
> Any machine-readable format is perfectly fine — CSV, TXT, XLSX/XLS, MAT, JSON or similar — and plain
> numeric values in an email with the units stated would also be sufficient. **I am not asking for any
> source code or unpublished material** — only the published benchmark's numerical values.
>
> The purpose is reproducibility of your published results: with these values I can compare my
> independent calculation point by point and report the comparison honestly, including any mismatch.
> Thank you very much for considering this request.
>
> With best regards,
> [PI name, affiliation, contact]

---

## 2. Request B2 — Li et al., *Sci. Rep.* **14**:24035 (2024), Fig. 2(b)

**Subject:** Request for the numerical data underlying Fig. 2(b) of *Scientific Reports* 14:24035 (2024), including the length-scale definition used — for independent validation

**Recipient:** `[corresponding author / contact channel as stated in the article's data-availability
statement]`

> Dear Dr. Li and co-authors,
>
> I am independently reproducing the strain-gradient dispersion results in your *Scientific Reports*
> 14:24035 (2024) article and would like to compare against **Fig. 2(b)** — the strain-gradient panel
> (flexoelectricity suppressed: f = 0, F = 0) for the AlN/BaTiO₃ bilayer.
>
> Two things would help enormously:
>
> **(a) The numerical data behind Fig. 2(b):**
> 1. the numerical points of the plotted dispersion curves (wavenumber–frequency pairs, in the panel's
>    normalisation);
> 2. the lower and upper edges of the plotted stop bands (normalised frequency);
> 3. the first four branch frequencies at a stated normalised wavenumber (two values would be ideal);
> 4. the exact parameter set used for that figure (both materials' ρ, c₃₃, layer thicknesses / cell
>    size, and the length-scale values l, l₁ for each layer), with units.
>
> **(b) One definitional clarification, on which the comparison depends:** the Fig. 2(b) panel annotates
> "l = 1e-5" (no units, no overbar), while the text defines a barred length scale. Could you confirm,
> **for that specific figure**: (i) whether the plotted case uses the **dimensional** l (in metres) or the
> **normalised** l̄; (ii) if normalised, **which length** is used for the normalisation (cell size,
> layer thickness, or other) and its numerical value for the figure; (iii) the corresponding convention
> for l₁ and its relation to l; and (iv) the material-coefficient convention in which l enters (e.g.
> whether μ₀ = c₃₃ l² is used).
>
> Machine-readable files are ideal (CSV, TXT, XLSX/XLS, MAT, JSON or equivalent), and plain numeric
> values with units stated are also fine. **I am not requesting any source code** — only the published
> figure's numerical values and this definitional point.
>
> The aim is reproducibility of your published result; without the l / l̄ clarification I cannot define
> the comparison unambiguously, which is the only reason I am asking. Thank you for considering this.
>
> With best regards,
> [PI name, affiliation, contact]

---

## 3. Request B3 — Li et al., *Waves in Random and Complex Media* **36**(4):5715–5735 (2023), Fig. 4(c)

**Subject:** Request for the numerical data underlying Fig. 4(c) of *Waves in Random and Complex Media* 36(4):5715–5735 (2023) — for independent validation

**Recipient:** `[publisher-listed corresponding author channel, as the article publishes no
data-availability statement]`

> Dear Dr. Li and co-authors,
>
> I am independently implementing the dipolar-gradient SH-wave dispersion problem for periodic layered
> composites and would like to validate against **Fig. 4(c)** of your *Waves in Random and Complex Media*
> 36(4):5715–5735 (2023) article — the gradient-elasticity panel compared with the earlier literature
> (thermoelastic coupling omitted), for the Pb/brass bilayer.
>
> If it is available, could you share:
>
> 1. the **numerical points** underlying the Fig. 4(c) curves (wavenumber–frequency pairs, first two
>    acoustic–optical branches, in the panel's normalisation);
> 2. the **band-gap edges** of the first gaps in that panel (normalised frequency);
> 3. the **non-dimensional coefficients actually used for that panel** — the values of c̄₁ and d̄₁ and
>    their ratios (and the τ_R value if relevant) — together with the definitions of c̄ and d̄, in
>    particular which length scale (a₁ or other) normalises them. (The panel itself annotates no
>    coefficient values, so this is essential for a defined comparison; I have been using the Fig. 3(b)
>    values c̄₁ = 0.15, d̄₁ = 0.25, c_R = d_R = 1.5 — please confirm whether those are the values behind
>    Fig. 4(c), or state the ones that are.)
> 4. the **material and geometric parameters** for the Pb and brass layers used in that figure (μ, ρ,
>    layer thicknesses), with units;
> 5. the **normalisation definitions** used for the panel's axes.
>
> Any machine-readable format is acceptable — CSV, TXT, XLSX/XLS, MAT, JSON or similar. **No source code
> or unpublished material is needed** — only the numerical values behind the published figure.
>
> The purpose is reproducibility of the published benchmark: the data would let me compare my
> independent calculation numerically, report the differences honestly, and cite your work accurately
> for the convention followed. Thank you for your consideration.
>
> With best regards,
> [PI name, affiliation, contact]

---

## 4. Acceptance protocol (what happens after data is received — no thresholds changed)

Applies identically to B1/B2/B3; artefacts are prepared in
`paper9/audit/author_data/B{1,2,3}_DATA_RECEIPT_TEMPLATE.md`.

1. **Author data received** → record sender, date, file name(s) and SHA-256; archive the received file
   unmodified under `paper9/audit/author_data/`; never edit the received bytes.
2. **Provenance verification** → confirm the data correspond to the named figure/panel; record the
   provider's attribution and any stated caveats.
3. **Parameter / normalisation verification** → check the supplied parameter set and normalisation
   against the published text and against the repository's recorded interpretation. **For B2 the data
   may not be used until the `l` vs `l̄` question is explicitly resolved** — an unresolved answer keeps
   B2 blocked regardless of data quality.
4. **Independent solver run** → run the existing solver configuration with the author-stated parameters
   only; no tuning, no fitting, no parameter search; archive the output JSON under `paper9/results/raw/`.
5. **Numerical point comparison** → compare the requested quantities pairwise: the curves' numerical
   points, the **band-gap edges**, and the **first four branch frequencies at the stated normalised
   wavenumber**.
6. **Benchmark error calculation** → relative error per quantity and the maximum relative error, computed
   only from the author-supplied numbers (never from digitised curves).
7. **Criterion** → the existing PCR1/G3 threshold: **≤ 2 % mandatory for all quantities**; the
   **≤ 0.5 % classical-limit target applies to B1** where applicable. No threshold is changed, added or
   relaxed.
8. **Evidence artifact** → completed receipt template, solver output, comparison table, and the
   updated `benchmark_evidence.json` entry (`quantitative_error` filled only from computed numbers;
   status changed only if the criterion is met).
9. **PCR1 reassessment** → PCR1 is re-evaluated **only** if all three mandatory benchmarks (B1, B2, B3)
   are closed with computed errors meeting the criterion; a partial closure changes no status.
10. **G3 reassessment** → G3 additionally requires its completeness conditions (full error table,
    per-benchmark PASS/FAIL, main-manuscript evidence, Layer 2c executed). G4 then remains a PI act
    after PCR1–PCR8 are checked. **Receipt of data alone closes nothing.**

**Independence note (governance safety):** author data can move only the PCR1 → G3 → G4 chain. It
cannot resolve **P5** (internal parallel-pipeline reconciliation) or **R-1** (pipeline-level
reproducibility), and it does not touch **PCR5** (already PASS) or the governing numerical baseline.

**Status while data is outstanding (locked):** PCR1 NOT PASS · G3 NOT MET · G4 NOT MET · P5 NOT
PASS/OPEN · R-1 OPEN · PCR5 PASS · **P13 BLOCKED**.
