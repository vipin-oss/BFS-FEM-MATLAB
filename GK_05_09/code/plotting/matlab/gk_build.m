function results = gk_build(varargin)
%GK_BUILD Build the manuscript figure set and report the outcome.
%   results = GK_BUILD()          build every figure
%   results = GK_BUILD('fig06')   build a subset by name fragment
%
%   Runs as a FUNCTION so that the `clear` statement at the top of each
%   figure script cannot destroy the loop state.

here = fileparts(mfilename('fullpath'));
addpath(here);
P = gk_paths();

scripts = { ...
    'fig01_geometry', ...
    'fig02_anchor_resonance', ...
    'fig03_anchor_overdiffusive', ...
    'fig04_convergence_certification', ...
    'fig05_parameter_study', ...
    'fig06_profile_surface_3d', ...
    'fig07_identifiability', ...
    'fig08_parameter_map', ...
    'fig09_model_comparison', ...
    'fig10_calibrations', ...
    'fig11_talbot_certification' };

if nargin > 0 && ~isempty(varargin{1})
    keep = false(size(scripts));
    for k = 1:numel(scripts)
        keep(k) = ~isempty(strfind(scripts{k}, varargin{1}));
    end
    scripts = scripts(keep);
end

fprintf('\n');
fprintf('=========================================================\n');
fprintf('  GK manuscript figures - authoritative MATLAB build\n');
fprintf('=========================================================\n');
fprintf('  data   : %s\n', P.data);
fprintf('  output : %s\n', P.out);
fprintf('  count  : %d\n', numel(scripts));
fprintf('---------------------------------------------------------\n');

nok = 0;
failed = {};
t0 = tic;

for k = 1:numel(scripts)
    name = scripts{k};
    fprintf('[%2d/%2d] %s\n', k, numel(scripts), name);
    try
        evalin('base', sprintf('run(''%s'');', fullfile(here, [name '.m'])));
        nok = nok + 1;
    catch err
        fprintf('        FAILED: %s\n', err.message);
        if ~isempty(err.stack)
            fprintf('        at %s line %d\n', err.stack(1).name, err.stack(1).line);
        end
        failed{end+1} = name; %#ok<AGROW>
    end
    close all;
end

el = toc(t0);
fprintf('---------------------------------------------------------\n');
fprintf('  generated %d of %d in %.1f s\n', nok, numel(scripts), el);
if isempty(failed)
    fprintf('  ALL FIGURES GENERATED\n');
else
    fprintf('  FAILED: %s\n', strjoin(failed, ', '));
end
fprintf('=========================================================\n\n');

results = struct('total', numel(scripts), 'ok', nok, 'failed', {failed}, ...
                 'elapsed_s', el, 'output_dir', P.out);
end
