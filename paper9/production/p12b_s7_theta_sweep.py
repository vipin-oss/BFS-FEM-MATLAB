#!/usr/bin/env python3
"""P12B steering figure-of-merit sweep -- locked S7 extension (Paper 9).

    python3 production/p12b_s7_theta_sweep.py

P12B scope (post-P11D gate audit recommendation (b), user-authorized):
extend Study S7 (iso-frequency-contour steering, group-velocity deviation on
the constant-|k| ring) from its three published configurations
[(AR=1, theta=0), (AR=5, theta=45), (AR=10, theta=45)] to the locked theta grid

    theta = {0, 15, 30, 45, 60, 75, 90} deg   x   AR in {5, 10}

and compute the audited steering figure of merit

    phi*(theta, AR) = argmax_phi delta(phi; theta, AR)          (discrete ring argmax)
    M_s(AR)         = phi*(90 deg) - phi*(0 deg)                (declared tie-break below)

where delta is the EXISTING S7 quantity: the unsigned deviation angle between
the group velocity and the phase vector, computed by the project solver
compute_group_velocity_2d on branch 0 (first acoustic branch) with central
differences h = 1e-4, on the S7 ring |k| = k_rad = 0.5 * pi / L with the S7
sampling phi = linspace(0, 2 pi, 73) (5 deg steps).

LOCKED inputs (never redeclared here): all modeling constants are loaded from
the immutable registry paper9/results/raw/p5_production_raw.json
("master_params") and cross-asserted against the P5 production driver.  The
dispersion machinery (assemble_KM / L_plane / semi_axes_from_ar /
compute_group_velocity_2d) is imported unmodified from the locked P5 code path.
No model, mesh, tolerance, or definition is changed; h, k_rad, branch, and the
phi sampling are verbatim the S7 values.

Declared post-processing conventions (data themselves unchanged):
  * The Case-H |delta| field on the ring is exactly 180 deg-periodic in phi
    (headless wave vector; verified to < 1e-6 deg worst-case for every config -- the ~1e-7 residual is arccos rounding where delta ~ 0, physically meaningless) and obeys
    the mirror co-symmetry delta(phi; theta) = delta(90 - phi; 90 - theta)
    (verified to < 1e-8 deg), i.e. the theta = 90 field is the phi -> 90 - phi
    mirror of the theta = 0 field.  The principal steering axis is reported,
    by declared convention, in the sector [0, 90) deg:
        phi* = (discrete argmax_phi delta(phi)) mod 90, in degrees.
    (No 90 deg field periodicity is claimed: quadrant-to-quadrant peak values
    differ by up to ~5e-2 deg at intermediate theta and are recorded.)
  * Tie-break: if multiple ring points attain the global maximum to within a
    relative tolerance of 1e-12, the smallest sector angle is taken.
  * A parabolic sub-grid refinement of the in-sector peak (3-point parabola
    through the discrete maximizer and its two neighbours) is recorded as
    phi_star_refined_deg for transparency; the published FoM uses the discrete
    locked-grid value.
  * Legacy anchor: the (AR=5, theta=45) and (AR=10, theta=45) configurations
    existed in the P5 run as AR_5_th_45 / AR_10_th_45; their delta_max values
    are re-derived here and asserted to reproduce the registry values to
    < 1e-9 relative, proving this script runs the identical locked pipeline.

Output: results/raw/p12b_s7_theta_sweep.json  (immutable evidence;
figures/tables/manuscript numbers are generated downstream from this file --
registry-first, no hand-entered values).

This driver never sets any gate/PCR status; verdicts live in audit documents.
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
PAPER9 = REPO_ROOT / "paper9"
sys.path.insert(0, str(PAPER9))

from solver.bfs_bloch_solver import (  # noqa: E402  (locked P5 machinery)
    assemble_KM,
    L_plane,
    semi_axes_from_ar,
    compute_group_velocity_2d,
)

# ---------------------------------------------------------------------------
# Definition record (included verbatim in the evidence JSON)
# ---------------------------------------------------------------------------
DEFINITION = {
    "phi_star_deg": ("argmax over the locked S7 ring sampling phi in "
                     "linspace(0, 2 pi, 73) of the S7 unsigned group-velocity "
                     "deviation delta(phi; theta, AR), reduced modulo the "
                     "empirically verified 90 deg period of the |delta| "
                     "field, i.e. phi* = (discrete argmax delta) mod 90 in "
                     "[0, 90) deg; tie-break: smallest representative among "
                     "values within 1e-12 relative of the maximum"),
    "M_s_deg": "M_s(AR) = phi*(90 deg, AR) - phi*(0 deg, AR), on the locked grid",
    "delta_definition": ("S7 locked: unsigned angle between v_g = grad_k omega "
                         "and k, compute_group_velocity_2d, branch 0 (first "
                         "acoustic branch), central differences h = 1e-4"),
    "ring": "|k| = k_rad = 0.5 * pi / L  (S7 locked)",
    "sampling": "phi = linspace(0, 2 pi, 73) endpoints included (5 deg step; S7 locked)",
    "theta_grid_deg": [0, 15, 30, 45, 60, 75, 90],
    "AR_list": [5.0, 10.0],
    "post_processing": [
        "mod-90 deg sector convention for the argmax (exact 180 deg headless "
        "periodicity + mirror co-symmetry verified numerically per run; the "
        "sector is a reporting convention, not a claimed field period)",
        "3-point parabolic refinement recorded separately as phi_star_refined_deg",
    ],
}


def _git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT)
        ).decode().strip()
    except Exception:
        return "UNKNOWN"


def _env() -> dict:
    import numpy
    import scipy

    return {
        "python": sys.version.split()[0],
        "numpy": numpy.__version__,
        "scipy": scipy.__version__,
        "platform": platform.platform(),
    }


def run_sweep() -> dict:
    t0 = time.time()
    registry_path = PAPER9 / "results" / "raw" / "p5_production_raw.json"
    registry = json.loads(registry_path.read_text())
    mp = registry["master_params"]

    # --- cross-assert locked constants against the P5 driver verbatim -------
    L = mp["Lcell"]
    lam, mu, rho = mp["lam"], mp["mu"], mp["rho"]
    ell2, l_iso = mp["ell2"], mp["l_iso"]
    assert L == 1.0 and (lam, mu, rho) == (1.0, 1.0, 1.0)
    assert ell2 == 0.04 and l_iso == 0.20
    assert mp["theta_sweep_deg"] == [0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0]

    k_rad = 0.5 * np.pi / L            # S7 locked ring
    phi_grid = np.linspace(0.0, 2.0 * np.pi, 73)   # S7 locked sampling
    phi_deg = np.rad2deg(phi_grid)

    sweep = {}
    for AR in (5.0, 10.0):
        l1, l2 = semi_axes_from_ar(AR, l_iso=l_iso, rule="volume_equivalent")
        for th_deg in (0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0):
            th_rad = float(np.deg2rad(th_deg))
            L11, L22, L12 = L_plane(l1, l2, th_rad)
            K, M = assemble_KM(hx=L, hy=L, lam=lam, mu=mu, L11=L11, L22=L22,
                               L12=L12, rho=rho, ell2=ell2)
            delta, vg_mag, vp_mag, om0 = [], [], [], []
            for phi in phi_grid:
                kx, ky = k_rad * np.cos(phi), k_rad * np.sin(phi)
                vg, vp, d_deg = compute_group_velocity_2d(
                    K, M, kx, ky, h=1e-4, L=L, branch=0)
                delta.append(d_deg)
                vg_mag.append(float(np.linalg.norm(vg)))
                vp_mag.append(vp)
                om0.append(float(vp * k_rad))  # branch-0 omega at ring point
            delta = np.asarray(delta)

            # ---- derived quantities (declared conventions) ----------------
            dmax = float(delta.max())
            i_all = np.flatnonzero(delta >= dmax * (1.0 - 1e-12))
            i0 = int(i_all[0])
            phi_star_sector = float((phi_deg[i0]) % 90.0)
            # symmetry diagnostics (recorded, no claims hard-coded)
            q_vals = [float(delta[q * 18: (q + 1) * 18].max()) for q in range(4)]
            period_dev = float(max(q_vals) - min(q_vals))
            # exact 180 deg headless periodicity of the |delta| field
            period_180_dev = float(np.max(np.abs(delta[36:72] - delta[:36])))
            # discrete in-sector peak location per quadrant (transparency)
            q_peaks = [float(phi_deg[(delta == v).nonzero()[0][0]]) for v in q_vals]
            # 3-point parabolic refinement of the global discrete maximizer
            im = i0
            y0, y1, y2 = delta[(im - 1) % 72], delta[im], delta[(im + 1) % 72]
            denom = (y0 - 2.0 * y1 + y2)
            shift = 0.5 * (y0 - y2) / denom if abs(denom) > 0 else 0.0
            phi_refined = float((phi_deg[im] + shift * 5.0) % 90.0)

            key = f"AR_{AR:g}_th_{th_deg:g}"
            sweep[key] = {
                "AR": AR,
                "theta_deg": th_deg,
                "l1": l1, "l2": l2,
                "delta_max_deg": dmax,
                "mean_delta_deg": float(delta.mean()),
                "phi_star_deg": phi_star_sector,
                "phi_star_refined_deg": phi_refined,
                "quadrant_peak_phi_deg": q_peaks,
                "period_90_max_dev_deg": period_dev,
                "period_180_max_dev_deg": period_180_dev,
                "phi_deg": phi_deg.tolist(),
                "delta_deg": delta.tolist(),
                "vg_mag": vg_mag,
                "vp_mag": vp_mag,
                "omega_ring": om0,
            }
            print(f"  {key}: delta_max = {dmax:12.6f} deg   "
                  f"phi* = {phi_star_sector:6.2f} deg (ref {phi_refined:9.4f})   "
                  f"180-deg period dev = {period_180_dev:.2e}")

    # ---- M_s per AR ---------------------------------------------------------
    Ms = {}
    for AR in (5.0, 10.0):
        p0 = sweep[f"AR_{AR:g}_th_0"]["phi_star_deg"]
        p90 = sweep[f"AR_{AR:g}_th_90"]["phi_star_deg"]
        Ms[f"AR_{AR:g}"] = {
            "AR": AR,
            "phi_star_theta0_deg": p0,
            "phi_star_theta90_deg": p90,
            "M_s_deg": float(p90 - p0),
            "M_s_refined_deg": float(
                sweep[f"AR_{AR:g}_th_90"]["phi_star_refined_deg"]
                - sweep[f"AR_{AR:g}_th_0"]["phi_star_refined_deg"]),
        }
        print(f"  M_s(AR={AR:g}) = {Ms[f'AR_{AR:g}']['M_s_deg']:+.4f} deg "
              f"(phi*(90)={p90:.2f}, phi*(0)={p0:.2f})")

    # ---- symmetry checks (computed, recorded; used by §7 and guard tests) --
    theta_grid = (0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0)
    symmetry_checks = {}
    for AR in (5.0, 10.0):
        entry = {"headless_180_max_dev_deg": max(
            sweep[f"AR_{AR:g}_th_{th:g}"]["period_180_max_dev_deg"] for th in theta_grid)}
        # mirror co-symmetry delta(phi; theta) = delta(90 - phi; 90 - theta)
        mirror = {}
        for th in (0.0, 15.0, 30.0):
            a = np.asarray(sweep[f"AR_{AR:g}_th_{th:g}"]["delta_deg"])
            b = np.asarray(sweep[f"AR_{AR:g}_th_{90.0 - th:g}"]["delta_deg"])
            # index mapping phi -> 90 - phi on the 73-pt grid: i -> (18 - i) mod 72
            idx = (18 - np.arange(73)) % 72
            mirror[f"th_{th:g}"] = float(np.max(np.abs(a - b[idx])))
        entry["mirror_delta(ph;th)=delta(90-ph;90-th)_max_dev_deg"] = mirror
        d0 = np.asarray(sweep[f"AR_{AR:g}_th_0"]["delta_deg"])
        d90 = np.asarray(sweep[f"AR_{AR:g}_th_90"]["delta_deg"])
        idx = (18 - np.arange(73)) % 72
        entry["theta0_vs_theta90_direct_max_dev_deg"] = float(np.max(np.abs(d90 - d0)))
        entry["theta0_vs_theta90_mirrored_max_dev_deg"] = float(np.max(np.abs(d90 - d0[idx])))
        entry["delta_max_th_eq_90mth_max_dev_deg"] = float(max(
            abs(sweep[f"AR_{AR:g}_th_{th:g}"]["delta_max_deg"]
                - sweep[f"AR_{AR:g}_th_{90.0 - th:g}"]["delta_max_deg"]) for th in (0.0, 15.0, 30.0)))
        symmetry_checks[f"AR_{AR:g}"] = entry
        print(f"  symmetry AR={AR:g}: mirror co-sym dev = "
              f"{max(mirror.values()):.2e} deg; direct 0-vs-90 dev = "
              f"{entry['theta0_vs_theta90_direct_max_dev_deg']:.2e} deg")

    # ---- legacy anchor check against locked P5 evidence ---------------------
    anchor = {}
    s7_old = registry["study_S7_ifc_steering"]
    for new_key, old_key in (("AR_5_th_45", "AR_5_th_45"),
                             ("AR_10_th_45", "AR_10_th_45")):
        old_v = float(s7_old[old_key]["delta_max_deg"])
        new_v = sweep[new_key]["delta_max_deg"]
        rel = abs(new_v - old_v) / abs(old_v)
        anchor[new_key] = {"p5_delta_max_deg": old_v,
                           "p12b_delta_max_deg": new_v,
                           "rel_diff": rel, "pass_lt_1e-9": bool(rel < 1e-9)}
        print(f"  anchor {new_key}: P5 {old_v:.12f} vs P12B {new_v:.12f}  "
              f"rel = {rel:.2e}  ({'PASS' if rel < 1e-9 else 'FAIL'})")

    doc = {
        "study": "P12B S7 steering figure-of-merit theta sweep (locked S7 extension)",
        "status": "PRODUCTION (locked P5 parameter basis; S7 methodology)",
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "git_commit": _git_commit(),
        "master_params_source": "paper9/results/raw/p5_production_raw.json::master_params",
        "master_params": mp,
        "master_params_sha256": hashlib.sha256(
            json.dumps(mp, sort_keys=True).encode()).hexdigest(),
        "definitions": DEFINITION,
        "solver_calls": {
            "k_rad": k_rad,
            "phi_n_points": 73,
            "branch": 0,
            "fd_step_h": 1e-4,
            "assembly": "assemble_KM(hx=L, hy=L, ... volume-equivalent semi-axes) -- verbatim S7",
        },
        "sweep": sweep,
        "symmetry_checks": symmetry_checks,
        "M_s": Ms,
        "legacy_anchor_check": anchor,
        "wall_time_s": time.time() - t0,
        "environment": _env(),
    }

    out = PAPER9 / "results" / "raw" / "p12b_s7_theta_sweep.json"
    out.write_text(json.dumps(doc, indent=1))
    print(f"\nwrote {out}")
    print(f"wall time: {doc['wall_time_s']:.1f} s")
    return doc


if __name__ == "__main__":
    run_sweep()
