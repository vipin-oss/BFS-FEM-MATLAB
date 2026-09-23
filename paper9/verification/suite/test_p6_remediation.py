"""
test_p6_remediation.py
Targeted regression tests for Phase-6 forensic remediations.
Enforces physical mode polarization, passive tensor rotation conventions,
clean convergence fit terminology, and accurate float descriptions.
"""
import os
import sys
import json
import numpy as np
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from paper9.solver.bfs_bloch_solver import assemble_KM, L_plane, semi_axes_from_ar, solve_bloch


def test_finding1_modal_polarization_at_X():
    """Verify physical polarization of the lowest 4 branches at X = (pi/L, 0).
    Branch 0: transverse acoustic (uy displacement).
    Branch 1: transverse microstructural (uy,x gradient).
    Branch 2: longitudinal acoustic (ux displacement, c_L/c_T = sqrt((lambda+2mu)/mu)).
    Branch 3: longitudinal microstructural (ux,x gradient).
    Branch 1 MUST NEVER be identified as longitudinal.
    """
    L = 1.0; lam = 1.0; mu = 1.0; rho = 1.0; ell2 = 0.04
    l_iso = 0.20; ar = 5.0
    l1, l2 = semi_axes_from_ar(ar, l_iso=l_iso, rule='volume_equivalent')
    L11, L22, L12 = L_plane(l1, l2, 0.0)
    K, M = assemble_KM(hx=L, hy=L, lam=lam, mu=mu, L11=L11, L22=L22, L12=L12, rho=rho, ell2=ell2)

    oms, om2, evecs, Mb, hK, hM = solve_bloch(K, M, np.pi/L, 0.0, L)
    # Node 0 DOFs: [ux, ux,x, ux,y, ux,xy, uy, uy,x, uy,y, uy,xy]
    v0 = evecs[:, 0]
    v1 = evecs[:, 1]
    v2 = evecs[:, 2]
    v3 = evecs[:, 3]

    # Branch 0 is transverse acoustic: strong uy, zero ux
    assert abs(v0[4]) > 1.0, "Branch 0 must have dominant uy displacement"
    assert abs(v0[0]) < 1e-12, "Branch 0 must have zero ux displacement"

    # Branch 1 is transverse microstructural: zero displacement, non-zero uy,x
    assert abs(v1[0]) < 1e-12 and abs(v1[4]) < 1e-12, "Branch 1 must have zero nodal displacement"
    assert abs(v1[5]) > 1.0, "Branch 1 must have non-zero uy,x gradient DOF"

    # Branch 2 is longitudinal acoustic: strong ux, zero uy
    assert abs(v2[0]) > 1.0, "Branch 2 must have dominant ux displacement"
    assert abs(v2[4]) < 1e-12, "Branch 2 must have zero uy displacement"

    # Branch 3 is longitudinal microstructural: zero displacement, non-zero ux,x
    assert abs(v3[0]) < 1e-12 and abs(v3[4]) < 1e-12, "Branch 3 must have zero nodal displacement"
    assert abs(v3[1]) > 1.0, "Branch 3 must have non-zero ux,x gradient DOF"

    # Verify that generator scripts use branch 2 for longitudinal acoustic
    with open(os.path.join(REPO_ROOT, 'paper9/figures/gen/fig08_theta_sweep.py')) as f:
        code8 = f.read()
    with open(os.path.join(REPO_ROOT, 'paper9/figures/gen/fig09_ar_sweep.py')) as f:
        code9 = f.read()

    assert "omega_X\'][2]" in code8, "fig08 must extract branch 2 (index 2) for longitudinal acoustic"
    assert "omega_X\'][2]" in code9, "fig09 must extract branch 2 (index 2) for longitudinal acoustic"
    assert "omega_X\'][1]" not in code8 or "Branch 1" not in code8.split("omega_X\'][1]")[1][:40], \
        "Branch 1 must not be labeled as longitudinal"


def test_finding2_passive_rotation_tensor_L():
    """Verify passive coordinate rotation convention L = R^T diag(l1^2, l2^2) R.
    - theta = 0 gives diag(l1^2, l2^2)
    - theta = 90 deg gives diag(l2^2, l1^2)
    - theta = 45 deg gives L12 < 0 when l1 > l2
    - eigenvalues are identically {l1^2, l2^2} for all theta.
    """
    l1 = 0.4472135954999579  # AR = 5
    l2 = 0.08944271909999159

    # theta = 0
    L11_0, L22_0, L12_0 = L_plane(l1, l2, 0.0)
    assert np.isclose(L11_0, l1**2), "L11(0) must equal l1^2"
    assert np.isclose(L22_0, l2**2), "L22(0) must equal l2^2"
    assert np.isclose(L12_0, 0.0, atol=1e-15), "L12(0) must be 0"

    # theta = 90 deg
    L11_90, L22_90, L12_90 = L_plane(l1, l2, np.pi/2)
    assert np.isclose(L11_90, l2**2), "L11(90) must equal l2^2"
    assert np.isclose(L22_90, l1**2), "L22(90) must equal l1^2"
    assert np.isclose(L12_90, 0.0, atol=1e-15), "L12(90) must be 0"

    # theta = 45 deg
    L11_45, L22_45, L12_45 = L_plane(l1, l2, np.pi/4)
    expected_L12_45 = (l2**2 - l1**2) / 2.0
    assert expected_L12_45 < 0.0, "L12 at 45 deg must be strictly negative for l1 > l2"
    assert np.isclose(L12_45, expected_L12_45), f"L12(45) {L12_45} must equal {expected_L12_45}"

    # Eigenvalue invariance across sweep
    for th in np.linspace(0, np.pi, 37):
        L11, L22, L12 = L_plane(l1, l2, th)
        L_mat = np.array([[L11, L12], [L12, L22]])
        evals = np.sort(np.linalg.eigvalsh(L_mat))
        expected_evals = np.sort([l2**2, l1**2])
        assert np.allclose(evals, expected_evals, atol=1e-14), f"Eigenvalues must remain invariant at theta={th}"

    # Verify that fig01 generator script uses (l2**2 - l1**2)
    with open(os.path.join(REPO_ROOT, 'paper9/figures/gen/fig01_ellipsoid_tensor.py')) as f:
        code1 = f.read()
    assert "(l2_b**2 - l1_b**2)" in code1, "fig01 must use passive convention (l2^2 - l1^2)"
