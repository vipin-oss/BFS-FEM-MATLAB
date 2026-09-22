# TV11 — LWZ2016 source record (P2.6)

**Status:** OPEN. No original PDF in `paper9/`.
**Date:** 2026-09-22

## Bibliographic identity — **[C]** confirmed at abstract level

Li, Y., Wei, P. J., Zhou, Y. H. (2016). Band gaps of elastic waves in 1-D phononic crystal with dipolar gradient elasticity. *Acta Mechanica* **227**:1005–1023.
DOI [10.1007/s00707-015-1495-z](https://doi.org/10.1007/s00707-015-1495-z).
Plan card **B6**.

## What the Springer abstract states (transcribed as facts, not formulas)

- Periodic **laminated** structure: two different **gradient elastic** solids, repeating 1-D cell.
- Modes in a homogeneous gradient solid: dispersive **P** and **SV**, plus **two evanescent** waves that become P-type and S-type **interface** waves.
- Interface continuity: displacement, **normal derivative of displacement**, **monopolar and dipolar tractions** (four conditions — matches our M8 interface count).
- **Transfer matrix** of the state vector on a typical cell; **Bloch** theorem → dispersion equation.
- In-plane and anti-plane Bloch waves; oblique and normal incidence.
- Two microstructure parameters of each gradient solid (plan language: `c1`, `d1` and ratios); numerical parametric study.

## What is **not** transcribed

No closed-form `det(T − e^{i k b} I) = 0` matrix entries, no constitutive `c1`/`d1` definitions, no numerical parameter table, no band-gap numbers.

## Classification vs our model

| Comparison | Tag |
|---|---|
| Homogeneous infinite-medium Case-H closed form (M10.2) | **[C] different problem** — LWZ is a **periodic bilayer**, not homogeneous |
| 1-D Case-C dipolar-gradient TM (future P3 B3/B6) | **[B] method-class related** (TM + 4 interface conditions) pending PDF |
| Exact closed form + parameters for Layer 3b machine precision | **TV11 OPEN** |

**Evaluator of LWZ2016 closed form: not written.**
