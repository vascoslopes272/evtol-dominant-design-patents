"""Build dataset_overview.html (static, no JavaScript) and dataset_overview.md for the public dataset.

Usage: python3 make_overview_html.py [DATASET_DIR] [--repo-docs DIR]
DATASET_DIR defaults to $EVTOL_DATASET. The page is written to DATASET_DIR/dataset_overview.html
and, with --repo-docs, a copy plus dataset_overview.md are written to that folder.
Descriptions (what it is / one row per / depends on) are taken only from the READMEs inside the dataset.
Files with no README row get no description and are listed on stderr.
"""
import os, re, sys, csv, html, json, shutil
import pandas as pd, openpyxl

args = sys.argv[1:]
docs = None
if "--repo-docs" in args:
    i = args.index("--repo-docs"); docs = args[i + 1]; del args[i:i + 2]
ROOT = os.path.abspath(args[0] if args else os.environ["EVTOL_DATASET"])
BLOCKS = {"05_images"}
SKIP = {"dataset_overview.html"}
e = html.escape

def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB": return f"{n:.0f} {u}" if u == "B" else f"{n:.1f} {u}"
        n /= 1024

def code(s):
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", e(s)).replace("**", "")
def plain(s): return s.replace("**", "")

# ---------- README parsing ----------
def split_row(line):
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|")); return [c.strip() for c in cells]
def parse_readme(path):
    """returns (sections, rows): sections {heading: first paragraph}, rows [(heading, cells)]"""
    sec, rows, head, buf = {}, [], "", []
    lines = open(path, encoding="utf-8").read().split("\n")
    def flush():
        if head not in sec:
            para = [p for p in "\n".join(buf).split("\n\n") if p.strip() and not p.lstrip().startswith(("|", "-"))]
            sec[head] = plain(para[0].strip().replace("\n", " ")) if para else ""
    for ln in lines:
        if ln.startswith("#"):
            flush(); head = ln.lstrip("#").strip(); buf = []; sec.setdefault(head, None); continue
        if ln.startswith("|"):
            c = split_row(ln)
            if c[0] in ("File", "File or folder") or set(c[0]) <= set("-: "): continue
            rows.append((head, c)); continue
        buf.append(ln)
    flush()
    return {k: v or "" for k, v in sec.items()}, rows

INFO = {}      # relpath (file or folder with trailing /) -> (what, grain, dep)
README_TOKENS = []  # (readme, token, resolved or None)
def all_files(folder):
    out = []
    for d, _, fs in os.walk(os.path.join(ROOT, folder)):
        for f in fs: out.append(os.path.relpath(os.path.join(d, f), ROOT))
    return out
def resolve(base, tok):
    p = os.path.normpath(os.path.join(base, tok))
    if os.path.exists(os.path.join(ROOT, p)): return p + ("/" if os.path.isdir(os.path.join(ROOT, p)) else "")
    if "/" not in tok:  # bare name: unique file with that name below base
        hits = [f for f in all_files(base) if os.path.basename(f) == tok] if base else []
        if len(hits) == 1: return hits[0]
    return None
FOLDER_TEXT = {}
def read_all():
    secs, rows = parse_readme(os.path.join(ROOT, "README.md"))
    FOLDER_TEXT[""] = secs.get("eVTOL_dataset", "")
    for h, v in secs.items():
        m = re.match(r"(\d\d_\w+)", h)
        if m: FOLDER_TEXT[m.group(1)] = v
    sources = [("", "README.md", rows)]
    for d in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, d, "README.md")
        if os.path.isfile(p):
            s, r = parse_readme(p); sources.append((d, f"{d}/README.md", r))
            if not FOLDER_TEXT.get(d): FOLDER_TEXT[d] = next((v for k, v in s.items() if v and k == d), "")
    for base, rd, rws in sources:
        for h, c in rws:
            if len(c) < 4: continue
            heading_dir = re.match(r"(\d\d_\w+)", h)
            b = base or (heading_dir.group(1) if heading_dir else "")
            toks = re.findall(r"`([^`]+)`", c[0])
            last = None
            for t in toks:
                r = resolve(b, t)
                if r is None and last: r = resolve(os.path.dirname(last), t)
                README_TOKENS.append((rd, t, r))
                if r:
                    last = r; info = (plain(c[1]), plain(c[2]), plain(c[3]))
                    if r not in INFO or not INFO[r][0]: INFO[r] = info
read_all()

# ---------- data dictionary (section only) ----------
SECTION = {}
dd = os.path.join(ROOT, "data_dictionary.csv")
if os.path.exists(dd):
    for r in csv.DictReader(open(dd, encoding="utf-8")): SECTION[(r["file"], r["column"])] = r.get("section", "")

def shorten(v, n=70):
    v = "" if v is None else str(v).replace("\n", " ")
    return v if len(v) <= n else v[:n - 1] + "…"
def fmt_cols(df, rel, nrows, filled):
    cols = []
    for c in df.columns:
        s = filled[c]
        ex = ""
        if s is not None and len(s): ex = shorten(s.iloc[0])
        cols.append({"n": str(c), "e": ex, "f": 0 if not nrows else round(100 * len(s) / nrows) if s is not None else 0,
                     "g": SECTION.get((rel, str(c)), "")})
    return cols
def isfilled(x): return x is not None and str(x).strip() != "" and str(x) != "nan"
def table_info(df, rel):
    df = df.astype(object).where(df.notna(), None)
    filled = {c: df[c][df[c].map(isfilled)] for c in df.columns}
    return {"rows": len(df), "cols": fmt_cols(df, rel, len(df), filled),
            "head": [[shorten(v, 50) for v in r] for r in df.head(5).values.tolist()]}

def node_file(rel):
    full = os.path.join(ROOT, rel); ext = os.path.splitext(rel)[1].lower()
    what, grain, dep = INFO.get(rel, ("", "", ""))
    n = {"dir": False, "name": os.path.basename(rel), "path": rel, "size": human(os.path.getsize(full)), "what": what, "grain": grain, "frm": dep}
    if ext == ".csv":
        try: n.update(kind="table", **table_info(pd.read_csv(full, dtype=str, keep_default_na=False, na_values=[""]), rel))
        except Exception as ex: n.update(kind="text", text=f"(could not read as a table: {ex})")
    elif ext == ".xlsx":
        wb = openpyxl.load_workbook(full, read_only=True, data_only=True); sheets = []
        for ws in wb.worksheets:
            it = ws.iter_rows(values_only=True); hdr = next(it, None)
            if hdr is None: sheets.append({"name": ws.title, "rows": 0, "cols": [], "head": []}); continue
            hdr = [("" if h is None else str(h)) for h in hdr]
            while hdr and not hdr[-1]: hdr.pop()
            k = len(hdr); cnt = [0] * k; ex = [""] * k; head = []; nr = 0
            for r in it:
                r = list(r[:k]) + [None] * (k - len(r)); nr += 1
                for i, v in enumerate(r):
                    if isfilled(v):
                        cnt[i] += 1
                        if not ex[i]: ex[i] = shorten(v)
                if nr <= 3: head.append([shorten(v, 40) for v in r])
            sheets.append({"name": ws.title, "rows": nr, "head": head,
                           "cols": [{"n": hdr[i], "e": ex[i], "f": round(100 * cnt[i] / nr) if nr else 0, "g": ""} for i in range(k)]})
        n.update(kind="xlsx", sheets=sheets)
    elif ext in (".txt", ".md", ".jsonl"):
        with open(full, encoding="utf-8", errors="replace") as fh: t = fh.read(1800)
        n.update(kind="text", text=t + ("\n…" if os.path.getsize(full) > 1800 else ""))
    return n

def node_dir(rel):
    full = os.path.join(ROOT, rel) if rel else ROOT
    name = os.path.basename(rel) if rel else os.path.basename(ROOT)
    if rel in BLOCKS:
        files = all_files(rel); tot = sum(os.path.getsize(os.path.join(ROOT, f)) for f in files)
        subs = {}
        for f in files:
            s = f.split("/")[1] if f.count("/") > 1 else "(top level)"; subs[s] = subs.get(s, 0) + 1
        return {"dir": True, "block": True, "name": name, "path": rel, "n": len(files), "size": human(tot), "what": FOLDER_TEXT.get(rel, ""),
                "subs": sorted(subs.items())}
    what = INFO.get(rel + "/", ("",))[0] or FOLDER_TEXT.get(rel, "")
    kids = []
    for x in sorted(os.listdir(full)):
        r = f"{rel}/{x}" if rel else x
        if x in SKIP or (not rel and x == "README.md") or (rel and x == "README.md" and "/" not in rel): continue
        kids.append(node_dir(r) if os.path.isdir(os.path.join(ROOT, r)) else node_file(r))
    kids.sort(key=lambda k: (not k["dir"], k["name"]))
    return {"dir": True, "name": name, "path": rel, "what": what, "kids": kids}

# the root README is listed as a file too
tree = node_dir("")
tree["kids"] = [k for k in tree["kids"]]

# ---------- rendering (same layout and CSS as the earlier static page) ----------
def cols_html(cols):
    out = "<table><tr><th>column</th><th>example</th><th>filled</th></tr>"; g = ""
    for c in cols:
        if c["g"] and c["g"] != g: g = c["g"]; out += f'<tr class="g"><td colspan="3">{e(g)}</td></tr>'
        out += f'<tr><td class="n">{e(c["n"])}</td><td>{e(c["e"])}</td><td>{c["f"]} %</td></tr>'
    return out + "</table>"
def head_html(cols, head):
    return "<table><tr>" + "".join(f'<th>{e(c["n"])}</th>' for c in cols) + "</tr>" + "".join("<tr>" + "".join(f"<td>{e(v)}</td>" for v in r) + "</tr>" for r in head) + "</table>"
def fmtn(n): return f"{n:,}".replace(",", " ")
def file_html(n):
    h = f'<details class="f"><summary><span class="k">{e(n["name"])}</span> <span class="s">{e(n["size"])}</span><span class="w">{code(n["what"])}</span></summary><div class="b">'
    if n.get("grain"): h += f'<p class="gr">One row per: <b>{code(n["grain"])}</b></p>'
    if n.get("frm"): h += f'<p class="fr">Depends on: {code(n["frm"])}</p>'
    if n.get("kind") == "table":
        h += f'<h5>{fmtn(n["rows"])} rows · {len(n["cols"])} columns</h5>' + cols_html(n["cols"])
        if n["head"]: h += "<h5>First rows</h5>" + head_html(n["cols"], n["head"])
    elif n.get("kind") == "xlsx":
        for s in n["sheets"]:
            h += f'<h5>Sheet “{e(s["name"])}” · {fmtn(s["rows"])} rows · {len(s["cols"])} columns</h5>'
            if s["cols"]:
                h += cols_html(s["cols"])
                if s["head"]: h += "<h5>First rows</h5>" + head_html(s["cols"], s["head"])
    elif n.get("kind") == "text": h += f'<h5>Start of the file</h5><pre>{e(n["text"])}</pre>'
    return h + "</div></details>"
def dir_html(n, depth=0):
    if n.get("block"):
        subs = "".join(f"<li><code>{e(s)}</code>: {fmtn(c)} files</li>" for s, c in n["subs"])
        return f'<details class="f"><summary><span class="k">{e(n["name"])}/</span> <span class="s">{fmtn(n["n"])} files · {e(n["size"])}</span><span class="w">{code(n["what"])}</span></summary><div class="b"><ul>{subs}</ul></div></details>'
    h = f'<details class="d"{" open" if depth < 2 else ""}><summary><span class="k">{e(n["name"])}/</span><span class="w">{code(n.get("what",""))}</span></summary><div class="in">'
    for k in n["kids"]: h += dir_html(k, depth + 1) if k["dir"] else file_html(k)
    return h + "</div></details>"
css = """body{font:15px/1.5 system-ui,Segoe UI,sans-serif;margin:0;background:#f5f6f8;color:#1c2330}header{background:#16233f;color:#fff;padding:14px 24px}header h1{margin:0;font-size:18px}
main{max-width:1100px;margin:18px auto;padding:0 18px}details{margin:4px 0}summary{cursor:pointer;padding:6px 8px;border-radius:7px}summary:hover{background:#e9eef8}.d>summary{font-weight:650}.k{font-family:ui-monospace,Menlo,monospace;font-size:13.5px}.s{color:#5f6b7a;font-size:12px;margin-left:8px}.w{color:#5f6b7a;margin-left:12px;font-size:13.5px}
.in{margin-left:18px;border-left:2px solid #dfe3ea;padding-left:10px}.f>.b{margin:6px 0 10px 18px;padding:10px 14px;background:#fff;border:1px solid #dfe3ea;border-radius:10px;overflow:auto}.gr{background:#eef3fb;display:inline-block;border-radius:8px;padding:3px 10px}.fr{color:#5f6b7a;font-size:13px}
code{font-family:ui-monospace,Menlo,monospace;font-size:12.5px}
table{border-collapse:collapse;font-size:12.5px;margin:6px 0}th,td{border:1px solid #dfe3ea;padding:3px 7px;text-align:left;vertical-align:top;max-width:380px;overflow-wrap:anywhere}th{background:#f3f5f8;color:#5f6b7a;font-size:11.5px;text-transform:uppercase}td.n{font-family:ui-monospace,Menlo,monospace;white-space:nowrap}tr.g td{background:#eef3fb;font-weight:650;color:#1f4b99}h5{margin:12px 0 4px;color:#5f6b7a;text-transform:uppercase;font-size:12px}pre{background:#f7f8fa;border:1px solid #dfe3ea;border-radius:8px;padding:8px 10px;font:12px/1.5 ui-monospace,Menlo,monospace;white-space:pre-wrap;overflow:auto;max-height:340px}"""
intro = FOLDER_TEXT.get("", "")
page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dataset overview</title><style>{css}</style></head><body>'
        f'<header><h1>eVTOL_dataset, file by file</h1></header><main><p>{code(intro)}</p><p>Click a folder or a file to open it. No JavaScript is needed. Descriptions are copied from the README files of the dataset; the columns, examples, fill percentages and first rows are read from the files.</p>'
        + dir_html(tree) + "</main></body></html>")

# ---------- markdown ----------
md = ["# eVTOL_dataset, file by file\n", intro + "\n"]
def md_dir(n, lvl):
    if n.get("block"):
        md.append(f'{"#"*min(lvl,5)} `{n["name"]}/` ({fmtn(n["n"])} files, {n["size"]})\n\n{n["what"]}\n')
        md.extend(f"- `{s}`: {fmtn(c)} files" for s, c in n["subs"]); md.append(""); return
    md.append(f'{"#"*min(lvl,5)} `{n["path"] or os.path.basename(ROOT)}/`\n\n{n.get("what","")}\n')
    for k in n["kids"]:
        if k["dir"]: md_dir(k, lvl + 1); continue
        md.append(f'{"#"*min(lvl+1,6)} `{k["name"]}` ({k["size"]})\n\n{k["what"]}\n')
        if k.get("grain"): md.append(f'**One row per:** {k["grain"]}\n')
        if k.get("frm"): md.append(f'**Depends on:** {k["frm"]}\n')
        def colt(cols):
            md.append("| column | example | filled |\n|---|---|---|"); g = ""
            for c in cols:
                if c["g"] and c["g"] != g: g = c["g"]; md.append(f'| **{g}** | | |')
                md.append(f'| `{c["n"]}` | {c["e"].replace("|","/")} | {c["f"]} % |')
            md.append("")
        if k.get("kind") == "table": md.append(f'{fmtn(k["rows"])} rows · {len(k["cols"])} columns\n'); colt(k["cols"])
        elif k.get("kind") == "xlsx":
            for s in k["sheets"]:
                md.append(f'Sheet “{s["name"]}”, {fmtn(s["rows"])} rows · {len(s["cols"])} columns\n')
                if s["cols"]: colt(s["cols"])
md_dir(tree, 2)
mdtext = "\n".join(md)

out = os.path.join(ROOT, "dataset_overview.html"); open(out, "w", encoding="utf-8").write(page)
if docs:
    os.makedirs(docs, exist_ok=True); shutil.copy(out, os.path.join(docs, "dataset_overview.html"))
    open(os.path.join(docs, "dataset_overview.md"), "w", encoding="utf-8").write(mdtext)

# ---------- report ----------
def walk(n):
    for k in n.get("kids", []):
        if k["dir"]: yield from walk(k)
        else: yield k
nofile = [k["path"] for k in walk(tree) if not k["what"]]
print(f"html {os.path.getsize(out)//1024} KB, md {len(mdtext)//1024} KB, script tags {page.count('<script')}", file=sys.stderr)
print("FILES WITHOUT README ROW:", *nofile, sep="\n  ", file=sys.stderr)
print("README TOKENS NOT FOUND:", *[f"{a}: {t}" for a, t, r in README_TOKENS if r is None], sep="\n  ", file=sys.stderr)
