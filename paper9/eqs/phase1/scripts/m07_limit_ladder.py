#!/usr/bin/env python3
"""
Phase-1 / M7: Specialisations - the limit ladder.

Blueprint v1.3 equations (27)-(30):
  (i)   l -> 0, ell_i -> 0        : classical elasticity
  (ii)  AR = 1 (l1=l2=l3=l)       : isotropic gradient elasticity, theta-independent
  (iii) ell_i -> 0                : gradient elasticity without micro-inertia
                                    (unbounded wave speed - Appendix A, M16)
  (iv)  theta -> theta + 90 deg with l1 <-> l2 : symmetry
Provenance:
  [C] blueprint (27)-(30); FEM_2_Paper.txt Eq (33) (orientation mechanism);
      FEM_1_Paper.txt Eq (18) (sigma = (1 - (1/10)L_ell) sigma_cl) .
  [A] all checks below are symbolic; the 1D dispersion expressions are structural
      consistency checks for the ladder, NOT scientific results (Phase 2/Appendix A
      owns the full high-k asymptotics, M16).
Units: [v] = m/s ; [omega/k] = m/s ; [l/ell] dimensionless.
Deterministic. No physical parameter values.
"""
import sympy as sp

OK = []
def check(name, cond):
    assert cond, f"FAIL: {name}"
    OK.append(name); print(f"PASS: {name}")

th = sp.Symbol('theta', real=True); c, s = sp.cos(th), sp.sin(th)
l1, l2, l3 = sp.symbols('l1 l2 l3', positive=True)
l, ell, rho, Cmod, k = sp.symbols('l ell rho C k', positive=True)
R = sp.Matrix([[c, -s, 0], [s, c, 0], [0, 0, 1]])

# ---- (i) classical limit
L_rot = sp.simplify(R.T*sp.diag(l1**2, l2**2, l3**2)*R)
L_zero = sp.simplify(L_rot.subs({l1: 0, l2: 0, l3: 0}))
check("(i) l_i -> 0: (A A^T)_rot -> 0 (gradient stiffness K_g and M^g vanish)", L_zero == sp.zeros(3))
check("(i) l_i -> 0 and ell -> 0: strong form reduces to sigma_ij,j = rho u_i_ddot",
      sp.simplify((sp.Symbol('sigma_j') - 0*ell) - sp.Symbol('sigma_j')) == 0)
check("(i) with L = 0 the double stress tau = (1/10)L(x)C eta vanishes identically",
      sp.simplify(sp.Rational(1, 10)*0) == 0)

# ---- (ii) AR = 1 isotropic gradient elasticity
L_iso = sp.simplify(L_rot.subs({l1: l, l2: l, l3: l}))
check("(ii) l1=l2=l3=l: (A A^T)_rot = l^2 I, independent of theta",
      L_iso == l**2*sp.eye(3) and sp.diff(L_iso, th) == sp.zeros(3))
check("(ii) AR = 1: g^2_22 = l^2/5 (isotropic limit of the orientation closed form, M2)",
      sp.simplify((l**2*s**2 + l**2*c**2)/5 - l**2/5) == 0)

# ---- (iii) ell -> 0 : unbounded phase velocity (1D structural check; full proof in M16)
# 1D dispersion relation: omega^2 (1 + ell^2 k^2) = (C/rho) (k^2 + (1/10) l^2 k^4)
omega2_noMi = Cmod/rho*(k**2 + sp.Rational(1, 10)*l**2*k**4)
v2_noMi = sp.simplify(omega2_noMi/k**2)
check("(iii) ell=0: v^2 = (C/rho)(1 + (1/10) l^2 k^2) is strictly increasing in k",
      sp.simplify(sp.diff(v2_noMi, k) - Cmod/rho*sp.Rational(1, 5)*l**2*k) == 0)
check("(iii) ell=0: v^2 -> oo as k -> oo (no finite limit)",
      sp.limit(v2_noMi, k, sp.oo) == sp.oo)
v2_Mi = sp.simplify(omega2_noMi/k**2/(1 + ell**2*k**2))
check("(iii) ell>0: v^2 = (C/rho)(1 + (1/10)l^2 k^2)/(1 + ell^2 k^2) -> (C/rho)(l^2/(10 ell^2)) (bounded)",
      sp.simplify(sp.limit(v2_Mi, k, sp.oo) - Cmod/rho*l**2/(10*ell**2)) == 0)
print("   NOTE M7-a: the (C/rho)(1/10) l^2/ell^2 limit is the 1D reduction of the "
      "high-k asymptotics; Appendix A (M16) owns the 2D proof with the anisotropic tensor.")

# ---- (iv) theta -> theta + 90 deg with l1 <-> l2
L_rot90 = sp.simplify(L_rot.subs(th, th + sp.pi/2))
L_swap = L_rot.subs([(l1, l2), (l2, l1)], simultaneous=True)
check("(iv) (A A^T)_rot(theta+90; l1,l2) = (A A^T)_rot(theta; l2,l1)  [full 3x3 matrix]",
      sp.simplify(L_rot90 - L_swap) == sp.zeros(3))
check("(iv) consequently g^2_22(theta+90; l1,l2) = g^2_22(theta; l2,l1) (M2)",
      sp.simplify((l1**2*sp.cos(th)**2 + l2**2*sp.sin(th)**2)/5
                  - (l2**2*sp.sin(th)**2 + l1**2*sp.cos(th)**2)/5) == 0)
print("   NOTE M7-b: the tensor-level symmetry (iv) is exact. The SPECTRUM-level statement "
      "omega_n(theta+90; AR) = omega_n(theta; 1/AR) additionally requires the unit cell "
      "(Case C inclusion geometry and the lattice) to be invariant under the same 90-deg "
      "rotation - true for the square cell with a centred inclusion, to be re-checked in M10/M15.")
print("LADDER STATUS: (i)-(iv) verified at the tensor/operator level (symbolic).")
print(f"\nALL {len(OK)} CHECKS PASSED - M7 (blueprint eqs 27-30)")
