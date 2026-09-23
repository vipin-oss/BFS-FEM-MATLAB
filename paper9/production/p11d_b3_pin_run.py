"""P11D pinned run for Benchmark B3 (remediation item 7).

Pins the EXACT computation whose output the manuscript quotes for B3
(Pb/Brass dipolar-gradient SH bilayer, Li et al. 2023 Fig. 4(c) parameters):

  run_id          : P11D-B3-R1
  resolution      : N_points = 720 on w_bar in [0.01, 3.6] (np.linspace)
  solver          : paper9.validation.b1_b2_b3_solver.BenchmarkB3 (LWZ 2016
                    Appendix 3 transfer matrix, sigma/tau quadratic roots)
  branch extraction: eigenvalues of T_cell = T_B T_A; a branch sample is
                    (w_bar, |arg(lambda)|/pi) for every eigenvalue with
                    | |lambda| - 1 | < 0.02
  gap detection   : w_bar intervals with NO such eigenvalue (grid-level,
                    edges = first grid points of the transition, 4-dp rounding
                    as in compute_heterogeneous_dispersion)
  parameters      : mu_1 = 2.3e10 Pa, rho_1 = 7.5e3 kg/m^3, a_1 = 1e-5 m,
                    c_1 = 0.15 a_1^2, d_1 = 0.25 a_1 (Li et al. 2023 Fig. 3(b)
                    c_bar/d_bar values carried to Fig. 4(c); provenance class
                    [S], NOT author-specified Fig. 4(c) parameters -- see
                    paper9/audit/P3_TV_RESOLUTION.md), layer 2: mu_2 = 0.056
                    mu_1, rho_2 = 0.157 rho_1, a_2 = a_1, c_2 = 1.5 c_1,
                    d_2 = 1.5 d_1; omega_0 = 2 pi / (a_1/Vs_1 + a_2/Vs_2),
                    Vs_i = sqrt(mu_i/rho_i)  (omega_0 = 4.1142e8 rad/s).

Output: paper9/results/raw/p11d_b3_run_P11D-B3-R1.json  (values unchanged from
the manuscript; this file merely supplies the missing provenance).  The script
FAILS if the 3-dp values do not reproduce the manuscript numbers.

Usage: python3 paper9/production/p11d_b3_pin_run.py
"""
from __future__ import annotations

import json
import os
import platform
import subprocess
import sys

import numpy as np
import scipy

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO_ROOT)

from paper9.validation.b1_b2_b3_solver import BenchmarkB3  # noqa: E402

RUN_ID = "P11D-B3-R1"
N_POINTS = 720
W_LO, W_HI = 0.01, 3.6
MODULUS_TOL = 0.02
OUT = os.path.join(REPO_ROOT, "paper9", "results", "raw", "p11d_b3_run_P11D-B3-R1.json")

# 3-dp values as printed in the manuscript (must reproduce; do NOT change)
MANUSCRIPT_3DP = [
    [0.340, 1.024, 0.684],
    [1.423, 1.867, 0.444],
    [2.477, 2.911, 0.434],
]


def main():
    b3 = BenchmarkB3()
    het = b3.compute_heterogeneous_dispersion(N_points=N_POINTS)
    gaps = het["band_gaps"]  # already 4-dp, first 5
    l1 = b3.run_level1_homogeneous()
    l2 = b3.run_level2_identical_reduction()

    repro_3dp = [[round(g[0], 3), round(g[1], 3), round(g[2], 3)] for g in gaps[:3]]
    reproducible = repro_3dp == MANUSCRIPT_3DP

    doc = {
        "schema": "p11d.b3_pinned_run.v1",
        "run_id": RUN_ID,
        "date": __import__("datetime").datetime.now().astimezone().isoformat(),
        "git_sha": (subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT,
                                   capture_output=True, text=True).stdout or "").strip(),
        "git_branch": (subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                                      cwd=REPO_ROOT, capture_output=True,
                                      text=True).stdout or "").strip(),
        "engine": "paper9.validation.b1_b2_b3_solver.BenchmarkB3 "
                  "(LWZ 2016 Appendix-3 transfer matrix; sigma_tau quadratic roots)",
        "resolution": {"N_points": N_POINTS, "w_bar_range": [W_LO, W_HI],
                       "grid": "numpy.linspace(0.01, 3.6, 720)"},
        "options": {
            "branch_extraction": "eigenvalues of T_cell = T_B T_A via "
                                 "scipy.linalg.eigvals; branch sample "
                                 "(w_bar, |arg(lambda)|/pi) per eigenvalue with "
                                 f"||lambda|-1| < {MODULUS_TOL}",
            "gap_detection": "w_bar intervals with no such eigenvalue; edges = "
                             "grid transition points; values rounded to 4 dp "
                             "(compute_heterogeneous_dispersion convention)",
            "modulus_tolerance": MODULUS_TOL,
        },
        "parameters": {
            "layer1_Pb": {"mu_1_Pa": b3.mu_1, "rho_1": b3.rho_1, "a_1_m": b3.a_1,
                          "c_1": b3.c_1, "d_1": b3.d_1},
            "layer2_Brass": {"mu_2_Pa": b3.mu_2, "rho_2": b3.rho_2, "a_2_m": b3.a_2,
                             "c_2": b3.c_2, "d_2": b3.d_2},
            "omega_0": b3.omega_0, "b": b3.b,
            "parameter_provenance": {
                "mu/rho/a ratios": "Li et al. (2023) p. 14 [C]",
                "c_bar_1 = 0.15, d_bar_1 = 0.25, c_R = d_R = 1.5":
                    "Li et al. (2023) Fig. 3(b) values; the Fig. 4(c) panel has "
                    "no c_bar/d_bar annotation -- provenance class [S] "
                    "(inherited/source-derived), NOT [C] (author-specified)",
            },
        },
        "environment": {
            "python": sys.version,
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "level1_homogeneous": l1,
        "level2_identical_reduction": l2,
        "band_gaps_4dp": gaps,
        "band_gaps_3dp": repro_3dp,
        "manuscript_values_3dp": MANUSCRIPT_3DP,
        "manuscript_values_reproduced": reproducible,
        "branches_count": het["branches_count"],
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=2)
    print(f"wrote {OUT}")
    print("gaps 3dp:", repro_3dp, "| reproduced:", reproducible)
    print("level1:", l1["status"], l1["max_error"], "| level2:", l2["status"], l2["max_error"])
    if not reproducible:
        raise SystemExit("FAIL: manuscript 3-dp values NOT reproduced -- investigate")
    if l1["status"] != "PASS" or l2["status"] != "PASS":
        raise SystemExit("FAIL: level checks not PASS at declared tolerance")


if __name__ == "__main__":
    main()
