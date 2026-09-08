# GK Identifiability Program

Reproducible implementation of

    <package>/manuscript/GK_COMPLETE_CALCULATIONS.tex

That document is the **single source of truth**. Every equation, parameter,
boundary condition, tolerance and acceptance value in this program is taken
from it, and each module names the equation labels it implements. No physics or
equation was invented in code.


---

## Data location

The scientific input data (the digitised published curves and the source raster
used to re-digitise Fig. 2) live in the central package tree, **not** inside this
program folder:

    <package>/data/input/digitised.npy          anchor curves (fig3, fig5)
    <package>/data/input/fig2_digitised_despeckled.npy
    <package>/data/input/gate4_fig2.npy
    <package>/data/input/gate4_fig2_corrected.npy
    <package>/data/input/p10_fig2.png           source raster for Fig. 2

`src/io.py` and `src/validation.py` resolve these position-independently
(`PROJECT/data/input`), so the program runs from any location you unpack it to.
The program writes its own outputs to `results/`, `acceptance/` and `figures/`
within this folder.

---

## 1. What this implements

| Area | Source section | Module |
|---|---|---|
| Parameters, `B`, reparameterisation | 1, 4, 6 | `src/model.py` |
| Propagation factor `m^2(s)`, kernel, pulse, sensitivities | 5, 11, 21 | `src/laplace.py` |
| Primary forward solver (Talbot + convolution) | 5, 21, 23 | `src/forward.py` |
| Independent cross-check solver (finite difference) | 23 | `src/fd_solver.py` |
| Deliberately defective split solver (test T16 only) | 21 | `src/split_solver.py` |
| Limits and truncated series | 7, 20.3 | `src/limits.py` |
| Fisher, bands, profile, BIC, estimation | 11, 13-16 | `src/statistics.py` |
| Landscape, Monte Carlo, BIC, profile drivers | 13-16 | `src/analysis.py` |
| Published calibrations | 17-19 | `src/calibration.py` |
| Anchor reproduction | 20 | `src/validation.py` |
| SymPy cross-check of the coded formulas | 24 | `src/symbolic.py` |

**Excluded permanently** (section 1.1 of the master): thermoelasticity,
piezoelectricity, two-temperature theory, fractional derivatives,
memory-dependent derivatives, Rabotnov kernels, porosity as a mechanism,
semiconductor coupling, Klein-Gordon terms, nonlocal elasticity, MGT.

---

## 2. Installation

Python 3.10 or newer.

```bash
pip install numpy scipy sympy matplotlib pytest
```

Optional, only to regenerate the Fig. 2 digitisation from the source image:

```bash
pip install pillow
```

No other dependency. No network access is required to run anything.

---

## 3. Quick start

Generic Python (Linux, macOS, Windows), from the package root:

```bash
cd code/main
python3 scripts/run_all.py
```

Windows PowerShell:

```powershell
cd code/main
python .\scripts\run_all.py
```

`run_all.py` executes, in order: symbolic checks, unit tests, acceptance tests
T1-T24, the full analysis, and figure generation. Expect roughly 15-25 minutes
on two cores; most of it is Monte Carlo and BIC.

### Fast smoke run (skips Monte Carlo and BIC, about 4 minutes)

```bash
GK_FAST=1 python scripts/run_all.py
```

```powershell
$env:GK_FAST=1; python .\scripts\run_all.py; Remove-Item Env:\GK_FAST
```

---

## 4. Running the parts separately

| Purpose | Command |
|---|---|
| Symbolic cross-check | `python -c "from src.symbolic import run_all; [print(r) for r in run_all()]"` |
| Unit tests | `python -m pytest tests/ -v` |
| Acceptance tests T1-T24 | `python scripts/run_acceptance.py` |
| Validation only (anchor) | `python scripts/run_validation.py` |
| Identifiability, MC, BIC, calibration | `python scripts/run_analysis.py` |
| All figures | `python scripts/generate_figures.py` |
| Rebuild Fig. 2 digitisation | `python scripts/regenerate_fig2_digitisation.py` |

PowerShell uses the same commands with `\` separators.

---

## 5. Custom random seed

Stochastic steps (Monte Carlo, BIC, profile noise) are seeded from
`config/default_parameters.json`:

```json
"mc_seed_base": 7000,
"bic_seed_base": 900
```

Change those values, or override on the command line:

```bash
python scripts/run_analysis.py --mc-seed 12345 --bic-seed 999
```

```powershell
python .\scripts\run_analysis.py --mc-seed 12345 --bic-seed 999
```

With the shipped seeds the results are bit-for-bit reproducible on reruns.
Changing the seed changes Monte Carlo digits slightly; it must not change any
conclusion, and the acceptance tolerances are set accordingly.

---

## 6. Expected outputs

```
results/all_tests.json            every acceptance test with provenance
results/all_tests.csv             same, tabular
results/validation_results.json   anchor NRMSE, sigma_d, residual statistics
results/identifiability_results.csv   Fisher landscape vs B
results/band_results.json         recomputed band edges
results/profile_results.json      profile likelihood curves
results/monte_carlo_results.csv   MC recovery vs Fisher
results/bic_results.csv           model selection
results/calibration_results.csv   twelve cases with LIT/DER provenance
results/calibration_summary.json  aggregate, discrepancy table
acceptance/T*.json                one file per test
figures/F1..F7 .pdf + .csv        figures and their plotted data
figures/figure_metadata.json
```

### Headline values the run should reproduce

| Quantity | Expected |
|---|---|
| Anchor Fig. 3 / Fig. 5 / Fig. 2 NRMSE | 0.384% / 0.382% / 0.483% |
| Spread on the resonance ray (double precision) | <= 1e-9 |
| Control spread at `B=1.05` | ~2.6e-2 |
| Fisher s.e.(tau_q) at `B=0.5` / `B=1.28` | 12.37% / 45.64% |
| Band edges at the 20% criterion | 0.628 and 1.804 |
| BIC at `B=1` | Fourier selected, GK delta ~6.6 |
| Calibration aggregate | 8 of 12 inside the band |
| `B` for Both et al. | 1.532 +/- 0.043 |

These are **acceptance targets recomputed by the program**, not constants
stored in it.

---

## 7. Two hard rules enforced in code

1. **The Talbot node count `M` must be odd.** An even `M` puts a quadrature
   node on the imaginary axis, which collides with the removable pulse pole at
   `t* = M*tau_Delta/10` (eq:tstar). `src/forward.py` warns on even `M`.
2. **The split / second-shift pulse formulation is prohibited** in the
   scientific pipeline. It exists only in `src/split_solver.py` so that test
   T16 can demonstrate the failure it causes.

---

## 8. Interpreting the validation

- Agreement with the published anchor figures is **external validation of the
  forward operator**.
- Agreement between `src/forward.py` and `src/fd_solver.py` is **numerical
  cross-checking**, not external validation.
- **No experimental validation of the inverse conclusions is claimed.**
- The band `[0.628, 1.804]` is **configuration dependent**, valid for the
  reference configuration in `config/default_parameters.json`. Change `n`,
  `eta_noise`, `t_min`, `t_max` or `tau_Delta` and it moves. Only the
  singularity at `B=1` is universal, because it is structural.

---

## 9. Known behaviour worth understanding before you run it

**Profile likelihood at `B = 0.9` is sensitive to the noise draw.** With the
shipped seed the 95% interval collapses to the low-`tau_q` edge of the grid,
because for that particular realisation the profiled SSE at small `tau_q`
falls slightly below the SSE at the true value. This is genuine flat-valley
behaviour near the degeneracy, not a solver failure: the objective really is
almost flat there, so a single realisation can place the minimum far from the
truth. The two profile acceptance tests that the master specifies (T13 at
`B=1.28`, T14 at `B=1`) are stable and both pass. Treat single-realisation
profile intervals at `B` near 1 as indicative only; use several seeds if you
need a stable interval in that region.

**Runtime.** The profile uses five optimiser starts per grid node (needed near
resonance, where a start anchored at the true `kappa2` is a poor guess once
`tau_q` moves), so `run_analysis.py` and `generate_figures.py` are the slow
steps. Budget 15-25 minutes for the whole pipeline on two cores.
