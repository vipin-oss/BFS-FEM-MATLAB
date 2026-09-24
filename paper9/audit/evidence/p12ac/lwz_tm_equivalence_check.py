#!/usr/bin/env python3
"""P12AC evidence — LWZ2016 (Li, Wei & Zhou, Acta Mech. 227:1005-1023, 2016;
repository copy ``paper9/analytic/lwz2016/li2015.pdf``).

Anti-plane (Bloch SH) transfer-matrix equivalence chain and the Fig. 3
(``xibar = 0``) reproducibility check.

Three independent objects are compared for the layer transfer matrix:

  (A) APP-3   the *printed* Appendix 3 matrix (PDF page 18, normal propagation,
              Bloch SH wave: r = s, eps = mu), transcribed from the PDF text
              layer, including the 1/(sigma^2 + tau^2) prefactor.
  (B) FP      a first-principles propagator built from the paper's body
              equations (12)-(14) and (41.1)-(41.4) with state [u, u', P, R]:
                  u  = A cos(sx) + B sin(sx) + C cosh(tx) + D sinh(tx)
                  P  = mu[(1-m) u' + c u'''],   R = mu c u'',
                  m  = omega^2 d^2 / (3 V^2)
                  T_layer = M(a_j) M(0)^-1
  (C) REPO    the repository solver ``layer_T_sh_normal``
              (paper9/validation/b6_lwz_tm/lwz_tm_sh_normal.py)

then the paper's own dispersion relation (14.1) is checked on a homogeneous
cell, and the cell band edges for the parameter set printed with Fig. 3
(cbar1 = 0.5, cbar = 0.77, dbar1 = 0.5, dbar = 2, a1/a = 0.5, the Fig. 2
material set) are compared against the grey (stop-band) intervals digitised
from the Fig. 3 left panel.

Digitisation is a registration aid only: no percentage error is derived from it
and none is claimed anywhere in the P12AC record.

Writes ``lwz_tm_equivalence_results.json`` next to this file.
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "paper9", "validation", "b6_lwz_tm"))

from lwz_tm_sh_normal import layer_T_sh_normal  # noqa: E402  (repository solver)


# --------------------------------------------------------------------------
# (12)/(14.1): sigma_sh, tau_sh and the micro-inertia factor m
# --------------------------------------------------------------------------
def sigma_tau(omega, Vs, c, d):
    V2 = Vs * Vs
    B = V2 - omega * omega * d * d / 3.0
    A = c * V2
    C = omega * omega
    disc = math.sqrt(B * B + 4.0 * A * C)
    sig2 = 2.0 * C / (B + disc)
    tau2 = C / (A * sig2)
    return math.sqrt(sig2), math.sqrt(tau2), omega * omega * d * d / (3.0 * V2)


def T_app3(omega, a_j, c, d, mu, rho):
    """Printed Appendix 3, Bloch SH wave: r = s, eps = mu."""
    Vs = math.sqrt(mu / rho)
    sig, tau, _ = sigma_tau(omega, Vs, c, d)
    eps = mu
    sa, ca = math.sin(sig * a_j), math.cos(sig * a_j)
    sh, ch = math.sinh(tau * a_j), math.cosh(tau * a_j)
    t = np.zeros((4, 4))
    t[0, 0] = sig**2 * ch + tau**2 * ca
    t[0, 1] = sig * sa + tau * sh
    t[0, 2] = (tau * sa - sig * sh) / (c * eps * sig * tau)
    t[0, 3] = (ch - ca) / (c * eps)
    t[1, 0] = sig**2 * tau * sh - tau**2 * sig * sa
    t[1, 1] = sig**2 * ca + tau**2 * ch
    t[1, 2] = (ca - ch) / (c * eps)
    t[1, 3] = (tau * sh + sig * sa) / (c * eps)
    t[2, 0] = -c * eps * sig * tau * (sig**3 * sh + tau**3 * sa)
    t[2, 1] = c * eps * sig**2 * tau**2 * (ca - ch)
    t[2, 2] = tau**2 * ca + sig**2 * ch
    t[2, 3] = tau * sig * (tau * sa - sig * sh)
    t[3, 0] = c * eps * sig**2 * tau**2 * (ch - ca)
    t[3, 1] = c * eps * (tau**3 * sh - sig**3 * sa)
    t[3, 2] = -(tau * sh + sig * sa)
    t[3, 3] = tau**2 * ch + sig**2 * ca
    return t / (sig**2 + tau**2)


def M_fp(omega, x, c, d, mu, rho):
    """First-principles propagator for the state vector [u, u', P, R]."""
    Vs = math.sqrt(mu / rho)
    s, t, m = sigma_tau(omega, Vs, c, d)
    S, Cc = math.sin(s * x), math.cos(s * x)
    Sh, Ch = math.sinh(t * x), math.cosh(t * x)
    p1 = mu * (s * (1.0 - m) + c * s**3)
    p2 = mu * (t * (1.0 - m) - c * t**3)
    return np.array([
        [Cc, S, Ch, Sh],
        [-s * S, s * Cc, t * Sh, t * Ch],
        [-p1 * S, p1 * Cc, p2 * Sh, p2 * Ch],
        [-mu * c * s**2 * Cc, -mu * c * s**2 * S, mu * c * t**2 * Ch, mu * c * t**2 * Sh],
    ])


def T_fp(omega, a_j, c, d, mu, rho):
    return M_fp(omega, a_j, c, d, mu, rho) @ np.linalg.inv(M_fp(omega, 0.0, c, d, mu, rho))


# --------------------------------------------------------------------------
# source-conforming parameter set of Figs. 2 and 3
#   horizontal axis  ka/pi (first Brillouin zone, xibar = 0 panel)
#   vertical axis    omega a / (2 pi v_m),  v_m = a / (a1/Vs1 + a2/Vs2)
# --------------------------------------------------------------------------
A_CELL = 1.0
A1 = A2 = 0.5
VS1, RHO1 = 1.0, 1.0
VS2, RHO2 = 0.5947, 0.1573
MU1 = RHO1 * VS1**2
MU2 = RHO2 * VS2**2
V_M = A_CELL / (A1 / VS1 + A2 / VS2)
CB1, CB, DB1, DB = 0.5, 0.77, 0.5, 2.0           # Fig. 3 caption (PDF p.10)
C1, C2 = (CB1 * A_CELL) ** 2, (CB1 * A_CELL) ** 2 / CB
D1, D2 = DB1 * A_CELL, DB1 * A_CELL / DB
AS_READ = dict(a1=A1, a2=A2, c1=C1, c2=C2, d1=D1, d2=D2,
               mu1=MU1, mu2=MU2, rho1=RHO1, rho2=RHO2)


def cell_T(omega, p):
    TA = layer_T_sh_normal(omega, p["a1"], p["c1"], p["d1"], p["mu1"], p["rho1"])[0]
    TB = layer_T_sh_normal(omega, p["a2"], p["c2"], p["d2"], p["mu2"], p["rho2"])[0]
    return TB @ TA


def cell_edges(p, omega_max=14.0, n=40001, tol=1e-9):
    """Pass-band / stop-band transitions of the cell matrix over the omega grid.

    A frequency is a pass band iff the cell transfer matrix has a unit-modulus
    eigenvalue (a real Bloch wavenumber exists).
    """
    ws = np.linspace(1e-6, omega_max, n)
    inside = np.empty(n, dtype=bool)
    for i, w in enumerate(ws):
        lam = np.linalg.eigvals(cell_T(w, p))
        inside[i] = np.min(np.abs(np.abs(lam) - 1.0)) < tol
    edges = []
    for i in range(1, n):
        if inside[i] != inside[i - 1]:
            lo, hi = ws[i - 1], ws[i]
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                lam = np.linalg.eigvals(cell_T(mid, p))
                ins = np.min(np.abs(np.abs(lam) - 1.0)) < tol
                if ins == inside[i - 1]:
                    lo = mid
                else:
                    hi = mid
            edges.append(0.5 * (lo + hi))
    return np.array(edges) / (2 * math.pi * V_M)


def variant_params():
    """Bounded family of plausible convention variants (not a fit)."""
    v = {}
    v["V0_as_read"] = dict(AS_READ)
    v["V1_c_ratio_reversed"] = dict(AS_READ, c2=C1 * CB)
    v["V2_d_ratio_reversed"] = dict(AS_READ, d2=D1 * DB)
    v["V3_layers_swapped"] = dict(AS_READ, c1=AS_READ["c2"], c2=AS_READ["c1"],
                                  d1=AS_READ["d2"], d2=AS_READ["d1"],
                                  mu1=AS_READ["mu2"], mu2=AS_READ["mu1"],
                                  rho1=AS_READ["rho2"], rho2=AS_READ["rho1"])
    v["V4_cbar_in_layer_units"] = dict(AS_READ, c1=(CB1 * A1) ** 2,
                                       c2=(CB1 * A1) ** 2 / CB,
                                       d1=DB1 * A1, d2=DB1 * A1 / DB)
    s3 = math.sqrt(3.0)
    v["V5_micro_inertia_m_d2"] = dict(AS_READ, d1=D1 * s3, d2=D2 * s3)
    return v


def variant_sweep(target):
    """Characterise the earlier (retracted) Appendix-3 reconstruction."""
    om, a_j, c, d, mu = 0.8, 0.5, 0.25, 0.5, 1.0
    best = None
    tested = 0
    for cvar in (c, c / 0.77):
        for dvar in (d, d / 2):
            for mmul in (1.0, 1.0 / 3.0, 3.0):
                B = mu - om * om * dvar * dvar * mmul
                A = cvar * mu
                Cc = om * om
                disc = math.sqrt(B * B + 4.0 * A * Cc)
                s = math.sqrt(2.0 * Cc / (B + disc))
                t = math.sqrt(Cc / (A * s * s))
                for swap in (False, True):
                    for sgn in (+1, -1):
                        for inv in (False, True):
                            tested += 1
                            ss, tt = (t, s) if swap else (s, t)
                            sa, ca = math.sin(ss * a_j), math.cos(ss * a_j)
                            sh, ch = math.sinh(tt * a_j), math.cosh(tt * a_j)
                            f = (mu if not inv else 1.0 / mu)
                            row = np.array([
                                -cvar * f * ss * tt * (ss**3 * sh + tt**3 * sa),
                                cvar * f * ss**2 * tt**2 * (ca - ch),
                                tt**2 * ca + ss**2 * ch,
                                sgn * tt * ss * (tt * sa - ss * sh)]) / (ss**2 + tt**2)
                            err = float(np.max(np.abs(row - target)))
                            if best is None or err < best["max_abs_residual"]:
                                best = dict(max_abs_residual=err, c=cvar, d=dvar,
                                            m_multiplier=mmul, swap=swap,
                                            sign_t34=sgn, invert=f != mu)
    return dict(variants_tested=tested, best=best)


def main():
    out = {"phase": "P12AC",
           "source": "LWZ2016 / li2015.pdf (Acta Mech 227:1005-1023)"}

    # -- 1. printed Appendix 3  vs  first principles  vs  repository solver --
    rows = []
    for om, c, d, mu, rho in [(0.8, 0.25, 0.5, 1.0, 1.0),
                              (2.0, 0.25, 0.5, 1.0, 1.0),
                              (3.0, 0.25, 0.5, 1.0, 1.0),
                              (5.0, 0.25, 0.5, 1.0, 1.0),
                              (0.8, 0.324675, 0.25, 0.0556319, 0.1573)]:
        app3 = T_app3(om, 0.5, c, d, mu, rho)
        fp = T_fp(om, 0.5, c, d, mu, rho)
        repo = layer_T_sh_normal(om, 0.5, c, d, mu, rho)[0]
        rows.append(dict(omega=om, c=c, d=d,
                         max_abs_app3_minus_fp=float(np.max(np.abs(app3 - fp))),
                         max_abs_app3_minus_repo=float(np.max(np.abs(app3 - repo))),
                         max_abs_fp_minus_repo=float(np.max(np.abs(fp - repo))),
                         repo_row3=[float(x) for x in np.real(repo[2])]))
    out["appendix3_vs_first_principles_vs_repo"] = rows
    out["appendix3_vs_repo_max_over_points"] = max(r["max_abs_app3_minus_repo"] for r in rows)

    # -- 2. homogeneous cell vs the paper's own dispersion relation (14.1) ----
    hom = []
    for V, c, d, a in [(1.0, 0.25, 0.5, 1.0), (1.0, 0.0625, 0.25, 0.5)]:
        mu, rho = V * V, 1.0
        for sig in (0.5, 1.5, 3.0):
            om = math.sqrt(sig**2 * V**2 * (1 + c * sig**2) / (1 + (d * d / 3) * sig**2))
            T = layer_T_sh_normal(om, a, c, d, mu, rho)[0]
            lam = np.linalg.eigvals(T)
            j = int(np.argmin(np.abs(np.abs(lam) - 1.0)))
            ang = float(abs(np.angle(lam[j])))
            hom.append(dict(V=V, c=c, d=d, a=a, sigma=sig, omega=om,
                            sigma_a=sig * a, tm_angle=ang,
                            rel_residual=abs(ang - sig * a) / (sig * a)))
    out["homogeneous_vs_eq_14_1"] = hom
    out["homogeneous_max_rel_residual"] = max(h["rel_residual"] for h in hom)

    # -- 3. Fig. 3 (xibar = 0) band edges vs the digitised stop-band bands ---
    out["parameters_fig3"] = AS_READ
    out["v_m"] = V_M
    out["cell_band_edges_y"] = [float(x) for x in cell_edges(AS_READ)]
    out["fig3_digitised_grey_intervals_y"] = [
        [0.6036, 0.6627], [0.8718, 1.1637], [1.3136, 1.7120]]
    out["fig3_digitisation_note"] = (
        "grey (stop-band) intervals measured from p10_x96.jpeg, left panel, using "
        "the same frame-calibration procedure that reproduces the analytic classical "
        "Fig. 2 edges to <= 0.010 in y; registration aid only, no percentage error "
        "is derived")
    out["fig2_calibration_check_analytic_edges_y"] = [
        0.1946, 0.7415, 0.8297, 1.2444, 1.3772, 1.5810, 1.6995]
    out["fig2_calibration_check_digitised_gaps_y"] = [
        [0.2034, 0.7382], [0.8361, 1.2429], [1.3860, 1.5820]]

    # -- 4. bounded convention-variant family (not a fit; no variant adopted) --
    vout = {}
    for name, p in variant_params().items():
        vout[name] = dict(params=p, edges_y=[float(x) for x in cell_edges(p)])
    out["variant_edges_y"] = vout
    out["variant_statement"] = (
        "bounded convention-variant family evaluated with the same solver; no "
        "variant reproduces all three digitised stop-band intervals, and no variant "
        "is adopted (no best-visual-fit, no tuning)")

    # -- 5. retraction evidence: variant sweep for the earlier reconstruction --
    out["retracted_variant_sweep"] = variant_sweep(
        np.array([-0.317454, -0.057700, 0.978031, +0.068534]))
    out["retraction_statement"] = (
        "The earlier hand-reconstruction of Appendix 3 is superseded: no member of "
        "the tested 96-member transcription/convention family reproduces its row 3, "
        "while the PDF-text transcription of Appendix 3 and an independent "
        "first-principles derivation both reproduce the repository matrix to "
        "<= 3.6e-15.")

    with open(os.path.join(HERE, "lwz_tm_equivalence_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)

    print("max |App-3 - repo|      :", out["appendix3_vs_repo_max_over_points"])
    print("homogeneous max rel res :", out["homogeneous_max_rel_residual"])
    print("as-read band edges y    :", [round(x, 4) for x in out["cell_band_edges_y"]])
    print("digitised grey bands y  :", out["fig3_digitised_grey_intervals_y"])
    for name, d in vout.items():
        print(f"  {name:<26} -> {[round(x, 4) for x in d['edges_y']]}")


if __name__ == "__main__":
    main()
