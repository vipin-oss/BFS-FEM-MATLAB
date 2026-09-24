# P12Q — PI Decision Handoff / No-Action Hold

**Entry state:** remote HEAD `059239efb15068b2477a3cf9a486738c3b7d88ec` (verified), tree clean; P12Q
pre-work checkpoint `580c90e0c6933cfdaf44d13242281c861f68764f` committed, pushed and verified before this
record was written. This record performs **no scientific work and no contact with authors.**

---

## 1. State of the prepared requests

1. The prepared **B1/B2/B3 author-data requests are awaiting explicit PI authorization to SEND.**
   They exist as three ready-to-send drafts in `paper9/audit/P12M_AUTHOR_REQUEST_DRAFTS.md` (B1 — Li et
   al. 2024 Fig. 2(a); B2 — Li et al. 2024 Fig. 2(b); B3 — Li et al. 2023 Fig. 4(c)).
2. **P12P found no explicit send authorization anywhere in the audit/governance records**
   (`paper9/audit/P12P_ACTION_GATE.md`; 164 records searched): outcome
   `SEND AUTHORIZATION NOT FOUND — REQUESTS REMAIN UNSENT`.
3. **Existing wording about "PI-authorized preparation" refers only to preparation, not sending** —
   e.g. `RECOVERY_CHECKPOINT_P12M.md` ("PI-authorized **preparation** … Requests are prepared but NOT
   sent"), `P12L_AUTHOR_DATA_REQUEST_SPEC.md` ("no contact has been initiated"), and
   `P12O_AUTHOR_DATA_BLOCKER_DECISION.md` §2 ("Preparation is **not** authorization to send").
4. **Sending is a PI act and must not be inferred** from draft preparation, from the completion of
   P12M/P12N/P12O/P12P, from the "awaiting PI/author action" wording, from blocker documentation, from
   previous assistant prompts, or from the existence of recipient placeholders.
5. **No author has been contacted.**
6. **No author data have been received** for B1/B2/B3.
7. **No numerical benchmark validation can be performed under the current evidence policy** — the
   published records contain no quantitative error values, digitisation is inadmissible (curve
   digitisation is permitted only for overlay figures, never for error percentages), and no substitute,
   estimated, interpolated or reconstructed values may be used. Accordingly B1/B2/B3
   `quantitative_error` remain **NULL** and the B2 `l` vs `l̄` ambiguity remains **unresolved**.
8. **P13 remains blocked.**

## 2. The two PI choices (exactly as recorded)

> ### OPTION A — AUTHORIZE SENDING
> "PI authorizes sending the three prepared B1/B2/B3 author-data requests exactly as currently drafted, without modification."

> ### OPTION B — DO NOT SEND
> "PI does not authorize sending at this stage; retain the requests as prepared drafts and keep PCR1/G3/G4/P5/R-1 blocked."

**The agent does not select either option.** Selection is a PI decision and must be recorded explicitly
(for example by a PI-authored decision entry in this repository or an equivalent governed record naming
the chosen option). Until such a record exists, the gate stays closed.

### Consequences, depending on the selected option

| If Option A is selected | If Option B is selected |
|---|---|
| Sending becomes a **PI act** performed by the PI (the agent still does not contact authors unless separately and explicitly instructed); drafts go out **unmodified**; on receipt of data, the P12N §3 receipt sequence begins | No sending; the three drafts are retained as prepared artifacts; all statuses below remain locked; no further author-data action is taken |

In **both** cases: no digitisation, no substitute numerical values, no threshold change, no manuscript
or Blueprint edit, and no P13.

## 3. Preserved statuses (locked — unchanged by this record)

| Item | Status |
|---|---|
| **PCR1** | **NOT PASS** |
| **G3** | **NOT MET** |
| **G4** | **NOT MET** |
| **P5** | **NOT PASS / OPEN** |
| **R-1** | **OPEN** |
| **PCR5** | **PASS** |
| **P13** | **BLOCKED** |

Governance note retained: author data can move only the **PCR1 → G3 → G4** chain; **P5** and **R-1**
remain independent of external data; the governing numerical baseline and Rule R-fit are untouched
(`p = 4.173919246515192`, CI `[3.1453687594104447, 5.202469733619939]`,
ε_Δ `4.6318154949690315e-11`).

## 4. Reference chain (all remote-verified)

| Phase | Content SHA | Final checkpoint SHA |
|---|---|---|
| P12L | `f1f67f3e6a7410f8e07909c6f7a6a5a491adb89f` | `de442bfcfaadc3ea741cde9daf7f911716b331f8` |
| P12M | `88961608524d8de51e29ee1662051efdedb3b9df` | `3ea85e36c85b22520e263dc58c6fca8cc0693720` |
| P12N | `dbaf1e92d51926adfa9b52873b61712e405c0e1f` | `4dcf91d51d126a165b02d0520d2d2638edf56c33` |
| P12O | `1610231ecf7644884774d9516ea814b3444736be` | `9f259a0907512c4291b578951b0862db66894a2d` |
| P12P | `c5138a591aba19fd2a29b017011d21782ff8306d` | `059239efb15068b2477a3cf9a486738c3b7d88ec` |

---

## PI DECISION REQUIRED

```
Decision:        PENDING PI DECISION
Sending status:  NOT AUTHORIZED / NOT SENT
Data status:     NOT RECEIVED
```

*Options available: A — authorize sending (as drafted, unmodified) · B — do not send (retain drafts,
keep PCR1/G3/G4/P5/R-1 blocked). No option is selected by this record.*
