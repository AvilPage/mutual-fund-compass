"""Render a static detail page for one fund row (see index.py)."""
from html import escape

SITE = 'Mutual Fund Compass'
GITHUB = 'https://github.com/AvilPage/mutual-fund-compass'

CSS = """
:root{color-scheme:light dark;--bg:#f7f7f5;--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#7a7974;
--line:#e4e3de;--accent:#256abf;--gain:#2a78d6;--loss:#e34948;--track:#f0efec}
@media (prefers-color-scheme:dark){:root{--bg:#121211;--surface:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--muted:#92918a;
--line:#2e2e2b;--accent:#6da7ec;--gain:#3987e5;--loss:#e66767;--track:#262624}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif;
-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.bar{background:var(--surface);border-bottom:1px solid var(--line)}
.bar div{max-width:960px;margin:0 auto;padding:12px 24px;display:flex;align-items:center;gap:24px}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;color:var(--ink)}
.brand:hover{text-decoration:none}
.brand img{width:28px;height:28px;border-radius:6px}
.bar nav{margin-left:auto;display:flex;gap:20px;font-size:.9rem}
.bar nav a{color:var(--ink2)}
main{max-width:960px;margin:0 auto;padding:28px 24px 32px}
.crumb{font-size:.85rem;color:var(--muted);margin-bottom:12px}
.crumb a{color:var(--muted)}
h1{margin:0 0 6px;font-size:1.75rem;line-height:1.25;letter-spacing:-.01em}
.amc{color:var(--ink2);margin:0 0 12px;font-size:1rem}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:24px}
.tag{border:1px solid var(--line);background:var(--surface);color:var(--ink2);border-radius:999px;padding:2px 12px;font-size:.8rem}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));background:var(--surface);
border:1px solid var(--line);border-radius:12px;margin-bottom:20px}
.stat{padding:16px 20px;border-right:1px solid var(--line)}
.stat:last-child{border-right:0}
.stat b{display:block;font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:600}
.stat span{display:block;font-size:1.35rem;font-weight:650;margin-top:2px;font-variant-numeric:tabular-nums}
.stat small{color:var(--muted);font-size:.8rem}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:20px 24px;margin-bottom:20px}
.panel h2{margin:0 0 16px;font-size:1rem;font-weight:650}
.rets{display:grid;gap:10px}
.ret{display:grid;grid-template-columns:150px 1fr 72px;align-items:center;gap:12px;font-size:.9rem}
.ret .lbl{color:var(--ink2)}
.ret .val{text-align:right;font-weight:600;font-variant-numeric:tabular-nums}
.track{position:relative;height:10px;background:var(--track);border-radius:5px}
.fill{position:absolute;top:0;height:10px}
.fill.pos{background:var(--gain);border-radius:0 4px 4px 0}
.fill.neg{background:var(--loss);border-radius:4px 0 0 4px}
.zero{position:absolute;top:-3px;bottom:-3px;width:1px;background:var(--muted)}
.note{color:var(--muted);font-size:.8rem;margin:14px 0 0}
dl{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:0 40px;margin:0}
dl div{display:flex;justify-content:space-between;gap:16px;padding:10px 0;border-bottom:1px solid var(--line)}
dt{color:var(--ink2)}dd{margin:0;text-align:right;font-weight:550}
.obj{margin:0;color:var(--ink2)}
footer{max-width:960px;margin:0 auto;padding:0 24px 40px;color:var(--muted);font-size:.8rem}
@media (max-width:600px){.ret{grid-template-columns:110px 1fr 64px}.stat{border-right:0;border-bottom:1px solid var(--line)}}
"""

RETURNS = [('week_1', '1 week'), ('year_1', '1 year'), ('year_3', '3 years'), ('year_5', '5 years'),
           ('inception', 'Since inception')]


def text(value, suffix='', prefix=''):
    if value is None or value == '':
        return None
    return f'{prefix}{escape(str(value))}{suffix}'


def money(value):
    return None if value is None else f'₹{value:,.0f}'


def stars(rating):
    if not rating:
        return None
    rating = int(rating)
    return f'<span aria-label="{rating} out of 5">{"★" * rating}{"☆" * (5 - rating)}</span>'


def stat(label, value, note=None):
    if not value:
        return ''
    note = f'<small>{escape(note)}</small>' if note else ''
    return f'<div class="stat"><b>{escape(label)}</b><span>{value}</span>{note}</div>'


def returns_panel(row):
    values = [(label, round(row[key], 2) + 0.0) for key, label in RETURNS if row.get(key) is not None]
    if not values:
        return ''
    low = min(0, min(v for _, v in values))
    high = max(0, max(v for _, v in values))
    span = (high - low) or 1
    zero = -low / span * 100
    rows = []
    for label, value in values:
        width = abs(value) / span * 100
        left, cls = (zero, 'pos') if value >= 0 else (zero - width, 'neg')
        rows.append(
            f'<div class="ret" title="{label}: {value:+.2f}%"><span class="lbl">{label}</span>'
            f'<div class="track"><div class="fill {cls}" style="left:{left:.2f}%;width:{width:.2f}%"></div>'
            f'<div class="zero" style="left:{zero:.2f}%"></div></div>'
            f'<span class="val">{value:+.2f}%</span></div>'
        )
    return (
        '<section class="panel"><h2>Returns</h2><div class="rets">' + ''.join(rows) + '</div>'
        '<p class="note">Periods over one year are annualised.</p></section>'
    )


def details_panel(row):
    info = row.get('info') or {}
    lock_in = info.get('lock_in_period')
    volatility = row.get('volatility')
    items = [
        ('AMC', text(row['fund_house'])),
        ('Plan', 'Direct · ' + escape(row['plan'].title()) if row.get('plan') else None),
        ('Fund type', text(row.get('type'))),
        ('Category', text(row.get('category'))),
        ('Structure', text(info.get('maturity_type'))),
        ('Launch date', text(row.get('start_date'))),
        ('Fund manager', text(info.get('fund_manager'))),
        ('Volatility', None if volatility is None else f'{volatility:.2f}'),
        ('Min lump sum', money(info.get('lump_min'))),
        ('Min additional', money(info.get('lump_min_additional'))),
        ('Min SIP', money(info.get('sip_min'))),
        ('Lock-in', None if lock_in is None else ('None' if not lock_in else f'{lock_in / 365:g} years')),
    ]
    rows = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in items if v)
    return f'<section class="panel"><h2>Fund details</h2><dl>{rows}</dl></section>'


def render(row):
    info = row.get('info') or {}
    title = f"{row['fund_house']} {row['name']}"
    aum = row.get('aum')
    stats = ''.join([
        stat('NAV', text(row.get('nav'), prefix='₹'), row.get('nav_date') and f"as of {row['nav_date']}"),
        stat('AUM', None if aum is None else f'₹{aum:,} Cr'),
        stat('Expense ratio', text(row.get('expense_ratio'), '%')),
        stat('Risk', text(row.get('risk'))),
        stat('Rating', stars(row.get('rating'))),
    ])
    tags = ''.join(f'<span class="tag">{escape(t)}</span>' for t in (row.get('type'), row.get('category')) if t)
    objective = info.get('investment_objective')
    objective = f'<section class="panel"><h2>Objective</h2><p class="obj">{escape(objective)}</p></section>' if objective else ''
    links = f'<a href="{escape(row["url"])}" rel="noopener">Source data</a>'
    if info.get('detail_info'):
        links += f' · <a href="{escape(info["detail_info"])}" rel="noopener">AMC website</a>'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | {SITE}</title>
<meta name="description" content="{escape(title)}: NAV, returns, AUM, expense ratio and fund details.">
<link rel="icon" href="../favicon.png">
<style>{CSS}</style></head>
<body>
<header class="bar"><div>
<a class="brand" href="../index.html"><img src="../favicon.png" alt="">{SITE}</a>
<nav><a href="../index.html">All funds</a><a href="{GITHUB}" rel="noopener">GitHub</a></nav>
</div></header>
<main>
<div class="crumb"><a href="../index.html">All funds</a> / {escape(row['isin'])}</div>
<h1>{escape(row['name'])}</h1>
<p class="amc">{escape(row['fund_house'])}</p>
<div class="tags">{tags}<span class="tag">{escape(row['isin'])}</span></div>
<div class="stats">{stats}</div>
{returns_panel(row)}
{details_panel(row)}
{objective}
<p class="note">{links}</p>
</main>
<footer>Data from Kuvera and mfapi.in. For information only, not investment advice.
Mutual fund investments are subject to market risks; past performance does not guarantee future returns.</footer>
</body></html>
"""
