# TV10 — PB2009 source record (P2.5)

**Status:** OPEN (equation-level evidence insufficient).
**Date:** 2026-09-22 (acquisition pass after `53b9ccc`)
**Rule:** transcribe only from the source paper; do not invent Eqs (22)–(28); do not close TV10 from secondary citations.

## Blueprint bibliographic claim

Papargyri-Beskou & Beskos (2009), *Int. J. Solids Struct.* **46**:2151–2159, Eqs (22)–(28).
Plan card **B5** / A5: infinite medium + axial bar, parameters `g²`, `h²`.

## 1. Source identity — bibliographic **[C]** of the *intended* paper (publisher metadata)

From ScienceDirect / DOI landing (HTML, not PDF):

| Field | Value | Tag |
|---|---|---|
| Title | Wave dispersion in gradient elastic solids and structures: A unified treatment | **[C]** publisher |
| Authors | S. Papargyri-Beskou, **D. Polyzos**, D. E. Beskos | **[C]** publisher |
| Journal | *International Journal of Solids and Structures* | **[C]** |
| Volume / issue | **46**(21) | **[C]** |
| Pages | **3751–3759** | **[C]** |
| Date | 15 October 2009 | **[C]** |
| DOI | [10.1016/j.ijsolstr.2009.05.002](https://doi.org/10.1016/j.ijsolstr.2009.05.002) | **[C]** |
| PII | S0020768309001966 | **[C]** |

Blueprint pages **2151–2159** and two-author cite: **[C] mismatch**. *IJSS* 46(20) occupies 3505–3750; 2151–2159 is not this article.

Bibliographic identity of the *intended* paper is confirmed. **That does not close TV10.**

## 2. Acquisition log (this pass)

| Attempt | Result |
|---|---|
| Local `paper9/analytic/pb2009/`, `paper9/bib/` | no PDF |
| `https://doi.org/10.1016/j.ijsolstr.2009.05.002` | Elsevier linking hub HTML; full text not served |
| ScienceDirect article HTML | abstract + keywords; no equation bodies |
| Unpaywall `v2/10.1016/j.ijsolstr.2009.05.002` | no OA location returned |
| arXiv search for this title | no preprint of *this* paper |

**Full paper / publisher PDF: not obtained.** Secondary papers that *cite* PB2009 (e.g. Gortsas–Aggelis–Polyzos arXiv:2210.09642) are **not** used as a substitute for Eqs (22)–(28).

## 3. Abstract-level statements **[C]** (publisher abstract only)

Analytical wave studies in: infinite space; axial bar; Bernoulli–Euler beam; Kirchhoff plate. Simple gradient elasticity with **micro-elastic** and **micro-inertia** characteristics. Micro-elastic terms alone are stated to be insufficient for realistic dispersion; micro-inertia is needed.

## 4. Equations (22)–(28) — **not verified**

| Check | Result |
|---|---|
| Exact bodies of (22)–(28) | **not available** |
| Definitions of `g²`, `h²` (constitutive vs inertia, tensor vs scalar) | **not available from PDF** |
| Surrounding model assumptions | **not available from PDF** |
| Whether (22) is infinite-space dispersion | **not verified from PDF**. Publisher HTML *snippets* (previous P2 pass) *mention* Eq. (22) as P/S phase velocities vs `k` with `g²`,`h²`; that snippet is **not** a transcription of the equation |
| Closed form usable for Layer-3 machine precision | **not obtained** |
| Restriction `g ≤ h` | **not verified from PDF**. Prior HTML snippet mentioned it; **not** treated as **[C]** equation-level |

## 5. Mapping `g² ↔ l²/10`, `h² ↔ ℓ²`

| Verdict | Tag |
|---|---|
| Source-supported **exact** mapping | **no** — source equations not in hand |
| Source-supported after a stated specialisation | **no** — would require their constitutive reduction in the PDF |
| Merely analogous (candidate) | **[B] candidate only**, unused numerically |
| Unsupported as identification | **yes, as identification** |

Our Case-H (M10.2) remains **[A]**. Anisotropic `L` (`l1≠l2`, `θ`) is **not** attributed to PB2009.

**Evaluator of PB2009 (22)–(28): not written.**

## Action to close TV10

Place a lawful full-text PDF (pp. 3751–3759) under `paper9/analytic/pb2009/` and transcribe (22)–(28) with definitions. Until then **TV10 stays OPEN**.
