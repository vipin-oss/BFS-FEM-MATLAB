"""P11D Benchmark B2 parameter-interpretation registry (single authoritative run).

Remediation items 3-5.  Runs THREE labelled interpretations of the Li et al.
(2023) Benchmark B2 length parameters (l, l-bar) through the stabilized
adaptive-precision engine (paper9/validation/b2_stable_tm.py), with derived
statuses only (no hardcoded PASS anywhere), independent checks, and stop bands
for each interpretation.

Output: paper9/results/raw/p11d_b2_gap_registry.json -- the SINGLE
authoritative B2 stop-band dataset.  benchmark_evidence.json and Table 3 are
REGENERATED from this file (paper9/audit/p11d_regenerate_evidence.py); no
number is hand-edited for agreement.

Usage:
    python3 paper9/production/p11d_b2_registry.py [--only CFG-...] [--quick]
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from validation.b2_stable_tm import (  # noqa: E402
    StableB2, judge_status, independent_polyroots_check,
)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "paper9", "results", "raw", "p11d_b2_gap_registry.json")

PARAMETER_SEMANTICS = {
    "l": "gradient-length parameter in the PDE (mu_0 = c33 l^2 prefactor); dimension [m]",
    "l1": "second gradient-length parameter; standard form l1 = 2 l; dimension [m]",
    "l_bar": "length parameter normalized BY THE LAYER WIDTH a (l_bar = l / a); dimensionless",
    "normalization_location": (
        "the P11B code path normalizes l -> l/a inside layer_scaled_T when "
        "use_micro_scale=True (published-axis 'modified geometry'); the present "
        "dimensional engine carries l and a with their units throughout and "
        "normalizes only the abscissa w_bar = w / omega_0"),
    "solver_usage": (
        "layer transfer matrices T_i(w) enter the cell monodromy T = T_B T_A; "
        "stop bands are w_bar intervals where no z = lambda + 1/lambda of T lies "
        "in [-2, 2] (palindromic reciprocal spectrum, det T = 1)"),
    "ambiguity_status": (
        "Li et al. (2023) tabulate l and l_bar for the micro-scale figure "
        "geometry but quote a = 1 cm macro width with dimensional l values in "
        "the text; the paper is internally inconsistent between the plotted "
        "scale and the quoted geometry.  The three configurations below are "
        "defensible interpretations run SEPARATELY and LABELLED; none resolves "
        "the source ambiguity; none is an external validation of the solver."),
}

ENGINE_DESCRIPTION = {
    "primary": "adaptive-precision mpmath evaluation of the exact monodromy with "
               "z = lambda + 1/lambda propagating test (z_small = 2P/(s1 + sqrt(s1^2-4P)), "
               "P = z1 z2 = (s1^2 - s2 - 4)/2 from traces s_k = tr T^k)",
    "precision_policy": "dps = max(50, ceil(0.4343 * Lambda) + 15), "
                        "Lambda = kappa_A a_A + kappa_B a_B at the scan top "
                        "(z_small absolute error ~ 10^-dps e^Lambda)",
    "cross_check_1": "long-double (clongdouble) monodromy + exact z-test (structurally "
                     "guarded palindromy) where exponent range allows",
    "cross_check_2": "mpmath.polyroots of the characteristic polynomial (independent "
                     "algorithm) at spot frequencies",
    "status_policy": "judge_status() derives every status from max_error vs tol; "
                     "non-finite errors FAIL; no code path can emit PASS with "
                     "error >> tol",
}


def band_count_estimate(sb: StableB2, w_lo=0.01, w_hi=3.0):
    """Rough Bragg count: propagating phase integral over w_bar / pi."""
    import math
    phase = 0.0
    dw = (w_hi - w_lo) / 200
    for which in ("A", "B"):
        d = sb.layer_data(which)
        for i in range(200):
            w = (w_lo + dw * (i + 0.5)) * sb.omega_0
            A_ = d["c33"] * d["l"] ** 2
            B_ = d["c33"] - d["rho"] * w ** 2 * d["l1"] ** 2
            C_ = -d["rho"] * w ** 2
            disc = B_ ** 2 - 4 * A_ * C_
            k2_1 = (-B_ + math.sqrt(disc)) / (2 * A_)
            if k2_1 > 0:
                phase += math.sqrt(k2_1) * d["a"] * dw
    return phase / math.pi  # ~ one gap per half wavelength of phase


def run_config(sb: StableB2, n_scan=600, scan_range=(0.01, 3.0),
               edge_iters=80, spot_freqs=(0.5, 1.3, 2.3), include_polyroots=True):
    t0 = time.time()
    dps = sb.required_dps()
    entry = {
        "config": sb.config,
        "label": sb.CONFIGS[sb.config]["label"],
        "params": {
            "l_A_m": sb.l_A, "l1_A_m": sb.l1_A, "l_bar_A": sb.lbar_A,
            "l_B_m": sb.l_B, "l1_B_m": sb.l1_B, "l_bar_B": sb.lbar_B,
            "a_A_m": sb.a_A, "a_B_m": sb.a_B,
            "rho_A": sb.rho_A, "c33_A": sb.c33_A,
            "rho_B": sb.rho_B, "c33_B": sb.c33_B,
            "omega_0": sb.omega_0,
        },
        "lambda_cell": sb.lambda_cell(),
        "dps": dps,
        "level1_homogeneous": sb.level1_homogeneous(),
        "level2_identical_reduction": sb.level2_identical_reduction(),
    }
    entry["structural_check"] = sb.structural_check(0.5)
    checks = []
    for wb in spot_freqs:
        prop, meta = sb.propagating_mp(wb)
        checks.append({"w_bar": wb, "trace_z_propagating": prop, "meta": meta})
        if include_polyroots:
            try:
                pr = independent_polyroots_check(sb, wb)
                checks[-1]["polyroots"] = pr
            except Exception as exc:  # noqa: BLE001
                checks[-1]["polyroots"] = {
                    "attempted": True, "ok": False,
                    "error": f"{type(exc).__name__}: {str(exc)[:200]}",
                    "note": "independent polyroots check could not run at this "
                            "dynamic range; primary engine verified by level1/2 "
                            "identities and structural checks instead",
                }
    entry["spot_checks"] = checks
    entry["estimated_stop_bands_full_range"] = band_count_estimate(sb)
    scan = sb.scan(scan_range[0], scan_range[1], n=n_scan, edge_tol=1e-6,
                   edge_iters=edge_iters)
    entry["scan"] = scan
    entry["elapsed_s"] = time.time() - t0
    return entry


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None, help="run a single CFG- id")
    ap.add_argument("--quick", action="store_true", help="reduced scan (debug)")
    args = ap.parse_args()

    cfgs = [args.only] if args.only else ["CFG-DIM-MICRO", "CFG-DIM-MACRO", "CFG-BAR-MACRO"]
    plans = {
        # authoritative full scan == the manuscript stop-band dataset
        "CFG-DIM-MICRO": dict(n_scan=600, scan_range=(0.01, 3.0), edge_iters=80,
                              include_polyroots=True,
                              scan_role="AUTHORITATIVE full-range stop-band dataset"),
        "CFG-DIM-MACRO": dict(n_scan=600, scan_range=(0.01, 3.0), edge_iters=80,
                              include_polyroots=True,
                              scan_role="full-range listing of the dimensional-macro "
                                        "interpretation (labelled; not the manuscript dataset)"),
        "CFG-BAR-MACRO": dict(n_scan=60, scan_range=(0.01, 3.0), edge_iters=10,
                              include_polyroots=False,
                              scan_role="reduced-fidelity full-range listing (grid "
                                        "d_w_bar~0.05: gaps narrower than that may be "
                                        "missed; edges bisected to bracket/2^10); "
                                        "adaptive precision ~5e4 dps"),
    }
    if args.quick:
        for p in plans.values():
            p["n_scan"] = min(p["n_scan"], 24)
            p["edge_iters"] = min(p["edge_iters"], 10)
            p["include_polyroots"] = False
    if os.path.exists(OUT) and args.only:
        with open(OUT) as f:
            doc = json.load(f)
    else:
        doc = {
            "schema": "p11d.b2_registry.v1",
            "benchmark": "Benchmark B2 (Li et al. 2023 two-phase gradient metamaterial)",
            "generator": "paper9/production/p11d_b2_registry.py",
            "git_sha": (subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                       capture_output=True, text=True).stdout or "").strip(),
            "engine": ENGINE_DESCRIPTION,
            "parameter_semantics": PARAMETER_SEMANTICS,
            "external_validation": "NOT EXTERNALLY VALIDATED: no author-released numerical "
                                   "tables exist for Benchmark B2 stop bands; all outputs "
                                   "here are internal calculation evidence only",
            "configs": {},
        }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    for cfg in cfgs:
        sb = StableB2(cfg)
        plan = plans[cfg]
        print(f"[registry] {cfg}: Lambda={sb.lambda_cell():.4g}, dps={sb.required_dps()}, "
              f"n={plan['n_scan']} range={plan['scan_range']}", flush=True)
        entry = run_config(sb, n_scan=plan["n_scan"], scan_range=plan["scan_range"],
                           edge_iters=plan["edge_iters"],
                           include_polyroots=plan["include_polyroots"])
        entry["scan_role"] = plan["scan_role"]
        doc["configs"][cfg] = entry
        with open(OUT, "w") as f:
            json.dump(doc, f, indent=2, default=str)
        print(f"[registry] {cfg} done in {entry['elapsed_s']:.1f}s -> {OUT}", flush=True)
        l1 = entry["level1_homogeneous"]
        print(f"  level1: err={l1['max_error']:.3e} status={l1['status']}", flush=True)
        print(f"  est. full-range stop bands: {entry['estimated_stop_bands_full_range']:.0f}", flush=True)
        for g in entry["scan"]["gaps"]:
            print(f"  gap: [{g[0]:.4f}, {g[1]:.4f}] width {g[2]:.4f}", flush=True)


if __name__ == "__main__":
    main()
