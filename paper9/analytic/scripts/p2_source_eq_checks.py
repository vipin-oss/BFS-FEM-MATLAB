#!/usr/bin/env python3
"""Lightweight checks of transcribed PB2009 (20)-(28) and LWZ (14.1)/(20.2)/(10).

Does not implement Layer-3 production or TM numerics.
"""
from __future__ import annotations

import sys

import sympy as sp

g, h, k, Cp, Cs, E, q = sp.symbols("g h k C_p C_s E q", positive=True)
omega, Vp = sp.symbols("omega V_p", positive=True)

# PB (20) and (22) consistency: Vp = omega/k
om2_p = Cp**2 * k**2 * (1 + g**2 * k**2) / (1 + h**2 * k**2)
Vp_22 = Cp * sp.sqrt((1 + g**2 * k**2) / (1 + h**2 * k**2))
assert sp.simplify(sp.sqrt(om2_p) / k - Vp_22) == 0

# g = h => V = C
assert sp.simplify(Vp_22.subs(g, h) - Cp) == 0

# bar (28) same ratio as (22) with Vc=sqrt(E/q)
Vc = sp.sqrt(E / q)
Vgh = Vc * sp.sqrt((1 + g**2 * k**2) / (1 + h**2 * k**2))
assert sp.simplify(Vgh / Vc - Vp_22 / Cp) == 0
assert sp.simplify(sp.limit(Vgh / Vc, k, sp.oo) - g / h) == 0

# h=0: V ~ C g k -> oo
assert sp.limit(Vp_22.subs(h, 0), k, sp.oo) == sp.oo

# g=0: V -> 0 as k->oo (bounded, actually -> 0)
assert sp.limit(Vp_22.subs(g, 0), k, sp.oo) == 0

# Case-H isotropic vs PB (21) after identification
mu, rho, l, ell = sp.symbols("mu rho l ell", positive=True)
om2_T_ours = (mu / rho) * k**2 * (1 + l**2 * k**2 / 10) / (1 + ell**2 * k**2)
om2_T_pb = (mu / rho) * k**2 * (1 + g**2 * k**2) / (1 + h**2 * k**2)
id_map = {g**2: l**2 / 10, h**2: ell**2}
# substitute symbols g,h not g**2 keys
diff = sp.simplify(om2_T_ours - om2_T_pb.subs({g: l / sp.sqrt(10), h: ell}))
assert diff == 0

# Without 1/10 the match fails
diff_bad = sp.simplify(om2_T_ours - om2_T_pb.subs({g: l, h: ell}))
assert diff_bad != 0

# LWZ (20.2): c and d^2/3 vs PB
c, d = sp.symbols("c d", positive=True)
om2_lwz = (mu / rho) * k**2 * (1 + c * k**2) / (1 + (d**2 / 3) * k**2)
diff_lwz_pb = sp.simplify(om2_lwz.subs({c: g**2, d**2: 3 * h**2}) - om2_T_pb)
# d**2 key may not work; use d = h*sqrt(3)
diff_lwz_pb = sp.simplify(om2_lwz.subs({c: g**2, d: h * sp.sqrt(3)}) - om2_T_pb)
assert diff_lwz_pb == 0

# LWZ inertia d^2/3 is NOT ell^2 unless d^2 = 3 ell^2
diff_lwz_ours = sp.simplify(
    om2_lwz.subs({c: l**2 / 10, d: ell}) - om2_T_ours
)
assert diff_lwz_ours != 0

print("P2_SOURCE_EQ_CHECKS: 8 checks PASS")
print("  PB (20)<->(22); g=h no dispersion; (28) ratio; k->oo g/h")
print("  h=0 unbounded; g=0 V->0")
print("  Case-H isotropic == PB (21) IFF g=l/sqrt(10) and h=ell")
print("  g=l (no 1/10) does NOT match")
print("  LWZ (20.2)==PB IFF c=g^2 and d^2=3 h^2")
print("  LWZ d!=ell (missing 1/3) does NOT match Case-H")
sys.exit(0)
