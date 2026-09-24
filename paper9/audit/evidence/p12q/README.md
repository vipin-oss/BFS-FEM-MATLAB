# P12Q evidence bundle — PI decision handoff / no-action hold

Entry state: local == remote == `059239efb15068b2477a3cf9a486738c3b7d88ec` (fetched and verified).
P12Q pre-work checkpoint: `580c90e0c6933cfdaf44d13242281c861f68764f` — pushed and verified by both
`git fetch` and `git ls-remote origin phase-1-symbolic`, **before** any P12Q work.

Also recorded: sandbox environment recovery (5th occurrence of the dropped `.git`/`*/out/` pattern) —
anonymous clone verified HEAD `059239e…`, `.git` moved in, worktree restored (24/24 tracked `out/`
artifacts), exec bits restored on the two P5 scripts, identity re-set. No history rewrite, no new branch.

| File | What it is |
|---|---|
| `suite_run1.txt` | Full suite: **126 passed, 1 skipped** (7.80 s in the checks run; confirmation run logged here). The skip is the pre-existing opt-in rerun. |

Added in P12Q: `audit/P12Q_PI_DECISION_HANDOFF.md` only (plus this bundle). The record presents the two
PI options verbatim (A — authorize sending as drafted, unmodified; B — do not send, retain drafts, keep
statuses blocked), the eight required state statements, the preserved statuses, and the
`PI DECISION REQUIRED` block. **Neither option is selected by the agent.**

Regression: suite 126P/1S; PCR/gate guard sub-suites 33P; manuscript/Blueprint cross-check 43/43;
immutability 8/8 anchors; `quantitative_error` still `[None, None, None]`. No test modified.
**No status promoted. Drafts untouched byte-identical. P13 blocked.**
