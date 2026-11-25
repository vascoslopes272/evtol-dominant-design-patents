"""Phase 3, merge (2026-11-21): writes the author's review into the wizard record. For each patent of the REVIEW16 batch,
the record rows are replaced by the rows of the author's export, in place (same position in the record), with their cell
types. Two patents keep their record rows (author's rulings, audit/review/README.md): WO2024168389A1 (disapproval withdrawn,
original labels right) and US2022371727A1 (not re-saved; passes as recorded since wizard change 15). No value is edited.
Writes 02_patents/wizard_record_Batch_ALL.xlsx and audit/review/merge_log.csv."""
import re, csv
from openpyxl import load_workbook, Workbook
EXP='audit/review/exports/reviewed_patents_Batch_REVIEW16 (2).xlsx'; REC='02_patents/wizard_record_Batch_ALL.xlsx'
KEEP={'WO2024168389A1','US2022371727A1'}
base=lambda v: re.sub(r'_arch\d+$','',str(v))
def rows(f):
    ws=load_workbook(f)['Review']; it=ws.iter_rows(values_only=True); h=next(it); return h,[r for r in it if r[0] is not None]
hr,R=rows(REC); he,E=rows(EXP); assert hr==he,(hr,he)
batch=list(dict.fromkeys(base(r[0]) for r in load_workbook('audit/review/wizard_record_Batch_REVIEW16.xlsx',read_only=True)['Review'].iter_rows(min_row=2,values_only=True) if r[0]))
byE={}
for r in E: byE.setdefault(base(r[0]),[]).append(r)
assert set(byE)==set(batch),(set(byE)^set(batch))
take=[p for p in batch if p not in KEEP]
out=[]; done=set(); log=[]
for r in R:
    p=base(r[0])
    if p in take:
        if p not in done:
            out.extend(byE[p]); done.add(p)
            log.append([p,sum(base(x[0])==p for x in R),len(byE[p]),'replaced by the export'])
        continue
    out.append(r)
for p in KEEP: log.append([p,sum(base(x[0])==p for x in R),sum(base(x[0])==p for x in R),'record rows kept (author ruling)'])
assert done==set(take)
wb=Workbook(); ws=wb.active; ws.title='Review'; ws.append(list(hr))
for r in out: ws.append(list(r))
wb.save(REC)
with open('audit/review/merge_log.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['patent','rows_before','rows_after','action']); w.writerows(log)
print('record rows',len(R),'->',len(out),'| patents',len({base(r[0]) for r in R}),'->',len({base(r[0]) for r in out}),'| replaced',len(take),'| kept',len(KEEP))
