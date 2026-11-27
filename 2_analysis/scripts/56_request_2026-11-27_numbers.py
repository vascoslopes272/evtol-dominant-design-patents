"""Numbers asked for on 2026-11-27 (paper P1 pre-submission check): cohort sizes, 2020-23 shares at three levels on both bases,
the Boom count dimension, the five extra disparity dimensions. Nothing is changed in the dataset.

    EVTOL_DATASET=<path to eVTOL_dataset> python 56_request_2026-11-27_numbers.py
Writes results/2_analysis/pending_numbers/pending_csv/R56_*.csv and prints the tables.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
import core  # noqa: E402

OUT = REPO / "results" / "2_analysis" / "pending_numbers" / "pending_csv"
pd.set_option("display.width", 250, "display.max_columns", 40)
base = core.load()
ctx = core.context(base, base.master)
fr, v = base.m.frames, ctx.v
live = v["aircraft_id"].map(fr.patent_state(ctx.ds, v)["in_force"]).astype(bool)      # in force or under examination
keys = fr.dd_level_keys(ctx.ds, v)
LV = {"A": "A0", "A·W·T": "A1t", "A·U": "A0c"}

# 1. designs per cohort
t1 = pd.DataFrame({"all designs": v.groupby("window").size(), "all, architecture known": v[v.topType.notna()].groupby("window").size(),
                   "protected": v[live].groupby("window").size(), "protected, architecture known": v[live & v.topType.notna()].groupby("window").size()})
t1 = t1.loc[["<= 2011", "2012-15", "2016-19", "2020-23", "2024-26 (partial)"]]
t1.loc["total"] = t1.sum()
t1.to_csv(OUT / "R56_1_designs_per_cohort.csv")
print(t1, "\nno architecture:", v.loc[v.topType.isna(), ["aircraft_id", "window"]].to_dict("records"))

# 2. share of the largest configuration, cohort 2020-23 and best single year inside it
rows = []
for lvl, lid in LV.items():
    k = keys[lid]
    for bname, mask in (("all designs", pd.Series(True, index=v.index)), ("protected", live)):
        s = v[mask & k.notna() & v.window.eq("2020-23")].assign(k=k)
        vc = s["k"].value_counts()
        yr = []
        for y in (2020, 2021, 2022, 2023):
            sy = v[mask & k.notna() & v.year.eq(y)].assign(k=k)
            vy = sy["k"].value_counts()
            yr.append((vy.iloc[0] / len(sy), y, fr._key_words(vy.index[0], lid), int(vy.iloc[0]), len(sy), int((vy == vy.iloc[0]).sum())))
        b = max(yr)
        rows.append({"level": lvl, "base": bname, "designs in cohort": len(s), "largest configuration (cohort)": fr._key_words(vc.index[0], lid),
                     "its designs": int(vc.iloc[0]), "its share in cohort": round(vc.iloc[0] / len(s), 4),
                     "best single-year share": round(b[0], 4), "year": b[1], "configuration": b[2], "designs": f"{b[3]} of {b[4]}", "tied at top that year": b[5]})
t2 = pd.DataFrame(rows)
t2.to_csv(OUT / "R56_2_2020_23_largest_configuration.csv", index=False)
print(t2.to_string())

# 4 and 5. dimensions of the 15-dimension distance (designs with an architecture, 619)
f15 = fr.form_frame15(ctx.ds)
rows = []
for c in ["Boom count", "Vertical Position", "Longitudinal Position", "Planform", "Tilt share", "Tractor/Pusher Arrangement"]:
    s = f15[c].dropna()
    vc = s.value_counts()
    rows.append({"dimension": c, "designs answering (of 621)": len(s), "options": len(vc), "most common": str(vc.index[0]), "its designs": int(vc.iloc[0]),
                 "top share": round(vc.iloc[0] / len(s), 4), "below 80 %": bool(vc.iloc[0] / len(s) < 0.8)})
    if c == "Vertical Position":
        s2 = s[s != "Unknown"]
        vc2 = s2.value_counts()
        rows.append({"dimension": "Vertical Position, 'Unknown' left out", "designs answering (of 621)": len(s2), "options": len(vc2), "most common": vc2.index[0],
                     "its designs": int(vc2.iloc[0]), "top share": round(vc2.iloc[0] / len(s2), 4), "below 80 %": bool(vc2.iloc[0] / len(s2) < 0.8)})
t4 = pd.DataFrame(rows)
t4.to_csv(OUT / "R56_4_5_dimensions.csv", index=False)
print(t4.to_string())
print("Boom count ranks:", f15["Boom count"].value_counts().sort_index().to_dict(), "(0, 1, 2, 3-4, 5+)")
print("Tilt share: share of designs at 0 =", round(float((f15['Tilt share'].dropna() == 0).mean()), 3))
vv = ctx.ds.variants
bc = [c for c in vv.columns if re.match(r"boom\d_count$", c)]
n = vv[bc].apply(pd.to_numeric, errors="coerce").fillna(0).sum(axis=1)
bp = vv["boomsPresent"].astype(str).eq("True")
print("boomsPresent recorded:", vv["boomsPresent"].notna().sum(), "of", len(vv), "; True", int(bp.sum()), "; True with no boom count:", int((bp & (n == 0)).sum()))
