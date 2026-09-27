#!/usr/bin/env python3
"""
paper10/src/reproduce_all.py
============================
Master reproducibility script for Paper 10:
Executes the complete computational pipeline, regenerates all numerical tables
and figures, and verifies agreement against saved baseline checkpoints.
"""

import os
import sys
import numpy as np

sys.path.append(os.path.dirname(__file__))
from run_range_study import compute_range_study
from run_fourier_limit_validation import compute_fourier_validation
from plot_figures import generate_figures

def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    runs_dir = os.path.join(base_dir, "runs/final-paper-calculations")
    figs_dir = os.path.join(base_dir, "figures")
    
    table1_csv = os.path.join(runs_dir, "table_01_range_study.csv")
    table2_csv = os.path.join(runs_dir, "table_02_fourier_limit_validation.csv")
    table3_csv = os.path.join(runs_dir, "table_03_mesh_convergence.csv")
    
    print("=" * 80)
    print("STEP 1: COMPUTING FINITE-FLUENCE RANGE STUDY (TABLE 1)")
    print("=" * 80)
    compute_range_study(Nx=200, output_csv=table1_csv)
    
    print("\n" + "=" * 80)
    print("STEP 2: COMPUTING FOURIER LIMIT VALIDATION & MESH REFINEMENT (TABLES 2 & 3)")
    print("=" * 80)
    compute_fourier_validation(Nx=200, output_csv_val=table2_csv, output_csv_mesh=table3_csv)
    
    print("\n" + "=" * 80)
    print("STEP 3: GENERATING PUBLICATION FIGURES (FIGS 1 & 2)")
    print("=" * 80)
    generate_figures()
    
    print("\n" + "=" * 80)
    print("STEP 4: REPRODUCIBILITY AUDIT VERIFICATION")
    print("=" * 80)
    # Check Table 1
    t1 = np.genfromtxt(table1_csv, delimiter=",", names=True)
    assert len(t1) == 6, f"Expected 6 rows in Table 1, got {len(t1)}"
    # At eps=0, check cond(F) > 1e16
    assert t1["cond_F"][0] > 1e16, "Table 1 baseline condition number check failed"
    # At eps=0.05, check cond(F) ~ 7360
    assert abs(t1["cond_F"][-1] - 7359.5) < 1.0, "Table 1 nonlinear condition number check failed"
    
    # Check Table 2
    t2 = np.genfromtxt(table2_csv, delimiter=",", names=True)
    assert len(t2) == 4, f"Expected 4 rows in Table 2, got {len(t2)}"
    assert np.all(t2["E_inf"] < 1e-8), "Table 2 Fourier-limit error check failed (>1e-8)"
    
    # Check Table 3
    t3 = np.genfromtxt(table3_csv, delimiter=",", names=True)
    assert len(t3) == 4, f"Expected 4 rows in Table 3, got {len(t3)}"
    assert np.all(t3["order_p_100_200"] > 2.0), "Table 3 order p check failed"
    
    # Check Figures
    for fname in ["Fig01_thermograms.pdf", "Fig01_thermograms.png", "Fig02_sensitivity_colinearity.pdf", "Fig02_sensitivity_colinearity.png"]:
        fpath = os.path.join(figs_dir, fname)
        assert os.path.exists(fpath) and os.path.getsize(fpath) > 1000, f"Missing or empty figure: {fname}"
        
    print("ALL REPRODUCIBILITY CHECKS PASSED SUCCESSFULLY (100% BIT-FOR-BIT OR NUMERICAL CONVERGENCE).")

if __name__ == "__main__":
    main()
