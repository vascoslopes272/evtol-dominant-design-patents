"""Paper P1 figure panels: one vector PDF per panel, 85 x 65 mm (one TFSC column).

    EVTOL_DATASET=<path to eVTOL_dataset> python 33_paper_figures.py [--only fig5 fig7 ...]

Needs: results/2_analysis/family_F/percentiles_balance.csv and percentiles_disparity.csv (script 31_family_F_numbers.py; they hold the
balance and disparity tables of notebook 23 for BOTH bases, each base with its own permutation band, permutations only inside that
base) and the dataset. Writes results/2_analysis/paper_figures/*.pdf, a csv per panel (the plotted values), comparison_with_notebooks.csv
and README.md. Nothing is recomputed that the notebooks compute: the values and the bands are those tables.

Common frame: every panel is 85 x 65 mm with the same axes rectangle (AX_RECT), Liberation Sans (Arial metrics) at 7 pt everywhere, no title, no
panel letter, no legend in the image, white background, left and bottom spines only.
"""
from __future__ import annotations

import argparse
import sys
import textwrap
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "2_analysis" / "src"))
sys.path.insert(0, str(REPO / "2_analysis" / "notebooks"))
OUT = REPO / "results" / "2_analysis" / "paper_figures"
FF = REPO / "results" / "2_analysis" / "family_F"
CSV = REPO / "results" / "2_analysis" / "freeze" / "csv"
TEST2 = Path("EVTOL_DATASET")  # replaced below once the environment is read

W_IN, H_IN = 85 / 25.4, 65 / 25.4
AX_RECT = [0.175, 0.215, 0.795, 0.765]          # left, bottom, width, height (fractions): the same in every panel
FS = 7.0
FONT = ["TeX Gyre Heros", "Arial", "Liberation Sans", "DejaVu Sans"]
COHORTS = ["≤ 2011", "2012–15", "2016–19", "2020–23", "2024–26*"]
WIN = ["<= 2011", "2012-15", "2016-19", "2020-23", "2024-26 (partial)"]
C_ALL = "#000000"        # all designs
C_PROT = "#0072B2"       # actively protected designs (own colour, solid line, filled markers)
C_PBAND = "#003F66"      # protected band: darker, thicker dotted line
C_UNT = "#8C8C8C"        # untested cohort 2024-26*: grey, dashed, hollow markers
F_COLOR = "#000000"      # family F panels use the same pair of colours as Fig 5 (set to "#005A8C" for the thesis' F blue)
RED = "#D62728"
BAND = "#E3E3E3"
EDGE_GREY = "#6E6E6E"
GRID = "#EBEBEB"
REF = "#555555"
MAIN_W = "w15"
LEVELS = {"5a": ("A0", "fig5a_balance_L1.pdf"), "5b": ("A1t", "fig5b_balance_L2.pdf"), "5c": ("A0c", "fig5c_balance_L3.pdf")}

LOG = []          # what did not fit, for the README
LABEL4 = {"HB": "Hoverbike"}          # Fig 4: HB (hoverbike / personal flying device) is not defined in the paper, so the label spells it out
# Fig 8 (file fig7c_...): the 15 dimensions of the disparity distance, in the order of test2_explore_per_dimension.csv, as the paper names them
DIM_LABELS = {"Architecture": "Architecture", "Fuselage Shape": "Fuselage shape", "Boom count": "Boom count",
              "Fuselage Kinematics": "Fuselage kinematics", "Wing count": "Number of wings", "Wing Architecture": "Wing configuration",
              "Vertical Position": "Primary wing vertical position", "Longitudinal Position": "Primary wing longitudinal position",
              "Planform": "Primary wing planform", "Empennage Type": "Tail type", "Propulsor band": "Propulsor number interval",
              "Tilt share": "Tilt share", "Propulsor Enclosure": "Propulsor enclosure",
              "Tractor/Pusher Arrangement": "Tractor/pusher arrangement", "Mount locations": "Mount locations"}


def rc():
    return mpl.rc_context({
        "font.family": "sans-serif", "font.sans-serif": FONT, "font.size": FS, "axes.labelsize": FS, "xtick.labelsize": FS,
        "ytick.labelsize": FS, "legend.fontsize": FS, "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "xtick.major.size": 2.5, "ytick.major.size": 2.5, "lines.linewidth": 1.2, "lines.markersize": 3.6,
        "savefig.bbox": "standard", "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.transparent": False, "savefig.facecolor": "white", "figure.facecolor": "white",
        "axes.facecolor": "white", "axes.spines.top": False, "axes.spines.right": False, "axes.unicode_minus": True,
        "hatch.linewidth": 0.5, "mathtext.default": "regular"})


def frame(name: str):
    fig = plt.figure(figsize=(W_IN, H_IN))
    ax = fig.add_axes(AX_RECT)
    ax.set_label(name)
    return fig, ax


def finish(fig, name: str, extra_ok_texts=()):
    """Save, then check: nothing under 7 pt, nothing outside the page, no tick labels touching."""
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    page = fig.bbox
    for t in fig.findobj(mpl.text.Text):
        if not t.get_text().strip() or not t.get_visible():
            continue
        if t.get_text().startswith("$\\mathdefault"):          # a tick label outside the axis limits: matplotlib keeps it but never draws it
            continue
        if t.get_fontsize() < FS - 1e-6:
            LOG.append(f"{name}: text under 7 pt: {t.get_text()!r} ({t.get_fontsize():.1f})")
        bb = t.get_window_extent(rend)
        if bb.x0 < page.x0 - 1 or bb.x1 > page.x1 + 1 or bb.y0 < page.y0 - 1 or bb.y1 > page.y1 + 1:
            LOG.append(f"{name}: text outside the 85 x 65 mm page: {t.get_text()!r}")
    for ax in fig.axes:
        labs = [t for t in ax.get_xticklabels() if t.get_text()]
        bbs = [t.get_window_extent(rend) for t in labs]
        for a, b in zip(bbs, bbs[1:]):
            if a.x1 > b.x0 - 1.0:
                LOG.append(f"{name}: x tick labels touch ({a.x1:.0f} > {b.x0:.0f} px at 72 dpi)")
                break
    fig.savefig(OUT / name, format="pdf")
    fig.savefig(OUT / (Path(name).stem + ".png"), format="png", dpi=300)
    plt.close(fig)


def cohort_axis(ax, ns=None):
    ax.set_xticks(range(5))
    if ns is None:
        ax.set_xticklabels(COHORTS)
    else:
        ax.set_xticklabels([f"{c}\nn {int(n)}" for c, n in zip(COHORTS, ns)], linespacing=1.15)
    ax.set_xlim(-0.5, 4.5)
    ax.set_xlabel("priority-year cohort")
    ax.grid(axis="y", color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)


def untested(ax, x4, y3, y4, ms=3.6):
    """The untested cohort 2024-26*: a dashed grey segment from the last tested cohort, hollow grey marker."""
    ax.plot([3, x4], [y3, y4], color=C_UNT, linewidth=1.0, linestyle=(0, (3, 1.6)), zorder=3)
    ax.plot([x4], [y4], marker="o", markersize=ms, markerfacecolor="white", markeredgecolor=C_UNT, markeredgewidth=0.9, linestyle="none", zorder=5)


def ring(ax, x, y, ms):
    """A point below its own permutation band: a red ring around the point (the point keeps the colour of its series)."""
    ax.plot([x], [y], marker="o", markersize=ms, markerfacecolor="none", markeredgecolor=RED, markeredgewidth=1.1, linestyle="none", zorder=6)


def two_series(ax, all_df, prot_df, val, lo, hi, wlo=None, whi=None, met_all=None, met_prot=None, prot_band=True, clip=None):
    """Same graph in every panel: all designs (black, solid line, filled markers, grey shaded band, whiskers when given) and actively
    protected designs (own colour, solid line, filled markers, same cohort position; own band as a dotted outline, balance only).
    The untested 2024-26* cohort is grey, dashed, hollow. A point below its own band has a red ring."""
    x = np.arange(5)
    a, p = all_df.reset_index(drop=True), prot_df.reset_index(drop=True)
    ax.fill_between(x, a[lo], a[hi], color=BAND, linewidth=0, zorder=1)
    if prot_band:
        for col in (lo, hi):
            ax.plot(x, p[col], color=C_PBAND, linewidth=1.4, linestyle=(0, (1, 1.4)), dash_capstyle="round", zorder=2)
    c = slice(0, 4)
    if wlo is not None:
        conts = [ax.errorbar(x[c], a[val][c], yerr=[a[val][c] - a[wlo][c], a[whi][c] - a[val][c]], fmt="none", ecolor=C_ALL, elinewidth=0.6,
                             capsize=1.4, capthick=0.6, zorder=3),
                 ax.errorbar(x[4:], a[val][4:], yerr=[a[val][4:] - a[wlo][4:], a[whi][4:] - a[val][4:]], fmt="none", ecolor=C_UNT,
                             elinewidth=0.6, capsize=1.4, capthick=0.6, zorder=3)]
        if clip is not None:          # whiskers are cut at the limits of the zoomed axis (they never run into the legend)
            box = mpl.patches.Rectangle((-0.5, clip[0]), 5.0, clip[1] - clip[0], transform=ax.transData)
            for ct in conts:
                for art in [ct.lines[0]] + list(ct.lines[1]) + list(ct.lines[2]):
                    if art is not None:
                        art.set_clip_path(box)
    for df, col, z in ((p, C_PROT, 4), (a, C_ALL, 4.1)):
        ax.plot(x[c], df[val][c], marker="o", color=col, markerfacecolor=col, markeredgecolor=col, zorder=z)
        untested(ax, 4, df[val][3], df[val][4])
    for i, m in enumerate(met_all if met_all is not None else []):
        if m:
            ring(ax, i, a[val][i], 6.0)
    for i, m in enumerate(met_prot if met_prot is not None else []):
        if m:
            ring(ax, i, p[val][i], 8.0)


def legend_handles():
    return [Line2D([], [], color=C_ALL, marker="o", markerfacecolor=C_ALL, label="All designs"),
          Line2D([], [], color=C_PROT, marker="o", markerfacecolor=C_PROT, label="Protected designs"),
          Line2D([], [], color=C_UNT, marker="o", markerfacecolor="white", markeredgecolor=C_UNT, markeredgewidth=0.9, linestyle=(0, (3, 1.6)),
                 label="Untested 2024–26*"),
          mpl.patches.Patch(facecolor=BAND, edgecolor="none", label="Band, all designs"),
          Line2D([], [], color=C_PBAND, linewidth=1.4, linestyle=(0, (1, 1.4)), dash_capstyle="round", label="Band, protected"),
          Line2D([], [], marker="o", markerfacecolor="none", markeredgecolor=RED, markeredgewidth=1.1, linestyle="none", label="Below band")]


def legend_5a(ax, loc="upper center"):
    ax.legend(handles=legend_handles(), loc=loc, ncol=2, frameon=False, handlelength=2.0, columnspacing=1.0, labelspacing=0.3, borderaxespad=0.0,
              handletextpad=0.5, fontsize=FS)


def tight_ylim(ax, lo, hi, legend=False):
    """y limits that just hold the plotted values; with a legend the top is raised so that the legend sits above the data."""
    span = hi - lo
    b, t = lo - 0.04 * span, hi + 0.04 * span
    if legend:
        t = b + (t - b) / 0.74
    ax.set_ylim(b, t)


# ---------------------------------------------------------------------------------------------------------------- tables
def load_tables():
    bal = pd.read_csv(FF / "percentiles_balance.csv")
    dis = pd.read_csv(FF / "percentiles_disparity.csv")
    note = (FF / "run_note.txt").read_text() if (FF / "run_note.txt").exists() else ""
    perms = int(note.split("permutations per band:")[1].split()[0]) if "permutations" in note else 0
    return bal, dis, perms


def pick_bal(bal, level, base):
    s = bal[(bal["level"] == level) & (bal["base"] == base)].set_index("window").reindex(WIN)
    s["met"] = s["below band"].astype(bool) & ~s.index.str.contains("partial")
    return s.reset_index()


def pick_dis(dis, level, base):
    s = dis[(dis["level"] == level) & (dis["base"] == base) & (dis["weighting"] == MAIN_W)].set_index("window").reindex(WIN)
    # the two earliest cohorts are the baseline of ΔQ and are not tested; 2024-26 is incomplete
    s["met"] = s["below band"].astype(bool) & ~s.index.str.contains("partial") & ~s.index.isin(WIN[:2])
    return s.reset_index()


# ---------------------------------------------------------------------------------------------------------------- Fig 4
def fig4(ctx):
    from viz import figures_part3 as p3
    import thesis_style as ts
    share, _, _ = p3.joined_shares(ctx)
    from viz import thesis_q6 as q6
    n_win = q6._data(ctx)["n_win"]
    codes = list(share.columns)
    big = ("SLC", "TR", "CVT")
    short = {"TR": "TP", "TB": "TF"}
    fig, ax = frame("fig4")
    x = np.arange(5)
    first_hollow = (0, 1, 4)           # ≤2011 and 2012-15 (few designs) and 2024-26* (incomplete): not tested
    for c in codes[::-1]:
        col = ts.ARCH[short.get(c, c)]
        y = share[c].to_numpy(float) * 100
        main = c in big
        ax.plot(x[:4], y[:4], color=col, linewidth=1.5 if main else 0.7, alpha=1 if main else 0.65, zorder=4 if main else 3)
        for i in range(5):
            if i in first_hollow:
                ax.plot([i], [y[i]], marker="o", markersize=3.6 if main else 2.4, markerfacecolor="white", markeredgecolor=col,
                        markeredgewidth=0.8, linestyle="none", alpha=0.75, zorder=5 if main else 3)
            else:
                ax.plot([i], [y[i]], marker="o", markersize=3.6 if main else 2.4, color=col, alpha=1 if main else 0.65, zorder=5 if main else 3)
    ax.set_ylim(0, 40)
    ax.set_yticks([0, 10, 20, 30, 40])
    ax.set_ylabel("share of all designs (%)")
    cohort_axis(ax, n_win)
    ax.set_xlim(-0.4, 5.55)
    ax.spines["bottom"].set_bounds(-0.4, 4.4)
    # direct labels (architecture codes) at the right of 2024-26*: a short leader from each last point to its label
    last = share.iloc[-1].to_numpy(float) * 100
    gap = 40 * (FS * 1.15 / 72) / (H_IN * AX_RECT[3])
    pos = spread(last, gap, 0.0, 40.0)
    for c, yv, yp in zip(codes, last, pos):
        k = short.get(c, c)
        col = ts.ARCH[k]
        ax.plot([4.1, 4.45], [yv, yp], color=col, linewidth=0.4, zorder=2)
        ax.text(4.5, yp, LABEL4.get(k, k), color=col, ha="left", va="center", fontsize=FS, fontweight="bold" if c in big else "normal")
    finish(fig, "fig4_architecture_shares.pdf")
    share.assign(designs=list(n_win)).round(4).to_csv(OUT / "fig4_architecture_shares.csv")


def spread(ys, gap, lo, hi):
    ys = np.asarray(ys, float)
    o = np.argsort(ys, kind="stable")
    p = ys[o].copy()
    p[0] = max(p[0], lo)
    for i in range(1, len(p)):
        p[i] = max(p[i], p[i - 1] + gap)
    if p[-1] > hi:
        p[-1] = hi
        for i in range(len(p) - 2, -1, -1):
            p[i] = min(p[i], p[i + 1] - gap)
    out = np.empty_like(p)
    out[o] = p
    return out


# ---------------------------------------------------------------------------------------------------------------- Fig 5 and 7b
def balance_axes(ax, bal, level, ylabel, zoom=False, legend=False, legend_loc="upper center"):
    """zoom: False = from 0; True = the whole plotted range (whiskers included); "tight" = the whole plotted range with 3 % padding (every whisker complete); with a legend at the top the limits leave 26 % of the axis free for it."""
    a, p = pick_bal(bal, level, "all designs"), pick_bal(bal, level, "actively protected")
    hi = float(np.nanmax(pd.concat([a[["D2 high", "D2 permutation high"]], p[["D2", "D2 permutation high"]]]).to_numpy()))
    clip = None
    if zoom == "tight":
        lo = float(np.nanmin(pd.concat([a[["D2 low", "D2 permutation low"]], p[["D2", "D2 permutation low"]]]).to_numpy()))
        span = hi - lo
        yb, yt = lo - 0.03 * span, hi + 0.03 * span
    elif zoom:
        lo = float(np.nanmin(pd.concat([a[["D2 low", "D2 permutation low"]], p[["D2", "D2 permutation low"]]]).to_numpy()))
        span = hi - lo
        yb, yt = lo - 0.04 * span, hi + 0.04 * span
    two_series(ax, a, p, "D2", "D2 permutation low", "D2 permutation high", "D2 low", "D2 high", a["met"].tolist(), p["met"].tolist(), clip=clip)
    if zoom:
        if legend and legend_loc.startswith("upper"):
            yt = yb + (yt - yb) / 0.74
        ax.set_ylim(yb, yt)
    else:
        ax.set_ylim(0, hi * 1.1)
    ax.set_ylabel(ylabel)
    cohort_axis(ax)
    if legend:
        legend_5a(ax, legend_loc)
    return a, p


def balance_panel(bal, level, name, ylabel, zoom=False, legend=False, legend_loc="upper center"):
    fig, ax = frame(name)
    a, p = balance_axes(ax, bal, level, ylabel, zoom, legend, legend_loc)
    finish(fig, name)
    pd.concat([a.assign(base="all designs"), p.assign(base="actively protected")]).to_csv(OUT / name.replace(".pdf", ".csv"), index=False)


def disparity_panel(dis, level, name):
    a, p = pick_dis(dis, level, "all designs"), pick_dis(dis, level, "actively protected")
    fig, ax = frame(name)
    two_series(ax, a, p, "ΔQ", "ΔQ permutation low", "ΔQ permutation high", None, None, a["met"].tolist(), p["met"].tolist())
    ax.axhline(0, color=REF, linewidth=0.5, zorder=2)
    top = float(np.nanmax(pd.concat([a[["ΔQ permutation high", "ΔQ"]], p[["ΔQ permutation high", "ΔQ"]]]).to_numpy()))
    bot = float(np.nanmin(pd.concat([a[["ΔQ permutation low", "ΔQ"]], p[["ΔQ permutation low", "ΔQ"]]]).to_numpy()))
    pad = 0.06 * (top - bot)
    ax.set_ylim(bot - pad, top + pad)
    ax.set_ylabel("ΔQ against the two earliest cohorts")
    cohort_axis(ax)
    finish(fig, name)
    pd.concat([a.assign(base="all designs"), p.assign(base="actively protected")]).to_csv(OUT / name.replace(".pdf", ".csv"), index=False)


def balance_three(bal, name="fig5abc_balance_three_levels.pdf", width_mm=183.0):
    """The three balance panels (A, A·W·T, A·U) side by side in one figure of two-column width; the same graph, ticks and 7 pt text as
    the single panels. Written in addition to fig5a/b/c (each of those stays a separate 85 x 65 mm file)."""
    fig = plt.figure(figsize=(width_mm / 25.4, H_IN))
    cell = 1 / 3
    names = {"A0": "A", "A1t": "A·W·T", "A0c": "A·U"}
    for k, level in enumerate(("A0", "A1t", "A0c")):
        ax = fig.add_axes([k * cell + 0.052, 0.215, cell - 0.075, 0.665])
        balance_axes(ax, bal, level, f"²D at {names[level]}", zoom="tight" if level in ("A0", "A1t") else True, legend=False)
        ax.set_xticklabels(["≤11", "12–15", "16–19", "20–23", "24–26*"])      # shorter labels: the panels are narrower than a single column
    fig.legend(handles=legend_handles(), loc="upper center", bbox_to_anchor=(0.5, 0.995), ncol=6, frameon=False, handlelength=2.0,
               columnspacing=1.2, handletextpad=0.5, fontsize=FS)
    finish(fig, name)


def thesis_reading_dis(dis, level_name="A"):
    """Disparity in the reading of the thesis (Table 4): the protected designs against the baseline and the band of ALL designs.
    2020-23 is the value of percentiles_disparity_protected_vs_all.csv (Table 4). The other cohorts of the line are the Q of the protected
    designs of the cohort (percentiles_disparity.csv, base 'actively protected') minus the same all-designs baseline."""
    a = pick_dis(dis, "A0", "all designs")
    t = pd.read_csv(FF / "percentiles_disparity_protected_vs_all.csv").set_index("level").loc[level_name]
    q = pick_dis(dis, "A0", "actively protected")
    p = a.copy()
    p["Q"] = q["Q"].to_numpy()
    p["ΔQ"] = p["Q"] - a["Q of the earliest windows"]
    p.loc[3, "ΔQ"] = float(t["ΔQ"])
    p["met"] = False
    p.loc[3, "met"] = bool(t["below band"])
    return a, p


def disparity_thesis_reading(dis, name="fig5d_disparity.pdf"):
    a, p = thesis_reading_dis(dis)
    fig, ax = frame(name)
    two_series(ax, a, p, "ΔQ", "ΔQ permutation low", "ΔQ permutation high", None, None, a["met"].tolist(), p["met"].tolist(), prot_band=False)
    ax.axhline(0, color=REF, linewidth=0.5, zorder=2)
    top = float(np.nanmax(pd.concat([a[["ΔQ permutation high", "ΔQ"]], p[["ΔQ"]]]).to_numpy()))
    bot = float(np.nanmin(pd.concat([a[["ΔQ permutation low", "ΔQ"]], p[["ΔQ"]]]).to_numpy()))
    pad = 0.06 * (top - bot)
    ax.set_ylim(bot - pad, top + pad)
    ax.set_ylabel("ΔQ against the two earliest cohorts")
    cohort_axis(ax)
    LOG.append("fig5d: every protected point (all five cohorts) is read against the ALL-DESIGNS baseline (mean Q of the two earliest cohorts of all designs, "
               f"{float(a['Q of the earliest windows'].iloc[0]):.4f}) and the all-designs permutation band, as in Table 4. 2020-23 is the Table 4 value "
               f"({float(p.loc[3, 'ΔQ']):.4f}); the other four are Q of the protected designs of the cohort minus that baseline (no protected-own baseline is used). "
               "The two earliest cohorts (<= 2011, 2012-15) form the baseline of ΔQ and are not tested; 2024-26* is incomplete and untested.")
    finish(fig, name)
    pd.concat([a.assign(base="all designs", **{"baseline used": "all designs"}),
               p.assign(base="actively protected, against the all-designs baseline and band", **{"baseline used": "all designs"})]).to_csv(OUT / name.replace(".pdf", ".csv"), index=False)


def fig5(bal, dis):
    ylab = "Effective number of configurations, ²D"
    for key, (level, name) in LEVELS.items():
        balance_panel(bal, level, name, ylab, zoom="tight" if level in ("A0", "A1t") else True, legend=level == "A0")     # 5a, 5b: tight y axis (bands stay whole); 5c: whole range; legend in 5a only
    balance_three(bal)
    disparity_thesis_reading(dis, "fig5d_disparity.pdf")      # the reading of the thesis (Table 4): protected designs against the all-designs baseline and band


def fig7(ctx, bal, dis):
    from lib import dominant_design as dd
    f = pd.read_csv(CSV / "q7_condition1_family.csv")
    f = f[f["priority year"].between(2016, 2023)]
    fig, ax = frame("fig7a")
    yrs = f["priority year"].astype(int).to_numpy()
    sa, sp = f["F share"].to_numpy(float) * 100, f["F share in force"].to_numpy(float) * 100
    ax.plot(yrs, sp, marker="o", color=C_PROT, markerfacecolor=C_PROT, markeredgecolor=C_PROT, zorder=4)
    ax.plot(yrs, sa, marker="o", color=F_COLOR, zorder=4.1)
    for share, ms in ((sa, 6.0), (sp, 8.0)):
        met = sorted(dd.condition1_years(pd.DataFrame({"priority year": yrs, "read": True, "above 50 %": share > 50})))
        for yr in met:
            ring(ax, yr, share[list(yrs).index(yr)], ms)
    ax.axhline(50, color=REF, linewidth=0.7, zorder=2)          # solid: dashed grey means "untested" in Fig 5
    ax.text(yrs[0] - 0.4, 51, "50 % threshold", ha="left", va="bottom", fontsize=FS, color=REF)
    top = float(sa.max())
    iy = int(np.argmax(sa))
    ax.annotate(f"{top:.1f} %", (yrs[iy], top), xytext=(yrs[iy] + 0.0, 33), ha="center", va="top", fontsize=FS, color=F_COLOR,
                arrowprops=dict(arrowstyle="-", color=F_COLOR, lw=0.5, shrinkA=1, shrinkB=3))
    ax.set_xlim(yrs[0] - 0.5, yrs[-1] + 0.5)
    ax.set_xticks(yrs)
    ax.set_xticklabels([str(y) if (y - yrs[0]) % 2 == 0 else "" for y in yrs])
    ax.set_ylim(0, 75)
    ax.set_yticks([0, 20, 40, 60])
    ax.set_ylabel("share of designs in F (%)")
    ax.set_xlabel("priority year")
    ax.grid(axis="y", color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)
    ax.legend(handles=[Line2D([], [], color=C_ALL, marker="o", markerfacecolor=C_ALL, label="All designs"),
                       Line2D([], [], color=C_PROT, marker="o", markerfacecolor=C_PROT, label="Protected designs"),
                       Line2D([], [], marker="o", markerfacecolor="none", markeredgecolor=RED, markeredgewidth=1.1, linestyle="none", label="Protected designs, two years above 50 %")],
              loc="lower center", ncol=1, frameon=False, handlelength=2.0, columnspacing=1.0, labelspacing=0.3, borderaxespad=0.0, handletextpad=0.5, fontsize=FS)
    met_a = sorted(dd.condition1_years(pd.DataFrame({"priority year": yrs, "read": True, "above 50 %": sa > 50})))
    met_p = sorted(dd.condition1_years(pd.DataFrame({"priority year": yrs, "read": True, "above 50 %": sp > 50})))
    LOG.append("fig7a: red ring = protected designs in a pair of consecutive priority years above 50 % (years " + ", ".join(map(str, met_p)) + "). "
               + ("The all-designs series does not meet the condition (no two consecutive years above 50 %), so it has no ring." if not met_a else
                  "CHECK: the all-designs series also meets the condition in " + ", ".join(map(str, met_a)) + "."))
    finish(fig, "fig7a_F_share.pdf")
    f[["priority year", "F share", "F share in force"]].to_csv(OUT / "fig7a_F_share.csv", index=False)
    balance_panel(bal, "family_b", "fig7b_F_balance.pdf", "Effective number of configurations, ²D", legend=True, legend_loc="lower center")


def fig7c(dataset_root: Path):
    """Disparity inside F, 120 x 170 mm: legend on top; a simple panel of ΔQ of F against its band per cohort (test2_summary.csv, architecture
    weight 0); below it ΔQ per dimension (test2_explore_per_dimension.csv). The two panels share the ΔQ axis."""
    d = dataset_root / "07_results" / "72_weight_sensitivity"
    if not (d / "test2_explore_per_dimension.csv").exists() or not (d / "test2_summary.csv").exists():
        LOG.append("fig7c: test2_explore_per_dimension.csv or test2_summary.csv not found: not made")
        return False
    t = pd.read_csv(d / "test2_explore_per_dimension.csv")
    sm = pd.read_csv(d / "test2_summary.csv").set_index("cohort")
    cohorts = (("2016-19", "o", "2016–19"), ("2020-23", "s", "2020–23"))
    Wmm, Hmm = 120.0, 170.0
    fig = plt.figure(figsize=(Wmm / 25.4, Hmm / 25.4))
    ax_d = fig.add_axes([0.45, 0.062, 0.52, 0.665])        # wider left margin: the longest label is "Primary wing longitudinal position"
    ax_c = fig.add_axes([0.45, 0.805, 0.52, 0.135], sharex=ax_d)
    ax_d.set_label("fig7c")
    mk = dict(linestyle="none", markersize=4.4, color=C_ALL, markerfacecolor=C_ALL, markeredgewidth=0.8, zorder=4)
    ek = dict(linestyle="none", marker="|", markersize=6.5, color=C_UNT, markeredgewidth=1.3, zorder=3)
    # panel on top: F as a whole, one row per cohort
    for k, (coh, m, _) in enumerate(cohorts):
        yy = 1 - k
        ax_c.plot([sm.loc[coh, "baseline (architecture 0): dQ"]], [yy], marker=m, **mk)
        ax_c.plot([sm.loc[coh, "baseline: band edge"]], [yy], **ek)
    ax_c.set_yticks([1, 0])
    ax_c.set_yticklabels([c[2] for c in cohorts])
    ax_c.set_ylim(-0.6, 1.6)
    ax_c.tick_params(axis="y", length=0)
    ax_c.tick_params(axis="x", labelbottom=False)
    ax_c.set_xlabel("")
    # panel below: per dimension
    n = len(t)
    y = np.arange(n)[::-1]
    for coh, m, _ in cohorts:
        off = 0.19 if coh == "2016-19" else -0.19
        ax_d.plot(t[f"{coh}: dQ"], y + off, marker=m, **mk)
        ax_d.plot(t[f"{coh}: band edge"], y + off, **ek)
    ax_d.set_yticks(y)
    missing = [d for d in t["dimension"] if d not in DIM_LABELS]
    assert not missing, f"fig7c: no paper label for {missing}"
    ax_d.set_yticklabels([DIM_LABELS[d] for d in t["dimension"]])
    ax_d.set_ylim(-0.7, n - 0.3)
    ax_d.set_xlabel("ΔQ inside F, architecture weight 0")
    for a_ in (ax_c, ax_d):
        a_.axvline(0, color=REF, linewidth=0.5, zorder=1)
        a_.grid(axis="x", color=GRID, linewidth=0.5)
        a_.set_axisbelow(True)
    ax_d.tick_params(axis="y", length=0)
    hs = [Line2D([], [], color=C_ALL, marker="o", markerfacecolor=C_ALL, linestyle="none", label="2016–19"),
          Line2D([], [], color=C_ALL, marker="s", markerfacecolor=C_ALL, linestyle="none", label="2020–23"),
          Line2D([], [], color=C_UNT, marker="|", markersize=6.5, markeredgewidth=1.3, linestyle="none", label="Lower edge of band")]
    fig.legend(handles=hs, loc="upper center", bbox_to_anchor=(0.5, 0.995), ncol=3, frameon=False, handletextpad=0.4, columnspacing=1.6, fontsize=FS)
    edge, dq = sm["baseline: band edge"], sm["baseline (architecture 0): dQ"]
    above = bool((dq > edge).all()) and bool((t["2016-19: dQ"] > t["2016-19: band edge"]).all()) and bool((t["2020-23: dQ"] > t["2020-23: band edge"]).all())
    LOG.append("fig7c: EXPLORATORY check of ΔQ inside F (architecture weight 0), 120 x 170 mm; top panel = ΔQ of F per cohort against the lower edge of its permutation band "
               "(test2_summary.csv), bottom panel = per dimension (test2_explore_per_dimension.csv); circle 2016-19, square 2020-23, grey tick = lower band edge. "
               + ("It shows no convergence inside F: both cohorts (and every dimension) sit above the lower band edge." if above else
                  "CHECK: some point is not above the lower band edge."))
    finish(fig, "fig7c_exploratory_check_dQ_inside_F.pdf")
    t.assign(**{"figure label": t["dimension"].map(DIM_LABELS)}).to_csv(OUT / "fig7c_exploratory_check_dQ_inside_F.csv", index=False)
    sm[["baseline (architecture 0): dQ", "baseline: band edge"]].to_csv(OUT / "fig7c_exploratory_check_dQ_inside_F_by_cohort.csv")
    return True


# ---------------------------------------------------------------------------------------------------------------- Fig 6
def fig6(ctx):
    from viz import figures_part2 as p2
    from viz import frames, thesis_q6 as q6
    from viz import thesis_latex_part4 as p4
    import thesis_style as ts
    pmix = q6._data(ctx)["pmix5"]
    wins = list(ctx.WIN_NAMES)
    k = len(wins)
    cols = {"SLC": ("fig6a_modal_SLC.pdf", "fig6_legend_SLC.pdf"), "TR": ("fig6b_modal_TP.pdf", "fig6_legend_TP.pdf"),
            "CVT": ("fig6c_modal_CVT.pdf", "fig6_legend_CVT.pdf")}
    rows = []
    for c, (fname, lname) in cols.items():
        col = p4.TS_COL[c]
        m = pmix[pmix["code"] == c]
        lastw = m[m["window"] == "2020-23"].sort_values("aircraft", ascending=False)
        ordc = [kk for kk in lastw["configuration"] if not frames.cfg_outside(kk)]
        keep = ordc[:3] if len(ordc) > 4 else ordc[:4]
        frac = lambda kk: (m[m["configuration"].isin(kk)].groupby("window")["aircraft"].sum().reindex(wins).fillna(0)       # noqa: E731
                           / m.groupby("window")["class aircraft"].first().reindex(wins))
        comp = pd.DataFrame({p4.LAYOUT_NAME[kk]: frac([kk]) for kk in keep})
        rest = frac([kk for kk in m["configuration"].unique() if kk not in keep])
        if rest.sum() > 0:
            comp[p4.OTHER_NAME[c]] = rest
        ns = m.groupby("window")["class aircraft"].first().reindex(wins).to_numpy()
        looks = p4._layout_looks(col)
        fig, ax = frame(fname)
        bottom = np.zeros(k)
        handles = []
        for i, name in enumerate(comp.columns):
            vals = comp[name].fillna(0).to_numpy(float)
            face, hatch, hcol = (p4.OTHER_FILL, "", None) if name == p4.OTHER_NAME[c] else looks[min(i, len(looks) - 1)]
            for xi in range(k):
                if vals[xi] <= 0:
                    continue
                inc = xi == k - 1
                ax.bar(xi, vals[xi] * 100, bottom=bottom[xi] * 100, width=0.78, color=face, edgecolor=hcol or "white", hatch=hatch,
                       linewidth=0 if hatch else 0.4, alpha=p4.LAYOUT_INC_ALPHA if inc else 1.0, zorder=3)
                if hatch:
                    ax.bar(xi, vals[xi] * 100, bottom=bottom[xi] * 100, width=0.78, fill=False, edgecolor="white", linewidth=0.4, zorder=3.5)
                if vals[xi] >= 0.08:
                    ink = p2.ts_ink_on(face) if not inc else "#1a1a1a"
                    ax.text(xi, (bottom[xi] + vals[xi] / 2) * 100, f"{100 * vals[xi]:.0f}", ha="center", va="center", fontsize=FS, color=ink,
                            alpha=0.85 if inc else 1.0, zorder=5,
                            bbox=dict(boxstyle="square,pad=0.05", fc=p2.ts_tint(col, 0.14), ec="none") if hatch else None)
            bottom = bottom + vals
            handles.append((name, face, hatch, hcol))
            rows.append(pd.DataFrame({"architecture": c, "layout": name, "cohort": wins, "share": vals, "designs of the architecture": ns}))
        cohort_axis(ax, ns)
        ax.set_xlim(-0.5, k - 0.5)
        ax.set_ylim(0, 100)
        ax.set_yticks([0, 20, 40, 60, 80, 100])
        ax.set_ylabel("share of the architecture's designs (%)")
        ax.grid(False)
        ax.axvline(1.5, color=REF, linewidth=0.5, linestyle=(0, (3, 2)), zorder=4)
        finish(fig, fname)
        legend_strip(lname, handles[::-1])
    pd.concat(rows).to_csv(OUT / "fig6_modal_layouts.csv", index=False)


def legend_strip(name, handles):
    """The categories of one panel, top to bottom as stacked, in two columns; 85 mm wide."""
    h_mm = 4.4 * ((len(handles) + 1) // 2) + 2.0
    fig = plt.figure(figsize=(W_IN, h_mm / 25.4))
    hs = [mpl.patches.Patch(facecolor=f, edgecolor=hc or "none", hatch=ha, linewidth=0, label=n) for n, f, ha, hc in handles]
    fig.legend(handles=hs, loc="center", ncol=2, frameon=False, handlelength=1.4, handleheight=1.0, columnspacing=1.4, labelspacing=0.35,
               fontsize=FS, borderaxespad=0.1)
    finish(fig, name)


# ---------------------------------------------------------------------------------------------------------------- comparison
def compare(bal, dis, perms):
    """The values and bands against the tables the notebooks wrote (freeze/csv): all-designs series of Fig 5 and F."""
    out = []
    b0 = pd.read_csv(CSV / "q7_condition2_balance.csv")
    lv = {"A0": "A", "A1t": "A·W·T", "A0c": "A·U"}
    for lid, nm in lv.items():
        a = pick_bal(bal, lid, "all designs").set_index("window")
        r = b0[b0["level"] == nm].set_index("cohort")
        for w in WIN:
            for col, key in (("D2", "D2"), ("D2 permutation low", "D2 permutation low"), ("D2 permutation high", "D2 permutation high")):
                if w in r.index:
                    out.append(dict(figure=f"fig5 balance {nm}", cohort=w, quantity=col, new=a.loc[w, col], notebooks=r.loc[w, key]))
    c0 = pd.read_csv(CSV / "q7_condition3_cohesion.csv")
    a = pick_dis(dis, "A0", "all designs").set_index("window")
    r = c0[(c0["level"].isin(["A", "A0"])) & (c0.get("weighting", "w15") == "w15")].drop_duplicates("cohort").set_index("cohort") if "cohort" in c0 else None
    if r is not None:
        for w in WIN:
            if w in r.index:
                for col in ("ΔQ", "ΔQ permutation low", "ΔQ permutation high"):
                    out.append(dict(figure="fig5d disparity", cohort=w, quantity=col, new=a.loc[w, col], notebooks=r.loc[w, col]))
    fc = pd.read_csv(CSV / "q7_family_conditions.csv")
    out_df = pd.DataFrame(out)
    out_df["difference"] = out_df["new"].astype(float) - out_df["notebooks"].astype(float)
    out_df["permutations in the new bands"] = perms
    out_df.to_csv(OUT / "comparison_with_notebooks.csv", index=False)
    return out_df, fc


def main():
    import os
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None, choices=["fig4", "fig5", "fig6", "fig7"])
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    from viz import config, thesis
    cfg = config.load()
    ctx = thesis.context(cfg)
    bal, dis, perms = load_tables()
    todo = a.only or ["fig4", "fig5", "fig6", "fig7"]
    with rc():
        if "fig4" in todo:
            fig4(ctx)
        if "fig5" in todo:
            fig5(bal, dis)
        if "fig6" in todo:
            fig6(ctx)
        if "fig7" in todo:
            fig7(ctx, bal, dis)
            root = Path(os.environ.get("EVTOL_DATASET", REPO.parent / "eVTOL_dataset"))
            fig7c(root)
    cmp_, _ = compare(bal, dis, perms)
    big = cmp_[(cmp_["difference"].abs() > 1e-9)]
    (OUT / "log.txt").write_text(f"permutations behind the bands: {perms}\nfigures: {todo}\n" + "\n".join(LOG) +
                                 f"\nvalues/bands that differ from the notebooks' tables: {len(big)} of {len(cmp_)}\n", encoding="utf-8")
    print(f"permutations behind the bands: {perms}")
    print("\n".join(LOG))
    print(f"differences vs notebooks' tables: {len(big)} of {len(cmp_)}")
    if len(big):
        print(big.to_string())


if __name__ == "__main__":
    main()
