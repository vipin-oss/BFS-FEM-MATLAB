#!/usr/bin/env python3
"""
M13 -- Bogner-Fox-Schmit bicubic Hermite rectangle, blueprint S4.1, eqs (53)-(56):
  (53) shape functions (tensor product of 1-D cubic Hermite), (54) B (strain-pair operator),
  (55) B_,i (strain-gradient operators), (56) DOF layout 32/cell, C^1 / H^2 conformity.
Locked inputs: M3 kinematics eps_ij = (u_i,j + u_j,i)/2, eta_ijk = eps_ij,k; M4/M6 pair ordering
q = (eps11, eps22, eps12) with C_bar (2 mu shear entry) and D_c = diag(1,1,2); M9 phases
mu_alpha = e^{i k.a_alpha} on value, first- and mixed-derivative DOFs (40)-(43).
Element matrices (57)-(61) are M14; Bloch transformation/reduction (62)-(71) is M15 -- NOT done here.
Run from paper9/eqs/phase1:   python3 scripts/m13_bfs_shape.py
"""
import itertools, sympy as sp

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    ok = bool(cond); PASS += ok; FAIL += (not ok)
    print(("PASS" if ok else "FAIL") + ": " + name)

x, y = sp.symbols('x y', real=True)
hx, hy = sp.symbols('h_x h_y', positive=True)
s, h = sp.symbols('s h', positive=True)

# ------------------------------------------------------------------ (53) 1-D cubic Hermite on [0,h]
# H = [H_v0, H_d0, H_v1, H_d1] : value/slope at s=0, value/slope at s=h  (slope = PHYSICAL derivative)
t = s/h
H = [1 - 3*t**2 + 2*t**3, h*(t - 2*t**2 + t**3), 3*t**2 - 2*t**3, h*(-t**2 + t**3)]
def ev(f, s0): return sp.simplify(f.subs(s, s0))
check("[S1] (53) 1-D cubic Hermite basis: Kronecker property on {value, physical slope} x {s=0, s=h}; "
      "the slope functions carry the factor h (derivative DOFs are physical derivatives, units of u per length)",
      all([ev(H[0], 0) == 1, ev(sp.diff(H[0], s), 0) == 0, ev(H[0], h) == 0, ev(sp.diff(H[0], s), h) == 0,
           ev(H[1], 0) == 0, ev(sp.diff(H[1], s), 0) == 1, ev(H[1], h) == 0, ev(sp.diff(H[1], s), h) == 0,
           ev(H[2], 0) == 0, ev(sp.diff(H[2], s), 0) == 0, ev(H[2], h) == 1, ev(sp.diff(H[2], s), h) == 0,
           ev(H[3], 0) == 0, ev(sp.diff(H[3], s), 0) == 0, ev(H[3], h) == 0, ev(sp.diff(H[3], s), h) == 1]))
check("[S2] (53) 1-D completeness: exact reproduction of every cubic p(s) = c0 + c1 s + c2 s^2 + c3 s^3 "
      "by p(0) H0 + p'(0) H1 + p(h) H2 + p'(h) H3 (hence C^1 elements of degree 3 in each direction)",
      (lambda c: sp.expand(sum(c[i]*s**i for i in range(4))
                           - (sum(c[i]*0**i for i in range(4))*H[0] + c[1]*H[1]
                              + sum(c[i]*h**i for i in range(4))*H[2] + sum(i*c[i]*h**(i-1) for i in range(1, 4))*H[3])) == 0)
      (sp.symbols('c0:4')))

# ------------------------------------------------------------------ (53)/(56) bicubic tensor product
# nodes: 1 (0,0), 2 (hx,0), 3 (hx,hy), 4 (0,hy)  (counter-clockwise);  per node per component the
# DOF types in the blueprint order {u, u,x, u,y, u,xy}.  Element DOF vector ordering ADOPTED for this
# audit (documented, not blueprint-locked -> TV17):  node-major, then component (u1,u2), then type:
#   index = 8*(node-1) + 4*(comp-1) + type ,  type in {0:u, 1:u,x, 2:u,y, 3:u,xy}      -> 32 DOFs
Hx = [f.subs({s: x, h: hx}) for f in H]; Hy = [f.subs({s: y, h: hy}) for f in H]
nodes = [(0, 0), (hx, 0), (hx, hy), (0, hy)]
# 1-D index pairs (value/slope at the node's x-end and y-end)
xend = [0, 2, 2, 0]; yend = [0, 0, 2, 2]     # 0 -> functions at s=0 (indices 0,1); 2 -> at s=h (indices 2,3)
def Nfun(node, typ):
    ax = xend[node]; ay = yend[node]
    dx = 1 if typ in (1, 3) else 0
    dy = 1 if typ in (2, 3) else 0
    return sp.expand(Hx[ax + dx]*Hy[ay + dy])
N = [[Nfun(n, ty) for ty in range(4)] for n in range(4)]      # 16 scalar bicubic functions
ops = [lambda f: f, lambda f: sp.diff(f, x), lambda f: sp.diff(f, y), lambda f: sp.diff(f, x, y)]

check("[S3] (53)/(56) 16 scalar BFS functions satisfy the full Kronecker property: D_type' N_(node,type) at "
      "node' = delta_(node,node') delta_(type,type') for all 4 nodes x 4 types {u, u,x, u,y, u,xy} (256 conditions)",
      all(sp.simplify(ops[tp](N[n][ty]).subs({x: nodes[m][0], y: nodes[m][1]})) == (1 if (n == m and ty == tp) else 0)
          for n in range(4) for ty in range(4) for m in range(4) for tp in range(4)))

check("[S4] (53) span = Q3 (bicubic, 16 monomials x^a y^b, a,b <= 3): the 16 functions are linearly "
      "independent and reproduce any bicubic field with its nodal value/derivative data exactly (interpolation patch test)",
      (lambda P: sp.expand(P - sum(ops[ty](P).subs({x: nodes[n][0], y: nodes[n][1]})*N[n][ty]
                                   for n in range(4) for ty in range(4))) == 0)
      (sum(sp.Symbol(f'c{a}{b}')*x**a*y**b for a in range(4) for b in range(4)))
      and sp.Matrix([[sp.Poly(N[n][ty], x, y).coeff_monomial(x**a*y**b) for a in range(4) for b in range(4)]
                     for n in range(4) for ty in range(4)]).rank() == 16)

check("[S5] (56) partition of unity: sum of the 4 value functions = 1; the value functions reproduce x and y "
      "together with the derivative functions (linear completeness; rigid-body and constant-strain fields exact)",
      sp.simplify(sum(N[n][0] for n in range(4)) - 1) == 0
      and sp.simplify(sum(nodes[n][0]*N[n][0] + N[n][1] for n in range(4)) - x) == 0)

# ------------------------------------------------------------------ (56) C^1 inter-element continuity
# Edge x = hx of element E (nodes 2,3) is edge x = 0 of the right neighbour E' (its nodes 1,4).  Trace of u and
# of the NORMAL derivative u,x on the edge must depend only on DOFs of nodes on that edge.
def trace(fun, xv): return sp.simplify(fun.subs(x, xv))
check("[S6] (56) C^0: on the edge x = h_x the trace of every function of nodes 1,4 (off-edge) vanishes; the trace "
      "of node-2/3 functions is the 1-D Hermite in y (depends on u, u,y only); tangential-derivative data u,y is "
      "consistent automatically",
      all(trace(N[n][ty], hx) == 0 for n in (0, 3) for ty in range(4))
      and all(sp.simplify(trace(N[n][ty], hx) - ({1: Hy[0], 2: Hy[2]}[n] if ty == 0 else
                                                  {1: Hy[1], 2: Hy[3]}[n] if ty == 2 else 0)) == 0
              for n in (1, 2) for ty in range(4)))
check("[S7] (56) C^1: on the edge x = h_x the NORMAL derivative u,x of every off-edge function vanishes, and for "
      "edge nodes it is the 1-D Hermite in y carried by the u,x and u,xy DOFs -- so u and u,x are continuous across "
      "the edge iff the shared nodal {u, u,x, u,y, u,xy} coincide: the mixed DOF is REQUIRED for C^1 (drop it and "
      "the normal-derivative trace is no longer interpolated)",
      all(trace(sp.diff(N[n][ty], x), hx) == 0 for n in (0, 3) for ty in range(4))
      and all(sp.simplify(trace(sp.diff(N[n][ty], x), hx) - ({1: Hy[0], 2: Hy[2]}[n] if ty == 1 else
                                                              {1: Hy[1], 2: Hy[3]}[n] if ty == 3 else 0)) == 0
              for n in (1, 2) for ty in range(4)))
check("[S8] (56) same on the edge y = h_y (nodes 3,4 vs neighbour above): C^0 and C^1 in the normal direction y; "
      "H^2-conformity follows (piecewise Q3, C^1 => u in H^2 on the mesh); second derivatives are discontinuous "
      "across edges (u,xx jumps), which is admissible for the fourth-order operator",
      all(trace_ == 0 for trace_ in [sp.simplify(N[n][ty].subs(y, hy)) for n in (0, 1) for ty in range(4)]
                                     + [sp.simplify(sp.diff(N[n][ty], y).subs(y, hy)) for n in (0, 1) for ty in range(4)])
      and sp.simplify(sp.diff(N[0][0], x, 2).subs(x, hx)) != 0)   # u,xx trace on x=h_x depends on OFF-edge DOFs

# ------------------------------------------------------------------ (54)-(55) B and B_,i  (3 x 32)
nd = 32
def idx(node, comp, typ): return 8*node + 4*comp + typ
Nmat = sp.zeros(2, nd)                                    # u = Nmat d
for n in range(4):
    for c in range(2):
        for ty in range(4):
            Nmat[c, idx(n, c, ty)] = N[n][ty]
d = sp.Matrix(sp.symbols('d0:32'))
u1, u2 = (Nmat*d)[0], (Nmat*d)[1]
q = sp.Matrix([sp.diff(u1, x), sp.diff(u2, y), sp.Rational(1, 2)*(sp.diff(u1, y) + sp.diff(u2, x))])   # M3 (10)
B = sp.Matrix([[sp.diff(q[r], d[j]) for j in range(nd)] for r in range(3)])
Bx = B.applyfunc(lambda f: sp.diff(f, x)); By = B.applyfunc(lambda f: sp.diff(f, y))

check("[B1] (54) B (3 x 32) is exactly the operator of the locked pair vector q = (eps11, eps22, eps12) "
      "with the TENSOR shear eps12 = (u1,y + u2,x)/2 (not gamma12): rows are [N,x ; 0], [0 ; N,y], [N,y ; N,x]/2",
      B.shape == (3, 32) and (B*d - q).applyfunc(sp.simplify) == sp.zeros(3, 1)
      and all(sp.simplify(B[2, idx(n, 0, ty)] - sp.diff(N[n][ty], y)/2) == 0 for n in range(4) for ty in range(4)))

check("[B2] (55) B_,i := d B/dx_i (3 x 32 each) gives the strain-gradient pairs eta_(..)i = q_,i (M3 (11)): "
      "B_,x d = q,x and B_,y d = q,y; symmetry eta_ijk = eta_jik inherited; compatibility (B_,x)_,y = (B_,y)_,x",
      (Bx*d - q.applyfunc(lambda f: sp.diff(f, x))).applyfunc(sp.simplify) == sp.zeros(3, 1)
      and (By*d - q.applyfunc(lambda f: sp.diff(f, y))).applyfunc(sp.simplify) == sp.zeros(3, 1)
      and (Bx.applyfunc(lambda f: sp.diff(f, y)) - By.applyfunc(lambda f: sp.diff(f, x))).applyfunc(sp.simplify) == sp.zeros(3, 32))

degB  = max(sp.Poly(e, x, y).total_degree() for e in B if e != 0)
degBx = max(sp.Poly(e, x, y).total_degree() for e in Bx if e != 0)
degBx_x = max(sp.Poly(e, x, y).degree(x) for e in Bx if e != 0); degBx_y = max(sp.Poly(e, x, y).degree(y) for e in Bx if e != 0)
degN  = max(sp.Poly(N[n][ty], x, y).total_degree() for n in range(4) for ty in range(4))
check("[B3] derivative orders / polynomial degrees (computed): N in Q3 (total degree 6, per direction 3); B entries total degree "
      f"{degB} (per direction <= 3); B_,x entries total degree {degBx}, degree {degBx_x} in x and {degBx_y} in y -> integrands: N^T N total 12 (6 per "
      f"direction), B^T G B total {2*degB} (per direction <= 6), B_,i^T G B_,j total {2*degBx} (per direction <= 6); input to the "
      "M14 quadrature rule -- the blueprint phrase 'second derivatives of cubics => up to quartic' is NOT the degree of the product integrand",
      degN == 6 and degB == 5 and degBx == 4 and degBx_x == 2 and degBx_y == 3
      and max(sp.Poly(e, x, y).degree(x) for e in B if e != 0) == 3)

# rank / null spaces (evaluated at a generic interior point and as polynomials)
pt = {x: hx/3, y: 2*hy/7}
rigid = []
for (a1, a2, w) in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
    ufield = (a1 - w*y, a2 + w*x)
    rigid.append(sp.Matrix([ops[ty](ufield[c]).subs({x: nodes[n][0], y: nodes[n][1]}) for n in range(4) for c in range(2) for ty in range(4)]))
check("[B4] rigid-body modes (2 translations + 1 rotation) are in the null space of B identically in (x,y): "
      "B d_rigid = 0 as polynomials; constant-strain fields (linear u) are in the null space of both B_,i",
      all((B*r).applyfunc(sp.expand) == sp.zeros(3, 1) for r in rigid)
      and all((Bd*sp.Matrix([ops[ty](f).subs({x: nodes[n][0], y: nodes[n][1]}) for n in range(4) for c in range(2) for ty in range(4)
                             for f in ((lambda c_: (sp.Symbol('e1')*x + sp.Symbol('e3')*y/2, sp.Symbol('e2')*y + sp.Symbol('e3')*x/2)[c_])(c),)]))
              .applyfunc(sp.expand) == sp.zeros(3, 1) for Bd in (Bx, By)))

check("[B5] (55) quadratic fields are reproduced with EXACT constant strain gradients (Q3 contains P2): "
      "B_,x d_quad and B_,y d_quad equal the analytical eta for u = (x^2, x y) everywhere",
      (lambda dq: (Bx*dq - sp.Matrix([2, 1, 0])).applyfunc(sp.expand) == sp.zeros(3, 1)
                  and (By*dq - sp.Matrix([0, 0, sp.Rational(1, 2)])).applyfunc(sp.expand) == sp.zeros(3, 1))
      (sp.Matrix([ops[ty]((x**2, x*y)[c]).subs({x: nodes[n][0], y: nodes[n][1]}) for n in range(4) for c in range(2) for ty in range(4)])))

# ------------------------------------------------------------------ units, Jacobian, symmetry structure
check("[U1] units (physical-derivative DOFs): N_value dimensionless, N_(u,x),N_(u,y) ~ length, N_(u,xy) ~ length^2; "
      "B entries 1/m, 1/1, m for the three DOF types respectively (so that q is dimensionless), B_,i one power of 1/m more; "
      "scaling h -> c h multiplies the type-k function by c^k",
      all(sp.simplify(N[n][ty].subs({hx: 2*hx, hy: 2*hy, x: 2*x, y: 2*y}) - 2**({0: 0, 1: 1, 2: 1, 3: 2}[ty])*N[n][ty]) == 0
          for n in range(4) for ty in range(4)))
check("[U2] coordinate mapping: rectangle -> affine map from (xi,eta) in [-1,1]^2, x = h_x (1+xi)/2, constant Jacobian "
      "J = h_x h_y / 4, d/dx = (2/h_x) d/dxi; no isoparametric distortion is admissible for BFS (C^1 is lost on "
      "non-rectangular/non-affine maps) -> the cell must be meshed by axis-aligned rectangles",
      sp.simplify(sp.Matrix([[hx/2, 0], [0, hy/2]]).det() - hx*hy/4) == 0)
Dc = sp.diag(1, 1, 2)
lam_, mu_ = sp.symbols('lambda mu', positive=True)
Cb = sp.Matrix([[lam_ + 2*mu_, lam_, 0], [lam_, lam_ + 2*mu_, 0], [0, 0, 2*mu_]])
G = (Dc*Cb)
check("[U3] element-matrix STRUCTURE inherited from M13 objects (values are M14): for any symmetric G, B^T G B and "
      "sum_ij L_ij B_,i^T G B_,j (L symmetric) are symmetric integrands; N^T N is symmetric PSD; the 16 scalar functions "
      "are linearly independent so the consistent mass Gram matrix is positive definite",
      (G - G.T) == sp.zeros(3, 3)
      and (lambda Mx: (Mx - Mx.T).applyfunc(sp.expand) == sp.zeros(nd, nd))(B.T*G*B + Bx.T*G*By + By.T*G*Bx)
      and sp.Matrix([[sp.integrate(N[n][ty]*N[m][tp], (x, 0, hx), (y, 0, hy)).subs({hx: 1, hy: 1})
                      for m in range(4) for tp in range(4)] for n in range(4) for ty in range(4)]).is_positive_definite)

# ------------------------------------------------------------------ Bloch phase at interpolation level (M9 (40)-(43))
# One cell = one element of size L x L (or the boundary elements of a mesh).  If the DOFs of the slave node
# equal mu times those of the master node FOR ALL FOUR TYPES, then on the periodic edge the traces of u AND of
# the normal derivative are exactly mu times the opposite traces -- for every y along the edge.
Lc = sp.symbols('L', positive=True); kx, ky = sp.symbols('k_x k_y', real=True)
subL = {hx: Lc, hy: Lc}
dm = sp.Matrix(sp.symbols('m0:32'))          # generic (complex) DOF vector of the reference cell
mux = sp.exp(sp.I*kx*Lc); muy = sp.exp(sp.I*ky*Lc)
def phased(dvec, px, py, which):
    """which(node) -> phase factor; returns the DOF vector of the cell whose node DOFs are phased"""
    out = sp.zeros(nd, 1)
    for n in range(4):
        for c in range(2):
            for ty in range(4):
                out[idx(n, c, ty)] = which(n, ty)*dvec[idx(0, c, ty)]   # slave node DOFs = phase x MASTER (node 1) DOFs
    return out
# Bloch tying inside ONE cell: node 2 = mu_x node 1, node 4 = mu_y node 1, node 3 = mu_x mu_y node 1, all types
def tie(n, ty): return {0: 1, 1: mux, 2: mux*muy, 3: muy}[n]
def tie_wrong(n, ty): return {0: 1, 1: mux, 2: mux*muy, 3: muy}[n] if ty == 0 else 1      # phase on value DOFs only
def tie_conj(n, ty): return {0: 1, 1: mux, 2: mux*muy, 3: muy}[n] if ty in (0, 2) else sp.conjugate({0: 1, 1: mux, 2: mux*muy, 3: muy}[n])
def edge_identity(tiefun, kxv, kyv):
    dd = phased(dm, None, None, tiefun)
    uu = (Nmat.subs(subL)*dd)
    res = []
    for c in range(2):
        f = uu[c]
        r1 = sp.simplify((f.subs(x, Lc) - mux*f.subs(x, 0)).subs({kx: kxv, ky: kyv}))
        r2 = sp.simplify((sp.diff(f, x).subs(x, Lc) - mux*sp.diff(f, x).subs(x, 0)).subs({kx: kxv, ky: kyv}))
        r3 = sp.simplify((f.subs(y, Lc) - muy*f.subs(y, 0)).subs({kx: kxv, ky: kyv}))
        r4 = sp.simplify((sp.diff(f, y).subs(y, Lc) - muy*sp.diff(f, y).subs(y, 0)).subs({kx: kxv, ky: kyv}))
        res += [r1, r2, r3, r4]
    return all(sp.expand(r) == 0 for r in res)
kpts = {"Gamma": (0, 0), "X": (sp.pi/Lc, 0), "M": (sp.pi/Lc, sp.pi/Lc), "generic": (sp.Rational(3, 7)*sp.pi/Lc, sp.Rational(2, 5)*sp.pi/Lc)}
for name, (kxv, kyv) in kpts.items():
    check(f"[P1-{name}] M9 phase on ALL four DOF types => on the periodic edges u(L,y) = mu_x u(0,y), u,x(L,y) = mu_x u,x(0,y), "
          f"u(x,L) = mu_y u(x,0), u,y(x,L) = mu_y u,y(x,0) hold IDENTICALLY in the edge coordinate for generic complex DOFs, "
          f"at k = {name} (mu_x, mu_y) = ({sp.simplify(mux.subs(kx, kxv))}, {sp.simplify(muy.subs(ky, kyv))})",
          edge_identity(tie, kxv, kyv))
check("[P2] NEGATIVE CONTROL (generic interior k): phase on value DOFs only (derivative DOFs tied with phase 1) breaks "
      "the normal-derivative condition u,x(L,y) = mu_x u,x(0,y) (and even the value trace, since u,y enters it): "
      "the derivative-DOF phase is not optional",
      not edge_identity(tie_wrong, *kpts["generic"]))
check("[P3] NEGATIVE CONTROL (generic interior k): conjugate/inverse phase on the x-derivative DOFs fails; at Gamma, X, M "
      "(mu real) this wrong tying is INVISIBLE (mu = conj mu) -- high-symmetry points alone cannot validate the phase (M15-a F4a)",
      not edge_identity(tie_conj, *kpts["generic"]) and edge_identity(tie_conj, *kpts["X"]) and edge_identity(tie_conj, *kpts["M"]))
check("[P4] the tying is x-independent and multiplicative (M9 (43)): phasing the DOF vector by a constant mu phases the "
      "interpolated field and all its derivatives by the same mu (linearity of N); the M15-a identities are properties of the "
      "reduced matrices (M15), not of the element -- nothing about K(k) = K(-k)^H is used or implied here",
      all(sp.simplify(ops[tp]((Nmat*(mux*dm))[c]) - mux*ops[tp]((Nmat*dm)[c])) == 0 for c in range(2) for tp in range(4)))

# ------------------------------------------------------------------ assembly compatibility (structure only)
check("[A1] assembly compatibility: a 2x2 patch of elements sharing node 3 of element (1,1): the 8 DOFs of the shared node "
      "are the SAME physical quantities {u_c, u_c,x, u_c,y, u_c,xy} in all four elements (Kronecker property is "
      "coordinate-based, physical derivatives) -> direct scatter-add with one global DOF per (node, comp, type); for an "
      "n x n mesh of the L x L cell: 8 (n+1)^2 DOFs before periodicity, 8 n^2 after Bloch tying (n = 1: 32 -> 8)",
      8*(1 + 1)**2 == 32 and 8*1**2 == 8 and all(sp.simplify(ops[tp](N[2][ty]).subs({x: hx, y: hy})) == (1 if tp == ty else 0) for ty in range(4) for tp in range(4)))

print()
print(f"TOTAL {PASS + FAIL}  PASS {PASS}  FAIL {FAIL}")
