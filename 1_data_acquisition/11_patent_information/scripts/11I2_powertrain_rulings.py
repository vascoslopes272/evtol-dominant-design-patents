"""Author's powertrain rulings of 2026-11-20/21, as for the Chinook:
a row in 02_patents/review_decisions/POWERTRAIN_DECISIONS.csv and the same value in aircraft_identity_ALL.xlsx (Identity:
is_electric_human, is_electric_final, is_electric_final_variants, powertrain_review; Variants: is_electric_final).
EP4741286A1 No (gas engine drives the cruise pusher), ES2288083A1 No (gas turbines give direct thrust; reverses the 'keep'
of 2026-09-30), WO2024168389A1 Unknown (the text names no power source). Openpyxl edits cells in place, nothing else moves."""
import csv
from openpyxl import load_workbook
RUL={'EP4741286A1':('No','engine_propulsor','remove_mech','Yes',"gas engine (16) drives the rear pusher propeller (5) in cruise; only the main rotor is electric",'author ruling 2026-11-20 (T1 tag ElectricSimilar set in wizard 16_0), typed in by Claude'),
     'ES2288083A1':('No','engine_propulsor','remove_mech','Yes',"gas turbines (turbofan type) give direct thrust; generators and batteries only assist. Reverses the row of 2026-09-30 (Yes, multi_source, keep)",'author ruling 2026-11-21 (T1 tag ElectricSimilar set in wizard 16_0), typed in by Claude'),
     'WO2024168389A1':('Unknown','unstated','remove_none','Yes',"the text names no power source (propellers, 'may be ... an engine'); electric appears only in the background",'author ruling 2026-11-21 (ok to the proposaloposal), typed in by Claude')}
P='02_patents/review_decisions/POWERTRAIN_DECISIONS.csv'
rows=list(csv.reader(open(P,newline='',encoding='utf-8'))); h=rows[0]; body=rows[1:]
old={r[0]:r for r in body}
out=[r for r in body if r[0]!='ES2288083A1']
for pid,(el,rev,dec,before,note,src) in RUL.items():
    if pid=='ES2288083A1': note+=f" (old row: {','.join(old[pid][1:4])})"
    out.append([pid,el,rev,dec,'',"false",before,note,'2026-11-21',src])
with open(P,'w',newline='',encoding='utf-8') as f: w=csv.writer(f); w.writerow(h); w.writerows(out)
X='02_patents/aircraft_identity_ALL.xlsx'; wb=load_workbook(X)
def cols(ws): return {c.value:i+1 for i,c in enumerate(ws[1])}
ws=wb['Identity']; C=cols(ws); n=0
for r in range(2,ws.max_row+1):
    pid=ws.cell(r,C['patent_id']).value
    if pid in RUL:
        el=RUL[pid][0]; ws.cell(r,C['is_electric_human']).value=el; ws.cell(r,C['is_electric_final']).value=el
        v=ws.cell(r,C['is_electric_final_variants']).value
        if v: ws.cell(r,C['is_electric_final_variants']).value='; '.join([el]*len(str(v).split(';')))
        ws.cell(r,C['powertrain_review']).value=RUL[pid][1]; n+=1
ws=wb['Variants']; C=cols(ws); m=0
for r in range(2,ws.max_row+1):
    if ws.cell(r,C['patent_id']).value in RUL: ws.cell(r,C['is_electric_final']).value=RUL[ws.cell(r,C['patent_id']).value][0]; m+=1
wb.save(X); print('powertrain rows',len(out),'| identity rows',n,'| variant rows',m)
