#!/usr/bin/env python3
"""P3 Layer 3 / 3b: PB2009 (20)-(22),(28) vs Case-H isotropic specialisation.

Reference type: (4) our closed-form specialisation vs independently coded PB formulae.
NOT an independent published-curve benchmark (PCR1). PCR3 source-equation check.

Mapping [B]: g = l/sqrt(10), h = ell. Not a PB2009 statement.
"""
from __future__ import annotations

import sys

import numpy as np
import sympy as sp

PASS = FAIL = 0


def check(name, cond, **meta):
    global PASS, FAIL
    ok = bool(cond)
    PASS += ok
    FAIL += not ok
    extra = " ".join(f"{k}={v}" for k, v in meta.items())
    print(("PASS" if ok else "FAIL") + ": " + name + (("  " + extra) if extra else ""))


def pb_omega2(C2, g, h, k):
    return C2 * k**2 * (1.0 + g**2 * k**2) / (1.0 + h**2 * k**2)


def caseH_omega2(C2, l, ell, k):
    return C2 * k**2 * (1.0 + (l**2 / 10.0) * k**2) / (1.0 + ell**2 * k**2)


def main():
    # --- symbolic PCR3 ---
    g, h, k, Cp, Cs, l, ell, mu, rho, lam = sp.symbols(
        "g h k C_p C_s l ell mu rho lam", positive=True
    )
    om2_21 = Cs**2 * k**2 * (1 + g**2 * k**2) / (1 + h**2 * k**2)
    Vp = Cs * sp.sqrt((1 + g**2 * k**2) / (1 + h**2 * k**2))
    check("L3 PB (21) vs (22) omega/k", sp.simplify(sp.sqrt(om2_21) / k - Vp) == 0)

    om2_H = (mu / rho) * k**2 * (1 + l**2 * k**2 / 10) / (1 + ell**2 * k**2)
    om2_id = om2_21.subs({Cs: sp.sqrt(mu / rho), g: l / sp.sqrt(10), h: ell})
    check("L3 Case-H isotropic == PB (21) after [B] ID", sp.simplify(om2_H - om2_id) == 0)

    om2_L_H = ((lam + 2 * mu) / rho) * k**2 * (1 + l**2 * k**2 / 10) / (1 + ell**2 * k**2)
    om2_20 = Cp**2 * k**2 * (1 + g**2 * k**2) / (1 + h**2 * k**2)
    om2_Lid = om2_20.subs({Cp: sp.sqrt((lam + 2 * mu) / rho), g: l / sp.sqrt(10), h: ell})
    check("L3 Case-H L == PB (20) after [B] ID", sp.simplify(om2_L_H - om2_Lid) == 0)

    # --- numeric scan ---
    mu_n, lam_n, rho_n = 1.0, 2.0, 1.0
    l_n, ell_n = 0.2, 0.15  # g < h after map: g=0.0632, h=0.15
    g_n = l_n / np.sqrt(10.0)
    h_n = ell_n
    Cs2 = mu_n / rho_n
    Cp2 = (lam_n + 2 * mu_n) / rho_n
    ks = np.array([0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0])
    rels_T, rels_L = [], []
    for kk in ks:
        eT = abs(caseH_omega2(Cs2, l_n, ell_n, kk) - pb_omega2(Cs2, g_n, h_n, kk)) / abs(
            pb_omega2(Cs2, g_n, h_n, kk)
        )
        eL = abs(caseH_omega2(Cp2, l_n, ell_n, kk) - pb_omega2(Cp2, g_n, h_n, kk)) / abs(
            pb_omega2(Cp2, g_n, h_n, kk)
        )
        rels_T.append(eT)
        rels_L.append(eL)
        print(f"  k={kk:6.1f}  rel_T={eT:.3e}  rel_L={eL:.3e}")
    check(
        "L3 numeric omega2 T/L vs PB over k-scan",
        max(rels_T) < 1e-12 and max(rels_L) < 1e-12,
        max_rel_T=f"{max(rels_T):.3e}",
        max_rel_L=f"{max(rels_L):.3e}",
        n_k=len(ks),
    )

    # long-wave
    k0 = 1e-4
    vT = np.sqrt(caseH_omega2(Cs2, l_n, ell_n, k0)) / k0
    vL = np.sqrt(caseH_omega2(Cp2, l_n, ell_n, k0)) / k0
    check(
        "L3 long-wave vT,vL -> Cs,Cp",
        abs(vT - np.sqrt(Cs2)) / np.sqrt(Cs2) < 1e-8
        and abs(vL - np.sqrt(Cp2)) / np.sqrt(Cp2) < 1e-8,
        eT=f"{abs(vT-np.sqrt(Cs2))/np.sqrt(Cs2):.3e}",
        eL=f"{abs(vL-np.sqrt(Cp2))/np.sqrt(Cp2):.3e}",
    )

    # bar (28) same ratio
    E = mu_n * (3 * lam_n + 2 * mu_n) / (lam_n + mu_n)
    Vc2 = E / rho_n
    rels_bar = []
    for kk in ks:
        Vgh = np.sqrt(Vc2) * np.sqrt((1 + g_n**2 * kk**2) / (1 + h_n**2 * kk**2))
        Vh = np.sqrt(caseH_omega2(Vc2, l_n, ell_n, kk)) / kk
        rels_bar.append(abs(Vgh - Vh) / Vgh)
    check(
        "L3 bar (28) vs Case-H 1D modulus E after [B] ID",
        max(rels_bar) < 1e-12,
        max_rel=f"{max(rels_bar):.3e}",
    )

    # --- Layer 3b: g,h regimes ---
    C = np.sqrt(Cs2)
    kbig = 1e6
    # g < h  => V < C
    V = C * np.sqrt((1 + g_n**2 * kbig**2) / (1 + h_n**2 * kbig**2))
    check("L3b g<h => V_inf = C g/h < C", V < C and abs(V - C * g_n / h_n) / C < 1e-10, V_over_C=f"{V/C:.6f}")
    # g = h
    Veq = C * np.sqrt((1 + h_n**2 * kbig**2) / (1 + h_n**2 * kbig**2))
    check("L3b g=h => V=C (no dispersion)", abs(Veq - C) / C < 1e-14)
    # h=0 unbounded: V ~ C g k
    Vhs = []
    for kk in (10.0, 100.0, 1.0e5):
        Vhs.append(C * np.sqrt(1 + g_n**2 * kk**2))  # h=0
    asympt = C * g_n * 1.0e5
    check(
        "L3b h=0 V increases ~ C g k (unbounded)",
        Vhs[0] < Vhs[1] < Vhs[2] and abs(Vhs[2] / asympt - 1) < 1e-7,
        V_1e5=f"{Vhs[2]:.6g}",
        ratio=f"{Vhs[2]/asympt:.8f}",
    )
    # Case-H ell=0 same
    vH = np.sqrt(caseH_omega2(Cs2, l_n, 0.0, 1000.0)) / 1000.0
    vP = C * np.sqrt(1 + g_n**2 * 1000.0**2)
    check("L3b Case-H ell=0 matches PB h=0 after ID", abs(vH - vP) / vP < 1e-12, rel=f"{abs(vH-vP)/vP:.3e}")

    # g=0 bounded -> 0
    V0 = C / np.sqrt(1 + h_n**2 * kbig**2)
    check("L3b g=0 V->0 bounded", V0 < 1e-4)

    print()
    print(f"TOTAL {PASS+FAIL}  PASS {PASS}  FAIL {FAIL}")
    print("CLASSIFICATION: L3 is [B] specialisation vs [C] PB formulae; not PCR1 published-curve.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
