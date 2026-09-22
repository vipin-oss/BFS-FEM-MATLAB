"""Level-1 homogeneous TM vs LWZ (14.1). Pre-declared tol 1e-8."""
import numpy as np
from lwz_tm_sh_normal import layer_T_sh_normal, omega_from_sigma, propagating_k_from_T

TOL = 1e-8
A, C, D, MU, RHO = 1.0, 0.25, 0.5, 1.0, 1.0
VS = 1.0


def test_homogeneous_vs_14_1():
    for sig in (0.1, 0.5, 1.0, 2.0, np.pi * 0.25):
        om = omega_from_sigma(sig, VS, C, D)
        T, _, _ = layer_T_sh_normal(om, A, C, D, MU, RHO)
        kB, _, dist = propagating_k_from_T(T, A, sigma_ref=sig)
        fold = ((sig + np.pi / A) % (2 * np.pi / A)) - np.pi / A
        assert abs(kB - fold) / max(abs(fold), 1e-12) < TOL
        assert dist < TOL


def test_identical_bilayer():
    from lwz_tm_sh_normal import bilayer_T

    sig = 1.0
    om = omega_from_sigma(sig, VS, C, D)
    T = bilayer_T(om, 0.5, 0.5, C, C, D, D, MU, MU, RHO, RHO)
    kB, _, dist = propagating_k_from_T(T, A, sigma_ref=sig)
    assert abs(kB - sig) / sig < 1e-7
    assert dist < 1e-7
