"""P12E definitive diagnostic (complex-corrected): does the 32^2 solve honour its tolerance,
and what is the achievable double-precision accuracy floor?  Scratch only."""
import os, time
for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[v] = "1"
import numpy as np, importlib.util, math
from scipy.sparse.linalg import eigsh
spec = importlib.util.spec_from_file_location("p4b", "/home/user/repo/paper9/verification/suite/p4b_5g_to_5i.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
P = mod.PARAMS; L = P["Lcell"]; ell = math.sqrt(P["ell2"]); l_iso = P["l_iso"]
L11, L22, L12 = mod.L_plane(l_iso, l_iso, 0.0)
kx, ky = 0.31*np.pi/L, 0.22*np.pi/L
om_ex = math.sqrt(float(mod.ombar2_T(np.hypot(kx,ky)*L/np.pi, ell/L, mod.leff2_dir(l_iso,l_iso,0,0))))*mod.omega0(P["mu"],P["rho"],L)
Kh, Mh = mod.assemble_nxn_bloch(32, kx, ky, L, P["lam"], P["mu"], P["rho"], ell**2, L11, L22, L12)
print("matrix dtype:", Kh.dtype, "nd =", Kh.shape[0], "| hermitian err:", float(abs(Kh-Kh.getH()).max()))

print(f"{'tol':>7s} {'seed':>9s} {'time':>6s} {'|lam-RQ|/lam':>13s} {'||r||/|lam|':>12s} {'eta_rel(K)':>11s} {'omega_T':>19s} {'err32':>10s}")
for tol, seed in ((1e-12, 20260924), (1e-14, 20260924), (1e-15, 20260924)):
    t0=time.time()
    w, v = eigsh(Kh, k=4, M=Mh, which="SM", tol=tol, maxiter=20000,
                 v0=np.random.default_rng(seed).standard_normal(Kh.shape[0]))
    dt=time.time()-t0
    idx=np.argsort(w.real); w=w[idx]; v=v[:,idx]
    x=v[:,0]; lam=float(w[0].real)
    Kx=Kh@x; Mx=Mh@x
    r=Kx-lam*Mx
    nr=float(np.linalg.norm(r)); nK=float(np.linalg.norm(Kx))
    rq=float((x.conj()@Kx)/(x.conj()@Mx).real)
    om=math.sqrt(lam)
    print(f"{tol:>7.0e} {seed:>9d} {dt:>5.0f}s {abs(lam-rq)/lam:>13.3e} {nr/abs(lam):>12.3e} {nr/nK:>11.3e} {om:>19.16f} {abs(om-om_ex)/om_ex:>10.3e}", flush=True)
print()
print("ARPACK criterion: converged when ||r||/|theta| <= tol.  ||r||/|theta| >> tol means the")
print("requested tolerance was NOT achieved by the shift-invert path (accuracy-limited by the")
print("conditioning of the shifted operator, not by tol).")
