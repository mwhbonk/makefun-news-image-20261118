#!/usr/bin/env python3
"""Draw the news-image-20261118 front page: 'The World in One Page'.

Wednesday 18 November 2026 — 35 stories, 6 continents, one page.
Lead: Ukraine collapses the Kerch/Crimea bridge for a second day while
Russia hits Kyiv's bridges; Trump lands in Manila for the Quad ahead of
the first Trump-Xi-Putin trilateral in China. Verified against Reuters,
AP, BBC/DW, SCMP, Indian Express and UN reporting for 17-18 Nov 2026.
Hero: generated illustration of a sea bridge span collapsed at dusk.
Output: 1024x1024 PNG, deterministic (no randomness, no network, no clock).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 236)
INK = (17, 17, 17)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)

F = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = os.path.join(F, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(F, "DejaVuSerif.ttf")
SANS = os.path.join(F, "DejaVuSans.ttf")
SANS_B = os.path.join(F, "DejaVuSans-Bold.ttf")
HERE = os.path.dirname(os.path.abspath(__file__))
HERO = os.path.join(HERE, "media-generation-news18-hero-bridge-manila-0-d09592af-53be-410c-b450-2b85310181c9.png")

COL = {
    "ASIA": (0, 87, 183), "EUROPE": (15, 118, 110), "AFRICA": (166, 90, 0),
    "AMERICAS": (166, 25, 46), "OCEANIA": (109, 40, 217), "SPORT": (51, 65, 85),
}


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def trunc(draw, text, fnt, max_w):
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + "...", font=fnt) > max_w:
        text = text.rsplit(" ", 1)[0] if " " in text else text[:-1]
    return text + "..."


def hero_crop(box_w, box_h):
    im = Image.open(HERO).convert("RGB")
    w, h = im.size
    target = box_w / box_h
    ch = int(w / target)
    ch = min(ch, h)
    im = im.crop((0, 0, w, ch))
    return im.resize((box_w, box_h), Image.LANCZOS)


# (region, headline, deck) — 33 grid stories; lead + Trump strip make 35.
ITEMS = [
    ("ASIA", "Modi urges Indo-Pacific peace", "India-ASEAN summit in Manila."),
    ("ASIA", "Cyclone Akvan nears Bengal coast", "Andhra Pradesh and Odisha on alert."),
    ("ASIA", "Baidu chief warns of AI bubble", "Warning lands just before APEC meets."),
    ("ASIA", "Japan scrambles jets on Russians", "Suspected Russian planes near Japan."),
    ("ASIA", "Canada, China extend trade deals", "Xi meets Carney ahead of APEC."),
    ("ASIA", "Iran hits US radar base in Bahrain", "Drones hit the base hosting the US Navy's 5th Fleet."),
    ("ASIA", "Tanker attacked in Strait of Hormuz", "21 Indians evacuated from LPG carrier MT TARA GAS."),
    ("ASIA", "India GDP up 7.5%; Amazon $7bn", "Amazon to fund renewables in India."),
    ("ASIA", "ASEAN backs AI for small firms", "New declaration to bring AI tools to micro firms."),
    ("ASIA", "Houthis seize Bab al-Mandab", "Rebels take key Yemen shipping point."),
    ("ASIA", "Thailand fire kills 11", "Major blaze in Thailand leaves more than a dozen hurt."),
    ("AMERICAS", "Pope Leo ends S. America tour", "Rosary from the crowd hits his eye at Mass in Peru."),
    ("EUROPE", "Russia downs record 1,441 drones", "Biggest single-day drone toll of the war, Moscow says."),
    ("EUROPE", "Probe: Russia used tear gas", "OPCW-backed inquiry confirms the use."),
    ("EUROPE", "Zelenskyy plans Berlin talks", "Kyiv shapes next phase of talks."),
    ("EUROPE", "EU to lend Ukraine EUR 45bn", "Covers Kyiv's EUR 70bn shortfall."),
    ("EUROPE", "UK sanctions settlement firms", "London acts to protect the two-state solution."),
    ("EUROPE", "Estonia shuts Russia border post", "Follows sabotage bid on a drone maker."),
    ("EUROPE", "COP31: EU pushes fossil-fuel exit", "MEPs in Antalya demand faster exit."),
    ("AFRICA", "17 killed in S. Africa shootings", "Two mass shootings in one day."),
    ("AFRICA", "Guinea mining ban displaces many", "Illegal-mining ban sparks tensions."),
    ("AFRICA", "Ebola in DR Congo out of control", "Outbreak passes six months with no end in sight."),
    ("AFRICA", "WHO: Eritrea eliminates trachoma", "Eye disease wiped out at last."),
    ("AFRICA", "Sudan drones killed 1,600 in 2026", "UN counts the civilian toll."),
    ("AFRICA", "Nigeria short of diphtheria drugs", "Thousands of children at risk as supplies run dry."),
    ("AMERICAS", "Costa Rica journalist shot dead", "Reporter killed after probing drug trafficking and graft."),
    ("AMERICAS", "Ecuador fishermen sue over US strikes", "Families challenge secret US strikes."),
    ("AMERICAS", "Buffett donates $5.5 billion", "Berkshire chief gives away another huge fortune share."),
    ("AMERICAS", "Drones are crime's new weapon", "Latin American gangs deploy drones; states struggle to cope."),
    ("OCEANIA", "Rio Tinto pays $250m for Panguna", "Miner funds repair of the shuttered Papua mine site."),
    ("OCEANIA", "PNG: Taiwan 'does not operate here'", "Papua New Guinea leader restates the one-China line."),
    ("SPORT", "Dhoni retires from the IPL", "CSK great, 5,439 runs, now mentor."),
    ("SPORT", "India win 10th SAFF title", "India beat Pakistan 2-1 in the Dhaka final."),
]


def main():
    assert len(ITEMS) == 33, len(ITEMS)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26
    # ---- masthead ----
    d.text((W // 2, 22), "THE WORLD", font=font(SERIF_B, 76), fill=INK, anchor="ma")
    d.text((W // 2, 112), "WEDNESDAY 18 NOVEMBER 2026  \u2022  35 STORIES  \u2022  6 CONTINENTS  \u2022  ONE PAGE",
           font=font(SANS_B, 17), fill=INK, anchor="ma")
    d.line([(M, 138), (W - M, 138)], fill=INK, width=4)
    d.line([(M, 144), (W - M, 144)], fill=INK, width=1)

    # ---- lead: Crimea bridge, hero right ----
    d.text((M, 154), "UKRAINE  \u2022  EUROPE", font=font(SANS_B, 15), fill=COL["EUROPE"])
    d.text((M, 176), "BRIDGE FALLS,", font=font(SERIF_B, 36), fill=INK)
    d.text((M, 216), "KYIV IS HIT", font=font(SERIF_B, 36), fill=INK)
    deck = ("Ukraine strikes the Kerch bridge a second day; its road arch "
            "collapses into the sea. Russia hits Kyiv's North and South "
            "bridges and damages the metro.")
    y = 264
    for ln in wrap(d, deck, font(SERIF, 17), 560):
        d.text((M, y), ln, font=font(SERIF, 17), fill=INK)
        y += 23
    hx, hy, hw, hh = 606, 154, 392, 190
    img.paste(hero_crop(hw, hh), (hx, hy))
    d.rectangle([hx, hy, hx + hw, hy + hh], outline=INK, width=2)
    d.rectangle([hx, hy + hh - 28, hx + hw, hy + hh], fill=(0, 87, 183))
    d.text((hx + hw // 2, hy + hh - 24), "KERCH STRAIT  \u2022  2 KILLED",
           font=font(SANS_B, 14), fill=WHITE, anchor="ma")

    # ---- Trump strip: story #2 ----
    ty = 356
    d.rectangle([M, ty, W - M, ty + 42], fill=INK)
    d.text((M + 14, ty + 6), "TRUMP IN MANILA  \u2022  ",
           font=font(SANS_B, 16), fill=(255, 213, 79))
    d.text((M + 14, ty + 24), "Quad talks today, then China for the first Trump\u2013Xi\u2013Putin summit",
           font=font(SANS, 15), fill=WHITE)
    d.text((W - M - 14, ty + 6), "ASIA", font=font(SANS_B, 16), fill=(255, 213, 79), anchor="ra")

    # ---- 33-item grid: 3 cols x 11 rows ----
    gx, gy = M, 412
    cw = (W - 2 * M - 24) // 3
    chh = 50
    for i, (reg, head, deck) in enumerate(ITEMS):
        x = gx + (i % 3) * (cw + 12)
        y = gy + (i // 3) * chh
        col = COL[reg]
        d.line([(x, y + 4), (x, y + chh - 8)], fill=col, width=4)
        d.text((x + 10, y), reg, font=font(SANS_B, 10), fill=col)
        d.text((x + 10, y + 13), trunc(d, head, font(SERIF_B, 13), cw - 12),
               font=font(SERIF_B, 13), fill=INK)
        d.text((x + 10, y + 31), trunc(d, deck, font(SANS, 11), cw - 12),
               font=font(SANS, 11), fill=(60, 60, 60))

    # ---- footer ----
    fy = 972
    d.text((W // 2, 978), "Sources: Reuters, AP, BBC, DW, SCMP, Indian Express, UN  \u2022  18 November 2026",
           font=font(SANS, 12), fill=GREY, anchor="ma")
    out = os.path.join(HERE, "news.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
