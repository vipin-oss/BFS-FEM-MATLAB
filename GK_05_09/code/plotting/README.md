# GK Manuscript — MATLAB R2020 Figure Package

Self-contained package to generate all 11 manuscript figures, specifically
audited for **MATLAB R2020** compatibility. This package has been checked
by **static inspection only** — no MATLAB R2020 installation was available
in the preparation environment, so **no runtime execution has been
performed or is claimed**. Running it on your own MATLAB R2020 installation
is the next step.

No scientific data, numerical value, panel structure, or figure design was
changed to build this package. Two categories of *non-scientific* fixes
were made this round (see below): a genuine MATLAB-vs-Octave graphics
handle bug, and a targeted layout fix to Figure 7. Every other file is
byte-for-byte identical to the project source.

## Runtime bug found and fixed: graphics-handle preallocation

A real MATLAB R2020 runtime error was reported from a prior version of this
package:
```
Error using ishold (line 47)
Using hold with double is not supported.
```
**Root cause:** `gk_grid.m` preallocated its axes-handle array with
`ax = zeros(nrow, ncol)` — a plain numeric array. Octave represents graphics
handles as doubles internally, so storing an axes handle into that array and
reading it back worked there. In MATLAB's HG2 graphics system, an axes
handle is a genuine object (`matlab.graphics.axis.Axes`), not a double;
assigning it into a pre-typed double array silently degrades it back to a
plain number on read-back, so every later handle-consuming call
(`ishold(ax)`, `hold(ax,...)`, `plot(ax,...)`, `legend(ax,...)`) fails or
misbehaves. This is a genuine behavioural MATLAB/Octave difference that a
keyword search cannot catch, exactly as reported.

**Fix:** `ax = zeros(nrow, ncol)` → `ax = gobjects(nrow, ncol)`.
`gobjects` preallocates true graphics-object placeholders and has been
available in MATLAB since R2014b (and in Octave), so it is safe for R2020
and does not change any plotted value.

The same anti-pattern was found and fixed in three more places where a
graphics handle (not a number) was being stored into a `zeros(...)` array:
- `fig05_parameter_study.m`: `h1` (line handles for panel (a)'s legend)
- `fig07_identifiability.m`: `hP` (line handles for panel (c)'s legend)
- `fig09_model_comparison.m`: `hb` and `h2` (marker/line handles for panels (a) and (b))

Two other `zeros(...)` calls were inspected and confirmed to be genuinely
numeric (not handles) and were left unchanged: `fig08_parameter_map.m`'s
`xt` (a tick-index array) and `fig10_calibrations.m`'s `cnt` (a count
array).

## Data/script synchronization bug found and fixed: fig08_parameter_map

A second real MATLAB R2020 runtime error was reported after the first round
of fixes:
```
[ 8/11] fig08_parameter_map
        FAILED: Index exceeds the number of array elements (4).
        at fig08_parameter_map line 63
```

**Root cause:** this is not a MATLAB-version issue but a genuine
data/script synchronization gap. `data/bands.csv` (shared with the
manuscript's design table) now has **five** rows (10/20/30/50/100%) because
a 30% design criterion was correctly added to the production pipeline in an
earlier stage of this project. `fig08_parameter_map.m` loops over every row
of `bands.csv` but shades each one using a **hardcoded four-element** array
(`shades = [0.10 0.16 0.24 0.34]`), sized for the original four criteria.
On the fifth loop iteration, `shades(5)` does not exist, producing exactly
the reported error.

**Why the fix keeps four bands, not five:** the manuscript's own caption
for this exact figure states *"...within which s.e.($\tau_q$) exceeds 10,
20, 50 and 100%"* -- four criteria, deliberately excluding 30%. Growing the
figure to five bands would create a new mismatch against its own already-
written caption. The correct fix is therefore to filter to exactly the four
criteria this figure was designed to show, so it continues to match its
caption regardless of how many rows the now-shared `bands.csv` contains for
other purposes (the manuscript's design table).

**Fix applied:** `fig08_parameter_map.m` now explicitly selects the four
rows where `criterion_pct` is 10, 20, 50, or 100 (via `ismember`) before
sorting and shading, with a comment explaining why the 30% row is excluded.
The end-of-script console diagnostic was also updated to report the four
bands actually plotted, rather than all five rows in the underlying file,
so the printed summary matches what the figure shows.

No numerical value in `bands.csv` was changed, and no value used by the
four retained bands was altered -- only which rows this one figure selects
to plot.

## Figure 7 layout fix

Direct visual inspection of the existing rendered `fig07_identifiability.pdf`
(the only figure specifically flagged) confirmed two genuine layout issues,
both now fixed at the code level:

1. **Panel (b)'s combined two-series legend** ("Condition number" /
   "Correlation deficit") was anchored inside the axes at `'southeast'`,
   where it visually competed with the descending tail of the blue
   condition-number curve and the right-hand (orange) axis's tick labels in
   the same corner. **Fix:** moved to `'southoutside'`, using the exact same
   helper call pattern (`gk_legend(...,'southoutside')`) already used
   successfully by panel (c) in the same figure, plus the existing
   `gk_assert_legend_clear` occlusion check (previously only applied to
   panel (c), now also applied to panel (b)).
2. **Insufficient top margin** for the title/panel-label region across the
   whole 2×2 grid. **Fix:** the grid's `'top'` margin for this figure only
   was increased from `0.120` to `0.145`, giving titles and panel labels
   more breathing room without affecting any other figure (this is a
   per-call-site parameter, not a change to the shared `gk_grid.m` default).

Two other multi-panel figures (`fig09_model_comparison.pdf`,
`fig10_calibrations.pdf`) were also visually inspected at print resolution
as a spot check and found already well-typeset, with no comparable issue —
confirming Figure 7 was a genuine, specific outlier rather than a systemic
problem across the set, and that a blanket relayout of all 11 figures was
not warranted.

**Important limitation, stated plainly:** these layout fixes were made by
reading the plotting code and by visually inspecting the *existing*
pre-rendered PDF (produced by a prior Octave run), since neither MATLAB nor
Octave is available in the environment that prepared this package. The
fixed code has **not** been re-rendered or re-verified visually after the
change. Please treat Figure 7's new layout as a well-reasoned, evidence-based
correction that still needs your own visual confirmation once you run it.

## R2020 compatibility audit — keyword-level findings

Beyond the handle-preallocation bug above (found by reading the code's
actual behavior, not by keyword search), the following MATLAB features,
each introduced at or after the R2019b/R2020 boundary, were also searched
for across all 33 `.m` files. None were found in actual code.

| Feature checked | Introduced | Found in code? |
|---|---|---|
| `exportgraphics` | R2020a | No |
| `tiledlayout` / `nexttile` | R2019b | No |
| `turbo` colormap | R2019b | No |
| `colororder` | R2019b | No |
| `arguments` validation blocks | R2019b | No (one comment contains the English word "arguments," not a code block) |
| `string`/`contains`/`erase`/`pattern`/`isstring`/`compose` (string-class methods) | R2016b–R2020a | No |
| `sgtitle` | R2018b | No |
| `categorical`/`datetime`/`split`/`join`/`pad` | various | No |
| `boxchart`/`swarmchart`/`heatmap` | R2019a–R2020a | No |
| `print(...,'-vector')` | **R2022a** | No — `gk_finish.m` explicitly documents avoiding this switch in favor of the `painters` renderer for exactly this reason |
| Named colormap strings (e.g., `'viridis'`) on axes-targeted `colormap(ax,...)` calls | reliability varies by release | No — `gk_cmap.m` explicitly avoids this, passing an explicit Nx3 RGB matrix instead, with its own header comment documenting the exact failure mode this sidesteps |

**Conclusion: no MATLAB R2020 incompatibility was found. No code was
modified, per your instruction to fix only a genuine incompatibility and
nothing else.**

## Terminology check (figure labels/legends)

Re-confirmed by direct search: zero instances of "this work," "published,"
"gate," or "test" used as an actual axis label, legend entry, or title
string anywhere in the 33 files. The only two textual matches are both
inside documentation comments (`gk_anchor_figure.m`, `gk_style.m`) that
explicitly *declare* these informal terms are never used as labels — the
opposite of a violation. Confirmed precise terminology in actual use
includes "Digitised benchmark solution," "Present convolution solution,"
"Finite-difference solution," "Truncated eigenfunction series," "Monte
Carlo estimate," "Fisher-information estimate," and the four named
candidate models ("Fourier model," "MCV model," "Nyíri model," "GK model").

## What this package contains

```
FEM4/code/plotting/
├── README.md                  (this file)
├── matlab/                    (fig01..fig11 scripts + gk_* helpers + run_all_figures.m)
│   ├── fig01_geometry.m ... fig11_talbot_certification.m
│   ├── gk_*.m
│   └── run_all_figures.m      (batch driver — run this)
└── (data/) -> reads ../../data/results/   (the 14 verified figure-data CSVs)
```
`gk_paths.m` resolves the data folder position-independently to
`<package>/data/results`, so the plotting package works from any location.

## How to run it in MATLAB R2020

1. Open MATLAB R2020 (R2020a or R2020b).
2. `cd` into `FEM4/code/plotting/matlab`.
3. At the MATLAB prompt:
   ```
   run_all_figures
   ```

All paths are resolved relative to the script's own location
(`mfilename('fullpath')` in `gk_paths.m`), so this works regardless of
MATLAB's prior working directory — only step 2 matters.

## Expected output

`matlab/output/`, created automatically on first run, will contain 33 files: for each of
the 11 figures, a `.pdf` (vector, via the `painters` renderer — vector
quality is fully supported by R2020's `print` command), a `.eps` (vector,
via `-depsc`), and a `.png` (400 dpi raster preview, high enough resolution
for manuscript-page inspection at print size). `run_all_figures` reports
each figure's success/failure individually and will not halt on one
failure — it continues through all 11 and prints a final summary.

## Preserved figure design

Unchanged from the project source: 11 figures, geometry as Figure 1,
multi-panel construction where scientifically appropriate (3–4 panels per
figure is typical), the existing 3-D profile-likelihood surface
(`fig06_profile_surface_3d.m`, using standard `surf`/`view`, no
version-specific lighting calls), and the full range of plot types already
present (line, bar, scatter, contour, 3-D surface, cumulative-distribution)
communicating distinct aspects of each result.

## What to do next

This package does not touch the manuscript. Once you have run it and are
satisfied with the output, copy the 11 PDFs from `matlab/output/` into the
manuscript's `figures/` folder yourself before recompiling — that step is
deliberately left manual so you can compare your R2020 output against the
existing figures first.
