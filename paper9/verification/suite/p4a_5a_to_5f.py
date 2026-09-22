#!/usr/bin/env python3
"""P4A early solver verification 5a-5f.

Reuses M14 4x4 Gauss assembly and M15 T(k) (same mu on all 4 BFS DOF types).
One homogeneous BFS rectangle = unit cell. No production bands, no Case C, no P3.
"""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

import numpy as np

try:
    from scipy.linalg import eigh as geigh
except ImportError:
    geigh = None

PASS = FAIL = 0
ROWS = []


def check(name, cond, **meta):
    global PASS, FAIL
    ok = bool(cond)
    PASS += ok
    FAIL += not ok
    rec = {"name": name, "result": "PASS" if ok else "FAIL", **meta}
    ROWS.append(rec)
    extra = ""
    for k, v in meta.items():
        if k in ("abs", "rel", "tol", "metric"):
            extra += f"  {k}={v}"
    print(("PASS" if ok else "FAIL") + ": " + name + extra)


def idx(node, comp, typ):
    return 8 * node + 4 * comp + typ


def hermite_num(s, h):
    t = s / h
    H = np.array(
        [1 - 3 * t**2 + 2 * t**3, h * (t - 2 * t**2 + t**3), 3 * t**2 - 2 * t**3, h * (-t**2 + t**3)],
        float,
    )
    dH = np.array(
        [(-6 * t + 6 * t**2) / h, 1 - 4 * t + 3 * t**2, (6 * t - 6 * t**2) / h, -2 * t + 3 * t**2],
        float,
    )
    d2H = np.array(
        [(-6 + 12 * t) / h**2, (-4 + 6 * t) / h, (6 - 12 * t) / h**2, (-2 + 6 * t) / h],
        float,
    )
    return H, dH, d2H


XEND = [0, 2, 2, 0]
YEND = [0, 0, 2, 2]


def gauss4():
    a = np.sqrt(3 / 7 - 2 / 7 * np.sqrt(6 / 5))
    b = np.sqrt(3 / 7 + 2 / 7 * np.sqrt(6 / 5))
    wa = (18 + np.sqrt(30)) / 36
    wb = (18 - np.sqrt(30)) / 36
    return [(-b, wb), (-a, wa), (a, wa), (b, wb)]


def assemble_KM(hx=1.0, hy=1.0, lam=1.0, mu=1.0, L11=1.0, L22=1.0, L12=0.0, rho=1.0, ell2=0.25):
    """M14/M15 assembly: K = Kc+Kg, M = M0+ell2 Mg. Factor 1/10 as M14."""
    Cbar = np.array([[lam + 2 * mu, lam, 0], [lam, lam + 2 * mu, 0], [0, 0, 2 * mu]], float)
    G = np.diag([1.0, 1.0, 2.0]) @ Cbar
    Lmat = np.array([[L11, L12], [L12, L22]], float)
    nd = gauss4()
    Kc = np.zeros((32, 32))
    Kg = np.zeros((32, 32))
    M0 = np.zeros((32, 32))
    Mg = np.zeros((32, 32))
    for xi, wi in nd:
        for eta, wj in nd:
            xv = (xi + 1) / 2 * hx
            yv = (eta + 1) / 2 * hy
            wjac = wi * wj * hx * hy / 4
            Hx, dHx, d2Hx = hermite_num(xv, hx)
            Hy, dHy, d2Hy = hermite_num(yv, hy)
            Nv = np.zeros((4, 4))
            Nx = np.zeros((4, 4))
            Ny = np.zeros((4, 4))
            Nxx = np.zeros((4, 4))
            Nxy = np.zeros((4, 4))
            Nyy = np.zeros((4, 4))
            for ndi in range(4):
                ax, ay = XEND[ndi], YEND[ndi]
                for ty in range(4):
                    dx = 1 if ty in (1, 3) else 0
                    dy = 1 if ty in (2, 3) else 0
                    ix, iy = ax + dx, ay + dy
                    Nv[ndi, ty] = Hx[ix] * Hy[iy]
                    Nx[ndi, ty] = dHx[ix] * Hy[iy]
                    Ny[ndi, ty] = Hx[ix] * dHy[iy]
                    Nxx[ndi, ty] = d2Hx[ix] * Hy[iy]
                    Nxy[ndi, ty] = dHx[ix] * dHy[iy]
                    Nyy[ndi, ty] = Hx[ix] * d2Hy[iy]
            Nmat = np.zeros((2, 32))
            B = np.zeros((3, 32))
            Bx = np.zeros((3, 32))
            By = np.zeros((3, 32))
            Nxmat = np.zeros((2, 32))
            Nymat = np.zeros((2, 32))
            for ndi in range(4):
                for c in range(2):
                    for ty in range(4):
                        j = idx(ndi, c, ty)
                        Nmat[c, j] = Nv[ndi, ty]
                        Nxmat[c, j] = Nx[ndi, ty]
                        Nymat[c, j] = Ny[ndi, ty]
                        if c == 0:
                            B[0, j] = Nx[ndi, ty]
                            B[2, j] = 0.5 * Ny[ndi, ty]
                            Bx[0, j] = Nxx[ndi, ty]
                            Bx[2, j] = 0.5 * Nxy[ndi, ty]
                            By[0, j] = Nxy[ndi, ty]
                            By[2, j] = 0.5 * Nyy[ndi, ty]
                        else:
                            B[1, j] = Ny[ndi, ty]
                            B[2, j] = 0.5 * Nx[ndi, ty]
                            Bx[1, j] = Nxy[ndi, ty]
                            Bx[2, j] = 0.5 * Nxx[ndi, ty]
                            By[1, j] = Nyy[ndi, ty]
                            By[2, j] = 0.5 * Nxy[ndi, ty]
            Kc += wjac * (B.T @ G @ B)
            Kg += wjac * (1 / 10) * (
                Lmat[0, 0] * (Bx.T @ G @ Bx)
                + Lmat[0, 1] * (Bx.T @ G @ By)
                + Lmat[1, 0] * (By.T @ G @ Bx)
                + Lmat[1, 1] * (By.T @ G @ By)
            )
            M0 += wjac * rho * (Nmat.T @ Nmat)
            Mg += wjac * rho * (Nxmat.T @ Nxmat + Nymat.T @ Nymat)
    return Kc + Kg, M0 + ell2 * Mg


def T_impl(kx, ky, L=1.0):
    mx = np.exp(1j * kx * L)
    my = np.exp(1j * ky * L)
    phases = [1.0, mx, mx * my, my]
    T = np.zeros((32, 8), dtype=complex)
    for n, ph in enumerate(phases):
        T[8 * n : 8 * (n + 1), :] = ph * np.eye(8)
    return T


def reduce_mat(A, T):
    return T.conj().T @ A @ T


def fro_rel(A, B):
    nrm = np.linalg.norm(A, "fro")
    return 0.0 if nrm == 0 else float(np.linalg.norm(A - B, "fro") / nrm)


def fro_abs(A, B):
    return float(np.linalg.norm(A - B, "fro"))


def L_plane(l1, l2, theta):
    """M02: L = R^T diag(l1^2,l2^2) R, R rotation about z (blueprint (5)-(8))."""
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s], [s, c]])
    D = np.diag([l1**2, l2**2])
    Lp = R.T @ D @ R
    return float(Lp[0, 0]), float(Lp[1, 1]), float(Lp[0, 1])


def omega2(K, M, kx, ky, L=1.0):
    T = T_impl(kx, ky, L)
    Kb = reduce_mat(K, T)
    Mb = reduce_mat(M, T)
    if geigh is not None:
        w = geigh(Kb, Mb, eigvals_only=True)
    else:
        w = np.real(np.linalg.eigvals(np.linalg.solve(Mb, Kb)))
    w = np.sort(np.real(w))
    return w, Kb, Mb


PARAMS = dict(
    Lcell=1.0,
    lam=1.0,
    mu=1.0,
    rho=1.0,
    ell2=0.04,
    l_iso=0.2,
    l1_aniso=0.30,
    l2_aniso=0.10,
    hx=1.0,
    hy=1.0,
)
Lcell = PARAMS["Lcell"]
TOL_H = 1e-12
TOL_BZ = 1e-10
TOL_ROT = 1e-10
TOL_SLOPE = 1e-6
TOL_SYM = 1e-10


def main():
    print("P4A 5a-5f  python", sys.version.split()[0], "numpy", np.__version__)
    print("params", PARAMS)

    # ----- 5a Hermiticity -----
    L11, L22, L12 = L_plane(PARAMS["l_iso"], PARAMS["l_iso"], 0.0)
    K, M = assemble_KM(
        hx=PARAMS["hx"],
        hy=PARAMS["hy"],
        lam=PARAMS["lam"],
        mu=PARAMS["mu"],
        L11=L11,
        L22=L22,
        L12=L12,
        rho=PARAMS["rho"],
        ell2=PARAMS["ell2"],
    )
    ks_5a = [
        ("interior", (3 * np.pi / (7 * Lcell), 2 * np.pi / (5 * Lcell))),
        ("interior2", (0.4 * np.pi / Lcell, 0.7 * np.pi / Lcell)),
        ("Gamma", (0.0, 0.0)),
        ("X", (np.pi / Lcell, 0.0)),
        ("M", (np.pi / Lcell, np.pi / Lcell)),
    ]
    max_rel_K = 0.0
    max_rel_M = 0.0
    for name, (kx, ky) in ks_5a:
        T = T_impl(kx, ky, Lcell)
        Kb = reduce_mat(K, T)
        Mb = reduce_mat(M, T)
        rK = fro_rel(Kb.conj().T, Kb)
        rM = fro_rel(Mb.conj().T, Mb)
        aK = fro_abs(Kb.conj().T, Kb)
        aM = fro_abs(Mb.conj().T, Mb)
        max_rel_K = max(max_rel_K, rK)
        max_rel_M = max(max_rel_M, rM)
        check(
            f"5a Hermiticity Kbar {name} k={kx:.6g},{ky:.6g} dim={Kb.shape}",
            rK < TOL_H,
            abs=aK,
            rel=rK,
            tol=TOL_H,
        )
        check(
            f"5a Hermiticity Mbar {name}",
            rM < TOL_H,
            abs=aM,
            rel=rM,
            tol=TOL_H,
        )
    print(f"5a max rel K={max_rel_K:.3e} M={max_rel_M:.3e}")

    # ----- 5b BZ periodicity -----
    kint = (3 * np.pi / (7 * Lcell), 2 * np.pi / (5 * Lcell))
    Gs = [
        (2 * np.pi / Lcell, 0.0),
        (0.0, 2 * np.pi / Lcell),
        (2 * np.pi / Lcell, 2 * np.pi / Lcell),
    ]
    w0, Kb0, Mb0 = omega2(K, M, *kint, Lcell)
    for G in Gs:
        kx = kint[0] + G[0]
        ky = kint[1] + G[1]
        wG, KbG, MbG = omega2(K, M, kx, ky, Lcell)
        rK = fro_rel(KbG, Kb0)
        rM = fro_rel(MbG, Mb0)
        dw = float(np.max(np.abs(wG - w0)) / max(1.0, np.max(np.abs(w0))))
        check(
            f"5b Kbar(k+G)=Kbar(k) G={G}",
            rK < TOL_H,
            rel=rK,
            abs=fro_abs(KbG, Kb0),
            tol=TOL_H,
        )
        check(
            f"5b Mbar(k+G)=Mbar(k) G={G}",
            rM < TOL_H,
            rel=rM,
            abs=fro_abs(MbG, Mb0),
            tol=TOL_H,
        )
        check(
            f"5b eig(k+G)=eig(k) G={G}",
            dw < TOL_BZ,
            rel=dw,
            tol=TOL_BZ,
        )

    # ----- 5c rotational invariance AR=1 -----
    thetas = [0.0, 15.0, 37.0, 90.0, 128.0]
    k_c = (0.31 * np.pi / Lcell, 0.47 * np.pi / Lcell)
    w_ref = None
    max_dw = 0.0
    for thd in thetas:
        th = np.deg2rad(thd)
        L11, L22, L12 = L_plane(PARAMS["l_iso"], PARAMS["l_iso"], th)
        Kt, Mt = assemble_KM(
            lam=PARAMS["lam"],
            mu=PARAMS["mu"],
            L11=L11,
            L22=L22,
            L12=L12,
            rho=PARAMS["rho"],
            ell2=PARAMS["ell2"],
        )
        w, _, _ = omega2(Kt, Mt, *k_c, Lcell)
        if w_ref is None:
            w_ref = w
        dw = float(np.max(np.abs(w - w_ref)) / max(1.0, np.max(np.abs(w_ref))))
        max_dw = max(max_dw, dw)
        check(
            f"5c AR=1 theta={thd} vs 0 interior k spectrum",
            dw < TOL_ROT,
            rel=dw,
            tol=TOL_ROT,
        )
    print(f"5c max rel eig diff={max_dw:.3e}")

    # ----- 5d long-wave slope -----
    L11, L22, L12 = L_plane(PARAMS["l_iso"], PARAMS["l_iso"], 0.0)
    K, M = assemble_KM(
        lam=PARAMS["lam"],
        mu=PARAMS["mu"],
        L11=L11,
        L22=L22,
        L12=L12,
        rho=PARAMS["rho"],
        ell2=PARAMS["ell2"],
    )
    cT = np.sqrt(PARAMS["mu"] / PARAMS["rho"])
    cL = np.sqrt((PARAMS["lam"] + 2 * PARAMS["mu"]) / PARAMS["rho"])
    kappas = [1e-2, 3e-3, 1e-3, 3e-4, 1e-4]
    slope_rows = []
    for kap in kappas:
        w, _, _ = omega2(K, M, kap, 0.0, Lcell)
        # two acoustic: smallest positive omega = sqrt(omega2)
        om = np.sqrt(np.maximum(w, 0.0))
        v = om[:2] / kap
        v_sorted = np.sort(v)
        eT = abs(v_sorted[0] - cT) / cT
        eL = abs(v_sorted[1] - cL) / cL
        slope_rows.append((kap, float(v_sorted[0]), float(v_sorted[1]), eT, eL))
        print(f"  5d kappa={kap:.1e} v=({v_sorted[0]:.8f},{v_sorted[1]:.8f}) eT={eT:.3e} eL={eL:.3e}")
    # criterion: at least two smallest-k points with both errors < 1e-6
    ok_pts = [r for r in slope_rows if r[3] < TOL_SLOPE and r[4] < TOL_SLOPE]
    best = min(slope_rows, key=lambda r: max(r[3], r[4]))
    check(
        "5d acoustic slopes vT,vL relative error <1e-6 at >=2 small-k points",
        len(ok_pts) >= 2,
        metric=f"n_ok={len(ok_pts)} best_eT={best[3]:.3e} best_eL={best[4]:.3e} kappa_best={best[0]}",
        tol=TOL_SLOPE,
    )
    # sequence must improve toward small k until roundoff
    emax_seq = [max(r[3], r[4]) for r in slope_rows]
    print("  5d max(eT,eL) sequence", ["%.3e" % e for e in emax_seq])

    # ----- 5e theta+90 with l1 <-> l2 -----
    th0 = np.deg2rad(20.0)
    L11a, L22a, L12a = L_plane(PARAMS["l1_aniso"], PARAMS["l2_aniso"], th0)
    L11b, L22b, L12b = L_plane(PARAMS["l2_aniso"], PARAMS["l1_aniso"], th0 + np.pi / 2)
    Ka, Ma = assemble_KM(
        lam=PARAMS["lam"], mu=PARAMS["mu"], L11=L11a, L22=L22a, L12=L12a,
        rho=PARAMS["rho"], ell2=PARAMS["ell2"],
    )
    Kb, Mb = assemble_KM(
        lam=PARAMS["lam"], mu=PARAMS["mu"], L11=L11b, L22=L22b, L12=L12b,
        rho=PARAMS["rho"], ell2=PARAMS["ell2"],
    )
    ks_e = [
        (0.31 * np.pi / Lcell, 0.47 * np.pi / Lcell),
        (0.22 * np.pi / Lcell, -0.18 * np.pi / Lcell),
        (0.6 * np.pi / Lcell, 0.15 * np.pi / Lcell),
    ]
    max_e = 0.0
    for kx, ky in ks_e:
        wa, _, _ = omega2(Ka, Ma, kx, ky, Lcell)
        wb, _, _ = omega2(Kb, Mb, kx, ky, Lcell)
        dw = float(np.max(np.abs(wa - wb)) / max(1.0, np.max(np.abs(wa))))
        max_e = max(max_e, dw)
        check(
            f"5e theta+90 l1<->l2 k=({kx:.4g},{ky:.4g})",
            dw < TOL_SYM,
            rel=dw,
            tol=TOL_SYM,
        )
    # sanity: without swap, spectra differ
    L11c, L22c, L12c = L_plane(PARAMS["l1_aniso"], PARAMS["l2_aniso"], th0 + np.pi / 2)
    Kc, Mc = assemble_KM(
        lam=PARAMS["lam"], mu=PARAMS["mu"], L11=L11c, L22=L22c, L12=L12c,
        rho=PARAMS["rho"], ell2=PARAMS["ell2"],
    )
    wa, _, _ = omega2(Ka, Ma, *ks_e[0], Lcell)
    wc, _, _ = omega2(Kc, Mc, *ks_e[0], Lcell)
    d_noswap = float(np.max(np.abs(wa - wc)) / max(1.0, np.max(np.abs(wa))))
    check(
        "5e negative control: theta+90 WITHOUT l1<->l2 is NOT identical",
        d_noswap > 1e-6,
        rel=d_noswap,
    )
    print(f"5e max rel with swap={max_e:.3e} noswap={d_noswap:.3e}")

    # ----- 5f positive definiteness -----
    L11, L22, L12 = L_plane(PARAMS["l_iso"], PARAMS["l_iso"], 0.0)
    K, M = assemble_KM(
        lam=PARAMS["lam"], mu=PARAMS["mu"], L11=L11, L22=L22, L12=L12,
        rho=PARAMS["rho"], ell2=PARAMS["ell2"],
    )
    wG, KbG, MbG = omega2(K, M, 0.0, 0.0, Lcell)
    evals_KG = np.sort(np.real(np.linalg.eigvalsh((KbG + KbG.conj().T) / 2)))
    evals_MG = np.sort(np.real(np.linalg.eigvalsh((MbG + MbG.conj().T) / 2)))
    print("  5f Gamma Kbar eigs", evals_KG)
    print("  5f Gamma Mbar eigs min/max", evals_MG[0], evals_MG[-1])
    # two acoustic null modes of Kbar at Gamma expected
    nK = np.linalg.norm(KbG, "fro")
    check(
        "5f Gamma: two near-null Kbar modes (translations), rest >0",
        evals_KG[0] / nK < 1e-10
        and evals_KG[1] / nK < 1e-10
        and evals_KG[2] > 0,
        metric=f"e0={evals_KG[0]:.3e} e1={evals_KG[1]:.3e} e2={evals_KG[2]:.3e}",
    )
    check(
        "5f Gamma Mbar SPD min eig>0",
        evals_MG[0] > 0,
        metric=f"min={evals_MG[0]:.3e} max={evals_MG[-1]:.3e} cond={evals_MG[-1]/evals_MG[0]:.3e}",
    )
    kint = (3 * np.pi / (7 * Lcell), 2 * np.pi / (5 * Lcell))
    wi, Kbi, Mbi = omega2(K, M, *kint, Lcell)
    evals_Ki = np.sort(np.real(np.linalg.eigvalsh((Kbi + Kbi.conj().T) / 2)))
    evals_Mi = np.sort(np.real(np.linalg.eigvalsh((Mbi + Mbi.conj().T) / 2)))
    check(
        "5f interior Kbar PD (min eig>0; no rigid-body null at k≠0)",
        evals_Ki[0] > 0,
        metric=f"min={evals_Ki[0]:.3e} max={evals_Ki[-1]:.3e}",
    )
    check(
        "5f interior Mbar SPD",
        evals_Mi[0] > 0,
        metric=f"min={evals_Mi[0]:.3e} max={evals_Mi[-1]:.3e} cond={evals_Mi[-1]/evals_Mi[0]:.3e}",
    )
    check(
        "5f interior all omega^2 > 0",
        np.min(wi) > 0,
        metric=f"min_om2={np.min(wi):.3e}",
    )

    print()
    print(f"TOTAL {PASS + FAIL}  PASS {PASS}  FAIL {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    rc = main()
    out = Path(__file__).resolve().parent.parent.parent / "verification" / "suite"
    # scripts live in paper9/verification/suite or paper9/eqs/phase4a
    sys.exit(rc)
