#!/usr/bin/env python3
"""Triage of every patent family the gold standard searches returned: keywords and PatentSBERTa only.

For each family: is it in the dataset, did the author record a decision on it, which keyword groups it matches (and the sentence that
matches), the keyword verdict, and the PatentSBERTa estimates of scope, field, target, architecture and kind of document.
The columns coder_* are the author's; they are kept when triage.xlsx already exists.

Run from the dataset root:
    python 02_gold_standard/search/11A19_triage.py --repo <Patent-Labelling-Tools> [--limit N] [--no-sbert] [--coder-from file.xlsx]

Reads  02_gold_standard/search/patseer_export.xlsx   every family the searches returned, as exported by PatSeer
       01_query/patseer_1639_2026-06-08.xlsx          the families of the dataset
       02_gold_standard/answers.csv, gold_standard.csv   the families the author decided on
Writes 02_gold_standard/search/triage.xlsx            sheets: triage, regexes, codebook
The PatentSBERTa model (AI-Growth-Lab/PatentSBERTa) and the helper functions of src/reviewer.py come from the Patent-Labelling-Tools repository.
"""
import argparse, os, re, sys
import numpy as np
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--repo", default=os.environ.get("PLT_REPO", "../Patent-Labelling-Tools"))
ap.add_argument("--limit", type=int, default=0, help="only the first N families (test)")
ap.add_argument("--no-sbert", action="store_true")
ap.add_argument("--coder-from", default="", help="xlsx with coder_* columns to seed (Record Number key)")
ap.add_argument("--root", default=".")
A = ap.parse_args()
R = A.root; S = f"{R}/02_gold_standard/search"
OUT = f"{S}/triage.xlsx"

FLAGS = {
 "electric":    r"\belectri\w*\W+(?:\w+\W+){0,2}(?:motor|propuls|driv|power|engine|rotor|fan)\w*|\bevtol\b|battery[- ](?:powered|driven|electric)|\ball[- ]electric\b|distributed(?: electric)? propulsion|\belectric(?:al)?ly[- ]driven",
 "vtol":        r"\bvtol\b|vertical(?:ly)?\W+(?:\w+\W+){0,2}(?:take[- ]?off|landing|lift[- ]?off)|\bhover(?:ing|s)?\b|\brotorcraft\b|\bevtol\b|take[- ]?off and land(?:ing)? vertically",
 "passenger":   r"\bpassengers?\b|\boccupants?\b|\bcabins?\b|\bcockpits?\b|\bmanned\b|\bpilots?\b|\bpiloted\b|\bcrew\b|\bseat(?:s|ing)?\b|\brider\b|\bpersons?\b|\bpeople\b|\bhumans?\b|\bcommuter|\bair taxi|\bflying car|\bpersonal (?:air|flying) vehicle|\bcarry(?:ing)? (?:a |one |two |several )?(?:person|people|human)",
 "multicopter": r"multi-?copter|multi-?rotor|quad-?copter|quad-?rotor|hexa-?copter|hexa-?rotor|octo-?copter|octo-?rotor|tri-?copter|volocopter|(?:three|four|six|eight|twelve|sixteen|eighteen|\b[34689]\b|\b1[0-9]\b|plurality of|multiple|array of|a number of|several)\W+(?:\w+\W+){0,3}(?:rotors?|propellers?|ducted fans?|propulsion units?|lift(?:ing)? units?|thrusters?)",
 "uav":         r"\buavs?\b|\bunmanned\b|\bdrones?\b|pilotless|unpiloted|remotely (?:piloted|controlled|operated)|\buas\b",
 "helicopter":  r"\bmain rotor|\btail rotor|\bcoaxial|\btandem rotor|swashplate|cyclic pitch|collective pitch|\bhelicopter",
 "wing":        r"\bwings?\b|fixed[- ]wing|tilt[- ]?(?:wing|rotor)|\bcanard|\bairfoil",
 "component":   r"\bmethod\b|\bbattery\b|\bmotor assembly|\bblade\b|\blanding gear|\bcontrol(?:ler| system| method)\b|\bcharging|\bcooling|\bsensor",
}
RX = {k: re.compile(v, re.I) for k, v in FLAGS.items()}
NEG_PILOT = re.compile(r"auto-?pilot\w*|pilotless|unpiloted|remotely[- ]piloted|without (?:a )?pilot", re.I)
SENT = re.compile(r"(?<=[.;!?])\s+|\n+")
PUB = re.compile(r"[A-Z]{2}\d+[A-Z]\d?")
norm = lambda s: re.sub(r"[^A-Z0-9]", "", str(s).upper())
base = lambda s: re.sub(r"[A-Z]\d?$", "", norm(s))
CODER = ["coder_shows_crewed_aircraft", "coder_architecture", "coder_vfs_design", "coder_in_627", "coder_design_key", "coder_in_domain", "coder_notes"]

ex = pd.read_excel(f"{S}/patseer_export.xlsx", dtype=str).fillna("")
if A.limit: ex = ex.head(A.limit)
th = pd.read_excel(f"{R}/01_query/patseer_1639_2026-06-08.xlsx", dtype=str).fillna("")
members = lambda r: set(PUB.findall(r.get("Simple Family Members", ""))) | {r["Record Number"]}
th_base = {base(m) for _, r in th.iterrows() for m in members(r)}
ex["in_dataset"] = ex.apply(lambda r: any(base(m) in th_base for m in members(r)), axis=1)

# families the author decided on (any identifier of the family in answers.csv or gold_standard.csv)
ids = set()
for f, cols in [(f"{R}/02_gold_standard/answers.csv", ["families", "item"]), (f"{R}/02_gold_standard/gold_standard.csv", ["family", "design_ids"])]:
    if os.path.exists(f):
        d = pd.read_csv(f, dtype=str, keep_default_na=False)
        for c in cols:
            if c in d: ids |= {base(x) for v in d[c] for x in PUB.findall(str(v))}
ex["author_decision_recorded"] = ex.apply(lambda r: any(base(m) in ids for m in members(r)), axis=1)

def fields(r):
    return [("title", r.get("Title", "")), ("abstract", r.get("Abstract", "")),
            ("claims", " ".join(r.get(c, "") for c in ("First Claim", "Independent Claims"))),
            ("description", " ".join(r.get(c, "") for c in ("Summary of Invention", "Description of Drawings", "Description")))]
def first_hit(rx, r, strip_neg=False):
    for name, txt in fields(r):
        if not txt.strip(): continue
        t = NEG_PILOT.sub(" ", txt) if strip_neg else txt
        m = rx.search(t)
        if m:
            sents = [s for s in SENT.split(t) if rx.search(s)]
            return name, (sents[0] if sents else t[max(0, m.start() - 120): m.end() + 120]).strip()[:300]
    return None, None
def count_hits(rx, r, strip_neg=False):
    return sum(len(rx.findall(NEG_PILOT.sub(" ", t) if strip_neg else t)) for _, t in fields(r))

rows = ex.to_dict("records"); kw = []
for r in rows:
    o = {}
    for k, rx in RX.items():
        f, ev = first_hit(rx, r, strip_neg=(k == "passenger")); o[f"kw_{k}_field"] = f; o[f"kw_{k}_evidence"] = ev; o[f"kw_{k}_n"] = count_hits(rx, r, strip_neg=(k == "passenger"))
    kw.append(o)
kw = pd.DataFrame(kw)
strength = {"title": "strong", "abstract": "strong", "claims": "medium", "description": "weak", None: "none"}
core = ["electric", "vtol", "passenger", "multicopter"]
for k in core: kw[f"kw_{k}"] = kw[f"kw_{k}_field"].map(strength)
def verdict(r):
    strong = {k for k in core if r[f"kw_{k}"] in ("strong", "medium")}; weak = {k for k in core if r[f"kw_{k}"] == "weak"}
    if r["kw_helicopter_field"] in ("title", "abstract") and r["kw_multicopter_field"] not in ("title", "abstract"): return "out (helicopter terms)"
    if r["kw_uav_field"] in ("title", "abstract") and r["kw_passenger_field"] not in ("title", "abstract"): return "out (UAV, no crew in title or abstract)"
    if len(strong) == 4: return "in"
    if "multicopter" in strong and "vtol" in strong | weak and len(strong | weak) >= 3: return "similar"
    if len(strong | weak) == 4: return "similar"
    return "out"
kw["kw_verdict"] = kw.apply(verdict, axis=1)

sb = pd.DataFrame({"Record Number": ex["Record Number"]})
SBC = ["sbert_scope", "sbert_scope_conf", "sbert_field", "sbert_field_conf", "sbert_target", "sbert_target_conf", "sbert_avg_conf", "sbert_arch", "sbert_arch_conf", "sbert_arch_margin", "sbert_arch_flagged", "sbert_domain_aux", "sbert_domain_aux_conf"]
for c in SBC: sb[c] = None
if not A.no_sbert:
    import torch
    from sentence_transformers import SentenceTransformer
    sys.path.insert(0, A.repo)
    from src.reviewer import classify_t1_dimensions, _sbert_best, _margin_flag, _G1_TOP_TYPE_DEFS
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer("AI-Growth-Lab/PatentSBERTa", cache_folder=f"{A.repo}/models/SBERT", device=dev); print("PatentSBERTa on", dev, flush=True)
    DOMAIN = {"crewed multicopter": "a passenger-carrying electric multirotor aircraft with several fixed lift rotors and no wing, carrying one or more people in a cabin or seat",
              "winged eVTOL": "a vertical take-off aircraft with wings for cruise flight and rotors or tilting propellers for hover",
              "unmanned drone": "an unmanned aerial vehicle or drone for cargo, inspection or photography without any person on board",
              "helicopter": "a conventional helicopter with a main rotor and a tail rotor or coaxial rotors",
              "component or method": "a component, subsystem, battery, motor, control method or software not describing a complete aircraft"}
    for i, r in enumerate(rows):
        if r["in_dataset"]: continue                       # the families of the dataset are already labelled
        txt = " ".join(r.get(c, "") for c in ("Title", "Abstract", "Description of Drawings"))
        t1 = classify_t1_dimensions(txt, model); confs = [t1[k]["confidence"] for k in ("scope", "t1Field", "t1Target") if t1[k]["value"]]
        g1 = _margin_flag(_sbert_best(txt, _G1_TOP_TYPE_DEFS, model)); dom = _sbert_best(txt, DOMAIN, model)
        sb.loc[i, SBC] = [t1["scope"]["value"], t1["scope"]["confidence"], t1["t1Field"]["value"], t1["t1Field"]["confidence"], t1["t1Target"]["value"], t1["t1Target"]["confidence"],
                          None if not confs else round(float(np.mean(confs)), 4), g1["value"], g1["confidence"], g1.get("margin"), bool(g1.get("flagged_ambiguous", False)), dom["value"], dom["confidence"]]
        if (i + 1) % 200 == 0: print(f"  SBERT {i + 1}/{len(rows)}", flush=True)

keep = ["Record Number", "Simple Family ID", "Title", "Assignee", "Priority Year", "Publication/Issue Date", "CPC", "PDF Link", "Simple Family Members", "Abstract"]
T = pd.concat([ex[[c for c in keep if c in ex]], ex[["in_dataset", "author_decision_recorded"]], kw, sb.drop(columns=["Record Number"])], axis=1)
T["sbert_complete_aircraft"] = T["sbert_domain_aux"].isin(["crewed multicopter", "winged eVTOL"])
unseen = (~T.in_dataset) & (~T.author_decision_recorded)
T["flag_keywords"] = unseen & T.kw_verdict.isin(["in", "similar"])
T["flag_sbert"] = unseen & T.sbert_complete_aircraft
T["core_strong"] = T.kw_multicopter_field.isin(["title", "abstract", "claims"]) & T.kw_vtol_field.isin(["title", "abstract", "claims"])
# 0: in the dataset or already decided. 1: keywords AND SBERT flag it. 2: only one of the two. 3: neither.
T["review_priority"] = np.where(~unseen, 0, np.where(T.flag_keywords & T.flag_sbert, 1, np.where(T.flag_keywords | T.flag_sbert, 2, 3)))
T["to_review"] = T.review_priority == 1
for c in CODER: T[c] = ""
seed = A.coder_from or (OUT if os.path.exists(OUT) else "")
if seed:
    sd = pd.read_excel(seed, sheet_name=0, dtype=str).fillna("")
    sd = sd.rename(columns={"title": "_t", "company": "_c"})
    have = [c for c in CODER if c in sd.columns]
    if have:
        m = sd.drop_duplicates("Record Number").set_index("Record Number")[have]
        for c in have: T[c] = T["Record Number"].map(m[c]).fillna("")
T["_p"] = T.review_priority.replace({0: 9})
T["_o"] = T.kw_verdict.map({"in": 0, "similar": 1}).fillna(2)
T = T.sort_values(["_p", "core_strong", "_o", "Priority Year"], ascending=[True, False, True, False]).drop(columns=["_p", "_o"])
codebook = pd.DataFrame([
 ("in_dataset", "the family is one of the 1 639 of the dataset"), ("author_decision_recorded", "an identifier of the family appears in answers.csv or gold_standard.csv"),
 ("kw_<group>_field / _evidence / _n", "where the group first matches (title, abstract, claims, description), the matching sentence, and the number of matches"),
 ("kw_verdict", "in: electric, VTOL, passenger and multicopter found in title, abstract or claims. similar: multicopter and VTOL plus one more, or all four anywhere. out: otherwise, or helicopter or UAV terms in title or abstract without the counterpart"),
 ("sbert_scope / field / target", "PatentSBERTa estimate of the T1 dimensions (the thesis wizard feed)"), ("sbert_arch", "PatentSBERTa estimate of the architecture over the taxonomy definitions; flagged when the margin is thin"),
 ("sbert_domain_aux", "zero-shot kind of document: crewed multicopter, winged eVTOL, unmanned drone, helicopter, component or method"),
 ("flag_keywords / flag_sbert", "outside the dataset, no recorded decision, and keyword verdict in or similar / PatentSBERTa says a complete crewed aircraft"),
 ("core_strong", "multicopter and VTOL words both found in title, abstract or claims"),
 ("review_priority", "0 in the dataset or already decided; 1 flagged by keywords AND SBERT (to_review); 2 flagged by one of the two; 3 by neither"),
 ("coder_*", "the author's reading of the families flagged for review")], columns=["column", "meaning"])
with pd.ExcelWriter(OUT, engine="openpyxl") as w:
    T.to_excel(w, sheet_name="triage", index=False); pd.DataFrame({"flag": list(FLAGS), "regex": list(FLAGS.values())}).to_excel(w, sheet_name="regexes", index=False); codebook.to_excel(w, sheet_name="codebook", index=False)
print(f"{len(T)} families | in dataset {int(T.in_dataset.sum())} | decision recorded {int(T.author_decision_recorded.sum())} | verdict {T.kw_verdict.value_counts().to_dict()}")
print(f"review priority {T.review_priority.value_counts().sort_index().to_dict()} | priority 1 with core_strong: {int((T.to_review & T.core_strong).sum())}")
