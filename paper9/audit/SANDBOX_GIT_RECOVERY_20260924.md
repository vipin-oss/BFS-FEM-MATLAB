# Sandbox git recovery — 2026-09-24 (third re-provisioning incident)

**What happened.** Between the P12E task and the P12F decision audit, the workspace was
re-provisioned again: the repository's `.git` directory and **every generated `*/out/` directory**
were dropped, exactly as in the two earlier incidents. All tracked *content* files survived
byte-identically.

**What was restored.**

| item | method | verification |
|---|---|---|
| `paper9/tables/out/` (7 files) + `paper9/figures/out/` (17 files) | copied from an anonymous clone of the public remote at `0d985029` | 24/24 files sha256-identical to the clone; aggregate tree hashes match the P12E pre-change snapshot (`tables/out eda2a0e2…`, `figures/out 2e21a83b…`, `latex a0f4fb8c…`) |
| `.git` | full anonymous clone (`git clone --branch phase-1-symbolic`), `.git` moved into the repository | clone HEAD confirmed `0d9850290b63a5da81b098d999714ab621684c77` = remote `phase-1-symbolic` |
| file modes | `chmod +x` re-applied to `paper9/production/p5_pilot.py`, `paper9/production/run_p5_production.py` | mode-only diffs cleared |

**Content verification (all 15 protected artifacts re-hashed against the P12E pre-change
snapshot, `audit/evidence/p12e/pre_change_snapshot.json`).** Zero mismatches — including the
Blueprint v1.3 (`ca71b91a…`), the governing P4B JSON (`38384363…`), the historical TXT
(`1daf0f32…`), the original P4B script (`b1c8d996…`), the P12C raw JSONs (`5547bae4…`,
`c8910c0d…`), the P11D evidence (`1d4476f1…`, `7dbabbd3…`), the manuscript files and the plan.
The P12E evidence bundle also re-verifies: run-1 JSON `0c027bfc…`, run-2 JSON `4fc30924…`,
`routeF_patch.diff` `03b902d2…`, suite log `450062bf…`.

**Superseded commit SHAs (local only, never pushed; objects unrecoverable).**
`e75d91b` · `6f7850d` · `bb32253` · `09d5196` · `ff139bf` — these were the recovery
re-materialisation, the post-B1 independent audit, the G-1 guard revision + R-1/C-1 readiness
audit, the P12D design audit, and the P12E re-baseline audit respectively. Their **content is
preserved exactly** in the working tree and is re-materialised by this recovery commit; only the
commit objects are lost. Documents that cite these SHAs are historical records and are **not**
rewritten — this note is the mapping legend. Remote `phase-1-symbolic` remains at `0d985029`;
nothing was pushed.

**Standing procedure (unchanged):** at task start, `git rev-parse` + check `*/out/` existence;
never attempt object recovery; verify content by hash rather than by SHA.
