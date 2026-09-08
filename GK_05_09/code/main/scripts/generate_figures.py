"""Generate all seven figures required by sec:program. Each figure writes a CSV
of its plotted data alongside the PDF, and a metadata JSON."""
from __future__ import annotations
import sys, json, warnings
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.model import Theta, Geometry
from src.forward import forward
from src.fd_solver import solve_fd
from src.split_solver import solve_split
from src.limits import T_series
from src.statistics import fisher
from src.analysis import make_grid, profile
from src.calibration import CASES, FITTING_DOMAIN
from src.validation import load_digitised, ANCHOR_CASES, metrics
from src.laplace import t_star
from src.io import save_csv, save_json, FIGS

CFG = json.loads((ROOT / "config" / "default_parameters.json").read_text())
cfg = dict(CFG["reference_configuration"]); cfg.update(CFG["statistics"])
GEOM = Geometry(cfg["L"], cfg["t_p"])
plt.rcParams.update({"font.size": 9, "figure.dpi": 160, "savefig.bbox": "tight"})
META = {}


def _fin(name, fig, csv_rows, header, desc):
    fig.savefig(FIGS / f"{name}.pdf"); plt.close(fig)
    save_csv(FIGS / f"{name}.csv", csv_rows, header)
    META[name] = desc
    print(f"  {name}.pdf + {name}.csv")


# F1 degeneracy -------------------------------------------------------------
# Three panels. Panels (a),(b) show the curves; panel (c) shows the SPREAD,
# which is the quantity the test actually measures. Without (c) the figure is
# uninformative: on a 0-1 axis a 1e-11 and a 2.6e-2 spread both look like a
# single line, hiding the ~9 orders of magnitude that separate them.
t = np.linspace(0.005, 1.0, 400)
TQS = (3e-3, 3e-2, 3e-1)
ray_curves, ctl_curves = [], []
fig, ax = plt.subplots(1, 3, figsize=(9.6, 2.9))
rows = []
for q, st in zip(TQS, ("-", "--", ":")):
    y1 = forward(Theta(1.0, q, 1.00 * q), t, GEOM)
    y2 = forward(Theta(1.0, q, 1.05 * q), t, GEOM)
    ray_curves.append(y1); ctl_curves.append(y2)
    ax[0].plot(t, y1, st, lw=1.4, label=rf"$\tau_q={q:g}$")
    ax[1].plot(t, y2, st, lw=1.4, label=rf"$\tau_q={q:g}$")
    rows += [[q, ti, a, b] for ti, a, b in zip(t, y1, y2)]
ray = np.array(ray_curves); ctl = np.array(ctl_curves)
spread_ray = ray.max(0) - ray.min(0)
spread_ctl = ctl.max(0) - ctl.min(0)
ax[0].set_title(r"(a) resonance ray $B=1$, $\kappa^2=\alpha\tau_q$", fontsize=9)
ax[1].set_title(r"(b) control $B=1.05$", fontsize=9)
for a in ax[:2]:
    a.set_xlabel(r"dimensionless time $\hat t$"); a.grid(alpha=.3); a.legend(fontsize=7)
ax[0].set_ylabel(r"$\hat T(1,\hat t)$")
ax[2].semilogy(t, np.maximum(spread_ray, 1e-18), lw=1.5, color="tab:blue",
               label=rf"$B=1$: max {spread_ray.max():.1e}")
ax[2].semilogy(t, np.maximum(spread_ctl, 1e-18), lw=1.5, color="tab:red",
               label=rf"$B=1.05$: max {spread_ctl.max():.1e}")
ax[2].set_xlabel(r"dimensionless time $\hat t$")
ax[2].set_ylabel(r"spread over $\tau_q$ (max$-$min)")
ax[2].set_title(rf"(c) spread: ratio ${spread_ctl.max()/spread_ray.max():.1e}$", fontsize=9)
ax[2].legend(fontsize=7); ax[2].grid(alpha=.3, which="both")
fig.tight_layout()
rows += [["spread", ti, a, b] for ti, a, b in zip(t, spread_ray, spread_ctl)]
_fin("F1_degeneracy", fig, rows, ["tau_q_or_tag", "t_hat", "T_B1_or_spread_B1",
                                  "T_B1.05_or_spread_B1.05"],
     "eq:S-ray/eq:S-ctl degeneracy on the ray vs control, with spread panel")

# F2 anchor reproduction ----------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(7.4, 5.0),
                         gridspec_kw={"height_ratios": [2.2, 1]})
rows = []
for j, (nm, ttl) in enumerate((("fig3", "Anchor Fig. 3 (resonance)"),
                               ("fig5", "Anchor Fig. 5 (over-diffusive)"))):
    p = ANCHOR_CASES[nm]
    x, y, sd = load_digitised(nm)
    k = x <= p["tmax"]; x, y = x[k], y[k]
    ours = forward(Theta(1.0, p["tau_q"], p["kappa2"]), x, GEOM)
    m = metrics(y, ours, sd); r = ours - y
    axes[0, j].plot(x, y, "o", ms=1.6, color="0.45", label="published (digitised)")
    axes[0, j].plot(x, ours, "-", lw=1.4, color="tab:red", label="this program")
    axes[0, j].set_title(f"{ttl}\nNRMSE = {m['nrmse_pct']:.3f}%", fontsize=8.5)
    axes[0, j].legend(fontsize=7); axes[0, j].grid(alpha=.3)
    axes[1, j].plot(x, r, lw=.8, color="tab:blue")
    axes[1, j].axhspan(-2*sd, 2*sd, color="tab:green", alpha=.18, label=r"$\pm2\sigma_d$")
    axes[1, j].axhline(0, color="k", lw=.6); axes[1, j].legend(fontsize=7)
    axes[1, j].set_xlabel(r"$\hat t$"); axes[1, j].grid(alpha=.3)
    rows += [[nm, a, b, c] for a, b, c in zip(x, y, ours)]
axes[0, 0].set_ylabel(r"$\hat T(1,\hat t)$"); axes[1, 0].set_ylabel("residual")
fig.suptitle("REPRODUCTION / VALIDATION of published results - not an original result",
             fontsize=8.5, y=1.005)
fig.tight_layout()
_fin("F2_anchor_reproduction", fig, rows, ["figure", "t_hat", "T_published", "T_program"],
     "calc:repro external validation of the forward operator")

# F3 Talbot pole collision --------------------------------------------------
# The grid MUST contain t* exactly, and points either side of it, or the
# collision is invisible: the failure is confined to the single node that
# lands on the pole (eq:tstar).
TS40, TS41 = t_star(40, 0.04), t_star(41, 0.04)
tt = np.unique(np.concatenate([
    np.linspace(0.05, 0.6, 120),
    [TS40 * 0.99, TS40, TS40 * 1.01, TS41 * 0.99, TS41, TS41 * 1.01]]))
ref = solve_fd(tt, 0.02, 0.02, 0.04, Nx=800, rtol=1e-12, atol=1e-14)
fig, ax = plt.subplots(figsize=(4.8, 3.1))
rows = []
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    for M, c in ((40, "tab:red"), (41, "tab:blue")):
        e = np.abs(solve_split(tt, 0.02, 0.02, 0.04, M=M) - ref) + 1e-18
        ax.semilogy(tt, e, color=c, lw=1.3,
                    label=f"$M={M}$ ({'even' if M % 2 == 0 else 'odd'}), split form")
        rows += [[M, a, b] for a, b in zip(tt, e)]
econv = np.abs(forward(Theta(1.0, 0.02, 0.02), tt, GEOM) - ref) + 1e-18
ax.semilogy(tt, econv, color="k", lw=1.2, ls="--", label="convolution, $M=41$")
rows += [["conv41", a, b] for a, b in zip(tt, econv)]
ax.axvline(t_star(40, 0.04), color="k", ls=":", lw=1,
           label=r"$t^\ast=M\tau_\Delta/10$")
ax.set_xlabel(r"$\hat t$"); ax.set_ylabel("absolute error")
ax.set_title("Talbot pole collision (eq:tstar)", fontsize=9)
ax.legend(fontsize=6.5); ax.grid(alpha=.3)
_fin("F3_talbot_pole", fig, rows, ["solver_M", "t_hat", "abs_error"],
     "eq:tstar even-M failure and the convolution remedy")

# F4 identifiability --------------------------------------------------------
Bs = np.array([0.10,0.30,0.50,0.70,0.90,0.98,1.02,1.10,1.28,1.50,2.00,2.41,3.00,5.00])
t80 = make_grid(cfg)
se_tq, se_al, se_B, cond = [], [], [], []
for B in Bs:
    r = fisher(Theta.from_B(cfg["alpha"], cfg["tau_q"], B), t80, GEOM, cfg["eta_noise"])
    se_tq.append(r["se_tau_q"]); se_al.append(r["se_alpha"])
    se_B.append(r["se_B"]); cond.append(r["cond"])
bands = json.loads((ROOT / "results" / "band_results.json").read_text())["data"] \
        if (ROOT / "results" / "band_results.json").exists() else {"20": [0.628, 1.804]}
lo, hi = bands["20"]
fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.9))
ax[0].semilogy(Bs, se_tq, "o-", ms=3.5, lw=1.3, label=r"$\tau_q$")
ax[0].semilogy(Bs, se_al, "s-", ms=3.5, lw=1.3, label=r"$\alpha$")
ax[0].semilogy(Bs, se_B, "^-", ms=3.5, lw=1.3, label=r"$B$")
ax[0].axvspan(lo, hi, color="tab:red", alpha=.13, label=r"$>20\%$ band")
ax[0].axhline(20, color="k", ls=":", lw=.8)
ax[0].set_xlabel(r"$B$"); ax[0].set_ylabel("Fisher s.e. [%]")
ax[0].legend(fontsize=7); ax[0].grid(alpha=.3)
ax[1].semilogy(Bs, cond, "o-", ms=3.5, lw=1.3, color="tab:purple")
ax[1].axvline(1.0, color="k", ls="--", lw=.9)
ax[1].set_xlabel(r"$B$"); ax[1].set_ylabel(r"cond$(\tilde F)$"); ax[1].grid(alpha=.3)
_fin("F4_identifiability", fig,
     [[b, a, c, d, e] for b, a, c, d, e in zip(Bs, se_tq, se_al, se_B, cond)],
     ["B", "se_tau_q_pct", "se_alpha_pct", "se_B_pct", "cond_F"],
     "calc:landscape Fisher diagnostics vs B")

# F5 profile likelihood -----------------------------------------------------
fig, ax = plt.subplots(figsize=(4.8, 3.1)); rows = []
for B, st in zip((0.5, 0.9, 1.0, 1.28, 5.0), ("-", "--", "-.", ":", "-")):
    p = profile(B, cfg, GEOM)
    ax.semilogx(p["grid"] / cfg["tau_q"], p["delta"], st, lw=1.4, label=f"$B={B}$")
    rows += [[B, g, d] for g, d in zip(p["grid"], p["delta"])]
ax.axhline(3.841, color="k", ls=":", lw=1)
ax.set_ylim(0, 25); ax.set_xlabel(r"$\tau_q/\tau_q^{\rm true}$")
ax.set_ylabel(r"$\Delta$SSE$/\sigma^2$"); ax.legend(fontsize=7, ncol=2); ax.grid(alpha=.3)
ax.set_title("Profile likelihood (eq:profile-stat)", fontsize=9)
_fin("F5_profile_likelihood", fig, rows, ["B", "tau_q", "delta_sse_over_sigma2"],
     "eq:profile-def/eq:profile-threshold")

# F6 BIC --------------------------------------------------------------------
bicf = ROOT / "results" / "bic_results.csv"
fig, ax = plt.subplots(figsize=(5.4, 3.1)); rows = []
if bicf.exists():
    import csv
    with bicf.open() as f:
        rd = list(csv.DictReader(f))
    Bl = [r["B"] for r in rd]
    models = ["dBIC_fourier", "dBIC_mcv", "dBIC_nyiri", "dBIC_gk"]
    lbl = ["Fourier", "MCV", "Nyiri", "GK"]
    xs = np.arange(len(Bl)); w = 0.2
    for j, (m, L) in enumerate(zip(models, lbl)):
        v = [min(float(r[m]), 400) for r in rd]
        ax.bar(xs + (j - 1.5) * w, v, w, label=L)
        rows += [[r["B"], L, r[m]] for r in rd]
    ax.set_xticks(xs); ax.set_xticklabels([f"$B={b}$" for b in Bl])
    ax.set_yscale("symlog", linthresh=1); ax.set_ylabel(r"$\Delta$BIC")
    ax.legend(fontsize=7, ncol=4); ax.grid(alpha=.3, axis="y")
    ax.set_title("Model selection (eq:bic)", fontsize=9)
_fin("F6_bic", fig, rows, ["B", "model", "delta_bic"], "calc:bic model selection")

# F7 calibrations in B space ------------------------------------------------
fig, ax = plt.subplots(figsize=(6.6, 3.9))
ax.axvspan(lo, hi, color="tab:red", alpha=.15, label=rf"$>20\%$ band [{lo:.3f}, {hi:.3f}]")
ax.axvspan(*FITTING_DOMAIN, color="tab:grey", alpha=.12,
           label=r"Fehér–Kovács domain $1\leq B<3$")
ax.axvline(1.0, color="k", ls="--", lw=1.2, label=r"$B=1$ resonance")
rows = []
for i, c in enumerate(CASES):
    B = c.B_used
    if c.dB_rel:
        ax.errorbar(B, i, xerr=B * c.dB_rel, fmt="o", ms=6, capsize=3, color="tab:purple")
    else:
        ax.plot(B, i, "o", ms=6, color="tab:blue")
    rows.append([c.idx, c.specimen, B, c.in_band(lo, hi), c.dB_rel or ""])
ax.set_yticks(range(len(CASES)))
ax.set_yticklabels([f"{c.idx}. {c.specimen}" for c in CASES], fontsize=7)
ax.set_xlabel(r"$B=\kappa^2/(\alpha\tau_q)$"); ax.set_xlim(0.5, 3.4)
ax.legend(fontsize=6.5, loc="lower right"); ax.grid(alpha=.3, axis="x")
ax.set_title("Published calibrations in $B$-space", fontsize=9)
_fin("F7_calibrations", fig, rows, ["case", "specimen", "B", "in_band", "dB_rel"],
     "sec:calibrations twelve audited cases")

save_json(FIGS / "figure_metadata.json", META)
print(f"\n{len(META)} figures written to {FIGS}")
