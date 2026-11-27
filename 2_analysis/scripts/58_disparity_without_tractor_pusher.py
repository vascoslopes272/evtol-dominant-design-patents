"""Disparity (condition 3) with and without the tractor/pusher dimension (14 against 15 dimensions), 2020-23.

    EVTOL_DATASET=<path to eVTOL_dataset> python 58_disparity_without_tractor_pusher.py [--perms 10000]

Same functions as the paper: frames.form_distance for the 15 dimensions; for the 14 the same frame and weights with the weight of 'Tractor/Pusher Arrangement'
set to 0 (blanks and zero weights leave a dimension out of both sums of the Gower distance, so the other weights are used as they are).
Bands: cohesion_band's procedure (shuffle the designs, cut into blocks of the cohort sizes, 2.5 / 97.5 percentiles), seed 42, a fresh generator per level,
with the percentile of the observed value added. Three readings per level: all designs; protected designs against their own baseline and band;
protected designs of 2020-23 against the all-designs baseline and band (the reading of the paper, as analysis_iii.form_ap_vs_all).
Family F (Lift + Cruise + CVT* family), architecture weight 0: its designs of 2016-19 and 2020-23 against the mean Q of its two earliest cohorts, the
10 000 shuffles of test 2 (all F designs shuffled into the five cohort sizes) (eVTOL_dataset/07_results/72_weight_sensitivity/test2_summary.csv).
Writes results/2_analysis/pending_numbers/pending_csv/R58_*.csv.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
sys.path.insert(0, str(REPO / "2_analysis" / "src"))
import core  # noqa: E402
from lib import distance as _dist  # noqa: E402
from lib import dominant_design as dd  # noqa: E402

OUT = REPO / "results" / "2_analysis" / "pending_numbers" / "pending_csv"
ap = argparse.ArgumentParser()
ap.add_argument("--perms", type=int, default=10000)
ARGS = ap.parse_args()
PERMS = ARGS.perms
TP = "Tractor/Pusher Arrangement"
LVL = {"A0": "A", "A1t": "A·W·T", "A0c": "A·U"}

base = core.load()
ctx = core.context(base, base.master)
fr = base.m.frames
ds, v = ctx.ds, ctx.v
WIN = list(ctx.WIN_NAMES)
live = v["aircraft_id"].map(fr.patent_state(ds, v)["in_force"]).astype(bool)

fi = fr.gower_inputs(ds, "w15")
frame = fi.frame
at = {a: i for i, a in enumerate(frame["aircraft_id"].to_numpy())}


def distance(drop=(), arch0=False):
    w = dict(fi.weights)
    for d in drop:
        w[d] = 0.0
    if arch0:
        w["Architecture"] = 0.0
    return _dist.gower_distance(frame, fi.fields, fi.numeric, w, ranges=fi.ranges, sets=fi.sets)


D15 = distance()
D14 = distance(drop=(TP,))


def band_all(D, rows, windows, perms, seed=42):
    """cohesion_band with the percentile of the observed dQ."""
    rows = np.asarray(rows, int)
    win = pd.Series(np.asarray(windows, dtype=object))
    per = {w: rows[win.eq(w).to_numpy()] for w in WIN}
    obs = {w: dd.mean_pairwise_distance(D, r) for w, r in per.items() if len(r) >= 10}
    bw = WIN[:2]
    ref = float(np.mean([obs[w] for w in bw]))
    rng = np.random.default_rng(seed)
    band = {w: [] for w in obs}
    for _ in range(perms):
        sh = rng.permutation(rows)
        cut, drawn = 0, {}
        for w in WIN:
            n = len(per[w])
            drawn[w] = dd.mean_pairwise_distance(D, sh[cut:cut + n]) if n >= 10 else np.nan
            cut += n
        r0 = float(np.mean([drawn[w] for w in bw if w in obs]))
        for w in obs:
            band[w].append(drawn[w] - r0)
    res = {}
    for w in obs:
        arr = np.array(band[w])
        res[w] = dict(n=len(per[w]), Q=obs[w], ref=ref, dQ=obs[w] - ref, low=float(np.percentile(arr, 2.5)), high=float(np.percentile(arr, 97.5)),
                      pct=float(np.mean(arr <= obs[w] - ref) * 100))
    return res


def prot_vs_all(D, rows, windows, ap_mask, perms, seed=42, cohort="2020-23"):
    rows = np.asarray(rows, int)
    win = np.asarray(windows, dtype=object)
    per = {w: rows[win == w] for w in WIN}
    bw = WIN[:2]
    ref = float(np.mean([dd.mean_pairwise_distance(D, per[w]) for w in bw]))
    tgt = rows[(win == cohort) & ap_mask]
    q = dd.mean_pairwise_distance(D, tgt)
    sizes = {w: (len(tgt) if w == cohort else len(per[w])) for w in WIN}
    rng, band = np.random.default_rng(seed), []
    for _ in range(perms):
        sh, cut, drawn = rng.permutation(rows), 0, {}
        for w in WIN:
            drawn[w] = dd.mean_pairwise_distance(D, sh[cut:cut + sizes[w]])
            cut += sizes[w]
        band.append(drawn[cohort] - np.mean([drawn[w] for w in bw]))
    band = np.array(band)
    return dict(n=len(tgt), Q=q, ref=ref, dQ=q - ref, low=float(np.percentile(band, 2.5)), high=float(np.percentile(band, 97.5)),
                pct=float(np.mean(band <= q - ref) * 100))


rows_out = []
for lid, lname in LVL.items():
    k = fr.archetype_key(v, lid)
    sub = v[k.notna()].dropna(subset=["window"]).copy()
    sub["row"] = sub["aircraft_id"].map(at)
    sub = sub[sub["row"].notna()]
    rows, win = sub["row"].astype(int).to_numpy(), sub["window"].to_numpy()
    apm = live[sub.index].to_numpy()
    for dname, D in (("15 dimensions", D15), ("14 dimensions, without tractor/pusher", D14)):
        r = band_all(D, rows, win, PERMS)["2020-23"]
        rows_out.append(dict(reading="all designs", level=lname, dimensions=dname, **r))
        sel = apm
        r = band_all(D, rows[sel], win[sel], PERMS)["2020-23"]
        rows_out.append(dict(reading="protected designs, own baseline and band", level=lname, dimensions=dname, **r))
        r = prot_vs_all(D, rows, win, apm, PERMS)
        rows_out.append(dict(reading="protected designs of 2020-23, baseline and band of all designs (the paper)", level=lname, dimensions=dname, **r))
        print(lname, dname, "done", flush=True)
T = pd.DataFrame(rows_out)
T["below band"] = T["dQ"] < T["low"]
T = T.rename(columns={"n": "designs", "ref": "baseline Q0", "low": "band low edge", "high": "band high edge", "pct": "percentile"})
T.round(4).to_csv(OUT / "R58_disparity_14_vs_15.csv", index=False)
print(T.round(4).to_string())

# family F, architecture weight 0, against the mean of Q of its two earliest cohorts. As in test 2 (p1_tests.py, ws_core.engine) Q of a set is the ratio of sums
# sum(N) / sum(V) over the pairs of the set (N = weighted mismatch, V = weight of the dimensions both designs answer), not the mean of the pair distances.
flags = fr.family_flags(ds, v)
fam = set(flags.loc[fr.family_mask(flags), "aircraft_id"])
fv = v[v["aircraft_id"].isin(fam) & v["topType"].notna()].dropna(subset=["window"])
fv = fv[fv["aircraft_id"].isin(at)]
frow = fv["aircraft_id"].map(at).astype(int).to_numpy()
fwin = fv["window"].to_numpy()
e1, e2 = frow[fwin == WIN[0]], frow[fwin == WIN[1]]
early = np.r_[e1, e2]
avail = np.column_stack([frame[f].notna().to_numpy(float) for f in fi.fields])
res = []
for dname, drop in (("15 dimensions, architecture weight 0", ()), ("14 dimensions, architecture weight 0, without tractor/pusher", (TP,))):
    w = dict(fi.weights)
    w["Architecture"] = 0.0
    for d in drop:
        w[d] = 0.0
    wv = np.array([w[f] for f in fi.fields], float)
    V = (avail * wv) @ avail.T
    Dm = _dist.gower_distance(frame, fi.fields, fi.numeric, w, ranges=fi.ranges, sets=fi.sets)
    N = np.nan_to_num(Dm * V)
    q = lambda i: float(N[np.ix_(i, i)].sum() / V[np.ix_(i, i)].sum())  # noqa: E731
    for c in ("2016-19", "2020-23"):
        cur = frow[fwin == c]
        dq = q(cur) - (q(e1) + q(e2)) / 2
        blocks = {ww: frow[fwin == ww] for ww in WIN}
        rng = np.random.default_rng(42)
        arr = np.empty(PERMS)
        for k in range(PERMS):          # all F designs shuffled into blocks of the five cohort sizes (as the engine of test 2)
            sh, cut, dr = rng.permutation(frow), 0, {}
            for ww in WIN:
                n = len(blocks[ww])
                dr[ww] = q(sh[cut:cut + n])
                cut += n
            arr[k] = dr[c] - (dr[WIN[0]] + dr[WIN[1]]) / 2
        res.append(dict(dimensions=dname, cohort=c, F_designs_in_cohort=len(cur), F_designs_earliest=f'{len(e1)} + {len(e2)}', dQ=dq, band_low_edge=float(np.percentile(arr, 2.5)),
                        percentile=float(np.mean(arr <= dq) * 100), below_band=bool(dq < np.percentile(arr, 2.5))))
F = pd.DataFrame(res)
F.round(4).to_csv(OUT / "R58_family_F_alone_14_vs_15.csv", index=False)
print(F.round(4).to_string())
