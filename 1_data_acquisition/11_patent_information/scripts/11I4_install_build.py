"""Installs a notebook-04 build (build A, 2026-11-21) into eVTOL_dataset_v1 and rebuilds every table derived from it.
Usage (from the dataset root):
  python3 _build/scripts/11I4_install_build.py <NB04 out dir> <analysis repo dir>
1. aircraft_table.csv, figure_table.csv, 02_patents/data_dictionary.csv; figure paths as in the dataset (approved figures in
   04_images/approved/<aircraft_id>/, file_exists recomputed); BUILD_LOG and ACTION_FLAGS into _build/.
2. ground_truth_798.csv from sheet ground_truth of 1639_LABELS.xlsx.
3. viz/data.py (the thesis analysis loader): designs_627.csv and aircraft_627.csv (the primary representative designs;
   firm, priority_year, final_trl, trl_source carried from the previous files) and patents_1639.csv.
4. images_index.csv: the wizard columns (t2_*, fig_key, is_main, is_primary, approved_copy_path) re-read from the new
   figure_table, patent_representative from the new patents table.
5. _build/viz_counts.json."""
import sys, os, json, shutil
import pandas as pd
OUT, REPO = sys.argv[1], sys.argv[2]; D = os.getcwd()
import re
def rd(f):
    # the published files carry <patent>_ad<N> (06e); notebook 04 and the analysis loader write <patent>_ua<N>, so the
    # previous files are read back in the pipeline's form and 06e renames everything at the end
    df = pd.read_csv(f, dtype=str, keep_default_na=False, low_memory=False)
    df = df.rename(columns={"ad": "ua", "points_to_ad": "points_to_ua"})
    return df.apply(lambda c: c.str.replace(r"(?<=[A-Z0-9])_ad(?=\d)", "_ua", regex=True))
def ints(df): return df.apply(lambda c: c.str.replace(r"^(\d+)\.0$", r"\1", regex=True))
shutil.copy(f"{OUT}/tables/aircraft_table.csv", "03_aircraft/aircraft_table.csv")
shutil.copy(f"{OUT}/tables/data_dictionary.csv", "02_patents/data_dictionary.csv")
# thesis names of the stored ids whose wizard label differs from the thesis wording (author, 2026-11-21; Tables A.2-A.4)
THESIS = [(r"^fusKin$", {"TiltBody": "Tail-sitter"}), (r"^wing\d+_role$", {"Stacked": "Biplane"}),
          (r"_chord$", {"Front": "Tractor", "Back": "Pusher", "None": "None or cannot tell"}),
          (r"_zoneSpan$", {"FullSpan": "Across the extension of the wing"})]
_dd = pd.read_csv("02_patents/data_dictionary.csv", dtype=str, keep_default_na=False)
def _tn(col, opts):
    ids = {o.split("=")[0].strip() for o in opts.split("|") if "=" in o}
    for pat, m in THESIS:
        if re.search(pat, col): return " | ".join(f"{k}={v}" for k, v in m.items() if k in ids)
    return ""
_dd["thesis_names"] = [_tn(c, o) for c, o in zip(_dd.column, _dd.options)]
_dd.to_csv("02_patents/data_dictionary.csv", index=False)
F = rd(f"{OUT}/tables/figure_table.csv"); ap = F.status.eq("approved")
F["approved_copy_path"] = [f"{D}/04_images/approved/{a}/{f}" if s else "" for a, f, s in zip(F.aircraft_id, F.image_file, ap)]
F["file_exists"] = F.image_path.map(lambda p: str(bool(p) and os.path.exists(p)))
F.to_csv("03_aircraft/figure_table.csv", index=False)
shutil.copy(f"{OUT}/BUILD_LOG.md", "_build/NB04_BUILD_LOG.md"); shutil.copy(f"{OUT}/ACTION_FLAGS.csv", "_build/NB04_ACTION_FLAGS.csv")
g = pd.read_excel(f"{OUT}/1639_LABELS.xlsx", sheet_name="ground_truth", dtype=str).fillna("")
g.to_csv("03_aircraft/ground_truth_798.csv", index=False)
sys.path.insert(0, REPO)
from viz import config as vc
from viz.data import load_dataset
ds = load_dataset(vc.load(f"{D}/_config/labelling_analysis.eVTOL_dataset_v1.yaml"))
v = ds.variants; ids = list(v.aircraft_id)
d6 = rd("03_aircraft/designs_627.csv").set_index("aircraft_id"); a6 = rd("03_aircraft/aircraft_627.csv").set_index("aircraft_id")
new = sorted(set(ids) - set(d6.index)); assert not new, f"new designs need firm / year / TRL: {new}"
d = d6.loc[ids].reset_index(); d["topType"] = v.set_index("aircraft_id").loc[ids, "topType"].fillna("").astype(str).values
d.to_csv("03_aircraft/designs_627.csv", index=False)
V = v.copy()
for c in ["firm", "priority_year", "final_trl", "trl_source"]: V[c] = a6.loc[V.aircraft_id, c].values
order = ["aircraft_id"] + [c for c in a6.columns if c in V.columns] + [c for c in V.columns if c not in a6.columns and c != "aircraft_id"]
V[order].to_csv("03_aircraft/aircraft_627.csv", index=False)   # written as the loader returns it, like the previous file
P0 = rd("02_patents/patents_1639.csv"); P = ds.patents.copy(); idt = ds.identity.set_index("patent_id")
for c in P0.columns:
    if c not in P.columns and c in idt.columns: P[c] = P.patent_id.map(idt[c])
P = P[[c for c in P0.columns if c in P.columns]]; P = P.astype(object).where(P.notna(), "").astype(str)
ints(P).to_csv("02_patents/patents_1639.csv", index=False)
I = rd("04_images/images_index.csv")
key = lambda a, f, k: (a, f, k)
Fm = {key(a, f, k): r for a, f, k, r in zip(F.aircraft_id, F.image_file, F.fig_key, F.to_dict("records"))}
Fa = {}
for r in F.to_dict("records"): Fa.setdefault((r["aircraft_id"], r["image_file"]), r)
changed = 0
for i, row in I.iterrows():
    if not row.aircraft_id or not row.crop_file: continue
    r = Fm.get(key(row.aircraft_id, row.crop_file, row.fig_key)) or Fa.get((row.aircraft_id, row.crop_file))
    new = ({"fig_key": r["fig_key"], "t2_verdict": r["status"] or "not_judged", "t2_status": r["status"], "t2_parts": r["parts"], "t2_arch": r["arch"],
            "is_main": r["is_main"], "is_primary": r["is_primary"], "approved_copy_path": r["approved_copy_path"]} if r else
           ({"t2_verdict": "not_judged", "t2_status": "", "t2_parts": "", "t2_arch": "", "approved_copy_path": ""} if row.t2_status else {}))
    for c, x in new.items():
        if I.at[i, c] != x: I.at[i, c] = x; changed += 1
rep = dict(zip(P.patent_id, P.is_representative))
pr = I.patent_id.map(rep).fillna(I.patent_representative); changed += int((pr != I.patent_representative).sum()); I["patent_representative"] = pr
I.to_csv("04_images/images_index.csv", index=False)
json.dump(ds.counts, open("_build/viz_counts.json", "w"), indent=1)
print("designs", len(d), "| patents representative", int((P.is_representative == "True").sum()), "| images_index cells changed", changed, "| counts", ds.counts)
