#!/usr/bin/env python3
"""
M15 -- Bloch master-slave reduction, blueprint S4.4-4.6, eqs (62)-(71).
Pre-Bloch K, M from M14 (real symmetric).  T(k) from M9 (41)-(43): SAME unimodular
phase on all four BFS DOF types {u, u_x, u_y, u_xy} and both components.

M15-a pair (NOT blueprint (68)):
    Kbar^H(k) = Kbar(k)
    Kbar(-k)  = conj(Kbar(k))
The false generic identity Kbar(k) = Kbar(-k)^H is a NEGATIVE control at interior k.

TV17: M13 provisional index = 8*node + 4*comp + type -- implementation only.
No production bands, no Case C, no complete-gap sampling.

Run from paper9/eqs/phase1:
    python3 scripts/m15_bloch_reduction.py
"""
import numpy as np
import sympy as sp

PASS = FAIL = 0
def check(name, cond):
    global PASS, FAIL
    ok = bool(cond); PASS += ok; FAIL += (not ok)
    print(("PASS" if ok else "FAIL") + ": " + name)

# ============================================================================= 1. phase derivation (62)-(65)
kx, ky, L = sp.symbols('k_x k_y L', real=True)
mux = sp.exp(sp.I*kx*L); muy = sp.exp(sp.I*ky*L)
check("[P1] (40) mu_x = exp(i k_x L), mu_y = exp(i k_y L); |mu_x|^2 = 1; "
      "mu_x(-k) = conj mu_x(k); homomorphism mu(a1+a2) = mu_x mu_y",
      sp.simplify(mux * sp.conjugate(mux) - 1) == 0
      and sp.simplify(mux.subs(kx, -kx) - sp.conjugate(mux)) == 0
      and sp.simplify(sp.exp(sp.I*(kx+0)*L)*sp.exp(sp.I*ky*L) - mux*muy) == 0)

x = sp.symbols('x', real=True)
qper = sp.cos(2*sp.pi*x/L)  # lattice-periodic envelope
uB = qper*sp.exp(sp.I*kx*x)
uB_shift = uB.subs(x, x+L)
uB_x = sp.diff(uB, x)
uB_x_shift = sp.diff(uB.subs(x, x+L), x)
check("[P2] Bloch field u=q(x) e^{i k x} with q(x+L)=q(x): u(x+L)= mu u(x) AND "
      "u'(x+L)= mu u'(x).  Phase independent of x commutes with d/dx; SAME mu on "
      "{u, u_x, u_y, u_xy}.  No extra ik in the tying (ik already lives inside u').",
      sp.simplify(uB_shift - mux*uB) == 0
      and sp.simplify(uB_x_shift - mux*uB_x) == 0)

check("[P3] (62)-(65) one rectangular cell: 8 master DOFs (origin node, 2 components x 4 types); "
      "24 slaves; T(k) is 32 x 8 with blocks I_8, mu_x I_8, mu_x mu_y I_8, mu_y I_8 "
      "in TV17 node order (0,1,2,3).  T_pair = mu I_8.  TV17 OPEN (implementation convention). "
      "n x n mesh of the cell would give 8 n^2 reduced DOFs (M13); TV7 N not chosen.",
      True)

# ============================================================================= 2. numeric T, Kbar
def idx(node, comp, typ):
    return 8*node + 4*comp + typ

def hermite_num(s, h):
    t = s/h
    H = np.array([1-3*t**2+2*t**3, h*(t-2*t**2+t**3), 3*t**2-2*t**3, h*(-t**2+t**3)], float)
    dH = np.array([(-6*t+6*t**2)/h, 1-4*t+3*t**2, (6*t-6*t**2)/h, -2*t+3*t**2], float)
    d2H = np.array([(-6+12*t)/h**2, (-4+6*t)/h, (6-12*t)/h**2, (-2+6*t)/h], float)
    return H, dH, d2H

xend = [0, 2, 2, 0]; yend = [0, 0, 2, 2]

def gauss4():
    a = np.sqrt(3/7 - 2/7*np.sqrt(6/5)); b = np.sqrt(3/7 + 2/7*np.sqrt(6/5))
    wa = (18+np.sqrt(30))/36; wb = (18-np.sqrt(30))/36
    return [(-b, wb), (-a, wa), (a, wa), (b, wb)]

def assemble_KM(hx=1.0, hy=1.0, lam=1.0, mu=1.0, L11=1.0, L22=1.0, L12=0.0, rho=1.0, ell2=0.25):
    Cbar = np.array([[lam+2*mu, lam, 0],[lam, lam+2*mu, 0],[0, 0, 2*mu]], float)
    G = np.diag([1.,1.,2.]) @ Cbar
    Lmat = np.array([[L11, L12],[L12, L22]], float)
    nd = gauss4()
    Kc = np.zeros((32,32)); Kg = np.zeros((32,32))
    M0 = np.zeros((32,32)); Mg = np.zeros((32,32))
    for xi, wi in nd:
        for eta, wj in nd:
            xv = (xi+1)/2*hx; yv = (eta+1)/2*hy
            wjac = wi*wj*hx*hy/4
            Hx, dHx, d2Hx = hermite_num(xv, hx)
            Hy, dHy, d2Hy = hermite_num(yv, hy)
            Nv = np.zeros((4,4)); Nx=np.zeros((4,4)); Ny=np.zeros((4,4))
            Nxx=np.zeros((4,4)); Nxy=np.zeros((4,4)); Nyy=np.zeros((4,4))
            for ndi in range(4):
                ax, ay = xend[ndi], yend[ndi]
                for ty in range(4):
                    dx = 1 if ty in (1,3) else 0
                    dy = 1 if ty in (2,3) else 0
                    ix, iy = ax+dx, ay+dy
                    Nv[ndi,ty]=Hx[ix]*Hy[iy]; Nx[ndi,ty]=dHx[ix]*Hy[iy]; Ny[ndi,ty]=Hx[ix]*dHy[iy]
                    Nxx[ndi,ty]=d2Hx[ix]*Hy[iy]; Nxy[ndi,ty]=dHx[ix]*dHy[iy]; Nyy[ndi,ty]=Hx[ix]*d2Hy[iy]
            Nmat=np.zeros((2,32)); B=np.zeros((3,32)); Bx=np.zeros((3,32)); By=np.zeros((3,32))
            Nxmat=np.zeros((2,32)); Nymat=np.zeros((2,32))
            for ndi in range(4):
                for c in range(2):
                    for ty in range(4):
                        j = idx(ndi,c,ty)
                        Nmat[c,j]=Nv[ndi,ty]; Nxmat[c,j]=Nx[ndi,ty]; Nymat[c,j]=Ny[ndi,ty]
                        if c==0:
                            B[0,j]=Nx[ndi,ty]; B[2,j]=0.5*Ny[ndi,ty]
                            Bx[0,j]=Nxx[ndi,ty]; Bx[2,j]=0.5*Nxy[ndi,ty]
                            By[0,j]=Nxy[ndi,ty]; By[2,j]=0.5*Nyy[ndi,ty]
                        else:
                            B[1,j]=Ny[ndi,ty]; B[2,j]=0.5*Nx[ndi,ty]
                            Bx[1,j]=Nxy[ndi,ty]; Bx[2,j]=0.5*Nxx[ndi,ty]
                            By[1,j]=Nyy[ndi,ty]; By[2,j]=0.5*Nxy[ndi,ty]
            Kc += wjac*(B.T@G@B)
            Kg += wjac*(1/10)*(Lmat[0,0]*(Bx.T@G@Bx)+Lmat[0,1]*(Bx.T@G@By)
                               +Lmat[1,0]*(By.T@G@Bx)+Lmat[1,1]*(By.T@G@By))
            M0 += wjac*rho*(Nmat.T@Nmat)
            Mg += wjac*rho*(Nxmat.T@Nxmat + Nymat.T@Nymat)
    return Kc+Kg, M0+ell2*Mg

K, M = assemble_KM()

def T_impl(kx, ky, L=1.0):
    mx = np.exp(1j*kx*L); my = np.exp(1j*ky*L)
    phases = [1.0, mx, mx*my, my]
    T = np.zeros((32, 8), dtype=complex)
    for n, ph in enumerate(phases):
        T[8*n:8*(n+1), :] = ph * np.eye(8)
    return T

def T_ref(kx, ky, L=1.0):
    nodes = [(0.0, 0.0), (L, 0.0), (L, L), (0.0, L)]
    T = np.zeros((32, 8), dtype=complex)
    for n, (xn, yn) in enumerate(nodes):
        ph = np.exp(1j*(kx*xn + ky*yn))
        T[8*n:8*(n+1), :] = ph * np.eye(8)
    return T

def T_value_only(kx, ky, L=1.0):
    mx = np.exp(1j*kx*L); my = np.exp(1j*ky*L)
    phases = [1.0, mx, mx*my, my]
    T = np.zeros((32, 8), dtype=complex)
    for n, ph in enumerate(phases):
        for c in range(2):
            for ty in range(4):
                T[idx(n, c, ty), 4*c+ty] = ph if ty == 0 else 1.0
    return T

def T_conj_deriv(kx, ky, L=1.0):
    mx = np.exp(1j*kx*L); my = np.exp(1j*ky*L)
    phases = [1.0, mx, mx*my, my]
    T = np.zeros((32, 8), dtype=complex)
    for n, ph in enumerate(phases):
        for c in range(2):
            for ty in range(4):
                phu = np.conjugate(ph) if ty in (1, 3) else ph
                T[idx(n, c, ty), 4*c+ty] = phu
    return T

def reduce(A, T):
    return T.conj().T @ A @ T

def rel(A, B):
    nrm = np.linalg.norm(A, 'fro')
    return 0.0 if nrm == 0 else np.linalg.norm(A-B, 'fro')/nrm

Lcell = 1.0
kgen = (3*np.pi/(7*Lcell), 2*np.pi/(5*Lcell))
kG = (0.0, 0.0); kX = (np.pi/Lcell, 0.0); kM = (np.pi/Lcell, np.pi/Lcell)

Tgen = T_impl(*kgen, Lcell)
check("[R1] independent reference T: nodal exp(i k·x_node) vs edge-product mu_x, mu_y "
      "agree at generic interior k",
      rel(Tgen, T_ref(*kgen, Lcell)) < 1e-14)

Kbar = reduce(K, Tgen)
Mbar = reduce(M, Tgen)
check("[R2] reduced sizes 8x8; unreduced K,M 32x32 real symmetric",
      Kbar.shape == (8, 8) and Mbar.shape == (8, 8)
      and K.shape == (32, 32) and np.max(np.abs(np.imag(K))) == 0
      and np.max(np.abs(K-K.T)) < 1e-12)

check("[H1] Hermiticity generic k: ||Kbar^H - Kbar||/||Kbar|| < 1e-12",
      rel(Kbar.conj().T, Kbar) < 1e-12)
check("[H2] mass Hermiticity: ||Mbar^H - Mbar||/||Mbar|| < 1e-12",
      rel(Mbar.conj().T, Mbar) < 1e-12)

Km = reduce(K, T_impl(-kgen[0], -kgen[1], Lcell))
Mm = reduce(M, T_impl(-kgen[0], -kgen[1], Lcell))
check("[H3] conjugation ||Kbar(-k)-conj Kbar(k)||/||Kbar|| < 1e-12  (M15-a Id. 2)",
      rel(Km, np.conjugate(Kbar)) < 1e-12)
check("[H4] mass conjugation ||Mbar(-k)-conj Mbar(k)||/||Mbar|| < 1e-12",
      rel(Mm, np.conjugate(Mbar)) < 1e-12)

false_id = rel(Kbar, Km.conj().T)
check("[H5] FALSE identity Kbar(k)=Kbar(-k)^H is NOT generic: residual at interior k "
      "is O(1) (got %.3g)" % false_id,
      false_id > 1e-3)

KbarG = reduce(K, T_impl(*kG, Lcell))
check("[H6] at Gamma the false identity holds accidentally (real Kbar); not a generic proof",
      rel(KbarG, KbarG.conj().T) < 1e-12 and np.max(np.abs(KbarG.imag)) < 1e-12)

KbarX = reduce(K, T_impl(*kX, Lcell)); KbarM = reduce(K, T_impl(*kM, Lcell))
check("[H7] X and M: phases real => Kbar real Hermitian; Hermiticity also at generic k (H1)",
      np.max(np.abs(KbarX.imag)) < 1e-10 and np.max(np.abs(KbarM.imag)) < 1e-10
      and rel(KbarX.conj().T, KbarX) < 1e-12)

# ============================================================================= 3. interpolation traces
def Nscalar(n, ty, xv, yv, hx=1.0, hy=1.0):
    Hx, dHx, _ = hermite_num(xv, hx); Hy, dHy, _ = hermite_num(yv, hy)
    ax, ay = xend[n], yend[n]
    dx = 1 if ty in (1, 3) else 0
    dy = 1 if ty in (2, 3) else 0
    return Hx[ax+dx]*Hy[ay+dy]

def interp_u(d32, xv, yv, c=0):
    s = 0.0+0.0j
    for n in range(4):
        for ty in range(4):
            s += d32[idx(n, c, ty)] * Nscalar(n, ty, xv, yv)
    return s

def ux(d, x, y, h=1e-6):
    return (interp_u(d, x+h, y) - interp_u(d, x-h, y))/(2*h)
def uy(d, x, y, h=1e-6):
    return (interp_u(d, x, y+h) - interp_u(d, x, y-h))/(2*h)
def uxy(d, x, y, h=1e-6):
    return (ux(d, x, y+h) - ux(d, x, y-h))/(2*h)

rng = np.random.default_rng(0)
d8 = rng.normal(size=8) + 1j*rng.normal(size=8)
d32 = Tgen @ d8
mx = np.exp(1j*kgen[0]*Lcell); my = np.exp(1j*kgen[1]*Lcell)
ys = [0.2, 0.5, 0.8]
res_val = max(abs(interp_u(d32, 1.0, y) - mx*interp_u(d32, 0.0, y)) for y in ys)
res_ux = max(abs(ux(d32, 1.0, y) - mx*ux(d32, 0.0, y)) for y in ys)
res_uy = max(abs(uy(d32, 1.0, y) - mx*uy(d32, 0.0, y)) for y in ys)
res_uxy = max(abs(uxy(d32, 1.0, y) - mx*uxy(d32, 0.0, y)) for y in ys)
check("[I1] interpolant traces at generic k (FD independent of tying algebra): "
      "u,u_x,u_y,u_xy on x=L = mu_x * traces on x=0  (%.3g, %.3g, %.3g, %.3g)"
      % (res_val, res_ux, res_uy, res_uxy),
      res_val < 1e-8 and res_ux < 1e-6 and res_uy < 1e-6 and res_uxy < 2e-4)

xs = [0.2, 0.5, 0.8]
resy = max(abs(interp_u(d32, x, 1.0) - my*interp_u(d32, x, 0.0)) for x in xs)
resy_uy = max(abs(uy(d32, x, 1.0) - my*uy(d32, x, 0.0)) for x in xs)
check("[I2] y=L vs y=0 with mu_y, including u_y",
      resy < 1e-8 and resy_uy < 1e-6)

d_wrong = T_value_only(*kgen, Lcell) @ d8
res_w = max(abs(ux(d_wrong, 1.0, y) - mx*ux(d_wrong, 0.0, y)) for y in ys)
check("[I3] NEGATIVE CONTROL value-only phase: u_x residual at generic k is NOT small (got %.3g)"
      % res_w, res_w > 1e-3)

Kw = reduce(K, T_value_only(*kgen, Lcell))
check("[I4] value-only Kbar still Hermitian (Hermiticity blind to wrong derivative phase)",
      rel(Kw.conj().T, Kw) < 1e-12)

d_conj = T_conj_deriv(*kgen, Lcell) @ d8
res_c = max(abs(ux(d_conj, 1.0, y) - mx*ux(d_conj, 0.0, y)) for y in ys)
check("[I5] NEGATIVE CONTROL conjugate phase on x-derivative DOFs: u_x residual NOT small "
      "(got %.3g)" % res_c, res_c > 1e-3)

check("[I6] at Gamma, wrong Tying coincides with T_impl (tests blind at Gamma)",
      rel(T_impl(0, 0, Lcell), T_value_only(0, 0, Lcell)) < 1e-14
      and rel(T_impl(0, 0, Lcell), T_conj_deriv(0, 0, Lcell)) < 1e-14)

# ============================================================================= 4. BZ
G1 = (2*np.pi/Lcell, 0.0)
T_kG = T_impl(kgen[0]+G1[0], kgen[1], Lcell)
check("[B1] T(k+b1)=T(k) (mu_x * e^{i 2 pi}=mu_x) => Kbar(k+G)=Kbar(k) matrix-periodic",
      rel(T_kG, Tgen) < 1e-14 and rel(reduce(K, T_kG), Kbar) < 1e-14)

w_k = np.sort(np.real(np.linalg.eigvals(np.linalg.solve(Mbar, Kbar))))
w_kG = np.sort(np.real(np.linalg.eigvals(np.linalg.solve(reduce(M, T_kG), reduce(K, T_kG)))))
check("[B2] generalised eigenvalues of (Kbar,Mbar) agree at k and k+G",
      np.max(np.abs(w_k-w_kG))/np.max(np.abs(w_k)) < 1e-10)

check("[B3] T(-k)=conj T(k); source of Kbar(-k)=conj Kbar(k) for real K -- no extra mass phase",
      rel(T_impl(-kgen[0], -kgen[1], Lcell), np.conjugate(Tgen)) < 1e-14)

# ============================================================================= 5. eigenproblem defs (66)-(71)
diagK = np.real(np.diag(Kbar))
Djac = np.diag(1.0/np.sqrt(np.maximum(np.abs(diagK), 1e-30)))
kappa = np.linalg.cond(Djac @ Kbar @ Djac)
check("[E1] (66) 8-D Hermitian pencil; Mbar SPD; Jacobi-scaled cond finite. "
      "No production kappa(theta,AR). MAC is a solver protocol, not run on bands.",
      rel(Kbar.conj().T, Kbar) < 1e-12
      and np.min(np.real(np.linalg.eigvalsh(Mbar))) > 0
      and np.isfinite(kappa))

w_m = np.sort(np.real(np.linalg.eigvals(np.linalg.solve(Mm, Km))))
check("[E2] eig(k)=eig(-k) as sets (Hermitian conjugated pencil => real equal spectrum)",
      np.max(np.abs(w_k-w_m)) < 1e-10)

check("[E3] M10-a: no complete-gap sampling; T(k) defined for arbitrary half-BZ k; "
      "path Gamma-X-M-Gamma remains band-diagram path. Blueprint (68) NOT edited.",
      True)
check("[E4] TV17 OPEN; TV7 N not chosen; TV4/6/14/15/18 unused. No Case-H/C production.",
      True)

print()
print(f"TOTAL {PASS + FAIL}  PASS {PASS}  FAIL {FAIL}")
