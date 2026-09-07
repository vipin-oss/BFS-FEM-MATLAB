"""V4 - formulation identities as symbolic regression tests
(frozen blueprint Validation V3; complements the numerical V0 checks).

Asserted symbolically (sympy, exact rational constants from the frozen
starred table):
  1. det M is degree 10 in p for all three models;
  2. Omega-degrees of det M are 10 (A), 8 (B), 10 (C);
  3. det M(Omega=0) = const * (k^2 + p^2)^5 (quintuple static factor);
  4. det A2 = (C11 K1 - R1^2)(C66 K3 - R6^2) k11 > 0 (symbolic identity);
  5. five admissible depth roots at a subsonic sample point (numerical,
     all models).
"""
import os, sys
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

k, p, Om = sp.symbols("k p Omega", real=True)
I = sp.I

# frozen starred constants as exact rationals
C11, C12, C66 = sp.Integer(1), sp.Rational(1, 2), sp.Rational(1, 4)
K1, K2, K3, K6 = sp.Rational(1, 4), sp.Rational(1, 10), sp.Rational(1, 10), sp.Rational(1, 20)
R1, R2, R6 = sp.Rational(1, 20), sp.Rational(1, 40), sp.Rational(1, 80)
rho, rho_w = sp.Integer(1), sp.Integer(1)
k11 = sp.Rational(26077, 10**7)
tau0 = sp.Rational(43462, 10**7)
T0b1 = sp.Rational(23047, 10**7)
beta1, c_e = sp.Integer(1), sp.Integer(1)
Dw = sp.Rational(22935, 2)

Phi = I * Om + tau0 * Om**2
Lam = {"A": -rho_w * Om**2,
       "B": -I * Om * Dw,
       "C": -rho_w * Om**2 - I * Om * Dw}

def pencil_sym(model):
    A0 = sp.zeros(5, 5); A1 = sp.zeros(5, 5); A2 = sp.zeros(5, 5)
    A2[0, 0] = -C66; A2[1, 1] = -C11
    A2[0, 2] = A2[2, 0] = -R6
    A2[1, 3] = A2[3, 1] = -R1
    A2[2, 2] = -K3;  A2[3, 3] = -K1
    A2[4, 4] = k11
    A1[0, 1] = A1[1, 0] = -(C12 + C66) * k
    A1[0, 3] = A1[3, 0] = -(R2 + R6) * k
    A1[1, 2] = A1[2, 1] = -(R2 + R6) * k
    A1[2, 3] = A1[3, 2] = -(K2 + K6) * k
    A1[1, 4] = -I * beta1
    A1[4, 1] = -I * T0b1 * Phi
    A0[0, 0] = -C11 * k**2 + rho * Om**2
    A0[1, 1] = -C66 * k**2 + rho * Om**2
    A0[0, 2] = A0[2, 0] = -R1 * k**2
    A0[1, 3] = A0[3, 1] = -R6 * k**2
    A0[2, 2] = -K1 * k**2 - Lam[model]
    A0[3, 3] = -K3 * k**2 - Lam[model]
    A0[0, 4] = -I * beta1 * k
    A0[4, 0] = -I * T0b1 * Phi * k
    A0[4, 4] = k11 * k**2 - c_e * Phi
    return A0, A1, A2

fails = []

# ---- 4. det A2 symbolic identity (independent of k, p, Omega) ----------
A0, A1, A2 = pencil_sym("C")
detA2 = sp.simplify(A2.det())
want = (C11 * K1 - R1**2) * (C66 * K3 - R6**2) * k11
if sp.simplify(detA2 - want) != 0:
    fails.append(f"det A2 symbolic identity mismatch: {detA2} != {want}")
if want <= 0:
    fails.append("det A2 <= 0")

expected_p_degree = {"A": 10, "B": 10, "C": 10}
expected_om_degree = {"A": 10, "B": 8, "C": 10}

for model in ("A", "B", "C"):
    A0, A1, A2 = pencil_sym(model)
    M = A0 + p * A1 + p**2 * A2
    detM = sp.expand(M.det())
    dp = sp.degree(detM, p)
    dom = sp.degree(detM, Om)
    print(f"model {model}: p-degree {dp} (expect {expected_p_degree[model]}), "
          f"Omega-degree {dom} (expect {expected_om_degree[model]})", flush=True)
    if dp != expected_p_degree[model]:
        fails.append(f"{model}: p-degree {dp} != {expected_p_degree[model]}")
    if dom != expected_om_degree[model]:
        fails.append(f"{model}: Omega-degree {dom} != {expected_om_degree[model]}")
    # det M(Omega=0) = const * (k^2+p^2)^5
    det0 = sp.expand(detM.subs(Om, 0))
    q = sp.cancel(det0 / (k**2 + p**2)**5)
    if q.free_symbols & {k, p}:
        fails.append(f"{model}: det M(Omega=0)/(k^2+p^2)^5 not constant: {q}")
    else:
        print(f"   det M(Omega=0) = {q} * (k^2+p^2)^5", flush=True)

# ---- 5. five admissible roots in the surface-branch region -------------
# "Subsonic" means below every real characteristic speed of the model:
# A is undamped-hyperbolic in the phason sector, so it needs
# V < sqrt(K3*) = 0.3162 (below 0.5 the second phason polarisation
# genuinely propagates); B/C have diffusive phasons, so V < 0.5 suffices.
import numpy as np
from solver.material import Material
from solver import roots as rt
m = Material()
samples = {"A": (2.0, 0.60), "B": (2.0, 0.90), "C": (2.0, 0.90)}
for model in ("A", "B", "C"):
    kk, omm = samples[model]
    rr = rt.depth_roots(kk, omm, model, m)
    if rr["n_ad"] != 5 or rr["n_grazing"] != 0:
        fails.append(f"{model}: sample (k={kk},Om={omm}) n_ad={rr['n_ad']} "
                     f"n_grazing={rr['n_grazing']} (expect 5/0)")
    if np.max(rr["root_residuals"]) > 1e-8:
        fails.append(f"{model}: root residual {np.max(rr['root_residuals']):.2e}")

if fails:
    print("\nV4 symbolic identities: FAIL -- STOP")
    for x in fails:
        print("   " + x)
    sys.exit(1)
print("\nV4 symbolic identities: PASS")
