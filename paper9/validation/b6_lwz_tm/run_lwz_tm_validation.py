#!/usr/bin/env python3
"""LWZ2016 independent SH-normal TM: Level 1 homogeneous, Level 2 bilayer.

ACCEPTANCE (declared before any comparison numbers are computed):
  L1: max_i |k_Bloch(sigma_i) - sigma_i| / sigma_i  < 1e-8
      max_i |lambda - exp(i sigma a)|               < 1e-8
  L1 robustness: same with 2x smaller a (period) must still satisfy 1e-8.
  L2: bilayer TM is executed with Fig. 3 parameters (PDF p.10).
      Published Fig. 3 has NO tabulated omega(k). Therefore L2 does NOT
      claim a percent error vs the figure. Quantitative L2 check =
      identical-layer reduction: bilayer with (c2,d2,mu2,rho2)=(c1,d1,mu1,rho1)
      and a1=a2=a/2 must recover L1 homogeneous to 1e-7 in relative k.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

from lwz_tm_sh_normal import (
    bilayer_T,
    layer_T_sh_normal,
    min_svd_residual,
    omega_from_sigma,
    propagating_k_from_T,
    scan_omega_for_k,
    sigma_tau_from_omega,
)

TOL_L1 = 1e-8
TOL_L2_IDENT = 1e-7

# dimensional unit cell (any consistent SI; ratios from paper)
A = 1.0
MU1 = 1.0
RHO1 = 1.0
VS1 = np.sqrt(MU1 / RHO1)

# Fig. 3 (PDF p.10): cbar1=sqrt(c1)/a = 0.5, dbar1=d1/a=0.5, cbar=c1/c2=0.77, dbar=d1/d2=2
# a1/a=0.5
CBAR1, DBAR1, CBAR, DBAR = 0.5, 0.5, 0.77, 2.0
C1 = (CBAR1 * A) ** 2
D1 = DBAR1 * A
C2 = C1 / CBAR
D2 = D1 / DBAR
A1 = 0.5 * A
A2 = 0.5 * A
# remaining Fig.3 / p.10 ratios
VS2 = 0.5947 * VS1
RHO2 = 0.1573 * RHO1
MU2 = RHO2 * VS2**2  # Vs^2 = mu/rho

PASS = FAIL = 0
ROWS = []


def check(name, cond, **meta):
    global PASS, FAIL
    ok = bool(cond)
    PASS += ok
    FAIL += not ok
    extra = " ".join(f"{k}={v}" for k, v in meta.items())
    print(("PASS" if ok else "FAIL") + ": " + name + (("  " + extra) if extra else ""))


def main():
    print("ACCEPTANCE L1 rel_k <", TOL_L1, "  |lam-exp| <", TOL_L1)
    print("ACCEPTANCE L2 identical-layer rel_k <", TOL_L2_IDENT)
    print("params C1,D1,C2,D2", C1, D1, C2, D2)

    # ----- Level 1: homogeneous, one layer thickness A, material 1 -----
    sigmas = np.array(
        [0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, np.pi / A * 0.25, np.pi / A * 0.6]
    )
    rels, lam_err, svd_res = [], [], []
    table = []
    for sig in sigmas:
        om = omega_from_sigma(sig, VS1, C1, D1)
        T, sig_b, tau_b = layer_T_sh_normal(om, A, C1, D1, MU1, RHO1)
        kB, lam, dist = propagating_k_from_T(T, A, sigma_ref=sig)
        # fold to (-pi/a, pi/a]
        # compare to sigma folded into first BZ
        sig_fold = ((sig + np.pi / A) % (2 * np.pi / A)) - np.pi / A
        rel = abs(kB - sig_fold) / max(abs(sig_fold), 1e-12)
        res, cond = min_svd_residual(T, sig, A)  # use unfolded sigma in phase e^{i sigma A}
        rels.append(rel)
        lam_err.append(dist)
        svd_res.append(res)
        table.append(
            dict(
                sigma=float(sig),
                omega=float(om),
                k_bloch=float(kB),
                rel_k=float(rel),
                lam_dist=float(dist),
                svd_min=float(res),
                cond=float(cond),
                sigma_from_omega=float(sig_b),
            )
        )
        print(
            f"  L1 sigma={sig:.5f} om={om:.5f} kB={kB:.5f} rel={rel:.3e} "
            f"|lam-e|={dist:.3e} svd={res:.3e}"
        )

    max_rel = max(rels)
    max_lam = max(lam_err)
    rms_rel = float(np.sqrt(np.mean(np.square(rels))))
    worst = int(np.argmax(rels))
    check(
        "L1 homogeneous TM vs (14.1): max rel k and |lam-exp|",
        max_rel < TOL_L1 and max_lam < TOL_L1,
        max_rel=f"{max_rel:.3e}",
        rms_rel=f"{rms_rel:.3e}",
        max_lam=f"{max_lam:.3e}",
        worst_sigma=f"{sigmas[worst]:.5g}",
        n=len(sigmas),
    )

    # robustness: half thickness, one sigma
    sig = 1.0
    om = omega_from_sigma(sig, VS1, C1, D1)
    T2, *_ = layer_T_sh_normal(om, 0.5 * A, C1, D1, MU1, RHO1)
    kB2, lam2, dist2 = propagating_k_from_T(T2, 0.5 * A, sigma_ref=sig)
    rel2 = abs(kB2 - sig) / sig
    check(
        "L1 robustness half-thickness same sigma",
        rel2 < TOL_L1 and dist2 < TOL_L1,
        rel=f"{rel2:.3e}",
        lam_dist=f"{dist2:.3e}",
    )

    # ----- Level 2: identical bilayer = homogeneous -----
    # two layers a/2, same material
    ident_rels = []
    for sig in [0.2, 1.0, 2.5]:
        om = omega_from_sigma(sig, VS1, C1, D1)
        Tcell = bilayer_T(om, A / 2, A / 2, C1, C1, D1, D1, MU1, MU1, RHO1, RHO1)
        kB, lam, dist = propagating_k_from_T(Tcell, A, sigma_ref=sig)
        sig_fold = ((sig + np.pi / A) % (2 * np.pi / A)) - np.pi / A
        rel = abs(kB - sig_fold) / max(abs(sig_fold), 1e-12)
        ident_rels.append(rel)
        print(f"  L2ident sigma={sig:.3f} kB={kB:.5f} rel={rel:.3e} |lam-e|={dist:.3e}")
    check(
        "L2 identical-layer bilayer recovers homogeneous (14.1)",
        max(ident_rels) < TOL_L2_IDENT,
        max_rel=f"{max(ident_rels):.3e}",
    )

    # ----- Level 2: true bilayer Fig.3 parameters, first BZ, acoustic window -----
    # no published omega table — report TM branches only, no % vs figure
    vm = A / (A1 / VS1 + A2 / VS2)  # LWZ PDF p.10 vertical-axis scale
    kbars = np.array([0.05, 0.15, 0.25, 0.40, 0.55, 0.70, 0.85, 0.95])
    ks = kbars * np.pi / A
    bilayer_rows = []
    dws = []
    for k, kbar in zip(ks, kbars):
        # acoustic window around k*vm; widen at large kbar for dispersion
        om_c = k * vm
        lo, hi = 0.25 * om_c, 4.0 * om_c
        omegas_coarse = np.linspace(lo, hi, 250)
        omegas_fine = np.linspace(lo, hi, 500)
        best_c, _ = scan_omega_for_k(
            k, A, A1, A2, C1, C2, D1, D2, MU1, MU2, RHO1, RHO2, omegas_coarse
        )
        best_f, _ = scan_omega_for_k(
            k, A, A1, A2, C1, C2, D1, D2, MU1, MU2, RHO1, RHO2, omegas_fine
        )
        if best_c is None or best_f is None:
            check(f"L2 bilayer root k={k:.4g}", False)
            continue
        wc, rc, cc = best_c
        wf, rf, cf = best_f
        dw = abs(wf - wc) / max(wf, 1e-30)
        dws.append(dw)
        wbar = wf * A / (2 * np.pi * vm)
        bilayer_rows.append(
            dict(
                k=float(k),
                kbar=float(kbar),
                omega_coarse=float(wc),
                omega_fine=float(wf),
                rel_dw=float(dw),
                svd_fine=float(rf),
                wbar_fig3_axis=float(wbar),
            )
        )
        print(
            f"  L2bil kbar={kbar:.3f} om_f={wf:.5f} dw={dw:.3e} svd={rf:.3e} wbar={wbar:.4f}"
        )
    check(
        "L2 bilayer TM produced roots on k-grid (no published omega table)",
        len(bilayer_rows) == len(ks),
        n=len(bilayer_rows),
    )
    if dws:
        check(
            "L2 robustness: coarse vs 2x-finer omega grid max rel d(omega)",
            max(dws) < 5e-3,
            max_rel_dw=f"{max(dws):.3e}",
            note="grid resolution not TM physics; 5e-3 is search-grid tolerance",
        )

    print()
    print(f"TOTAL {PASS+FAIL}  PASS {PASS}  FAIL {FAIL}")
    print("NO PCR1/G3 claim. NO B6 PASS vs Fig.3 (no tabulated omega).")
    out = {
        "tol_L1": TOL_L1,
        "L1_max_rel": max_rel,
        "L1_rms_rel": rms_rel,
        "L1_table": table,
        "L2_ident_max_rel": max(ident_rels),
        "L2_bilayer": bilayer_rows,
        "PASS": PASS,
        "FAIL": FAIL,
    }
    Path("lwz_tm_results.json").write_text(json.dumps(out, indent=2))
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
