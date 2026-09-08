"""Anchor reproduction only (sec:anchor / calc:repro). No fitting."""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.model import Theta, Geometry
from src.forward import forward
from src.limits import T_series
from src.validation import (load_digitised, load_fig2_despeckled, metrics,
                            ANCHOR_CASES, FIG2, FIG2_ASSIGN_RADIUS)
from src.io import save_json, RESULTS

GEOM = Geometry(1.0, 0.04)
out = {}
print("=" * 92)
print("VALIDATION AGAINST THE PUBLISHED ANCHOR (external validation of the forward operator)")
print("Published parameters used verbatim. No fitting, no tuning. (calc:repro)")
print("=" * 92)
print(f"{'figure':>7} {'n':>6} {'RMSE':>10} {'NRMSE %':>9} {'sigma_d':>9} "
      f"{'RMSE/sd':>8} {'<=2sd %':>8}")
for nm in ("fig3", "fig5"):
    p = ANCHOR_CASES[nm]
    x, y, sd = load_digitised(nm)
    k = x <= p["tmax"]; x, y = x[k], y[k]
    ours = forward(Theta(1.0, p["tau_q"], p["kappa2"]), x, GEOM)
    m = metrics(y, ours, sd); out[nm] = m
    print(f"{nm:>7} {m['n']:>6} {m['rmse']:>10.5f} {m['nrmse_pct']:>9.3f} "
          f"{sd:>9.5f} {m['rmse_over_sigma_d']:>8.2f} {m['within_2sigma_pct']:>8.1f}")

f2 = load_fig2_despeckled()
X, Y = np.asarray(f2["X"]), np.asarray(f2["Y"]); FR = float(f2["full_range"])
tt = np.linspace(0.002, 0.44, 900)
curves = {N: T_series(tt, int(N), FIG2["tau_D"]) for N in FIG2["N_list"]}
res, per = [], {}
for x, y in zip(X, Y):
    best, bd = None, 1e9
    for N, c in curves.items():
        yy = np.interp(x, tt, c)
        if abs(yy - y) < bd:
            bd, best = abs(yy - y), N
    if bd < FIG2_ASSIGN_RADIUS:
        r = T_series(np.array([x]), int(best), FIG2["tau_D"])[0] - y
        res.append(r); per.setdefault(best, []).append(r)
res = np.asarray(res)
rmse = float(np.sqrt(np.mean(res ** 2)))
out["fig2"] = {"n": int(len(res)), "rmse": rmse,
               "nrmse_pct_full_range": 100 * rmse / FR, "full_range": FR,
               "per_N": {str(N): {"n": len(v),
                                  "rmse": float(np.sqrt(np.mean(np.square(v))))}
                         for N, v in sorted(per.items())}}
print(f"{'fig2':>7} {len(res):>6} {rmse:>10.5f} "
      f"{100*rmse/FR:>9.3f}   (normalised by the full figure range {FR:.4f})")
for N, v in sorted(per.items()):
    print(f"        N={N:<3} n={len(v):>4} RMSE={float(np.sqrt(np.mean(np.square(v)))):.6f}")
save_json(RESULTS / "validation_results.json", out)
print("\nNOTE: this validates the FORWARD operator only. It does not validate")
print("the inverse problem, and no experimental validation is claimed.")
