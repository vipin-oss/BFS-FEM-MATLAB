"""INDEPENDENT cross-check solver: staggered-grid method of lines.

Implements eq:nd-energy and eq:nd-gk directly in the TIME domain. It shares no
Laplace transform, no Talbot contour and no convolution with src/forward.py,
so agreement between the two is a meaningful cross-check (sec:program Module 3).

Per sec:anchor, agreement between our own two solvers is NUMERICAL
CROSS-CHECKING, not external validation.

PERFORMANCE NOTE (performance-only change, no mathematics altered)
------------------------------------------------------------------
The right-hand side is unchanged. The only addition is `jac_sparsity`, an
OPTIONAL structural hint passed to `solve_ivp`.

Without it, SciPy's BDF assumes the Jacobian is dense and forms all n = 2*Nx-1
columns by finite differences, then LU-factorises an n-by-n dense matrix a few
hundred times per solve. That is O(n^2) memory and O(n^3) work per
factorisation, which is why Nx=3200 needed ~19 GB and did not finish.

The true Jacobian of eq:nd-energy and eq:nd-gk is banded with at most five
structural nonzeros per row: dT_i/dt touches only q_i and q_{i+1}; dq_j/dt
touches only T_{j-1}, T_j and q_{j-1}, q_j, q_{j+1}. Supplying that pattern
lets SciPy group columns and use a sparse LU. The pattern is a mathematical
property of the discretisation, not an approximation: it is derived in
validation/phase5_perf/derive_sparsity.py and verified there against the dense
numerical Jacobian with zero missing and zero spurious entries.

`sparse_jac` defaults to False so that existing call sites keep their exact
previous numerical behaviour. Set sparse_jac=True to enable the hint.
"""
from __future__ import annotations
import numpy as np
from scipy.integrate import solve_ivp


def fd_jac_sparsity(Nx: int):
    """Structural sparsity of d(rhs)/dy for y = [T_0..T_{Nx-1}, q_1..q_{Nx-1}].

    Derived analytically from eq:nd-energy and eq:nd-gk. q_0 (the pulse) and
    q_Nx = 0 are boundary data, not unknowns, so they contribute no columns.
    Returns a scipy.sparse matrix of 0/1 structural entries.
    """
    from scipy.sparse import csr_matrix

    n = 2 * Nx - 1
    rows, cols = [], []

    def qcol(j):
        return Nx + (j - 1) if 1 <= j <= Nx - 1 else None

    for i in range(Nx):                       # eq:nd-energy
        for j in (i, i + 1):
            c = qcol(j)
            if c is not None:
                rows.append(i); cols.append(c)

    for j in range(1, Nx):                    # eq:nd-gk
        r = Nx + (j - 1)
        for c in (j - 1, j):                  # T_{j-1}, T_j
            rows.append(r); cols.append(c)
        for jj in (j - 1, j, j + 1):          # q_{j-1}, q_j, q_{j+1}
            c = qcol(jj)
            if c is not None:
                rows.append(r); cols.append(c)

    return csr_matrix((np.ones(len(rows), dtype=np.int8), (rows, cols)),
                      shape=(n, n))


def solve_fd(t_hat, tau_q_hat, kappa2_hat, tau_D_hat,
             Nx=400, rtol=1e-10, atol=1e-12, sparse_jac=False):
    """Rear-face T on the dimensionless grid. sec:program Module 3 settings.

    sparse_jac: pass the exact banded Jacobian pattern to the BDF integrator.
                Performance only. The equations, boundary conditions,
                discretisation, initial condition and tolerances are identical
                either way.
    """
    t_hat = np.atleast_1d(np.asarray(t_hat, float))
    dx = 1.0 / Nx

    def q_front(t):
        # eq:nd-bc
        if 0.0 < t <= tau_D_hat:
            return 1.0 - np.cos(2.0 * np.pi * t / tau_D_hat)
        return 0.0

    def rhs(t, y):
        T = y[:Nx]
        q = np.empty(Nx + 1)
        q[0] = q_front(t)
        q[Nx] = 0.0                      # eq:bc-rear-dim
        q[1:Nx] = y[Nx:]
        dTdt = -(q[1:] - q[:-1]) / (dx * tau_D_hat)          # eq:nd-energy
        d2q = (q[2:] - 2.0 * q[1:Nx] + q[:Nx - 1]) / dx ** 2
        gradT = (T[1:] - T[:-1]) / dx
        dqdt = (-q[1:Nx] - tau_D_hat * gradT + kappa2_hat * d2q) / tau_q_hat
        return np.concatenate([dTdt, dqdt])               # eq:nd-gk

    kw = {}
    if sparse_jac:
        kw["jac_sparsity"] = fd_jac_sparsity(Nx)

    sol = solve_ivp(rhs, (0.0, float(np.max(t_hat))),
                    np.zeros(2 * Nx - 1),                 # eq:nd-ic
                    t_eval=t_hat, method="BDF", rtol=rtol, atol=atol, **kw)
    return sol.y[Nx - 1, :]

