"""Depth-root diagnostics (blueprint §10, Fig. 8 data).

All 10 depth roots at three frequencies for models A, B, C: Re p, Im p,
admissibility, grazing flag, per-root residual, ordering index, plus the
dominant penetration depth delta* = 1/|Im p_j| (a depth-localisation
measure, NOT attenuation) and phason participation P_w (amplitude ratio,
not energy).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
from solver.material import Material
from solver import roots as rt, diagnostics as dg, record as rc, branch as br

def main():
    with open(os.path.join(os.path.dirname(HERE), "grids.json")) as f:
        g = json.load(f)["roots_diag"]
    m = Material()
    bc = dict(phason="free", thermal="isothermal")
    run = rc.run_id(); sh = rc.solver_version_hash()
    header = ["run_id", "solver_hash", "model", "Omega", "root_index",
              "Re_p", "Im_p", "admissible", "grazing", "root_residual"]
    rows = []
    hdr2 = ["model", "Omega", "n_ad", "n_grazing", "delta_pen", "P_w",
            "k_branch", "V_branch", "r_branch"]
    rows2 = []
    for model in g["models"]:
        for Om in g["Omega"]:
            rr = rt.depth_roots(2.0 * Om, Om, model, m)   # k on the branch line
            res_ad = {int(i): rv for i, rv in zip(rr["idx_ad"], rr["root_residuals"])}
            for j in range(len(rr["p_all"])):
                p = rr["p_all"][j]
                rows.append([run, sh, model, f"{Om:.6e}", j,
                             f"{p.real:.12e}", f"{p.imag:.12e}",
                             int(j in set(int(i) for i in rr["idx_ad"])),
                             int(j in set(int(i) for i in rr["idx_grazing"])),
                             f"{res_ad[j]:.3e}" if j in res_ad else "NaN"])
            # branch point at this Omega for context + diagnostics
            out = br.solve_k_at_Omega(Om, model, m, bc)
            if out["Ok"]:
                pen = dg.penetration(out["k"], Om, model, m, bc)
                pw = dg.participation(out["k"], Om, model, m, bc)
                rows2.append([model, f"{Om:.6e}", out["n_ad"], out["n_grazing"],
                              f"{pen['delta']:.6e}", f"{pw['P_w']:.6e}",
                              f"{out['k']:.12e}", f"{out['V']:.12e}", f"{out['r']:.3e}"])
            print(f"  {model} Om={Om:g}: n_ad={rr['n_ad']} n_grz={rr['n_grazing']}", flush=True)
    f8 = rc.write_csv("fig8_roots.csv", header, rows)
    f8s = rc.write_csv("fig8_roots_summary.csv", hdr2, rows2)
    rc.manifest_entry(run, "roots_diag", [os.path.basename(f8), os.path.basename(f8s)])
    print("Roots diagnostics written:", f8, f8s)

if __name__ == "__main__":
    main()
