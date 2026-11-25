"""Brings the two image folders of 04_images in line with the tables (2026-11-21). Run from the dataset root, AFTER
11I5_rename_ids.py (folders and tables then carry the same ids). Nothing is deleted: what leaves goes to <work dir>/04_images_removed/.
Usage: python3 _build/scripts/11I6_images.py <work dir>
- approved/<aircraft_id>/<figure>: one copy of every figure with status approved in figure_table.csv (copied from its crop);
  folders and files no longer approved are moved out; MANIFEST.csv rewritten (dataset paths, bytes, sha256).
- main_by_architecture/<image_label>/<aircraft_id>.png (named aircraft: <image_label>/named/<name>__<aircraft_id>.png): the main figure (aircraft_table.main_figure) of every aircraft of
  ground_truth_798.csv, in the folder of its image label (thesis codes). The previous folder is moved out whole."""
import sys, os, shutil, hashlib
import pandas as pd
W = os.path.join(sys.argv[1], "04_images_removed"); os.makedirs(W, exist_ok=True)
rd = lambda f: pd.read_csv(f, dtype=str, keep_default_na=False, low_memory=False)
F = rd("03_aircraft/figure_table.csv"); T = rd("03_aircraft/aircraft_table.csv").set_index("aircraft_id")
G = rd("03_aircraft/ground_truth_798.csv"); P = rd("02_patents/patents_1639.csv").set_index("patent_id")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
A = "04_images/approved"; ap = F[F.status == "approved"]
VAR = "ad" if "ad" in F.columns else "ua"                     # the variant column, named as in the tables
want = {(a, f): p for a, f, p in zip(ap.aircraft_id, ap.image_file, ap.image_path)}
moved = copied = 0
for a in sorted(os.listdir(A)):
    d = os.path.join(A, a)
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        if (a, f) not in want:
            os.makedirs(os.path.join(W, "approved", a), exist_ok=True); shutil.move(os.path.join(d, f), os.path.join(W, "approved", a, f)); moved += 1
    if not os.listdir(d): os.rmdir(d)
for (a, f), src in want.items():
    dst = os.path.join(A, a, f)
    if not os.path.exists(dst): os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst); copied += 1
if os.path.exists(os.path.join(A, "MANIFEST.csv")): shutil.copy2(os.path.join(A, "MANIFEST.csv"), os.path.join(W, "approved_MANIFEST_before.csv"))
man = []
for r in ap.itertuples():
    dst = os.path.join(os.getcwd(), A, r.aircraft_id, r.image_file)
    man.append(dict(aircraft_id=r.aircraft_id, patent_id=r.patent_id, company=r.company, **{VAR: getattr(r, VAR)}, fig_key=r.fig_key, figure_file=r.image_file,
                    src=r.image_path, dst=dst, bytes=os.path.getsize(dst), sha256=sha(dst)))
pd.DataFrame(man).to_csv(os.path.join(A, "MANIFEST.csv"), index=False)
M = "04_images/main_by_architecture"
if os.path.exists(M):
    tgt = os.path.join(W, "main_by_architecture_before"); k = 1
    while os.path.exists(tgt): k += 1; tgt = os.path.join(W, f"main_by_architecture_before_{k}")
    shutil.move(M, tgt)
import re
GEN = re.compile(r"^[A-Z0-9]+_(ua|ad)\d+$")                      # a generated name, not an aircraft name
safe = lambda s: re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_")
for a, lab, nm in zip(G.aircraft_id, G.image_label, G.aircraft_name):
    src = T.at[a, "main_figure"]
    named = bool(nm) and not GEN.match(nm)                          # named aircraft go to <code>/named/<name>__<id>.png
    dst = os.path.join(M, lab or "none", "named", f"{safe(nm)}__{a}.png") if named else os.path.join(M, lab or "none", a + ".png")
    os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst)
print("approved: moved out", moved, "| copied in", copied, "| manifest rows", len(man), "| main images", len(G), "folders", sorted(os.listdir(M)))
