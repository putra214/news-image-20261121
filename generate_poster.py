"""Generate the news poster for 21 November 2026 (deterministic, PIL).

Run:  python3 generate_poster.py            -> writes entry.png (1024x1024)
The image is drawn entirely in code: flat vector-style art + real text, so
every letter stays sharp. No network, no randomness, no timestamps in the
output: the same script always writes the same bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (17, 17, 17)
GREY = (90, 88, 80)
RED = (176, 30, 30)
BLUE = (29, 78, 137)
TEAL = (14, 107, 92)
LIGHT = (255, 255, 255)
RULE = (150, 146, 134)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = os.path.join(FONT_DIR, "dejavu", "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "dejavu", "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "dejavu", "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines; returns y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.22)


# ---------------------------------------------------------------------------
# Flat illustrations (all drawn with PIL primitives, no photos, no text
# except the short "H200" label on the chip).
# ---------------------------------------------------------------------------

def art_globe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 236, 247))
    d.ellipse([x + w - 52, y + 8, x + w - 12, y + 48], fill=(242, 160, 7))
    cx, cy, r = x + w // 2 - 10, y + h // 2 + 8, 62
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(126, 178, 107))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(43, 92, 60), width=3)
    # longitude / latitude lines
    d.arc([cx - 26, cy - r, cx + 26, cy + r], 270, 90, fill=(43, 92, 60), width=2)
    d.arc([cx - 26, cy - r, cx + 26, cy + r], 90, 270, fill=(43, 92, 60), width=2)
    d.arc([cx - r, cy - 26, cx + r, cy + 26], 180, 360, fill=(43, 92, 60), width=2)
    d.arc([cx - r, cy - 26, cx + r, cy + 26], 0, 180, fill=(43, 92, 60), width=2)
    # land blobs
    d.ellipse([cx - 44, cy - 38, cx - 6, cy - 2], fill=(52, 110, 71))
    d.ellipse([cx + 2, cy + 6, cx + 44, cy + 40], fill=(52, 110, 71))
    d.ellipse([cx - 10, cy - 52, cx + 26, cy - 24], fill=(52, 110, 71))


def art_pin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(247, 226, 222))
    cx, cy = x + w // 2, y + h // 2 - 8
    d.polygon([(cx - 16, cy + 26), (cx + 16, cy + 26), (cx, cy + 52)], fill=RED)
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=RED)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=LIGHT)


def art_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 244))
    # deck and towers
    d.rectangle([x + 8, y + h - 34, x + w - 8, y + h - 26], fill=(70, 78, 88))
    for tx in (x + 26, x + w - 40):
        d.rectangle([tx, y + 22, tx + 12, y + h - 26], fill=(70, 78, 88))
    d.line([x + 32, y + 28, x + w // 2, y + h - 30], fill=(120, 128, 138), width=2)
    d.line([x + w - 32, y + 28, x + w // 2, y + h - 30], fill=(120, 128, 138), width=2)
    # explosion burst on the deck
    cx, cy = x + w // 2, y + h - 52
    pts = []
    import math
    for i in range(12):
        ang = math.pi * i / 6
        rr = 30 if i % 2 == 0 else 13
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(242, 140, 20))
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 210, 90))


def art_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.line([x + 14, y + 12, x + 14, y + h - 14], fill=GREY, width=2)
    d.line([x + 14, y + h - 14, x + w - 10, y + h - 14], fill=GREY, width=2)
    pts = [(x + 18, y + 22), (x + 42, y + 34), (x + 62, y + 30),
           (x + 82, y + 52), (x + 100, y + 66), (x + w - 16, y + h - 24)]
    d.line(pts, fill=RED, width=4, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 2, ey - 12)], fill=RED)


def art_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 234, 248))
    # waves
    for wy in (y + h - 26, y + h - 14):
        for k in range(4):
            d.arc([x + k * 30 - 6, wy - 8, x + k * 30 + 24, wy + 8],
                  180, 360, fill=(43, 110, 160), width=2)
    # hull
    d.polygon([(x + 12, y + h - 46), (x + w - 12, y + h - 46),
               (x + w - 26, y + h - 26), (x + 26, y + h - 26)], fill=(31, 58, 95))
    # containers
    for i, col in enumerate([(176, 30, 30), (242, 160, 7), (14, 107, 92)]):
        d.rectangle([x + 22 + i * 26, y + h - 66, x + 44 + i * 26, y + h - 46],
                    fill=col)
    d.rectangle([x + w - 34, y + h - 72, x + w - 16, y + h - 46], fill=(70, 78, 88))
    d.line([x + w - 25, y + h - 84, x + w - 25, y + h - 72], fill=GREY, width=3)


def art_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(239, 239, 239))
    cx, cy = x + w // 2, y + h // 2
    for i in range(5):
        px = x + 18 + i * 18
        d.rectangle([px, y + 12, px + 8, y + 26], fill=(120, 120, 120))
        d.rectangle([px, y + h - 26, px + 8, y + h - 12], fill=(120, 120, 120))
    for i in range(4):
        py = y + 18 + i * 20
        d.rectangle([x + 12, py, x + 26, py + 8], fill=(120, 120, 120))
        d.rectangle([x + w - 26, py, x + w - 12, py + 8], fill=(120, 120, 120))
    d.rectangle([cx - 34, cy - 34, cx + 34, cy + 34], fill=(34, 34, 34))
    d.rectangle([cx - 20, cy - 20, cx + 20, cy + 20], outline=(200, 200, 200), width=2)
    f = font(SANS_B, 17)
    t = "H200"
    tw = d.textlength(t, font=f)
    d.text((cx - tw / 2, cy - 9), t, font=f, fill=(255, 255, 255))


def art_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(243, 232, 216))
    d.polygon([(x + 6, y + h - 20), (x + 42, y + 26), (x + 78, y + h - 20)],
              fill=(138, 109, 75))
    d.polygon([(x + 46, y + h - 20), (x + 84, y + 14), (x + w - 6, y + h - 20)],
              fill=(169, 138, 95))
    d.polygon([(x + 36, y + 32), (x + 42, y + 26), (x + 48, y + 32), (x + 42, y + 40)],
              fill=(255, 255, 255))
    pts = [(x + 8, y + h - 44), (x + 28, y + h - 44), (x + 38, y + h - 62),
           (x + 48, y + h - 30), (x + 58, y + h - 56), (x + 68, y + h - 44),
           (x + 88, y + h - 44), (x + 98, y + h - 60), (x + 108, y + h - 44)]
    d.line(pts, fill=RED, width=3, joint="curve")


# ---------------------------------------------------------------------------
# Content — every event verified to have happened, or first been reported,
# on Saturday 21 November 2026 (sources: Reuters, AP, One Turn, KIRO/AP).
# The two 19-20 Nov items are kept in a separate, honestly dated line.
# ---------------------------------------------------------------------------

LEAD = {
    "kicker": "CLIMATE  •  ANTALYA, TURKEY",
    "headline": "COP31 talks run into overtime as fossil fuels vanish from the draft",
    "deck": ("Negotiators miss the Friday deadline in Antalya. The draft drops "
             "every mention of fossil fuels — and a $120bn fund for poorer nations. "
             "The EU warns: \u201ca good deal or no deal.\u201d"),
    "art": art_globe,
}

STORIES = [
    {"kicker": "AMERICAS  •  SINALOA, MEXICO", "art": art_pin,
     "headline": "Mexico captures FBI most-wanted cartel boss \u201cEl Chapo Isidro\u201d",
     "body": ("Fausto Isidro Meza Flores is seized after a shoot-out. "
              "Eleven are killed as violence flares across the state.")},
    {"kicker": "EUROPE  •  UKRAINE", "art": art_bridge,
     "headline": "Russian missile hits Zelenskyy\u2019s hometown",
     "body": ("A ballistic missile strikes central Kryvyi Rih, killing 2 and "
              "wounding 60. Kyiv says 148 drones flew overnight.")},
    {"kicker": "MARKETS  •  NEW YORK & TOKYO", "art": art_chart,
     "headline": "AI sell-off rattles world markets",
     "body": ("The S&P 500 falls 3.7% and the Nikkei 5.1% as doubts grow "
              "over AI spending. The rout spreads across Asia and Europe.")},
    {"kicker": "MIDDLE EAST  •  STRAIT OF HORMUZ", "art": art_tanker,
     "headline": "Iran steps up tanker strikes as the Hormuz standoff deepens",
     "body": ("Attacks near the strait hit a monthly high. Tehran shows off "
              "new missile launchers while the US blockade holds.")},
    {"kicker": "ASIA  •  TECHNOLOGY", "art": art_chip,
     "headline": "Nvidia halts H200 chip exports to China",
     "body": ("The halt lands amid Washington\u2019s debate over advanced AI "
              "chips — and Beijing watches the curbs tighten.")},
    {"kicker": "SOUTH AMERICA  •  PERU", "art": art_quake,
     "headline": "Magnitude 6.7 quake shakes Peru\u2019s Andes",
     "body": ("A strong tremor strikes the high Andes. No damage or "
              "casualties are reported.")},
]

BRIEFS_LEFT = [
    ("POLAND", "Russian missile lands in Poland; NATO protests."),
    ("SAUDI ARABIA", "Houthis fire missiles at Riyadh."),
    ("GULF OF FINLAND", "Drones hit cargo ship Sparta II."),
    ("FRANCE", "Police sentenced over the racist beating of Michel Zecler."),
    ("UNITED STATES", "Man convicted over the deadly Palisades fire."),
    ("UNITED KINGDOM", "Princess Catherine on life after cancer."),
]
BRIEFS_RIGHT = [
    ("HAITI", "Heavy fighting as forces battle gangs for a key corridor."),
    ("ETHIOPIA", "700,000 people displaced in the south of the country."),
    ("TURKEY", "State takes control of S\u00f6zc\u00fc TV."),
    ("NEW YORK", "Indian man sentenced over a plot to kill a Sikh leader."),
    ("GENEVA", "UN talks agree to keep working on AI weapons rules."),
    ("BRAZIL", "Mosquitoes cut dengue cases by 69%."),
]

WEEK_LINE = ("ALSO THIS WEEK  —  19 NOV: Myanmar found guilty of Rohingya genocide "
             "•  20 NOV: Trump, Xi, Putin sign Shenzhen declaration "
             "•  19 NOV: Anthropic debuts at $2tn")


def draw_card(d, x, y, w, h, story):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    iw = 118
    story["art"](d, x + 1, y + 1, iw, h - 2)
    d.line([x + iw + 1, y, x + iw + 1, y + h], fill=RULE, width=1)
    tx = x + iw + 12
    tw = w - iw - 24
    f_kick = font(SANS_B, 12)
    f_head = font(SANS_B, 18)
    f_body = font(SANS, 13)
    yy = y + 10
    d.text((tx, yy), story["kicker"], font=f_kick, fill=RED)
    yy += 20
    yy = text_block(d, tx, yy, wrap(d, story["headline"], f_head, tw),
                    f_head, leading=22)
    yy += 2
    text_block(d, tx, yy, wrap(d, story["body"], f_body, tw),
               f_body, leading=17)


def draw_briefs(d, x, y, w, items, f_bold, f_reg):
    yy = y
    for place, text in items:
        lead = place + " — "
        lw = d.textlength(lead, font=f_bold)
        d.text((x, yy), lead, font=f_bold, fill=INK)
        rest = wrap(d, text, f_reg, w - lw)
        xx = x + lw
        for i, line in enumerate(rest):
            d.text((xx if i == 0 else x, yy), line, font=f_reg, fill=INK)
            yy += 16
        yy += 4
    return yy


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # double border
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)
    d.rectangle([16, 16, W - 17, H - 17], outline=RULE, width=1)

    # masthead
    f_mast = font(SERIF_B, 52)
    centered(d, W // 2, 26, "THE WORLD IN ONE DAY", f_mast)
    d.line([40, 96, W - 40, 96], fill=INK, width=2)
    f_date = font(SANS_B, 24)
    # black dateline bar
    d.rectangle([40, 102, W - 40, 134], fill=INK)
    tw = d.textlength("SATURDAY, 21 NOVEMBER 2026", font=f_date)
    d.text(((W - tw) / 2, 107), "SATURDAY, 21 NOVEMBER 2026", font=f_date, fill=LIGHT)
    f_sub = font(SANS_B, 13)
    centered(d, W // 2, 140, "ONE DAY  •  SEVEN REGIONS  •  THE WORLD\u2019S NEWS IN ONE IMAGE",
             f_sub, fill=GREY)

    # lead story
    y0 = 164
    d.line([40, y0, W - 40, y0], fill=RULE, width=1)
    lx, lw = 40, 600
    f_kick = font(SANS_B, 15)
    f_head = font(SANS_B, 30)
    f_deck = font(SANS, 15)
    yy = y0 + 10
    d.text((lx, yy), LEAD["kicker"], font=f_kick, fill=RED)
    yy += 24
    yy = text_block(d, lx, yy, wrap(d, LEAD["headline"], f_head, lw), f_head, leading=35)
    yy += 4
    text_block(d, lx, yy, wrap(d, LEAD["deck"], f_deck, lw), f_deck, leading=20)
    # lead illustration, right
    LEAD["art"](d, W - 40 - 300, y0 + 10, 300, 150)
    d.rectangle([W - 40 - 300, y0 + 10, W - 40, y0 + 160], outline=RULE, width=1)

    # story grid 2 x 3
    gy = 338
    gw, gh, gap = 464, 138, 10
    gx0 = 40
    for i, story in enumerate(STORIES):
        cx = gx0 + (i % 2) * (gw + gap)
        cy = gy + (i // 2) * (gh + gap)
        draw_card(d, cx, cy, gw, gh, story)
    grid_bottom = gy + 3 * gh + 2 * gap

    # briefs
    by = grid_bottom + 12
    d.line([40, by, W - 40, by], fill=INK, width=2)
    f_sec = font(SANS_B, 15)
    d.text((40, by + 8), "MORE FROM 21 NOVEMBER", font=f_sec, fill=INK)
    f_bold = font(SANS_B, 13)
    f_reg = font(SANS, 13)
    col_w = 464
    end_l = draw_briefs(d, 40, by + 32, col_w, BRIEFS_LEFT, f_bold, f_reg)
    end_r = draw_briefs(d, 40 + col_w + 16, by + 32, col_w, BRIEFS_RIGHT, f_bold, f_reg)
    briefs_bottom = max(end_l, end_r)

    # honestly dated week line
    wy = briefs_bottom + 6
    d.line([40, wy, W - 40, wy], fill=RULE, width=1)
    f_week = font(SANS, 11)
    text_block(d, 40, wy + 7, wrap(d, WEEK_LINE, f_week, W - 80), f_week, leading=15)

    # footer
    f_foot = font(SANS, 11)
    centered(d, W // 2, H - 44,
             "Events happened or were first reported on 21 November 2026, unless dated otherwise.",
             f_foot, fill=GREY)
    return img


def main():
    img = build()
    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
