"""Paint entry.png: Friday front page for Friday 20 November 2026.

Layout, top to bottom, on a 1024 square:
  masthead block -> lead story with an EU-map picture -> two side briefs ->
  three illustrated mid cards -> an IN BRIEF column of six.

Every story below is one reported on 19-20 Nov 2026, written here from the
day's wire copy (Reuters, AP, Politico, Guardian, BBC, Straits Times).
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W = 1024
PAD = 26
A = (246, 243, 235)      # newsprint
INK = (18, 22, 32)
MUTE = (92, 99, 114)
DEEP = (12, 18, 34)
CRIM = (188, 38, 46)
BLUE = (34, 78, 156)
GOLD = (206, 152, 40)
TEAL = (17, 112, 110)
VIOL = (116, 44, 118)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
_fonts = {}


def px(size, strong=True):
    """Cached face lookup so repeated calls stay cheap."""
    key = (size, strong)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(BOLD if strong else PLAIN, size)
    return _fonts[key]


def wrap(draw, words, fnt, width):
    """Wrap a phrase into lines no wider than `width`."""
    lines, cur = [], ""
    for w in words.split():
        probe = f"{cur} {w}".strip()
        if draw.textlength(probe, font=fnt) <= width:
            cur = probe
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


sheet = Image.new("RGB", (W, W), DEEP)
d = ImageDraw.Draw(sheet)

# ---------------------------------------------------------------- masthead
d.text((PAD, 20), "THE WORLD TODAY", font=px(58), fill=(255, 255, 255))
d.text((PAD + 2, 92), "FRIDAY 20 NOVEMBER 2026", font=px(30), fill=GOLD)
d.text((PAD + 2, 128), "twelve stories from one day  ·  Brexit reset, markets slide, cyclone hits India",
       font=px(18, False), fill=(152, 162, 182))
d.line((PAD, 156, W - PAD, 156), fill=(58, 68, 94), width=3)

# ------------------------------------------------------------------- lead
LEAD = (PAD, 168, 646, 470)
d.rounded_rectangle(LEAD, radius=14, fill=A)
d.rounded_rectangle((PAD, 168, PAD + 9, 470), radius=4, fill=CRIM)
chip_lbl = "EUROPE  ·  SUMMIT"
chip_w = d.textlength(chip_lbl, font=px(14))
d.rounded_rectangle((PAD + 24, 184, PAD + 44 + chip_w, 210), radius=10, fill=CRIM)
d.text((PAD + 34, 187), chip_lbl, font=px(14), fill=(255, 255, 255))

# EU circle of stars with two linked flags
gx, gy, gr = PAD + 96, 322, 66
d.ellipse((gx - gr, gy - gr, gx + gr, gy + gr), fill=(24, 46, 110))
d.ellipse((gx - gr, gy - gr, gx + gr, gy + gr), outline=(255, 204, 0), width=3)
for k in range(12):
    ang = math.pi * 2 * k / 12 - math.pi / 2
    sx, sy = gx + 46 * math.cos(ang), gy + 46 * math.sin(ang)
    d.polygon([(sx, sy - 6), (sx + 5, sy + 4), (sx - 5, sy + 4)], fill=(255, 204, 0))
d.rounded_rectangle((gx - 44, gy - 4, gx - 4, gy + 24), radius=4, fill=(0, 36, 125))
d.line((gx - 44, gy + 2, gx - 4, gy + 2), fill=(255, 255, 255), width=3)
d.rounded_rectangle((gx + 4, gy - 4, gx + 44, gy + 24), radius=4, fill=(0, 94, 184))
for j in range(3):
    d.line((gx + 14 + j * 8, gy - 4, gx + 14 + j * 8, gy + 24), fill=(255, 255, 255), width=2)
d.text((gx - 52, gy + gr + 12), "3 deals signed", font=px(15), fill=INK)

lead_x = gx + gr + 34
lead_room = LEAD[2] - lead_x - 18
head = wrap(d, "Burnham in Brussels: UK and EU sign Brexit-reset deals on food, carbon, youth",
            px(30), lead_room)[:4]
ty = 232
for line in head:
    d.text((lead_x, ty), line, font=px(30), fill=INK)
    ty += 35
for line in wrap(d, "PM signs the SPS food deal worth up to £5.1bn a year, links carbon markets to skip "
                    "£6.5bn of CBAM charges, and caps a 100,000-a-year youth mobility scheme from 2028.",
                 px(17, False), lead_room)[:6]:
    d.text((lead_x, ty + 4), line, font=px(17, False), fill=MUTE)
    ty += 22

# ------------------------------------------------------- two side briefs
SIDE_X = 662
for i, (tag, tint, title, note, glyph) in enumerate([
    ("MARKETS", TEAL, "Anthropic closes debut at $97, near $2tn as tech sells off",
     "Biggest IPO on record; Dow sinks 1,800", "ant"),
    ("ASIA", BLUE, "Cyclone Akvan makes landfall near Gopalpur, Odisha",
     "1.2 lakh evacuated; rail services cancelled", "storm"),
]):
    top = 168 + i * 154
    box = (SIDE_X, top, W - PAD, top + 146)
    d.rounded_rectangle(box, radius=12, fill=A)
    d.rounded_rectangle((SIDE_X, top, SIDE_X + 8, top + 146), radius=4, fill=tint)
    tw = d.textlength(tag, font=px(13))
    d.rounded_rectangle((SIDE_X + 18, top + 12, SIDE_X + 34 + tw, top + 34), radius=9, fill=tint)
    d.text((SIDE_X + 26, top + 14), tag, font=px(13), fill=(255, 255, 255))
    cx, cy = SIDE_X + 60, top + 90
    if glyph == "ant":
        d.rounded_rectangle((cx - 34, cy - 20, cx + 34, cy + 20), radius=5, fill=TEAL)
        d.text((cx - 26, cy - 14), "ANT", font=px(17), fill=(255, 255, 255))
        d.text((cx - 26, cy + 2), "$97", font=px(15), fill=(255, 238, 176))
    elif glyph == "storm":
        for j in range(3):
            d.arc((cx - 26, cy - 30 + j * 14, cx + 26, cy + 6 + j * 14), 200, 340, fill=(120, 150, 200), width=4)
        d.polygon([(cx - 8, cy + 26), (cx + 8, cy + 26), (cx, cy + 44)], fill=(150, 170, 210))
    else:
        for j, tint2 in enumerate((CRIM, GOLD, TEAL)):
            hx = cx - 22 + j * 22
            d.ellipse((hx - 9, cy - 26, hx + 9, cy - 8), fill=tint2)
            d.polygon([(hx - 11, cy + 12), (hx + 11, cy + 12), (hx, cy - 8)], fill=tint2)
    tx = SIDE_X + 108
    room = W - PAD - tx - 14
    yy = top + 40
    for line in wrap(d, title, px(18), room)[:3]:
        d.text((tx, yy), line, font=px(18), fill=INK)
        yy += 21
    for line in wrap(d, note, px(15, False), room)[:2]:
        d.text((tx, yy + 2), line, font=px(15, False), fill=MUTE)
        yy += 17

# ------------------------------------------------------------ mid row (3)
COL_W = (W - 2 * PAD - 2 * 12) // 3
MID_Y = 480
for i, (tag, tint, title, note) in enumerate([
    ("MIDEAST", CRIM, "Israel urges US join strikes on Iran; Gulf fears wider war",
     "Netanyahu calls an operation 'inevitable' as allies race to calm it"),
    ("EAST ASIA", VIOL, "Trump, Xi and Putin sign Shenzhen peace declaration",
     "Joint text omits Ukraine and Iran wars; Europe wary of 'Yalta format'"),
    ("HORN OF AFRICA", GOLD, "Ethiopia and Eritrea mass troops near Badme border",
     "Clash reports stoke fears of a new war on the Red Sea flank"),
]):
    left = PAD + i * (COL_W + 12)
    top = MID_Y
    d.rounded_rectangle((left, top, left + COL_W, top + 158), radius=12, fill=A)
    d.rounded_rectangle((left, top, left + COL_W, top + 8), radius=4, fill=tint)
    tw = d.textlength(tag, font=px(13))
    d.rounded_rectangle((left + 16, top + 20, left + 32 + tw, top + 42), radius=9, fill=tint)
    d.text((left + 24, top + 22), tag, font=px(13), fill=(255, 255, 255))
    yy = top + 52
    for line in wrap(d, title, px(18), COL_W - 32)[:4]:
        d.text((left + 16, yy), line, font=px(18), fill=INK)
        yy += 22
    for line in wrap(d, note, px(13, False), COL_W - 32)[:3]:
        d.text((left + 16, yy + 2), line, font=px(13, False), fill=MUTE)
        yy += 17

# ------------------------------------------------------------- in brief
d.text((PAD, 654), "IN BRIEF", font=px(20), fill=(255, 255, 255))
d.line((PAD + 110, 668, W - PAD, 668), fill=(58, 68, 94), width=2)

briefs = [
    ("MARKETS", "Nasdaq tumbles into correction as the AI trade wobbles; Seoul opens lower"),
    ("MYANMAR", "ICJ rules Myanmar committed genocide against the Rohingya - a first"),
    ("EUROPE", "Five EU states plan Rwanda 'return hubs' for refused asylum seekers"),
    ("VENEZUELA", "Hegseth visits Caracas, boasting of Maduro's capture by US forces"),
    ("INDONESIA", "Semeru erupts in East Java; hundreds shelter as ash blankets villages"),
    ("CULTURE", "GTA 6 out now - fans pull all-nighters in the biggest launch in games"),
]
col_x = [PAD, W // 2 + 6]
row_h = 55
for n, (tag, text) in enumerate(briefs):
    col = n % 2
    row = n // 2
    x = col_x[col]
    y = 686 + row * row_h
    tw = d.textlength(tag, font=px(13))
    d.rounded_rectangle((x, y + 6, x + 20 + tw, y + 27), radius=8, fill=(44, 54, 76))
    d.text((x + 9, y + 8), tag, font=px(13), fill=(220, 228, 244))
    body_x = x + 30 + tw
    body = wrap(d, text, px(15, False), (W // 2 - PAD - 26) - (body_x - x))[:2]
    for k, line in enumerate(body):
        d.text((body_x, y + 5 + k * 20), line, font=px(15, False), fill=(226, 231, 242))
d.line((PAD, 990, W - PAD, 990), fill=(58, 68, 94), width=2)
d.text((PAD, 996), "compiled 20 Nov 2026 · twelve stories · six regions",
       font=px(14, False), fill=(128, 138, 158))

sheet.save("/home/agentuser/makefun/entries/news20/entry.png", optimize=True)
print("bytes", os.path.getsize("/home/agentuser/makefun/entries/news20/entry.png"))
