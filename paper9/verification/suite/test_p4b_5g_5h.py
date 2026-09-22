"""Lightweight 5g/5h pytest (no 5i mesh). Tolerances as in p4b_5g_to_5i.py."""
import numpy as np
from p4b_5g_to_5i import (
    TOL_5G_ASY,
    TOL_5H_IDENTITY,
    caseH_1d_averages,
    central_vg,
    leff2_dir,
    vbar_T,
)


def test_5g_bounded_kbar200():
    le2 = leff2_dir(0.2, 0.2, 0.0, 0.0)
    vinf = np.sqrt(le2) / (np.sqrt(10.0) * 0.2)
    v = vbar_T(200.0, 0.2, le2)
    assert abs(v / vinf - 1.0) < TOL_5G_ASY


def test_5g_unbounded_kbar200():
    le2 = leff2_dir(0.2, 0.2, 0.0, 0.0)
    v = vbar_T(200.0, 0.0, le2)
    pred = np.pi * np.sqrt(le2) / np.sqrt(10.0) * 200.0
    assert abs(v / pred - 1.0) < TOL_5G_ASY
    assert v > 10.0  # unbounded vs vinf~0.32


def test_5h_energy_vs_central_diff():
    W, T, S, _ = caseH_1d_averages("T", 1.1, 1.0, 1.0, 1.0, 1.0, 0.2, 0.2)
    ve = S / (W + T)
    vg = central_vg("T", 1.1, 2e-4, 1.0, 1.0, 1.0, 0.2, 0.2)
    assert abs(W - T) / abs(W) < TOL_5H_IDENTITY
    assert abs(ve - vg) / abs(vg) < TOL_5H_IDENTITY
