Scientific input data (read-only)

Digitised published curves (from the anchor figures of Kovacs, Int. J. Heat
Mass Transf. 127A (2018) 631-636) used to validate the forward operator:

  digitised.npy                 anchor curves fig3 and fig5 (noise floor sigma_d)
  fig2_digitised_despeckled.npy despeckled Fig. 2 digitisation
  gate4_fig2.npy                independent digitisation pass (Gate 4)
  gate4_fig2_corrected.npy      corrected Gate-4 Fig. 2 data
  p10_fig2.png                  source raster used to (re)digitise Fig. 2

These are INPUT DATA, not program output. They are read by
code/main/src/validation.py (resolved from <package>/data/input) and, for the
optional Fig. 2 re-digitisation, by scripts/regenerate_fig2_digitisation.py.
