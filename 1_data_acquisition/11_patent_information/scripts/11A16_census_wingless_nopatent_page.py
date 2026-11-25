"""Gold standard v2 census: last search for the wingless programmes, personal flying devices and rotorcraft with no patent found.
Source: 01_query/patseer_gs_v2_wingless_nopatent_580_*.xlsx (query_goldstandard_v2_census_wingless_nopatent.txt, 580 families).
Claude screened the 580 families on applicant, title and class, read the drawings of 8, and kept the candidates below.
That screening is provisional. The author's answer on this page is the one that counts.
Drawings: drawing sheets of the PatSeer PDF (pages with under 200 characters of text), or the USPTO PDF for US designs.
Set PDF_CACHE to a folder that holds <record>.pdf files to avoid downloading again.
Output: sheets_v2/census_wingless_nopatent.html. Answers: gs_v2_census_wingless_nopatent_<stamp>.csv (Downloads).
"""
import os
import re, os, html, glob, subprocess, time, tempfile, requests, openpyxl
from pathlib import Path
import pandas as pd
HERE = Path(__file__).resolve().parent
src = (HERE / "02b_pool_candidates.py").read_text(encoding="utf-8")
exec(src[:src.index("S = pd.read_csv(OUT")])
exec(re.search(r'CSS = """.*?"""', src, re.S).group(0)); exec(re.search(r'JS = r""".*?"""', src, re.S).group(0))
JS = JS.replace("gs_v2_pool_answers_v1", "gs_v2_census_wingless_nopatent_v1").replace("gs_v2_pool_answers_", "gs_v2_census_wingless_nopatent_")
XL = sorted(glob.glob(str(DATA_DIR / "01_query/patseer_gs_v2_wingless_nopatent_*.xlsx")))[-1]
X = pd.read_excel(XL).set_index("Record Number")
ws = openpyxl.load_workbook(XL).active; hd = [c.value for c in ws[1]]; li = hd.index("PDF Link")
LINK = {r[0].value: r[li].hyperlink.target for r in ws.iter_rows(min_row=2) if r[li].hyperlink}
P = set(pd.read_csv(DATA_DIR / "02_patents/patents_1639.csv", low_memory=False).patent_id.astype(str))
PDFC = Path(os.environ.get("PDF_CACHE", tempfile.gettempdir())); FIG = SH / "_wl"; FIG.mkdir(exist_ok=True)
# aircraft -> candidate families with Claude's provisional note
CAND = [
 ("hangzhouzhiyuanresearchinstitute", "Wearable Flying Device", [("CN122540371B", "2026, wearable aircraft with three ducted fans and a support frame with legs. Closest candidate"),
                        ("CN119348819B", "2024, wearable three-duct aircraft. The author already read this family on 11 Nov and answered that it is not the aircraft"),
                        ("CN119262304B", "2024, escape device of a single-person aircraft, shows a backpack unit")]),
 ("zerog", "ZG-ONE", [("CN113978712B", "2021, six-arm multirotor with no cabin. Weak candidate")]),
]
NOCAND = ["Star 8 Koncepto Millenya", "Voltline Skyla", "DTA eVTOL-2", "Rotor X Dragon", "Vertical VA-X2", "Jetson One", "Tier 1 e-R44"]
def figs(rn):
    if not list(FIG.glob(rn + "-*.png")):
        m = re.fullmatch(r"USD(\d+)S", rn); pdf = PDFC / (("US" + "D" + m.group(1)) if m else rn); pdf = pdf.with_suffix(".pdf")
        if not pdf.exists():
            url = f"https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/D{m.group(1)}" if m else LINK.get(rn)
            if not url: return []
            pdf.write_bytes(requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=120).content); time.sleep(1)
        n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout).group(1))
        pg = [k for k in range(1, n + 1) if len(subprocess.run(["pdftotext", "-f", str(k), "-l", str(k), str(pdf), "-"], capture_output=True, text=True).stdout.strip()) < 200]
        pg = (pg or [1] + list(range(max(2, n - 3), n + 1)))[:8]
        for k in pg: subprocess.run(["pdftoppm", "-f", str(k), "-l", str(k), "-r", "80", "-png", str(pdf), str(FIG / rn)], capture_output=True)
    return sorted(FIG.glob(rn + "-*.png"))
A = pd.read_csv(OUT / "gs_v2_census_aircraft.csv")
parts = [f"<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Censo: sem asa sem patente</title><style>{CSS} .f img{{max-height:420px}}</style>",
    "<div id='bar'><span class='s' id='prog'></span><button onclick='exportCSV()'>Exportar respostas (CSV)</button><button onclick='copyTxt()'>Copiar como texto</button>"
    "<span>Verde = mostra a aeronave · Laranja = dúvida · Cinzento = não é.</span></div><main>",
    "<h1>Censo: última pesquisa dos sem asa sem patente</h1><p>A pesquisa devolveu 580 famílias, quase todas de empresas sem relação. O Claude triou-as por requerente, título e classe, viu os desenhos de 8 e deixou aqui as candidatas. "
    "A leitura dele (em itálico) é provisória, a tua resposta é a que conta. Em cada família carrega em <b>É o …</b>, <b>Dúvida</b> ou <b>Não é</b>. Se nenhuma mostra a aeronave, carrega em <b>Nenhuma família mostra</b>.</p>"
    f"<p>Sem nenhuma candidata nesta pesquisa: {', '.join(NOCAND)}.</p>"]
for ck, ac, fams in CAND:
    r = A[(A.ck == ck) & (A.aeronave == ac)].iloc[0]; co = r.empresa
    ph = sorted((SH / "_vfs").glob(r.url.rstrip("/").split("/")[-1] + "__*"))[:3]
    parts.append(f"<h2>{html.escape(co)}: {html.escape(ac)}</h2><div class='ref'><figure><figcaption>{html.escape(ac)} (VFS) · <a href='{r.url}' target='_blank'>página</a></figcaption>" + "".join(f"<img src='{p.relative_to(SH)}'>" for p in ph) + "</figure></div>")
    parts.append(f"<div class='ans' data-ac='{html.escape(ac)}' data-co='{html.escape(co)}'><b>{html.escape(ac)}:</b> <span class='st'></span><button class='nb' data-ac='{html.escape(ac)}'>Nenhuma família mostra o {html.escape(ac)}</button></div>")
    for rn, note in fams:
        x = X.loc[rn]; mem = set(re.findall(r"[A-Z]{2}[A-Z0-9]+", str(x["Simple Family Members"]))) | {rn}
        inds = " · <b>no dataset</b>" if mem & P else ""
        imgs = "".join(f"<img src='_wl/{p.name}'>" for p in figs(rn)) or "<i>sem PDF: abre o link</i>"
        fam = f"{rn}|{ac}"
        bts = f"<button data-fam='{fam}' data-ac='{html.escape(ac)}' data-v='match'>É o {html.escape(ac)}</button><button class='dv' data-fam='{fam}' data-ac='{html.escape(ac)}' data-v='doubt'>Dúvida</button><button class='no' data-fam='{fam}' data-ac='{html.escape(ac)}' data-v='no'>Não é</button>"
        parts.append(f"<div class='f' data-fam='{fam}'><b><a href='{gp(rn)}' target='_blank'>{rn}</a></b> · <a href='https://worldwide.espacenet.com/patent/search?q=pn%3D{rn}' target='_blank'>Espacenet</a> · {x.get('Priority Year', '')}{inds} · {html.escape(str(x['Title']))} · {html.escape(str(x['Current Assignee'])[:60])}<br><i>Claude: {html.escape(note)}</i><div class='bt'>{bts}</div>{imgs}<div style='clear:both'></div></div>")
    print(ck, ac, len(fams), flush=True)
parts.append(f"</main><script>{JS}</script>")
(SH / "census_wingless_nopatent.html").write_text("\n".join(parts), encoding="utf-8")
print("página:", SH / "census_wingless_nopatent.html")
