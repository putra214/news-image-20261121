# The World in One Day — Saturday 21 November 2026

One image that sums up the world's news of Saturday 21 November 2026, for
make.fun's "Sum up 21 November's world news in one image" bounty.

## The image

A one-page newspaper front page, drawn entirely in code
(`generate_poster.py`, Python + Pillow): a masthead dated
**SATURDAY, 21 NOVEMBER 2026**, a strip of six big numbers from the day's
news (146 aboard safe, magnitude 6.7, 148 drones, $120bn climate fund,
109 bridge strikes, 11 killed), a lead story on the COP31 climate talks
running into overtime in Antalya — illustrated by a dotted world map with
numbered pins ("WHERE IT HAPPENED") matching the lead and grid stories —
six more main stories (the Sparta II drone attack in the Gulf of Finland,
the Russian missile strike on Kryvyi Rih, the Hormuz standoff, Bitcoin's
two-year low and rebound, Mexico's capture of cartel boss "El Chapo Isidro",
the M6.7 Peru quake), twenty-four briefs from across seven regions
(including the Iran strikes on Bahrain, the Basra power-station fire, the
CAF backing of Infantino in Abuja, the M6.8 East Timor quake, the EU–
Indonesia trade pact, and Verstappen's Las Vegas pole), and a DATE CHECK box
listing the big non-21-November stories that were deliberately left out.
Story kickers are coloured by region so the spread of the news is visible
at a glance.

Every event in the main sections happened, or was first reported, on
21 November 2026. Stories from other days are not in the main sections: the
DATE CHECK box lists nine of them with their real dates — Nvidia H200
(17 Nov), Wall Street sell-off (20 Nov), Poland missile (20 Nov), Zecler
verdict (20 Nov), Palisades verdict (20 Nov), ICJ Myanmar ruling (19 Nov),
Shenzhen declaration (19 Nov), Anthropic's $2tn debut (19 Nov), Voyager 1
(18 Nov) — so nothing is presented as the day's news that was not.

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
