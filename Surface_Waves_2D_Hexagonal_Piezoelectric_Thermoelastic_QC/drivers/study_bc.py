"""Study BC - phason boundary condition comparison (blueprint §12, Fig. 7).

Models A and C; free phason (H_xz = H_zz = 0) vs clamped phason
(w_x = w_z = 0); mechanical and thermal rows unchanged; frozen Study-1
Omega grid. Outputs relative velocity difference DeltaV/V and
penetration-depth difference.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
from solver.material import Material
from solver import branch as br, diagnostics as dg, record as rc

def main():
    with open(os.path.join(os.path.dirname(HERE), "grids.json")) as f:
        g = json.load(f)["bc_study"]
    Omegas = np.logspace(g["Omega"]["start"], g["Omega"]["stop"], g["Omega"]["n"])
    m = Material()
    run = rc.run_id(); sh = rc.solver_version_hash()

    header = ["run_id", "solver_hash", "model", "bc_phason", "Omega", "k", "V",
              "r", "status", "delta_pen"]
    rows = []
    V = {}; PEN = {}
    for model in g["models"]:
        for var in g["variants"]:
            bc = dict(phason=var["phason"], thermal=var["thermal"])
            key = (model, var["phason"])
            V[key] = np.full(len(Omegas), np.nan)
            PEN[key] = np.full(len(Omegas), np.nan)
            k_seed = None; r_prev = None
            for i, Om in enumerate(Omegas):
                out = br.solve_k_at_Omega(Om, model, m, bc, k_seed=k_seed, r_prev=r_prev)
                if out["Ok"]:
                    k_seed, r_prev = out["k"], out["r"]
                    V[key][i] = out["V"]
                    pen = dg.penetration(out["k"], Om, model, m, bc)
                    PEN[key][i] = pen["delta"]
                    rows.append([run, sh, model, var["phason"], f"{Om:.10e}",
                                 f"{out['k']:.12e}", f"{out['V']:.12e}",
                                 f"{out['r']:.6e}", out["status"], f"{pen['delta']:.6e}"])
                else:
                    k_seed = None; r_prev = None
                    rows.append([run, sh, model, var["phason"], f"{Om:.10e}",
                                 "NaN", "NaN", "NaN", "no_branch", "NaN"])
            print(f"  {model}/{var['phason']}: done", flush=True)

    f7 = rc.write_csv("fig7_bc.csv", header, rows)
    # summary deltas
    hs = ["Omega"]
    rs_ = [[] for _ in Omegas]
    for model in g["models"]:
        dV = np.abs(V[(model, "clamped")] - V[(model, "free")]) / np.abs(V[(model, "free")])
        dP = np.abs(PEN[(model, "clamped")] - PEN[(model, "free")]) / np.abs(PEN[(model, "free")])
        hs += [f"dV_over_V_{model}", f"dPen_{model}"]
        for i in range(len(Omegas)):
            rs_[i] += [f"{dV[i]:.6e}", f"{dP[i]:.6e}"]
    f7s = rc.write_csv("fig7_bc_summary.csv", hs,
                       [[f"{Om:.10e}"] + r for Om, r in zip(Omegas, rs_)])
    rc.manifest_entry(run, "study_bc", [os.path.basename(f7), os.path.basename(f7s)])
    print("Study BC written:", f7, f7s)

if __name__ == "__main__":
    main()
