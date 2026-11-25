"""Gold standard v2: candidate families for the sampled designs whose company is already in the 572-family pool.

A family inside the thesis dataset (1 639) that showed the design would already have put it in the 626, so only the pool families
OUTSIDE the dataset can hide it. For each such company: its out-of-dataset families not yet coded in the 51, with priority year inside
[first-flight year - 6, first-flight year + 2] (the same window as the PatSeer queries), with their first drawings from Google Patents.
Output: 06_gold_standard/v2/sheets_v2/index.html (+ figures) and gs_v2_pool_candidates.csv.
"""
import os
import re, time, html
from pathlib import Path
import pandas as pd, requests

DATA_DIR = Path(__file__).resolve().parent.parent
OUT = DATA_DIR / "06_gold_standard/v2"; SH = OUT / "sheets_v2"; SH.mkdir(exist_ok=True)
H = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
CDN = re.compile(r'https://patentimages\.storage\.googleapis\.com/[^\s"\'<>]+\.png')
PDFU = re.compile(r'https://patentimages\.storage\.googleapis\.com/[^\s"\'<>]+\.pdf')
US = re.compile(r"^(US)(\d{4})(\d{6})(A\d)$")
PUB = re.compile(r"\b[A-Z]{2}\d{6,}[A-Z]\d?\b")
ASN = {"joby": "Joby", "eve": "Embraer / Eve", "aerofugia": "Aerofugia / Geely", "ehang": "EHang", "autoflight": "AutoFlight",
       "skydrive": "SkyDrive", "verticalaerospace": "Vertical Aerospace", "xpeng": "Huitian", "airbus": "Airbus"}

def gp(pub):
    m = US.match(pub); return f"https://patents.google.com/patent/{m[1]}{m[2]}0{m[3]}{m[4] if m else ''}/en" if m else f"https://patents.google.com/patent/{pub}/en"
def get(url, tries=1):
    for i in range(tries):
        try:
            r = requests.get(url, headers=H, timeout=20)
            if r.status_code == 200: return r
            if r.status_code == 404: return None
        except Exception: pass
        if i + 1 < tries: time.sleep(4 * 3 ** i)
    return None
def figs(row, n=4):
    d = SH / row["Record Number"]; d.mkdir(exist_ok=True)
    have = sorted(d.glob("fig_*.png"))
    if have or (d / "none").exists(): return have
    pubs = [row["Record Number"]] + [p for p in PUB.findall(str(row["Simple Family Members"])) if p != row["Record Number"]]
    pubs = sorted(dict.fromkeys(pubs), key=lambda p: (p != row["Record Number"], p[:2] not in ("US", "EP", "WO")))
    for pub in pubs[:2]:
        r = get(gp(pub)); time.sleep(0.6)
        if r is None: continue
        seen = {}
        for u in CDN.findall(r.text): seen[u.rsplit("/", 1)[-1]] = u
        out = []
        for i, (_, u) in enumerate(sorted(seen.items())[:n], 1):
            im = get(u, 2)
            if im is not None: p = d / f"fig_{i:02d}.png"; p.write_bytes(im.content); out.append(p)
            time.sleep(0.3)
        if out: return out
    # no PNG drawings (typical of CN): render pages of the PDF. Text-layer PDFs: pages with little text; scanned PDFs: the last pages.
    import subprocess, tempfile
    for pub in pubs[:2]:
        r = get(gp(pub)); m = PDFU.search(r.text) if r is not None else None
        if not m: continue
        pr = get(m.group(0), 2)
        if pr is None: continue
        tmp = Path(tempfile.mkdtemp()); pdf = tmp / "p.pdf"; pdf.write_bytes(pr.content)
        try: npg = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout).group(1))
        except Exception: continue
        chars = [len(subprocess.run(["pdftotext", "-f", str(q), "-l", str(q), str(pdf), "-"], capture_output=True, text=True).stdout.strip()) for q in range(1, npg + 1)]
        pages = [q for q in range(2, npg + 1) if chars[q - 1] < 250] if sum(chars) > 250 * max(1, npg // 2) else list(range(max(2, npg - n + 1), npg + 1))
        out = []
        for i, q in enumerate(pages[:n], 1):
            dest = d / f"fig_{i:02d}"
            subprocess.run(["pdftoppm", "-f", str(q), "-l", str(q), "-r", "50", "-png", "-singlefile", str(pdf), str(dest)], capture_output=True)
            if dest.with_suffix(".png").exists(): out.append(dest.with_suffix(".png"))
        if out: return out
    (d / "none").write_text(""); return []

S = pd.read_csv(OUT / "gs_v2_sample.csv"); E = pd.read_csv(OUT / "eligible.csv")[["empresa", "aeronave", "ck", "url", "slugs"]].rename(columns={"url": "vfs_url"})
# photos of the sought aircraft: the VFS images already downloaded (EVTOLNEWS_DS/0_source/images), copied small next to the page
from PIL import Image
IMG = pd.read_csv(Path(os.environ.get("EVTOLNEWS_SOURCE", "data/evtolnews/0_source")) / "images.csv", dtype=str).fillna("")
IMG = IMG[IMG.dl_error == ""]
PH = SH / "_vfs"; PH.mkdir(exist_ok=True)
def photos(slugs, n=3):
    out = []
    for s in str(slugs).split("|"):
        for _, r in IMG[IMG.slug_key == s].sort_values("img_pos", key=lambda x: x.astype(int)).iterrows():
            dst = PH / (r.image_uid + ".jpg")
            if not dst.exists():
                try:
                    im = Image.open(r.local_path).convert("RGB"); im.thumbnail((640, 640)); im.save(dst, quality=80)
                except Exception: continue
            out.append(dst)
            if len(out) >= n: return out
    return out
S = S[S.o_que_falta == "ver famílias da empresa no pool"].merge(E, on=["empresa", "aeronave"], how="left")
DES = []   # per sought design: how many candidate families its company block has
rv = pd.read_excel(OUT / "goldstandard_pool_review.xlsx")
rv = rv[(~rv.in_thesis_dataset) & rv.priority_group.isna()]
CSS = """body{font:14px sans-serif;margin:0;background:#fafafa;color:#222}main{max-width:1500px;margin:0 auto;padding:0 20px 80px}
h2{background:#234;color:#fff;padding:8px;margin-top:40px}.f{border:1px solid #ccc;margin:8px 0;padding:8px;background:#fff}
.f img{height:220px;margin-right:6px;border:1px solid #eee}.ref{display:flex;gap:16px;flex-wrap:wrap;margin:8px 0}.ref figure{margin:0}
.ref img{height:240px;border:3px solid #36c}.ref figcaption{font-weight:bold}.mini{float:right;text-align:right}.mini img{height:100px;border:2px solid #36c;margin-left:4px}
.t{background:#ffe;padding:6px;border:1px solid #cc9}.bt{margin:6px 0}.bt button{font-size:14px;padding:6px 12px;margin-right:6px;border:1px solid #888;border-radius:4px;background:#eee;cursor:pointer}
.bt button.on{background:#2a7;color:#fff;border-color:#2a7}.bt button.dv.on{background:#d90;border-color:#d90}.bt button.no.on{background:#999;border-color:#999;color:#fff}
.f.match{border:3px solid #2a7}.f.doubt{border:3px solid #d90}.f.none{opacity:.55}
.ans{background:#eef;border:1px solid #99c;padding:8px;margin:8px 0}.ans button{font-size:14px;padding:6px 12px;margin-left:8px}.ans .ok{color:#2a7;font-weight:bold}.ans .pend{color:#c33;font-weight:bold}
#bar{position:sticky;top:0;z-index:9;background:#123;color:#fff;padding:10px 20px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}#bar button{font-size:15px;padding:7px 14px}
#bar .s{font-weight:bold}"""
JS = r"""
const KEY='gs_v2_pool_answers_v1';let A={};try{A=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
function save(){try{localStorage.setItem(KEY,JSON.stringify(A))}catch(e){}render()}
function famFor(ac){return A['f:'+ac]||[]}
function setFam(fam,ac,val){ // val: match | doubt | no
  const k='m:'+fam+'|'+ac; if(A[k]===val){delete A[k]}else{A[k]=val}; if(val!=='no'){delete A['n:'+ac]} save()}
function setNone(ac){if(A['n:'+ac]){delete A['n:'+ac]}else{A['n:'+ac]=1;for(const k of Object.keys(A)){if(k.startsWith('m:')&&k.endsWith('|'+ac)&&A[k]!=='no')delete A[k]}}save()}
function answer(ac){const m=[],d=[];for(const k of Object.keys(A)){if(!k.startsWith('m:'))continue;const [f,a]=k.slice(2).split('|');if(a!==ac)continue;if(A[k]==='match')m.push(f);if(A[k]==='doubt')d.push(f)}
  if(m.length)return{s:'família',f:m,d};if(d.length)return{s:'dúvida',f:d,d:[]};if(A['n:'+ac])return{s:'nenhuma',f:[],d:[]};return{s:'',f:[],d:[]}}
function render(){
  document.querySelectorAll('.bt button[data-fam]').forEach(b=>{b.classList.toggle('on',A['m:'+b.dataset.fam+'|'+b.dataset.ac]===b.dataset.v)});
  document.querySelectorAll('.f').forEach(div=>{const fam=div.dataset.fam;let mt=false,dv=false,no=true;
    div.querySelectorAll('button[data-v=match]').forEach(b=>{const v=A['m:'+fam+'|'+b.dataset.ac];if(v==='match')mt=true;if(v==='doubt')dv=true;if(v!=='no')no=false});
    div.classList.toggle('match',mt);div.classList.toggle('doubt',!mt&&dv);div.classList.toggle('none',no)});
  let done=0,tot=0;document.querySelectorAll('.ans').forEach(el=>{const ac=el.dataset.ac;tot++;const r=answer(ac);
    const st=el.querySelector('.st');if(r.s){done++;st.className='st ok';st.textContent=r.s==='nenhuma'?'nenhuma família mostra o '+ac:(r.s==='dúvida'?'dúvida: '+r.f.join(', '):'mostrado por '+r.f.join(', '))}else{st.className='st pend';st.textContent='por responder'}
    el.querySelector('.nb').classList.toggle('on',!!A['n:'+ac])});
  document.getElementById('prog').textContent=done+' de '+tot+' aeronaves respondidas'}
function exportCSV(){const rows=[['aeronave','empresa','resposta','familias','duvidas']];
  document.querySelectorAll('.ans').forEach(el=>{const r=answer(el.dataset.ac);rows.push([el.dataset.ac,el.dataset.co,r.s,r.f.join(' '),r.d.join(' ')])});
  const csv=rows.map(r=>r.map(x=>'"'+String(x).replace(/"/g,'""')+'"').join(',')).join('\n');
  const d=new Date(),p=n=>String(n).padStart(2,'0'),st=d.getFullYear()+p(d.getMonth()+1)+p(d.getDate())+p(d.getHours())+p(d.getMinutes());
  const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));a.download='gs_v2_pool_answers_'+st+'.csv';a.click()}
function copyTxt(){const L=[];document.querySelectorAll('.ans').forEach(el=>{const r=answer(el.dataset.ac);L.push(el.dataset.ac+': '+(r.s==='família'?r.f.join(' '):(r.s||'?'))+(r.d.length?' (dúvida: '+r.d.join(' ')+')':''))});
  const txt=L.join('\n');navigator.clipboard?navigator.clipboard.writeText(txt).then(()=>alert('Copiado:\n\n'+txt),()=>prompt('Copia:',txt)):prompt('Copia:',txt)}
document.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
  if(b.dataset.fam)setFam(b.dataset.fam,b.dataset.ac,b.dataset.v);else if(b.classList.contains('nb'))setNone(b.dataset.ac)});
render();
"""
rows, parts = [], [f"<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>v2: candidatas no pool</title><style>{CSS}</style>",
    "<div id='bar'><span class='s' id='prog'></span><button onclick='exportCSV()'>Exportar respostas (CSV)</button><button onclick='copyTxt()'>Copiar como texto</button>"
    "<span>Verde = mostra a aeronave · Laranja = dúvida · Cinzento = não é. As respostas ficam guardadas neste browser.</span></div><main>",
    "<h1>Gold standard v2: famílias candidatas no pool</h1><p>Em cada família carrega no botão da aeronave que ela mostra, em <b>Dúvida</b>, ou em <b>Não é</b>. "
    "Se nenhuma família de uma empresa mostra a aeronave, carrega em <b>Nenhuma família mostra</b> na caixa azul. No fim, <b>Exportar respostas</b>: o ficheiro vai para Transferências e eu leio-o de lá.</p>"]
for ck, g in S.groupby("ck", sort=False):
    lo, hi = int(g.ano_1o_voo.min()) - 6, int(g.ano_1o_voo.max()) + 2
    fam = rv[(rv.asn_company == ASN[ck]) & rv["Priority Year"].between(lo, hi)].sort_values("Priority Year")
    for a_ in g.aeronave: DES.append({"aeronave": a_, "empresa": g.empresa.iloc[0], "n_familias_candidatas": len(fam), "janela": f"{lo}-{hi}"})
    if fam.empty:
        parts.append(f"<h2>{html.escape(g.empresa.iloc[0])}: sem famílias candidatas</h2><p>{', '.join(html.escape(a) for a in g.aeronave)}: nada a fazer, fica como \"sem patente no pool\".</p>")
        continue
    parts.append(f"<h2>{html.escape(g.empresa.iloc[0])}: {len(fam)} famílias (prioridade {lo}–{hi})</h2><div class='t'><b>Procura:</b> " +
                 " &nbsp;|&nbsp; ".join(f"<a href='{u}' target='_blank'>{html.escape(a)}</a> ({c}, {int(y)})" for a, c, y, u in zip(g.aeronave, g.categoria_vfs, g.ano_1o_voo, g.vfs_url)) + "</div>")
    ref = [(a, photos(sl)) for a, sl in zip(g.aeronave, g.slugs)]
    parts.append("<div class='ref'>" + "".join(f"<figure><figcaption>{html.escape(a)} (VFS)</figcaption>" + "".join(f"<img src='{p.relative_to(SH)}'>" for p in ph) + "</figure>" for a, ph in ref) + "</div>")
    for a in g.aeronave:
        parts.append(f"<div class='ans' data-ac='{html.escape(a)}' data-co='{html.escape(g.empresa.iloc[0])}'><b>{html.escape(a)}:</b> <span class='st'></span><button class='nb' data-ac='{html.escape(a)}'>Nenhuma família mostra o {html.escape(a)}</button></div>")
    mini = "<div class='mini'>" + "".join(f"<img src='{ph[0].relative_to(SH)}' title='{html.escape(a)}'>" for a, ph in ref if ph) + "<br><small>" + " · ".join(html.escape(a) for a, _ in ref) + "</small></div>"
    for _, r in fam.iterrows():
        ff = figs(r); rn = r["Record Number"]
        imgs = "".join(f"<img src='{p.relative_to(SH)}'>" for p in ff) or "<i>sem desenhos no Google Patents (abre o link)</i>"
        bts = "".join(f"<button data-fam='{rn}' data-ac='{html.escape(a)}' data-v='match'>É o {html.escape(a)}</button>" for a in g.aeronave)
        bts += "".join(f"<button class='dv' data-fam='{rn}' data-ac='{html.escape(a)}' data-v='doubt'>Dúvida{(' ' + html.escape(a)) if len(g) > 1 else ''}</button>" for a in g.aeronave)
        bts += "".join(f"<button class='no' data-fam='{rn}' data-ac='{html.escape(a)}' data-v='no'>Não é{(' o ' + html.escape(a)) if len(g) > 1 else ''}</button>" for a in g.aeronave)
        parts.append(f"<div class='f' data-fam='{rn}'>{mini}<b><a href='{gp(rn)}' target='_blank'>{rn}</a></b> · {int(r['Priority Year'])} · {html.escape(str(r['Title']))} · <small>keywords: {r['kw_verdict']}</small><div class='bt'>{bts}</div>{imgs}<div style='clear:both'></div></div>")
        rows.append({"empresa": g.empresa.iloc[0], "designs_procurados": "; ".join(g.aeronave), "Record Number": rn, "Priority Year": r["Priority Year"],
                     "Title": r["Title"], "kw_verdict": r["kw_verdict"], "n_desenhos": len(ff), "mostra_o_design": ""})
    print(ck, len(fam), flush=True)
parts.append(f"</main><script>{JS}</script>")
(SH / "index.html").write_text("\n".join(parts), encoding="utf-8")
pd.DataFrame(rows).to_csv(OUT / "gs_v2_pool_candidates.csv", index=False)
pd.DataFrame(DES).to_csv(OUT / "gs_v2_pool_designs.csv", index=False)
print(len(rows), "famílias")
