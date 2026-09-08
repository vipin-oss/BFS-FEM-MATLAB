function h = gk_band(ax, x0, x1, y0, y1, col, frac)
%GK_BAND Shaded axis-aligned region built from dense vertical LINE segments.
%
%   WHY NOT patch()/fill()/rectangle():
%   In vector (painters) output this Octave/Qt backend intermittently
%   rendered flat-coloured patch faces with spurious gradient shading, so a
%   pale tint came out as a dark streaked block. The fault appeared only in
%   some figures, which made it look like a data problem rather than a
%   rendering one. Line primitives are never gradient-shaded, so building
%   the region from closely spaced vertical lines is immune to it and gives
%   an exactly flat fill in both screen and print output.
%
%   The colour is pre-blended towards white by gk_tint, so no transparency
%   is required and the appearance is identical on screen and on paper.
%
%   Returns a handle suitable for use as a legend key.

if nargin < 7 || isempty(frac), frac = 0.18; end
c = gk_tint(col, frac);

nSeg = 420;                       % dense enough to read as a solid fill
xs   = linspace(x0, x1, nSeg);

wasHeld = ishold(ax);
hold(ax, 'on');

h = [];
for k = 1:nSeg
    hk = plot(ax, [xs(k) xs(k)], [y0 y1], '-', ...
              'Color', c, 'LineWidth', 1.6);
    if k == 1
        h = hk;                   % representative handle for the legend
    else
        try
            set(get(get(hk,'Annotation'),'LegendInformation'), ...
                'IconDisplayStyle','off');
        catch
        end
    end
end

if ~wasHeld
    hold(ax, 'off');
end
end
