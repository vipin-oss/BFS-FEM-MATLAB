"""Study 1 - baseline dispersion (blueprint §11, Figs. 3-4 data).

Models A, B, C on the frozen Study-1 grid (Omega = 10^-3..10^3, 121 log
points), free phason / isothermal, PRODUCTION route with continuation.
Full raw record per point (params implied by manifest, model, Omega, k*,
V*, residual, root/admissibility data, diagnostics, tolerances, solver
hash, run ID). Deltas Delta_BC/Delta_AC/Delta_AB computed here from the
same run and written alongside. Plots read these CSVs only.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
from solver.material import Material
from solver import branch as br, diagnostics as dg, record as rc

def main():
    with open(os.path.join(os.path.dirname(HERE), "grids.json")) as f:
        g1 = json.load(f)["study1"]
    Omegas = np.logspace(g1["Omega"]["start"], g1["Omega"]["stop"], g1["Omega"]["n"])
    bc = dict(phason=g1["bc"]["phason"], thermal=g1["bc"]["thermal"])
    m = Material()
    run = rc.run_id(); sh = rc.solver_version_hash()

    header = ["run_id", "solver_hash", "model", "bc_phason", "bc_thermal",
              "Omega", "k", "V", "r", "status", "n_ad", "n_grazing", "condB",
              "jump", "root_flags", "max_root_res", "k_comp", "r_comp",
              "P_w", "delta_pen", "delta_pen_weighted", "rel_xtol", "n_scan"]
    rows = {mod: [] for mod in g1["models"]}
    V = {}
    for model in g1["models"]:
        V[model] = np.full(len(Omegas), np.nan)
        k_seed = None; r_prev = None
        for i, Om in enumerate(Omegas):
            out = br.solve_k_at_Omega(Om, model, m, bc, k_seed=k_seed, r_prev=r_prev)
            if out["Ok"]:
                k_seed, r_prev = out["k"], out["r"]
                V[model][i] = out["V"]
                pw = dg.participation(out["k"], Om, model, m, bc)
                pen = dg.penetration(out["k"], Om, model, m, bc)
                rows[model].append([run, sh, model, bc["phason"], bc["thermal"],
                                    f"{Om:.10e}", f"{out['k']:.12e}", f"{out['V']:.12e}",
                                    f"{out['r']:.6e}", out["status"], out["n_ad"],
                                    out["n_grazing"], f"{out['condB']:.6e}", int(out["jump"]),
                                    out["root_flags"], f"{out['max_root_res']:.3e}",
                                    f"{out['k_comp']:.12e}", f"{out['r_comp']:.6e}",
                                    f"{pw['P_w']:.6e}", f"{pen['delta']:.6e}",
                                    f"{pen['delta_weighted']:.6e}", "1e-15", m.defaults["n_scan"]])
            else:
                k_seed = None; r_prev = None
                rows[model].append([run, sh, model, bc["phason"], bc["thermal"],
                                    f"{Om:.10e}", "NaN", "NaN", "NaN", "no_branch",
                                    0, 0, "NaN", 0, 0, "NaN", "NaN", "NaN",
                                    "NaN", "NaN", "NaN", "1e-15", m.defaults["n_scan"]])
        print(f"  model {model}: done", flush=True)

    f3 = rc.write_csv("study1_baseline.csv", header,
                      [r for mod in g1["models"] for r in rows[mod]])
    # Fig. 4 data: deltas from the same run
    dBC = np.abs(V["B"] - V["C"]) / np.abs(V["C"])
    dAC = np.abs(V["A"] - V["C"]) / np.abs(V["C"])
    dAB = np.abs(V["A"] - V["B"]) / np.abs(V["B"])
    h4 = ["Omega", "V_A", "V_B", "V_C", "Delta_BC", "Delta_AC", "Delta_AB"]
    r4 = [[f"{Om:.10e}"] + [f"{x:.12e}" for x in vals]
          for Om, vals in zip(Omegas, zip(V["A"], V["B"], V["C"], dBC, dAC, dAB))]
    f4 = rc.write_csv("fig4_deltas.csv", h4, r4)
    rc.manifest_entry(run, "study1_baseline", [os.path.basename(f3), os.path.basename(f4)])
    print("Study 1 written:", f3, f4)

if __name__ == "__main__":
    main()
