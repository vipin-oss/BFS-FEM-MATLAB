"""Statistical-layer tests (eq:fisher-def, eq:bic, eq:seB)."""
import sys, numpy as np, pytest, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.model import Theta, Geometry
from src.statistics import fisher, bic, sigma_of, band_edge
from src.calibration import CASES, aggregate, max_B_deviation

CFG = json.loads((ROOT / "config" / "default_parameters.json").read_text())
cfg = dict(CFG["reference_configuration"]); cfg.update(CFG["statistics"])
GEOM = Geometry(cfg["L"], cfg["t_p"])
T80 = np.linspace(cfg["t_min"], cfg["t_max"], cfg["n_points"])


def test_eq_bic_formula():
    # BIC = n ln(SSE/n) + k ln n
    assert bic(10.0, 80, 3) == pytest.approx(80 * np.log(10.0 / 80) + 3 * np.log(80))
    # penalty difference between k=3 and k=1 at n=80
    assert bic(1.0, 80, 3) - bic(1.0, 80, 1) == pytest.approx(2 * np.log(80))


def test_sigma_definition():
    y = np.array([0.0, 0.5, 2.0])
    assert sigma_of(y, 0.02) == pytest.approx(0.04)


def test_fisher_well_conditioned_away_from_resonance():
    r = fisher(Theta.from_B(1.0, 0.03, 5.0), T80, GEOM, 0.02)
    assert r["cond"] < 1e3 and r["se_tau_q"] < 15


def test_fisher_ill_conditioned_at_resonance():
    r = fisher(Theta.from_B(1.0, 0.03, 1.0 + 1e-7), T80, GEOM, 0.02)
    assert r["cond"] > 1e12


def test_band_edges_bracket_resonance():
    lo = band_edge(20.0, 1.0, 0.01, T80, GEOM, 0.02)
    hi = band_edge(20.0, 1.0, 20.0, T80, GEOM, 0.02)
    assert lo < 1.0 < hi
    assert lo == pytest.approx(0.628, abs=0.005)
    assert hi == pytest.approx(1.804, abs=0.005)


def test_calibration_dataset_integrity():
    assert len(CASES) == 12
    assert max_B_deviation() < 0.02
    # exactly one case reports uncertainties
    assert sum(1 for c in CASES if c.dB_rel is not None) == 1
    a = aggregate(0.628, 1.804)
    assert a["n_inside"] == 8 and a["n_outside"] == 4


def test_both_case_arithmetic():
    c = [x for x in CASES if x.idx == 12][0]
    assert c.B_calc == pytest.approx(1.532, abs=0.001)
    assert c.dB_rel == pytest.approx(0.0278, abs=0.0005)
