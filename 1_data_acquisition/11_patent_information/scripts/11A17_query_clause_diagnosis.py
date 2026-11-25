"""Clause-by-clause reading of the thesis query (branch A) and of branch B on families with full text.

Each clause of 01_query/query_branchA_plus_B.txt is re-expressed as a regular expression over the PatSeer export fields
(T = title, TA = title + abstract, TACD = title + abstract + claims + description, CPC). 'x Wn y' is read as x and y within n words,
either order. This is an approximation of PatSeer's own matching, on the one record exported per family, so a result here is an
indication of which clause rejects a family and not a replay of the search engine.
"""
import re
from pathlib import Path
import pandas as pd
DATA_DIR = Path(__file__).resolve().parent.parent

def near(a, b, n):
    return re.compile(rf"\b(?:{a})\b(?:\W+\w+){{0,{n}}}?\W+(?:{b})\b|\b(?:{b})\b(?:\W+\w+){{0,{n}}}?\W+(?:{a})\b", re.I)
VEH = r"aircraft|evtol|rotorcraft|vtol|vehicle"
ARCH = r"architecture|configuration|topology|airframe|fuselage|layout|frame|structur\w*|body|wing\w*|boom|tilt\w*|canard"
R = {
 "arch": near(VEH, ARCH, 5),
 "elec": re.compile(r"\bevtol\b", re.I), "elec2": near(r"electri\w*", r"motor\w*|propuls\w*|drive\w*", 3), "elec3": near("distributed", "propulsion", 2),
 "multi": re.compile(r"\b(?:multicopter\w*|multirotor\w*|multi[- ]rotor\w*|multi[- ]copter\w*|quadcopter\w*|quadrotor\w*|hexacopter\w*|octocopter\w*|volocopter\w*)\b", re.I),
 "multi2": near(r"four|six|eight|plurality|array|multiple", r"rotor\w*|propeller\w*", 3),
 "crew": re.compile(r"\b(?:passenger\w*|occupant\w*|cabin\w*|cockpit\w*|manned|pilot\w*|crew)\b", re.I),
 "crew_u": re.compile(r"\b(?:passenger\w*|occupant\w*|cabin\w*|manned)\b", re.I),
 "comb": re.compile(r"\b(?:gasoline|petrol|jet|turbine) engine\b|\bdiesel\b|internal combustion|jet propulsion|gas turbine|fuel cell|\bhydrogen\b", re.I),
 "uav": re.compile(r"\b(?:uav|unmanned|drone)\b", re.I),
 "heli": re.compile(r"main rotor|tail rotor|\bcoaxial\b|\btandem\b|\bswashplate\b", re.I),
 "title": re.compile(r"\bbattery\b|charging system\w*|power management|\bcooling\b|\bwiring\b|\bseat\w*|\bdisplay\w*|\bsimulator\w*|\bgyroscopic\w*|\bgearbox\b|\bcircuits\b|\bmethod\b", re.I),
 "tilt_t": re.compile(r"tiltrotor|tilt rotor|tilting rotor\w*|tilting propeller\w*", re.I),
}
CPC_EL = re.compile(r"B64D27/3[0-4]"); CPC_NOT = re.compile(r"B64B|B64G|B64F|F28|B64D11/06|B64D43|B64D45|B60F5")

def clauses(r):
    T = str(r.get("Title", "")); TA = T + " " + str(r.get("Abstract", ""))
    TACD = TA + " " + str(r.get("Claims", "")) + " " + str(r.get("Description", "")); cpc = str(r.get("CPC", ""))
    yr = pd.to_datetime(r.get("Publication/Issue Date"), errors="coerce").year
    elec = bool(CPC_EL.search(cpc) or R["elec"].search(TACD) or R["elec2"].search(TACD) or R["elec3"].search(TACD))
    c = {"A1 CPC B64C29": "B64C29" in cpc,
         "B1 scope (27/08 no 29, or U10/1 + crew)": (("B64C27/08" in cpc) and ("B64C29" not in cpc)) or (bool(re.search(r"B64U10/1", cpc)) and bool(R["crew_u"].search(TA))),
         "B2 multicopter words (TACD)": bool(R["multi"].search(TACD) or R["multi2"].search(TACD)),
         "B3 crew words (TA)": bool(R["crew"].search(TA)),
         "4 architecture words (TACD)": bool(R["arch"].search(TACD)),
         "5 electric (CPC or TACD)": elec,
         "6 year 2005-2026": bool(2005 <= (yr or 0) <= 2026),
         "N1 not excluded CPC": not CPC_NOT.search(cpc),
         "N2 not combustion (TA)": not R["comb"].search(TA),
         "N3 not UAV without crew (TA)": not (R["uav"].search(TA) and not R["crew_u"].search(TA)),
         "N4 not helicopter words (TA)": not R["heli"].search(TA),
         "N5 not component title": not R["title"].search(T)}
    c["branch B"] = all(v for k, v in c.items() if k != "A1 CPC B64C29")
    return c

if __name__ == "__main__":
    pool = pd.read_excel(DATA_DIR / "01_query/patseer_goldstandard_572_2026-11-08.xlsx")
    rv = pd.read_excel(DATA_DIR / "06_gold_standard/v2/goldstandard_pool_review.xlsx")
    pos = rv[(rv.coder_in_domain == "yes") & (rv.coder_shows_crewed_aircraft == "s") & (rv.coder_architecture == "MR")]
    P = pool[pool["Record Number"].isin(pos["Record Number"])].merge(pos[["Record Number", "coder_design_key", "coder_vfs_design", "coder_in_627"]], on="Record Number")
    out = pd.concat([P[["Record Number", "coder_vfs_design", "coder_in_627", "Title"]], P.apply(lambda r: pd.Series(clauses(r)), axis=1)], axis=1)
    out.to_csv(DATA_DIR / "06_gold_standard/v2/query_clause_diagnosis_wingless.csv", index=False)
    pd.set_option("display.width", 250, "display.max_colwidth", 30)
    cl = [c for c in out.columns if c[0] in "AB456N" and c != "branch B"]
    print(len(out), "wingless in-domain families coded by the author")
    print(out[cl].mean().round(2).to_string())
    short = out.rename(columns={c: c.split(" ")[0] for c in cl})
    print(short[["Record Number", "coder_vfs_design"] + [c.split(" ")[0] for c in cl] + ["branch B"]].replace({True: "ok", False: "FAIL"}).to_string())
