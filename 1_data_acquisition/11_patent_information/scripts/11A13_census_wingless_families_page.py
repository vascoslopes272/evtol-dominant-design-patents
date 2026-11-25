"""Gold standard v2, second stratum (wingless at TRL 6): page for the PatSeer search of the programmes the author admitted.
Same page as 02g, built from 01_query/patseer_gs_v2_widen_wingless_*.xlsx for the programmes with outcome "search pending".
Drawings come from the USPTO full-text PDF of a US family member (Google Patents was throttled). Families with no US member show a link only.
Output: sheets_v2/census_wingless_families.html. Answers: gs_v2_census_wingless_families_<stamp>.csv.
"""
import re, sys, os, html, glob, subprocess, tempfile, requests
from pathlib import Path
import pandas as pd
HERE = Path(__file__).resolve().parent
src = (HERE / "02b_pool_candidates.py").read_text(encoding="utf-8")
exec(src[:src.index("S = pd.read_csv(OUT")])
exec(re.search(r'CSS = """.*?"""', src, re.S).group(0)); exec(re.search(r'JS = r""".*?"""', src, re.S).group(0))
exec(src[src.index("from PIL import Image"):src.index("rows, parts = [], [")].replace('S = S[S.o_que_falta', '#').split("rv = pd.read_excel")[0])
JS = JS.replace("gs_v2_pool_answers_v1", "gs_v2_census_wingless_families_v1").replace("gs_v2_pool_answers_", "gs_v2_census_wingless_families_")

X = pd.read_excel(sorted(glob.glob(str(DATA_DIR / "01_query/patseer_gs_v2_widen_wingless_*.xlsx")))[-1])
asg = (X["Current Assignee"].fillna("").astype(str) + " | " + X["Assignee"].fillna("").astype(str)).str.lower()
RX = {"hangzhouzhiyuanresearchinstitute": "zhiyuan", "verticalaerospace": "vertical aerospace", "jetson": "jetson", "dtaaircraftmanufacturer": "dta aircraft", "rotorxaircraftmanufacturing": "rotor x"}
T0 = pd.read_csv(OUT / "gs_v2_census_widen_triage.csv")
ans = pd.read_csv(OUT / "gs_v2_census_wingless_stratum_answers.csv"); ans = ans[ans.resposta == "entra"]
keys = set(ans.item)
A = T0[(T0.ck + "|" + T0.aeronave).isin(keys) & T0.ck.isin(RX)].copy()
T = T0.set_index(["ck", "aeronave"]).slugs
P = set(pd.read_csv(DATA_DIR / "02_patents/patents_1639.csv", low_memory=False).patent_id.astype(str))
def members(r): return set(re.findall(r"[A-Z]{2}[A-Z0-9]+", str(r["Simple Family Members"]))) | {r["Record Number"]}
def uspto_no(r):
    us = [m for m in members(r) if m.startswith("US")]
    for m in us:
        if re.fullmatch(r"USD\d+S\d?", m): return "D" + re.sub(r"\D", "", m[3:].split("S")[0])
    for m in us:
        g = re.fullmatch(r"US(\d{7,8})B\d", m)
        if g: return g.group(1)
    for m in us:
        g = re.fullmatch(r"US(\d{4})0?(\d{6})A\d", m)
        if g: return g.group(1) + "0" + g.group(2)
    return None
(SH / "_uspto").mkdir(exist_ok=True)
def uspto_figs(rn, n):
    if not list((SH / "_uspto").glob(rn + "-*.png")):
        try:
            pdf = Path(tempfile.mkdtemp()) / "p.pdf"
            pdf.write_bytes(requests.get(f"https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/{n}", headers={"User-Agent": "Mozilla/5.0"}, timeout=90).content)
            subprocess.run(["pdftoppm", "-f", "1", "-l", "6", "-r", "45", "-png", str(pdf), str(SH / "_uspto" / rn)], capture_output=True)
        except Exception as e: print("uspto fail", rn, e)
    return sorted((SH / "_uspto").glob(rn + "-*.png"))

parts = [f"<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Censo: famílias do alargamento</title><style>{CSS}</style>",
    "<div id='bar'><span class='s' id='prog'></span><button onclick='exportCSV()'>Exportar respostas (CSV)</button><button onclick='copyTxt()'>Copiar como texto</button>"
    "<span>Verde = mostra a aeronave · Laranja = dúvida · Cinzento = não é.</span></div><main>",
    "<h1>Segundo estrato (sem asa, TRL 6): famílias das empresas</h1><p>Em cada família carrega no botão da aeronave que ela mostra, em <b>Dúvida</b> ou em <b>Não é</b>. "
    "Se nenhuma família mostra a aeronave, carrega em <b>Nenhuma família mostra</b>. As famílias marcadas <b>no dataset</b> já estão nas 1 639. No fim, <b>Exportar respostas</b>.</p>"]
des = []
for ck, g in A.groupby("ck", sort=False):
    co = g.empresa.iloc[0]
    if ck not in RX: parts.append(f"<h2>{html.escape(co)}: não pesquisada</h2><p>{', '.join(map(html.escape, g.aeronave))}</p>"); continue
    fam = X[asg.str.contains(RX[ck])].sort_values("Priority Year")
    for a in g.aeronave: des.append({"ck": ck, "aeronave": a, "empresa": co, "n_familias": len(fam)})
    if fam.empty: parts.append(f"<h2>{html.escape(co)}: 0 famílias no PatSeer</h2><p>{', '.join(map(html.escape, g.aeronave))}: sem patente encontrada.</p>"); continue
    ref = [(a, photos(T.get((ck, a), ""))) for a in g.aeronave]
    parts.append(f"<h2>{html.escape(co)}: {len(fam)} famílias</h2><div class='ref'>" + "".join(f"<figure><figcaption>{html.escape(a)} (VFS)</figcaption>" + "".join(f"<img src='{p.relative_to(SH)}'>" for p in ph) + "</figure>" for a, ph in ref) + "</div>")
    for a in g.aeronave:
        parts.append(f"<div class='ans' data-ac='{html.escape(a)}' data-co='{html.escape(co)}'><b>{html.escape(a)}:</b> <span class='st'></span><button class='nb' data-ac='{html.escape(a)}'>Nenhuma família mostra o {html.escape(a)}</button></div>")
    mini = "<div class='mini'>" + "".join(f"<img src='{ph[0].relative_to(SH)}' title='{html.escape(a)}'>" for a, ph in ref if ph) + "</div>"
    for _, r in fam.iterrows():
        rn = r["Record Number"]; n = uspto_no(r); ff = uspto_figs(rn, n) if n else []
        inds = " · <b>no dataset</b>" if members(r) & P else ""
        imgs = "".join(f"<img src='_uspto/{p.name}'>" for p in ff) or "<i>sem membro americano: abre o link para ver os desenhos</i>"
        bts = "".join(f"<button data-fam='{rn}' data-ac='{html.escape(a)}' data-v='match'>É o {html.escape(a)}</button><button class='dv' data-fam='{rn}' data-ac='{html.escape(a)}' data-v='doubt'>Dúvida</button><button class='no' data-fam='{rn}' data-ac='{html.escape(a)}' data-v='no'>Não é</button> " for a in g.aeronave)
        parts.append(f"<div class='f' data-fam='{rn}'>{mini}<b><a href='{gp(rn)}' target='_blank'>{rn}</a></b> · <a href='https://worldwide.espacenet.com/patent/search?q=pn%3D{rn}' target='_blank'>Espacenet</a> · {r.get('Priority Year', '')}{inds} · {html.escape(str(r['Title']))}<div class='bt'>{bts}</div>{imgs}<div style='clear:both'></div></div>")
    print(ck, len(fam), flush=True)
parts.append(f"</main><script>{JS}</script>")
(SH / "census_wingless_families.html").write_text("\n".join(parts), encoding="utf-8")
pd.DataFrame(des).to_csv(OUT / "gs_v2_census_wingless_families_designs.csv", index=False)
print("página:", SH / "census_wingless_families.html")
