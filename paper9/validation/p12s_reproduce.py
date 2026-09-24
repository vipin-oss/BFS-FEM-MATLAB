#!/usr/bin/env python3
"""P12S Phase C — independent reproduction of B1, B2, B3 for graphical validation.

Routes (Blueprint v1.5 §13 / amendment A2):
  QUANTITATIVE_VALIDATION  source numerical values exist  -> not the case for B1/B2/B3
  GRAPHICAL_VALIDATION     source graph + sufficient parameters -> overlay comparison
  NOT_VALIDATED            insufficient / contradictory / ambiguous source

This module computes the reproduced curves from the source-stated equations and
parameters (transfer-matrix methods already present in the repository), digitises the
published curves ONLY as a graphical-registration tool, and writes an overlay figure.
No percentage is derived from the overlay; ``quantitative_error`` stays NULL.

Sources (authoritative PDFs in this repository):
  Li et al. 2024, Sci. Rep. 14:24035, Fig. 2(a) p.9  (B1, classical AlN/BaTiO3)
  Li et al. 2024, Sci. Rep. 14:24035, Fig. 2(b) p.9  (B2, strain gradient)
  Li et al. 2023, WRCM 36(4):5715,  Fig. 4(c) p.15   (B3, dipolar gradient Pb/brass)
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import scipy.linalg as la

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

import p12s_panels as P

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[0] / "audit" / "evidence" / "p12s"   # = paper9/audit/evidence/p12s   # tracked evidence directory (paper9/audit/evidence/p12s)
WORK.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------------- parameters
# Li et al. 2024, p.7:  rho=3.23e3 kg/m3, a3=8.4e-11 C2/Nm2, c33=3.9e11 Pa, aA=aB=0.01 m
# Li et al. 2024, p.8:  rho'=5.8e3 kg/m3, a3'=1.26e-8 C2/Nm2, c33'=1.62e11 Pa
P24 = dict(rho_A=3.23e3, c33_A=3.9e11, rho_B=5.8e3, c33_B=1.62e11, a_A=0.01, a_B=0.01)
# Li et al. 2023, p.14:  a1=1e-5 m, rho1=7.5e3 kg/m3, mu1=2.3e10 Pa, w0=4.1e8 Hz, aR=1,
#                       muR=0.056, rhoR=0.157  ->  cR = 1.5, dR = 1.5, cbar1=0.15, dbar1=0.25
P23 = dict(mu_1=2.3e10, rho_1=7.5e3, a_1=1e-5, c1_bar=0.15, d1_bar=0.25, cR=1.5, dR=1.5,
           muR=0.056, rhoR=0.157)


def omega0_24(a_A, a_B, rho_A, c33_A, rho_B, c33_B) -> float:
    """Li 2024 Eq. (55): omega0 = 2*pi / ( aA*sqrt(rho/c33) + aB*sqrt(rho'/c33') )."""
    return 2 * np.pi / (a_A * np.sqrt(rho_A / c33_A) + a_B * np.sqrt(rho_B / c33_B))


# ----------------------------------------------------------------------------- B1 engine
def b1_dispersion(n_w: int = 4000):
    """Classical Rytov dispersion of the AlN/BaTiO3 bilayer (Li 2024 Fig. 2(a))."""
    rho_A, c_A, rho_B, c_B = P24["rho_A"], P24["c33_A"], P24["rho_B"], P24["c33_B"]
    a_A, a_B = P24["a_A"], P24["a_B"]
    vA, vB = np.sqrt(c_A / rho_A), np.sqrt(c_B / rho_B)
    ZA, ZB = rho_A * vA, rho_B * vB
    w0 = omega0_24(a_A, a_B, rho_A, c_A, rho_B, c_B)
    wbar = np.linspace(1e-6, 3.0, n_w)
    w = wbar * w0
    kA, kB = w / vA, w / vB
    cosKb = (np.cos(kA * a_A) * np.cos(kB * a_B)
             - 0.5 * (ZA / ZB + ZB / ZA) * np.sin(kA * a_A) * np.sin(kB * a_B))
    prop = np.abs(cosKb) <= 1.0
    kbar = np.where(prop, np.arccos(np.clip(cosKb, -1, 1)) / np.pi, np.nan)
    gaps = _gap_intervals(wbar, prop)
    return wbar, kbar, prop, gaps, w0


def _gap_intervals(wbar: np.ndarray, prop: np.ndarray):
    out, s = [], None
    for i in range(len(prop)):
        if not prop[i] and s is None:
            s = wbar[i]
        elif prop[i] and s is not None:
            out.append((round(float(s), 4), round(float(wbar[i]), 4))); s = None
    return out


# ----------------------------------------------------------------------------- B2 engine
def b2_dispersion(a_scale: float, n_w: int = 3000, use_barred: bool = False):
    """Strain-gradient bilayer dispersion (Li 2024 Eq. 45-55) with l,l1 from the Fig. 2 caption.

    ``a_scale``: layer thickness in metres (geometry to be tested).
    ``use_barred``: interpret the caption values as l_bar = l/b (normalised) instead of
    dimensional metres.
    """
    rho_A, c_A, rho_B, c_B = P24["rho_A"], P24["c33_A"], P24["rho_B"], P24["c33_B"]
    b = 2 * a_scale
    l, l1 = (1e-5, 2e-5)
    if use_barred:                      # lbar = l/b  ->  l = lbar * b
        l, l1 = l * b, l1 * b
    L, L1 = 5.0, 5.0                    # caption: L = l'/l = 5, L1 = l1'/l1 = 5
    props = [dict(rho=rho_A, c=c_A, l=l, l1=l1), dict(rho=rho_B, c=c_B, l=L * l, l1=L1 * l1)]

    def layer_T(w: float, p) -> np.ndarray:
        A = p["c"] * p["l"] ** 2
        B = p["c"] - p["rho"] * w**2 * p["l1"] ** 2
        C = -p["rho"] * w**2
        disc = B**2 - 4 * A * C
        k2a = (-B + np.sqrt(disc + 0j)) / (2 * A)
        k2b = (-B - np.sqrt(disc + 0j)) / (2 * A)
        # complex square roots: a negative k^2 is an evanescent branch (imaginary k),
        # which is physical in the gradient model and must not be dropped.
        ka, kb = np.sqrt(k2a + 0j), np.sqrt(k2b + 0j)
        ks = [ka, kb, -ka, -kb]
        Pm = np.zeros((4, 4), dtype=complex)
        for s, k in enumerate(ks):
            Pm[0, s] = 1.0
            Pm[1, s] = 1j * k
            Pm[2, s] = 1j * k * (p["c"] - p["rho"] * p["l1"] ** 2 * w**2 + k**2 * p["l"] ** 2 * p["c"])
            Pm[3, s] = -(k**2) * p["l"] ** 2 * p["c"]
        d = np.max(np.abs(Pm), axis=1)
        D, Di = np.diag(1 / d), np.diag(d)
        Ps = D @ Pm
        G = np.diag(np.exp(np.array([1j * k * a_scale for k in ks])))
        return Di @ (Ps @ G @ la.inv(Ps)) @ D, ks

    w0 = omega0_24(a_scale, a_scale, rho_A, c_A, rho_B, c_B)
    wbar = np.linspace(1e-6, 3.0, n_w)
    prop = np.zeros(len(wbar), dtype=bool)
    kbar = np.full(len(wbar), np.nan)
    for i, wb in enumerate(wbar):
        w = wb * w0
        TA, _ = layer_T(w, props[0]); TB, _ = layer_T(w, props[1])
        ev = la.eigvals(TB @ TA)
        on_circle = ev[np.abs(np.abs(ev) - 1.0) < 1e-6]
        if on_circle.size:
            prop[i] = True
            kbar[i] = float(np.mean(np.abs(np.angle(on_circle)))) / np.pi
    return dict(wbar=wbar, kbar=kbar, prop=prop, gaps=_gap_intervals(wbar, prop), w0=w0,
                l=l, l1=l1, a=a_scale, cell=b)


# ----------------------------------------------------------------------------- B3 engine
def b3_dispersion(n_w: int = 4000):
    """Dipolar-gradient SH dispersion of the Pb/brass bilayer (Li 2023 Fig. 4(c) / LWZ 2016)."""
    mu_1, rho_1, a1 = P23["mu_1"], P23["rho_1"], P23["a_1"]
    mu_2, rho_2, a2 = mu_1 * P23["muR"], rho_1 * P23["rhoR"], a1
    c1, d1 = P23["c1_bar"] * a1**2, P23["d1_bar"] * a1
    c2, d2 = c1 * P23["cR"], d1 * P23["dR"]
    V1, V2 = np.sqrt(mu_1 / rho_1), np.sqrt(mu_2 / rho_2)
    w0 = 2 * np.pi / (a1 / V1 + a2 / V2)

    def sh_T(w: float, a: float, c: float, d: float, mu: float, rho: float):
        Vs2 = mu / rho
        ms = w**2 * d**2 / (3 * Vs2)
        disc = (1 - ms) ** 2 + 4 * c * w**2 / Vs2
        D = np.sqrt(disc)
        sig2 = max((D - (1 - ms)) / (2 * c), 0.0)
        tau2 = max((D + (1 - ms)) / (2 * c), 0.0)
        sig, tau = np.sqrt(sig2), np.sqrt(tau2)
        sa, ca = np.sin(sig * a), np.cos(sig * a)
        sh, ch = np.sinh(tau * a), np.cosh(tau * a)
        den = sig**2 + tau**2
        T = np.zeros((4, 4), dtype=complex)
        T[0, 0] = sig**2 * ch + tau**2 * ca
        T[0, 1] = sig * sa + tau * sh
        T[0, 2] = (tau * sa - sig * sh) / (c * mu * sig * tau)
        T[0, 3] = (ch - ca) / (c * mu)
        T[1, 0] = sig**2 * tau * sh - tau**2 * sig * sa
        T[1, 1] = sig**2 * ca + tau**2 * ch
        T[1, 2] = (ca - ch) / (c * mu)
        T[1, 3] = (tau * sh + sig * sa) / (c * mu)
        T[2, 0] = -c * mu * sig * tau * (sig**3 * sh + tau**3 * sa)
        T[2, 1] = c * mu * sig**2 * tau**2 * (ca - ch)
        T[2, 2] = tau**2 * ca + sig**2 * ch
        T[2, 3] = tau * sig * (tau * sa - sig * sh)
        T[3, 0] = c * mu * sig**2 * tau**2 * (ch - ca)
        T[3, 1] = c * mu * (tau**3 * sh - sig**3 * sa)
        T[3, 2] = -tau * sh - sig * sa
        T[3, 3] = tau**2 * ch + sig**2 * ca
        return T / den, sig, tau

    wbar = np.linspace(1e-6, 3.0, n_w)
    prop = np.zeros(len(wbar), dtype=bool)
    curves: list[tuple[float, float]] = []
    for i, wb in enumerate(wbar):
        w = wb * w0
        T1, s1, _ = sh_T(w, a1, c1, d1, mu_1, rho_1)
        T2, _, _ = sh_T(w, a2, c2, d2, mu_2, rho_2)
        ev = la.eigvals(T2 @ T1)
        on_circle = ev[np.abs(np.abs(ev) - 1.0) < 1e-6]
        if on_circle.size:
            prop[i] = True
            for e in on_circle:
                curves.append((wb, abs(float(np.angle(e))) / np.pi))
    curves.sort()
    return dict(wbar=wbar, prop=prop, curves=curves, gaps=_gap_intervals(wbar, prop),
                w0=w0, omega0_stated=4.1e8, Vs1=V1, Vs2=V2)


# ----------------------------------------------------------------------------- digitisation
def digitise_reference(bid: str, panels: dict, n_cols: int = 420):
    """Curve pixels of the published panel, in data coordinates (registration overlay only)."""
    p = panels[bid]
    tr = p["transform"]
    img = p["panel"]
    dark = np.asarray(img) < 110
    h, w = dark.shape
    pad = 4                                   # exclude the axis frame itself
    xs, ys = [], []
    for cx in np.linspace(pad, w - 1 - pad, n_cols):
        j = int(round(cx))
        col = np.where(dark[pad:h - pad, j])[0] + pad
        if col.size == 0:
            continue
        # split into contiguous clusters (distinct branches in the same column)
        splits = np.where(np.diff(col) > 3)[0]
        groups = np.split(col, splits + 1)
        for g in groups:
            py = float(np.mean(g))
            x, y = P.px_to_data(tr, np.array([j]), np.array([py]))
            xs.append(float(x[0])); ys.append(float(y[0]))
    return np.array(xs), np.array(ys)


# ----------------------------------------------------------------------------- overlays
def overlay(bid: str, panels: dict, repro: dict, title: str, out_name: str):
    p = panels[bid]
    tr = p["transform"]
    ref_x, ref_y = digitise_reference(bid, panels)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), dpi=150)
    # left: published panel with digitised registration overlay
    axes[0].imshow(p["panel"], cmap="gray", extent=[-1, 1, 0, 2], aspect="auto")
    axes[0].plot(ref_x, ref_y, ".", ms=1.0, color="#1f77b4", alpha=0.6,
                 label="published figure (digitised for registration)")
    # right: independent reproduction + digitised reference for direct comparison
    if "kbar" in repro:
        for sign in (+1, -1):
            axes[1].plot(sign * repro["kbar"], repro["wbar"], lw=1.4, color="#d62728",
                         label="independent reproduction" if sign > 0 else None)
    else:
        cx = np.array([c[1] for c in repro["curves"]]); cy = np.array([c[0] for c in repro["curves"]])
        for sign in (+1, -1):
            axes[1].plot(sign * cx, cy, lw=1.4, color="#d62728",
                         label="independent reproduction" if sign > 0 else None)
    axes[1].plot(ref_x, ref_y, ".", ms=1.0, color="#1f77b4", alpha=0.5,
                 label="published figure (digitised)")
    for ax in axes:
        ax.set_xlim(-1.02, 1.02); ax.set_ylim(-0.02, 2.05)
        ax.set_xlabel(r"$\bar k$"); ax.set_ylabel(r"$\bar\omega$")
        ax.grid(alpha=0.25); ax.legend(loc="upper right", fontsize=7)
    axes[0].set_title("published panel + registration digits", fontsize=9)
    axes[1].set_title("independent reproduction vs published", fontsize=9)
    fig.suptitle(title, fontsize=10)
    fig.tight_layout()
    out = WORK / out_name
    fig.savefig(out); plt.close(fig)
    return out, (ref_x, ref_y)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


if __name__ == "__main__":
    panels = P.panel_arrays()
    result: dict = {}

    # ---- B1 -------------------------------------------------------------------------
    wbar, kbar, prop, gaps, w0 = b1_dispersion()
    b1 = dict(wbar=wbar, kbar=kbar, prop=prop, gaps=gaps, w0=w0)
    edges = {}
    for target in (0.0, 1.0):
        idx = int(np.argmin(np.abs(np.abs(kbar) - target)))
        edges[f"kbar={target}"] = float(wbar[idx])
    # first-band edge values on the branches (vertices at kbar = 0 and 1)
    verts = {"omega_bar at kbar=0 (first band)": 0.0,
             "omega_bar at kbar=0 (branch intersection)": float(wbar[np.nanargmin(np.abs(kbar - 0.0))] if np.any(prop) else np.nan)}
    fig_b1, ref_b1 = overlay("B1", panels, b1,
        "B1 — Li et al. 2024 Fig. 2(a), classical AlN/BaTiO3 bilayer: graphical reproduction",
        "B1_overlay.png")
    result["B1"] = dict(gaps=gaps, omega0=w0, reference_pixels=int(ref_b1[0].size),
                        overlay=str(fig_b1), overlay_sha256=sha256(fig_b1))

    # ---- B2: three labelled interpretations ----------------------------------------
    cfg = {}
    cfg["source_geometry_dimensional"] = b2_dispersion(P24["a_A"], n_w=1200, use_barred=False)
    cfg["source_geometry_barred"] = b2_dispersion(P24["a_A"], n_w=1200, use_barred=True)
    cfg["micro_geometry"] = b2_dispersion(1e-5, n_w=1200, use_barred=False)
    fig_b2, ref_b2 = overlay("B2", panels, cfg["source_geometry_dimensional"],
        "B2 — Li et al. 2024 Fig. 2(b): source-stated geometry a=0.01 m with dimensional l=1e-5 m\n"
        "(gradient correction O(1e-6): the reproduction collapses onto the classical panel)",
        "B2_overlay_interpretation1.png")
    result["B2"] = {
        "interpretations": {k: dict(gaps=v["gaps"], l=v["l"], l1=v["l1"], a=v["a"], cell=v["cell"],
                                    w0=v["w0"]) for k, v in cfg.items()},
        "overlay_interpretation1": str(fig_b2), "overlay_sha256": sha256(fig_b2),
        "reference_pixels": int(ref_b2[0].size)}

    # ---- B3 -------------------------------------------------------------------------
    b3 = b3_dispersion()
    fig_b3, ref_b3 = overlay("B3", panels, b3,
        "B3 — Li et al. 2023 Fig. 4(c), dipolar-gradient Pb/brass bilayer: graphical reproduction",
        "B3_overlay.png")
    result["B3"] = dict(gaps=b3["gaps"], omega0=b3["w0"], omega0_stated=b3["omega0_stated"],
                        Vs1=b3["Vs1"], Vs2=b3["Vs2"], reference_pixels=int(ref_b3[0].size),
                        overlay=str(fig_b3), overlay_sha256=sha256(fig_b3))

    (WORK / "p12s_reproduction.json").write_text(json.dumps(result, indent=1, default=str))
    print(json.dumps(result, indent=1, default=str)[:2600])
