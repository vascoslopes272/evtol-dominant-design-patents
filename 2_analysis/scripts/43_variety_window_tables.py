"""Items 6 and 7 (pending B/C): named settled/varying dimensions per threshold; share-window verdict at every level and base.

    python3 2_analysis/scripts/43_variety_window_tables.py
Reads S5_variety_top_shares.csv (38_parameter_sweep.py --part variety) and S5_share_window.csv (--part window; all four levels L1, L2=A.W.T, L3=A.U, F, both bases).
Writes pending_csv/6_variety_settled_vs_varying.csv and pending_csv/7_share_window_all_levels.csv.
"""
import pandas as pd
N = "/mnt/storage_11tb/Drive_files_to_syncronize/paper_figures_for_other_pc/numbers/"
t = pd.read_csv(N + "supplementary_csv/S5_variety_top_shares.csv"); rows = []
for th in (0.7, 0.8, 0.9):
    for _, r in t.iterrows():
        rows.append({"threshold": th, "dimension": r["name"], "answered": r["answered"], "leading_share": r["top_share"], "status": "varies" if r["top_share"] < th else "settled"})
pd.DataFrame(rows).to_csv(N + "pending_csv/6_variety_settled_vs_varying.csv", index=False)
w = pd.read_csv(N + "supplementary_csv/S5_share_window.csv")
w["level"] = w["level"].map({"L1": "A", "L2": "A.W.T", "L3": "A.U", "F": "F"})
w.to_csv(N + "pending_csv/7_share_window_all_levels.csv", index=False)
for th in (0.7, 0.8, 0.9):
    s = pd.DataFrame(rows); s = s[s.threshold == th]
    print(th, "SETTLED:", "; ".join(s[s.status == "settled"].dimension), "| VARY:", "; ".join(s[s.status == "varies"].dimension))
print(w.to_string())
