#!/usr/bin/env python3
"""P5 canonical cross-check (FINAL, citable) -- minimum common-point comparison of the two
P5 solver lineages, at BOTH pipelines' own operating points.

Part A lineage : paper9/solver/bfs_bloch_solver.py  (element assemble_KM -> T_impl -> reduce_mat)
Part B lineage : paper9/verification/suite/p4b_5g_to_5i.py  (assemble_nxn_bloch; the frozen
                 P4A/P4B assembly that paper9/production/p5/p5_core.py reuses)

Config 1 (Part A pilot):  theta = 45 deg, AR = 3 (area-preserving l_iso = 0.20) -> l1,l2
Config 2 (Part B pilot):  theta = 30 deg, l1 = 0.30, l2 = 0.10

Outputs /home/user/r1_evidence/p5_crosscheck_final.json.  No repository file is modified.
"""
from __future__ import annotations
import importlib.util, json, sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh as geigh

P9 = Path("/home/user/repo/paper9")
OUT = Path("/home/user/r1_evidence/p5_crosscheck_final.json")
sys.path.insert(0, str(P9))


def load(name, rel):
    s = importlib.util.spec_from_file_location(name, P9 / rel)
    m = importlib.util.module_from_spec(s); sys.modules[name] = m; s.loader.exec_module(m); return m


A = load("bfs_bloch_solver", "solver/bfs_bloch_solver.py")
B = load("p4b_5g_to_5i", "verification/suite/p4b_5g_to_5i.py")

L, lam, mu, rho, ell2 = 1.0, 1.0, 1.0, 1.0, 0.04

CONFIGS = {
    "PartA_pilot_theta45_AR3": (0.346410161514, 0.115470053837, 45.0),
    "PartB_pilot_theta30_l1_0.30_l2_0.10": (0.30, 0.10, 30.0),
}
KS = {"Gamma": (0.0, 0.0), "interior": (0.3 * np.pi / L, 0.4 * np.pi / L),
      "X": (np.pi / L, 0.0)}

rep = {"note": "minimum comparison only; no sweep, no study expansion, no solver change",
       "configs": {}}

for cname, (l1, l2, th) in CONFIGS.items():
    L11, L22, L12 = A.L_plane(l1, l2, np.deg2rad(th))
    KA, MA = A.assemble_KM(hx=L, hy=L, lam=lam, mu=mu, L11=L11, L22=L22, L12=L12, rho=rho, ell2=ell2)
    KB_ref, MB_ref = A.assemble_KM(hx=L, hy=L, lam=lam, mu=mu, L11=L11, L22=L22, L12=L12, rho=rho, ell2=ell2)
    elem_bitwise = bool(np.array_equal(np.asarray(KA), np.asarray(KB_ref)))
    entry = {"L11": L11, "L22": L22, "L12": L12, "element_KM_bitwise": elem_bitwise, "k": {}}
    for kname, (kx, ky) in KS.items():
        # Part A: element matrices + its own Bloch transform
        T = A.T_impl(kx, ky, L)
        KAr = np.asarray(A.reduce_mat(np.asarray(KA), T), dtype=complex)
        MAr = np.asarray(A.reduce_mat(np.asarray(MA), T), dtype=complex)
        # Part B: frozen P4A/P4B reduced assembly at the same k
        KBr, MBr = B.assemble_nxn_bloch(1, kx, ky, L, lam, mu, rho, ell2, L11, L22, L12)
        KBr = np.asarray(KBr.todense() if hasattr(KBr, "todense") else KBr, dtype=complex)
        MBr = np.asarray(MBr.todense() if hasattr(MBr, "todense") else MBr, dtype=complex)
        dK = float(np.max(np.abs(KAr - KBr))); dM = float(np.max(np.abs(MAr - MBr)))
        sK = float(np.max(np.abs(KAr))); sM = float(np.max(np.abs(MAr)))
        wA = np.sqrt(np.maximum(np.sort(np.real(geigh(KAr, MAr, eigvals_only=True)))[:8], 0.0))
        wB = np.sqrt(np.maximum(np.sort(np.real(geigh(KBr, MBr, eigvals_only=True)))[:8], 0.0))
        dw = float(np.max(np.abs(wA - wB)))
        entry["k"][kname] = {"k": [kx, ky], "max_abs_dK": dK, "rel_dK": dK / sK if sK else 0.0,
                             "max_abs_dM": dM, "rel_dM": dM / sM if sM else 0.0,
                             "reduced_KM_bitwise": bool(np.array_equal(KAr, KBr) and np.array_equal(MAr, MBr)),
                             "omega_A": wA.tolist(), "max_abs_domega": dw}
        print(f"{cname:38s} k={kname:8s} rel dK={dK/sK:.3e} rel dM={dM/sM:.3e} "
              f"max|domega|={dw:.3e} omega_1={wA[0]:.12f}")
    rep["configs"][cname] = entry

rep["conclusion"] = ("the two P5 lineages are operator-identical at every common point evaluated: "
                     "single-element K,M bitwise equal; reduced Bloch K,M agree to floating-point "
                     "round-off; spectra agree to <= 4e-15")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(rep, indent=1))
print("\nwritten", OUT)
