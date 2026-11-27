"""Items 8 and 9 (pending B/C): configurations and effective number 2D per level; new configurations in the last 100 designs against random order.

    EVTOL_DATASET=<path to eVTOL_dataset> PYTHONPATH=2_analysis/src python3 2_analysis/scripts/41_levels_and_last100.py
Thesis functions unchanged, seed 42: frames.archetype_levels_table (whole corpus, all years), frames.discovery_inputs + diversity.discovery_curve_levels +
frames.discovery_estimators + diversity.discovery_tail_band (complete years, up to last_complete_year; 1000 date orderings, 10000 shuffles, tail 100),
exactly as thesis_q6._data and thesis_latex_part2.tab_discovery_last100_band.
Writes pending_csv/8_levels_configurations_2D.csv, 8b_configurations_complete_years.csv, 9_last100_estimators.csv, 9_last100_band.csv.
"""
import os as _os
from pathlib import Path as _Path
_REPO = _Path(__file__).resolve().parents[2]
_SUPP = _os.environ.get("SUPP_OUT", str(_REPO / "results" / "2_analysis" / "numbers"))
_DS = _os.environ.get("EVTOL_DATASET", str(_REPO.parent / "eVTOL_dataset"))
for _d in ("pending_csv", "supplementary_csv"):
    _os.makedirs(_os.path.join(_SUPP, _d), exist_ok=True)
import sys
from pathlib import Path
import pandas as pd
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
import core
from lib import diversity
O = (_SUPP + "/pending_csv/")
LV = {"A0": "A", "A1t": "A.W.T", "A0c": "A.U"}
base = core.load(); ctx = core.context(base, base.master); fr = base.m.frames; cfg = ctx.cfg
lv = fr.archetype_levels_table(ctx.ds, ctx.v, cfg); lv = lv[lv.level.isin(LV)].copy(); lv["level"] = lv["level"].map(LV)
lv.to_csv(O + "8_levels_configurations_2D.csv", index=False); print(lv.to_string())
tail, orders, last = cfg.analysis["discovery_tail"], cfg.analysis["discovery_orders"], cfg.analysis["last_complete_year"]
inputs = fr.discovery_inputs(ctx.v, base.m.q6.SETS3, last)
curve = diversity.discovery_curve_levels(inputs, orders=orders, seed=ctx.SEED)
est = fr.discovery_estimators(inputs, curve, tail=tail); est["level"] = est["level"].map(LV); est.to_csv(O + "9_last100_estimators.csv", index=False)
print(est.to_string())
b = diversity.discovery_tail_band(inputs, tail=tail, orders=orders, seed=ctx.SEED); b["level"] = b["level"].map(LV); b.to_csv(O + "9_last100_band.csv", index=False)
print(b.to_string()); print("last_complete_year", last, "tail", tail, "orders", orders)

# --- diagnostics for the article's values: (a) 1D and 2D on the complete-years designs (the discovery set); (b) the last-100 test on all years (no year cut)
from lib import concentration
rows = []
for sid, (_, keys) in inputs.items():
    c = keys.value_counts()
    rows.append({"level": LV[sid], "base": f"complete years (priority year <= {last})", "designs": len(keys), "configurations": len(c), "singletons": int((c == 1).sum()),
                 "1D": round(diversity.effective_number(keys), 2), "2D": round(concentration.inverse_hhi(c), 2)})
allin = {}
w = ctx.v.dropna(subset=["year"])
for sid in base.m.q6.SETS3:
    k = fr.archetype_key(w, sid); ok = k.notna(); allin[sid] = (w.loc[ok, "year"].to_numpy(), k[ok])
    c = k[ok].value_counts()
    rows.append({"level": LV[sid], "base": "all designs with a year", "designs": int(ok.sum()), "configurations": len(c), "singletons": int((c == 1).sum()),
                 "1D": round(diversity.effective_number(k[ok]), 2), "2D": round(concentration.inverse_hhi(c), 2)})
pd.DataFrame(rows).to_csv(O + "8b_configurations_complete_years.csv", index=False); print(pd.DataFrame(rows).to_string())
b2 = diversity.discovery_tail_band(allin, tail=tail, orders=orders, seed=ctx.SEED); b2["level"] = b2["level"].map(LV)
b2.to_csv(O + "9b_last100_band_all_years_diagnostic.csv", index=False); print(b2.to_string())
