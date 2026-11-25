#!/usr/bin/env python3
"""Render 'The World in One Picture — Tuesday 24 November 2026'.

Original code written in this session for make.fun news-image-20261124.
PIL + Noto Serif broadsheet: masthead, UTC timeline, 3 heroes, 12 panels,
world map with numbered pins, 38 briefs, DATE CHECK box, sources footer.
All 53 stories happened or were first reported on Tuesday 24 November 2026;
see stories.md for the verified list with sources.
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 22, 18)
RED = (176, 30, 36)
RED_DK = (140, 20, 26)
BLUE = (38, 74, 120)
GREEN = (46, 110, 58)
GREY = (110, 104, 92)
RULE = (60, 52, 44)
SKY = (214, 228, 236)
SAND = (232, 222, 200)
MAP_LAND = (226, 214, 186)
MAP_LINE = (140, 128, 100)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
DISPLAY_B = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- data
# (num, region, field, headline, dek, tag, tag_source, map_lon, map_lat, scene)
HEROES = [
    (1, "MIDDLE EAST · GAZA", "Israeli strikes kill Hamas security chief in Gaza",
     "Naeem Abu Nahel and six others die in Gaza City strikes; three more killed at a Khan Younis police post.",
     "CONFIRMED", "REUTERS", 34.5, 31.5, "strike"),
    (2, "EUROPE · UKRAINE WAR", "Russian night strike on Zaporizhzhia kills 2, wounds 40",
     "Overnight attack hits an apartment block; four children among the wounded, the governor says.",
     "CONFIRMED", "REUTERS", 35.2, 47.8, "city"),
    (3, "GLOBAL · MARKETS", "Nvidia falls 7% as Huang's return rally fades",
     "AI stocks slide a day after the board reinstated Jensen Huang; a chip index drops about 8%.",
     "CONFIRMED", "ONETURN", -74.0, 40.7, "chart"),
]

PANELS = [
    (4, "SPACE", "Three rockets fly in a single day",
     "Progress MS-36 lifts off 10:17 UTC; Ariane 64 carries Amazon Leo at 11:14; Falcon 9 flies USSF-266 at 16:08.",
     "CONFIRMED", "LAUNCH LIBRARY", 63.3, 45.9, "rockets"),
    (5, "ASIA · SPACE", "Pakistan astronaut to visit China's Tiangong",
     "Zeeshan Ali will be the first foreign visitor to the station, flying on Shenzhou 24.",
     "CONFIRMED", "NATURE", 100.3, 40.9, "station"),
    (6, "N. AMERICA · TECH LAW", "Oregon and Virginia sue SpaceX over Grok images",
     "States say the chatbot made child sexual abuse images and non-consensual pictures.",
     "CLAIM", "ANC", -77.5, 37.5, "gavel"),
    (7, "GLOBAL · PHARMA", "Sanofi to buy Insmed for $41bn",
     "Cash deal is the biggest drug deal since 2023; Insmed shares jump 14%.",
     "CONFIRMED", "ONETURN", 2.35, 48.85, "pill"),
    (8, "GLOBAL · CYBER", "CrowdStrike agrees $43.9bn Zscaler deal",
     "Cybersecurity merger announced Tuesday; CrowdStrike shares fall 4%.",
     "CONFIRMED", "MARKETPEDIA", -97.7, 30.3, "shield"),
    (9, "ASIA · MARKETS", "Seoul jumps 6%, Nikkei up 3.9%",
     "Asian stocks rebound after Huang's return; Korean shares lead the rally.",
     "CONFIRMED", "HORIZON", 127.0, 37.5, "market"),
    (10, "EUROPE · DEFENCE", "Germany first into Ukraine's Delta war system",
     "Berlin signs a letter of intent in the first access deal for the battlefield network.",
     "CONFIRMED", "KYIV INDEPENDENT", 13.4, 52.5, "flags"),
    (11, "ASIA · DEFENCE", "Russian jets enter South Korea's air zone",
     "Several aircraft flew inside the air defence zone over waters between Korea and Japan.",
     "CONFIRMED", "AP", 130.0, 38.0, "jets"),
    (12, "AFRICA · JUSTICE", "Amnesty: Tigray strikes may be war crimes",
     "Ethiopian forces hit crowded urban areas; rebels also endangered civilians, the group says.",
     "REPORTED", "AMNESTY", 39.5, 13.5, "mountains"),
    (13, "OCEANIA · CRICKET", "England blast Australia to level T20 series",
     "Donald hits 85, Salt 58, as England chase 184 in 13.1 overs to win by 8 wickets.",
     "CONFIRMED", "CRICINFO", 151.2, -33.9, "cricket"),
    (14, "ASIA · HEALTH", "Bangladesh reports nine suspected measles deaths",
     "Nine deaths in a day after a fatality-free day, health data show.",
     "REPORTED", "DAILY STAR", 90.4, 23.8, "virus"),
    (15, "EUROPE · TRADE", "EU to cap Chinese hybrid car imports",
     "Cap of 191,780 cars from 1 Dec to 18 June under provisional safeguards.",
     "CONFIRMED", "GUARDIAN", 4.35, 50.85, "car"),
]

BRIEFS_A = [
    (16, "US: Huckabee doubts Israel aid ends this year", "Reuters", "CONFIRMED"),
    (17, "US: FBI deputy Raia to retire by year-end", "NYT", "CONFIRMED"),
    (18, "US: Senate probes Vance role in Vitol oil deal", "Reuters", "CONFIRMED"),
    (19, "US: Court revives Trump hush-money transfer", "NYT", "CONFIRMED"),
    (20, "US: Paxton drops cases against two doctors", "AP", "CONFIRMED"),
    (21, "US: Pennsylvania measles claims ninth death", "Horizon", "REPORTED"),
    (22, "Mexico: 'El Chapo Isidro' to be tried at home", "Horizon", "REPORTED"),
    (23, "Colombia: Car bomb wrecks buildings in Villavicencio", "Hindu", "CONFIRMED"),
    (24, "Brazil: 2027 growth forecast cut to 1.8%", "OneTurn", "REPORTED"),
    (25, "Brazil: Grêmio beat Santos 2-0", "ScoreZaap", "REPORTED"),
    (26, "DRC: Fighting traps Ebola teams in Ituri", "UN News", "CONFIRMED"),
    (27, "Somalia, Uganda step up anti-Shabaab drive", "iqmia", "REPORTED"),
    (28, "Libya: Tripoli seeks answers from Kyiv", "Horizon", "REPORTED"),
    (29, "Iraq: Baghdad to run Kurdish-area oilfields", "Reuters", "CONFIRMED"),
    (30, "Iran: Singer Parastoo Ahmadi given 74 lashes", "Horizon", "REPORTED"),
    (31, "Iran: No talks until US meets seven terms", "Horizon", "CLAIM"),
    (32, "Yemen: Houthis say dozens killed in strikes", "Horizon", "CLAIM"),
    (33, "US: Citizen wrongly deported, filings say", "The Hill", "CONFIRMED"),
    (34, "US: Army to blow up Iowa explosives cache", "NYT", "CONFIRMED"),
]
BRIEFS_B = [
    (35, "Norway: Dialogue open with Ukraine: minister", "Reuters", "CONFIRMED"),
    (36, "Latvia: War may hit tipping point next year", "Reuters", "CONFIRMED"),
    (37, "Japan: Full 2027 ICC payment early: Takaichi", "Reuters", "CONFIRMED"),
    (38, "Bangladesh: Hasina plans 16 Dec return", "Reuters", "CONFIRMED"),
    (39, "S. Korea: $375,000 rewards for AI exam cheats", "WSJ", "CONFIRMED"),
    (40, "Nepal: 5.4 quake shakes Nepal, neighbours", "ANI", "CONFIRMED"),
    (41, "Indian Ocean: M6.4 quake; no tsunami threat", "USGS", "CONFIRMED"),
    (42, "Climate: Reuters asks what now after COP31 flop", "Reuters", "CONFIRMED"),
    (43, "ISS: Crew runs biomedical research in orbit", "NASA", "CONFIRMED"),
    (44, "Science: Trauma leaves scars in brain cells", "Nature", "CONFIRMED"),
    (45, "Science: Menopause may speed brain ageing", "Nature", "CONFIRMED"),
    (46, "Markets: German Ifo business mood steadies", "Newsquawk", "CONFIRMED"),
    (47, "Culture: ATEEZ score fourth No. 1 album", "Billboard", "CONFIRMED"),
    (48, "Culture: Final 'Avengers: Doomsday' trailer", "7 Lights", "REPORTED"),
    (49, "Sport: Arya's 181 powers Delhi win", "Cricinfo", "CONFIRMED"),
    (50, "Sport: Sooryavanshi smashes 204 off 53 balls", "SportzCraazy", "REPORTED"),
    (51, "Sport: Brentford beat Everton 4-0", "GalaxySports", "REPORTED"),
    (52, "Markets: Tesla, SpaceX weigh $3.5tn merger", "SuMarket", "REPORTED"),
    (53, "Markets: AI stocks slide after Monday's surge", "OneTurn", "REPORTED"),
]

TIMELINE = [
    ("01:32", "Nepal quake, 5.4"),
    ("08:20", "ISS crew's biomedical day"),
    ("10:17", "Progress MS-36 lifts off"),
    ("11:06", "M6.4 quake, Indian Ocean"),
    ("11:14", "Ariane 64 launches Amazon Leo"),
    ("16:08", "Falcon 9 flies USSF-266"),
    ("21:00", "Wall St closes; Nvidia down 7%"),
]

DATECHECK = [
    ("COP31 collapses in Antalya", "Sun 22 Nov"),
    ("FIFA names 2031 & 2035 Women's World Cup hosts", "Mon 23 Nov"),
    ("BepiColombo captured by Mercury", "Sat 21 Nov"),
    ("Nvidia reinstates Jensen Huang as CEO", "Mon 23 Nov"),
    ("14 nations back ICJ Rohingya genocide ruling", "Mon 23 Nov"),
    ("Trump says he will order faster federal executions", "Mon 23 Nov"),
    ("Peru Junín quake toll: 1 dead, 15 hurt", "Fri 20 Nov"),
    ("M6.5 quake near Vanuatu", "Mon 23 Nov"),
    ("Miley Cyrus marries Maxx Morando", "Sat 21 Nov"),
    ("Adelaide space-medicine test announced", "Mon 23 Nov"),
    ("Not yet: Shenzhou 24 crewed launch", "due Wed 25 Nov"),
    ("Not yet: Hasina's return to Dhaka", "due 16 Dec"),
]

# Coarse continent outlines (lon, lat), schematic equirectangular map.
CONTINENTS = [
    [(-168, 66), (-158, 58), (-152, 60), (-140, 60), (-130, 54), (-125, 49), (-124, 42),
     (-120, 34), (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-90, 14), (-83, 9),
     (-79, 9), (-82, 10), (-87, 13), (-92, 15), (-97, 16), (-97, 26), (-93, 30),
     (-89, 30), (-84, 30), (-81, 25), (-80, 32), (-76, 35), (-74, 40), (-70, 42),
     (-65, 44), (-60, 47), (-55, 52), (-60, 55), (-65, 60), (-78, 62), (-85, 66),
     (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68)],
    [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-22, 70), (-20, 74),
     (-25, 76), (-35, 77), (-50, 76), (-58, 74), (-60, 70)],
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23),
     (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54), (-66, -55), (-68, -50),
     (-65, -45), (-62, -41), (-58, -38), (-52, -33), (-48, -28), (-41, -23), (-39, -17),
     (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-53, 4), (-58, 6),
     (-62, 9), (-68, 11), (-72, 12), (-75, 10)],
    [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-5, 35), (0, 36), (10, 37), (11, 34),
     (20, 32), (30, 31), (32, 31), (34, 28), (37, 22), (39, 18), (43, 12), (48, 11),
     (51, 10), (46, 5), (42, 0), (40, -5), (40, -10), (36, -18), (33, -26), (28, -33),
     (20, -35), (17, -32), (14, -28), (12, -18), (12, -10), (9, -1), (9, 4), (-8, 4),
     (-13, 8), (-17, 12)],
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49), (0, 50),
     (3, 51), (5, 53), (8, 55), (8, 57), (10, 59), (5, 60), (5, 62), (10, 64), (13, 66),
     (18, 69), (25, 71), (30, 70), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73),
     (90, 75), (100, 76), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70),
     (158, 69), (162, 66), (170, 66), (178, 65), (178, 62), (170, 60), (162, 60),
     (158, 58), (156, 52), (150, 59), (142, 55), (140, 50), (135, 45), (130, 42),
     (127, 40), (122, 38), (120, 35), (122, 31), (120, 28), (110, 21), (108, 18),
     (105, 10), (103, 8), (100, 8), (98, 10), (95, 16), (92, 21), (89, 22), (86, 20),
     (82, 17), (80, 15), (77, 8), (75, 10), (73, 16), (70, 20), (66, 25), (62, 25),
     (58, 25), (55, 26), (52, 28), (50, 29), (48, 30), (44, 29), (40, 30), (36, 36),
     (33, 36), (30, 36), (27, 37), (23, 36), (22, 38), (19, 40), (16, 38), (12, 44),
     (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36), (-9, 37)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 36), (140, 38), (141, 41),
     (142, 43), (144, 44), (143, 42), (141, 39), (139, 37)],
    [(114, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32), (132, -32),
     (135, -35), (137, -35), (140, -38), (142, -38), (145, -38), (147, -39), (150, -37),
     (153, -32), (153, -27), (151, -24), (146, -19), (142, -15), (142, -11), (140, -17),
     (136, -15), (135, -12), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (178, -37), (176, -40), (173, -41),
     (170, -43), (167, -46)],
    [(44, -16), (47, -15), (50, -16), (49, -20), (46, -24), (44, -22), (43, -18)],
    [(95, 5), (98, 2), (101, -1), (104, -3), (106, -6), (104, -4), (100, 0), (97, 4)],
    [(105, -6), (110, -7), (114, -7), (114, -8), (108, -8)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -8), (147, -9), (142, -8),
     (137, -5), (132, -3)],
]


# ---------------------------------------------------------------- helpers
def text_w(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, s, f, max_w):
    """Greedy word wrap; returns list of lines."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(d, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, s, f, max_w, max_lines, min_size, path):
    """Shrink font until text fits in max_lines; returns (font, lines)."""
    size = f.size
    while size > min_size:
        ff = font(path, size)
        lines = wrap(d, s, ff, max_w)
        if len(lines) <= max_lines:
            return ff, lines
        size -= 1
    ff = font(path, size)
    return ff, wrap(d, s, ff, max_w)[:max_lines]


def draw_badge(d, x, y, num, r=9):
    """Numbered circle badge."""
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED, outline="white", width=1)
    f = font(SANS_B, 11)
    t = str(num)
    tw = text_w(d, t, f)
    d.text((x + r - tw / 2, y + r - 6), t, font=f, fill="white")


def tag_color(tag):
    return GREEN if tag == "CONFIRMED" else (176, 110, 20) if tag == "REPORTED" else RED


# ---------------------------------------------------------------- scenes
# Each draws a flat vector illustration inside box (x, y, w, h).
def scene(d, kind, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    cx, cy = x + w / 2, y + h / 2
    if kind == "strike":
        d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(58, 52, 46))
        for bx, bw, bh in [(0.05, 0.22, 0.45), (0.30, 0.18, 0.60), (0.52, 0.24, 0.38),
                           (0.78, 0.18, 0.52)]:
            d.rectangle([x + w * bx, y + h * 0.55 - h * bh * 0.5,
                         x + w * (bx + bw), y + h * 0.55 + h * 0.45], fill=(38, 34, 30))
        for sx, sy, r in [(0.68, 0.30, 14), (0.74, 0.22, 9), (0.62, 0.20, 7)]:
            d.ellipse([x + w * sx - r, y + h * sy - r, x + w * sx + r, y + h * sy + r],
                      fill=(232, 120, 30))
        d.ellipse([x + w * 0.68 - 5, y + h * 0.30 - 5, x + w * 0.68 + 5, y + h * 0.30 + 5],
                  fill=(255, 210, 90))
    elif kind == "city":
        d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(70, 66, 60))
        for bx, bw, bh in [(0.04, 0.26, 0.55), (0.34, 0.24, 0.75), (0.62, 0.30, 0.62)]:
            d.rectangle([x + w * bx, y + h * 0.62 - h * bh * 0.55,
                         x + w * (bx + bw), y + h * 0.62 + h * 0.38], fill=(44, 40, 36))
            for wy in range(3):
                for wx in range(2):
                    d.rectangle([x + w * (bx + 0.04 + wx * 0.10),
                                 y + h * (0.62 - bh * 0.55 + 0.08 + wy * 0.13),
                                 x + w * (bx + 0.09 + wx * 0.10),
                                 y + h * (0.62 - bh * 0.55 + 0.13 + wy * 0.13)],
                                fill=(255, 214, 110))
        d.polygon([(x + w * 0.85, y + h * 0.15), (x + w * 0.95, y + h * 0.35),
                   (x + w * 0.75, y + h * 0.35)], fill=RED)
        d.ellipse([x + w * 0.82, y + h * 0.35, x + w * 0.88, y + h * 0.41], fill=RED)
    elif kind == "chart":
        d.rectangle([x, y, x + w, y + h], fill=(24, 28, 36))
        pts = [(0.08, 0.30), (0.25, 0.38), (0.40, 0.34), (0.55, 0.55), (0.70, 0.62),
               (0.85, 0.78), (0.94, 0.72)]
        xy = [(x + w * px, y + h * py) for px, py in pts]
        d.line(xy, fill=(232, 80, 70), width=3)
        for px, py in xy:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 210, 90))
        d.text((x + 6, y + 4), "NVDA -7%", font=font(SANS_B, 13), fill=(255, 210, 90))
        d.text((x + 6, y + h - 20), "AI STOCKS SLIDE", font=font(SANS_B, 10), fill=(180, 190, 200))
    elif kind == "rockets":
        d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(96, 84, 66))
        for i, rx in enumerate([0.18, 0.50, 0.80]):
            bx = x + w * rx
            d.polygon([(bx, y + h * 0.12), (bx - 7, y + h * 0.42), (bx + 7, y + h * 0.42)],
                      fill=RED if i != 1 else BLUE)
            d.rectangle([bx - 7, y + h * 0.42, bx + 7, y + h * 0.62], fill="white",
                        outline=INK)
            d.polygon([(bx - 7, y + h * 0.62), (bx - 13, y + h * 0.72), (bx - 2, y + h * 0.66)],
                      fill=(232, 120, 30))
            d.polygon([(bx + 7, y + h * 0.62), (bx + 13, y + h * 0.72), (bx + 2, y + h * 0.66)],
                      fill=(232, 120, 30))
            d.ellipse([bx - 3, y + h * 0.46, bx + 3, y + h * 0.52], fill=SKY)
        for sx, sy in [(0.08, 0.15), (0.35, 0.10), (0.62, 0.08), (0.92, 0.18)]:
            d.ellipse([x + w * sx - 2, y + h * sy - 2, x + w * sx + 2, y + h * sy + 2],
                      fill="white")
    elif kind == "station":
        d.rectangle([x, y, x + w, y + h], fill=(18, 24, 40))
        d.ellipse([cx - 26, cy - 18, cx + 26, cy + 18], outline=(200, 210, 220), width=3)
        d.ellipse([cx - 12, cy - 8, cx + 12, cy + 8], fill=(200, 210, 220))
        d.rectangle([x + 6, cy - 5, cx - 26, cy + 5], fill=(90, 140, 200))
        d.rectangle([cx + 26, cy - 5, x + w - 6, cy + 5], fill=(90, 140, 200))
        for sx, sy in [(0.12, 0.18), (0.85, 0.14), (0.20, 0.82), (0.90, 0.80)]:
            d.ellipse([x + w * sx - 2, y + h * sy - 2, x + w * sx + 2, y + h * sy + 2],
                      fill="white")
    elif kind == "gavel":
        d.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
        d.rectangle([x + w * 0.55, y + h * 0.30, x + w * 0.85, y + h * 0.44], fill=(90, 60, 40))
        d.rectangle([x + w * 0.52, y + h * 0.26, x + w * 0.58, y + h * 0.48], fill=(90, 60, 40))
        d.rectangle([x + w * 0.20, y + h * 0.30, x + w * 0.52, y + h * 0.40], fill=(120, 84, 52))
        d.rectangle([x + w * 0.18, y + h * 0.62, x + w * 0.86, y + h * 0.74], fill=(70, 50, 36))
    elif kind == "pill":
        d.rectangle([x, y, x + w, y + h], fill=(220, 236, 228))
        d.rounded_rectangle([x + w * 0.18, y + h * 0.30, x + w * 0.82, y + h * 0.58],
                            radius=14, fill="white", outline=RED, width=2)
        d.rectangle([x + w * 0.50, y + h * 0.30, x + w * 0.82, y + h * 0.58], fill=RED)
        d.ellipse([x + w * 0.70, y + h * 0.66, x + w * 0.78, y + h * 0.78], fill=BLUE)
        d.ellipse([x + w * 0.80, y + h * 0.70, x + w * 0.86, y + h * 0.80], fill=GREEN)
        d.text((x + w * 0.30, y + h - 16), "$41bn", font=font(SANS_B, 13), fill=RED_DK)
    elif kind == "shield":
        d.rectangle([x, y, x + w, y + h], fill=(24, 28, 36))
        d.polygon([(cx, y + h * 0.12), (cx + w * 0.28, y + h * 0.24), (cx + w * 0.28, y + h * 0.52),
                   (cx, y + h * 0.86), (cx - w * 0.28, y + h * 0.52), (cx - w * 0.28, y + h * 0.24)],
                  fill=(90, 140, 200), outline=(200, 210, 220))
        d.line([(cx - 10, cy), (cx - 3, cy + 8), (cx + 12, cy - 8)], fill="white", width=3)
        for sx, sy in [(0.12, 0.2), (0.88, 0.18), (0.10, 0.75), (0.90, 0.78)]:
            d.ellipse([x + w * sx - 2, y + h * sy - 2, x + w * sx + 2, y + h * sy + 2],
                      fill=(255, 210, 90))
    elif kind == "market":
        d.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
        bars = [(0.12, 0.55, 0.72), (0.30, 0.45, 0.60), (0.48, 0.42, 0.62),
                (0.66, 0.35, 0.55), (0.84, 0.25, 0.68)]
        for bx, top, bot in bars:
            d.line([(x + w * bx, y + h * (top - 0.08)), (x + w * bx, y + h * (bot + 0.08))],
                   fill=INK, width=2)
            d.rectangle([x + w * (bx - 0.06), y + h * top, x + w * (bx + 0.06), y + h * bot],
                        fill=GREEN)
        d.text((x + 6, y + 4), "+6%", font=font(SANS_B, 13), fill=GREEN)
    elif kind == "flags":
        d.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
        d.rectangle([x + w * 0.08, y + h * 0.22, x + w * 0.44, y + h * 0.55], fill=(0, 0, 0))
        d.rectangle([x + w * 0.08, y + h * 0.33, x + w * 0.44, y + h * 0.44], fill=RED)
        d.rectangle([x + w * 0.08, y + h * 0.44, x + w * 0.44, y + h * 0.55], fill=(255, 206, 0))
        d.rectangle([x + w * 0.56, y + h * 0.22, x + w * 0.92, y + h * 0.55], fill=(0, 91, 187))
        d.rectangle([x + w * 0.56, y + h * 0.38, x + w * 0.92, y + h * 0.55], fill=(255, 213, 0))
    elif kind == "jets":
        d.rectangle([x, y, x + w, y + h], fill=(214, 228, 236))
        for jx, jy, c in [(0.30, 0.35, (70, 70, 78)), (0.68, 0.60, (90, 40, 40))]:
            bx, by = x + w * jx, y + h * jy
            d.polygon([(bx, by - 14), (bx + 22, by + 6), (bx + 6, by + 6), (bx + 2, by + 14),
                       (bx - 4, by + 6), (bx - 16, by + 8)], fill=c)
        d.line([(x, y + h * 0.85), (x + w, y + h * 0.85)], fill=RED, width=2)
        d.text((x + 6, y + 4), "ADIZ", font=font(SANS_B, 11), fill=RED_DK)
    elif kind == "mountains":
        d.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
        d.ellipse([x + w * 0.72, y + h * 0.10, x + w * 0.86, y + h * 0.26], fill=(232, 150, 40))
        d.polygon([(x, y + h), (x + w * 0.35, y + h * 0.25), (x + w * 0.70, y + h)], fill=(120, 110, 90))
        d.polygon([(x + w * 0.30, y + h), (x + w * 0.65, y + h * 0.35), (x + w, y + h)], fill=(90, 82, 66))
        d.polygon([(x + w * 0.35, y + h * 0.25), (x + w * 0.28, y + h * 0.38),
                   (x + w * 0.42, y + h * 0.38)], fill="white")
    elif kind == "cricket":
        d.rectangle([x, y, x + w, y + h], fill=(34, 110, 60))
        d.rectangle([x + w * 0.42, y + h * 0.18, x + w * 0.52, y + h * 0.62], fill=(210, 180, 120))
        d.rectangle([x + w * 0.44, y + h * 0.08, x + w * 0.50, y + h * 0.18], fill=(210, 180, 120))
        d.ellipse([x + w * 0.72, y + h * 0.30, x + w * 0.84, y + h * 0.46], fill=RED)
        for sx in [0.18, 0.24, 0.30]:
            d.rectangle([x + w * sx, y + h * 0.60, x + w * sx + 3, y + h * 0.86], fill=(240, 220, 160))
        d.text((x + 6, y + 4), "188/2", font=font(SANS_B, 12), fill="white")
    elif kind == "virus":
        d.rectangle([x, y, x + w, y + h], fill=(248, 240, 225))
        for vx, vy, r in [(0.30, 0.40, 16), (0.68, 0.55, 12), (0.55, 0.25, 8)]:
            bx, by = x + w * vx, y + h * vy
            for ang in range(0, 360, 45):
                import math
                ex = bx + (r + 6) * math.cos(math.radians(ang))
                ey = by + (r + 6) * math.sin(math.radians(ang))
                d.line([(bx, by), (ex, ey)], fill=RED, width=2)
            d.ellipse([bx - r, by - r, bx + r, by + r], fill=RED)
            d.ellipse([bx - r // 2, by - r // 2, bx + r // 3, by + r // 3], fill=(255, 150, 140))
    elif kind == "car":
        d.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
        d.polygon([(x + w * 0.12, y + h * 0.62), (x + w * 0.22, y + h * 0.38),
                   (x + w * 0.68, y + h * 0.38), (x + w * 0.88, y + h * 0.62)], fill=BLUE)
        d.rectangle([x + w * 0.08, y + h * 0.58, x + w * 0.92, y + h * 0.72], fill=BLUE)
        d.ellipse([x + w * 0.20, y + h * 0.66, x + w * 0.32, y + h * 0.82], fill=INK)
        d.ellipse([x + w * 0.68, y + h * 0.66, x + w * 0.80, y + h * 0.82], fill=INK)
        d.text((x + 6, y + 4), "191,780", font=font(SANS_B, 12), fill=BLUE)
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)


# ---------------------------------------------------------------- layout
REGION_COLORS = {
    "Europe": (38, 74, 120), "Middle East": (200, 110, 20), "Asia": (110, 60, 140),
    "Americas": (46, 110, 58), "Africa": (140, 90, 40), "Oceania": (20, 130, 130),
}
PIN_REGION = {1: "Middle East", 2: "Europe", 3: "Americas", 4: "Asia", 5: "Asia",
              6: "Americas", 7: "Europe", 8: "Americas", 9: "Asia", 10: "Europe",
              11: "Asia", 12: "Africa", 13: "Oceania", 14: "Asia", 15: "Europe"}
PIN_OFFSET = {6: (-15, 12), 11: (13, -11), 15: (14, -11)}


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 14
    CW = W - 2 * MX  # 996

    # ---- masthead kicker
    d.text((MX, 10), "THE WORLD'S NEWS OF ONE DAY", font=font(SANS_B, 12), fill=RED)
    right = "53 STORIES · 7 REGIONS · 20 FIELDS · ALL FROM THIS TUESDAY"
    d.text((W - MX - text_w(d, right, font(SANS_B, 11)), 11), right,
           font=font(SANS_B, 11), fill=INK)
    # ---- date headline
    date = "Tuesday 24 November 2026"
    df = font(DISPLAY_B, 58)
    d.text(((W - text_w(d, date, df)) / 2, 28), date, font=df, fill=INK)
    d.line([(MX, 100), (W - MX, 100)], fill=RULE, width=2)
    d.line([(MX, 104), (W - MX, 104)], fill=RULE, width=1)

    # ---- UTC timeline strip (winner-1117 style cells)
    ty = 110
    d.rectangle([MX, ty, MX + 62, ty + 42], fill=RED)
    d.text((MX + 6, ty + 6), "THE DAY", font=font(SANS_B, 11), fill="white")
    d.text((MX + 6, ty + 21), "IN UTC", font=font(SANS_B, 11), fill="white")
    cell_x = MX + 70
    cell_w = (W - MX - cell_x) / 7
    for i, (t, ev) in enumerate(TIMELINE):
        cx = cell_x + i * cell_w
        d.line([(cx, ty + 2), (cx, ty + 40)], fill=GREY, width=1)
        d.text((cx + 6, ty + 2), t, font=font(SANS_B, 11), fill=RED_DK)
        ef = font(SERIF, 11)
        for j, ln in enumerate(wrap(d, ev, ef, cell_w - 12)):
            d.text((cx + 6, ty + 17 + j * 13), ln, font=ef, fill=INK)
    d.line([(MX, ty + 46), (W - MX, ty + 46)], fill=RULE, width=1)

    # ---- heroes
    hy, hh, hw, gap = 164, 186, 326, 9
    for i, (num, region, head, dek, tag, src, lon, lat, kind) in enumerate(HEROES):
        x = MX + i * (hw + gap)
        scene(d, kind, x, hy, hw, 76)
        draw_badge(d, x + 6, hy + 76 - 24, num)
        d.text((x, hy + 82), region, font=font(SANS_B, 10), fill=RED)
        hf, hlines = fit_lines(d, head, font(SERIF_B, 19), hw, 2, 14, SERIF_B)
        yy = hy + 97
        for ln in hlines:
            d.text((x, yy), ln, font=hf, fill=INK)
            yy += hf.size + 2
        df2 = font(SERIF, 12)
        yy = hy + 142
        for ln in wrap(d, dek, df2, hw)[:2]:
            d.text((x, yy), ln, font=df2, fill=(50, 46, 40))
            yy += 14
        vf = font(SANS_B, 9)
        d.text((x, hy + 172), tag, font=vf, fill=tag_color(tag))
        d.text((x + text_w(d, tag, vf) + 6, hy + 172), "· " + src,
               font=font(SANS, 9), fill=GREY)

    # ---- panels (2 rows x 6)
    pxs = [MX, 181, 348, 515, 682, 849]
    pw, ph = 160, 158
    for row in range(2):
        for col in range(6):
            idx = row * 6 + col
            num, region, head, dek, tag, src, lon, lat, kind = PANELS[idx]
            x, y = pxs[col], 358 + row * 166
            scene(d, kind, x, y, pw, 54)
            draw_badge(d, x + 4, y + 54 - 20, num, r=8)
            d.text((x, y + 58), region, font=font(SANS_B, 8), fill=RED)
            hf, hlines = fit_lines(d, head, font(SERIF_B, 12), pw, 3, 10, SERIF_B)
            yy = y + 71
            for ln in hlines:
                d.text((x, yy), ln, font=hf, fill=INK)
                yy += hf.size + 1
            df2 = font(SERIF, 10)
            yy = y + 71 + 3 * 13
            for ln in wrap(d, dek, df2, pw)[:3]:
                d.text((x, yy), ln, font=df2, fill=(50, 46, 40))
                yy += 12
            vf = font(SANS_B, 8)
            d.text((x, y + ph - 12), tag, font=vf, fill=tag_color(tag))
            d.text((x + text_w(d, tag, vf) + 4, y + ph - 12), "· " + src,
                   font=font(SANS, 8), fill=GREY)

    # ---- bottom headers
    by = 690
    d.text((MX, by), "WHERE IT HAPPENED", font=font(SANS_B, 11), fill=RED)
    d.text((352, by), "AMERICAS · AFRICA · MIDDLE EAST — 19",
           font=font(SANS_B, 10), fill=INK)
    d.text((683, by), "EUROPE · ASIA · OCEANIA · MARKETS — 19",
           font=font(SANS_B, 10), fill=INK)
    d.line([(MX, by + 15), (W - MX, by + 15)], fill=RULE, width=1)

    # ---- map
    map_x, map_y, map_w, map_h = MX, 710, 324, 132
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(238, 234, 220),
                outline=RULE, width=1)

    def proj(lon, lat):
        px = map_x + (lon + 170) / 360.0 * map_w
        py = map_y + (78 - lat) / 136.0 * map_h
        return px, py

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=MAP_LAND,
                  outline=MAP_LINE)
    all_stories = HEROES + PANELS
    for (num, region, head, dek, tag, src, lon, lat, kind) in all_stories:
        px, py = proj(lon, lat)
        ox, oy = PIN_OFFSET.get(num, (0, 0))
        cx, cy = px + ox, py + oy
        if (ox, oy) != (0, 0):
            d.line([(px, py), (cx, cy)], fill=INK, width=1)
        col = REGION_COLORS[PIN_REGION[num]]
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=col, outline="white", width=1)
        nf = font(SANS_B, 8)
        t = str(num)
        d.text((cx - text_w(d, t, nf) / 2, cy - 5), t, font=nf, fill="white")
    # map legend
    lx, ly = map_x, map_y + map_h + 6
    lf = font(SANS_B, 8)
    for name, col in REGION_COLORS.items():
        d.ellipse([lx, ly + 2, lx + 7, ly + 9], fill=col)
        d.text((lx + 10, ly), name, font=lf, fill=INK)
        lx += 10 + text_w(d, name, lf) + 8

    # ---- DATE CHECK box (under map)
    dc_x, dc_y, dc_w = MX, 872, 324
    d.rectangle([dc_x, dc_y, dc_x + dc_w, dc_y + 96], outline=RED, width=1)
    d.rectangle([dc_x, dc_y, dc_x + dc_w, dc_y + 16], fill=RED)
    d.text((dc_x + 6, dc_y + 3), "DATE CHECK — LEFT OUT AS OLDER NEWS",
           font=font(SANS_B, 9), fill="white")
    dc_items = [
        ("COP31 collapses", "Sun 22 Nov"),
        ("FIFA names WWC hosts", "Mon 23 Nov"),
        ("BepiColombo captured", "Sat 21 Nov"),
        ("Huang back at Nvidia", "Mon 23 Nov"),
        ("14 back ICJ ruling", "Mon 23 Nov"),
        ("Executions sped up", "Mon 23 Nov"),
        ("Peru quake: 1 dead", "Fri 20 Nov"),
        ("M6.5 quake, Vanuatu", "Mon 23 Nov"),
        ("Miley Cyrus marries", "Sat 21 Nov"),
        ("Space-medicine test", "Mon 23 Nov"),
        ("Not yet: Shenzhou 24", "due 25 Nov"),
        ("Not yet: Hasina", "due 16 Dec"),
    ]
    itf = font(SERIF, 8)
    dtf = font(SANS_B, 8)
    for i, (item, when) in enumerate(dc_items):
        col = i % 2
        row = i // 2
        ix = dc_x + 6 + col * 162
        iy = dc_y + 20 + row * 13
        dw = text_w(d, when, dtf)
        max_tw = 162 - 6 - dw - 6
        txt = item
        while text_w(d, txt, itf) > max_tw and len(txt) > 4:
            txt = txt[:-2]
        if txt != item:
            txt = txt.rstrip() + "…"
        d.text((ix, iy), txt, font=itf, fill=INK)
        d.text((ix + 162 - 6 - dw, iy), when, font=dtf, fill=RED_DK)

    # ---- briefs
    bf = font(SERIF, 11)
    for ci, briefs in enumerate([BRIEFS_A, BRIEFS_B]):
        bx = 352 + ci * 331
        for j, (num, txt, srcname, tier) in enumerate(briefs):
            yy = 712 + j * 13
            d.ellipse([bx, yy + 1, bx + 12, yy + 13], fill=tag_color(tier))
            nf = font(SANS_B, 8)
            t = str(num)
            d.text((bx + 6 - text_w(d, t, nf) / 2, yy + 2), t, font=nf, fill="white")
            fnt = bf
            while text_w(d, txt + " · " + srcname, fnt) > 325 - 18 and fnt.size > 9:
                fnt = font(SERIF, fnt.size - 1)
            d.text((bx + 17, yy), txt, font=fnt, fill=INK)
            d.text((bx + 17 + text_w(d, txt, fnt), yy), " · " + srcname,
                   font=fnt, fill=GREY)

    # ---- footer
    fy = 966
    d.text((MX, fy), "Every story here happened or was first reported on Tuesday 24 November 2026.",
           font=font(SERIF_I, 10), fill=(60, 54, 46))
    d.text((MX, fy + 13), "CLAIM = one side's account, not independently confirmed. Brief badges: "
                          "green CONFIRMED · amber REPORTED · red CLAIM.",
           font=font(SERIF_I, 10), fill=(60, 54, 46))
    d.text((MX, fy + 26), "Sources: Reuters, AP, AFP, NYT, WSJ, Nature, NASA, USGS, Cricinfo, "
                          "Kyiv Independent, Horizon, OneTurn, SuMarket. Original drawings.",
           font=font(SERIF, 9), fill=GREY)
    return img


if __name__ == "__main__":
    im = build()
    im.save("entry.png", optimize=True)
    data = open("entry.png", "rb").read()
    print("size", len(data), "bytes; sha256", hashlib.sha256(data).hexdigest())
    print("dimensions", im.size)
