#!/usr/bin/env python3
"""Rewrite the manuscript's production literals from the n = 16 authoritative data.

Every replacement is derived from the regenerated JSON artefacts
(results/raw/p5_production_raw_mesh16.json, results/processed/table5_gap_summary_mesh16.json,
results/raw/p12b_s7_theta_sweep_mesh16.json); nothing is typed by hand.  Each
target string must be found exactly once, otherwise the script aborts without
writing, so a stale literal cannot silently survive.

Usage:  python3 production/update_mesh16_literals.py [--check]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER9 = HERE.parent
SEC = PAPER9 / "latex" / "sections"
RAW = PAPER9 / "results" / "raw" / "p5_production_raw_mesh16.json"
TAB5 = PAPER9 / "results" / "processed" / "table5_gap_summary_mesh16.json"
S7 = PAPER9 / "results" / "raw" / "p12b_s7_theta_sweep_mesh16.json"


def fmt(x, nd):
    return f"{x:.{nd}f}"


def build_replacements():
    raw = json.loads(RAW.read_text())
    t5 = json.loads(TAB5.read_text())
    s7 = json.loads(S7.read_text())
    design = raw["study_S5_design_map"]

    def case(ar, th):
        return [p for p in design if p["AR"] == ar and p["theta_deg"] == th][0]

    c = case(10.0, 45.0)
    dgx_10_45 = c["gaps"][1]["delta_GX"]
    # the bound quoted in the text is the least negative complete-gap value over the design map
    dcomp_10_45 = max(p["gaps"][1]["delta_complete"] for p in design)
    dgx = [p["gaps"][1]["delta_GX"] for p in design]
    best = max(dgx)
    best_pt = design[dgx.index(best)]
    s_th = raw["study_S6_sensitivity_Stheta"]["AR_10"]["S_theta_rad_inv"]
    s7p5 = raw["study_S7_ifc_steering"]
    dmax1 = s7p5["AR_1_th_0"]["delta_max_deg"]
    dmax5 = s7p5["AR_5_th_45"]["delta_max_deg"]
    dmax10 = s7p5["AR_10_th_45"]["delta_max_deg"]

    sweep = s7["sweep"]
    d5 = [sweep[f"AR_5_th_{int(t)}"]["delta_max_deg"] for t in (0, 15, 30, 45, 60, 75, 90)]
    d10 = [sweep[f"AR_10_th_{int(t)}"]["delta_max_deg"] for t in (0, 15, 30, 45, 60, 75, 90)]
    lo5, hi5, span5 = min(d5), max(d5), (max(d5) - min(d5)) / max(d5) * 100.0
    lo10, hi10, span10 = min(d10), max(d10), (max(d10) - min(d10)) / max(d10) * 100.0
    ms5 = s7["M_s"]["AR_5"]["M_s_deg"]
    ms10 = s7["M_s"]["AR_10"]["M_s_deg"]
    resid180 = max(s7["symmetry_checks"][k]["headless_180_max_dev_deg"] for k in ("AR_5", "AR_10"))
    residmir = max(
        max(s7["symmetry_checks"][k]["mirror_delta(ph;th)=delta(90-ph;90-th)_max_dev_deg"].values())
        for k in ("AR_5", "AR_10"))

    out = {}
    out.setdefault("sec06_results.tex", [])

    def rep(section, old, new, count=1):
        out.setdefault(section, []).append((old, new, count))

    # ---- sec06: Case H directional gap, complete-gap bound, design-map maximum, S_theta


    rep("sec06_results.tex",
        f"$\\Delta_{{GX}} = +{fmt(0.0431, 4)}$ along $\\Gamma$--$X$ while strictly preserving the "
        f"absence of complete omnidirectional band gaps ($\\Delta_{{\\mathrm{{complete}}}} \\le "
        f"{fmt(-0.3758, 4)}$)",
        f"$\\Delta_{{GX}} = +{fmt(dgx_10_45, 4)}$ along $\\Gamma$--$X$ while strictly preserving the "
        f"absence of complete omnidirectional band gaps ($\\Delta_{{\\mathrm{{complete}}}} \\le "
        f"{fmt(dcomp_10_45, 4)}$)")


    rep("sec06_results.tex",
        f"opening a directional stop band $\\Delta_{{GX}} = +{fmt(0.0431, 4)}$ between bands 2 and 3",
        f"opening a directional stop band $\\Delta_{{GX}} = +{fmt(dgx_10_45, 4)}$ between bands 2 and 3")


    rep("sec06_results.tex",
        f"confirms $\\Delta_{{\\mathrm{{complete}}}} \\le {fmt(-0.3758, 4)}$",
        f"confirms $\\Delta_{{\\mathrm{{complete}}}} \\le {fmt(dcomp_10_45, 4)}$")


    rep("sec06_results.tex",
        f"stop bands ($\\Delta_{{\\mathrm{{complete}}}} \\le {fmt(-0.3758, 4)}$), introducing periodic",
        f"stop bands ($\\Delta_{{\\mathrm{{complete}}}} \\le {fmt(dcomp_10_45, 4)}$), introducing periodic")


    rep("sec06_results.tex",
        f"global maximum of $\\Delta_{{GX}} = {fmt(0.0896, 4)}$ at $(\\theta = {int(30.0)}^\\circ, "
        f"\\mathrm{{AR}} = {int(10.0)})$ (and $\\Delta_{{GX}} = {fmt(0.0431, 4)}$ at $\\theta = 45^\\circ$)",
        f"global maximum of $\\Delta_{{GX}} = {fmt(best, 4)}$ at $(\\theta = {int(best_pt['theta_deg'])}^\\circ, "
        f"\\mathrm{{AR}} = {int(best_pt['AR'])})$ (and $\\Delta_{{GX}} = {fmt(dgx_10_45, 4)}$ at $\\theta = 45^\\circ$)")


    rep("sec06_results.tex",
        f"reaching $S_\\theta = {fmt(3.946, 3)}\\,\\mathrm{{rad}}^{{-1}}$ at $\\mathrm{{AR}} = 10$",
        f"reaching $S_\\theta = {fmt(s_th, 3)}\\,\\mathrm{{rad}}^{{-1}}$ at $\\mathrm{{AR}} = 10$")

    # ---- sec07: steering peaks and orientation-sweep spans


    rep("sec07_steering.tex",
        f"$\\delta_{{\\max}} = {fmt(0.01, 2)}^\\circ$ ($\\mathrm{{AR}}=1$), "
        f"${fmt(1.41, 2)}^\\circ$ ($\\mathrm{{AR}}=5$), and ${fmt(2.79, 2)}^\\circ$ ($\\mathrm{{AR}}=10$)",
        f"$\\delta_{{\\max}} = {fmt(dmax1, 2)}^\\circ$ ($\\mathrm{{AR}}=1$), "
        f"${fmt(dmax5, 2)}^\\circ$ ($\\mathrm{{AR}}=5$), and ${fmt(dmax10, 2)}^\\circ$ ($\\mathrm{{AR}}=10$)")


    rep("sec07_steering.tex",
        f"($\\delta_{{\\max}} = {fmt(0.01, 2)}^\\circ$, well within numerical noise)",
        f"($\\delta_{{\\max}} = {fmt(dmax1, 2)}^\\circ$, well within numerical noise)")


    rep("sec09_conclusions.tex",
        f"producing directional stop bands up to $\\Delta_{{GX}} = {fmt(0.0896, 4)}$ along "
        f"$\\Gamma$--$X$ while strictly adhering to the absence of complete band gaps "
        f"($\\Delta_{{\\mathrm{{complete}}}} \\le {fmt(-0.3758, 4)}$). The orientation sensitivity "
        f"metric $S_\\theta$ increases monotonically with aspect ratio up to ${fmt(3.946, 3)}\\,"
        f"\\mathrm{{rad}}^{{-1}}$ at $\\mathrm{{AR}} = 10$.",
        f"producing directional stop bands up to $\\Delta_{{GX}} = {fmt(best, 4)}$ along "
        f"$\\Gamma$--$X$ while strictly adhering to the absence of complete band gaps "
        f"($\\Delta_{{\\mathrm{{complete}}}} \\le {fmt(dcomp_10_45, 4)}$). The orientation sensitivity "
        f"metric $S_\\theta$ increases monotonically with aspect ratio up to ${fmt(s_th, 3)}\\,"
        f"\\mathrm{{rad}}^{{-1}}$ at $\\mathrm{{AR}} = 10$.")


    rep("sec09_conclusions.tex",
        f"up to $\\delta_{{\\max}} = {fmt(2.79, 2)}^\\circ$ at $\\mathrm{{AR}} = 10$",
        f"up to $\\delta_{{\\max}} = {fmt(dmax10, 2)}^\\circ$ at $\\mathrm{{AR}} = 10$")

    return out, {
        "delta_GX_AR10_th45": dgx_10_45, "delta_complete_AR10_th45": dcomp_10_45,
        "delta_GX_max": best, "delta_GX_max_theta": best_pt["theta_deg"], "delta_GX_max_AR": best_pt["AR"],
        "S_theta_AR10": s_th, "delta_max_AR1": dmax1, "delta_max_AR5_th45": dmax5,
        "delta_max_AR10_th45": dmax10, "range_AR5": [lo5, hi5], "range_AR10": [lo10, hi10],
        "span_AR5_pct": span5, "span_AR10_pct": span10, "M_s_AR5": ms5, "M_s_AR10": ms10,
        "sym_resid_180": resid180, "sym_resid_mirror": residmir,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    reps, metrics = build_replacements()
    problems = []
    for section, items in reps.items():
        text = (SEC / section).read_text()
        for old, _new, count in items:
            found = text.count(old)
            if found != count:
                problems.append((section, old, found, count))
    if problems:
        for section, old, found, want in problems:
            print(f"TARGET PROBLEM {section}: found {found}, expected {want}: {old[:90]!r}")
        return 1
    print(json.dumps(metrics, indent=1))
    if args.check:
        print("check only: every target literal found exactly once; nothing written")
        return 0
    n = 0
    for section, items in reps.items():
        path = SEC / section
        text = path.read_text()
        for old, new, count in items:
            text = text.replace(old, new, count)
            n += 1
        path.write_text(text)
        print(f"updated {section}: {len(items)} literals")
    print(f"total replacements: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
