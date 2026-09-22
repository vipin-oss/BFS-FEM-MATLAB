#!/usr/bin/env python3
"""P5 production run driver (Paper 9).

    python3 production/p5/p5_run.py --params params/<file>.yaml

Produces, for the requested case, an immutable raw dataset under results/raw/<run_id>/:
    bands_path.npz   k-path, omega, omega^2, leg ids, phase velocity
    zone_omega.npz   omega on the full-BZ grid (gap verification + IFC dataset)
    vg_zone.npz      group velocity on the zone grid (central differences, M12 (51))
    gaps.json        directional / path / complete gaps (M12.3)
    checks.json      integrity checks with pass/fail and residuals
    manifest.json    run id, git commit, parameter snapshot + hash, env, output hashes
    run_log.txt      full driver log (stdout capture of this run)
A byte-identical copy of manifest.json is also written to runs/<run_id>/manifest.json
(the location named by plan/CALC_MASTER_PLAN.md section I), so the plan path and the
self-contained run directory never diverge.

Exit code 0 only if every integrity check passes. The manifest distinguishes a
PILOT run (machinery validation on a declared parameter basis) from a PRODUCTION
run (locked parameter set). This driver never sets the P5 gate: gate status lives
in audit/P5_STATUS.md.
"""
from __future__ import annotations

import argparse
import multiprocessing as mp
import os
import sys
import time
from pathlib import Path

# Thread pinning must happen before the first numpy/scipy import. Measured on the
# P5 pre-flight box (2 CPUs): two workers with 2 BLAS threads each ran 5.2x SLOWER
# per k-point than two workers with 1 thread each (spline-factorisation oversub-
# scription). This is a scheduling setting only; the spectrum is unchanged (it is
# checked: identical w2 to 0.0 in the n_proc 1 vs 2 comparison).
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np  # noqa: E402

try:  # runtime limiter, effective even when numpy was imported earlier (tests)
    from threadpoolctl import threadpool_limits
except Exception:  # pragma: no cover
    threadpool_limits = None

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import p5_core as core  # noqa: E402

# Structural literals of this driver only (no scientific value; the scientific
# values and every solver setting are read from the params file).
NUMERIC_LITERAL_ALLOWLIST = {
    0: "index / additive identity, and axis=0 of np.gradient",
    1: "stride, second axis of np.gradient, reciprocal-vector factor",
    -1: "sequence reversal (slice step; symmetric zone grid)",
    2: "two components of k; double reciprocal vector",
    3: "third leg index used to pick a representative path point",
    4: "worker chunk size for the k-point pool",
    8: "8 DOF per BFS node (2 components x 4 types, M13)",
    16: "hex digest prefix length in reporting",
    20: "worker recycling interval (maxtasksperchild) to bound worker memory",
    25: "default progress print cadence",
    78: "log banner width (presentation only)",
    0.0: "additive identity in comparisons",
    2.0: "reciprocal lattice vectors 2*pi/L and double of them",
}


class _Tee:
    """stdout mirror: keeps the driver log in memory for run_log.txt."""

    def __init__(self, stream):
        self.stream = stream
        self.buf = []

    def write(self, text):
        self.buf.append(text)
        return self.stream.write(text)

    def flush(self):
        self.stream.flush()


def _solve_pair(job):
    kx, ky, conf, solver, with_vectors = job
    if threadpool_limits is not None:
        with threadpool_limits(limits=1):
            return core.band_solve(kx, ky, conf, solver, with_vectors=with_vectors)
    return core.band_solve(kx, ky, conf, solver, with_vectors=with_vectors)


def _solve_many(ks, conf, solver, with_vectors, n_proc, label, cadence=25):
    jobs = [(float(k[0]), float(k[1]), conf, solver, with_vectors) for k in ks]
    out = [None] * len(jobs)
    t0 = time.time()
    if n_proc > 1 and len(jobs) > 4:
        ctx = mp.get_context("fork")
        with ctx.Pool(processes=n_proc, maxtasksperchild=20) as pool:
            for i, r in enumerate(pool.imap(_solve_pair, jobs, chunksize=4)):
                out[i] = r
                if (i + 1) % cadence == 0:
                    print(f"    [{label}] {i+1}/{len(jobs)} k-points "
                          f"({time.time()-t0:.0f}s)", flush=True)
    else:
        for i, jb in enumerate(jobs):
            out[i] = _solve_pair(jb)
            if (i + 1) % cadence == 0:
                print(f"    [{label}] {i+1}/{len(jobs)} k-points "
                      f"({time.time()-t0:.0f}s)", flush=True)
    print(f"    [{label}] done: {len(jobs)} k-points in {time.time()-t0:.0f}s", flush=True)
    return out


def _zone_solver(solver):
    """Zone-grid solves only feed gap/coverage checks: they report the lowest
    n_bands and are never tracked, so the tracking buffer is not requested there
    (solver setting only; the reported spectrum is unchanged)."""
    return dict(solver, n_bands_buffer=0)


def _mac_streaming(ks, V, w2_all, conf, solver, n_reported):
    """MAC continuation without retaining a matrix per k-point (memory bound)."""
    steps = []
    prev = V[0]
    for i in range(1, len(ks)):
        M = core.reduced_matrices(float(ks[i][0]), float(ks[i][1]), conf)[1]
        steps.append(core.mac_step(prev, V[i], M, w2_all[i - 1], w2_all[i], solver,
                                   n_reported, int(solver.get("track_guard", 2))))
        prev = V[i]
    vals = [s["min_mac_matched"] for s in steps if s["min_mac_matched"] is not None]
    worst = min(vals, default=1.0)
    return {
        "n_steps": len(steps), "min_mac": worst,
        "min_mac_step": next((i + 1 for i, s in enumerate(steps)
                              if s["min_mac_matched"] == worst), None),
        "n_evaluable_steps": len(vals),
        "n_steps_without_evaluable_mode": sum(1 for s in steps if s["min_mac_matched"] is None),
        "reordering_steps": [i + 1 for i, s in enumerate(steps) if s["reordered_reported"]],
        "reordering_pairs": [s["swap_pairs"] for s in steps if s["reordered_reported"]],
        "matched_into_buffer_steps": [i + 1 for i, s in enumerate(steps)
                                      if s["matched_into_buffer"]],
        "max_abs_index_drift": max((s["max_abs_index_drift"] for s in steps), default=0),
        "steps_with_guard_risk": [i + 1 for i, s in enumerate(steps)
                                  if s["n_partners_in_guard"] > 0],
        "mac_min_tol": float(solver["mac_min"]),
        "steps": steps,
    }


def main(argv=None) -> int:
    tee = _Tee(sys.stdout)
    sys.stdout = tee
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True, type=Path)
    ap.add_argument("--outdir", default=str(core.REPO / "results" / "raw"), type=Path)
    args = ap.parse_args(argv)

    params = core.load_params(args.params)
    vals = core.resolved_values(params)
    phash = core.params_hash(params)
    conf = core.solve_conf(params)
    solver = core.solver_conf(params)
    sampling = params["sampling"]
    meta = params.get("meta", {})
    case = meta.get("case", "H")
    status = meta.get("status", "PILOT")
    run_id = core.make_run_id(case, str(status).lower(), phash)

    print("=" * 78)
    print(f"P5 run {run_id}")
    print(f"  case={case}  status={status}  params_file={args.params}")
    print(f"  params_hash={phash}")
    print(f"  parameters: {vals}")
    print(f"  study     : {params.get('study', {})}")
    print(f"  sampling  : {sampling}")
    print(f"  solver    : {solver}")
    if status != "PRODUCTION":
        print("  NOTE: parameters are NOT the locked production set; this dataset is"
              " machinery validation only and must not be reported as a paper result.")
    print("=" * 78, flush=True)

    floor = core.p4b_resolution_floor()
    print(f"P4B resolution floor: eps_Delta={floor['eps_Delta']:.6e} "
          f"(validated n_mesh up to {floor['n_mesh_validated']})", flush=True)

    group = core.point_group(conf["theta_deg"], conf["l1"], conf["l2"],
                             float(solver["group_tol"]))
    print(f"point group of the locked operator (M10.3): {group}", flush=True)

    # ---------------- path ---------------- #
    ks_p, legs = core.path_points(conf["L"], int(sampling["path_N_seg"]))
    print(f"path: 3 legs x {sampling['path_N_seg']} + 1 = {len(ks_p)} k-points", flush=True)
    res_p = _solve_many(ks_p, conf, solver, True, int(solver.get("n_proc", 1)), "path",
                        cadence=int(solver.get("progress_cadence", 25)))
    w2_p = np.array([r["w2"] for r in res_p])
    w_p = core.omega_from_w2(w2_p)
    V_p = [r["V"] for r in res_p]
    w2_p_all = [r["w2_all"] for r in res_p]
    track = _mac_streaming(ks_p, V_p, w2_p_all, conf, solver, conf["n_bands"])

    # ---------------- zone (full-BZ superset; M10-a §6) ---------------- #
    sol_z = _zone_solver(solver)
    ks_z, (n1, n2) = core.zone_grid(conf["L"], int(sampling["zone_N1"]),
                                    int(sampling["zone_N2"]))
    mask_irr = core.irreducible_subset(ks_z, group)
    print(f"zone grid: {n1}x{n2} = {len(ks_z)} k-points; irreducible subset ({group}): "
          f"{int(mask_irr.sum())} points ({mask_irr.sum()/len(ks_z):.3f} of the grid)", flush=True)
    res_z = _solve_many(ks_z, conf, sol_z, False, int(solver.get("n_proc", 1)), "zone",
                        cadence=int(solver.get("progress_cadence", 25)))
    w2_z = np.array([r["w2"] for r in res_z])
    w_z = core.omega_from_w2(w2_z)

    # ---------------- velocities ---------------- #
    k1 = np.unique(ks_z[:, 0])
    k2 = np.unique(ks_z[:, 1])
    dk1, dk2 = float(k1[1] - k1[0]), float(k2[1] - k2[0])
    W = w_z.reshape(n1, n2, conf["n_bands"])
    vg = np.stack([np.gradient(W, dk1, axis=0).reshape(-1, conf["n_bands"]),
                   np.gradient(W, dk2, axis=1).reshape(-1, conf["n_bands"])], axis=-1)
    nrm = np.linalg.norm(ks_p, axis=1)
    nz = nrm > float(solver["k_norm_tol"])
    vp = np.zeros_like(w_p)
    vp[nz] = w_p[nz] / nrm[nz, None]

    # ---------------- gaps (M12.3) ---------------- #
    gaps = core.gap_table(w_p, legs, w_z, mask_irr, case,
                          float(solver["ordering_slack_tol"]))

    # ---------------- integrity checks ---------------- #
    checks = []

    def check(name, ok, **kwd):
        checks.append({"name": name, "result": "PASS" if ok else "FAIL", **kwd})
        extra = "  ".join(f"{k}={v}" for k, v in kwd.items())
        print(("PASS: " if ok else "FAIL: ") + name + ("  " + extra if extra else ""), flush=True)

    ndof = res_p[0]["ndof"]
    bad = int(sum(1 for r in res_p + res_z if not np.all(np.isfinite(r["w2"]))))
    check("C1 solver completed on every sampled k; ndof = 8 n^2; all bands returned",
          bad == 0 and ndof == 8 * conf["n_mesh"] ** 2
          and all(len(r["w2"]) == conf["n_bands"] for r in res_p + res_z),
          n_kpoints=len(res_p) + len(res_z), ndof=ndof, nonfinite_solves=bad)

    herm = [core.hermiticity_residual(*core.reduced_matrices(float(k[0]), float(k[1]), conf))
            for k in ks_p[[0, len(ks_p) // 2, len(ks_p) - 1]]]
    hmax = max(max(h["K_rel"], h["M_rel"]) for h in herm)
    check("C2a Hermiticity of the reduced pencil (M15-a pair) on sampled k",
          hmax < float(solver["herm_tol"]), max_rel=hmax, tol=float(solver["herm_tol"]))

    G1 = np.array([2.0 * np.pi / conf["L"], 0.0])
    kt = ks_p[len(ks_p) // 3]
    Kt, _ = core.reduced_matrices(float(kt[0]), float(kt[1]), conf)
    wt = core.omega_from_w2(core.band_solve(float(kt[0]), float(kt[1]), conf, solver)["w2"])
    per, per_w = [], []
    for G in (G1, np.array([0.0, 2.0 * np.pi / conf["L"]]), 2.0 * G1):
        Kb, _ = core.reduced_matrices(float(kt[0]) + G[0], float(kt[1]) + G[1], conf)
        per.append(float(np.linalg.norm((Kb - Kt).data) / np.linalg.norm(Kt.data)))
        wb = core.omega_from_w2(core.band_solve(float(kt[0]) + G[0], float(kt[1]) + G[1],
                                                conf, solver)["w2"])
        per_w.append(float(np.max(np.abs(wb - wt))))
    check("C2b Bloch phase consistency: Kbar(k+G) = Kbar(k) and omega(k+G) = omega(k)",
          max(per) < float(solver["bz_tol"]) and max(per_w) < float(solver["bz_omega_tol"]),
          max_matrix_rel=max(per), max_omega_abs=max(per_w))

    check("C3 mesh resolution at/above the validated P4B floor",
          conf["n_mesh"] >= floor["n_mesh_validated"],
          n_mesh=conf["n_mesh"], floor=floor["n_mesh_validated"], eps_Delta=floor["eps_Delta"])

    check("C4 branch continuity/tracking: matched-mode MAC >= tol over non-degenerate "
          "modes (crossings reported, M12.2) and the tracking window is adequate",
          track["min_mac"] >= float(solver["mac_min"]) and track["n_evaluable_steps"] >= 1
          and not track["steps_with_guard_risk"],
          min_mac=track["min_mac"], min_mac_step=track["min_mac_step"],
          n_evaluable_steps=track["n_evaluable_steps"],
          steps_without_evaluable_mode=track["n_steps_without_evaluable_mode"],
          reordering_steps=track["reordering_steps"],
          reordering_pairs=track["reordering_pairs"],
          max_abs_index_drift=track["max_abs_index_drift"],
          steps_with_guard_risk=track["steps_with_guard_risk"],
          n_requested=track["steps"][0]["n_requested"] if track["steps"] else None,
          tol=float(solver["mac_min"]))

    # Eigenpair residuals of the reported modes, gated only where a per-mode
    # residual is meaningful (a mode inside a degenerate cluster is a mixture of
    # that cluster, so neither its MAC nor its per-mode residual is defined; the
    # cluster degeneracy itself is reported under C5).
    resid_ok, resid_excluded, n_resid_points = [], 0, 0
    for r in res_p:
        deg = r["degenerate_mask"]
        n_resid_points += 1
        for i in range(int(conf["n_bands"])):
            if deg is not None and deg[i]:
                resid_excluded += 1
            else:
                resid_ok.append(r["residuals"][i])
    max_resid = float(max(resid_ok)) if resid_ok else 0.0
    check("C9 eigenpair residuals of reported modes (scale-normalised, non-degenerate) <= tol",
          max_resid < float(solver["residual_tol"]),
          max_residual=max_resid, tol=float(solver["residual_tol"]),
          n_points_checked=n_resid_points, modes_gated=len(resid_ok),
          modes_excluded_degenerate=resid_excluded,
          n_bands_buffer=int(solver.get("n_bands_buffer", 0)))

    filt = [core.mode_filter(w, solver) for w in list(w2_p) + list(w2_z)]
    n_nf = sum(f["nonfinite"] for f in filt)
    n_neg = sum(f["negative"] for f in filt)
    n_null = sum(f["null_modes"] for f in filt)
    check("C5 no NaN/Inf and no unphysical negative eigenvalue silently retained",
          n_nf == 0 and n_neg == 0,
          nonfinite=n_nf, negative=n_neg, null_modes_reported_not_dropped=n_null,
          filter_rule="TV7: only non-finite/negative roots would be flagged; nothing is dropped")

    slack_min = min(p["ordering_slack_path_minus_complete"] for p in gaps["pairs"])
    claimed = [p["n"] for p in gaps["pairs"] if p["complete_gap_claimed"]]
    max_complete = max(p["complete_irreducible_zone"] for p in gaps["pairs"])
    check("C6a frozen gap definition: path gap >= complete gap (sampling slack tolerated)",
          slack_min >= -float(solver["ordering_slack_tol"]),
          min_slack=slack_min, tol=float(solver["ordering_slack_tol"]))
    check("C6b no complete gap claimed where the model cannot have one (Case H, M12 G6)",
          (case != "H") or (len(claimed) == 0 and max_complete <= 0.0),
          case=case, complete_gaps_claimed=claimed, max_complete_gap=max_complete)

    d_even = float(np.max(np.abs(w_z - w_z[::-1])))
    ext_lo = float(np.max(np.abs([np.min(w_z[mask_irr, b]) for b in range(conf["n_bands"])]
                                 - np.array([np.min(w_z[:, b]) for b in range(conf["n_bands"])]))))
    ext_hi = float(np.max(np.abs([np.max(w_z[mask_irr, b]) for b in range(conf["n_bands"])]
                                 - np.array([np.max(w_z[:, b]) for b in range(conf["n_bands"])]))))
    check("C7a k-evenness omega(-k) = omega(k) on the symmetric zone grid",
          d_even < float(solver["bz_omega_tol"]), max_abs_diff=d_even)
    check("C7b irreducible-zone extrema equal full-grid extrema (required coverage realised)",
          max(ext_lo, ext_hi) < float(solver["bz_omega_tol"]),
          max_min_diff=ext_lo, max_max_diff=ext_hi, domain=group,
          n_irreducible=int(mask_irr.sum()))

    ck = np.array(solver["check_k"], float) * np.pi / conf["L"]
    base = core.omega_from_w2(core.band_solve(float(ck[0]), float(ck[1]), conf, solver)["w2"])
    sym_res = {}
    for name, Q in core.group_elements(group).items():
        kq = Q @ ck
        wq = core.omega_from_w2(core.band_solve(float(kq[0]), float(kq[1]), conf, solver)["w2"])
        sym_res[name] = float(np.max(np.abs(wq - base)))
    kq = core.group_elements("C4v")["R90"] @ ck
    r90 = float(np.max(np.abs(core.omega_from_w2(
        core.band_solve(float(kq[0]), float(kq[1]), conf, solver)["w2"]) - base)))
    iso = abs(conf["l1"] - conf["l2"]) <= float(solver["group_tol"]) * max(conf["l1"], conf["l2"])
    check("C7c every element of the ACTUAL point group G is a symmetry of the spectrum",
          max(sym_res.values()) < float(solver["bz_omega_tol"]),
          group=group, max_residual=max(sym_res.values()), per_element=sym_res)
    check("C7d C4v NOT imposed where anisotropy reduces the symmetry (R90 witness)",
          (r90 < float(solver["bz_omega_tol"])) if iso
          else (r90 > float(solver["aniso_witness_tol"])),
          isotropic=bool(iso), R90_witness_residual=r90,
          witness_tol=float(solver["aniso_witness_tol"]))

    wX = core.omega_from_w2(core.band_solve(np.pi / conf["L"], 0.0, conf, solver)["w2"])
    wY = core.omega_from_w2(core.band_solve(0.0, np.pi / conf["L"], conf, solver)["w2"])
    dxy = float(np.max(np.abs(wX - wY)))
    check("C7e X and Y are inequivalent when l1 != l2 (explicit non-C4v witness)",
          (dxy < float(solver["bz_omega_tol"])) if iso
          else (dxy > float(solver["aniso_witness_tol"])),
          max_abs_diff=dxy, omega_X_lowest=float(wX[0]), omega_Y_lowest=float(wY[0]))

    det, det_w = [], []
    for i in (0, len(ks_p) // 2, len(ks_p) - 1):
        r = core.band_solve(float(ks_p[i][0]), float(ks_p[i][1]), conf, solver)
        det.append(float(np.max(np.abs(r["w2"] - w2_p[i]))))
        # reported for information only: omega = sqrt(omega^2) amplifies the absolute
        # eigenvalue noise of the Gamma null modes (w2 ~ 1e-11 -> omega ~ 3e-6), so
        # the determinism gate is applied to omega^2.
        det_w.append(float(np.max(np.abs(core.omega_from_w2(r["w2"]) - w_p[i]))))
    check("C8 repeatability of the spectrum on re-solve (gate on omega^2; sqrt is "
          "ill-conditioned at the Gamma null modes)",
          max(det) < float(solver["det_tol"]), max_abs_diff_w2=max(det),
          max_abs_diff_omega_info_only=max(det_w), tol=float(solver["det_tol"]),
          n_repeats=len(det))

    n_pass = sum(1 for c in checks if c["result"] == "PASS")
    n_fail = len(checks) - n_pass
    print(f"\nP5 run {run_id}: checks PASS {n_pass} FAIL {n_fail}", flush=True)

    # ---------------- raw outputs (immutable) ---------------- #
    outdir = Path(args.outdir) / run_id
    hashes = {}
    hashes["bands_path.npz"] = core.write_immutable(outdir / "bands_path.npz", core.npz_bytes(
        ks=ks_p, legs=legs, omega=w_p, omega2=w2_p, phase_velocity=vp))
    hashes["zone_omega.npz"] = core.write_immutable(outdir / "zone_omega.npz", core.npz_bytes(
        ks=ks_z, grid=np.array([n1, n2]), omega=w_z, omega2=w2_z,
        irreducible_mask=mask_irr, dk=np.array([dk1, dk2])))
    hashes["vg_zone.npz"] = core.write_immutable(outdir / "vg_zone.npz", core.npz_bytes(
        ks=ks_z, vg=vg, note="central differences of omega on the full-BZ grid (M12 (51))"))
    hashes["gaps.json"] = core.write_immutable(outdir / "gaps.json", core.json_bytes(gaps))
    checks_obj = {
        "run_id": run_id, "case": case, "status": status, "params_hash": phash,
        "group": group, "n_pass": n_pass, "n_fail": n_fail, "run_ok": n_fail == 0,
        "checks": checks, "branch_tracking": track,
        "zone_coverage": {"grid": [n1, n2], "group": group,
                          "irreducible_points": int(mask_irr.sum()),
                          "k_evenness_max_abs": d_even,
                          "extrema_match_full_grid": bool(max(ext_lo, ext_hi)
                                                          < float(solver["bz_omega_tol"]))},
        "resolution": {"n_mesh": conf["n_mesh"], "p4b_floor": floor},
        "eigenpair_residuals": {"max_non_degenerate": max_resid,
                                "modes_gated": len(resid_ok),
                                "modes_excluded_degenerate": resid_excluded,
                                "tol": float(solver["residual_tol"])},
        "solver": solver,
    }
    hashes["checks.json"] = core.write_immutable(outdir / "checks.json", core.json_bytes(checks_obj))

    manifest = {
        "run_id": run_id,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "case": case,
        "status": status,
        "status_meaning": ("machinery validation on a declared parameter basis; NOT a paper "
                           "result and NOT a P5 gate" if status != "PRODUCTION"
                           else "production dataset for the locked parameter set"),
        "git": core.git_state(),
        "env": core.env_state(),
        "params_file": str(args.params),
        "params_file_sha256": core._sha256_file(args.params),
        "params_hash": phash,
        "params_snapshot": core.provenance_table(params),
        "study": params.get("study", {}),
        "sampling": sampling,
        "solver": solver,
        "frozen_sources": core.FROZEN_SOURCES,
        "p4b_resolution_floor": floor,
        "outputs": {k: {"sha256": v, "immutable": True} for k, v in hashes.items()},
        "zone_coverage": checks_obj["zone_coverage"],
        "checks": {"n_pass": n_pass, "n_fail": n_fail, "run_ok": n_fail == 0},
        "gates": {"P5": "NOT PASS (see audit/P5_STATUS.md)", "B6": "PARTIAL",
                  "PCR1": "NOT PASS", "G3": "not met"},
        "open_TV_items": ["TV4 path/zone sampling", "TV6 production parameters",
                          "TV7 band count + filter", "TV14 Case-C reference phase",
                          "TV16 S_theta definition", "TV18 inclusion representation"],
    }
    man_bytes = core.json_bytes(manifest)
    hashes["manifest.json"] = core.write_immutable(outdir / "manifest.json", man_bytes)
    # plan/CALC_MASTER_PLAN.md section I names runs/<run_id>/manifest.json: write the
    # same bytes there so the plan path and the self-contained run directory agree.
    core.write_immutable(core.REPO / "runs" / run_id / "manifest.json", man_bytes)
    log_text = "".join(tee.buf)
    hashes["run_log.txt"] = core.write_immutable(outdir / "run_log.txt", log_text.encode())

    print(f"raw outputs: {outdir}")
    for k, v in hashes.items():
        print(f"  {k:16s} sha256={v[:16]}...")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
