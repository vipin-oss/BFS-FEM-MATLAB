# P3 source-acquisition audit (blocked validations)

**Date:** 2026-09-22  
**HEAD at start:** `0293adb823f69f4298891525b399f1256f827d99`  
**Rule:** missing PDF ⇒ STOP that validation, keep OPEN, do not invent/digitise.  
**Not started:** new TM/FE solver, P4B, P5, PCR1/G3 claims.

Local PDFs in `paper9/`: only `analytic/pb2009/papargyri-beskou2009.pdf` and `analytic/lwz2016/li2015.pdf`.  
`bench/cards/`, `bench/reference_tm/`, `bench/overlays/`: empty (README only).  
Solver: 1-cell 2-D Case-H BFS Bloch (`verification/suite/p4a_5a_to_5f.py`, M14/M15). P4A 34/34 **untouched**.

---

## B1 — Layer 1 classical (GATE ≤ 0.5%)

| Field | Content |
|---|---|
| Paper | Li, Y.; Li, Y.; Guo, Z.; Wang, H.; Wang, C. (2024). Band gaps of elastic waves in 1-D dielectric phononic crystal with the flexoelectric and strain gradient effects consideration. *Scientific Reports* **14**:24035 |
| DOI | **10.1038/s41598-024-75049-1** |
| Required figure | **Fig. 2(a)** classical elasticity |
| Required eqs | (48)–(53) TM + Bloch `det(T_B T_A − e^{ikb} I)=0`; classical limit of (27)–(31) with `l=l_1=f=0` |
| Caption (Nature HTML, not a substitute PDF) | `(l=0, l_1=0, f=0, L=0, L_1=0, F=0)` |
| Geometry/materials (HTML numerical section) | Layer A AlN: ρ=3.23×10³ kg/m³, c₃₃=3.9×10¹¹ Pa, a_A=0.01 m; Layer B BaTiO₃: ρ′=5.8×10³, c′₃₃=1.62×10¹¹ Pa, a_B=0.01 m; a₃, a′₃ given. ω₀ and k̄=kb/π as (55). **TV2:** confirm `b=a_A+a_B` from PDF body of (51) |
| Reference curve | Fig. 2(a) dispersion/gaps. Digitisation **overlay-only**; error vs **independent TM** + **C¹ bilayer FE**, not vs pixels |
| PDF in `paper9/` | **MISSING** |
| Extra capability | 1-D bilayer TM (classical 2-wave or 4-state reduced) **and** C¹ Bloch-FE bilayer. Case-H 2-D homogeneous **not** a substitute |

**B1 status: OPEN / STOPPED pending PDF.** HTML metadata is not the archival source.

---

## B2 — Layer 2a gradient, flexoelectric off (GATE ≤ 2%)

Same paper/DOI as B1. Required **Fig. 2(b)**.

| Field | Content |
|---|---|
| Caption (HTML) | `(l=10^{-5}, l_1=2×10^{-5}, f=0, L=5, L_1=5, F=0)` — **unbarred** `l`, `l_1` |
| Plan/blueprint lock | `l̄=1e-5`, `ℓ̄_i=2e-5`, `f=0` |
| Conflict | Caption vs `l̄=l/b`. With `b=0.02` m, `l=10^{-5}` m ⇒ `l̄=5×10^{-4}`, **not** 1e-5. **Must be read from PDF**, not assumed |
| Eqs | (24)–(32), (35)–(41), (48)–(53) with `f=0`; four interface quantities `{u_z, u_{z,z}, P_z, R_z}` |
| PDF | **MISSING** (same file as B1) |
| Capability | gradient 4×4 TM + C¹ bilayer FE with strain-gradient + micro-inertia; flexoelectric **off**. Not Case-H |

**B2 status: OPEN / STOPPED pending the same PDF.** Do not treat plan `l̄=1e-5` as verified.

---

## B3 — Layer 2b Li–Askes–Gitman–Krynkin–Wei 2023 (GATE ≤ 2%)

**Not LWZ2016. Not Pb/brass as an LWZ dataset.**

| Field | Content |
|---|---|
| Paper | Li, Y.Q.; Askes, H.; Gitman, I.M.; Krynkin, A.; Wei, P.J. (2023). Band gaps of thermoelastic waves in 1D phononic crystal with fractional order generalized thermoelasticity and dipolar gradient elasticity. *Waves in Random and Complex Media* **36**(4):5715–5735 (plan pagination; White Rose: online 9 Jun 2023) |
| DOI | **10.1080/17455030.2023.2222189** |
| Required (gate) | **Fig. 4(c)** “dipolar gradient elastic, thermoelastic coupling ignored” |
| Optional B4 | **Fig. 3** first two cases (classical / gradient); TV8 |
| Plan params (not TV-closed) | a₁=1e-5 m, a₂/a₁=1, ρ₁=7.5e3, μ₁=2.3e10, ω₀=4.1e8 Hz; k̄=k·a₁/π; λ_R=0.047, μ_R=0.056, ρ_R=0.157 (Pb/brass **this paper**, not LWZ) |
| TV1 | `c̄₁, c̄_R, d₁, d̄_R` **for Fig. 4(c)** from original |
| TV12 | overlay axis ranges |
| PDF in `paper9/` | **MISSING** |
| Capability | isothermal dipolar-gradient 1-D TM (4 ICs) + C¹ bilayer FE |

**B3 status: OPEN / STOPPED pending PDF.** TV1/TV8 remain OPEN.

---

## B6 — LWZ2016 1-D PC (analytic Layer 3b; not Case-H)

| Field | Content |
|---|---|
| PDF | **PRESENT** `paper9/analytic/lwz2016/li2015.pdf` sha256 `88115557…` DOI 10.1007/s00707-015-1495-z |
| Equations | (3)–(10) constitutive/EOM; (14.1)(20.*) homogeneous; (23)(28) 4-state SH; (34) 8-state in-plane; TM (25)–(26); Bloch (32)(39)(40); App. 1–3 T entries; Fig. 3 params PDF p.10 |
| Missing | Independent TM **code**; C¹ **bilayer** FE; published-curve comparison not required for B6 (analytic), but TM vs FE is |

**Do not re-request this PDF.**

### Implementation-gap specification (do not build in this task)

| Item | Requirement (from LWZ PDF) |
|---|---|
| Unknowns | Anti-plane: `V=[u_z, u_{z,x}, P_z, R_z]^T` (23). In-plane: 8-vector (34) |
| Weak form | Dipolar gradient: W (3), T (5); EOM (8)/(10); **not** implemented in Case-H bilayer |
| Interface | Perfect: `V` continuous (28); four (SH) or eight (in-plane) conditions |
| Bloch | `V_B^R = e^{i k_x a} V_A^L` (30); `det(T_B T_A − I e^{i k_x a})=0` (32)(39)(40) |
| Materials | Two isotropic gradient solids; numerical example PDF p.10 (`V_p1/V_s1=2.6621`, … `c̄1=0.5`, `d̄1=0.5`, `c̄=0.77`, `d̄=2`) — **not** Pb/brass |
| Reference | Independent TM from App. 3 (normal) / App. 1–2 (oblique) |
| FE | C¹ elements, same 4/8 traces, Bloch on **laminated** cell — **absent**. 1-cell homogeneous Case-H **invalid** |
| Outputs | ω(k) branches, gap edges; compare TM vs FE ≤2% if used as numerical gate |

**B6 status: source CLOSED; implementation OPEN / STOPPED.** Await a separate implementation task.

---

## Existing solver capability (no code change)

| Capability | Present? |
|---|---|
| 2-D homogeneous Case-H BFS + Bloch T(k), 8 reduced DOF | Yes (P4A 34/34) |
| 1-D laminated bilayer mesh | **No** |
| Independent TM | **No** (`bench/reference_tm/` empty) |
| Four interface conditions in FE | **No** (periodic Case-H only) |
| Flexoelectric Li 2024 | **No** |
| Thermoelastic 2023 | **No** |

P4A Case-H solver **not modified**.

---

## PCR / G3

PCR1 **NOT PASS**. PCR2 **NOT PASS**. PCR3 **PASS** (unchanged). G3 **NOT MET**.
