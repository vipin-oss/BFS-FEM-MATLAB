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


def test_finding3_convergence_order_language():
    """Verify that no convergence float claims theoretical convergence order.
    Master Plan §5.7 / line 240:
    'observed rate with 95 % CI reported; no theoretical order claimed; eps_Delta = locked operational floor'
    Forbidden: 'Babuska--Osborn conforming', 'O(h^4.17)', 'fourth-order convergence'.
    """
    fig5_path = os.path.join(REPO_ROOT, 'paper9/figures/gen/fig05_mesh_convergence.py')
    tab6_gen_path = os.path.join(REPO_ROOT, 'paper9/tables/gen/tab06_convergence_floor.py')
    tab6_out_path = os.path.join(REPO_ROOT, 'paper9/tables/out/tab06_convergence_floor.tex')

    with open(fig5_path) as f:
        fig5_code = f.read()
    with open(tab6_gen_path) as f:
        tab6_gen = f.read()
    with open(tab6_out_path) as f:
        tab6_out = f.read()

    forbidden = ["Babu\\v{s}ka--Osborn conforming", "Babu\\v{s}ka-Osborn", "Babuska", "\\mathcal{O}(h", "O(h^4"]
    for word in forbidden:
        assert word not in fig5_code, f"fig05_mesh_convergence.py contains forbidden theoretical claim: {word}"
        assert word not in tab6_gen, f"tab06_convergence_floor.py contains forbidden theoretical claim: {word}"
        assert word not in tab6_out, f"tab06_convergence_floor.tex contains forbidden theoretical claim: {word}"

    # Verify that empirical fit and no-theoretical-claim wording are present
    assert "Empirical fit" in fig5_code, "fig05 must state 'Empirical fit'"
    assert "no theoretical order claimed" in tab6_gen, "tab06_gen must state 'no theoretical order claimed'"
    assert "no theoretical order claimed" in tab6_out, "tab06_out must state 'no theoretical order claimed'"

    # Verify numerical invariants preserved
    assert "4.17" in tab6_out, "Table 6 must preserve slope 4.17"
    assert "3.15" in tab6_out and "5.20" in tab6_out, "Table 6 must preserve 95% CI [3.15, 5.20]"
    assert "4.63e-11" in tab6_out, "Table 6 must preserve eps_Delta = 4.63e-11"


def test_finding5_gap_classification_terminology():
    """Verify that Figure 11 clearly qualifies Delta_GX as a directional gap.
    Path/directional gaps must never be called complete band gaps.
    """
    fig11_path = os.path.join(REPO_ROOT, 'paper9/figures/gen/fig11_polar_map_regimes.py')
    with open(fig11_path) as f:
        code11 = f.read()

    assert "Directional stop band" in code11, "Figure 11 must qualify Delta_GX as 'Directional stop band'"
    assert "complete band gap" not in code11.lower(), "Figure 11 must not claim a complete band gap for Case H"


def test_finding4_fig12_scope_description():
    """Verify Figure 12 accurately describes wave-vector steering at kbar = 0.5.
    Must not claim closed 2D IFC contours.
    """
    fig12_path = os.path.join(REPO_ROOT, 'paper9/figures/gen/fig12_ifc_wave_steering.py')
    with open(fig12_path) as f:
        code12 = f.read()

    assert "bar{k} = 0.5" in code12 or "kbar = 0.5" in code12, "Fig 12 must identify kbar = 0.5 evaluation"
    assert "Steering Deviation" in code12, "Fig 12 panel (a) must identify steering deviation"
    assert "Group Velocity Magnitude" in code12, "Fig 12 panel (b) must identify group velocity magnitude"


def test_finding6_table2_latex_safety():
    """Verify Table 2 contains valid, cleanly escaped LaTeX syntax."""
    tab2_path = os.path.join(REPO_ROOT, 'paper9/tables/out/tab02_parameters.tex')
    with open(tab2_path) as f:
        content = f.read()

    assert "$volume_equivalent$" not in content, "Table 2 must not have unescaped underscore in math volume_equivalent"
    assert "\\texttt{volume\\_equivalent}" in content, "Table 2 must format volume_equivalent cleanly"
    assert "CALC\\_MASTER\\_PLAN" in content, "Table 2 must escape underscores in CALC_MASTER_PLAN"
    assert "\\det(\\mathbf{A}^\\mathsf{T} \\mathbf{A})" in content, "Table 2 must use proper LaTeX math for det(A^T A)"


def test_finding7_table4_scientific_notation():
    """Verify Table 4 formats 5g and 5h in standard publication LaTeX scientific notation."""
    tab4_path = os.path.join(REPO_ROOT, 'paper9/tables/out/tab04_consistency_suite.tex')
    with open(tab4_path) as f:
        content = f.read()

    assert "2.85e-04" not in content, "Table 4 must not contain raw 2.85e-04"
    assert "6.91e-10" not in content, "Table 4 must not contain raw 6.91e-10"
    assert "2.85 \\times 10^{-4}" in content, "Table 4 must format 5g as 2.85 \\times 10^{-4}"
    assert "6.91 \\times 10^{-10}" in content, "Table 4 must format 5h as 6.91 \\times 10^{-10}"
    assert content.count("\\textbf{PASS}") == 8, "Table 4 must have all 8 tests marked PASS"
