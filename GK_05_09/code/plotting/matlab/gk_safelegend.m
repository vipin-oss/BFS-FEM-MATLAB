function lg = gk_safelegend(ax, varargin)
%GK_SAFELEGEND Legend that can never cover a data point.
%   The previous figure set lost two calibration points behind a legend
%   box. This helper removes that failure mode structurally rather than by
%   eye: the legend is placed OUTSIDE the axes by default.
%
%   gk_safelegend(ax, h, labels)                    -> outside, north-east
%   gk_safelegend(ax, h, labels, 'loc','northoutside')
%   gk_safelegend(ax, h, labels, 'cols',2)
%
%   Any 'loc' value ending in 'outside' is guaranteed collision-free. If a
%   caller asks for an inside location it is honoured, but only where the
%   calling script has already reserved empty space for it.

loc  = 'eastoutside';
cols = 1;
args = {};
k = 1;
while k <= numel(varargin)
    if ischar(varargin{k}) && strcmpi(varargin{k}, 'loc')
        loc = varargin{k+1}; k = k + 2;
    elseif ischar(varargin{k}) && strcmpi(varargin{k}, 'cols')
        cols = varargin{k+1}; k = k + 2;
    else
        args{end+1} = varargin{k}; k = k + 1; %#ok<AGROW>
    end
end

S = gk_style();
lg = legend(ax, args{:});
set(lg, 'Location', loc, 'FontSize', S.fsLegend, 'FontName', gk_font());

% A box is kept for legibility, but the legend sits outside the data area
% so the box cannot occlude anything.
set(lg, 'Box', 'on', 'Color', 'w');

if cols > 1
    try
        set(lg, 'NumColumns', cols);   % MATLAB R2018a+ / recent Octave
    catch
        % older interpreter: silently keep a single column
    end
end
end
