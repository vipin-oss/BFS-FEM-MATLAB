#!/usr/bin/env python3
"""P12B steering figure-of-merit sweep re-executed on the n = 16 production mesh.

Identical in *definition* to paper9/production/p12b_s7_theta_sweep.py (locked S7
extension): same theta grid {0,15,30,45,60,75,90} deg x AR in {5,10}, same ring
|k| = 0.5 pi / L, same phi sampling linspace(0, 2 pi, 73), same central-difference
step h = 1e-4, same branch 0, same post-processing conventions (mod-90 sector
argmax with tie-break, 3-point parabolic refinement, symmetry diagnostics).

Only the discretisation differs: the Bloch operator is the frozen n-order assembly
evaluated at n = 16 x 16 BFS elements per unit cell (the mesh-refinement repair of
the P5 production numbers), solved with the deterministic shift-invert ARPACK
solver of paper9/production/p5_mesh16_solver.py.

Output: paper9/results/raw/p12b_s7_theta_sweep_mesh16.json (default).

The same code path also serves the n = 8 comparison leg of the P5 mesh-repair audit: the optional
arguments --n-elem / --registry / --out select a different element count and its matching P5
registry, changing nothing else in the sweep definition.  Defaults reproduce the n = 16 run exactly.
"""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
PAPER9 = REPO_ROOT / "paper9"
sys.path.insert(0, str(PAPER9))

from solver.bfs_bloch_solver import L_plane, semi_axes_from_ar          # noqa: E402
from production.p5_mesh16_solver import (                                  # noqa: E402
    CaseAssembly, BlochEigensolver, DenseSubset,
)

N_ELEM = 16
THETA_GRID = (0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0)
AR_LIST = (5.0, 10.0)
H_FD = 1.0e-4
PHI_N = 73


def _git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"],
                                       cwd=str(REPO_ROOT)).decode().strip()
    except Exception:
        return "UNKNOWN"


def _env() -> dict:
    import numpy
    import scipy
    return {"python": sys.version.split()[0], "numpy": numpy.__version__,
            "scipy": scipy.__version__, "platform": platform.platform()}


def ring_delta(ca: CaseAssembly, solver: BlochEigensolver, k_rad: float, phi_grid: np.ndarray):
    """S7 locked quantity: unsigned deviation between v_g and k on the ring, branch 0."""
    delta, vg_mag, vp_mag, om0 = [], [], [], []
    for phi in phi_grid:
        kx, ky = k_rad * np.cos(phi), k_rad * np.sin(phi)
        kpts = np.array([[kx + H_FD, ky], [kx - H_FD, ky],
                         [kx, ky + H_FD], [kx, ky - H_FD], [kx, ky]])
        om = np.zeros((5, 4))
        for j in range(5):
            K, M = ca.matrices(float(kpts[j, 0]), float(kpts[j, 1]))
            lam, Y, res, ok = solver.solve(K, M)
            om[j, :] = np.sqrt(np.maximum(lam, 0.0))
        vg = np.array([(om[0, 0] - om[1, 0]) / (2.0 * H_FD),
                       (om[2, 0] - om[3, 0]) / (2.0 * H_FD)])
        kmag = float(np.hypot(kx, ky))
        vp = float(om[4, 0] / kmag) if kmag > 0 else 0.0
        delta.append(float(np.rad2deg(np.arccos(np.clip(
            np.dot(vg, [kx, ky]) / (np.linalg.norm(vg) * kmag), -1.0, 1.0)))))
        vg_mag.append(float(np.linalg.norm(vg)))
        vp_mag.append(vp)
        om0.append(vp * k_rad)
    return np.asarray(delta), vg_mag, vp_mag, om0


def run_sweep(n_elem: int = N_ELEM, registry_name: str = "p5_production_raw_mesh16.json",
              out_name: str = "p12b_s7_theta_sweep_mesh16.json") -> dict:
    """Run the locked S7 sweep at the requested element count.

    Only the mesh (and the P5 registry whose master parameters are adopted) may differ between
    invocations; every sweep-defining constant above is shared, so the n = 8 leg is the same
    measurement taken on a coarser discretisation.
    """
    t0 = time.time()
    registry_path = PAPER9 / "results" / "raw" / registry_name
    registry = json.loads(registry_path.read_text())
    mp = registry["master_params"]
    L = mp["Lcell"]
    lam, mu, rho = mp["lam"], mp["mu"], mp["rho"]
    ell2, l_iso = mp["ell2"], mp["l_iso"]
    assert L == 1.0 and (lam, mu, rho) == (1.0, 1.0, 1.0)
    assert ell2 == 0.04 and l_iso == 0.20
    assert mp["theta_sweep_deg"] == list(THETA_GRID)
    assert mp["N_elem_per_side"] == n_elem

    k_rad = 0.5 * np.pi / L
    phi_grid = np.linspace(0.0, 2.0 * np.pi, PHI_N)
    phi_deg = np.rad2deg(phi_grid)
    solver = BlochEigensolver(n_want=4, n_extra=2, sigma=1e-3, tol=1e-11, ncv=16,
                              tol_res=1e-10, n_elem=n_elem, fallback=DenseSubset(n_want=4))

    sweep = {}
    for AR in AR_LIST:
        l1, l2 = semi_axes_from_ar(AR, l_iso=l_iso, rule="volume_equivalent")
        for th_deg in THETA_GRID:
            L11, L22, L12 = L_plane(l1, l2, float(np.deg2rad(th_deg)))
            ca = CaseAssembly(n_elem, L, lam, mu, rho, ell2, L11, L22, L12)
            delta, vg_mag, vp_mag, om0 = ring_delta(ca, solver, k_rad, phi_grid)
            dmax = float(delta.max())
            i_all = np.flatnonzero(delta >= dmax * (1.0 - 1e-12))
            i0 = int(i_all[0])
            phi_star_sector = float(phi_deg[i0] % 90.0)
            q_vals = [float(delta[q * 18:(q + 1) * 18].max()) for q in range(4)]
            period_dev = float(max(q_vals) - min(q_vals))
            period_180_dev = float(np.max(np.abs(delta[36:72] - delta[:36])))
            q_peaks = [float(phi_deg[(delta == v).nonzero()[0][0]]) for v in q_vals]
            im = i0
            y0, y1, y2 = delta[(im - 1) % 72], delta[im], delta[(im + 1) % 72]
            denom = y0 - 2.0 * y1 + y2
            shift = 0.5 * (y0 - y2) / denom if abs(denom) > 0 else 0.0
            phi_refined = float((phi_deg[im] + shift * 5.0) % 90.0)
            key = f"AR_{AR:g}_th_{th_deg:g}"
            sweep[key] = {"AR": AR, "theta_deg": th_deg, "l1": l1, "l2": l2,
                          "delta_max_deg": dmax, "mean_delta_deg": float(delta.mean()),
                          "phi_star_deg": phi_star_sector,
                          "phi_star_refined_deg": phi_refined,
                          "quadrant_peak_phi_deg": q_peaks,
                          "period_90_max_dev_deg": period_dev,
                          "period_180_max_dev_deg": period_180_dev,
                          "phi_deg": phi_deg.tolist(), "delta_deg": delta.tolist(),
                          "vg_mag": vg_mag, "vp_mag": vp_mag, "omega_ring": om0}
            print(f"  {key}: delta_max = {dmax:12.6f} deg  phi* = {phi_star_sector:6.2f} deg "
                  f"(ref {phi_refined:9.4f})  180-deg dev = {period_180_dev:.2e}", flush=True)

    Ms = {}
    for AR in AR_LIST:
        p0 = sweep[f"AR_{AR:g}_th_0"]["phi_star_deg"]
        p90 = sweep[f"AR_{AR:g}_th_90"]["phi_star_deg"]
        Ms[f"AR_{AR:g}"] = {"AR": AR, "phi_star_theta0_deg": p0, "phi_star_theta90_deg": p90,
                            "M_s_deg": float(p90 - p0),
                            "M_s_refined_deg": float(sweep[f"AR_{AR:g}_th_90"]["phi_star_refined_deg"]
                                                     - sweep[f"AR_{AR:g}_th_0"]["phi_star_refined_deg"])}
        print(f"  M_s(AR={AR:g}) = {Ms[f'AR_{AR:g}']['M_s_deg']:+.4f} deg", flush=True)

    symmetry_checks = {}
    for AR in AR_LIST:
        entry = {"headless_180_max_dev_deg": max(
            sweep[f"AR_{AR:g}_th_{th:g}"]["period_180_max_dev_deg"] for th in THETA_GRID)}
        mirror = {}
        for th in (0.0, 15.0, 30.0):
            a = np.asarray(sweep[f"AR_{AR:g}_th_{th:g}"]["delta_deg"])
            b = np.asarray(sweep[f"AR_{AR:g}_th_{90.0 - th:g}"]["delta_deg"])
            idx = (18 - np.arange(PHI_N)) % 72
            mirror[f"th_{th:g}"] = float(np.max(np.abs(a - b[idx])))
        entry["mirror_delta(ph;th)=delta(90-ph;90-th)_max_dev_deg"] = mirror
        d0 = np.asarray(sweep[f"AR_{AR:g}_th_0"]["delta_deg"])
        d90 = np.asarray(sweep[f"AR_{AR:g}_th_90"]["delta_deg"])
        idx = (18 - np.arange(PHI_N)) % 72
        entry["theta0_vs_theta90_direct_max_dev_deg"] = float(np.max(np.abs(d90 - d0)))
        entry["theta0_vs_theta90_mirrored_max_dev_deg"] = float(np.max(np.abs(d90 - d0[idx])))
        entry["delta_max_th_eq_90mth_max_dev_deg"] = float(max(
            abs(sweep[f"AR_{AR:g}_th_{th:g}"]["delta_max_deg"]
                - sweep[f"AR_{AR:g}_th_{90.0 - th:g}"]["delta_max_deg"]) for th in (0.0, 15.0, 30.0)))
        symmetry_checks[f"AR_{AR:g}"] = entry

    anchor_key = ("anchor_check_vs_p5_mesh16" if registry_name == "p5_production_raw_mesh16.json"
                  else f"anchor_check_vs_{Path(registry_name).stem}")
    anchor = {}
    s7 = registry["study_S7_ifc_steering"]
    for key in ("AR_5_th_45", "AR_10_th_45"):
        old_v = float(s7[key]["delta_max_deg"])
        new_v = sweep[key]["delta_max_deg"]
        rel = abs(new_v - old_v) / abs(old_v)
        anchor[key] = {"p5_mesh16_delta_max_deg": old_v, "p12b_mesh16_delta_max_deg": new_v,
                       "rel_diff": rel, "pass_lt_1e-9": bool(rel < 1e-9)}
        print(f"  anchor {key}: P5-mesh16 {old_v:.12f} vs sweep {new_v:.12f} rel {rel:.2e}", flush=True)

    doc = {
        "study": (f"P12B S7 steering figure-of-merit theta sweep on the n = {n_elem} "
                  "production mesh"),
        "status": "PRODUCTION (mesh-refined P5 basis; S7 methodology)",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "git_commit": _git_commit(),
        "master_params_source": f"paper9/results/raw/{registry_name}::master_params",
        "master_params": mp,
        "master_params_sha256": hashlib.sha256(json.dumps(mp, sort_keys=True).encode()).hexdigest(),
        "definitions": {
            "phi_star_deg": ("argmax over the locked S7 ring sampling phi in linspace(0, 2 pi, 73) "
                             "of the S7 unsigned group-velocity deviation delta(phi; theta, AR), "
                             "reduced modulo the verified 90 deg period of the field, i.e. "
                             "phi* = (discrete argmax delta) mod 90 in [0, 90) deg; tie-break: "
                             "smallest representative among values within 1e-12 relative of the maximum"),
            "M_s_deg": "M_s(AR) = phi*(90 deg, AR) - phi*(0 deg, AR), on the locked grid",
            "delta_definition": ("S7 locked: unsigned angle between v_g = grad_k omega and k, "
                                 "branch 0 (first acoustic branch), central differences h = 1e-4"),
            "ring": "|k| = k_rad = 0.5 * pi / L",
            "sampling": "phi = linspace(0, 2 pi, 73) endpoints included (5 deg step)",
            "theta_grid_deg": list(THETA_GRID), "AR_list": list(AR_LIST),
        },
        "discretisation": {"N_elem_per_side": n_elem, "DOF": 8 * n_elem * n_elem,
                           "assembly": f"frozen n-order BFS assembly at n = {n_elem}",
                           "eigensolver": "shift-invert ARPACK, fixed analytic start, tol=1e-11, ncv=16"},
        "solver_calls": {"k_rad": k_rad, "phi_n_points": PHI_N, "branch": 0, "fd_step_h": H_FD,
                         "solves": 5 * PHI_N * len(THETA_GRID) * len(AR_LIST)},
        "sweep": sweep, "symmetry_checks": symmetry_checks, "M_s": Ms,
        anchor_key: anchor,
        "wall_time_s": time.time() - t0,
        "environment": _env(),
    }
    out = PAPER9 / "results" / "raw" / out_name
    out.write_text(json.dumps(doc, indent=1))
    print(f"\nwrote {out}\nwall time: {doc['wall_time_s']:.1f} s")
    return doc


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="locked S7 steering sweep at a chosen element count")
    ap.add_argument("--n-elem", type=int, default=N_ELEM,
                    help="BFS elements per cell side (default 16; 8 produces the comparison leg)")
    ap.add_argument("--registry", default="p5_production_raw_mesh16.json",
                    help="P5 production registry under paper9/results/raw/ whose master_params are adopted")
    ap.add_argument("--out", default="p12b_s7_theta_sweep_mesh16.json",
                    help="output file name under paper9/results/raw/")
    a = ap.parse_args()
    run_sweep(n_elem=a.n_elem, registry_name=a.registry, out_name=a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
