# P3 — published analytical validation (2026-09-22)

**Phase order:** P4A done; P3 active; **P4B not started**.
**Solver available:** 1-cell 2-D homogeneous Case-H BFS Bloch (P4A). **No** 1-D bilayer C¹ FE, **no** production TM in `bench/reference_tm/`.

## Compact results

| ID | Layer | Source | Executed? | Metric | Result |
|---|---|---|---|---|---|
| B1 | 1 / Fig 2(a) Li 2024 | Sci. Rep. 14:24035 | **No** vs published curve | ≤0.5% | **OPEN / blocked** |
| B2 | 2a / Fig 2(b) Li 2024 | same; f=0, l=1e-5, l₁=2e-5 | **No** vs published curve | ≤2% | **OPEN / blocked** |
| B3 | 2b Li–Askes–Gitman 2023 | WRAM Fig 4(c); TV1 | **No** | ≤2% | **OPEN** (TV1, no PDF) |
| B4 | 2c optional Fig 3 2023 | TV8 | **No** | optional | **OPEN** |
| B5 | 3 PB2009 (20)–(28) | PDF [C] vs Case-H [B] | **Yes** 11/11 | machine | **PASS specialisation** (not PCR1) |
| B6 | 3b LWZ2016 TM PC | PDF [C] | **No** bilayer FE | ≤2% | **OPEN / blocked** |
| L3b | PB g,h regimes | PDF [C] | **Yes** | — | **PASS** vs specialised Case-H |

## Why B1 / B2 / B3 / B6 are not scored

1. **No C¹ Bloch-FE bilayer.** Existing solver is homogeneous Case-H. Building a 1-D Case-C FE would be a new solver (forbidden unless a demonstrated bug). Comparing Case-H bands to a 1-D PC figure would be the wrong physics.
2. **Errors vs figures require digitised curves.** Project rule: digitisation is overlay-only, never the error metric. No immutable digitised Fig 2/3/4 data in `paper9/`.
3. **Independent TM** of Li 2024 (53) / LWZ (32) is not implemented in-repo; implementing it here without a second independent FE still cannot close G3.
4. **TV2** (`b` in `k̄=kb/π`) assumed `b=a_A+a_B` in the plan, not re-locked from PDF body beyond (51).
5. **Fig 2 caption** writes `l=10^{-5}` unbarred; plan locked `l̄=1e-5`. Not resolved by invention.
6. **B3 / B4:** 2023 PDF absent; TV1/TV8 OPEN. User “Layer 2B LWZ + Pb/brass a1=1e-5” mixes **B3 (2023)** with **B6 (2016)**. Pb/brass is **not** used as an LWZ parameter (LWZ Fig 3 uses `c̄1=0.5` etc., not Pb/brass).
7. **Do not** substitute PB2009 for LWZ.

**STOP** on G3 published-curve gates rather than invent TM/FE or digitise.

Li 2024 parameters **[C]** from Nature HTML (not used to claim PASS): AlN ρ=3.23e3, c33=3.9e11, a_A=0.01 m; BaTiO₃ ρ′=5.8e3, c′33=1.62e11, a_B=0.01 m; Fig 2(a) l=l₁=f=L=L₁=F=0; Fig 2(b) l=1e-5, l₁=2e-5, f=0, L=5, L₁=5, F=0. ω0 as plan.

## Layer 3 — executed

Independence: **(4) our closed-form specialisation** vs **(2) independently coded PB (20)–(22),(28)**. Same mapping `[B]`; **not** PCR1.

| quantity | n | max rel error | thresh | result |
|---|---|---|---|---|
| ω_T², ω_L² vs (20)(21) | 8 k ∈ [0.1,50] | **5.47e-16** | 1e-12 | PASS |
| long-wave v | κ=1e-4 | **9.25e-11** | 1e-8 | PASS |
| bar (28) vs E-modulus Case-H | 8 k | **2.67e-16** | 1e-12 | PASS |

## Layer 3b — executed

| case | observation |
|---|---|
| g<h (l=0.2, ℓ=0.15 ⇒ g/h≈0.422) | V_∞/C = **0.421637** = g/h < 1 |
| g=h | V=C |
| h=0 | V∼C g k unbounded; k=1e5 ratio to Cgk = 1.00000001 |
| Case-H ℓ=0 vs PB h=0 | rel **2.25e-16** |
| g=0 | V→0 bounded |

Anisotropic `L` **not** compared to PB.

## Gates

| Gate | Status |
|---|---|
| PCR1 (≤0.5% classical, ≤2% other **published**) | **NOT PASS** — B1/B2/B3 not executed vs published data |
| PCR2 evidence for manuscript overlays | **NOT PASS** — no digitised overlays |
| PCR3 closed-form documented + checked | **PASS** for PB2009↔Case-H isotropic `[B]` (11/11, two identical runs) |
| G3 | **not met** |

## Files

`paper9/validation/P3_STATUS.md`, `paper9/validation/L3/p3_layer3_pb2009.py`, log txt, `paper9/audit/P3_STATUS.md`.
TV10/TV11/Blueprint/solver **not** modified.


**Follow-up (source audit):** see `paper9/audit/P3_SOURCE_AUDIT.md`. B1/B2/B3 remain OPEN pending PDFs; B6 PDF present, TM/FE gap specified, not implemented. PCR1/G3 unchanged.

**2024-09-22 PDF extraction:** `audit/P3_B1B2B3_EXTRACT.md`. TV2 CLOSED from Li 2024 (51). TV8 CLOSED for Fig. 3. TV1 Fig.4(c) still OPEN. B1/B2/B3 SOURCE VERIFIED or partial — VALIDATION IMPLEMENTATION BLOCKED. PCR1/G3 unchanged.
