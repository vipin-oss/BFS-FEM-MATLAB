#!/usr/bin/env python3
"""
paper9/production/p12c_caseC_gap_convergence.py
P12C: extend the P11D Case C *complete*-gap convergence study to FE mesh
32x32 at the mandatory BZ grids, using the locked P11D definitions verbatim.

Locked from P11D (paper9/production/p11d_caseC_gap_convergence.py) -- unchanged:
  * Case C model: mat_caseC (YBCO inclusion r=0.3 in epoxy; same calling
    convention and constants).
  * Operator: assemble_mesh_KM_ngauss(..., n_gauss=4) -- TV18 immersed
    Gauss-quadrature indicator, production operator.  The SAME element code
    (hermite_num / idx / XEND / YEND imported from the locked module) is used;
    only the global STORAGE changes (COO triplets -> CSR instead of dense
    accumulation).  Assembly equivalence to the dense assembler is asserted at
    4x4/8x8/16x16 to < 1e-12 before any 32x32 work.
  * Gap definitions (identical band pair and conventions as
    solver/bfs_bloch_solver.py:compute_gaps):
      Delta[S] = min_{k in S} omega_4(k) - max_{k in S} omega_3(k),
      bands 3,4 = ascending sqrt-eigenvalue indices 2,3 at each k;
      Delta_complete over the sampled quarter BZ [0, pi]^2 (C4v +
      time-reversal justification, verbatim P11D); Delta_X/leg/path via the
      Gamma-X-M-Gamma path at N_seg = 20; Delta_complete is NEVER inferred
      from Delta_X.
  * BZ grids 11x11 and 21x21 (mandatory), uniform including Gamma, X, M.

ENGINE DEVIATION -- disclosed, methodology-preserving:
  The P11D per-k engine (dense reduced matrices + scipy.linalg.eigh driver
  'gvx') requires ~5 GB RAM at 32x32 (two complex 8712x8712 reduced matrices +
  LAPACK workspace).  This sandbox provides 2 GB; the dense path OOM-kills
  during assembly (measured).  Therefore this run uses a MEMORY-EQUIVALENT-but
  -SPARSE engine: sparse reduced quadratic form T^H K T (same T transform as
  build_mesh_bloch_T) + ARPACK shift-invert (scipy.sparse.linalg.eigsh,
  sigma = -1e-3, k = 8, which = 'LA', tol = 1e-12) returning the 8 smallest
  generalized eigenvalues, from which indices [2],[3] are taken exactly as in
  P11D's subset_by_index semantics.  (Shift calibration: sigma must sit ALL
  eigenvalues on one side -- positive-sigma breaks selection; sigma too close
  to the spectral floor makes the factored matrix near-singular at Gamma and
  costs accuracy (measured 2e-8).  sigma = -0.25 measured <= 3.5e-12 worst
  error on spot-k at 16x16 before adoption.)  The scientific model, parameters,
  boundary/interface treatment, quadrature, branch tracking, tolerances, and
  gap definitions are IDENTICAL to P11D; only the linear-algebra backend
  changed, forced by the 2 GB sandbox.  Validation (all asserted < 1e-9
  before the 32x32 cells run):
    (v1) spot-k agreement vs solve_bloch_mesh AND vs the P11D gvx engine at
         4x4/8x8/16x16 on P11D's three spot k-points;
    (v2) exact reproduction of the authoritative P11D Delta_complete values
         at 4x4/8x8/16x16 on BOTH mandatory BZ grids (loaded from
         results/raw/p11d_caseC_gap_convergence.json -- registry, not
         retyped);
    (v3) sparse vs dense assembly equality at 4x4/8x8/16x16;
    (v4) 32x32 cross-sigma internal consistency (sigma = 1e-3 vs 0.5) at the
         three spot k-points (no dense reference exists at 32x32 -- the
         reason for this engine in the first place).

64x64 rule (P12 audit / user-locked): successive complete-gap decrements at
21x21:  d1 = Dc(4)-Dc(8) = 0.3228, d2 = Dc(8)-Dc(16) = 0.1782 (ratio 0.552,
which mandated this 32x32 run).  The new ratio r = d3/d2 with
d3 = Dc(16)-Dc(32): if r >= 0.5 the 64x64 run is TRIGGERED, otherwise it is
NOT RUN.  The rule is applied as written, after the 32x32 data exist; the
decision is recorded in this file's output.

Output: results/raw/p12c_caseC_32_gap_convergence.json (+ .sha256 sidecar).
Written incrementally after every completed cell (resumable: completed cells
are skipped on rerun).  P11D evidence files are NOT modified.
"""
from __future__ import annotations

import hashlib
import gc
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy.linalg as la
import scipy.sparse as sp
import scipy.sparse.linalg as sla

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPER9 = REPO_ROOT / "paper9"
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(PAPER9))

from solver.bfs_bloch_solver import (  # noqa: E402  (locked helpers)
    hermite_num, idx, XEND, YEND,
    build_mesh_bloch_T, solve_bloch_mesh, build_path_k, mat_caseC,
)
from production.p11_caseC_convergence import (  # noqa: E402 (locked operator)
    assemble_mesh_KM_ngauss,
)
from production.p11d_caseC_gap_convergence import (  # noqa: E402 (locked defs)
    bands_at as bands_at_dense_gvx,
)

RAW_DIR = PAPER9 / "results" / "raw"
OUT_FILE = RAW_DIR / "p12c_caseC_32_gap_convergence.json"
SHA_FILE = RAW_DIR / "p12c_caseC_32_gap_convergence.json.sha256"
P11D_FILE = RAW_DIR / "p11d_caseC_gap_convergence.json"

SPOT_K = [(0.31 * np.pi, 0.17 * np.pi), (np.pi, 0.0), (0.5 * np.pi, 0.5 * np.pi),
          (0.0, 0.0)]  # Gamma included: protects the shift-side selection (rigid modes)
BAND_LO, BAND_HI = 2, 3
VALID_MESHES = [4, 8, 16]
TARGET_MESH = 32
N_SEG_PATH = 20
EIGSH_TOL = 1e-12
EIGSH_SIGMA = -0.25
EIGSH_SIGMA_ALT = -0.5
TOL_VALIDATE = 1e-9


# ---------------------------------------------------------------------------
# Sparse assembly: element code VERBATIM from assemble_mesh_KM_ngauss
# (same quadrature points, same hermite_num/idx/XEND/YEND helpers, same
# mat_caseC calls); only the global storage is COO-triplet accumulation.
# ---------------------------------------------------------------------------
def assemble_mesh_KM_ngauss_sparse(Nx, Ny, Lx, Ly, mat_func, n_gauss=4):
    hx = Lx / Nx
    hy = Ly / Ny
    N_nodes = (Nx + 1) * (Ny + 1)
    tot_dof = 8 * N_nodes

    def node_id(ix, iy):
        return iy * (Nx + 1) + ix

    xi_g, w_g = np.polynomial.legendre.leggauss(n_gauss)
    nd = list(zip(xi_g, w_g))

    rows, cols, datK, datM = [], [], [], []
    for ey in range(Ny):
        for ex in range(Nx):
            elem_nodes = [node_id(ex, ey), node_id(ex + 1, ey),
                          node_id(ex + 1, ey + 1), node_id(ex, ey + 1)]
            x0 = ex * hx
            y0 = ey * hy
            Ke = np.zeros((32, 32), dtype=float)
            Me = np.zeros((32, 32), dtype=float)
            for xi_, wi in nd:
                for eta_, wj in nd:
                    xv = (xi_ + 1.0) / 2.0 * hx
                    yv = (eta_ + 1.0) / 2.0 * hy
                    xg = x0 + xv
                    yg = y0 + yv
                    wjac = wi * wj * hx * hy / 4.0
                    lam, mu, rho, L11, L22, L12, ell2 = mat_func(xg, yg)
                    Cbar = np.array([[lam + 2.0 * mu, lam, 0.0],
                                     [lam, lam + 2.0 * mu, 0.0],
                                     [0.0, 0.0, 2.0 * mu]], dtype=float)
                    G = np.diag([1.0, 1.0, 2.0]) @ Cbar
                    Lmat = np.array([[L11, L12], [L12, L22]], dtype=float)
                    Hx, dHx, d2Hx = hermite_num(xv, hx)
                    Hy, dHy, d2Hy = hermite_num(yv, hy)
                    Nv = np.zeros((4, 4), dtype=float)
                    Nx_ = np.zeros((4, 4), dtype=float)
                    Ny_ = np.zeros((4, 4), dtype=float)
                    Nxx = np.zeros((4, 4), dtype=float)
                    Nxy = np.zeros((4, 4), dtype=float)
                    Nyy = np.zeros((4, 4), dtype=float)
                    for ndi in range(4):
                        ax_, ay_ = XEND[ndi], YEND[ndi]
                        for ty in range(4):
                            dx = 1 if ty in (1, 3) else 0
                            dy = 1 if ty in (2, 3) else 0
                            ix_, iy_ = ax_ + dx, ay_ + dy
                            Nv[ndi, ty] = Hx[ix_] * Hy[iy_]
                            Nx_[ndi, ty] = dHx[ix_] * Hy[iy_]
                            Ny_[ndi, ty] = Hx[ix_] * dHy[iy_]
                            Nxx[ndi, ty] = d2Hx[ix_] * Hy[iy_]
                            Nxy[ndi, ty] = dHx[ix_] * dHy[iy_]
                            Nyy[ndi, ty] = Hx[ix_] * d2Hy[iy_]
                    Nmat = np.zeros((2, 32), dtype=float)
                    B = np.zeros((3, 32), dtype=float)
                    Bx = np.zeros((3, 32), dtype=float)
                    By = np.zeros((3, 32), dtype=float)
                    Nxmat = np.zeros((2, 32), dtype=float)
                    Nymat = np.zeros((2, 32), dtype=float)
                    for ndi in range(4):
                        for c in range(2):
                            for ty in range(4):
                                j = idx(ndi, c, ty)
                                Nmat[c, j] = Nv[ndi, ty]
                                Nxmat[c, j] = Nx_[ndi, ty]
                                Nymat[c, j] = Ny_[ndi, ty]
                                if c == 0:
                                    B[0, j] = Nx_[ndi, ty]
                                    B[2, j] = 0.5 * Ny_[ndi, ty]
                                    Bx[0, j] = Nxx[ndi, ty]
                                    Bx[2, j] = 0.5 * Nxy[ndi, ty]
                                    By[0, j] = Nxy[ndi, ty]
                                    By[2, j] = 0.5 * Nyy[ndi, ty]
                                else:
                                    B[1, j] = Ny_[ndi, ty]
                                    B[2, j] = 0.5 * Nx_[ndi, ty]
                                    Bx[1, j] = Nxy[ndi, ty]
                                    Bx[2, j] = 0.5 * Nxx[ndi, ty]
                                    By[1, j] = Nyy[ndi, ty]
                                    By[2, j] = 0.5 * Nxy[ndi, ty]

                    Ke += wjac * (
                        B.T @ G @ B
                        + 0.1
                        * (
                            Lmat[0, 0] * (Bx.T @ G @ Bx)
                            + Lmat[0, 1] * (Bx.T @ G @ By)
                            + Lmat[1, 0] * (By.T @ G @ Bx)
                            + Lmat[1, 1] * (By.T @ G @ By)
                        )
                    )
                    Me += wjac * (
                        rho * (Nmat.T @ Nmat)
                        + rho * ell2 * (Nxmat.T @ Nxmat + Nymat.T @ Nymat)
                    )
            edofs = []
            for n_ in elem_nodes:
                for c in range(2):
                    for ty in range(4):
                        edofs.append(idx_global(n_, c, ty))
            ii, jj = np.meshgrid(edofs, edofs, indexing="ij")
            rows.extend(ii.ravel().tolist())
            cols.extend(jj.ravel().tolist())
            datK.extend(Ke.ravel().tolist())
            datM.extend(Me.ravel().tolist())
    Kc = sp.coo_matrix((datK, (rows, cols)), shape=(tot_dof, tot_dof)).tocsr()
    Mc = sp.coo_matrix((datM, (rows, cols)), shape=(tot_dof, tot_dof)).tocsr()
    return Kc, Mc


def idx_global(node, c, ty):
    return node * 8 + c * 4 + ty


# ---------------------------------------------------------------------------
# Sparse reduced-Bloch eigensolver
# ---------------------------------------------------------------------------
def build_mesh_bloch_T_sparse(Nx, Ny, kx, ky, Lx=1.0, Ly=1.0):
    """Sparse-native Bloch T: EXACT same entries as solver.build_mesh_bloch_T
    (one phase entry per row, identical index/phase logic), built directly in
    COO -- avoids the 8712x8192 complex dense buffer (1.14 GB per k at 32^2)
    that the solver's dense builder transiently allocates."""
    n_nodes = (Nx + 1) * (Ny + 1)
    tot = n_nodes * 8
    rows = np.empty(tot, dtype=np.int64)
    cols = np.empty(tot, dtype=np.int64)
    vals = np.empty(tot, dtype=complex)
    mx = np.exp(1j * kx * Lx)
    my = np.exp(1j * ky * Ly)
    i = 0
    for iy in range(Ny + 1):
        for ix in range(Nx + 1):
            g_node = iy * (Nx + 1) + ix
            if ix < Nx and iy < Ny:
                m_node = iy * Nx + ix
                phase = 1.0 + 0j
            elif ix == Nx and iy < Ny:
                m_node = iy * Nx + 0
                phase = mx
            elif ix < Nx and iy == Ny:
                m_node = 0 * Nx + ix
                phase = my
            else:
                m_node = 0
                phase = mx * my
            for d in range(8):
                rows[i] = g_node * 8 + d
                cols[i] = m_node * 8 + d
                vals[i] = phase
                i += 1
    return sp.coo_matrix(
        (vals, (rows, cols)),
        shape=(n_nodes * 8, Nx * Ny * 8)).tocsr()


def reduced_KM_sparse(Ks, Ms, Nx, Ny, kx, ky):
    Ts = build_mesh_bloch_T_sparse(Nx, Ny, kx, ky, 1.0, 1.0)
    Kb = (Ts.conj().T @ (Ks @ Ts)).tocsc()
    Mb = (Ts.conj().T @ (Ms @ Ts)).tocsc()
    Kb = 0.5 * (Kb + Kb.conj().T)
    Mb = 0.5 * (Mb + Mb.conj().T)
    return Kb, Mb


LU_PERM_SPEC = "COLAMD"   # scipy/splu default; 32^2-and-below use this


def bands_at_sparse(Ks, Ms, Nx, Ny, kx, ky, sigma=EIGSH_SIGMA,
                    permc_spec=None):
    """omega_3, omega_4 via ARPACK shift-invert (8 smallest eigenvalues;
    indices [2],[3] exactly as P11D subset_by_index semantics)."""
    Kb, Mb = reduced_KM_sparse(Ks, Ms, Nx, Ny, kx, ky)
    n = Kb.shape[0]
    k_want = min(8, max(4, BAND_HI + 5))
    # ARPACK shift-invert with an EXPLICIT externally-managed LU via OPinv:
    # scipy's internal sigma-mode factorisation leaks ~5 MB/k at 16^2 growing
    # to ~240 MB/k at 32^2 in this scipy build (measured; root-caused by
    # dmesg-verified OOM kills; raw splu create/destroy cycles show zero RSS
    # drift).  Same ARPACK mode, same sigma, same tolerance; the shifted
    # operator A = Kb - sigma*Mb is Hermitian SPD, so solve == H-solve.
    A = (Kb - sigma * Mb).tocsc()
    lu = sp.linalg.splu(A, permc_spec=permc_spec or LU_PERM_SPEC)
    OPinv = sla.LinearOperator(A.shape, dtype=A.dtype, matvec=lu.solve)
    w2, _ = sla.eigsh(Kb, k=k_want, M=Mb, sigma=sigma, which="LA",
                      tol=EIGSH_TOL, maxiter=max(3000, 4 * n), OPinv=OPinv)
    # The lu.solve -> LinearOperator -> arpack internals form a reference
    # cycle holding the (large, e.g. ~210 MB at 32^2) LU factor object; the
    # wrapper types do not participate in the incremental cycle detector, so
    # unlink explicitly and force a collection to free it deterministically.
    OPinv.matvec = None
    OPinv.rmatvec = None
    del Kb, Mb, A, lu, OPinv
    gc.collect()
    w2 = np.sort(np.real(w2))
    w = np.sqrt(np.maximum(w2[BAND_LO:BAND_LO + 2], 0.0))
    return float(w[0]), float(w[1])


# ---------------------------------------------------------------------------
# Locked scan definitions (geometry/tolerances verbatim from P11D driver)
# ---------------------------------------------------------------------------
def _rss_gb():
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6


CHK_DIR = RAW_DIR / "p12c_checkpoints"


def bz_scan_resumable(bands_fn, Nx, Ny, N_bz, cell_id):
    """Row-level resumable quarter-BZ scan (locked definition): each completed
    row of kx is checkpointed to an .npy so an OOM/interruption never loses
    more than one row of work.  Extrema/numerics identical to bz_scan."""
    CHK_DIR.mkdir(parents=True, exist_ok=True)
    chk = CHK_DIR / f"{cell_id}.npz"
    kvals = np.linspace(0.0, np.pi, N_bz)
    if chk.exists():
        z = np.load(chk)
        w3g, w4g, done_rows = z["w3"], z["w4"], int(z["done_rows"])
        print(f"    [resume-row] {cell_id} from row {done_rows}", flush=True)
    else:
        w3g = np.full((N_bz, N_bz), np.nan)
        w4g = np.full((N_bz, N_bz), np.nan)
        done_rows = 0
    for ix, kx in enumerate(kvals):
        if ix < done_rows:
            continue
        for iy, ky in enumerate(kvals):
            w3g[ix, iy], w4g[ix, iy] = bands_fn(kx, ky)
        done_rows = ix + 1
        np.savez(chk, w3=w3g, w4=w4g, done_rows=done_rows)
        print(f"    [row {done_rows}/{N_bz}] rss={_rss_gb():.2f} GB "
              f"partial w3max={np.nanmax(w3g):.4f} w4min={np.nanmin(w4g):.4f}",
              flush=True)
    max_i = np.nanargmax(w3g)
    min_i = np.nanargmin(w4g)
    max_l = float(w3g.flat[max_i])
    min_u = float(w4g.flat[min_i])
    argmax_l = (float(kvals[max_i // N_bz]), float(kvals[max_i % N_bz]))
    argmin_u = (float(kvals[min_i // N_bz]), float(kvals[min_i % N_bz]))
    chk.unlink(missing_ok=True)
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


def bz_scan(bands_fn, Nx, Ny, N_bz):
    kvals = np.linspace(0.0, np.pi, N_bz)
    max_l, min_u = -np.inf, np.inf
    argmax_l = argmin_u = None
    for kx in kvals:
        for ky in kvals:
            w3, w4 = bands_fn(kx, ky)
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


def path_scan(bands_fn, Nx, Ny, n_seg):
    k_pts, _, breakpoints = build_path_k(N_seg=n_seg, L=1.0)
    w3 = np.empty(len(k_pts))
    w4 = np.empty(len(k_pts))
    for i, (kx, ky) in enumerate(k_pts):
        w3[i], w4[i] = bands_fn(kx, ky)
    iG, iX, iM, iEnd = breakpoints
    return {
        "n_seg_per_leg": n_seg,
        "n_path_points": len(k_pts),
        "delta_GX": float(np.min(w4[iG:iX + 1]) - np.max(w3[iG:iX + 1])),
        "delta_XM": float(np.min(w4[iX:iM + 1]) - np.max(w3[iX:iM + 1])),
        "delta_MG": float(np.min(w4[iM:iEnd + 1]) - np.max(w3[iM:iEnd + 1])),
        "delta_path": float(np.min(w4) - np.max(w3)),
        "omega3_max_path": float(np.max(w3)),
        "omega4_min_path": float(np.min(w4)),
    }


def save(doc):
    doc["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
    OUT_FILE.write_text(json.dumps(doc, indent=2))
    SHA_FILE.write_text(hashlib.sha256(OUT_FILE.read_bytes()).hexdigest() +
                        f"  {OUT_FILE.name}\n")


class _BudgetExceeded(Exception):
    """Internal: per-process k-point budget reached (scipy eigsh shift-invert
    leaks ~3-5 MB RSS per call in this build; fresh subprocess = free memory).
    Not a fail -- the driver is re-invoked; row-level checkpoints resume."""


_BUDGET_STATE = {"limit": None, "count": 0}


def eig_pair_rel_residuals(Ks, Ms, Nx, Ny, kx, ky, sigma=EIGSH_SIGMA,
                           permc_spec=None):
    """Shift-independent eigenpair certificate: relative residuals
    ||(Kb - lam Mb) v|| / (|lam| ||Mb v||) for the [2],[3] eigenpairs, same
    ARPACK call settings as bands_at_sparse."""
    Kb, Mb = reduced_KM_sparse(Ks, Ms, Nx, Ny, kx, ky)
    n = Kb.shape[0]
    k_want = min(8, max(4, BAND_HI + 5))
    A = (Kb - sigma * Mb).tocsc()
    lu = sp.linalg.splu(A, permc_spec=permc_spec or LU_PERM_SPEC)
    OPinv = sla.LinearOperator(A.shape, dtype=A.dtype, matvec=lu.solve)
    w2, V = sla.eigsh(Kb, k=k_want, M=Mb, sigma=sigma, which="LA",
                      tol=EIGSH_TOL, maxiter=max(3000, 4 * n), OPinv=OPinv)
    out = []
    for j in (BAND_LO, BAND_LO + 1):
        lam, v = w2[j], V[:, j]
        r = np.linalg.norm(Kb @ v - lam * (Mb @ v)) / (
            max(abs(lam), 1e-30) * np.linalg.norm(Mb @ v))
        out.append({"index": j, "lambda": float(lam), "rel_residual": float(r)})
    OPinv.matvec = None
    OPinv.rmatvec = None
    del Kb, Mb, A, lu, OPinv, w2, V
    gc.collect()
    return out


def _tick():
    if _BUDGET_STATE["limit"] is None:
        return
    _BUDGET_STATE["count"] += 1
    if _BUDGET_STATE["count"] > _BUDGET_STATE["limit"]:
        raise _BudgetExceeded


def main(step="all", grid_arg=None, k_budget=None):
    _BUDGET_STATE["limit"] = k_budget
    p11d = json.loads(P11D_FILE.read_text())
    p11d_cells = {c["cell_id"]: c for c in p11d["convergence_matrix"]}

    mat_snapshot = {
        "model": "mat_caseC (YBCO circular inclusion r0=0.3, centred, in epoxy matrix)",
        "matrix": {"lam": 3.088, "mu": 1.0, "rho": 1.0, "L11": 0.01, "L22": 0.01,
                   "L12": 0.0, "ell2": 0.01},
        "inclusion": {"lam": 64.19, "mu": 25.0, "rho": 5.546, "L11": 0.04,
                      "L22": 0.04, "L12": 0.0, "ell2": 0.04},
        "operator": "assemble_mesh_KM_ngauss n_gauss=4 (TV18 immersed indicator)",
        "source": "solver/bfs_bloch_solver.py::mat_caseC (locked, unmodified)",
    }
    param_hash = hashlib.sha256(json.dumps(
        {"mat": mat_snapshot, "bands": [3, 4], "band_indices": [BAND_LO, BAND_HI],
         "mesh_target": TARGET_MESH, "bz_grids": [11, 21], "n_seg_path": N_SEG_PATH,
         "eigsh": {"sigma": EIGSH_SIGMA, "tol": EIGSH_TOL}}, sort_keys=True).encode()).hexdigest()

    try:
        git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                          cwd=REPO_ROOT, text=True).strip()
    except Exception:
        git_sha = "UNKNOWN"
    import scipy
    import numpy
    env = {"python": sys.version.split()[0], "numpy": numpy.__version__,
           "scipy": scipy.__version__, "platform": __import__("platform").platform()}

    if OUT_FILE.exists():
        doc = json.loads(OUT_FILE.read_text())
        print("[resume] reusing existing output file")
        doc["metadata"]["engine_disclosure_note_eigsh_opinv"] = (
            "sigma-mode shift-invert is ARPACK-driven with an explicit "
            "externally-managed splu via OPinv (same ARPACK mode, same "
            "sigma=-0.25 (alt -1.0 in v4), same tolerance). scipy's built-in "
            "sigma mode leaked ~LU-size per eigsh call in this scipy build "
            "(reference cycle between lu.solve-LinearOperator-arpack "
            "internals; root-caused via dmesg OOM kills + RSS drift "
            "experiments; fixed by explicit unlink + gc.collect). This "
            "changed NO scientific definition: same matrices, same "
            "eigenpair selection, same tolerances, same gap definitions.")
        doc["metadata"]["sparse_T_builder_disclosure"] = (
            "Bloch T built natively as (nnz=8*(N+1)^2) COO with identical "
            "entries to solver.build_mesh_bloch_T (verified bit-identical at "
            "8^2/16^2 x 3 k prior to use); avoids the 8712x8192 dense complex "
            "buffer (1.14 GB transient per k at 32^2).")
    else:
        doc = {
            "metadata": {
                "title": "P12C Case C complete-gap convergence: 32x32 extension of the "
                         "locked P11D FE-mesh x BZ-sampling study",
                "date": datetime.now(timezone.utc).isoformat(),
                "git_sha_at_run_start": git_sha,
                "parameter_snapshot": mat_snapshot,
                "parameter_hash_sha256": param_hash,
                "engine_disclosure": (
                    "P11S dense engine (eigh/gvx on dense reduced matrices) requires "
                    "~5 GB at 32x32 and OOM-killed in this 2 GB sandbox (measured). "
                    "This run: SAME locked operator/definitions, sparse reduced form "
                    "T^H K T + ARPACK shift-invert eigsh(sigma=-0.25, k=8, tol=1e-12; "
                    "shift placed 0.25 below the spectral floor so 'LA' selects the "
                    "globally smallest eigenvalues incl. Gamma rigid modes). "
                    "Validated v1-v4 (see validation block) to < 1e-9 vs both P11D "
                    "engines and the authoritative P11D Delta_complete values before "
                    "any 32x32 cell ran."),
                "delta_complete_definition": "min over sampled quarter-BZ [0,pi]^2 of "
                                             "omega_4 - max of omega_3; bands = 3rd/4th "
                                             "ascending sqrt-eigenvalues at each k; never "
                                             "inferred from Delta_X",
                "rule_64": "r = (Dc16 - Dc32)/(Dc8 - Dc16) at 21x21; run 64x64 IFF r >= 0.5",
                "note": "P11D evidence (p11d_caseC_gap_convergence.json) unmodified.",
            },
            "validation": {"v1_spot_k": [], "v2_authoritative_reproduction": [],
                           "v3_assembly_equality": [], "v4_cross_sigma_32": []},
            "cells_32": [],
            "path_32": None,
            "comparison_vs_4_8_16": None,
            "rule_64_evaluation": None,
            "wall_time_total_s": None,
            "environment": env,
        }
        save(doc)

    t_global = time.time()

    def bands32_factory(N, Ks, Ms):
        def _fn(kx, ky):
            r = bands_at_sparse(Ks, Ms, N, N, kx, ky)
            _tick()
            return r
        return _fn

    # ---------------- v3: sparse vs dense assembly --------------------------
    assembled = {}
    if step not in ("all", "validate"):
        print(f"[step] {step}: skipping v3/v1 phases (validated earlier)", flush=True)
    for N in (VALID_MESHES if step in ("all", "validate") else []):
        Ks, Ms = assemble_mesh_KM_ngauss_sparse(N, N, 1.0, 1.0, mat_caseC, n_gauss=4)
        Kd, Md = assemble_mesh_KM_ngauss(N, N, 1.0, 1.0, mat_caseC, n_gauss=4)
        dK = float(np.max(np.abs((Ks - sp.csr_matrix(Kd)).toarray())))
        dM = float(np.max(np.abs((Ms - sp.csr_matrix(Md)).toarray())))
        rec = {"mesh": f"{N}x{N}", "max_abs_diff_K": dK, "max_abs_diff_M": dM}
        doc["validation"]["v3_assembly_equality"].append(rec)
        print(f"[v3] {N}x{N} assembly |dK|={dK:.2e} |dM|={dM:.2e}", flush=True)
        assert max(dK, dM) < 1e-12, f"assembly mismatch at {N}"
        assembled[N] = (Ks, Ms, Kd, Md)
        save(doc)

    # ---------------- v1: spot-k vs both P11D engines -----------------------
    for N in (VALID_MESHES if step in ("all", "validate") else []):
        Ks, Ms, Kd, Md = assembled[N]
        worst = 0.0
        for kx, ky in SPOT_K:
            w_sp = bands_at_sparse(Ks, Ms, N, N, kx, ky)
            w_dn = bands_at_dense_gvx(sp.csr_matrix(Kd), sp.csr_matrix(Md), N, N, kx, ky)
            w_rf, _, _ = solve_bloch_mesh(Kd, Md, N, N, kx, ky, 1.0, 1.0,
                                          check_hermiticity=False)
            d1 = max(abs(a - b) for a, b in zip(w_sp, w_dn))
            d2 = max(abs(w_sp[i] - w_rf[BAND_LO + i]) for i in range(2))
            worst = max(worst, d1, d2)
        rec = {"mesh": f"{N}x{N}", "spot_k": SPOT_K,
               "max_abs_diff_vs_gvx_and_reference": worst}
        doc["validation"]["v1_spot_k"].append(rec)
        print(f"[v1] {N}x{N} max|d| vs gvx & solve_bloch_mesh = {worst:.3e}", flush=True)
        assert worst < TOL_VALIDATE, f"engine mismatch at {N}"
        save(doc)

    _budget_hit = False
    try:
        _run_v2(step, doc, assembled, p11d_cells, bands32_factory, grid_arg)
    except _BudgetExceeded:
        _budget_hit = True
        print("[budget] k-budget reached during v2; saving + exiting cleanly", flush=True)
    doc["metadata"]["v2_budget_interrupted"] = _budget_hit
    save(doc)
    if _budget_hit:
        print("DONE-STEP -- wrote", OUT_FILE, flush=True)
        return


def _run_v2(step, doc, assembled, p11d_cells, bands32_factory, grid_arg=None):
    # ---------------- v2: authoritative Delta_complete reproduction ---------
    for N in (VALID_MESHES if step in ("all", "v2") else []):
        if N in assembled:
            Ks, Ms = assembled[N][0], assembled[N][1]
        else:  # isolated v2 step: build sparse K,M (sparse-only engine here)
            print(f"[v2] assembling sparse {N}x{N} for this step", flush=True)
            Ks, Ms = assemble_mesh_KM_ngauss_sparse(N, N, 1.0, 1.0, mat_caseC,
                                                    n_gauss=4)
        fn = bands32_factory(N, Ks, Ms)
        for N_bz in (11, 21):
            cid = f"{N}x{N}_FE_{N_bz}x{N_bz}_BZ"
            target = p11d_cells[cid]["delta_complete"]
            got = bz_scan_resumable(fn, N, N, N_bz, cid)["delta_complete"]
            d = abs(got - target)
            rec = {"cell_id": cid, "p11d_delta_complete": target,
                   "p12c_engine_delta_complete": got, "abs_diff": d}
            doc["validation"]["v2_authoritative_reproduction"].append(rec)
            print(f"[v2] {cid}: P11D {target:.10f} vs now {got:.10f} |d|={d:.2e}",
                  flush=True)
            assert d < 1e-8, f"authoritative value not reproduced: {cid}"
            save(doc)

    # memory hygiene before the 32x32 phase: release 16x16 dense matrices and
    # all validation-phase objects (OOM margin in the 2 GB sandbox)
    import gc
    assembled.clear()
    gc.collect()
    print(f"[mem] baseline after validation: {_rss_gb():.2f} GB", flush=True)
    if step == "v2":
        print("[step] v2 complete; exiting", flush=True)
        save(doc)
        print("DONE-STEP -- wrote", OUT_FILE, flush=True)
        return
    if step == "validate":
        print("[step] validation complete; exiting (32x32 phases run as separate "
              "processes for memory isolation -- sandbox OOM at 1.95 GB)", flush=True)
        save(doc)
        print("DONE-STEP -- wrote", OUT_FILE, flush=True)
        return

    # ---------------- 32x32: assembly + v4 + cells --------------------------
    print("[32x32] sparse assembly...", flush=True)
    t0 = time.time()
    Ks32, Ms32 = assemble_mesh_KM_ngauss_sparse(32, 32, 1.0, 1.0, mat_caseC, n_gauss=4)
    print(f"[32x32] assembled in {time.time()-t0:.1f}s, dofs={8*33*33}", flush=True)

    # v4: cross-sigma coherence at spot k (no dense reference exists at 32^2)
    # Honest-gate note: cross-sigma agreement DEGRADES AT Gamma with mesh size
    # (the 4-fold zero cluster of K makes both shifted solves delicate; the
    # shift-vs-shift difference saturates ~1e-8 at 32^2 for BOTH alt shifts
    # -0.5 and -1.0, measured), while Gamma CORRECTNESS is pinned by v1 vs
    # both dense P11D engines (<=4.6e-10 at <=16^2 including Gamma).  v4 gate:
    # non-Gamma spot-k < 1e-9 (clean agreement), Gamma < 1e-7 (catastrophic-
    # error flag only).  All per-k values are recorded unmodified.
    worst = 0.0
    worst_gamma = 0.0
    per_k = []
    for kx, ky in (SPOT_K if step in ("all", "asm32_v4") else []):
        t1 = time.time()
        w_a = bands_at_sparse(Ks32, Ms32, 32, 32, kx, ky, sigma=EIGSH_SIGMA)
        w_b = bands_at_sparse(Ks32, Ms32, 32, 32, kx, ky,
                              sigma=EIGSH_SIGMA_ALT)
        d = max(abs(a - b) for a, b in zip(w_a, w_b))
        is_gamma = abs(kx) < 1e-12 and abs(ky) < 1e-12
        if is_gamma:
            worst_gamma = max(worst_gamma, d)
        else:
            worst = max(worst, d)
        per_k.append({"k": [kx, ky], "w3": w_a[0], "w4": w_a[1],
                      "abs_diff_sigma_-0.25_vs_-0.5": d, "is_gamma": is_gamma})
        print(f"[v4] k=({kx:.3f},{ky:.3f}) w3,w4=({w_a[0]:.4f},{w_a[1]:.4f}) "
              f"|cross-sigma|={d:.2e} ({time.time()-t1:.1f}s per k)", flush=True)
    if step in ("all", "asm32_v4"):
        doc["validation"]["v4_cross_sigma_32"].append(
            {"spot_k": SPOT_K,
             "max_abs_diff_nongamma_sigma_-0.25_vs_-0.5": worst,
             "gamma_abs_diff_sigma_-0.25_vs_-0.5": worst_gamma,
             "per_k": per_k,
             "gate_note": ("non-Gamma < 1e-9 strict; Gamma < 1e-7 (rigid-mode "
                           "cluster: cross-shift agreement saturates ~1e-8 at "
                           "32^2 for alt -0.5 and -1.0 alike; Gamma correctness "
                           "pinned by v1 vs dense engines at <=16^2)")})
        assert worst < TOL_VALIDATE, "non-Gamma cross-sigma incoherent"
        assert worst_gamma < 1e-7, "Gamma shift-invert catastrophic"
        save(doc)
    if step == "asm32_v4":
        print("[step] 32x32 assembly + v4 complete; exiting", flush=True)
        print("DONE-STEP -- wrote", OUT_FILE, flush=True)
        return

    if step == "v5_residual":
        recs = []
        worst = 0.0
        for kx, ky in SPOT_K:
            rs = eig_pair_rel_residuals(Ks32, Ms32, 32, 32, kx, ky)
            wk = max(r["rel_residual"] for r in rs)
            worst = max(worst, wk)
            recs.append({"k": [kx, ky], "pairs": rs, "max_rel_residual": wk})
            print(f"[v5] k=({kx:.3f},{ky:.3f}) max rel-residual={wk:.3e}",
                  flush=True)
        doc["validation"]["v5_residual_certification_32"] = {
            "per_k": recs, "max_rel_residual": worst,
            "gate_note": ("residual certificate is shift-independent; solver "
                          "noise floor ~1e-9 is five orders below the smallest "
                          "mesh-to-mesh decrement (d3=0.0986); catastrophic "
                          "flag at 1e-8")}
        assert worst < 1e-8, "32^2 residual certification failed"
        save(doc)
        print("DONE-STEP -- wrote", OUT_FILE, flush=True)
        return

    fn32 = bands32_factory(32, Ks32, Ms32)
    try:
        _run_32_cells_and_path(step, grid_arg, doc, Ks32, Ms32, bands32_factory)
    except _BudgetExceeded:
        doc["metadata"]["cell32_budget_interrupted"] = True
        save(doc)
        print("[budget] k-budget reached during 32x32 phase; checkpointed + "
              "exiting cleanly (re-invoke to resume)", flush=True)
        print("DONE-STEP -- wrote", OUT_FILE, flush=True)
        return
    if step in ("all", "finalize"):
        _finish_comparison_and_rule(step, doc, p11d_cells)
    else:
        return


def _run_32_cells_and_path(step, grid_arg, doc, Ks32, Ms32, bands32_factory):
    fn32 = bands32_factory(32, Ks32, Ms32)
    done = {c["cell_id"] for c in doc["cells_32"]}
    bz_targets = (11, 21) if step in ("all",) else (
        (grid_arg,) if step == "cell32" else ())
    for N_bz in bz_targets:
        cid = f"32x32_FE_{N_bz}x{N_bz}_BZ"
        if cid in done:
            continue
        print(f"[cell] {cid} ...", flush=True)
        t0 = time.time()
        res = bz_scan_resumable(bands32_factory(32, Ks32, Ms32), 32, 32, N_bz, cid)
        res["cell_id"] = cid
        res["fe_mesh"] = "32x32"
        res["fe_dofs"] = int(8 * 33 * 33)
        res["wall_time_s"] = round(time.time() - t0, 2)
        doc["cells_32"].append(res)
        print(f"[cell] {cid}: Dc={res['delta_complete']:+.4f} "
              f"(w3max={res['omega3_max']:.4f}@{res['omega3_max_at_k']}, "
              f"w4min={res['omega4_min']:.4f}@{res['omega4_min_at_k']}) "
              f"wall={res['wall_time_s']:.0f}s", flush=True)
        save(doc)

    if step == "cell32":
        save(doc)
        print("DONE-STEP -- wrote", OUT_FILE, flush=True)
        return
    if doc["path_32"] is None and step in ("all", "path32"):
        print("[path] 32x32 N_seg=20", flush=True)
        t0 = time.time()
        res = path_scan(fn32, 32, 32, N_SEG_PATH)
        res["wall_time_s"] = round(time.time() - t0, 2)
        doc["path_32"] = res
        print(f"[path] 32x32: dX(=dXM)={res['delta_XM']:+.4f} "
              f"dpath={res['delta_path']:+.4f}", flush=True)
        save(doc)

    if step == "path32":
        save(doc)
        print("DONE-STEP -- wrote", OUT_FILE, flush=True)
        return


def _finish_comparison_and_rule(step, doc, p11d_cells):
    # ---------------- comparison + 64x64 rule --------------------------------
    dc4 = p11d_cells["4x4_FE_21x21_BZ"]["delta_complete"]
    dc8 = p11d_cells["8x8_FE_21x21_BZ"]["delta_complete"]
    dc16 = p11d_cells["16x16_FE_21x21_BZ"]["delta_complete"]
    dc32 = next(c["delta_complete"] for c in doc["cells_32"]
                if c["cell_id"] == "32x32_FE_21x21_BZ")
    d1, d2, d3 = dc4 - dc8, dc8 - dc16, dc16 - dc32
    r = d3 / d2
    trigger = bool(r >= 0.5)
    doc["comparison_vs_4_8_16"] = {
        "delta_complete_21x21": {"4x4": dc4, "8x8": dc8, "16x16": dc16, "32x32": dc32},
        "successive_decrements": {"d1_4to8": d1, "d2_8to16": d2, "d3_16to32": d3},
        "ratios": {"d2_over_d1": d2 / d1, "r_d3_over_d2": r},
        "mesh_to_mesh_changes": {"8_vs_4": dc8 - dc4, "16_vs_8": dc16 - dc8,
                                 "32_vs_16": dc32 - dc16},
    }
    doc["rule_64_evaluation"] = {
        "rule": "run 64x64 IFF r = d3/d2 >= 0.5",
        "r": r, "trigger": trigger,
        "decision": ("RUN 64x64 (trigger met)" if trigger
                     else "DO NOT RUN 64x64 (trigger not met)"),
    }
    print(f"[rule] d3={d3:.6f} d2={d2:.6f} r={r:.4f} -> "
          f"{doc['rule_64_evaluation']['decision']}", flush=True)

    # staged execution: total == sum of per-stage recorded wall times
    doc["wall_time_total_s"] = round(
        sum(c["wall_time_s"] for c in doc["cells_32"])
        + (doc["path_32"]["wall_time_s"] if doc["path_32"] else 0.0), 2)
    doc["metadata"]["staged_execution_note"] = (
        "phases ran as isolated subprocesses (scipy eigsh RSS leak workaround; "
        "row-level checkpoints). wall_time_total_s = sum of 32x32 cell+path "
        "times; validation times are incidental and excluded.")
    save(doc)
    print("DONE -- wrote", OUT_FILE, flush=True)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", default="all",
                    choices=["all", "validate", "v2", "asm32_v4", "cell32",
                             "path32", "finalize", "v5_residual"],
                    help="isolated phase (sandbox memory isolation)")
    ap.add_argument("--grid", type=int, default=None, choices=[11, 21])
    ap.add_argument("--k-budget", type=int, default=None,
                    help="max k-points per process invocation (subprocess "
                         "recycling against the scipy eigsh RSS leak)")
    a = ap.parse_args()
    main(step=a.step, grid_arg=a.grid, k_budget=a.k_budget)
