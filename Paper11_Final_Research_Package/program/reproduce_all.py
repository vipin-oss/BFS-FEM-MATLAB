"""
reproduce_all.py - Master Automated End-to-End Reproducibility Runner for Paper 11
Part of the Paper 11 Research Package.

Executes:
  1. run_validation.py: Dual Laplace & Cowan benchmarks + grid refinement.
  2. run_heatloss_study.py: Biot number sweeps & sensitivity profiles.
  3. plot_figures.py: All vector PDF & 300-DPI PNG figures.
  4. Comprehensive audit & verification of all generated data artifacts.
"""

import sys
import os
import time
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
RUNS_DIR = os.path.join(BASE_DIR, "data") if os.path.isdir(os.path.join(BASE_DIR, "data")) else os.path.join(BASE_DIR, "runs", "calculations")
FIG_DIR = os.path.join(BASE_DIR, "figures")
OVERLEAF_FIG_DIR = os.path.join(BASE_DIR, "overleaf", "figures")

sys.path.insert(0, SRC_DIR)

from run_validation import run_laplace_validation, run_cowan_fourier_validation, run_mesh_convergence
from run_heatloss_study import run_resonance_heatloss_sweep, run_off_resonance_sweep, run_sensitivity_profiles
from plot_figures import plot_fig1, plot_fig2, plot_fig3, plot_fig4, plot_fig5

def main():
    t_start = time.time()
    print("=" * 80)
    print("PAPER 11: MASTER REPRODUCIBILITY EXECUTION")
    print("Invariance of Guyer-Krumhansl Fourier-Resonance Sensitivity Singularity")
    print("to Boundary Heat Loss in Laser Flash Testing")
    print("=" * 80)

    # 1. Validation Suite
    print("\n>>> STAGE 1: EXECUTING VALIDATION SUITE...")
    run_laplace_validation()
    run_cowan_fourier_validation()
    run_mesh_convergence()

    # 2. Production Calculations
    print("\n>>> STAGE 2: EXECUTING PRODUCTION PARAMETER SWEEPS...")
    run_resonance_heatloss_sweep()
    run_off_resonance_sweep()
    run_sensitivity_profiles()

    # 3. Figure Generation
    print("\n>>> STAGE 3: GENERATING PUBLICATION FIGURES...")
    plot_fig1()
    plot_fig2()
    plot_fig3()
    plot_fig4()
    plot_fig5()

    # 4. Artifact Verification
    print("\n>>> STAGE 4: ARTIFACT CERTIFICATION & AUDIT...")
    expected_files = [
        os.path.join(RUNS_DIR, "validation_laplace.csv"),
        os.path.join(RUNS_DIR, "validation_cowan.csv"),
        os.path.join(RUNS_DIR, "mesh_convergence.csv"),
        os.path.join(RUNS_DIR, "heatloss_parameter_sweep.csv"),
        os.path.join(RUNS_DIR, "off_resonance_sweep.csv"),
        os.path.join(RUNS_DIR, "sensitivity_profiles.csv"),
        os.path.join(FIG_DIR, "fig1_heatloss_temperature_response.pdf"),
        os.path.join(FIG_DIR, "fig1_heatloss_temperature_response.png"),
        os.path.join(FIG_DIR, "fig2_sensitivity_profiles_collinearity.pdf"),
        os.path.join(FIG_DIR, "fig2_sensitivity_profiles_collinearity.png"),
        os.path.join(FIG_DIR, "fig3_invariance_metrics_vs_biot.pdf"),
        os.path.join(FIG_DIR, "fig3_invariance_metrics_vs_biot.png"),
        os.path.join(FIG_DIR, "fig4_singular_spectrum_and_canyon.pdf"),
        os.path.join(FIG_DIR, "fig4_singular_spectrum_and_canyon.png"),
        os.path.join(FIG_DIR, "fig5_validation_dual_benchmarks.pdf"),
        os.path.join(FIG_DIR, "fig5_validation_dual_benchmarks.png"),
    ]

    all_passed = True
    for f in expected_files:
        if os.path.exists(f) and os.path.getsize(f) > 0:
            print(f"  [PASS] {os.path.relpath(f, BASE_DIR)} ({os.path.getsize(f):,} bytes)")
        else:
            print(f"  [FAIL] Missing or empty artifact: {f}")
            all_passed = False

    t_elapsed = time.time() - t_start
    print("\n" + "=" * 80)
    if all_passed:
        print(f"MASTER REPRODUCIBILITY TEST: PASSED in {t_elapsed:.1f} seconds!")
    else:
        print(f"MASTER REPRODUCIBILITY TEST: FAILED in {t_elapsed:.1f} seconds.")
    print("=" * 80)

if __name__ == "__main__":
    main()
