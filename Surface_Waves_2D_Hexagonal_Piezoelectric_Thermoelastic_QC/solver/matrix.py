"""Plane-wave matrix module (architecture item 3).

Entrywise transcription of the frozen matrix M(k,p,Omega) (frozen
formulation §8, eq. (M)); NO alternative derivation, NO symmetrisation of
the phason block (H_xz != H_zx lives in rows 3/4 via K3 <-> K6 roles).

Harmonic convention exp[i(k x + p z - Omega t)]; decay for Im p > 0.
Fields a = [u_x, u_z, w_x, w_z, theta]^T.

Phi = i*Omega + tau0*Omega**2
M(5,5) = k11*(k^2+p^2) - c_e*Phi  with the nondimensional c_e = 1 EXACTLY
(F1: dimensional c_e = 500 J/(kg K) is absorbed into the row normalisation;
it must never be inserted here).

Pencil: M = A0 + p*A1 + p^2*A2 with A0/A1/A2 built explicitly (V0 asserts
the identity against the entrywise M).
"""
import numpy as np

MODELS = ("A", "B", "C")

def Phi_of(Omega, m):
    return 1j * Omega + m.tau0 * Omega ** 2

def Lambda_of(Omega, model, m):
    """Frozen phason temporal symbol (frozen formulation §6)."""
    if model == "A":
        return -m.rho_w * Omega ** 2
    if model == "B":
        return -1j * Omega * m.Dw
    if model == "C":
        return -m.rho_w * Omega ** 2 - 1j * Omega * m.Dw
    raise ValueError(f"unknown model {model!r}")

def M_matrix(k, p, Omega, model, m):
    Phi = Phi_of(Omega, m)
    Lam = Lambda_of(Omega, model, m)
    M = np.zeros((5, 5), dtype=complex)
    # phonon block
    M[0, 0] = -m.C11 * k * k - m.C66 * p * p + m.rho * Omega ** 2
    M[1, 1] = -m.C66 * k * k - m.C11 * p * p + m.rho * Omega ** 2
    M[0, 1] = M[1, 0] = -(m.C12 + m.C66) * k * p
    # phonon-phason coupling (symmetric block)
    M[0, 2] = M[2, 0] = -m.R1 * k * k - m.R6 * p * p
    M[0, 3] = M[3, 0] = -(m.R2 + m.R6) * k * p
    M[1, 2] = M[2, 1] = -(m.R2 + m.R6) * k * p
    M[1, 3] = M[3, 1] = -m.R6 * k * k - m.R1 * p * p
    # phason block (K1/K3 depth-anisotropy swap; NOT symmetrised: K3 != K6)
    M[2, 2] = -m.K1 * k * k - m.K3 * p * p - Lam
    M[3, 3] = -m.K3 * k * k - m.K1 * p * p - Lam
    M[2, 3] = M[3, 2] = -(m.K2 + m.K6) * k * p
    # thermal couplings (LS non-self-adjoint corner pair)
    M[0, 4] = -1j * m.beta1 * k
    M[1, 4] = -1j * m.beta1 * p
    M[4, 0] = -1j * m.T0b1 * Phi * k
    M[4, 1] = -1j * m.T0b1 * Phi * p
    # thermal row (F1: c_e = 1 nondimensional, exact)
    M[4, 4] = m.k11 * (k * k + p * p) - m.c_e * Phi
    return M

def pencil(k, Omega, model, m):
    """Explicit A0, A1, A2 with M = A0 + p A1 + p^2 A2."""
    Phi = Phi_of(Omega, m)
    Lam = Lambda_of(Omega, model, m)
    A0 = np.zeros((5, 5), dtype=complex)
    A1 = np.zeros((5, 5), dtype=complex)
    A2 = np.zeros((5, 5), dtype=complex)
    # A2 (p^2 coefficients)
    A2[0, 0] = -m.C66; A2[1, 1] = -m.C11
    A2[0, 2] = A2[2, 0] = -m.R6
    A2[1, 3] = A2[3, 1] = -m.R1
    A2[2, 2] = -m.K3;  A2[3, 3] = -m.K1
    A2[4, 4] = m.k11
    # A1 (p coefficients)
    A1[0, 1] = A1[1, 0] = -(m.C12 + m.C66) * k
    A1[0, 3] = A1[3, 0] = -(m.R2 + m.R6) * k
    A1[1, 2] = A1[2, 1] = -(m.R2 + m.R6) * k
    A1[2, 3] = A1[3, 2] = -(m.K2 + m.K6) * k
    A1[1, 4] = -1j * m.beta1
    A1[4, 1] = -1j * m.T0b1 * Phi
    # A0 (p-independent)
    A0[0, 0] = -m.C11 * k * k + m.rho * Omega ** 2
    A0[1, 1] = -m.C66 * k * k + m.rho * Omega ** 2
    A0[0, 2] = A0[2, 0] = -m.R1 * k * k
    A0[1, 3] = A0[3, 1] = -m.R6 * k * k
    A0[2, 2] = -m.K1 * k * k - Lam
    A0[3, 3] = -m.K3 * k * k - Lam
    A0[0, 4] = -1j * m.beta1 * k
    A0[4, 0] = -1j * m.T0b1 * Phi * k
    A0[4, 4] = m.k11 * k * k - m.c_e * Phi
    return A0, A1, A2

def A1_check_entries(m):
    """Frozen-value guard used by tests: A1(3,4) = A1(4,3) = -(K2+K6)k."""
    return -(m.K2 + m.K6)
