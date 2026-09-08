% FIG03  External validation, anchor 2 (over-diffusive case).
%
% TYPE      : 4-panel reproduction (scatter + line + overlay + residual band)
% PANELS    : (a) published reference   (b) independent reproduction
%             (c) overlay               (d) residual vs +/-2 sigma_d
% DATA      : F2_anchor_reproduction.csv (tag 'fig5'), anchor_metrics.csv
% VERIFIED  : NRMSE = 0.3817215373831442 %, RMSE = 2.8804077890293733e-03,
%             n = 743, sigma_d = 0.006027123741366962, 99.46 % within 2 sigma_d
% SUPPORTS  : shows the agreement of fig02 is not case-specific, because a
%             dynamically different regime is reproduced by the SAME
%             unmodified solver with published parameters and no fitting.
%
% External validation of the FORWARD OPERATOR only.

clear; close all;
here = fileparts(mfilename('fullpath')); addpath(here);

gk_anchor_figure('fig5', ...
    'reference case 2 (over-diffusive)', ...
    'fig03_anchor_overdiffusive');
