#!/usr/bin/env python3
"""
paper9/tables/gen/tab03_anchor_errors.py
Generates Table 2: Literature Benchmark Verification & Error Metrics (tab03_anchor_errors.tex).
Strictly complies with Paper9 Blueprint v1.3/v1.5 and zero-fabrication forensic standards:
  - Exact equations, parameters, and boundary conditions documented.
  - Level 1 (Homogeneous identity) & Level 2 (Identical-material reduction) errors reported.
  - Level 2 (Heterogeneous bilayer) computed band edges reported.
  - Reference data types explicitly classified (AUTHOR_TABLE, SOURCE_EQUATIONS, GRAPH_ONLY).
  - No synthetic error percentages manufactured from visual curve matching.
  - Explicit footnotes documenting absence of published floating-point eigenvalue tables.

Template provenance (P12AG, 2026-09-24):
  This template is the P12AF-authorised content of the table - the A2 re-tiering recorded in
  paper9/audit/P12AF_MANUSCRIPT_RETIERING_RECORD.md (B1 GRAPHICAL_VALIDATION / PASS, B2/B3
  NOT VALIDATED, footnote g, footnote c/d re-tiers, the governing B2 numerical values) - with the
  P12AG layout correction (tabularx column specification, zero-width break opportunities inside the
  long underscore identifiers).  It replaces a stale template that would have regenerated the
  pre-P12AF wording and pre-remediation B2 values.  Regenerating this table can no longer revert an
  audited scientific record; test_p12ag_clean_build.py asserts byte-identity with the committed file.
"""
from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = REPO_ROOT / "paper9" / "tables" / "out"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TEX_CONTENT = r"""\begin{table*}[t]
\centering
\caption{Validation summary and quantitative error metrics for external literature benchmarks (B1--B3, B5). Level~1/Level~2 errors and computed gap~1 intervals are regenerated from the single authoritative runs (B2: \texttt{p11d\_b2\_gap\_registry.json}, config CFG-DIM-MICRO, exact $z$-test edges; B3: pinned run P11D-B3-R1). In compliance with the evidence hierarchy (Blueprint v1.5 \S13, amendment A2), quantitative solver error against published curves is marked N/A rather than manufactured from pixel digitization, and no percentage is asserted for any graphically compared benchmark.}
\label{tab:anchor_errors}
\footnotesize
\renewcommand{\arraystretch}{1.2}
\setlength{\tabcolsep}{2pt}
\begin{tabularx}{\textwidth}{@{}l >{\raggedright\arraybackslash}X >{\raggedright\arraybackslash}X ccc >{\raggedright\arraybackslash}p{2.0cm} >{\raggedright\arraybackslash}p{2.4cm}@{}}
\hline\hline
\textbf{Benchmark} & \textbf{Physical System} & \textbf{Published Anchor} & \textbf{Level 1 Err.}$^a$ & \textbf{Level 2 Err.}$^b$ & \textbf{Comp. Gap 1} & \textbf{Ref. Data Type} & \textbf{Status} \\
\hline
\textbf{B1} & 1D Classical Bilayer (AlN / $\mathrm{BaTiO_3}$) & Li et al.\ (2024) \cite{li2024anchorB}, Fig.~2(a); Zheng \& Wei \cite{zhengwei2009} & $6.47 \times 10^{-16}$ & $7.22 \times 10^{-16}$ & $[0.481, 0.521]$ & GRAPH\_\hspace{0pt}ONLY / EQN$^c$ & GRAPHICAL\_\hspace{0pt}VALIDATION / PASS \\
\textbf{B2} & 1D Gradient Bilayer (AlN / $\mathrm{BaTiO_3}$, flexo off) & Li et al.\ (2024) \cite{li2024anchorB}, Fig.~2(b) ($f=0, F=0$) & $4.10 \times 10^{-57}$ & $4.10 \times 10^{-57}$ & $[0.078, 0.242]$ & GRAPH\_\hspace{0pt}ONLY$^d$ & NOT VALIDATED$^e$ \\
\textbf{B3} & 1D Dipolar Gradient Bilayer (Pb / Brass, SH wave) & Li et al.\ (2023) \cite{li2023anchorA}, Fig.~4(c)$^f$; LWZ (2016) \cite{liweizhou2016} & $1.37 \times 10^{-13}$ & $4.19 \times 10^{-14}$ & $[0.340, 1.024]$ & GRAPH\_\hspace{0pt}ONLY$^d$ & NOT VALIDATED$^g$ \\
\textbf{B5} & Micro-beam Pure Bending (Papargyri-Beskou limit) & Papargyri-Beskou \& Beskos \cite{papargyribeskou2009}, Eqs.~(22)--(28) & $< 10^{-15}$ & $< 10^{-15}$ & N/A & SOURCE\_\hspace{0pt}EQUATIONS & PASS \\
\hline\hline
\end{tabularx}
\begin{flushleft}
\scriptsize
$^a$ Level~1 homogeneous test: relative error in multi-cell composition identity $\mathbf{T}(a)\mathbf{T}(a) = \mathbf{T}(2a)$ and exact bulk wavenumber.\\
$^b$ Level~2 identical-material reduction: algebraic recovery of bulk acoustic dispersion when Layer~B material properties approach Layer~A.\\
$^c$ Rytov exact dispersion formula verified to $< 10^{-15}$; graphical comparison confirmed against Fig.~2(a) under the labelled graphical route (A2), with no percentage asserted; original authors published no numerical tables.\\
$^d$ Heterogeneous bilayer transfer-matrix dispersion solved numerically; raster comparison for audit only; NOT validated (published parameter/normalisation information insufficient); quantitative percentage error withheld per the evidence hierarchy because author raw floating-point eigenvalue tables are unreleased.\\
$^e$ B2 is NOT externally validated: the source $l/\bar{l}$ parameterization is dimensionally ambiguous (three labelled interpretations run separately; see \texttt{p11d\_b2\_gap\_registry.json}).\\
$^f$ The Fig.~4(c) panel (gradient elasticity, comparison with literature~\cite{liweizhou2016}, thermoelastic coupling ignored) annotates no $\bar{c}/\bar{d}$ values; the source's $\tau_R$ sweep belongs to its Fig.~7, not Fig.~4(c) (source-figure identification corrected 2026-09-23); the evaluated $\bar{c}/\bar{d}$ are inherited from Fig.~3(b) (provenance [S], not author-specified Fig.~4(c) parameters).\\
$^g$ B3 is NOT externally validated: the source publishes no numerical curve data and the Fig.~4(c) parameter set/normalisation is not stated; the reproduction is formulation-equivalent to the source's own Appendix~3 form to machine precision, but that is a formulation-consistency finding, not a validation; no agreement value or percentage is claimed for B3.\\
\end{flushleft}
\end{table*}
"""


def generate_table3():
    out_file = OUT_DIR / "tab03_anchor_errors.tex"
    with open(out_file, "w") as f:
        f.write(TEX_CONTENT)
    print(f"Generated Table 2: {out_file}")


if __name__ == "__main__":
    generate_table3()
