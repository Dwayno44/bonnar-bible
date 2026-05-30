"""Generate PWA app icons: a Scott Bonnar green tile with a stylised reel-mower
cylinder (an end-on reel = ring + helical blades)."""
import math
import os
from PIL import Image, ImageDraw

GREEN = (31, 92, 58)
GREEN_D = (21, 64, 42)
GOLD = (200, 161, 58)
CREAM = (244, 241, 232)
HERE = os.path.dirname(__file__)


def draw_reel(d, cx, cy, r, blades=7, lw=3):
    # outer ring
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=lw)
    # hub
    hr = max(2, r * 0.12)
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=GOLD)
    # helical blades: arcs sweeping from hub outward
    for k in range(blades):
        base = (360 / blades) * k
        pts = []
        steps = 24
        for s in range(steps + 1):
            t = s / steps
            rad = hr + (r - hr) * t
            ang = math.radians(base + 55 * t)  # twist
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        d.line(pts, fill=GOLD, width=lw)


def make(size, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if maskable:
        # full-bleed background (safe zone ~80%)
        d.rectangle([0, 0, size, size], fill=GREEN)
        margin = size * 0.22
    else:
        # rounded square
        rad = int(size * 0.22)
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=rad, fill=GREEN)
        margin = size * 0.16
    cx = cy = size / 2
    r = (size / 2) - margin
    lw = max(2, int(size * 0.018))
    draw_reel(d, cx, cy, r, blades=7, lw=lw)
    return img


def main():
    out = HERE
    for name, size, mask in [
        ("icon-192.png", 192, False),
        ("icon-512.png", 512, False),
        ("icon-maskable-512.png", 512, True),
        ("apple-touch-icon.png", 180, False),
        ("favicon-32.png", 32, False),
    ]:
        make(size, mask).save(os.path.join(out, name))
        print("wrote", name)


if __name__ == "__main__":
    main()
