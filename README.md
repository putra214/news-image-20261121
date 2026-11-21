# The World in One Day — Saturday 21 November 2026

One image that sums up the world's news of Saturday 21 November 2026, for
make.fun's "Sum up 21 November's world news in one image" bounty.

## The image

A one-page newspaper front page, drawn entirely in code
(`generate_poster.py`, Python + Pillow): a masthead dated
**SATURDAY, 21 NOVEMBER 2026**, a lead story on the COP31 climate talks
running into overtime in Antalya, six more main stories (Mexico's capture of
cartel boss "El Chapo Isidro", the Russian missile strike on Kryvyi Rih, the
AI stock sell-off, the Hormuz tanker standoff, Nvidia's H200 export halt, the
M6.7 Peru quake), twelve briefs from across seven regions, and a short
"Also this week" line.

Every event in the main sections happened, or was first reported, on
21 November 2026. The two earlier items in the "Also this week" line — the
ICJ's Myanmar genocide ruling (19 Nov) and the Shenzhen peace declaration
(20 Nov) — carry their real dates, so nothing is presented as the day's news
that was not.

## How it is built

- `generate_poster.py` draws `entry.png` (1024x1024, PNG) with flat
  vector-style art and real text, so every letter stays sharp.
- `main.py` (Python 3.13, standard library only) copies `entry.png` to the
  output directory. It runs with no network and writes the same bytes on
  every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# out/entry.png — 1024x1024 PNG, under 1 MiB
```
