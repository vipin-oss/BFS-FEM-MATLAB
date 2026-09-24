# RECOVERY CHECKPOINT — P12M

**Purpose:** authoritative recovery point for the author-data-request preparation phase. Recovery must
be possible from the remote branch alone.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| Local SHA at P12M entry | `de442bfcfaadc3ea741cde9daf7f911716b331f8` (verified, tree clean) |
| P12M checkpoint-push SHA | `912f14133efc4016d9a8b699ad8eb6e71c84f7a4` (pushed and verified **before** any new work) |
| Remote SHA at P12M entry | `de442bfcfaadc3ea741cde9daf7f911716b331f8` (fetched and `ls-remote`-verified — **local == remote**) |
| P12J SHA | `876213a8c4211ed4971735f6291a9a943f2dda24` |
| P12K SHA (content) | `476cac0c0b788b805563c766e3992ce2271b108b` (plus checkpoint records `f4d965d3ae120c3a4e9e8a088d872807c61b1d5c`, ledger `8d6895ad9c4aa75be9a70f7633167732cbec1177`) |
| P12L content SHA | `f1f67f3e6a7410f8e07909c6f7a6a5a491adb89f` |
| P12L checkpoint SHA | `de442bfcfaadc3ea741cde9daf7f911716b331f8` |
| **P12M content SHA** | **`88961608524d8de51e29ee1662051efdedb3b9df`** (pushed `912f141..8896160`, fetched, `ls-remote` verified) |
| P12M checkpoint-record SHA | printed in the P12M session report — **remote HEAD** after the final push (a file cannot embed its own hash) |

## Status (locked; nothing promoted in P12M)

| Item | Status |
|---|---|
| PCR1 | **NOT PASS** |
| G3 | **NOT MET** |
| G4 | **NOT MET** |
| P5 | **NOT PASS / OPEN** |
| R-1 | **OPEN** |
| PCR5 | **PASS** |
| C-1 | OPEN · G-1 CLOSED |
| **P13** | **BLOCKED** |

## Governing numerical values (unchanged)

```
p        = 4.173919246515192
CI       = [3.1453687594104447, 5.202469733619939]
ε_Δ      = 4.6318154949690315e-11
admissible subset = {4², 8², 16²};  excluded = {32²};  "no theoretical order claimed"
```

Key hashes: Blueprint v1.3 `ca71b91a…` (byte-identical), Blueprint v1.4 `2ae0b1e8…`, Rule R-fit
`rule_rfit.py` `d4fed492…`, governing JSON `38384363…`, historical TXT `1daf0f32…`, P4B script
`b1c8d996…`, `benchmark_evidence.json` `e9191506…`.

## Author-data route — the current authorized action

- **Specification (authoritative):** `paper9/audit/P12L_AUTHOR_DATA_REQUEST_SPEC.md`
- **Blocking rationale (authoritative):** `paper9/audit/P12L_PCR1_G3_FORMAL_BLOCKER_RECORD.md`
- **Forensic basis:** `paper9/audit/P12K_PCR1_G3_BLOCKER_FORENSIC_AUDIT.md`
- **This phase (P12M):** PI-authorized preparation of three scoped, ready-to-send author requests
  (`paper9/audit/P12M_AUTHOR_REQUEST_DRAFTS.md`) and the evidence-receipt templates
  (`paper9/audit/author_data/B{1,2,3}_DATA_RECEIPT_TEMPLATE.md`). **Requests are prepared but NOT
  sent; no author contact has been made; no recipient address is stated anywhere.**
- **Next action after P12M:** the PI sends the three requests (or decides otherwise). Nothing else is
  authorized; receipt of data alone closes no gate.

## Remaining blockers

1. **PCR1 / G3** — author-released numerical benchmark data for B1/B2/B3 (B2 additionally requires the
   `l` vs `l̄` clarification). No repository-only closure route exists (P12L).
2. **G4** — PI signature after PCR1–PCR8 are checked; independent of, and not implied by, PCR1 closure.
3. **P5** — parallel-pipeline reconciliation (internal; unaffected by author data).
4. **R-1** — pipeline-level reproducibility (requires the unauthorized re-baseline; unaffected by
   author data).
5. **C-1** — discriminant criterion not deployed in the production script.

## Exact next action

Send the three requests (PI act) using `P12M_AUTHOR_REQUEST_DRAFTS.md`; on receipt of data, follow the
acceptance protocol and use the receipt templates. **Do not start P13.** After every major block,
create and push a recovery checkpoint before the next risky block.
