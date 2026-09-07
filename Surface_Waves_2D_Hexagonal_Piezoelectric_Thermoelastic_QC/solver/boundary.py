"""Surface boundary-matrix constructor (architecture item 6).

Rows (frozen formulation §10; half-space z > 0, outward normal n = -e_z,
prescribed-load convention t_z = -sigma_zz = P0):

  1  sigma_zz = 0   (free; the eigenproblem uses P0 = 0)
  2  sigma_xz = 0
  3  phason:  free -> H_xz = 0 ;  clamped -> w_x = 0
  4  phason:  free -> H_zz = 0 ;  clamped -> w_z = 0
  5  thermal: isothermal -> theta = 0 ; insulated -> d(theta)/dz = 0

Entries are the Fourier images (factor i = derivative) of the frozen
constitutive rows; the phason rows keep the K3/K6 asymmetry (H_xz uses
K3 on w_x,z and K6 on w_z,x; H_zz uses K2 on w_x,x and K1 on w_z,z).
"""
import numpy as np

def B_matrix(k, p_ad, V, m, bc):
    """bc = {'phason': 'free'|'clamped', 'thermal': 'isothermal'|'insulated'}."""
    ph = bc.get("phason", "free")
    th = bc.get("thermal", "isothermal")
    n = len(p_ad)
    B = np.zeros((5, n), dtype=complex)
    for j in range(n):
        p = p_ad[j]
        v = V[:, j]
        ux, uz, wx, wz, th_j = v
        # sigma_zz row
        B[0, j] = 1j * (m.C12 * k * ux + m.C11 * p * uz
                        + m.R2 * k * wx + m.R1 * p * wz) - m.beta1 * th_j
        # sigma_xz row
        B[1, j] = 1j * (m.C66 * p * ux + m.C66 * k * uz
                        + m.R6 * p * wx + m.R6 * k * wz)
        # phason rows
        if ph == "free":
            B[2, j] = 1j * (m.R6 * p * ux + m.R6 * k * uz
                            + m.K3 * p * wx + m.K6 * k * wz)   # H_xz (K3, K6)
            B[3, j] = 1j * (m.R2 * k * ux + m.R1 * p * uz
                            + m.K2 * k * wx + m.K1 * p * wz)   # H_zz (K2, K1)
        elif ph == "clamped":
            B[2, j] = wx
            B[3, j] = wz
        else:
            raise ValueError("bc['phason'] must be 'free' or 'clamped'")
        # thermal row
        if th == "isothermal":
            B[4, j] = th_j
        elif th == "insulated":
            B[4, j] = 1j * p * th_j
        else:
            raise ValueError("bc['thermal'] must be 'isothermal' or 'insulated'")
    return B
