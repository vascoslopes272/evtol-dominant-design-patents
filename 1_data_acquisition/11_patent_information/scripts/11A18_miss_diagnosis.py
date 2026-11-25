"""Clause-by-clause diagnosis of the gold standard v2 families that show a census aircraft and are absent from the dataset.
Each clause of the dataset acquisition query (branch A of 01_query/query_branchA_plus_B.txt) is emulated with a regular expression on the PatSeer export fields
(CPC, Title, Abstract, Claims, Description). The emulation is not PatSeer itself: stemming and field coverage can differ.
Output: 06_gold_standard/v2/gs_v2_miss_diagnosis.csv"""
import re, glob, warnings
from pathlib import Path
import pandas as pd
warnings.filterwarnings("ignore")
D = Path(__file__).resolve().parents[1]
FAM = [("EHang EH216-S", "CN214267937U"), ("SkyDrive SD-05", "WO2024176796A1"), ("LIFT HEXA", "US11487283B1"), ("Pivotal BlackFly", "US2014097290A1"),
       ("Zero Gravity ZG-T6", "CN115214881A"), ("Muyutian EV4", "CN114954952B"), ("Crisalion Integrity 1", "HRP20220528T1"), ("CycloTech Blackbird", "EP4091939C0"),
       ("Aerofugia TF-2", "CN114771826A"), ("CityAirbus NextGen", "EP4556366A1"), ("Lanyi LE200", "CN117842348A"), ("EHang VT-30", "CN114572392B"),
       ("Zhiyuan Wearable Flying Device", "CN119348819B"), ("Zhiyuan Wearable Flying Device (2026)", "CN122540371B")]   # last four: search of 2026-11-12
X = pd.concat([pd.read_excel(f) for f in sorted(glob.glob(str(D / "01_query/patseer_g*.xlsx")))], ignore_index=True)
def find(rn):
    core = re.sub(r"[A-Z]\d?$", "", rn)
    m = X[(X["Record Number"] == rn) | X["Simple Family Members"].astype(str).str.contains(core, regex=False) | X["Record Number"].astype(str).str.startswith(core)]
    return m.iloc[0] if len(m) else None
# The clauses below are those of the query that produced the 1 639 families: branch A of 01_query/query_branchA_plus_B.txt
# (handoff of 7 Nov 2026, "the thesis query verbatim"). The file query_branchA.txt (Tab. 3.3) is an earlier text: 478 of the
# 1 639 families carry B64U and 667 have no crew word, which that text would have excluded. Checked on 2026-11-12.
W = r"(?:\W+\w+){0,%d}\W+"
def near(a, b, n): return re.compile(rf"\b(?:{a})\b{W % n}(?:{b})\b|\b(?:{b})\b{W % n}(?:{a})\b", re.I)
ARCH = near(r"aircraft|evtol|rotorcraft|vtol|vehicle", r"architecture|configuration|topology|airframe|fuselage|layout|frame|structur\w*|body|wing\w*|boom|tilt\w*|canard", 5)
ELEC = [near(r"electri\w*", r"motor\w*|propuls\w*|drive\w*", 3), re.compile(r"\bevtol\b", re.I), near("distributed", "propulsion", 2)]
ELEC_T = re.compile(r"\btiltrotor\b|\btilt[\s-]rotor\b|\btilting[\s-]rotor\w*|\btilting[\s-]propeller\w*", re.I)
VTOL_T = (re.compile(r"\bvtol\b", re.I), re.compile(r"\b(?:wing\w*|fuselage|airframe|rotor\w*|boom|canard|frame)\b", re.I))
FUEL = re.compile(r"\b(?:gasoline|petrol|jet|turbine)\W+engine\b|\bdiesel\b|internal[\s-]combustion|jet[\s-]propulsion|gas[\s-]turbine|fuel[\s-]cell|\bhydrogen\b", re.I)
UAV = re.compile(r"\b(?:UAV|unmanned|drone)\b", re.I)
TITLE = re.compile(r"\b(?:battery|charging[\s-]system\w*|power[\s-]management|cooling|wiring|seat\w*|display\w*|simulator\w*|gyroscopic\w*|gearbox|circuits|method)\b", re.I)
XC = ["B64B", "B64G", "B64F", "F28", "B64D11/06", "B64D43", "B64D45", "B60F5"]
rows = []
for ac, rn in FAM:
    r = find(rn)
    if r is None: rows.append({"aircraft": ac, "family": rn, "note": "text not in any export"}); continue
    cpc = [c.strip().replace(" ", "") for c in re.split(r"[;|\n]", str(r["CPC"])) if c.strip()]
    has = lambda pre: [c for c in cpc if any(c.startswith(p) for p in pre)]
    t = str(r["Title"]); ta = t + " " + str(r.get("Abstract", "")); tacd = " ".join(str(r.get(k, "")) for k in ["Title", "Abstract", "Claims", "Description"])
    elec = bool(has(["B64D27/30", "B64D27/31", "B64D27/32", "B64D27/33", "B64D27/34"]) or any(e.search(tacd) for e in ELEC) or ELEC_T.search(t) or (VTOL_T[0].search(t) and VTOL_T[1].search(t)))
    ok = {"1 CPC B64C29": bool(has(["B64C29"])), "2 architecture words (W5)": bool(ARCH.search(tacd)), "3 electric (CPC B64D27/30-34 or words)": elec,
          "4 no excluded CPC": not has(XC), "5 no combustion or fuel-cell words (TA)": not FUEL.search(ta), "6 no UAV, unmanned, drone (TA)": not UAV.search(ta), "7 no excluded title words": not TITLE.search(t)}
    ev = {"UAV hit": "; ".join(sorted({m.group(0).lower() for m in UAV.finditer(ta)})), "title hit": "; ".join(m.group(0) for m in TITLE.finditer(t)),
          "excluded CPC": "; ".join(has(XC)), "fuel hit": "; ".join(sorted({m.group(0).lower() for m in FUEL.finditer(ta)}))}
    rows.append({"aircraft": ac, "family": rn, "record_in_export": r["Record Number"], "title": t, "text_chars": len(tacd), **ok,
                 "fails": " | ".join(k for k, v in ok.items() if not v), **ev, "CPC": "; ".join(cpc[:14])})
out = pd.DataFrame(rows); out.to_csv(D / "06_gold_standard/v2/gs_v2_miss_diagnosis.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 90)
print(out[["aircraft", "family", "text_chars", "fails"]].to_string()); print(out[["aircraft", "UAV hit", "title hit", "excluded CPC", "fuel hit"]].to_string()); print(out[["aircraft","title","CPC"]].to_string())
