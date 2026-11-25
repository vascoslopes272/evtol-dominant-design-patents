"""Writes a wizard export into the record (2026-11-21): for every patent in the export, the record rows of that patent are
replaced, in place and with their cell types, by the export's rows. No value is edited. Run from the dataset root.
Usage: python3 _build/scripts/11I7_merge_export.py <reviewed_patents_*.xlsx> [patent ...]   (default: every patent in the export)"""
import re, sys
from openpyxl import load_workbook, Workbook
EXP, ONLY = sys.argv[1], set(sys.argv[2:]); REC = "02_patents/wizard_record_Batch_ALL.xlsx"
base = lambda v: re.sub(r"_arch\d+$", "", str(v))
def rows(f):
    it = load_workbook(f)["Review"].iter_rows(values_only=True); h = next(it); return h, [r for r in it if r[0] is not None]
hr, R = rows(REC); he, E = rows(EXP); assert hr == he, (hr, he)
by = {}
for r in E: by.setdefault(base(r[0]), []).append(r)
take = {p for p in by if not ONLY or p in ONLY}; assert take <= {base(r[0]) for r in R}, take - {base(r[0]) for r in R}
out, done = [], set()
for r in R:
    p = base(r[0])
    if p in take:
        if p not in done: out.extend(by[p]); done.add(p)
        continue
    out.append(r)
wb = Workbook(); ws = wb.active; ws.title = "Review"; ws.append(list(hr))
for r in out: ws.append(list(r))
wb.save(REC); print("record rows", len(R), "->", len(out), "| patents replaced", sorted(done))
