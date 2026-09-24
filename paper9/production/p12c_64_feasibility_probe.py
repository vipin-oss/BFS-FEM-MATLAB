"""P12C 64x64 feasibility probe (NOT evidence): measures, on the actual
sandbox, whether a single 64^2 spot-k solve fits memory/time budgets before
any full 64^2 study is entered.  Uses the exact same element/assembly/T/
OPinv code as the locked study script (imported, not reimplemented).

If triggered (r >= 0.5), the 64^2 study would need 441 of these solves plus
assembly; this probe records the honest per-k cost and peak RSS so the
decision is based on measured sandbox data, not extrapolation from memory.
"""
import resource
import sys
import time

sys.path.insert(0, "/home/user/repo")
sys.path.insert(0, "/home/user/repo/paper9")

from solver.bfs_bloch_solver import mat_caseC
from production.p12c_caseC_gap_convergence import (
    assemble_mesh_KM_ngauss_sparse, bands_at_sparse)


def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6


if __name__ == "__main__":
    t0 = time.time()
    Ks, Ms = assemble_mesh_KM_ngauss_sparse(64, 64, 1.0, 1.0, mat_caseC,
                                            n_gauss=4)
    print(f"[64] assembled in {time.time()-t0:.1f}s, dofs={8*65*65}, "
          f"K nnz={Ks.nnz}, rss={rss_gb():.2f} GB", flush=True)
    for kx, ky in ((0.974, 0.534), (3.141592653589793, 0.0)):  # spot + X
        t0 = time.time()
        w = bands_at_sparse(Ks, Ms, 64, 64, kx, ky)
        print(f"[64] k=({kx:.3f},{ky:.3f}) w3,w4=({w[0]:.4f},{w[1]:.4f}) "
              f"{time.time()-t0:.1f}s rss={rss_gb():.2f} GB", flush=True)
    print("PROBE-OK", flush=True)
