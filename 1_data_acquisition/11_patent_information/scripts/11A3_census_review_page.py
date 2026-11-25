"""Gold standard v2 census: one review page for the author, every aircraft of the census with the evidence behind each decision.

Per aircraft: evtol.news photos, why it entered (index edition or the TRL >= 7 sentence), the domain fields of its evtol.news page
(power source, capacity, piloting), the outcome, and, when captured, the drawing of the dataset design it was matched to.
Buttons record the author's verdict; the export (gs_v2_census_review_<stamp>.csv) is read by notebook 02.
Output: 06_gold_standard/v2/sheets_v2/census_review.html
"""
import os
import re, html
from pathlib import Path
import pandas as pd
from PIL import Image
DATA_DIR = Path(__file__).resolve().parent.parent
OUT = DATA_DIR / "06_gold_standard/v2"; SH = OUT / "sheets_v2"; PH = SH / "_vfs"; DS = SH / "_census"; PH.mkdir(exist_ok=True); DS.mkdir(exist_ok=True)
SRC = Path(os.environ.get("EVTOLNEWS_SOURCE", "data/evtolnews/0_source"))
C = pd.read_csv(OUT / "gs_v2_census.csv").fillna("")
A = pd.read_csv(DATA_DIR / "05_secondary/vfs/aircraft.csv", keep_default_na=False).set_index("slug_key")
D6 = pd.read_csv(DATA_DIR / "03_aircraft/aircraft_627.csv", dtype=str).fillna("").set_index("aircraft_id")
IMG = pd.read_csv(SRC / "images.csv", dtype=str).fillna(""); IMG = IMG[IMG.dl_error == ""]
ANS = pd.read_csv(OUT / "gs_v2_census_answers.csv", dtype=str).fillna("").set_index("aeronave")
IM = pd.read_csv(OUT / "gs_v2_index_map.csv").fillna("")
def small(src, dst, s=520):
    if not dst.exists():
        try: im = Image.open(src).convert("RGB"); im.thumbnail((s, s)); im.save(dst, quality=80)
        except Exception: return None
    return dst
def photos(slugs, n=3):
    out = []
    for s in str(slugs).split("|"):
        for _, r in IMG[IMG.slug_key == s].sort_values("img_pos", key=lambda x: x.astype(int)).iterrows():
            p = small(r.local_path, PH / (r.image_uid + ".jpg"))
            if p: out.append(p)
            if len(out) >= n: return out
    return out
CSS = """body{font:14px sans-serif;margin:0;background:#f4f4f4;color:#222}main{max-width:1400px;margin:0 auto;padding:0 20px 80px}
.c{background:#fff;border:1px solid #bbb;margin:14px 0;padding:10px;border-left:8px solid #999}.c.cap{border-left-color:#2a7}.c.mis{border-left-color:#c33}.c.nop{border-left-color:#888}.c.out{border-left-color:#bbb;opacity:.8}
.c h3{margin:0 0 6px}.tag{display:inline-block;padding:2px 8px;border-radius:10px;background:#eef;margin-right:6px;font-size:12px}.res{font-weight:bold}
.row{display:flex;gap:10px;flex-wrap:wrap;margin:8px 0}.row img{height:200px;border:2px solid #36c}.row.ds img{border:2px solid #2a7}figure{margin:0}figcaption{font-size:12px;max-width:300px}
table{border-collapse:collapse;margin:6px 0}td{border:1px solid #ddd;padding:3px 8px;vertical-align:top}td:first-child{background:#f7f7f7;white-space:nowrap}
.bt button{font-size:14px;padding:6px 12px;margin-right:6px;border:1px solid #888;border-radius:4px;background:#eee;cursor:pointer}.bt button.on{background:#234;color:#fff}
.bt input{font-size:14px;padding:6px;width:420px}.c.v-ok{background:#f1fbf5}.c.v-fora{background:#fbf1f1}.c.v-errado{background:#fff6e5}.c.v-duvida{background:#fffbe0}
#bar{position:sticky;top:0;z-index:9;background:#123;color:#fff;padding:10px 20px;display:flex;gap:14px;align-items:center}#bar button{font-size:15px;padding:7px 14px}h2{background:#234;color:#fff;padding:8px;margin-top:36px}"""
JS = r"""
const KEY='gs_v2_census_review_v1';let A={};try{A=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
function save(){try{localStorage.setItem(KEY,JSON.stringify(A))}catch(e){}render()}
function render(){let n=0,t=0;document.querySelectorAll('.c[data-id]').forEach(c=>{t++;const v=(A[c.dataset.id]||{}).v||'';if(v)n++;
  c.classList.remove('v-ok','v-fora','v-errado','v-duvida');if(v)c.classList.add('v-'+v);
  c.querySelectorAll('button').forEach(b=>b.classList.toggle('on',b.dataset.v===v));const i=c.querySelector('input');if(document.activeElement!==i)i.value=(A[c.dataset.id]||{}).n||''});
  document.getElementById('prog').textContent=n+' de '+t+' revistas'}
document.addEventListener('click',e=>{const b=e.target.closest('.bt button');if(!b)return;const id=b.closest('.c').dataset.id;A[id]=A[id]||{};A[id].v=(A[id].v===b.dataset.v)?'':b.dataset.v;save()});
document.addEventListener('input',e=>{if(e.target.matches('.bt input')){const id=e.target.closest('.c').dataset.id;A[id]=A[id]||{};A[id].n=e.target.value;try{localStorage.setItem(KEY,JSON.stringify(A))}catch(x){}}});
function exportCSV(){const rows=[['aeronave','empresa','veredicto','nota']];document.querySelectorAll('.c[data-id]').forEach(c=>{const a=A[c.dataset.id]||{};rows.push([c.dataset.ac,c.dataset.co,a.v||'',a.n||''])});
  const csv=rows.map(r=>r.map(x=>'"'+String(x).replace(/"/g,'""')+'"').join(',')).join('\n');const d=new Date(),p=n=>String(n).padStart(2,'0');
  const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));a.download='gs_v2_census_review_'+d.getFullYear()+p(d.getMonth()+1)+p(d.getDate())+p(d.getHours())+p(d.getMinutes())+'.csv';a.click()}
render();"""
def card(r, k):
    sl = str(r.slugs).split("|"); s0 = next((s for s in sl if s in A.index), None)
    out = r.motivo_fora != ""
    cls = "out" if out else "cap" if r.resultado.startswith("capturado") else "mis" if r.resultado.startswith("em falta") else "nop"
    why = []
    if "índice" in r.criterio:
        m = IM[(IM.aeronave == r.aeronave)]
        why.append("AAM Reality Index, Maio 2026: " + (f"{m.oem.iloc[0]}, veículo «{m.veiculo_indice.iloc[0]}»" + (f" ({m.nota.iloc[0]})" if len(m) and m.nota.iloc[0] else "") if len(m) else "edição anterior do índice (histórico), veículo escolhido pelo Claude"))
    if r.frase_trl7: why.append("TRL ≥ 7, frase da página: «" + html.escape(r.frase_trl7[:330]) + "»")
    spec = "".join(f"<tr><td>{n}</td><td>{html.escape(str(A.loc[s0, c]))[:220]}</td></tr>" for n, c in [("Tipo", "spec_aircraft_type"), ("Energia", "spec_power_source"), ("Capacidade", "spec_capacity"), ("Pilotagem", "spec_piloting"), ("Estado VFS", "status")] if s0 and str(A.loc[s0, c]))
    ids = [i.strip() for i in str(r.ids_nos_626).split(";") if i.strip()]
    if r.aeronave in ANS.index and ANS.resposta[r.aeronave] not in ("", "nenhum"): ids = [ANS.resposta[r.aeronave]] + [i for i in ids if i != ANS.resposta[r.aeronave]]
    ds = ""
    for i in ids[:4]:
        if i in D6.index:
            p = small(D6.main_figure[i], DS / (i + ".jpg"))
            ds += f"<figure>{f'<img src=\"_census/{p.name}\">' if p else '<i>sem imagem</i>'}<figcaption>{i} · {D6.topType[i]} · {D6.company[i]}<br>{html.escape(D6.title[i][:90])}</figcaption></figure>"
    fam = " ".join(x for x in [r.familia_pool, r.familia_pool_resposta] if x)
    fl = " ".join(f"<a href='https://patents.google.com/patent/{f.strip(';')}/en' target='_blank'>{f.strip(';')}</a>" for f in fam.split()) if fam else ""
    note = ANS.fonte.get(r.aeronave, "") if r.aeronave in ANS.index else ""
    return (f"<div class='c {cls}' data-id='{k}' data-ac='{html.escape(r.aeronave)}' data-co='{html.escape(r.empresa)}'><h3>{k}. {html.escape(r.empresa)} · <a href='{r.url}' target='_blank'>{html.escape(r.aeronave)}</a></h3>"
            f"<span class='tag'>{r.categoria_vfs}</span><span class='tag'>{r.criterio}</span><span class='tag'>ano {str(r.ano_1o_voo)[:4]}</span> <span class='res'>{r.resultado}{(' · ' + r.motivo_fora) if out else ''}</span>"
            f"<div class='row'>{''.join(f'<img src=\"{p.relative_to(SH)}\">' for p in photos(r.slugs))}</div>"
            f"<table><tr><td>Porque entrou</td><td>{'<br>'.join(why)}</td></tr>{spec}"
            + (f"<tr><td>Família que a mostra</td><td>{fl}</td></tr>" if fl else "") + (f"<tr><td>Nota</td><td>{html.escape(note)}</td></tr>" if note else "") + "</table>"
            + (f"<b>Design do dataset a que foi ligada:</b><div class='row ds'>{ds}</div>" if ds else "")
            + "<div class='bt'><button data-v='ok'>Está certo</button><button data-v='fora'>Não devia estar no censo</button><button data-v='errado'>Resultado ou ligação errada</button><button data-v='duvida'>Dúvida</button> <input placeholder='nota (opcional)'></div></div>")
order = {"capturado": 0, "em falta": 1, "sem": 2, "por": 3}
C["o"] = C.resultado.map(lambda s: next((v for k_, v in order.items() if s.startswith(k_)), 9)); C.loc[C.motivo_fora != "", "o"] = 8
parts = [f"<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Censo v2: revisão</title><style>{CSS}</style>",
         "<div id='bar'><b id='prog'></b><button onclick='exportCSV()'>Exportar revisão (CSV)</button><span>Verde = no dataset · Vermelho = em falta com patente · Cinzento = sem patente encontrada</span></div><main>",
         "<h1>Gold standard v2: as aeronaves do censo, uma a uma</h1><p>Cada cartão mostra a aeronave, porque entrou no censo, os campos de domínio da página VFS, o resultado e, quando está no dataset, o desenho a que foi ligada. Carrega num botão por cartão e exporta no fim.</p>"]
k = 0
for title, sub in [("No dataset (nos 626)", C[C.o == 0]), ("Fora do dataset, com patente", C[C.o == 1]), ("Sem patente encontrada", C[C.o == 2]), ("Por decidir", C[C.o == 3]), ("Candidatas que ficaram fora do censo", C[C.o == 8])]:
    if sub.empty: continue
    parts.append(f"<h2>{title}: {len(sub)}</h2>")
    for r in sub.sort_values(["categoria_vfs", "empresa"]).itertuples():
        k += 1; parts.append(card(r, k))
parts.append(f"</main><script>{JS}</script>")
(SH / "census_review.html").write_text("\n".join(parts), encoding="utf-8")
print(k, "cartões ->", SH / "census_review.html")
