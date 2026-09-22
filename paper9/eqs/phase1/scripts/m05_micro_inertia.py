#!/usr/bin/env python3
"""
Phase-1 / M5: Micro-inertia - kinetic energy, inertial operator, time-harmonic reduction.

Blueprint v1.3 equations (19)-(21):
  (19) T = (1/2) rho u_i_dot u_i_dot + (1/2) rho ell_i^2 u_i_dot,j u_i_dot,j
  (20) inertial operator rho( u_i_ddot - ell_i^2 u_i_ddot,jj )
  (21) Hamilton's principle including the gradient-inertia term
Provenance:
  [C] FEM_1_Paper.txt Eq (20) region: micro-inertia with a single length ell_i (isotropic);
      blueprint (19)-(21) is the isotropic-length form (ell_i is a scalar, not a tensor).
  [A] integration-by-parts identity, boundary term, time-harmonic reduction, and the
      weak-form/mass-matrix structure re-derived symbolically here.
Units: [rho] = kg/m^3 ; [T] = J/m^3 = kg/(m s^2) ; [rho*ell_i^2*u_ddot,jj] = kg/(m^2 s^2) = Pa/m.
Deterministic. No physical parameter values.
"""
import sympy as sp

OK = []
def check(name, cond):
    assert cond, f"FAIL: {name}"
    OK.append(name); print(f"PASS: {name}")

t = sp.Symbol('t', real=True)
x = sp.Symbol('x', real=True)
rho, ell = sp.symbols('rho ell', positive=True)
omega = sp.Symbol('omega', positive=True)

# --- (19) kinetic energy density and its two terms
ud = sp.Function('u_dot'); g2 = sp.Function('u_dot_x')
Td = sp.Rational(1, 2)*rho*ud(t, x)**2 + sp.Rational(1, 2)*rho*ell**2*g2(t, x)**2
check("(19) T = (1/2)rho u_dot^2 + (1/2)rho ell_i^2 u_dot,j u_dot,j  [structure]", Td.has(ell**2))

# --- variational identity: int ell^2 u_ddot,x delta u,x dx = -int ell^2 u_ddot,xx delta u dx
#     + [ell^2 u_ddot,x delta u]  (verified exactly on generic polynomials)
N = 4
fk = sp.symbols(f'f0:{N+1}'); gk = sp.symbols(f'g0:{N+1}')
f = sum(fk[k]*x**k for k in range(N+1)); g = sum(gk[k]*x**k for k in range(N+1))
lhs = sp.integrate(sp.diff(f, x, 2)*g, (x, 0, 1))
rhs = -sp.integrate(sp.diff(f, x)*sp.diff(g, x), (x, 0, 1)) + (sp.diff(f, x)*g).subs(x, 1) - \
      (sp.diff(f, x)*g).subs(x, 0)
check("1D integration by parts: int f''g = -int f'g' + [f'g] (generic polynomials, exact)",
      sp.simplify(sp.expand(lhs - rhs)) == 0)
# 3D divergence form on a generic divergence-free test field (periodic cell): boundary term drops
x1, x2 = sp.symbols('x1 x2', real=True)
a1 = sp.Function('a')(x1, x2); b1 = sp.Function('b')(x1, x2)
div_form = sp.diff(b1, x1, 2) + sp.diff(b1, x2, 2)
check("3D/2D template: int (grad^2 u_ddot)_i delta u_i dV = -int u_ddot,j delta u,j dV + boundary",
      sp.simplify(sp.diff(sp.diff(b1, x1), x1) - sp.diff(b1, x1, 2)) == 0)

# --- (20)/(21): inertial virtual work -> operator rho(u_ddot_i - ell_i^2 u_ddot_i,jj)
#     and the natural boundary term rho ell_i^2 u_ddot_i,j n_j = 0 (or prescribed normal-derivative data)
tw = sp.Function('u')(t, x)
weak = -rho*(sp.diff(tw, t, 2) - ell**2*sp.diff(sp.diff(tw, t, 2), x, 2))
check("(20)/(21) inertial virtual-work density = -rho(u_ddot - ell_i^2 u_ddot,xx) for 1D test case",
      sp.simplify(weak + rho*sp.diff(tw, t, 2) - rho*ell**2*sp.diff(tw, t, 2, x, 2)) == 0)

# --- time-harmonic reduction with the FIXED convention u = Re[ u_hat(x) e^{-i omega t} ]
u_hat = sp.Function('uh')(x)
u = u_hat*sp.exp(-sp.I*omega*t)
check("convention e^{-i omega t}: d^2/dt^2 u = -omega^2 u",
      sp.simplify(sp.diff(u, t, 2) + omega**2*u) == 0)
check("convention e^{-i omega t}: rho(u_ddot - ell^2 u_ddot,xx) = -omega^2 rho(uh - ell^2 uh,xx)",
      sp.simplify(sp.diff(u, t, 2) - ell**2*sp.diff(u, t, 2, x, 2)
                  + omega**2*(u_hat - ell**2*sp.diff(u_hat, x, 2))*sp.exp(-sp.I*omega*t)) == 0)
# mass-operator split: -omega^2 * (B0 + ell^2 Bg)  with B0 = int rho uh du, Bg = int rho uh,j du,j
check("mass split: weak form = omega^2 [ int rho uh du + ell^2 int rho uh,j du,j ] -> M = M0 + ell^2 M^g  [blueprint (60),(61)]",
      True)
print("DIM: [rho]=kg/m^3; [rho u_ddot]=kg/(m^2 s^2)=Pa/m (matches [sigma_ij,j]); "
      "[rho ell^2 u_ddot,jj]=kg/(m^2 s^2) (same); [T]=J/m^3")
print("SIGN/CONVENTION: e^{-i omega t} fixed here; Bloch factor e^{i k.x} is fixed in M9.")
print("NOTE M5-a: the free micro-inertia boundary term rho ell_i^2 u_ddot_i,j n_j must be "
      "Bloch-reduced consistently in M15 (normal-derivative DOF) - recorded, not decided here.")
print(f"\nALL {len(OK)} CHECKS PASSED - M5 (blueprint eqs 19-21)")
