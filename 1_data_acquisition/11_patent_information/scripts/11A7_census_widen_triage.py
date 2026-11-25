"""Gold standard v2 census, widening to TRL 6: triage of the candidates.

Candidates: in-domain evtol.news aircraft, outside the census, whose page status is a full-scale prototype, technology demonstrator or
production aircraft and whose text reports a flight (gs_v2_census_widen_candidates.csv, 72 aircraft).
The census admits commercial actors only. This script proposes, per aircraft, whether the developer is clearly a company, from three
signals read on the evtol.news page, and builds a page where the author confirms or overrules each proposal.
  company signal : a legal form in the developer's name (Inc, Ltd, GmbH, Corp, LLC, Co., ...), or a company website on the page
                   together with company wording in the text (founded, startup, investors, funding, employees, orders, certification ...)
  no proposal    : neither signal is clear, or both appear: left to the author as "duvida"
  private signal : the text describes a personal project (hobby, garage, home-built, inventor, YouTube, DIY, amateur, kit ...)
  other flags    : roadable-vehicle wording, cargo or uncrewed wording, and "the company already has an aircraft in the census" (a version)
Output: gs_v2_census_widen_triage.csv, sheets_v2/census_widen.html ; export gs_v2_census_widen_<stamp>.csv
"""
import json
src = (__import__("pathlib").Path(__file__).resolve().parent / "02e_census_review_page.py").read_text(encoding="utf-8")
exec(src[src.index("import re, html"):src.index("CSS = ")])
W = pd.read_csv(OUT / "gs_v2_census_widen_candidates.csv").fillna("")
E = pd.read_csv(OUT / "eligible.csv").fillna("").set_index(["ck", "aeronave"])
TXT = {}
for line in open(SRC / "pages.jsonl", encoding="utf-8"):
    r = json.loads(line); TXT[r["slug_key"]] = r["text"]
LEGAL = re.compile(r"\b(inc|incorporated|ltd|limited|llc|gmbh|corp|corporation|co|company|s\.?a|s\.?r\.?l|pty|plc|ag|ab|as|bv|kk|pte|pvt|oy|sas|holdings|group)\b\.?", re.I)
COMP = re.compile(r"\b(founded|co-?founded|start-?up|headquarter|investor|invest(ed|ment)|funding|raised|series [a-d]\b|employees|pre-?orders?|orders? (for|from)|customers?|type certif|certification|airworthiness|production (line|facility)|factory|subsidiary|listed on|stock exchange|ipo)\b", re.I)
PRIV = re.compile(r"\b(hobby|hobbyist|garage|home-?built|home-?made|backyard|diy|do-it-yourself|amateur|youtuber|enthusiast|one-man|by himself|personal project)\b", re.I)
ROAD = re.compile(r"flying car|roadable|road[- ]legal|drive on|driving mode|wheels? .{0,30}road|land aircraft carrier", re.I)
CARGO = re.compile(r"cargo|uncrewed|unmanned|autonomous cargo", re.I)
CAR_CO = {"xpeng", "xpengaeroht", "aridge"}      # author, 2026-11-10: "XPeng AeroHT: isto é um carro, não entra no dataset"
OUT_AC = set()
def hits(rx, t, n=3): return "; ".join(dict.fromkeys(m.group(0).lower() for m in rx.finditer(t)))[:120] if t else ""
def snip(rx, t):
    m = rx.search(t)
    return ("…" + t[max(0, m.start() - 110):m.end() + 110].replace("\n", " ") + "…") if m else ""
LEGAL_CK = {r.ck for _, r in W.iterrows() if LEGAL.search(r.empresa)}      # the legal form counts for every page of the same developer
rows = []
for _, r in W.iterrows():
    slugs = str(E.loc[(r.ck, r.aeronave), "slugs"]) if (r.ck, r.aeronave) in E.index else ""
    sl = [s for s in slugs.split("|") if s]; t = " ".join(re.split(r"\n\s*Resources:?\s*\n", TXT.get(s, ""))[0] for s in sl)      # body text only, the Resources list is dropped
    web = next((A.loc[s, "website"] for s in sl if s in A.index and A.loc[s, "website"]), ""); loc = next((A.loc[s, "location"] for s in sl if s in A.index and A.loc[s, "location"]), "")
    typ = " | ".join(dict.fromkeys(A.loc[s, "spec_aircraft_type"] for s in sl if s in A.index and A.loc[s, "spec_aircraft_type"]))
    cap = next((A.loc[s, "spec_capacity"] for s in sl if s in A.index and A.loc[s, "spec_capacity"]), "")
    legal, comp, priv = bool(LEGAL.search(r.empresa)), hits(COMP, t), hits(PRIV, t)
    road = hits(ROAD, typ + " " + t[:1500]); cargo = bool(re.search(r"cargo only", cap, re.I)) or (bool(CARGO.search(typ + " " + cap)) and not re.search(r"passenger|pilot|person|people|seat", typ + " " + cap, re.I))
    is_co = legal or (bool(web) and len(comp.split("; ")) >= 2 and comp != "")
    legal_ck = legal or r.ck in LEGAL_CK; is_co = is_co or legal_ck
    prop = "carro" if (re.search(r"roadable|road[- ]legal|land aircraft carrier|flying car|\bair ?car\b", typ + " " + r.aeronave + " " + r.empresa, re.I) or r.ck in CAR_CO) else "fora" if (cargo or (r.ck, r.aeronave) in OUT_AC) else "empresa" if (is_co and not priv) else "particular" if (priv and not is_co) else "duvida"
    rows.append({**r.to_dict(), "slugs": slugs, "website": web, "local": loc, "tipo_vfs": typ[:160], "capacidade": cap[:80], "forma_legal_no_nome": legal, "sinais_empresa": comp,
                 "sinais_particular": priv, "sinais_estrada": road, "proposta": prop, "frase_particular": snip(PRIV, t)[:300], "frase_empresa": snip(COMP, t)[:300]})
T = pd.DataFrame(rows); T.to_csv(OUT / "gs_v2_census_widen_triage.csv", index=False)
print(T.proposta.value_counts().to_string()); print("versões de empresas já no censo:", int(T.empresa_ja_no_censo.sum()))
CSS = """body{font:14px sans-serif;margin:0;background:#f4f4f4;color:#222}main{max-width:1300px;margin:0 auto;padding:0 20px 80px}
.c{background:#fff;border:1px solid #bbb;margin:12px 0;padding:10px;border-left:8px solid #999}.c h3{margin:0 0 6px}.tag{display:inline-block;padding:2px 8px;border-radius:10px;background:#eef;margin-right:6px;font-size:12px}
.tag.w{background:#fde3c0}.tag.r{background:#f8caca}.row{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}.row img{height:190px;border:2px solid #36c}q{display:block;color:#555;font-size:13px;margin:3px 0}
.bt button{font-size:14px;padding:6px 12px;margin-right:6px;border:1px solid #888;border-radius:4px;background:#eee;cursor:pointer}.bt button.on{background:#234;color:#fff}
.c.v-empresa{border-left-color:#2a7;background:#f1fbf5}.c.v-particular{border-left-color:#c33;background:#fbf1f1}.c.v-carro,.c.v-fora{border-left-color:#888;background:#eee}.c.v-duvida{border-left-color:#d90;background:#fffbe0}
#bar{position:sticky;top:0;z-index:9;background:#123;color:#fff;padding:10px 20px;display:flex;gap:14px;align-items:center}#bar button{font-size:15px;padding:7px 14px}h2{background:#234;color:#fff;padding:8px;margin-top:34px}"""
JS = r"""
const KEY='gs_v2_census_widen_v1';let A={};try{A=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
function val(c){return A[c.dataset.k]||c.dataset.p}
function render(){const n={};document.querySelectorAll('.c').forEach(c=>{const v=val(c);c.className='c v-'+v;c.querySelectorAll('button').forEach(b=>b.classList.toggle('on',b.dataset.v===v));
  c.querySelector('.who').textContent=A[c.dataset.k]?' (decisão tua)':' (proposta, por confirmar)';n[v]=(n[v]||0)+1});
  document.getElementById('prog').textContent=Object.keys(A).length+' decididas por ti · '+Object.entries(n).map(e=>e[0]+' '+e[1]).join(' · ')}
document.addEventListener('click',e=>{const b=e.target.closest('.bt button');if(!b)return;const c=b.closest('.c');A[c.dataset.k]=b.dataset.v;try{localStorage.setItem(KEY,JSON.stringify(A))}catch(x){}render()});
function exportCSV(){const rows=[['ck','aeronave','empresa','decisao','quem']];document.querySelectorAll('.c').forEach(c=>rows.push([c.dataset.ck,c.dataset.ac,c.dataset.co,val(c),A[c.dataset.k]?'autor':'proposta']));
  const csv=rows.map(r=>r.map(x=>'"'+String(x).replace(/"/g,'""')+'"').join(',')).join('\n');const d=new Date(),p=n=>String(n).padStart(2,'0');
  const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));a.download='gs_v2_census_widen_'+d.getFullYear()+p(d.getMonth()+1)+p(d.getDate())+p(d.getHours())+p(d.getMinutes())+'.csv';a.click()}
render();"""
ORD = {"particular": 0, "duvida": 1, "carro": 2, "fora": 3, "empresa": 4}
NAME = {"particular": "Proposta: particular, sai", "duvida": "Proposta: dúvida. Sem forma legal no nome e poucos sinais de empresa, ou sinais dos dois lados. Decide tu", "carro": "Proposta: carro voador, sai", "fora": "Proposta: carga ou não tripulado, sai", "empresa": "Proposta: empresa, entra"}
parts = [f"<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Censo: triagem do alargamento</title><style>{CSS}</style>",
         "<div id='bar'><b id='prog'></b><button onclick='exportCSV()'>Exportar (CSV)</button><span>O botão escuro é a decisão em vigor. Só precisas de carregar onde discordas.</span></div><main>",
         "<h1>Alargar o censo a TRL 6: é claramente uma empresa?</h1><p>72 aeronaves com protótipo à escala real que voou. Entram as que são de uma <b>empresa</b>. Saem os projectos de <b>particulares</b>, os <b>carros voadores</b> e as de carga. "
         "A proposta vem de sinais lidos na página do VFS e está marcada em cada cartão. As secções com mais risco estão primeiro.</p>"]
for p, g in sorted(T.groupby("proposta"), key=lambda x: ORD[x[0]]):
    parts.append(f"<h2>{NAME[p]} ({len(g)})</h2>")
    for _, r in g.sort_values(["categoria_vfs", "empresa"]).iterrows():
        ph = "".join(f"<img src='{x.relative_to(SH)}' loading='lazy'>" for x in photos(r.slugs, 3))
        tags = f"<span class='tag'>{r.categoria_vfs}</span><span class='tag'>{str(r.ano_1o_voo)[:4]}</span><span class='tag'>{html.escape(r.estado_vfs)}</span>"
        if r.empresa_ja_no_censo: tags += "<span class='tag w'>empresa já no censo: é uma versão</span>"
        if r.ja_ligado_aos_626: tags += "<span class='tag'>já ligado aos 626</span>"
        if r.sinais_estrada: tags += f"<span class='tag r'>estrada: {html.escape(r.sinais_estrada)}</span>"
        k = f"{r.ck}|{r.aeronave}"
        parts.append(f"<div class='c' data-k='{html.escape(k)}' data-p='{p}' data-ck='{html.escape(r.ck)}' data-ac='{html.escape(r.aeronave)}' data-co='{html.escape(r.empresa)}'><h3>{html.escape(r.empresa)} · {html.escape(r.aeronave)} <a href='{r.url}' target='_blank' style='font-size:12px'>página VFS</a></h3>{tags}"
                     f"<div class='row'>{ph}</div><div>{html.escape(r.local)} · {html.escape(r.website) or '<i>sem site</i>'} · {html.escape(r.tipo_vfs)} · {html.escape(r.capacidade)}</div>"
                     f"<div><b>Sinais de empresa:</b> {'forma legal no nome; ' if r.forma_legal_no_nome else ''}{html.escape(r.sinais_empresa) or '-'}<q>{html.escape(r.frase_empresa)}</q></div>"
                     f"<div><b>Sinais de particular:</b> {html.escape(r.sinais_particular) or '-'}<q>{html.escape(r.frase_particular)}</q></div>"
                     "<div class='bt'><button data-v='empresa'>Empresa, entra</button><button data-v='particular'>Particular, sai</button><button data-v='carro'>Carro voador, sai</button><button data-v='fora'>Carga / fora, sai</button><button data-v='duvida'>Dúvida</button><span class='who'></span></div></div>")
parts.append(f"</main><script>{JS}</script>")
(SH / "census_widen.html").write_text("\n".join(parts), encoding="utf-8"); print(SH / "census_widen.html")
