# RECOVERY CHECKPOINT — P12R (pre-work)

**Purpose:** recovery point created **before any P12R work** (Blueprint v1.5 graphical-validation
amendment phase).

**Naming note:** an earlier status-only audit labelled P12R (PI-decision wait) produced **no files** and
left the repository unchanged; this file belongs to the **Blueprint amendment** phase of the same label.

| Field | Value |
|---|---|
| Repository | `https://github.com/vipin-oss/BFS-FEM-MATLAB` |
| Branch | `phase-1-symbolic` |
| Starting local SHA | `1b0523606a0545121c8ffb807b7a2203fe548a9a` |
| Starting remote SHA | `1b0523606a0545121c8ffb807b7a2203fe548a9a` (verified by fetch + `ls-remote`) |
| Tree at entry | **clean**; 24/24 tracked `*/out/` artifacts present |
| P12Q content / final checkpoint | `379abcaf0f5a4a84c73617f24ad1d68542820da4` / `1b0523606a0545121c8ffb807b7a2203fe548a9a` |
| P12P content / final checkpoint | `c5138a591aba19fd2a29b017011d21782ff8306d` / `059239efb15068b2477a3cf9a486738c3b7d88ec` |
| P12O content / final checkpoint | `1610231ecf7644884774d9516ea814b3444736be` / `9f259a0907512c4291b578951b0862db66894a2d` |
| P12N content / final checkpoint | `dbaf1e92d51926adfa9b52873b61712e405c0e1f` / `4dcf91d51d126a165b02d0520d2d2638edf56c33` |
| P12M content / final checkpoint | `88961608524d8de51e29ee1662051efdedb3b9df` / `3ea85e36c85b22520e263dc58c6fca8cc0693720` |
| P12L content / checkpoint | `f1f67f3e6a7410f8e07909c6f7a6a5a491adb89f` / `de442bfcfaadc3ea741cde9daf7f911716b331f8` |
| **Governing Blueprint at entry** | **v1.4** `2ae0b1e8f37e10a0685a0b0ffd94e695bd62e3b4da6a02052a76190fc0acb638` (= v1.3 `ca71b91a…` + exactly 4 locked line-blocks) |
| P12R pre-work checkpoint SHA (this file) | recorded in the P12R session report after the verified push |
| P12R amendment commit SHA | recorded in the P12R session report after the verified push |

## Status at entry (locked; the amendment does not change these)

| Item | Status |
|---|---|
| **PCR1** | **NOT PASS** |
| **G3** | **NOT MET** |
| **G4** | **NOT MET** |
| **P5** | **NOT PASS / OPEN** |
| **R-1** | **OPEN** |
| **PCR5** | **PASS** |
| **P13** | **BLOCKED** |

External-evidence state: author requests **NOT SENT**; **no author contacted**; **no author data
received**; B1/B2/B3 `quantitative_error` **NULL**; B2 `l` vs `l̄` **unresolved**; no digitisation; no
substitute values; thresholds unchanged (≤ 2 %; B1 ≤ 0.5 %).

## P12R scope (this phase)

Prepare a **minimal, documented amendment** introducing a three-way external-validation classification
(quantitative / graphical / not validated) with the quantitative tier and its thresholds unchanged:
Blueprint **v1.5 = v1.4 + the smallest possible new amendment block(s)**, v1.4 preserved intact; a
governance classifier plus synthetic tests for the classification; the amendment record; and evidence
that no governing numerical result, manuscript, draft request or benchmark-evidence file changed.

**Not in scope / not performed:** B1/B2/B3 revalidation, curve digitisation, threshold changes, model
or production changes, manuscript edits, author contact, P13. **PCR1/G3 are not promoted** by the
existence of the amendment; promotion requires an actual audited benchmark reproduction in a later,
separately authorized phase.
