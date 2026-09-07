"""V0 - code integrity: dimensions, finiteness, matrix construction,
pencil identity M == A0 + p A1 + p^2 A2, A1(3,4) frozen value, root count,
admissibility bookkeeping, residual calculation, det(A2) != 0.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver.material import Material
from solver import matrix as mx, roots as rt, residual as rs

rng = np.random.default_rng(7)
m = Material()
fails = []

# 1. matrix shape/finiteness + pencil identity (exact entrywise vs pencil)
for _ in range(20):
    k = 10 ** rng.uniform(-2, 2)
    p = complex(*rng.normal(size=2) * 2)
    Om = 10 ** rng.uniform(-2, 2)
    for model in mx.MODELS:
        M = mx.M_matrix(k, p, Om, model, m)
        A0, A1, A2 = mx.pencil(k, Om, model, m)
        err = np.max(np.abs(M - (A0 + p * A1 + p * p * A2))) / np.max(np.abs(M))
        if not np.isfinite(err) or err > 1e-13:
            fails.append(f"pencil identity err {err:.3e} ({model})")
        if not np.all(np.isfinite(M.view(float))):
            fails.append("non-finite M")
# 2. frozen A1 entries
A0, A1, A2 = mx.pencil(1.7, 0.3, "C", m)
if abs(A1[2, 3] - mx.A1_check_entries(m) * 1.7) > 1e-15 or abs(A1[3, 2] - A1[2, 3]) > 0:
    fails.append("A1(3,4)/(4,3) not -(K2+K6)k")
# 3. phason asymmetry present (K3 != K6 roles): off-diagonal is K2+K6, diagonal K1/K3 swap
if abs(A2[2, 2] + m.K3) > 1e-15 or abs(A2[3, 3] + m.K1) > 1e-15:
    fails.append("phason diagonal K1/K3 swap wrong")
if abs(m.K3 - m.K6) < 1e-15:
    fails.append("K3 == K6 would erase the H asymmetry signature")
# 4. root count / admissibility / residuals at sample points
for Om in (0.01, 1.0, 100.0):
    for model in mx.MODELS:
        k = Om / 0.46
        rr = rt.depth_roots(k, Om, model, m)
        if rr["n_roots"] != 10:
            fails.append(f"root count {rr['n_roots']} != 10")
        if rr["n_ad"] + rr["n_grazing"] > 10:
            fails.append("admissibility bookkeeping")
        if not np.isfinite(rr["detA2"]) or rr["detA2"] == 0:
            fails.append("det A2 zero/nonfinite")
        if rr["n_ad"] == 5:
            if np.any(rr["root_residuals"] > 1e-6):
                fails.append(f"large root residual at Om={Om} {model}")
        out = rs.secular(k, Om, model, m, {"phason": "free", "thermal": "isothermal"})
        if rr["n_ad"] == 5 and not np.isfinite(out["r"]):
            fails.append("residual non-finite with 5 admissible roots")
# 5. det A2 formula vs explicit
k = 2.3
A0, A1, A2 = mx.pencil(k, 1.0, "A", m)
det_formula = (m.C11 * m.K1 - m.R1 ** 2) * (m.C66 * m.K3 - m.R6 ** 2) * m.k11
if abs(np.linalg.det(A2) - det_formula) / det_formula > 1e-12:
    fails.append("det(A2) formula mismatch")

print("V0 code integrity:", "FAIL " + "; ".join(fails) if fails else "PASS")
sys.exit(1 if fails else 0)
