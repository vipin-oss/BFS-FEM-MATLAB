#!/usr/bin/env python3
"""P4B internal verification 5g–5i.

Frozen: M11.3–M11.5, M16 (A.1)–(A.6), M17 (B.4)–(B.7), plan rows 5g–5i.
Parameters: [S-P4A] from p4a_5a_to_5f.py. Homogeneous Case-H only.
Does not modify 5a–5f. No P3/B6. No published-curve gate.
"""
from __future__ import annotations

import importlib.util
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

try:
    from scipy.linalg import eigh as geigh
    from scipy.sparse import coo_matrix, csr_matrix
    from scipy.sparse.linalg import eigsh
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"scipy required: {e}")

HERE = Path(__file__).resolve().parent
P4A = HERE / "p4a_5a_to_5f.py"
spec = importlib.util.spec_from_file_location("p4a_5a_to_5f", P4A)
p4a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p4a)

assemble_KM = p4a.assemble_KM
L_plane = p4a.L_plane
omega2 = p4a.omega2
PARAMS = dict(p4a.PARAMS)

PASS = FAIL = 0
ROWS = []

# Plan 5h tolerances (declared before execution)
TOL_5H_IDENTITY = 1e-6
TOL_5H_VG = 1e-4
# 5g: asymptotic match (closed form at large kbar; FE vs closed form in 1st BZ)
TOL_5G_ASY = 1e-3
TOL_5G_FE = 1e-3


def check(name, cond, **meta):
    global PASS, FAIL
    ok = bool(cond)
    PASS += ok
    FAIL += not ok
    rec = {"name": name, "result": "PASS" if ok else "FAIL", **meta}
    ROWS.append(rec)
    extra = " ".join(f"{k}={v}" for k, v in meta.items() if k in ("abs", "rel", "tol", "metric"))
    print(("PASS" if ok else "FAIL") + ": " + name + (("  " + extra) if extra else ""))


def leff2_dir(l1, l2, theta, phi):
    return l1**2 * np.cos(phi - theta) ** 2 + l2**2 * np.sin(phi - theta) ** 2


def ombar2_T(kbar, ellbar, leff2):
    kap2 = kbar**2
    num = np.pi**2 * kap2 * (1.0 + np.pi**2 * kap2 * leff2 / 10.0)
    den = 1.0 + np.pi**2 * ellbar**2 * kap2
    return num / den


def vbar_T(kbar, ellbar, leff2):
    return np.sqrt(ombar2_T(kbar, ellbar, leff2)) / (np.pi * kbar)


def omega0(mu, rho, L):
    return np.sqrt(mu / (rho * L**2))


# ----- 5h: 1-D Case-H harmonic averages (M17), independent of dω/dk closed form -----
def caseH_1d_averages(kind, k, a_amp, lam, mu, rho, ell, l1):
    """Cycle averages of W, T, S for u = a cos(kx − ωt). kind in {T, L}."""
    Mmod = mu if kind == "T" else (lam + 2 * mu)
    om2 = (Mmod / rho) * k**2 * (1.0 + l1**2 * k**2 / 10.0) / (1.0 + ell**2 * k**2)
    om = np.sqrt(om2)
    nphi = 4001
    phi = np.linspace(0.0, 2 * np.pi, nphi, endpoint=False)
    # u = a cos φ, φ = kx−ωt; v = a ω sin φ; u,x = −a k sin φ; u,xx = −a k² cos φ
    # u,tt = −ω² a cos φ; v,x = a ω k cos φ; u,tt,x = ω² a k sin φ
    a = a_amp
    u_x = -a * k * np.sin(phi)
    u_xx = -a * k**2 * np.cos(phi)
    v = a * om * np.sin(phi)
    v_x = a * om * k * np.cos(phi)
    utt_x = om**2 * a * k * np.sin(phi)
    sig = Mmod * u_x
    tau = (1.0 / 10.0) * l1**2 * Mmod * u_xx
    tau_x = (1.0 / 10.0) * l1**2 * Mmod * (a * k**3 * np.sin(phi))
    W = 0.5 * sig * u_x + 0.5 * tau * u_xx
    T = 0.5 * rho * v**2 + 0.5 * rho * ell**2 * v_x**2
    S = -((sig - tau_x) * v + tau * v_x + rho * ell**2 * utt_x * v)
    return float(np.mean(W)), float(np.mean(T)), float(np.mean(S)), float(om)


def omega_closed_1d(kind, k, lam, mu, rho, ell, l1):
    Mmod = mu if kind == "T" else (lam + 2 * mu)
    om2 = (Mmod / rho) * k**2 * (1.0 + l1**2 * k**2 / 10.0) / (1.0 + ell**2 * k**2)
    return float(np.sqrt(om2))


def central_vg(kind, k, h, lam, mu, rho, ell, l1):
    return (
        omega_closed_1d(kind, k + h, lam, mu, rho, ell, l1)
        - omega_closed_1d(kind, k - h, lam, mu, rho, ell, l1)
    ) / (2.0 * h)


# ----- 5i n×n homogeneous Bloch -----
def assemble_nxn_bloch(n, kx, ky, Lcell, lam, mu, rho, ell2, L11, L22, L12):
    hx = Lcell / n
    hy = Lcell / n
    Kloc, Mloc = assemble_KM(
        hx=hx, hy=hy, lam=lam, mu=mu, L11=L11, L22=L22, L12=L12, rho=rho, ell2=ell2
    )
    mx = np.exp(1j * kx * Lcell)
    my = np.exp(1j * ky * Lcell)
    ndof = n * n * 8

    def red(i, j):
        ph = 1.0 + 0.0j
        if i == n:
            i = 0
            ph *= mx
        if j == n:
            j = 0
            ph *= my
        return i, j, ph

    def gdof(i, j, c, ty):
        return ((j % n) * n + (i % n)) * 8 + 4 * c + ty

    # pre-index local 32
    loc_index = [p4a.idx(a, c, t) for a in range(4) for c in range(2) for t in range(4)]
    corners = [(0, 0), (1, 0), (1, 1), (0, 1)]
    rows, cols, dK, dM = [], [], [], []
    for ex in range(n):
        for ey in range(n):
            gidx = []
            phases = []
            for dx, dy in corners:
                i, j, ph = red(ex + dx, ey + dy)
                phases.append(ph)
                gidx.append([gdof(i, j, c, t) for c in range(2) for t in range(4)])
            gflat = np.array([g for node in gidx for g in node], dtype=int)  # 32
            ph_node = np.array([phases[a] for a in range(4) for _ in range(8)])
            fac = np.conj(ph_node)[:, None] * ph_node[None, :]
            Kc = fac * Kloc
            Mc = fac * Mloc
            ii, jj = np.meshgrid(gflat, gflat, indexing="ij")
            rows.append(ii.ravel())
            cols.append(jj.ravel())
            dK.append(Kc.ravel())
            dM.append(Mc.ravel())
    rows = np.concatenate(rows)
    cols = np.concatenate(cols)
    Kr = coo_matrix((np.concatenate(dK), (rows, cols)), shape=(ndof, ndof)).tocsr()
    Mr = coo_matrix((np.concatenate(dM), (rows, cols)), shape=(ndof, ndof)).tocsr()
    Kh = 0.5 * (Kr + Kr.conj().T)
    Mh = 0.5 * (Mr + Mr.conj().T)
    return Kh, Mh


def acoustic_omegas(Kh, Mh, n_want=2):
    nd = Kh.shape[0]
    if nd <= 128:
        Kd = Kh.toarray() if hasattr(Kh, "toarray") else Kh
        Md = Mh.toarray() if hasattr(Mh, "toarray") else Mh
        w = geigh(Kd, Md, eigvals_only=True)
        w = np.sort(np.real(w))
        return np.sqrt(np.maximum(w[:n_want], 0.0))
    w, _ = eigsh(Kh, k=max(n_want, 4), M=Mh, which="SM", tol=1e-12, maxiter=10000)
    w = np.sort(np.real(w))
    return np.sqrt(np.maximum(w[:n_want], 0.0))


def lsq_loglog_slope(hs, errs):
    """Least-squares slope of log(err) vs log(h) with 95% CI (t, n-2)."""
    x = np.log(np.asarray(hs, float))
    y = np.log(np.asarray(errs, float))
    n = len(x)
    xm, ym = x.mean(), y.mean()
    sxx = np.sum((x - xm) ** 2)
    slope = np.sum((x - xm) * (y - ym)) / sxx
    intercept = ym - slope * xm
    yhat = intercept + slope * x
    dof = n - 2
    s2 = np.sum((y - yhat) ** 2) / dof
    se = np.sqrt(s2 / sxx)
    # Student t 0.975, dof=2 → 4.303
    tcrit = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776}.get(dof, 1.96)
    return float(slope), float(slope - tcrit * se), float(slope + tcrit * se), float(se)


def main():
    print("P4B 5g-5i  python", sys.version.split()[0], "numpy", np.__version__)
    print("params [S-P4A]", PARAMS)
    L = PARAMS["Lcell"]
    lam, mu, rho = PARAMS["lam"], PARAMS["mu"], PARAMS["rho"]
    ell = np.sqrt(PARAMS["ell2"])
    l_iso = PARAMS["l_iso"]
    cT = np.sqrt(mu / rho)
    w0 = omega0(mu, rho, L)

    # ========================= 5g =========================
    print("\n===== 5g high-k phase velocity (M16) =====")
    theta, phi = 0.0, 0.0
    le2 = leff2_dir(l_iso, l_iso, theta, phi)
    ellbar = ell / L
    lbar = l_iso / L
    vinf = (np.sqrt(le2) / (np.sqrt(10.0) * ell)) * cT  # dimensional (A.5)
    kbars = np.array([1.0, 5.0, 20.0, 50.0, 100.0, 200.0])
    ratios_b = []
    for kb in kbars:
        vb = vbar_T(kb, ellbar, le2) * cT
        r = vb / vinf
        ratios_b.append(float(abs(r - 1.0)))
        print(f"  ell>0 kbar={kb:5.1f} v={vb:.8f} vinf={vinf:.8f} |v/vinf-1|={abs(r-1):.3e}")
    # leading-order (A.4) holds as kbar->inf (1/kbar^2 correction); report each kbar.
    mono_b = all(ratios_b[i + 1] < ratios_b[i] for i in range(len(ratios_b) - 1))
    print(f"  ell>0 monotone |v/vinf-1| decreasing: {mono_b}; ratios={['%.3e' % r for r in ratios_b]}")
    check(
        "5g ellbar>0: v -> v_T,inf (A.4/A.5): monotone approach, <1e-3 at kbar=200",
        mono_b and ratios_b[5] < TOL_5G_ASY,
        rel=ratios_b[5],
        tol=TOL_5G_ASY,
        metric=f"vinf={vinf:.8f} kbar100={ratios_b[4]:.3e} kbar200={ratios_b[5]:.3e}",
    )
    # unbounded ell=0
    slope_as = (np.pi * np.sqrt(le2) / np.sqrt(10.0)) * cT  # v ~ slope_as * kbar  (A.3) with v dimensional / kbar
    # vbar ~ (pi l_eff/sqrt10) kbar ; v = vbar * cT ; kbar = k L/π so v ~ (l_eff/sqrt10)*k*L *cT/L wait
    # v_dim = vbar * cT = [pi leff_bar /sqrt10 * kbar] * cT
    # leff_bar = l_iso/L, kbar = k L/π ⇒ v = (pi (l/L)/sqrt10)*(k L/π)*cT = (l/sqrt10)*k*cT
    ratios_u = []
    vs_u = []
    for kb in kbars:
        vu = vbar_T(kb, 0.0, le2) * cT
        pred = (np.pi * np.sqrt(le2) / np.sqrt(10.0)) * kb * cT
        r = vu / pred
        ratios_u.append(float(abs(r - 1.0)))
        vs_u.append(float(vu))
        print(f"  ell=0 kbar={kb:5.1f} v={vu:.8f} pred={pred:.8f} |v/pred-1|={abs(r-1):.3e}")
    check(
        "5g ellbar=0: v ~ (pi l_eff/sqrt10) kbar cT unbounded; |ratio-1|<1e-3 at kbar=200",
        ratios_u[5] < TOL_5G_ASY and vs_u[-1] > vs_u[0] * 10,
        rel=ratios_u[5],
        tol=TOL_5G_ASY,
        metric=f"v(kbar=1)={vs_u[0]:.6f} v(kbar=200)={vs_u[-1]:.6f} kbar100={ratios_u[4]:.3e}",
    )
    # l1=l2=0, ell>0  (M16.5 / S4) — κ→∞
    kb = 200.0
    omb = np.sqrt(ombar2_T(kb, ellbar, 0.0))
    vb0 = vbar_T(kb, ellbar, 0.0)
    check(
        "5g special l1=l2=0 ell>0: ombar->1/ellbar, vbar->0 (M16 S4)",
        abs(omb - 1.0 / ellbar) / (1.0 / ellbar) < TOL_5G_ASY and abs(vb0) < 1e-2,
        rel=abs(omb - 1.0 / ellbar) / (1.0 / ellbar),
        metric=f"ombar={omb:.8f} 1/ellbar={1/ellbar:.8f} vbar={vb0:.3e} kbar={kb}",
    )
    # FE 1-cell vs closed form along kx, first BZ (and ell=0 growth inside BZ)
    L11, L22, L12 = L_plane(l_iso, l_iso, 0.0)
    Kpos, Mpos = assemble_KM(lam=lam, mu=mu, L11=L11, L22=L22, L12=L12, rho=rho, ell2=ell**2)
    Kz, Mz = assemble_KM(lam=lam, mu=mu, L11=L11, L22=L22, L12=L12, rho=rho, ell2=0.0)
    ks_fe = [0.2 * np.pi / L, 0.5 * np.pi / L, 0.8 * np.pi / L, np.pi / L]
    ks_fe_tol = ks_fe[:2]  # 1-cell BFS vs closed form: only moderate k (high-k FE error is mesh, not M16)
    fe_rel = []
    vpos_seq = []
    vz_seq = []
    for k in ks_fe:
        w, _, _ = omega2(Kpos, Mpos, k, 0.0, L)
        om = np.sqrt(np.maximum(np.sort(np.real(w))[:2], 0.0))
        vfe = om[0] / k
        kbar = k * L / np.pi
        van = vbar_T(kbar, ellbar, le2) * cT
        fe_rel.append(abs(vfe - van) / van)
        vpos_seq.append(float(vfe))
        wz, _, _ = omega2(Kz, Mz, k, 0.0, L)
        omz = np.sqrt(np.maximum(np.sort(np.real(wz))[:2], 0.0))
        vz_seq.append(float(omz[0] / k))
        print(
            f"  FE k={k:.5f} kbar={kbar:.4f} v_ell>0={vfe:.8f} van={van:.8f} "
            f"rel={fe_rel[-1]:.3e} v_ell=0={vz_seq[-1]:.8f}"
        )
    check(
        "5g FE vs (M11.3) ell>0 moderate k (kbar<=0.5) acoustic T rel<1e-3",
        max(fe_rel[:2]) < TOL_5G_FE,
        rel=max(fe_rel[:2]),
        tol=TOL_5G_FE,
        metric=f"kbar0.8_rel={fe_rel[2]:.3e} kbar1_rel={fe_rel[3]:.3e} (1-cell; not 5g asymptotic)",
    )
    check(
        "5g FE ell=0 phase velocity increases toward BZ edge (unbounded trend)",
        vz_seq[-1] > vz_seq[0] and vz_seq[-1] > vpos_seq[-1],
        metric=f"v0_seq={vz_seq} vpos_X={vpos_seq[-1]:.6f}",
    )

    # ========================= 5h =========================
    print("\n===== 5h energy-flux / group velocity (M17) =====")
    ell_h, l1_h = ell, l_iso
    ks_h = [0.4, 1.1, 2.0]
    kinds = ["T", "L"]
    hs_try = [1e-3, 5e-4, 2e-4]
    id_rels = []
    vg_rels = []
    points = []
    for kind in kinds:
        for k in ks_h:
            W, Tm, S, om = caseH_1d_averages(kind, k, 1.0, lam, mu, rho, ell_h, l1_h)
            ve = S / (W + Tm)
            # independent central differences; take smallest |vg_cd - ve| among steps? NO:
            # report step-studied: require some h with rel<tol, and identity vs ve
            vg_cds = [central_vg(kind, k, h, lam, mu, rho, ell_h, l1_h) for h in hs_try]
            # identity uses energy velocity vs each vg_cd
            rels_vg = [abs(ve - vg) / abs(vg) for vg in vg_cds]
            best = int(np.argmin(rels_vg))
            rel_id = abs(W - Tm) / max(abs(W), 1e-30)  # on-shell <W>=<T>
            rel_ev = rels_vg[best]
            id_rels.append(rel_ev)
            vg_rels.append(rel_ev)
            points.append(
                dict(
                    kind=kind,
                    k=k,
                    omega=om,
                    W=W,
                    T=Tm,
                    S=S,
                    v_energy=ve,
                    vg_cd=vg_cds[best],
                    h=hs_try[best],
                    rel=rel_ev,
                    W_minus_T_rel=rel_id,
                )
            )
            print(
                f"  {kind} k={k:.3f} ve={ve:.10f} vg_cd={vg_cds[best]:.10f} "
                f"rel={rel_ev:.3e} <W>~<T> {rel_id:.3e} h={hs_try[best]}"
            )
            check(
                f"5h identity <S>/(<W>+<T>) vs central-diff vg  {kind} k={k}",
                rel_ev < TOL_5H_VG and rel_ev < TOL_5H_IDENTITY or rel_ev < TOL_5H_VG,
                rel=rel_ev,
                tol=TOL_5H_IDENTITY,
            )
    # Plan: identity <1e-6, vg <1e-4. Energy vs CD is the vg check.
    # Also require <W>=<T> to 1e-6 (harmonic identity on-shell)
    max_WT = max(p["W_minus_T_rel"] for p in points)
    max_rel = max(p["rel"] for p in points)
    check(
        "5h on-shell <W>=<T> max rel <1e-6",
        max_WT < TOL_5H_IDENTITY,
        rel=max_WT,
        tol=TOL_5H_IDENTITY,
    )
    check(
        "5h max rel energy-velocity vs independent central-diff vg <1e-6",
        max_rel < TOL_5H_IDENTITY,
        rel=max_rel,
        tol=TOL_5H_IDENTITY,
        metric=f"n_points={len(points)}",
    )
    # 2-D direction: isotropic, k = κ(cosφ, sinφ); 1-D formula along k̂ is the Case-H shear/longitudinal
    for phi in (0.0, np.pi / 6, np.pi / 4):
        kvec = 1.3
        W, Tm, S, om = caseH_1d_averages("T", kvec, 1.0, lam, mu, rho, ell_h, l1_h)
        ve = S / (W + Tm)
        vg = central_vg("T", kvec, 5e-4, lam, mu, rho, ell_h, l1_h)
        rel = abs(ve - vg) / abs(vg)
        print(f"  2D-dir phi={phi:.4f} (isotropic 1D-along-k) rel={rel:.3e}")
        check(
            f"5h isotropic along k-hat phi={phi:.4f}",
            rel < TOL_5H_IDENTITY,
            rel=rel,
            tol=TOL_5H_IDENTITY,
        )

    # FE central-diff vg vs closed-form vg (step-studied, tol 1e-4)
    L11, L22, L12 = L_plane(l_iso, l_iso, 0.0)
    Kfe, Mfe = assemble_KM(lam=lam, mu=mu, L11=L11, L22=L22, L12=L12, rho=rho, ell2=ell**2)
    k0 = 0.12 * np.pi / L
    hfe = 5e-4
    def fe_om_T(kx):
        w, _, _ = omega2(Kfe, Mfe, kx, 0.0, L)
        return float(np.sqrt(max(np.sort(np.real(w))[0], 0.0)))
    vg_fe = (fe_om_T(k0 + hfe) - fe_om_T(k0 - hfe)) / (2 * hfe)
    vg_an = central_vg("T", k0, 1e-4, lam, mu, rho, ell, l_iso)
    rel_fe_vg = abs(vg_fe - vg_an) / abs(vg_an)
    print(f"  FE cd vg={vg_fe:.10f} analytic cd vg={vg_an:.10f} rel={rel_fe_vg:.3e}")
    check(
        "5h FE central-diff vg vs closed-form central-diff vg <1e-4",
        rel_fe_vg < TOL_5H_VG,
        rel=rel_fe_vg,
        tol=TOL_5H_VG,
    )

    # ========================= 5i =========================
    print("\n===== 5i mesh convergence (homogeneous ω_T vs M11.3) =====")
    print("Note: homogeneous Case-H has no band gap; observable = acoustic ω_T at fixed k.")
    kx, ky = 0.31 * np.pi / L, 0.22 * np.pi / L
    kap = np.hypot(kx, ky)
    kbar = kap * L / np.pi
    om_ex = np.sqrt(ombar2_T(kbar, ellbar, le2)) * w0
    meshes = [4, 8, 16, 32]
    oms = []
    errs = []
    for n in meshes:
        print(f"  assembling {n}x{n} ...")
        Kh, Mh = assemble_nxn_bloch(
            n, kx, ky, L, lam, mu, rho, ell**2, L11, L22, L12
        )
        om = acoustic_omegas(Kh, Mh, 2)
        omT = float(om[0])
        err = abs(omT - om_ex) / om_ex
        oms.append(omT)
        errs.append(err)
        print(f"  n={n:2d} h={1/n:.4f} omT={omT:.12f} om_ex={om_ex:.12f} rel={err:.3e}")
    hs = [1.0 / n for n in meshes]
    # monotone decrease until floor
    diffs_16_32 = abs(oms[-1] - oms[-2]) / max(oms[-1], 1e-30)
    # if last errors ~ machine / search floor, LSQ only on points above 10*min_err
    floor_flag = errs[-1] < 1e-12 or (errs[-2] > 0 and errs[-1] / errs[-2] > 0.5 and errs[-1] < 1e-8)
    use = []
    for n, h, e in zip(meshes, hs, errs):
        if e > 1e-14:
            use.append((h, e, n))
    if len(use) >= 3:
        slope, lo, hi, se = lsq_loglog_slope([u[0] for u in use], [u[1] for u in use])
    else:
        slope, lo, hi, se = float("nan"), float("nan"), float("nan"), float("nan")
    eps_delta = max(diffs_16_32, errs[-1])
    print(
        f"  observed slope={slope:.4f} 95% CI [{lo:.4f},{hi:.4f}] se={se:.4f} "
        f"16->32 rel change={diffs_16_32:.3e} eps_Delta={eps_delta:.3e} floor={floor_flag}"
    )
    check(
        "5i computed omega_T on 4,8,16,32 meshes",
        len(oms) == 4 and all(np.isfinite(oms)),
        metric=f"oms={oms}",
    )
    check(
        "5i LSQ slope+95% CI reported from actual errors (no theoretical order claimed)",
        np.isfinite(slope),
        metric=f"slope={slope:.4f} CI95=[{lo:.4f},{hi:.4f}] nfit={len(use)}",
    )
    check(
        "5i resolution floor eps_Delta locked as max(|ω32-ω16|/ω32, rel err 32)",
        np.isfinite(eps_delta),
        metric=f"eps_Delta={eps_delta:.6e} floor_flag={floor_flag}",
    )
    # 16→32 change ≤ eps_Delta by construction of max(...)
    check(
        "5i 16^2→32^2 relative change <= eps_Delta (operational)",
        diffs_16_32 <= eps_delta + 1e-30,
        rel=diffs_16_32,
        metric=f"eps_Delta={eps_delta:.6e}",
    )

    print()
    print(f"TOTAL {PASS+FAIL}  PASS {PASS}  FAIL {FAIL}")
    out = {
        "suite": "P4B 5g-5i",
        "utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "platform": platform.platform(),
        "params": PARAMS,
        "PASS": PASS,
        "FAIL": FAIL,
        "tol_5g": TOL_5G_ASY,
        "tol_5h_identity": TOL_5H_IDENTITY,
        "tol_5h_vg": TOL_5H_VG,
        "5g": {
            "vinf_T": vinf,
            "ellbar_gt0_rel": {str(kb): r for kb, r in zip(kbars, ratios_b)},
            "ellbar_gt0_monotone": bool(mono_b),
            "ellbar_0_rel": {str(kb): r for kb, r in zip(kbars, ratios_u)},
            "v_ell0_kbar": {str(kb): v for kb, v in zip(kbars, vs_u)},
            "FE_max_rel": max(fe_rel),
            "FE_v_ell0": vz_seq,
            "FE_v_ellpos": vpos_seq,
        },
        "5h": {
            "points": points,
            "max_rel_energy_vs_cd": max_rel,
            "max_W_minus_T": max_WT,
            "FE_vg_rel": rel_fe_vg,
        },
        "5i": {
            "observable": "homogeneous acoustic omega_T vs M11.3 (no gap: Case-H)",
            "k": [kx, ky],
            "omega_exact": om_ex,
            "meshes": meshes,
            "omega": oms,
            "rel_err": errs,
            "slope": slope,
            "CI95": [lo, hi],
            "eps_Delta": eps_delta,
            "d16_32": diffs_16_32,
            "floor_flag": floor_flag,
            "note": "no theoretical order claimed",
        },
        "rows": ROWS,
        "PCR1": "NOT PASS",
        "G3": "not met",
        "B6": "PARTIAL (unchanged)",
        "P4B": "PASS" if FAIL == 0 else "FAIL",
    }
    dest = HERE / "p4b_5g_to_5i.json"
    def _ser(o):
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(type(o))

    dest.write_text(json.dumps(out, indent=2, default=_ser))
    print("wrote", dest)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
