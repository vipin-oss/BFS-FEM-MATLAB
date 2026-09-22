# P3 source extraction — Li 2024 & Li 2023 PDFs

**Date:** 2026-09-22  
**Rule:** values only from these PDFs. No HTML. No Case-H substitution. No PCR1/G3.

## Files located

PDFs were on GitHub **`main`** (commit `93c10ff3`, “Add files via upload”), **not** on `phase-1-symbolic`. Copied into `paper9/` for this branch.

| Paper | Repo path (this branch, after copy) | Origin on `main` | Size (bytes) | Pages | Opens |
|---|---|---|---|---|---|
| Li et al. 2024 Sci Rep | `paper9/analytic/li2024/s41598-024-75049-1.pdf` | `Band-gaps-of-elastic-waves-in-1-D-dielectric-phononic-crystal-with-the-flexoelectric-and.pdf` | 2854249 | 14 | yes |
| Li et al. 2023 WRAM | `paper9/analytic/li2023/17455030.2023.2222189.pdf` | `Band-gaps-of-thermoelastic-waves-in-1D-phononic-crystal-with-fractional-order-generalized.pdf` | 2568304 | 22 | yes |

**2024 identity [C]:** Ying Li, Yueqiu Li, Zihao Guo, Hong Wang, Changda Wang. *Sci. Rep.* **14**:24035 (2024). PDF `/doi` **10.1038/s41598-024-75049-1**. Footer matches.

**2023 identity [C]:** Yueqiu Li, Harm Askes, Inna M. Gitman, Anton Krynkin, Peijun Wei. *Waves Random Complex Media* **36**(4):5715–5735. DOI **10.1080/17455030.2023.2222189**. Published online 9 Jun 2023. **Not** LWZ2016.

---

## B1 / B2 — Li 2024 (same PDF)

### Equations [C]

| Eq | PDF p. (article p.) | Content |
|---|---|---|
| (24) | p.4 / 4 | reduced EOM in `uz`; classical when `l=l1=f=0` (explicit sentence) |
| (27)–(31) | p.5 / 5 | quartic in k; (30)(31) omit flexoelectricity |
| (32) | p.5 | 4-wave superposition |
| (35)–(41) | p.5–6 | σ, μ, P, R traces |
| (48) | p.7 | `Tj = P0 G(aj) P0^{-1}` |
| (51) | p.7 | `V_B^R = e^{i k b} V_A^L` with **`b = a_A + a_B`** |
| (52)(53) | p.7 | `det(T_B T_A − e^{ikb} I)=0` |
| (55) | p.7 | nondim: `l̄=l/b`, `l̄1=l1/b`, `k̄=kb/π`, `ω̄=ω/ω0` |

**TV2: CLOSED [C].** Eq. (51): `b` **is** the single-cell thickness `a_A+a_B`.

### Materials / geometry [C] PDF p.7–8 / 7–8

| symbol | value | unit | where |
|---|---|---|---|
| ρ (AlN, A) | 3.23×10³ | kg/m³ | p.7 |
| a3 (A) | 8.4×10⁻¹¹ | C²/N m² | p.7 |
| c33 (A) | 3.9×10¹¹ | Pa | p.7 |
| a_A | 0.01 | m | p.7 |
| a_B | 0.01 | m | p.7 |
| ρ′ (BaTiO3, B) | 5.8×10³ | kg/m³ | p.8 |
| a3′ | 1.26×10⁻⁸ | C²/N m² | p.8 |
| c33′ | 1.62×10¹¹ | Pa | p.8 |
| ω0 | 2π / (a_A/√(c33/ρ)+a_B/√(c′33/ρ′)) | 1/s | p.7, stated |
| b | a_A+a_B = 0.02 m | m | **derived** from (51)+a_A,a_B |

### Fig. 2 caption [C] PDF p.9 / 9

**(a) Classical:** `(l=0, l1=0, f=0, L=0, L1=0, F=0)`  
**(b) Gradient:** `(l=10^{-5}, l1=2×10^{-5}, f=0, L=5, L1=5, F=0)`  
**(c)** not a P3 gate.

`L=l′/l`, `L1=l1′/l1`, `F=f′/f` defined p.7.

### `l=10^{-5}` interpretation — **OPEN (not silently reconciled)**

PDF defines `l̄ = l/b` (p.7) and the **caption writes unbarred `l`**. It does **not** say `l̄=10^{-5}`.

| If caption `l` is | then `l̄=l/b` with b=0.02 m |
|---|---|
| dimensional metres | 5×10⁻⁴ |
| already `l̄` (notation slip) | 10⁻⁵ |

Plan/blueprint `l̄=1e-5` is **not** PDF-verified. **Do not use it as [C].**

### B1/B2 implementation

**SOURCE VERIFIED — VALIDATION IMPLEMENTATION BLOCKED.**  
Need independent 1-D TM (53) + laminated C¹ FE. Current solver = homogeneous 2-D Case-H only. **B1, B2 remain OPEN.** No numerical PASS.

---

## B3 — Li 2023 WRAM

### Fig. 4(c) [C] PDF p.15 / journal 5728

Caption: comparison of gradient-elastic solids with literature **[34]** = Li & Wei, *Acta Mech.* 2016;227:1005–1023 (**LWZ2016**). Thermoelastic coupling ignored in the *present* model for that panel.

**No `c̄1,d̄` values in the Fig. 4 caption.** TV1 for **Fig. 4(c)** remains **OPEN**.

Do **not** copy LWZ Fig. 3 numbers (`c̄1=0.5`…) into Fig. 4(c) without the 2023 PDF saying so.

### Fig. 3 [C] optional B4 / TV8 — PDF p.15 / 5728

Vertical propagation:

- (a) classical: `c̄1=c̄2=d̄1=d̄2=τ̄1=τ̄2=α1=α2=0`
- (b) gradient: `c̄1=0.15, c_R=1.5, d̄1=0.25, d_R=1.5, τ̄1=τ̄2=α1=α2=0`
- (c) thermal+gradient: same c,d plus `τ_R=1, α_R=1`

TV8 **CLOSED for Fig. 3 panels** as above. That does **not** close TV1 for Fig. 4(c).

### Shared numerical constants [C] PDF p.14 / 5727

| symbol | value | unit | tag |
|---|---|---|---|
| material A | lead | — | [C] |
| material B | brass | — | [C] |
| a1 | 10⁻⁵ | m | [C] |
| a_R=a2/a1 | 1 | — | [C] |
| ρ1 | 7.5×10³ | kg/m³ | [C] |
| μ1 | 2.3×10¹⁰ | Pa | [C] |
| T01 | 300 | K | [C] |
| ω0 | 4.1×10⁸ | Hz | [C] stated (also formula p.14) |
| λ̄1 | 0.928 | — | [C] |
| μ̄1 | 0.182 | — | [C] |
| λ_R | 0.047 | — | [C] |
| μ_R | 0.056 | — | [C] |
| ρ_R | 0.157 | — | [C] |
| k̄ | k a1 / π | — | [C] |

**TV12:** axis ranges for Fig. 4 **not** printed as numbers. **OPEN**.

### B3 implementation

**SOURCE PARTIALLY VERIFIED — VALIDATION IMPLEMENTATION BLOCKED.**  
Fig. 4(c) parameters (TV1) missing from caption. No bilayer TM/FE. Not Case-H. **B3 OPEN.**

---

## B6

LWZ2016 PDF already in `paper9/analytic/lwz2016/li2015.pdf`. Implementation still blocked (no TM, no laminated C¹ FE). Unchanged.

---

## TV register (this extraction)

| ID | Was | Now |
|---|---|---|
| TV2 | assumed b=a_A+a_B | **CLOSED [C]** Li 2024 (51) |
| TV1 | Fig 4(c) c̄,d̄ | **OPEN** — not in 2023 Fig. 4 caption |
| TV8 | Fig 3 panels | **CLOSED [C]** Fig. 3 caption values |
| TV12 | overlay axes | **OPEN** |
| TV10/TV11 | closed | **not modified** |

PCR1/G3 **not** claimed. P4A solver **not** modified.

**Resolution pass:** see `audit/P3_TV_RESOLUTION.md`. B2 `l` vs `l̄` still OPEN. TV1/TV12 still OPEN. TV2/TV8 unchanged.
