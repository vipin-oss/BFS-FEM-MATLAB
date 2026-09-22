# TV11 — LWZ2016 source record (P2.6)

**Status:** OPEN (equation-level evidence insufficient for the intended validation role).
**Date:** 2026-09-22 (acquisition pass after `53b9ccc`)

## 1. Source identity — bibliographic **[C]** (publisher metadata)

| Field | Value | Tag |
|---|---|---|
| Title | Band gaps of elastic waves in 1-D phononic crystal with dipolar gradient elasticity | **[C]** Springer |
| Authors | Yueqiu Li, Peijun Wei, Yahong Zhou | **[C]** |
| Journal | *Acta Mechanica* | **[C]** |
| Volume / pages | **227**:1005–1023 | **[C]** |
| Online date | 15 December 2015 (volume year 2016) | **[C]** |
| DOI | [10.1007/s00707-015-1495-z](https://doi.org/10.1007/s00707-015-1495-z) | **[C]** |
| OA | `isAccessibleForFree: false` (publisher JSON-LD) | **[C]** |

Plan card **B6**. Bibliographic identity is confirmed. **That does not close TV11.**

## 2. Acquisition log (this pass)

| Attempt | Result |
|---|---|
| Local `paper9/` | no PDF |
| Springer article HTML | abstract + references; subscription preview |
| Unpaywall `v2/10.1007/s00707-015-1495-z` | no OA location returned |
| ResearchGate landing | abstract / snippets, not a complete equation set |
| Circumvention copies | **not used** |

**Full paper / publisher PDF: not obtained.**

## 3. Abstract-level formulation **[C]** (Springer abstract)

- 1-D **periodic laminated** cell of **two different** gradient elastic solids.
- Homogeneous gradient solid: dispersive **P** and **SV** plus **two evanescent** waves (interface P-type / S-type).
- Continuity: displacement, **normal derivative of displacement**, **monopolar and dipolar tractions**.
- Cell **transfer matrix** of a state vector; **Bloch** theorem → dispersion equation (solved **numerically** in the paper).
- In-plane and anti-plane; oblique and normal incidence.
- Two microstructure parameters per solid (plan language `c1`, `d1` and ratios) — **definitions not transcribed from PDF**.

## 4. Equation-level items — **not verified**

| Check | Result |
|---|---|
| Governing constitutive equations | **not in hand** |
| Exact TM matrix entries | **not in hand** |
| Exact Bloch/determinant equation | **not in hand** (abstract: numerical solution of a dispersion equation) |
| Homogeneous infinite-medium closed form like Case-H | **not claimed by the abstract**; problem is a **PC**, not homogeneous |
| Numerical parameter tables | **not in hand** |

## 5. Validation relevance (no Case-H claim)

| Our model | Transferability | Tag |
|---|---|---|
| Present 2-D anisotropic Case-H (homogeneous `L(θ)`) | **not transferable** as a validation source | **[C] different problem** |
| Future 1-D Case-C bilayer TM (P3 B6) | **method-class related** (TM + 4 interface conditions) **if** PDF supplies equations | **[B]** pending PDF |
| Layer-3b machine-precision closed form | **not obtained** | TV11 OPEN |

**Do not label LWZ2016 as validation of the present anisotropic 2-D Case-H model.**

**Evaluator of LWZ2016 closed form: not written.**

## Action to close TV11

Place a lawful full-text PDF under `paper9/analytic/lwz2016/` and transcribe the TM/Bloch equation plus constitutive `c1`,`d1`. Until then **TV11 stays OPEN**.
