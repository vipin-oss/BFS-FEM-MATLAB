# P2 source-to-model mapping (acquisition pass)

**Date:** 2026-09-22. Equation bodies of PB2009 and LWZ2016 **not** in hand. Nothing here is a closed identification.

| Source | Source model | Source equation(s) | Source parameters | Our quantities | Required specialisation | Grade | Validation role |
|---|---|---|---|---|---|---|---|
| PB2009 intended paper 46:3751–3759 | infinite space + bar + beam + plate, simple gradient elasticity (abstract **[C]**) | (22)–(28) **not transcribed** | `g²`, `h²` mentioned in prior HTML snippets; **definitions not [C] from PDF** | Case-H `L`, `l1`,`l2`,`θ`, `ℓ` | isotropic `L=l² I` would be needed even to *compare* | analogous / **[B] candidate** only | Layer 3 **blocked** until TV10 closed |
| Proposed `g² ↔ l²/10` | — | — | — | `l²/10` from M4 Form-II factor **[A]** | would require PB constitutive = our Form-II isotropic reduction | **not source-supported** | do not use numerically |
| Proposed `h² ↔ ℓ²` | — | — | — | micro-inertia `ℓ` **[A]** M5 | would require their kinetic-energy operator | **not source-supported** | do not use numerically |
| Anisotropic `L(θ)` | not in PB2009 abstract | — | — | `l1≠l2`, `θ` **[A]** | none | **not transferable** to PB2009 | internal Case-H only |
| LWZ2016 227:1005–1023 | 1-D laminated **PC**, dipolar gradient, TM+Bloch (abstract **[C]**) | TM/Bloch **not transcribed** | `c1`,`d1` and ratios (plan language; **not [C] from PDF**) | not Case-H | 1-D Case-C bilayer **if** equations match M8 interface set | **not transferable** to 2-D Case-H; **[B]** to future 1-D Case-C pending PDF | Layer 3b **blocked** until TV11 closed |
| Our Case-H M10.2 | homogeneous infinite medium, Form-II + micro-inertia, anisotropic `L` | `ω_{L,T}² = c_{L,T}² \|k\|² (1+k·L·k/10)/(1+ℓ²\|k\|²)` | `λ,μ,ρ,L,ℓ` | — | — | **[A]** | internal / solver, **not** published Layer 3 |

Equivalence is **not** claimed because formulas “look similar.”
