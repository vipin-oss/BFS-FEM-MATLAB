"""Study 3 - thermal-relaxation sensitivity (blueprint §13, Fig. 6).

Model C, five declared tau0* values, frozen Study-1 Omega grid, free
phason / isothermal. Delta_T(Omega; tau0*) = |V(tau0*) - V(tau_ref*)| /
V(tau_ref*), tau_ref* = baseline tau0* (4.3462e-3, which is one of the
five values). If Delta_T sits at the resolution floor, the result is
reported as thermal insensitivity (a finding, not a failure) - the
floor eps_Delta is recorded in the CSV from results/resolution_bench.csv.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
from solver.material import Material
from solver import branch as br, record as rc

def main():
    with open(os.path.join(os.path.dirname(HERE), "grids.json")) as f:
        g3 = json.load(f)["study3"]
    Omegas = np.logspace(g3["Omega"]["start"], g3["Omega"]["stop"], g3["Omega"]["n"])
    bc = dict(phason=g3["bc"]["phason"], thermal=g3["bc"]["thermal"])
    m0 = Material()
    run = rc.run_id(); sh = rc.solver_version_hash()

    V = {}
    for tau in g3["tau0s"]:
        m = Material(overrides={"tau0": float(tau)})
        V[tau] = np.full(len(Omegas), np.nan)
        k_seed = None; r_prev = None
        for i, Om in enumerate(Omegas):
            out = br.solve_k_at_Omega(Om, g3["model"], m, bc, k_seed=k_seed, r_prev=r_prev)
            if out["Ok"]:
                V[tau][i] = out["V"]; k_seed, r_prev = out["k"], out["r"]
            else:
                k_seed = None; r_prev = None
        print(f"  tau0*={tau:g}: done", flush=True)

    tau_ref = 4.3462e-3
    Vref = V[tau_ref]
    # eps_Delta from the resolution benchmark
    eps = np.nan
    bench = os.path.join(os.path.dirname(HERE), "results", "resolution_bench.csv")
    if os.path.exists(bench):
        with open(bench) as f:
            lines = [l for l in f if not l.startswith("#")]
        hdr = lines[0].strip().split(",")
        eps = float(lines[1].strip().split(",")[hdr.index("eps_Delta")])

    header = ["run_id", "solver_hash", "Omega", "tau0", "V", "Delta_T",
              "above_floor"]
    rows = []
    for tau in g3["tau0s"]:
        dT = np.abs(V[tau] - Vref) / Vref
        for i, Om in enumerate(Omegas):
            above = (dT[i] * Vref[i] > eps) if np.isfinite(dT[i]) and np.isfinite(eps) else ""
            rows.append([run, sh, f"{Om:.10e}", f"{tau:.10e}",
                         f"{V[tau][i]:.12e}" if np.isfinite(V[tau][i]) else "NaN",
                         f"{dT[i]:.6e}" if np.isfinite(dT[i]) else "NaN", above])
    f6 = rc.write_csv("fig6_tau.csv", header, rows)
    np.savez(os.path.join(os.path.dirname(HERE), "results", "fig9c_map_dT.npz"),
             Omegas=Omegas, taus=np.array(g3["tau0s"]),
             dT=np.array([np.abs(V[t] - Vref) / Vref for t in g3["tau0s"]]))
    rc.manifest_entry(run, "study3_thermal", [os.path.basename(f6), "fig9c_map_dT.npz"],
                      extra={"eps_Delta": eps})
    dmax = np.nanmax([np.nanmax(np.abs(V[t] - Vref) / Vref) for t in g3["tau0s"]])
    print(f"max Delta_T over grid = {dmax:.3e}   eps_Delta = {eps:.3e}")
    print("Study 3 written:", f6)

if __name__ == "__main__":
    main()
