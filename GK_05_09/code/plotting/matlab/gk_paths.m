function P = gk_paths()
%GK_PATHS Project-relative paths for the authoritative MATLAB figure package.
%   No absolute or personal paths are used anywhere. The project root is
%   resolved from this file's own location, so every script runs unchanged
%   from the project root, from figures/matlab, or from any other folder.
%
%   P.data  verified Phase-5 CSV inputs   (READ ONLY - never written to)
%   P.out   figure outputs (PDF/EPS/PNG)

here        = fileparts(mfilename('fullpath'));   % .../code/plotting/matlab
P.matlab    = here;
P.plotting  = fileparts(here);                    % .../code/plotting
P.code      = fileparts(P.plotting);              % .../code
P.root      = fileparts(P.code);                  % package root
P.data      = fullfile(P.root, 'data', 'results');  % verified figure-data CSVs (read-only)
P.out       = fullfile(here, 'output');           % required by Phase 7A

if ~exist(P.out, 'dir')
    mkdir(P.out);
end

if ~exist(P.data, 'dir')
    error('gk_paths:noData', ...
        ['Verified data folder not found:\n  %s\n' ...
         'Run the scripts with the repository intact.'], P.data);
end
end
