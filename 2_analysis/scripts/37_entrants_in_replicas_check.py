"""E14: do the coding-noise replicas use entrant definition (b)? Rebuilds the entrant flags (frames.named_entries, the function core.r7_entrants calls)
on the original table and on replicas 0..4, and compares them design by design.
    EVTOL_DATASET=<path> PYTHONPATH=2_analysis/src python 2_analysis/scripts/37_entrants_in_replicas_check.py
Writes numbers/supplementary_csv/E14_entrant_flags_original_vs_replicas.csv
"""
import os, sys
from pathlib import Path
import pandas as pd
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
import core, perturb
OUT = Path(os.environ.get("SUPP_OUT", "/mnt/storage_11tb/Drive_files_to_syncronize/paper_figures_for_other_pc/numbers")) / "supplementary_csv"
base = core.load()
ctx0 = core.context(base, base.master)
e0 = base.m.frames.named_entries(ctx0.v, ctx0.WIN_NAMES).set_index("aircraft_id")
P = perturb.Perturber(base, r=0.15)
rows = []
for i in range(5):
    m, _ = P.replica(20261118, i)
    ctx = core.context(base, m)
    e = base.m.frames.named_entries(ctx.v, ctx.WIN_NAMES).set_index("aircraft_id")
    common = e0.index.intersection(e.index)
    rows.append({"replica": i, "named designs original": len(e0), "named designs replica": len(e), "designs compared": len(common),
                 "first_time flag differs": int((e0.loc[common, "first_time"] != e.loc[common, "first_time"]).sum()),
                 "window differs": int((e0.loc[common, "window"] != e.loc[common, "window"]).sum()),
                 "firm differs": int((e0.loc[common, "firm"] != e.loc[common, "firm"]).sum()),
                 "architecture (topType) differs": int((e0.loc[common, "topType"] != e.loc[common, "topType"]).sum())})
t = pd.DataFrame(rows); t.to_csv(OUT / "E14_entrant_flags_original_vs_replicas.csv", index=False); print(t.to_string())
