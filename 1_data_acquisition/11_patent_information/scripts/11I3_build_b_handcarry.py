"""Build B (2026-11-21): carries the changes into the CURRENT aircraft_table.csv by hand, without the pipeline, to check
build A (notebook 04 re-run). Steps: (1) every record cell that changed between the pre-merge record (git tag
pre-merge-2026-11-21) and the merged record is written into its column (code before ' — '), on the rows of that variant;
(2) the v16.0 readings (TR/TB -> TP/TF, hull_array/core_layout -> fuselage, purity tick -> G1 uncertainty);
(3) the powertrain rulings of 2026-11-21 (is_electric_final, ElectricSimilar tag). Derived columns are NOT recomputed.
Usage: python3 _build/scripts/11I3_build_b_handcarry.py <pre-merge record.xlsx> <out.csv>"""
import sys, re
import pandas as pd
OLD, OUT = sys.argv[1], sys.argv[2]
T = pd.read_csv('03_aircraft/aircraft_table.csv', dtype=str, keep_default_na=False, low_memory=False).set_index('aircraft_id')
o = pd.read_excel(OLD, sheet_name='Review', dtype=str).fillna('')
n = pd.read_excel('02_patents/wizard_record_Batch_ALL.xlsx', sheet_name='Review', dtype=str).fillna('')
k = ['Patent_ID', 'Section', 'Sub_Dimension', 'Field']
for d in (o, n): d.drop_duplicates(k, keep='last', inplace=True)
m = o[k + ['Value']].merge(n[k + ['Value']], on=k, how='outer', suffixes=('_old', '_new')).fillna('')
m = m[m.Value_old != m.Value_new]
code = lambda v: v.split(' — ')[0].strip() if ' — ' in v else v.strip()
def aid(pid):
    b = re.sub(r'_arch\d+$', '', pid); a = re.search(r'_arch(\d+)$', pid); return f"{b}_ua{a.group(1) if a else 1}", b
applied = skipped = 0
for r in m.itertuples():
    a, b = aid(r.Patent_ID)
    if r.Field not in T.columns: skipped += 1; continue
    rows = [a] if a in T.index else ([x for x in T.index if x.startswith(b + '_ua')] if not re.search(r'_arch\d+$', r.Patent_ID) else [])
    for x in rows: T.at[x, r.Field] = code(r.Value_new)
    applied += bool(rows)
# v16.0 readings on the whole table
T['topType'] = T.topType.replace({'TR': 'TP', 'TB': 'TF'})
if 'ml_topType' in T.columns: T['ml_topType'] = T.ml_topType.replace({'TR': 'TP', 'TB': 'TF'})
old_cols = [c for c in T.columns if re.match(r'^(hull_array|core_layout)_', c)]
cnt = lambda v: 1 if v == 'True' else (int(v) if str(v).isdigit() else 0)
for x in T.index:
    has_old = any(T.at[x, c] not in ('',) for c in old_cols)
    if not has_old or cnt(T.at[x, 'fuselage_count']) > 0: continue
    for c in [c for c in T.columns if c.startswith('fuselage_')]: T.at[x, c] = ''
    for c in old_cols:
        if T.at[x, c] != '': T.at[x, re.sub(r'^(hull_array|core_layout)_', 'fuselage_', c)] = T.at[x, c]
T = T.drop(columns=old_cols)
DEF = 'There is ambiguity, from the images, about which architecture it is.'
for x in T.index[T.notPureArch == 'True']:
    T.at[x, 'g1_humanUncertain'] = 'True'
    if not T.at[x, 'g1_uncertainNote'].strip(): T.at[x, 'g1_uncertainNote'] = DEF
T = T.drop(columns=['notPureArch'])
# powertrain rulings
for pid, el in {'EP4741286A1': 'No', 'ES2288083A1': 'No', 'WO2024168389A1': 'Unknown'}.items():
    s = T.patent_id == pid; T.loc[s, 'is_electric_final'] = el
    if el == 'No':
        T.loc[s & (T.is_primary == 'True'), 'edgeTags'] = T.loc[s & (T.is_primary == 'True'), 'edgeTags'].map(lambda v: '|'.join(sorted(set(filter(None, v.split('|'))) | {'ElectricSimilar'})))
T.reset_index().to_csv(OUT, index=False)
print('record cells changed', len(m), '| written', applied, '| field not a table column', skipped, '| out', T.shape)
