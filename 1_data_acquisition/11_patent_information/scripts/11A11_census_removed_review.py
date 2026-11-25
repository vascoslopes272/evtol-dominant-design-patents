"""Gold standard v2 census: review page for the steps the author has not checked.
Part 1: the vehicle chosen by Claude for each former AAM Reality Index company (11 aircraft).
Part 2: the candidates removed on routes A (index), B (index history) and C (evtol.news TRL 7).
Output: sheets_v2/census_removed_review.html. Answers: gs_v2_census_removed_review_<stamp>.csv (Downloads)."""
import re, html
from pathlib import Path
import pandas as pd
HERE = Path(__file__).resolve().parent
src = (HERE / "02b_pool_candidates.py").read_text(encoding="utf-8")
exec(src[:src.index("S = pd.read_csv(OUT")])
exec(src[src.index("from PIL import Image"):src.index("rows, parts = [], [")].replace('S = S[S.o_que_falta', '#').split("rv = pd.read_excel")[0])
A = pd.read_csv(DATA_DIR / "05_secondary/vfs/aircraft.csv", keep_default_na=False)
DOM = pd.read_csv(DATA_DIR / "05_secondary/vfs/DOMAIN.csv").set_index("slug_key").in_domain
C = pd.read_csv(OUT / "gs_v2_census.csv")
E = html.escape
def card(key, title, sub, slugs, opts, extra=""):
    ph = photos(slugs, 3) if slugs else []
    imgs = "".join(f"<img src='{p.relative_to(SH)}'>" for p in ph) or "<i>sem página ou sem fotografia no evtol.news</i>"
    spec = ""
    for s in str(slugs).split("|"):
        r = A[A.slug_key == s]
        if len(r):
            r = r.iloc[0]
            spec += (f"<div class='sp'><a href='{r.url}' target='_blank'>{E(r.title)}</a> · estado: {E(r.status)} · energia: {E(r.spec_power_source) or '?'} · "
                     f"capacidade: {E(r.spec_capacity) or '?'} · pilotagem: {E(r.spec_piloting) or '?'} · domínio (regra): <b>{'dentro' if DOM.get(s, False) else 'fora'}</b></div>")
    bt = "".join(f"<label><input type='radio' name='{E(key)}' value='{E(v)}'> {E(t)}</label>" for v, t in opts)
    return (f"<div class='c' data-k='{E(key)}'><h3>{E(title)}</h3><p>{sub}</p>{spec}{extra}<div class='im'>{imgs}</div>"
            f"<div class='bt'>{bt} <input type='text' placeholder='nota (opcional)' class='nt'></div></div>")
def others(pattern, chosen):
    r = A[A.slug_key.str.contains(pattern) & ~A.slug_key.isin(str(chosen).split("|"))]
    if r.empty: return ""
    return "<div class='ot'>Outras páginas desta empresa: " + " · ".join(
        f"<a href='{x.url}' target='_blank'>{E(x.title)}</a> ({'dentro' if DOM.get(x.slug_key, False) else 'fora'})" for x in r.itertuples()) + "</div>"

parts = []
parts.append("<h2>Parte 1. Veículo escolhido para cada empresa que saiu do índice (11)</h2><p>O histórico do AAM Reality Index só dá o nome da empresa. "
             "O veículo foi escolhido pelo Claude. Confirma, ou diz que devia ser outro, ou que a empresa devia sair.</p>")
PAT = {"Lilium": "lilium", "Pipistrel": "pipistrel", "Volkswagen": "volkswagen", "Wanfeng": "wanfeng", "Jaunt": "jaunt", "Airbus Acubed": "acubed|a3-by|vahana",
       "Bell": "^bell", "Kitty": "kitty-hawk", "Overair": "overair|karem", "Airbus Helicopters": "airbus-helicopters|cityairbus"}
O1 = [("ok", "Veículo certo"), ("outro", "Devia ser outro veículo (escreve na nota)"), ("sai", "Devia sair do censo")]
for _, r in C[C.criterio.str.contains("hist")].iterrows():
    pat = next((v for k, v in PAT.items() if r.empresa.startswith(k)), None)
    parts.append(card("B|" + r.aeronave, f"{r.empresa} · {r.aeronave}", f"Categoria: {E(r.categoria_vfs)} · resultado actual: {E(r.resultado)}", r.slugs, O1, others(pat, r.slugs) if pat else ""))

parts.append("<h2>Parte 2. Candidatas retiradas (vias A, B e C)</h2><p>Foram retiradas por regra ou pela leitura do Claude. Confirma que saem, ou diz que deviam entrar.</p>")
O2 = [("sai", "Concordo, fica de fora"), ("entra", "Devia entrar no censo"), ("duvida", "Dúvida")]
REM = [("A. Índice", "Electra · EL-9", "não é VTOL (eSTOL)", ""), ("A. Índice", "REGENT · Viceroy", "não é VTOL (seaglider)", ""),
       ("A. Índice", "Heart Aerospace · ES-30", "não é VTOL (avião regional)", ""), ("A. Índice", "Vaeridion · Microliner", "não é VTOL (avião convencional)", ""),
       ("A. Índice", "Volocopter · VoloUrban", "sem página no evtol.news. A Volocopter já está no censo com o VoloCity e o VoloRegion", ""),
       ("A. Índice", "Beta · CX300", "sem página no evtol.news (versão de descolagem convencional do ALIA). A Beta já está no censo com o ALIA-250", ""),
       ("A. Índice", "Robinson · dois veículos sem nome", "sem página no evtol.news", ""),
       ("A. Índice", "Honda · F1", "híbrido, fora do domínio no evtol.news", "honda-aircraft-company-f1"),
       ("B. Histórico", "Sabrewing · Rhaegal", "carga, não tripulado, turbo-eléctrico", "sabrewing-rhaegal-uas"),
       ("B. Histórico", "Elroy Air · Chaparral", "carga, não tripulado, híbrido", "elroy-air-chaparral-c1|elroy-air-chapparral"),
       ("B. Histórico", "Dufour Aerospace · Aero2 / Aero3", "híbrido, fora do domínio no evtol.news. Atenção: há uma página de um demonstrador de tecnologia", "dufour-aerospace-aero3-production-aircraft|dufour-aero2|dufour-aerospace-vtol-technology-demonstrator|dufour-aerospace-aero-3"),
       ("B. Histórico", "Airflow", "eSTOL, não é VTOL", ""), ("B. Histórico", "Eviation · Alice", "avião convencional, não é VTOL", ""),
       ("B. Histórico", "eAviation (Textron)", "sem página no evtol.news", ""),
       ("B. Histórico", "Alaka'i Technologies · Skai", "hidrogénio, fora do domínio no evtol.news", "alakai-technologies-skai|alakai-technologies-skai-prototype"),
       ("B. Histórico", "Bell · Nexus 6HX", "híbrido. A Bell está no censo com o Nexus 4EX", ""),
       ("C. TRL 7", "Liaoning General Aviation Academy · HX1E Electric Helicopter", "actor académico", "liaoning-general-aviation-academy-hx1e-electric-helicopter"),
       ("C. TRL 7", "amazingDIYprojects · chAIR Multicopter", "construtor particular", "chair-multicopter"),
       ("C. TRL 7", "Trek Aerospace · SoloTrek Springtail EFV", "fora do domínio no evtol.news", "trek-aerospace-springtail"),
       ("C. TRL 7", "Weslax · Proof of Concept", "fora do domínio no evtol.news", "weslax-proof-of-concept")]
for via, name, why, slugs in REM:
    parts.append(card("R|" + name, f"{via} · {name}", f"Motivo da retirada: <b>{E(why)}</b>", slugs, O2))

CSS = """body{font:15px/1.45 system-ui,sans-serif;margin:0;background:#f4f5f7;color:#1a1a1a}main{max-width:1150px;margin:70px auto 60px;padding:0 16px}
#bar{position:fixed;top:0;left:0;right:0;background:#1f2937;color:#fff;padding:10px 16px;display:flex;gap:14px;align-items:center;z-index:9}
#bar button{padding:6px 12px;border:0;border-radius:5px;background:#10b981;color:#fff;font-weight:600;cursor:pointer}
.c{background:#fff;border:1px solid #d5d8de;border-left:6px solid #9ca3af;border-radius:8px;padding:12px 16px;margin:14px 0}.c.done{border-left-color:#10b981}.c.flag{border-left-color:#f59e0b}
.c h3{margin:0 0 4px}.c p{margin:4px 0}.sp,.ot{font-size:13px;color:#333;margin:3px 0}.im img{height:190px;margin:6px 6px 0 0;border-radius:4px}
.bt{margin-top:10px;display:flex;flex-wrap:wrap;gap:16px;align-items:center}.bt label{cursor:pointer}.nt{flex:1;min-width:220px;padding:5px 8px;border:1px solid #bbb;border-radius:4px}"""
JS = r"""const K='gs_v2_census_removed_review_v1';let S={};try{S=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
function save(){try{localStorage.setItem(K,JSON.stringify(S))}catch(e){}paint()}
function paint(){let n=0,t=0;document.querySelectorAll('.c').forEach(c=>{t++;const k=c.dataset.k,s=S[k]||{};c.classList.toggle('done',!!s.v&&(s.v==='ok'||s.v==='sai'));c.classList.toggle('flag',!!s.v&&!(s.v==='ok'||s.v==='sai'));if(s.v)n++;
 c.querySelectorAll('input[type=radio]').forEach(r=>r.checked=(r.value===s.v));const nt=c.querySelector('.nt');if(document.activeElement!==nt)nt.value=s.n||''});document.getElementById('prog').textContent=n+' de '+t+' respondidas'}
document.querySelectorAll('.c').forEach(c=>{const k=c.dataset.k;c.querySelectorAll('input[type=radio]').forEach(r=>r.addEventListener('change',()=>{S[k]=S[k]||{};S[k].v=r.value;save()}));
 c.querySelector('.nt').addEventListener('input',e=>{S[k]=S[k]||{};S[k].n=e.target.value;save()})});
function exportCSV(){const q=s=>'"'+String(s||'').replace(/"/g,'""')+'"';let rows=['item,resposta,nota'];document.querySelectorAll('.c').forEach(c=>{const s=S[c.dataset.k]||{};rows.push([q(c.dataset.k),q(s.v),q(s.n)].join(','))});
 const d=new Date(),p=x=>String(x).padStart(2,'0');const st=d.getFullYear()+p(d.getMonth()+1)+p(d.getDate())+p(d.getHours())+p(d.getMinutes());
 const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([rows.join('\n')],{type:'text/csv'}));a.download='gs_v2_census_removed_review_'+st+'.csv';a.click()}
paint();"""
page = (f"<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Censo: revisão do que saiu</title><style>{CSS}</style>"
        "<div id='bar'><b>Censo: o que ainda não foi revisto</b><span id='prog'></span><button onclick='exportCSV()'>Exportar respostas (CSV)</button></div><main>"
        "<h1>Revisão: veículos escolhidos e candidatas retiradas</h1><p>31 cartões. Em cada um escolhe uma opção. A nota é opcional. No fim, <b>Exportar respostas</b>.</p>"
        + "\n".join(parts) + f"</main><script>{JS}</script>")
(SH / "census_removed_review.html").write_text(page, encoding="utf-8")
print("cartões:", page.count("class='c'"), SH / "census_removed_review.html")
