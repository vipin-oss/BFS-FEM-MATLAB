"""Primary forward solver: kernel inversion + exact pulse convolution.

Implements:
  eq:convolution   T(1,t) = int_0^min(t,tauD) k(t-u) q0(u) du
  eq:nd-bc         q0(u) = 1 - cos(2 pi u / tauD)
  eq:talbot-nodes  fixed Talbot, M odd (default 41)
  sec:program      Module 1 specification

The split/second-shift formulation is PROHIBITED here (res:talbot). It exists
only in src/split_solver.py, which is a deliberately-defective reference used
by acceptance test T16.

SOURCE: manuscript/GK_COMPLETE_CALCULATIONS.tex sections 5, 21, 23.
"""
from __future__ import annotations
import warnings
import numpy as np
from .laplace import K_hat, dK_hat_dparams, talbot_nodes
from .model import Theta, Geometry, nondimensional, scale_time

DEFAULT_M = 41      # sec:program
DEFAULT_NQ = 32     # sec:program, Gauss-Legendre nodes


def _check_M(M: int):
    if M % 2 == 0:
        warnings.warn(
            f"M={M} is EVEN. sec:program requires odd M: an even M places a "
            f"quadrature node on the imaginary axis, colliding with the "
            f"removable pulse pole at t*=M*tauD/10 (eq:tstar) in the split "
            f"formulation. Use an odd M.", RuntimeWarning)


class ForwardSolver:
    """Rear-face temperature on a fixed dimensionless time grid.

    Talbot nodes are precomputed per (time, quadrature-node) pair so the whole
    forward model and its Jacobian are array operations.
    """

    def __init__(self, t_hat, tau_D_hat, M=DEFAULT_M, nq=DEFAULT_NQ):
        _check_M(M)
        self.t_hat = np.atleast_1d(np.asarray(t_hat, float))
        self.tau_D = float(tau_D_hat)
        self.M = int(M)
        self.nq = int(nq)

        xg, wg = np.polynomial.legendre.leggauss(nq)
        hi = np.minimum(self.t_hat, self.tau_D)          # eq:convolution limit
        u = 0.5 * hi[:, None] * (xg[None, :] + 1.0)
        self.wq = 0.5 * hi[:, None] * wg[None, :]
        self.q0 = 1.0 - np.cos(2.0 * np.pi * u / self.tau_D)   # eq:nd-bc
        lag = self.t_hat[:, None] - u                    # kernel argument > 0

        k = np.arange(1, self.M)
        th = k * np.pi / self.M
        cot = 1.0 / np.tan(th)
        sig = th + (th * cot - 1.0) * cot
        r = 2.0 * self.M / (5.0 * lag)
        self.s0 = r.astype(complex)
        self.s = r[..., None] * th * (cot + 1j)
        self.w = np.exp(lag[..., None] * self.s) * (1.0 + 1j * sig)
        self.e0 = np.exp(r * lag)
        self.pref = r / self.M

    def _invert(self, fn):
        """Fixed-Talbot inversion of a transform callable, on the (t,u) grid."""
        a0 = fn(self.s0)
        aa = fn(self.s)
        acc = 0.5 * self.e0 * np.real(a0) + np.sum(np.real(self.w * aa), axis=-1)
        return self.pref * acc

    def _convolve(self, arr):
        """eq:convolution quadrature."""
        return np.sum(self.wq * self.q0 * arr, axis=1)

    def T(self, tau_q_hat, kappa2_hat):
        """Rear-face temperature, eq:convolution."""
        k = self._invert(lambda s: K_hat(s, tau_q_hat, kappa2_hat, self.tau_D))
        return self._convolve(k)

    def T_and_grad_hat(self, tau_q_hat, kappa2_hat):
        """T and dT/d(tau_q_hat, kappa2_hat), analytic (eq:dK-dparams)."""
        k = self._invert(lambda s: K_hat(s, tau_q_hat, kappa2_hat, self.tau_D))
        dq = self._invert(
            lambda s: dK_hat_dparams(s, tau_q_hat, kappa2_hat, self.tau_D)[0])
        dk = self._invert(
            lambda s: dK_hat_dparams(s, tau_q_hat, kappa2_hat, self.tau_D)[1])
        return self._convolve(k), self._convolve(dq), self._convolve(dk)


def forward(theta: Theta, t_phys, geom: Geometry, M=DEFAULT_M, nq=DEFAULT_NQ):
    """T(1,t) for physical parameters. sec:program Module 1."""
    nd = nondimensional(theta, geom)
    slv = ForwardSolver(scale_time(t_phys, theta, geom), nd["tau_D_hat"], M, nq)
    return slv.T(nd["tau_q_hat"], nd["kappa2_hat"])


def forward_and_jacobian(theta: Theta, t_phys, geom: Geometry,
                         M=DEFAULT_M, nq=DEFAULT_NQ, h_alpha=1e-6):
    """T and dT/d(alpha, tau_q, kappa2). sec:program Module 2.

    tau_q and kappa2 are ANALYTIC (finite differences prohibited for them).
    alpha rescales the time axis and pulse length rather than entering the
    kernel, so it uses one central difference, as the specification allows.
    """
    nd = nondimensional(theta, geom)
    slv = ForwardSolver(scale_time(t_phys, theta, geom), nd["tau_D_hat"], M, nq)
    T, dq_hat, dk_hat = slv.T_and_grad_hat(nd["tau_q_hat"], nd["kappa2_hat"])
    L2 = geom.L ** 2
    dT_dtau_q = dq_hat * (theta.alpha / L2)   # chain rule through eq:ndparams
    dT_dkappa2 = dk_hat * (1.0 / L2)
    hp = theta.alpha * h_alpha
    Tp = forward(Theta(theta.alpha + hp, theta.tau_q, theta.kappa2),
                 t_phys, geom, M, nq)
    Tm = forward(Theta(theta.alpha - hp, theta.tau_q, theta.kappa2),
                 t_phys, geom, M, nq)
    dT_dalpha = (Tp - Tm) / (2.0 * hp)
    return T, np.column_stack([dT_dalpha, dT_dtau_q, dT_dkappa2])
