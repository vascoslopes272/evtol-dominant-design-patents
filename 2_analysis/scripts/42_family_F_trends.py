"""Item 10 (pending B/C): trends inside family F alone.

    EVTOL_DATASET=<path to eVTOL_dataset> PYTHONPATH=2_analysis/src python3 2_analysis/scripts/42_family_F_trends.py
(a) Spearman trace trends inside F: thesis drivers.trace_drift / trace_trends / q6._with_holm called unchanged on the trace frame of the F designs only
    (F = frames.family_flags + family_mask, topType relabelled "F" so the F designs form one class; Spearman p is scipy's two-sided p, as in the thesis; no permutation).
(b) CVT* share inside F: per cohort, and drivers.trend_test (Spearman on priority year, indicator CVT*, complete years).
(c) dQ inside F and the per-dimension dQ: read from the 10000-shuffle seed-42 runs of 3_robustness/32_weight_sensitivity (p1_tests.py f_since_peak, f_per_dimension, f_slc_cvt),
    copied to pending_csv; they are not recomputed here.
Writes pending_csv/10a_F_trace_trends.csv, 10b_F_cvt_share_by_cohort.csv, 10c_dQ_inside_F_*.csv
"""
import os as _os
from pathlib import Path as _Path
_REPO = _Path(__file__).resolve().parents[2]
_SUPP = _os.environ.get("SUPP_OUT", str(_REPO / "results" / "2_analysis" / "numbers"))
_DS = _os.environ.get("EVTOL_DATASET", str(_REPO.parent / "eVTOL_dataset"))
for _d in ("pending_csv", "supplementary_csv"):
    _os.makedirs(_os.path.join(_SUPP, _d), exist_ok=True)
import shutil, sys
from pathlib import Path
import numpy as np, pandas as pd
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
import core
from lib import drivers
O = (_SUPP + "/pending_csv/")
W = Path((_DS + "/07_results/72_weight_sensitivity"))
base = core.load(); ctx = core.context(base, base.master); fr = base.m.frames; ds, v = ctx.ds, ctx.v
fl = fr.family_flags(ds, v); fm = fr.family_mask(fl); print("F designs:", int(fm.sum()), "of", len(fl))
Fid = set(fl.loc[fm, "aircraft_id"])
tf = fr.trace_frame(ds, v); tf = tf[tf["aircraft_id"].isin(Fid)].copy(); tf["topType"] = "F"
drift = drivers.trace_drift(tf, ["F"], class_names={"F": "F"})
tr = drivers.trace_trends(tf, drift, ["F"], class_names={"F": "F"})
tr = tr[tr["code"].eq("F")].copy()
tr["p_holm"] = np.nan   # Holm over the traces (one family), written here; q6._with_holm is for the class x trace table and is not used
ok = tr["p"].notna()
if ok.any():
    p = tr.loc[ok, "p"].to_numpy(); o = np.argsort(p); m = len(p); adj = np.empty(m); run = 0
    for i, j in enumerate(o):
        run = max(run, (m - i) * p[j]); adj[j] = min(1, run)
    tr.loc[ok, "p_holm"] = adj
tr.to_csv(O + "10a_F_trace_trends.csv", index=False); print(tr[["trace", "aircraft", "first window", "first value", "2020-23 value", "rho", "p", "p_holm", "movement"]].to_string())
d = fl.merge(pd.DataFrame({"aircraft_id": fl["aircraft_id"], "F": fm.values}), on="aircraft_id")
f = fl[fm].copy(); f["CVT*"] = f["topType"].eq("CVT").astype(float)
rows = []
for w, g in f.groupby("window"):
    rows.append({"cohort": w, "F designs": len(g), "CVT* designs": int(g["CVT*"].sum()), "Lift + Cruise designs": int((g["topType"] == "SLC").sum()), "CVT* share inside F": round(g["CVT*"].mean(), 4)})
res = drivers.trend_test(f["year"], f["CVT*"])
rows.append({"cohort": "Spearman, priority year vs CVT* indicator inside F (complete years)", "F designs": res["aircraft"], "rho": res["rho"], "p": res["p"], "movement": res["movement"]})
pd.DataFrame(rows).to_csv(O + "10b_F_cvt_share_by_cohort.csv", index=False); print(pd.DataFrame(rows).to_string())
for src, dst in (("test2_summary.csv", "10c_dQ_inside_F_summary.csv"), ("test2_explore_since_peak.csv", "10c_dQ_inside_F_since_peak.csv"),
                 ("test2_explore_per_dimension.csv", "10c_dQ_inside_F_per_dimension.csv"), ("test2_explore_slc_cvt.csv", "10c_F_Q_by_component_cohort.csv")):
    shutil.copy(W / src, O + dst)
