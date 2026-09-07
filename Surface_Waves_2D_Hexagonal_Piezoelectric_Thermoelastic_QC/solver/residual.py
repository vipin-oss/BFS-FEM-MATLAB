"""Secular residual evaluator (architecture item 7).

r(Omega, k*) = sigma_min(B) / ||B||_2   (spectral norm).

Frozen scaling convention: rows are already commensurate via the frozen
nondimensionalisation (all starred; beta1* = 1); NO extra row or column
rescaling is performed (sigma_min/||B|| is invariant under uniform scaling
only - frozen §11). Eigenvector columns are unit-norm by convention
(roots.py), which fixes the residual's normalisation.

Returns NaN when the admissible-root count != 5 (recorded as 'no_branch'
by the caller - never fabricated).
"""
import numpy as np
from . import roots as rt
from . import boundary as bd

def secular(k, Omega, model, m, bc, need=5):
    rr = rt.depth_roots(k, Omega, model, m)
    if rr["n_ad"] != need:
        return dict(r=np.nan, n_ad=rr["n_ad"], n_grazing=rr["n_grazing"],
                    condB=np.nan, normB=np.nan, smin=np.nan, rr=rr)
    B = bd.B_matrix(k, rr["p_ad"], rr["V"], m, bc)
    sv = np.linalg.svd(B, compute_uv=False)
    normB = sv[0]
    smin = sv[-1]
    r = smin / max(normB, 1e-300)
    return dict(r=float(r), n_ad=rr["n_ad"], n_grazing=rr["n_grazing"],
                condB=float(normB / max(smin, 1e-300)), normB=float(normB),
                smin=float(smin), rr=rr)

def r_scalar(k, Omega, model, m, bc):
    """Scalar residual for optimisers; NaN marks invalid points (never a
    large finite stand-in at this level - the optimiser wrapper handles
    finite substitution locally)."""
    out = secular(k, Omega, model, m, bc)
    return out["r"]
