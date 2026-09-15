# Builds assets/hero.svg -- an inset banner card with four original chibi busts
# sitting on the transparent outer margin, overlapping the card's corners.

import math
import random

import os

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')

random.seed(45)

W, H = 1290, 467
CARD_X, CARD_Y, CARD_W, CARD_H = 155, 46, 980, 340

# ---- palette (direction taken from the user's reference sheet) ----
OUTLINE = "#3a2d1e"
HAIR = "#f5d98a"
HAIR_HI = "#fdf0c0"
HAIR_SH = "#e0b55c"
SKIN = "#ffe6d0"
SKIN_SH = "#f7c9aa"
SHIRT = "#c9ecf7"
SHIRT_SH = "#a5d9ea"
SUIT = "#fdfdf8"
SUIT_Y = "#ffe680"
TEAL = "#6fd8d0"
TEAL_D = "#1fa3a0"
VIOLET = "#b06fe8"
VIOLET_HI = "#e8a0ff"
VIOLET_D = "#5a2a7a"
GOLD = "#f2c14e"
GOLD_HI = "#fff6dc"
PINK = "#ff8fb3"
CORAL = "#ff7a59"
BLUE = "#4db8e8"

NL = "\n"


def crown_path(seed_key):
    """Messy spiked hair: walk the top arc alternating tip and valley radii,
    then close along a plain lower arc so the head still reads as a head."""
    rnd = random.Random(hash(seed_key) & 0xFFFF)
    pts = ["M-64,10"]
    steps = 11
    a0, a1 = 196.0, 344.0  # spikes only across the crown; sides stay smooth
    for i in range(steps + 1):
        t = a0 + (a1 - a0) * i / steps
        rad = math.radians(t)
        if i % 2 == 1:
            r = 70 + rnd.uniform(-4, 9)    # spike tip, swept outward
        else:
            r = 58 + rnd.uniform(-2, 3)    # valley between spikes
        px = math.cos(rad) * r * 1.06
        py = math.sin(rad) * r * 0.98
        pts.append("L%.1f,%.1f" % (px, py))
    # smooth sides and lower half, so it frames the face instead of radiating
    pts.append("L64,10")
    pts.append("Q72,30 58,46")
    pts.append("Q30,58 0,56")
    pts.append("Q-30,58 -58,46")
    pts.append("Q-72,30 -64,10")
    pts.append("Z")
    return " ".join(pts)


# ============================================================ chibi bust
def chibi(pose, x, y, scale, flip=False, delay=0.0):
    """One chibi bust. Origin of local coords is the centre of the head."""
    p = []
    a = p.append

    bob = 2.6 + (hash(pose) % 7) * 0.13
    sway = 4.4 + (hash(pose) % 5) * 0.21

    # ---- pose-specific extras drawn behind the body ----
    if pose == "ball":
        a('<g transform="translate(-100,98)">'
          '<circle r="44" fill="#f0cf86" stroke="%s" stroke-width="3.5"/>'
          '<g>'
          '  <path d="M0,-44 Q22,0 0,44 Q-8,0 0,-44 Z" fill="#e2bb6a" opacity="0.9"/>'
          '  <path d="M0,-44 Q-30,0 0,44 Q-40,0 -30,-26 Z" fill="#d9ad52" opacity="0.75"/>'
          '  <animateTransform attributeName="transform" type="rotate" from="0" to="360"'
          ' dur="16s" repeatCount="indefinite"/>'
          '</g>'
          '<circle r="44" fill="none" stroke="%s" stroke-width="3.5"/>'
          '<ellipse cx="-15" cy="-19" rx="12" ry="8" fill="#fff6dc" opacity="0.6"/>'
          '</g>' % (OUTLINE, OUTLINE))

    if pose == "gun":
        a('<g transform="translate(-104,104)">'
          '<rect x="-24" y="-34" width="44" height="30" rx="9" fill="%s" stroke="%s" stroke-width="3"/>'
          '<rect x="-14" y="-6" width="22" height="34" rx="8" fill="%s" stroke="%s" stroke-width="3"/>'
          '<rect x="14" y="-28" width="26" height="13" rx="6" fill="#8ad4f5" stroke="%s" stroke-width="3"/>'
          '<circle cx="-2" cy="-20" r="7" fill="#eaf8ff" stroke="%s" stroke-width="2.4"/>'
          '<g transform="translate(6,40)">'
          '  <ellipse rx="11" ry="9" fill="%s" stroke="%s" stroke-width="2.4"/>'
          '  <circle cx="6" cy="-8" r="6" fill="%s" stroke="%s" stroke-width="2.4"/>'
          '  <path d="M11,-9 L17,-7 L11,-5 Z" fill="%s"/>'
          '  <animateTransform attributeName="transform" type="rotate" values="-8;8;-8"'
          '   additive="sum" dur="2.4s" repeatCount="indefinite"/>'
          '</g>'
          '</g>' % (BLUE, OUTLINE, "#2f9fd6", OUTLINE, OUTLINE, OUTLINE,
                    SUIT_Y, OUTLINE, SUIT_Y, OUTLINE, CORAL))

    if pose == "drink":
        a('<g transform="translate(-86,104)">'
          '<path d="M-19,-42 L19,-42 L14,34 L-14,34 Z" fill="#fff4c9" stroke="%s" stroke-width="3"/>'
          '<path d="M-17,-18 L17,-18 L14,34 L-14,34 Z" fill="%s" opacity="0.92"/>'
          '<ellipse cy="-42" rx="19" ry="6" fill="#eaf8ff" stroke="%s" stroke-width="2.6"/>'
          '<rect x="6" y="-74" width="7" height="36" rx="3.5" fill="%s" stroke="%s" stroke-width="2.4"'
          ' transform="rotate(12,9,-56)"/>'
          '<path d="M-24,-46 Q-30,-56 -20,-58 Q-26,-48 -20,-46 Z" fill="%s" stroke="%s" stroke-width="2"/>'
          '<animateTransform attributeName="transform" type="rotate" values="-3;3;-3"'
          ' additive="sum" dur="3.2s" repeatCount="indefinite"/>'
          '</g>' % (OUTLINE, SUIT_Y, OUTLINE, TEAL, OUTLINE, TEAL, OUTLINE))

    # ---------------------------------------------------------- body
    a('<g>')
    a('  <animateTransform attributeName="transform" type="translate" values="0,0;0,-5;0,0"'
      ' dur="%.2fs" begin="%.2fs" repeatCount="indefinite"/>' % (bob, delay))

    # shoulders / open shirt
    a('  <path d="M-78,132 Q-72,64 0,58 Q72,64 78,132 Z" fill="%s" stroke="%s" stroke-width="3.5"'
      ' stroke-linejoin="round"/>' % (SHIRT, OUTLINE))
    a('  <path d="M-78,132 Q-74,82 -44,66 L-30,132 Z" fill="%s" opacity="0.6"/>' % SHIRT_SH)
    # swimsuit underneath
    a('  <path d="M-30,64 Q0,104 30,64 L30,132 L-30,132 Z" fill="%s" stroke="%s" stroke-width="3"'
      ' stroke-linejoin="round"/>' % (SUIT, OUTLINE))
    a('  <path d="M-30,112 L30,112 L30,132 L-30,132 Z" fill="%s" opacity="0.85"/>' % SUIT_Y)
    # collar
    a('  <path d="M-44,66 Q-26,92 -6,66" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>'
      % OUTLINE)
    a('  <path d="M44,66 Q26,92 6,66" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>'
      % OUTLINE)
    # beaded choker
    a('  <path d="M-24,62 Q0,74 24,62" fill="none" stroke="%s" stroke-width="3.4" stroke-linecap="round"/>'
      % OUTLINE)
    for i, c in enumerate([TEAL, CORAL, SUIT_Y, PINK, TEAL_D]):
        a('  <circle cx="%d" cy="%.1f" r="3.1" fill="%s"/>'
          % (-20 + i * 10, 66 + (0 if abs(-20 + i * 10) > 12 else 3), c))

    # ---------------------------------------------------------- arm + prop hand
    if pose == "ball":
        # forearm reaches under the ball; the cupped hand sits on its lower edge
        a('  <g transform="translate(-46,118)">'
          '    <path d="M0,0 Q-16,16 -30,18" fill="none" stroke="%s" stroke-width="17"'
          ' stroke-linecap="round"/>'
          '    <path d="M0,0 Q-16,16 -30,18" fill="none" stroke="%s" stroke-width="12"'
          ' stroke-linecap="round"/>'
          '    <path d="M-46,20 Q-36,6 -24,16 Q-34,26 -46,20 Z" fill="%s" stroke="%s"'
          ' stroke-width="3" stroke-linejoin="round"/>'
          '  </g>' % (OUTLINE, SKIN, SKIN, OUTLINE))
    if pose == "gun":
        a('  <g transform="translate(46,104)">'
          '    <path d="M0,0 Q22,-10 30,-28" fill="none" stroke="%s" stroke-width="17"'
          ' stroke-linecap="round"/>'
          '    <path d="M0,0 Q22,-10 30,-28" fill="none" stroke="%s" stroke-width="12"'
          ' stroke-linecap="round"/>'
          '    <circle cx="32" cy="-32" r="10" fill="%s" stroke="%s" stroke-width="3"/>'
          '    <animateTransform attributeName="transform" type="rotate" values="-3;3;-3"'
          ' additive="sum" dur="%.2fs" repeatCount="indefinite"/>'
          '  </g>' % (OUTLINE, SKIN, SKIN, OUTLINE, sway))
    if pose == "peace":
        a('  <g transform="translate(-48,108)">'
          '    <path d="M0,0 Q-20,-8 -28,-26" fill="none" stroke="%s" stroke-width="17"'
          ' stroke-linecap="round"/>'
          '    <path d="M0,0 Q-20,-8 -28,-26" fill="none" stroke="%s" stroke-width="12"'
          ' stroke-linecap="round"/>'
          '    <g transform="translate(-30,-32)">'
          '      <circle r="11" fill="%s" stroke="%s" stroke-width="3"/>'
          '      <rect x="-9" y="-24" width="7" height="18" rx="3.5" fill="%s" stroke="%s" stroke-width="2.6"/>'
          '      <rect x="2" y="-26" width="7" height="20" rx="3.5" fill="%s" stroke="%s" stroke-width="2.6"/>'
          '      <animateTransform attributeName="transform" type="rotate" values="-9;9;-9"'
          ' additive="sum" dur="1.8s" repeatCount="indefinite"/>'
          '    </g>'
          '  </g>' % (OUTLINE, SKIN, SKIN, OUTLINE, SKIN, OUTLINE, SKIN, OUTLINE))
    if pose == "drink":
        a('  <g transform="translate(-50,112)">'
          '    <path d="M0,0 Q-18,6 -30,0" fill="none" stroke="%s" stroke-width="17"'
          ' stroke-linecap="round"/>'
          '    <path d="M0,0 Q-18,6 -30,0" fill="none" stroke="%s" stroke-width="12"'
          ' stroke-linecap="round"/>'
          '    <circle cx="-34" cy="-1" r="10" fill="%s" stroke="%s" stroke-width="3"/>'
          '  </g>' % (OUTLINE, SKIN, SKIN, OUTLINE))

    # ---------------------------------------------------------- head
    a('  <g>')
    a('    <animateTransform attributeName="transform" type="rotate" values="-2.2;2.2;-2.2"'
      ' dur="%.2fs" begin="%.2fs" repeatCount="indefinite"/>' % (sway, delay))

    # outer hair silhouette: alternating long/short spikes around the crown
    a('    <path d="%s" fill="%s" stroke="%s" stroke-width="3.5" stroke-linejoin="round"/>'
      % (crown_path(pose), HAIR, OUTLINE))

    # face
    a('    <circle r="52" fill="%s" stroke="%s" stroke-width="3.5"/>' % (SKIN, OUTLINE))
    a('    <ellipse cx="-50" cy="8" rx="6" ry="9" fill="%s" stroke="%s" stroke-width="2.6"/>'
      % (SKIN_SH, OUTLINE))
    a('    <ellipse cx="50" cy="8" rx="6" ry="9" fill="%s" stroke="%s" stroke-width="2.6"/>'
      % (SKIN_SH, OUTLINE))
    # gold earring
    a('    <circle cx="52" cy="20" r="3.4" fill="%s" stroke="%s" stroke-width="1.8"/>' % (GOLD, OUTLINE))

    # fringe over the face
    a('    <g>')
    a('      <path d="M-56,-6 Q-54,-48 -18,-58 Q4,-68 26,-56 Q56,-46 58,-4'
      ' Q46,-26 30,-22 Q22,-6 14,-24 Q-2,-4 -10,-26 Q-26,-8 -34,-28 Q-48,-22 -56,-6 Z"'
      ' fill="%s" stroke="%s" stroke-width="3.2" stroke-linejoin="round"/>' % (HAIR, OUTLINE))
    a('      <path d="M8,-58 Q34,-58 48,-34 Q34,-44 14,-42 Z" fill="%s"/>' % HAIR_HI)
    a('      <path d="M-40,-40 Q-22,-52 -6,-46 Q-24,-42 -34,-30 Z" fill="%s"/>' % HAIR_HI)
    # long side lock + teal braid streak
    a('      <path d="M40,-30 Q66,-18 62,26 Q58,46 46,52 Q54,24 46,4 Z"'
      ' fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (HAIR_SH, OUTLINE))
    a('      <path d="M50,-14 Q60,6 54,34" fill="none" stroke="%s" stroke-width="4"'
      ' stroke-linecap="round" opacity="0.95"/>' % TEAL)
    a('      <path d="M55,-8 Q62,10 57,30" fill="none" stroke="%s" stroke-width="2"'
      ' stroke-linecap="round" opacity="0.7"/>' % TEAL_D)
    a('      <animateTransform attributeName="transform" type="rotate" values="-1.4;1.4;-1.4"'
      ' dur="%.2fs" repeatCount="indefinite"/>' % (sway * 0.78))
    a('    </g>')

    # sunglasses pushed up into the hair
    a('    <g transform="translate(0,-48)">')
    a('      <path d="M-40,2 L-8,2" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % GOLD)
    a('      <path d="M8,2 L40,2" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % GOLD)
    a('      <path d="M-40,-4 Q-38,14 -22,15 Q-8,15 -8,-2 Z" fill="url(#lens)"'
      ' stroke="%s" stroke-width="3.4" stroke-linejoin="round"/>' % GOLD)
    a('      <path d="M40,-4 Q38,14 22,15 Q8,15 8,-2 Z" fill="url(#lens)"'
      ' stroke="%s" stroke-width="3.4" stroke-linejoin="round"/>' % GOLD)
    a('      <path d="M-8,0 L8,0" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % GOLD)
    a('    </g>')

    # brows
    brow_l = 'M-32,-12 Q-22,-18 -12,-13'
    brow_r = 'M12,-13 Q22,-18 32,-12'
    if pose in ("peace", "drink"):
        brow_r = 'M12,-16 Q22,-20 32,-13'
    a('    <path d="%s" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (brow_l, HAIR_SH))
    a('    <path d="%s" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (brow_r, HAIR_SH))

    # ---- eyes: violet, ringed iris, in matching pairs ----
    def eye(ex, closed=False):
        if closed:
            return ('    <path d="M%d,4 Q%d,14 %d,4" fill="none" stroke="%s"'
                    ' stroke-width="3.4" stroke-linecap="round"/>' % (ex - 11, ex, ex + 11, OUTLINE))
        return (
            '    <g>'
            '<ellipse cx="%d" cy="6" rx="11" ry="14" fill="#fdf7ff" stroke="%s" stroke-width="3"/>'
            '<ellipse cx="%d" cy="6" rx="9" ry="12" fill="%s"/>'
            '<ellipse cx="%d" cy="6" rx="6.5" ry="9" fill="none" stroke="%s" stroke-width="2.6"/>'
            '<ellipse cx="%d" cy="7" rx="3.6" ry="5.4" fill="%s"/>'
            '<circle cx="%d" cy="1" r="3.2" fill="#ffffff"/>'
            '<circle cx="%d" cy="12" r="1.7" fill="#ffffff" opacity="0.75"/>'
            '<animate attributeName="ry" values="14;14;1.5;14;14" keyTimes="0;0.9;0.93;0.96;1"'
            ' dur="%.2fs" begin="%.2fs" repeatCount="indefinite"/>'
            '</g>'
            % (ex, OUTLINE, ex, VIOLET, ex, VIOLET_HI, ex, VIOLET_D,
               ex - 3, ex + 4, 5.2 + (hash(pose) % 4) * 0.3, delay)
        )

    if pose == "peace":
        a(eye(-22))
        a(eye(22, closed=True))
    elif pose == "gun":
        a(eye(-22, closed=True))
        a(eye(22))
    else:
        a(eye(-22))
        a(eye(22))

    # blush
    a('    <ellipse cx="-36" cy="24" rx="10" ry="5.6" fill="%s" opacity="0.5"/>' % PINK)
    a('    <ellipse cx="36" cy="24" rx="10" ry="5.6" fill="%s" opacity="0.5"/>' % PINK)

    # mouth
    if pose == "ball":
        a('    <path d="M-9,30 Q0,38 9,30" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % OUTLINE)
    elif pose == "gun":
        a('    <ellipse cy="33" rx="7" ry="8" fill="#b3543f" stroke="%s" stroke-width="2.6"/>' % OUTLINE)
    elif pose == "peace":
        a('    <path d="M-10,28 Q0,42 10,28 Z" fill="#b3543f" stroke="%s" stroke-width="2.8"'
          ' stroke-linejoin="round"/>' % OUTLINE)
        a('    <path d="M-10,28 L10,28" stroke="#fdfdf8" stroke-width="3" stroke-linecap="round"/>')
    else:
        a('    <path d="M-11,28 Q-2,42 8,28 Z" fill="#b3543f" stroke="%s" stroke-width="2.8"'
          ' stroke-linejoin="round"/>' % OUTLINE)
        a('    <path d="M2,32 L6,40 L9,31 Z" fill="#fdfdf8"/>')

    a('  </g>')  # head
    a('</g>')  # body

    # ---------------------------------------------------------- floating deco
    if pose == "ball":
        a('<g transform="translate(74,72)"><path d="M0,4 Q-9,-6 -4,-10 Q0,-12 0,-7'
          ' Q0,-12 4,-10 Q9,-6 0,4 Z" fill="%s">'
          '<animateTransform attributeName="transform" type="translate" values="0,0;0,-12;0,0"'
          ' dur="3.2s" repeatCount="indefinite"/>'
          '<animate attributeName="opacity" values="0.2;1;0.2" dur="3.2s" repeatCount="indefinite"/>'
          '</path></g>' % TEAL)
    if pose == "gun":
        for i, (sx, sy, sc, col, dl) in enumerate(
            [(-118, 10, 1.15, GOLD, 0.0), (96, -28, 0.85, GOLD_HI, 0.8), (110, 40, 0.65, TEAL, 1.6)]
        ):
            a('<g transform="translate(%d,%d)"><use href="#hspk" fill="%s">'
              '<animateTransform attributeName="transform" type="scale" values="0;%.2f;0"'
              ' dur="2.8s" begin="%.1fs" repeatCount="indefinite"/></use></g>' % (sx, sy, col, sc, dl))
    if pose == "peace":
        a('<g transform="translate(-58,-16)"><path d="M0,-10 Q7,0 0,10 Q-7,0 0,-10 Z"'
          ' fill="#9fdcf5" stroke="%s" stroke-width="2">'
          '<animate attributeName="opacity" values="0.35;1;0.35" dur="2.4s" repeatCount="indefinite"/>'
          '</path></g>' % OUTLINE)
        a('<g transform="translate(78,26)">'
          '<path d="M-2,0 Q14,8 26,0" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" opacity="0.7">'
          '<animate attributeName="opacity" values="0.2;0.8;0.2" dur="2s" repeatCount="indefinite"/>'
          '</path></g>' % TEAL_D)
    if pose == "drink":
        for i, (sx, sy, r, dl) in enumerate([(84, 66, 13, 0.0), (112, 34, 10, 0.7), (70, 20, 8, 1.4)]):
            a('<g transform="translate(%d,%d)">'
              '<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="#cdeefb" stroke="%s"'
              ' stroke-width="2.4" opacity="0.9">'
              '<animateTransform attributeName="transform" type="rotate" values="-12;12;-12"'
              ' additive="sum" dur="%.1fs" begin="%.1fs" repeatCount="indefinite"/>'
              '</rect></g>'
              % (sx, sy, -r // 2, -r // 2, r, r, OUTLINE, 3.0 + i * 0.4, dl))
        a('<g transform="translate(-104,16)"><path d="M0,4 Q-9,-6 -4,-10 Q0,-12 0,-7'
          ' Q0,-12 4,-10 Q9,-6 0,4 Z" fill="%s">'
          '<animate attributeName="opacity" values="0.25;1;0.25" dur="2.6s" repeatCount="indefinite"/>'
          '</path></g>' % TEAL)

    inner = NL.join("    " + ln for ln in p)
    tf = "translate(%.1f,%.1f) scale(%.3f)" % (x, y, scale)
    if flip:
        tf += " scale(-1,1)"
    return '  <g transform="%s">\n%s\n  </g>' % (tf, inner)


# ============================================================ banner interior
def sine_path(amp, wavelen, ybase, width, phase, bottom, step=10):
    pts = []
    xx = 0
    while xx <= width * 2:
        yy = ybase + amp * math.sin((xx / wavelen) * 2 * math.pi + phase)
        pts.append(("M%.1f,%.1f" % (xx, yy)) if xx == 0 else ("L%.1f,%.1f" % (xx, yy)))
        xx += step
    pts.append("L%.1f,%d" % (width * 2, bottom))
    pts.append("L0,%d Z" % bottom)
    return " ".join(pts)


card = []
ca = card.append
CB = CARD_Y + CARD_H  # card bottom

ca('    <rect x="%d" y="%d" width="%d" height="%d" rx="18" fill="url(#sea)"/>'
   % (CARD_X, CARD_Y, CARD_W, CARD_H))

# sunburst
rays = []
for i in range(14):
    ang = i * (360.0 / 14)
    rays.append('      <polygon points="0,0 -9,-470 9,-470" fill="url(#rayGrad)" opacity="%.2f"'
                ' transform="rotate(%.1f)"/>' % (0.5 if i % 2 == 0 else 0.2, ang))
ca('    <g transform="translate(%d,%d)" opacity="0.45">' % (CARD_X + CARD_W // 2, CARD_Y + 20))
ca(NL.join(rays))
ca('      <animateTransform attributeName="transform" type="rotate" from="0" to="360"'
   ' additive="sum" dur="150s" repeatCount="indefinite"/>')
ca('    </g>')
ca('    <ellipse cx="%d" cy="%d" rx="250" ry="120" fill="url(#sunGlow)" filter="url(#blur20)">'
   '<animate attributeName="opacity" values="0.6;1;0.6" dur="7s" repeatCount="indefinite"/></ellipse>'
   % (CARD_X + CARD_W // 2, CARD_Y + 14))

# caustics
for i in range(5):
    yv = random.uniform(CARD_Y + 40, CB - 90)
    amp = random.uniform(4, 10)
    wl = random.uniform(130, 250)
    dur = random.uniform(9, 17)
    dp = []
    xx = CARD_X
    while xx <= CARD_X + CARD_W:
        dp.append(("M%.0f,%.1f" % (xx, yv + amp * math.sin(xx / wl * 6.28)))
                  if xx == CARD_X else ("L%.0f,%.1f" % (xx, yv + amp * math.sin(xx / wl * 6.28))))
        xx += 14
    ca('    <path d="%s" fill="none" stroke="%s" stroke-width="1.4" stroke-linecap="round"'
       ' opacity="0.3" stroke-dasharray="26 46">'
       '<animate attributeName="stroke-dashoffset" values="0;-720" dur="%.1fs" repeatCount="indefinite"/>'
       '<animate attributeName="opacity" values="0.12;0.4;0.12" dur="%.1fs" repeatCount="indefinite"/>'
       '</path>' % (" ".join(dp), random.choice(["#f4e9d6", GOLD, "#3fd8d0"]), dur, dur * 0.6))

# bubbles
for i in range(18):
    bx = random.uniform(CARD_X + 15, CARD_X + CARD_W - 15)
    r = random.uniform(1.6, 5.0)
    dur = random.uniform(7, 14)
    dl = random.uniform(0, 14)
    dr = random.uniform(-24, 24)
    op = random.uniform(0.25, 0.65)
    ca('    <circle cx="%.1f" cy="%d" r="%.2f" fill="none" stroke="%s" stroke-width="1" opacity="0">'
       '<animate attributeName="cy" from="%d" to="%d" dur="%.1fs" begin="%.1fs" repeatCount="indefinite"/>'
       '<animate attributeName="cx" values="%.1f;%.1f;%.1f" dur="%.1fs" begin="%.1fs" repeatCount="indefinite"/>'
       '<animate attributeName="opacity" values="0;%.2f;%.2f;0" keyTimes="0;0.2;0.8;1" dur="%.1fs"'
       ' begin="%.1fs" repeatCount="indefinite"/></circle>'
       % (bx, CB, r, random.choice(["#3fd8d0", "#f4e9d6", GOLD]),
          CB, CARD_Y - 10, dur, dl, bx, bx + dr, bx, dur, dl, op, op, dur, dl))

# waves
ca('    <g transform="translate(%d,0)">' % CARD_X)
for grad, amp, wl, yb, ph, dur in [
    ("waveC", 9, 230, CB - 28, 3.4, 19),
    ("waveB", 15, 380, CB - 36, 1.9, 13),
    ("waveA", 11, 300, CB - 46, 0.0, 9),
]:
    ca('      <path d="%s" fill="url(#%s)">'
       '<animateTransform attributeName="transform" type="translate" from="0,0" to="-%d,0"'
       ' dur="%ds" repeatCount="indefinite"/></path>'
       % (sine_path(amp, wl, yb, CARD_W, ph, CB), grad, CARD_W, dur))
ca('    </g>')

# glitter inside the card
for i in range(30):
    # keep glitter out of the band the title and subtitles occupy
    for _attempt in range(40):
        sx = random.uniform(CARD_X + 24, CARD_X + CARD_W - 24)
        sy = random.uniform(CARD_Y + 18, CB - 60)
        in_text_band = (CARD_Y + 92 < sy < CARD_Y + 228) and abs(sx - (CARD_X + CARD_W / 2)) < 330
        if not in_text_band:
            break
    s = random.uniform(0.3, 1.0)
    dur = random.uniform(1.8, 4.2)
    dl = random.uniform(0, 4.2)
    col = random.choice([GOLD, "#f4e9d6", "#3fd8d0", "#ff5fa2", "#ffffff", "#a55ce0"])
    ca('    <g transform="translate(%.1f,%.1f)"><use href="#hspk" fill="%s">'
       '<animateTransform attributeName="transform" type="scale" values="0;%.2f;0" dur="%.2fs"'
       ' begin="%.2fs" repeatCount="indefinite"/>'
       '<animate attributeName="opacity" values="0;1;0" dur="%.2fs" begin="%.2fs"'
       ' repeatCount="indefinite"/></use></g>' % (sx, sy, col, s, dur, dl, dur, dl))

# title
TX = CARD_X + CARD_W // 2
ca('    <g filter="url(#glowS)">')
ca('      <text x="%d" y="%d" text-anchor="middle" font-family="Georgia,\'Times New Roman\',serif"'
   ' font-size="54" font-weight="bold" letter-spacing="12" fill="#03141f" opacity="0.45">TAN SZU JEAN</text>'
   % (TX + 2, CARD_Y + 134))
ca('      <text x="%d" y="%d" text-anchor="middle" font-family="Georgia,\'Times New Roman\',serif"'
   ' font-size="54" font-weight="bold" letter-spacing="12" fill="url(#goldName)">TAN SZU JEAN</text>'
   % (TX, CARD_Y + 132))
ca('    </g>')
ca('    <g clip-path="url(#nameClip)"><rect x="-320" y="%d" width="300" height="80" fill="url(#shimmer)">'
   '<animate attributeName="x" values="-320;1260" dur="4.5s" repeatCount="indefinite"/></rect></g>'
   % (CARD_Y + 76))
ca('    <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1" opacity="0.6"/>'
   % (TX - 232, CARD_Y + 158, TX - 48, CARD_Y + 158, GOLD))
ca('    <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1" opacity="0.6"/>'
   % (TX + 48, CARD_Y + 158, TX + 232, CARD_Y + 158, GOLD))
ca('    <g transform="translate(%d,%d)" filter="url(#glowS)"><use href="#hspk" fill="#fff6dc">'
   '<animateTransform attributeName="transform" type="scale" values="1;1.7;1" dur="2.4s"'
   ' repeatCount="indefinite"/></use></g>' % (TX, CARD_Y + 158))
ca('    <text x="%d" y="%d" text-anchor="middle" font-family="\'Courier New\',monospace"'
   ' font-size="14.5" letter-spacing="5" fill="#f4e9d6" opacity="0.95">'
   'SOFTWARE ENGINEER &#183; AI ENTHUSIAST &#183; OPEN SOURCE</text>' % (TX, CARD_Y + 192))
ca('    <text x="%d" y="%d" text-anchor="middle" font-family="\'Courier New\',monospace"'
   ' font-size="12.5" letter-spacing="3" fill="#3fd8d0" opacity="0.92">'
   'KUALA LUMPUR, MALAYSIA</text>' % (TX, CARD_Y + 218))

ca('    <rect x="%.1f" y="%.1f" width="%d" height="%d" rx="18" fill="none" stroke="%s"'
   ' stroke-width="2" opacity="0.65"/>' % (CARD_X + 0.5, CARD_Y + 0.5, CARD_W - 1, CARD_H - 1, GOLD))

# ============================================================ assemble
chibis = [
    chibi("ball", 121, 90, 0.56, flip=False, delay=0.0),
    chibi("gun", 1169, 90, 0.56, flip=True, delay=0.6),
    chibi("peace", 121, 316, 0.56, flip=False, delay=1.2),
    chibi("drink", 1169, 316, 0.56, flip=True, delay=1.8),
]

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 __W__ __H__" width="__W__" height="__H__" role="img" aria-label="Tan Szu Jean - Waveflair banner with four chibi mascots">
<defs>
  <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#03141f"/>
    <stop offset="38%" stop-color="#06364a"/>
    <stop offset="72%" stop-color="#0a6a72"/>
    <stop offset="100%" stop-color="#128a86"/>
  </linearGradient>
  <linearGradient id="rayGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#f2c14e" stop-opacity="0.5"/>
    <stop offset="100%" stop-color="#f2c14e" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="goldName" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#fff6dc"/>
    <stop offset="42%" stop-color="#f2c14e"/>
    <stop offset="72%" stop-color="#c98f2b"/>
    <stop offset="100%" stop-color="#fff0c4"/>
  </linearGradient>
  <linearGradient id="shimmer" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
    <stop offset="50%" stop-color="#ffffff" stop-opacity="0.85"/>
    <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="waveA" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#3fd8d0" stop-opacity="0.55"/>
    <stop offset="100%" stop-color="#1fa3a0" stop-opacity="0.15"/>
  </linearGradient>
  <linearGradient id="waveB" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#a55ce0" stop-opacity="0.4"/>
    <stop offset="100%" stop-color="#ff5fa2" stop-opacity="0.12"/>
  </linearGradient>
  <linearGradient id="waveC" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#f2c14e" stop-opacity="0.5"/>
    <stop offset="100%" stop-color="#ff7a59" stop-opacity="0.1"/>
  </linearGradient>
  <linearGradient id="lens" x1="0" y1="0" x2="0.3" y2="1">
    <stop offset="0%" stop-color="#ffe680"/>
    <stop offset="45%" stop-color="#7fd6ee"/>
    <stop offset="100%" stop-color="#4db8e8"/>
  </linearGradient>
  <radialGradient id="sunGlow" cx="50%" cy="50%">
    <stop offset="0%" stop-color="#f2c14e" stop-opacity="0.5"/>
    <stop offset="100%" stop-color="#f2c14e" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="pop" cx="50%" cy="50%">
    <stop offset="40%" stop-color="#ffffff" stop-opacity="0.07"/>
    <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
  </radialGradient>

  <path id="hspk" d="M0,-7 Q1.1,-1.1 7,0 Q1.1,1.1 0,7 Q-1.1,1.1 -7,0 Q-1.1,-1.1 0,-7"/>

  <filter id="glowS" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="blur20"><feGaussianBlur stdDeviation="20"/></filter>

  <clipPath id="cardClip"><rect x="__CX__" y="__CY__" width="__CW__" height="__CH__" rx="18"/></clipPath>
  <clipPath id="nameClip">
    <text x="__TX__" y="__TY__" text-anchor="middle" font-family="Georgia,'Times New Roman',serif"
          font-size="54" font-weight="bold" letter-spacing="12">TAN SZU JEAN</text>
  </clipPath>
</defs>

  <!-- soft haloes so the chibis read on light AND dark page backgrounds -->
  <circle cx="121" cy="121" r="112" fill="url(#pop)"/>
  <circle cx="1169" cy="121" r="112" fill="url(#pop)"/>
  <circle cx="121" cy="346" r="112" fill="url(#pop)"/>
  <circle cx="1169" cy="346" r="112" fill="url(#pop)"/>

  <g clip-path="url(#cardClip)">
__CARD__
  </g>

__CHIBIS__
</svg>
"""

SVG = (SVG.replace("__W__", str(W)).replace("__H__", str(H))
       .replace("__CX__", str(CARD_X)).replace("__CY__", str(CARD_Y))
       .replace("__CW__", str(CARD_W)).replace("__CH__", str(CARD_H))
       .replace("__TX__", str(TX)).replace("__TY__", str(CARD_Y + 132))
       .replace("__CARD__", NL.join(card))
       .replace("__CHIBIS__", NL.join(chibis)))

with open(os.path.join(ASSETS, 'hero.svg'), "w", encoding="utf-8") as f:
    f.write(SVG)
print("hero.svg written:", len(SVG), "bytes")

# Same banner with an empty corner slot, so build_hero_art.py can drop real
# artwork into the four corners instead of the drawn chibis.
BASE = SVG.replace(NL.join(chibis), "<!--CHIBI_SLOT-->")
with open(os.path.join(ASSETS, 'hero-base.svg'), "w", encoding="utf-8") as f:
    f.write(BASE)
print("hero-base.svg written:", len(BASE), "bytes")
