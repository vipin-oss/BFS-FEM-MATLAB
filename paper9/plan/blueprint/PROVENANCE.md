# Blueprint frozen copies - provenance

Source of truth (working copy): /home/user/femcheck/blueprint/Paper9_Blueprint.tex (= v1.3).
These repository copies are version-controlled frozen snapshots for traceability.

| File | Version | sha256 | Status |
|---|---|---|---|
| Paper9_Blueprint_v1.2.tex | 1.2 | 742acc9ec97864999595e6c6248017285944747fe02c11eac86521334b06fe9c | FROZEN, superseded |
| Paper9_Blueprint_v1.3.tex | 1.3 | ca71b91aba4ca4abe9f157eb595ac8c2f709d838957a08ea0dce7160685dbf9f | CURRENT governing specification |

v1.2 -> v1.3 diff (2026-09-22, editorial-only, user-authorised): exactly three hunks -
(1) SUBSTANTIVE: Week-6 schedule G2 cell "all 7 internal tests pass" -> "all 8 automated internal tests pass";
(2) metadata: title-page version string 1.2 -> 1.3;
(3) record: lock-banner revision clause documenting the editorial change.
No equation, parameter, table, figure, gate meaning, benchmark card, phase or scientific
requirement was altered. v1.0 backup remains at /home/user/femcheck/blueprint/Paper9_Blueprint_v1.0_backup.tex.

---

**Added 2026-09-24 (P12R) — additive provenance for the later frozen copies. Nothing above is altered.**

| File | Version | sha256 | Status |
|---|---|---|---|
| Paper9_Blueprint_v1.4.tex | 1.4 | 2ae0b1e8f37e10a0685a0b0ffd94e695bd62e3b4da6a02052a76190fc0acb638 | FROZEN, superseded by v1.5; byte-identical since creation |
| Paper9_Blueprint_v1.5.tex | 1.5 | b96c8e76071d03decb55dd6d71bc76cb2a9c206b945f692879d92cda2de37a91 | CURRENT governing specification |

v1.3 -> v1.4 (2026-09-24, A1, user-authorised): exactly four changed single-line blocks (lines 95, 446,
618, 895) - the version row, the §5.7 pre-declared resolution/admissibility rule "Rule R-fit", the
figure-register wording for the convergence figure, and PCR5. Itemised in
`paper9/audit/P12H_A1_PROTOCOL_CLOSURE_AUDIT.md`; the §5.7 declared zero was later stated explicitly by
P12J (`e_i > F * max(s_i, 1e-15)`, F = 3).

v1.4 -> v1.5 (2026-09-24, amendment A2, PI-directed, P12R): exactly eight blocks (six single-line
replacements 95, 457, 471, 803, 886-888, 1046 and two insertions - new Section 13 and a footer revision
note) introducing the three external-validation evidence routes (quantitative / graphical / not
validated). **Quantitative thresholds unchanged (<= 2 %; <= 0.5 % classical target)**; v1.4 preserved
byte-identical. Itemised in `paper9/audit/BLUEPRINT_V1_5_GRAPHICAL_VALIDATION_AMENDMENT.md`.

*Note: the rows above this block still describe v1.3 as current; that was true when they were written and
they are deliberately left unedited.*
