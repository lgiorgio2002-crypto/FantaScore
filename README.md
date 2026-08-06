# FantaScore

A single-file, client-side auction assistant for **Fantacalcio** (Italian fantasy football), built for Serie A 2026/27. Search the full player list, build your squad, and get a live squad-strength score plus a dynamic max-bid suggestion for every player — all running in the browser with no backend.

**[Live demo](#)** · Open `index.html` locally, or host it on GitHub Pages.

## What it does

- **Player scoring model**: combines a recency-weighted fantasy average across the last 4 Serie A seasons, a reliability factor based on actual playing time (not just rating), and bonuses for confirmed penalty-takers and free-kick specialists.
- **New-arrival handling**: players with no Serie A history (foreign transfers) are flagged and assigned the role-average score instead of a distorted stat.
- **Squad score, 0–100**: your squad's strength per position group and overall, normalized against the best theoretically achievable squad under the same role constraints.
- **Dynamic max-bid calculator**: recalculates a suggested maximum bid for every remaining player after each pick, based on remaining budget and remaining roster slots — so the suggestion tightens as money runs low, or loosens if you're under budget, and always leaves at least 1 credit for every other open slot.
- **Full searchable player list** (490 players), filterable by role, sortable by score.

## Why

Built to use live during a fantasy football auction draft — a second-screen tool a friend group actually used to prep for and run their 2026/27 season auction.

## Tech

Plain HTML/CSS/JS, no build step, no dependencies beyond a webfont icon CDN. All player data is embedded as a static JSON blob generated from public Serie A quotation and statistics spreadsheets.

## Data sources

- Official Fantacalcio Serie A 2026/27 player quotations
- 4 seasons of Serie A performance stats (2022/23 through 2025/26)
- Penalty-taker and free-kick-taker hierarchies per team

## Disclaimer

Personal project, not affiliated with Lega Serie A, Fantacalcio.it, or any official product. Player names and team data reflect the 2026/27 Serie A season.

## License

MIT
