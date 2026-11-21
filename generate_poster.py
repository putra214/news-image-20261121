"""Generate the news poster for 21 November 2026 (deterministic, PIL).

Run:  python3 generate_poster.py            -> writes entry.png (1024x1024)
The image is drawn entirely in code: flat vector-style art + real text, so
every letter stays sharp. No network, no randomness, no timestamps in the
output: the same script always writes the same bytes.

v4 (2026-11-22, fix session): replaces the v3 poster. See build-report.md.
v5 (2026-11-22, visual-fix session): adds a big-number strip under the
masthead, a much larger date line, a bolder DATE CHECK with ✕ per item, and
region-coloured kickers — visual fixes only, no news content changed.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (17, 17, 17)
GREY = (90, 88, 80)
RED = (176, 30, 30)
BLUE = (29, 78, 137)
TEAL = (14, 107, 92)
AMBER = (150, 80, 0)
PURPLE = (96, 52, 120)
GREEN = (43, 92, 60)
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
# Flat illustrations (all drawn with PIL primitives, no photos, no text).
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
    # thermometer, bottom right (climate is heating up)
    tx = x + w - 32
    d.rectangle([tx, y + h - 62, tx + 8, y + h - 22], outline=GREY, width=2, fill=LIGHT)
    d.rectangle([tx + 2, y + h - 44, tx + 6, y + h - 24], fill=RED)
    d.ellipse([tx - 3, y + h - 26, tx + 11, y + h - 12], outline=GREY, width=2, fill=RED)


def art_pin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(247, 226, 222))
    cx, cy = x + w // 2, y + h // 2 - 8
    d.polygon([(cx - 16, cy + 26), (cx + 16, cy + 26), (cx, cy + 52)], fill=RED)
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=RED)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=LIGHT)


def art_ship(d, x, y, w, h):
    """Sparta II: cargo ship on fire in the Gulf of Finland, drones above."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 234, 248))
    # two drones in the sky
    for dx, dy in ((x + 22, y + 16), (x + 78, y + 26)):
        d.ellipse([dx - 5, dy - 3, dx + 5, dy + 3], fill=(40, 40, 40))
        d.line([dx - 10, dy - 6, dx + 10, dy - 6], fill=(40, 40, 40), width=2)
        d.line([dx - 10, dy + 6, dx + 10, dy + 6], fill=(40, 40, 40), width=2)
    # sea
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(43, 110, 160))
    for wy in (y + h - 22, y + h - 12):
        for k in range(4):
            d.arc([x + k * 30 - 6, wy - 7, x + k * 30 + 24, wy + 7],
                  180, 360, fill=(214, 234, 248), width=2)
    # hull
    d.polygon([(x + 10, y + h - 52), (x + w - 10, y + h - 52),
               (x + w - 24, y + h - 30), (x + 24, y + h - 30)], fill=(31, 58, 95))
    # containers
    for i, col in enumerate([(176, 30, 30), (242, 160, 7), (14, 107, 92)]):
        d.rectangle([x + 20 + i * 26, y + h - 70, x + 42 + i * 26, y + h - 52],
                    fill=col)
    # bridge tower
    d.rectangle([x + w - 32, y + h - 78, x + w - 16, y + h - 52], fill=(70, 78, 88))
    # fire on deck + smoke
    cx, cy = x + w // 2, y + h - 66
    pts = []
    for i in range(10):
        ang = math.pi * i / 5
        rr = 16 if i % 2 == 0 else 7
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(242, 140, 20))
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 210, 90))
    for sx, sy, sr in ((cx - 8, cy - 22, 7), (cx + 4, cy - 34, 9), (cx - 2, cy - 48, 8)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 120))


def art_city(d, x, y, w, h):
    """Kryvyi Rih: dusk skyline, missile trail, impact burst on a rooftop."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 205, 160))
    d.ellipse([x + w - 34, y + 8, x + w - 10, y + 32], fill=(242, 160, 7))
    # missile trail from top right to the impact point
    ix, iy = x + 62, y + h - 58
    d.line([x + w - 8, y + 10, ix, iy], fill=(255, 120, 40), width=3)
    d.ellipse([x + w - 12, y + 6, x + w - 4, y + 14], fill=(255, 255, 255))
    # skyline with lit windows
    base = y + h
    for bx, bh in ((x + 4, 52), (x + 30, 74), (x + 58, 60), (x + 84, 44)):
        d.rectangle([bx, base - bh, bx + 24, base], fill=(52, 58, 72))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in (bx + 5, bx + 14):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90))
    # impact burst
    pts = []
    for i in range(12):
        ang = math.pi * i / 6
        rr = 18 if i % 2 == 0 else 8
        pts.append((ix + rr * math.cos(ang), iy + rr * math.sin(ang)))
    d.polygon(pts, fill=(242, 140, 20))
    d.ellipse([ix - 5, iy - 5, ix + 5, iy + 5], fill=(255, 210, 90))


def art_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    # faint gridlines
    for gy in (y + 30, y + 54, y + 78):
        d.line([x + 14, gy, x + w - 10, gy], fill=(225, 225, 225), width=1)
    d.line([x + 14, y + 12, x + 14, y + h - 14], fill=GREY, width=2)
    d.line([x + 14, y + h - 14, x + w - 10, y + h - 14], fill=GREY, width=2)
    # gold coin, top right
    ccx, ccy, cr = x + w - 28, y + 26, 15
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=(242, 160, 7),
              outline=(150, 100, 10), width=2)
    f_coin = font(SANS_B, 20)
    bw = d.textlength("B", font=f_coin)
    d.text((ccx - bw / 2, ccy - 11), "B", font=f_coin, fill=(120, 70, 0))
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
# Content — every event in the main sections verified to have happened, or
# first been reported, on Saturday 21 November 2026 (sources: Reuters, AP,
# One Turn, ESA/Nature, Interfax-Ukraine, Ukrinform, Wisden, UKMTO, Finwire).
# Overnight Fri->Sat events (Kryvyi Rih, Mexico capture, Peru quake) count
# because they were first reported on Saturday 21 Nov.
# Items from other days are NOT in the main sections: they are listed with
# their real dates in the DATE CHECK box.
# Dropped from v3 after verification: Haiti (operation 19 Nov), Ethiopia
# (statement 19 Nov), Sozcu TV (seizure 17 Nov), Sikh-plot sentence (20 Nov),
# Zecler verdict (20 Nov), Palisades verdict (20 Nov), Mlambo-Ngcuka death
# (20 Nov), WHO Ebola update (20 Nov), Trump/Iran-strikes report (18 Nov).
# ---------------------------------------------------------------------------

LEAD = {
    "kicker": "CLIMATE  •  ANTALYA, TURKEY",
    "color": TEAL,
    "headline": "COP31 talks run into overtime as fossil fuels vanish from the draft",
    "deck": ("Negotiators miss the Friday deadline in Antalya. The draft drops "
             "every mention of fossil fuels — and a $120bn fund for poorer nations. "
             "The EU warns: \u201ca good deal or no deal.\u201d"),
    "art": art_globe,
}

# Big-number strip under the masthead (v5). Every number already appears
# in the poster itself — verified against the stories/briefs below:
# 146 = Davao brief ("all 146 aboard safe"); 6.7 = Peru card (magnitude);
# 148 = Ukraine brief ("148 drones overnight"); $120BN = lead deck
# ("$120bn fund"); 109 = Kyiv brief ("bridges 109 times"); 11 = Mexico
# card ("11 are killed in the violence").
STATS = [
    ("146", "ABOARD, ALL SAFE"),
    ("6.7", "QUAKE MAGNITUDE"),
    ("148", "DRONES OVERNIGHT"),
    ("$120BN", "CLIMATE FUND"),
    ("109", "BRIDGE STRIKES"),
    ("11", "KILLED IN SINALOA"),
]

STORIES = [
    {"kicker": "BALTIC SEA  •  GULF OF FINLAND", "color": BLUE, "art": art_ship,
     "headline": "Drones strike Russian cargo ship Sparta II",
     "body": ("Two drones hit the ship bound for Kaliningrad; "
              "all 16 crew are rescued.")},
    {"kicker": "EUROPE  •  UKRAINE", "color": BLUE, "art": art_city,
     "headline": "Russian missile hits Zelenskyy\u2019s hometown",
     "body": ("A boy of 7 and a paramedic are killed; "
              "60 are wounded in Kryvyi Rih.")},
    {"kicker": "MIDDLE EAST  •  STRAIT OF HORMUZ", "color": AMBER, "art": art_tanker,
     "headline": "Iran says it downed a US drone over Hormuz",
     "body": ("Tehran claims a US MQ-9 downed as two tankers are hit. "
              "The US has not confirmed it.")},
    {"kicker": "MARKETS  •  CRYPTO", "color": PURPLE, "art": art_chart,
     "headline": "Bitcoin hits a two-year low, then rebounds",
     "body": ("Bitcoin falls to about $55,000, its lowest since 2024, "
              "then climbs back above $60,000.")},
    {"kicker": "AMERICAS  •  SINALOA, MEXICO", "color": RED, "art": art_pin,
     "headline": "Mexico captures \u201cEl Chapo Isidro\u201d",
     "body": ("FBI most-wanted Fausto Isidro Meza Flores is seized; "
              "11 are killed in the violence.")},
    {"kicker": "SOUTH AMERICA  •  PERU", "color": GREEN, "art": art_quake,
     "headline": "Magnitude 6.7 quake shakes Peru\u2019s Andes",
     "body": ("A strong tremor strikes the high Andes. No damage or "
              "casualties are reported.")},
]

BRIEFS_LEFT = [
    ("DAVAO", "Air Niugini jet lands safely; all 146 aboard safe.", TEAL),
    ("MERCURY", "BepiColombo enters orbit after an 8-year trip.", PURPLE),
    ("WELLINGTON", "Rahul\u2019s 136 puts India 118 ahead of New Zealand.", BLUE),
    ("KYIV", "Zelenskyy: Russia hit our bridges 109 times.", BLUE),
    ("WARSAW", "Rutte: NATO will defend every inch of Poland.", BLUE),
    ("LUHANSK", "Ukraine hits depot, command posts and bridge.", BLUE),
    ("RIYADH", "Houthis fire missiles at Riyadh and Jizan.", AMBER),
    ("GENEVA", "UN talks on AI weapons end with no binding rules.", BLUE),
    ("BRAZIL", "Wolbachia mosquitoes cut dengue 69% in children.", GREEN),
]
BRIEFS_RIGHT = [
    ("UNITED KINGDOM", "Catherine on life after cancer in film \u201cHeal\u201d.", BLUE),
    ("SINALOA", "11 killed in violence after cartel boss\u2019s capture.", RED),
    ("LONDON", "England beat New Zealand 37\u201312, a record margin.", BLUE),
    ("TUSCANY", "Ex-police chief De Gennaro found dead amid mafia probe.", BLUE),
    ("HELSINKI", "Finland limits air and sea traffic in the eastern Gulf.", BLUE),
    ("BRUSSELS", "NATO to meet Monday over Poland airspace breach.", BLUE),
    ("QESHM", "Iran claims a second US drone downed over the Gulf.", AMBER),
    ("ANTALYA", "100 groups call COP31 \u201cone of the most disappointing\u201d.", TEAL),
    ("UKRAINE", "Russia fired 3 missiles and 148 drones overnight.", BLUE),
]

DATE_CHECK_TITLE = "DATE CHECK \u2014 WHAT WE LEFT OUT:"
DATE_CHECK_ITEMS = [
    "Nvidia H200 (17 Nov)",
    "Wall Street sell-off (20 Nov)",
    "Poland missile (20 Nov)",
    "Zecler verdict (20 Nov)",
    "Palisades verdict (20 Nov)",
    "ICJ Myanmar ruling (19 Nov)",
    "Shenzhen declaration (19 Nov)",
    "Anthropic $2tn debut (19 Nov)",
    "Voyager 1 (18 Nov)",
]


def balance_date_check(d, items, fnt, max_w):
    """Split the 9 DATE CHECK items into 2 lines, balanced by measured width."""
    sep = "  \u00b7  "
    lines, widths = [[], []], [0, 0]
    for item in items:
        text = "\u2715 " + item
        w = d.textlength(text, font=fnt)
        li = 0 if widths[0] <= widths[1] else 1
        widths[li] += w + (d.textlength(sep, font=fnt) if lines[li] else 0)
        lines[li].append(text)
    return [sep.join(line) for line in lines]


def draw_stats(d, x, y, w, h):
    """Big-number strip: 6 numbers, each with a short label (v5)."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 235, 228))
    d.line([x, y, x + w, y], fill=RED, width=2)
    d.line([x, y + h, x + w, y + h], fill=RED, width=2)
    cell = w / len(STATS)
    f_num = font(SANS_B, 30)
    f_lab = font(SANS_B, 10)
    for i, (num, lab) in enumerate(STATS):
        cx = x + cell * i + cell / 2
        nw = d.textlength(num, font=f_num)
        d.text((cx - nw / 2, y + 4), num, font=f_num, fill=RED)
        lw = d.textlength(lab, font=f_lab)
        d.text((cx - lw / 2, y + h - 14), lab, font=f_lab, fill=INK)
        if i:
            sx = x + cell * i
            d.line([sx, y + 6, sx, y + h - 6], fill=RULE, width=1)


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
    d.text((tx, yy), story["kicker"], font=f_kick, fill=story["color"])
    yy += 20
    yy = text_block(d, tx, yy, wrap(d, story["headline"], f_head, tw),
                    f_head, leading=22)
    yy += 2
    text_block(d, tx, yy, wrap(d, story["body"], f_body, tw),
               f_body, leading=17)


def draw_briefs(d, x, y, w, items, f_bold, f_reg, leading=14, gap=2):
    yy = y
    for place, text, color in items:
        lead = place + " \u2014 "
        lw = d.textlength(lead, font=f_bold)
        d.text((x, yy), lead, font=f_bold, fill=color)
        rest = wrap(d, text, f_reg, w - lw)
        xx = x + lw
        for i, line in enumerate(rest):
            d.text((xx if i == 0 else x, yy), line, font=f_reg, fill=INK)
            yy += leading
        yy += gap
    return yy


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # double border
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)
    d.rectangle([16, 16, W - 17, H - 17], outline=RULE, width=1)

    # masthead
    f_mast = font(SERIF_B, 52)
    centered(d, W // 2, 18, "THE WORLD IN ONE DAY", f_mast)
    d.line([40, 78, W - 40, 78], fill=INK, width=2)
    # the day itself, big and red (v5) — no longer hidden in a black bar
    f_date = font(SERIF_B, 34)
    centered(d, W // 2, 84, "SATURDAY, 21 NOVEMBER 2026", f_date, fill=RED)
    f_sub = font(SANS_B, 13)
    centered(d, W // 2, 128, "ONE DAY  \u2022  SIX REGIONS  \u2022  THE WORLD\u2019S NEWS IN ONE IMAGE",
             f_sub, fill=GREY)

    # big-number strip (v5)
    draw_stats(d, 40, 150, W - 80, 50)

    # lead story
    y0 = 208
    d.line([40, y0, W - 40, y0], fill=RULE, width=1)
    lx, lw = 40, 600
    f_kick = font(SANS_B, 15)
    f_head = font(SANS_B, 30)
    f_deck = font(SANS, 14)
    yy = y0 + 10
    d.text((lx, yy), LEAD["kicker"], font=f_kick, fill=LEAD["color"])
    yy += 24
    yy = text_block(d, lx, yy, wrap(d, LEAD["headline"], f_head, lw), f_head, leading=33)
    yy += 4
    text_block(d, lx, yy, wrap(d, LEAD["deck"], f_deck, lw), f_deck, leading=18)
    # lead illustration, right
    LEAD["art"](d, W - 40 - 300, y0 + 10, 300, 140)
    d.rectangle([W - 40 - 300, y0 + 10, W - 40, y0 + 150], outline=RULE, width=1)

    # story grid 2 x 3
    gy = 372
    gw, gh, gap = 464, 122, 6
    gx0 = 40
    for i, story in enumerate(STORIES):
        cx = gx0 + (i % 2) * (gw + gap)
        cy = gy + (i // 2) * (gh + gap)
        draw_card(d, cx, cy, gw, gh, story)
    grid_bottom = gy + 3 * gh + 2 * gap

    # DATE CHECK box (v5: bolder title, ✕ per item)
    by = grid_bottom + 8
    d.rectangle([40, by, W - 40, by + 56], outline=RED, width=2)
    f_dc_title = font(SANS_B, 13)
    f_dc = font(SANS, 12)
    d.text((52, by + 6), DATE_CHECK_TITLE, font=f_dc_title, fill=RED)
    dc_lines = balance_date_check(d, DATE_CHECK_ITEMS, f_dc, W - 40 - 52)
    d.text((52, by + 24), dc_lines[0], font=f_dc, fill=INK)
    d.text((52, by + 40), dc_lines[1], font=f_dc, fill=INK)

    # briefs
    hy = by + 56 + 12
    d.line([40, hy, W - 40, hy], fill=INK, width=2)
    f_sec = font(SANS_B, 15)
    d.text((40, hy + 6), "MORE FROM 21 NOVEMBER", font=f_sec, fill=INK)
    f_bold = font(SANS_B, 12)
    f_reg = font(SANS, 12)
    col_w = 464
    end_l = draw_briefs(d, 40, hy + 28, col_w, BRIEFS_LEFT, f_bold, f_reg,
                        leading=13, gap=1)
    end_r = draw_briefs(d, 40 + col_w + 16, hy + 28, col_w, BRIEFS_RIGHT, f_bold, f_reg,
                        leading=13, gap=1)
    briefs_bottom = max(end_l, end_r)

    # footer
    f_foot = font(SANS, 11)
    centered(d, W // 2, H - 40,
             "Events happened or were first reported on 21 November 2026, unless dated otherwise.",
             f_foot, fill=GREY)
    return img


def main():
    img = build()
    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
