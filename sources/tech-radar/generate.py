#!/usr/bin/env python3
"""Generate the Endo Founder Tech Radar run report + master index from index.json (founder schema)."""
import json, datetime, sys, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
DATE_LONG = datetime.datetime.strptime(DATE, "%Y-%m-%d").strftime("%B %d, %Y")

with open(os.path.join(HERE, "index.json"), encoding="utf-8") as f:
    items = json.load(f)

THEME_ORDER = [
    "Soil & agri sensing",
    "Soil carbon / MRV",
    "Electrochemical / soil sensors",
    "IoT device & fleet platforms",
    "Edge AI",
    "LoRa / connectivity",
    "Precision-ag peers",
    "Funding & M&A",
]

def e(x):
    return html.escape(str(x)) if x is not None else ""

CSS = """
:root{--bg:#f8f9fa;--card:#fff;--accent:#1d3557;--secondary:#457b9d;--highlight:#2a9d8f;--text:#1b1b1b;--muted:#6c757d;}
*{box-sizing:border-box;}
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--text);margin:0;line-height:1.55;}
.wrap{max-width:900px;margin:0 auto;padding:32px 20px 64px;}
header{border-bottom:3px solid var(--accent);padding-bottom:16px;margin-bottom:8px;}
h1{color:var(--accent);font-size:1.95rem;margin:0 0 6px;}
.sub{color:var(--muted);font-size:.95rem;}
h2{color:var(--accent);font-size:1.3rem;margin:36px 0 6px;border-left:5px solid var(--highlight);padding-left:10px;}
h3{color:var(--secondary);font-size:.85rem;margin:24px 0 10px;text-transform:uppercase;letter-spacing:.6px;}
.note-box{background:#eef4f3;border-left:4px solid var(--highlight);border-radius:8px;padding:16px 18px;margin:14px 0 8px;}
.narrative{background:#fff;border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,.06);padding:14px 16px;margin:10px 0;font-size:.92rem;}
ul.bv{margin:10px 0;padding-left:20px;}
ul.bv li{margin-bottom:8px;font-size:.92rem;}
.card{background:var(--card);border-radius:10px;box-shadow:0 1px 4px rgba(0,0,0,.08);padding:16px 18px;margin-bottom:14px;}
.card .top{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;flex-wrap:wrap;}
.card a.title{font-weight:600;color:var(--accent);text-decoration:none;font-size:1.08rem;}
.card a.title:hover{text-decoration:underline;}
.meta{color:var(--muted);font-size:.8rem;margin:3px 0 8px;}
.desc{font-size:.92rem;margin:8px 0;}
.line{font-size:.86rem;margin:5px 0;}
.line b{color:var(--accent);}
.take{font-size:.88rem;color:#173d36;background:#eef4f3;border-radius:6px;padding:8px 10px;margin-top:9px;}
.badges{display:flex;gap:6px;flex-shrink:0;}
.badge{display:flex;flex-direction:column;align-items:center;color:#fff;border-radius:8px;padding:4px 9px;min-width:54px;font-size:.62rem;line-height:1.25;text-align:center;}
.badge b{font-size:1.05rem;}
.tag{display:inline-block;border-radius:20px;padding:2px 9px;font-size:.66rem;font-weight:700;color:#fff;background:var(--highlight);margin-left:6px;vertical-align:middle;}
.tag.update{background:#e76f51;}
.type{display:inline-block;font-size:.68rem;color:var(--secondary);font-weight:600;text-transform:uppercase;letter-spacing:.4px;margin-left:4px;}
table{width:100%;border-collapse:collapse;background:var(--card);border-radius:10px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.08);margin-top:10px;}
th{background:var(--accent);color:#fff;text-align:left;padding:9px 11px;font-size:.8rem;}
td{padding:8px 11px;border-top:1px solid #eee;font-size:.85rem;vertical-align:top;}
tr:nth-child(even) td{background:#fafbfc;}
td a{color:var(--secondary);}
.cb{font-weight:700;color:var(--accent);}
.btn{display:inline-block;background:var(--highlight);color:#fff;border:none;border-radius:8px;padding:11px 22px;font-size:1rem;cursor:pointer;margin:22px 0 6px;}
.btn:hover{background:#21867a;}
@media print{.btn{display:none;}body{background:#fff;}.card,table,.narrative{box-shadow:none;}}
"""

def bcolor(v):
    return "#2a9d8f" if v >= 4 else ("#e9c46a" if v == 3 else "#adb5bd")

def badge(label, v):
    return (f'<div class="badge" style="background:{bcolor(v)}">'
            f'<span>{label}</span><b>{v}</b></div>')

def card(t):
    is_upd = str(t.get("status", "")).upper() == "UPDATE"
    tag = ('<span class="tag update">UPDATE</span>' if is_upd
           else '<span class="tag">NEW</span>')
    return f"""<div class="card">
  <div class="top">
    <div>
      <a class="title" href="{e(t['url'])}" target="_blank">{e(t['name'])}</a>{tag}
      <span class="type">{e(t['type'])}</span>
      <div class="meta">First seen {e(t['first_seen'])} &middot; last seen {e(t['last_seen'])}</div>
    </div>
    <div class="badges">{badge('Capability',t['capability'])}{badge('Ease',t['ease'])}{badge('Momentum',t['momentum'])}</div>
  </div>
  <div class="desc">{e(t['what_it_is'])}</div>
  <div class="line"><b>Backers &amp; Funding:</b> {e(t['backers'])} {e(t['funding'])}</div>
  <div class="line"><b>Traction:</b> {e(t['traction'])}</div>
  <div class="line"><b>Reviews:</b> {e(t['reviews'])}</div>
  <div class="line"><b>Pricing:</b> {e(t['pricing'])}</div>
  <div class="take"><b>Endo take:</b> {e(t['endo_take'])}</div>
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

# This run's items = first_seen == DATE OR status UPDATE refreshed this run (last_seen == DATE)
run_items = [t for t in items if t.get("last_seen") == DATE]
by_combined_run = sorted(run_items, key=lambda t: -t["combined"])
all_by_combined = sorted(items, key=lambda t: -t["combined"])

# ---------- RUN REPORT ----------
top = by_combined_run[0] if by_combined_run else all_by_combined[0]
n_new = len([t for t in run_items if str(t.get("status","")).upper() == "NEW"])
n_upd = len([t for t in run_items if str(t.get("status","")).upper() == "UPDATE"])

editor = (
    f"This run's most important development for Endo is <b>{e(top['name'])}</b> "
    f"(Combined {top['combined']}/15): {e(top['endo_take'])} "
    f"Across the run, India keeps surfacing on both sides of the ledger — "
    f"<b>Krishitantra's</b> rapid in-field soil lab as a direct low-cost peer, and "
    f"<b>AgroStar's</b> $30M from Just Climate (its first India bet) showing global climate capital "
    f"now chasing Indian climate-ag distribution at scale."
)

body = [f'<div class="note-box"><b>Editor\'s Note.</b> {editor}</div>']

body.append("<h2>Movers &amp; Money</h2>")
for theme in THEME_ORDER:
    its = sorted([t for t in run_items if t["theme"] == theme], key=lambda t: -t["combined"])
    if not its:
        continue
    body.append(f"<h3>{e(theme)}</h3>")
    body += [card(t) for t in its]
# any themes not in THEME_ORDER
for theme in sorted({t["theme"] for t in run_items} - set(THEME_ORDER)):
    its = sorted([t for t in run_items if t["theme"] == theme], key=lambda t: -t["combined"])
    body.append(f"<h3>{e(theme)}</h3>")
    body += [card(t) for t in its]

body.append("<h2>Funding &amp; Market Pulse</h2>")
pulse = (
    "Money this run is flowing to <b>connectivity and edge intelligence for off-grid sensing</b> and to "
    "<b>India climate-ag distribution</b>. BrainChip's $25M (Dec 2025) and the broader edge-AI surge "
    "(average late-2025/2026 rounds ~2x larger than 2023) are pushing always-on, ultra-low-power inference "
    "down to battery sensor nodes, while Lacuna Space and the satellite-LoRa wave are racing to blanket "
    "farmland with no cellular. On the India side, AgroStar's $30M from Just Climate (its first India "
    "investment) signals that global climate funds now see Indian agtech distribution as investable — even "
    "as deep-tech soil players like Krishitantra and soil-carbon MRV startups (Seqana) stay capital-light, "
    "underscoring that reach raises money faster than measurement hardware."
)
body.append(f'<div class="narrative">{pulse}</div>')

body.append("<h2>Build vs Buy</h2>")
body.append("""<ul class="bv">
<li><b>Buy / integrate the fleet-ops layer (Golioth).</b> Device management + OTA is a solved, cheap-to-start commodity now backed by Canonical/Ubuntu — Endo should buy here (Golioth, or Memfault/Blues) rather than build fleet observability in-house.</li>
<li><b>Pilot, don't depend on, satellite connectivity (Lacuna Space).</b> Standards-based LoRa direct-to-satellite is ideal for off-grid Indian fields and works with off-the-shelf LoRa hardware — pilot it as a fallback layer alongside Sateliot, but it's partner-mediated and store-and-forward today.</li>
<li><b>Watch edge AI by tier (BrainChip vs DEEPX).</b> For ultra-low-power always-on sensing, keep BrainChip's Akida on the radar (best perf-per-watt, niche toolchain); for standard on-device vision/anomaly AI today, DEEPX's cheap Pi-compatible NPUs remain the easier buy.</li>
<li><b>Partner on MRV software, supply the ground truth (Seqana/Boomitra/Varaha).</b> Endo should not build satellite SOC models; instead position its cheap in-field soil sensors as the ground-truth feed that de-risks satellite-only MRV — and use AgroStar/FPO channels (Krishitantra-style) for distribution rather than building reach from scratch.</li>
</ul>""")

body.append("<h2>This Run — Quick Table</h2>")
rows = "".join(
    f"<tr><td><a href='{e(t['url'])}' target='_blank'>{e(t['name'])}</a></td><td>{e(t['theme'])}</td>"
    f"<td>{t['capability']}</td><td>{t['ease']}</td><td>{t['momentum']}</td>"
    f"<td class='cb'>{t['combined']}</td>"
    f"<td><a href='{e(t['url'])}' target='_blank'>link</a></td></tr>"
    for t in by_combined_run)
body.append("<table><tr><th>Name</th><th>Theme</th><th>Capability</th><th>Ease</th>"
            "<th>Momentum</th><th>Combined</th><th>Link</th></tr>" + rows + "</table>")

body.append("<h2>All-Time Leaderboard (Top 12)</h2>")
lb = "".join(
    f"<tr><td>{i+1}</td><td><a href='{e(t['url'])}' target='_blank'>{e(t['name'])}</a></td>"
    f"<td>{e(t['theme'])}</td><td class='cb'>{t['combined']}</td>"
    f"<td>{e(t.get('funding','n/a'))}</td><td>{e(t['first_seen'])}</td></tr>"
    for i, t in enumerate(all_by_combined[:12]))
body.append("<table><tr><th>#</th><th>Name</th><th>Theme</th><th>Combined</th>"
            "<th>Funding</th><th>First seen</th></tr>" + lb + "</table>")

report = page("Endo Founder Tech Radar",
              f"Market &amp; tech intelligence for Endo Automation &middot; {DATE_LONG} "
              f"&middot; {n_new} new, {n_upd} updated", "\n".join(body))
rpath = os.path.join(HERE, f"Endo_Tech_Radar_{DATE}.html")
with open(rpath, "w", encoding="utf-8") as f:
    f.write(report)

# ---------- MASTER INDEX ----------
mrows = "".join(
    f"<tr><td><a href='{e(t['url'])}' target='_blank'>{e(t['name'])}</a></td><td>{e(t['theme'])}</td>"
    f"<td>{e(t.get('funding','n/a'))}</td><td>{t['capability']}</td><td>{t['ease']}</td>"
    f"<td>{t['momentum']}</td><td class='cb'>{t['combined']}</td><td>{e(t['first_seen'])}</td></tr>"
    for t in all_by_combined)
mtable = ("<table><tr><th>Name</th><th>Theme</th><th>Funding</th><th>Capability</th><th>Ease</th>"
          "<th>Momentum</th><th>Combined</th><th>First seen</th></tr>" + mrows + "</table>")
master = page("Endo Founder Tech Radar — Master Index",
              f"Every company / product tracked, sorted by Combined score &middot; "
              f"{len(items)} entries &middot; updated {DATE_LONG}", mtable)
with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
    f.write(master)

print(f"Wrote {rpath}")
print(f"Wrote {os.path.join(HERE, 'index.html')}")
print(f"Total entries: {len(items)} | This run: {len(run_items)} ({n_new} new, {n_upd} upd) "
      f"| Top: {top['name']} ({top['combined']})")
