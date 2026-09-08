Figure-data CSVs (read-only inputs to the MATLAB plotting package)

These 14 CSV files are the "verified Phase-5" figure data read by the 11
manuscript figures (code/plotting/matlab/*.m). They are treated as an
authoritative, read-only reference dataset:

  F1_degeneracy.csv             resolved/control degeneracy on the resonance ray
  F2_anchor_reproduction.csv    anchor reproduction (reference cases 1 & 2)
  F3_talbot_pole.csv            Laplace-inversion / Talbot pole certification
  F5_profile_likelihood.csv     profile-likelihood response surface
  F6_bic.csv                    Bayesian model comparison
  F7_calibrations.csv           audited published calibrations
  anchor_metrics.csv            anchor reproduction metrics
  bands.csv                     >10/20/50/100% band criteria
  calibration_results.csv       calibration aggregate
  fd_convergence_windows5.csv   Windows 5-point convergence ladder
  identifiability_results.csv   Fisher landscape vs B
  monte_carlo_results.csv       Monte-Carlo recovery vs Fisher
  series_convergence.csv        truncated-series convergence
  talbot_parity.csv             Talbot parity record

`gk_paths.m` resolves these from <package>/data/results, position-independently.
