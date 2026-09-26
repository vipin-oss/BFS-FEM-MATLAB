"""
Unit test for parameters module
"""
import sys
import os
import numpy as np

# Add solver path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from solver.parameters import (
    MaterialParameters,
    UnitCellGeometry,
    get_benchmark_papargyri_beskou_material,
    get_li_acta_mech_materials
)

def test_material_parameters():
    mat = get_benchmark_papargyri_beskou_material()
    assert mat.rho == 2000.0
    assert np.isclose(mat.Vs, 1000.0)
    assert np.isclose(mat.g, 0.001)
    assert np.isclose(mat.h, 0.0015)
    assert mat.beta == 0.0
    
    # Check micro-inertia ms
    omega = 1.0e5
    ms_expected = (omega**2 * mat.d**2) / (3.0 * mat.Vs**2)
    assert np.isclose(mat.ms(omega), ms_expected)
    print("test_material_parameters: PASS")

def test_li_materials():
    matA, matB, geom = get_li_acta_mech_materials(a=1.0)
    assert geom.a == 1.0
    assert geom.a1 == 0.5
    assert geom.a2 == 0.5
    assert np.isclose(matA.Vs, 1.0)
    assert np.isclose(matB.Vs, 0.5947)
    assert np.isclose(matB.rho, 0.1573)
    print("test_li_materials: PASS")

if __name__ == "__main__":
    test_material_parameters()
    test_li_materials()
    print("ALL PARAMETER TESTS PASSED!")
