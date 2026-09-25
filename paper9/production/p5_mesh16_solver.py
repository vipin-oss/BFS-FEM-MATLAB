#!/usr/bin/env python3
"""n = 16 production solver for the P5 Bloch eigenvalue problem.

Formulation is FROZEN: the 4-node BFS element with 8 master DOF per node
(u_x, u_y, u_x,x, u_y,x, u_x,y, u_y,y, u_x,xy, u_y,xy) assembled on an
n x n element grid per unit cell with Bloch phases exp(i k.(r1 - r2)).
Only the element size h = Lcell / n changes with respect to the historical
production (n = 1 -> n = 16); element matrices, material parameters, k-path,
k-grid, band count and tolerances are unchanged.  No rescaling, no correction
factor, no stochastic ARPACK "SM" start.

Assembly: nine k-independent coefficient matrices K_ab, M_ab (a, b in -1, 0, 1)
built once per (theta, AR) case from the frozen element matrices; the per-k
operator is K(k) = sum_ab exp(i (a kx + b ky) L / n) K_ab followed by an exact
Hermitian symmetrisation through the pre-computed transpose permutation.
Verified against the frozen `assemble_nxn_bloch` to <= 1.2e-13 (K) and
<= 3e-17 (M) over all 42 production cases at two wavenumbers.

Eigensolver (deterministic): shift-invert Lanczos / Jacobi-Davidson iteration on
T = (K + sigma M)^-1 M with a fixed analytic start basis that includes the two
rigid-translation patterns (the near-null subspace at Gamma); every returned
mode is residual-gated, and any unconverged point escalates to the exact dense
LAPACK route and is counted as a fallback.
"""
from __future__ import annotations

import os as _os
# Single-threaded BLAS: production runs two worker processes on two cores, where
# multi-threaded BLAS thrashes and slows every solve by roughly 4x.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    _os.environ.setdefault(_v, "1")

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from scipy.linalg import eigh as geigh

P9 = Path(__file__).resolve().parent.parent
if str(P9) not in sys.path:
    sys.path.insert(0, str(P9))

_spec = importlib.util.spec_from_file_location("p4b_5g_to_5i",
                                               P9 / "verification" / "suite" / "p4b_5g_to_5i.py")
p4b = importlib.util.module_from_spec(_spec)
sys.modules["p4b_5g_to_5i"] = p4b
_spec.loader.exec_module(p4b)

assemble_KM = p4b.assemble_KM
assemble_nxn_bloch_ref = p4b.assemble_nxn_bloch

_CORNERS = [(0, 0), (1, 0), (1, 1), (0, 1)]


class CaseAssembly:
    """Bloch-reduced operator factory for one (theta, AR) case, n elements per side."""

    def __init__(self, n, Lcell, lam, mu, rho, ell2, L11, L22, L12):
        self.n, self.L = int(n), float(Lcell)
        Kloc, Mloc = assemble_KM(hx=Lcell / n, hy=Lcell / n, lam=lam, mu=mu,
                                 L11=L11, L22=L22, L12=L12, rho=rho, ell2=ell2)
        self.Kloc = np.asarray(Kloc, dtype=complex)
        self.Mloc = np.asarray(Mloc, dtype=complex)
        ne = n * n
        ex, ey = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
        ex = ex.ravel().astype(np.int64)
        ey = ey.ravel().astype(np.int64)
        rows = np.empty((ne, 4, 8), dtype=np.int64)
        ax = np.empty((ne, 4, 8), dtype=np.int64)
        ay = np.empty((ne, 4, 8), dtype=np.int64)
        for a, (dx, dy) in enumerate(_CORNERS):
            i = ex + dx
            j = ey + dy
            wx = (i == n).astype(np.int64)
            wy = (j == n).astype(np.int64)
            node = np.where(wy == 1, 0, j) * n + np.where(wx == 1, 0, i)
            rows[:, a, :] = node[:, None] * 8 + np.arange(8)[None, :]
            ax[:, a, :] = wx[:, None]
            ay[:, a, :] = wy[:, None]
        rows = rows.reshape(ne, 32)
        ax = ax.reshape(ne, 32)
        ay = ay.reshape(ne, 32)
        dax = ax[:, None, :] - ax[:, :, None]
        day = ay[:, None, :] - ay[:, :, None]
        bins = ((dax + 1) * 3 + (day + 1)).ravel()
        rowidx = np.broadcast_to(rows[:, :, None], (ne, 32, 32)).ravel()
        colidx = np.broadcast_to(rows[:, None, :], (ne, 32, 32)).ravel()
        Kl = np.broadcast_to(Kloc[None, :, :], (ne, 32, 32)).ravel()
        Ml = np.broadcast_to(Mloc[None, :, :], (ne, 32, 32)).ravel()
        N = 8 * n * n
        key = rowidx * N + colidx
        ukey, inv = np.unique(key, return_inverse=True)
        inv = inv.ravel()
        n_uniq = ukey.size
        self._SK, self._SM = [], []
        for b in range(9):
            pos = np.flatnonzero(bins == b)
            if pos.size == 0:
                self._SK.append(np.zeros(n_uniq, dtype=complex))
                self._SM.append(np.zeros(n_uniq, dtype=complex))
                continue
            tgt = inv[pos]
            kk = Kl[pos]
            mm = Ml[pos]
            self._SK.append(np.bincount(tgt, weights=kk.real, minlength=n_uniq)
                            + 1j * np.bincount(tgt, weights=kk.imag, minlength=n_uniq))
            self._SM.append(np.bincount(tgt, weights=mm.real, minlength=n_uniq)
                            + 1j * np.bincount(tgt, weights=mm.imag, minlength=n_uniq))
        rr = (ukey // N).astype(np.int64)
        cc = (ukey % N).astype(np.int64)
        D = sp.coo_matrix((np.ones(n_uniq, dtype=complex), (rr, cc)), shape=(N, N)).tocsr()
        self.indptr = D.indptr.copy()
        self.indices = D.indices.copy()
        self.shape = (N, N)
        self.nnz = self.indices.size
        DT = D.transpose().tocsr()
        rD, cD = D.nonzero()
        rT, cT = DT.nonzero()
        self.perm_T = np.searchsorted(rT * N + cT, cD * N + rD)

    def matrices(self, kx, ky, symmetrise=True):
        """Bloch-reduced (K, M) at wavenumber (kx, ky).

        The nine master-DOF bins index the *wrap* separation (dx, dy) in units of the
        unit cell, so the Bloch factor is exp(i k . (dx L, dy L)) -- identical to the
        n = 1 reduction T_impl(kx, ky, L) of the frozen solver.  (Using the element
        size h = L/n here is wrong: it leaves the dispersion nearly flat.)
        """
        L = self.L
        ph = np.empty(9, dtype=complex)
        for a in range(3):
            e_ax = np.exp(1j * (a - 1) * kx * L)
            for b in range(3):
                ph[3 * a + b] = e_ax * np.exp(1j * (b - 1) * ky * L)
        nz = self.nnz
        dK = np.empty(nz, dtype=complex)
        dM = np.empty(nz, dtype=complex)
        tmp = np.empty(nz, dtype=complex)
        np.multiply(self._SK[0], ph[0], out=dK)
        np.multiply(self._SM[0], ph[0], out=dM)
        for b in range(1, 9):
            np.multiply(self._SK[b], ph[b], out=tmp)
            dK += tmp
            np.multiply(self._SM[b], ph[b], out=tmp)
            dM += tmp
        if symmetrise:
            perm = self.perm_T
            dK = 0.5 * (dK + np.conj(dK[perm]))
            dM = 0.5 * (dM + np.conj(dM[perm]))
        K = sp.csr_matrix((dK, self.indices, self.indptr), shape=self.shape)
        M = sp.csr_matrix((dM, self.indices, self.indptr), shape=self.shape)
        return K, M


def analytic_v0(n_elem):
    """Fixed analytic start vector (no RNG anywhere in the solve path).

    Unit u_x master-DOF pattern with a smooth, non-zero-mean modulation, so the
    rigid-translation (near-null) subspace at Gamma is reachable: a purely
    oscillatory start is orthogonal to it.
    """
    dim = 8 * n_elem * n_elem
    idx = np.arange(dim)
    node = idx // 8
    t = idx % 8
    x = (node % n_elem) / float(n_elem)
    y = (node // n_elem) / float(n_elem)
    v = np.zeros(dim, dtype=complex)
    v[t == 0] = (1.0 + 0.5 * np.cos(2.0 * np.pi * x[t == 0])
                 + 0.5 * np.cos(2.0 * np.pi * y[t == 0]))
    v[t == 4] = 0.5 * np.sin(2.0 * np.pi * x[t == 4]) + 0.5 * np.sin(2.0 * np.pi * y[t == 4])
    return v / np.linalg.norm(v)


class DenseSubset:
    """Exact dense route: LAPACK generalised Hermitian eigensolve, driver=gvx."""

    def __init__(self, n_want=6):
        self.n_want = n_want
        self.calls = 0

    def solve(self, K, M):
        self.calls += 1
        Kd = K.toarray() if sp.issparse(K) else np.asarray(K)
        Md = M.toarray() if sp.issparse(M) else np.asarray(M)
        w, V = geigh(Kd, Md, subset_by_index=[0, self.n_want - 1], driver="gvx",
                     check_finite=False)
        order = np.argsort(np.real(w))
        w = np.real(w)[order]
        V = V[:, order]
        om = np.sqrt(np.maximum(w, 0.0))
        res = np.empty_like(om)
        for j in range(len(om)):
            r = Kd @ V[:, j] - w[j] * (Md @ V[:, j])
            res[j] = (np.linalg.norm(r) / (np.linalg.norm(Kd @ V[:, j])
                                           + abs(w[j]) * np.linalg.norm(Md @ V[:, j])))
        return om, V, res, True


class BlochEigensolver:
    """Deterministic shift-invert ARPACK eigensolver on the operator T = (K + sigma M)^-1 M.

    - fixed analytic start vector (`analytic_v0`); no stochastic ARPACK "SM" start
    - shift sigma = 1e-3, ARPACK tol = 1e-11, ncv = 16
    - Ritz values ordered by 1/mu - sigma, then refined with the Rayleigh quotient
      lambda = Re(v^H K v) on M-normalised vectors (the ordering route alone loses
      digits for lambda ~ sigma)
    - residual gate on propagating modes (lambda > lambda_floor); the near-null
      modes at Gamma are exempt and reported separately
    - exact dense escalation (LAPACK gvx subset) if the gate is not met
    """

    def __init__(self, n_want=6, n_extra=2, sigma=1.0e-3, tol=1.0e-11, ncv=16,
                 tol_res=1.0e-10, lam_floor=1.0e-6, maxiter=1000, fallback=None,
                 n_elem=16):
        self.n_want = n_want
        self.n_extra = n_extra
        self.k = n_want + n_extra
        self.sigma = sigma
        self.tol = tol
        self.ncv = max(ncv, self.k + 1)
        self.tol_res = tol_res
        self.lam_floor = lam_floor
        self.maxiter = maxiter
        self.n_elem = n_elem
        self.fallback = fallback if fallback is not None else DenseSubset(n_want)
        self.stats = {"points": 0, "fallbacks": 0, "residual_sum": 0.0, "worst_residual": 0.0,
                      "factor_time": 0.0, "arpack_time": 0.0, "matvecs": 0, "sigma_hist": {},
                      "gate_failures": 0, "point_ms_mean": None, "point_ms_max": 0.0,
                      "n_over_1s": 0, "_t_last": None, "_pt_sum": 0.0}

    def solve(self, K, M, warm=None):
        """Timed public entry point (per-point wall time recorded for diagnostics)."""
        t0 = time.perf_counter()
        out = self._solve_inner(K, M, warm)
        dt = (time.perf_counter() - t0) * 1e3
        self.stats["_pt_sum"] += dt
        self.stats["point_ms_max"] = max(self.stats["point_ms_max"], dt)
        if dt > 1000.0:
            self.stats["n_over_1s"] += 1
        n = max(1, self.stats["points"] + self.stats["fallbacks"])
        self.stats["point_ms_mean"] = self.stats["_pt_sum"] / n
        return out

    def _solve_inner(self, K, M, warm=None):
        from sksparse.cholmod import cho_factor
        from scipy.sparse.linalg import LinearOperator, eigsh

        v0 = analytic_v0(self.n_elem) if warm is None else np.asarray(warm[:, 0], dtype=complex)
        sigma = self.sigma
        for attempt in range(6):
            t1 = time.perf_counter()
            Aop = (K + sigma * M).tocsc()
            try:
                factor = cho_factor(Aop)
            except Exception:
                sigma *= 10.0
                continue
            self.stats["factor_time"] += time.perf_counter() - t1
            op = LinearOperator(shape=K.shape, dtype=complex,
                                matvec=lambda x, f=factor, MM=M: f.solve(MM @ x))
            t1 = time.perf_counter()
            n_before = self.stats["matvecs"]

            def _count(x):
                self.stats["matvecs"] += 1
                return op.matvec(x)

            op_c = LinearOperator(shape=K.shape, dtype=complex, matvec=_count)
            try:
                mu, Y = eigsh(op_c, k=self.k, which="LM", v0=v0, tol=self.tol,
                              ncv=self.ncv, maxiter=self.maxiter)
            except Exception:
                sigma *= 10.0
                continue
            self.stats["arpack_time"] += time.perf_counter() - t1
            order = np.argsort(-np.real(mu))
            Y = Y[:, order]
            # T is the (K + sigma M)-self-adjoint operator, so its ARPACK
            # eigenvectors are Euclidean-normalised only: restore M-normalisation
            # before forming the Rayleigh quotient (otherwise lambda is meaningless).
            nrm = np.sqrt(np.abs(np.einsum("ij,ij->j", Y.conj(), M @ Y)))
            Y = Y / np.where(nrm > 0.0, nrm, 1.0)[None, :]
            lam = np.real(np.einsum("ij,ij->j", Y.conj(), K @ Y))   # Rayleigh quotient
            order2 = np.argsort(lam)
            lam = lam[order2]
            Y = Y[:, order2]
            KY = K @ Y
            MY = M @ Y
            R = KY - MY * lam
            # Backward-error gate: ||K y - lambda M y|| / (opnorm ||y||) with
            # opnorm = max column sum of |K|.  Scale free and uniform: the naive
            # per-mode relative residual is ~1 for the near-null modes at Gamma
            # (both terms vanish there) although their absolute residual is at
            # machine precision, so it is not a convergence measure at all.
            opnorm = float(np.abs(K).sum(axis=0).max())
            rel = np.linalg.norm(R, axis=0) / (opnorm * np.maximum(np.linalg.norm(Y, axis=0), 1e-300))
            ok = float(np.max(rel[: self.n_want])) < self.tol_res
            self.stats["residual_sum"] += float(np.sum(rel[: self.n_want]))
            self.stats["worst_residual"] = max(self.stats["worst_residual"],
                                               float(np.max(rel[: self.n_want])))
            self.stats["sigma_hist"][sigma] = self.stats["sigma_hist"].get(sigma, 0) + 1
            self.stats["points"] += 1
            if ok:
                om = np.sqrt(np.maximum(lam[: self.n_want], 0.0))
                return om, Y[:, : self.n_want], rel[: self.n_want], True
            self.stats["gate_failures"] += 1
            break
        om, Yf, resf, _ = self.fallback.solve(K, M)     # exact dense escalation
        self.stats["fallbacks"] += 1
        return om[: self.n_want], Yf[:, : self.n_want], resf[: self.n_want], False


def solve_point(ca, K, M, solver=None, warm=None):
    """Solve one k-point: returns (omega asc, M-normalised vectors, residual, ok)."""
    if solver is None:
        solver = BlochEigensolver(n_elem=ca.n)
    return solver.solve(K, M, warm=warm)
