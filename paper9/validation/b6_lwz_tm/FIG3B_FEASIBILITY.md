# LWZ2016 Fig. 3(b) quantitative comparison — feasibility

**Verdict: BLOCKED** (not PASS). No quantitative comparison against Fig. 3(b) was performed.

Governing PDF: `paper9/analytic/lwz2016/li2015.pdf` (Li, Wei & Zhou, *Acta Mech.* **227**:1005–1023, 2016).  
TM code unchanged: `paper9/validation/b6_lwz_tm/`. L1 vs (14.1) and L2 identical-layer results **not** modified.

## What Fig. 3 actually is (PDF p.10 caption, extracted)

> Fig. 3 The dispersive curves and band gaps of anti-plane Bloch waves in the periodic structure consisting of the gradient elastic solids (\(\bar c_1=0.5\), \(\bar c=0.77\), \(\bar d_1=0.5\), \(\bar d=2\)). **Left** in the normal propagation situation (\(\bar\xi=0\)); **right** in the oblique propagation situation (\(\bar\xi\neq 0\)); **middle** the change of upper and lower band edge.

The extracted caption **does not** letter the panels as (a)/(b)/(c). The body text never writes “Fig. 3(b)”. A three-panel Left / middle / right figure is therefore **not uniquely identified** as one curve.

| If 3(b) means | Quantity | Extra source gap |
|---|---|---|
| Left | \(\omega(k)\) SH, \(\bar\xi=0\) | Graph only; no table |
| Middle | upper/lower **band edges vs** \(\bar\xi\) | Graph only; \(\bar\xi\) axis undocumented in text |
| Right | \(\omega(k)\) SH, **oblique** | \(\bar\xi\neq 0\) **with no numerical \(\bar\xi\)** |

## Numerical information in the source

**Present (text, p.10):**

- Axes for the left/right dispersion plots: horizontal \(ka/\pi\) in the first Brillouin zone; vertical \(\omega a/(2\pi v_m)\) with \(v_m=a/(a_1/V_{sA}+a_2/V_{sB})\).
- **No** printed axis *limits* (min/max of \(ka/\pi\) or \(\omega a/2\pi v_m\)).
- Parameter set for Fig. 3: \(\bar c_1=\sqrt{c_1}/a=0.5\), \(\bar d_1=d_1/a=0.5\), \(\bar c=c_1/c_2=0.77\), \(\bar d=d_1/d_2=2\), plus the section-6 defaults \(V_{p1}/V_{s1}=2.6621\), \(V_{p2}/V_{p1}=0.562\), \(V_{s2}/V_{s1}=0.5947\), \(\rho_2/\rho_1=0.1573\), \(a_1/a=0.5\).
- \(\bar\xi=0\) for the left (normal) panel only.

**Absent (full PDF, 19 pages, no `Table` objects):**

- No tabulated \(\omega(k)\) or \((ka/\pi,\,\omega a/2\pi v_m)\) points.
- No printed band-edge frequencies.
- No numerical \(\bar\xi\) for the **right** panel (only \(\bar\xi\neq 0\)).
- No numeric tick lists.

## Existing B6 TM vs Fig. 3 barred definitions

Implementation uses the **same barred identities as the PDF** (not reinterpreted):

- \(\bar c_1=\sqrt{c_1}/a=0.5\) ⇒ \(c_1=(0.5 a)^2\)
- \(\bar d_1=d_1/a=0.5\) ⇒ \(d_1=0.5 a\)
- \(\bar c=c_1/c_2=0.77\), \(\bar d=d_1/d_2=2\)
- \(a_1/a=0.5\), \(V_{s2}/V_{s1}=0.5947\), \(\rho_2/\rho_1=0.1573\)

The TM is **SH, normal incidence** (\(\xi=0\)), Appendix 3. That matches the **left** panel’s physics class, **not** the middle (band edge vs \(\xi\)) or right (oblique, \(\xi\) unknown). L2 already **scanned** that left-panel parameter set; those \(\omega\) values are **solver output**, not paper numbers.

## Why a defensible % comparison is not possible

Project rule: digitisation is overlay-only and is **not** an error metric. Without tabulated \(\omega(k)\), any “relative discrepancy vs Fig. 3(b)” would be digitiser uncertainty, not a solver test.

Oblique / middle-panel comparison would also need a **different** TM (\(\xi\neq 0\)). That solver is **not** built here.

## Comparison actually obtained

**None vs Fig. 3(b).** No points were read off the figure. No relative errors vs the paper are reported.

Unchanged prior evidence (not Fig. 3): L1 vs closed form (14.1) max rel \(k=1.429\times 10^{-14}\); L2 identical-layer \(4.441\times 10^{-16}\).

## B6 completeness

**Partial.** Independent TM + L1/L2 self-consistency **done**. Fig. 3(b) published-curve gate **BLOCKED**. PCR1/G3 unchanged.
