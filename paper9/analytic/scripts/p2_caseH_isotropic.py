#!/usr/bin/env python3
"""P2.1 isotropic Case-H: two-route check of M10.2 specialisation.

Does NOT evaluate PB2009 Eqs (22)-(28) (TV10 OPEN).
Does NOT evaluate LWZ2016 (TV11 OPEN).
"""
from __future__ import annotations

import sys

import sympy as sp

lam, mu, rho, l, ell, k = sp.symbols("lambda mu rho l ell k", positive=True)

om2_T = (mu / rho) * k**2 * (1 + l**2 * k**2 / 10) / (1 + ell**2 * k**2)
om2_L = ((lam + 2 * mu) / rho) * k**2 * (1 + l**2 * k**2 / 10) / (1 + ell**2 * k**2)

# long-wave: series in k
cT2 = sp.limit(om2_T / k**2, k, 0)
cL2 = sp.limit(om2_L / k**2, k, 0)
assert cT2 == mu / rho
assert cL2 == (lam + 2 * mu) / rho

# high-k ell>0
vTinf2 = sp.limit(om2_T / k**2, k, sp.oo)
assert sp.simplify(vTinf2 - (mu / rho) * (l**2 / (10 * ell**2))) == 0

# two-route numeric: exact rationals vs float
subs = {lam: 2, mu: 1, rho: 1, l: sp.Rational(1, 10), ell: sp.Rational(1, 20), k: 3}
sym_T = om2_T.subs(subs)
flt_T = float(om2_T.subs({lam: 2.0, mu: 1.0, rho: 1.0, l: 0.1, ell: 0.05, k: 3.0}))
rel = abs(float(sym_T) - flt_T) / abs(flt_T)
assert rel < 1e-14, rel

# anisotropic reduction: L = l^2 I recovers isotropic
L11, L22, kx, ky = sp.symbols("L11 L22 kx ky", real=True)
kdotLk = L11 * kx**2 + L22 * ky**2
om2_T_an = (mu / rho) * (kx**2 + ky**2) * (1 + kdotLk / 10) / (
    1 + ell**2 * (kx**2 + ky**2)
)
iso = om2_T_an.subs({L11: l**2, L22: l**2, kx: k, ky: 0})
assert sp.simplify(iso - om2_T) == 0

print("P2_CASEH_ISOTROPIC: 4 checks PASS")
print("  long-wave cT2, cL2 exact")
print("  high-k vTinf2 = (mu/rho) l^2/(10 ell^2)")
print("  sympy vs float rel", rel)
print("  anisotropic L=l^2 I -> isotropic")
print("TV10 OPEN; TV11 OPEN; no PB2009/LWZ evaluator")
sys.exit(0)
