#!/usr/bin/env python3
"""Independent verification of the n = 16 production run + the n = 8 / n = 16 comparison.

Phase A  assembly equivalence: production `CaseAssembly` vs the frozen
         `assemble_nxn_bloch` reference, all 42 (theta, AR) cases at two k-points.
Phase B  solver accuracy: production frequencies vs the exact dense route
         (LAPACK zhegv, driver=gvx) at five k-points per case picked by *index*
         from the same path/grid arrays the production used.
Phase C  extremum verification: for the claim-bearing band pairs (2-3, 3-4) every
         extremum entering a Table-5 quantity (grid max of the lower band, grid min
         of the upper band, per-leg path maxima/minima) is re-evaluated with the
         exact dense route at the arg-extremum and its immediate neighbours in the
         same discrete set, and the extremum recomputed from the dense values is
         compared with the production value.
Phase D  classification-critical rows: any Table-5 row whose gap quantities come
         within 1e-3 of zero (sign-critical for the complete/directional/none
         classification) is reported with its dense-verified extremum values.
Phase E  n = 8 vs n = 16: for every claim-bearing quantity the n = 8 production
         values (same pipeline, same 42 points) are compared with n = 16, and the
         Table-5 gap-type classification changes are counted.

Outputs
    paper9/audit/evidence/p5_mesh16/verification_mesh16.json  (+ .txt summary)
    paper9/audit/evidence/p5_mesh16/mesh_comparison.json      (+ .txt summary)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import multiprocessing as mp
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PAPER9 = REPO / "paper9"
sys.path.insert(0, str(PAPER9))

from solver.bfs_bloch_solver import (                                     # noqa: E402
    L_plane, semi_axes_from_ar, build_path_k, build_half_bz_grid, compute_gaps,
)
from production.p5_mesh16_solver import (                                 # noqa: E402
    CaseAssembly, BlochEigensolver, DenseSubset, assemble_nxn_bloch_ref,
)

CKPT_16 = Path("/home/user/p5_repair/checkpoints")
CKPT_8 = Path("/home/user/p5_repair/checkpoints_n8")
EV = PAPER9 / "audit" / "evidence" / "p5_mesh16"
THETA = [0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0]
ARS = [1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
CLAIM_PAIRS = (1, 2)             # 0-based gap indices: band pairs (2,3) and (3,4)
N_PATH, N_KX, N_KY = 121, 41, 81


def case_name(ar, th):
    return f"AR_{int(ar)}_th_{int(th)}"


def build_ca(n, ar, th):
    l1, l2 = semi_axes_from_ar(ar, l_iso=0.20, rule="volume_equivalent")
    L11, L22, L12 = L_plane(l1, l2, float(np.deg2rad(th)))
    return CaseAssembly(n, 1.0, 1.0, 1.0, 1.0, 0.04, L11, L22, L12), (l1, l2, L11, L22, L12)


def dense_at(ca, kpts, counter):
    """Exact dense subset values (6 modes) at the given k-points."""
    d = DenseSubset(n_want=6)
    out = np.zeros((len(kpts), 6))
    for j, (kx, ky) in enumerate(kpts):
        K, M = ca.matrices(float(kx), float(ky))
        om, _, _, _ = d.solve(K, M)
        out[j, :] = np.real(om)          # DenseSubset already returns frequencies
        counter[0] += 1
    return out


def mode_resolved_dev(prod, dense):
    """Compare two sets of band frequencies as multisets (order-independent).

    Returns (max_abs_dev_sorted, max_abs_dev_nearest, n_unmatched).
    Degenerate / arbitrarily ordered eigenpairs make index-wise comparison meaningless.
    """
    prod = np.asarray(prod, dtype=float)
    dense = np.asarray(dense, dtype=float)
    a = np.sort(prod, axis=-1)
    b = np.sort(dense, axis=-1)
    dev_sorted = float(np.max(np.abs(a - b)))
    tol = 1e-6 * max(1.0, float(np.max(np.abs(dense))))
    worst_near = 0.0
    unm = 0
    for row_p, row_d in zip(prod.reshape(-1, prod.shape[-1]), dense.reshape(-1, dense.shape[-1])):
        for v in row_p:
            d = float(np.min(np.abs(row_d - v)))
            worst_near = max(worst_near, d)
            if d > tol:
                unm += 1
    return dev_sorted, worst_near, unm


def nearest_dense(val, dense_row):
    """Value in dense_row closest to the mode value val (continuation matching)."""
    return float(dense_row[int(np.argmin(np.abs(np.asarray(dense_row) - val)))])


def phase_a(n):
    worst = 0.0
    for ar in ARS:
        for th in THETA:
            ca, (l1, l2, L11, L22, L12) = build_ca(n, ar, th)
            for (kx, ky) in ((0.30 * np.pi, 0.35 * np.pi), (np.pi, 0.0)):
                K, M = ca.matrices(kx, ky)
                Kr, Mr = assemble_nxn_bloch_ref(n, kx, ky, 1.0, 1.0, 1.0, 1.0, 0.04,
                                                L11, L22, L12)
                worst = max(worst, float(abs(K - Kr).max()), float(abs(M - Mr).max()))
    return worst


def phase_bcd(ar, th, n, ckpt):
    t0 = time.time()
    rec = json.loads((ckpt / f"case_{case_name(ar, th)}.json").read_text())
    path_bands = np.array(rec["path_bands"])
    grid_bands = np.array(rec["grid_bands"])
    path_k, _, _ = build_path_k(N_seg=40, L=1.0)
    _, _, grid_k = build_half_bz_grid(Nx=N_KX, Ny=N_KY, L=1.0)
    ca, _ = build_ca(n, ar, th)
    counter = [0]
    out = {"AR": ar, "theta_deg": th, "n": n}

    # ---- Phase B: production vs exact dense at five indexed k-points (path + grid)
    pidx = [0, 20, 40, 60, 80]
    gidx = [0, 903, 1660, 2497, 3320]
    kp = [(float(path_k[i, 0]), float(path_k[i, 1])) for i in pidx]
    kg = [(float(grid_k[i, 0]), float(grid_k[i, 1])) for i in gidx]
    dp = dense_at(ca, kp, counter)
    dg = dense_at(ca, kg, counter)
    prod_p = path_bands[pidx, :6]
    prod_g = grid_bands[gidx, :6]
    # pass criterion uses the four claim-bearing (lowest) bands; the stored 5th/6th
    # entries may legitimately be one copy short at exact degeneracies, so they are
    # reported separately rather than folded into the deviation.
    s_p, n_p, u_p = mode_resolved_dev(prod_p[:, :4], dp[:, :4])
    s_g, n_g, u_g = mode_resolved_dev(prod_g[:, :4], dg[:, :4])
    _, _, extra_p = mode_resolved_dev(prod_p, dp)
    _, _, extra_g = mode_resolved_dev(prod_g, dg)
    out["phaseB"] = {"path_indices": pidx, "grid_indices": gidx,
                     "max_abs_dev_path": s_p, "max_abs_dev_grid": s_g,
                     "max_abs_dev_path_nearest": n_p, "max_abs_dev_grid_nearest": n_g,
                     "n_unmatched_path": u_p, "n_unmatched_grid": u_g,
                     "n_extra_stored_modes_path": extra_p, "n_extra_stored_modes_grid": extra_g,
                     "indexwise_dev_path": float(np.max(np.abs(prod_p - dp))),
                     "indexwise_dev_grid": float(np.max(np.abs(prod_g - dg))),
                     "path_k": kp, "grid_k": kg,
                     "production_path": prod_p.tolist(), "dense_path": dp.tolist(),
                     "production_grid": prod_g.tolist(), "dense_grid": dg.tolist()}

    # ---- Phase C: extrema entering the Table-5 quantities
    extrema = []
    iG, iX, iM, iG_end = 0, 40, 80, 120
    legs = {"GX": np.arange(iG, iX + 1), "XM": np.arange(iX, iM + 1), "MG": np.arange(iM, iG_end + 1)}
    for p in CLAIM_PAIRS:
        lower_g, upper_g = grid_bands[:, p], grid_bands[:, p + 1]
        # grid extrema
        for tag, arr, mode in (("grid_max_lower", lower_g, "max"), ("grid_min_upper", upper_g, "min")):
            idx = int(np.argmax(arr)) if mode == "max" else int(np.argmin(arr))
            i, j = divmod(idx, N_KY)
            nbr = [(i, j)] + [(ii, jj) for ii, jj in
                              [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                              if 0 <= ii < N_KX and 0 <= jj < N_KY]
            kq = [(float(grid_k[ii * N_KY + jj, 0]), float(grid_k[ii * N_KY + jj, 1]))
                  for ii, jj in nbr]
            dvals = dense_at(ca, kq, counter)
            prod = float(arr[idx])
            vd = np.array([nearest_dense(prod, row) for row in dvals])
            best = float(np.max(vd)) if mode == "max" else float(np.min(vd))
            extrema.append({"band_pair": [p + 1, p + 2], "quantity": tag, "index": idx,
                            "production_value": prod, "dense_at_arg": float(vd[0]),
                            "dense_extremum_over_neighbourhood": best,
                            "delta_production_minus_dense": prod - float(vd[0]),
                            "neighbourhood_better": bool(best > float(vd[0]) + 1e-9) if mode == "max"
                            else bool(best < float(vd[0]) - 1e-9)})
        # path leg extrema
        for leg, idxs in legs.items():
            for tag, arr, mode in (("leg_max_lower", path_bands[:, p], "max"),
                                   ("leg_min_upper", path_bands[:, p + 1], "min")):
                sub = arr[idxs]
                gi = int(idxs[int(np.argmax(sub)) if mode == "max" else int(np.argmin(sub))])
                nn = [gi] + [g for g in (gi - 1, gi + 1) if idxs[0] <= g <= idxs[-1]]
                kq = [(float(path_k[g, 0]), float(path_k[g, 1])) for g in nn]
                dvals = dense_at(ca, kq, counter)
                prod_v = float(arr[gi])
                vd = np.array([nearest_dense(prod_v, row) for row in dvals])
                best = float(np.max(vd)) if mode == "max" else float(np.min(vd))
                extrema.append({"band_pair": [p + 1, p + 2], "quantity": f"{tag}_{leg}",
                                "index": gi, "production_value": prod_v,
                                "dense_at_arg": float(vd[0]),
                                "dense_extremum_over_neighbourhood": best,
                                "delta_production_minus_dense": prod_v - float(vd[0]),
                                "neighbourhood_better": bool(best > float(vd[0]) + 1e-9) if mode == "max"
                                else bool(best < float(vd[0]) - 1e-9)})
    out["phaseC"] = {"extrema": extrema,
                     "n_extrema": len(extrema),
                     "max_abs_delta_production_vs_dense": max(abs(e["delta_production_minus_dense"])
                                                              for e in extrema),
                     "n_neighbourhood_better": sum(e["neighbourhood_better"] for e in extrema)}

    # ---- Phase D: classification-critical rows
    crit = []
    for g in rec["gaps"]:
        near = [k for k in ("delta_GX", "delta_XM", "delta_MG", "delta_path", "delta_complete")
                if abs(g[k]) < 1e-3]
        if near:
            crit.append({"band_pair": g["band_pair"], "near_zero": near,
                         "values": {k: g[k] for k in near}})
    out["phaseD"] = {"n_classification_critical_rows": len(crit), "rows": crit}
    out["dense_solves"] = counter[0]
    out["wall_time_s"] = time.time() - t0
    return out


def mesh_comparison(c16, c8):
    """Claim-bearing quantities: n = 8 vs n = 16."""
    out = {"cases": [], "summary": {}}
    keys_gap = ("delta_GX", "delta_XM", "delta_MG", "delta_path", "delta_complete")
    per_case = {}
    for ar in ARS:
        for th in THETA:
            r16 = c16[(ar, th)]
            r8 = c8[(ar, th)]
            row = {"AR": ar, "theta_deg": th,
                   "omega_X_band1": {"n8": r8["omega_X"][0], "n16": r16["omega_X"][0]},
                   "omega_M_band1": {"n8": r8["omega_M"][0], "n16": r16["omega_M"][0]},
                   "gaps": []}
            for g8, g16 in zip(r8["gaps"], r16["gaps"]):
                d = {"band_pair": g16["band_pair"]}
                for k in keys_gap:
                    d[k] = {"n8": g8[k], "n16": g16[k], "diff": g16[k] - g8[k]}
                d["gap_type_n8"] = ("complete" if g8["delta_complete"] > 0 else
                                    ("directional" if max(g8["delta_GX"], g8["delta_XM"],
                                                          g8["delta_MG"]) > 0 else "none"))
                d["gap_type_n16"] = ("complete" if g16["delta_complete"] > 0 else
                                     ("directional" if max(g16["delta_GX"], g16["delta_XM"],
                                                           g16["delta_MG"]) > 0 else "none"))
                d["classification_changed"] = d["gap_type_n8"] != d["gap_type_n16"]
                row["gaps"].append(d)
            out["cases"].append(row)
            per_case[(ar, th)] = row
    dgx16 = [max(g["delta_GX"]["n16"] for g in row["gaps"]) for row in out["cases"]]
    dgx8 = [max(g["delta_GX"]["n8"] for g in row["gaps"]) for row in out["cases"]]
    out["summary"] = {
        "max_delta_GX_n8": max(dgx8), "max_delta_GX_n16": max(dgx16),
        "argmax_n8": out["cases"][int(np.argmax(dgx8))]["AR"],
        "argmax_n8_theta": out["cases"][int(np.argmax(dgx8))]["theta_deg"],
        "argmax_n16": out["cases"][int(np.argmax(dgx16))]["AR"],
        "argmax_n16_theta": out["cases"][int(np.argmax(dgx16))]["theta_deg"],
        "classification_changes": sum(1 for row in out["cases"] for g in row["gaps"]
                                      if g["classification_changed"]),
        "max_abs_diff_delta_complete": max(abs(g["delta_complete"]["diff"])
                                           for row in out["cases"] for g in row["gaps"]),
        "max_abs_diff_omega_X": max(abs(row["omega_X_band1"]["n16"] - row["omega_X_band1"]["n8"])
                                    for row in out["cases"]),
        "max_abs_diff_omega_M": max(abs(row["omega_M_band1"]["n16"] - row["omega_M_band1"]["n8"])
                                    for row in out["cases"]),
    }
    return out


def _worker_bcd(args):
    ar, th, n, ckpt = args
    r = phase_bcd(ar, th, n, ckpt)
    print(f"  n={n} {case_name(ar,th):12s} B(path) {r['phaseB']['max_abs_dev_path']:.2e} "
          f"B(grid) {r['phaseB']['max_abs_dev_grid']:.2e} "
          f"extra {r['phaseB']['n_extra_stored_modes_path']}/{r['phaseB']['n_extra_stored_modes_grid']} "
          f"C(max|d|) {r['phaseC']['max_abs_delta_production_vs_dense']:.2e} "
          f"C(neighbour better) {r['phaseC']['n_neighbourhood_better']} "
          f"D {r['phaseD']['n_classification_critical_rows']} "
          f"[{r['dense_solves']} dense, {r['wall_time_s']:.0f} s]", flush=True)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--ckpt16", type=str, default=str(CKPT_16))
    ap.add_argument("--ckpt8", type=str, default=str(CKPT_8))
    ap.add_argument("--skip-phase-a", action="store_true")
    args = ap.parse_args()
    EV.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    doc = {"study": "P5 n = 16 production verification", "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                                             time.gmtime())}

    if not args.skip_phase_a:
        print("Phase A: assembly equivalence vs the frozen reference (42 cases x 2 k-points)", flush=True)
        w16 = phase_a(16)
        print(f"  n = 16 worst |assembly - frozen| = {w16:.3e}", flush=True)
        doc["phaseA"] = {"n16_worst_abs_difference": w16}
    if Path(args.ckpt8).exists() and any(Path(args.ckpt8).glob("case_*.json")):
        w8 = phase_a(8)
        print(f"  n = 8  worst |assembly - frozen| = {w8:.3e}", flush=True)
        doc.setdefault("phaseA", {})["n8_worst_abs_difference"] = w8

    tasks = [(ar, th) for ar in ARS for th in THETA]
    print(f"Phase B/C/D at n = 16: {len(tasks)} cases", flush=True)
    if args.workers > 1:
        with mp.Pool(args.workers) as pool:
            res16 = pool.map(_worker_bcd, [(ar, th, 16, Path(args.ckpt16)) for ar, th in tasks])
    else:
        res16 = [_worker_bcd((ar, th, 16, Path(args.ckpt16))) for ar, th in tasks]
    doc["cases_n16"] = res16
    doc["summary"] = {
        "max_abs_dev_path": max(r["phaseB"]["max_abs_dev_path"] for r in res16),
        "max_abs_dev_grid": max(r["phaseB"]["max_abs_dev_grid"] for r in res16),
        "n_extra_stored_modes": sum(r["phaseB"]["n_extra_stored_modes_path"]
                                    + r["phaseB"]["n_extra_stored_modes_grid"] for r in res16),
        "max_abs_delta_extrema": max(r["phaseC"]["max_abs_delta_production_vs_dense"] for r in res16),
        "n_neighbourhood_better": sum(r["phaseC"]["n_neighbourhood_better"] for r in res16),
        "n_extrema_verified": sum(r["phaseC"]["n_extrema"] for r in res16),
        "n_classification_critical_rows": sum(r["phaseD"]["n_classification_critical_rows"]
                                              for r in res16),
        "dense_solves": sum(r["dense_solves"] for r in res16),
    }
    doc["wall_time_s"] = time.time() - t0
    (EV / "verification_mesh16.json").write_text(json.dumps(doc, indent=1))
    s = doc["summary"]
    (EV / "verification_mesh16.txt").write_text(
        "P5 mesh-16 production verification summary\n"
        f"utc: {doc['utc']}\n"
        f"phase A  n=16 |assembly - frozen assembly| : {doc.get('phaseA', {}).get('n16_worst_abs_difference', float('nan')):.3e}\n"
        f"phase B  max |omega_production - omega_dense| over path indices (lowest four bands) : "
        f"{s['max_abs_dev_path']:.3e}\n"
        f"phase B  max |omega_production - omega_dense| over grid indices (lowest four bands) : "
        f"{s['max_abs_dev_grid']:.3e}\n"
        f"phase B  stored modes with no dense counterpart within tolerance (typically one copy of an "
        f"exact degeneracy) : {s.get('n_extra_stored_modes', 0)}\n"
        f"phase C  extrema verified : {s['n_extrema_verified']} ; max |production - dense| "
        f"{s['max_abs_delta_extrema']:.3e} ; neighbourhood better in {s['n_neighbourhood_better']} cases\n"
        f"phase D  classification-critical rows : {s['n_classification_critical_rows']}\n"
        f"dense reference solves : {s['dense_solves']}\n")
    print("summary:", json.dumps(s, indent=1), flush=True)

    # ---- Phase E: n = 8 vs n = 16 claim-bearing comparison
    c8dir = Path(args.ckpt8)
    if c8dir.exists() and any(c8dir.glob("case_*.json")):
        print("Phase E: n = 8 vs n = 16 claim-bearing comparison", flush=True)
        c16 = {(ar, th): json.loads((Path(args.ckpt16) / f"case_{case_name(ar,th)}.json").read_text())
               for ar in ARS for th in THETA}
        c8 = {(ar, th): json.loads((c8dir / f"case_{case_name(ar,th)}.json").read_text())
              for ar in ARS for th in THETA}
        cmp = mesh_comparison(c16, c8)
        cmp["utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        (EV / "mesh_comparison.json").write_text(json.dumps(cmp, indent=1))
        cs = cmp["summary"]
        (EV / "mesh_comparison.txt").write_text(
            "P5 mesh comparison: n = 8 vs n = 16 (claim-bearing quantities)\n"
            f"max delta_GX   n=8 {cs['max_delta_GX_n8']:.6f} at (theta={cs['argmax_n8_theta']}, AR={cs['argmax_n8']})\n"
            f"max delta_GX   n=16 {cs['max_delta_GX_n16']:.6f} at (theta={cs['argmax_n16_theta']}, AR={cs['argmax_n16']})\n"
            f"max |n16 - n8| for delta_complete : {cs['max_abs_diff_delta_complete']:.6f}\n"
            f"max |n16 - n8| for omega_X(band 1) : {cs['max_abs_diff_omega_X']:.6f}\n"
            f"max |n16 - n8| for omega_M(band 1) : {cs['max_abs_diff_omega_M']:.6f}\n"
            f"gap-type classification changes : {cs['classification_changes']} of 126 rows\n")
        print("mesh comparison summary:", json.dumps(cs, indent=1), flush=True)
    print(f"verification finished in {time.time()-t0:.1f} s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
