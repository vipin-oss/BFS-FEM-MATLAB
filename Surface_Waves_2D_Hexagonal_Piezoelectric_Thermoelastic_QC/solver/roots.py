"""Depth-root solver + admissible-root selector (architecture items 4-5).

Quadratic pencil (A0 + p A1 + p^2 A2) a = 0 solved via the exact 10x10
companion linearisation  [0 I; -A2^-1 A0, -A2^-1 A1] v = p v  (A2 is
invertible: det A2 = (C11 K1 - R1^2)(C66 K3 - R6^2) k11 > 0; V0 asserts
det A2 != 0). Root polishing: two Newton steps on det M(p) (the tested
Stage-6 approach, retained) plus a per-root residual diagnostic
sigma_min(M(p_j))/||M(p_j)||; poorly resolved roots are FLAGGED, never
silently accepted.

Admissibility: Im p > tol * max(1, |p|) (decay into z > 0). Nearly real
(|Im p| <= tol) roots are excluded AND flagged with diagnostics; no
universal group-velocity rule is applied (blueprint §7 keeps the
first-paper implementation simple; grazing cases are recorded for
inspection).

Eigenvectors: unit-norm null vectors of M(k, p_j, Omega) via SVD
(consistent normalisation convention for B; sigma_min(B)/||B|| zeros are
independent of this convention, near-zero minima only mildly so).
"""
import numpy as np
from . import matrix as mx

def _det_M(k, p, Omega, model, m):
    return np.linalg.det(mx.M_matrix(k, p, Omega, model, m))

def _polish(p, k, Omega, model, m, iters=2):
    for _ in range(iters):
        f = _det_M(k, p, Omega, model, m)
        h = 1e-6 * max(1.0, abs(p))
        d = (_det_M(k, p + h, Omega, model, m) - f) / h
        if abs(d) < np.finfo(float).eps * max(1.0, abs(f)):
            break
        step = f / d
        if not np.isfinite(step):
            break
        p = p - step
    return p

def depth_roots(k, Omega, model, m, polish_iters=None, flag_tol=None):
    if polish_iters is None:
        polish_iters = int(m.defaults["root_polish_newton_iters"])
    if flag_tol is None:
        flag_tol = m.defaults["root_residual_flag"]
    tol = m.defaults["admissibility_tol"]

    A0, A1, A2 = mx.pencil(k, Omega, model, m)
    detA2 = np.linalg.det(A2)
    if not np.isfinite(detA2) or abs(detA2) < 1e-300:
        raise FloatingPointError("A2 singular")
    Comp = np.zeros((10, 10), dtype=complex)
    Comp[:5, 5:] = np.eye(5)
    A2inv_A0 = np.linalg.solve(A2, A0)
    A2inv_A1 = np.linalg.solve(A2, A1)
    Comp[5:, :5] = -A2inv_A0
    Comp[5:, 5:] = -A2inv_A1
    p_all = np.linalg.eigvals(Comp)
    p_all = np.array([_polish(p, k, Omega, model, m, polish_iters) for p in p_all])

    im = p_all.imag
    scale = np.maximum(1.0, np.abs(p_all))
    ad_mask = im > tol * scale
    grazing_mask = np.abs(im) <= tol * scale

    order = np.argsort(im[ad_mask])
    idx_ad = np.flatnonzero(ad_mask)[order]

    # eigenvectors + root residuals for the admissible set
    p_ad = p_all[idx_ad]
    V = np.zeros((5, len(idx_ad)), dtype=complex)
    root_res = np.zeros(len(idx_ad))
    root_flag = np.zeros(len(idx_ad), dtype=bool)
    for j, pj in enumerate(p_ad):
        Mj = mx.M_matrix(k, pj, Omega, model, m)
        U, sv, Vh = np.linalg.svd(Mj)
        V[:, j] = Vh[-1].conj()          # unit-norm null vector
        res = sv[-1] / max(sv[0], 1e-300)
        root_res[j] = res
        root_flag[j] = res > flag_tol
    return dict(
        p_all=p_all, p_ad=p_ad, idx_ad=idx_ad, V=V,
        n_roots=len(p_all), n_ad=len(idx_ad), n_grazing=int(grazing_mask.sum()),
        idx_grazing=np.flatnonzero(grazing_mask),
        root_residuals=root_res, root_flags=root_flag,
        detA2=detA2,
    )
