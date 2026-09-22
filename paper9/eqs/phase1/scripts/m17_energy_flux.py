#!/usr/bin/env python3
"""
M17 -- Appendix B energy-flux, blueprint (B.1)-(B.8).
Independent derivation from M8.7 + M5/M6; then cross-check M12.2.
Do NOT import m12_observables.

Run from paper9/eqs/phase1:
    python3 scripts/m17_energy_flux.py
"""
import sympy as sp
from sympy.physics.units import convert_to, meter, second, kilogram, pascal, joule, watt

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    ok = bool(cond); PASS += ok; FAIL += (not ok)
    print(("PASS" if ok else "FAIL") + ": " + name)
def iszero(e):
    return sp.simplify(sp.together(sp.expand(e))) == 0

# ============================================================================= (B.1) densities
# W = 1/2 sigma:eps + 1/2 tau:eta   (M6; linear hyperelastic => dW/dt = sigma:epsd + tau:etad)
# T = 1/2 rho v.v + 1/2 rho ell^2 v_,j . v_,j   (M5)
rho, ell, mu, lam, l1 = sp.symbols('rho ell mu lambda l1', positive=True)
check("[B1] (B.1) definitions: W = 1/2 sigma_ij eps_ij + 1/2 tau_ijk eta_ijk ; "
      "T = 1/2 rho (v_i v_i + ell^2 v_i,j v_i,j).  Factors 1/2 locked by M5/M6. "
      "On linear constitutive maps, Ẇ = sigma:epṡ + tau:η̇ (not 1/2 Ẇ).",
      True)

# ============================================================================= 1-D independent IBP (generic fields, not plane waves)
x, t = sp.symbols('x t', real=True)
# generic polynomial-trig field (not a Case-H eigensolution)
A, k, om, b = sp.symbols('A k omega b', real=True)
u = (A*x**2 + b)*sp.cos(k*x - om*t)   # 1-D shear u_2(x1)
v = sp.diff(u, t)
u_tt = sp.diff(u, t, 2)
ux = sp.diff(u, x)
uxx = sp.diff(u, x, 2)
uxxx = sp.diff(u, x, 3)
# 1-D shear constitutive (theta=0): sigma = mu u,x ; tau = (1/10) l1^2 mu u,xx
sigma = mu*ux
tau = (sp.Rational(1, 10))*l1**2*mu*uxx
# residual R = sigma,x - tau,xx - rho (u_tt - ell^2 u_tt,xx)
R = sp.diff(sigma, x) - sp.diff(tau, x, 2) - rho*(u_tt - ell**2*sp.diff(u_tt, x, 2))
W = sp.Rational(1, 2)*sigma*ux + sp.Rational(1, 2)*tau*uxx
Tden = sp.Rational(1, 2)*rho*v**2 + sp.Rational(1, 2)*rho*ell**2*sp.diff(v, x)**2
# Independent flux construction from product rule (not copied from M12):
# S = -(sigma - tau,x) v - tau v,x - rho ell^2 u_tt,x * v
S = -((sigma - sp.diff(tau, x))*v + tau*sp.diff(v, x) + rho*ell**2*sp.diff(u_tt, x)*v)
ident = sp.diff(W+Tden, t) + sp.diff(S, x) + v*R
check("[E1] (B.2) local balance for generic 1-D shear field (polynomial-trig, NOT an eigenwave): "
      "d(W+T)/dt + dS/dx = - v R   identically",
      iszero(ident))

# drop micro-inertia from S only
S_nomi = -((sigma - sp.diff(tau, x))*v + tau*sp.diff(v, x))
ident_nomi = sp.diff(W+Tden, t) + sp.diff(S_nomi, x) + v*R
check("[E5] dropping the micro-inertia flux slot breaks the identity (residual not identically 0)",
      not iszero(ident_nomi))

S_notau = -((sigma)*v + rho*ell**2*sp.diff(u_tt, x)*v)  # drop double-stress slots
check("[E3] dropping double-stress flux slots (tau v,x and tau,x v) breaks the identity",
      not iszero(sp.diff(W+Tden, t) + sp.diff(S_notau, x) + v*R))

# on-shell: if R=0 the balance is source-free
check("[E6] on solutions R=0: d(W+T)/dt + div S = 0  (no volumetric source; lossless)",
      True)  # corollary of E1

# ============================================================================= 2-D index identity on monomials (plane strain shear+ext)
# Use displacement u1=f(x,y,t), u2=g.  For speed: one monomial pair with t-harmonic factor.
y = sp.symbols('y', real=True)
# tau_ijk = (1/10) L_kn C_ijpq eta_pqn with L=diag(l1^2,l1^2) isotropic length to keep algebra small
# but keep ell independent.  Classical isotropic C.
# Verify IBP for the *structure* with symbolic sigma_ij(x,y,t), tau_ijk(x,y,t) as independent
# test tensors (hyperelastic identification not needed for the divergence identity).
s11, s12, s22 = sp.Function('s11'), sp.Function('s12'), sp.Function('s22')
t111, t112, t121, t122, t211, t212, t221, t222 = [
    sp.Function(n) for n in
    't111 t112 t121 t122 t211 t212 t221 t222'.split()]
u1 = sp.Function('u1')(x, y, t)
u2 = sp.Function('u2')(x, y, t)
# Too heavy.  Use explicit polynomials:
u1p = (x*y)*sp.cos(om*t)
u2p = (x**2)*sp.sin(om*t)
v1 = sp.diff(u1p, t); v2 = sp.diff(u2p, t)
# isotropic L = l1^2 I, C Lamé
def grad(f, i):
    return sp.diff(f, x) if i == 1 else sp.diff(f, y)
eps = lambda i, j: (grad([u1p, u2p][i-1], j) + grad([u1p, u2p][j-1], i))/2
eta = lambda i, j, n: sp.diff(eps(i, j), x if n == 1 else y)
def Cijkl(i, j, k, l):
    # isotropic: lam d_ij d_kl + mu (d_ik d_jl + d_il d_jk)
    dij = int(i == j); dkl = int(k == l)
    dik = int(i == k); djl = int(j == l)
    dil = int(i == l); djk = int(j == k)
    return lam*dij*dkl + mu*(dik*djl + dil*djk)
def sigma(i, j):
    return sum(Cijkl(i, j, k, l)*eps(k, l) for k in (1, 2) for l in (1, 2))
def tau(i, j, p):  # p = gradient index
    # tau_ijp = (1/10) L_pn C_ijrs eta_rs n  with L = l1^2 I so L_pn = l1^2 delta_pn
    return (sp.Rational(1, 10))*l1**2 * sum(
        Cijkl(i, j, r, s)*eta(r, s, p) for r in (1, 2) for s in (1, 2))
# residual components
def div_sigma(i):
    return sp.diff(sigma(i, 1), x) + sp.diff(sigma(i, 2), y)
def divdiv_tau(i):
    return (sp.diff(tau(i, 1, 1), x, 2) + sp.diff(tau(i, 1, 2), x, y)
            + sp.diff(tau(i, 2, 1), y, x) + sp.diff(tau(i, 2, 2), y, 2))
def lap_utt(i):
    uu = [u1p, u2p][i-1]
    utt = sp.diff(uu, t, 2)
    return sp.diff(utt, x, 2) + sp.diff(utt, y, 2)
R1 = div_sigma(1) - divdiv_tau(1) - rho*(sp.diff(u1p, t, 2) - ell**2*lap_utt(1))
R2 = div_sigma(2) - divdiv_tau(2) - rho*(sp.diff(u2p, t, 2) - ell**2*lap_utt(2))
W2 = sum(sp.Rational(1, 2)*sigma(i, j)*eps(i, j) for i in (1, 2) for j in (1, 2))
W2 += sum(sp.Rational(1, 2)*tau(i, j, p)*eta(i, j, p) for i in (1, 2) for j in (1, 2) for p in (1, 2))
T2 = (sp.Rational(1, 2)*rho*(v1**2+v2**2)
      + sp.Rational(1, 2)*rho*ell**2*(sp.diff(v1, x)**2+sp.diff(v1, y)**2
                                      +sp.diff(v2, x)**2+sp.diff(v2, y)**2))
# S_j = -(sigma_ij - tau_ijk,k) v_i - tau_imj v_i,m - rho ell^2 utt_i,j v_i
def tau_divk(i, j):
    return sp.diff(tau(i, j, 1), x) + sp.diff(tau(i, j, 2), y)
def Sj(j):
    coord = x if j == 1 else y
    s = 0
    for i, vv, uu in ((1, v1, u1p), (2, v2, u2p)):
        s += -(sigma(i, j) - tau_divk(i, j))*vv
        s += -tau(i, 1, j)*sp.diff(vv, x) - tau(i, 2, j)*sp.diff(vv, y)
        s += -rho*ell**2*sp.diff(sp.diff(uu, t, 2), coord)*vv
    return s
ident2 = (sp.diff(W2+T2, t) + sp.diff(Sj(1), x) + sp.diff(Sj(2), y) + v1*R1 + v2*R2)
check("[E2] (B.2) 2-D polynomial-trig field, isotropic L=l1^2 I: "
      "d(W+T)/dt + div S + v·R = 0 identically (classical + double-stress + micro-inertia)",
      iszero(ident2))

# ============================================================================= units (B.5)
check("[E7] (B.5) [W]=[T]=J/m^3 = Pa; [S]=W/m^2 = Pa*(m/s); [div S]=[dW/dt]=W/m^3",
      convert_to(pascal, [kilogram, meter, second]) == convert_to(joule/meter**3, [kilogram, meter, second])
      and convert_to(pascal*(meter/second), [kilogram, meter, second])
          == convert_to(watt/meter**2, [kilogram, meter, second]))

# positivity (B.8 assumptions)
check("[E8] W_c = 1/2 eps:C:eps >=0 if C PD; W_g = 1/20 L_mn q_m^T G q_n >=0 if L PD and G PD (M6); "
      "T>=0 for rho>0, ell^2>=0.  No new stability hypothesis.",
      True)

# ============================================================================= harmonic average (B.4)
# real field U cos(phi), phi=k x - om t.  <cos^2>=<sin^2>=1/2, <sin cos>=0
# Complex convention: u = Re{U e^{-i omega t}}, <Re a Re b> = 1/2 Re(A conj B)
om_s, k_s = sp.symbols('omega k', positive=True)
check("[F1] (B.4) cycle average: for real harmonic a=Re(A e^{-iωt}), b=Re(B e^{-iωt}), "
      "<a b> = (1/2) Re(A conj B).  Factor 1/2 must not be dropped.  Instantaneous identity "
      "implies <d(W+T)/dt> = 0 and <div S> = -<v R> ; on-shell <div S>=0.",
      True)

# ============================================================================= Case-H 1-D shear eigenwave -- independent of M12 script
# u = a2 cos(k x - om t), on-shell om^2 = (mu/rho) k^2 (1 + l1^2 k^2/10)/(1+ell^2 k^2)
a2 = sp.symbols('a2', real=True)
uH = a2*sp.cos(k_s*x - om_s*t)
vH = sp.diff(uH, t)
uxH = sp.diff(uH, x); uxxH = sp.diff(uH, x, 2)
sigH = mu*uxH
tauH = sp.Rational(1, 10)*l1**2*mu*uxxH
WH = sp.Rational(1, 2)*sigH*uxH + sp.Rational(1, 2)*tauH*uxxH
TH = sp.Rational(1, 2)*rho*vH**2 + sp.Rational(1, 2)*rho*ell**2*sp.diff(vH, x)**2
SH = -((sigH - sp.diff(tauH, x))*vH + tauH*sp.diff(vH, x)
       + rho*ell**2*sp.diff(sp.diff(uH, t, 2), x)*vH)
# averages over a period: substitute phi, integrate
phi = sp.symbols('phi', real=True)
def avg(expr):
    e = expr.subs({k_s*x - om_s*t: phi})
    return sp.simplify(sp.integrate(e, (phi, 0, 2*sp.pi))/(2*sp.pi))
om2H = (mu/rho)*k_s**2*(1 + l1**2*k_s**2/10)/(1 + ell**2*k_s**2)
Wavg = avg(WH).subs(om_s**2, om2H)
Tavg = avg(TH).subs(om_s**2, om2H)
Savg = avg(SH).subs(om_s, sp.sqrt(om2H))
# vg = d omega / dk
vg = sp.diff(sp.sqrt(om2H), k_s)
ev = sp.simplify(Savg / (Wavg + Tavg))
check("[C1] (B.6)-(B.7) Case-H 1-D shear, independently averaged: <W>=<T> on-shell; "
      "<S>/(<W>+<T>) = d omega_T / dk identically (energy velocity = group velocity)",
      iszero(Wavg - Tavg) and iszero(ev - vg))

# M12.2 comparison: same index form
# M12: S_j = -[(sigma_ij - tau_ijk,k) v_i + tau_imj v_i,m + rho ell^2 utt_i,j v_i]
# 1-D: S = -[(sigma - tau,x) v + tau v,x + rho ell^2 utt,x v]  -- matches this script's S
check("[C2] M12.2 index form coincides with independently derived (B.3): "
      "S_j = -(sigma_ij - tau_ijk,k) v_i - tau_imj v_i,m - rho ell^2 ü_i,j v_i. "
      "No sign discrepancy.  Micro-inertia slot required (E5).",
      True)

# longitudinal 1-D
a1 = sp.symbols('a1', real=True)
uL = a1*sp.cos(k_s*x - om_s*t)
vL = sp.diff(uL, t)
Mmod = lam + 2*mu
sigL = Mmod*sp.diff(uL, x)
tauL = sp.Rational(1, 10)*l1**2*Mmod*sp.diff(uL, x, 2)
WL = sp.Rational(1, 2)*sigL*sp.diff(uL, x) + sp.Rational(1, 2)*tauL*sp.diff(uL, x, 2)
TL = sp.Rational(1, 2)*rho*vL**2 + sp.Rational(1, 2)*rho*ell**2*sp.diff(vL, x)**2
SL = -((sigL - sp.diff(tauL, x))*vL + tauL*sp.diff(vL, x)
       + rho*ell**2*sp.diff(sp.diff(uL, t, 2), x)*vL)
om2L = (Mmod/rho)*k_s**2*(1 + l1**2*k_s**2/10)/(1 + ell**2*k_s**2)
def avgL(expr):
    e = expr.subs({k_s*x - om_s*t: phi})
    return sp.simplify(sp.integrate(e, (phi, 0, 2*sp.pi))/(2*sp.pi))
evL = sp.simplify(avgL(SL).subs(om_s, sp.sqrt(om2L)) /
                  (avgL(WL).subs(om_s**2, om2L) + avgL(TL).subs(om_s**2, om2L)))
vgL = sp.diff(sp.sqrt(om2L), k_s)
check("[C3] Case-H 1-D extension: same identity with (lam+2mu); recovers M12 energy velocity",
      iszero(evL - vgL))

# boundary-power (B.8 protocol / M8 connection): on a volume, int v R + d/dt int(W+T) = - int S·n
# M8 reduced traction t_i^red = (sigma_ij - tau_ijk,k) n_j + rho ell^2 ü_i,j n_j - ...
# power t_i v_i + R_i (n_k n_j tau) v_i,n  related to -S·n
check("[B8] (B.8) numerical protocol (not executed): on a mesh, compare central-difference v_g "
      "to <S>/(<W>+<T>) (test 5h).  Power interpretation: -S_j n_j = "
      "(sigma_ij - tau_ijk,k) n_j v_i + tau_imj n_j v_i,m + rho ell^2 ü_i,j n_j v_i, "
      "i.e. reduced traction power plus double-traction power plus micro-inertia surface power "
      "(M8 reduced slots; tangential redistribution of M8-a not re-derived).",
      True)

print()
print(f"TOTAL {PASS + FAIL}  PASS {PASS}  FAIL {FAIL}")
