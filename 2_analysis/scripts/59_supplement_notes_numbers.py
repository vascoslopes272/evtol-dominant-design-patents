"""Numbers for the notes of the supplement (request of 2026-11-27, items D2, D4, D5 and B).

    EVTOL_DATASET=<path to eVTOL_dataset> python 59_supplement_notes_numbers.py
Writes results/2_analysis/pending_numbers/pending_csv/R59_*.csv.
 D2  the designs whose architecture from the drawing differs from the public aircraft (files 42, 43, 44 of the dataset)
 D4  Spearman rho and Holm p of the five traced quantities in SLC, TP, CVT (freeze q6_driver_trends and thesis_q6 sets-per-unit)
 D5  the archetype sets that were built and not used (frames.archetype_levels_table and screens)
 B   the design that has an architecture but no key at A.W.T and A.U in 2020-23
"""
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "3_robustness" / "31_label_reliability" / "src"))
sys.path.insert(0, str(REPO / "2_analysis" / "src"))
import core  # noqa: E402

DS = Path(os.environ.get("EVTOL_DATASET", REPO.parent / "eVTOL_dataset"))
OUT = REPO / "results" / "2_analysis" / "pending_numbers" / "pending_csv"

# D2
t44 = pd.read_csv(DS / "04_aircraft" / "44_trl.csv", low_memory=False)
t43 = pd.read_csv(DS / "04_aircraft" / "43_architecture_image_and_text.csv")
des = pd.read_csv(DS / "04_aircraft" / "45_designs.csv")
x = des[["aircraft_id", "architecture"]].merge(t44[["aircraft_id", "company", "aircraft_name", "arch_match", "public_arch"]], on="aircraft_id") \
    .merge(t43[["aircraft_id", "architecture_from_text"]], on="aircraft_id", how="left")
x = x[x["arch_match"].isin(["no", "image only"])].copy()
x["cause"] = np.where(x["arch_match"].eq("image only"), "the drawing label differs from the text and the aircraft (drawing misread or cannot show it)",
                      "drawing and text agree with each other and differ from the aircraft as built (the patent describes another architecture)")
x = x.rename(columns={"architecture": "architecture in the drawing", "architecture_from_text": "architecture in the patent text", "public_arch": "architecture of the public aircraft",
                      "company": "assignee", "aircraft_name": "aircraft"})
x.to_csv(OUT / "R59_D2_ten_disagreements.csv", index=False)
print(x.to_string())

# D4
base = core.load()
ctx = core.context(base, base.master)
tr = pd.read_csv(REPO / "results" / "2_analysis" / "freeze" / "csv" / "q6_driver_trends.csv")
rows = []
for label, trace in (("Propulsors per design", "propulsive units"), ("Tilting sets (mean)", "tilting joint groups"),
                     ("Propulsors on booms (share)", "units carried on booms"), ("Ducted propulsor (share)", "a ducted unit")):
    for code, name in (("SLC", "SLC"), ("TR", "TP"), ("CVT", "CVT")):
        r = tr[(tr["trace"] == trace) & (tr["code"] == code)].iloc[0]
        rows.append({"quantity": label, "architecture": name, "rho": r["rho"], "p": r["p"], "p Holm": r["p_holm"], "designs": r["aircraft"]})
spu = base.m.q6._data(ctx)["spu"]
tp = spu[(spu["code"] == "TR") & (spu["measure"] == "tilting sets per propulsive unit")].iloc[0]
cv = spu[(spu["code"] == "CVT") & (spu["measure"] == "tilting sets per propulsive unit")].iloc[0]
ps = sorted([("TP", tp["p"]), ("CVT", cv["p"])], key=lambda z: z[1])
holm, run = {}, 0.0
for i, (n, p) in enumerate(ps):
    run = max(run, min(1.0, p * (len(ps) - i)))
    holm[n] = run
rows += [{"quantity": "Tilting sets per propulsor", "architecture": "SLC", "rho": np.nan, "p": np.nan, "p Holm": np.nan, "designs": np.nan},
         {"quantity": "Tilting sets per propulsor", "architecture": "TP", "rho": tp["rho"], "p": tp["p"], "p Holm": holm["TP"], "designs": tp["aircraft"]},
         {"quantity": "Tilting sets per propulsor", "architecture": "CVT", "rho": cv["rho"], "p": cv["p"], "p Holm": holm["CVT"], "designs": cv["aircraft"]}]
d4 = pd.DataFrame(rows)
d4.to_csv(OUT / "R59_D4_trend_cells.csv", index=False)
print(d4.to_string())

# D5
fr = base.m.frames
lev = fr.archetype_levels_table(ctx.ds, ctx.v, base.cfg)
scr = fr.archetype_screens(lev, base.cfg)
names = {k: v for k, v in fr.SET_CODES.items()}
lev["code"] = lev["level"].map(lambda k: names[k][0])
lev["what it adds to the architecture"] = lev["level"].map(lambda k: names[k][1])
lev = lev.merge(scr[["level", "screens passed (config.yaml archetype_screens)"]] if "screens passed (config.yaml archetype_screens)" in scr.columns else scr.iloc[:, [0, -1]], on="level", how="left")
lev.to_csv(OUT / "R59_D5_levels_built.csv", index=False)
print(lev[["level", "code", "aircraft", "archetypes", "singletons", "effective number ²D", "largest share", "largest archetype"]].to_string())
