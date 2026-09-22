# P2 source-to-model mapping (PDF-verified)

**Date:** 2026-09-22. PDFs: PB2009 sha256 `8ca9c820…`, LWZ2016 sha256 `88115557…`.

| Source | Source model | Source eq. (PDF / journal) | Source parameters | Our quantities | Specialisation required | Grade | Validation role |
|---|---|---|---|---|---|---|---|
| PB2009 | infinite isotropic gradient solid, EOM (14) | (20)–(22) p.3 / 3753 | `g²` micro-elastic, `h²` micro-inertia; `g≤h` ⇒ `V≤C` | Case-H M10.2 | isotropic `L=l²I` **and** identify `g²:=l²/10`, `h²:=ℓ²` | form **[C]**; map **[B]** | Layer 3 vs (22) **after** that ID |
| PB2009 | axial bar | (25)–(28) p.5 / 3755 | same `g,h`; `E` Young | 1-D reduction of Case-H | same ID; bar uses `E` not `μ` or `λ+2μ` | **[C]** bar; **[B]** vs 3-D L/T | Layer 3 annex (bar), not 2-D bands |
| — | proposed `g² = l²/10` | never in PB | — | M4 factor `1/10` **[A]** | define, do not derive from (12) | **[B]** not **[C]** | allowed only as ID |
| — | proposed `h² = ℓ²` | (14) coeff. of `∇²ü` | `h²` | M5/M8 `ℓ²` | EOM-slot match | **[B]** strong | same |
| PB2009 | anisotropic `L(θ)` | absent | — | `l1,l2,θ` **[A]** | none | **not transferable** | internal Case-H only |
| LWZ2016 | one isotropic gradient solid | (14.1),(20.1–2) PDF pp.4–5 | `c`, `d` with inertia `d²/3` | Case-H isotropic | `c:=l²/10`, `d²/3:=ℓ²` | **[B]** | not B6; optional vs PB |
| LWZ2016 | 1-D laminated PC, TM+Bloch | (32),(39),(40) PDF pp.7–9 | `c_i,d_i,a_i,V_{p,s i},ρ_i`; Fig.3 set PDF p.10 | future 1-D Case-C | bilayer + 4/8 interface DOF | **[C]** | Layer 3b (P3 B6), **not** Case-H |
| Our Case-H | homogeneous anisotropic Form-II | M10.2 **[A]** | `λ,μ,ρ,L,ℓ` | — | — | **[A]** | solver; Layer 3 only after **[B]** ID |

Do not claim equivalence from visual similarity. `1/10` and `d²/3` are different constitutive reductions.
