"""TRL of every evtol.news (VFS) page, with the thesis's rule-based script applied page by page.

The rule is the author's `trl_page_rule.py` (keywords only, no model): read every sentence of the page outside the source list, drop
company history, plans and "as of" statements, keep sentences that name the model or say "the aircraft / prototype / ...", give each
one `trl_rule.rule_trl`, cap sub-scale pages at 5, and keep the highest level. In the thesis it was run only on pages linked to a
patented design; here the same loop runs on all pages, so that unpatented aircraft also get a TRL.
The code is imported unchanged from the code repository (it is not part of the dataset, DECISIONS.md item 11).

Output: 05_secondary/vfs/VFS_PAGE_TRL_SCRIPT.csv  (slug_key, trl_script, sentence)
"""
import os
import json, sys
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent
CODE = Path(__file__).resolve().parent / "yearscript"
SRC = Path(os.environ.get("EVTOLNEWS_SOURCE", "data/evtolnews/0_source"))
sys.path.insert(0, str(CODE))
from trl_rule import rule_trl, SCALE
from trl_page_rule import SPLIT, GEN
from year_rule import COMPANY, FUT, ASOF, PAST, model_tokens

A = pd.read_csv(DATA_DIR / "05_secondary/vfs/aircraft.csv", keep_default_na=False).set_index("slug_key")
ev = pd.read_csv(SRC / "years/readers/evidence_ids.csv", dtype=str, keep_default_na=False)
res = {k: set(s.strip()[:60] for s in g.loc[g["is_resource"].eq("True"), "sentence"]) for k, g in ev.groupby("slug_key")}
rows = []
for line in open(SRC / "pages.jsonl", encoding="utf-8"):
    r = json.loads(line); k = r["slug_key"]
    if k not in A.index: continue
    tk = model_tokens(A.loc[k, "model"])
    sub = bool(SCALE.search(A.loc[k, "spec_aircraft_type"] + " " + A.loc[k, "title"]))
    best = (2, "")
    for s in SPLIT.split(r["text"]):
        if not s.strip() or s.strip()[:60] in res.get(k, set()): continue
        if COMPANY.search(s) or ASOF.search(s) or (FUT.search(s) and not PAST.search(s)): continue
        if not (any(x in s.lower() for x in tk) or GEN.search(s)): continue
        v = rule_trl(s)
        if sub and v > 5: v = 5
        if v > best[0]: best = (v, s.strip())
    rows.append({"slug_key": k, "trl_script": best[0], "sentence": best[1]})
out = pd.DataFrame(rows)
out.to_csv(DATA_DIR / "05_secondary/vfs/VFS_PAGE_TRL_SCRIPT.csv", index=False)
print(len(out), "pages;", out.trl_script.value_counts().sort_index().to_dict())
