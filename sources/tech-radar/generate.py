#!/usr/bin/env python3
"""Generate the Endo Tech Radar run report + master index from index.json."""
import json, datetime, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
DATE_LONG = datetime.datetime.strptime(DATE, "%Y-%m-%d").strftime("%B %d, %Y")

with open(os.path.join(HERE, "index.json"), encoding="utf-8") as f:
    tools = json.load(f)

CATEGORY_ORDER = [
    "Embedded firmware", "LoRa / LoRaWAN", "Go backend", "MQTT",
    "Time-series / IoT DB", "React Native", "RPi / edge fleet management",
    "RS-485 / Modbus", "Electrochemical sensing", "Edge AI / TinyML",
    "Agentic dev tooling",
]

CSS = """
:root{--bg:#f8f9fa;--card:#fff;--accent:#1d3557;--secondary:#457b9d;--highlight:#2a9d8f;--text:#1b1b1b;--muted:#6c757d;}
*{box-sizing:border-box;}
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--text);margin:0;line-height:1.55;}
.wrap{max-width:900px;margin:0 auto;padding:32px 20px 64px;}
header{border-bottom:3px solid var(--accent);padding-bottom:16px;margin-bottom:8px;}
h1{color:var(--accent);font-size:1.95rem;margin:0 0 6px;}
.sub{color:var(--muted);font-size:.95rem;}
h2{color:var(--accent);font-size:1.3rem;margin:36px 0 6px;border-left:5px solid var(--highlight);padding-left:10px;}
h3{color:var(--secondary);font-size:1.02rem;margin:22px 0 10px;text-transform:uppercase;letter-spacing:.5px;font-size:.85rem;}
.note-box{background:#eef4f3;border-left:4px solid var(--highlight);border-radius:8px;padding:16px 18px;margin:14px 0 8px;}
.card{background:var(--card);border-radius:10px;box-shadow:0 1px 4px rgba(0,0,0,.08);padding:16px 18px;margin-bottom:14px;}
.card .top{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;flex-wrap:wrap;}
.card a.title{font-weight:600;color:var(--accent);text-decoration:none;font-size:1.06rem;}
.card a.title:hover{text-decoration:underline;}
.meta{color:var(--muted);font-size:.82rem;margin:3px 0 8px;}
.desc{font-size:.92rem;margin:6px 0;}
.why{font-size:.88rem;color:#333;background:#fafbfc;border-radius:6px;padding:8px 10px;margin-top:8px;}
.badges{display:flex;gap:6px;flex-shrink:0;}
.badge{display:flex;flex-direction:column;align-items:center;color:#fff;border-radius:8px;padding:4px 9px;min-width:46px;font-size:.7rem;line-height:1.2;}
.badge b{font-size:1.05rem;}
.tag{display:inline-block;border-radius:20px;padding:2px 9px;font-size:.68rem;font-weight:600;color:#fff;background:var(--highlight);margin-left:6px;vertical-align:middle;}
.tag.update{background:#e76f51;}
table{width:100%;border-collapse:collapse;background:var(--card);border-radius:10px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.08);margin-top:10px;}
th{background:var(--accent);color:#fff;text-align:left;padding:9px 11px;font-size:.82rem;}
td{padding:8px 11px;border-top:1px solid #eee;font-size:.86rem;vertical-align:top;}
tr:nth-child(even) td{background:#fafbfc;}
td a{color:var(--secondary);}
.cb{font-weight:700;color:var(--accent);}
.btn{display:inline-block;background:var(--highlight);color:#fff;border:none;border-radius:8px;padding:11px 22px;font-size:1rem;cursor:pointer;margin:22px 0 6px;}
.btn:hover{background:#21867a;}
@media print{.btn{display:none;}body{background:#fff;}.card,table{box-shadow:none;}}
"""

def bcolor(v):
    return "#2a9d8f" if v >= 4 else ("#e9c46a" if v == 3 else "#adb5bd")

def badge(label, v):
    return f'<div class="badge" style="background:{bcolor(v)}"><span>{label}</span><b>{v}</b></div>'

def card(t):
    tag = '<span class="tag update">UPDATE</span>' if t.get("_update") else '<span class="tag">NEW</span>'
    return f"""<div class="card">
  <div class="top">
    <div>
      <a class="title" href="{t['url']}" target="_blank">{t['name']}</a>{tag}
      <div class="meta">{t['version']} &middot; {t['release_date']} &middot; {t['language']} &middot; {t['license']}</div>
    </div>
    <div class="badges">{badge('Ease',t['ease'])}{badge('Qual',t['quality'])}{badge('Rel',t['relevance'])}</div>
  </div>
  <div class="desc">{t['description']}</div>
  <div class="why"><b>Why it matters:</b> {t['note']}</div>
</div>"""

def page(title, sub, body):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title><style>{CSS}</style></head><body><div class="wrap">
<header><h1>{title}</h1><div class="sub">{sub}</div></header>
<button class="btn" onclick="window.print()">Save as PDF</button>
{body}
<button class="btn" onclick="window.print()">Save as PDF</button>
</div></body></html>"""

# ---------- RUN REPORT ----------
by_combined = sorted(tools, key=lambda t: -t["combined"])
top = by_combined[0]
editor = (f"Today's standout is <b>{top['name']}</b> ({top['version']}, Combined {top['combined']}/15) "
          f"in {top['category']}: {top['note']} "
          "Two finds tie at a perfect 15 — TimescaleDB v2.26 and libmodbus — both directly serving the planned "
          "InfluxDB migration and our RS-485 sensor bus. Also worth a look: mochi-mqtt (embed the broker in the Go API) "
          "and Mender (atomic A/B OTA with rollback) as we scale toward 1000 devices.")

body = [f'<div class="note-box"><b>Editor\'s Note.</b> {editor}</div>']

body.append("<h2>New &amp; Notable</h2>")
for cat in CATEGORY_ORDER:
    items = sorted([t for t in tools if t["category"] == cat], key=lambda t: -t["combined"])
    if not items:
        continue
    body.append(f"<h3>{cat}</h3>")
    body += [card(t) for t in items]

body.append("<h2>This Run — Quick Reference</h2>")
rows = "".join(
    f"<tr><td><a href='{t['url']}' target='_blank'>{t['name']}</a></td><td>{t['category']}</td>"
    f"<td>{t['ease']}</td><td>{t['quality']}</td><td>{t['relevance']}</td>"
    f"<td class='cb'>{t['combined']}</td></tr>"
    for t in by_combined)
body.append("<table><tr><th>Tool</th><th>Category</th><th>Ease</th><th>Qual</th><th>Rel</th><th>Combined</th></tr>"
            + rows + "</table>")

body.append("<h2>All-Time Leaderboard (Top 12)</h2>")
lb = "".join(
    f"<tr><td>{i+1}</td><td><a href='{t['url']}' target='_blank'>{t['name']}</a></td>"
    f"<td>{t['category']}</td><td class='cb'>{t['combined']}</td><td>{t['first_seen']}</td></tr>"
    for i, t in enumerate(by_combined[:12]))
body.append("<table><tr><th>#</th><th>Tool</th><th>Category</th><th>Combined</th><th>First seen</th></tr>"
            + lb + "</table>")

report = page("Endo Tech Radar", f"New &amp; updated tools across the Endo stack &middot; {DATE_LONG}", "\n".join(body))
rpath = os.path.join(HERE, f"Endo_Tech_Radar_{DATE}.html")
with open(rpath, "w", encoding="utf-8") as f:
    f.write(report)

# ---------- MASTER INDEX ----------
mrows = "".join(
    f"<tr><td><a href='{t['url']}' target='_blank'>{t['name']}</a></td><td>{t['category']}</td>"
    f"<td>{t['version']}</td><td>{t['ease']}</td><td>{t['quality']}</td><td>{t['relevance']}</td>"
    f"<td class='cb'>{t['combined']}</td><td>{t['first_seen']}</td><td>{t['last_seen']}</td></tr>"
    for t in by_combined)
mtable = ("<table><tr><th>Tool</th><th>Category</th><th>Version</th><th>Ease</th><th>Qual</th>"
          "<th>Rel</th><th>Combined</th><th>First seen</th><th>Last seen</th></tr>" + mrows + "</table>")
master = page("Endo Tech Radar — Master Index",
              f"Every tool tracked, sorted by Combined score &middot; {len(tools)} tools &middot; updated {DATE_LONG}",
              mtable)
with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
    f.write(master)

print(f"Wrote {rpath}")
print(f"Wrote {os.path.join(HERE, 'index.html')}")
print(f"Tools: {len(tools)} | Top: {top['name']} ({top['combined']})")
