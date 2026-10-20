# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "requests",
#     "requests-cache",
#     "loguru",
# ]
# ///
"""
Fetch direct growth mutual fund details into data/<isin>.json, then build index.csv and index.html.
Falls back to basic mfapi.in details when Kuvera returns 404.
"""
import argparse
import csv
import json
import os.path
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
import webbrowser

import requests
import requests_cache
from loguru import logger

import fund_page

session = requests_cache.CachedSession('mf_cn_kuvera_cache', expire_after=86400, allowable_codes=(200, 404))


def log_response(response):
    cached = getattr(response, 'from_cache', False)
    logger.debug(
        f"{response.request.method} {response.url} -> {response.status_code} "
        f"{response.elapsed.total_seconds():.2f}s cached={cached} bytes={len(response.content)}"
    )

os.makedirs('data', exist_ok=True)


def mf_list():
    file = 'mf.json'
    if os.path.exists(file):
        with open(file, 'r') as f:
            data = json.load(f)
            print("Data loaded from mf.json")
            return data
    else:
        url = 'https://api.mfapi.in/mf'
        response = requests.get(url)
        log_response(response)
        if response.status_code == 200:
            data = response.json()
            with open('mf.json', 'w') as file:
                json.dump(data, file, indent=4)
            print("Data saved to data.json")
    return data


def is_direct_growth(fund):
    name = fund['schemeName'].lower()
    return bool(fund['isinGrowth']) and 'direct' in name and 'growth' in name


def get_mfapi_basic(isin, scheme_code):
    """Fallback when Kuvera has no data: basic details + latest NAV from mfapi.in."""
    response = session.get(f'https://api.mfapi.in/mf/{scheme_code}/latest')
    log_response(response)
    if response.status_code != 200 or response.json().get('status') != 'SUCCESS':
        logger.warning(f"No mfapi.in fallback for ISIN {isin}: HTTP {response.status_code}")
        return
    with open(f'data/{isin}.mfapi.json', 'w') as file:
        json.dump(response.json(), file, indent=4)
    logger.info(f"Used mfapi.in fallback for ISIN {isin}")


def get_mf_info(isin, scheme_code=None):
    if not isin:
        return

    url = 'https://mf.captnemo.in/kuvera/' + isin
    response = session.get(url)
    log_response(response)
    if not response.from_cache:
        delay = random.uniform(1, 3)
        logger.debug(f"sleeping {delay:.1f}s")
        time.sleep(delay)
    if not response.status_code == 200:
        logger.bind(not_found=response.status_code == 404).warning(
            f"Skipping ISIN {isin}: HTTP {response.status_code}"
        )
        if response.status_code == 404 and scheme_code:
            get_mfapi_basic(isin, scheme_code)
        return None

    data = response.json()
    if 'error' in data:
        print(f"Error in response for ISIN {isin}: {data['error']}")
        return None

    with open(f'data/{isin}.json', 'w') as file:
        json.dump(response.json(), file, indent=4)


CSV_COLUMNS = {
    'isin': 'ISIN',
    'name': 'Name', 'type': 'Type', 'category': 'Category',
    'aum': 'AUM (Cr)',
    'expense_ratio': 'TER', 'nav': 'NAV',
    'year_1': '1Y', 'year_3': '3Y', 'year_5': '5Y',
    'risk': 'Risk', 'rating': 'Rating', 'volatility': 'Volatility',
    'nav_date': 'NAV Date', 'inception': 'Since Inception',
    'start_date': 'Start Date', 'week_1': '1W',
    'fund_house': 'AMC',
    'plan': 'Plan',
}


def rnd(value, digits=2):
    if isinstance(value, (int, float)):
        return round(value, digits) if digits else int(round(value))
    return value


def split_amc(fund_name, name):
    amc = re.sub(r'\s*mutual fund$', '', fund_name, flags=re.I)
    # if name.lower().startswith(amc.lower()):
    #     name = name[len(amc):].lstrip(' -') or name
    return amc, name


def kuvera_row(info):
    returns = info.get('returns') or {}
    nav = info.get('nav') or {}
    amc, name = split_amc(info['fund_name'], info['name'])
    return {
        'url': f"https://mf.captnemo.in/kuvera/{info['ISIN']}",
        'info': info,
        'isin': info['ISIN'],
        'name': name,
        'fund_house': amc,
        'type': info['fund_type'],
        'category': info['fund_category'],
        'plan': info['plan'],
        'aum': rnd(info.get('aum'), 0),
        'expense_ratio': rnd(info.get('expense_ratio')),
        'nav': rnd(nav.get('nav')),
        'nav_date': nav.get('date'),
        'week_1': rnd(returns.get('week_1')),
        'year_1': rnd(returns.get('year_1')),
        'year_3': rnd(returns.get('year_3')),
        'year_5': rnd(returns.get('year_5')),
        'inception': rnd(returns.get('inception')),
        'volatility': info.get('volatility'),
        'risk': info.get('crisil_rating'),
        'rating': info.get('fund_rating'),
        'start_date': info.get('start_date'),
    }


def mfapi_row(info):
    meta = info['meta']
    latest = info['data'][0] if info.get('data') else {}
    amc, name = split_amc(meta['fund_house'], meta['scheme_name'])
    type_, _, category = meta['scheme_category'].partition(' - ')
    day, month, year = latest['date'].split('-') if latest else ('', '', '')
    return {
        'url': f"https://api.mfapi.in/mf/{meta['scheme_code']}/latest",
        'isin': meta['isin_growth'],
        'name': name,
        'fund_house': amc,
        'type': re.sub(r' Scheme$', '', type_),
        'category': category,
        'plan': 'GROWTH',
        'nav': rnd(float(latest['nav'])) if latest else None,
        'nav_date': f'{year}-{month}-{day}' if latest else None,
    }


def load_row(isin):
    file = f"data/{isin}.json"
    if os.path.exists(file):
        with open(file) as g:
            items = json.load(g)
        if items:
            return kuvera_row(items[0])
    file = f"data/{isin}.mfapi.json"
    if os.path.exists(file):
        with open(file) as g:
            return mfapi_row(json.load(g))


def write_csv(funds, path='index.csv'):
    rows = [row for row in (load_row(fund['isinGrowth']) for fund in funds) if row]
    write_rows(rows, path)
    logger.info(f"Wrote {len(rows)} funds to {path}")
    return rows


def write_rows(rows, path):
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(CSV_COLUMNS.values()))
        writer.writeheader()
        for row in rows:
            writer.writerow({CSV_COLUMNS[k]: row.get(k) for k in CSV_COLUMNS})


def write_fund_pages(rows, directory='isin'):
    shutil.rmtree(directory, ignore_errors=True)
    os.makedirs(directory)
    for row in rows:
        with open(f"{directory}/{row['isin']}.html", 'w') as f:
            f.write(fund_page.render(row))
    logger.info(f"Wrote {len(rows)} fund pages to {directory}/")


COLUMN_WIDTHS = {
    'NAV': 80, 'Name': 392,
    'Type': 120, 'Category': 165,
    'AMC': 150
}


def width_css():
    """Per-column widths by header name, so column order can change freely."""
    rules = []
    for index, header in enumerate(CSV_COLUMNS.values(), start=1):
        if header in COLUMN_WIDTHS:
            width = COLUMN_WIDTHS[header]
            rules.append(
                f'table.csvtotable-table th:nth-child({index}), table.csvtotable-table td:nth-child({index}) '
                f'{{ width: {width}px; min-width: {width}px; max-width: {width}px; white-space: normal; }}'
            )
    return '\n'.join(rules)


def build_html(rows, html_path='index.html'):
    """index.csv stays plain; the HTML table links each ISIN to its fund page."""
    write_fund_pages(rows)
    linked = [{**row, 'isin': f'<a href="isin/{row["isin"]}.html">{row["isin"]}</a>'} for row in rows]
    with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False) as tmp:
        write_rows(linked, tmp.name)
    with tempfile.NamedTemporaryFile('w', suffix='.css', delete=False) as css:
        css.write(open('custom.css').read() + '\n' + width_css())
    try:
        subprocess.run(
            ['uvx', 'csvtotable@3.2.0', '-o',
             '--description', '@about.md', '--css', css.name, '--js', 'site.js', tmp.name, html_path],
            check=True,
        )
    finally:
        os.remove(tmp.name)
        os.remove(css.name)
    logger.info(f"Built {html_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='store_true', help='log every API call')
    parser.add_argument('--no-open', action='store_true', help='do not open index.html in the browser')
    args = parser.parse_args()

    logger.remove()
    logger.add(sys.stderr, level='DEBUG' if args.verbose else 'INFO')
    logger.add('not_found.log', mode='w', format='{message}', filter=lambda r: r['extra'].get('not_found'))

    funds = [f for f in mf_list() if is_direct_growth(f)]
    logger.info(f"{len(funds)} direct growth funds")
    for index, fund in enumerate(funds):
        logger.info(f"Processing {index + 1}/{len(funds)}: {fund['schemeName']}")
        get_mf_info(fund['isinGrowth'], fund['schemeCode'])

    rows = write_csv(funds)
    build_html(rows)
    if not args.no_open:
        webbrowser.open(f'file://{os.path.abspath("index.html")}')
