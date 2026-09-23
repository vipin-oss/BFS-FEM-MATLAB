#!/usr/bin/env python3
"""
paper9/production/p11d_caseC_gap_convergence.py
P11D remediation (CF-1/CF-2 of the P11C read-only audit): Case C *complete* gap
convergence, computed directly from the BZ definition

    Delta_complete = min_BZ omega_4(k) - max_BZ omega_3(k)

on a controlled FE-mesh x BZ-sampling matrix.  Delta_complete is NEVER inferred
from the pointwise gap Delta_X.

Study matrix (P11D specification):
  FE meshes : 4x4, 8x8, 16x16  (BFS C1 elements, mat_caseC, TV18 immersed
              Gauss-quadrature indicator, n_gauss = 4 -- the production operator)
  BZ grids  : 11x11, 21x21  (mandatory), 41x41 (specification "if feasible")
  Path legs : Delta_GX, Delta_XM, Delta_MG, Delta_path at N_seg = 20 per leg
              (same path discretisation as P11B for direct comparability),
              plus an N_seg = 40 path-sampling control.

Definitions (identical band pair and conventions as
paper9/solver/bfs_bloch_solver.py:compute_gaps):
  omega_n(k)  : n-th ascending eigenvalue sqrt of the Bloch problem at k
                (bands 3 and 4 are stored eigenvalue indices 2 and 3).
  Delta[S]    = min_{k in S} omega_4(k) - max_{k in S} omega_3(k)
                for S = one leg, the Gamma-X-M-Gamma path, or the sampled BZ.
  BZ domain   : [0, pi/L]^2 quarter zone (C4v + time-reversal symmetry of
                mat_caseC: isotropic L11 = L22, L12 = 0; centred circular
                inclusion).  Sampling: uniform N x N grids including the
                high-symmetry points Gamma, X, M and the M-Gamma diagonal.

Solver engine: sparse-transform + generalized Hermitian eigensolve restricted
to the wanted band pair (driver 'gvx', subset_by_index = [2, 3]).  This is
mathematically identical to solve_bloch_mesh (same T transform, same operator,
same sorted-eigenvalue band definition) and is validated against it at three
k-points per mesh before use (max |delta omega| recorded in the output).

Output: paper9/results/raw/p11d_caseC_gap_convergence.json (written
incrementally after every completed matrix cell).
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy.linalg as la
import scipy.sparse as sp

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "paper9"))

from solver.bfs_bloch_solver import (  # noqa: E402
    build_mesh_bloch_T,
    build_path_k,
    mat_caseC,
    solve_bloch_mesh,
)
from production.p11_caseC_convergence import assemble_mesh_KM_ngauss  # noqa: E402

RAW_DIR = REPO_ROOT / "paper9" / "results" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = RAW_DIR / "p11d_caseC_gap_convergence.json"

MESHES = [4, 8, 16]
BZ_MANDATORY = [11, 21]
BZ_EXTENDED = [41]
N_SEG_PATH = 20
N_SEG_CONTROL = 40
BAND_LO, BAND_HI = 2, 3  # eigenvalue indices of bands 3 and 4


def reduced_KM(Ks, Ms, Nx, Ny, kx, ky):
    """Bloch-reduced (Kbar, Mbar) via the sparse T transform (identical T as
    solve_bloch_mesh)."""
    T = build_mesh_bloch_T(Nx, Ny, kx, ky, 1.0, 1.0)
    Ts = sp.csr_matrix(T)
    Kb = (Ts.conj().T @ (Ks @ Ts)).toarray()
    Mb = (Ts.conj().T @ (Ms @ Ts)).toarray()
    Kb = 0.5 * (Kb + Kb.conj().T)
    Mb = 0.5 * (Mb + Mb.conj().T)
    return Kb, Mb


def bands_at(Ks, Ms, Nx, Ny, kx, ky):
    """omega_3, omega_4 (ascending sqrt-eigenvalue convention, bands 3/4)."""
    Kb, Mb = reduced_KM(Ks, Ms, Nx, Ny, kx, ky)
    w2 = la.eigh(Kb, Mb, eigvals_only=True,
                 subset_by_index=[BAND_LO, BAND_HI], driver="gvx")
    w = np.sqrt(np.maximum(w2, 0.0))
    return float(w[0]), float(w[1])


def bz_scan(Ks, Ms, Nx, Ny, N_bz):
    """min/max of bands 3,4 over the sampled quarter-BZ grid; extrema k tracked."""
    kvals = np.linspace(0.0, np.pi, N_bz)
    max_l, min_u = -np.inf, np.inf
    argmax_l = argmin_u = None
    for kx in kvals:
        for ky in kvals:
            w3, w4 = bands_at(Ks, Ms, Nx, Ny, kx, ky)
            if w3 > max_l:
                max_l, argmax_l = w3, (float(kx), float(ky))
            if w4 < min_u:
                min_u, argmin_u = w4, (float(kx), float(ky))
    return {
        "N_bz": N_bz,
        "total_k_points": N_bz * N_bz,
        "omega3_max": max_l,
        "omega4_min": min_u,
        "omega3_max_at_k": argmax_l,
        "omega4_min_at_k": argmin_u,
        "delta_complete": min_u - max_l,
        "norm_gap_pct": (min_u - max_l) / (0.5 * (min_u + max_l)) * 100.0,
        "is_complete_open": bool(min_u > max_l),
    }


def path_scan(Ks, Ms, Nx, Ny, n_seg):
    """Leg/path gaps from the Gamma-X-M-Gamma path at n_seg per leg."""
    k_pts, _, breakpoints = build_path_k(N_seg=n_seg, L=1.0)
    w3 = np.empty(len(k_pts))
    w4 = np.empty(len(k_pts))
    for i, (kx, ky) in enumerate(k_pts):
        w3[i], w4[i] = bands_at(Ks, Ms, Nx, Ny, kx, ky)
    iG, iX, iM, iEnd = breakpoints
    legs = {
        "delta_GX": float(np.min(w4[iG:iX + 1]) - np.max(w3[iG:iX + 1])),
        "delta_XM": float(np.min(w4[iX:iM + 1]) - np.max(w3[iX:iM + 1])),
        "delta_MG": float(np.min(w4[iM:iEnd + 1]) - np.max(w3[iM:iEnd + 1])),
    }
    d_path = float(np.min(w4) - np.max(w3))
    return {
        "n_seg_per_leg": n_seg,
        "n_path_points": len(k_pts),
        **legs,
        "delta_path": d_path,
        "omega3_max_path": float(np.max(w3)),
        "omega4_min_path": float(np.min(w4)),
    }


def save(package):
    package["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(OUT_FILE, "w") as f:
        json.dump(package, f, indent=2)


def main():
    git_sha = "7888220531833cefe182d48fd9dd74d8aa2cdeee (start of P11D remediation)"
    try:  # best-effort live SHA
        import subprocess
        git_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()
    except Exception:
        pass

    package = {
        "metadata": {
            "title": "P11D Case C complete-gap FE-mesh x BZ-sampling convergence",
            "date": datetime.now(timezone.utc).isoformat(),
            "git_sha_at_run": git_sha,
            "engine": "sparse-T Bloch transform + scipy.linalg.eigh(gvx, subset [2,3]); "
                      "identical operator and band definition as solve_bloch_mesh "
                      "(validated per mesh, see engine_validation)",
            "operator": "assemble_mesh_KM_ngauss(n_gauss=4) == assemble_mesh_KM "
                        "(production operator, TV18 immersed quadrature, mat_caseC)",
            "delta_complete_definition": "min over sampled BZ grid of omega_4 - max over "
                                         "sampled BZ grid of omega_3 (bands = 3rd/4th "
                                         "ascending sqrt-eigenvalues at each k)",
            "bz_domain": "quarter zone [0, pi]^2 justified by C4v + time-reversal symmetry "
                         "(isotropic L11=L22, L12=0; centred circular inclusion)",
            "note": "Delta_complete is computed directly; never inferred from Delta_X.",
        },
        "engine_validation": [],
        "convergence_matrix": [],
        "per_mesh_gaps": {},
        "path_sampling_control": {},
    }
    save(package)

    # ---- engine validation at three k-points per mesh vs solve_bloch_mesh ----
    spot_k = [(0.31 * np.pi, 0.17 * np.pi), (np.pi, 0.0), (0.5 * np.pi, 0.5 * np.pi)]
    assembled = {}
    for N in MESHES:
        print(f"[engine] assemble {N}x{N}", flush=True)
        K, M = assemble_mesh_KM_ngauss(N, N, 1.0, 1.0, mat_caseC, n_gauss=4)
        Ks, Ms = sp.csr_matrix(K), sp.csr_matrix(M)
        assembled[N] = (Ks, Ms, K, M)
        worst = 0.0
        for kx, ky in spot_k:
            w_fast = bands_at(Ks, Ms, N, N, kx, ky)
            w_ref, _, _ = solve_bloch_mesh(K, M, N, N, kx, ky, 1.0, 1.0,
                                           check_hermiticity=False)
            d = float(np.max(np.abs(np.array(w_fast) - w_ref[BAND_LO:BAND_HI + 1])))
            worst = max(worst, d)
        rec = {"mesh": f"{N}x{N}", "spot_k": [[float(a), float(b)] for a, b in spot_k],
               "max_abs_diff_vs_solve_bloch_mesh": worst}
        package["engine_validation"].append(rec)
        print(f"[engine] {N}x{N} max |diff| = {worst:.3e}", flush=True)
        assert worst < 1e-9, f"fast engine mismatch on {N}x{N}: {worst}"
        save(package)

    # ---- phase 1: mandatory matrix {4,8,16} x {11,21} ----
    # ---- phase 2: extended BZ {41} (specification: 'if feasible')        ----
    for phase, bz_list in (("mandatory", BZ_MANDATORY), ("extended", BZ_EXTENDED)):
        for N in MESHES:
            Ks, Ms, _, _ = assembled[N]
            for N_bz in bz_list:
                cell_id = f"{N}x{N}_FE_{N_bz}x{N_bz}_BZ"
                if any(c.get("cell_id") == cell_id for c in package["convergence_matrix"]):
                    continue
                print(f"[cell] {cell_id} ...", flush=True)
                t0 = time.time()
                res = bz_scan(Ks, Ms, N, N, N_bz)
                res["cell_id"] = cell_id
                res["fe_mesh"] = f"{N}x{N}"
                res["fe_dofs"] = int(8 * (N + 1) ** 2)
                res["phase"] = phase
                res["wall_time_s"] = round(time.time() - t0, 2)
                package["convergence_matrix"].append(res)
                print(f"[cell] {cell_id}: Delta_complete = {res['delta_complete']:.4f} "
                      f"(lower {res['omega3_max']:.4f} @ {res['omega3_max_at_k']}, "
                      f"upper {res['omega4_min']:.4f} @ {res['omega4_min_at_k']})",
                      flush=True)
                save(package)

    # ---- per-mesh leg/path gaps (N_seg = 20) + path-sampling control ----
    for N in MESHES:
        Ks, Ms, _, _ = assembled[N]
        print(f"[path] {N}x{N} legs/path N_seg={N_SEG_PATH}", flush=True)
        res = path_scan(Ks, Ms, N, N, N_SEG_PATH)
        best_bz = f"{BZ_EXTENDED[-1]}x{BZ_EXTENDED[-1]}"
        for c in package["convergence_matrix"]:
            if c["fe_mesh"] == f"{N}x{N}" and c["N_bz"] == BZ_EXTENDED[-1]:
                res["delta_complete_at_" + best_bz] = c["delta_complete"]
        package["per_mesh_gaps"][f"{N}x{N}"] = res
        save(package)

    print("[control] 4x4 path N_seg=40", flush=True)
    Ks, Ms, _, _ = assembled[4]
    package["path_sampling_control"]["4x4_Nseg40"] = path_scan(Ks, Ms, 4, 4, N_SEG_CONTROL)
    package["path_sampling_control"]["4x4_Nseg20_vs_40_note"] = (
        "difference quantifies path-sampling error of the directional leg gaps")
    save(package)

    print("DONE -- wrote", OUT_FILE, flush=True)


if __name__ == "__main__":
    main()
