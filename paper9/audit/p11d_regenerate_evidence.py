"""P11D single-dataset regeneration (remediation item 5; P12A corrections).

Regenerates, FROM ONE AUTHORITATIVE RUN SET (never hand-edited):
  * paper9/audit/benchmark_evidence.json   (B1 fresh run; B2 from the gap
    registry CFG-DIM-MICRO; B3 from pinned run P11D-B3-R1; B5 freshness
    re-run in P12A; explicit provenance note)
  * paper9/tables/out/tab03_anchor_errors.tex (cells derived from the same data)
  * paper9/audit/evidence/fig4c_overlay.png  (honest QUALITATIVE GRAPHICAL
    COMPARISON: the GENUINE published Fig. 4 raster beside the present
    calculation; panel (c) is the B3 comparison target)

P12A SOURCE-FIGURE CORRECTION (2026-09-23): the raster previously used as
"Fig. 4(c)" (paper9/audit/evidence/fig4c_raw.png, three panels annotated
tau_R = 1 / 0.1 / 0.05) is pixel-identical to FIGURE 7 of Li et al. (2023)
(gradient THERMO-elastic model), not Figure 4(c).  The genuine Figure 4
(PDF printed page 15, embedded image of size 1500x437, in-repo as
paper9/audit/evidence/li2023_p15_img1_Im1.png) has panel (c) titled
"Gradient elasticity" (present vs Li and Wei [34]); it carries no
tau_R sweep and no c_bar/d_bar annotation.  The tau_R sweep belongs to the
source's Figure 7.  This correction changes no number: no trace overlay and
no error metric were or are possible or claimed; the c_bar/d_bar provenance
[S] (inherited from Fig. 3(b)) is unchanged.

Usage: python3 paper9/audit/p11d_regenerate_evidence.py
"""
from __future__ import annotations

import datetime
import json
import os
import subprocess
import sys

import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO_ROOT)
sys.path.insert(0, os.path.join(REPO_ROOT, "paper9"))

from paper9.validation.b1_b2_b3_solver import BenchmarkB1, BenchmarkB3  # noqa: E402

REGISTRY = os.path.join(REPO_ROOT, "paper9", "results", "raw", "p11d_b2_gap_registry.json")
B3_PIN = os.path.join(REPO_ROOT, "paper9", "results", "raw", "p11d_b3_run_P11D-B3-R1.json")
EVIDENCE = os.path.join(REPO_ROOT, "paper9", "audit", "benchmark_evidence.json")
TAB03 = os.path.join(REPO_ROOT, "paper9", "tables", "out", "tab03_anchor_errors.tex")
FIG4C = os.path.join(REPO_ROOT, "paper9", "audit", "evidence", "fig4c_overlay.png")
# P12A: the genuine Li et al. (2023) FIGURE 4 raster (PDF printed page 15,
# embedded image 1500x437), verified pixel-identical to the source PDF
# (dict xref 394).  The old FIG4C_RAW file (fig4c_raw.png) is the
# source's FIGURE 7 (tau_R sweep), mislabelled pre-P12A; it is retained
# on disk as historical evidence with an identification note beside it.
FIG4C_RAW = os.path.join(REPO_ROOT, "paper9", "audit", "evidence", "fig4c_raw.png")
FIG4_TRUE = os.path.join(REPO_ROOT, "paper9", "audit", "evidence", "li2023_p15_img1_Im1.png")


def fmt_sci(x: float) -> str:
    m, e = f"{x:.2e}".split("e")
    return f"${m} \\times 10^{{{int(e)}}}$"


def regen_evidence(reg, pin):
    b1 = BenchmarkB1()
    l1 = b1.run_level1_homogeneous()
    l2 = b1.run_level2_identical_reduction()
    het1 = b1.compute_heterogeneous_dispersion()
    b1_gaps = [list(g) for g in het1["band_gaps"][:3]]

    micro = reg["configs"]["CFG-DIM-MICRO"]
    b2_gaps3 = [[round(g[0], 3), round(g[1], 3), round(g[2], 3)] for g in micro["scan"]["gaps"]]
    all_cfgs = {k: {"label": v["label"], "l_bar_A": v["params"]["l_bar_A"],
                    "a_A_m": v["params"]["a_A_m"],
                    "level1_status": v["level1_homogeneous"]["status"],
                    "gaps": v["scan"]["gaps"]} for k, v in reg["configs"].items()}

    doc = {
        "metadata": {
            "title": "Machine-Readable Benchmark Evidence Registry",
            "date": datetime.date.today().isoformat(),
            "governing_document": "Paper9 Blueprint v1.3",
            "policy_rule": "Curve digitization is permitted ONLY to draw overlay "
                           "figures, NEVER to compute solver-error percentages. "
                           "If author raw numerical tables are unreleased, benchmark "
                           "status is formally GRAPHICAL_ONLY / PARTIAL.",
            "regenerated_by": "paper9/audit/p11d_regenerate_evidence.py (P11D; "
                              "single authoritative dataset -- no hand-edited numbers)",
            "regenerated_from": [
                "paper9/results/raw/p11d_b2_gap_registry.json (CFG-DIM-MICRO)",
                "paper9/results/raw/p11d_b3_run_P11D-B3-R1.json",
                "BenchmarkB1().run_level1/2/heterogeneous (fresh deterministic run)",
            ],
        },
        "benchmarks": {
            "B1": {
                "benchmark_id": "B1",
                "source": "Li et al., Scientific Reports 14:24035 (2024)",
                "doi": "10.1038/s41598-024-75049-1",
                "figure": "Fig. 2(a)",
                "parameter_source": "Li et al. (2024) 'Numerical results and discussions' "
                            "narrative (the paper contains NO tables; P12A citation "
                            "correction: pre-P12A text said 'Section 4.1 text & Table 1')",
                "reference_data_type": "GRAPH_ONLY (Analytical Rytov verified)",
                "reference_data_available": False,
                "solver_data_available": True,
                "comparison_type": "QUALITATIVE_GRAPHICAL_COMPARISON",
                "quantitative_error_allowed": False,
                "quantitative_error": None,
                "level1_homogeneous_error": l1["max_error"],
                "level1_status": l1["status"],
                "level2_identical_reduction_error": l2["max_error"],
                "level2_status": l2["status"],
                "band_gaps_computed": b1_gaps,
                "graphical_overlay": "paper9/audit/evidence/fig2a_analytical_overlay.png",
                "graphical_overlay_note": "P11B-era qualitative raster comparison "
                                          "(digitized display only; no error metric)",
                "status": "PARTIAL / GRAPHICAL_ONLY",
                "blocking_reason": "Original authors published graphic curves only; "
                                   "no numerical floating-point eigenvalue tables released.",
            },
            "B2": {
                "benchmark_id": "B2",
                "source": "Li et al., Scientific Reports 14:24035 (2024)",
                "doi": "10.1038/s41598-024-75049-1",
                "figure": "Fig. 2(b) (f=0, F=0)",
                "parameter_source": "Fig. 2(b) caption & Section 4.1 -- l / l_bar "
                                    "AMBIGUOUS in the source (micro-scale figure axes "
                                    "vs 1 cm macro text); three labelled "
                                    "interpretations run separately",
                "parameter_semantics": reg["parameter_semantics"],
                "reference_data_type": "GRAPH_ONLY",
                "reference_data_available": False,
                "solver_data_available": True,
                "comparison_type": "QUALITATIVE_GRAPHICAL_COMPARISON",
                "quantitative_error_allowed": False,
                "quantitative_error": None,
                "authoritative_dataset": "paper9/results/raw/p11d_b2_gap_registry.json"
                                        " (config CFG-DIM-MICRO, adaptive-precision "
                                        "z-test engine)",
                "level1_homogeneous_error": micro["level1_homogeneous"]["max_error"],
                "level1_status": micro["level1_homogeneous"]["status"],
                "level2_identical_reduction_error": micro["level2_identical_reduction"]["max_error"],
                "level2_status": micro["level2_identical_reduction"]["status"],
                "band_gaps_computed": b2_gaps3,
                "band_gaps_units": "w_bar = omega/omega_0, 3 dp, exact z-test edges "
                                   "(bisection 1e-6); full-precision values in the registry",
                "interpretation_runs": all_cfgs,
                "graphical_overlay": "paper9/audit/evidence/fig2b_tm_overlay.png",
                "graphical_overlay_note": "P11B-era raster underlay + unaligned scatter; "
                                          "retained as historical audit evidence only",
                "status": "NOT_VALIDATED / GRAPHICAL_ONLY (l/l_bar AMBIGUITY)",
                "blocking_reason": "Original authors published graphic curves only; "
                                   "no numerical tables released; source l / l_bar "
                                   "parameterization is internally inconsistent "
                                   "(dimensional ambiguity preserved, not resolved).",
            },
            "B3": {
                "benchmark_id": "B3",
                "source": "Li et al., Waves in Random and Complex Media 36(4):5715-5735 (2023)",
                "doi": "10.1080/17455030.2023.2222189",
                "figure": "Fig. 4(c)",
                "parameter_source": "c_bar_1 = 0.15, d_bar_1 = 0.25, c_R = d_R = 1.5 are "
                                    "Li et al. (2023) Fig. 3(b) values; the Fig. 4(c) panel "
                                    "(gradient elasticity, comparison with literature [34], "
                                    "thermoelastic coupling ignored) annotates NO c_bar/d_bar "
                                    "values -- the tau_R sweep belongs to the source's Fig. 7, "
                                    "not Fig. 4(c) (P12A source-figure identification "
                                    "correction) -- provenance [S] (inherited), never [C]",
                "reference_data_type": "GRAPH_ONLY",
                "reference_data_available": False,
                "solver_data_available": True,
                "comparison_type": "QUALITATIVE_GRAPHICAL_COMPARISON",
                "quantitative_error_allowed": False,
                "quantitative_error": None,
                "pinned_run": "paper9/results/raw/p11d_b3_run_P11D-B3-R1.json "
                              f"(run_id {pin['run_id']}, N_points=720)",
                "level1_homogeneous_error": pin["level1_homogeneous"]["max_error"],
                "level1_status": pin["level1_homogeneous"]["status"],
                "level2_identical_reduction_error": pin["level2_identical_reduction"]["max_error"],
                "level2_status": pin["level2_identical_reduction"]["status"],
                "band_gaps_computed": pin["band_gaps_3dp"],
                "graphical_overlay": "paper9/audit/evidence/fig4c_overlay.png",
                "graphical_overlay_note": "P12A-corrected qualitative graphical comparison: "
                                          "the GENUINE published Fig. 4 raster (panel (c) = "
                                          "gradient elasticity vs Li and Wei [34]) beside the "
                                          "present calculation. The pre-P12A overlay embedded "
                                          "the source's Fig. 7 (tau_R sweep) mislabelled as "
                                          "Fig. 4(c); corrected 2026-09-23. NOT a trace overlay "
                                          "-- the source figure provides no extractable values "
                                          "for this parameter set; no error metric is computed.",
                "status": "GRAPHICAL_ONLY / PARTIAL",
                "blocking_reason": "Original authors published graphic curves only; "
                                   "no numerical floating-point eigenvalue tables released.",
            },
            "B5": {
                "benchmark_id": "B5",
                "source": "Papargyri-Beskou & Beskos (2009)",
                "reference_data_type": "SOURCE_EQUATIONS",
                "quantitative_error_allowed": True,
                "quantitative_error": "< 1e-15 (reported)",
                "provenance_note": "freshness re-run in P12A (2026-09-23): new execution of "
                                   "paper9/validation/L3/p3_layer3_pb2009.py reproduced "
                                   "11/11 PASS with max rel err 5.466e-16 (< 1e-15 claim "
                                   "intact); deterministic closed-form identities. "
                                   "Pre-P12A note: carried from Phase-1 pipeline; not "
                                   "regenerated in P11D (outside remediation scope)",
                "status": "PASS / SOURCE_EQUATIONS",
            },
        },
    }
    with open(EVIDENCE, "w") as f:
        json.dump(doc, f, indent=2)
    return doc


def regen_tab03(doc):
    b1 = doc["benchmarks"]["B1"]
    b2 = doc["benchmarks"]["B2"]
    b3 = doc["benchmarks"]["B3"]
    b1_gap = b1["band_gaps_computed"][0]
    b2_gap = b2["band_gaps_computed"][0]
    b3_gap = b3["band_gaps_computed"][0]
    tex = r"""\begin{table*}[t]
\centering
\caption{Validation summary and quantitative error metrics for external literature benchmarks (B1--B3, B5). Level~1/Level~2 errors and computed gap~1 intervals are regenerated from the single authoritative runs (B2: \texttt{p11d\_b2\_gap\_registry.json}, config CFG-DIM-MICRO, exact $z$-test edges; B3: pinned run P11D-B3-R1). In compliance with the evidence hierarchy, quantitative solver error against published curves is marked N/A (Graphical Only) rather than manufactured from pixel digitization.}
\label{tab:anchor_errors}
\footnotesize
\renewcommand{\arraystretch}{1.2}
\begin{tabular}{lp{3.2cm}p{2.8cm}cccp{2.5cm}c}
\hline\hline
\textbf{Benchmark} & \textbf{Physical System} & \textbf{Published Anchor} & \textbf{Level 1 Err.}$^a$ & \textbf{Level 2 Err.}$^b$ & \textbf{Comp. Gap 1} & \textbf{Ref. Data Type} & \textbf{Status} \\
\hline
\textbf{B1} & 1D Classical Bilayer (AlN / $\mathrm{BaTiO_3}$) & Li et al.\ (2024) \cite{li2024anchorB}, Fig.~2(a); Zheng \& Wei \cite{zhengwei2009} & """ + fmt_sci(b1["level1_homogeneous_error"]) + r" & " + fmt_sci(b1["level2_identical_reduction_error"]) + r" & $[" + f"{b1_gap[0]:.3f}, {b1_gap[1]:.3f}" + r"]$ & GRAPH\_ONLY / EQN$^c$ & PARTIAL \\" + r"""
\textbf{B2} & 1D Gradient Bilayer (AlN / $\mathrm{BaTiO_3}$, flexo off) & Li et al.\ (2024) \cite{li2024anchorB}, Fig.~2(b) ($f=0, F=0$) & """ + fmt_sci(b2["level1_homogeneous_error"]) + r" & " + fmt_sci(b2["level2_identical_reduction_error"]) + r" & $[" + f"{b2_gap[0]:.3f}, {b2_gap[1]:.3f}" + r"]$ & GRAPH\_ONLY$^d$ & NOT VALIDATED$^e$ \\" + r"""
\textbf{B3} & 1D Dipolar Gradient Bilayer (Pb / Brass, SH wave) & Li et al.\ (2023) \cite{li2023anchorA}, Fig.~4(c)$^f$; LWZ (2016) \cite{liweizhou2016} & """ + fmt_sci(b3["level1_homogeneous_error"]) + r" & " + fmt_sci(b3["level2_identical_reduction_error"]) + r" & $[" + f"{b3_gap[0]:.3f}, {b3_gap[1]:.3f}" + r"]$ & GRAPH\_ONLY$^d$ & PARTIAL \\" + r"""
\textbf{B5} & Micro-beam Pure Bending (Papargyri-Beskou limit) & Papargyri-Beskou \& Beskos \cite{papargyribeskou2009}, Eqs.~(22)--(28) & $< 10^{-15}$ & $< 10^{-15}$ & N/A & SOURCE\_EQUATIONS & PASS \\
\hline\hline
\end{tabular}
\begin{flushleft}
\scriptsize
$^a$ Level~1 homogeneous test: relative error in multi-cell composition identity $\mathbf{T}(a)\mathbf{T}(a) = \mathbf{T}(2a)$ and exact bulk wavenumber.\\
$^b$ Level~2 identical-material reduction: algebraic recovery of bulk acoustic dispersion when Layer~B material properties approach Layer~A.\\
$^c$ Rytov exact dispersion formula verified to $< 10^{-15}$; qualitative graphical comparison confirmed against Fig.~2(a); original authors published no numerical tables.\\
$^d$ Heterogeneous bilayer transfer-matrix dispersion solved numerically; qualitative graphical comparison only; quantitative percentage error withheld per evidence hierarchy because author raw floating-point eigenvalue tables are unreleased.\\
$^e$ B2 is NOT externally validated: the source $l/\bar{l}$ parameterization is dimensionally ambiguous (three labelled interpretations run separately; see \texttt{p11d\_b2\_gap\_registry.json}).\\
$^f$ The Fig.~4(c) panel (gradient elasticity, comparison with literature~\cite{liweizhou2016}, thermoelastic coupling ignored) annotates no $\bar{c}/\bar{d}$ values; the source's $\tau_R$ sweep belongs to its Fig.~7, not Fig.~4(c) (source-figure identification corrected 2026-09-23); the evaluated $\bar{c}/\bar{d}$ are inherited from Fig.~3(b) (provenance [S], not author-specified Fig.~4(c) parameters).
\end{flushleft}
\end{table*}
"""
    with open(TAB03, "w") as f:
        f.write(tex)


def regen_fig4c_overlay(pin):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import image as mpimg

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.2, 4.6), constrained_layout=True)
    img = mpimg.imread(FIG4_TRUE)
    # the genuine Fig. 4 raster is 8-bit grayscale (PIL mode L); render it in
    # grayscale, never through the default false-colour map (P12A fix)
    axL.imshow(img, cmap="gray")  # mpimg normalizes uint8 PNG to float [0, 1]
    axL.set_axis_off()
    axL.set_title("Source figure: Li et al. (2023) Fig. 4 as published\n"
                  "(panel (c) = gradient elasticity vs Li and Wei [34]\n"
                  "is the B3 target; no $\\bar{c}/\\bar{d}$ annotation; no tables;\n"
                  "the $\\tau_R$ sweep belongs to the source's Fig. 7)", fontsize=10)

    b3 = BenchmarkB3()
    omegas = np.linspace(0.01, 3.6, 720)
    pts = []
    for w_bar in omegas:
        w = w_bar * b3.omega_0
        TA, _, _ = b3.layer_T_sh(w, b3.a_1, b3.c_1, b3.d_1, b3.mu_1, b3.rho_1)
        TB, _, _ = b3.layer_T_sh(w, b3.a_2, b3.c_2, b3.d_2, b3.mu_2, b3.rho_2)
        for ev in np.linalg.eigvals(TB @ TA):
            if abs(abs(ev) - 1.0) < 0.02:
                pts.append((abs(np.angle(ev)) / np.pi, w_bar))
    pts = np.array(pts)
    if len(pts):
        axR.scatter(pts[:, 0], pts[:, 1], s=3, color="crimson",
                    label="Present calculation (run P11D-B3-R1)")
    for idx, (w_lo, w_hi, width) in enumerate(pin["band_gaps_4dp"][:3]):
        axR.axhspan(w_lo, w_hi, color="mistyrose", alpha=0.45,
                    label="Present stop bands" if idx == 0 else None)
    axR.set_xlim(0.0, 1.0)
    axR.set_ylim(0.0, 6.0)
    axR.set_xlabel(r"normalized Bloch wavenumber $\bar{k}$ (half-zone $[0,\pi]$, mirrored)")
    axR.set_ylabel(r"normalized frequency $\bar{\omega}$")
    axR.set_title("Present calculation: 1D dipolar TM (SH),\n"
                  r"$\bar{c}_1/\bar{d}_1$ inherited from Fig. 3(b) [S]", fontsize=10)
    axR.grid(True, ls=":", alpha=0.6)
    axR.legend(loc="upper right", fontsize=8, framealpha=0.9)

    fig.suptitle("QUALITATIVE GRAPHICAL COMPARISON ONLY -- not a trace overlay; "
                 "source values not extractable for this parameter set; "
                 "no error metric computed", fontsize=11)
    fig.savefig(FIG4C, dpi=200)
    plt.close(fig)


def main():
    with open(REGISTRY) as f:
        reg = json.load(f)
    with open(B3_PIN) as f:
        pin = json.load(f)
    if not pin.get("manuscript_values_reproduced"):
        raise SystemExit("B3 pin does not reproduce manuscript values -- abort")
    doc = regen_evidence(reg, pin)
    regen_tab03(doc)
    regen_fig4c_overlay(pin)
    print("regenerated:", EVIDENCE)
    print("regenerated:", TAB03)
    print("regenerated:", FIG4C)
    b2 = doc["benchmarks"]["B2"]
    print("B2 authoritative gaps (3dp):", b2["band_gaps_computed"])


if __name__ == "__main__":
    main()
