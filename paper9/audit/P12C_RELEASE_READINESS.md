# P12C Release-Readiness Summary (Part K)

Base commit: `phase-1-symbolic @ 0d985029` (P12C close-out) + audit commits
`75d2eb9` (Parts A–C), `3138584` (Parts D–E), `355c660` (Parts F–H), `f529253` (Parts I–J).
One branch; no push; no P12E integration (P12E objects unavailable here); P12C raw results,
production scripts and Blueprint v1.3 unmodified.

## 1. Evidence
All P12C Case-C evidence re-verified directly (Part A): raw JSONs byte-identical (32²
`5547bae4…`, 64² `c8910c0d…`, sidecars match), five-mesh Δ_complete series
2.5732 / 2.2504 / 2.0722 / 1.9736 / 1.9179 reproduced from the files, decrements
0.3228 / 0.17814 / 0.09861 / 0.05575 and ratios 0.552 / 0.554 / 0.565 recomputed, 64² trigger
fired legitimately (r = 0.5535652777739338 ≥ 0.5), NOT-mesh-converged status honoured, P11D 4²/8²/16²
and the 41² BZ evidence preserved, Δ_X ≢ Δ_complete kept distinct, extrema locations correct,
real-calculation provenance and deterministic repeatability confirmed. **PASS.**

## 2. Traceability
S1–S6 constant ledgers + 24-row trace (Part B): every Case-C manuscript number maps to a governing
raw artefact; no unsourced hard-coded numbers; duplicates and rounding documented (F-1…F-10).
**PASS with B-class notes** (see §9).

## 3. Manuscript
C-1…C-18 classification (Part C); 11 corrections applied and test-verified. After correction the
manuscript contains: no "fully solved"/"converged complete gap"/"quadrature invariance"/"exact
interface" claims; correct 4×4 attributions for the 2.5732 series; correct 5a–5h test list; correct
ε_Δ equation; P4B p = 4.17 with "no theoretical order claimed" and a locked operational floor.
**PASS.**

## 4. Quadrature / FEM mathematics
4×4 Gauss–Legendre is the minimal exact tensor rule for the homogeneous element matrices (degree 6
per coordinate; probe-confirmed 1.2e-15 agreement at n=4, exactness limits 3/5/7); cut/interface
elements are integrated with O(h) indicator error (7.09e-2 → 1.22e-4) and are **not** claimed exact;
"quartic" in the Blueprint denotes the factor degree only. **PASS, properly scoped.**

## 5. P4B
Governing `verification/suite/p4b_5g_to_5i.json`: slope 4.173919246515192, CI95
[3.1453687594104447, 5.202469733619939], ε_Δ = 4.6318154949690315e-11, 5i criterion satisfied,
5g subset {0.2, 0.5}. All manuscript P4B values match the JSON. **Blocker B1 (RESOLVED 2026-09-24 — see the update section at the end):** the paired
`p4b_5g_to_5i.txt` log reports slope 5.4857 / ε_Δ 4.626e-11 from an earlier execution and was
**not** reconciled or edited. Prompt-supplied P12E values (slope 4.71578752682248, CI
[3.377399590254491, 6.054175463390468], ε 4.6619906233888485e-11) are absent from this tree →
unverifiable here, not imported.

## 6. PCR1–PCR8 (Blueprint v1.3, unchanged definitions)
PCR1 **NOT MET** (no author-released floating-point datasets). PCR2 PASS (internally verified B2
registry), PCR3 PASS, PCR4 PASS, PCR5 PASS (eight-test 5a–5h suite), PCR6 PASS (32 tagged parameter
rows + Table 2), PCR7 **PASS** (P12B §6 FoM evidence; M_s = 0.0000°, δ_max = 2.79°, figures 12/14,
live-recompute guard), PCR8 PASS. No status promoted merely because tests pass.

## 7. G1–G4 (Blueprint v1.3, unchanged definitions)
G1 MET (internal verification + convergence evidence), G2 MET (implementation/consistency),
**G3 NOT MET** (external quantitative validation demands author tables), **G4 NOT MET**.
P5 production status **NOT PASS / OPEN** — and no P5-production claim appears in
`latex/sections/` (Part F). Pre-registered verifications (G5/G6) remain PASS in their existing
audit records and were not altered here.

## 8. Test suite
Authoritative suite run twice independently: **83/83 passed, 0 failed, 0 skipped, exit 0**
(6.84 s / 7.10 s) — `paper9/audit/P12C_POST_CLOSEOUT_SUITE_RUN.md`, logs under
`paper9/audit/logs/` (sha256 recorded). Non-suite tests: 30/30 passed. Whole-repo collection: 113
tests. Suite = 72 pre-audit tests + 11 new Part G guards (guards also run twice on their own).
No test deleted, weakened or skipped. A third, post-audit confirmation run (after Parts I–K were
written) is logged at `paper9/audit/logs/p12c_post_closeout_suite_final.txt`
(sha256 `8db9d9ee8150918e58bedf199100ca0caa0f74b527c5d24363288c6635ecfb41`): **83 passed, exit 0**.

## 9. Stale claims
Repo-wide term search (Part I): 26 terms, all tracked files, classified ACTIVE / HISTORICAL /
EVIDENCE / FIXED / STALE. **Zero STALE active claims after the Part C/E fixes**; historical audit
records preserved (not silently deleted). Watchlist (documented, not blockers): P11 raw-JSON
metadata TV18 wording, P11B "negligible" phrasing, P12A PCR7 "PARTIAL" superseded by P12B, P4B
txt/json divergence (B1), CSV `TV6` row stale vs the JSON matrix.

## 10. Blockers
- **B1 — P4B json↔txt divergence (open).** Do not quote the txt log; reconcile before submission or
  next-phase release. Recorded in Parts E and L-of-K; no silent fix applied.
- **B2 — Governing gates unmet by design.** PCR1, G3, G4 NOT MET; P5 NOT PASS/OPEN. These require
  external evidence (author datasets, P5 production closure), not internal tests; they block any
  "final"/"release-ready" language.
- **B3 — P12E artifacts unavailable in this environment.** Any P12E-derived number is unverifiable
  here; nothing P12E was reconstructed or transplanted (per instruction).
- **B4 — Cosmetic/historical:** CSV `TV6` row; P12C run-log checkpoint dir not committed (reruns
  supported from scratch); Part B duplicate-value notes (F-5) and A-F2 inert hard-code.

## 11. Verdict

**BLOCKED for release** — governing gates PCR1, G3, G4 are NOT MET and P5 is NOT PASS/OPEN; the
paper must not be described as final or release-ready. **READY_FOR_NEXT_PHASE** for continued
development: evidence is intact and reproducible, traceability is complete, the manuscript is
consistent with P12C evidence, guards enforce the invariants, and the suite is green twice
(83/83 + 30/30). Blocker B1 is the one open in-tree reconciliation item; B2 requires new external
evidence and cannot be closed by internal work.


---

## Update — B1 resolved (appended 2026-09-24; no earlier text altered)

The P4B json↔txt blocker B1 (Part E, finding E-F1) is **CLOSED**:
`P4B_B1_PROVENANCE_RECONCILIATION.md` and `P4B_B1_RESOLUTION_CLOSEOUT.md` establish that the pair is
two executions of the same script (TXT = run 1, JSON = run 2), that the divergence comes from the
nondeterministic 5i eigensolve straddling the script's fixed `err > 1e-14` fit-subset cut, and that
the JSON governs on provenance, consumption and reproducibility grounds. The TXT is preserved
byte-identical and labelled; the record carries an append-only provenance addendum; a regression
guard (`verification/suite/test_p4b_b1_json_txt_consistency.py`, 8 tests, run twice) now fails on any
silent TXT/JSON drift, manuscript leakage of run-1 values, or theoretical-order claim. Full suite
after the change: 91 collected, 90 passed, 1 skipped, exit 0 (twice).

The release verdict above is **unchanged** (PCR1 / G3 / G4 NOT MET; P5 NOT PASS/OPEN): B1 was a
reconciliation item, not a governing gate.
