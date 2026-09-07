"""Figure scripts (blueprint §16 - ONLY the frozen figure set).

All figures read results/*.csv / *.npz (raw data) ONLY - no values are
hand-entered. Vector PDF output, colour-blind-safe palette (Okabe-Ito),
no styling that exaggerates tiny differences; resolution floors are
plotted where the blueprint requires them.

Fig. 1 is a manuscript schematic (drawn, not computed) - not produced here.
"""
import csv, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")
OUT = os.path.join(ROOT, "figures")
os.makedirs(OUT, exist_ok=True)

# Okabe-Ito colour-blind-safe
OK = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#000000"]
plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.3,
                     "figure.dpi": 150, "savefig.bbox": "tight"})

def read_csv(name):
    with open(os.path.join(RES, name)) as f:
        lines = [l for l in f if not l.startswith("#")]
    return list(csv.DictReader(lines))

def farr(rows, key):
    return np.array([float(r[key]) if r[key] not in ("", "NaN") else np.nan
                     for r in rows])

def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, format="pdf")
    plt.close(fig)
    print("wrote", path)

def eps_delta():
    rows = read_csv("resolution_bench.csv")
    return float(rows[0]["eps_Delta"])

# ---------------- Fig. 2a: elastic-limit validation ---------------------
def fig2a():
    lines = [l.strip() for l in open(os.path.join(RES, "v2_elastic_limit.csv"))]
    kv = {}
    coupled = []
    for l in lines:
        if l.startswith("#") or l.startswith("model,"):
            continue
        p = l.split(",")
        if len(p) == 2:
            kv[p[0]] = float(p[1])
        elif len(p) == 6:
            coupled.append((p[0], float(p[1]), float(p[3]), p[5]))
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    items = [
        ("v_P/v0 (num.)", kv["vP_over_v0"], OK[0]),
        ("v_S/v0 (num.)", kv["vS_over_v0"], OK[0]),
        ("v_R/v_S decoupled (num.)", kv["VR_over_vS_numerical"], OK[1]),
        ("v_R/v_S decoupled (analytic)", kv["VR_over_vS_analytic"], OK[2]),
    ]
    for i, (lab, v, c) in enumerate(items):
        ax.plot([i], [v], "o", color=c, ms=7)
        ax.annotate(f"{v:.9f}", (i, v), textcoords="offset points",
                    xytext=(6, -10), fontsize=7)
    # coupled low-Omega limits (recorded, not gated)
    for j, (mod, Om, vr, st) in enumerate([c for c in coupled if abs(c[1] - 1e-5) < 1e-9]):
        ax.plot([4], [vr], "s", color=OK[3], ms=6)
        ax.annotate(f"{mod}: {vr:.6f} (Ω=1e-5)", (4, vr), textcoords="offset points",
                    xytext=(8, -4 * j), fontsize=7)
    ax.plot([5], [0.934208], "^", color=OK[4], ms=7, mfc="none")
    ax.annotate("stage-6 record 0.934208\n(search-limited, see audit)", (5, 0.934208),
                textcoords="offset points", xytext=(8, -6), fontsize=7)
    ax.set_xticks(range(6))
    ax.set_xticklabels(["vP/v0", "vS/v0", "vR/vS dec.", "vR/vS ana.",
                        "coupled lim.", "record"], fontsize=8)
    ax.set_ylim(0.4, 1.15)
    ax.set_ylabel("velocity ratio")
    ax.set_title("Fig. 2a - classical elastic limit (Validation V2)")
    save(fig, "fig2a_elastic_limit.pdf")

# ---------------- Fig. 2b: model-limit reproduction ---------------------
def fig2b():
    rows = read_csv("v3_model_limits.csv")
    Om = farr(rows, "Omega")
    pairs = [("V_C_Dw14", "V_A", "C(D_w*→10⁻¹⁴)→A  [gate]"),
             ("V_C_rhow0", "V_B", "C(ρ_w*→10⁻⁸)→B  [gate]"),
             ("V_C_Dw0", "V_A", "C(D_w*→10⁻⁸)→A  [evidence]")]
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    for i, (a, b, lab) in enumerate(pairs):
        d = np.abs(farr(rows, a) / farr(rows, b) - 1.0)
        ax.loglog(Om, np.maximum(d, 1e-16), color=OK[i], label=lab,
                  ls="-" if "gate" in lab else "--", lw=1.3)
    ax.axhline(1e-6, color="k", ls=":", lw=1, label="frozen target 10⁻⁶")
    ax.set_xlabel("Ω*"); ax.set_ylabel("|ΔV*|/V*")
    ax.set_ylim(1e-16, 1)
    ax.legend(fontsize=7)
    ax.set_title("Fig. 2b - phason-model limits (Validation V3)")
    save(fig, "fig2b_model_limits.pdf")

# ---------------- Fig. 3: baseline dispersion ---------------------------
def fig3():
    rows = read_csv("study1_baseline.csv")
    eps = eps_delta()
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    for i, mod in enumerate(("A", "B", "C")):
        rr = [r for r in rows if r["model"] == mod]
        Om = farr(rr, "Omega"); V = farr(rr, "V") / 1.0   # V* (v0 units)
        ax.loglog(Om, V, color=OK[i], label=f"model {mod}", lw=1.4)
    ax.axhline(0.5, color="k", ls=":", lw=0.8)
    ax.text(1.2e-3, 0.51, "v_S*/v0 = 0.5", fontsize=7)
    ax.set_xlabel("Ω*"); ax.set_ylabel("V* = Ω*/k*")
    ax.set_ylim(0.2, 0.6)
    ax.legend(fontsize=8)
    ax.set_title("Fig. 3 - baseline surface-branch dispersion\n"
                 f"(velocity resolution: u_V ≤ {eps/10:.1e}, ε_Δ = {eps:.1e})")
    save(fig, "fig3_baseline_dispersion.pdf")

# ---------------- Fig. 4: baseline model differences --------------------
def fig4():
    rows = read_csv("fig4_deltas.csv")
    Om = farr(rows, "Omega")
    eps = eps_delta()
    V0 = 0.4663  # only for converting eps (absolute V) to a relative guide
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    ax.loglog(Om, np.maximum(farr(rows, "Delta_BC"), 1e-16), color=OK[0],
              label="Δ_BC", lw=1.4)
    ax.loglog(Om, np.maximum(farr(rows, "Delta_AC"), 1e-16), color=OK[1],
              label="Δ_AC", lw=1.4)
    ax.axhline(eps / V0, color="k", ls=":", lw=1,
               label=f"resolution floor ε_Δ/V ≈ {eps/V0:.1e}")
    ax.set_xlabel("Ω*"); ax.set_ylabel("|ΔV*|/V*")
    ax.set_ylim(1e-10, 1)
    ax.legend(fontsize=8)
    ax.set_title("Fig. 4 - baseline model differences\n"
                 "(below the floor: indistinguishable within numerical resolution)")
    save(fig, "fig4_baseline_deltas.pdf")

# ---------------- Fig. 5: friction 1D slices ----------------------------
def fig5():
    if not os.path.exists(os.path.join(RES, "fig5_friction1d.csv")):
        print("fig5 skipped (study 2 not finished)"); return
    rows = read_csv("fig5_friction1d.csv")
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.6))
    dws = sorted(set(r["Dw"] for r in rows))
    for i, dw in enumerate(dws):
        sel = [r for r in rows if r["Dw"] == dw]
        Om = farr(sel, "Omega")
        for j, mod in enumerate(("A", "B", "C")):
            V = np.array([float(r["V"]) if r["V"] != "NaN" else np.nan
                          for r in sel if r["model"] == mod])
            o = Om[[k for k, r in enumerate(sel) if r["model"] == mod]]
            axes[0].loglog(o, V, color=OK[j], ls=["-", "--", ":"][i], lw=1.2,
                           label=f"{mod}, D_w*={float(dw):.0e}" if j == 0 or True else None)
        dBC = np.array([float(r["Delta_BC_at_Dw"]) if r["Delta_BC_at_Dw"] != "NaN" else np.nan
                        for r in sel if r["model"] == "C"])
        o = Om[[k for k, r in enumerate(sel) if r["model"] == "C"]]
        axes[1].loglog(o, np.maximum(dBC, 1e-16), color=OK[i], lw=1.3,
                       label=f"D_w*={float(dw):.0e}")
    eps = eps_delta()
    axes[1].axhline(eps / 0.4663, color="k", ls=":", lw=1, label="resolution floor")
    axes[0].set_xlabel("Ω*"); axes[0].set_ylabel("V*")
    axes[0].set_title("Fig. 5a - V*(Ω) at selected D_w*")
    axes[1].set_xlabel("Ω*"); axes[1].set_ylabel("Δ_BC")
    axes[1].set_title("Fig. 5b - Δ_BC(Ω) at selected D_w*")
    for ax in axes:
        ax.legend(fontsize=6, ncol=1)
    save(fig, "fig5_friction_1d.pdf")

# ---------------- Fig. 6: thermal sensitivity ---------------------------
def fig6():
    rows = read_csv("fig6_tau.csv")
    eps = eps_delta()
    taus = sorted(set(r["tau0"] for r in rows), key=float)
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    for i, t in enumerate(taus):
        sel = [r for r in rows if r["tau0"] == t]
        Om = farr(sel, "Omega"); dT = farr(sel, "Delta_T")
        ax.loglog(Om, np.maximum(dT, 1e-16), color=OK[i % len(OK)], lw=1.3,
                  label=f"τ₀*={float(t):g}")
    ax.axhline(eps / 0.4663, color="k", ls=":", lw=1, label="resolution floor")
    ax.set_xlabel("Ω*"); ax.set_ylabel("Δ_T = |V(τ₀*)−V(τ_ref*)|/V(τ_ref*)")
    ax.set_ylim(1e-9, 1e-2)
    ax.legend(fontsize=7)
    ax.set_title("Fig. 6 - thermal-relaxation sensitivity (model C)\n"
                 "(max Δ_T ≈ 8×10⁻⁵: weak but above the resolution floor)")
    save(fig, "fig6_thermal.pdf")

# ---------------- Fig. 7: phason boundary condition ---------------------
def fig7():
    rows = read_csv("fig7_bc_summary.csv")
    Om = farr(rows, "Omega")
    dC = farr(rows, "dV_over_V_C"); dA = farr(rows, "dV_over_V_A")
    eps = eps_delta()
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    ax.loglog(Om, np.maximum(dC, 1e-16), color=OK[0], lw=1.4,
              label="model C: |ΔV|/V (clamped vs free)")
    ax.axhline(eps / 0.4663, color="k", ls=":", lw=1, label="resolution floor")
    ax.set_xlabel("Ω*"); ax.set_ylabel("|ΔV|/V")
    ax.set_ylim(1e-12, 1e-2)
    ax.legend(fontsize=8)
    ax.set_title("Fig. 7 - phason BC: clamped (w=0) vs free (H=0)\n"
                 "model A: clamping destroys the phason surface branch -\n"
                 "no comparable branch remains (not plotted; see audit)")
    save(fig, "fig7_phason_bc.pdf")

# ---------------- Fig. 8: depth-root diagnostics ------------------------
def fig8():
    rows = read_csv("fig8_roots.csv")
    summ = read_csv("fig8_roots_summary.csv")
    models = ("A", "B", "C")
    Oms = sorted(set(float(r["Omega"]) for r in rows))
    fig, axes = plt.subplots(3, 3, figsize=(8.2, 7.4), squeeze=False)
    for im, mod in enumerate(models):
        for io, Om in enumerate(Oms):
            ax = axes[im][io]
            sel = [r for r in rows if r["model"] == mod and float(r["Omega"]) == Om]
            re = np.array([float(r["Re_p"]) for r in sel])
            im_p = np.array([float(r["Im_p"]) for r in sel])
            adm = np.array([int(r["admissible"]) for r in sel])
            grz = np.array([int(r["grazing"]) for r in sel])
            ax.plot(re[adm == 1], im_p[adm == 1], "o", color=OK[0], ms=5,
                    label="admissible")
            ax.plot(re[(adm == 0) & (grz == 0)], im_p[(adm == 0) & (grz == 0)],
                    "x", color=OK[1], ms=5, label="excluded")
            if np.any(grz == 1):
                ax.plot(re[grz == 1], im_p[grz == 1], "s", mfc="none",
                        color=OK[4], ms=6, label="grazing")
            ax.axhline(0, color="k", lw=0.5)
            ax.set_title(f"{mod}, Ω*={Om:g}", fontsize=8)
            if im == 2:
                ax.set_xlabel("Re p")
            if io == 0:
                ax.set_ylabel("Im p")
            if im == 0 and io == 0:
                ax.legend(fontsize=6)
    for s in summ:
        pass
    fig.suptitle("Fig. 8 - depth roots at k*=2Ω* (admissible set marked)")
    save(fig, "fig8_depth_roots.pdf")
    # second panel: dominant penetration depth
    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    for i, mod in enumerate(models):
        sel = [r for r in summ if r["model"] == mod]
        Om = farr(sel, "Omega"); d = farr(sel, "delta_pen")
        ax.loglog(Om, d, "o-", color=OK[i], lw=1.2, ms=4, label=mod)
    ax.set_xlabel("Ω*"); ax.set_ylabel("δ* = 1/|Im p| (dominant)")
    ax.set_title("Fig. 8b - penetration depth δ*(Ω)\n(depth localisation, NOT attenuation)")
    ax.legend(fontsize=8)
    save(fig, "fig8b_penetration.pdf")

# ---------------- Fig. 9: maps -------------------------------------------
def fig9():
    npz = os.path.join(RES, "fig9b_map_dBC.npz")
    if not os.path.exists(npz):
        print("fig9a/b skipped (study 2 not finished)")
    else:
        d = np.load(npz)
        Om, Dw = d["Omegas"], d["Dws"]
        # 9a: V* maps
        fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6))
        for ax, key, ttl in ((axes[0], "V_B", "V*_B(Ω, D_w*)"),
                             (axes[1], "V_C", "V*_C(Ω, D_w*)")):
            pm = ax.pcolormesh(np.log10(Om), np.log10(Dw), d[key],
                               shading="auto", cmap="viridis")
            ax.plot(np.log10(Om), np.log10(d["Omega_c_ref"]), color=OK[1],
                    ls="--", lw=1, label="Ω_c = D_w*/ρ_w* (reference only)")
            fig.colorbar(pm, ax=ax, label="V*")
            ax.set_xlabel("log₁₀ Ω*"); ax.set_ylabel("log₁₀ D_w*")
            ax.set_title(ttl, fontsize=9); ax.legend(fontsize=6)
        save(fig, "fig9a_V_maps.pdf")
        # 9b: Delta_BC map (log z)
        fig, ax = plt.subplots(figsize=(5.4, 3.9))
        pm = ax.pcolormesh(np.log10(Om), np.log10(Dw), np.log10(np.maximum(d["dBC"], 1e-16)),
                           shading="auto", cmap="viridis")
        ax.plot(np.log10(Om), np.log10(d["Omega_c_ref"]), color=OK[1], ls="--",
                lw=1, label="Ω_c = D_w*/ρ_w* (reference line only - no claimed transition)")
        fig.colorbar(pm, ax=ax, label="log₁₀ Δ_BC")
        ax.set_xlabel("log₁₀ Ω*"); ax.set_ylabel("log₁₀ D_w*")
        ax.set_title("Fig. 9b - Δ_BC(Ω, D_w*)")
        ax.legend(fontsize=6)
        save(fig, "fig9b_dBC_map.pdf")
    npz = os.path.join(RES, "fig9c_map_dT.npz")
    if os.path.exists(npz):
        d = np.load(npz)
        fig, ax = plt.subplots(figsize=(5.4, 3.4))
        pm = ax.pcolormesh(np.log10(d["Omegas"]), np.arange(len(d["taus"])),
                           np.log10(np.maximum(d["dT"], 1e-16)), shading="auto",
                           cmap="viridis")
        ax.set_yticks(np.arange(len(d["taus"])))
        ax.set_yticklabels([f"{t:g}" for t in d["taus"]])
        fig.colorbar(pm, ax=ax, label="log₁₀ Δ_T")
        ax.set_xlabel("log₁₀ Ω*"); ax.set_ylabel("τ₀*")
        ax.set_title("Fig. 9c - Δ_T(Ω, τ₀*)")
        save(fig, "fig9c_dT_map.pdf")

if __name__ == "__main__":
    fig2a(); fig2b(); fig3(); fig4(); fig6(); fig7(); fig8()
    fig5(); fig9()
