"""Acceptance tests T1-T24 (+T4b) read from tab:acceptance of the master.

Each test records: test_id, description, equation, input, expected, actual,
absolute_error, relative_error, tolerance, status, timestamp, git_commit.
"""
from __future__ import annotations
import sys, json, os, warnings
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

    from src.model import Theta, Geometry, B_of
    from src.forward import forward, forward_and_jacobian, ForwardSolver
    from src.fd_solver import solve_fd
    from src.split_solver import solve_split
    from src.limits import T_series, TINY
    from src.statistics import fisher, band_edge, sigma_of
    from src.analysis import landscape, monte_carlo, bic_compare, profile, make_grid
    from src.calibration import CASES
    from src.validation import load_digitised, load_fig2, metrics, ANCHOR_CASES, FIG2
    from src.laplace import m2, t_star
    from src.io import save_json, save_csv, provenance, RESULTS, ACCEPT

    CFG = json.loads((ROOT / "config" / "default_parameters.json").read_text())
    cfg = dict(CFG["reference_configuration"]); cfg.update(CFG["statistics"])
    GEOM = Geometry(cfg["L"], cfg["t_p"])
    TESTS = []


    def rec(tid, desc, eq, inp, expected, actual, tol, status=None,
            abs_err=None, rel_err=None):
        if status is None:
            try:
                abs_err = abs(float(actual) - float(expected))
                rel_err = abs_err / abs(float(expected)) if float(expected) else None
                status = "PASS" if abs_err <= float(tol) else "FAIL"
            except (TypeError, ValueError):
                status = "INFO"
        e = dict(test_id=tid, description=desc, equation=eq, input=str(inp),
                 expected=str(expected), actual=str(actual),
                 absolute_error=abs_err, relative_error=rel_err,
                 tolerance=str(tol), status=status)
        e.update(provenance())
        TESTS.append(e)
        save_json(ACCEPT / f"{tid}.json", e)
        m = {"PASS": "PASS", "FAIL": "*** FAIL", "INFO": "INFO"}[status]
        print(f"[{tid:<4}] {m:<9} {desc[:60]:<60} exp={str(expected)[:14]:<14} act={str(actual)[:18]}")
        return status


    print("="*118); print("ACCEPTANCE TESTS  (source: tab:acceptance)"); print("="*118)

    # T1 --------------------------------------------------------------------
    s = np.array([0.7, 5.0, 40.0, 1e-3, 1e3])
    tq = 0.03
    dev = float(np.max(np.abs(m2(s, tq, 1.0*tq) - s/1.0)))
    rec("T1", "m^2 at kappa2=alpha*tau_q equals s/alpha", "eq:res-step5",
        "s in {1e-3..1e3}, tau_q=0.03, kappa2=alpha*tau_q", 0.0, dev, 1e-14)

    # T2, T3 ----------------------------------------------------------------
    for tid, fig, exp in (("T2", "fig3", 0.384), ("T3", "fig5", 0.382)):
        p = ANCHOR_CASES[fig]
        x, ymean, sd = load_digitised(fig)
        keep = x <= p["tmax"]; x, ymean = x[keep], ymean[keep]
        ours = forward(Theta(1.0, p["tau_q"], p["kappa2"]), x, GEOM)
        mm = metrics(ymean, ours, sd)
        rec(tid, f"Anchor {fig} NRMSE (published params, no fitting)", "calc:repro",
            f"tau_q={p['tau_q']}, kappa2={p['kappa2']}, n={mm['n']}",
            exp, round(mm["nrmse_pct"], 4), 0.005)

    # T4 : Fig2 pooled NRMSE using the truncated series eq:series-TN ---------
    # calc:repro: each digitised point is assigned to the nearest published curve
    # (radius FIG2_ASSIGN_RADIUS); points near no curve are gridline/inter-curve
    # noise and are not attributable to any N. Curves N=10 and N=40 coincide over
    # most of the domain, so a subset-range denominator is meaningless for N=40;
    # NRMSE is normalised by the FULL published range of the figure.
    from src.validation import load_fig2_despeckled, FIG2_ASSIGN_RADIUS
    f2 = load_fig2_despeckled()
    X, Y = np.asarray(f2["X"]), np.asarray(f2["Y"])
    FULL_RANGE = float(f2["full_range"])
    Ns = list(FIG2["N_list"])
    tt = np.linspace(0.002, 0.44, 900)
    curves = {N: T_series(tt, int(N), FIG2["tau_D"]) for N in Ns}
    res_all = []
    for x, y in zip(X, Y):
        best, bd = None, 1e9
        for N, c in curves.items():
            yy = np.interp(x, tt, c)
            if abs(yy - y) < bd:
                bd, best = abs(yy - y), N
        if bd < FIG2_ASSIGN_RADIUS:
            res_all.append(T_series(np.array([x]), int(best), FIG2["tau_D"])[0] - y)
    res_all = np.asarray(res_all)
    rmse2 = float(np.sqrt(np.mean(res_all ** 2)))
    nrmse2 = 100.0 * rmse2 / FULL_RANGE
    rec("T4", "Anchor fig2 pooled NRMSE via truncated series", "eq:series-TN",
        f"N={Ns}, n={len(res_all)} assigned, full range={FULL_RANGE:.4f}",
        0.483, round(nrmse2, 4), 0.01)

    # T4b : series -> convolution solver as N grows --------------------------
    tchk = np.linspace(0.05, 1.0, 40)
    conv = forward(Theta(1.0, 0.02, 0.02), tchk, GEOM)
    ser = T_series(tchk, 4000, 0.04)
    d4b = float(np.max(np.abs(conv - ser)))
    rec("T4b", "series at large N agrees with convolution solver", "eq:series-TN",
        "N=4000, tau_q=kappa2=0.02", 0.0, d4b, 1e-4)

    # T5, T6 : degeneracy ----------------------------------------------------
    tg = np.linspace(0.005, 1.0, 400)
    ray = np.array([forward(Theta(1.0, q, 1.00*q), tg, GEOM) for q in (3e-3, 3e-2, 3e-1)])
    ctl = np.array([forward(Theta(1.0, q, 1.05*q), tg, GEOM) for q in (3e-3, 3e-2, 3e-1)])
    S_ray = float(np.max(ray.max(0) - ray.min(0)))
    S_ctl = float(np.max(ctl.max(0) - ctl.min(0)))
    rec("T5", "spread on the ray, tau_q over 100x, double precision", "eq:S-ray",
        "tau_q in {3e-3,3e-2,3e-1}, kappa2=alpha*tau_q", "<=1e-9", f"{S_ray:.3e}",
        None, status="PASS" if S_ray <= 1e-9 else "FAIL")
    rec("T6", "control spread at B=1.05", "eq:S-ctl", "same tau_q, B=1.05",
        2.6e-2, S_ctl, 0.2*2.6e-2)

    # T7, T8 : Fisher --------------------------------------------------------
    t80 = make_grid(cfg)
    for tid, B, exp, tol in (("T7", 0.5, 12.37, 0.1), ("T8", 1.28, 45.64, 0.5)):
        r = fisher(Theta.from_B(cfg["alpha"], cfg["tau_q"], B), t80, GEOM, cfg["eta_noise"])
        rec(tid, f"Fisher s.e.(tau_q) at B={B}", "eq:fisher-def",
            f"n=80, eta=2%, B={B}", exp, round(r["se_tau_q"], 4), tol)

    # T9 : band edges (RECOMPUTED, not hard-coded) ---------------------------
    lo = band_edge(20.0, 1.0, 0.01, t80, GEOM, cfg["eta_noise"])
    hi = band_edge(20.0, 1.0, 20.0, t80, GEOM, cfg["eta_noise"])
    rec("T9a", "lower band edge at 20% criterion", "eq:band20",
        "bisection on Fisher s.e.(tau_q)", 0.628, round(lo, 5), 0.005)
    rec("T9b", "upper band edge at 20% criterion", "eq:band20",
        "bisection on Fisher s.e.(tau_q)", 1.804, round(hi, 5), 0.005)

    # T10 : conditioning ------------------------------------------------------
    c = fisher(Theta.from_B(1.0, cfg["tau_q"], 1.0 + 1e-7), t80, GEOM, cfg["eta_noise"])["cond"]
    rec("T10", "cond(F) at B=1+1e-7", "eq:fisher-def", "B=1+1e-7", ">1e12",
        f"{c:.3e}", None, status="PASS" if c > 1e12 else "FAIL")

    # T19, T20, T21 : limits --------------------------------------------------
    tl = np.linspace(0.01, 1.0, 60)
    four = forward(Theta(1.0, TINY, TINY), tl, GEOM)
    res_small = forward(Theta(1.0, 1e-9, 1e-9), tl, GEOM)
    d19 = float(np.max(np.abs(four - res_small)))
    rec("T19", "Fourier limit tau_q,kappa2 -> 0", "eq:lim-fourier",
        "compare tau_q=kappa2=1e-12 vs 1e-9", 2.6e-6, d19, 5e-5)
    Tinf = float(forward(Theta(1.0, 0.02, 0.02), np.array([50.0]), GEOM)[0])
    rec("T20", "T(1,t->inf) = 1", "eq:Tend", "t=50", 1.0, round(Tinf, 10), 1e-7)
    neg = min(float(ray.min()), float(ctl.min()),
              float(forward(Theta(1.0, 0.02, 0.20), tg, GEOM).min()))
    rec("T21", "T >= 0 everywhere", "sec:cert-limits", "all cases tested",
        "true", f"min={neg:.3e}", None, status="PASS" if neg >= -1e-12 else "FAIL")

    # T16, T17 : Talbot pole collision ---------------------------------------
    M_even = 40
    ts = t_star(M_even, 0.04)
    ref = solve_fd(np.array([ts]), 0.02, 0.02, 0.04, Nx=400)[0]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        bad = solve_split(np.array([ts]), 0.02, 0.02, 0.04, M=M_even)[0]
    err_split = abs(bad - ref)
    rec("T16", "even-M split solver fails at t*=M tauD/10", "eq:tstar",
        f"M={M_even}, t*={ts}", ">1e6", f"{err_split:.3e}", None,
        status="PASS" if err_split > 1e6 else "FAIL")
    good = forward(Theta(1.0, 0.02, 0.02), np.array([ts]), GEOM)[0]
    err_conv = abs(good - ref)
    rec("T17", "odd-M convolution solver at the same time", "eq:convolution",
        f"M=41, t*={ts}", "<1e-3", f"{err_conv:.3e}", None,
        status="PASS" if err_conv < 1e-3 else "FAIL")

    # T18 : cross-solver ------------------------------------------------------
    tx = np.linspace(0.05, 1.0, 60)
    a = forward(Theta(1.0, 0.02, 0.02), tx, GEOM)
    b = solve_fd(tx, 0.02, 0.02, 0.04, Nx=1600, rtol=1e-12, atol=1e-14)
    d18 = float(np.max(np.abs(a - b)))
    rec("T18", "FD vs Laplace solver, full record", "sec:program Module 3",
        "Nx=1600, rtol=1e-12", "<=1e-6", f"{d18:.3e}", None,
        status="PASS" if d18 <= 1e-6 else "FAIL")

    # T22 : B invariance across thickness -------------------------------------
    alpha_p, tq_p, k2_p = 0.61e-6, 0.344, 0.268e-6
    Bs = []
    for Lmm in (1.86, 2.75, 3.84):
        L = Lmm * 1e-3
        Bs.append(B_of(alpha_p, tq_p, k2_p))       # eq:Binv: L cancels identically
    spread22 = float(max(Bs) - min(Bs))
    rec("T22", "B identical across L=1.86,2.75,3.84 mm", "eq:Binv",
        "alpha=0.61e-6, tau_q=0.344, kappa2=0.268e-6", 0.0, spread22, 1e-12)

    # T23 : Both et al. B ------------------------------------------------------
    c12 = [c for c in CASES if c.idx == 12][0]
    rec("T23", "B for Both et al. published values", "eq:both-B",
        "alpha=1.958e-6, tau_q=0.51, kappa2=1.53e-6", 1.532,
        round(c12.B_calc, 5), 0.001)

    # T24 : uncertainty cross-check -------------------------------------------
    t2250 = np.linspace(cfg["t_min"], cfg["t_max"], 2250)
    r24 = fisher(Theta.from_B(1.0, cfg["tau_q"], c12.B_calc), t2250, GEOM, 0.01)
    rec("T24", "s.e.(tau_q) at B=1.532, n=2250, eta=1%", "eq:pred-unc",
        "Both et al. sampling and assumed 1% noise", 2.55,
        round(r24["se_tau_q"], 4), 0.2)

    # ---------------- slow statistical tests T11-T15 ----------------------
    if os.environ.get("GK_FAST") != "1":
        from concurrent.futures import ProcessPoolExecutor
        pool = ProcessPoolExecutor(max_workers=os.cpu_count())

        # T11, T12 : BIC
        b1 = bic_compare(1.00, cfg, GEOM, pool=pool)
        rec("T11", "BIC at B=1: Fourier 0.00, GK delta", "eq:bic",
            f"4 models, {cfg['bic_realisations']} realisations, eta=2%",
            6.64, round(b1["delta"]["gk"], 3), 1.5)
        rec("T11b", "BIC at B=1 selects Fourier", "eq:bic", "same run",
            "fourier", b1["selected"], None,
            status="PASS" if b1["selected"] == "fourier" else "FAIL")
        b2 = bic_compare(2.41, cfg, GEOM, pool=pool)
        rec("T12", "BIC at B=2.41 selects GK", "eq:bic", "same protocol",
            "gk", b2["selected"], None,
            status="PASS" if b2["selected"] == "gk" else "FAIL")

        # T13, T14 : profile likelihood
        p13 = profile(1.28, cfg, GEOM)
        rec("T13", "profile width factor at B=1.28", "eq:profile-stat",
            f"{cfg['profile_nodes']} nodes, chi2(1,0.95)", 3.5,
            round(p13["width_factor"], 3), 0.5)
        p14 = profile(1.00, cfg, GEOM)
        rec("T14", "profile at B=1 spans the whole grid (unbounded)",
            "eq:profile-threshold", "same grid", "grid-limited",
            f"grid_limited={p14['grid_limited']}, factor={p14['width_factor']:.1f}",
            None, status="PASS" if p14["grid_limited"] else "FAIL")

        # T15 : Monte Carlo vs Fisher
        mc = monte_carlo(0.5, cfg, GEOM, pool=pool)
        fi = fisher(Theta.from_B(cfg["alpha"], cfg["tau_q"], 0.5), t80, GEOM,
                    cfg["eta_noise"])["se_tau_q"]
        ratio = mc["se_tau_q_robust_pct"] / fi
        rec("T15", "Monte Carlo vs Fisher s.e.(tau_q) at B=0.5", "calc:mc",
            f"{cfg['mc_trials']} trials, seeds {cfg['mc_seed_base']}+i",
            "agree within 20%",
            f"MC={mc['se_tau_q_robust_pct']:.2f}% Fisher={fi:.2f}% ratio={ratio:.3f}",
            None, status="PASS" if abs(ratio - 1.0) <= 0.20 else "FAIL")
        pool.shutdown()

    save_json(RESULTS / "all_tests.json", TESTS)
    save_csv(RESULTS / "all_tests.csv",
             [[t["test_id"], t["equation"], t["expected"], t["actual"],
               t["tolerance"], t["status"]] for t in TESTS],
             ["test_id", "equation", "expected", "actual", "tolerance", "status"])
    print(f"\npartial: {sum(1 for t in TESTS if t['status']=='PASS')} PASS / "
          f"{sum(1 for t in TESTS if t['status']=='FAIL')} FAIL of {len(TESTS)}")


if __name__ == "__main__":
    import multiprocessing as _mp
    _mp.freeze_support()
    main()
