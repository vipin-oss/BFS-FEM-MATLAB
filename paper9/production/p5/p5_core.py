#!/usr/bin/env python3
"""P5 production core (Paper 9).

Provides, for every P5 production run:
  * parameter / provenance loading  (plan CALC_MASTER_PLAN.md §J; the solver reads
    parameters ONLY from a params YAML file),
  * adapters to the FROZEN implementation (P4A element assembly + P4B Bloch
    reduction, imported read-only from verification/suite/),
  * the locked sampling conventions (M10.1 path, M10-a §6 irreducible-zone grid),
  * the locked gap definitions (M12.3: directional / path / complete),
  * branch tracking (M15 §4.6 MAC), spurious/invalid-mode accounting (TV7 rules),
  * run manifests with git commit, parameter hash, environment, output hashes,
  * integrity checks (hermiticity, BZ periodicity, resolution floor, validity,
    zone coverage, gap-definition consistency).

NOTHING in this module changes the formulation frozen through P4B. No scientific
parameter is hard-coded: every numeric setting is read from the params file.
Every numeric literal appearing in this module is declared in
NUMERIC_LITERAL_ALLOWLIST with a justification; production/p5/lint_p5_params.py
enforces that and additionally forbids literals equal to scientific values.
"""
from __future__ import annotations

import gc
import hashlib
import importlib.util
import io
import json
import os
import platform
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(f"PyYAML required: {exc}")

try:
    from scipy.linalg import eigh as dense_eigh
    from scipy.optimize import linear_sum_assignment
    from scipy.sparse.linalg import LinearOperator, eigsh, splu
except ImportError as exc:  # pragma: no cover
    raise SystemExit(f"scipy required: {exc}")

# --------------------------------------------------------------------------- #
# repository layout + frozen sources (read-only imports)
# --------------------------------------------------------------------------- #
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]                       # paper9/
SUITE = REPO / "verification" / "suite"
P4A_PATH = SUITE / "p4a_5a_to_5f.py"
P4B_PATH = SUITE / "p4b_5g_to_5i.py"
P4B_JSON = SUITE / "p4b_5g_to_5i.json"

# structural constants ONLY (no scientific value). Anything else must come from
# the params file. Justification strings are part of the audit trail.
NUMERIC_LITERAL_ALLOWLIST = {
    0: "index / additive identity",
    1: "container/matrix dimension stride",
    -1: "sequence reversal (slice step) and the inversion element sign",
    2: "2 components of k, and 2-D grid construction",
    3: "three legs of the Gamma-X-M-Gamma path",
    8: "8 DOF per BFS node (M13); run-id hash prefix length",
    90.0: "degrees per right angle (angle convention only)",
    45.0: "half a right angle (angle convention only)",
    0.0: "additive identity in comparisons",
    1.0: "unit value used in linear algebra guards (no physical value)",
    -1.0: "negative identity (inversion element)",
}

# scientific values that must NEVER appear as literals in production solver code
FORBIDDEN_LITERAL_NAMES = (
    "L", "lam", "mu", "rho", "ell2", "l1", "l2", "theta_deg", "AR",
    "n_mesh", "n_bands", "path_N_seg", "zone_N1", "zone_N2",
)


def _sha256_file(path: Path) -> str:
    with open(path, "rb") as fh:
        return hashlib.file_digest(fh, "sha256").hexdigest()


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


p4a = _load_module("p4a_frozen", P4A_PATH)
p4b = _load_module("p4b_frozen", P4B_PATH)

assemble_nxn_bloch = p4b.assemble_nxn_bloch      # M14/M15 assembly, validated in P4B 5i
L_plane = p4b.L_plane                            # M02 rotation of the length tensor

RUNID_HASH_CHARS = 8

MODE_READ_ONLY = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH

FROZEN_SOURCES = {
    "p4a_5a_to_5f.py": _sha256_file(P4A_PATH),
    "p4b_5g_to_5i.py": _sha256_file(P4B_PATH),
}


def p4b_resolution_floor() -> dict:
    """Locked resolution floor eps_Delta, read from the P4B artifact (TV13)."""
    with open(P4B_JSON) as fh:
        d = json.load(fh)
    return {
        "eps_Delta": d["5i"]["eps_Delta"],
        "meshes_validated": d["5i"]["meshes"],
        "n_mesh_validated": max(d["5i"]["meshes"]),
        "observable": d["5i"]["observable"],
        "source": str(P4B_JSON.relative_to(REPO)),
        "source_sha256": _sha256_file(P4B_JSON),
    }


# --------------------------------------------------------------------------- #
# parameters / provenance
# --------------------------------------------------------------------------- #
def load_params(path: Path) -> dict:
    with open(path) as fh:
        raw = yaml.safe_load(fh)
    for key in ("parameters", "sampling", "solver"):
        if key not in raw:
            raise SystemExit(f"{path}: params file must define {key}/")
    names = [p["name"] for p in raw["parameters"]]
    if len(names) != len(set(names)):
        raise SystemExit(f"{path}: duplicate parameter names")
    for p in raw["parameters"]:
        if "tag" not in p or "source" not in p:
            raise SystemExit(f"{path}: parameter {p['name']} lacks provenance tag/source")
    return raw


def resolved_values(params: dict) -> dict:
    """Flat {name: value} of the scientific parameters (what the solver consumes)."""
    return {p["name"]: p["value"] for p in params["parameters"]}


def params_hash(params: dict) -> str:
    """Deterministic hash of resolved parameter values + units + study + sampling."""
    payload = {
        "parameters": resolved_values(params),
        "units": {p["name"]: p.get("unit") for p in params["parameters"]},
        "study": params.get("study", {}),
        "sampling": params["sampling"],
    }
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def provenance_table(params: dict) -> list:
    return [
        {
            "name": p["name"],
            "value": p["value"],
            "unit": p.get("unit"),
            "tag": p.get("tag"),
            "source": p.get("source"),
            "locked_in_phase": p.get("locked_in_phase"),
            "verified_by": p.get("verified_by"),
        }
        for p in params["parameters"]
    ]


def solver_conf(params: dict) -> dict:
    return dict(params["solver"])


def solve_conf(params: dict) -> dict:
    """Everything the band solver needs, resolved from the params file."""
    vals = resolved_values(params)
    samp = params["sampling"]
    study = params.get("study", {})
    return {
        "n_mesh": int(samp["n_mesh"]),
        "n_bands": int(samp["n_bands"]),
        "L": vals["L"],
        "lam": vals["lam"],
        "mu": vals["mu"],
        "rho": vals["rho"],
        "ell2": vals["ell2"],
        "l1": vals["l1"],
        "l2": vals["l2"],
        "theta_rad": float(np.deg2rad(study["theta_deg"])),
        "theta_deg": float(study["theta_deg"]),
        "AR": float(study["AR"]),
    }


# --------------------------------------------------------------------------- #
# sampling conventions (locked)
# --------------------------------------------------------------------------- #
def path_points(L: float, n_seg: int) -> tuple:
    """M10.1 triple leg Gamma-X-M-Gamma: k = A + (B-A) j/N_seg, j = 0..N_seg.

    Returns (ks[N,2], leg[N]) with leg index 0 (G-X), 1 (X-M), 2 (M-G).
    Shared endpoints are emitted once, so N = 3*n_seg + 1 nodes (M10.1); the
    closing point is Gamma. A shared endpoint keeps the label of the leg that
    first emitted it (X -> leg 0, M -> leg 1).
    """
    corners = np.array(
        [[0.0, 0.0], [np.pi / L, 0.0], [np.pi / L, np.pi / L], [0.0, 0.0]]
    )
    ks, legs = [], []
    for leg in range(3):
        A, B = corners[leg], corners[leg + 1]
        for j in range(n_seg + 1):
            if leg > 0 and j == 0:
                continue                     # endpoint already emitted (M10.1)
            t = j / n_seg
            ks.append(A + (B - A) * t)
            legs.append(leg)
    return np.array(ks), np.array(legs)


def zone_grid(L: float, n1: int, n2: int) -> tuple:
    """M10-a §6 zone sampling: uniform grid over the full BZ [-pi/L, pi/L]^2.

    A uniform full-BZ grid is a valid superset for every symmetry case, so the
    same data serves complete gaps, IFCs and central-difference gradients; the
    irreducible domain of the ACTUAL group (M10.3) is a subset of the grid.
    The grid is symmetric about k=0 in both axes, so k-evenness holds pointwise
    between the irreducible subset and the full grid (checked in the run).
    """
    k1 = np.linspace(-np.pi / L, np.pi / L, n1)
    k2 = np.linspace(-np.pi / L, np.pi / L, n2)
    K1, K2 = np.meshgrid(k1, k2, indexing="ij")
    return np.stack([K1.ravel(), K2.ravel()], axis=1), (n1, n2)


def irreducible_subset(ks: np.ndarray, group: str) -> np.ndarray:
    """Boolean mask selecting the irreducible domain of the actual point group G.

    M10.3:  C4v (AR=1) -> triangle G-X-M ;  C2v (theta=0,90) -> quarter square ;
    C2v' (theta=45) -> wedge |k2| <= k1 <= pi/L ;  C2 (generic) -> half BZ k1 >= 0.
    """
    k1, k2 = ks[:, 0], ks[:, 1]
    if group == "C4v":
        return (k2 >= 0.0) & (k2 <= k1)
    if group == "C2v":
        return (k1 >= 0.0) & (k2 >= 0.0)
    if group == "C2v'":
        return (k2 <= k1) & (k2 >= -k1)
    if group == "C2":
        return k1 >= 0.0
    raise ValueError(f"unknown group {group}")


def point_group(theta_deg: float, l1: float, l2: float, tol: float) -> str:
    """M10.3 table: point group of the locked operator for the given (theta, AR)."""
    if abs(l1 - l2) <= tol * max(abs(l1), abs(l2)):
        return "C4v"
    rem = theta_deg % 90.0
    if min(rem, 90.0 - rem) <= tol * 90.0:
        return "C2v"
    if abs(rem - 45.0) <= tol * 90.0:
        return "C2v'"
    return "C2"


def group_elements(group: str) -> dict:
    """Explicit 2x2 elements of G (M10.3)."""
    I = np.array([[1.0, 0.0], [0.0, 1.0]])
    R90 = np.array([[0.0, -1.0], [1.0, 0.0]])
    R180 = -I
    sx = np.array([[1.0, 0.0], [0.0, -1.0]])
    sy = np.array([[-1.0, 0.0], [0.0, 1.0]])
    sd = np.array([[0.0, 1.0], [1.0, 0.0]])
    sdp = np.array([[0.0, -1.0], [-1.0, 0.0]])
    table = {
        "C4v": {"I": I, "R90": R90, "R180": R180, "R270": -R90, "sx": sx, "sy": sy, "sd": sd, "sd'": sdp},
        "C2v": {"I": I, "-I": R180, "sx": sx, "sy": sy},
        "C2v'": {"I": I, "-I": R180, "sd": sd, "sd'": sdp},
        "C2": {"I": I, "-I": R180},
    }
    return table[group]


# --------------------------------------------------------------------------- #
# band solver (frozen assembly; params-only settings)
# --------------------------------------------------------------------------- #
def reduced_matrices(kx: float, ky: float, conf: dict):
    L11, L22, L12 = L_plane(conf["l1"], conf["l2"], conf["theta_rad"])
    return assemble_nxn_bloch(
        conf["n_mesh"], kx, ky, conf["L"], conf["lam"], conf["mu"], conf["rho"],
        conf["ell2"], L11, L22, L12,
    )


def hermiticity_residual(K, M) -> dict:
    """Locked M15-a pair: K^H = K, M^H = M (never the false K(k) = K(-k)^H)."""
    def rel(A):
        d = A - A.conj().T
        n = np.linalg.norm(A.data)
        if n == 0:
            return 0.0
        return float(np.linalg.norm(d.data) / n)

    return {"K_rel": rel(K), "M_rel": rel(M)}


def band_solve(kx: float, ky: float, conf: dict, solver: dict, with_vectors: bool = False):
    """Lowest `n_bands` eigenvalues of the reduced Hermitian pencil.

    `n_bands_buffer` extra Ritz pairs are requested as well. They are NOT reported
    as physics, but they are returned so that branch tracking can match a reported
    band whose continuation partner lies just outside the reported window (a
    boundary Ritz pair can otherwise look like a mode-shape jump; diagnosed in
    P5 pre-flight). This is a solver setting, not a change of the observable.

    Diagnostics returned for the audit trail:
      * per-mode scale-normalised residuals
        res_i = ||K v_i - lambda_i M v_i|| / (||K||_F ||v_i||_2)   (reported modes)
      * the degeneracy mask of the requested spectrum (see degenerate_mask): inside
        a degenerate cluster an individual eigenvector is a mixture of the cluster
        and neither its MAC nor its per-mode residual is meaningful.

    Dense path for small problems, shift-invert ARPACK otherwise; the two paths are
    cross-checked by production/p5/test_p5_integrity.py.

    The sparse (ARPACK) path is started from a FIXED deterministic vector (seed
    `arpack_v0_seed`), so repeated solves of the same k are bitwise reproducible
    (without it, ARPACK's random start perturbs the individual members of a
    symmetry-degenerate cluster at the level of its convergence tolerance, which
    broke the C8 determinism gate in the P5 pre-flight; the cluster members
    themselves are basis-arbitrary, the cluster position is not).
    """
    K, M = reduced_matrices(kx, ky, conf)
    nd = K.shape[0]
    n_rep = int(conf["n_bands"])
    k_req = min(n_rep + int(solver.get("n_bands_buffer", 0)), nd - 1)
    if nd <= int(solver["dense_max_dof"]):
        w2_all_sorted, V_all = dense_eigh(K.toarray(), M.toarray())
        order = np.argsort(np.real(w2_all_sorted))[:k_req]
        w2_all = np.real(w2_all_sorted)[order]
        V_all = V_all[:, order] if with_vectors else None
    else:
        sigma = float(solver["sigma_shift"])
        OP = splu((K - sigma * M).tocsc())
        OPinv = LinearOperator(matvec=OP.solve, shape=K.shape, dtype=K.dtype)
        v0 = np.random.default_rng(int(solver.get("arpack_v0_seed", 0))).standard_normal(nd)
        vals, vecs = eigsh(
            K, k=k_req, M=M, sigma=sigma, which="LM", OPinv=OPinv, v0=v0,
            tol=float(solver["tol"]), maxiter=int(solver["maxiter"]),
        )
        del v0
        order = np.argsort(np.real(vals))
        w2_all = np.real(vals)[order]
        V_all = vecs[:, order] if with_vectors else None
        del OP, OPinv, vals, vecs
    kfro = float(np.linalg.norm(K.data))
    resid = resid_all = None
    if V_all is not None:
        norms = np.sqrt(np.sum(np.abs(V_all) ** 2, axis=0))
        resid_all = []
        for i in range(V_all.shape[1]):
            v = V_all[:, i]
            r = K @ v - w2_all[i] * (M @ v)
            den = kfro * norms[i]
            resid_all.append(float(np.linalg.norm(r) / den) if den > 0 else 0.0)
        resid = resid_all[:n_rep]
        del v
    deg_all = degenerate_mask(w2_all, solver) if V_all is not None else None
    del K, M
    gc.collect()
    return {"w2": w2_all[:n_rep], "w2_all": w2_all, "V": V_all, "ndof": nd,
            "residuals": resid, "residuals_all": resid_all, "degenerate_mask": deg_all,
            "n_requested": k_req, "n_reported": n_rep}


def mode_filter(w2: np.ndarray, solver: dict) -> dict:
    """Documented spurious-mode / invalid-root accounting (TV7).

    No root is discarded silently:
      * non-finite eigenvalues -> counted, flagged, run FAILS;
      * omega^2 < neg_tol      -> counted as unphysical, flagged, run FAILS;
      * |omega^2| <= null_tol  -> internal null modes (rigid translations at
        Gamma, M15-a / P4A 5f), reported, NOT dropped.
    No smoothing, interpolation or manual reordering of data anywhere.
    """
    w2 = np.asarray(w2, float)
    return {
        "nonfinite": int(np.sum(~np.isfinite(w2))),
        "negative": int(np.sum(w2 < float(solver["neg_tol"]))),
        "null_modes": int(np.sum(np.abs(w2) <= float(solver["null_tol"]))),
    }


def omega_from_w2(w2: np.ndarray) -> np.ndarray:
    """omega = sqrt(max(omega^2,0)). Negative roots are accounted for by mode_filter."""
    return np.sqrt(np.maximum(np.asarray(w2, float), 0.0))


def mac(v1: np.ndarray, v2: np.ndarray, M) -> float:
    """Mass-weighted modal assurance criterion (M15 §4.6 continuation criterion)."""
    Mv2 = M @ v2
    num = np.abs(np.vdot(v1, Mv2)) ** 2
    den = np.vdot(v1, M @ v1).real * np.vdot(v2, Mv2).real
    return float(num / den) if den > 0 else 0.0


def degenerate_mask(w2: np.ndarray, solver: dict) -> np.ndarray:
    """Modes inside a symmetry-degenerate cluster (relative gap <= deg_tol).

    Inside such a cluster the eigenvector basis is arbitrary, so a per-mode MAC or
    per-mode residual measures the arbitrary mixture, not a change of the mode.
    Clusters are reported, never silently averaged or re-based.
    """
    lam = np.asarray(w2, float)
    nb = len(lam)
    tol = float(solver["deg_tol"]) * max(float(np.max(np.abs(lam))), 1.0)
    deg = np.zeros(nb, bool)
    for i in range(nb):
        gaps = []
        if i > 0:
            gaps.append(lam[i] - lam[i - 1])
        if i < nb - 1:
            gaps.append(lam[i + 1] - lam[i])
        deg[i] = min(gaps) <= tol if gaps else True
    return deg


def mac_step(prev_V, V, M, prev_w2, w2, solver, n_reported, n_guard=2) -> dict:
    """One continuation step: optimal MAC assignment over the tracking window.

    Metric: `MAC(v_i(k), v_j(k'))` in the mass metric (M15 (69)-(71)).
    Window: the *requested* set = reported bands + tracking buffer, so a reported
    band whose continuation partner has shuffled a few sorted-band indices can
    still be matched; a partner in the last `n_guard` columns is flagged as a
    possible window truncation (widen `n_bands_buffer` rather than accept the MAC).
    Evaluability: a reported mode is evaluable only if it is non-degenerate at
    BOTH endpoints (see degenerate_mask); otherwise its MAC is the arbitrary
    mixture of the cluster basis. Non-evaluable modes are counted, not dropped.
    Ordering: the band index is the sorted-eigenvalue label (M12.2); index swaps
    caused by crossings are reported with their k-position and are not failures.
    """
    nb = V.shape[1]
    n_rep = int(n_reported)
    deg_p = degenerate_mask(prev_w2, solver)
    deg_n = degenerate_mask(w2, solver)
    na = prev_V.shape[1]
    C = np.array([[mac(prev_V[:, a], V[:, b], M) for b in range(nb)] for a in range(na)])
    n = max(na, nb)
    pad = np.zeros((n, n))
    pad[:C.shape[0], :C.shape[1]] = C          # zero cost for non-existent pairs
    rows, cols = linear_sum_assignment(-pad)
    assign = {int(r): int(c) for r, c in zip(rows, cols) if r < na and c < nb}
    rep = list(range(n_rep))
    per_mode = {int(i): {"partner": (int(assign[i]) if i in assign else None),
                         "mac": (float(C[i, assign[i]]) if i in assign else 0.0),
                         "evaluable": bool(i in assign and not deg_p[i]
                                           and not deg_n[assign[i]])}
                for i in rep}
    vals = [per_mode[i]["mac"] for i in rep if per_mode[i]["evaluable"]]
    swaps = [i for i in rep if assign[i] != i]
    return {
        "min_mac_matched": float(min(vals)) if vals else None,
        "n_evaluable_modes": len(vals),
        "n_degenerate_prev": int(deg_p.sum()),
        "n_degenerate_next": int(deg_n.sum()),
        "swaps": swaps,
        "swap_pairs": [[i, assign[i]] for i in swaps],
        "matched_into_buffer": [i for i in swaps if assign[i] >= n_rep],
        "reordered_reported": [i for i in swaps if assign[i] < n_rep],
        "mac_matrix_min": float(C.min()),
        "max_abs_index_drift": int(max((abs(assign[i] - i) for i in rep if i in assign),
                                       default=0)),
        "n_partners_in_guard": int(sum(1 for i in rep if i in assign and assign[i] >= nb - n_guard)),
        "n_requested": int(nb), "n_guard": int(n_guard),
        "per_mode": per_mode,
    }


def track_branches(prev_Vs: list, Vs: list, Ms: list, prev_w2s: list, w2s: list,
                   solver: dict, n_reported: int) -> dict:
    """MAC continuation along a sampled path (list form; used by the tests).

    Memory-lean callers (the production runner) call mac_step step by step instead
    of holding every M; both use the identical rule.
    """
    steps = [mac_step(prev_Vs[i], Vs[i], Ms[i], prev_w2s[i], w2s[i], solver,
                      n_reported, int(solver.get("track_guard", 2)))
             for i in range(len(Vs))]
    vals = [s["min_mac_matched"] for s in steps if s["min_mac_matched"] is not None]
    worst = min(vals, default=1.0)
    return {
        "n_steps": len(steps), "min_mac": worst,
        "min_mac_step": next((i + 1 for i, s in enumerate(steps)
                              if s["min_mac_matched"] == worst), None),
        "n_evaluable_steps": len(vals),
        "n_steps_without_evaluable_mode": sum(1 for s in steps
                                              if s["min_mac_matched"] is None),
        "reordering_steps": [i + 1 for i, s in enumerate(steps) if s["reordered_reported"]],
        "matched_into_buffer_steps": [i + 1 for i, s in enumerate(steps)
                                      if s["matched_into_buffer"]],
        "max_abs_index_drift": max((s["max_abs_index_drift"] for s in steps), default=0),
        "steps_with_guard_risk": [i + 1 for i, s in enumerate(steps)
                                  if s["n_partners_in_guard"] > 0],
        "mac_min_tol": float(solver["mac_min"]),
        "steps": steps,
    }


# --------------------------------------------------------------------------- #
# gap machinery — M12.3 definitions, verbatim
# --------------------------------------------------------------------------- #
def delta_gap(w: np.ndarray, mask: np.ndarray, n: int) -> float:
    """Delta_g[S] = min_S omega_{n+1} - max_S omega_n   (1-based band index n)."""
    return float(np.min(w[mask, n]) - np.max(w[mask, n - 1]))


def gap_table(w_path: np.ndarray, legs: np.ndarray, w_zone: np.ndarray,
              zone_mask: np.ndarray, case: str, slack_tol: float) -> dict:
    """Directional (per leg), path and complete gaps for every adjacent band pair.

    Complete gap = extremum over the irreducible zone of the ACTUAL group
    (M10-a ruling (a)), sampled by the full-BZ grid reduced to that domain. A
    complete gap is only ever *claimed* for a cell with periodic contrast
    (Case C, §3.5); Case H is reported as "dispersion only".
    """
    n_bands = w_path.shape[1]
    leg_names = ["Gamma-X", "X-M", "M-Gamma"]
    out = {"case": case,
           "definition": "Delta_g[S] = min_S w_{n+1} - max_S w_n (M12.3)",
           "pairs": []}
    for n in range(1, n_bands):
        direction = {name: delta_gap(w_path, legs == i, n) for i, name in enumerate(leg_names)}
        d_path = delta_gap(w_path, np.ones(len(w_path), bool), n)
        d_complete = delta_gap(w_zone, zone_mask, n)
        d_zonefull = delta_gap(w_zone, np.ones(len(w_zone), bool), n)
        out["pairs"].append({
            "n": n,
            "directional": direction,
            "path_Gamma-X-M-Gamma": d_path,
            "complete_irreducible_zone": d_complete,
            "zone_full_grid_reference": d_zonefull,
            "ordering_slack_path_minus_complete": float(d_path - d_complete),
            "ordering_ok_within_slack": bool(d_path - d_complete >= -slack_tol),
            "complete_gap_claimed": bool(d_complete > 0.0 and case == "C"),
        })
    return out


# --------------------------------------------------------------------------- #
# run manifest / immutability
# --------------------------------------------------------------------------- #
def git_state() -> dict:
    def run(*args):
        try:
            return subprocess.run(
                ["git", "-C", str(REPO), *args], capture_output=True, text=True, check=False
            ).stdout.strip()
        except Exception:  # pragma: no cover
            return ""
    return {"commit": run("rev-parse", "HEAD"),
            "branch": run("rev-parse", "--abbrev-ref", "HEAD"),
            "dirty": bool(run("status", "--porcelain"))}


def env_state() -> dict:
    import scipy
    return {
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "platform": platform.platform(),
        "cpu_count": os.cpu_count(),
    }


def write_immutable(path: Path, data: bytes) -> str:
    """Write once, then remove write permission; returns sha256 of the bytes."""
    if path.exists():
        raise SystemExit(f"refusing to overwrite raw output: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    os.chmod(path, MODE_READ_ONLY)
    return hashlib.sha256(data).hexdigest()


def npz_bytes(**arrays) -> bytes:
    buf = io.BytesIO()
    np.savez(buf, **arrays)
    return buf.getvalue()


def json_bytes(obj) -> bytes:
    def default(o):
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(type(o))
    return json.dumps(obj, indent=2, default=default).encode()


def make_run_id(case: str, mode: str, phash: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"P5-{stamp}-{case}-{mode}-{phash[:RUNID_HASH_CHARS]}"
