# RECOVERY CHECKPOINT — P12AA (pre-work)

**Phase:** P12AA — traceability metadata remediation (P12Z-O1/O2/O3) + pre-P13 readiness audit.
**Objective:** remediate the three remaining traceability-metadata observations with byte-minimal,
provenance-preserving edits (historical values stay labelled; canonical values become resolvable),
run a full metadata-integrity audit of the register, and produce a consolidated pre-P13 blocker
matrix and readiness audit. **No** scientific result, route, threshold, gate definition, Blueprint or
manuscript change; no author contact; no gate promotion.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| **Entry SHA (verified)** | **`70ad253a98f4ea96e3ceb98c37f85bde629f615d`** (P12Z final; local = origin = ls-remote, clean tree) |
| **P12AA pre-work checkpoint** | this commit (SHA recorded in the final checkpoint) |
| Baseline | `/home/user/p12aa_baseline_hashes.txt` — 530 tracked files (`git ls-files -z \| xargs -0 sha256sum`) |
| Register at entry | `traceability_matrix.csv` `4ce06f024bf41f12688998fd26c2861cf04dd9adaefbab93213d48698e573b04`; `traceability_matrix.json` `f332e03117b60643ecd901d64c585d3accac401b55c7bca54054d5bff1118b6f` |

**Planned remediations (Part B/C/D):**

* **O1** — `BP-v1.4` row / JSON `p12h_amendment.blueprint`: keep the P12H-time hash `0089754b…`
  explicitly labelled historical and add the canonical frozen v1.4 hash `2ae0b1e8…` (from
  `plan/blueprint/PROVENANCE.md`).
* **O2** — `PLAN-5i` row / JSON `p12h_amendment.plan`: the recorded `a45a5448…` matches no reachable
  revision (462 reconstruction variants + BOM/CRLF variants + a full filesystem hash scan found no
  artifact); point the active reference at the canonical amended plan `1f1c080b…` and keep
  `a45a5448…` / `0e2c3a3a…` explicitly labelled historical.
* **O3** — `TV6` state word aligned with the authoritative JSON (`LOCKED [S]`); `TV14`/`TV18`
  (`CLOSED [S]` vs `LOCKED [S]`) assessed as register-vocabulary equivalents (the repository's own
  `check_traceability.py` treats CLOSED/LOCKED/RESOLVED/DISCHARGED alike) and left unnormalised
  unless the audit shows otherwise.

**Off-limits / immutable:** Blueprint v1.4 and v1.5, `PROVENANCE.md`, Rule R-fit, manuscript,
production, results, tables, analytic sources, source PDFs, validation assets, P12S–P12Z evidence and
records, raw P12S/P12U records, author-request drafts and specification, historical audit documents
(including the P12H audit, whose recorded `a45a5448…` stays untouched as history).

**Deliverables:** register metadata corrections (CSV + JSON, kept in agreement); a provenance checker
(`paper9/audit/check_register_provenance.py`); a register-integrity audit record; the pre-P13 blocker
matrix (machine-readable + human-readable); a readiness audit; the P12AA guard suite; this checkpoint
(final form); the audit commit and the final checkpoint commit, pushed and tri-equal verified.
