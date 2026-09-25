#!/usr/bin/env python3
"""P5 production re-run at n = 16 BFS elements per unit cell (mesh-refinement repair).

Same frozen formulation, materials, parameters, k-path (Gamma-X-M-Gamma, 40
segments, 121 nodes), half-BZ grid (41 x 81 = 3321 points), band count (4) and
42 (theta, AR) design-map points as the historical production; only the element
size changes (h = Lcell / n, n = 1 historically, n = 16 here).  No rescaling, no
correction factor, no stochastic eigensolver start.

Eigensolver: production/p5_mesh16_solver.BlochEigensolver (shift-invert ARPACK
on T = (K + sigma M)^-1 M with a fixed analytic start vector, M-normalised Ritz
vectors, Rayleigh-quotient eigenvalues, backward-error gate, exact dense
escalation).  Assembly: production/p5_mesh16_solver.CaseAssembly, verified against
the frozen assemble_nxn_bloch to <= 1.2e-13.

Usage
    python3 production/run_p5_mesh16_production.py compute  --workers 2
    python3 production/run_p5_mesh16_production.py assemble

Outputs (new files; the historical n = 1 artefacts are never modified)
    results/raw/p5_production_raw_mesh16.json            (+ _mesh16_grid.npz)
    results/processed/table5_gap_summary_mesh16.json
    results/processed/p5_production_highlights_mesh16.json
    audit/evidence/p5_mesh16/run_log_mesh16.txt
"""
from __future__ import annotations

import os as _os
# Single-threaded BLAS before numpy loads: two worker processes on two cores.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    _os.environ.setdefault(_v, "1")

import argparse
import hashlib
import json
import multiprocessing as mp
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

from solver.bfs_bloch_solver import (                                     # noqa: E402
    L_plane, semi_axes_from_ar, build_path_k, build_half_bz_grid, compute_gaps,
)
from production.p5_mesh16_solver import (                                 # noqa: E402
    CaseAssembly, BlochEigensolver, DenseSubset,
)

N_ELEM = 16
N_BANDS = 4
N_KEEP = 6                     # requested modes: 4 claim-bearing + 2 margin
CKPT_DEFAULT = Path("/home/user/p5_repair/checkpoints")

PARAMS = {
    "Lcell": 1.0,
    "lam": 1.0,
    "mu": 1.0,
    "rho": 1.0,
    "ell2": 0.04,
    "l_iso": 0.20,
    "theta_sweep_deg": [0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0],
    "ar_sweep": [1.0, 2.0, 3.0, 5.0, 7.0, 10.0],
    "N_seg": 40,
    "N_kx": 41,
    "N_ky": 81,
    "N_bands": N_BANDS,
    "tol_herm": 1.0e-12,
    "eps_Delta": 4.63e-11,
    "N_elem_per_side": N_ELEM,
    "elem_size_h": 1.0 / N_ELEM,
    "dof_per_cell": 8 * N_ELEM * N_ELEM,
    "assembly": "frozen BFS n-order assembly (n x n elements per cell) at n=16",
    "eigensolver": ("shift-invert ARPACK on T=(K+sigma*M)^-1 M, which='LM', fixed analytic "
                    "start vector, tol=1e-11, ncv=16, k=8, M-normalised Ritz vectors, "
                    "Rayleigh-quotient eigenvalues, backward-error gate 1e-10"),
    "eigensolver_shift_sigma": 1.0e-3,
    "eigensolver_n_extra_modes": 2,
    "eigensolver_tol": 1.0e-11,
    "eigensolver_ncv": 16,
    "eigensolver_backward_error_tol": 1.0e-10,
    "modes_reported_per_k": N_KEEP,
}
S1_CASES = [(1.0, 0.0), (1.0, 45.0), (10.0, 0.0), (10.0, 45.0)]
S7_CASES = [(1.0, 0.0), (5.0, 45.0), (10.0, 45.0)]
S7_PHI = np.linspace(0.0, 2.0 * np.pi, 73)
S7_H = 1.0e-4


def case_name(ar, th):
    return f"AR_{int(ar)}_th_{int(th)}"


def git_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT),
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "UNKNOWN"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def new_solver():
    return BlochEigensolver(n_want=N_KEEP, n_extra=PARAMS["eigensolver_n_extra_modes"],
                            sigma=PARAMS["eigensolver_shift_sigma"],
                            tol=PARAMS["eigensolver_tol"], ncv=PARAMS["eigensolver_ncv"],
                            tol_res=PARAMS["eigensolver_backward_error_tol"],
                            maxiter=20000, n_elem=N_ELEM,
                            fallback=DenseSubset(N_KEEP))


def case_assembly(ar, th_deg):
    l1, l2 = semi_axes_from_ar(ar, l_iso=PARAMS["l_iso"], rule="volume_equivalent")
    L11, L22, L12 = L_plane(l1, l2, float(np.deg2rad(th_deg)))
    return CaseAssembly(N_ELEM, PARAMS["Lcell"], PARAMS["lam"], PARAMS["mu"], PARAMS["rho"],
                        PARAMS["ell2"], L11, L22, L12), l1, l2


def solve_k_list(ca, solver, kpts, keep_vectors=False):
    n_k = kpts.shape[0]
    om = np.zeros((n_k, N_KEEP))
    vecs = [] if keep_vectors else None
    worst = 0.0
    t0 = time.time()
    t_pt = np.zeros(n_k)
    for j in range(n_k):
        t1 = time.perf_counter()
        K, M = ca.matrices(float(kpts[j, 0]), float(kpts[j, 1]))
        om_j, Y, res, _ok = solver.solve(K, M)
        t_pt[j] = time.perf_counter() - t1
        om[j, :] = om_j
        worst = max(worst, float(np.max(res)))
        if keep_vectors:
            vecs.append(Y)
    info = {"mean_ms": float(t_pt.mean() * 1e3), "max_ms": float(t_pt.max() * 1e3),
            "n_over_1s": int((t_pt > 1.0).sum()), "wall_s": time.time() - t0}
    return om, worst, vecs, info


def mac_tracked(path_om, path_vectors, ca, path_k):
    """Mode continuation along the k-path (frozen MAC algorithm, streamed matrix access).

    Identical rule to solver.bfs_bloch_solver.track_modes_mac: MAC_mn =
    |v_m^H M v_n|^2 / ((v_m^H M v_m)(v_n^H M v_n)) on the current k-point's mass
    matrix, greedy assignment, fallback fill.  The per-k matrices are rebuilt and
    released one at a time to keep the memory footprint of the sweep small.
    """
    n_pts, n_modes = path_om.shape
    tracked = np.zeros_like(path_om)
    tracked[0, :] = path_om[0, :]
    curr_V = path_vectors[0]
    for i in range(1, n_pts):
        next_V = path_vectors[i]
        _, M = ca.matrices(float(path_k[i, 0]), float(path_k[i, 1]))
        MV_curr = M @ curr_V
        MV_next = M @ next_V
        MAC = np.zeros((n_modes, n_modes))
        for m in range(n_modes):
            vm = curr_V[:, m]
            denom_m = np.real(vm.conj() @ MV_curr[:, m])
            for n in range(n_modes):
                wn = next_V[:, n]
                denom_n = np.real(wn.conj() @ MV_next[:, n])
                num = np.abs(vm.conj() @ MV_next[:, n]) ** 2
                MAC[m, n] = num / (denom_m * denom_n) if (denom_m > 0 and denom_n > 0) else 0.0
        matched = -np.ones(n_modes, dtype=int)
        used = set()
        for _ in range(n_modes):
            best_val, best_m, best_n = -1.0, -1, -1
            for m in range(n_modes):
                if matched[m] != -1:
                    continue
                for n in range(n_modes):
                    if n in used:
                        continue
                    if MAC[m, n] > best_val:
                        best_val, best_m, best_n = MAC[m, n], m, n
            if best_m != -1 and best_n != -1:
                matched[best_m] = best_n
                used.add(best_n)
        for m in range(n_modes):
            if matched[m] == -1:
                for n in range(n_modes):
                    if n not in used:
                        matched[m] = n
                        used.add(n)
                        break
        tracked[i, :] = path_om[i, matched]
        curr_V = next_V[:, matched]
    return tracked


def run_case(task):
    """Full production work for one (theta, AR) point."""
    ar, th = task["AR"], task["theta_deg"]
    t0 = time.time()
    ca, l1, l2 = case_assembly(ar, th)
    solver = new_solver()
    path_om, res_path, vecs, t_path = solve_k_list(ca, solver, task["path_k"], keep_vectors=True)
    grid_om, res_grid, _, t_grid = solve_k_list(ca, solver, task["grid_k"])
    gaps = compute_gaps(path_om[:, :N_BANDS], grid_om[:, :N_BANDS], task["breakpoints"],
                        N_bands=N_BANDS)
    rec = {
        "AR": ar, "theta_deg": th, "theta_rad": float(np.deg2rad(th)),
        "l1": l1, "l2": l2, "N_elem_per_side": N_ELEM,
        "dof": 8 * N_ELEM * N_ELEM, "n_modes_reported": N_KEEP,
        "n_path": int(task["path_k"].shape[0]), "n_grid": int(task["grid_k"].shape[0]),
        "omega_X": path_om[task["breakpoints"][1], :N_BANDS].tolist(),
        "omega_M": path_om[task["breakpoints"][2], :N_BANDS].tolist(),
        "path_bands": path_om.tolist(),
        "grid_bands": grid_om.tolist(),
        "gaps": gaps["gaps"],
        "worst_backward_error_path": res_path,
        "worst_backward_error_grid": res_grid,
        "n_dense_fallbacks": solver.stats["fallbacks"],
        "n_solves": solver.stats["points"],
        "arpack_matvecs": solver.stats["matvecs"],
        "solver_time_s": solver.stats["factor_time"] + solver.stats["arpack_time"],
        "timing_path": t_path, "timing_grid": t_grid,
        "point_time_ms_mean": solver.stats.get("point_ms_mean"),
        "point_time_ms_max": solver.stats.get("point_ms_max"),
        "n_points_over_1s": solver.stats.get("n_over_1s", 0),
    }
    if (ar, th) in S1_CASES:
        rec["raw_bands"] = path_om[:, :N_BANDS].tolist()
        rec["tracked_bands"] = mac_tracked(path_om[:, :N_BANDS], vecs, ca,
                                           task["path_k"]).tolist()
    rec["runtime_s"] = time.time() - t0
    return rec


def worker_main(tasks, ckpt_dir, force):
    ckpt_dir = Path(ckpt_dir)
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    for task in tasks:
        name = case_name(task["AR"], task["theta_deg"])
        out = Path(ckpt_dir) / f"case_{name}.json"
        if out.exists() and not force:
            print(f"  [skip] {name}", flush=True)
            continue
        t0 = time.time()
        rec = run_case(task)
        out.write_text(json.dumps(rec))
        print(f"  [done] {name}: {rec['n_solves']} solves, {rec['runtime_s']:.1f} s "
              f"(mean {rec['runtime_s']/rec['n_solves']*1e3:.0f} ms/pt, "
              f"backward error {max(rec['worst_backward_error_path'], rec['worst_backward_error_grid']):.1e}, "
              f"fallbacks {rec['n_dense_fallbacks']})", flush=True)


def cmd_compute(args):
    path_k, _, breakpoints = build_path_k(N_seg=PARAMS["N_seg"], L=PARAMS["Lcell"])
    _, _, grid_k = build_half_bz_grid(Nx=PARAMS["N_kx"], Ny=PARAMS["N_ky"], L=PARAMS["Lcell"])
    tasks = [{"AR": ar, "theta_deg": th, "path_k": path_k, "grid_k": grid_k,
              "breakpoints": breakpoints}
             for ar in PARAMS["ar_sweep"] for th in PARAMS["theta_sweep_deg"]]
    if args.only:
        want = {tuple(float(x) for x in tok.split(":")) for tok in args.only.split(",")}
        tasks = [t for t in tasks if (t["AR"], t["theta_deg"]) in want]
    print(f"P5 mesh-16 compute: {len(tasks)} cases, n={N_ELEM}, dof={8*N_ELEM*N_ELEM}, "
          f"path={path_k.shape[0]}, grid={grid_k.shape[0]}", flush=True)
    t0 = time.time()
    if args.workers <= 1:
        worker_main(tasks, args.checkpoint_dir, args.force)
    else:
        chunks = [tasks[i::args.workers] for i in range(args.workers)]
        procs = [mp.Process(target=worker_main, args=(ch, args.checkpoint_dir, args.force))
                 for ch in chunks]
        for p in procs:
            p.start()
        rc = 0
        for p in procs:
            p.join()
            if p.exitcode != 0:
                print(f"worker exit code {p.exitcode}", flush=True)
                rc = 1
        if rc:
            return rc
    print(f"compute finished in {time.time()-t0:.1f} s", flush=True)
    return 0


def s7_steering(ar, th_deg):
    """Iso-frequency steering: identical definitions to the frozen S7 study."""
    ca, _, _ = case_assembly(ar, th_deg)
    solver = new_solver()
    k_rad = 0.5 * np.pi / PARAMS["Lcell"]
    delta_angles, vg_mags, vp_mags = [], [], []
    for phi in S7_PHI:
        kx, ky = k_rad * np.cos(phi), k_rad * np.sin(phi)
        kpts = np.array([[kx + S7_H, ky], [kx - S7_H, ky], [kx, ky + S7_H],
                         [kx, ky - S7_H], [kx, ky]])
        om, _, _, _ = solve_k_list(ca, solver, kpts)
        vg = np.array([(om[0, 0] - om[1, 0]) / (2.0 * S7_H), (om[2, 0] - om[3, 0]) / (2.0 * S7_H)])
        kmag = float(np.hypot(kx, ky))
        vp = float(om[4, 0] / kmag) if kmag > 0 else 0.0
        vg_mag = float(np.linalg.norm(vg))
        if kmag > 0 and vg_mag > 0:
            cos_delta = np.clip(np.dot(vg, [kx, ky]) / (vg_mag * kmag), -1.0, 1.0)
            delta = float(np.rad2deg(np.arccos(cos_delta)))
        else:
            delta = 0.0
        delta_angles.append(delta)
        vg_mags.append(vg_mag)
        vp_mags.append(vp)
    return {"AR": ar, "theta_deg": th_deg,
            "delta_max_deg": float(np.max(delta_angles)),
            "mean_delta_deg": float(np.mean(delta_angles)),
            "phi_deg": np.rad2deg(S7_PHI).tolist(),
            "delta_deg": delta_angles, "vg_mag": vg_mags, "vp_mag": vp_mags,
            "k_radius": k_rad, "h_finite_difference": S7_H, "branch": 0,
            "n_solves_steering": solver.stats["points"],
            "n_dense_fallbacks": solver.stats["fallbacks"]}


def s8_payload():
    L, mu, rho, ell2 = PARAMS["Lcell"], PARAMS["mu"], PARAMS["rho"], PARAMS["ell2"]
    l1, l2 = semi_axes_from_ar(5.0, l_iso=PARAMS["l_iso"], rule="volume_equivalent")
    out = []
    for kb in np.linspace(0.05, 1.0, 20):
        kmag = kb * np.pi / L
        om_major = np.sqrt((mu / rho) * kmag ** 2 * (1.0 + l1 ** 2 * kmag ** 2 / 10.0)
                           / (1.0 + ell2 * kmag ** 2))
        om_minor = np.sqrt((mu / rho) * kmag ** 2 * (1.0 + l2 ** 2 * kmag ** 2 / 10.0)
                           / (1.0 + ell2 * kmag ** 2))
        wg_major = (l1 ** 2 * kmag ** 2 / 10.0) / (1.0 + l1 ** 2 * kmag ** 2 / 10.0)
        wg_minor = (l2 ** 2 * kmag ** 2 / 10.0) / (1.0 + l2 ** 2 * kmag ** 2 / 10.0)
        tg = (ell2 * kmag ** 2) / (1.0 + ell2 * kmag ** 2)
        out.append({"kbar": float(kb), "k_dim": float(kmag), "omega_major": float(om_major),
                    "omega_minor": float(om_minor), "Wg_over_W_major": float(wg_major),
                    "Wg_over_W_minor": float(wg_minor), "Tg_over_T": float(tg),
                    "Wc_over_W_major": float(1.0 - wg_major), "T0_over_T": float(1.0 - tg)})
    return out


def s9_payload():
    L, mu, rho, ell2, l_iso = (PARAMS["Lcell"], PARAMS["mu"], PARAMS["rho"],
                               PARAMS["ell2"], PARAMS["l_iso"])
    cT = np.sqrt(mu / rho)
    leff2 = l_iso ** 2
    vinf = (np.sqrt(leff2) / (np.sqrt(10.0) * np.sqrt(ell2))) * cT
    out = []
    for kb in np.array([0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0]):
        kmag = kb * np.pi / L
        vp_pos = np.sqrt((mu / rho) * kmag ** 2 * (1.0 + leff2 * kmag ** 2 / 10.0)
                         / (1.0 + ell2 * kmag ** 2)) / kmag
        vp_zero = np.sqrt((mu / rho) * kmag ** 2 * (1.0 + leff2 * kmag ** 2 / 10.0)) / kmag
        asymp_zero = (np.pi * np.sqrt(leff2) / np.sqrt(10.0)) * kb * cT
        out.append({"kbar": float(kb), "k_dim": float(kmag), "vp_ell_pos": float(vp_pos),
                    "vp_ell_zero": float(vp_zero), "vinf_theory": float(vinf),
                    "rel_vinf_error": float(abs(vp_pos - vinf) / vinf),
                    "rel_zero_asymp_error": float(abs(vp_zero - asymp_zero) / asymp_zero)})
    return out


def cmd_assemble(args):
    ckpt = Path(args.checkpoint_dir)
    raw_dir = PAPER9 / "results" / "raw"
    proc_dir = PAPER9 / "results" / "processed"
    ev_dir = PAPER9 / "audit" / "evidence" / f"p5_mesh{N_ELEM}"
    for d in (raw_dir, proc_dir, ev_dir):
        d.mkdir(parents=True, exist_ok=True)
    print("assembling n = 16 production outputs ...", flush=True)
    cases = {}
    for ar in PARAMS["ar_sweep"]:
        for th in PARAMS["theta_sweep_deg"]:
            f = ckpt / f"case_{case_name(ar, th)}.json"
            if not f.exists():
                raise SystemExit(f"missing checkpoint {f}")
            cases[(ar, th)] = json.loads(f.read_text())

    s1 = {case_name(ar, th): {"AR": ar, "theta_deg": th, "l1": cases[(ar, th)]["l1"],
                              "l2": cases[(ar, th)]["l2"],
                              "raw_bands": cases[(ar, th)]["raw_bands"],
                              "tracked_bands": cases[(ar, th)]["tracked_bands"]}
          for (ar, th) in S1_CASES}
    s3 = [{"theta_deg": th, "theta_rad": cases[(5.0, th)]["theta_rad"],
           "omega_X": cases[(5.0, th)]["omega_X"], "omega_M": cases[(5.0, th)]["omega_M"],
           "bands": [row[:N_BANDS] for row in cases[(5.0, th)]["path_bands"]]}
          for th in PARAMS["theta_sweep_deg"]]
    s4 = [{"AR": ar, "l1": cases[(ar, 45.0)]["l1"], "l2": cases[(ar, 45.0)]["l2"],
           "omega_X": cases[(ar, 45.0)]["omega_X"], "omega_M": cases[(ar, 45.0)]["omega_M"],
           "bands": [row[:N_BANDS] for row in cases[(ar, 45.0)]["path_bands"]]}
          for ar in PARAMS["ar_sweep"]]

    design_map, polar_map, table5_rows = [], [], []
    for pid, (ar, th) in enumerate([(a, t) for a in PARAMS["ar_sweep"]
                                    for t in PARAMS["theta_sweep_deg"]], start=1):
        rec = cases[(ar, th)]
        th_rad = rec["theta_rad"]
        gaps = rec["gaps"]
        design_map.append({"id": pid, "AR": ar, "theta_deg": th, "theta_rad": th_rad,
                           "l1": rec["l1"], "l2": rec["l2"],
                           "X_polar": float(ar * np.cos(th_rad)),
                           "Y_polar": float(ar * np.sin(th_rad)), "gaps": gaps})
        polar_map.append({"X": float(ar * np.cos(th_rad)), "Y": float(ar * np.sin(th_rad)),
                          "AR": ar, "theta_deg": th,
                          "delta_complete_12": gaps[0]["delta_complete"],
                          "delta_complete_23": gaps[1]["delta_complete"],
                          "delta_complete_34": gaps[2]["delta_complete"]})
        for g in gaps:
            gt = ("complete" if g["delta_complete"] > 0 else
                  ("directional" if (g["delta_GX"] > 0 or g["delta_XM"] > 0 or g["delta_MG"] > 0)
                   else "none"))
            table5_rows.append({"AR": ar, "theta_deg": th, "band_pair": g["band_pair"],
                                "delta_GX": g["delta_GX"], "delta_XM": g["delta_XM"],
                                "delta_MG": g["delta_MG"], "delta_path": g["delta_path"],
                                "delta_complete": g["delta_complete"], "gap_type": gt,
                                "omega_lower_max": g["omega_lower_max"],
                                "omega_upper_min": g["omega_upper_min"],
                                "omega_mid": g["omega_mid"],
                                "norm_gap_width": g["norm_gap_width"],
                                "inequality_holds": g["inequality_holds"]})

    dth = float(np.deg2rad(15.0))
    stheta = {}
    for ar in PARAMS["ar_sweep"]:
        pts = sorted([d for d in design_map if d["AR"] == ar], key=lambda d: d["theta_deg"])
        deltas = np.array([p["gaps"][1]["delta_GX"] for p in pts])
        grad = np.zeros_like(deltas)
        grad[0] = (deltas[1] - deltas[0]) / dth
        grad[-1] = (deltas[-1] - deltas[-2]) / dth
        for k in range(1, len(deltas) - 1):
            grad[k] = (deltas[k + 1] - deltas[k - 1]) / (2.0 * dth)
        mg, md = float(np.max(np.abs(grad))), float(np.max(np.abs(deltas)))
        stheta[f"AR_{int(ar)}"] = {"AR": ar, "max_grad_dtheta": mg, "max_delta": md,
                                   "S_theta_rad_inv": mg / md if md > 0 else 0.0,
                                   "S_theta_deg_inv": (mg / md if md > 0 else 0.0) * (np.pi / 180.0)}

    print("  S7 steering sweep ...", flush=True)
    s7 = {case_name(ar, th): s7_steering(ar, th) for (ar, th) in S7_CASES}
    s8, s9 = s8_payload(), s9_payload()

    npz_path = raw_dir / f"p5_production_mesh{N_ELEM}_grid.npz"
    np.savez_compressed(npz_path, **{f"grid_bands_{case_name(ar, th)}":
                                     np.array(cases[(ar, th)]["grid_bands"], dtype=float)
                                     for ar in PARAMS["ar_sweep"]
                                     for th in PARAMS["theta_sweep_deg"]})
    param_hash = hashlib.sha256(json.dumps(PARAMS, sort_keys=True).encode()).hexdigest()
    n_solves = sum(c["n_solves"] for c in cases.values()) + sum(v["n_solves_steering"]
                                                               for v in s7.values())
    payload = {
        "status": "COMPLETED",
        "utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "master_params": PARAMS,
        "param_hash": param_hash,
        "timing_seconds": sum(c["runtime_s"] for c in cases.values()),
        "n_solves_total": n_solves,
        "n_dense_fallbacks": sum(c["n_dense_fallbacks"] for c in cases.values()),
        "worst_backward_error": max(max(c["worst_backward_error_path"],
                                        c["worst_backward_error_grid"]) for c in cases.values()),
        "environment": {"python": sys.version.split()[0], "numpy": np.__version__,
                        "platform": platform.platform()},
        "provenance": {
            "supersedes": "results/raw/p5_production_raw.json (historical n = 1 production, preserved unchanged)",
            "mesh": f"{N_ELEM} x {N_ELEM} BFS elements per unit cell (h = {1.0/N_ELEM})",
            "dof_per_cell": 8 * N_ELEM * N_ELEM,
            "assembly": PARAMS["assembly"],
            "eigensolver": PARAMS["eigensolver"],
            "start_vector": "fixed analytic (unit u_x pattern, non-zero mean; no RNG)",
            "no_random_start": True, "no_rescaling": True,
            "driver": "production/run_p5_mesh16_production.py",
            "solver": "production/p5_mesh16_solver.py",
            "grid_archive": {"file": npz_path.name, "sha256": sha256_file(npz_path)},
            "modes_reported_per_k": N_KEEP,
            "notes": ("path_bands/grid_bands carry 6 modes per k-point (4 claim-bearing + "
                      "2 margin), all gated by the backward-error tolerance "
                      f"{PARAMS['eigensolver_backward_error_tol']:.0e}; the historical n = 1 "
                      "artefact carried 8 dense modes per k-point."),
        },
        "study_S1": s1, "study_S3": s3, "study_S4": s4,
        "study_S5_design_map": design_map, "study_S6_polar_map": polar_map,
        "study_S6_sensitivity_Stheta": stheta, "study_S7_ifc_steering": s7,
        "study_S8_energy_flux": s8, "study_S9_microinertia": s9,
    }
    raw_path = raw_dir / f"p5_production_raw_mesh{N_ELEM}.json"
    raw_path.write_text(json.dumps(payload, indent=2))
    table5_path = proc_dir / f"table5_gap_summary_mesh{N_ELEM}.json"
    table5_path.write_text(json.dumps({
        "title": f"Table 5 Band Gap and Regime Summary (n = {N_ELEM} production)",
        "git_commit": payload["git_commit"], "param_hash": param_hash,
        "n_cases": len(design_map),
        "columns": ["AR", "theta_deg", "band_pair", "delta_GX", "delta_XM", "delta_MG",
                    "delta_path", "delta_complete", "gap_type", "omega_lower_max",
                    "omega_upper_min", "omega_mid", "norm_gap_width", "inequality_holds"],
        "rows": table5_rows, "sensitivity_Stheta": stheta}, indent=2))
    highlights_path = proc_dir / f"p5_production_highlights_mesh{N_ELEM}.json"
    highlights_path.write_text(json.dumps({
        "suite": f"P5 Scientific Production (n = {N_ELEM} refinement)",
        "git_commit": payload["git_commit"], "param_hash": param_hash,
        "completed_studies": [
            "S1: Case H bands (AR=1 vs AR=10 along Gamma-X-M-Gamma)",
            "S3: Orientation sweep (theta in {0,15,30,45,60,75,90} deg at AR=5)",
            "S4: Aspect-ratio sweep (AR in {1,2,3,5,7,10} at theta=45 deg)",
            "S5: 42-point (theta, AR) design map",
            "S6: Polar design map and gap regime classification (Table 5)",
            "S7: Iso-frequency contours and wave steering (delta_max and FoM)",
            "S8: Energy-flux partition vs frequency",
            "S9: Micro-inertia study (bounded vs unbounded phase velocity)"],
        "key_findings": {
            "caseH_no_complete_bragg_gap": bool(all(g["delta_complete"] <= 0
                                                    for (ar, th) in S1_CASES
                                                    for g in cases[(ar, th)]["gaps"])),
            "gap_hierarchy_verified": f"Delta[leg] >= Delta[path] >= Delta[complete] holds for "
                                      f"{sum(1 for r in table5_rows if r['inequality_holds'])} of "
                                      f"{len(table5_rows)} rows",
            "steering_delta_max_AR1": s7["AR_1_th_0"]["delta_max_deg"],
            "steering_delta_max_AR5": s7["AR_5_th_45"]["delta_max_deg"],
            "steering_delta_max_AR10": s7["AR_10_th_45"]["delta_max_deg"],
            "microinertia_bounded_vinf": s9[-1]["vp_ell_pos"],
            "microinertia_unbounded_v200": s9[-1]["vp_ell_zero"]}}, indent=2))

    run_log = ev_dir / f"run_log_mesh{N_ELEM}.txt"
    with open(run_log, "w") as fh:
        fh.write("P5 mesh-16 production run log\n")
        fh.write(f"utc                    : {payload['utc']}\n")
        fh.write(f"git commit             : {payload['git_commit']}\n")
        fh.write("driver                 : production/run_p5_mesh16_production.py\n")
        fh.write("solver                 : production/p5_mesh16_solver.py\n")
        fh.write(f"elements per side      : {N_ELEM} (h = {1.0/N_ELEM}), DOF = {8*N_ELEM*N_ELEM}\n")
        fh.write(f"assembly               : {PARAMS['assembly']}\n")
        fh.write(f"eigensolver            : {PARAMS['eigensolver']}\n")
        fh.write(f"sweep                  : 42 (theta, AR) points; path 121 nodes; grid 3321 points\n")
        fh.write(f"k-path / grid          : N_seg 40 (Gamma-X-M-Gamma) / 41 x 81 half BZ\n")
        fh.write(f"modes per k-point      : {N_KEEP} (4 claim-bearing + 2 margin)\n")
        fh.write(f"parametric hash        : {param_hash}\n")
        fh.write(f"solves (total)         : {n_solves}\n")
        fh.write(f"dense fallbacks        : {payload['n_dense_fallbacks']}\n")
        fh.write(f"worst backward error   : {payload['worst_backward_error']:.3e}\n")
        fh.write(f"runtime (sum of cases) : {payload['timing_seconds']:.1f} s\n")
        fh.write(f"environment            : python {sys.version.split()[0]}, numpy {np.__version__}, "
                 f"{platform.platform()}\n")
        for name, path in (("raw", raw_path), ("grid", npz_path), ("table5", table5_path),
                           ("highlights", highlights_path)):
            fh.write(f"{name:22s} : {path.name} sha256 {sha256_file(path)}\n")
        for (ar, th) in sorted(cases, key=lambda k: (k[1], k[0])):
            c = cases[(ar, th)]
            fh.write(f"  case {case_name(ar,th):12s} solves {c['n_solves']:5d} "
                     f"runtime {c['runtime_s']:8.1f} s ({c['runtime_s']/c['n_solves']*1e3:5.0f} ms/pt) "
                     f"matvecs {c['arpack_matvecs']:7d} fallbacks {c['n_dense_fallbacks']} "
                     f"backward error {max(c['worst_backward_error_path'], c['worst_backward_error_grid']):.1e}\n")
    for p in (raw_path, npz_path, table5_path, highlights_path):
        print(f"  wrote {p.name} sha256 {sha256_file(p)}", flush=True)
    print(f"  run log: {run_log}")
    print(f"  solves {n_solves}, cases {len(cases)}, worst backward error "
          f"{payload['worst_backward_error']:.2e}", flush=True)
    return 0


def main():
    global N_ELEM
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("compute", "assemble"):
        p = sub.add_parser(name)
        p.add_argument("--n-elem", type=int, default=N_ELEM,
                       help="elements per unit-cell side (16 = production; 4/8 only for "
                            "mesh-comparison evidence)")
        p.add_argument("--workers", type=int, default=2)
        p.add_argument("--checkpoint-dir", type=str, default=str(CKPT_DEFAULT))
        p.add_argument("--force", action="store_true")
        p.add_argument("--only", type=str, default="")
    args = ap.parse_args()
    if args.n_elem != N_ELEM:
        N_ELEM = args.n_elem
        PARAMS["N_elem_per_side"] = N_ELEM
        PARAMS["elem_size_h"] = 1.0 / N_ELEM
        PARAMS["dof_per_cell"] = 8 * N_ELEM * N_ELEM
        PARAMS["assembly"] = f"frozen BFS n-order assembly (n x n elements per cell) at n={N_ELEM}"
    return cmd_compute(args) if args.cmd == "compute" else cmd_assemble(args)


if __name__ == "__main__":
    sys.exit(main())
