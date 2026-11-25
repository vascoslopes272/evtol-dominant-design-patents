"""Share of entrants per cohort under two definitions.

(b) the first design of the firm falls in the cohort (the rule of the analysis, notebook 25).
(a) the first family of the firm in the corpus (all 1 639 families of the query, approved or not) falls in the cohort.
    A firm with earlier aircraft patents outside the corpus cannot be seen, so (a) is a lower bound on the incumbents.

Run:  EVTOL_DATASET=/path/to/eVTOL_dataset PYTHONPATH=src python scripts/30_entrants_two_definitions.py
Writes ../results/2_analysis/entrants/entrants_two_definitions.csv
"""
import pathlib
import numpy as np
import pandas as pd
from viz import config, thesis, frames

cfg = config.load()
ctx = thesis.context(cfg)
v, ds = ctx.v, ctx.ds
ident = ds.identity.copy()
da = frames.design_assignees(ident).set_index("patent_id")
raw = ident["patent_id"].map(da["assignee_chosen"])
cc = ident["patent_id"].map(da["canon"])
filer = raw.map(frames.filer_from_assignee)
resolved = cc.notna() & ~cc.isin(frames.CATCH_ALL)
is_org = filer.isin(["Named company", "University / institute"])
firm = pd.Series(np.where(resolved, cc, np.where(is_org, raw.map(frames.firm_from_assignee), None)), index=ident.index)
ident["firm"] = firm.where(~firm.isin(["", "None"]) & firm.notna(), None)
ident["py"] = pd.to_numeric(ident["priority_year"], errors="coerce")
W, names = ctx.WIN, ctx.WIN_NAMES
cohort_of = lambda y: frames.window_of(y, W)
first_corpus = ident[ident.firm.notna()].groupby("firm")["py"].min().map(cohort_of)
dsg = v[v["firm"].notna()].copy()
dsg["py"] = pd.to_numeric(dsg["priority_year"])
first_design = dsg.groupby("firm")["py"].min().map(cohort_of)
rows = []
for n in names:
    active = dsg[dsg["window"] == n]["firm"].unique()
    b = [f for f in active if first_design[f] == n]
    a = [f for f in active if f in first_corpus.index and first_corpus[f] == n]
    rows.append({"cohort": n, "firms active": len(active),
                 "entrants (b) first design in the cohort": len(b), "share (b)": round(len(b) / len(active), 3),
                 "entrants (a) first family in the corpus in the cohort": len(a), "share (a)": round(len(a) / len(active), 3)})
out = pd.DataFrame(rows)
dst = pathlib.Path(__file__).resolve().parents[2] / "results" / "2_analysis" / "entrants"
dst.mkdir(parents=True, exist_ok=True)
out.to_csv(dst / "entrants_two_definitions.csv", index=False)
print(out.to_string(index=False))
