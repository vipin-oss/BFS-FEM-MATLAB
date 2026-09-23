# P3 source-resolution pass (no solver)

**Date:** 2026-09-22  
**HEAD in:** `2467737e5bfce55f7b987850778c4d9afd131055`  
**PDFs:** `paper9/analytic/li2024/s41598-024-75049-1.pdf`, `paper9/analytic/li2023/17455030.2023.2222189.pdf`

**At this pass (HEAD `2467737`):** no TM/FE. PCR1/G3 not claimed. P4A untouched. TV10/TV11/Blueprint untouched.

**Later (B6):** SH-normal TM exists; Fig. 3 quantitative still **BLOCKED**; B6 **PARTIAL**; PCR1/G3 **NOT PASS**. See `validation/b6_lwz_tm/FIG3B_FEASIBILITY.md`.

---

## B2 — `l` in Fig. 2(b)

**Ambiguity remains OPEN.** The 2024 PDF does not state that Fig. 2(b) `l=10^{-5}` is `\bar l`.

### Evidence [C]

1. **Dimensional definitions** (PDF p.7, art. p.7): `l`, `l1`, `f` appear in (54) with thicknesses `a_A`, `a_B`. Then  
   `\bar l = l/b`, `\bar l_1 = l_1/b`, `\bar f = f/(b^2 ω_0 √(ρ a_3))`, `L = l'/l`, `L_1 = l'_1/l_1`, `F = f'/f`, `b = a_A+a_B` (51).

2. **Fig. 2 caption** (PDF p.9): unbarred  
   `(l=10^{-5}, l_1=2×10^{-5}, f=0, L=5, L_1=5, F=0)`.  
   Same unbarred `l,l_1,f` in Figs. 3–5 captions (PDF pp.10–12). Equation (55) *does* write `\bar l, \bar l_1, \bar f`.

3. **Mixed symbols in one caption:** `L,L_1,F` exist in the paper *only* as the ratios `l'/l` etc. (already dimensionless). `l,l_1,f` exist both dimensionally (54) and as barred copies (55). The caption never prints `\bar l`.

4. **Fig. 3** title: “influence of micro-stiffness length scale parameter **l**” with `l_1,f,L,L_1,F` held fixed — still unbarred `l`, no statement “here l means \bar l”.

### What is *not* done

No choice between (a) dimensional `l=10^{-5}` m ⇒ `\bar l = 10^{-5}/0.02 = 5×10^{-4}` and (b) caption already `\bar l`.  
**B2 not run.** Plan `l̄=1e-5` is **not** adopted as [C].

---

## B3 TV1 — Fig. 4(c) `c̄1, c_R, d̄1, d_R`

**TV1 remains OPEN.**

Fig. 4(c) caption (PDF p.15 / 5728): “the dispersion curves for the gradient elastic solids and the comparison with literature **[34]**.”  
Body: dipolar gradient solids, thermoelastic coupling ignored; consistence with **[34] = Li & Wei, Acta Mech. 227:1005–1023 (2016)** (PDF p.20).

**No numerical `c̄1, c_R, d̄1, d_R` (or `c1,d1`) appear in the Fig. 4 caption or in the two paragraphs on Fig. 4.**

Fig. 3(b) values (`c̄1=0.15, c_R=1.5, d̄1=0.25, d_R=1.5`, thermal 0) stay **Fig. 3(b) / TV8 only**. The paper does **not** say they apply to Fig. 4(c).  
LWZ2016 Fig. 3 (`c̄1=0.5,…`) is **not** copied into TV1.

Missing for TV1: the exact microstructure set used to generate Fig. 4(c) (present-model curve and/or the [34] overlay).

---

## B3 TV12 — Fig. 4(c) axes / sampling

**TV12 remains OPEN.**

Stated [C]:

- Horizontal: Bloch wavenumber, nondim `\bar k = k a_1/π` (p.14).
- Vertical: `\bar ω = ω/ω_0` (p.14).
- Vertical propagation for Fig. 3; Fig. 4 is a literature comparison (incidence not restated for 4(c)).

**Not stated:** x-limits, y-limits, tick spacing, number of k-samples, truncation.  
Record: **sampling not specified in source.** No visual estimate.

---

## B3 parameter consistency (shared numerical example, PDF p.14 / 5727) — [C]

| item | PDF |
|---|---|
| A / B | lead / brass |
| a1 | 10^{-5} m |
| a_R | 1 (a1=a2) |
| ρ1 | 7.5×10^3 kg/m³ |
| μ1 | 2.3×10^{10} Pa |
| ω0 | 4.1×10^8 Hz (also formula on p.14) |
| λ_R, μ_R, ρ_R | 0.047, 0.056, 0.157 |
| k̄ | k a1 / π |
| Fig. 4(c) thermal | ignored (body p.15) |
| Fig. 4(c) vs [34] | comparison with LWZ2016; **not** identified with Fig. 3(b) parameter set |

These constants **do not** close TV1.

---

## TV register

| ID | Status after this pass |
|---|---|
| TV2 | CLOSED (2024 eq. 51) — no contradiction found |
| TV8 | CLOSED (Fig. 3 captions) — not extended to Fig. 4(c) |
| TV1 | **OPEN** — Fig. 4(c) microstructure numbers absent |
| TV12 | **OPEN** — limits/sampling not in source |
| B2 `l` vs `\bar l` | **OPEN** (notation, not a TV-ID in the plan; recorded here) |

---

## P11D addendum (2026-09-23) — TV1 retag [C] -> [S]; B2 l/l-bar ambiguity status

This addendum supersedes the TV register above for TV1 only; the historical
record is preserved unchanged.

**TV1 is CLOSED with provenance [S] (inherited / source-derived), NOT [C].**
Finding: the Li et al. (2023) Fig. 4(c) panel sweeps the relaxation parameter
tau_R and annotates **no** c_bar/d_bar values (P11C finding CF-5).  The
evaluated set (c_bar_1 = 0.15, c_R = 1.5, d_bar_1 = 0.25, d_R = 1.5) is
stated in the Section 4.2 shared-example text and the **Fig. 3(b) caption**
and is *inherited* into the Fig. 4(c) computation.  Per the Blueprint v1.3
provenance tags this is [S] (source-derived/design inheritance): the values
are traceable to the source but are **not author-specified Fig. 4(c)
parameters**.  Any text describing them as [C] Fig. 4(c) parameters is
incorrect.  Fig. 4(c) numerical source data remain unreleased
(GRAPH_ONLY): the pinned evaluation is paper9/results/raw/p11d_b3_run_P11D-B3-R1.json
and the honest graphical comparison is
paper9/audit/evidence/fig4c_overlay.png (qualitative graphical comparison
only; not a trace overlay; no error metric).

**B2 `l` vs `bar l` remains OPEN (ambiguity preserved).**  P11D ran the three
defensible interpretations separately and labelled them
(paper9/results/raw/p11d_b2_gap_registry.json):
CFG-DIM-MICRO (dimensional micro scale -- the published-axis
configuration and the authoritative stop-band dataset),
CFG-DIM-MACRO (source 1 cm width with dimensional l), and
CFG-BAR-MACRO (barred reading l = l_bar * a).  The source remains
internally inconsistent (micro-scale figure axes vs macro-scale text);
B2 is **not externally validated**.

| ID | Status after P11D |
|---|---|
| TV1 | **CLOSED [S]** -- inherited from Fig. 3(b)/Sec. 4.2; Fig. 4(c) annotates no c_bar/d_bar |
| TV12 | OPEN (unchanged) |
| B2 `l` vs `bar l` | **OPEN** (ambiguity preserved; three labelled interpretation runs) |

---

## P12A ADDENDUM (2026-09-23) — source-figure identification correction

**P12A forensic finding (verified by byte-level raster comparison against the
source PDF embedded images, PyMuPDF):** the archived raster
`paper9/audit/evidence/fig4c_raw.png` (three panels annotated tau_R = 1,
0.1, 0.05) is **pixel-identical (mean |diff| = 0.0000) to Figure 7 of
Li et al. (2023)** ("The influence of thermal relaxation time ratio tau_R …
in the case of gradient **thermo-elastic** model"), printed page 16 —
**not to Figure 4(c)**.  The genuine Figure 4 (printed page 15, embedded
image 1500×437, in-repo as `paper9/audit/evidence/li2023_p15_img1_Im1.png`)
has panel (c) titled **"Gradient elasticity"** (present-model curves vs
literature [34] = Li, Wei & Zhou 2016, thermoelastic coupling ignored),
carries **no tau_R sweep**, and — as previously established — annotates
**no** c_bar/d_bar values (re-verified from the PDF text layer).

Consequences (corrections applied in P12A, history preserved):

1. The sentence in the P11D addendum above, "the Li et al. (2023) Fig. 4(c)
   panel sweeps the relaxation parameter tau_R", is **factually wrong** and
   is superseded by this addendum.  The tau_R sweep belongs to the source's
   **Figure 7**, which is a gradient *thermo-elastic* figure and can never
   be the comparison target of the isothermal B3 evaluation.
2. Identical wrong statements in `sec05_verification.tex` (B3 item and Fig. 4
   caption), `tab03_anchor_errors.tex` footnote f, `traceability_matrix.json`
   TV1, `benchmark_evidence.json` B3 `parameter_source`, and the two
   generator scripts were corrected and regenerated registry-first
   (see `paper9/audit/P12A_CLOSEOUT.md`).  Historical P11/P11D audit
   documents are preserved unmodified; this addendum is the record.
3. **What survives unchanged:** the TV1 verdict itself.  TV1 stays
   **CLOSED [S]**: Fig. 4(c)'s caption annotates no c_bar/d_bar
   (re-verified), so the evaluated c_bar_1 = 0.15, c_R = 1.5, d_bar_1 = 0.25,
   d_R = 1.5 remain **inherited from Fig. 3(b)** (source-derived/design,
   Blueprint tag [S]) and must never be described as author-specified
   Fig. 4(c) parameters ([C]).  The pinned run P11D-B3-R1 and all B3 numbers
   are unaffected.  Only the *rationale sentence* and the overlay basis were
   wrong and are corrected.
4. `fig4c_overlay.png` was regenerated with the genuine Fig. 4 raster beside
   the present calculation (still qualitative graphical only; no error
   metric; no trace overlay).  The mislabelled raster is retained on disk
   with `paper9/audit/evidence/fig4c_raw_IS_FIGURE7.md` documenting its
   true identity.

| ID | Status after P12A |
|---|---|
| TV1 | **CLOSED [S]** (unchanged verdict; rationale corrected — tau_R sweep is source Fig. 7, not Fig. 4(c)) |
| TV12 | OPEN (unchanged) |
| B2 `l` vs `bar l` | **OPEN** (unchanged; ambiguity preserved; P12A additionally verified the source defines l_bar = l/b with b = a_A + a_B = 0.02 m, not l/a) |
