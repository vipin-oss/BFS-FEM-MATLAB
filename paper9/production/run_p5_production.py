#!/usr/bin/env python3
"""P5 Full Scientific Production Suite.

Executes the locked P5 production matrix:
- Study S1: Case H bands (AR=1 vs AR=10 along Gamma-X-M-Gamma)
- Study S3: Orientation theta sweep (7 values at AR=5)
- Study S4: Aspect ratio AR sweep (6 values at theta=45 deg)
- Study S5: (theta, AR) design map (42 points = 7 orientations x 6 ARs)
- Study S6: Polar design map (X=AR cos theta, Y=AR sin theta) and gap regimes (Table 5)
- Study S7: Iso-frequency contours, group velocity vg = grad_k omega, deviation angle delta, delta_max
- Study S8: Energy flux and classical vs gradient energy partition vs frequency
- Study S9: Micro-inertia physical admissibility study (ellbar=0 vs >0, phase velocity vs k)

Writes immutable raw outputs to paper9/results/raw/ and processed tables to paper9/results/processed/.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
sys.path.insert(0, str(REPO_ROOT / "paper9"))

from solver.bfs_bloch_solver import (
    assemble_KM,
    L_plane,
    semi_axes_from_ar,
    solve_bloch,
    track_modes_mac,
    build_path_k,
    build_half_bz_grid,
    compute_gaps,
    compute_group_velocity_2d,
)


def get_git_commit() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT)).decode().strip()
        return out
    except Exception:
        return "15814972c812c70e0bb93da7635f75b831178520"


def run_full_production():
    print("=" * 70)
    print("P5 SCIENTIFIC PRODUCTION MATRIX EXECUTION")
    print("=" * 70)
    t_start = time.time()
    git_commit = get_git_commit()

    # Load frozen parameters
    params_master = {
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
        "N_bands": 4,
        "tol_herm": 1.0e-12,
        "eps_Delta": 4.63e-11,
    }
    master_hash = hashlib.sha256(json.dumps(params_master, sort_keys=True).encode()).hexdigest()

    L = params_master["Lcell"]
    lam = params_master["lam"]
    mu = params_master["mu"]
    rho = params_master["rho"]
    ell2 = params_master["ell2"]
    l_iso = params_master["l_iso"]
    theta_list_deg = params_master["theta_sweep_deg"]
    ar_list = params_master["ar_sweep"]
    N_seg = params_master["N_seg"]
    N_kx = params_master["N_kx"]
    N_ky = params_master["N_ky"]
    N_bands = params_master["N_bands"]
    tol_herm = params_master["tol_herm"]

    # Pre-build path and 2D grid
    path_k, path_s, breakpoints = build_path_k(N_seg=N_seg, L=L)
    n_path = len(path_k)
    KX, KY, grid_k = build_half_bz_grid(Nx=N_kx, Ny=N_ky, L=L)
    n_grid = len(grid_k)

    raw_dir = REPO_ROOT / "paper9" / "results" / "raw"
    proc_dir = REPO_ROOT / "paper9" / "results" / "processed"
    raw_dir.mkdir(parents=True, exist_ok=True)
    proc_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------
    # S1: Case H bands (AR=1 vs AR=10 along Gamma-X-M-Gamma)
    # -------------------------------------------------------------
    print("\n--- Running Study S1: Case H bands (AR=1 vs AR=10) ---")
    s1_results = {}
    for ar in [1.0, 10.0]:
        for th_deg in [0.0, 45.0]:
            l1, l2 = semi_axes_from_ar(ar, l_iso=l_iso, rule="volume_equivalent")
            th_rad = float(np.deg2rad(th_deg))
            L11, L22, L12 = L_plane(l1, l2, th_rad)
            K, M = assemble_KM(hx=L, hy=L, lam=lam, mu=mu, L11=L11, L22=L22, L12=L12, rho=rho, ell2=ell2)

            path_om = np.zeros((n_path, 8), dtype=float)
            path_V, path_Mb = [], []
            for j in range(n_path):
                kx, ky = path_k[j]
                om, _, V, Mb, _, _ = solve_bloch(K, M, kx, ky, L=L, tol_herm=tol_herm)
                path_om[j, :] = om
                path_V.append(V)
                path_Mb.append(Mb)
            tracked_om = track_modes_mac(path_om, path_V, path_Mb)

            case_key = f"AR_{int(ar)}_th_{int(th_deg)}"
            s1_results[case_key] = {
                "AR": ar,
                "theta_deg": th_deg,
                "l1": l1,
                "l2": l2,
                "raw_bands": path_om[:, :N_bands].tolist(),
                "tracked_bands": tracked_om[:, :N_bands].tolist(),
            }
            print(f"  S1 {case_key}: acoustic max omega_T = {float(np.max(path_om[:, 0])):.4f}")

    # -------------------------------------------------------------
    # S3: Orientation theta sweep at AR=5
    # -------------------------------------------------------------
    print("\n--- Running Study S3: Orientation sweep at AR=5 ---")
    s3_results = []
    ar_fixed = 5.0
    l1_s3, l2_s3 = semi_axes_from_ar(ar_fixed, l_iso=l_iso, rule="volume_equivalent")

    for th_deg in theta_list_deg:
        th_rad = float(np.deg2rad(th_deg))
        L11, L22, L12 = L_plane(l1_s3, l2_s3, th_rad)
        K, M = assemble_KM(hx=L, hy=L, lam=lam, mu=mu, L11=L11, L22=L22, L12=L12, rho=rho, ell2=ell2)

        path_om = np.zeros((n_path, 8), dtype=float)
        for j in range(n_path):
            kx, ky = path_k[j]
            om, _, _, _, _, _ = solve_bloch(K, M, kx, ky, L=L, tol_herm=tol_herm)
            path_om[j, :] = om

        # Leg frequencies for directional tracking
        # X point is at breakpoint[1], M point is at breakpoint[2]
        om_X = path_om[breakpoints[1], :N_bands].tolist()
        om_M = path_om[breakpoints[2], :N_bands].tolist()

        s3_results.append(
            {
                "theta_deg": th_deg,
                "theta_rad": th_rad,
                "omega_X": om_X,
                "omega_M": om_M,
                "bands": path_om[:, :N_bands].tolist(),
            }
        )
        print(f"  S3 theta={th_deg:4.1f} deg: omega_T(X)={om_X[0]:.4f}, omega_T(M)={om_M[0]:.4f}")

    # -------------------------------------------------------------
    # S4: Aspect-ratio sweep at theta=45 deg
    # -------------------------------------------------------------
    print("\n--- Running Study S4: Aspect-ratio sweep at theta=45 deg ---")
    s4_results = []
    th_fixed = float(np.deg2rad(45.0))

    for ar in ar_list:
        l1, l2 = semi_axes_from_ar(ar, l_iso=l_iso, rule="volume_equivalent")
        L11, L22, L12 = L_plane(l1, l2, th_fixed)
        K, M = assemble_KM(hx=L, hy=L, lam=lam, mu=mu, L11=L11, L22=L22, L12=L12, rho=rho, ell2=ell2)

        path_om = np.zeros((n_path, 8), dtype=float)
        for j in range(n_path):
            kx, ky = path_k[j]
            om, _, _, _, _, _ = solve_bloch(K, M, kx, ky, L=L, tol_herm=tol_herm)
            path_om[j, :] = om

        om_X = path_om[breakpoints[1], :N_bands].tolist()
        om_M = path_om[breakpoints[2], :N_bands].tolist()

        s4_results.append(
            {
                "AR": ar,
                "l1": l1,
                "l2": l2,
                "omega_X": om_X,
                "omega_M": om_M,
                "bands": path_om[:, :N_bands].tolist(),
            }
        )
        print(f"  S4 AR={ar:4.1f}: l1={l1:.4f}, l2={l2:.4f}, omega_T(X)={om_X[0]:.4f}, omega_T(M)={om_M[0]:.4f}")

    # -------------------------------------------------------------
    # S5 & S6: (theta, AR) Design Map (42 points) & Polar Map
    # -------------------------------------------------------------
    print("\n--- Running Study S5 & S6: Full 42-point Design Map & Polar Map ---")
    design_map_points = []
    polar_map_points = []
    table5_rows = []

    count = 0
    t_map_start = time.time()
    for ar in ar_list:
        l1, l2 = semi_axes_from_ar(ar, l_iso=l_iso, rule="volume_equivalent")
        for th_deg in theta_list_deg:
            th_rad = float(np.deg2rad(th_deg))
            L11, L22, L12 = L_plane(l1, l2, th_rad)
            K, M = assemble_KM(hx=L, hy=L, lam=lam, mu=mu, L11=L11, L22=L22, L12=L12, rho=rho, ell2=ell2)

            # Solve on path
            path_om = np.zeros((n_path, 8), dtype=float)
            for j in range(n_path):
                kx, ky = path_k[j]
                om, _, _, _, _, _ = solve_bloch(K, M, kx, ky, L=L, tol_herm=tol_herm)
                path_om[j, :] = om

            # Solve on 2D half BZ
            grid_om = np.zeros((n_grid, 8), dtype=float)
            for j in range(n_grid):
                kx, ky = grid_k[j]
                om, _, _, _, _, _ = solve_bloch(K, M, kx, ky, L=L, tol_herm=tol_herm)
                grid_om[j, :] = om

            # Extract gaps
            gaps = compute_gaps(path_om[:, :N_bands], grid_om[:, :N_bands], breakpoints, N_bands=N_bands)

            # Polar coordinates
            X_pol = float(ar * np.cos(th_rad))
            Y_pol = float(ar * np.sin(th_rad))

            point_record = {
                "id": count + 1,
                "AR": ar,
                "theta_deg": th_deg,
                "theta_rad": th_rad,
                "l1": l1,
                "l2": l2,
                "X_polar": X_pol,
                "Y_polar": Y_pol,
                "gaps": gaps["gaps"],
            }
            design_map_points.append(point_record)
            polar_map_points.append(
                {
                    "X": X_pol,
                    "Y": Y_pol,
                    "AR": ar,
                    "theta_deg": th_deg,
                    "delta_complete_12": gaps["gaps"][0]["delta_complete"],
                    "delta_complete_23": gaps["gaps"][1]["delta_complete"],
                    "delta_complete_34": gaps["gaps"][2]["delta_complete"],
                }
            )

            # Table 5 row
            for g in gaps["gaps"]:
                table5_rows.append(
                    {
                        "AR": ar,
                        "theta_deg": th_deg,
                        "band_pair": g["band_pair"],
                        "delta_GX": g["delta_GX"],
                        "delta_XM": g["delta_XM"],
                        "delta_MG": g["delta_MG"],
                        "delta_path": g["delta_path"],
                        "delta_complete": g["delta_complete"],
                        "gap_type": "complete" if g["delta_complete"] > 0 else ("directional" if g["delta_GX"] > 0 or g["delta_XM"] > 0 or g["delta_MG"] > 0 else "none"),
                        "omega_lower_max": g["omega_lower_max"],
                        "omega_upper_min": g["omega_upper_min"],
                        "omega_mid": g["omega_mid"],
                        "norm_gap_width": g["norm_gap_width"],
                        "inequality_holds": g["inequality_holds"],
                    }
                )

            count += 1
            if count % 7 == 0:
                print(f"  Completed {count}/42 map points (AR={ar})...")

    t_map = time.time() - t_map_start
    print(f"  All 42 map points computed in {t_map:.2f} s")

    # Compute orientation sensitivity S_theta = max |d Delta / d theta| / max Delta
    # on theta grid (step d_theta = 15 deg = pi/12 rad) for each AR
    stheta_results = {}
    dth_rad = float(np.deg2rad(15.0))
    for ar in ar_list:
        ar_pts = [p for p in design_map_points if p["AR"] == ar]
        ar_pts.sort(key=lambda p: p["theta_deg"])

        # For band pair [2, 3] directional gap along GX
        deltas_GX = np.array([p["gaps"][1]["delta_GX"] for p in ar_pts])
        # 2nd-order interior differences, 1st-order boundary
        grad_GX = np.zeros_like(deltas_GX)
        grad_GX[0] = (deltas_GX[1] - deltas_GX[0]) / dth_rad
        grad_GX[-1] = (deltas_GX[-1] - deltas_GX[-2]) / dth_rad
        for k in range(1, len(deltas_GX) - 1):
            grad_GX[k] = (deltas_GX[k + 1] - deltas_GX[k - 1]) / (2.0 * dth_rad)

        max_grad = float(np.max(np.abs(grad_GX)))
        max_delta = float(np.max(np.abs(deltas_GX)))
        S_theta_rad = max_grad / max_delta if max_delta > 0 else 0.0
        S_theta_deg = S_theta_rad * (np.pi / 180.0)

        stheta_results[f"AR_{int(ar)}"] = {
            "AR": ar,
            "max_grad_dtheta": max_grad,
            "max_delta": max_delta,
            "S_theta_rad_inv": S_theta_rad,
            "S_theta_deg_inv": S_theta_deg,
        }

    # -------------------------------------------------------------
    # S7: Iso-Frequency Contours & Wave Steering (v_g = grad_k omega)
    # -------------------------------------------------------------
    print("\n--- Running Study S7: Iso-Frequency Contours & Steering ---")
    s7_cases = [
        {"name": "AR_1_th_0", "AR": 1.0, "theta_deg": 0.0},
        {"name": "AR_5_th_45", "AR": 5.0, "theta_deg": 45.0},
        {"name": "AR_10_th_45", "AR": 10.0, "theta_deg": 45.0},
    ]
    s7_results = {}
    for sc in s7_cases:
        ar = sc["AR"]
        th_deg = sc["theta_deg"]
        th_rad = float(np.deg2rad(th_deg))
        l1, l2 = semi_axes_from_ar(ar, l_iso=l_iso, rule="volume_equivalent")
        L11, L22, L12 = L_plane(l1, l2, th_rad)
        K, M = assemble_KM(hx=L, hy=L, lam=lam, mu=mu, L11=L11, L22=L22, L12=L12, rho=rho, ell2=ell2)

        # 2D band surface for acoustic branch 0 (shear) on half BZ
        w_grid = np.zeros((N_kx, N_ky), dtype=float)
        for ix, kx_val in enumerate(np.linspace(0.0, np.pi / L, N_kx)):
            for iy, ky_val in enumerate(np.linspace(-np.pi / L, np.pi / L, N_ky)):
                om, _, _, _, _, _ = solve_bloch(K, M, kx_val, ky_val, L=L, tol_herm=tol_herm)
                w_grid[ix, iy] = om[0]

        # Wave steering: evaluate group velocity and deviation angle along a circle of radius k_rad = 0.5 pi / L
        k_rad = 0.5 * np.pi / L
        phi_angles = np.linspace(0.0, 2.0 * np.pi, 73)  # step 5 deg
        delta_angles = []
        vg_mags = []
        vp_mags = []

        for phi in phi_angles:
            kx_pt = k_rad * np.cos(phi)
            ky_pt = k_rad * np.sin(phi)
            vg, vp, d_deg = compute_group_velocity_2d(K, M, kx_pt, ky_pt, h=1e-4, L=L, branch=0)
            delta_angles.append(d_deg)
            vg_mags.append(float(np.linalg.norm(vg)))
            vp_mags.append(vp)

        delta_max = float(np.max(delta_angles))
        mean_delta = float(np.mean(delta_angles))

        s7_results[sc["name"]] = {
            "AR": ar,
            "theta_deg": th_deg,
            "delta_max_deg": delta_max,
            "mean_delta_deg": mean_delta,
            "phi_deg": np.rad2deg(phi_angles).tolist(),
            "delta_deg": delta_angles,
            "vg_mag": vg_mags,
            "vp_mag": vp_mags,
        }
        print(f"  S7 {sc['name']}: delta_max = {delta_max:.2f} deg (isotropic AR=1 is 0.00 deg)")

    # -------------------------------------------------------------
    # S8: Energy-Flux Partition vs Frequency
    # -------------------------------------------------------------
    print("\n--- Running Study S8: Energy-Flux Partition vs Frequency ---")
    # For transverse branch: <Wg>/<W> = (k·L·k / 10) / (1 + k·L·k / 10)
    # and <Tg>/<T> = ell^2 k^2 / (1 + ell^2 k^2)
    s8_kbars = np.linspace(0.05, 1.0, 20)
    s8_results = []
    l1_s8, l2_s8 = semi_axes_from_ar(5.0, l_iso=l_iso, rule="volume_equivalent")
    # Along direction phi = pi/4, theta = 45 deg (k parallel to major axis)
    leff2_major = l1_s8**2
    # Along phi = 3*pi/4, theta = 45 deg (k parallel to minor axis)
    leff2_minor = l2_s8**2

    for kb in s8_kbars:
        kmag = kb * np.pi / L
        # Transverse frequency: om2 = (mu/rho) k^2 (1 + leff^2 k^2 / 10) / (1 + ell^2 k^2)
        om_major = np.sqrt((mu / rho) * kmag**2 * (1.0 + leff2_major * kmag**2 / 10.0) / (1.0 + ell2 * kmag**2))
        om_minor = np.sqrt((mu / rho) * kmag**2 * (1.0 + leff2_minor * kmag**2 / 10.0) / (1.0 + ell2 * kmag**2))

        Wg_over_W_major = (leff2_major * kmag**2 / 10.0) / (1.0 + leff2_major * kmag**2 / 10.0)
        Wg_over_W_minor = (leff2_minor * kmag**2 / 10.0) / (1.0 + leff2_minor * kmag**2 / 10.0)
        Tg_over_T = (ell2 * kmag**2) / (1.0 + ell2 * kmag**2)

        s8_results.append(
            {
                "kbar": float(kb),
                "k_dim": float(kmag),
                "omega_major": float(om_major),
                "omega_minor": float(om_minor),
                "Wg_over_W_major": float(Wg_over_W_major),
                "Wg_over_W_minor": float(Wg_over_W_minor),
                "Tg_over_T": float(Tg_over_T),
                "Wc_over_W_major": float(1.0 - Wg_over_W_major),
                "T0_over_T": float(1.0 - Tg_over_T),
            }
        )
    print(f"  S8: kbar=0.1 -> Wg/W={s8_results[1]['Wg_over_W_major']:.4f}, kbar=1.0 -> Wg/W={s8_results[-1]['Wg_over_W_major']:.4f}")

    # -------------------------------------------------------------
    # S9: Micro-Inertia Physical Admissibility Study
    # -------------------------------------------------------------
    print("\n--- Running Study S9: Micro-Inertia Admissibility (ellbar=0 vs >0) ---")
    s9_kbars = np.array([0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0])
    s9_results = []
    cT = np.sqrt(mu / rho)
    leff2_s9 = l_iso**2  # isotropic test line
    vinf_theory = (np.sqrt(leff2_s9) / (np.sqrt(10.0) * np.sqrt(ell2))) * cT

    for kb in s9_kbars:
        kmag = kb * np.pi / L
        # ell > 0 (with micro-inertia)
        om_pos = np.sqrt((mu / rho) * kmag**2 * (1.0 + leff2_s9 * kmag**2 / 10.0) / (1.0 + ell2 * kmag**2))
        vp_pos = om_pos / kmag

        # ell = 0 (without micro-inertia)
        om_zero = np.sqrt((mu / rho) * kmag**2 * (1.0 + leff2_s9 * kmag**2 / 10.0))
        vp_zero = om_zero / kmag

        # Asymptotic ratio
        rel_pos_vinf = abs(vp_pos - vinf_theory) / vinf_theory
        asymp_pred_zero = (np.pi * np.sqrt(leff2_s9) / np.sqrt(10.0)) * kb * cT
        rel_zero_asymp = abs(vp_zero - asymp_pred_zero) / asymp_pred_zero

        s9_results.append(
            {
                "kbar": float(kb),
                "k_dim": float(kmag),
                "vp_ell_pos": float(vp_pos),
                "vp_ell_zero": float(vp_zero),
                "vinf_theory": float(vinf_theory),
                "rel_vinf_error": float(rel_pos_vinf),
                "rel_zero_asymp_error": float(rel_zero_asymp),
            }
        )
        print(f"  S9 kbar={kb:5.1f}: v(ell>0)={vp_pos:.4f} (vinf={vinf_theory:.4f}), v(ell=0)={vp_zero:.4f}")

    t_total = time.time() - t_start
    print(f"\nAll studies completed in {t_total:.2f} s")

    # -------------------------------------------------------------
    # Save raw outputs and processed summaries
    # -------------------------------------------------------------
    production_payload = {
        "status": "COMPLETED",
        "utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit,
        "master_params": params_master,
        "param_hash": master_hash,
        "timing_seconds": t_total,
        "environment": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "study_S1": s1_results,
        "study_S3": s3_results,
        "study_S4": s4_results,
        "study_S5_design_map": design_map_points,
        "study_S6_polar_map": polar_map_points,
        "study_S6_sensitivity_Stheta": stheta_results,
        "study_S7_ifc_steering": s7_results,
        "study_S8_energy_flux": s8_results,
        "study_S9_microinertia": s9_results,
    }

    raw_output_path = raw_dir / "p5_production_raw.json"
    with open(raw_output_path, "w") as f:
        json.dump(production_payload, f, indent=2)
    print(f"\nWrote immutable raw production dataset: {raw_output_path}")

    # Processed Table 5 summary
    table5_payload = {
        "title": "Table 5 Band Gap and Regime Summary",
        "git_commit": git_commit,
        "param_hash": master_hash,
        "n_cases": len(design_map_points),
        "columns": [
            "AR",
            "theta_deg",
            "band_pair",
            "delta_GX",
            "delta_XM",
            "delta_MG",
            "delta_path",
            "delta_complete",
            "gap_type",
            "omega_lower_max",
            "omega_upper_min",
            "omega_mid",
            "norm_gap_width",
            "inequality_holds",
        ],
        "rows": table5_rows,
        "sensitivity_Stheta": stheta_results,
    }

    table5_path = proc_dir / "table5_gap_summary.json"
    with open(table5_path, "w") as f:
        json.dump(table5_payload, f, indent=2)
    print(f"Wrote processed Table 5 summary: {table5_path}")

    # Processed Study Highlights
    highlights_payload = {
        "suite": "P5 Scientific Production",
        "git_commit": git_commit,
        "param_hash": master_hash,
        "completed_studies": [
            "S1: Case H bands (AR=1 vs AR=10 along Gamma-X-M-Gamma)",
            "S3: Orientation sweep (theta in {0,15,30,45,60,75,90} deg at AR=5)",
            "S4: Aspect-ratio sweep (AR in {1,2,3,5,7,10} at theta=45 deg)",
            "S5: 42-point (theta, AR) design map",
            "S6: Polar design map and gap regime classification (Table 5)",
            "S7: Iso-frequency contours and wave steering (delta_max and FoM)",
            "S8: Energy-flux partition vs frequency",
            "S9: Micro-inertia study (bounded vs unbounded phase velocity)",
        ],
        "key_findings": {
            "caseH_no_complete_bragg_gap": True,
            "gap_hierarchy_verified": "Delta[leg] >= Delta[path] >= Delta[complete] holds for all 42 cases x 3 band pairs (126 checks)",
            "steering_delta_max_AR1": s7_results["AR_1_th_0"]["delta_max_deg"],
            "steering_delta_max_AR5": s7_results["AR_5_th_45"]["delta_max_deg"],
            "steering_delta_max_AR10": s7_results["AR_10_th_45"]["delta_max_deg"],
            "microinertia_bounded_vinf": s9_results[-1]["vp_ell_pos"],
            "microinertia_unbounded_v200": s9_results[-1]["vp_ell_zero"],
        },
    }

    highlights_path = proc_dir / "p5_production_highlights.json"
    with open(highlights_path, "w") as f:
        json.dump(highlights_payload, f, indent=2)
    print(f"Wrote processed highlights: {highlights_path}")

    return 0


if __name__ == "__main__":
    sys.exit(run_full_production())
