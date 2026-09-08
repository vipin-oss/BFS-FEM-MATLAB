function nHidden = gk_assert_legend_clear(ax, lg, mode)
%GK_ASSERT_LEGEND_CLEAR Verify that a legend hides no plotted data point.
%
%   Phase 7A requirement K: "No legend may cover any data point."
%   This helper enforces it at RUNTIME rather than by eye. It projects every
%   marker/line vertex in the axes into normalised axes coordinates and tests
%   them against the legend rectangle.
%
%   nHidden = GK_ASSERT_LEGEND_CLEAR(ax, lg)          warn on occlusion
%   nHidden = GK_ASSERT_LEGEND_CLEAR(ax, lg, 'error') stop on occlusion
%
%   Any legend placed with a '*outside' location is clear by construction and
%   is reported as such without further testing.
%
%   Returns the number of occluded vertices (0 is the required outcome).

if nargin < 3 || isempty(mode)
    mode = 'warn';
end
nHidden = 0;

if isempty(lg) || ~ishandle(lg)
    return
end

loc = '';
try
    loc = lower(get(lg, 'Location'));
catch
end
if ~isempty(strfind(loc, 'outside'))
    fprintf('      legend [%s]: outside the axes, clear by construction\n', loc);
    return
end

% ---- legend rectangle in normalised FIGURE coordinates ---------------
oldLgU = get(lg, 'Units');  set(lg, 'Units', 'normalized');
lgPos  = get(lg, 'Position');
set(lg, 'Units', oldLgU);

oldAxU = get(ax, 'Units');  set(ax, 'Units', 'normalized');
axPos  = get(ax, 'Position');
set(ax, 'Units', oldAxU);

% legend rectangle expressed in normalised AXES coordinates
lx0 = (lgPos(1) - axPos(1)) / axPos(3);
ly0 = (lgPos(2) - axPos(2)) / axPos(4);
lx1 = (lgPos(1) + lgPos(3) - axPos(1)) / axPos(3);
ly1 = (lgPos(2) + lgPos(4) - axPos(2)) / axPos(4);

xl = get(ax, 'XLim');  yl = get(ax, 'YLim');
xlog = strcmp(get(ax, 'XScale'), 'log');
ylog = strcmp(get(ax, 'YScale'), 'log');

kids = findall(ax, 'Type', 'line');
total = 0;
for k = 1:numel(kids)
    xd = get(kids(k), 'XData');
    yd = get(kids(k), 'YData');
    if isempty(xd), continue; end
    xd = xd(:); yd = yd(:);
    good = isfinite(xd) & isfinite(yd);
    xd = xd(good); yd = yd(good);
    if isempty(xd), continue; end

    if xlog
        nx = (log10(xd) - log10(xl(1))) / (log10(xl(2)) - log10(xl(1)));
    else
        nx = (xd - xl(1)) / (xl(2) - xl(1));
    end
    if ylog
        ny = (log10(yd) - log10(yl(1))) / (log10(yl(2)) - log10(yl(1)));
    else
        ny = (yd - yl(1)) / (yl(2) - yl(1));
    end

    inside = nx >= lx0 & nx <= lx1 & ny >= ly0 & ny <= ly1;
    nHidden = nHidden + sum(inside);
    total   = total + numel(nx);
end

if nHidden > 0
    msg = sprintf(['legend [%s] overlaps %d of %d plotted vertices in this ' ...
                   'axes; move it outside or enlarge the limits'], ...
                   loc, nHidden, total);
    if strcmpi(mode, 'error')
        error('gk:legendOcclusion', '%s', msg);
    else
        fprintf('      WARNING: %s\n', msg);
    end
else
    fprintf('      legend [%s]: clear, 0 of %d vertices occluded\n', loc, total);
end
end
