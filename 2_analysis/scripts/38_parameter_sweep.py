"""Parameter sweep for S5 (paper P1): rarefaction size, variety threshold, share window. Thesis functions, nothing rewritten.

    EVTOL_DATASET=<path> PYTHONPATH=2_analysis/src python 2_analysis/scripts/38_parameter_sweep.py --part rare --n 30 [--perms 10000]
    ... --part variety      (80 % rule of the design-space table, at 70 / 80 / 90 %)
    ... --part window       (condition 1 with k consecutive years above 50 %, k = 2, 3, 4)

rare:    condition 2 (balance) at the four levels, both bases, every cohort, rarefied to n designs, permutation percentile and band
         (same patched balance_band as 31_family_F_numbers.py; seed 42; 10 000 shuffles).
variety: dimensions of the design-space table whose leading option holds under the threshold, and (per architecture with 20+ designs)
         the winged architectures in which the wing configuration is fixed at the threshold (core.r1_design_space logic).
window:  years in which condition 1 is met, per level and base, when k consecutive read years (>= 20 designs) are above 50 %.
Writes numbers/supplementary_csv/S5_*.csv
"""
import os as _os
from pathlib import Path as _Path
_REPO = _Path(__file__).resolve().parents[2]
_SUPP = _os.environ.get("SUPP_OUT", str(_REPO / "results" / "2_analysis" / "numbers"))
_DS = _os.environ.get("EVTOL_DATASET", str(_REPO.parent / "eVTOL_dataset"))
for _d in ("pending_csv", "supplementary_csv"):
    _os.makedirs(_os.path.join(_SUPP, _d), exist_ok=True)
import argparse, importlib.util, os, sys
from pathlib import Path
import numpy as np, pandas as pd
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
import core
OUT = Path(os.environ.get("SUPP_OUT", _SUPP)) / "supplementary_csv"
OUT.mkdir(parents=True, exist_ok=True)
ap = argparse.ArgumentParser(); ap.add_argument("--part", required=True); ap.add_argument("--n", type=int, default=30); ap.add_argument("--perms", type=int, default=10000)
a = ap.parse_args()
base = core.load(); ctx = core.context(base, base.master); fr = base.m.frames; v = ctx.v
live = v["aircraft_id"].map(fr.patent_state(ctx.ds, v)["in_force"]).astype(bool)
LV = {"A0": "L1", "A1t": "L2", "A0c": "L3", "family_b": "F"}

if a.part == "rare":
    spec = importlib.util.spec_from_file_location("f31", REPO / "2_analysis" / "scripts" / "31_family_F_numbers.py"); f31 = importlib.util.module_from_spec(spec); spec.loader.exec_module(f31)
    import lib.dominant_design as dd
    dd.balance_band = f31._patched(dd.balance_band, '        r["D2 permutation low"] = round(float(np.percentile(b, 2.5)), 2)',
        '        r["percentile of the observed D2 (share of shuffles at or below)"] = round(float(np.mean(b <= r["D2"]) * 100), 1)\n        r["D2 permutation low"] = round(float(np.percentile(b, 2.5)), 2)')
    fr._dd = dd
    parts = []
    for name, vv in (("all designs", v), ("actively protected", v[live])):
        t = fr.dd_balance_table(ctx.ds, vv, ctx.WIN_NAMES, a.n, a.perms, ctx.SEED).assign(base=name, rarefied_to=a.n, permutations=a.perms)
        t["L"] = t["level"].map(LV); parts.append(t)
    pd.concat(parts).to_csv(OUT / f"S5_rarefaction_{a.n}.csv", index=False)
elif a.part == "variety":
    t6 = fr.selected_fields(ctx.ds); rows = []
    for th in (0.7, 0.8, 0.9):
        ctx._q6 = {"t6": t6, "cut": base.cfg.analysis["field_drop_top_share"]}
        _, det = base.m.q6.fixed_by_architecture(ctx, share=th, min_designs=core.MIN_ARCH_DESIGNS); ctx._q6 = None
        wc = det[det["dimension"].astype(str).str.contains("wing configuration", case=False)]
        rd = wc[wc["code"].isin(core.WINGED) & wc["read"].astype(bool)]
        rows.append({"threshold": th, "dimensions read": len(t6), "dimensions that vary (leading share < threshold)": int((t6["top_share"] < th).sum()),
                     "varying, landing gear left out": int((t6.loc[~t6["name"].astype(str).str.contains("landing-gear", case=False), "top_share"] < th).sum()),
                     "winged architectures read (wing configuration)": len(rd), "of which wing configuration fixed at the threshold": int((rd["share"] >= th).sum()),
                     "varying dimensions": "; ".join(t6.loc[t6["top_share"] < th, "name"].astype(str))})
    pd.DataFrame(rows).to_csv(OUT / "S5_variety_threshold.csv", index=False)
    t6[["name", "answered", "top_share"]].to_csv(OUT / "S5_variety_top_shares.csv", index=False)
elif a.part == "window":
    dy = fr.dd_yearly(ctx.ds, v, ctx.cfg.analysis["last_complete_year"]); rows = []
    for (lid, base_), g in dy.groupby(["level id", "base"]):
        g = g[g["read"].astype(bool)]; over = sorted(g.loc[g["above 50 %"].astype(bool), "priority year"].astype(int))
        for k in (2, 3, 4):
            yrs = {y for i in range(len(over)) for y in over[i:i + k] if len(over[i:i + k]) == k and over[i + k - 1] - over[i] == k - 1}
            rows.append({"level": LV[lid], "base": {"all": "all designs", "in force": "actively protected"}[base_], "consecutive years required": k,
                         "years read": len(g), "years above 50 %": ", ".join(map(str, over)), "years in which condition 1 is met": ", ".join(map(str, sorted(yrs))), "condition 1 met": bool(yrs)})
    pd.DataFrame(rows).to_csv(OUT / "S5_share_window.csv", index=False)
print("done", a.part, a.n)
