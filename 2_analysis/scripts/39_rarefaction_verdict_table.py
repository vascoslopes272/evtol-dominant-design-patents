"""Item 5 (pending B/C): balance verdict (below band, percentile) per level, base, cohort at rarefaction 30/40/50.

    python3 2_analysis/scripts/39_rarefaction_verdict_table.py
Reads S5_rarefaction_30.csv, S5_rarefaction_50.csv (38_parameter_sweep.py --part rare, 10000 perms, seed 42) and
results/2_analysis/family_F/percentiles_balance.csv (40). Writes pending_csv/5_rarefaction_verdict_30_40_50.csv and 5_rarefaction_verdict_changes.csv.
"""
import pandas as pd
N = "/mnt/storage_11tb/Drive_files_to_syncronize/paper_figures_for_other_pc/numbers/"
LV = {"A0": "A", "A1t": "A.W.T", "A0c": "A.U", "family_b": "F"}
fs = {30: N + "supplementary_csv/S5_rarefaction_30.csv", 40: N + "family_F/percentiles_balance.csv", 50: N + "supplementary_csv/S5_rarefaction_50.csv"}
P = "percentile of the observed D2 (share of shuffles at or below)"
out = None
for n, f in fs.items():
    d = pd.read_csv(f); assert len(d) == 40 and d[P].notna().all(), (n, len(d))
    d["level"] = d["level"].map(LV)
    d = d[["level", "base", "window", "aircraft", "D2", "D2 permutation low", "D2 permutation high", P, "below band"]]
    d.columns = ["level", "base", "cohort", "aircraft", f"D2_{n}", f"band_low_{n}", f"band_high_{n}", f"percentile_{n}", f"below_band_{n}"]
    out = d if out is None else out.merge(d, on=["level", "base", "cohort"], suffixes=("", f"_{n}"))
cols = ["level", "base", "cohort"] + [c for c in out.columns if c.endswith(("_30", "_40", "_50"))]
out = out[cols]; out["verdict_changes"] = ~((out.below_band_30 == out.below_band_40) & (out.below_band_40 == out.below_band_50))
O = N + "pending_csv/"
out.to_csv(O + "5_rarefaction_verdict_30_40_50.csv", index=False)
ch = out[out.verdict_changes]; ch.to_csv(O + "5_rarefaction_verdict_changes.csv", index=False)
print(out[["level","base","cohort","percentile_30","below_band_30","percentile_40","below_band_40","percentile_50","below_band_50"]].to_string())
print("changes:\n", ch.to_string())
