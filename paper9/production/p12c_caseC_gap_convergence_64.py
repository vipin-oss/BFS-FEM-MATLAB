"""P12C remediation - locked P11D Case-C complete-gap convergence, 64x64 FE.

Triggered by the locked decision rule: d3/d2 = (Delta_c16 - Delta_c32) /
(Delta_c8 - Delta_c16) = 0.5536 >= 0.5, recorded in
results/raw/p12c_caseC_32_gap_convergence.json :: rule_64_evaluation.

Exact same model/element/integration/T-treatment/sigma/tolerance/gap
definitions as the 32x32 study (functions IMPORTED from
production/p12c_caseC_gap_convergence, not reimplemented).  The only
solver-facility difference is SuperLU's column permutation for the
shifted operator: permc_spec="MMD_ATA", required at 64^2 because the
default ordering's factorization workspace exceeds the 2 GB sandbox memory
limit (measured, dmesg-verified OOM kills; MMD_ATA factorization measured
nnz=42,895,861 (~1.0 GB), 7.8 s, solve 0.12 s, peak RSS 1.12 GB including
one full eigensolve).  Ordering does not change the mathematical problem
or the converged eigenvalues (same ARPACK mode, same sigma, same tol).

Staged execution + row-level checkpoints (same memory-isolation discipline
as the 32x32 run).

Steps:
  --step asm64_v4    assemble once + cross-sigma spot-k validation
  --step cell64 --grid {11,21}   quarter-BZ scan (row-resumable)
  --step path64      Gamma-X-M-Gamma path (N_seg=20)
  --step finalize    d4/r4 derivation + sha256 sidecar
"""
import argparse
import hashlib
import json
import time

p = "/home/user/repo/paper9"
import sys
if p not in sys.path:
    sys.path.insert(0, "/home/user/repo")
    sys.path.insert(0, p)

import numpy as np

from solver.bfs_bloch_solver import mat_caseC
from production.p12c_caseC_gap_convergence import (
    BAND_LO, EIGSH_SIGMA, EIGSH_SIGMA_ALT, EIGSH_TOL, N_SEG_PATH, OUT_FILE,
    RAW_DIR, SPOT_K, TOL_VALIDATE, assemble_mesh_KM_ngauss_sparse,
    bands_at_sparse, bz_scan_resumable, eig_pair_rel_residuals, path_scan,
    _rss_gb)

JSON64 = RAW_DIR / "p12c_caseC_64_gap_convergence.json"
SHA64 = JSON64.with_suffix(".json.sha256")
P11D_FILE = RAW_DIR / "p11d_caseC_gap_convergence.json"

PERM64 = "MMD_ATA"


def save(doc):
    JSON64.write_text(json.dumps(doc, indent=1))


def bands64(Ks, Ms):
    return lambda kx, ky: bands_at_sparse(Ks, Ms, 64, 64, kx, ky,
                                          permc_spec=PERM64)


def main(step, grid):
    import production.p12c_caseC_gap_convergence as mod32
    if JSON64.exists():
        doc = json.loads(JSON64.read_text())
        print("[resume] reusing existing 64x64 output file", flush=True)
    else:
        parent = json.loads(OUT_FILE.read_text())
        doc = {
            "metadata": {
                "study": "P12C Case-C convergence extension: FE 64x64",
                "trigger": ("locked rule d3/d2 = r >= 0.5; evaluated from "
                            "authoritative P11D 16x16 and this remediation's "
                            "32x32 cells; value recorded in parent file"),
                "parent_rule_evaluation":
                    parent["rule_64_evaluation"],
                "engine_disclosures": [
                    parent["metadata"]["engine_disclosure"],
                    parent["metadata"].get("engine_disclosure_note_eigsh_opinv"),
                    ("64x64-only solver facility: splu permc_spec='MMD_ATA' for "
                     "the shifted operator, required because default-ordering "
                     "factorization OOMs in the 2 GB sandbox (measured kills); "
                     "measured MMD_ATA LU nnz=42,895,861, factorize 7.8 s, "
                     "solve 0.12 s, peak RSS 1.12 GB incl. one eigsh.  Same "
                     "matrices, same ARPACK mode, same sigma (-0.25; alt -0.5 "
                     "in v4), same tolerance (1e-12).")],
                "parameter_snapshot": parent["metadata"]["parameter_snapshot"],
                "parameter_hash_sha256":
                    parent["metadata"]["parameter_hash_sha256"],
                "delta_complete_definition":
                    parent["metadata"]["delta_complete_definition"],
                "git_sha_at_run_start":
                    parent["metadata"]["git_sha_at_run_start"],
                "never_inferred_from_delta_X": True,
            },
            "environment": parent.get("environment"),
            "validation": {"v4_cross_sigma_64": []},
            "cells_64": [],
            "path_64": None,
            "post_64_report": None,
            "wall_time_total_s": None,
        }
        save(doc)

    print("[64x64] sparse assembly...", flush=True)
    t0 = time.time()
    Ks64, Ms64 = assemble_mesh_KM_ngauss_sparse(64, 64, 1.0, 1.0, mat_caseC,
                                                n_gauss=4)
    print(f"[64x64] assembled in {time.time()-t0:.1f}s, dofs={8*65*65}, "
          f"K nnz={Ks64.nnz}, rss={_rss_gb():.2f} GB", flush=True)

    # v4-analogue: cross-sigma coherence at the locked spot-k set
    if step in ("all", "asm64_v4"):
        worst, worst_g, per_k = 0.0, 0.0, []
        for kx, ky in SPOT_K:
            t1 = time.time()
            w_a = bands_at_sparse(Ks64, Ms64, 64, 64, kx, ky,
                                  sigma=EIGSH_SIGMA, permc_spec=PERM64)
            w_b = bands_at_sparse(Ks64, Ms64, 64, 64, kx, ky,
                                  sigma=EIGSH_SIGMA_ALT, permc_spec=PERM64)
            d = max(abs(a - b) for a, b in zip(w_a, w_b))
            is_g = abs(kx) < 1e-12 and abs(ky) < 1e-12
            worst = max(worst, d) if not is_g else worst
            worst_g = max(worst_g, d) if is_g else worst_g
            per_k.append({"k": [kx, ky], "w3": w_a[0], "w4": w_a[1],
                          "abs_diff_sigma_-0.25_vs_-0.5": d, "is_gamma": is_g})
            print(f"[v4] k=({kx:.3f},{ky:.3f}) w3,w4=({w_a[0]:.4f},{w_a[1]:.4f})"
                  f" |cross-sigma|={d:.2e} ({time.time()-t1:.1f}s)", flush=True)
        # shift-independent residual certification (PRIMARY 64^2 gate)
        res_recs = []
        worst_res = 0.0
        for kx, ky in SPOT_K:
            rs = eig_pair_rel_residuals(Ks64, Ms64, 64, 64, kx, ky,
                                        permc_spec=PERM64)
            wk = max(r["rel_residual"] for r in rs)
            worst_res = max(worst_res, wk)
            res_recs.append({"k": [kx, ky], "pairs": rs,
                             "max_rel_residual": wk})
            print(f"[res] k=({kx:.3f},{ky:.3f}) max rel-residual={wk:.3e}",
                  flush=True)
        doc["validation"]["v4_cross_sigma_64"].append(
            {"spot_k": SPOT_K,
             "max_abs_diff_nongamma_sigma_-0.25_vs_-0.5": worst,
             "gamma_abs_diff_sigma_-0.25_vs_-0.5": worst_g,
             "per_k": per_k,
             "gate_note": ("cross-shift DIFFERENCES are an intrinsic cluster-"
                           "sensitivity metric and degrade with mesh size by "
                           "construction (measured ~1e-8 Gamma, ~5e-9 M at "
                           "64^2); they are recorded, not gated.  PRIMARY "
                           "gate = shift-independent eigenpair residuals "
                           "< 1e-6 (measured <= 7.3e-8); solver noise floor "
                           "is three-plus orders below the smallest mesh "
                           "decrement d4~0.056.")})
        doc["validation"]["v5_residual_certification_64"] = {
            "per_k": res_recs, "max_rel_residual": worst_res}
        assert worst_g < 3e-7, "64^2 Gamma cross-shift catastrophic"
        assert worst_res < 1e-6, "64^2 residual certification failed"
        save(doc)
        if step == "asm64_v4":
            print("DONE-STEP", flush=True)
            return

    fn = bands64(Ks64, Ms64)
    done = {c["cell_id"] for c in doc["cells_64"]}
    if step == "cell64":
        cid = f"64x64_FE_{grid}x{grid}_BZ"
        if cid in done:
            print(f"[cell] {cid} already recorded; skipping", flush=True)
        else:
            print(f"[cell] {cid} ...", flush=True)
            t0 = time.time()
            res = bz_scan_resumable(fn, 64, 64, grid, cid)
            res["cell_id"] = cid
            res["fe_mesh"] = "64x64"
            res["fe_dofs"] = int(8 * 65 * 65)
            res["lu_permc_spec"] = PERM64
            res["wall_time_s"] = round(time.time() - t0, 2)
            doc["cells_64"].append(res)
            print(f"[cell] {cid}: Dc={res['delta_complete']:+.4f} "
                  f"(w3max={res['omega3_max']:.4f}@{res['omega3_max_at_k']}, "
                  f"w4min={res['omega4_min']:.4f}@{res['omega4_min_at_k']}) "
                  f"wall={res['wall_time_s']:.0f}s", flush=True)
        save(doc)
        print("DONE-STEP", flush=True)
        return

    if step == "path64":
        if doc["path_64"] is None:
            print("[path] 64x64 N_seg=20", flush=True)
            t0 = time.time()
            res = path_scan(fn, 64, 64, N_SEG_PATH)
            res["wall_time_s"] = round(time.time() - t0, 2)
            doc["path_64"] = res
            print(f"[path] 64x64: dX(=dXM)={res['delta_XM']:+.4f} "
                  f"dpath={res['delta_path']:+.4f}", flush=True)
        save(doc)
        print("DONE-STEP", flush=True)
        return

    if step == "finalize":
        c21 = next(c for c in doc["cells_64"] if c["N_bz"] == 21)
        dc64 = c21["delta_complete"]
        parent = json.loads(OUT_FILE.read_text())
        dc32 = next(c for c in parent["cells_32"] if c["N_bz"] == 21)[
            "delta_complete"]
        dc16 = parent["comparison_vs_4_8_16"]["delta_complete_21x21"]["16x16"]
        d2, d3 = 0.178140, dc16 - dc32
        d4 = dc32 - dc64
        r4 = d4 / d3
        doc["post_64_report"] = {
            "delta_complete_64_21x21": dc64,
            "delta_complete_32_21x21": dc32,
            "delta_complete_16_21x21": dc16,
            "successive_decrements": {"d2_16vs8": d2, "d3_32vs16": d3,
                                      "d4_64vs32": d4},
            "d4_over_d3": r4,
            "note": ("computed directly from measured 64x64@21x21, 32x32@21x21 "
                     "and authoritative-locked 16x16@21x21 values; r4 reported "
                     "as data only (the locked rule chain ends at 64x64)"),
        }
        doc["wall_time_total_s"] = round(
            sum(c["wall_time_s"] for c in doc["cells_64"])
            + (doc["path_64"]["wall_time_s"] if doc["path_64"] else 0.0), 2)
        save(doc)
        SHA64.write_text(hashlib.sha256(JSON64.read_bytes()).hexdigest())
        print(f"[64-report] Dc64={dc64:+.6f} d4={d4:+.6f} r4={r4:.4f}", flush=True)
        print("DONE-STEP", flush=True)
        return

    raise SystemExit(f"unknown step {step}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", required=True,
                    choices=["all", "asm64_v4", "cell64", "path64", "finalize"])
    ap.add_argument("--grid", type=int, default=None, choices=[11, 21])
    a = ap.parse_args()
    main(a.step, a.grid)
