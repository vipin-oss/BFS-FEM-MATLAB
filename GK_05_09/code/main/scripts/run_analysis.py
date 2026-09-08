"""Full scientific analysis: landscape, bands, profile, Monte Carlo, BIC,
calibration. Writes machine-readable results to results/.

Everything is RECOMPUTED. No scientific value is hard-coded.
"""
from __future__ import annotations
import sys, json, os
from pathlib import Path
import numpy as np


# ===========================================================================
# WINDOWS-SAFE ENTRY POINT
# Under the "spawn" start method (Windows/macOS) every worker re-imports this
# module, so module-level work would run again in each child. All executable
# work is therefore inside main(). CONTROL FLOW ONLY: no equation, grid,
# tolerance, seed or acceptance criterion is affected.
# ===========================================================================
def main():
    ROOT = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(ROOT))

    from src.model import Theta, Geometry
    from src.statistics import band_edge, fisher
    from src.analysis import landscape, monte_carlo, bic_compare, profile, make_grid
    from src.calibration import CASES, DISCREPANCY, aggregate, max_B_deviation, FITTING_DOMAIN
    from src.io import save_json, save_csv, RESULTS

    import argparse
    _ap = argparse.ArgumentParser(description="GK analysis (source: GK_COMPLETE_CALCULATIONS.tex)")
    _ap.add_argument("--mc-seed", type=int, default=None, help="override mc_seed_base")
    _ap.add_argument("--bic-seed", type=int, default=None, help="override bic_seed_base")
    _args, _ = _ap.parse_known_args()

    CFG = json.loads((ROOT / "config" / "default_parameters.json").read_text())
    cfg = dict(CFG["reference_configuration"]); cfg.update(CFG["statistics"])
    if _args.mc_seed is not None:
        cfg["mc_seed_base"] = _args.mc_seed
    if _args.bic_seed is not None:
        cfg["bic_seed_base"] = _args.bic_seed
    print(f"seeds: mc_seed_base={cfg['mc_seed_base']} bic_seed_base={cfg['bic_seed_base']}")
    BANDS = CFG["bands"]["targets_pct"]
    GEOM = Geometry(cfg["L"], cfg["t_p"])
    t80 = make_grid(cfg)
    pool = None
    if os.environ.get("GK_FAST") != "1":
        from concurrent.futures import ProcessPoolExecutor
        pool = ProcessPoolExecutor(max_workers=os.cpu_count())

    print("=" * 96); print("1. IDENTIFIABILITY LANDSCAPE (calc:landscape)"); print("=" * 96)
    Bs = [0.10, 0.30, 0.50, 0.70, 0.90, 0.98, 1.00, 1.02, 1.10, 1.28, 1.50,
          2.00, 2.41, 3.00, 5.00]
    land = landscape(Bs, cfg, GEOM)
    print(f"{'B':>6} {'cond(F)':>11} {'corr':>9} {'se_tq%':>11} {'se_al%':>9} {'se_B%':>9}")
    for r in land:
        print(f"{r['B']:>6.2f} {r['cond']:>11.3e} {r['corr']:>9.4f} "
              f"{r['se_tau_q']:>11.4g} {r['se_alpha']:>9.4g} {r['se_B']:>9.4g}")
    save_csv(RESULTS / "identifiability_results.csv",
             [[r["B"], r["cond"], r["corr"], r["se_tau_q"], r["se_kappa2"],
               r["se_alpha"], r["se_B"]] for r in land],
             ["B", "cond_F", "corr_tq_k2", "se_tau_q_pct", "se_kappa2_pct",
              "se_alpha_pct", "se_B_pct"])

    print("\n" + "=" * 96); print("2. BAND EDGES (eq:band-def, recomputed)"); print("=" * 96)
    bands = {}
    for tgt in BANDS:
        lo = band_edge(float(tgt), 1.0, 0.01, t80, GEOM, cfg["eta_noise"])
        hi = band_edge(float(tgt), 1.0, 20.0, t80, GEOM, cfg["eta_noise"])
        bands[str(tgt)] = [lo, hi]
        print(f"  s.e.(tau_q) > {tgt:>3}% : B in [{lo:.4f}, {hi:.4f}]   "
              f"design: B <= {lo:.4f} or B >= {hi:.4f}")
    save_json(RESULTS / "band_results.json", bands)

    print("\n" + "=" * 96); print("3. PROFILE LIKELIHOOD (calc:profile)"); print("=" * 96)
    prof = {}
    for B in (0.50, 0.90, 1.00, 1.28, 5.00):
        p = profile(B, cfg, GEOM)
        prof[str(B)] = {k: (v.tolist() if isinstance(v, np.ndarray) else v)
                        for k, v in p.items()}
        wf = p["width_factor"]
        print(f"  B={B:<5} 95% interval tau_q=[{p['lo']:.5g},{p['hi']:.5g}] "
              f"= [{p['lo']/cfg['tau_q']:.2f},{p['hi']/cfg['tau_q']:.2f}]x  "
              f"factor {wf:.1f}{'  GRID-LIMITED' if p['grid_limited'] else ''}")
    save_json(RESULTS / "profile_results.json", prof)

    print("\n" + "=" * 96); print("4. MONTE CARLO (calc:mc)"); print("=" * 96)
    mcs = []
    for B in (0.50, 0.90, 1.28, 2.41, 5.00):
        m = monte_carlo(B, cfg, GEOM, pool=pool)
        fi = fisher(Theta.from_B(cfg["alpha"], cfg["tau_q"], B), t80, GEOM,
                    cfg["eta_noise"])["se_tau_q"]
        m["fisher_se_tau_q_pct"] = fi
        mcs.append(m)
        print(f"  B={B:<5} MC={m['se_tau_q_robust_pct']:>8.2f}%  Fisher={fi:>8.2f}%  "
              f"tq 5-95%=[{m['tq_p5']:.3f},{m['tq_p95']:.3f}]")
    save_csv(RESULTS / "monte_carlo_results.csv",
             [[m["B"], m["n"], m["se_tau_q_robust_pct"], m["fisher_se_tau_q_pct"],
               m["tq_p5"], m["tq_p95"], m["alpha_p5"], m["alpha_p95"],
               m["B_p5"], m["B_p95"]] for m in mcs],
             ["B", "n_trials", "mc_se_tau_q_pct", "fisher_se_tau_q_pct",
              "tq_p5", "tq_p95", "alpha_p5", "alpha_p95", "B_p5", "B_p95"])

    print("\n" + "=" * 96); print("5. BIC MODEL SELECTION (calc:bic)"); print("=" * 96)
    bics = []
    for B in (1.00, 1.28, 2.41, 5.00):
        b = bic_compare(B, cfg, GEOM, pool=pool)
        bics.append(b)
        d = b["delta"]
        print(f"  B={B:<5} fourier={d['fourier']:>8.2f} mcv={d['mcv']:>8.2f} "
              f"nyiri={d['nyiri']:>8.2f} gk={d['gk']:>8.2f}  -> {b['selected'].upper()}")
    save_csv(RESULTS / "bic_results.csv",
             [[b["B"], b["delta"]["fourier"], b["delta"]["mcv"], b["delta"]["nyiri"],
               b["delta"]["gk"], b["selected"]] for b in bics],
             ["B", "dBIC_fourier", "dBIC_mcv", "dBIC_nyiri", "dBIC_gk", "selected"])

    print("\n" + "=" * 96); print("6. PUBLISHED CALIBRATIONS (sec:calibrations)"); print("=" * 96)
    lo20, hi20 = bands["20"]
    rows = []
    for c in CASES:
        B = c.B_used
        rows.append([c.idx, c.source, c.citekey, c.specimen, c.alpha_1e6, c.tau_q_s,
                     c.kappa2_1e6 if c.kappa2_1e6 is not None else "",
                     c.B_calc if c.B_calc is not None else "",
                     c.B_reported if c.B_reported is not None else "",
                     round(B, 4), c.in_band(lo20, hi20),
                     c.dB_rel if c.dB_rel is not None else "", c.R2 or "", c.note])
        flag = "IN " if c.in_band(lo20, hi20) else "out"
        print(f"  {c.idx:>2} {c.specimen:<22} B={B:6.3f} {flag}  "
              f"{'dB=%.2f%%' % (100*c.dB_rel) if c.dB_rel else ''}")
    agg = aggregate(lo20, hi20)
    print(f"\n  AGGREGATE: {agg['n_inside']} of {agg['n_total']} inside "
          f"[{lo20:.3f},{hi20:.3f}]; {agg['n_outside']} outside")
    print(f"  max |B_calc - B_reported| = {max_B_deviation():.4f}")
    print(f"  Feher-Kovacs fitting domain (eq:fitting-domain): {FITTING_DOMAIN}")
    save_csv(RESULTS / "calibration_results.csv", rows,
             ["case", "source", "citekey", "specimen", "alpha_1e6_LIT",
              "tau_q_s_LIT", "kappa2_1e6_LIT", "B_calc_DER", "B_reported_LIT",
              "B_used", "in_band", "dB_rel_DER", "R2_LIT", "note"])
    save_json(RESULTS / "calibration_summary.json",
              {"band": [lo20, hi20], "aggregate": agg,
               "max_B_deviation": max_B_deviation(),
               "fitting_domain": list(FITTING_DOMAIN),
               "discrepancy": [{"specimen": d[0], "tau_q_earlier_LIT": d[1],
                                "tau_q_refined_LIT": d[2],
                                "ratio_DER": round(max(d[1], d[2]) / min(d[1], d[2]), 3),
                                "R2_LIT": d[3]} for d in DISCREPANCY]})

    if pool:
        pool.shutdown()
    print("\nAnalysis complete; results written to results/")


if __name__ == "__main__":
    import multiprocessing as _mp
    _mp.freeze_support()
    main()
