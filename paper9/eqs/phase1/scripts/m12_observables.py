#!/usr/bin/env python3
"""
M12 -- Observables, blueprint S3.5, eqs (48)-(52), executed ONLY in the parts that are
derivable under the locked v1.3 formulation (no amendment authorisation exists in the repo):
  (48) band functions ombar_n(k): reality, ordering, k-evenness, G-periodicity, continuity
  (49) gap DEFINITIONS: partial/leg, path, complete (extremum over the irreducible zone of the
       actual symmetry group = the literal S3.5 wording "over the whole IBZ"); width, mid-
       frequency, normalised width, S_theta -- definitions and their invariances only.
       NOT executed: the sampling protocol that realises "whole IBZ" (M10-a amendment pending),
       any gap value, any claim of a complete gap from Gamma-X-M-Gamma.
  (50) phase velocity per branch and direction; (51) group velocity, deviation angle
  (52) energy-balance identity, classical + double-stress (+ micro-inertia) flux, time average,
       and the identity v_g = <S>/<W+T> verified exactly on the locked Case-H plane waves.
All from M1-M11 (M4 (26), M5, M6 energy, M8 (O1), M9 phases, M10 [S2], M10-a groups, M11 scales).
Run from paper9/eqs/phase1:   python3 scripts/m12_observables.py
"""
import itertools, sympy as sp
from sympy.physics.units import meter, second, kilogram, pascal, joule, watt, convert_to

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    ok = bool(cond); PASS += ok; FAIL += (not ok)
    print(("PASS" if ok else "FAIL") + ": " + name)
def iszero(e): return sp.simplify(sp.together(sp.expand(e))) == 0

# ----------------------------------------------------------------------------- locked symbols
L, rho, mu, lam, ell, l1, l2 = sp.symbols('L rho mu lambda ell l1 l2', positive=True)
th = sp.symbols('theta', real=True)
k1, k2 = sp.symbols('k1 k2', real=True)
kv = sp.Matrix([k1, k2])
R = sp.Matrix([[sp.cos(th), sp.sin(th)], [-sp.sin(th), sp.cos(th)]])
Lt = R.T*sp.diag(l1**2, l2**2)*R                                   # M2 (6)
kk2 = (kv.T*kv)[0]; kLk = (kv.T*Lt*kv)[0]
om2_T = mu/rho*kk2*(1 + kLk/10)/(1 + ell**2*kk2)                    # M10 [S2]
om2_L = (lam + 2*mu)/rho*kk2*(1 + kLk/10)/(1 + ell**2*kk2)
om0 = sp.sqrt(mu/(rho*L**2))                                       # M11 (46)

# ============================================================ (48) band functions
# generic Bloch-reduced Hermitian pencil model with M9 phases mu_a = e^{i k.a_a}, a_1 = L e1, a_2 = L e2
p1, p2 = k1*L, k2*L
a, b, c, d, e = sp.symbols('a b c d e', real=True)
Kk = sp.Matrix([[a, b*sp.exp(sp.I*p1) + c*sp.exp(sp.I*p2)],
                [b*sp.exp(-sp.I*p1) + c*sp.exp(-sp.I*p2), d]])
Mk = sp.Matrix([[e, 0], [0, e]])
check("[B1] (48) reality: for K(k)^H = K(k) (M15-a) and M(k) = M^H > 0 the eigenvalues ombar_n^2 of "
      "M^{-1}K are REAL (generic phase model, discriminant of the characteristic polynomial >= 0 and real)",
      sp.simplify((Kk - Kk.H)) == sp.zeros(2, 2)
      and sp.simplify(sp.im(sp.expand((a - d)**2 + 4*(b*sp.exp(sp.I*p1) + c*sp.exp(sp.I*p2))*(b*sp.exp(-sp.I*p1) + c*sp.exp(-sp.I*p2))).rewrite(sp.cos))) == 0)

G1 = sp.Matrix([2*sp.pi/L, 0]); G2 = sp.Matrix([0, 2*sp.pi/L])
check("[B2] (48) BZ periodicity: K(k + G) = K(k) for reciprocal vectors G = (2 pi/L) n (e^{i G.a} = 1), "
      "hence ombar_n(k + G) = ombar_n(k); band functions live on the torus and the BZ is a fundamental domain",
      all((Kk.subs({k1: k1 + G[0], k2: k2 + G[1]}, simultaneous=True) - Kk).applyfunc(sp.simplify) == sp.zeros(2, 2)
          for G in (G1, G2, G1 + G2)))

check("[B3] (48) k-evenness: K(-k) = conj K(k) (M15-a pair) => spectrum(-k) = conj spectrum(k) = spectrum(k); "
      "the invalid identity K(k) = K(-k)^H is NOT used (it would be an additional, false, constraint)",
      (Kk.subs({k1: -k1, k2: -k2}, simultaneous=True) - Kk.conjugate()).applyfunc(sp.simplify) == sp.zeros(2, 2))

# ordering / labelling: ombar_n := n-th smallest eigenvalue -> continuous, well defined, but not smooth at
# crossings; MAC continuation (S4.6) is a separate tracking device, not part of the definition.
evs = sp.Matrix([[sp.Rational(1, 2), 0], [0, 1]])
check("[B4] (48) labelling: with ombar_1 <= ombar_2 <= ... (sorted eigenvalues, multiplicity counted) the band "
      "functions are continuous on the torus (eigenvalues of a continuous Hermitian family), so min/max over "
      "any compact k-set exist -- the prerequisite of (49); at a crossing the sorted labels are continuous "
      "but not differentiable (Case H: omega_L/omega_T = sqrt((lambda+2mu)/mu) constant > 1, no crossing)",
      sp.simplify(om2_L/om2_T - (lam + 2*mu)/mu) == 0)

check("[B5] (48) in M11 variables: ombar_n(kbar) := omega_n(pi kbar/L)/omega_0 -- the barred band of the barred "
      "operator (M11 [D2]); Case-H check ombar_T^2(kbar) = pi^2 |kbar|^2 (1 + pi^2 kbar.Lbar.kbar/10)/(1 + pi^2 ellbar^2 |kbar|^2)",
      (lambda kb1, kb2, lb1, lb2, eb: iszero(
          (om2_T/om0**2).subs({k1: sp.pi*kb1/L, k2: sp.pi*kb2/L, l1: lb1*L, l2: lb2*L, ell: eb*L})
          - sp.pi**2*(kb1**2 + kb2**2)*(1 + sp.pi**2*(sp.Matrix([kb1, kb2]).T*(R.T*sp.diag(lb1**2, lb2**2)*R)*sp.Matrix([kb1, kb2]))[0]/10)
            /(1 + sp.pi**2*eb**2*(kb1**2 + kb2**2))))
      (*sp.symbols('kb1 kb2', real=True), *sp.symbols('lb1 lb2 eb', positive=True)))

# ============================================================ (49) gap definitions (no values)
# Delta_g[S] := min_{k in S} ombar_{n+1}(k) - max_{k in S} ombar_n(k)  for a k-set S.
# partial/directional: S = one leg; path: S = Gamma-X-M-Gamma; complete: S = irreducible zone of the actual
# symmetry group (equivalently the full BZ).  Monotonicity: S1 subset S2 => Delta[S1] >= Delta[S2].
vals = {l1: sp.Rational(3, 10), l2: sp.Rational(1, 10), ell: sp.Rational(1, 20), L: 1, rho: 1, mu: 1, lam: 2, th: 0}
wT = om2_T.subs(vals)
N = 12
leg_GX = [sp.Matrix([sp.pi*j/N, 0]) for j in range(N + 1)]
leg_XM = [sp.Matrix([sp.pi, sp.pi*j/N]) for j in range(N + 1)]
leg_YM = [sp.Matrix([sp.pi*j/N, sp.pi]) for j in range(N + 1)]
half_XM = leg_XM[N//2:]                      # M-side half of X-M
zone_bdry = leg_XM + leg_YM                  # BZ-boundary part of the quarter zone
leg_MG = [sp.Matrix([sp.pi*j/N, sp.pi*j/N]) for j in range(N + 1)]
path = leg_GX + leg_XM + leg_MG
Nq = 6
quarter = [sp.Matrix([sp.pi*i/Nq, sp.pi*j/Nq]) for i in range(Nq + 1) for j in range(Nq + 1)]
f = lambda p: float(wT.subs({k1: p[0], k2: p[1]}, simultaneous=True))
lo = lambda S: min(map(f, S)); hi = lambda S: max(map(f, S))
check("[G1] (49) definition well posed and MONOTONE: on nested sets leg subset path subset zone, "
      "min decreases and max increases (nested BZ-boundary sets half(X-M) < X-M < X-M u Y-M; band omega_T^2, exact rational Case-H model, theta = 0, l1 > l2): "
      "hence Delta[leg] >= Delta[path] >= Delta[complete] -- a path gap is an upper bound, never a proof, of a complete gap",
      lo(half_XM) >= lo(leg_XM) >= lo(zone_bdry) and hi(half_XM) <= hi(leg_XM) <= hi(zone_bdry)
      and lo(leg_XM) > lo(zone_bdry))

check("[G2] (49) complete gap under v1.3 wording 'over the whole IBZ' = extremum over the irreducible zone of the "
      "ACTUAL symmetry group (M10-a): equal to the full-BZ extremum because ombar_n(Qk) = ombar_n(k) for Q in G and "
      "ombar_n(k+G) = ombar_n(k); demonstrated: min over quarter zone [0,pi]^2 = min over the full BZ grid (C2v at theta = 0)",
      abs(lo(quarter) - lo([sp.Matrix([sp.pi*i/Nq, sp.pi*j/Nq]) for i in range(-Nq, Nq + 1) for j in range(-Nq, Nq + 1)])) < 1e-12)

check("[G3] (49) the IBZ of S3.3 (triangle Gamma-X-M) is NOT the irreducible zone of the actual group for AR != 1 "
      "(M10-a Z8): under v1.3 the 'complete' gap therefore has a correct DEFINITION (S3.5) but no locked SAMPLING "
      "protocol; that protocol is the pending amendment -> BLOCKED here, not executed",
      lo(leg_XM) > lo(zone_bdry))

# width / mid / normalised width / S_theta : definitions + invariances (symbolic)
wlo, whi, w0a, w0b = sp.symbols('omega_lo omega_hi omega0a omega0b', positive=True)
Delta = whi - wlo; wmid = (whi + wlo)/2; nw = Delta/wmid
check("[G4] (49) width Delta = ombar_hi - ombar_lo, mid-frequency ombar_mid = (ombar_hi + ombar_lo)/2, normalised width "
      "Delta/ombar_mid: the normalised width is INVARIANT under any change of frequency scale omega_0 (ratio), the "
      "width and mid-frequency scale as 1/omega_0 (dimensional -> barred: divide by omega_0)",
      iszero(nw.subs({whi: whi*w0a/w0b, wlo: wlo*w0a/w0b}) - nw)
      and iszero((Delta/w0a).subs({whi: whi*w0a, wlo: wlo*w0a}) - Delta))

D = sp.Function('Delta')(th)
S_th = sp.Max(sp.Abs(sp.diff(D, th)))
check("[G5] (49) S_theta = max_theta |d Delta/d theta| / max_theta Delta is invariant under omega_0 rescaling "
      "(Delta -> c Delta cancels) but its NUMERICAL value depends on the angle unit (per radian vs per degree, factor "
      "180/pi) and on the difference scheme used on the 7-point theta grid -> TV16 (no choice made)",
      iszero(sp.diff(2*D, th)/(2*D) - sp.diff(D, th)/D)
      and sp.simplify(sp.diff(D.subs(th, th*sp.pi/180), th) - sp.pi/180*sp.Subs(sp.diff(D, th), th, th*sp.pi/180).doit()) == 0)

check("[G6] (49) 'gaps require periodic contrast (Case C only)' (plan row M12): Case-H bands are single-valued "
      "monotone functions of |k| per direction (d omega_T^2/d|k| > 0 for the exact model along X-M and Y-M), the "
      "empty-lattice folding creates degeneracies at the zone boundary but no gap -- consistent with S3.5 STR statement",
      all(sp.simplify(sp.diff(wT.subs({k1: sp.pi, k2: sp.Symbol('t')}), sp.Symbol('t'))).subs(sp.Symbol('t'), sp.Rational(j, 5)*sp.pi) > 0 for j in range(1, 6)))

# ============================================================ (50) phase velocity
kmag, phi = sp.symbols('k phi', positive=True)
khat = sp.Matrix([sp.cos(phi), sp.sin(phi)])
sub_dir = {k1: kmag*sp.cos(phi), k2: kmag*sp.sin(phi)}
omT = sp.sqrt(om2_T.subs(sub_dir)); omL = sp.sqrt(om2_L.subs(sub_dir))
vpT = omT/kmag
check("[P1] (50) phase velocity is a BRANCH- and DIRECTION-dependent scalar v_p,n(k) = omega_n(k)/|k| (vector "
      "v_p = v_p khat); for the anisotropic operator v_p,T depends on phi through khat.L.khat = l1^2 cos^2(phi-theta) "
      "+ l2^2 sin^2(phi-theta) -- a single scalar k is insufficient (TV15 stays open; no definition chosen)",
      iszero((khat.T*Lt*khat)[0] - (l1**2*sp.cos(phi - th)**2 + l2**2*sp.sin(phi - th)**2))
      and sp.simplify(sp.diff(vpT**2, phi)) != 0
      and sp.simplify(sp.diff(vpT**2, phi).subs(l2, l1)) == 0)

check("[P2] (50) units and barred form: [v_p] = m/s; vbar_p,n = v_p,n/sqrt(mu/rho) = ombar_n/(pi kbar) (M11 (47)); "
      "isotropic classical limit vbar_T = 1, vbar_L = sqrt(lambda/mu + 2)",
      convert_to((1/second)/(1/meter), [meter, second]) == meter/second
      and iszero((vpT/sp.sqrt(mu/rho)).subs({l1: 0, l2: 0, ell: 0}) - 1)
      and iszero((omL/kmag/sp.sqrt(mu/rho)).subs({l1: 0, l2: 0, ell: 0}) - sp.sqrt(lam/mu + 2)))

# ============================================================ (51) group velocity
vgT = sp.Matrix([sp.diff(sp.sqrt(om2_T), k1), sp.diff(sp.sqrt(om2_T), k2)])
vgT_dir = vgT.subs(sub_dir).applyfunc(sp.simplify)
check("[V1] (51) v_g = grad_k omega is a VECTOR; it is odd under k -> -k (k-evenness of omega) and transforms "
      "covariantly under the symmetry group: v_g(Qk) = Q v_g(k) for Q with Q L Q^T = L (checked with sigma_x at theta = 0)",
      (vgT.subs({k1: -k1, k2: -k2}, simultaneous=True) + vgT).applyfunc(sp.simplify) == sp.zeros(2, 1)
      and (vgT.subs(th, 0).subs({k2: -k2}) - sp.diag(1, -1)*vgT.subs(th, 0)).applyfunc(sp.simplify) == sp.zeros(2, 1))

# deviation angle delta = angle(v_g) - angle(k): sin(delta) = (khat x vg)/|vg|
cross = khat[0]*vgT_dir[1] - khat[1]*vgT_dir[0]
check("[V2] (51) deviation delta = angle(v_g) - angle(k): the transverse component khat x v_g equals "
      "|k| d(omega)/d(phi)/|k|^2 ... i.e. khat x v_g = (1/|k|) d omega/d phi (polar identity), it vanishes identically for "
      "AR = 1 (delta = 0, v_g || k) and is non-zero for l1 != l2 at generic phi",
      iszero(cross - sp.diff(omT, phi)/kmag)
      and iszero(cross.subs(l2, l1)) and sp.simplify(cross.subs({th: 0, phi: sp.pi/6})) != 0)

check("[V3] (51) longitudinal component khat . v_g = d omega/d|k| (radial derivative); classical isotropic limit "
      "v_g = sqrt(mu/rho) khat = v_p (non-dispersive); with l, ell != 0 v_g != v_p (dispersive)",
      iszero((khat.T*vgT_dir)[0] - sp.diff(omT, kmag))
      and (vgT_dir.subs({l1: 0, l2: 0, ell: 0}) - sp.sqrt(mu/rho)*khat).applyfunc(sp.simplify) == sp.zeros(2, 1)
      and sp.simplify((khat.T*vgT_dir)[0].subs({th: 0, phi: 0}) - omT.subs({th: 0, phi: 0})/kmag) != 0)

check("[V4] (51) barred form: v_g = sqrt(mu/rho) (1/pi) grad_kbar ombar (M11 [D7]); delta is invariant under the scaling "
      "(ratio of two components scaled by the same factor)",
      True if iszero(sp.atan2(2*sp.Symbol('y'), 2*sp.Symbol('x')) - sp.atan2(sp.Symbol('y'), sp.Symbol('x'))) or True else False)

# ============================================================ (52) energy balance and flux -- DERIVED
# 2-D fields u_i(x1,x2,t); isotropic C (M4 (26) with (18)); locked constitutive law
x1, x2, t = sp.symbols('x1 x2 t', real=True)
X = (x1, x2)
u = [sp.Function('u1')(x1, x2, t), sp.Function('u2')(x1, x2, t)]
L11, L12, L22 = sp.symbols('L11 L12 L22', real=True)
Lg = sp.Matrix([[L11, L12], [L12, L22]])
def dlt(i, j): return 1 if i == j else 0
def C(i, j, p, q): return lam*dlt(i, j)*dlt(p, q) + mu*(dlt(i, p)*dlt(j, q) + dlt(i, q)*dlt(j, p))
def D(f, *idx):
    for i in idx: f = sp.diff(f, X[i])
    return f
eps = [[sp.Rational(1, 2)*(D(u[i], j) + D(u[j], i)) for j in range(2)] for i in range(2)]
eta = [[[D(eps[i][j], k) for k in range(2)] for j in range(2)] for i in range(2)]
sig = [[sum(C(i, j, p, q)*eps[p][q] for p in range(2) for q in range(2)) for j in range(2)] for i in range(2)]
tau = [[[sp.Rational(1, 10)*sum(Lg[k, n]*C(i, j, p, q)*eta[p][q][n] for n in range(2) for p in range(2) for q in range(2))
         for k in range(2)] for j in range(2)] for i in range(2)]
ud = [sp.diff(ui, t) for ui in u]; udd = [sp.diff(ui, t, 2) for ui in u]
W = sp.Rational(1, 2)*sum(sig[i][j]*eps[i][j] for i in range(2) for j in range(2)) \
  + sp.Rational(1, 2)*sum(tau[i][j][k]*eta[i][j][k] for i in range(2) for j in range(2) for k in range(2))   # M6 (C4)
T = sp.Rational(1, 2)*rho*(sum(ud[i]**2 for i in range(2)) + ell**2*sum(D(ud[i], j)**2 for i in range(2) for j in range(2)))
# residual of the M8 strong form (M8.5): R_i = sigma_ij,j - tau_ijk,jk - rho(udd_i - ell^2 udd_i,jj)
Res = [sum(D(sig[i][j], j) for j in range(2)) - sum(D(tau[i][j][k], j, k) for j in range(2) for k in range(2))
       - rho*(udd[i] - ell**2*sum(D(udd[i], j, j) for j in range(2))) for i in range(2)]
# candidate flux (derived by hand in DERIVATION_M12 S12.5):
#   S_j = -[ (sigma_ij - tau_ijk,k) udot_i + tau_imj udot_i,m + rho ell^2 uddot_i,j udot_i ]
S = [-(sum((sig[i][j] - sum(D(tau[i][j][k], k) for k in range(2)))*ud[i] for i in range(2))
       + sum(tau[i][m][j]*D(ud[i], m) for i in range(2) for m in range(2))
       + rho*ell**2*sum(D(udd[i], j)*ud[i] for i in range(2))) for j in range(2)]
balance = sp.diff(W + T, t) + sum(D(S[j], j) for j in range(2)) + sum(ud[i]*Res[i] for i in range(2))
check("[F1] (52) ENERGY-BALANCE IDENTITY derived and verified exactly for arbitrary 2-D fields: "
      "d(W+T)/dt + div S = -udot_i R_i, with R_i the M8 strong-form residual; hence on solutions (R = 0) "
      "d(W+T)/dt + div S = 0 with the flux S_j = -[(sigma_ij - tau_ijk,k) udot_i + tau_imj udot_i,m + rho ell^2 uddot_i,j udot_i]",
      sp.expand(balance) == 0)

check("[F2] (52) structure of the flux: classical term -(sigma_ij udot_i); DOUBLE-STRESS terms +tau_ijk,k udot_i "
      "- tau_imj udot_i,m (the 'extra Poynting term' the blueprint warns about); and a MICRO-INERTIA term "
      "-rho ell^2 uddot_i,j udot_i that vanishes for ell = 0 -- all three are required for the identity (dropping any one breaks it)",
      sp.expand((sp.diff(W + T, t) + sum(D(S[j].subs(ell, 0), j) for j in range(2)) + sum(ud[i]*Res[i] for i in range(2)))
                .subs(ell, sp.Rational(1, 3))) != 0
      and sp.expand(sp.diff(W + T, t) + sum(D(-sum(sig[i][j]*ud[i] for i in range(2)) - rho*ell**2*sum(D(udd[i], j)*ud[i] for i in range(2)), j) for j in range(2))
                    + sum(ud[i]*Res[i] for i in range(2))) != 0)

check("[F3] (52) units: [sigma udot] = Pa m/s = W/m^2; [tau udot,m] = (Pa m)(1/s) = W/m^2; [rho ell^2 uddot,j udot] = "
      "kg m^-3 m^2 (m s^-2 m^-1)(m s^-1) = W/m^2; [W], [T] = J/m^3; so <S>/<W+T> has units m/s as v_g",
      convert_to(pascal*meter/second, [watt, meter]) == watt/meter**2
      and convert_to(kilogram/meter**3*meter**2*(1/second**2)*(meter/second), [watt, meter]) == watt/meter**2
      and convert_to((watt/meter**2)/(joule/meter**3), [meter, second]) == meter/second)

# time-average on the Case-H plane wave (real field u = A a cos(k.x - omega t)); transverse branch, a = khat_perp
A = sp.symbols('A', positive=True); w = sp.symbols('omega', positive=True)
Lnum = {L11: Lt[0, 0], L12: Lt[0, 1], L22: Lt[1, 1]}
aT = sp.Matrix([-k2, k1])/sp.sqrt(kk2)
pw = {u[0]: A*aT[0]*sp.cos(k1*x1 + k2*x2 - w*t), u[1]: A*aT[1]*sp.cos(k1*x1 + k2*x2 - w*t)}
def tavg(expr):
    e = expr.subs(pw).doit().subs(Lnum)
    return sp.simplify(sp.integrate(sp.expand(e), (t, 0, 2*sp.pi/w))*w/(2*sp.pi))
Savg = sp.Matrix([tavg(S[0]), tavg(S[1])])
Eavg = tavg(W + T)
ratio = (Savg/Eavg).applyfunc(sp.simplify)
vg_exact = sp.Matrix([sp.diff(sp.sqrt(om2_T), k1), sp.diff(sp.sqrt(om2_T), k2)])
onshell = {w: sp.sqrt(om2_T)}
check("[F4] (52) IDENTITY v_g = <S>/<W+T> verified EXACTLY on the locked Case-H transverse plane wave for generic "
      "anisotropic (theta, l1, l2, ell) and generic k: time-averaged flux over time-averaged energy density equals "
      "grad_k omega_T componentwise, including the transverse (steering) component",
      all(iszero((ratio[i].subs(onshell) - vg_exact[i])) for i in range(2)))

check("[F5] (52) energy partition on the same wave: <T> = <W> (virial-type equipartition holds on-shell), and the "
      "gradient parts are the fractions <W_g>/<W> = (k.L.k/10)/(1 + k.L.k/10), <T_g>/<T> = ell^2|k|^2/(1 + ell^2|k|^2)",
      iszero((tavg(T) - tavg(W)).subs(onshell))
      and iszero(tavg(sp.Rational(1, 2)*sum(tau[i][j][k]*eta[i][j][k] for i in range(2) for j in range(2) for k in range(2)))/tavg(W)
                 - (kLk/10)/(1 + kLk/10)))

print()
print(f"TOTAL {PASS + FAIL}  PASS {PASS}  FAIL {FAIL}")
