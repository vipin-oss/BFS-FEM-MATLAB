function cm = gk_cmap(n)
%GK_CMAP Perceptually uniform sequential colormap, available on every MATLAB.
%
%   Requesting the map BY NAME, e.g. colormap(ax,'viridis'), fails on MATLAB
%   releases before R2019b with
%       Error using colormap: Invalid colormap name
%   because 'viridis' is not a built-in name there (it is in Octave). Passing
%   an explicit Nx3 matrix works identically on every version and in Octave,
%   so the colour scale is guaranteed to be the same everywhere.
%
%   The anchors below are the standard viridis control points. Colour choice
%   is presentational only; no scientific value depends on it.
%
%   cm = GK_CMAP()    256 rows
%   cm = GK_CMAP(n)   n rows

if nargin < 1 || isempty(n)
    n = 256;
end

anchors = [ ...
    0.267004 0.004874 0.329415
    0.282623 0.140926 0.457517
    0.253935 0.265254 0.529983
    0.206756 0.371758 0.553117
    0.163625 0.471133 0.558148
    0.127568 0.566949 0.550556
    0.134692 0.658636 0.517649
    0.266941 0.748751 0.440573
    0.477504 0.821444 0.318195
    0.741388 0.873449 0.149561
    0.993248 0.906157 0.143936 ];

m  = size(anchors, 1);
xi = linspace(1, m, n).';
x  = (1:m).';

cm = zeros(n, 3);
for c = 1:3
    cm(:, c) = interp1(x, anchors(:, c), xi, 'linear');
end
cm = min(max(cm, 0), 1);
end
