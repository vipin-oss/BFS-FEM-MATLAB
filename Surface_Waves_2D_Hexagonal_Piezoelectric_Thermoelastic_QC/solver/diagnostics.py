"""Modal diagnostics (blueprint §22 rules).

- Penetration depth delta* = 1/|Im p_j|: an evanescent DEPTH-LOCALISATION
  measure. It is NOT propagation attenuation and is never reported as such.
- Phason participation P_w = (|w_x|^2+|w_z|^2)/sum_i|a_i|^2 over the
  surface-mode eigenvector combination: an AMPLITUDE diagnostic, not an
  energy fraction.
- Surface-response sensitivity ratio S_BC = Delta_BC /
  (|Lambda_C-Lambda_B|/|Lambda_B|): EMPIRICAL diagnostic only; defined
  only where the denominator exceeds denom_min (flagged/omitted
  otherwise; never artificially regularised; no law is claimed).
"""
import numpy as np
from . import matrix as mx

def surface_mode(k, Omega, model, m, bc):
    """Admissible-set eigenvector combination closest to satisfying BC.

    Returns (coeffs, amplitudes) where amplitudes = |V @ coeffs| normalised.
    Used for participation/penetration weighting; the secular condition is
    sigma_min(B), and this returns the corresponding singular vector.
    """
    from . import roots as rt, boundary as bd
    rr = rt.depth_roots(k, Omega, model, m)
    if rr["n_ad"] != 5:
        return None
    B = bd.B_matrix(k, rr["p_ad"], rr["V"], m, bc)
    U, sv, Vh = np.linalg.svd(B)
    coeffs = Vh[-1].conj()
    return dict(p_ad=rr["p_ad"], V=rr["V"], coeffs=coeffs, smin=sv[-1])

def penetration(k, Omega, model, m, bc):
    sm = surface_mode(k, Omega, model, m, bc)
    if sm is None:
        return dict(delta=np.nan, delta_w=np.nan)
    a = np.abs(sm["V"] @ sm["coeffs"])       # weighted modal amplitudes
    # dominant penetration: weighted by amplitude over the five fields
    delta = 1.0 / np.abs(sm["p_ad"].imag)
    wgt = np.abs(sm["coeffs"]); wgt = wgt / wgt.sum()
    return dict(delta=float(1.0 / np.abs(sm["p_ad"].imag).min()),
                delta_weighted=float(np.sum(wgt * delta)),
                per_root=delta.tolist(), amp=a.tolist())

def participation(k, Omega, model, m, bc):
    sm = surface_mode(k, Omega, model, m, bc)
    if sm is None:
        return dict(P_w=np.nan, ratio_w=np.nan, ratio_th=np.nan)
    a = np.abs(sm["V"] @ sm["coeffs"])
    tot = np.sum(a ** 2)
    P_w = (a[2] ** 2 + a[3] ** 2) / tot if tot > 0 else np.nan
    phon = a[0] ** 2 + a[1] ** 2
    return dict(P_w=float(P_w),
                ratio_w=float((a[2] ** 2 + a[3] ** 2) / phon) if phon > 0 else np.nan,
                ratio_th=float(a[4] ** 2 / phon) if phon > 0 else np.nan)

def operator_ratio_BC(Omega, m):
    """|Lambda_C - Lambda_B| / |Lambda_B| = rho_w* Omega / D_w* (analytic)."""
    LamB = mx.Lambda_of(Omega, "B", m)
    LamC = mx.Lambda_of(Omega, "C", m)
    if abs(LamB) == 0:
        return np.nan
    return float(abs(LamC - LamB) / abs(LamB))

def S_BC(Delta_BC, Omega, m, denom_min=1e-12):
    den = operator_ratio_BC(Omega, m)
    if not np.isfinite(den) or den < denom_min:
        return np.nan, True     # flagged: denominator too small -> omit
    return float(Delta_BC / den), False
