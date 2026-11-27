"""Pending part D, items 11 and 12 (paper P1): Asia-Pacific share of 2016-19, patents by priority year with the publication lag,
and the level step of 2016 in patent families against aeronautics (B64).

    EVTOL_DATASET=<eVTOL_dataset> PYTHONPATH=2_analysis/src python3 2_analysis/scripts/45_pending_D_items_11_12.py

Thesis functions unchanged (viz.frames, viz.thesis_q1, lib.growth, lib.growth_models). Seed 42. Writes CSVs to numbers/pending_csv/
and a JSON of values (scratch) for the markdown.
"""
from __future__ import annotations

import os as _os
from pathlib import Path as _Path
_REPO = _Path(__file__).resolve().parents[2]
_SUPP = _os.environ.get("SUPP_OUT", str(_REPO / "results" / "2_analysis" / "numbers"))
_DS = _os.environ.get("EVTOL_DATASET", str(_REPO.parent / "eVTOL_dataset"))
for _d in ("pending_csv", "supplementary_csv"):
    _os.makedirs(_os.path.join(_SUPP, _d), exist_ok=True)
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
import core  # noqa: E402

OUT = Path((_SUPP + "/pending_csv"))
OUT.mkdir(parents=True, exist_ok=True)


def main():
    base = core.load()
    ctx = core.context(base, base.master)
    m, ds, v, cfg = base.m, ctx.ds, ctx.v, base.cfg
    fr, q1 = m.frames, m.q1
    res = {}

    # ---------------- item 11a: Asia-Pacific share of the designs of 2016-19
    rows = []
    for w in ctx.WIN_NAMES:
        s = v[v["window"].eq(w)]
        n = len(s)
        for reg in fr.REGIONS + ["Other regions"]:
            k = int(s["region3"].eq(reg).sum())
            rows.append({"cohort": w, "region": reg, "designs": k, "designs in cohort (denominator)": n, "share": k / n})
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "D11a_region_share_per_cohort.csv", index=False)
    ap = t[(t.cohort == "2016-19") & (t.region == "Asia-Pacific")].iloc[0]
    res["ap_1619"] = dict(num=int(ap["designs"]), den=int(ap["designs in cohort (denominator)"]), share=float(ap["share"]))
    s = v[v["window"].eq("2016-19")]
    three = int(s["region3"].isin(fr.REGIONS).sum())
    res["ap_1619_three_regions_den"] = dict(den=three, share=res["ap_1619"]["num"] / three)
    res["ap_1619_with_architecture"] = dict(num=int((s["region3"].eq("Asia-Pacific") & s["topType"].notna()).sum()), den=int(s["topType"].notna().sum()))

    # ---------------- item 11b: patents by priority year and the publication lag
    j = fr.with_publication(ds, v)
    lagrow = fr.publication_lag(ds)                                     # one row per representative primary patent
    p90 = float(m.frames._growth.lag_quantile(lagrow["lag"])) if hasattr(m.frames, "_growth") else float(lagrow["lag"].quantile(0.9))
    res["p90_lag_unrounded"] = p90
    res["p90_lag_yaml"] = cfg.analysis["publication_lag_p90_years"]
    res["lag_patents_n"] = int(lagrow["lag"].notna().sum())
    res["lag_by_region"] = fr.publication_lag(ds, by="region").to_dict("records")
    fpy = fr.filings_per_year(ds, v, cfg)
    snap = fpy.attrs.get("snapshot")
    res["snapshot"] = str(snap)
    cols = ["unique aircraft", "patents acquired", "patents representative", "years since year end", "complete"]
    tab = fpy[cols].copy()
    pid = v.dropna(subset=["year"]).assign(year=lambda d: d["year"].astype(int)).groupby("year")["patent_id"].nunique()
    tab["primary patents behind the designs"] = pid.reindex(tab.index, fill_value=0).to_numpy()
    for c in ("unique aircraft", "patents acquired", "patents representative", "primary patents behind the designs"):
        tab[f"share of all years: {c}"] = tab[c] / tab[c].sum()
    # visibility of each year at the snapshot (the correction of frames.region_years / notebook 21): overall and per region
    S = int(pd.to_datetime(ds.identity["snapshot_date"].dropna().iloc[0]).year)
    frac = float(pd.to_datetime(ds.identity["snapshot_date"].dropna().iloc[0]).dayofyear / 365.0)
    jj = j[j["region3"].isin(fr.REGIONS)]
    ref = jj[jj["year"].between(2016, 2021)]
    vis = {"all three regions": m.frames._growth.visible_share(ref["lag"].dropna().to_numpy(), 0, 0) if False else None}
    from lib import growth as G
    def visf(lags, y):
        return G.visible_share(np.asarray(lags), S - y, frac)
    rows = []
    for y in range(2012, S + 1):
        r = {"priority year": y, "visible at the snapshot, all designs of three regions (reference 2016-21, n=%d)" % len(ref): visf(ref["lag"].dropna(), y)}
        for reg in fr.REGIONS:
            r[f"visible, {reg} (n ref={int(ref['region3'].eq(reg).sum())})"] = visf(ref.loc[ref["region3"].eq(reg), "lag"].dropna(), y)
        rows.append(r)
    visdf = pd.DataFrame(rows)
    visdf.to_csv(OUT / "D11c_visible_share_by_priority_year.csv", index=False)
    tab = tab.reset_index().rename(columns={"index": "priority year", "year": "priority year"})
    tab.to_csv(OUT / "D11b_patents_by_priority_year.csv", index=False)
    res["snapshot_year"] = S
    res["snapshot_fraction"] = frac
    res["lag_distribution_2016_21"] = ref["lag"].value_counts().sort_index().to_dict()
    res["ref_n"] = int(len(ref))
    lc = pd.read_csv(REPO / "results/2_analysis/freeze/csv/q1_filings_per_year_lag_corrected.csv")
    res["freeze_lag_corrected_2023"] = lc[lc["priority year"].eq(2023)].to_dict("records")

    # ---------------- item 12: level step of 2016 (patent families) against aeronautics
    c = q1._calc(ctx)
    gm = q1.growth_models(ctx)
    est = pd.concat([gm["tables"][last]["estimates"].assign(fit_last=last) for last in gm["tables"]], ignore_index=True)
    est = est[est["model"].str.startswith("(a)")]
    keep = ["series", "years", "fit_last", "break year", "break low", "break high", "level step (factor)", "step low", "step high"]
    est[[k for k in keep if k in est.columns]].to_csv(OUT / "D12a_level_step_model_a.csv", index=False)
    res["level_step"] = est[[k for k in keep if k in est.columns]].to_dict("records")
    # the turning point (a different procedure: jump factor at the SSE-minimising break, bootstrap share)
    rng = np.random.default_rng(ctx.SEED)
    d = c["fpy"] if "fpy" in c else None
    tp_rows = []
    try:
        tpd = c["tp"]
        for k, r in tpd.items():
            tp_rows.append({"series": k, "break": r["break"], "jump factor (unrounded)": float(r["jump"]), "share of resampled fits": float(r["share"]),
                            "low": r["lo"], "high": r["hi"]})
    except Exception as e:                                   # noqa: BLE001
        res["tp_error"] = repr(e)
    pd.DataFrame(tp_rows).to_csv(OUT / "D12b_turning_point_jump.csv", index=False)
    res["turning_point"] = tp_rows
    json.dump(res, open(OUT / "_D11_D12_values.json", "w"), indent=1, default=str)
    print(json.dumps(res, indent=1, default=str)[:6000])


if __name__ == "__main__":
    main()
