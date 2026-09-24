# P12AC — Final literature-resolution pass: candidate classification and **Decision B** for B2/B3

**Phase:** P12AC (final scientific literature-resolution pass; opened after P12AB closed at `5093c58…`).
**Nature of this record:** it closes the search for a *published* replacement/augmentation of the two external
benchmarks **B2** (Layer 2a) and **B3** (Layer 2b). It changes **no** gate, threshold, validation route,
Blueprint text, manuscript byte, numerical result or benchmark status.

**Constraints honoured.** One bounded literature resolution only (repository-held sources + one bounded
external query); no author contact and no author-data request; no Blueprint v1.5 / PCR1 / G3 / G4 / Rule R-fit
modification; every candidate classified explicitly; no forced matching; no parameter tuning or visual
best-fit; no percentage asserted where the source supports only graphical comparison; `l` is not assumed to
equal `l̄`.

---

## 1. What was searched

Repository-held literature (`paper9/sources/`, `paper9/analytic/`), the analytic PDFs held for the two
anchors, and one bounded external query for published dipolar-gradient / strain-gradient 1-D phononic-crystal
band-structure benchmarks with an explicitly stated parameter set and normalisation. The repository-held set
is the complete set available to this project: the two benchmark anchors, LWZ2016, PB2009, and the remaining
inventory entries.

---

## 2. Candidate classification (exact reason per candidate)

| Candidate | Role tested | Classification | Exact reason |
|---|---|---|---|
| **Li et al. 2024**, *Sci. Rep.*, `s41598-024-75049-1.pdf` (B1/B2 anchor) | replacement for **B2** | **NOT COMPATIBLE** (as a replacement) | it *is* the incumbent B2 anchor: the paper supplies the compared figure but no machine-readable dispersion data and no resolvable definition/units of the plotted length scale (`l` dimensional vs the normalised `l̄ := l/b` of its Eq. (55)); a source cannot replace itself, and its own information is exactly what is insufficient |
| **Li et al. 2023**, *Waves Random Complex Media*, doi 10.1080/17455030.2023.2222189 (B3 anchor) | replacement for **B3** | **NOT COMPATIBLE** (as a replacement) | same reason: it is the incumbent B3 anchor; its Fig. 4(c) caption states no parameter values and no normalisation, and no numerical curve data are published |
| **LWZ2016** — Y. Li, P. Wei, Y. Zhou, *Acta Mech.* **227**:1005–1023 (2016), doi 10.1007/s00707-015-1495-z (`paper9/analytic/lwz2016/li2015.pdf`) | augmentation/replacement for **B3** (same dipolar-gradient family) | **SUPPORTING ONLY** | the *formulation* is now verified source-equivalent (see §3: printed Appendix 3 ≡ first-principles derivation ≡ repository implementation, ≤ 3.6e-15; the paper's own dispersion relation (14.1) reproduced on a homogeneous cell, ≤ 1.4e-15), **but** its published Fig. 3 (`ξ̄ = 0`) stop-band edges are **not reproducible** from the caption's stated gradient parameter set under the source-conforming formulation (§4), so the figure does not satisfy the Layer-2 benchmark definition (parameter set + normalisation + independently reproducible dispersion quantity) |
| **PB2009** — Papargyri-Beskou et al. 2009 (`paper9/analytic/pb2009/papargyri-beskou2009.pdf`) | replacement for **B2**/**B3** | **NOT COMPATIBLE** | different constitutive reduction from the anchors (`g² := l²/10, h² := ℓ²` versus LWZ2016's `c := l²/10, d²/3 := ℓ²`), i.e. a different length-scale mapping, and it supplies no bilayer Bloch dispersion benchmark with an explicit parameter set. Remains usable as a supporting analytic/formulation check only |
| **Mishra, Kumar & Sharma 2026**, *Acta Mech.* 237:3951–3982, `s00707-026-04680-y.pdf` (project Anchor C) | replacement for **B2**/**B3** | **NOT COMPATIBLE** | a different formulation and object: "tunable wave propagation and band gap characteristics in **functionally graded lattices** with multiple topologies via dynamic stiffness and Floquet–Bloch formulation" — no dipolar-gradient constitutive reduction, no micro-stiffness/micro-inertia length-scale mapping, so the Layer-2 benchmark definition (same/equivalent gradient-elastic bilayer formulation) is not met. Remains the project's Anchor C |
| **Zheng & Wei 2009** (`zheng2009.pdf`, *Int. J. Miner. Metall. Mater.* 16(5):608) | replacement for **B2**/**B3** | **NOT COMPATIBLE** | 1-D bilayer Bloch-transmission benchmark but in **classical** elasticity with imperfect interfaces (traction/displacement jumps); no gradient length scales at all, so it cannot carry the B2/B3 quantity. Usable only as a supporting classical-limit reference |
| **Zhan & Wei 2010** (`zhan2010.pdf`, *Acta Mech. Solida Sin.* 23(2)) | replacement for **B2**/**B3** | **NOT COMPATIBLE** | different dimensionality and formulation: influence of **anisotropy** on band gaps of **2-D** phononic crystals; not a 1-D dipolar-gradient bilayer dispersion benchmark |
| `hosseini2021.pdf` | replacement for **B2**/**B3** | **NOT COMPATIBLE** | content mismatch: the file contains an unrelated humanities article (1999 *Revista de Letras*), not a mechanics paper (P11 inventory finding, re-confirmed here) |
| `s10773-022-05163-1.pdf` | replacement for **B2**/**B3** | **NOT COMPATIBLE** | content mismatch: the file contains "Two Classes of Quantum Synchronizable Codes" (*Int. J. Theor. Phys.*), not a phononic-crystal paper (P11 inventory finding, re-confirmed here) |
| Bounded external query | new published candidate | **none found** | no published source with the same dipolar-gradient bilayer formulation, an explicitly stated parameter set/normalisation and a reproducible dispersion curve surfaced; the field is confined to the sources already held |

**Outcome: no admissible ACCEPTABLE replacement or augmentation exists, for B2 or for B3.** The search is
closed permanently (§6).

---

## 3. LWZ2016 formulation verification (the one substantive positive result)

Three independent objects were compared at five `(ω, c, d, μ, ρ)` points, including both material sets:

* **(A) printed Appendix 3** — transcribed from the PDF text layer (normal propagation, Bloch SH wave,
  `r = s`, `ε = μ`, including the `1/(σ² + τ²)` prefactor);
* **(B) first principles** — propagator `M(a)M(0)⁻¹` with `u = A cos σx + B sin σx + C cosh τx + D sinh τx`,
  `P = μ[(1−m)u′ + c u′′′]`, `R = μ c u″`, `m = ω²d²/(3V²)` from Eqs. (12)–(14) and (41.1)–(41.4);
* **(C) repository solver** — `paper9/validation/b6_lwz_tm/lwz_tm_sh_normal.py::layer_T_sh_normal`.

| comparison | maximum discrepancy over the tested points |
|---|---|
| printed Appendix 3 − repository solver | **3.6e-15** |
| printed Appendix 3 − first principles | **3.6e-15** |
| first principles − repository solver | **1.8e-15** |

Homogeneous-cell check of the paper's own dispersion relation (14.1)
(`ω² = σ²V²(1 + cσ²)/(1 + d²σ²/3)`), `σa` versus the Bloch angle of the layer matrix:
**maximum relative residual 1.4e-15** over `σ = 0.5, 1.5, 3.0` for two parameter sets.

**Retraction.** The earlier note in this project's P12AB-family working record that *"the repository
implementation does not reproduce the matrix printed in Appendix 3"* is **superseded**. The recorded
mismatch (0.12 – 0.90; rows 3 differing) came from a defective hand-reconstruction, not from the
implementation: no member of a 96-member transcription/convention family reproduces the row that the earlier
reconstruction used, while the direct PDF-text transcription and an independent first-principles derivation
both reproduce the implementation to ≤ 3.6e-15. Reproducible evidence:
`paper9/audit/evidence/p12ac/lwz_tm_equivalence_check.py` and its output
`paper9/audit/evidence/p12ac/lwz_tm_equivalence_results.json`.

**What this positive result does and does not establish.** It establishes that the repository's anti-plane
dipolar-gradient layer solver is a faithful implementation of the LWZ2016 formulation as printed. It is
*internal/framework consistency* between a source and an implementation of that source; it is **not**
validation of the repository against an independent experiment, and it does **not** validate B2 or B3.

---

## 4. Why LWZ2016 Fig. 3 cannot be admitted as a benchmark

With the source-conforming formulation and the parameter set printed with Fig. 3
(`c̄1 = 0.5`, `c̄ = 0.77`, `d̄1 = 0.5`, `d̄ = 2`, `a1/a = 0.5`, Fig. 2 material set), the cell band edges are
(vertical axis `ωa/2πv_m`, `v_m = 0.7458456136`):

```
computed stop bands (y)   : [0.6675, 0.6937]   [1.2946, 2.2617]   [2.6098, …]
digitised grey bands (y)  : [0.6036, 0.6627]   [0.8718, 1.1637]   [1.3136, 1.7120]
```

The digitisation is a **registration aid only** (the same frame calibration reproduces the analytic classical
Fig. 2 edges to ≤ 0.010 in `y`); no percentage error is derived from it and none is claimed. Even so, the
discrepancy is structural, not marginal: the computed structure has **no** stop band in `[0.87, 1.16]` at all,
and the remaining intervals do not coincide.

A bounded convention-variant family was evaluated with the same solver (no variant adopted, no fit):

| variant | stop bands (y) |
|---|---|
| as read | 0.6675–0.6937 · 1.2946–2.2617 · 2.6098–… |
| `c̄` direction reversed | 0.5576–0.6627 · 1.0919–2.2155 · 2.4811–… |
| `d̄` direction reversed | 0.5142–0.6464 · 0.9781–1.3995 · 1.6174–1.9039 · … |
| layers swapped | identical to "as read" (the cell matrices are similar, so layer order **cannot** explain the difference) |
| `c̄1`, `d̄1` in layer units | 0.3885–0.9056 · 1.3056–2.0153 · 2.5642–… |
| micro-inertia `m = ω²d²/V²` (non-source-conforming) | 0.4505–0.6285 · 0.8162–1.3841 · 1.5659–2.5972 · … |

No **source-conforming** variant reproduces the three digitised stop bands. The residual is therefore
**source-side** (the parameter values or normalisation actually used for that panel are not the ones the
caption/parameter list states, or are not recoverable from the published text), **not** an implementation
defect — the implementation has just been shown to reproduce the source's own printed matrix and dispersion
relation to machine precision. Because the source provides neither the actual plotted parameter set nor
machine-readable curve data, LWZ2016 Fig. 3 fails the Layer-2 benchmark definition: it is
**SUPPORTING ONLY**.

---

## 5. Formal decision

> **Decision B.** *B2/B3 remain source-limited and NOT_VALIDATED because the published sources do not
> provide sufficient authoritative parameter/curve information.*
>
> This is a property of the published record, **not** a solver defect: the solver involved has been
> verified against the source's own printed formulation to machine precision (§3), and the residual
> benchmark mismatch is structural in the source's published information (§4).
>
> It is recorded, in addition, that the search for a *published* replacement or augmentation of B2 or B3
> (quantitative or graphical) is **closed permanently**. No further benchmark-hunting phase is authorised by
> this record.

Consequences, effective immediately and without any gate change:

1. **B2** stays `NOT_VALIDATED` — ambiguity unreconciled (`l` versus `l̄`), quantitative route impossible
   (no machine-readable source data), graphical route not admissible (plotted parameter set/length-scale
   definition not resolvable from the source);
2. **B3** stays `NOT_VALIDATED` (`quantitative_error` NULL); its formulation status is
   `ESTABLISHED / SOURCE-EQUIVALENT` and that status does **not** constitute validation;
3. no percentage, error bar or "agreement" number may be attached to either benchmark;
4. the previously prepared author-data route (P12M drafts / P12L spec, **NOT SENT**, **NOT AUTHORISED**)
   is not withdrawn by this decision, but it is **no longer required for any scientific reason created by
   the benchmark search**: no published source can substitute for it, and its absence is now a documented,
   permanent limitation rather than an open-ended search.

---

## 6. Path-forward determinations (no gate lowered)

**(a) Can PCR1 be satisfied with the remaining admissible evidence? — No.**
PCR1 item 1 requires *every* mandatory published benchmark (Layers 1, 2a, 2b) to be validated by one of the
two admissible routes. B1 satisfies its item by the labelled graphical route; **B2 and B3 satisfy neither**
route, and Decision B records that no published source can make them do so. PCR1 therefore remains
`NOT PASS`, item 1 being the sole failing item; items 2–8 are unaffected.

**(b) Manuscript limitation statement (exact text, to be inserted only under separate authorisation — the
manuscript is not edited here):**

> *External benchmark coverage.* The two external dispersion benchmarks used to support the band-structure
> discussion (Layer 2a, reference [B2]; Layer 2b, reference [B3]) are compared against the graphical
> information published in their source articles. Neither source provides numerical curve data, and the
> parameter and normalisation information published with the relevant figures is insufficient to reproduce
> them independently: for Layer 2a the definition and units of the length-scale parameter are ambiguous as
> published, and for Layer 2b the parameter set and normalisation of the published dispersion figure are not
> stated. These two benchmarks are therefore reported as **not validated**, and the corresponding
> verification gate is **not** claimed as met. No numerical agreement value is claimed for either benchmark;
> the Layer 1 comparison is graphical only, for the same reason (no machine-readable source data). The
> gradient-elasticity formulation implemented here has been verified against the formulation printed in the
> source that defines it to machine precision (≤ 4 × 10⁻¹⁵ on the transfer matrix and the dispersion
> relation); this is a formulation-consistency check and not a validation of the two benchmarks.

**(c) Can P5 proceed with B2/B3 explicitly marked NOT_VALIDATED? — Yes.**
P5 is the production-highlights gate. It is not downstream of B2/B3: the dependency chain is
`B2/B3 → PCR1 → G3 → G4`, and P5 is a parallel, independently gated item whose blocker is the internal
production-record reconciliation decision (authorisation), not external benchmark data. Conditions: B2/B3
must remain explicitly marked `NOT_VALIDATED` in every artefact that carries a status table; no P5 artefact
may imply benchmark validation; and any manuscript use accompanies the limitation statement of (b).

**(d) Are R-1 and C-1 independent of the B2/B3 blocker? — Yes, genuinely independent — but they are
governance-gated, not science-gated.**
*R-1* concerns the pipeline-level reproducibility of the governing production artefact (an internal
numerical property of the deployed configuration), and *C-1* concerns promotion of the already-validated 5i
criterion predicate set (an internal governance decision). Neither consumes PCR1's quantity, neither is
reachable by any external benchmark, and Decision B therefore neither helps nor hinders them. They are not
"leftovers" of the B2/B3 blocker: they remain open for their own, separately recorded reasons, and closing
them requires the corresponding explicitly authorised internal action.

**(e) Can P13 proceed after an explicitly authorised internal decision without lowering any gate? — Yes, in
principle, and Decision B is what makes this the only remaining route.**
Conditions, all of which must hold in the same authorised decision:
(i) the decision is recorded as an internal governance act; (ii) B2/B3 stay `NOT_VALIDATED` in every active
artefact and PCR1, G3, G4 stay `NOT PASS` / `NOT MET` — a submission decision must not restate them as met;
(iii) the limitation statement (b) is carried by the manuscript and no unvalidated benchmark is presented as
validated; (iv) the P5 record is reconciled or left explicitly open; (v) R-1 and C-1 are either decided or
left explicitly open; (vi) no threshold, route, gate definition or numerical result changes.
Decision B **does not itself** start P13 and **does not** authorise submission: it removes the expectation
that author-supplied data would arrive for these benchmarks, so that P13 no longer has to wait on an external
route that may never close.

---

## 7. What this phase did **not** change

Blueprint v1.5 (`b96c8e76…`), Blueprint v1.4 (`2ae0b1e8…`), Rule R-fit (`d4fed492…`), the active
`benchmark_validation_record.json` (`2fad2d92…`), the traceability register (CSV `8d86528f…`, JSON
`83ff8723…`), the manuscript (`paper9/latex/`, set hash `5ba2c22e…`), all production/results artefacts, all
source PDFs and all historical audit records are **byte-unchanged**. No gate status, threshold, validation
route, number or manuscript byte moved. The author-data request material remains **NOT SENT** and
**NOT AUTHORISED**.

## 8. Files added by this phase

| File | Purpose |
|---|---|
| `paper9/audit/P12AC_LITERATURE_RESOLUTION_DECISION_B.md` | this record |
| `paper9/audit/evidence/p12ac/lwz_tm_equivalence_check.py` | rerunnable equivalence / Fig. 3 evidence |
| `paper9/audit/evidence/p12ac/lwz_tm_equivalence_results.json` | machine-readable evidence output |
| `paper9/verification/suite/test_p12ac_decision_b.py` | guard: Decision B, classification, retraction and frozen-hash invariants |
| `paper9/audit/RECOVERY_CHECKPOINT_P12AC.md` | pre-work + final recovery checkpoint |
