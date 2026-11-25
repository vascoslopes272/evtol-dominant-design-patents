"""Gold standard v2 census: page for the PatSeer search of the two last programmes (AVIC AR-E3000, Beta Ava XC).
Families whose title names a subsystem (control, battery, charging, monitoring ...) are listed by title with links and no drawings.
Same page as 02g, built from 01_query/patseer_gs_v2_avic_beta_*.xlsx for the programmes with outcome "search pending".
Drawings come from the USPTO full-text PDF of a US family member. For every other family they come from the PDF link of the PatSeer export: the pages with almost no text (the drawing sheets) are shown.
Output: sheets_v2/census_avic_beta.html. Answers: gs_v2_census_avic_beta_<stamp>.csv.
"""
import os
import re, sys, os, html, glob, subprocess, tempfile, requests
from pathlib import Path
import pandas as pd
HERE = Path(__file__).resolve().parent
src = (HERE / "02b_pool_candidates.py").read_text(encoding="utf-8")
exec(src[:src.index("S = pd.read_csv(OUT")])
exec(re.search(r'CSS = """.*?"""', src, re.S).group(0)); exec(re.search(r'JS = r""".*?"""', src, re.S).group(0))
exec(src[src.index("from PIL import Image"):src.index("rows, parts = [], [")].replace('S = S[S.o_que_falta', '#').split("rv = pd.read_excel")[0])
JS = JS.replace("gs_v2_pool_answers_v1", "gs_v2_census_avic_beta_v1").replace("gs_v2_pool_answers_", "gs_v2_census_avic_beta_")

X = pd.read_excel(sorted(glob.glob(str(DATA_DIR / "01_query/patseer_gs_v2_avic_beta_*.xlsx")))[-1])
asg = (X["Current Assignee"].fillna("").astype(str) + " | " + X["Assignee"].fillna("").astype(str)).str.lower()
RX = {"avic": "china helicopter", "beta": "beta air"}
SUB = re.compile(r"system|method|batter|charg|control|monitor|navigation|display|network|data|power|motor|stator|landing gear|payload|station|protection|detection|estimat|observer|analysis|mechanism|device|assembly|airfoil|vibration", re.I)
A = pd.read_csv(OUT / "gs_v2_census_aircraft.csv"); A = A[(A.outcome == "search pending") & A.ck.isin(RX)]
T = pd.read_csv(OUT / "gs_v2_census_widen_triage.csv").set_index(["ck", "aeronave"]).slugs
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

import openpyxl, time
_ws = openpyxl.load_workbook(sorted(glob.glob(str(DATA_DIR / "01_query/patseer_gs_v2_avic_beta_*.xlsx")))[-1]).active
_h = [c.value for c in _ws[1]]; _i = _h.index("PDF Link")
PDFL = {r[0].value: r[_i].hyperlink.target for r in _ws.iter_rows(min_row=2) if r[_i].hyperlink}
PDFC = Path(os.environ.get("PDF_CACHE", tempfile.gettempdir())) / "avic_beta_pdf"; PDFC.mkdir(parents=True, exist_ok=True)
(SH / "_pspdf").mkdir(exist_ok=True)
def patseer_figs(rn, cap=8):
    """Drawing sheets of the PatSeer PDF: pages with fewer than 200 characters of text."""
    if not list((SH / "_pspdf").glob(rn + "-*.png")) and rn in PDFL:
        try:
            pdf = PDFC / (rn + ".pdf")
            if not pdf.exists():
                pdf.write_bytes(requests.get(PDFL[rn], timeout=120).content); time.sleep(1)
            n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout).group(1))
            pg = [k for k in range(1, n + 1) if len(subprocess.run(["pdftotext", "-f", str(k), "-l", str(k), str(pdf), "-"], capture_output=True, text=True).stdout.strip()) < 200]
            pg = (pg or [1] + list(range(max(2, n - 3), n + 1)))[:cap]
            for k in pg: subprocess.run(["pdftoppm", "-f", str(k), "-l", str(k), "-r", "45", "-png", str(pdf), str(SH / "_pspdf" / rn)], capture_output=True)
        except Exception as e: print("patseer pdf fail", rn, e)
    return sorted((SH / "_pspdf").glob(rn + "-*.png"))

parts = [f"<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Censo: famílias do alargamento</title><style>{CSS}</style>",
    "<div id='bar'><span class='s' id='prog'></span><button onclick='exportCSV()'>Exportar respostas (CSV)</button><button onclick='copyTxt()'>Copiar como texto</button>"
    "<span>Verde = mostra a aeronave · Laranja = dúvida · Cinzento = não é.</span></div><main>",
    "<h1>Censo: AVIC AR-E3000 e Beta Ava XC</h1><p>Em cada família carrega no botão da aeronave que ela mostra, em <b>Dúvida</b> ou em <b>Não é</b>. "
    "Se nenhuma família mostra a aeronave, carrega em <b>Nenhuma família mostra</b>." + (" <b>Lista curta:</b> o Claude viu os desenhos das 116 famílias e deixou aqui só as candidatas. A leitura dele é provisória, a tua resposta é a que conta." if os.environ.get('SHORT') else "") + " As famílias marcadas <b>no dataset</b> já estão nas 1 639. No fim, <b>Exportar respostas</b>.</p>"]
des = []
SHORT = [x for x in os.environ.get('SHORT', '').split(',') if x]  # shortlist mode: only these families, larger drawings from _short/
for ck, g in A.groupby("ck", sort=False):
    co = g.empresa.iloc[0]
    if ck not in RX: parts.append(f"<h2>{html.escape(co)}: não pesquisada</h2><p>{', '.join(map(html.escape, g.aeronave))}</p>"); continue
    fam = X[asg.str.contains(RX[ck])].copy(); fam['_s'] = fam.Title.astype(str).map(lambda t: bool(SUB.search(t))); fam = fam.sort_values(['_s', 'Priority Year'])
    if SHORT: fam = fam[fam['Record Number'].isin(SHORT)]
    for a in g.aeronave: des.append({"ck": ck, "aeronave": a, "empresa": co, "n_familias": len(fam)})
    if fam.empty: parts.append(f"<h2>{html.escape(co)}: 0 famílias no PatSeer</h2><p>{', '.join(map(html.escape, g.aeronave))}: sem patente encontrada.</p>"); continue
    ref = [(a, photos(T.get((ck, a), ""))) for a in g.aeronave]
    parts.append(f"<h2>{html.escape(co)}: {len(fam)} famílias</h2><div class='ref'>" + "".join(f"<figure><figcaption>{html.escape(a)} (VFS)</figcaption>" + "".join(f"<img src='{p.relative_to(SH)}'>" for p in ph) + "</figure>" for a, ph in ref) + "</div>")
    for a in g.aeronave:
        parts.append(f"<div class='ans' data-ac='{html.escape(a)}' data-co='{html.escape(co)}'><b>{html.escape(a)}:</b> <span class='st'></span><button class='nb' data-ac='{html.escape(a)}'>Nenhuma família mostra o {html.escape(a)}</button></div>")
    mini = "<div class='mini'>" + "".join(f"<img src='{ph[0].relative_to(SH)}' title='{html.escape(a)}'>" for a, ph in ref if ph) + "</div>"
    for _, r in fam.iterrows():
        rn = r["Record Number"]; sub = bool(SUB.search(str(r['Title']))); n = None if sub else uspto_no(r); ff = uspto_figs(rn, n) if n else []
        inds = " · <b>no dataset</b>" if members(r) & P else ""
        if not ff: ff = patseer_figs(rn)
        if SHORT: ff = sorted((SH / '_short').glob(rn + '-*.png')) or ff
        imgs = "".join(f"<img src='{p.parent.name}/{p.name}'>" for p in ff) or ("<i>sem PDF: abre o link para ver os desenhos</i>" if sub else "<i>sem PDF: abre o link para ver os desenhos</i>")
        bts = "".join(f"<button data-fam='{rn}' data-ac='{html.escape(a)}' data-v='match'>É o {html.escape(a)}</button><button class='dv' data-fam='{rn}' data-ac='{html.escape(a)}' data-v='doubt'>Dúvida</button><button class='no' data-fam='{rn}' data-ac='{html.escape(a)}' data-v='no'>Não é</button> " for a in g.aeronave)
        parts.append(f"<div class='f' data-fam='{rn}'>{mini}<b><a href='{gp(rn)}' target='_blank'>{rn}</a></b> · <a href='https://worldwide.espacenet.com/patent/search?q=pn%3D{rn}' target='_blank'>Espacenet</a> · {r.get('Priority Year', '')}{inds} · {html.escape(str(r['Title']))}<div class='bt'>{bts}</div>{imgs}<div style='clear:both'></div></div>")
    print(ck, len(fam), flush=True)
parts.append(f"</main><script>{JS}</script>")
(SH / ("census_avic_beta_short.html" if SHORT else "census_avic_beta.html")).write_text("\n".join(parts), encoding="utf-8")
if not SHORT: pd.DataFrame(des).to_csv(OUT / "gs_v2_census_avic_beta_designs.csv", index=False)
print("página:", SH / "census_avic_beta.html")
