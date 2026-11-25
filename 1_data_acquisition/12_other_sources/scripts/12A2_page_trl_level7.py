"""TRL >= 7 per evtol.news (VFS) page, keyword rule written on 2026-11-10 for the gold standard v2 'mature programmes' set.

The thesis rule (trl_rule.py) reaches 7 only for the words "piloted / crewed / manned flight", so on the author's 50 reviewed designs
it found 2 of the 10 the author rated 7 or more. The author's TRL 7 is "a full-scale prototype flown free through its working mode:
transition / wingborne flight for a winged aircraft, crewed or open-air forward flight for a wingless one". This rule reads the same
page sentences as trl_page_rule.py (company history, plans and 'as of' dropped; sentence must name the model or say 'the aircraft ...')
and gives 7 when a past-tense sentence reports either
  - a crewed flight (piloted / crewed / manned flight, pilot(s) on board, flown by a (test) pilot), not 'unmanned' in the same sentence, or
  - a transition to forward / wingborne flight (completed / achieved / made / performed / demonstrated ... transition),
and 8 for a type certificate. Sub-scale pages are capped at 5. Scored once on the author's 50 reviewed designs (printed at the end).
Output: 05_secondary/vfs/VFS_PAGE_TRL7.csv (slug_key, trl7, sentence).
"""
import os
import json, re, sys
from pathlib import Path
import pandas as pd
DATA_DIR = Path(__file__).resolve().parent.parent
CODE = Path(__file__).resolve().parent / "yearscript"
SRC = Path(os.environ.get("EVTOLNEWS_SOURCE", "data/evtolnews/0_source"))
sys.path.insert(0, str(CODE))
from trl_rule import CERT, SCALE
from trl_page_rule import SPLIT, GEN
from year_rule import COMPANY, FUT, ASOF, PAST, model_tokens

CREW = re.compile(r"\b(?:first |maiden |successful |multiple |several )?(?:piloted|crewed|manned) (?:test |maiden |free )?(?:flight|flights|hover|hovers|take-?off)s?\b"
                  r"|(?:test )?pilots? on ?board|(?:was|were|has been|had been|been) (?:successfully )?(?:flown|piloted) by (?:a |an |the |its |test )?(?:test |chief |company )?pilot"
                  r"|\bflew (?:it|the aircraft)? ?with (?:a |an )?(?:test )?pilot|flown by test pilot", re.I)
UNMAN = re.compile(r"\b(?:unmanned|uncrewed|unpiloted|remotely|tethered|radio[- ]control|remote drone controller)\b", re.I)
TRANS = re.compile(r"(?:complet|achiev|made|perform|demonstrat|conduct|accomplish)\w*\b[^.]{0,60}\btransition|\btransitioned (?:between|from|to)\b|transition flight tests? (?:was|were|has been|had been) (?:completed|achieved|successful)", re.I)
HYPO = re.compile(r"\b(?:no (?:crewed|piloted|manned)|never|not yet|might|could|would|may|can be|designed to|paves? the way|in preparation|ahead of|aims?|hypothetical\w*)\b", re.I)
DONE = re.compile(r"\b(?:was|were|had|did|completed|achieved|made|performed|demonstrated|conducted|flew|took|began|announced|has made|have made|has completed|has achieved|has flown|have flown|has been)\b", re.I)

def trl7(text, model, sub):
    tk = model_tokens(model); best = (0, "")
    for s in SPLIT.split(text):
        s = s.strip()
        if not s or COMPANY.search(s) or ASOF.search(s) or (FUT.search(s) and not PAST.search(s)): continue
        if not (any(x in s.lower() for x in tk) or GEN.search(s)): continue
        if not DONE.search(s) or HYPO.search(s): continue
        v = 8 if CERT.search(s) else 7 if ((CREW.search(s) and not UNMAN.search(s)) or TRANS.search(s)) else 0
        if v and (sub or SCALE.search(s)): v = 5
        if v > best[0]: best = (v, s)
    return best

A = pd.read_csv(DATA_DIR / "05_secondary/vfs/aircraft.csv", keep_default_na=False).set_index("slug_key")
ev = pd.read_csv(SRC / "years/readers/evidence_ids.csv", dtype=str, keep_default_na=False)
res = {k: set(s.strip()[:60] for s in g.loc[g["is_resource"].eq("True"), "sentence"]) for k, g in ev.groupby("slug_key")}
rows = []
for line in open(SRC / "pages.jsonl", encoding="utf-8"):
    r = json.loads(line); k = r["slug_key"]
    if k not in A.index: continue
    body = "\n".join(s for s in SPLIT.split(r["text"]) if s.strip()[:60] not in res.get(k, set()))
    sub = bool(SCALE.search(A.loc[k, "spec_aircraft_type"] + " " + A.loc[k, "title"]))
    v, s = trl7(body, A.loc[k, "model"], sub)
    rows.append({"slug_key": k, "trl7": v, "sentence": s})
out = pd.DataFrame(rows); out.to_csv(DATA_DIR / "05_secondary/vfs/VFS_PAGE_TRL7.csv", index=False)

# score on the author's 50 reviewed designs (design = max over its linked pages)
pl = pd.read_csv(DATA_DIR / "05_secondary/vfs/patent_links.csv"); pl = pl[pl.use == "yes"]
t = pd.read_csv(DATA_DIR / "03_aircraft/trl/TRL.csv"); rv = t[t.author_trl.notna()].set_index("aircraft_id")
pg = out.set_index("slug_key").trl7
des = {r.aircraft_uid: max([pg.get(s, 0) for s in str(r.slug_keys).split("|")] + [0]) for r in pl.itertuples()}
sc = rv.assign(rule=rv.index.map(lambda i: des.get(i, 0)))
print(pd.crosstab(sc.rule >= 7, sc.author_trl >= 7, rownames=["regra >= 7"], colnames=["autor >= 7"]))
print(out.trl7.value_counts().to_dict())
