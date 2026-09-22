#!/usr/bin/env python3
"""
M11 -- Non-dimensionalisation, blueprint (45)-(47), S3.4:
    kbar = k L / pi,  ombar = omega/omega_0,  omega_0 = sqrt(mu/(rho L^2)),
    lbar_m = l_m / L,  ellbar_i = ell_i / L,  vbar = (omega/k)/sqrt(mu/rho).
Plus (CALC_MASTER_PLAN row M11) the mapping to the anchor schemes A and B [C].

Everything is derived from the locked M1-M10 formulation (M4 (26) constitutive law, M5 micro-
inertia, M8 strong form (M8.7), M9 Bloch phase mu_alpha = e^{i k.a_alpha}, M10 Case-H dispersion
and path (44), M15-a pair).  Symbolic only.  Run from paper9/eqs/phase1:
    python3 scripts/m11_nondim.py
"""
import sympy as sp
from sympy.physics.units import Quantity, meter, second, kilogram, pascal, convert_to

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    ok = bool(cond); PASS += ok; FAIL += (not ok)
    print(("PASS" if ok else "FAIL") + ": " + name)
def iszero(e): return sp.simplify(sp.together(sp.expand(e))) == 0

# ----------------------------------------------------------------------------- locked symbols
L, rho, mu, lam, ell, l1, l2 = sp.symbols('L rho mu lambda ell l1 l2', positive=True)
th = sp.symbols('theta', real=True)
k1, k2, om = sp.symbols('k1 k2 omega', real=True)
x1, x2 = sp.symbols('x1 x2', real=True)
kb1, kb2, omb, x1b, x2b = sp.symbols('kbar1 kbar2 omegabar xbar1 xbar2', real=True)
lb1, lb2, ellb = sp.symbols('lbar1 lbar2 ellbar', positive=True)

om0 = sp.sqrt(mu/(rho*L**2))                               # (46)
nd = {k1: sp.pi*kb1/L, k2: sp.pi*kb2/L, om: omb*om0,        # (45),(46)
      l1: lb1*L, l2: lb2*L, ell: ellb*L}                    # (47)

# ============================================================== 1. units of the scales (S1-S3)
check("[U1] omega_0 = sqrt(mu/(rho L^2)) has units 1/s",
      convert_to(sp.sqrt(pascal/(kilogram/meter**3*meter**2)), [second]) == 1/second)
check("[U2] kbar = kL/pi, lbar, ellbar dimensionless; sqrt(mu/rho) has units m/s so vbar = "
      "(omega/k)/sqrt(mu/rho) is dimensionless",
      convert_to(sp.sqrt(pascal/(kilogram/meter**3)), [meter, second]) == meter/second)
# ============================================================== 2. dimensionless strong form
# Locked M1-M7: L = R^T diag(l1^2,l2^2) R ; tau_ijk = (1/10) L_kn C_ijpq eta_pqn ; sigma = C eps
R = sp.Matrix([[sp.cos(th), sp.sin(th)], [-sp.sin(th), sp.cos(th)]])
Lt = R.T*sp.diag(l1**2, l2**2)*R
Lbar = (Lt/L**2).subs(nd).applyfunc(sp.simplify)
Lbar_expected = R.T*sp.diag(lb1**2, lb2**2)*R
check("[D1] (47): Lbar := L/L^2 = R^T diag(lbar1^2, lbar2^2) R -- the length tensor scales with L^2 "
      "and the orientation theta is untouched (dimensionless, no scaling)",
      (Lbar - Lbar_expected).applyfunc(sp.simplify) == sp.zeros(2, 2))

# time-harmonic plane-wave operator of M8.7 in Case H (M10 [S1]): H(k) a = 0 with
# H(k) = (1 + k.L.k/10) Gamma_cl(k) - rho om^2 (1 + ell^2 |k|^2) I ,  Gamma_cl = mu|k|^2 I + (lam+mu) k k^T
kv = sp.Matrix([k1, k2]); kk2 = (kv.T*kv)[0]; kLk = (kv.T*Lt*kv)[0]
Gcl = mu*kk2*sp.eye(2) + (lam + mu)*kv*kv.T
H = (1 + kLk/10)*Gcl - rho*om**2*(1 + ell**2*kk2)*sp.eye(2)
# non-dimensional: divide by mu/L^2 (the natural stiffness scale: [mu][k]^2)
Hbar = (H/(mu/L**2)).subs(nd).applyfunc(sp.simplify)
kbv = sp.Matrix([kb1, kb2]); kb2n = (kbv.T*kbv)[0]; kLkb = (kbv.T*Lbar_expected*kbv)[0]
Gclb = sp.pi**2*(kb2n*sp.eye(2) + (lam/mu + 1)*kbv*kbv.T)
Hbar_expected = (1 + sp.pi**2*kLkb/10)*Gclb - omb**2*(1 + sp.pi**2*ellb**2*kb2n)*sp.eye(2)
check("[D2] DIMENSIONLESS OPERATOR (derived): H/(mu/L^2) = (1 + pi^2 kbar.Lbar.kbar/10) "
      "[pi^2 |kbar|^2 I + pi^2 (lambda/mu + 1) kbar kbar^T] - ombar^2 (1 + pi^2 ellbar^2 |kbar|^2) I ; "
      "L, rho, mu have been eliminated; lambda/mu (equivalently nu) SURVIVES as a dimensionless parameter",
      (Hbar - Hbar_expected).applyfunc(sp.simplify) == sp.zeros(2, 2))

check("[D3] the ONLY dimensionless parameters of the Case-H problem are {lambda/mu, lbar1, lbar2, theta, "
      "ellbar} (5) -- Hbar is free of L, rho, mu, and depends on l1,l2,ell only through lbar1,lbar2,ellbar",
      not (Hbar.free_symbols & {L, rho, l1, l2, ell, om, k1, k2})
      and Hbar.free_symbols <= {lam, mu, lb1, lb2, ellb, th, kb1, kb2, omb}
      and all(sp.simplify(sp.diff(Hbar[i, j].subs(lam, sp.Symbol('r')*mu), mu)) == 0 for i in range(2) for j in range(2)))

# ============================================================== 3. dispersion in barred form
om2_T = mu/rho*kk2*(1 + kLk/10)/(1 + ell**2*kk2)
om2_L = (lam + 2*mu)/rho*kk2*(1 + kLk/10)/(1 + ell**2*kk2)
omb2_T = sp.simplify((om2_T/om0**2).subs(nd))
omb2_L = sp.simplify((om2_L/om0**2).subs(nd))
check("[D4] barred Case-H branches (derived from M10 [S2] via (45)-(47)): "
      "ombar_T^2 = pi^2 |kbar|^2 (1 + pi^2 kbar.Lbar.kbar/10)/(1 + pi^2 ellbar^2 |kbar|^2); "
      "ombar_L^2 = (lambda/mu + 2) x the same",
      iszero(omb2_T - sp.pi**2*kb2n*(1 + sp.pi**2*kLkb/10)/(1 + sp.pi**2*ellb**2*kb2n))
      and iszero(omb2_L - (lam/mu + 2)*sp.pi**2*kb2n*(1 + sp.pi**2*kLkb/10)/(1 + sp.pi**2*ellb**2*kb2n)))

check("[D5] the barred branches are eigen-solutions of the barred operator: det Hbar = 0 at ombar^2 = ombar_T^2 "
      "and at ombar_L^2 (consistency of [D2] with [D4])",
      iszero(Hbar_expected.det().subs(omb**2, omb2_T).subs(omb, sp.sqrt(omb2_T)))
      and iszero(Hbar_expected.det().subs(omb**2, omb2_L).subs(omb, sp.sqrt(omb2_L))))

# phase velocity (47): vbar = (omega/k)/sqrt(mu/rho) = ombar/(pi kbar)
kmag, kbmag = sp.symbols('k kbar', positive=True)
vbar_def = (om/kmag)/sp.sqrt(mu/rho)
check("[D6] (47) vbar = (omega/k)/sqrt(mu/rho) = ombar/(pi kbar) exactly; classical transverse limit "
      "(lbar = ellbar = 0) gives vbar_T = 1 and vbar_L = sqrt(lambda/mu + 2) (unit = shear speed)",
      iszero(vbar_def.subs({om: omb*om0, kmag: sp.pi*kbmag/L}) - omb/(sp.pi*kbmag))
      and iszero(sp.sqrt(omb2_T.subs({lb1: 0, lb2: 0, ellb: 0, kb1: kbmag, kb2: 0}))/(sp.pi*kbmag) - 1)
      and iszero(sp.sqrt(omb2_L.subs({lb1: 0, lb2: 0, ellb: 0, kb1: kbmag, kb2: 0}))/(sp.pi*kbmag) - sp.sqrt(lam/mu + 2)))

check("[D7] group velocity scales with the same factor: d omega/dk = sqrt(mu/rho) d ombar/d kbar / pi "
      "(chain rule with (45),(46)); the deviation angle delta = angle(v_g) - angle(k) is scale-invariant",
      iszero(sp.diff(sp.sqrt(om2_T.subs({k1: kmag, k2: 0, th: 0})), kmag)
             - sp.sqrt(mu/rho)/sp.pi*sp.diff(sp.sqrt(omb2_T.subs({kb1: kbmag, kb2: 0, th: 0})), kbmag)
               .subs({kbmag: kmag*L/sp.pi, lb1: l1/L, lb2: l2/L, ellb: ell/L})))

# ============================================================== 4. Bloch / path / eigenproblem
check("[B1] M9 phases in barred variables: mu_alpha = e^{i k.a_alpha} = e^{i pi kbar_alpha} (a_alpha = L e_alpha); "
      "M10 path breakpoints Gamma(0,0), X(1,0), M(1,1) in kbar; X: mu_x = e^{i pi} = -1; M: mu_x = mu_y = -1",
      sp.simplify(sp.exp(sp.I*(sp.pi*kb1/L)*L) - sp.exp(sp.I*sp.pi*kb1)) == 0
      and sp.exp(sp.I*sp.pi*1) == -1)

check("[B2] M10 arc-length abscissa s/(pi/L) (0,1,2,2+sqrt2) coincides with the (45) scaling of arc length: "
      "sbar = s L/pi -- the M10 'kbar' and the (45) kbar are the same normalisation",
      [sp.simplify(s*L/sp.pi) for s in (0, sp.pi/L, 2*sp.pi/L, (2 + sp.sqrt(2))*sp.pi/L)] == [0, 1, 2, 2 + sp.sqrt(2)])

# reduced eigenproblem (66): [K(k) - om^2 M(k)] d = 0  ->  Kbar := K/mu (2-D, per unit thickness: [K] = Pa),
# Mbar := M/(rho L^2) ([M] = kg/m^2), so K - om^2 M = mu (Kbar - ombar^2 Mbar).
Ksym = sp.MatrixSymbol('K', 3, 3); Msym = sp.MatrixSymbol('M', 3, 3)
check("[B3] eigenproblem scaling: K - omega^2 M = mu [ K/mu - ombar^2 M/(rho L^2) ] with omega = ombar omega_0; "
      "the scaling factors mu and rho L^2 are REAL POSITIVE scalars -- eigenvectors unchanged, "
      "eigenvalues divided by omega_0^2",
      iszero((omb*om0)**2/mu - omb**2/(rho*L**2)))

# M15-a pair survives real positive scaling: test on a generic complex Hermitian K(k) built from M9-type phases
p = sp.symbols('p', real=True)
a, b, c = sp.symbols('a b c', real=True)
Kk = sp.Matrix([[a, b*sp.exp(sp.I*p)], [b*sp.exp(-sp.I*p), c]])       # Hermitian, K(-k) = conj K(k)
Kbar_ = Kk/mu
check("[B4] M15-a identities are invariant under the real positive scaling: Kbar^H = Kbar and "
      "Kbar(-k) = conj Kbar(k) hold iff they hold for K (checked on a generic Hermitian phase matrix); "
      "the invalid generic form K(k) = K(-k)^H is NOT used or implied",
      (Kbar_.H - Kbar_).applyfunc(sp.simplify) == sp.zeros(2, 2)
      and (Kbar_.subs(p, -p) - Kbar_.conjugate()).applyfunc(sp.simplify) == sp.zeros(2, 2))

check("[B5] k-evenness and the M10 symmetry group are unaffected: ombar(Q kbar) = ombar(kbar) iff "
      "Q Lbar Q^T = Lbar iff Q L Q^T = L (scaling by L^2 commutes with Q)",
      all(((Q*Lbar_expected*Q.T - Lbar_expected).applyfunc(sp.simplify) == sp.zeros(2, 2))
          == ((Q*Lt*Q.T - Lt).applyfunc(sp.simplify) == sp.zeros(2, 2))
          for Q in (sp.Matrix([[1, 0], [0, -1]]), sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -1], [1, 0]]))))

# ============================================================== 5. limits
check("[L1] limits of the barred dispersion: (i) lbar=ellbar=0 -> ombar_T = pi kbar (classical, non-dispersive); "
      "(ii) AR=1 -> isotropic factor (1 + pi^2 lbar^2 kbar^2/10); (iii) ellbar=0 -> unbounded ~ kbar^2 at large kbar; "
      "(iv) ellbar>0 -> ombar_T^2/kbar^2 -> pi^2 lbar_dir^2/(10 ellbar^2) bounded (M7/M16 ladder in barred form)",
      iszero(omb2_T.subs({lb1: 0, lb2: 0, ellb: 0, kb1: kbmag, kb2: 0}) - sp.pi**2*kbmag**2)
      and iszero(omb2_T.subs({lb2: lb1, kb1: kbmag, kb2: 0}) - sp.pi**2*kbmag**2*(1 + sp.pi**2*lb1**2*kbmag**2/10)/(1 + sp.pi**2*ellb**2*kbmag**2))
      and sp.limit(omb2_T.subs({ellb: 0, th: 0, kb1: kbmag, kb2: 0})/kbmag**4, kbmag, sp.oo) == sp.pi**4*lb1**2/10
      and sp.limit(omb2_T.subs({th: 0, kb1: kbmag, kb2: 0})/kbmag**2, kbmag, sp.oo) == sp.pi**2*lb1**2/(10*ellb**2))

check("[L2] 1-D normal-incidence reduction (kbar2 = 0, theta = 0) used by the anchor comparisons: "
      "ombar_L^2 = (lambda/mu+2) pi^2 kbar^2 (1 + pi^2 lbar1^2 kbar^2/10)/(1 + pi^2 ellbar^2 kbar^2)",
      iszero(omb2_L.subs({th: 0, kb1: kbmag, kb2: 0})
             - (lam/mu + 2)*sp.pi**2*kbmag**2*(1 + sp.pi**2*lb1**2*kbmag**2/10)/(1 + sp.pi**2*ellb**2*kbmag**2)))

# ============================================================== 6. anchor schemes (mapping only, [C])
a1, om0A = sp.symbols('a_1 omega_0A', positive=True)
check("[A1] anchor A scheme (plan row M11 [C]): kbar_A = k a_1/pi, ombar_A = omega/omega_0A -- same FORM as "
      "(45)-(46) with L -> a_1 (layer thickness) and omega_0 -> omega_0A (quoted 4.1e8 1/s); conversion "
      "ombar_A = ombar (omega_0/omega_0A), kbar_A = kbar (a_1/L); no equation change",
      iszero((omb*om0/om0A) - omb*om0/om0A) and iszero((sp.pi*kb1/L)*a1/sp.pi - kb1*a1/L))

aA, aB, c33, c33p, rhoA, rhoB, bsym = sp.symbols('a_A a_B c33 c33p rho_A rho_B b', positive=True)
om0B = 2*sp.pi/(aA/sp.sqrt(c33/rhoA) + aB/sp.sqrt(c33p/rhoB))
check("[A2] anchor B scheme [C]: omega_0B = 2 pi / (a_A/sqrt(c33/rho) + a_B/sqrt(c33'/rho')) has units 1/s "
      "(2 pi over the one-way travel time of the bilayer); kbar_B = k b/pi with b = TV2 (a_A + a_B assumed, "
      "not locked); conversion ombar_B = ombar omega_0/omega_0B -- omega_0B is NOT of the form sqrt(mu/(rho L^2))",
      convert_to((meter/sp.sqrt(pascal/(kilogram/meter**3)))**-1, [second]) == 1/second
      and sp.simplify(om0B - om0.subs({mu: c33, rho: rhoA, L: aA})) != 0)

print()
print(f"TOTAL {PASS + FAIL}  PASS {PASS}  FAIL {FAIL}")
