"""Gold standard v2, final unit: the programme.

Reads the census (one row per aircraft), applies the author's decisions of
2026-11-11, adds the winged aircraft of the TRL 6 widening, and writes
  06_gold_standard/v2/gs_v2_census_aircraft.csv    one row per aircraft
  06_gold_standard/v2/gs_v2_census_programmes.csv  one row per programme
A programme is every evtol.news aircraft of one company in one architecture
category. Its outcome is the best outcome among its aircraft.
"""
import pandas as pd
from pathlib import Path
V2 = Path(__file__).resolve().parents[1] / "06_gold_standard" / "v2"
WINGED = {"Lift + Cruise", "Vectored Thrust"}

c = pd.read_csv(V2 / "gs_v2_census.csv")
c = c[c.resultado != "fora"].copy()
# author's decisions, 2026-11-11
c = c[~((c.ck == "volocopter") & (c.aeronave == "VC1"))]      # proof-of-concept rig
c = c[~((c.ck == "leoflight") & (c.aeronave == "LX1-R"))]     # not clearly a company
def outcome(r):
    s = r.resultado
    if s.startswith("capturado"): return "captured"
    if s.startswith("em falta"): return "outside, patent found"
    return "no patent found"
c["outcome"] = c.apply(outcome, axis=1)
bf = (c.ck == "pivotal") & (c.aeronave == "BlackFly V2")
c.loc[bf, "outcome"] = "outside, patent found"                 # US2014097290A1, earlier version (level 2)
c.loc[bf, "familia_pool"] = "US2014097290A1"
# author's override: the CityAirbus NextGen has a wing and is a separate programme
ng = (c.ck == "airbus") & (c.aeronave == "CityAirbus NextGen")
c.loc[ng, "categoria_vfs"] = "Lift + Cruise"
c.loc[ng, "ids_nos_626"] = pd.NA
# author's override (2026-11-11): the Jaunt Journey is a slowed-rotor compound with a wing (SRW in the dataset), not a rotorcraft.
# SRW belongs to the independent-thrust family of the thesis taxonomy, so it is grouped with lift plus cruise.
c.loc[(c.ck == "jauntairmobility") & (c.aeronave == "Journey"), "categoria_vfs"] = "Lift + Cruise"
c["entry"] = "census (index or TRL 7)"

t = pd.read_csv(V2 / "gs_v2_census_widen_triage.csv")
a = pd.read_csv(V2 / "gs_v2_census_widen_answers.csv")
w = t.merge(a[["ck", "aeronave", "decisao"]], on=["ck", "aeronave"])
w = w[(w.decisao == "empresa") & (w.proposta != "carro") & w.categoria_vfs.isin(WINGED)].copy()
w["outcome"] = w.ja_ligado_aos_626.map({True: "captured", False: "search pending"})
# EHang was searched on 2026-11-10 (B64C29, B64C27/22-28): no family shows a winged EHang
w.loc[(w.ck == "ehang") & (w.aeronave == "VT-30"), "outcome"] = "no patent found"
w["ids_nos_626"] = w.ids_dataset
w["entry"] = "widening (winged, TRL 6)"
w["criterio"] = "VFS TRL 6, winged"

# PatSeer search of the widening companies (2026-11-11), read by the author in sheets_v2/census_widen_families.html
w = w[w.ck != "moller"]                                      # author: Skycar 100 is not clearly electric
w = w[w.ck != "bluespaceaircraft"]                           # author: Yunfan-2 is a cargo aircraft (evtol.news: passengers only "possibly") and its family CN118811132A claims an unmanned aerial vehicle
FOUND = {("muyutianaviationtechnology", "EV4"): "CN114954952B",
         ("crisalionmobility", "Concept Integrity 1"): "HRP20220528T1", ("cyclotech", "CycloTech Blackbird"): "EP4091939C0"}
NONE = {"aerofugia", "rangeaviation", "terrafugia", "thisisengineering",          # families read, none shows the aircraft
        "evtaerotechnics", "guangdongpengchengwanliaviationtechnology", "bartiniaero", "zeva",   # no family returned
        "avic", "beta"}   # 116 families (query_goldstandard_v2_census_avic_beta.txt): author, 11 Nov, none shows the AR-E3000 or the Ava XC
w["familia_pool"] = pd.NA
for (ck, ac), fam in FOUND.items():
    m = (w.ck == ck) & (w.aeronave == ac); w.loc[m, "outcome"] = "outside, patent found"; w.loc[m, "familia_pool"] = fam
w.loc[w.ck.isin(NONE) & (w.outcome == "search pending"), "outcome"] = "no patent found"
sg = (w.ck == "airspaceexperiencetechnologies")              # author: same concept, only the skids differ (level 2)
w.loc[sg, "outcome"] = "captured"; w.loc[sg, "ids_nos_626"] = "US2022144421A1_ua1"
# 2026-11-11, author: one threshold for every architecture (TRL 6 or higher). The wingless aircraft at TRL 6 that the author
# judged mature (gs_v2_census_wingless_stratum_answers.csv, "entra") and that open a new programme enter the census.
# The eight "entra" aircraft that are versions of programmes already present are not listed (the programme is the unit).
SIX = {("hangzhouzhiyuanresearchinstitute", "Wearable Flying Device"), ("jetson", "Jetson One"), ("kittyhawk", "Flyer"),
       ("dtaaircraftmanufacturer", "eVTOL-2 DTA"), ("rotorxaircraftmanufacturing", "Dragon"), ("verticalaerospace", "VA-X2")}
x = t.merge(a[["ck", "aeronave", "decisao"]], on=["ck", "aeronave"])
x = x[[k in SIX for k in zip(x.ck, x.aeronave)]].copy()
assert len(x) == 6 and (x.decisao == "empresa").all(), x[["ck", "aeronave", "decisao"]]
x["outcome"] = "no patent found"          # 20 families by applicant, read by the author (census_wingless_families.html): none
x["ids_nos_626"] = pd.NA; x["familia_pool"] = pd.NA
kh = x.ck == "kittyhawk"; x.loc[kh, "outcome"] = "captured"; x.loc[kh, "ids_nos_626"] = "US10526079B1_ua1"
x["entry"] = "TRL 6, wingless (author's maturity screen)"; x["criterio"] = "VFS TRL 6, wingless"
cols = ["entry", "criterio", "ck", "empresa", "aeronave", "categoria_vfs", "ano_1o_voo",
        "outcome", "ids_nos_626", "familia_pool", "url"]
for k in cols:
    if k not in w: w[k] = pd.NA
for k in cols:
    if k not in x: x[k] = pd.NA
air = pd.concat([c[cols], w[cols], x[cols]], ignore_index=True)
# 2026-11-12: last search of the lift plus cruise programmes with no patent (829 families, query_goldstandard_v2_census_lc_nopatent.txt).
# Claude screened them and the author read 17 candidates on sheets_v2/census_lc_nopatent.html (gs_v2_census_lc_nopatent_answers.csv).
# None of the four families is in the 1 639. Wanfeng Diamond, Pipistrel 801, Terrafugia TF-2A and EHang VT35: none (blank in the export, confirmed by the author in conversation on 2026-11-12).
FOUND2 = {("aerofugia", "TF-2"): "CN114771826A", ("airbus", "CityAirbus NextGen"): "EP4556366A1",
          ("rangeaviation", "LE200"): "CN117842348A", ("ehang", "VT-30"): "CN114572392B",
          # 2026-11-12, search of the wingless programmes with no patent (580 families, sheets_v2/census_wingless_nopatent.html,
          # gs_v2_census_wingless_nopatent_answers.csv): the author matched two Zhiyuan families and answered none for the ZG-ONE.
          ("hangzhouzhiyuanresearchinstitute", "Wearable Flying Device"): "CN119348819B; CN122540371B"}
for (ck, ac), fam in FOUND2.items():
    m = (air.ck == ck) & (air.aeronave == ac); assert m.sum() == 1, (ck, ac)
    air.loc[m, "outcome"] = "outside, patent found"; air.loc[m, "familia_pool"] = fam
air["programme"] = air.ck + " | " + air.categoria_vfs
air.to_csv(V2 / "gs_v2_census_aircraft.csv", index=False)

RANK = {"captured": 0, "outside, patent found": 1, "search pending": 2, "no patent found": 3}
rows = []
for p, g in air.groupby("programme", sort=False):
    g = g.assign(r=g.outcome.map(RANK)).sort_values("r")
    b = g.iloc[0]
    rows.append(dict(programme=p, empresa=b.empresa, categoria_vfs=b.categoria_vfs,
                     n_aircraft=len(g), aircraft="; ".join(g.aeronave),
                     outcome=b.outcome, decided_by=b.aeronave,
                     mixed="yes" if g.outcome.nunique() > 1 else "",
                     entry="census" if (g.entry.str.startswith("census")).any() else "widening",
                     tier="TRL 7 or higher" if (g.entry.str.startswith("census")).any() else "TRL 6"))
pr = pd.DataFrame(rows)
pr.to_csv(V2 / "gs_v2_census_programmes.csv", index=False)

print("aircraft", len(air), "programmes", len(pr))
print(pd.crosstab(air.categoria_vfs, air.outcome, margins=True))
print(pd.crosstab(pr.categoria_vfs, pr.outcome, margins=True))
print(pr[pr.mixed == "yes"][["programme", "aircraft", "outcome", "decided_by"]].to_string())
print(pr[pr.outcome == "search pending"][["empresa", "aircraft"]].to_string())
