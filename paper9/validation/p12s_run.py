#!/usr/bin/env python3
"""P12S — run the B1/B2/B3 graphical-validation reproductions and build the validation record.

Route decisions are made from the forensic source facts (Phase A) and the reproduction
outcomes (Phase C); they are never tuned to reach a PASS.  No percentage is ever derived
from an overlay: ``quantitative_error`` remains NULL for every benchmark.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
for _p in (str(HERE), str(REPO_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import p12s_panels as P
import p12s_reproduce as R2

WORK = R2.WORK


def sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ------------------------------------------------------------------ B2 evidence figure
def b2_evidence(panels: dict) -> dict:
    """Published panel (b) vs three labelled interpretations of the caption."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from paper9.validation.b2_stable_tm import StableB2

    ref_x, ref_y = R2.digitise_reference("B2", panels)
    p = panels["B2"]

    # (i) source-stated geometry: the gradient correction is far below figure resolution,
    #     so the reproduction is the classical solution at the same geometry; its band
    #     edges are confirmed by the adaptive-precision engine (recorded below).
    sb = StableB2("CFG-DIM-MACRO")
    wbar, kbar, prop, gaps_macro, w0 = R2.b1_dispersion(n_w=3000)

    # (ii) micro-geometry reading (a = 1e-5 m): qualitatively different structure
    micro = R2.b2_dispersion(1e-5, n_w=700, use_barred=False)

    # (iii) barred reading (l = l_bar*b): required precision, i.e. feasibility
    sb_bar = StableB2("CFG-BAR-MACRO")
    dps_bar = sb_bar.required_dps()

    fig, axes = plt.subplots(1, 3, figsize=(16.5, 4.8), dpi=150)
    axes[0].imshow(p["panel"], cmap="gray", extent=[-1, 1, 0, 2], aspect="auto")
    axes[0].plot(ref_x, ref_y, ".", ms=1.0, color="#1f77b4", alpha=0.6)
    axes[0].set_title("published panel (b): gradient elasticity\n(caption: l = 1e-5, l1 = 2e-5, L = L1 = 5)",
                      fontsize=9)

    ax = axes[1]
    ax.plot(ref_x, ref_y, ".", ms=1.0, color="#1f77b4", alpha=0.45,
            label="published Fig. 2(b) (digitised)")
    for sign in (1, -1):
        ax.plot(sign * kbar, wbar, lw=1.3, color="#d62728",
                label="reproduction, source geometry a=0.01 m" if sign > 0 else None)
    for g in gaps_macro:
        ax.axhline(g[0], color="#2ca02c", lw=0.6, ls=":")
    ax.set_title("interpretation (i): source-stated geometry a = 0.01 m\n"
                 "reproduction collapses onto the classical curve (gradient correction O(1e-6))",
                 fontsize=9)
    ax.set_xlim(-1.02, 1.02); ax.set_ylim(-0.02, 2.05)
    ax.set_xlabel(r"$\bar k$"); ax.set_ylabel(r"$\bar\omega$"); ax.grid(alpha=0.25)
    ax.legend(loc="lower right", fontsize=6)

    ax = axes[2]
    ax.plot(ref_x, ref_y, ".", ms=1.0, color="#1f77b4", alpha=0.45,
            label="published Fig. 2(b) (digitised)")
    for sign in (1, -1):
        ax.plot(sign * micro["kbar"], micro["wbar"], lw=1.2, color="#9467bd",
                label="reproduction, a = l = 1e-5 m (micro)" if sign > 0 else None)
    ax.set_title("interpretation (ii)/(iii): a = 1e-5 m (micro) — different band/gap structure;\n"
                 f"barred reading infeasible (adaptive precision {dps_bar:.0f} digits)",
                 fontsize=9)
    ax.set_xlim(-1.02, 1.02); ax.set_ylim(-0.02, 2.05)
    ax.set_xlabel(r"$\bar k$"); ax.set_ylabel(r"$\bar\omega$"); ax.grid(alpha=0.25)
    ax.legend(loc="lower right", fontsize=6)

    fig.suptitle("B2 — Li et al. 2024 Fig. 2(b): no admissible interpretation reproduces the published panel",
                 fontsize=10)
    fig.tight_layout()
    out = WORK / "B2_overlay_interpretations.png"
    fig.savefig(out); plt.close(fig)
    return dict(overlay=str(out), overlay_sha256=sha(out), reference_pixels=int(ref_x.size),
                gaps_source_geometry=gaps_macro, barred_required_dps=float(dps_bar),
                micro_gaps=micro["gaps"])


# ------------------------------------------------------------------ B3
def b3_evidence(panels: dict) -> dict:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    b3 = R2.b3_dispersion(n_w=3000)
    ref_x, ref_y = R2.digitise_reference("B3", panels)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), dpi=150)
    axes[0].imshow(panels["B3"]["panel"], cmap="gray", extent=[-1, 1, 0, 2], aspect="auto")
    axes[0].plot(ref_x, ref_y, ".", ms=1.0, color="#1f77b4", alpha=0.6)
    axes[0].plot([], [], ".", color="#1f77b4", label="published Fig. 4(c) (digitised)")
    axes[0].legend(loc="upper right", fontsize=7)
    axes[0].set_title("published panel (c): gradient elasticity", fontsize=9)
    cx = np.array([c[1] for c in b3["curves"]]); cy = np.array([c[0] for c in b3["curves"]])
    for sign in (1, -1):
        axes[1].plot(sign * cx, cy, lw=1.3, color="#d62728",
                     label="independent reproduction" if sign > 0 else None)
    axes[1].plot(ref_x, ref_y, ".", ms=1.0, color="#1f77b4", alpha=0.5,
                 label="published Fig. 4(c) (digitised)")
    axes[1].set_title("reproduction vs published (same axes/normalisation)", fontsize=9)
    for ax in axes:
        ax.set_xlim(-1.02, 1.02); ax.set_ylim(-0.02, 2.05)
        ax.set_xlabel(r"$\bar k$"); ax.set_ylabel(r"$\bar\omega$"); ax.grid(alpha=0.25)
        ax.legend(loc="upper right", fontsize=7)
    fig.suptitle("B3 — Li et al. 2023 Fig. 4(c), dipolar-gradient Pb/brass bilayer: graphical reproduction",
                 fontsize=10)
    fig.tight_layout()
    out = WORK / "B3_overlay.png"
    fig.savefig(out); plt.close(fig)
    return dict(overlay=str(out), overlay_sha256=sha(out), reference_pixels=int(ref_x.size),
                gaps=b3["gaps"], omega0=b3["w0"], omega0_stated=b3["omega0_stated"])


def main():
    panels = P.panel_arrays()
    rec: dict = {"benchmarks": {}}

    # ---------------- B1 ------------------------------------------------
    wbar, kbar, prop, gaps, w0 = R2.b1_dispersion(n_w=4000)
    b1_ov, ref_b1 = R2.overlay(
        "B1", panels, dict(wbar=wbar, kbar=kbar, prop=prop, gaps=gaps, w0=w0),
        "B1 — Li et al. 2024 Fig. 2(a), classical AlN/BaTiO3 bilayer: graphical reproduction",
        "B1_overlay.png")
    rec["benchmarks"]["B1"] = dict(
        route="GRAPHICAL_VALIDATION", graphical_validation="PASS",
        quantitative_error=None,
        reproduced_gaps=gaps,
        published_features_read="band edges at kbar=0: 0.0 / ~1.48 / ~1.98; at kbar=1: ~1.48 / ~0.51",
        overlay=str(b1_ov), overlay_sha256=sha(b1_ov),
        reason=("source provides no machine-readable numerical values; the published curve is "
                "reproduced from the source-stated parameters (AlN/BaTiO3, a_A = a_B = 0.01 m, "
                "Eq. 55 normalisation) and lies on the published curve; classical Rytov solution "
                "verified against the source's own equations"))

    # ---------------- B2 ------------------------------------------------
    b2 = b2_evidence(panels)
    rec["benchmarks"]["B2"] = dict(
        route="NOT_VALIDATED", graphical_validation="NOT_APPLICABLE",
        quantitative_error=None, ambiguity_status="UNRESOLVED",
        interpretation_gaps=b2["gaps_source_geometry"],
        micro_gaps=b2["micro_gaps"], barred_required_dps=b2["barred_required_dps"],
        overlay=b2["overlay"], overlay_sha256=b2["overlay_sha256"],
        reason=("the caption's length-scale values are a bare unlabelled 'l = 1e-5', while Eq. 55 "
                "defines l_bar = l/b; with the source-stated geometry a = 0.01 m the dimensional "
                "reading gives l/b = 5e-4 and a gradient correction O(1e-6), so the reproduction "
                "coincides with the classical panel and contradicts the published panel (b); the "
                "barred reading is numerically infeasible (adaptive precision ~5.2e4 digits); an "
                "unstated micro geometry (a = 1e-5 m) yields a different band/gap structure. "
                "No interpretation is selected: the ambiguity is unresolved"))

    # ---------------- B3 ------------------------------------------------
    b3 = b3_evidence(panels)
    rec["benchmarks"]["B3"] = dict(
        route="NOT_VALIDATED", graphical_validation="NOT_APPLICABLE",
        quantitative_error=None,
        reproduced_gaps=b3["gaps"],
        omega0_reproduced=b3["omega0"], omega0_stated=b3["omega0_stated"],
        published_features_read=("first two branches from the published panel: (kbar, wbar) "
                                 "(0,0) -> (1,~0.45) and (~0.3,0.30) -> (1,~0.50); first gap ~0.1-0.3"),
        overlay=b3["overlay"], overlay_sha256=b3["overlay_sha256"],
        reason=("source parameters are available (cbar1 = 0.15, dbar1 = 0.25, cR = dR = 1.5, "
                "a1 = 1e-5 m, rho1 = 7.5e3 kg/m3, mu1 = 2.3e10 Pa, muR = 0.056, rhoR = 0.157; "
                "omega0 reproduced 4.115e8 Hz vs stated 4.1e8 Hz), BUT the independent "
                "reproduction does NOT overlay the published panel: the lowest branch reaches "
                "omega_bar ~= 0.35 at k_bar = 1 whereas the source's own figure and the exact "
                "classical-limit value require 0.50; the available dipolar-gradient transfer-matrix "
                "implementation is numerically unstable in its own classical limit (overflow of "
                "sinh(tau a) as the gradient parameters -> 0, so the machinery cannot be validated "
                "against its analytic limit); per the phase rule no parameter was tuned to force "
                "agreement, and the unresolved question (which dipolar-gradient formulation / "
                "coefficient convention the source used) is a SOURCE_UNAVAILABLE item"))
    rec["blocked_reason_B3"] = ("faithful reproduction not achieved with the available "
                               "implementation; classical-limit self-check not evaluable (overflow)")

    (WORK / "p12s_validation_record.json").write_text(json.dumps(rec, indent=1, default=str))
    print(json.dumps(rec, indent=1, default=str))
    return rec


if __name__ == "__main__":
    main()
