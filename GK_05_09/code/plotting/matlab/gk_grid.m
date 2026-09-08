function ax = gk_grid(fig, nrow, ncol, varargin)
%GK_GRID Deterministic panel grid with explicit, reserved margins.
%
%   Replaces subplot(), whose automatic positioning caused the collisions in
%   the earlier figure set: super-titles overprinting panel titles, panel
%   labels landing on tick labels, and x labels clipped at the figure edge.
%
%   Every margin here is reserved explicitly, so a panel title, a panel
%   label, an axis label and the super-title each have their own space and
%   cannot overlap. All figures use this one function, which is what makes
%   panel size, panel spacing and plotting-region alignment identical across
%   the whole set.
%
%   ax = gk_grid(fig, nrow, ncol)
%   ax = gk_grid(fig, nrow, ncol, 'top',0.14, 'hgap',0.10)
%
%   Returns a nrow x ncol array of axes handles, filled row-wise.
%
%   Margins are fractions of the figure; defaults are tuned for the house
%   font sizes with a two-line super-title.

p.left   = 0.075;   % room for the y label + tick labels
p.right  = 0.020;
p.top    = 0.150;   % super-title + panel label + panel title
p.bottom = 0.150;   % x label + tick labels
p.hgap   = 0.095;   % horizontal gap between panels
p.vgap   = 0.170;   % vertical gap between rows

for k = 1:2:numel(varargin)
    key = lower(varargin{k});
    if isfield(p, key)
        p.(key) = varargin{k+1};
    else
        error('gk_grid:badOption','Unknown option "%s"', varargin{k});
    end
end

W = (1 - p.left - p.right - (ncol-1)*p.hgap) / ncol;
H = (1 - p.top  - p.bottom - (nrow-1)*p.vgap) / nrow;

if W <= 0 || H <= 0
    error('gk_grid:noRoom', ...
        'Margins leave no room for panels (W=%.3f, H=%.3f).', W, H);
end

% Preallocate as a graphics-object array, not a numeric one. Octave
% represents graphics handles as doubles internally, so ax = zeros(...)
% happened to work there; in MATLAB (HG2), assigning an axes handle into a
% double array silently degrades it back to a plain double on read-back,
% which then fails downstream in any handle-consuming call (e.g.
% "ishold(ax)"/"hold(ax,...)" raise "Using hold with double is not
% supported"). gobjects() preallocates true graphics-object placeholders
% and is safe in both MATLAB (since R2014b) and Octave.
ax = gobjects(nrow, ncol);
for r = 1:nrow
    for c = 1:ncol
        x = p.left + (c-1)*(W + p.hgap);
        y = 1 - p.top - r*H - (r-1)*p.vgap;
        ax(r,c) = axes('Parent', fig, 'Units','normalized', ...
                       'Position', [x y W H]);
    end
end
end
