function parts = gk_splitcsv(line)
%GK_SPLITCSV Split one CSV record, honouring double-quoted fields.
%   A plain strsplit on "," breaks any field that legitimately contains a
%   comma, e.g. the provenance string
%       "earlier eval., in FeherKovacs2021 Table 1"
%   which was silently truncated to  "earlier eval.  and rendered with a
%   stray quote character in the figure. This splitter follows RFC 4180:
%   a field may be wrapped in double quotes, inside which commas are literal
%   and a doubled quote ("") denotes one literal quote.

parts = {};
buf   = '';
inq   = false;
i     = 1;
n     = numel(line);

while i <= n
    c = line(i);
    if inq
        if c == '"'
            if i < n && line(i+1) == '"'
                buf(end+1) = '"';  %#ok<AGROW>
                i = i + 2;
                continue
            end
            inq = false;
            i = i + 1;
            continue
        end
        buf(end+1) = c;  %#ok<AGROW>
        i = i + 1;
    else
        if c == '"'
            inq = true;
            i = i + 1;
        elseif c == ','
            parts{end+1} = buf;  %#ok<AGROW>
            buf = '';
            i = i + 1;
        else
            buf(end+1) = c;  %#ok<AGROW>
            i = i + 1;
        end
    end
end
parts{end+1} = buf;
end
