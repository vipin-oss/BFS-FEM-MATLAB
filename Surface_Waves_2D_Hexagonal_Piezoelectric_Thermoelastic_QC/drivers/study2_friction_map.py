"""Study 2 - controlled phason-friction sensitivity (blueprint §11/H2).

Map: models B and C over the frozen 61x61 grid (Omega = 10^-3..10^2,
D_w* = 10^-2..10^4), free phason / isothermal, production route with
continuation in Omega at each D_w*. Primary output Delta_BC(Omega, D_w*),
supporting output V*(Omega, D_w*). Omega_c = D_w*/rho_w* is a REFERENCE
LINE only (never a claimed transition). Incremental CSV (flushed per
row) so a long run can be resumed/inspected; converted to npz at the end.

Fig. 5 (1D slices at D_w* = 10^0, 10^2, 10^4, models A/B/C) is written
from the same map rows plus a short model-A sweep (A is D_w-independent).
"""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
from solver.material import Material
from solver import branch as br, record as rc

def main():
    with open(os.path.join(os.path.dirname(HERE), "grids.json")) as f:
        g2 = json.load(f)["study2"]
    Omegas = np.logspace(g2["Omega"]["start"], g2["Omega"]["stop"], g2["Omega"]["n"])
    Dws = np.logspace(g2["Dw"]["start"], g2["Dw"]["stop"], g2["Dw"]["n"])
    bc = dict(phason=g2["bc"]["phason"], thermal=g2["bc"]["thermal"])
    m0 = Material()
    run = rc.run_id(); sh = rc.solver_version_hash()
    out_csv = os.path.join(os.path.dirname(HERE), "results", "study2_map_incremental.csv")
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)

    # resume support: skip (model, iDw) combos already complete
    done = set()
    if os.path.exists(out_csv):
        with open(out_csv) as f:
            next(f)
            seen = {}
            for line in f:
                p = line.split(",")
                key = (p[2], p[3])
                seen[key] = seen.get(key, 0) + 1
            for key, n in seen.items():
                if n >= len(Omegas):
                    done.add(key)
        print(f"resume: {len(done)} (model,iDw) rows already complete", flush=True)

    hdr_written = os.path.exists(out_csv) and os.path.getsize(out_csv) > 0
    f = open(out_csv, "a")
    if not hdr_written:
        f.write("run_id,solver_hash,model,i_Dw,Dw,Omega,k,V,r,status,jump\n")

    t0 = time.time()
    for model in ("B", "C"):
        for iDw, Dw in enumerate(Dws):
            if (model, str(iDw)) in done:
                continue
            m = Material(overrides={"Dw": float(Dw)})
            k_seed = None; r_prev = None
            for Om in Omegas:
                out = br.solve_k_at_Omega(Om, model, m, bc, k_seed=k_seed, r_prev=r_prev)
                if out["Ok"]:
                    k_seed, r_prev = out["k"], out["r"]
                    f.write(f"{run},{sh},{model},{iDw},{Dw:.10e},{Om:.10e},"
                            f"{out['k']:.12e},{out['V']:.12e},{out['r']:.6e},"
                            f"{out['status']},{int(out['jump'])}\n")
                else:
                    k_seed = None; r_prev = None
                    f.write(f"{run},{sh},{model},{iDw},{Dw:.10e},{Om:.10e},"
                            f"NaN,NaN,NaN,no_branch,0\n")
            f.flush()
            print(f"{model} D_w*={Dw:.4g} done ({time.time()-t0:.0f}s)", flush=True)
    f.close()

    # ---- assemble map + Fig. 5 ----
    nO, nD = len(Omegas), len(Dws)
    Vm = {mm: np.full((nD, nO), np.nan) for mm in ("B", "C")}
    with open(out_csv) as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\n").split(",")
            mm, iDw, iOm = p[2], int(p[3]), None
            Om = float(p[5])
            iOm = int(np.argmin(np.abs(Omegas - Om)))
            Vm[mm][iDw, iOm] = float(p[7]) if p[7] != "NaN" else np.nan
    dBC = np.abs(Vm["B"] - Vm["C"]) / np.abs(Vm["C"])
    npz = os.path.join(os.path.dirname(HERE), "results", "fig9b_map_dBC.npz")
    np.savez(npz, Omegas=Omegas, Dws=Dws, V_B=Vm["B"], V_C=Vm["C"], dBC=dBC,
             Omega_c_ref=Dws / m0.rho_w)
    # Fig. 5: 1D slices, models A/B/C at D_w* in {1e0, 1e2, 1e4}
    m = Material()
    VA = np.full(nO, np.nan)
    k_seed = None; r_prev = None
    for i, Om in enumerate(Omegas):
        out = br.solve_k_at_Omega(Om, "A", m, bc, k_seed=k_seed, r_prev=r_prev)
        if out["Ok"]:
            VA[i] = out["V"]; k_seed, r_prev = out["k"], out["r"]
        else:
            k_seed = None; r_prev = None
    h5 = ["Omega", "Dw", "model", "V", "Delta_BC_at_Dw"]
    r5 = []
    for Dwv in (1e0, 1e2, 1e4):
        iD = int(np.argmin(np.abs(Dws - Dwv)))
        dsl = np.abs(Vm["B"][iD] - Vm["C"][iD]) / np.abs(Vm["C"][iD])
        for i, Om in enumerate(Omegas):
            for mm, VV in (("A", VA[i]), ("B", Vm["B"][iD, i]), ("C", Vm["C"][iD, i])):
                r5.append([f"{Om:.10e}", f"{Dws[iD]:.6e}", mm, f"{VV:.12e}", f"{dsl[i]:.6e}"])
    f5 = rc.write_csv("fig5_friction1d.csv", h5, r5)
    rc.manifest_entry(run, "study2_friction_map",
                      ["study2_map_incremental.csv", os.path.basename(npz),
                       os.path.basename(f5)])
    print("Study 2 written:", npz, f5)

if __name__ == "__main__":
    main()
