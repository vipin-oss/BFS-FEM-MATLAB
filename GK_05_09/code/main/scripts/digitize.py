"""
Digitisation of the published figures of Kovacs (2018), IJHMT 127(A), 631-636.
Source raster: arXiv:1804.05225v1 embedded images (4000x1908 px).

GATE 4 requires TWO INDEPENDENT digitisation passes so that digitisation
uncertainty sigma_d is measured, not assumed.

PASS A : intensity-weighted centroid of dark pixels in each column.
PASS B : midpoint of the extreme dark pixels (min/max envelope) in each column.
These respond differently to line thickness, dashes and grid crossings, so their
spread is a genuine estimate of digitisation uncertainty.

The published figures each contain TWO curves ('analytical' thin solid and
'numerical' thick dashed) which overlie each other almost everywhere. We
therefore digitise the union band and treat its half-width as part of sigma_d.
This is stated explicitly rather than hidden.
"""
import numpy as np
from PIL import Image

# Axis calibration, read from the raster frame + tick labels of each figure.
# Frame pixel coords are identical for the two IJHMT-style plots.
CAL = {
    # name : (x0px, x1px, y0px, y1px, xmin, xmax, ymin, ymax, legend_box)
    # Rows 145-384 hold the legend text; the T=1.0 curve band starts at row 385,
    # so the mask must stop at 384 or it clips the curve. Verified by a
    # column-density scan of the raster (see validation report).
    'fig3':  (521, 3620, 1664, 143, 0.0, 1.0, 0.0, 1.2, (2500, 3621, 145, 384)),
    'fig5':  (521, 3620, 1664, 143, 0.0, 2.0, 0.0, 1.2, (2500, 3621, 145, 384)),
    # Fig 2 has a different frame and a negative y-range
    'fig2':  (521, 3620, 1698, 143, 0.0, 0.45, -0.8, 1.0, (521, 1100, 143, 560)),
}


def load_gray(path):
    return np.array(Image.open(path).convert('L'))


def mask_curve(img, cal, thresh=110):
    """Dark-pixel mask with frame, gridlines and legend removed."""
    x0, x1, y0, y1, *_ , legend = cal
    H, W = img.shape
    dark = img < thresh

    # remove near-full rows/cols: frame + solid gridlines
    rows = dark.sum(1)
    cols = dark.sum(0)
    for i in range(H):
        if rows[i] > 0.45 * W:
            dark[i, :] = False
    for j in range(W):
        if cols[j] > 0.45 * H:
            dark[:, j] = False

    # blank the legend box
    lx0, lx1, ly0, ly1 = legend
    dark[ly0:ly1, lx0:lx1] = False

    # restrict to plot interior
    out = np.zeros_like(dark)
    top, bot = min(y0, y1), max(y0, y1)
    out[top + 3:bot - 2, x0 + 3:x1 - 2] = dark[top + 3:bot - 2, x0 + 3:x1 - 2]
    return out


def px_to_data(cal, xs, ys):
    x0, x1, y0, y1, xmin, xmax, ymin, ymax, _ = cal
    X = xmin + (xs - x0) * (xmax - xmin) / (x1 - x0)
    Y = ymin + (ys - y0) * (ymax - ymin) / (y1 - y0)
    return X, Y


def digitise(img, cal, pass_name='A', col_step=4):
    """Return (x_data, y_data) for one digitisation pass."""
    m = mask_curve(img, cal)
    x0, x1 = cal[0], cal[1]
    xs, ys = [], []
    for j in range(x0 + 4, x1 - 3, col_step):
        idx = np.nonzero(m[:, j])[0]
        if idx.size == 0:
            continue
        if pass_name == 'A':          # intensity-weighted centroid
            w = (255.0 - img[idx, j])
            yy = float((idx * w).sum() / w.sum())
        else:                          # envelope midpoint
            yy = 0.5 * (idx.min() + idx.max())
        xs.append(j); ys.append(yy)
    xs = np.array(xs, float); ys = np.array(ys, float)
    return px_to_data(cal, xs, ys)


def band_halfwidth(img, cal, col_step=4):
    """Half vertical extent of the dark band, in DATA units -> curve-thickness term."""
    m = mask_curve(img, cal)
    x0, x1 = cal[0], cal[1]
    hw = []
    for j in range(x0 + 4, x1 - 3, col_step):
        idx = np.nonzero(m[:, j])[0]
        if idx.size == 0:
            continue
        hw.append(0.5 * (idx.max() - idx.min()))
    hw = np.array(hw, float)
    _, ymin, = 0, cal[6]
    ymax = cal[7]
    y0, y1 = cal[2], cal[3]
    scale = abs((ymax - ymin) / (y1 - y0))
    return hw * scale


def digitise_multi(img, cal, col_step=4, gap=25):
    """
    For Fig 2: several distinct curves per column. Cluster the dark pixels in each
    column into runs separated by > gap px and return every cluster centre.
    """
    m = mask_curve(img, cal)
    x0, x1 = cal[0], cal[1]
    pts = []
    for j in range(x0 + 4, x1 - 3, col_step):
        idx = np.nonzero(m[:, j])[0]
        if idx.size == 0:
            continue
        splits = np.split(idx, np.nonzero(np.diff(idx) > gap)[0] + 1)
        for s in splits:
            pts.append((j, float(s.mean())))
    pts = np.array(pts, float)
    X, Y = px_to_data(cal, pts[:, 0], pts[:, 1])
    return X, Y
