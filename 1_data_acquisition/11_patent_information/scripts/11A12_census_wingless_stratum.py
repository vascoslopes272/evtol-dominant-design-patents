"""Gold standard v2: maturity screen of the wingless aircraft at TRL 6 (second stratum).
The 32 wingless aircraft and personal flying devices that passed the company screen were left out by the wing rule.
This page shows those that belong to programmes not yet in the census, with the sentence that reports the flight,
and asks the author whether the aircraft is mature enough to enter a wingless stratum.
Output: sheets_v2/census_wingless_stratum.html. Answers: gs_v2_census_wingless_stratum_<stamp>.csv (Downloads)."""
import re, html
from pathlib import Path
import pandas as pd
HERE = Path(__file__).resolve().parent
src = (HERE / "02b_pool_candidates.py").read_text(encoding="utf-8")
exec(src[:src.index("S = pd.read_csv(OUT")])
exec(src[src.index("from PIL import Image"):src.index("rows, parts = [], [")].replace('S = S[S.o_que_falta', '#').split("rv = pd.read_excel")[0])
m2 = (HERE / "02m_census_removed_review.py").read_text(encoding="utf-8")
exec(re.search(r'CSS = """.*?"""', m2, re.S).group(0)); exec(re.search(r'JS = r""".*?"""', m2, re.S).group(0))
JS = JS.replace("gs_v2_census_removed_review", "gs_v2_census_wingless_stratum").replace("s.v==='ok'||s.v==='sai'", "s.v==='entra'||s.v==='nao'")
A = pd.read_csv(DATA_DIR / "05_secondary/vfs/aircraft.csv", keep_default_na=False)
TR = pd.read_csv(DATA_DIR / "05_secondary/vfs/VFS_PAGE_TRL_SCRIPT.csv", keep_default_na=False).set_index("slug_key")
T7 = pd.read_csv(DATA_DIR / "05_secondary/vfs/VFS_PAGE_TRL7.csv", keep_default_na=False).set_index("slug_key")
t = pd.read_csv(OUT / "gs_v2_census_widen_triage.csv"); w = pd.read_csv(OUT / "gs_v2_census_widen_answers.csv")
m = t.merge(w[["ck", "aeronave", "decisao"]], on=["ck", "aeronave"])
m = m[(m.decisao == "empresa") & (m.proposta != "carro") & m.categoria_vfs.isin(["Wingless", "Hoverbike/PFD"])].copy()
have = set(pd.read_csv(OUT / "gs_v2_census_programmes.csv").programme)
m["programme"] = m.ck + " | " + m.categoria_vfs; m["novo"] = ~m.programme.isin(have)
E = html.escape
O = [("entra", "Entra: no domínio, à escala real, voou"), ("nao", "Não entra: imatura (bancada, preso, escala reduzida, projecto fraco)"),
     ("fora", "Não entra: fora do domínio (não eléctrica, não tripulada ou só carga)"), ("duvida", "Dúvida")]
DOM = pd.read_csv(DATA_DIR / "05_secondary/vfs/DOMAIN.csv").set_index("slug_key")
OV = set(pd.read_csv(DATA_DIR / "05_secondary/vfs/domain_overrides.csv").iloc[:, 0].astype(str))
def card(r):
    ph = photos(r.slugs, 3); imgs = "".join(f"<img src='{p.relative_to(SH)}'>" for p in ph) or "<i>sem fotografia</i>"
    spec = ""
    for s in str(r.slugs).split("|"):
        a = A[A.slug_key == s]
        if not len(a): continue
        a = a.iloc[0]; fr = TR.sentence.get(s, "") if s in TR.index else ""; t7 = T7.sentence.get(s, "") if s in T7.index else ""
        spec += (f"<div class='sp'><a href='{a.url}' target='_blank'>{E(a.title)}</a> · estado: <b>{E(a.status)}</b> · capacidade: {E(a.spec_capacity) or '?'} · pilotagem: {E(a.spec_piloting) or '?'}</div>"
                 f"<div class='sp'>Domínio: energia: <b>{E(a.spec_power_source) or '?'}</b> · tipo: {E(a.spec_aircraft_type) or '?'} · regra automática: "
                 f"<b>{'dentro' if bool(DOM.in_domain.get(s, False)) else 'FORA'}</b> (eléctrica: {'sim' if bool(DOM.not_combustion.get(s, False)) else 'não'}, tripulada: {'sim' if bool(DOM.crewed.get(s, False)) else 'não'})"
                 f"{' · <b>já revista por ti</b>' if s in OV else ''}</div>"
                 + (f"<div class='sp'>Frase do voo (regra TRL 6): <i>{E(str(fr))[:500]}</i></div>" if fr else "")
                 + (f"<div class='sp'>Frase TRL 7: <i>{E(str(t7))[:400]}</i></div>" if t7 else ""))
    bt = "".join(f"<label><input type='radio' name='{E(r.ck + r.aeronave)}' value='{v}'> {E(tx)}</label>" for v, tx in O)
    return (f"<div class='c' data-k='{E(r.ck)}|{E(r.aeronave)}'><h3>{E(r.empresa)} · {E(r.aeronave)}</h3><p>{E(r.categoria_vfs)} · primeiro ano: {'' if pd.isna(r.ano_1o_voo) else int(r.ano_1o_voo)}"
            f"{' · <b>já ligado a um design dos 626</b>' if r.ja_ligado_aos_626 else ''}</p>{spec}<div class='im'>{imgs}</div><div class='bt'>{bt} <input type='text' placeholder='nota (opcional)' class='nt'></div></div>")
new = m[m.novo].sort_values(["categoria_vfs", "empresa", "aeronave"]); old = m[~m.novo].sort_values(["empresa", "aeronave"])
parts = [f"<h2>Parte 1. Programas novos ({new.programme.nunique()} programas, {len(new)} aeronaves)</h2><p>Empresas ou arquitecturas que ainda não estão no censo. São estas que aumentam a amostra sem asa.</p>"]
parts += [card(r) for r in new.itertuples()]
parts.append(f"<h2>Parte 2. Versões de programas que já estão no censo ({len(old)} aeronaves)</h2><p>Não acrescentam programas. Estão aqui só para veres a lista. Podes saltar esta parte.</p>")
parts += [card(r) for r in old.itertuples()]
page = (f"<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Censo: estrato sem asa</title><style>{CSS}</style>"
        "<div id='bar'><b>Censo: aeronaves sem asa em TRL 6</b><span id='prog'></span><button onclick='exportCSV()'>Exportar respostas (CSV)</button></div><main>"
        "<h1>Aeronaves sem asa que voaram como protótipo (TRL 6)</h1><p>Já decidiste que todas estas são de empresas. Todas passaram a regra automática de domínio, mas essa regra só acerta em cerca de três em cada quatro páginas que mantém, e tu ainda não as viste uma a uma. Por isso cada cartão mostra a energia, a capacidade e a pilotagem. A pergunta é dupla: está no <b>domínio</b> (eléctrica, VTOL, tripulada) e tem <b>maturidade</b>: "
        "é uma aeronave à escala real, pensada para levar pessoas, que voou de facto? Se sim, entra no estrato sem asa do gold standard. "
        "Lê a frase do voo e olha para a fotografia. No fim, <b>Exportar respostas</b>.</p>" + "\n".join(parts) + f"</main><script>{JS}</script>")
(SH / "census_wingless_stratum.html").write_text(page, encoding="utf-8")
print("novos:", new.programme.nunique(), "programas,", len(new), "aeronaves | versões:", len(old), "|", SH / "census_wingless_stratum.html")
