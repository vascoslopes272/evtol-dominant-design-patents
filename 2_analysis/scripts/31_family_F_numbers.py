"""Family F numbers for the paper (items 3b and 3d).

    EVTOL_DATASET=<path to eVTOL_dataset> python 31_family_F_numbers.py [--perms 10000] [--only b|d]

3b  Similarity of F to the rest. In 2020-23, for number of wings, propulsor band, wing configuration, tractor/pusher and booms:
    the top option inside F, its share inside F and outside F (all designs that answer), and a Fisher exact test of that option
    inside F against outside F. Written to results/2_analysis/family_F/F_vs_rest_2020_23.csv.
3d  For balance (condition 2) and disparity (condition 3), at every level, on both bases and in every cohort: the percentile of the
    observed value in its own permutation distribution (share of shuffles at or below the observed value; the test reads the low tail).
    The thesis functions balance_band and cohesion_band are used as they are, with one added line that keeps the percentile; the shuffles
    and the random numbers are the thesis's (seed 42), so the band edges equal those of notebook 23 when --perms 1000.
    Written to results/2_analysis/family_F/percentiles_balance.csv, percentiles_disparity.csv, percentiles_disparity_protected_vs_all.csv.

Seeds: 42 (thesis seed, ctx.SEED). Designs: the analysis table of the dataset (621 designs; 619 with an architecture enter the tests).
"""
from __future__ import annotations

import argparse
import inspect
import os
import sys
import textwrap
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
import core  # noqa: E402

OUT = REPO / "results" / "2_analysis" / "family_F"
COHORT = "2020-23"
DIMS = ["number of wings (winged designs)", "propulsor units per aircraft (band)", "wing configuration", "booms present"]


def b_similarity(base, ctx) -> pd.DataFrame:
    fr = base.m.frames
    ds, v = ctx.ds, ctx.v
    flags = fr.family_flags(ds, v)
    fam = set(flags.loc[fr.family_mask(flags), "aircraft_id"])
    series = fr.selected_field_series(ds)
    series["tractor / pusher"] = fr.form_frame15(ds).set_index("aircraft_id")["Tractor/Pusher Arrangement"]\
        .reindex(ds.variants["aircraft_id"]).set_axis(ds.variants.index)
    win = ds.variants["aircraft_id"].map(v.set_index("aircraft_id")["window"])
    has_arch = ds.variants["aircraft_id"].map(v.set_index("aircraft_id")["topType"]).notna()
    inF = ds.variants["aircraft_id"].isin(fam)
    rows = []
    for name in DIMS + ["tractor / pusher"]:
        s = series[name].astype(object).where(series[name].notna())
        ok = s.notna() & win.eq(COHORT) & has_arch
        f, r = s[ok & inF], s[ok & ~inF]
        top = f.value_counts().index[0]
        a, b_ = int((f == top).sum()), int(len(f) - (f == top).sum())
        c, d = int((r == top).sum()), int(len(r) - (r == top).sum())
        top_r = r.value_counts().index[0]
        rows.append({"dimension": name, "cohort": COHORT, "designs in F answering": len(f), "designs outside F answering": len(r),
                     "top option inside F": top, "its share inside F": round(a / len(f), 3), "its share outside F": round(c / len(r), 3),
                     "difference (F minus rest)": round(a / len(f) - c / len(r), 3),
                     "Fisher exact p": float(fisher_exact([[a, b_], [c, d]])[1]),
                     "top option outside F": top_r, "its share outside F (own top)": round(float((r == top_r).mean()), 3),
                     "same top option inside and outside": bool(top == top_r)})
    return pd.DataFrame(rows)


def _patched(func, old: str, new: str):
    src = textwrap.dedent(inspect.getsource(func))
    assert old in src, old
    ns = dict(func.__globals__)
    exec(src.replace(old, new), ns)                                    # noqa: S102 (the thesis function plus one added line)
    return ns[func.__name__]


def d_percentiles(base, ctx, perms: int) -> dict:
    import lib.dominant_design as dd
    from viz import analysis_iii, frames, thesis_q7
    m = base.m
    thesis_q7.PERMS = perms
    dd.balance_band = _patched(
        dd.balance_band, '        r["D2 permutation low"] = round(float(np.percentile(b, 2.5)), 2)',
        '        r["percentile of the observed D2 (share of shuffles at or below)"] = round(float(np.mean(b <= r["D2"]) * 100), 1)\n'
        '        r["D2 permutation low"] = round(float(np.percentile(b, 2.5)), 2)')
    dd.cohesion_band = _patched(
        dd.cohesion_band, '        out.append({"window": w, "aircraft": int(len(per[w])), "Q": round(obs[w], 4),',
        '        out.append({"percentile of the observed dQ (share of shuffles at or below)": round(float(np.mean(arr <= obs[w] - ref) * 100), 1),\n'
        '                    "window": w, "aircraft": int(len(per[w])), "Q": round(obs[w], 4),')
    frames._dd = dd
    v = ctx.v
    live = v["aircraft_id"].map(frames.patent_state(ctx.ds, v)["in_force"]).astype(bool)
    res = {}
    n = ctx.cfg.analysis["rarefy_n"]
    for base_name, vv in (("all designs", v), ("actively protected", v[live])):
        bal = frames.dd_balance_table(ctx.ds, vv, ctx.WIN_NAMES, n, perms, ctx.SEED)
        frm = frames.dd_form_table(ctx.ds, vv, ctx.WIN_NAMES, perms, ctx.SEED)
        res.setdefault("balance", []).append(bal.assign(base=base_name))
        res.setdefault("disparity", []).append(frm.assign(base=base_name))
    # protected designs of 2020-23 against the all-designs baseline and band (the reading of Table 4, section 3.4.4)
    src = textwrap.dedent(inspect.getsource(analysis_iii.form_ap_vs_all))
    src = src.replace('out.append({"level": _LVL[lvl], "cohort": cohort,',
                      'out.append({"percentile of the observed dQ (share of shuffles at or below)": round(float(np.mean(np.array(band) <= q - ref) * 100), 1), '
                      '"level": _LVL[lvl], "cohort": cohort,')
    src = src.replace('    if getattr(ctx, "_a3_ap_all", None) is not None and cohort == "2020-23":\n        return ctx._a3_ap_all\n', "")
    src = src.replace('    if cohort == "2020-23":\n        ctx._a3_ap_all = t\n', "")
    ns = dict(analysis_iii.__dict__)
    exec(src, ns)                                                     # noqa: S102
    res["protected_vs_all"] = ns["form_ap_vs_all"](ctx)
    return {"balance": pd.concat(res["balance"], ignore_index=True), "disparity": pd.concat(res["disparity"], ignore_index=True),
            "protected_vs_all": res["protected_vs_all"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--perms", type=int, default=10000)
    ap.add_argument("--only", choices=("b", "d"))
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    base = core.load()
    ctx = core.context(base, base.master)
    if a.only in (None, "b"):
        t = b_similarity(base, ctx)
        t.to_csv(OUT / "F_vs_rest_2020_23.csv", index=False)
        print(t.to_string())
    if a.only in (None, "d"):
        r = d_percentiles(base, ctx, a.perms)
        r["balance"].to_csv(OUT / "percentiles_balance.csv", index=False)
        r["disparity"].to_csv(OUT / "percentiles_disparity.csv", index=False)
        r["protected_vs_all"].to_csv(OUT / "percentiles_disparity_protected_vs_all.csv", index=False)
        (OUT / "run_note.txt").write_text(f"permutations per band: {a.perms}\nseed: {ctx.SEED}\ndesigns in the table: {len(ctx.v)}\n")
        print(r["balance"].head(12).to_string())


if __name__ == "__main__":
    main()
