function T = gk_readcsv(name)
%GK_READCSV Read a verified Phase-5 CSV into a struct of columns.
%   T = GK_READCSV('bands.csv') returns a struct whose fields are the CSV
%   column headers. Numeric columns become double arrays; anything that is
%   not fully numeric stays a cell array of strings.
%
%   READ ONLY. This function never writes, never fills missing values and
%   never alters a stored number. Empty cells become NaN so that missing
%   entries stay visibly missing rather than silently becoming zero.
%
%   Implemented with low-level I/O so it behaves identically on MATLAB and
%   on GNU Octave, and does not depend on any toolbox.

P = gk_paths();
f = fullfile(P.data, name);
if ~exist(f, 'file')
    error('gk_readcsv:missing', 'Verified data file not found: %s', f);
end

fid = fopen(f, 'r');
if fid < 0
    error('gk_readcsv:open', 'Cannot open %s', f);
end
raw = fread(fid, inf, 'uint8=>char').';
fclose(fid);

raw   = strrep(raw, sprintf('\r\n'), sprintf('\n'));   % CRLF -> LF
raw   = strrep(raw, sprintf('\r'),   sprintf('\n'));
lines = strsplit(raw, sprintf('\n'));
lines = lines(~cellfun(@(s) isempty(strtrim(s)), lines));
if isempty(lines)
    error('gk_readcsv:empty', 'File is empty: %s', f);
end

hdr = strtrim(strsplit(lines{1}, ','));
n   = numel(lines) - 1;
m   = numel(hdr);

cols = cell(1, m);
for j = 1:m
    cols{j} = cell(n, 1);
end

for i = 1:n
    parts = gk_splitcsv(lines{i+1});
    for j = 1:m
        if j <= numel(parts)
            cols{j}{i} = strtrim(parts{j});
        else
            cols{j}{i} = '';
        end
    end
end

T = struct();
for j = 1:m
    field = regexprep(hdr{j}, '[^A-Za-z0-9_]', '_');
    if isempty(field) || ~isletter(field(1))
        field = ['c' field];
    end
    strvals = cols{j};
    num     = nan(n, 1);
    isnum   = true;
    for i = 1:n
        s = strvals{i};
        if isempty(s)
            num(i) = NaN;                 % missing stays missing
        else
            v = str2double(s);
            if isnan(v)
                isnum = false;            % genuine text column
                break
            end
            num(i) = v;
        end
    end
    if isnum
        T.(field) = num;
    else
        T.(field) = strvals;
    end
end
T.n_rows_ = n;
end
