"""Drop four real chibi images into the corners of the banner.

    python build_hero_art.py <folder-with-the-four-images>

Looks for chibi-1..chibi-4 (png/webp/jpg) in that folder, or just takes the
first four images it finds, sorted by name. Order is TL, TR, BL, BR.

Each image is background-stripped if needed, trimmed, scaled to a common box,
and embedded into assets/hero-art.svg as a base64 <image> that bobs and sways
the same way the drawn chibis do.
"""

import base64
import io
import os
import sys
from collections import deque

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

# corner anchor points in hero.svg coordinates (1260 x 470), and the flip flag
CORNERS = [
    ("top-left", 121, 121, False, 0.0),
    ("top-right", 1169, 121, False, 0.6),
    ("bottom-left", 121, 346, False, 1.2),
    ("bottom-right", 1169, 346, False, 1.8),
]

BOX = 215          # rendered size of the longest side, in hero coordinates
WHITE_CUT = 232    # channel value at or above which an edge pixel counts as background
RENDER_MAX = 560   # px; cap on the embedded bitmap's longest side


def strip_background(im):
    """Flood the background in from the edges so interior whites (the shirt,
    highlights, ice cubes) survive. Returns RGBA."""
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()

    # already has meaningful transparency? leave it alone
    alpha = im.getchannel("A")
    if alpha.getextrema()[0] < 250:
        return im

    seen = bytearray(w * h)
    q = deque()

    def is_bg(x, y):
        r, g, b, a = px[x, y]
        return r >= WHITE_CUT and g >= WHITE_CUT and b >= WHITE_CUT

    for x in range(w):
        for y in (0, h - 1):
            if not seen[y * w + x] and is_bg(x, y):
                seen[y * w + x] = 1
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not seen[y * w + x] and is_bg(x, y):
                seen[y * w + x] = 1
                q.append((x, y))

    while q:
        x, y = q.popleft()
        px[x, y] = (255, 255, 255, 0)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and is_bg(nx, ny):
                seen[ny * w + nx] = 1
                q.append((nx, ny))

    return im


def prepare(path, fmt):
    im = Image.open(path)
    im = strip_background(im)
    bbox = im.getchannel("A").getbbox()
    if bbox:
        im = im.crop(bbox)
    scale = RENDER_MAX / max(im.size)
    if scale < 1:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))),
                       Image.LANCZOS)
    buf = io.BytesIO()
    if fmt == "png8":
        # palette PNG: bigger than webp but decodes everywhere
        im.quantize(colors=256, method=Image.FASTOCTREE).save(buf, format="PNG", optimize=True)
        mime = "image/png"
    else:
        # webp carries this flat line art at roughly an eighth of PNG's weight
        im.save(buf, format="WEBP", quality=82, method=6)
        mime = "image/webp"
    return im.size, buf.getvalue(), mime


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fmt = "png8" if "--png8" in sys.argv else "webp"
    src = args[0] if args else ASSETS
    if not os.path.isdir(src):
        sys.exit("not a folder: %s" % src)

    exts = (".png", ".webp", ".jpg", ".jpeg")
    named = []
    for i in range(1, 5):
        for e in exts:
            p = os.path.join(src, "chibi-%d%s" % (i, e))
            if os.path.exists(p):
                named.append(p)
                break
    if len(named) < 4:
        found = sorted(f for f in os.listdir(src) if f.lower().endswith(exts))
        named = [os.path.join(src, f) for f in found[:4]]
    if len(named) < 4:
        sys.exit("need four images in %s, found %d" % (src, len(named)))

    base_path = os.path.join(ASSETS, "hero-base.svg")
    if not os.path.exists(base_path):
        sys.exit("run gen_hero.py first (hero-base.svg is missing)")
    svg = open(base_path, encoding="utf-8").read()

    groups = []
    for (label, cx, cy, flip, delay), path in zip(CORNERS, named):
        (iw, ih), data, mime = prepare(path, fmt)
        k = BOX / max(iw, ih)
        w, h = iw * k, ih * k
        b64 = base64.b64encode(data).decode("ascii")
        tf = "translate(%.1f,%.1f)" % (cx, cy)
        if flip:
            tf += " scale(-1,1)"
        groups.append(
            '  <g transform="%s">\n'
            '    <animateTransform attributeName="transform" type="translate"'
            ' values="0,0;0,-7;0,0" additive="sum" dur="%.2fs" begin="%.2fs"'
            ' repeatCount="indefinite"/>\n'
            '    <g>\n'
            '      <animateTransform attributeName="transform" type="rotate"'
            ' values="-2;2;-2" dur="%.2fs" begin="%.2fs" repeatCount="indefinite"/>\n'
            '      <image x="%.1f" y="%.1f" width="%.1f" height="%.1f"'
            ' href="data:%s;base64,%s"/>\n'
            '    </g>\n'
            '  </g>' % (tf, 2.8 + delay * 0.15, delay, 5.2 + delay * 0.2, delay,
                        -w / 2, -h / 2, w, h, mime, b64)
        )
        print("%-13s %-28s %dx%d  %.0f KB" % (label, os.path.basename(path), iw, ih, len(data) / 1024))

    out_svg = svg.replace("<!--CHIBI_SLOT-->", "\n".join(groups))
    out = os.path.join(ASSETS, "hero-art.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write(out_svg)
    print("\nhero-art.svg written: %.0f KB  (format: %s)" % (len(out_svg) / 1024, fmt))
    print("Point README.md at assets/hero-art.svg to use it.")


if __name__ == "__main__":
    main()
