"""Model constants, parameter vectors and the B transformation.

Implements:
  eq:theta-def   theta = (alpha, tau_q, kappa2)
  eq:phi-def     phi   = (alpha, tau_q, B)
  eq:Bdef        B = kappa2 / (alpha tau_q)
  eq:kappa-from-B  kappa2 = alpha tau_q B
  eq:param-det   det(dtheta/dphi) = alpha tau_q
  eq:ndparams    hat tau_q, hat kappa2, hat tau_Delta
  eq:Binv        B is invariant under the scaling (thickness cancels)

SOURCE: manuscript/GK_COMPLETE_CALCULATIONS.tex, sections 1, 4, 6.
No quantity in this module is defined anywhere but that document.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Theta:
    """Physical parameter vector, eq:theta-def. SI units.

    alpha  [m^2/s]  thermal diffusivity, eq:rhoc..eq:lambda -> alpha=lambda/(rho c)
    tau_q  [s]      flux relaxation time, eq:tauq
    kappa2 [m^2]    nonlocal coefficient, eq:kappa2
    """
    alpha: float
    tau_q: float
    kappa2: float

    def __post_init__(self):
        for nm in ("alpha", "tau_q", "kappa2"):
            v = getattr(self, nm)
            if not (v > 0):
                raise ValueError(f"{nm} must be positive (assumption A5); got {v}")

    @property
    def B(self) -> float:
        """eq:Bdef."""
        return self.kappa2 / (self.alpha * self.tau_q)

    def as_array(self) -> np.ndarray:
        return np.array([self.alpha, self.tau_q, self.kappa2], float)

    @staticmethod
    def from_B(alpha: float, tau_q: float, B: float) -> "Theta":
        """eq:kappa-from-B: kappa2 = alpha tau_q B."""
        return Theta(alpha, tau_q, alpha * tau_q * B)


def B_of(alpha: float, tau_q: float, kappa2: float) -> float:
    """eq:Bdef. Single authoritative implementation."""
    return kappa2 / (alpha * tau_q)


def kappa2_of(alpha: float, tau_q: float, B: float) -> float:
    """eq:kappa-from-B. Single authoritative implementation."""
    return alpha * tau_q * B


def param_jacobian_det(alpha: float, tau_q: float) -> float:
    """eq:param-det: det(dtheta/dphi) = alpha tau_q."""
    return alpha * tau_q


@dataclass(frozen=True)
class Geometry:
    """Slab geometry and excitation. eq:domain, def:pulse."""
    L: float      # [m] thickness
    t_p: float    # [s] pulse duration


def nondimensional(theta: Theta, geom: Geometry) -> dict:
    """eq:ndparams and der:nd-flux.

    Returns the hatted parameters. NOTE (sec:program): the dimensionless
    diffusivity is IDENTICALLY 1; the physical alpha must never appear in the
    same expression as alpha_hat.
    """
    L2 = geom.L ** 2
    return {
        "tau_q_hat": theta.alpha * theta.tau_q / L2,   # eq:ndparams
        "kappa2_hat": theta.kappa2 / L2,               # eq:ndparams
        "tau_D_hat": theta.alpha * geom.t_p / L2,      # eq:ndparams
        "alpha_hat": 1.0,                              # der:nd-flux
    }


def scale_time(t_phys, theta: Theta, geom: Geometry) -> np.ndarray:
    """eq:scaling: hat t = alpha t / L^2."""
    return theta.alpha * np.asarray(t_phys, float) / geom.L ** 2
