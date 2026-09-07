"""Numerical resolution benchmark (architecture item 10; blueprint §12).

Resolution is NOT defined by a +/-1e-10 parameter perturbation (that is
kept only as an auxiliary sensitivity probe). The operational measures:

  r_floor : residual sigma_min(B)/||B|| at the converged branch point;
  u_V     : velocity uncertainty from REFINEMENT - the difference of V*
            between the production refinement level and a doubled-scan
            level (all tolerances unchanged);
  eps_Delta : comparison threshold for any velocity difference
            (e.g. Delta_BC, Delta_T): eps_Delta = eps_mult * max(u_V)
            over the frozen benchmark points (eps_mult = 10, frozen in
            params.json). Differences below eps_Delta are reported as
            "indistinguishable within numerical resolution".

Results are written to results/resolution_bench.csv and returned.
"""
import os
import numpy as np
from . import branch as br

def benchmark(points, m, bc, out_csv=None):
    d = m.defaults
    eps_mult = float(d["eps_Delta_multiplier"])
    rows = []
    for model, Om in points:
        out1 = br.solve_k_at_Omega(Om, model, m, bc)
        out2 = br.solve_k_at_Omega(Om, model, m, bc, n_scan=3 * int(d["n_scan"]))
        uV = abs(out2["V"] - out1["V"]) if out1["Ok"] and out2["Ok"] else np.nan
        # auxiliary perturbation probe (NOT the definition): relative
        # response of V* to a 1e-10 relative change of Omega
        outp = br.solve_k_at_Omega(Om * (1 + 1e-10), model, m, bc)
        sens = (abs(outp["V"] - out1["V"]) / out1["V"] / 1e-10
                if out1["Ok"] and outp["Ok"] else np.nan)
        rows.append(dict(model=model, Omega=Om,
                         V_L1=out1["V"], V_L2=out2["V"], u_V=uV,
                         r_L1=out1["r"], r_L2=out2["r"],
                         condB_L1=out1["condB"], aux_dVdOm_rel=sens,
                         status=out1["status"]))
    uVs = np.array([r["u_V"] for r in rows], dtype=float)
    eps_Delta = eps_mult * np.nanmax(uVs)
    for r in rows:
        r["eps_Delta"] = eps_Delta
    if out_csv:
        os.makedirs(os.path.dirname(out_csv), exist_ok=True)
        cols = ["model", "Omega", "V_L1", "V_L2", "u_V", "r_L1", "r_L2",
                "condB_L1", "aux_dVdOm_rel", "status", "eps_Delta"]
        with open(out_csv, "w") as f:
            f.write("# resolution benchmark: u_V from scan refinement "
                    "(production vs 3x scan); eps_Delta = "
                    f"{eps_mult:g} * max(u_V); aux probe NOT a definition\n")
            f.write(",".join(cols) + "\n")
            for r in rows:
                f.write(",".join(
                    f"{r[c]:.12e}" if isinstance(r[c], float) else str(r[c])
                    for c in cols) + "\n")
    return rows, eps_Delta
