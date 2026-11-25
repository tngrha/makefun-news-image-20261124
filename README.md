# The World in One Picture — Tuesday 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/tngrha/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image that sums up the world's news of Tuesday 24 November 2026: a serif
broadsheet front page with **53 verified stories across 7 regions and 20 fields**
— 3 heroes, 12 illustrated panels, 38 one-line briefs — plus a UTC timeline
strip, a world map with numbered pins, and a DATE CHECK box that names the
stories deliberately left out because they broke on an earlier day.

Every story here happened, or was first reported, on Tuesday 24 November 2026.
CLAIM = one side's account, not independently confirmed. Sources are named on
every panel; the full verified list is in `stories.md`.

## Files

- `entry.png` — the image (1024×1024, ≤1 MiB), drawn by `render.py`
- `render.py` — the original PIL + Noto Serif renderer that draws the page
- `main.py` — the entry program: copies `entry.png` to `/output/entry.png`
- `stories.md` — the 53 verified stories with sources, fields and regions

## Run it

```sh
python3 render.py   # redraw entry.png from stories.md data
python3 main.py     # copy entry.png to /output/entry.png
```

No network access is needed at run time; both runs write identical bytes.

## License

MIT — see `LICENSE`.
