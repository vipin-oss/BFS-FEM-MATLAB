# Evidence identification note — fig4c_raw.png is Li et al. (2023) FIGURE 7, not Fig. 4(c)

**Date:** 2026-09-23 (P12A)
**Status:** identification correction; the raster is retained as historical evidence.

`fig4c_raw.png` (three panels annotated tau_R = 1, 0.1, 0.05) was archived in P11 as
"Li et al. (2023) Fig. 4(c) raw raster".  P12A byte-level comparison against the
images embedded in `paper9/sources/Band-gaps-of-thermoelastic-waves-in-1D-phononic-crystal-with-fractional-order-generalized (1).pdf`
(PyMuPDF extraction) shows it is **pixel-identical (mean |diff| = 0.0000) to the
embedded image on printed page 16 that the PDF's own caption block identifies as
Figure 7**: "The influence of thermal relaxation time ratio tau_R on the dispersion
curves and the band gaps ... in the case of gradient **thermo-elastic** model
(c_bar_1 = 0.15, c_R = 1.5, d_bar_1 = 0.25, d_R = 1.5, alpha_R = 1, tau_bar_2 = 0.15)".

The genuine **Figure 4** is the embedded 1500×437 image on printed page 15, in-repo
as `li2023_p15_img1_Im1.png`: panels (a)/(b) classical elasticity vs Zheng & Wei [59]
and Li & Wei [34]; panel (c) **"Gradient elasticity"** (present vs Li and Wei [34]),
omega_bar in [0, 2], k_bar in [-1, 1], **no tau_R sweep and no c_bar/d_bar annotation**.

Consequences: B3 qualitative comparisons must use the genuine Fig. 4 raster; the
tau_R-sweep figure is a gradient *thermo-elastic* figure outside the isothermal B3
model scope.  TV1's [S] provenance verdict is unaffected (Fig. 4(c) annotates no
c_bar/d_bar; values inherited from Fig. 3(b)).  See `paper9/audit/P3_TV_RESOLUTION.md`
(P12A addendum) and `paper9/audit/P12A_CLOSEOUT.md`.
