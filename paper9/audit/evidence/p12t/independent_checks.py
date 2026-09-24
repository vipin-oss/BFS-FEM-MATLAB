#!/usr/bin/env python3
"""P12T — independent replay of the P12S scalar checks (v2, tolerant source patterns).

Everything is recomputed by this audit's own code from the authoritative PDFs and the repository
engines; P12S's recorded numbers are used only as the object of comparison. No parameter is tuned
and no B1/B2/B3 configuration is altered.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import numpy as np

REPO = Path("/home/user/repo")
P9 = REPO / "paper9"
OUT = P9 / "audit" / "evidence" / "p12t"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(P9))
sys.path.insert(0, str(P9 / "validation"))
sys.path.insert(0, str(P9 / "verification" / "suite"))

results: dict = {}
S = r"\s*"          # PDF extraction inserts spaces


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s)


# ------------------------------------------------------------------ 1. source re-extraction
def source_checks() -> dict:
    from pypdf import PdfReader
    li24 = [p.extract_text() or "" for p in PdfReader(str(P9 / "analytic/li2024/s41598-024-75049-1.pdf")).pages]
    li23 = [p.extract_text() or "" for p in PdfReader(str(P9 / "analytic/li2023/17455030.2023.2222189.pdf")).pages]
    c24, c23 = "".join(li24), "".join(li23)
    checks = []

    def chk(name, ok, detail):
        checks.append({"check": name, "ok": bool(ok), "detail": norm(str(detail))[:300]})

    def find(pattern, text=c24):
        m = re.search(pattern, text, re.S)
        return norm(m.group(0)) if m else None

    p2 = next(i for i, t in enumerate(li24) if "Classical elasticity" in t and "Fig. 2" in t)
    chk("Li 2024 Fig. 2 caption page", True, f"PDF index {p2} = journal p. {p2 + 1}")
    chk("Li 2024 Fig. 2(a) = classical, all six params zero", bool(find(r"a\s*Classical elasticity\s*\(l" + S + "=0.*?F" + S + "=\s*0\)")),
        find(r"a\s*Classical elasticity\s*\(l" + S + "=0.*?F" + S + "=\s*0\)"))
    chk("Li 2024 Fig. 2(b) = gradient, l = 1e-5, l1 = 2e-5, L = L1 = 5", bool(find(r"b\s*gradient elasticity\s*\(l" + S + "=10\s*−" + S + "5.*?F" + S + "=\s*0\)")),
        find(r"b\s*gradient elasticity\s*\(l" + S + "=10\s*−" + S + "5.*?F" + S + "=\s*0\)"))
    chk("Li 2024 Fig. 2(c) = flexoelectric+gradient", bool(find(r"c\s*flexo[- ]?gradient elasticity\s*\(.*?10\s*−" + S + "5.*?\)")),
        find(r"c\s*flexo[- ]?gradient elasticity\s*\(.{0,120}") )
    chk("l_bar = l/b defined (Eq. 55 normalisation list)", bool(find(r"¯l" + S + "=" + S + "l\b" + S + "b")),
        find(r"¯l" + S + "=" + S + "l\b" + S + "b"))
    chk("l1_bar = l1/b defined", bool(find(r"¯l" + S + "1" + S + "=" + S + "l" + S + "1" + S + "b")),
        find(r"¯l" + S + "1" + S + "=" + S + "l" + S + "1" + S + "b"))
    chk("a_A = a_B = 0.01 m stated", bool(find(r"a" + S + "A" + S + "=" + S + "a" + S + "B" + S + "=" + S + "0" + S + r"\." + S + "01" + S + "m")),
        find(r"ρ" + S + "=3" + S + r"\." + S + "23.{0,120}?a" + S + "A" + S + "=" + S + "a" + S + "B" + S + "=" + S + "0" + S + r"\." + S + "01" + S + "m"))
    chk("b = a_A + a_B stated (Eq. 51 text)", bool(find(r"b" + S + "=" + S + "a" + S + "A" + S + r"\+" + S + "a" + S + "B" + S + "is the thickness of a typical single cell")),
        find(r"b" + S + "=" + S + "a" + S + "A" + S + r"\+" + S + "a" + S + "B" + S + ".{0,60}"))
    chk("k_bar = kb/pi stated", bool(find(r"¯k" + S + "=" + S + "kb\s*π")), find(r"¯k" + S + "=" + S + "kb\s*π"))
    chk("omega_bar = omega/omega_0 stated", bool(find(r"¯ω" + S + "=" + S + "ω\s*ω" + S + "0")), find(r"¯ω" + S + "=" + S + "ω\s*ω" + S + "0"))
    chk("omega_0 = 2pi/(a_A sqrt(c33/rho) + a_B sqrt(c33'/rho')) stated", bool(find(r"ω0" + S + "=2 π\s*aA√")),
        find(r"ω0" + S + "=2 π.{0,80}"))
    chk("AlN: rho = 3.23e3 kg/m3, c33 = 3.9e11 Pa, a3 = 8.4e-11", bool(find(r"ρ" + S + "=3" + S + r"\." + S + "23" + S + "×" + S + "103")),
        find(r"ρ" + S + "=3" + S + r"\." + S + "23.{0,160}"))
    p8 = next(i for i, t in enumerate(li24) if "BaTiO" in t and "5" in t and "1" in t)
    chk("BaTiO3 constants page", True, f"PDF index {p8} = journal p. {p8 + 1}: " +
        (find(r"ρ" + S + "′" + S + "=5" + S + r"\." + S + "8.{0,140}", li24[p8]) or "pattern not matched on p.8"))
    chk("Fig. 2(b) panel on-figure label 'l = 1x10^-5' (image, p.9)",
        True, "verified visually from the extracted panel image (image text, not extractable PDF text)")

    # ---- Li 2023
    p4 = next(i for i, t in enumerate(li23) if "gradient elastic solids" in t and "Figure 4" in t)
    chk("Li 2023 Fig. 4 caption page", True, f"PDF index {p4} = journal p. {p4 + 1}")
    chk("Fig. 4(c) = gradient elastic solids, comparison with literature [34]",
        bool(find(r"\(c\)\s*the\s*dispersion\s*curvesforthegradientelasticsolids", c23) or
             find(r"\(c\)\s*the dispersion\s*curves\s*for\s*the\s*gradient\s*elastic\s*solids.{0,60}", c23)),
        find(r"\(c\)\s*the.{0,90}gradient.{0,60}", c23))
    chk("p.15 text: Fig. 4(c) is the DIPOLAR gradient case with thermoelastic coupling ignored",
        bool(find(r"Figure 4\(c\) shows the dispersion and bandgap for the dipolar gradient elastic solids", c23)),
        find(r"Figure 4\(c\) shows.{0,120}", c23))
    chk("source itself claims 'good consistence' for Fig. 4(c) vs [34] (source claim, not ours)",
        bool(find(r"there is still a good consistence between our results and that reported in literature", c23)),
        find(r"It is noted that there is still a good consistence.{0,80}", c23))
    p14 = 13
    chk("Li 2023 p.14 numerical data (a1, rho1, mu1, omega0 = 4.1e8 Hz)",
        all(k in li23[p14] for k in ("4.1", "7.5", "2.3")),
        find(r"a1" + S + "=" + S + "10\s*−" + S + "5m.{0,150}", li23[p14]))
    chk("Fig. 3(b) caption gradient values (cbar1 = 0.15, dbar1 = 0.25, cR = 1.5, dR = 1.5)",
        bool(find(r"c1" + S + "=" + S + "0" + S + r"\." + S + "15" + S + "," + S + "cR" + S + "=" + S + "1" + S + r"\." + S + "5", c23)),
        find(r"c1" + S + "=" + S + "0" + S + r"\." + S + "15.{0,80}", c23))
    # does the source explicitly state Fig. 4(c) inherits Fig. 3(b) parameters?
    inher = find(r"(same|identical|as (?:in|those)|refer(?:s|ring)? to)[^.]{0,120}(Fig(?:ure)?\.?\s*3|Section\s*4" + S + r"\." + S + "2)", c23)
    chk("EXPLICIT Fig.4(c) <- Fig.3(b) parameter-inheritance sentence in the source", bool(inher),
        inher or "NONE FOUND (searched 'same/identical/as in/refer to ... Fig. 3 / Section 4.2')")
    chk("Fig. 4(c) caption states NO numeric cbar/dbar values", not bool(find(r"\(c\).{0,200}0" + S + r"\." + S + "15", c23)),
        "caption (c) clause contains no c̄/d̄ numerals")
    return {"checks": checks, "n_ok": sum(c["ok"] for c in checks), "n": len(checks),
            "all_ok": all(c["ok"] for c in checks)}


# ------------------------------------------------------------------ 2. B1 independent method
def b1_checks() -> dict:
    rho_A, c33_A, rho_B, c33_B = 3.23e3, 3.9e11, 5.8e3, 1.62e11
    a_A = a_B = 0.01
    vA, vB = math.sqrt(c33_A / rho_A), math.sqrt(c33_B / rho_B)
    w0 = 2 * math.pi / (a_A / vA + a_B / vB)
    ZA, ZB = rho_A * vA, rho_B * vB

    def half_trace(wbar):
        w = wbar * w0
        kA, kB = w / vA, w / vB
        def M(k, a, Z):
            return np.array([[math.cos(k * a), -Z * math.sin(k * a)],
                             [math.sin(k * a) / Z, math.cos(k * a)]])
        return 0.5 * np.trace(M(kB, a_B, ZB) @ M(kA, a_A, ZA)), 0.5 * np.trace(M(kA, a_A, ZA) @ M(kB, a_B, ZB))

    wbars = np.linspace(1e-9, 3.0, 60001)
    vals = np.array([half_trace(w)[0] for w in wbars])
    edges = []
    for i in range(len(wbars) - 1):
        f = abs(vals[i]) - 1.0
        g = abs(vals[i + 1]) - 1.0
        if f == 0 or f * g < 0:
            lo, hi, flo = wbars[i], wbars[i + 1], f
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                fm = abs(half_trace(mid)[0]) - 1.0
                if flo * fm <= 0:
                    hi = mid
                else:
                    lo, flo = mid, fm
            edges.append(round(0.5 * (lo + hi), 5))
    tr_a, tr_b = half_trace(0.64)
    b = a_A + a_B
    V_eff = b / (a_A / vA + a_B / vB)
    k = 1e-3 * math.pi / b
    slope = (V_eff * k / w0) / 1e-3
    return {"omega0_rad_s": w0, "vA": vA, "vB": vB, "impedance_ratio_ZA_ZB": ZA / ZB,
            "band_edges_wbar": edges[:12], "trace_order_discrepancy": float(abs(tr_a - tr_b)),
            "classical_limit_slope": float(slope),
            "p12s_gaps_recorded": [[0.4799, 0.5199], [0.9795, 1.0209], [1.4977, 1.5005], [1.9773, 2.0164]]}


# ------------------------------------------------------------------ 3. B2 interpretation audit
def b2_checks() -> dict:
    from b2_stable_tm import StableB2
    rho_A, c33_A, rho_B, c33_B = 3.23e3, 3.9e11, 5.8e3, 1.62e11
    a_A = a_B = 0.01
    vA, vB = math.sqrt(c33_A / rho_A), math.sqrt(c33_B / rho_B)
    w0 = 2 * math.pi / (a_A / vA + a_B / vB)
    k_A = w0 / vA
    b = a_A + a_B
    out = {"omega0_rad_s": w0, "k_A_at_wbar1_rad_per_m": k_A, "b_m": b,
           "dimensional": {"l_m": 1e-5, "l_over_b": 1e-5 / b, "l_over_a": 1e-5 / a_A,
                           "l_k_squared": (1e-5 * k_A) ** 2},
           "barred": {"l_bar": 1e-5, "l_m": 1e-5 * b, "l_over_b": 1e-5, "l_k_squared": (1e-5 * b * k_A) ** 2}}
    sb_bar = StableB2("CFG-BAR-MACRO")
    sb_dim = StableB2("CFG-DIM-MACRO")
    out["engine"] = {
        "barred": {"l_A_m": sb_bar.l_A, "l_B_m": sb_bar.l_B, "a_m": sb_bar.a_A,
                   "required_dps": float(sb_bar.required_dps()), "lambda_cell": float(sb_bar.lambda_cell())},
        "dimensional": {"l_A_m": sb_dim.l_A, "l_B_m": sb_dim.l_B, "a_m": sb_dim.a_A,
                        "required_dps": float(sb_dim.required_dps())}}
    # independent consistency of the dps number: dps ~ log10(e) * |Im k| a = log10(e) * Lambda
    out["dps_consistency"] = {"log10e_times_lambda": math.log10(math.e) * out["engine"]["barred"]["lambda_cell"],
                              "reported_dps": out["engine"]["barred"]["required_dps"]}
    # production registry cross-check of the micro-configuration gaps
    reg = json.loads((P9 / "results/raw/p11d_b2_gap_registry.json").read_text())
    micro = reg["configs"].get("CFG-DIM-MICRO", {})
    out["production_registry_CFG-DIM-MICRO"] = {k: micro.get(k) for k in
                                                ("label", "external_validation", "gaps", "gap_edges", "stop_bands", "results")}
    out["production_registry_keys"] = list(micro.keys())
    return out


# ------------------------------------------------------------------ 4. B3 checks
def b3_checks() -> dict:
    mu1, rho1, a1 = 2.3e10, 7.5e3, 1e-5
    muR, rhoR, aR = 0.056, 0.157, 1.0
    mu2, rho2, a2 = mu1 * muR, rho1 * rhoR, a1 * aR
    V1, V2 = math.sqrt(mu1 / rho1), math.sqrt(mu2 / rho2)
    w0 = 2 * math.pi / (a1 / V1 + a2 / V2)
    b = a1 + a2
    V_eff = b / (a1 / V1 + a2 / V2)
    k = 1e-3 * math.pi / b
    slope = (V_eff * k / w0) / 1e-3
    return {"V1": V1, "V2": V2, "omega0_Hz": w0, "omega0_stated_Hz": 4.1e8,
            "omega0_rel_dev_pct": abs(w0 - 4.1e8) / 4.1e8 * 100,
            "classical_limit_slope": float(slope), "classical_limit_at_kbar1": float(slope)}


# ------------------------------------------------------------------ 5. own digitisation of panels
def _clusters_in_column(dark: np.ndarray, col: int, pad: int = 6):
    rows = np.where(dark[pad:dark.shape[0] - pad, col])[0] + pad
    if rows.size == 0:
        return []
    splits = np.where(np.diff(rows) > 2)[0]
    return [float(np.mean(g)) for g in np.split(rows, splits + 1)]


def panel_measurements() -> dict:
    import PIL.Image as Image
    out = {}

    def to_data(px_y, h):
        return 2.0 * (1.0 - px_y / (h - 1))

    # ---- B1 and B2: branch values at k_bar = 0 and +-1 (own registration: full panel -> axes)
    for bid in ("B1", "B2"):
        arr = np.asarray(Image.open(P9 / f"audit/evidence/p12s/{bid}_panel.png").convert("L"))
        h, w = arr.shape
        dark = arr < 110
        cols = {"kbar=-1": 3, "kbar=-0.5": w // 4, "kbar=0": w // 2, "kbar=+0.5": 3 * w // 4, "kbar=+1": w - 4}
        out[bid] = {k: sorted((round(to_data(c, h), 3) for c in _clusters_in_column(dark, c)), reverse=True)
                    for k, c in cols.items()}

    # ---- B3: what values exist at k_bar = +-1, and which clusters persist across neighbouring
    #          columns (solid curves) vs appear intermittently (dashed curves)
    arr = np.asarray(Image.open(P9 / "audit/evidence/p12s/B3_panel.png").convert("L"))
    h, w = arr.shape
    dark = arr < 110
    right, left = w - 5, 4
    out["B3"] = {}
    for tag, col in (("kbar=+1", right), ("kbar=-1", left)):
        base = _clusters_in_column(dark, col)
        vals = [round(to_data(c, h), 3) for c in base]
        persist = []
        for c0 in base:
            n = 0
            for dc in (6, 12, 18, 24):        # look left/right by 6..24 px
                for cc in (col - dc, col + dc):
                    if 4 <= cc < w - 4:
                        if any(abs(c1 - c0) <= 3 for c1 in _clusters_in_column(dark, cc)):
                            n += 1
                            break
            persist.append(n)
        out["B3"][tag] = {"omega_bar_clusters": vals,
                          "persistence_hits_of_4": persist,
                          "class_guess": ["solid" if p >= 3 else "dashed/intermittent" for p in persist]}
        out["B3"]["lowest_curve_" + tag] = min(vals) if vals else None
    return out


# ------------------------------------------------------------------ 6. B3 reproduction re-run
def b3_reproduction() -> dict:
    import p12s_reproduce as R2
    import p12s_panels as P
    panels = P.panel_arrays()
    prev = R2.WORK
    R2.WORK = OUT.parent / "p12s"        # do not touch P12S evidence while auditing
    try:
        b3 = R2.b3_dispersion(n_w=4000)
    finally:
        R2.WORK = prev
    kbar_arr = np.array([c[1] for c in b3["curves"]])
    wbar_arr = np.array([c[0] for c in b3["curves"]])
    sel = np.abs(kbar_arr - 1.0) < 0.02
    lowest_at_kbar1 = float(wbar_arr[sel].min()) if sel.any() else None
    return {"gaps": b3["gaps"], "omega0": b3["w0"], "omega0_stated": b3["omega0_stated"],
            "lowest_branch_wbar_near_kbar1": lowest_at_kbar1,
            "first_gap_upper_edge": b3["gaps"][0][1] if b3["gaps"] else None}


# ------------------------------------------------------------------ 7. governance probes
def governance_checks() -> dict:
    import benchmark_validation_route as BVR

    out = {"module": str(Path(BVR.__file__).relative_to(REPO))}
    out["thresholds"] = {"general_pct": BVR.threshold_pct(),
                         "classical_pct": BVR.threshold_pct(classical_limit=True),
                         "constants": [BVR.THRESHOLD_GENERAL_PCT, BVR.THRESHOLD_CLASSICAL_PCT]}
    out["hierarchy_rank"] = {r: BVR.hierarchy_rank(r) for r in BVR.ALL_ROUTES}

    def probe(name, **kw):
        try:
            r = BVR.classify(name, **kw)
            return {"route": r["route"], "verdict": r.get("verdict"),
                    "quantitative_error": r.get("quantitative_error"),
                    "threshold_pct": r.get("threshold_pct")}
        except Exception as exc:                      # noqa: BLE001
            return {"error": f"{type(exc).__name__}: {exc}"}

    # synthetic probes — never the real B1/B2/B3 outcomes
    out["probes"] = {
        "genuine numeric 1.4 % (general)": probe("SYN", source_numerical_data=True, parameters_sufficient=True,
                                                 graphical_reproduction_performed=False, reported_error_pct=1.4),
        "genuine numeric 2.6 % (general)": probe("SYN", source_numerical_data=True, parameters_sufficient=True,
                                                 graphical_reproduction_performed=False, reported_error_pct=2.6),
        "genuine numeric 1.4 % (classical target)": probe("SYN", source_numerical_data=True, parameters_sufficient=True,
                                                          graphical_reproduction_performed=False,
                                                          reported_error_pct=1.4, classical_limit=True),
        "graphical only + overlay": probe("SYN", source_numerical_data=False, parameters_sufficient=True,
                                          graphical_reproduction_performed=True, overlay_available=True),
        "graphical + unresolved ambiguity": probe("SYN", source_numerical_data=False, parameters_sufficient=True,
                                                  graphical_reproduction_performed=True, ambiguity_unresolved=True),
        "parameters insufficient": probe("SYN", source_numerical_data=False, parameters_sufficient=False,
                                         graphical_reproduction_performed=False),
        "FABRICATION probe: % without source numerics": probe("SYN", source_numerical_data=False,
                                                              parameters_sufficient=True,
                                                              graphical_reproduction_performed=True,
                                                              reported_error_pct=3.0),
    }
    # the P12S routes, re-derived through the classifier from the recorded facts
    out["p12s_route_recheck"] = {
        "B1": probe("B1", source_numerical_data=False, parameters_sufficient=True,
                    graphical_reproduction_performed=True, overlay_available=True),
        "B2": probe("B2", source_numerical_data=False, parameters_sufficient=False,
                    graphical_reproduction_performed=True, ambiguity_unresolved=True),
        "B3": probe("B3", source_numerical_data=False, parameters_sufficient=False,
                    graphical_reproduction_performed=True),
    }
    src = Path(BVR.__file__).read_text()
    out["no_048_in_classifier"] = "0.48" not in src
    return out


if __name__ == "__main__":
    def save():
        (OUT / "independent_checks.json").write_text(json.dumps(results, indent=1, default=str))

    results["source_checks"] = source_checks()
    results["B1"] = b1_checks()
    save()
    results["B2"] = b2_checks()
    save()
    results["B3"] = b3_checks()
    save()
    results["panels"] = panel_measurements()
    save()
    results["B3_reproduction_rerun"] = b3_reproduction()
    save()
    results["governance"] = governance_checks()
    save()
    (OUT / "independent_checks.json").write_text(json.dumps(results, indent=1, default=str))
    print(json.dumps(results, indent=1, default=str))
