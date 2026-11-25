#!/usr/bin/env python3
"""og.png 1200x630 — Vintage Press Café — letterpress plate on ink. v2 (vision pass:
gap between Press and CAFÉ, band moved under frame with clearance, brighter slug/email)."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

INK = (28, 25, 23); PAPER = (245, 239, 227); RED = (200, 74, 44)
SLUG = (178, 164, 138); BAND = (43, 37, 33); GOLD = (212, 175, 82); FRAME = (245, 239, 227)

def font(paths, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in paths:
            p = b + n
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size)
                except Exception: pass
    return ImageFont.load_default()

serif = lambda s: font(["Iowan Old Style.ttc", "Palatino.ttc", "Georgia.ttf", "Times New Roman.ttf"], s)
mono = lambda s: font(["Menlo.ttc", "Menlo-Regular.ttf", "Courier New.ttf"], s)

img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img)

# halftone dot field in the upper corners (dim, symmetric, same fade)
for cx0 in (0, W - 220):
    for yy in range(0, 200, 22):
        for xx in range(0, 200, 22):
            r = 3.2 - 2.6 * (yy / 200.0)
            x = cx0 + xx + (11 if (yy // 22) % 2 else 0)
            d.ellipse([x - r, yy - r, x + r, yy + r], fill=(58, 50, 42))

# double frame (letterpress rule)
d.rectangle([26, 26, W - 26, H - 26], outline=FRAME, width=3)
d.rectangle([36, 36, W - 36, H - 36], outline=RED, width=1)

def center(text, f, y, fill, tracking=0):
    if tracking:
        widths = []
        for ch in text:
            bb = d.textbbox((0, 0), ch, font=f)
            widths.append(bb[2] - bb[0])
        tw = sum(widths) + tracking * (len(text) - 1)
        x = (W - tw) / 2
        for ch, w in zip(text, widths):
            bb = d.textbbox((0, 0), ch, font=f)
            d.text((x - bb[0], y), ch, font=f, fill=fill)
            x += w + tracking
        return tw
    bb = d.textbbox((0, 0), text, font=f)
    d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], y), text, font=f, fill=fill)
    return bb[2] - bb[0]

# plate mark
center("NO. 256 SALMON BROOK  ·  GRANBY, CONNECTICUT", mono(21), 78, SLUG, tracking=3)

# brand, two colors on one line WITH a real gap before CAFÉ
f_big, f_acc = serif(108), serif(88)
name = "Vintage Press"
nb = d.textbbox((0, 0), name, font=f_big)
cb = d.textbbox((0, 0), "CAFÉ", font=f_acc)
GAP = 34
nw, cw = nb[2] - nb[0], cb[2] - cb[0]
x = (W - (nw + GAP + cw)) / 2
y1 = 148
d.text((x - nb[0], y1), name, font=f_big, fill=PAPER)
d.text((x + nw + GAP - cb[0], y1 + 16), "CAFÉ", font=f_acc, fill=RED)

# tagline — single normal space
center("Vintage vibes. Modern brews.", serif(44), 302, PAPER)

# red rule
d.rectangle([(W - 260) / 2, 382, (W + 260) / 2, 385], fill=RED)

# offerings line
center("Specialty coffee  ·  Loose-leaf tea  ·  Breakfast & lunch", serif(30), 408, PAPER)

# bottom band — INSIDE the frame, with clearance for the border and descenders
bx0, by0, bx1, by1 = 44, 480, W - 44, 576
d.rectangle([bx0, by0, bx1, by1], fill=BAND)
d.rectangle([bx0, by0, bx1, by1], outline=(94, 80, 58), width=1)
center("OPEN EVERY DAY  ·  7 A.M. – 2 P.M.", mono(24), 496, GOLD, tracking=3)
center("hello@vintagepresscafe.com", mono(21), 534, SLUG, tracking=0)

img.save(OUT, "PNG", optimize=True)
print("og.png", img.size, os.path.getsize(OUT) // 1024, "KB")
