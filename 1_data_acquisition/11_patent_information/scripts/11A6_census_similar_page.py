"""Gold standard v2 census, similar-aircraft reading: for each census aircraft NOT captured, is a design among the 626 similar enough
to count as agreement (level 2, version by the same applicant, or level 3, similar design of another applicant, the Axe rule)?
Same page as 02f. Output: sheets_v2/census_similar.html ; export gs_v2_census_similar_<stamp>.csv.

Original 02f note:

For the census aircraft the author is unsure about, the 626 designs of the same evtol.news parent class (and every design of the same
company) are ranked by DINOv2 similarity between the evtol.news photos and the design's patent figures (dinov2-large_518, layer 24 cls,
embeddings already computed for the thesis). The top 48 are shown with their main figure. The ranking only orders the page: the
author's eye decides. Output: sheets_v2/census_find.html ; export gs_v2_census_find_<stamp>.csv (aeronave, design id or 'nenhum').
"""
import os
import html, sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
src = (Path(__file__).resolve().parent / "02e_census_review_page.py").read_text(encoding="utf-8")
exec(src[src.index("import re, html"):src.index("CSS = ")])          # paths, tables, small(), photos()
EMB = Path(os.environ.get("EVTOLNEWS_EMBEDDINGS", "data/evtolnews/2_embedding_extraction"))
def load(d):
    m = pd.read_parquet(EMB / d / "dinov2-large_518/metadata.parquet"); e = np.load(EMB / d / "dinov2-large_518/emb_layer24_cls.npy")
    return m, e / np.linalg.norm(e, axis=1, keepdims=True)
mp, ep = load("embeddings"); md, ed = load("patent_reference")
FOLD = {"VT": ["TW", "TR", "TB", "PTC", "DS", "CVT"], "LC": ["SLC", "SRW", "CVT"], "WM": ["MR"], "ER": ["RC", "SRW"], "HB": ["HB", "PFV", "MR"]}
CLS = {"Vectored Thrust": "VT", "Lift + Cruise": "LC", "Wingless": "WM", "Rotorcraft": "ER", "Hoverbike/PFD": "HB"}
TARGETS = sys.argv[1:] or ["BlackFly V2", "LX1-R", "e-R44 1st Generation", "Koncepto Millenya", "Skyla", "Romeo", "Matrix 1", "801", "Wanfeng Diamond", "VT35", "CityAirbus NextGen", "VC1", "ZG-ONE", "ZG-T6", "EH216-S", "SD-05", "HEXA"]
CO = {"BlackFly V2": "Pivotal|Opener|Leng|SkyKar", "LX1-R": "LEO Flight|Bitar", "e-R44 1st Generation": "Tier 1", "Koncepto Millenya": "Star 8", "Skyla": "Voltline", "Wanfeng Diamond": "Wanfeng|Diamond Aircraft", "CityAirbus NextGen": "Airbus", "801": "Pipistrel", "Romeo": "ERC System|IABG", "Matrix 1": "Vertaxi|Yufeng", "VC1": "Volocopter|e-volo", "ZG-ONE": "Zero ?G", "ZG-T6": "Zero ?G", "EH216-S": "ehang", "SD-05": "SkyDrive", "HEXA": "LIFT Aircraft", "Nexus 4EX": "Bell", "CarryAll V2000CG": "AutoFlight", "Prosperity V2000EM": "AutoFlight", "CityAirbus NextGen": "Airbus", "VT35": "ehang", "801": "Pipistrel", "Romeo": "ERC System|IABG", "Matrix 1": "Vertaxi|Yufeng", "Axe": "Skyfly"}
CSS = """body{font:14px sans-serif;margin:0;background:#f4f4f4}main{max-width:1600px;margin:0 auto;padding:0 20px 80px}h2{background:#234;color:#fff;padding:8px;margin-top:40px}
.ref{display:flex;gap:10px;flex-wrap:wrap;position:sticky;top:46px;background:#f4f4f4;padding:6px 0;z-index:5;border-bottom:2px solid #36c}.ref img{height:170px;border:3px solid #36c}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:8px;margin-top:8px}.d{background:#fff;border:2px solid #ccc;padding:6px;cursor:pointer}.d img{width:100%;height:190px;object-fit:contain}
.d small{display:block}.d.on{border:4px solid #2a7;background:#eafaf0}.d.co{border-color:#d90}.nb{font-size:15px;padding:8px 14px;margin:8px 0}.nb.on{background:#999;color:#fff}
#bar{position:sticky;top:0;z-index:9;background:#123;color:#fff;padding:10px 20px;display:flex;gap:14px;align-items:center}#bar button{font-size:15px;padding:7px 14px}"""
JS = r"""
const KEY='gs_v2_census_similar_v1';let A={};try{A=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
function save(){try{localStorage.setItem(KEY,JSON.stringify(A))}catch(e){}render()}
function render(){let n=0,t=0;document.querySelectorAll('section').forEach(s=>{t++;const a=A[s.dataset.ac]||{ids:[],none:false};if(a.ids.length||a.none)n++;
  s.querySelectorAll('.d').forEach(d=>d.classList.toggle('on',a.ids.includes(d.dataset.id)));s.querySelector('.nb').classList.toggle('on',a.none);
  s.querySelector('.st').textContent=a.ids.length?(' escolhido: '+a.ids.join(', ')):(a.none?' nenhum destes':' por responder')});
  document.getElementById('prog').textContent=n+' de '+t+' respondidas'}
document.addEventListener('click',e=>{const d=e.target.closest('.d'),b=e.target.closest('.nb');if(!d&&!b)return;const ac=(d||b).closest('section').dataset.ac;A[ac]=A[ac]||{ids:[],none:false};
  if(d){if(e.target.tagName==='A')return;const i=A[ac].ids.indexOf(d.dataset.id);if(i>=0)A[ac].ids.splice(i,1);else A[ac].ids.push(d.dataset.id);A[ac].none=false}else{A[ac].none=!A[ac].none;if(A[ac].none)A[ac].ids=[]}save()});
function exportCSV(){const rows=[['aeronave','resposta']];document.querySelectorAll('section').forEach(s=>{const a=A[s.dataset.ac]||{ids:[],none:false};rows.push([s.dataset.ac,a.ids.length?a.ids.join(' '):(a.none?'nenhum':'')])});
  const csv=rows.map(r=>r.map(x=>'"'+String(x).replace(/"/g,'""')+'"').join(',')).join('\n');const d=new Date(),p=n=>String(n).padStart(2,'0');
  const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));a.download='gs_v2_census_similar_'+d.getFullYear()+p(d.getMonth()+1)+p(d.getDate())+p(d.getHours())+p(d.getMinutes())+'.csv';a.click()}
render();"""
parts = [f"<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Censo: aeronave semelhante</title><style>{CSS}</style>",
         "<div id='bar'><b id='prog'></b><button onclick='exportCSV()'>Exportar (CSV)</button><span>Clica no design do dataset que é semelhante o bastante à aeronave das fotos azuis para contar como concordância. Moldura laranja = mesma empresa.</span></div><main>",
         "<h1>Há nos 626 um design semelhante o bastante a esta aeronave?</h1><p>Uma secção por cada aeronave do censo que <b>não</b> foi capturada. Usa a mesma régua do Axe e da AutoFlight: mesma arquitectura, mesma disposição de asas, rotores e hélices, de modo que dirias que é o mesmo tipo de aeronave. Se for só a mesma categoria (por exemplo, outro lift + cruise qualquer), não conta. Os designs estão ordenados por semelhança visual (DINOv2); a ordem só ajuda. Se nenhum serve, carrega em <b>Nenhum destes</b>.</p>"]
for t in TARGETS:
    r = C[C.aeronave == t]
    if r.empty: print("?", t); continue
    r = r.iloc[0]; slugs = str(r.slugs).split("|")
    q = ep[mp.aircraft_uid.isin(slugs).values]
    co_txt = D6.company.fillna("") + " | " + D6.assignee.fillna("")      # the company field is "Unknown / Independent" for 128 designs: match the original assignee too
    cand = D6[D6.topType.isin(FOLD[CLS[r.categoria_vfs]]) | co_txt.str.contains(CO.get(t, "§§§"), case=False)].copy()
    sim = pd.Series(0.0, index=cand.index)
    if len(q):
        s = pd.Series((ed @ q.T).max(axis=1), index=md.aircraft_uid.values).groupby(level=0).max()
        sim = cand.index.to_series().map(s).fillna(0.0)
    cand["sim"] = sim; cand["same"] = co_txt[cand.index].str.contains(CO.get(t, "§§§"), case=False)
    # no design of the same company in the dataset: show the whole class from eight years before the aircraft's first year, not only the top 48
    rest = cand[~cand.same].sort_values("sim", ascending=False)
    if not cand.same.any():
        y0 = float(str(r.ano_1o_voo)[:4] or 2000) - 8
        rest = rest[pd.to_numeric(rest.priority_year, errors="coerce").fillna(0) >= y0].head(60)
    else: rest = rest.head(48)
    top = pd.concat([cand[cand.same].sort_values("sim", ascending=False), rest])
    parts.append(f"<section data-ac='{html.escape(t)}'><h2>{html.escape(r.empresa)} · {html.escape(t)} ({r.categoria_vfs}, {str(r.ano_1o_voo)[:4]}) <span class='st'></span></h2>"
                 f"<div class='ref'>{''.join(f'<img src=\"{p.relative_to(SH)}\">' for p in photos(r.slugs, 4))}<a href='{r.url}' target='_blank' style='align-self:center'>página VFS</a></div>"
                 f"<button class='nb'>Nenhum destes é semelhante o bastante ao {html.escape(t)}</button><div class='g'>")
    for i, d in top.iterrows():
        p = small(d.main_figure, DS / (i + ".jpg"))
        parts.append(f"<div class='d{' co' if d.same else ''}' data-id='{i}'>{f'<img src=\"_census/{p.name}\" loading=\"lazy\">' if p else '<i>sem imagem</i>'}<small><b>{i}</b> · {d.topType} · {d.priority_year} · sem. {d.sim:.2f}</small><small>{html.escape(d.company)}</small><small>{html.escape(d.title[:70])} <a href='https://patents.google.com/patent/{d.patent_id}/en' target='_blank'>patente</a></small></div>")
    parts.append("</div></section>"); print(t, len(top), int(top.same.sum()), "da empresa", flush=True)
parts.append(f"</main><script>{JS}</script>")
(SH / "census_similar.html").write_text("\n".join(parts), encoding="utf-8"); print(SH / "census_similar.html")
