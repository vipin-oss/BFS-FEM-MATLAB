function name = gk_font()
%GK_FONT Resolve a serif font that actually exists on this machine.
%   Prefers Times New Roman (journal standard), then Times, then Nimbus
%   Roman (the common Linux metric clone), and finally falls back to the
%   interpreter default. Avoids the missing-font warnings that otherwise
%   appear on Linux/Octave and silently change text metrics.

persistent cached
if ~isempty(cached)
    name = cached;
    return
end

wanted = {'Times New Roman', 'Times', 'Nimbus Roman', 'Liberation Serif', 'FreeSerif'};

available = {};
try
    available = listfonts();     %#ok<NASGU>
catch
    available = {};
end

name = '';
for k = 1:numel(wanted)
    if isempty(available)
        break
    end
    if any(strcmpi(available, wanted{k}))
        name = wanted{k};
        break
    end
end

if isempty(name)
    % listfonts unavailable or none matched: Times is a safe generic request,
    % every backend maps it to some serif face.
    name = 'Times';
end

cached = name;
end
