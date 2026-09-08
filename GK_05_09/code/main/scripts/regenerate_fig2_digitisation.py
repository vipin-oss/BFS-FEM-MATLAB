"""Regenerate the despeckled Fig.2 digitisation from the anchor figure image.

INPUT DATA generation, not a scientific result. Run once; output is
data/fig2_digitised_despeckled.npy. Requires the archived digitiser and the
figure image from validation/.
"""
import sys, numpy as np
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent   # .../code/main
PROJECT = ROOT.parent.parent                    # package root
INPUT_DIR = PROJECT / "data" / "input"          # central read-only input tree
sys.path.insert(0, str(ROOT))                   # find src/ and this script's modules
sys.path.insert(0, str(ROOT / "scripts"))       # find digitize.py
import digitize as D

# Anchor source raster (publication figure used to re-digitise Fig. 2).
IMG = INPUT_DIR / "p10_fig2.png"


def despeckle(X, Y, dx_tol=0.0035, need=2):
    keep = np.zeros(len(X), bool)
    for i in range(len(X)):
        m = (np.abs(X - X[i]) < dx_tol) & (np.abs(Y - Y[i]) < 0.05)
        keep[i] = (m.sum() - 1) >= need
    return X[keep], Y[keep]


if __name__ == "__main__":
    X, Y = D.digitise_multi(D.load_gray(str(IMG)), D.CAL["fig2"],
                            col_step=2, gap=25)
    k = (X > 0.006) & (X < 0.444)
    X, Y = X[k], Y[k]
    n0 = len(X)
    X, Y = despeckle(X, Y)
    out = INPUT_DIR / "fig2_digitised_despeckled.npy"
    np.save(out, dict(X=X, Y=Y, full_range=float(Y.max() - Y.min())),
            allow_pickle=True)
    print(f"{n0} -> {len(X)} points after despeckle; saved {out}")
