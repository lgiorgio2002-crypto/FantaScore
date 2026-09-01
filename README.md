# FantaScore

A single-file, client-side auction assistant for **Fantacalcio** (Italian fantasy football), built for Serie A 2026/27. Search the full player list, build your squad, and get a live squad-strength score plus a dynamic max-bid suggestion for every player — all running in the browser with no backend.

**[Live demo](#)** · Open `index.html` locally, or host it on GitHub Pages.

## What it does

- **Player scoring model**: combines a recency-weighted fantasy average across the last 4 Serie A seasons, a reliability factor based on actual playing time (not just rating), and bonuses for confirmed penalty-takers and free-kick specialists.
- **New-arrival handling**: players with no Serie A history (foreign transfers) are flagged and assigned the role-average score instead of a distorted stat.
- **Squad score, 0–100**: your squad's strength per position group and overall, normalized against the best theoretically achievable squad under the same role constraints.
- **Dynamic max-bid calculator**: recalculates a suggested maximum bid for every remaining player after each pick, based on remaining budget and remaining roster slots — so the suggestion tightens as money runs low, or loosens if you're under budget, and always leaves at least 1 credit for every other open slot.
- **Full searchable player list** (536 players), filterable by role, sortable by score.
- **Listone import**: drag in the official quotations file (`.xlsx`/`.csv`) to refresh prices and squads. Known players keep their computed score; new arrivals are added automatically with the role average. Persists in `localStorage`.
- **Matchday hub**: once you lock in your squad, the probable lineups for the current giornata — filtered to *your* players and grouped into starters, ballottaggi and out-of-squad.
- **Lineup recommender**: proposes the best formation and XI for the week, scored 0–100. Each player is weighted by `score × start probability`, with a penalty for ballottaggi and a bonus for penalty-takers and set-piece specialists.

## Why

Built to use live during a fantasy football auction draft — a second-screen tool a friend group actually used to prep for and run their 2026/27 season auction — and then kept for weekly lineup calls.

## Tech

Plain HTML/CSS/JS in a single file, no build step. All player data is embedded as a static JSON blob generated from public Serie A quotation and statistics spreadsheets. SheetJS is loaded from a CDN only to parse `.xlsx` uploads; everything else works offline.

## Updating the probable lineups

Probable lineups change every matchday, and the page is static (the browser can't fetch them cross-origin). Refresh them before each giornata with:

```bash
python scripts/update_probabili.py            # scrape and rewrite index.html
python scripts/update_probabili.py --dry-run  # preview without writing
```

Standard library only, no dependencies. Players are matched to the listone by their fantacalcio.it Id — the same Id used in the quotations file — so no name matching is involved.

## Data sources

- Official Fantacalcio Serie A 2026/27 player quotations
- 4 seasons of Serie A performance stats (2022/23 through 2025/26)
- Penalty-taker and free-kick-taker hierarchies per team
- [Probabili formazioni Serie A](https://www.fantacalcio.it/probabili-formazioni-serie-a) (fantacalcio.it), refreshed per matchday

## Disclaimer

Personal project, not affiliated with Lega Serie A, Fantacalcio.it, or any official product. Player names and team data reflect the 2026/27 Serie A season.

## License

MIT
