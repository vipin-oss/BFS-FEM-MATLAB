% FIG02  External validation, anchor 1 (resonance case).
%
% TYPE      : 4-panel reproduction (scatter + line + overlay + residual band)
% PANELS    : (a) published reference   (b) independent reproduction
%             (c) overlay               (d) residual vs +/-2 sigma_d
% DATA      : F2_anchor_reproduction.csv (tag 'fig3'), anchor_metrics.csv
% VERIFIED  : NRMSE = 0.38390241640748424 %, RMSE = 3.842944664757361e-03,
%             n = 729, sigma_d = 0.00593382511692216, 99.86 % within 2 sigma_d
% SUPPORTS  : external validation of the FORWARD OPERATOR only.
%             Not inverse validation. Not experimental validation.
%
% The reference case is one of three reference figures taken from a single
% published study; the wording used throughout is "reference case/figure",
% never "independent publication".

clear; close all;
here = fileparts(mfilename('fullpath')); addpath(here);

gk_anchor_figure('fig3', ...
    'reference case 1 (resonance)', ...
    'fig02_anchor_resonance');
