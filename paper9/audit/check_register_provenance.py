#!/usr/bin/env python3
"""P12AA — traceability-register provenance checker.

Verifies that the *active* traceability register (``paper9/audit/traceability_matrix.{csv,json}``)
only points at artifacts that actually resolve, that every non-resolvable hash is explicitly labelled
as a historical record, that the CSV and the JSON agree, and that the register's version/provenance
claims match the authoritative records (`plan/blueprint/PROVENANCE.md`, the active machine record).

Anomaly classes (P12AA Part E):

* **A** ACTIVE ERROR        — an active reference that does not resolve and is not labelled historical
* **B** HISTORICAL/VALID    — an explicitly labelled historical citation (superseded snapshot, prior
                              revision, prior phase value) or a point-in-time register row
* **C** HARMLESS EQUIVALENT — vocabulary differences between CSV and JSON that carry the same governed
                              meaning (e.g. ``CLOSED`` vs ``LOCKED`` resolution words, both accepted by
                              the repository's own ``check_traceability.py`` predicate)
* **D** UNRESOLVED          — cannot be decided from repository evidence

Exit status: 0 when no ``A`` or ``D`` finding remains, 1 otherwise.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
AUDIT = REPO / "paper9" / "audit"
CSV = AUDIT / "traceability_matrix.csv"
TM_JSON = AUDIT / "traceability_matrix.json"
PROVENANCE = REPO / "paper9" / "plan" / "blueprint" / "PROVENANCE.md"
BP15 = REPO / "paper9" / "plan" / "blueprint" / "Paper9_Blueprint_v1.5.tex"
BP14 = REPO / "paper9" / "plan" / "blueprint" / "Paper9_Blueprint_v1.4.tex"
RECORD = AUDIT / "benchmark_validation_record.json"
GOVERNING_JSON = REPO / "paper9" / "verification" / "suite" / "p4b_5g_to_5i.json"

# Documented historical citations that are *expected* not to resolve to a current file. Each entry
# records what the token identified and why it is retained.
HISTORICAL_TOKENS = {
    "0089754b076f": "v1.4 blueprint as committed at P12H (commit dd42e81); superseded by the P12J C1 "
                    "clarification; retained as the historical P12H snapshot",
    "a45a5448a767": "P12H-recorded post-amendment plan hash; matches no reachable revision (P12AA-O2 "
                    "forensics); retained as the historical P12H bookkeeping record only",
    "0e2c3a3a0e47d435": "pre-amendment CALC_MASTER_PLAN.md (verified at commit fb9bd5d); historical",
}
# Resolution words that the repository's own checker treats alike (see check_traceability.py).
RESOLVED_WORDS = {"CLOSED", "LOCKED", "RESOLVED", "DISCHARGED"}


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _rows() -> list[dict]:
    return list(csv.DictReader(io.StringIO(CSV.read_text())))


def _json() -> dict:
    return json.loads(TM_JSON.read_text())


def _current_file_hashes() -> dict[str, str]:
    out = {}
    for f in subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True).stdout.split():
        p = REPO / f
        try:
            out[f] = _sha(p)
        except OSError:
            pass
    return out


def _resolve_path(token: str) -> bool:
    token = token.strip().rstrip(".,;:)")
    for cand in (token, f"paper9/{token}"):
        if (REPO / cand).exists():
            return True
    return False


PATH_RE = re.compile(r"(?:paper9/)?(?:audit|verification|plan|params|results|production|solver|eqs|validation|latex|tables|figures|bench)/[A-Za-z0-9_./-]+")
SHA_RE = re.compile(r"sha256[^\n]{0,120}?([0-9a-f]{12,64})")


def _hash_tokens(text: str) -> set[str]:
    """Hash-like tokens cited after a `sha256` label, excluding decimal-number fragments."""
    out = set()
    for m in SHA_RE.finditer(text):
        tok = m.group(1)
        start, end = m.start(1), m.end(1)
        before = text[start - 1] if start else ""
        after = text[end:end + 3]
        if not any(c in "abcdef" for c in tok):
            continue                      # pure digit run (a decimal number)
        if before.isdigit() or before == ".":
            continue                      # part of a decimal number
        if after.startswith("e-") or after[:1].isdigit():
            continue                      # float exponent tail
        out.add(tok)
    return out


def collect_findings() -> list[dict]:
    findings: list[dict] = []
    rows = _rows()
    js = _json()
    fh = _current_file_hashes()

    # ---- 1. duplicate ids ----------------------------------------------------
    ids = [r["claim_id"] for r in rows]
    for cid in sorted({i for i in ids if ids.count(i) > 1}):
        findings.append(dict(id=cid, cat="A", what="duplicate claim id in the CSV"))

    # ---- 2. referenced paths resolve ----------------------------------------
    cells = []
    for r in rows:
        cells += [f"{k}: {v}" for k, v in r.items()]
    cells += [json.dumps(js)]
    for cell in cells:
        for tok in PATH_RE.findall(cell):
            if not _resolve_path(tok):
                findings.append(dict(id="register", cat="A", what=f"referenced path does not resolve: {tok}"))

    # ---- 3. hash citations resolve or are labelled historical ---------------
    seen_tokens: set[str] = set()
    for cell in cells:
        for tok in _hash_tokens(cell):
            if tok in seen_tokens:
                continue
            seen_tokens.add(tok)
            if any(h.startswith(tok) or tok.startswith(h) for h in fh.values()):
                continue
            hist = [h for h in HISTORICAL_TOKENS if h.startswith(tok) or tok.startswith(h)]
            if hist:
                findings.append(dict(id="register", cat="B",
                                     what=f"historical hash citation {tok[:12]}… ({HISTORICAL_TOKENS[hist[0]]})"))
                continue
            findings.append(dict(id="register", cat="D", what=f"unclassified hash citation {tok[:12]}…"))

    # ---- 4. explicit historical labelling present ---------------------------
    blob = CSV.read_text() + TM_JSON.read_text()
    for tok, why in HISTORICAL_TOKENS.items():
        if tok not in blob:
            findings.append(dict(id="register", cat="D", what=f"historical citation {tok[:12]}… removed"))
    for needle in ("historical snapshot", "historical P12H record only", "historical; verified against commit fb9bd5d"):
        if needle not in blob:
            findings.append(dict(id="register", cat="A", what=f"missing historical label: {needle!r}"))

    # ---- 5. CSV / JSON agreement -------------------------------------------
    meta = js["metadata"]["p12h_amendment"]
    canonical_bp = meta["blueprint"].get("v1.4_sha256_canonical")
    canonical_plan = meta["plan"].get("sha256_canonical")
    if not canonical_bp:
        findings.append(dict(id="BP-v1.4", cat="A", what="no canonical v1.4 hash registered (historical-only citation)"))
    elif canonical_bp != _sha(BP14):
        findings.append(dict(id="BP-v1.4", cat="A", what="JSON canonical v1.4 hash does not match the frozen file"))
    if not canonical_plan:
        findings.append(dict(id="PLAN-5i", cat="A", what="no canonical plan hash registered (historical-only citation)"))
    elif canonical_plan != _sha(REPO / "paper9" / "plan" / "CALC_MASTER_PLAN.md"):
        findings.append(dict(id="PLAN-5i", cat="A", what="JSON canonical plan hash does not match the plan file"))
    csv_bp = [r for r in rows if r["claim_id"] == "BP-v1.4"][0]["notes"] if any(r["claim_id"] == "BP-v1.4" for r in rows) else ""
    csv_pl = [r for r in rows if r["claim_id"] == "PLAN-5i"][0]["notes"] if any(r["claim_id"] == "PLAN-5i" for r in rows) else ""
    if canonical_bp and canonical_bp not in csv_bp:
        findings.append(dict(id="BP-v1.4", cat="A", what="CSV row does not carry the canonical v1.4 hash"))
    if canonical_plan and canonical_plan not in csv_pl:
        findings.append(dict(id="PLAN-5i", cat="A", what="CSV row does not carry the canonical plan hash"))
    if meta["blueprint"]["v1.4_sha256"][:12] not in csv_bp:
        findings.append(dict(id="BP-v1.4", cat="D", what="CSV row lost the historical P12H v1.4 hash"))
    if meta["plan"]["sha256"][:12] not in csv_pl:
        findings.append(dict(id="PLAN-5i", cat="D", what="CSV row lost the historical P12H plan hash"))

    # ---- 6. TV state agreement --------------------------------------------
    tvj = js["technical_variations"]
    csv_tv = {r["claim_id"]: r["status"] for r in rows if r["claim_id"].startswith("TV")}
    for cid, status in csv_tv.items():
        if cid not in tvj:
            continue
        a, b = status.split()[0], tvj[cid]["status"].split()[0]
        if status.split()[-1] != tvj[cid]["status"].split()[-1]:
            findings.append(dict(id=cid, cat="A", what="provenance class differs between CSV and JSON"))
        elif a != b:
            if a in RESOLVED_WORDS and b in RESOLVED_WORDS:
                findings.append(dict(id=cid, cat="C",
                                     what=f"resolution-word variant {a!r} vs {b!r} (same governed meaning)"))
            else:
                findings.append(dict(id=cid, cat="A", what=f"state conflict: CSV {status!r} vs JSON {tvj[cid]['status']!r}"))
    for cid, tv in tvj.items():
        if tv["status"].split()[0] not in RESOLVED_WORDS and "OPEN" not in tv["status"]:
            findings.append(dict(id=cid, cat="A", what=f"JSON state {tv['status']!r} is neither resolved nor OPEN"))

    # ---- 7. version / provenance claims ------------------------------------
    prov = PROVENANCE.read_text()
    if "| Paper9_Blueprint_v1.5.tex | 1.5 | b96c8e76" not in prov or "CURRENT governing specification" not in prov:
        findings.append(dict(id="BP-v1.5", cat="A", what="PROVENANCE.md does not declare v1.5 CURRENT"))
    if _sha(BP15) != "b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91":
        findings.append(dict(id="BP-v1.5", cat="A", what="frozen v1.5 hash changed"))
    rec = json.loads(RECORD.read_text())
    if not rec["governing_spec"].startswith("Paper9_Blueprint v1.5"):
        findings.append(dict(id="BP-v1.5", cat="A", what="machine record does not point at v1.5"))
    if "FROZEN, superseded by v1.5" not in prov:
        findings.append(dict(id="BP-v1.4", cat="A", what="PROVENANCE.md does not mark v1.4 frozen/superseded"))

    # ---- 8. governing numbers in the metadata ------------------------------
    g = json.loads(GOVERNING_JSON.read_text())
    if meta["governing_numerical_artifact_unchanged"]["p"] != repr(g["5i"]["slope"]):
        findings.append(dict(id="PLAN-5i", cat="A", what="metadata p does not match the governing artifact"))
    if meta["governing_numerical_artifact_unchanged"]["ci95"] != [repr(x) for x in g["5i"]["CI95"]]:
        findings.append(dict(id="PLAN-5i", cat="A", what="metadata CI does not match the governing artifact"))
    if meta["governing_numerical_artifact_unchanged"]["epsilon_delta"] != repr(g["5i"]["eps_Delta"]):
        findings.append(dict(id="PLAN-5i", cat="A", what="metadata eps_Delta does not match the governing artifact"))

    # ---- 9. no BP-v1.5/A2 row may exist (P12Z decision A stands) -----------
    if "BP-v1.5" in ids:
        findings.append(dict(id="BP-v1.5", cat="A", what="a BP-v1.5 row was added (P12Z decision A forbids)"))
    if "A2" in CSV.read_text() or "v1.5" in CSV.read_text():
        findings.append(dict(id="register", cat="A", what="the register body now cites A2/v1.5"))

    return findings


def dedupe(findings: list[dict]) -> list[dict]:
    seen, out = set(), []
    for f in findings:
        key = (f["id"], f["cat"], f["what"])
        if key not in seen:
            seen.add(key)
            out.append(f)
    return out


def summarise(findings: list[dict]) -> dict:
    cats = {"A": 0, "B": 0, "C": 0, "D": 0}
    for f in findings:
        cats[f["cat"]] += 1
    return cats


def main() -> int:
    findings = dedupe(collect_findings())
    cats = summarise(findings)
    print("=" * 78)
    print("P12AA TRACEABILITY-REGISTER PROVENANCE CHECK")
    print("=" * 78)
    print(f"register : {CSV.name} ({_sha(CSV)[:16]}…)")
    print(f"           {TM_JSON.name} ({_sha(TM_JSON)[:16]}…)")
    print(f"rows     : {len(_rows())} CSV claims / {len(_json()['technical_variations'])} JSON TVs")
    print("-" * 78)
    for f in sorted(findings, key=lambda x: (x["cat"], x["id"], x["what"])):
        print(f"  [{f['cat']}] {f['id']:<12} {f['what']}")
    print("-" * 78)
    print(f"anomalies: A(active error) = {cats['A']} | B(historical/valid) = {cats['B']} | "
          f"C(harmless equivalent) = {cats['C']} | D(unresolved) = {cats['D']}")
    ok = cats["A"] == 0 and cats["D"] == 0
    print("RESULT   :", "PASS — every active reference resolves or is explicitly labelled historical"
          if ok else "FAIL — active errors or unresolved references remain")
    print("=" * 78)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
