"""Raw-result writer + reproducibility manifest (architecture items 12-13
data side; blueprint §18-19, task §23).

Every physics result is written as machine-readable CSV with the full
record columns. A manifest links runs to parameter/grid hashes and solver
version hash. Plotting scripts read these files ONLY.
"""
import csv, hashlib, json, os, time

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(_ROOT, "results")
os.makedirs(RESULTS, exist_ok=True)

def _sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def solver_version_hash():
    h = hashlib.sha256()
    d = os.path.join(_ROOT, "solver")
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".py"):
            h.update(fn.encode())
            h.update(_sha_file(os.path.join(d, fn)).encode())
    return h.hexdigest()[:16]

def run_id():
    return time.strftime("%Y%m%d-%H%M%S")

def write_csv(name, header, rows):
    path = os.path.join(RESULTS, name)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return path

def manifest_entry(run, study, files, extra=None):
    mpath = os.path.join(RESULTS, "MANIFEST.md")
    new = not os.path.exists(mpath)
    with open(mpath, "a") as f:
        if new:
            f.write("# Reproducibility manifest\n\n")
            f.write("| run_id | study | params.json sha | grids.json sha | solver ver | files | notes |\n")
            f.write("|---|---|---|---|---|---|---|\n")
        f.write(f"| {run} | {study} | `{_sha_file(os.path.join(_ROOT,'params.json'))[:12]}` "
                f"| `{_sha_file(os.path.join(_ROOT,'grids.json'))[:12]}` "
                f"| `{solver_version_hash()}` | {', '.join(files)} "
                f"| {json.dumps(extra) if extra else ''} |\n")
    return mpath
