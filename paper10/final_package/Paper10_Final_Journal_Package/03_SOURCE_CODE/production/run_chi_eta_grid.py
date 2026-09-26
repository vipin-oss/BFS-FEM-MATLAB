#!/usr/bin/env python3
"""
Supplementary Phase-0 Study: 2-D Material-Contrast x Filling-Fraction Grid
===========================================================================
Runs the frozen 10-state DPL-dipolar gradient transfer-matrix solver on a
dense (chi, eta) grid to quantify the *simultaneous* interaction of material
contrast (chi) and geometric filling fraction (eta) on the first Bragg
band-gap width Delta_Omega.

This is a SUPPLEMENTARY computation (Phase 0 manuscript-expansion campaign):
- The frozen S1-S7 production datasets are NOT modified.
- Solver machinery is reproduced verbatim from `run_phase3b_production.py`
  (generalized interface eigenvalue formulation, Hungarian branch tracking,
  propagating-coverage band-gap extraction).
- Sanity anchors: grid points (chi, eta) that coincide with frozen S2/S4
  production cases must reproduce PRODUCTION_BANDGAP_SUMMARY.csv values.

Outputs (written to 04_PRODUCTION_DATA/):
- SUPP_CHI_ETA_GAP_SUMMARY.csv   : full gap table over the grid
- SUPP_CHI_ETA_CASE_METRICS.csv  : per-case runtime/conditioning/attenuation
- SUPP_CHI_ETA_GRID_META.json    : run metadata
"""

import os
import sys
import json
import time
import csv
import numpy as np
from scipy.linalg import eig
from scipy.optimize import linear_sum_assignment

HERE = os.path.abspath(os.path.dirname(__file__))
SRC = os.path.abspath(os.path.join(HERE, ".."))
PKG = os.path.abspath(os.path.join(SRC, ".."))
sys.path.insert(0, SRC)

from transfer_matrix.coupled10 import Coupled10StateSolver  # noqa: E402
from transfer_matrix.parameters import MaterialParameters   # noqa: E402


# -----------------------------------------------------------------------------
# Core unit-cell Bloch solver (verbatim logic from run_phase3b_production.py)
# -----------------------------------------------------------------------------

def solve_unit_cell_bloch(matA, matB, a1, a2, omega, xi=0.0):
    solverA = Coupled10StateSolver(matA, xi=xi)
    solverB = Coupled10StateSolver(matB, xi=xi)

    PA, _, cond_PA = solverA.compute_modal_matrix(omega)
    PB, _, cond_PB = solverB.compute_modal_matrix(omega)

    rootsA = solverA.compute_characteristic_roots(omega)["all_roots"]
    rootsB = solverB.compute_characteristic_roots(omega)["all_roots"]

    fwdA = [i for i, k in enumerate(rootsA) if k.imag > 1e-12 or (abs(k.imag) <= 1e-12 and k.real > 0)]
    bwdA = [i for i, k in enumerate(rootsA) if i not in fwdA]
    fwdB = [i for i, k in enumerate(rootsB) if k.imag > 1e-12 or (abs(k.imag) <= 1e-12 and k.real > 0)]
    bwdB = [i for i, k in enumerate(rootsB) if i not in fwdB]

    if len(fwdA) != 5:
        # Sort by imaginary part descending
        orderA = np.argsort([-k.imag for k in rootsA])
        fwdA = list(orderA[:5])
        bwdA = list(orderA[5:])
    if len(fwdB) != 5:
        orderB = np.argsort([-k.imag for k in rootsB])
        fwdB = list(orderB[:5])
        bwdB = list(orderB[5:])

    kA_fwd = rootsA[fwdA]
    kA_bwd = rootsA[bwdA]
    kB_fwd = rootsB[fwdB]
    kB_bwd = rootsB[bwdB]

    EA_fwd = np.diag(np.exp(1j * kA_fwd * a1))
    EA_bwd = np.diag(np.exp(-1j * kA_bwd * a1))
    EB_fwd = np.diag(np.exp(1j * kB_fwd * a2))
    EB_bwd = np.diag(np.exp(-1j * kB_bwd * a2))

    A_mat = np.zeros((20, 20), dtype=complex)
    B_mat = np.zeros((20, 20), dtype=complex)

    # Interface matching at x = a1: V_A(a1) - V_B(0) = 0
    A_mat[0:10, 0:5] = PA[:, fwdA] @ EA_fwd
    A_mat[0:10, 5:10] = PA[:, bwdA]
    A_mat[0:10, 10:15] = -PB[:, fwdB]
    A_mat[0:10, 15:20] = -PB[:, bwdB] @ EB_bwd

    # Bloch periodic condition at x = a2: V_B(a2) - lambda * V_A(0) = 0
    A_mat[10:20, 10:15] = PB[:, fwdB] @ EB_fwd
    A_mat[10:20, 15:20] = PB[:, bwdB]
    B_mat[10:20, 0:5] = PA[:, fwdA]
    B_mat[10:20, 5:10] = PA[:, bwdA] @ EA_bwd

    try:
        evals = eig(A_mat, B_mat, right=False)
    except Exception:
        evals = np.zeros(20, dtype=complex)

    # Standard transfer matrix cond for monitoring
    TA, _, cond_TA = solverA.compute_transfer_matrix(omega, a1)
    TB, _, cond_TB = solverB.compute_transfer_matrix(omega, a2)
    Tcell = TB @ TA
    r_T = np.maximum(np.linalg.norm(Tcell, axis=1, keepdims=True), 1e-30)
    Tc_r = Tcell / r_T
    c_T = np.maximum(np.linalg.norm(Tc_r, axis=0, keepdims=True), 1e-30)
    cond_Tcell = float(np.linalg.cond(Tc_r / c_T))

    bloch_modes = []
    for ev in evals:
        if not np.isfinite(ev) or abs(ev) < 1e-15:
            continue
        mag_ev = abs(ev)
        log_ev = -1j * np.log(ev)
        kr = float(log_ev.real)
        kr_a_bz = abs(kr) % (2.0 * np.pi)
        if kr_a_bz > np.pi:
            kr_a_bz = 2.0 * np.pi - kr_a_bz
        ki = float(log_ev.imag)
        bloch_modes.append({
            "eigval": complex(ev),
            "kr_a": kr_a_bz,
            "ki_signed": ki,
            "alpha_a": abs(ki),
            "is_forward": bool(mag_ev <= 1.0001),
        })

    return bloch_modes, cond_PA, 0.0


def track_branches(prev_modes, curr_modes):
    if not prev_modes:
        sorted_modes = sorted(curr_modes, key=lambda m: (m["kr_a"], m["alpha_a"]))
        for i, m in enumerate(sorted_modes):
            m["branch_id"] = i
        return sorted_modes

    N_prev = len(prev_modes)
    N_curr = len(curr_modes)
    cost_matrix = np.zeros((N_prev, N_curr))
    for i, m_p in enumerate(prev_modes):
        kp = m_p["kr_a"] + 1j * m_p["ki_signed"]
        for j, m_c in enumerate(curr_modes):
            kc = m_c["kr_a"] + 1j * m_c["ki_signed"]
            cost_matrix[i, j] = abs(kc - kp) / (abs(kp) + 0.1)
    cost_matrix = np.nan_to_num(cost_matrix, nan=1e5, posinf=1e5, neginf=1e5)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    tracked = []
    assigned_cols = set()
    for r, c in zip(row_ind, col_ind):
        m = curr_modes[c]
        m["branch_id"] = prev_modes[r]["branch_id"]
        tracked.append(m)
        assigned_cols.add(c)

    next_id = max(m["branch_id"] for m in tracked) + 1 if tracked else 0
    for j, m in enumerate(curr_modes):
        if j not in assigned_cols:
            m["branch_id"] = next_id
            next_id += 1
            tracked.append(m)
    return tracked


def extract_bandgaps_from_raw(case_raw, alpha_pass=0.05, kr_min=0.01, dOm_min=0.02):
    """
    Phase-A corrected gap extraction: propagating coverage is evaluated on the
    RAW Bloch modes at each frequency (tracking-independent), removing any
    dependence on Hungarian branch assignment. A frequency is propagating iff
    ANY mode satisfies 0.01 < kr < pi-0.01 and alpha_a < alpha_pass.
    """
    omegas = sorted(case_raw.keys())
    is_pass = {}
    for om in omegas:
        is_pass[om] = any((m["kr_a"] > kr_min) and (m["kr_a"] < (np.pi - kr_min))
                          and (m["alpha_a"] < alpha_pass) for m in case_raw[om])
    gaps = []
    in_gap = False
    g_start = None
    gap_idx = 1
    for om in omegas:
        if not is_pass[om] and not in_gap:
            in_gap = True
            g_start = om
        elif is_pass[om] and in_gap:
            in_gap = False
            g_end = om
            dOm = g_end - g_start
            if dOm >= dOm_min:
                mid = 0.5 * (g_start + g_end)
                gaps.append({
                    "gap_index": gap_idx,
                    "Omega_L": round(g_start, 4),
                    "Omega_U": round(g_end, 4),
                    "delta_Omega": round(dOm, 4),
                    "Omega_mid": round(mid, 4),
                    "gap_to_midgap_ratio": round(dOm / mid, 4),
                    "is_boundary_truncated": False,
                })
                gap_idx += 1
    if in_gap:
        dOm = omegas[-1] - g_start
        if dOm >= dOm_min:
            mid = 0.5 * (g_start + omegas[-1])
            gaps.append({
                "gap_index": gap_idx,
                "Omega_L": round(g_start, 4),
                "Omega_U": round(omegas[-1], 4),
                "delta_Omega": round(dOm, 4),
                "Omega_mid": round(mid, 4),
                "gap_to_midgap_ratio": round(dOm / mid, 4),
                "is_boundary_truncated": True,
            })
    return gaps


def extract_bandgaps_from_case(case_records):
    """Gap extraction for a single case (propagating-coverage criterion)."""
    prop_omegas = set(r["Omega"] for r in case_records if r["is_pass_band"])
    all_omegas = sorted(set(r["Omega"] for r in case_records))
    gaps = []
    in_gap = False
    g_start = None
    gap_idx = 1
    for om in all_omegas:
        is_prop = (om in prop_omegas)
        if not is_prop and not in_gap:
            in_gap = True
            g_start = om
        elif is_prop and in_gap:
            in_gap = False
            g_end = om
            dOm = g_end - g_start
            if dOm >= 0.02:
                mid = 0.5 * (g_start + g_end)
                gaps.append({
                    "gap_index": gap_idx,
                    "Omega_L": round(g_start, 4),
                    "Omega_U": round(g_end, 4),
                    "delta_Omega": round(dOm, 4),
                    "Omega_mid": round(mid, 4),
                    "gap_to_midgap_ratio": round(dOm / mid, 4),
                    "is_boundary_truncated": False,
                })
                gap_idx += 1
    if in_gap:
        dOm = all_omegas[-1] - g_start
        if dOm >= 0.02:
            mid = 0.5 * (g_start + all_omegas[-1])
            gaps.append({
                "gap_index": gap_idx,
                "Omega_L": round(g_start, 4),
                "Omega_U": round(all_omegas[-1], 4),
                "delta_Omega": round(dOm, 4),
                "Omega_mid": round(mid, 4),
                "gap_to_midgap_ratio": round(dOm / mid, 4),
                "is_boundary_truncated": True,
            })
    return gaps


# -----------------------------------------------------------------------------
# Grid campaign
# -----------------------------------------------------------------------------

def main():
    t0 = time.time()
    with open(os.path.join(PKG, "04_PRODUCTION_DATA", "PHASE3_PARAMETER_MATRIX.json")) as f:
        cfg = json.load(f)

    a = cfg["lattice_geometry"]["lattice_constant_a_m"]
    vm = cfg["frequency_sampling"]["reference_velocity_vm_m_s"]
    Omega_grid = np.linspace(0.05, 1.80, 100)

    matA_base = MaterialParameters(
        name="Epoxy (Layer A)",
        rho=cfg["layer_A_epoxy"]["rho_kg_m3"], mu=cfg["layer_A_epoxy"]["mu_Pa"],
        lambda_param=cfg["layer_A_epoxy"]["lambda_Pa"], c=cfg["layer_A_epoxy"]["c_m2"],
        d=cfg["layer_A_epoxy"]["d_m"], k=cfg["layer_A_epoxy"]["k_W_m_K"],
        cv=cfg["layer_A_epoxy"]["cv_J_kg_K"], alpha_t=cfg["layer_A_epoxy"]["alpha_t_1_K"],
        T0=cfg["layer_A_epoxy"]["T0_K"], tau_q=cfg["layer_A_epoxy"]["tau_q_baseline_s"],
        tau_theta=cfg["layer_A_epoxy"]["tau_theta_baseline_s"],
    )
    matB_base = MaterialParameters(
        name="Aluminum (Layer B)",
        rho=cfg["layer_B_aluminum"]["rho_kg_m3"], mu=cfg["layer_B_aluminum"]["mu_Pa"],
        lambda_param=cfg["layer_B_aluminum"]["lambda_Pa"], c=cfg["layer_B_aluminum"]["c_m2"],
        d=cfg["layer_B_aluminum"]["d_m"], k=cfg["layer_B_aluminum"]["k_W_m_K"],
        cv=cfg["layer_B_aluminum"]["cv_J_kg_K"], alpha_t=cfg["layer_B_aluminum"]["alpha_t_1_K"],
        T0=cfg["layer_B_aluminum"]["T0_K"], tau_q=cfg["layer_B_aluminum"]["tau_q_baseline_s"],
        tau_theta=cfg["layer_B_aluminum"]["tau_theta_baseline_s"],
    )

    def interpolate_mat(mat1, mat2, frac):
        return MaterialParameters(
            name=f"Contrast_{frac:.3f}",
            rho=(1 - frac) * mat1.rho + frac * mat2.rho,
            mu=(1 - frac) * mat1.mu + frac * mat2.mu,
            lambda_param=(1 - frac) * mat1.lambda_param + frac * mat2.lambda_param,
            c=(1 - frac) * mat1.c + frac * mat2.c,
            d=(1 - frac) * mat1.d + frac * mat2.d,
            k=(1 - frac) * mat1.k + frac * mat2.k,
            cv=(1 - frac) * mat1.cv + frac * mat2.cv,
            alpha_t=(1 - frac) * mat1.alpha_t + frac * mat2.alpha_t,
            T0=mat1.T0, tau_q=mat1.tau_q, tau_theta=mat1.tau_theta,
        )

    chi_vals = [round(v, 3) for v in np.linspace(0.0, 1.0, 11)]
    eta_vals = [round(v, 3) for v in np.linspace(0.2, 0.8, 11)]
    print(f"Grid: {len(chi_vals)} chi x {len(eta_vals)} eta = {len(chi_vals)*len(eta_vals)} cases "
          f"(DPL-active baseline, Omega in [0.05,1.80], 100 steps)")

    gap_rows = []
    metric_rows = []
    for eta in eta_vals:
        a1 = eta * a
        a2 = (1.0 - eta) * a
        for chi in chi_vals:
            matB = interpolate_mat(matA_base, matB_base, chi) if chi > 0 else matA_base
            tc = time.time()
            prev_modes = []
            case_records = []
            case_raw = {}
            worst_cond_P = 0.0
            for Om in Omega_grid:
                omega = Om * 2.0 * np.pi * vm / a
                raw_modes, cond_P, cond_T = solve_unit_cell_bloch(matA_base, matB, a1, a2, omega, xi=0.0)
                worst_cond_P = max(worst_cond_P, cond_P)
                # Phase-A: retain ALL raw modes for tracking-independent gap extraction
                case_raw[float(Om)] = [{"kr_a": float(m["kr_a"]), "alpha_a": float(m["alpha_a"])}
                                        for m in raw_modes]
                fwd_modes = [m for m in raw_modes if m["is_forward"]]
                if len(fwd_modes) < 5:
                    fwd_modes = sorted(raw_modes, key=lambda m: m["alpha_a"])[:5]
                else:
                    fwd_modes = sorted(fwd_modes, key=lambda m: m["alpha_a"])[:5]
                tracked = track_branches(prev_modes, fwd_modes)
                prev_modes = tracked
                for m in tracked:
                    is_pass = bool(m["alpha_a"] < 0.05 and 0.01 < m["kr_a"] < (np.pi - 0.01))
                    case_records.append({"Omega": float(Om), "alpha_a": float(m["alpha_a"]),
                                         "is_pass_band": is_pass})
            gaps = extract_bandgaps_from_raw(case_raw)
            dt = time.time() - tc
            for g in gaps:
                gap_rows.append({"chi": chi, "eta": eta, **g})
            pass_a = [r["alpha_a"] for r in case_records if r["is_pass_band"]]
            stop_a = [r["alpha_a"] for r in case_records if not r["is_pass_band"]]
            metric_rows.append({
                "chi": chi, "eta": eta,
                "runtime_s": round(dt, 3),
                "worst_cond_P": float(f"{worst_cond_P:.6g}"),
                "pass_alpha_mean": float(np.mean(pass_a)) if pass_a else 0.0,
                "stop_alpha_peak": float(np.max(stop_a)) if stop_a else 0.0,
                "n_gaps": len(gaps),
            })
            g1 = gaps[0] if gaps else None
            print(f"  chi={chi:.1f} eta={eta:.1f}: gaps={len(gaps)}"
                  + (f", G1=[{g1['Omega_L']:.4f},{g1['Omega_U']:.4f}] dW={g1['delta_Omega']:.4f}"
                     f"{' TRUNC' if g1['is_boundary_truncated'] else ''}" if g1 else ", no gap")
                  + f" ({dt:.1f}s)")

    # Sanity anchors vs frozen production data
    anchors = {
        (1.0, 0.5): (0.6687, 0.7040),
        (0.5, 0.5): (0.9162, 1.0045),
        (1.0, 0.2): (0.5626, 0.7394),
        (1.0, 0.8): (0.6687, 0.9338),
    }
    print("\n--- Sanity anchors vs PRODUCTION_BANDGAP_SUMMARY.csv (Gap 1, DPL) ---")
    all_ok = True
    lookup = {(r["chi"], r["eta"]): r for r in gap_rows if r["gap_index"] == 1}
    for (chi, eta), (L, U) in anchors.items():
        r = lookup.get((chi, eta))
        if r is None:
            print(f"  ({chi},{eta}): no Gap 1 found!")
            all_ok = False
            continue
        ok = abs(r["Omega_L"] - L) <= 0.02 + 1e-9 and abs(r["Omega_U"] - U) <= 0.02 + 1e-9
        all_ok &= ok
        print(f"  ({chi},{eta}): grid=({r['Omega_L']:.4f},{r['Omega_U']:.4f}) "
              f"frozen=({L:.4f},{U:.4f}) -> {'MATCH' if ok else 'MISMATCH'}")

    data_dir = os.path.join(PKG, "04_PRODUCTION_DATA")
    with open(os.path.join(data_dir, "SUPP_CHI_ETA_GAP_SUMMARY.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(gap_rows[0].keys()))
        w.writeheader()
        w.writerows(gap_rows)
    with open(os.path.join(data_dir, "SUPP_CHI_ETA_CASE_METRICS.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(metric_rows[0].keys()))
        w.writeheader()
        w.writerows(metric_rows)
    meta = {
        "document": "SUPP_CHI_ETA_GRID_META.json",
        "campaign": "Phase-0 supplementary 2-D (chi, eta) grid, DPL-active baseline",
        "governing_solver": "03_SOURCE_CODE/transfer_matrix (frozen)",
        "runner": "03_SOURCE_CODE/production/run_chi_eta_grid.py",
        "gap_extraction": "Phase-A: raw-mode propagating classification (tracking-independent; "
                          "pass at Omega iff any mode has 0.01 < kr < pi-0.01 and alpha_a < 0.05)",
        "chi_values": chi_vals,
        "eta_values": eta_vals,
        "omega_grid": {"range": [0.05, 1.80], "steps": 100},
        "vm_m_s": vm,
        "a_m": a,
        "anchors_passed": bool(all_ok),
        "total_runtime_s": round(time.time() - t0, 2),
    }
    with open(os.path.join(data_dir, "SUPP_CHI_ETA_GRID_META.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"\nSaved {len(gap_rows)} gap rows + {len(metric_rows)} metric rows -> 04_PRODUCTION_DATA/")
    print(f"Anchors passed: {all_ok}; total runtime {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
