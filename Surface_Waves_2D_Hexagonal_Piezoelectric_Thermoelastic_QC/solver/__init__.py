"""Semi-analytical surface-wave solver for 2D hexagonal thermoelastic QC.

Frozen sources of truth: QC_First_Paper_Blueprint.md (design) and
QC_Final_Mathematical_Formulation.pdf (equations). No FEM, no complex-k,
no leaky modes, no added physics.
"""
from . import material, matrix, roots, boundary, residual, branch, diagnostics, record
