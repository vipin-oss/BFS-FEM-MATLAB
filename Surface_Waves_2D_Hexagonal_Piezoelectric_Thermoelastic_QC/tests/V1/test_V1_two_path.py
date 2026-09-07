"""V1 - F2 GATING TEST: two-path consistency.

Production route: prescribed real Omega -> solve real positive k* -> V*.
Alternate route : prescribed real k* -> solve real positive Omega -> V*.
Compared at the anchors declared in grids.json (Omega = 0.01..100, models
A/B/C). Tolerance: the blueprint's branch-point velocity accuracy target,
1e-8 relative on V* (no new tolerance invented).

MUST PASS before any physics sweep (task §3). On failure: prints the
diagnostic record and exits nonzero - STOP, do not proceed.
"""
import json, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver.material import Material
from solver import branch as br

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grids = json.load(open(os.path.join(ROOT, "grids.json")))
anchors = grids["two_path"]["Omega"]
models = grids["two_path"]["models"]
TOL = 1e-8   # blueprint §10: branch-point velocity accuracy target

m = Material()
bc = {"phason": "free", "thermal": "isothermal"}
rows = []
fails = []
for model in models:
    k_seed = None
    for Om in anchors:
        prod = br.solve_k_at_Omega(Om, model, m, bc, k_seed=k_seed)
        if not prod["Ok"]:
            fails.append(f"{model} Om={Om}: production route found no branch (r={prod['r']})")
            rows.append((model, Om, np.nan, np.nan, np.nan, np.nan, "no_branch"))
            continue
        k_seed = prod["k"]
        alt = br.solve_Omega_at_k(prod["k"], model, m, bc, Om_seed=Om)
        if not alt["Ok"]:
            fails.append(f"{model} Om={Om}: alternate route failed")
            rows.append((model, Om, prod["k"], prod["V"], np.nan, np.nan, "alt_fail"))
            continue
        dv = abs(alt["V"] - prod["V"]) / prod["V"]
        status = "OK" if dv <= TOL else "MISMATCH"
        if dv > TOL:
            fails.append(f"{model} Om={Om}: dV/V = {dv:.3e} > {TOL:.0e} "
                         f"(prod V={prod['V']:.12g} r={prod['r']:.2e}; "
                         f"alt V={alt['V']:.12g} r={alt['r']:.2e}; k*={prod['k']:.12g})")
        rows.append((model, Om, prod["k"], prod["V"], alt["V"], dv, status))

print("model  Omega        k*            V*_prod        V*_alt         |dV|/V      status")
for r in rows:
    print(f"{r[0]:5s} {r[1]:<10g} {r[2]:<13.8g} {r[3]:<14.10g} {r[4]:<14.10g} {r[5]:<10.2e} {r[6]}")
print()
if fails:
    print("V1 two-path: FAIL -- STOP (do not proceed to physics sweeps)")
    for f_ in fails:
        print("  ", f_)
    sys.exit(1)
print("V1 two-path: PASS (15/15 anchors within 1e-8 relative on V*)")
