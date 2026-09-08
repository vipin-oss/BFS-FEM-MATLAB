% RUN_ALL_FIGURES  Generate the complete authoritative MATLAB figure set.
%
% Usage, from anywhere:
%     >> run <path-to>/figures/matlab/run_all_figures.m
% or, from figures/matlab:
%     >> run_all_figures
%
% Outputs go to figures/matlab/output/ as PDF (vector), EPS (vector) and
% 600 dpi PNG previews.
%
% EVERY NUMBER PLOTTED COMES FROM A VERIFIED PHASE-5 CSV IN figures/data/.
% No script computes, fits, smooths or invents a scientific value.
%
% IMPLEMENTATION NOTE. Each figure script begins with its own `clear`, which
% would wipe this runner's loop variables if the scripts were executed in
% this workspace. The build loop is therefore delegated to gk_build(), a
% FUNCTION, whose workspace the scripts cannot touch.

clear; close all;
addpath(fileparts(mfilename('fullpath')));
gk_build();
