"""P12E discriminative diagnostic: is the 32^2 off-trend value a property of THIS k
(superconvergence) or a solver accuracy floor?  Test: repeat the mesh sequence at a
different k with the same authorized configuration.  Scratch only."""
import os, time
for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[v] = "1"
import numpy as np, importlib.util, math
from scipy.sparse.linalg import eigsh
spec = importlib.util.spec_from_file_location("p4b", "/home/user/repo/paper9/verification/suite/p4b_5g_to_5i.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
P = mod.PARAMS; L = P["Lcell"]; ell = math.sqrt(P["ell2"]); l_iso = P["l_iso"]
L11, L22, L12 = mod.L_plane(l_iso, l_iso, 0.0)
le2 = mod.leff2_dir(l_iso, l_iso, 0.0, 0.0)
w0 = mod.omega0(P["mu"], P["rho"], L)

def run(kx, ky, n, tol, seed):
    om_ex = math.sqrt(float(mod.ombar2_T(np.hypot(kx,ky)*L/np.pi, ell/L, le2)))*w0
    Kh, Mh = mod.assemble_nxn_bloch(n, kx, ky, L, P["lam"], P["mu"], P["rho"], ell**2, L11, L22, L12)
    t0=time.time()
    w,_ = eigsh(Kh, k=4, M=Mh, which="SM", tol=tol, maxiter=20000,
                v0=np.random.default_rng(seed).standard_normal(Kh.shape[0]))
    dt=time.time()-t0
    om=float(np.sqrt(np.maximum(np.sort(np.real(w))[0],0.0)))
    return om, abs(om-om_ex)/om_ex, dt

for tag, kx, ky in (("5i k=(0.31,0.22)pi/L", 0.31*np.pi/L, 0.22*np.pi/L),
                    ("new k=(0.37,0.19)pi/L", 0.37*np.pi/L, 0.19*np.pi/L)):
    print(f"--- {tag} ---", flush=True)
    es=[]
    for n in (8, 16, 32):
        o1, e1, d1 = run(kx, ky, n, 1e-14, 20260924)
        o2, e2, d2 = run(kx, ky, n, 1e-14, 7)
        es.append((e1, e2))
        print(f"  n={n:2d}: err(seedA)={e1:.4e} err(seedB)={e2:.4e} | seed spread(rel)={abs(o1-o2)/o1:.2e} | solve {d1:.0f}s/{d2:.0f}s", flush=True)
    if tag.startswith("5i"):
        continue
    print("  ratio err16/err32 per seed:", f"{es[1][0]/es[2][0]:.1f}", f"{es[1][1]/es[2][1]:.1f}", "(pure h^4 -> 16)")
    print("  h^4 prediction for err32 from err16 :", f"{es[1][0]/16:.3e} (seedA)  {es[1][1]/16:.3e} (seedB)")
