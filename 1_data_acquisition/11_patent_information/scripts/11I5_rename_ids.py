"""Renames the aircraft ids of the published files from <patent>_ua<N> ("unique aircraft") to <patent>_ad<N>
("aircraft design", the thesis term), 2026-11-21, author's request. Run from the dataset root, LAST (after 06d and 06f).
- text files (csv, json, md, txt, yaml) under the data folders: every id <patent>_ua<N> -> <patent>_ad<N>; csv headers
  ua -> ad and points_to_ua -> points_to_ad;
- folders and files named by aircraft id in 04_images/approved and 04_images/main_by_architecture.
Not renamed: the wizard record (02_patents/wizard_record_Batch_ALL.xlsx). Its aircraftName cells hold the pipeline's
generated names (<patent>_ua<N>), which notebook 04 compares with the ids it generates to tell a named aircraft from an
unnamed one; the rename is applied to the tables notebook 04 writes, not to its input.
Usage: python3 _build/scripts/11I5_rename_ids.py"""
import os, re
ID = re.compile(r"(?<=[A-Z0-9])_ua(?=\d)")
ROOTS = ["01_query", "02_patents", "03_aircraft", "04_images", "05_secondary", "06_gold_standard", "docs", "_build", "README.md", "DECISIONS.md"]
SKIP_DIRS = {"raw_pages", "crops", "nb04_v16", "scripts"}
EXT = (".csv", ".json", ".md", ".txt", ".yaml")
files = changed = 0
def walk():
    for r in ROOTS:
        if os.path.isfile(r): yield r; continue
        for d, ds, fs in os.walk(r):
            ds[:] = [x for x in ds if x not in SKIP_DIRS]
            for f in fs:
                if f.endswith(EXT): yield os.path.join(d, f)
for p in walk():
    s = open(p, encoding="utf-8", errors="surrogateescape").read()
    t = ID.sub("_ad", s)
    if p.endswith(".csv"):
        first, nl, rest = t.partition("\n")
        cols = ["ad" if c == "ua" else "points_to_ad" if c == "points_to_ua" else c for c in first.split(",")]
        t = ",".join(cols) + nl + rest
    if t != s: open(p, "w", encoding="utf-8", errors="surrogateescape").write(t); changed += 1
    files += 1
ren = 0
for base in ("04_images/approved", "04_images/main_by_architecture"):
    for d, ds, fs in os.walk(base, topdown=False):
        for n in fs + ds:
            if ID.search(n): os.rename(os.path.join(d, n), os.path.join(d, ID.sub("_ad", n))); ren += 1
print("text files read", files, "| changed", changed, "| folders/files renamed", ren)
