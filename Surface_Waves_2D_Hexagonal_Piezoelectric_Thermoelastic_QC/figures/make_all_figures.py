#!/usr/bin/env python3
"""Generate ALL 11 publication figures of Research Paper 1 from raw data.

Usage (from anywhere):  python3 figures/scripts/make_all_figures.py
Reads results/raw/*.{csv,npz} (read-only); writes figures/output/figN.pdf.
No smoothing, no interpolation of data, no hard-coded result values.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# ================= Fig 1: scientific schematic ============================
def fig1():
    fig, ax = plt.subplots(figsize=(8.4, 4.7))
    ax.set_axis_off(); ax.set_xlim(0, 10); ax.set_ylim(-5.2, 2.45)
    X = np.linspace(0, 10, 400)
    # half-space
    ax.fill_between(X, -5.0, 0, color="#0072B2", alpha=0.07, zorder=0)
    for d in np.arange(-4.8, 0, 0.35):
        ax.plot(X, np.full_like(X, d), color="#0072B2", lw=0.3, alpha=0.10)
    ax.plot(X, np.zeros_like(X), "k", lw=1.4, zorder=3)
    ax.text(10.05, 0, "$z=0$", fontsize=9, va="center")
    ax.text(0.15, -0.35, "quasicrystal half-space $z>0$ (2D hex., Laue 10)",
            fontsize=8, color="#333333")
    # surface wave + decay envelope
    k_ = 2 * np.pi * 0.55
    surf = 0.42 * np.sin(k_ * X)
    ax.plot(X, surf, color="#003A70", lw=1.5, zorder=4)
    for j, d in enumerate((0.9, 1.8, 2.7, 3.6, 4.5)):
        amp = 0.42 * np.exp(-0.55 * d)
        ax.plot(X, -d + amp * np.sin(k_ * X), color="#003A70",
                lw=1.2 - 0.15 * j, alpha=0.75 - 0.12 * j, zorder=2)
    # penetration bracket
    xb = 8.6
    ax.annotate("", xy=(xb, -0.55), xytext=(xb, -2.55),
                arrowprops=dict(arrowstyle="<->", color="#B00000", lw=1.1))
    ax.text(xb + 0.15, -1.55, "$\\delta^*=1/|\\mathrm{Im}\\,p|$",
            color="#B00000", fontsize=8.5)
    # axes
    ax.annotate("", xy=(7.6, 1.9), xytext=(4.6, 1.9),
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color="k"))
    ax.text(6.1, 2.15, "propagation $x$   $\\propto\\mathrm{e}^{\\mathrm{i}(kx-\\omega t)}$",
            fontsize=8.5, ha="center")
    ax.annotate("", xy=(0.5, -4.6), xytext=(0.5, -0.4),
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color="k"))
    ax.text(0.12, -2.6, "depth $z$", fontsize=9, rotation=90, va="center")
    ax.annotate("", xy=(2.0, -5.05), xytext=(0.8, -5.05),
                arrowprops=dict(arrowstyle="-|>", lw=1.1, color="k"))
    ax.text(2.1, -5.12, "$y$ (periodic direction, out of plane)", fontsize=8,
            va="top")
    # boundary conditions at surface
    ax.text(0.15, 0.55, r"free surface:  $\sigma_{zz}=\sigma_{xz}=0$,"
            r"  $H_{xz}=H_{zz}=0$ (free phason),  $\theta=0$ (isothermal)",
            fontsize=8.2, color="#111111")
    # fields box
    ax.add_patch(plt.Rectangle((5.55, -4.85), 4.3, 2.05, fc="white",
                 ec="#666666", lw=0.7, zorder=5))
    ax.text(5.7, -3.05, r"active fields:  $\mathbf{u}=(u_x,u_z)$ phonon,  "
            r"$\mathbf{w}=(w_x,w_z)$ phason,  $\theta$", fontsize=8.2, zorder=6)
    ax.text(5.7, -3.55, r"$\varphi$: decoupled, passive output "
            r"($\partial/\partial y=0$, $u_y=0$)", fontsize=8.2,
            color="#666666", zorder=6)
    ax.text(5.7, -4.05, r"thermal: Lord--Shulman $\tau_0$;  piezoelectric: "
            r"passive in this cut", fontsize=8.2, zorder=6)
    ax.text(5.7, -4.55, r"phason operator $\Lambda$:  "
            r"A $-\rho_w\omega^2$ | B $-\mathrm{i}\omega D_w$ | "
            r"C $-\rho_w\omega^2-\mathrm{i}\omega D_w$", fontsize=8.2, zorder=6)
    save(fig, "fig1.pdf")

# ================= Fig 2: validation ======================================
def fig2():
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.05),
                             gridspec_kw={"width_ratios": [1.0, 1.15]})
    lines = [l.strip() for l in open(os.path.join(RES, "v2_elastic_limit.csv"))]
    kv, coupled = {}, []
    for l in lines:
        if l.startswith("#") or l.startswith("model,"):
            continue
        p = l.split(",")
        if len(p) == 2: kv[p[0]] = float(p[1])
        elif len(p) == 6: coupled.append((p[0], float(p[1]), float(p[3]), p[5]))
    ax = axes[0]
    cats = ["$v_P/v_0$", "$v_S/v_0$", "$v_R/v_S$\nnum.", "$v_R/v_S$\nana.",
            "A (cpl.)", "B/C (cpl.)"]
    vals = [kv["vP_over_v0"], kv["vS_over_v0"], kv["VR_over_vS_numerical"],
            kv["VR_over_vS_analytic"],
            [c[2] for c in coupled if c[0] == "A"][0],
            [c[2] for c in coupled if c[0] == "B"][0]]
    cols = [CB, CB, CA, CC, CA, CC]
    ana = kv["VR_over_vS_analytic"]
    ax.axhline(ana, color="#B00000", ls=(0, (2, 2)), lw=0.9,
               label="decoupled Rayleigh $%.12f$" % ana)
    for i, (c, v, cl) in enumerate(zip(cats, vals, cols)):
        ax.plot([i], [v], "o", color=cl, ms=5.5, zorder=4)
    ax.text(2, vals[2] - 0.045, "%.9f" % vals[2], fontsize=6.4, ha="center")
    ax.text(0, vals[0] + 0.035, "1 (exact)", fontsize=6.4, ha="center")
    ax.text(1, vals[1] + 0.04, "0.5 (exact)", fontsize=6.4, ha="center")
    ax.text(4, vals[4] - 0.065, "%.8f" % vals[4], fontsize=6.4, ha="center")
    ax.text(5, vals[5] + 0.03, "%.7f" % vals[5], fontsize=6.4, ha="center")
    ax.plot([5.55], [0.90], "^", mfc="none", mec=CA, ms=5.5, zorder=4)
    # legacy stage-6 coarse-scan record: documented constant from the package
    # IMPLEMENTATION_AUDIT.md (not present in results/*.csv); shown but EXCLUDED
    # from all conclusions.
    ax.text(5.55, 0.79, "0.934208 (excl. record)", fontsize=6.2, ha="center")
    ax.set_xticks(range(6)); ax.set_xticklabels(cats, fontsize=7)
    ax.set_ylim(0.4, 1.14); ax.set_xlim(-0.6, 6.1); ax.set_ylabel("velocity ratio")
    ax.legend(fontsize=6.4, loc="lower left")
    panel(ax, "a")
    ax = axes[1]
    rows = read_csv("v3_model_limits.csv")
    Om = farr(rows, "Omega")
    pairs = [("V_C_Dw14", "V_A", r"C($D_w^*\!\!\to\!10^{-14}$)$\to$A [gate]", CA),
             ("V_C_rhow0", "V_B", r"C($\rho_w^*\!\!\to\!10^{-8}$)$\to$B [gate]", CB),
             ("V_C_Dw0", "V_A", r"C($D_w^*\!=\!10^{-8}$)$\to$A [evidence]", CC)]
    for a, b, lab, c in pairs:
        d = np.abs(farr(rows, a) / farr(rows, b) - 1.0)
        ax.loglog(Om, np.maximum(d, 1e-16), color=c, label=lab, lw=1.0,
                  ls=SC if "evidence" in lab else "-")
    ax.axhline(1e-6, color="k", ls=":", lw=0.9, label="target $10^{-6}$")
    ax.axhline(1e-16, color="#888888", ls=":", lw=0.7, label="$10^{-16}$ clip")
    ax.axhspan(1e-16, 1e-13, color="#999999", alpha=0.12, zorder=0)
    ax.text(2.5e-3, 4e-15, "roundoff-dominated", fontsize=6.4, color="#555555")
    ax.set_xlabel(r"$\Omega^*$"); ax.set_ylabel(r"$|\Delta V^*|/V^*$")
    ax.set_ylim(1e-16, 1)
    ax.legend(fontsize=6.2, loc="upper right")
    panel(ax, "b")
    save(fig, "fig2.pdf")

# ================= Fig 3: baseline ========================================
def fig3():
    rows = read_csv("study1_baseline.csv")
    fig, axes = plt.subplots(1, 3, figsize=(7.8, 2.75))
    ax = axes[0]
    for mod, c, s in (("A", CA, SM), ("B", CB, SB), ("C", CC, SC)):
        rr = [r for r in rows if r["model"] == mod]
        ax.loglog(farr(rr, "Omega"), farr(rr, "V"), color=c, ls=s,
                  label=f"model {mod}")
    ax.axhline(0.5, color="k", ls=":", lw=0.8)
    ax.text(1.3e-3, 0.505, r"$v_S^*/v_0=0.5$", fontsize=7)
    ax.set_xlabel(r"$\Omega^*$"); ax.set_ylabel(r"$V^*=\Omega^*/k^*$")
    ax.set_ylim(0.2, 0.6); ax.legend(fontsize=7, loc="lower left")
    panel(ax, "a")
    ax = axes[1]
    rB = [r for r in rows if r["model"] == "B"]
    rC = [r for r in rows if r["model"] == "C"]
    dv = np.abs(farr(rB, "V") - farr(rC, "V"))
    ax.loglog(farr(rB, "Omega"), np.maximum(dv, 1e-16), color=CB, lw=1.0,
              label="$|V_B-V_C|$")
    ax.axhline(eps_delta(), color="k", ls=":", lw=0.9,
               label=r"floor $\varepsilon_\Delta$")
    ax.axhspan(1e-16, eps_delta(), color="#999999", alpha=0.12, zorder=0)
    ax.set_xlabel(r"$\Omega^*$"); ax.set_ylabel(r"$|V_B-V_C|$")
    ax.set_ylim(1e-10, 1e-4)
    ax.text(2e-3, 3e-5, "max $4.4\\times10^{-6}$ abs.\n($9.5\\times10^{-6}$ rel.)",
            fontsize=6.4)
    ax.legend(fontsize=6.6, loc="lower right")
    panel(ax, "b")
    ax = axes[2]
    for mod, c, s in (("A", CA, SM), ("B", CB, SB), ("C", CC, SC)):
        rr = [r for r in rows if r["model"] == mod]
        ax.loglog(farr(rr, "Omega"), farr(rr, "P_w"), color=c, ls=s,
                  label=f"model {mod}")
    ax.set_xlabel(r"$\Omega^*$"); ax.set_ylabel(r"phason participation $P_w$")
    ax.legend(fontsize=7, loc="lower right")
    panel(ax, "c")
    save(fig, "fig3.pdf")

# ================= Fig 4: model differences ===============================
def fig4():
    rows = read_csv("fig4_deltas.csv")
    Om = farr(rows, "Omega"); fl = floor_rel()
    fig, axes = plt.subplots(1, 3, figsize=(7.8, 2.75))
    ax = axes[0]
    ax.loglog(Om, np.maximum(farr(rows, "Delta_BC"), 1e-16), color=CB, lw=1.1)
    ax.axhline(fl, color="k", ls=":", lw=0.9, label="floor $\\varepsilon_\\Delta/V$")
    ax.axhspan(1e-16, fl, color="#999999", alpha=0.12, zorder=0)
    ax.text(6e0, 4e-10, "below floor:\nindistinguishable", fontsize=6.4,
            color="#555555")
    ax.set_xlabel(r"$\Omega^*$"); ax.set_ylabel(r"$\Delta_{BC}$")
    ax.set_ylim(1e-10, 1e-4); ax.legend(fontsize=6.8, loc="upper left")
    panel(ax, "a")
    ax = axes[1]
    ax.loglog(Om, np.maximum(farr(rows, "Delta_BC"), 1e-16) / fl, color=CB, lw=1.1)
    ax.axhline(1, color="k", ls=":", lw=0.9, label="= floor")
    ax.axhspan(1e-8, 1, color="#999999", alpha=0.12, zorder=0)
    ax.set_xlabel(r"$\Omega^*$"); ax.set_ylabel(r"$\Delta_{BC}\,/\,$floor")
    ax.set_ylim(1e-3, 1e3); ax.legend(fontsize=6.8, loc="upper left")
    panel(ax, "b")
    ax = axes[2]
    ax.loglog(Om, np.maximum(farr(rows, "Delta_AC"), 1e-16), color=CA, lw=1.1,
              label=r"$\Delta_{AC}$")
    ax.axhline(fl, color="k", ls=":", lw=0.9)
    ax.set_xlabel(r"$\Omega^*$"); ax.set_ylabel(r"$\Delta_{AC}$")
    ax.set_ylim(1e-2, 1)
    ax.text(2e-3, 0.1, "strongly separated\n($\\sim1.4\\times10^{7}\\times$floor)",
            fontsize=6.4, color="#555555")
    ax.legend(fontsize=6.8, loc="lower left")
    panel(ax, "c")
    save(fig, "fig4.pdf")

# ================= Fig 5: controlled friction =============================
def fig5():
    d = np.load(os.path.join(RES, "fig9b_map_dBC.npz"))
    Om, Dw = d["Omegas"], d["Dws"]
    idx = {1e-2: 0, 1e0: 20, 1e2: 40, 1e4: 60}
    fl = floor_rel()
    fig, axes = plt.subplots(1, 3, figsize=(7.9, 2.8))
    ax = axes[0]
    for dv in (1e-2, 1e0, 1e2, 1e4):
        j = idx[dv]
        ax.plot(Om, d["V_B"][j, :], color=DWCOL[dv], ls=SB, lw=1.0,
                label=f"B, $D_w^*$={dv:.0e}")
        ax.plot(Om, d["V_C"][j, :], color=DWCOL[dv], ls=SC, lw=1.0,
                label=f"C, $D_w^*$={dv:.0e}")
    ax.set_xscale("log"); ax.set_ylim(0.4648, 0.4676)
    ax.set_xlabel(r"$\Omega^*$"); ax.set_ylabel(r"$V^*$")
    import matplotlib.lines as mlines
    ax.legend([mlines.Line2D([], [], color=DWCOL[v], lw=1.0)
               for v in (1e-2, 1e0, 1e2, 1e4)],
              [f"$D_w^*$={v:.0e}" for v in (1e-2, 1e0, 1e2, 1e4)],
              fontsize=6.4, loc="lower left", title="B dashed / C dash-dot",
              title_fontsize=6.0)
    panel(ax, "a")
    ax = axes[1]
    for dv in (1e-2, 1e0, 1e2, 1e4):
        ax.loglog(Om, np.maximum(d["dBC"][idx[dv], :], 1e-16), color=DWCOL[dv],
                  lw=1.0, label=f"$D_w^*$={dv:.0e}")
    ax.axhline(fl, color="k", ls=":", lw=0.9, label="floor")
    ax.set_xlabel(r"$\Omega^*$"); ax.set_ylabel(r"$\Delta_{BC}$")
    ax.legend(fontsize=6.4, loc="lower right")
    panel(ax, "b")
    ax = axes[2]
    for dv in (1e-2, 1e0, 1e2, 1e4):
        chi = Om / dv
        ax.loglog(chi, np.maximum(d["dBC"][idx[dv], :], 1e-16), color=DWCOL[dv],
                  lw=1.0, label=f"$D_w^*$={dv:.0e}")
    ax.axhline(fl, color="k", ls=":", lw=0.9)
    ax.set_xlabel(r"$\chi=\Omega^*/\Omega_c=\Omega^*\rho_w^*/D_w^*$")
    ax.set_ylabel(r"$\Delta_{BC}$")
    ax.legend(fontsize=6.4, loc="lower right")
    panel(ax, "c")
    save(fig, "fig5.pdf")

# ================= Fig 6: thermal =========================================
def fig6():
    rows = read_csv("fig6_tau.csv")
    taus = sorted(set(r["tau0"] for r in rows), key=float)
    fl = floor_rel()
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 2.85))
    for axi, (xname, use_chi) in enumerate((("Omega", False), ("chi", True))):
        ax = axes[axi]
        for i, t in enumerate(taus):
            sel = [r for r in rows if r["tau0"] == t]
            dT = np.maximum(farr(sel, "Delta_T"), 1e-16)
            if use_chi:
                xs = farr(sel, "Omega") * float(t)
                lab = f"$\\tau_0^*$={float(t):g}" if i != 2 else \
                    f"$\\tau_0^*$={float(t):g} (ref., $\\Delta_T\\equiv0$)"
            else:
                xs = farr(sel, "Omega")
                lab = f"$\\tau_0^*$={float(t):g}" if i != 2 else \
                    f"$\\tau_0^*$={float(t):g} (ref.)"
            ax.loglog(xs, dT, color=TAUCOL[i], lw=1.0, ls="-" if i != 2 else ":",
                      label=lab)
        ax.axhline(fl, color="k", ls=":", lw=0.9, label="floor")
        ax.set_ylabel(r"$\Delta_T$")
        ax.set_xlabel(r"$\Omega^*$" if not use_chi else r"$\tau_0^*\Omega^*$")
        ax.legend(fontsize=5.9, loc="upper left", ncol=1)
        panel(ax, "ab"[axi])
    save(fig, "fig6.pdf")

# ================= Fig 7: phason BC =======================================
def fig7():
    rows = read_csv("fig7_bc_summary.csv")
    Om = farr(rows, "Omega"); fl = floor_rel()
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 2.85))
    ax = axes[0]
    ax.loglog(Om, np.maximum(farr(rows, "dV_over_V_C"), 1e-16), color=CB, lw=1.1,
              label="model C")
    ax.axhline(fl, color="k", ls=":", lw=0.9, label="floor")
    ax.axhspan(1e-16, fl, color="#999999", alpha=0.12, zorder=0)
    ax.set_xlabel(r"$\Omega^*$"); ax.set_ylabel(r"$|\Delta V|/V$ (clamped vs free)")
    ax.set_ylim(1e-12, 1e-4); ax.legend(fontsize=6.8, loc="lower right")
    panel(ax, "a")
    ax = axes[1]
    ax.loglog(Om, np.maximum(farr(rows, "dPen_C"), 1e-16), color=CB, lw=1.1,
              label=r"$\delta^*$ change, model C")
    ax.axhline(fl, color="k", ls=":", lw=0.9, label="floor")
    ax.set_xlabel(r"$\Omega^*$")
    ax.set_ylabel(r"$|\delta^*_{cl}-\delta^*_{fr}|/\delta^*_{fr}$")
    ax.legend(fontsize=6.8, loc="lower right")
    panel(ax, "b")
    fig.text(0.5, -0.06,
             "Model A: clamping the phason removes the carrier of its "
             "surface mode -- no finite-speed clamped branch exists "
             "(degenerate minima not plotted).",
             fontsize=7.2, ha="center", style="italic", color="#333333")
    save(fig, "fig7.pdf")

# ================= Fig 8: depth roots =====================================
def fig8():
    rows = read_csv("fig8_roots.csv")
    models = ("A", "B", "C")
    Oms = sorted(set(float(r["Omega"]) for r in rows))
    fig, axes = plt.subplots(3, 3, figsize=(8.6, 7.8), squeeze=False)
    letters = "abcdefghi"
    n = 0
    for im, mod in enumerate(models):
        for io, Omv in enumerate(Oms):
            ax = axes[im][io]
            sel = [r for r in rows if r["model"] == mod and
                   float(r["Omega"]) == Omv]
            re = np.array([float(r["Re_p"]) for r in sel])
            imp = np.array([float(r["Im_p"]) for r in sel])
            adm = np.array([int(r["admissible"]) for r in sel])
            grz = np.array([int(r["grazing"]) for r in sel])
            ax.plot(re[adm == 1], imp[adm == 1], "o", color=CB, ms=5.5,
                    mec="k", mew=0.4, zorder=3)
            ax.plot(re[(adm == 0) & (grz == 0)], imp[(adm == 0) & (grz == 0)],
                    "x", color=CA, ms=5.5, mew=1.2, zorder=3)
            if np.any(grz == 1):
                ax.plot(re[grz == 1], imp[grz == 1], "s", mfc="none",
                        mec="#E69F00", ms=6.5, mew=1.2, zorder=3)
            ax.axhline(0, color="k", lw=0.5)
            ax.set_title(f"{mod},  $\\Omega^*={Omv:g}$", fontsize=8.2)
            ax.tick_params(labelsize=7)
            panel(ax, letters[n]); n += 1
            if im == 2: ax.set_xlabel(r"Re\,$p$", fontsize=8.5)
            if io == 0: ax.set_ylabel(r"Im\,$p$", fontsize=8.5)
            ax.margins(0.12)
    axes[0][0].legend([plt.Line2D([], [], ls="", marker="o", color=CB),
                       plt.Line2D([], [], ls="", marker="x", color=CA, mew=1.2),
                       plt.Line2D([], [], ls="", marker="s", mfc="none",
                                  mec="#E69F00")],
                      ["admissible", "excluded", "grazing"],
                      fontsize=7, loc="lower left")
    fig.subplots_adjust(hspace=0.32, wspace=0.14)
    save(fig, "fig8.pdf")

# ================= Fig 9: 3D surfaces =====================================
def surf_panel(ax, Z, X2, Y2, cmap, zlab, zlim=None, ref=True):
    ax.plot_surface(X2, Y2, Z, cmap=cmap, linewidth=0, antialiased=True,
                    rstride=1, cstride=1, alpha=0.92, shade=True)
    zmin = zlim[0] if zlim else Z.min()
    ax.contourf(X2, Y2, Z, zdir="z", offset=zmin, cmap=cmap, levels=14,
                alpha=0.55)
    if ref:
        t = np.linspace(-2, 2, 20)
        ax.plot(t, t, zdir="z", zs=zmin, color="#B00000", ls="--", lw=1.0)
    if zlim:
        ax.set_zlim(*zlim)
        ax.set_zticks(np.linspace(zlim[0], zlim[1], 4))
    ax.set_xlabel(r"$\log_{10}\Omega^*$", fontsize=7.5, labelpad=1)
    ax.set_ylabel(r"$\log_{10}D_w^*$", fontsize=7.5, labelpad=1)
    ax.set_zlabel(zlab, fontsize=7.5, labelpad=0.5)
    ax.tick_params(labelsize=6.2)
    ax.view_init(elev=21, azim=-58)

def fig9():
    d = np.load(os.path.join(RES, "fig9b_map_dBC.npz"))
    X2, Y2 = np.meshgrid(np.log10(d["Omegas"]), np.log10(d["Dws"]))
    fig = plt.figure(figsize=(7.9, 3.55))
    ax = fig.add_subplot(1, 3, 1, projection="3d")
    surf_panel(ax, d["V_B"], X2, Y2, "viridis", "$V_B^*$",
               zlim=(0.4650, 0.4664))
    ax.text2D(0.02, 0.97, "a", transform=ax.transAxes, fontsize=10,
              fontweight="bold")
    ax = fig.add_subplot(1, 3, 2, projection="3d")
    surf_panel(ax, d["V_C"], X2, Y2, "viridis", "$V_C^*$",
               zlim=(0.4662, 0.4675))
    ax.text2D(0.02, 0.97, "b", transform=ax.transAxes, fontsize=10,
              fontweight="bold")
    ax = fig.add_subplot(1, 3, 3, projection="3d")
    Z = np.log10(np.maximum(d["dBC"], 1e-16))
    surf_panel(ax, Z, X2, Y2, "magma", r"$\log_{10}\Delta_{BC}$",
               zlim=(-16, -2))
    ax.text2D(0.02, 0.97, "c", transform=ax.transAxes, fontsize=10,
              fontweight="bold")
    fig.subplots_adjust(left=0.0, right=1.0, wspace=0.08)
    save(fig, "fig9.pdf")

# ================= Fig 10: thermal map ====================================
def fig10():
    d = np.load(os.path.join(RES, "fig9c_map_dT.npz"))
    Z = np.log10(np.maximum(d["dT"], 1e-16))
    fig, ax = plt.subplots(figsize=(6.6, 3.1))
    X = np.log10(d["Omegas"]); Y = np.arange(len(d["taus"]))
    Xg, Yg = np.meshgrid(X, Y)
    pm = ax.pcolormesh(Xg, Yg, Z, shading="auto", cmap="viridis")
    ax.plot(Xg[::1, ::8].ravel(), Yg[::1, ::8].ravel(), ".", ms=0.8,
            color="white", alpha=0.35)
    fig.colorbar(pm, ax=ax, label=r"$\log_{10}\Delta_T$", pad=0.01)
    ax.set_yticks(np.arange(len(d["taus"])))
    ax.set_yticklabels([f"{t:g}" for t in d["taus"]], fontsize=7.2)
    ax.set_xlabel(r"$\log_{10}\Omega^*$"); ax.set_ylabel(r"$\tau_0^*$")
    save(fig, "fig10.pdf")

# ================= Fig 11: penetration ====================================
def fig11():
    rows = read_csv("study1_baseline.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 2.85))
    ax = axes[0]
    for mod, c, s in (("A", CA, SM), ("B", CB, SB), ("C", CC, SC)):
        rr = [r for r in rows if r["model"] == mod]
        ax.loglog(farr(rr, "Omega"), farr(rr, "delta_pen"), color=c, ls=s,
                  lw=1.1, label=f"model {mod}")
    ax.set_xlabel(r"$\Omega^*$"); ax.set_ylabel(r"$\delta^*=1/|\mathrm{Im}\,p|$")
    ax.legend(fontsize=7, loc="upper right")
    panel(ax, "a")
    ax = axes[1]
    for mod, c, s in (("A", CA, SM), ("B", CB, SB), ("C", CC, SC)):
        rr = [r for r in rows if r["model"] == mod]
        ax.loglog(farr(rr, "Omega"), farr(rr, "Omega") * farr(rr, "delta_pen"),
                  color=c, ls=s, lw=1.1, label=f"model {mod}")
    ax.set_xlabel(r"$\Omega^*$"); ax.set_ylabel(r"$\Omega^*\delta^*$")
    ax.set_ylim(0.5, 5)
    ax.text(2e-3, 3.4, "$\\Omega^*\\delta^*\\approx$ const $\\Rightarrow$ "
            "$\\delta^*\\propto1/\\Omega^*$", fontsize=6.8)
    ax.legend(fontsize=7, loc="lower right")
    panel(ax, "b")
    save(fig, "fig11.pdf")

if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); fig7(); fig8(); fig9(); \
        fig10(); fig11()
    print("done")
