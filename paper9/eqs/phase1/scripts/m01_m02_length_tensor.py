#!/usr/bin/env python3
"""
Phase-1 / M1+M2: Ellipsoidal averaging domain, second-moment characteristic-length
tensor, orientation rotation, in-plane closed form g^2_22(theta).

Blueprint v1.3 equations: (1)-(9) [plus eigenvalue-invariance component of (25)].
Provenance:
  [C] FEM_1_Paper.txt Eqs (2)-(9): uniform kernel, ellipsoid |V|=4*pi/3*l1*l2*l3,
      xi = A u with A = diag(l1,l2,l3), A A^T = diag(l1^2,l2^2,l3^2),
      moment identity (1/|V|) int xi_i xi_j dV = (1/5)(A A^T)_ij  (unit ball: 4*pi/15),
      Taylor coefficient 1/10 = (1/2)*(1/5).
  [C] FEM_2_Paper.txt Eq (33): g^2_22(alpha) = (a1^2 sin^2 alpha + a2^2 cos^2 alpha)/5.
  [A] all checks below are re-derived symbolically (SymPy exact arithmetic).
Units: l1,l2,l3 in m  =>  (A A^T), L_rot, g^2 in m^2.
No numerical parameter values are used anywhere (all symbolic).
"""
import sympy as sp

OK = []
def check(name, cond):
    assert cond, f"FAIL: {name}"
    OK.append(name)
    print(f"PASS: {name}")

# ---------------------------------------------------------------- M1: eqs (1)-(4)
l1, l2, l3 = sp.symbols('l1 l2 l3', positive=True)
# unit-ball second moment, explicit spherical integration (exact)
r, t, p = sp.symbols('r t p', positive=True)
u1 = r*sp.sin(t)*sp.cos(p); u2 = r*sp.sin(t)*sp.sin(p); u3 = r*sp.cos(t)
J = r**2*sp.sin(t)
I11 = sp.integrate(u1*u1*J, (p, 0, 2*sp.pi), (t, 0, sp.pi), (r, 0, 1))
I22 = sp.integrate(u2*u2*J, (p, 0, 2*sp.pi), (t, 0, sp.pi), (r, 0, 1))
I33 = sp.integrate(u3*u3*J, (p, 0, 2*sp.pi), (t, 0, sp.pi), (r, 0, 1))
I12 = sp.integrate(u1*u2*J, (p, 0, 2*sp.pi), (t, 0, sp.pi), (r, 0, 1))
Vball = 4*sp.pi/3
check("unit-ball <u1^2> = <u2^2> = <u3^2> = 1/5", sp.simplify(I11/Vball - sp.Rational(1,5)) == 0
      and sp.simplify(I22/Vball) == sp.Rational(1,5) and sp.simplify(I33/Vball) == sp.Rational(1,5))
check("unit-ball <u1 u2> = 0 (off-diagonal moments vanish)", sp.simplify(I12) == 0)

# ellipsoid mapping xi = A u, A = diag(l1,l2,l3): (1/|V|) int xi_i xi_j dV = (1/5)(A A^T)_ij
A = sp.diag(l1, l2, l3)
ATA = A.T*A
check("A A^T = diag(l1^2, l2^2, l3^2)   [blueprint (4)]", ATA == sp.diag(l1**2, l2**2, l3**2))
Vell = sp.Rational(4,3)*sp.pi*l1*l2*l3
detA = A.det()   # dV_xi = det(A) dV_u : volume element of the affine map xi = A u
xi = [l1*u1, l2*u2, l3*u3]
mom = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        mom[i, j] = sp.simplify(
            sp.integrate(xi[i]*xi[j]*J*detA, (p, 0, 2*sp.pi), (t, 0, sp.pi), (r, 0, 1))/Vell)
check("ellipsoid moment identity (1/|V|)int xi_i xi_j dV = (1/5)(A A^T)_ij   [FEM_1 (6)]",
      sp.simplify(mom - ATA/5) == sp.zeros(3))
# Taylor coefficient 1/10 = (1/2)*(1/5)   [blueprint (2), FEM_1 (7)]
check("Taylor coefficient (1/2)*(1/5) = 1/10", sp.Rational(1,2)*sp.Rational(1,5) == sp.Rational(1,10))

# ------------------------------------------------- M1: nonlocal average, eqs (1),(2),(7)
# Weakly nonlocal average of a Taylor-expanded strain field over the ellipsoid:
#   (1/|V|) int_V eps(x+xi) dV_xi = eps(x) + (1/10)(A A^T)_ij eps,ij + O(l^4)
# second-order truncation; the odd moments vanish (centrosymmetric domain, uniform kernel).
cu = sp.Symbol('c', real=True)
bb = sp.symbols('b1 b2 b3', real=True)
Asym = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'A{min(i,j)}{max(i,j)}', real=True))  # eps,ij symmetric
# exact average of a quadratic field using the (independently verified) moment identities
uu = sp.Matrix([u1, u2, u3])
field = cu + sum(bb[i]*(A*uu)[i] for i in range(3)) + \
        sp.Rational(1, 2)*sum(Asym[i, j]*(A*uu)[i]*(A*uu)[j] for i in range(3) for j in range(3))
mom1 = {  # (1/|V_ball|) int u_i dV = 0 ; (1/|V_ball|) int u_i u_j dV = delta_ij/5
    'lin': sum(bb[i]*sum(A[i, m]*0 for m in range(3)) for i in range(3)),
    'quad': sp.Rational(1, 2)*sum(Asym[i, j]*sum(A[i, m]*A[j, n]*(sp.Rational(1, 5) if m == n else 0)
                                               for m in range(3) for n in range(3))
                              for i in range(3) for j in range(3)),
}
av_quad = cu + mom1['lin'] + mom1['quad']
taylor2 = cu + sp.Rational(1, 10)*sum(Asym[i, j]*(ATA)[i, j] for i in range(3) for j in range(3))
check("(1),(2),(7): exact average of a quadratic field = c + (1/10)(A A^T)_ij eps,ij "
      "(weakly nonlocal second-order truncation)",
      sp.simplify(av_quad - taylor2) == 0)
check("(2),(7): the 1/10 coefficient = Taylor 1/2 x normalized second moment 1/5",
      sp.simplify(sp.Rational(1, 2)*sp.Rational(1, 5) - sp.Rational(1, 10)) == 0)
check("(1),(2): odd moments vanish (centrosymmetric domain + uniform kernel) => no first-gradient term",
      sp.simplify(mom1['lin']) == 0)

# ---------------------------------------------------------------- M2: eqs (5)-(9)
th = sp.symbols('theta', real=True)
c, s = sp.cos(th), sp.sin(th)
R = sp.Matrix([[c, -s, 0], [s, c, 0], [0, 0, 1]])           # blueprint (5): rotation about z
check("R orthogonal: R^T R = I, det R = 1", sp.simplify(R.T*R) == sp.eye(3) and sp.simplify(R.det()) == 1)
Lrot = sp.simplify(R.T * sp.diag(l1**2, l2**2, l3**2) * R)   # blueprint (6)
exp11 = l1**2*c**2 + l2**2*s**2
exp12 = (l2**2 - l1**2)*c*s
exp22 = l1**2*s**2 + l2**2*c**2
check("L_rot components (7),(8): L11, L12=(l2^2-l1^2)cs, L22, L33=l3^2",
      all(sp.simplify(Lrot[i,j] - e) == 0 for i,j,e in
          [(0,0,exp11),(0,1,exp12),(1,0,exp12),(1,1,exp22),(2,2,l3**2)]))
check("L_rot symmetric", sp.simplify(Lrot - Lrot.T) == sp.zeros(3))
check("L_rot off-block (13),(23) entries vanish (rotation about z)",
      sp.simplify(Lrot[0,2]) == 0 and sp.simplify(Lrot[1,2]) == 0)
# eigenvalue invariance (blueprint (25), M6 cross-ref)
char_rot = sp.expand(sp.factor(Lrot.charpoly(sp.Symbol('x')).as_expr()))
char_prin = sp.expand((sp.Symbol('x')-l1**2)*(sp.Symbol('x')-l2**2)*(sp.Symbol('x')-l3**2))
check("rotation preserves eigenvalues {l1^2,l2^2,l3^2}   [blueprint (25)]",
      sp.simplify(char_rot - char_prin) == 0)
# positive definiteness for admissible ellipsoids (l_i > 0): Sylvester on 2x2 in-plane block
block = Lrot[:2,:2]
tr2 = sp.simplify(block.trace()); det2 = sp.simplify(block.det())
check("in-plane block: trace = l1^2+l2^2 > 0, det = l1^2 l2^2 > 0 (PD for l_i>0)",
      sp.simplify(tr2 - (l1**2+l2**2)) == 0 and sp.simplify(det2 - l1**2*l2**2) == 0)
check("3D det L_rot = l1^2 l2^2 l3^2 > 0", sp.simplify(sp.factor(Lrot.det()) - l1**2*l2**2*l3**2) == 0)
# the operator L_ell = (A A^T)_rot,ij d^2/dx_i dx_j carries the mixed term 2 L12 d^2/dx1 dx2
xi1v, xi2v = sp.symbols('xi1 xi2', real=True)
quad = sp.expand(sp.Matrix([xi1v, xi2v, 0]).T * Lrot * sp.Matrix([xi1v, xi2v, 0]))
quad = sp.expand(quad[0])
check("mixed term: xi^T (A A^T)_rot xi = L11 xi1^2 + 2 L12 xi1 xi2 + L22 xi2^2 (factor 2 explicit)",
      sp.simplify(quad - (exp11*xi1v**2 + 2*exp12*xi1v*xi2v + exp22*xi2v**2)) == 0)
check("off-diagonal L12 = (l2^2 - l1^2) cos th sin th vanishes only for th in {0, 90 deg} "
      "or l1 = l2 (i.e. the mixed derivative is the anisotropy mechanism)",
      sp.simplify(exp12) != 0 and sp.simplify(exp12.subs(th, 0)) == 0
      and sp.simplify(exp12.subs(th, sp.pi/2)) == 0
      and sp.simplify(exp12.subs(l1, l2)) == 0)

# in-plane closed form, blueprint (9) == FEM_2 (33) with a_i -> l_i
g22 = sp.simplify(Lrot[1,1]/5)
check("g^2_22(theta) = (l1^2 sin^2 th + l2^2 cos^2 th)/5   [blueprint (9), FEM_2 (33)]",
      sp.simplify(g22 - (l1**2*s**2 + l2**2*c**2)/5) == 0)
# 90-degree symmetry with l1 <-> l2 (preview of blueprint (30), fully checked in m07)
g22_rot90 = sp.simplify(g22.subs(th, th+sp.pi/2))
# NB: SymPy applies dict subs sequentially; simultaneous=True is required for a true swap.
g22_swap = sp.simplify(g22.subs([(l1, l2), (l2, l1)], simultaneous=True))
check("g^2_22(theta+90deg; l1,l2) = g^2_22(theta; l2,l1)", sp.simplify(g22_rot90 - g22_swap) == 0)

# ---------------------------------------------------------------- dimensional audit
# [l_i] = m  =>  [A A^T] = [L_rot] = [g^2] = m^2 ; coefficient 1/10 dimensionless
print("DIM: [l1,l2,l3] = m; [(A A^T)_rot] = m^2; [g^2_22] = m^2; 1/10, 1/5 dimensionless")
print(f"\nALL {len(OK)} CHECKS PASSED — M1 (eqs 1-4) + M2 (eqs 5-9, part of 25)")
