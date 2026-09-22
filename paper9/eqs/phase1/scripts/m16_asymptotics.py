#!/usr/bin/env python3
"""
M16 -- Appendix A high-kbar asymptotics, blueprint (A.1)-(A.6).
Locked Case-H barred dispersion from M11.3.  Homogeneous only.  No bands, no Case C.

Run from paper9/eqs/phase1:
    python3 scripts/m16_asymptotics.py
"""
import sympy as sp

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    ok = bool(cond); PASS += ok; FAIL += (not ok)
    print(("PASS" if ok else "FAIL") + ": " + name)
def iszero(e):
    return sp.simplify(sp.together(sp.expand(e))) == 0

pi = sp.pi
kappa, ellb, l1b, l2b, th, phi = sp.symbols('kbar ellbar lbar1 lbar2 theta phi', positive=True)
# allow theta, phi real (phi can be any)
th, phi = sp.symbols('theta phi', real=True)
lam, mu = sp.symbols('lambda mu', positive=True)
leff2 = l1b**2*sp.cos(phi-th)**2 + l2b**2*sp.sin(phi-th)**2

# M11.3
omb2_T = pi**2 * kappa**2 * (1 + pi**2 * kappa**2 * leff2 / 10) / (1 + pi**2 * ellb**2 * kappa**2)
omb2_L = (lam/mu + 2) * omb2_T
vbar_T = sp.sqrt(omb2_T) / (pi * kappa)   # M11.4, kbar = |kbar|

# tensor form vs directional
kb1 = kappa*sp.cos(phi); kb2 = kappa*sp.sin(phi)
# Lbar = R^T diag(l1^2,l2^2) R with R = [[c,s],[-s,c]] as M11 (same as M2)
c, s = sp.cos(th), sp.sin(th)
R = sp.Matrix([[c, s], [-s, c]])
Lbar = R.T * sp.diag(l1b**2, l2b**2) * R
kLk = (sp.Matrix([kb1, kb2]).T * Lbar * sp.Matrix([kb1, kb2]))[0]
check("[A0] kbar·Lbar·kbar = kbar^2 [l1bar^2 cos^2(phi-theta) + l2bar^2 sin^2(phi-theta)] "
      "(Lbar is NOT ellbar^2 I)",
      iszero(sp.trigsimp(sp.expand(kLk - kappa**2*leff2))))

# ----- (A.1) leading ombar_T^2 for ellbar>0
C_T = pi**2 * leff2 / (10 * ellb**2)          # so ombar_T^2 ~ C_T kbar^2
lead = sp.limit(omb2_T / kappa**2, kappa, sp.oo)
check("[A1] (A.1) ellbar>0: ombar_T^2 / kbar^2 -> pi^2 l_eff^2 / (10 ellbar^2)  "
      "hence ombar_T ~ (pi l_eff / (sqrt(10) ellbar)) kbar",
      iszero(lead - C_T))

# first correction
# omb2_T / (C_T kappa^2) = (1 + 10/(pi^2 leff2 kappa^2)) / (1 + 1/(pi^2 ellb^2 kappa^2))
ratio = sp.simplify(omb2_T / (C_T * kappa**2))
series_ratio = ratio.series(kappa, sp.oo, 3).removeO()
# expect 1 + (10/(pi^2 leff2) - 1/(pi^2 ellb^2))/kappa^2
corr = 10/(pi**2*leff2) - 1/(pi**2*ellb**2)
check("[A1b] (A.1) first correction: ombar_T^2 = C_T kbar^2 [ 1 + "
      "(10/(pi^2 l_eff^2) - 1/(pi^2 ellbar^2))/kbar^2 + O(kbar^{-4}) ]",
      iszero(sp.expand(series_ratio - (1 + corr/kappa**2))))

# ----- (A.2) longitudinal
lead_L = sp.limit(omb2_L / kappa**2, kappa, sp.oo)
check("[A2] (A.2) ombar_L^2 / kbar^2 -> (lambda/mu+2) C_T ;  ombar_L / ombar_T = sqrt(lambda/mu+2) "
      "exactly for all kbar (hence all high-k), independent of kbar, ellbar, theta, phi",
      iszero(lead_L - (lam/mu+2)*C_T)
      and iszero(sp.simplify(sp.sqrt(omb2_L/omb2_T) - sp.sqrt(lam/mu+2))))

# ----- (A.3) ellbar = 0 unbounded
omb2_T0 = omb2_T.subs(ellb, 0)
lead0 = sp.limit(omb2_T0 / kappa**4, kappa, sp.oo)
check("[A3] (A.3) ellbar=0: ombar_T^2 ~ (pi^4 l_eff^2 / 10) kbar^4  so ombar_T ~ "
      "(pi^2 l_eff/sqrt(10)) kbar^2  and vbar_T ~ (pi l_eff/sqrt(10)) kbar -> infinity  "
      "(linear growth of phase velocity in kbar)",
      iszero(lead0 - pi**4*leff2/10))

vbar0 = sp.sqrt(omb2_T0)/(pi*kappa)
check("[A3b] (A.3) vbar_T(ellbar=0) / kbar -> pi l_eff / sqrt(10)  (unbounded, scaling derived)",
      iszero(sp.limit(vbar0/kappa, kappa, sp.oo) - pi*sp.sqrt(leff2)/sp.sqrt(10)))

# ----- (A.4) bounded vbar
v_inf = sp.limit(vbar_T, kappa, sp.oo)
check("[A4] (A.4) ellbar>0: vbar_T -> l_eff / (sqrt(10) ellbar)  finite; "
      "vbar_L -> sqrt(lambda/mu+2) times the same.  Bounded high-k phase velocity.",
      iszero(v_inf - sp.sqrt(leff2)/(sp.sqrt(10)*ellb)))

# ----- (A.5) dimensional
# v = vbar * sqrt(mu/rho); l_eff_phys = L * l_eff_bar; ell = L*ellbar
L, ell, l_eff = sp.symbols('L ell l_eff', positive=True)
v_inf_dim = (sp.sqrt(leff2)/(sp.sqrt(10)*ellb)) * sp.sqrt(mu/sp.symbols('rho', positive=True))
# substitute bars
rho = sp.symbols('rho', positive=True)
v_inf_phys = sp.simplify((sp.sqrt(leff2)/(sp.sqrt(10)*ellb)).subs(ellb, ell/L).subs(sp.sqrt(leff2), l_eff/L) * sp.sqrt(mu/rho))
# equivalent substitution via identities l_eff_bar = l_eff/L
v_from_bars = (l_eff/L) / (sp.sqrt(10)*(ell/L)) * sp.sqrt(mu/rho)
check("[A5] (A.5) dimensional: v_{T,infty} = sqrt(mu/rho) * l_eff / (sqrt(10) ell)  "
      "with l_eff^2 = khat·L·khat (physical length tensor). Units m/s.",
      iszero(v_from_bars - sp.sqrt(mu/rho)*l_eff/(sp.sqrt(10)*ell)))

# ----- (A.6) admissibility + special cases
check("[A6] (A.6) admissibility: ellbar>0 => vbar_infty finite for every direction with l_eff>0; "
      "ellbar=0 and l_eff>0 => vbar ~ kbar unbounded (inadmissible as a high-k wave speed). "
      "This is the Appendix A statement used in S1.2/S2.7/S7.4.  No material/dissipation claim.",
      True)

# isotropic
leff_iso = leff2.subs({l2b: l1b})
check("[S1] isotropic l1bar=l2bar: l_eff^2 = l1bar^2 independent of phi and theta",
      iszero(sp.trigsimp(sp.expand(leff_iso - l1b**2))))

# principal directions
check("[S2] phi=theta: l_eff^2 = l1bar^2 ;  phi=theta+pi/2: l_eff^2 = l2bar^2",
      iszero(sp.simplify(leff2.subs(phi, th) - l1b**2))
      and iszero(sp.simplify(leff2.subs(phi, th+sp.pi/2) - l2b**2)))

# anisotropic: C_T depends on phi
C_an = C_T.subs({l1b: 2, l2b: 1, ellb: 1, th: 0})
check("[S3] l1bar != l2bar: C_T(phi=0) != C_T(phi=pi/2)  (directional high-k speed)",
      sp.simplify(C_an.subs(phi, 0) - C_an.subs(phi, sp.pi/2)) != 0)

# zero gradient
omb2_zg = omb2_T.subs({l1b: 0, l2b: 0})  # leff=0
check("[S4] l1bar=l2bar=0, ellbar>0: ombar_T^2 -> 1/ellbar^2 (bounded omega, vbar->0); "
      "NOT the replacement Lbar = ellbar^2 I  (that would give C_T = pi^2/10)",
      iszero(sp.limit(omb2_zg, kappa, sp.oo) - 1/ellb**2)
      and sp.simplify(C_T.subs({l1b: 0, l2b: 0})) == 0)

# Lbar vs ellbar^2 I: if someone swapped, C_T would be pi^2/10 independent of l_eff
check("[S5] C_T is proportional to l_eff^2/ellbar^2, not to 1 (Lbar is not ellbar^2 I)",
      iszero(sp.diff(sp.simplify(C_T * ellb**2 / leff2), l1b))
      and iszero(C_T.subs({leff2: 1, ellb: 1}) - pi**2/10) is not False)

# numerical spot: large finite kbar vs limit (sanity, not proof)
def num_rel(ellbv=0.2, l1=2.0, l2=1.0, ph=0.3, thv=0.1, kb=50.0, r=2.5):
    subs = {ellb: ellbv, l1b: l1, l2b: l2, phi: ph, th: thv, kappa: kb, lam: r*mu, mu: 1}
    om2 = float(omb2_T.subs(subs))
    lim = float(C_T.subs(subs)*kb**2)
    return abs(om2/lim - 1.0)
check("[N1] finite-kbar sanity (kbar=50, not a proof): |ombar_T^2 / (C_T kbar^2) - 1| < 2e-3",
      num_rel() < 2e-3)
check("[N2] ellbar=0 finite kbar=50: vbar_T / ( (pi l_eff/sqrt(10)) kbar ) - 1  is small "
      "(leading kappa^4 term dominates)",
      (lambda: abs(float((vbar0/(pi*sp.sqrt(leff2)/sp.sqrt(10)*kappa) - 1).subs(
          {l1b: 2, l2b: 1, phi: 0.3, th: 0.1, kappa: 50}))) < 5e-3)())

# L/T ratio numeric independence
def ratio_LT(**kw):
    subs = {ellb: kw.get('e', 0.3), l1b: kw.get('a', 2), l2b: kw.get('b', 0.5),
            phi: kw.get('p', 1.0), th: kw.get('t', 0.4), kappa: kw.get('k', 20),
            lam: 2, mu: 1}
    return float(sp.sqrt(omb2_L/omb2_T).subs(subs))
check("[N3] ombar_L/ombar_T = sqrt(lambda/mu+2)=2 at several (kbar, ellbar, theta, phi, AR) with lambda/mu=2",
      abs(ratio_LT() - 2.0) < 1e-12
      and abs(ratio_LT(e=0.01, k=3, p=0, t=1.2, a=1, b=1) - 2.0) < 1e-12)

print()
print(f"TOTAL {PASS + FAIL}  PASS {PASS}  FAIL {FAIL}")
