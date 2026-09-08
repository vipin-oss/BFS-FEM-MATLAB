"""Unit tests tied to specific equation labels in the calculation master."""
import sys, numpy as np, pytest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.model import Theta, Geometry, B_of, kappa2_of, param_jacobian_det, nondimensional
from src.laplace import m2, t_star, csch, coth
from src.limits import m2_limit, mcv_wave_speed, T_series
from src.forward import forward, forward_and_jacobian

GEOM = Geometry(1.0, 0.04)


def test_eq_Bdef_and_inverse():
    assert B_of(2.0, 0.5, 3.0) == pytest.approx(3.0 / (2.0 * 0.5))
    assert kappa2_of(2.0, 0.5, 1.7) == pytest.approx(2.0 * 0.5 * 1.7)
    assert Theta.from_B(2.0, 0.5, 1.7).B == pytest.approx(1.7)


def test_eq_param_det():
    assert param_jacobian_det(2.0, 0.5) == pytest.approx(1.0)


def test_eq_res_step5_cancellation():
    s = np.array([1e-3, 0.7, 5.0, 40.0, 1e3])
    for al, tq in ((1.0, 0.03), (2.7, 0.3), (0.5, 0.01)):
        assert np.allclose(m2(s, tq, al * tq, al), s / al, rtol=0, atol=1e-14)


def test_eq_Binv_thickness_cancels():
    a, tq, k2 = 0.61e-6, 0.344, 0.268e-6
    vals = []
    for Lmm in (1.86, 2.75, 3.84):
        g = Geometry(Lmm * 1e-3, 0.01)
        nd = nondimensional(Theta(a, tq, k2), g)
        vals.append(nd["kappa2_hat"] / (nd["alpha_hat"] * nd["tau_q_hat"]))
    assert max(vals) - min(vals) < 1e-12
    assert vals[0] == pytest.approx(B_of(a, tq, k2))


def test_eq_limits():
    s = np.array([0.5, 5.0])
    assert np.allclose(m2_limit(s, "fourier", alpha_hat=2.0), s / 2.0)
    assert np.allclose(m2_limit(s, "mcv", tau_q_hat=0.1, alpha_hat=2.0),
                       s * (1 + 0.1 * s) / 2.0)
    assert np.allclose(m2_limit(s, "nyiri", kappa2_hat=0.3, alpha_hat=2.0),
                       s / (2.0 + 0.3 * s))
    assert mcv_wave_speed(4.0, 1.0) == pytest.approx(2.0)


def test_eq_tstar():
    assert t_star(40, 0.04) == pytest.approx(0.16)


def test_overflow_guards_finite():
    m = np.array([1e-6, 1.0, 50.0, 800.0], dtype=complex)
    assert np.all(np.isfinite(csch(m))) and np.all(np.isfinite(coth(m)))


def test_even_M_warns():
    with pytest.warns(RuntimeWarning):
        forward(Theta(1.0, 0.02, 0.02), np.array([0.5]), GEOM, M=40)


def test_analytic_jacobian_matches_central_difference():
    """Module-2 acceptance (<1e-6 relative) for the tau_q and kappa2 columns.

    The comparison uses RICHARDSON-EXTRAPOLATED central differences. A plain
    central difference is only O(h^2) accurate and, for h below about 1e-5
    relative, is dominated by round-off cancellation: a step of h=1e-6 gives a
    2.7e-5 apparent deviation that is an artefact of the difference, not of the
    analytic derivative. The extrapolated estimate reaches 4e-7.
    """
    th = Theta(1.0, 0.03, 0.03 * 1.28)
    t = np.linspace(0.05, 1.0, 25)
    _, J = forward_and_jacobian(th, t, GEOM)
    p = th.as_array()

    def central(i, h):
        pp = p.copy(); pp[i] += h
        pm = p.copy(); pm[i] -= h
        return (forward(Theta(*pp), t, GEOM) - forward(Theta(*pm), t, GEOM)) / (2 * h)

    for i in (1, 2):
        h = p[i] * 1e-4
        rich = (4.0 * central(i, h / 2) - central(i, h)) / 3.0
        rel = np.max(np.abs(rich - J[:, i])) / np.max(np.abs(J[:, i]))
        assert rel < 1e-6, f"column {i}: relative deviation {rel:.3e}"


def test_series_converges_to_convolution():
    t = np.linspace(0.05, 1.0, 30)
    conv = forward(Theta(1.0, 0.02, 0.02), t, GEOM)
    assert np.max(np.abs(T_series(t, 4000, 0.04) - conv)) < 1e-4


def test_positivity_and_steady_state():
    t = np.linspace(0.005, 1.0, 200)
    for k2 in (0.02, 0.20):
        y = forward(Theta(1.0, 0.02, k2), t, GEOM)
        assert y.min() >= -1e-12
    assert forward(Theta(1.0, 0.02, 0.02), np.array([50.0]), GEOM)[0] == \
        pytest.approx(1.0, abs=1e-7)


def test_theta_rejects_nonpositive():
    with pytest.raises(ValueError):
        Theta(1.0, -0.1, 0.02)
