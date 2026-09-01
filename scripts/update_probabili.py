#!/usr/bin/env python3
"""Aggiorna le probabili formazioni dentro index.html.

Scarica https://www.fantacalcio.it/probabili-formazioni-serie-a, ne estrae per
ogni squadra il modulo, gli undici probabili e le riserve con la percentuale di
titolarita', e riscrive la riga `let PROBABILI = ...;` di index.html.

I giocatori sono agganciati al listone tramite l'Id fantacalcio.it, che e' lo
stesso usato nel file delle quotazioni: nessun match per nome.

Uso:
    python scripts/update_probabili.py            # aggiorna index.html
    python scripts/update_probabili.py --dry-run  # stampa e basta

Nessuna dipendenza esterna: solo standard library.
"""
import argparse
import html as htmllib
import json
import pathlib
import re
import sys
import urllib.request
from datetime import date

URL = 'https://www.fantacalcio.it/probabili-formazioni-serie-a'
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
HTML = pathlib.Path(__file__).resolve().parent.parent / 'index.html'

RE_GIORNATA = re.compile(r'-\s*(\d+)\s*&#xB0;\s*giornata', re.I)
RE_MATCH_DATE = re.compile(r'<div class="match-date">([^<]+)</div>')
RE_TEAM = re.compile(
    r'<h3 class="h6 team-name">([^<]+)</h3>\s*'
    r'<div class="h6 team-formation">([^<]*)</div>'
    r'(.*?)(?=<h3 class="h6 team-name">|\Z)', re.S)
RE_LIST = re.compile(r'<ul class="player-list (starters|reserves)">(.*?)</ul>', re.S)
RE_ITEM = re.compile(r'<li class="player-item pill" data-status="([^"]+)">(.*?)</li>', re.S)
RE_ROLE = re.compile(r'<span class="role" data-value="(\w)"')
RE_ID = re.compile(r'/(\d+)"[^>]*>')
RE_NAME = re.compile(r'<span>([^<]+)</span>')
RE_PCT = re.compile(r'aria-valuenow="(\d+)"')


def fetch(url=URL):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode('utf-8', 'replace')


def parse(html):
    teams = []
    for name, formation, body in RE_TEAM.findall(html):
        players = []
        for kind, chunk in RE_LIST.findall(body):
            for status, inner in RE_ITEM.findall(chunk):
                pid = RE_ID.search(inner)
                nome = RE_NAME.search(inner)
                if not pid or not nome:
                    continue
                role = RE_ROLE.search(inner)
                pct = RE_PCT.search(inner)
                players.append({
                    'Id': int(pid.group(1)),
                    'Nome': htmllib.unescape(nome.group(1)).strip(),
                    'R': role.group(1).upper() if role else '',
                    'pct': int(pct.group(1)) if pct else 0,
                    'titolare': kind == 'starters',
                    'ballottaggio': status == 'warn',
                })
        if players:
            teams.append({'team': htmllib.unescape(name).strip(),
                          'formation': formation.strip(),
                          'players': players})

    giornata = RE_GIORNATA.search(html)
    dates = RE_MATCH_DATE.findall(html)
    matches = []
    for i in range(0, len(teams) - 1, 2):
        matches.append({
            'home': teams[i]['team'],
            'away': teams[i + 1]['team'],
            'when': htmllib.unescape(dates[i // 2]).strip() if i // 2 < len(dates) else '',
        })

    return {
        'giornata': int(giornata.group(1)) if giornata else None,
        'aggiornato': date.today().isoformat(),
        'fonte': URL,
        'matches': matches,
        'teams': {t['team']: {'formation': t['formation'], 'players': t['players']}
                  for t in teams},
    }


def check_ids(data, html_text):
    """Quante voci si agganciano al listone via Id."""
    m = re.search(r'let FANTA_DATA = (\{"players".*?\}\};)', html_text, re.S)
    if not m:
        return None
    known = {p['Id'] for p in json.loads(m.group(1)[:-1])['players']}
    entries = [p for t in data['teams'].values() for p in t['players']]
    missing = [p for p in entries if p['Id'] not in known]
    return len(entries), missing


def inject(data, html_text):
    blob = 'let PROBABILI = ' + json.dumps(data, ensure_ascii=False) + ';'
    if re.search(r'^let PROBABILI = .*?;$', html_text, re.M | re.S):
        return re.sub(r'^let PROBABILI = .*?;$', lambda _: blob, html_text,
                      count=1, flags=re.M | re.S)
    # prima installazione: subito dopo il dataset dei giocatori
    anchor = re.search(r'^const LS_LISTONE_KEY = .*?;$', html_text, re.M)
    if not anchor:
        sys.exit('Non trovo il punto di inserimento in index.html.')
    return html_text[:anchor.end()] + '\n' + blob + html_text[anchor.end():]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true',
                    help='mostra cosa verrebbe scritto senza toccare index.html')
    args = ap.parse_args()

    print(f'Scarico {URL} ...')
    data = parse(fetch())
    if not data['teams']:
        sys.exit('Nessuna squadra trovata: il markup del sito e\' cambiato.')

    entries = sum(len(t['players']) for t in data['teams'].values())
    print(f"Giornata {data['giornata']} — {len(data['teams'])} squadre, "
          f"{len(data['matches'])} partite, {entries} voci giocatore")

    html_text = HTML.read_text(encoding='utf-8')
    stats = check_ids(data, html_text)
    if stats:
        total, missing = stats
        print(f'Agganciati al listone: {total - len(missing)}/{total}')
        for p in missing:
            print(f"  non nel listone: {p['Nome']} (Id {p['Id']})")

    if args.dry_run:
        for m in data['matches']:
            print(f"  {m['home']} - {m['away']}  ({m['when']})")
        return

    HTML.write_text(inject(data, html_text), encoding='utf-8')
    print(f'index.html aggiornato.')


if __name__ == '__main__':
    main()
