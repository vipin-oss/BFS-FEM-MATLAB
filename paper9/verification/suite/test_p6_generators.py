"""
test_p6_generators.py
Automated verification of Phase 6 figure and table deliverables.
Verifies file existence, vector PDF headers, LaTeX syntax, and non-fabrication of blocked floats.
"""
import os
import glob
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
FIG_OUT = os.path.join(REPO_ROOT, 'paper9/figures/out')
TAB_OUT = os.path.join(REPO_ROOT, 'paper9/tables/out')

PERMISSIBLE_FIGS = [
    'fig01_ellipsoid_tensor.pdf',
    'fig02_lattice_ibz.pdf',
    'fig03_bfs_dof_bloch.pdf',
    'fig05_mesh_convergence.pdf',
    'fig06_caseH_dispersion.pdf',
    'fig08_theta_sweep.pdf',
    'fig09_ar_sweep.pdf',
    'fig10_design_map_3d.pdf',
    'fig11_polar_map_regimes.pdf',
    'fig12_ifc_wave_steering.pdf',
    'fig13_energy_microinertia.pdf'
]

BLOCKED_FIGS = [
    'fig04_anchor_overlays.pdf',
    'fig07_caseC_bands_modes.pdf'
]

PERMISSIBLE_TABS = [
    'tab01_literature_positioning.tex',
    'tab02_parameters.tex',
    'tab04_consistency_suite.tex',
    'tab05_gap_summary.tex',
    'tab06_convergence_floor.tex'
]

BLOCKED_TABS = [
    'tab03_anchor_errors.tex'
]

def test_permissible_figures_exist_and_valid():
    """Verify that all 11 unlocked figures exist and have valid PDF headers."""
    for fig_name in PERMISSIBLE_FIGS:
        path = os.path.join(FIG_OUT, fig_name)
        assert os.path.isfile(path), f"Missing figure file: {fig_name}"
        assert os.path.getsize(path) > 1000, f"Figure file suspiciously small: {fig_name}"
        with open(path, 'rb') as f:
            header = f.read(5)
            assert header == b'%PDF-', f"Figure {fig_name} is not a valid PDF: {header}"

def test_blocked_figures_not_fabricated():
    """Verify that blocked figures are not fabricated as fake/empty files."""
    for fig_name in BLOCKED_FIGS:
        path = os.path.join(FIG_OUT, fig_name)
        assert not os.path.exists(path), f"Blocked figure was fabricated: {fig_name}"

def test_permissible_tables_exist_and_valid():
    """Verify that all 5 unlocked tables exist and have valid LaTeX tabular environments."""
    for tab_name in PERMISSIBLE_TABS:
        path = os.path.join(TAB_OUT, tab_name)
        assert os.path.isfile(path), f"Missing table file: {tab_name}"
        assert os.path.getsize(path) > 100, f"Table file suspiciously small: {tab_name}"
        with open(path, 'r') as f:
            content = f.read()
            assert '\\begin{tabularx}' in content, f"Table {tab_name} lacks begin tabularx"
            assert '\\end{tabularx}' in content, f"Table {tab_name} lacks end tabularx"

def test_blocked_tables_not_fabricated():
    """Verify that blocked tables are not fabricated."""
    for tab_name in BLOCKED_TABS:
        path = os.path.join(TAB_OUT, tab_name)
        assert not os.path.exists(path), f"Blocked table was fabricated: {tab_name}"
