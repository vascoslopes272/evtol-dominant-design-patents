"""Gold standard v2 census: page for the enhanced search (alternative applicant and inventor names, no dates).
Same page as 02d, built from 01_query/patseer_gs_v2_enhanced_*.xlsx. Families already read in 02d are skipped.
Output: sheets_v2/census_enhanced.html. Answers: gs_v2_census_enhanced_answers_<stamp>.csv.


Reads the PatSeer export of 01_query/query_goldstandard_v2_census.txt (saved as 01_query/patseer_gs_v2_*.xlsx), matches each family
to a census company by assignee, and builds the same interactive page as 02b (VFS photos of the sought aircraft, first drawings of
each family, buttons, CSV export). Output: 06_gold_standard/v2/sheets_v2/census_query.html, gs_v2_census_query_designs.csv.
The author's answers (gs_v2_census_query_answers_<stamp>.csv, from Downloads) are read by notebook 02.
"""
import os
import re, sys, os, html, glob
from pathlib import Path
import pandas as pd
HERE = Path(__file__).resolve().parent
src = (HERE / "02b_pool_candidates.py").read_text(encoding="utf-8")
exec(src[:src.index("S = pd.read_csv(OUT")])                       # helpers: gp, get, figs, OUT, SH ...
exec(re.search(r'CSS = """.*?"""', src, re.S).group(0)); exec(re.search(r'JS = r""".*?"""', src, re.S).group(0))
exec(src[src.index("from PIL import Image"):src.index("rows, parts = [], [")].replace('S = S[S.o_que_falta', '#').split("rv = pd.read_excel")[0])
JS = JS.replace("gs_v2_pool_answers_v1", "gs_v2_census_enhanced_answers_v1").replace("gs_v2_pool_answers_", "gs_v2_census_enhanced_answers_")

exports = sorted(glob.glob(os.environ.get("GS_EXPORT", str(DATA_DIR / "01_query/patseer_gs_v2_enhanced_*.xlsx"))), key=os.path.getmtime)
if not exports: sys.exit("no export yet: run 01_query/query_goldstandard_v2_census.txt in PatSeer and save it as 01_query/patseer_gs_v2_<n>_<date>.xlsx")
X = pd.read_excel(exports[-1]); _seen = set(pd.read_excel(sorted(glob.glob(str(DATA_DIR / "01_query/patseer_gs_v2_[0-9]*.xlsx")))[-1])["Simple Family ID"]); X = X[~X["Simple Family ID"].isin(_seen)]; print("export:", Path(exports[-1]).name, len(X), "families")
asg = (X.get("Current Assignee", "").fillna("").astype(str) + " | " + X.get("Assignee", "").fillna("").astype(str)).str.lower()
RX = {"pivotal": "pivotal|opener|skykar|leng mark", "tier1engineering": "tier ?1", "leoflight": "leo flight|bitar pete", "star8green": "star ?8|koncepto", "ercsystem": "erc system",
      "zerog": "zero ?g", "pipistrelaviation": "pipistrel", "wanfengautoholdinggroup": "wanfeng", "skyflytechnologies": "skyfly"}
C = pd.read_csv(OUT / "gs_v2_census.csv"); C = C[C.resultado.str.contains("sem patente", na=False)]
rows, parts, des = [], [f"<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Censo: pesquisa alargada</title><style>{CSS}</style>",
    "<div id='bar'><span class='s' id='prog'></span><button onclick='exportCSV()'>Exportar respostas (CSV)</button><button onclick='copyTxt()'>Copiar como texto</button>"
    "<span>Verde = mostra a aeronave · Laranja = dúvida · Cinzento = não é.</span></div><main>",
    "<h1>Censo dos programas maduros: pesquisa alargada (inventor e requerente alternativo)</h1><p>Em cada família carrega no botão da aeronave que ela mostra, em <b>Dúvida</b> ou em <b>Não é</b>. "
    "Se nenhuma família mostra a aeronave, carrega em <b>Nenhuma família mostra</b>. No fim, <b>Exportar respostas</b>.</p>"], []
for ck, g in C.groupby("ck", sort=False):
    if ck not in ("pivotal", "leoflight"): continue
    fam = X[asg.str.contains(RX.get(ck, re.escape(re.sub(r"[^a-z0-9 ]", " ", g.empresa.iloc[0].lower()).split()[0])))].sort_values("Priority Year")
    for a in g.aeronave: des.append({"aeronave": a, "empresa": g.empresa.iloc[0], "n_familias": len(fam)})
    if fam.empty:
        parts.append(f"<h2>{html.escape(g.empresa.iloc[0])}: 0 famílias no PatSeer</h2><p>{', '.join(html.escape(a) for a in g.aeronave)}: sem patente encontrada.</p>"); continue
    ref = [(a, photos(sl)) for a, sl in zip(g.aeronave, g.slugs)]
    parts.append(f"<h2>{html.escape(g.empresa.iloc[0])}: {len(fam)} famílias</h2><div class='ref'>" + "".join(f"<figure><figcaption>{html.escape(a)} (VFS)</figcaption>" + "".join(f"<img src='{p.relative_to(SH)}'>" for p in ph) + "</figure>" for a, ph in ref) + "</div>")
    for a in g.aeronave:
        parts.append(f"<div class='ans' data-ac='{html.escape(a)}' data-co='{html.escape(g.empresa.iloc[0])}'><b>{html.escape(a)}:</b> <span class='st'></span><button class='nb' data-ac='{html.escape(a)}'>Nenhuma família mostra o {html.escape(a)}</button></div>")
    mini = "<div class='mini'>" + "".join(f"<img src='{ph[0].relative_to(SH)}' title='{html.escape(a)}'>" for a, ph in ref if ph) + "</div>"
    for _, r in fam.iterrows():
        ff = figs(r); rn = r["Record Number"]
        imgs = "".join(f"<img src='{p.relative_to(SH)}'>" for p in ff) or "<i>sem desenhos no Google Patents (abre o link)</i>"
        bts = "".join(f"<button data-fam='{rn}' data-ac='{html.escape(a)}' data-v='match'>É o {html.escape(a)}</button><button class='dv' data-fam='{rn}' data-ac='{html.escape(a)}' data-v='doubt'>Dúvida</button><button class='no' data-fam='{rn}' data-ac='{html.escape(a)}' data-v='no'>Não é</button> " for a in g.aeronave)
        parts.append(f"<div class='f' data-fam='{rn}'>{mini}<b><a href='{gp(rn)}' target='_blank'>{rn}</a></b> · {r.get('Priority Year', '')} · {html.escape(str(r['Title']))}<div class='bt'>{bts}</div>{imgs}<div style='clear:both'></div></div>")
    print(ck, len(fam), flush=True)
parts.append(f"</main><script>{JS}</script>")
(SH / "census_enhanced.html").write_text("\n".join(parts), encoding="utf-8")
pd.DataFrame(des).to_csv(OUT / "gs_v2_census_enhanced_designs.csv", index=False)
print("página:", SH / "census_enhanced.html")

# Google Patents throttled (503) on 2026-11-10: the drawings of the granted US families come from the USPTO full-text PDF instead.
import subprocess, tempfile, requests
USPTO = {"US2014097290A1": "9346542", "USD1078586S": "D1078586", "US2012298790A1": "9440736", "US2024239531A1": "12145753"}
page = (SH / "census_enhanced.html").read_text(encoding="utf-8"); (SH / "_uspto").mkdir(exist_ok=True)
for rn, n in USPTO.items():
    if not list((SH / "_uspto").glob(rn + "-*.png")):
        pdf = Path(tempfile.mkdtemp()) / "p.pdf"
        pdf.write_bytes(requests.get(f"https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/{n}", headers={"User-Agent": "Mozilla/5.0"}, timeout=60).content)
        subprocess.run(["pdftoppm", "-f", "2", "-l", "5", "-r", "45", "-png", str(pdf), str(SH / "_uspto" / rn)], capture_output=True)
    ims = "".join(f"<img src='_uspto/{f.name}'>" for f in sorted((SH / "_uspto").glob(rn + "-*.png")))
    page = re.sub(r"(<div class='f' data-fam='%s'>.*?)<i>sem desenhos no Google Patents \(abre o link\)</i>" % rn, lambda m: m.group(1) + ims, page, flags=re.S)
(SH / "census_enhanced.html").write_text(page, encoding="utf-8")
