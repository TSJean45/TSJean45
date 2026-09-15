import math
import random

import os

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')

random.seed(45)

W, H = 1000, 300

GOLD = "#f2c14e"
GOLD_DEEP = "#c98f2b"
TEAL = "#3fd8d0"
TEAL_DEEP = "#1fa3a0"
VIOLET = "#a55ce0"
PINK = "#ff5fa2"
CORAL = "#ff7a59"
SAND = "#f4e9d6"


def sine_path(amp, wavelen, ybase, width, phase=0.0, step=10):
    """Seamless sine band, drawn twice as wide so it can loop by translation."""
    pts = []
    x = 0
    while x <= width * 2:
        y = ybase + amp * math.sin((x / wavelen) * 2 * math.pi + phase)
        pts.append(("M%.1f,%.1f" % (x, y)) if x == 0 else ("L%.1f,%.1f" % (x, y)))
        x += step
    pts.append("L%.1f,%d" % (width * 2, H))
    pts.append("L0,%d Z" % H)
    return " ".join(pts)


# ---------------------------------------------------------------- glitter
sparkles = []
for i in range(38):
    x = random.uniform(20, W - 20)
    y = random.uniform(18, H - 70)
    s = random.uniform(0.28, 1.05)
    dur = random.uniform(1.6, 4.2)
    delay = random.uniform(0, 4.2)
    col = random.choice([GOLD, SAND, TEAL, PINK, "#ffffff", VIOLET])
    spin = random.choice([0, 45, 90])
    sparkles.append(
        '  <g transform="translate(%.1f,%.1f) rotate(%d)">\n'
        '    <use href="#spk" fill="%s" opacity="0.95">\n'
        '      <animateTransform attributeName="transform" type="scale" values="0;%.2f;0"'
        ' dur="%.2fs" begin="%.2fs" repeatCount="indefinite"/>\n'
        '      <animate attributeName="opacity" values="0;1;0" dur="%.2fs" begin="%.2fs" repeatCount="indefinite"/>\n'
        "    </use>\n"
        "  </g>" % (x, y, spin, col, s, dur, delay, dur, delay)
    )

# ---------------------------------------------------------------- bubbles
bubbles = []
for i in range(22):
    x = random.uniform(15, W - 15)
    r = random.uniform(1.6, 5.4)
    dur = random.uniform(7, 15)
    delay = random.uniform(0, 15)
    drift = random.uniform(-26, 26)
    op = random.uniform(0.25, 0.7)
    bubbles.append(
        '  <circle cx="%.1f" cy="%d" r="%.2f" fill="none" stroke="%s" stroke-width="1" opacity="0">\n'
        '    <animate attributeName="cy" from="%d" to="-20" dur="%.1fs" begin="%.1fs" repeatCount="indefinite"/>\n'
        '    <animate attributeName="cx" values="%.1f;%.1f;%.1f" dur="%.1fs" begin="%.1fs" repeatCount="indefinite"/>\n'
        '    <animate attributeName="opacity" values="0;%.2f;%.2f;0" keyTimes="0;0.2;0.8;1" dur="%.1fs" begin="%.1fs" repeatCount="indefinite"/>\n'
        "  </circle>"
        % (
            x, H + 12, r, random.choice([TEAL, SAND, GOLD]),
            H + 12, dur, delay,
            x, x + drift, x, dur, delay,
            op, op, dur, delay,
        )
    )

# ---------------------------------------------------------------- sunburst
rays = []
for i in range(14):
    a = i * (360.0 / 14)
    rays.append(
        '    <polygon points="0,0 -9,-460 9,-460" fill="url(#rayGrad)" opacity="%.2f" transform="rotate(%.1f)"/>'
        % (0.5 if i % 2 == 0 else 0.22, a)
    )

# ---------------------------------------------------------------- caustics
caustics = []
for i in range(6):
    y = random.uniform(40, H - 80)
    amp = random.uniform(4, 11)
    wl = random.uniform(120, 260)
    dur = random.uniform(9, 18)
    d_pts = []
    x = 0
    while x <= W:
        d_pts.append(
            ("M%.0f,%.1f" % (x, y + amp * math.sin(x / wl * 6.28)))
            if x == 0
            else ("L%.0f,%.1f" % (x, y + amp * math.sin(x / wl * 6.28)))
        )
        x += 14
    caustics.append(
        '  <path d="%s" fill="none" stroke="%s" stroke-width="1.4" stroke-linecap="round"\n'
        '        opacity="0.3" stroke-dasharray="26 46">\n'
        '    <animate attributeName="stroke-dashoffset" values="0;-720" dur="%.1fs" repeatCount="indefinite"/>\n'
        '    <animate attributeName="opacity" values="0.14;0.42;0.14" dur="%.1fs" repeatCount="indefinite"/>\n'
        "  </path>" % (" ".join(d_pts), random.choice([SAND, GOLD, TEAL]), dur, dur * 0.6)
    )

NL = "\n"

TPL = r"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 __W__ __H__" width="__W__" height="__H__" role="img" aria-label="Tan Szu Jean - Waveflair">
<defs>
  <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#03141f"/>
    <stop offset="38%" stop-color="#06364a"/>
    <stop offset="72%" stop-color="#0a6a72"/>
    <stop offset="100%" stop-color="#128a86"/>
  </linearGradient>
  <linearGradient id="rayGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#f2c14e" stop-opacity="0.55"/>
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
  <radialGradient id="sunGlow" cx="50%" cy="50%">
    <stop offset="0%" stop-color="#f2c14e" stop-opacity="0.5"/>
    <stop offset="100%" stop-color="#f2c14e" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="violetGlow" cx="50%" cy="50%">
    <stop offset="0%" stop-color="#a55ce0" stop-opacity="0.38"/>
    <stop offset="100%" stop-color="#a55ce0" stop-opacity="0"/>
  </radialGradient>

  <path id="spk" d="M0,-7 Q1.1,-1.1 7,0 Q1.1,1.1 0,7 Q-1.1,1.1 -7,0 Q-1.1,-1.1 0,-7"/>

  <filter id="glowS" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="glowL" x="-80%" y="-80%" width="260%" height="260%">
    <feGaussianBlur stdDeviation="10" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="blur22"><feGaussianBlur stdDeviation="22"/></filter>

  <clipPath id="frame"><rect x="0" y="0" width="__W__" height="__H__" rx="12"/></clipPath>
  <clipPath id="nameClip">
    <text x="500" y="126" text-anchor="middle" font-family="Georgia,'Times New Roman',serif"
          font-size="55" font-weight="bold" letter-spacing="13">TAN SZU JEAN</text>
  </clipPath>
</defs>

<g clip-path="url(#frame)">
  <rect width="__W__" height="__H__" fill="url(#sea)"/>

  <!-- sunburst -->
  <g transform="translate(500,26)" opacity="0.5">
__RAYS__
    <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                      additive="sum" dur="140s" repeatCount="indefinite"/>
  </g>
  <ellipse cx="500" cy="20" rx="260" ry="130" fill="url(#sunGlow)" filter="url(#blur22)">
    <animate attributeName="opacity" values="0.65;1;0.65" dur="7s" repeatCount="indefinite"/>
  </ellipse>
  <ellipse cx="150" cy="250" rx="240" ry="120" fill="url(#violetGlow)" filter="url(#blur22)">
    <animate attributeName="cx" values="150;300;150" dur="20s" repeatCount="indefinite"/>
  </ellipse>

  <!-- peacock-feather eye (Aventurine's sigil) -->
  <g transform="translate(886,86)" opacity="0.5">
    <ellipse rx="42" ry="54" fill="none" stroke="#1fa3a0" stroke-width="1.4" opacity="0.7"/>
    <ellipse rx="29" ry="38" fill="none" stroke="#a55ce0" stroke-width="1.4" opacity="0.7"/>
    <ellipse rx="17" ry="23" fill="#f2c14e" opacity="0.28"/>
    <circle r="6" fill="#ff5fa2" opacity="0.8" filter="url(#glowS)">
      <animate attributeName="r" values="6;9;6" dur="3.4s" repeatCount="indefinite"/>
    </circle>
    <animateTransform attributeName="transform" type="rotate" values="-6;6;-6" additive="sum" dur="11s" repeatCount="indefinite"/>
  </g>

  <!-- spinning IPC coin -->
  <g transform="translate(112,92)">
    <g filter="url(#glowS)">
      <ellipse rx="22" ry="22" fill="#f2c14e" opacity="0.9">
        <animate attributeName="rx" values="22;2;22;2;22" dur="4.2s" repeatCount="indefinite"/>
      </ellipse>
      <ellipse rx="15" ry="15" fill="none" stroke="#7a4d10" stroke-width="1.6" opacity="0.65">
        <animate attributeName="rx" values="15;1;15;1;15" dur="4.2s" repeatCount="indefinite"/>
      </ellipse>
    </g>
  </g>

  <!-- dice: quantum purple, drifting -->
  <g transform="translate(196,214)" opacity="0.75">
    <rect x="-13" y="-13" width="26" height="26" rx="6" fill="#a55ce0" opacity="0.55" stroke="#f4e9d6" stroke-width="1.2"/>
    <circle cx="-5" cy="-5" r="2.1" fill="#f4e9d6"/><circle cx="5" cy="5" r="2.1" fill="#f4e9d6"/>
    <circle cx="0" cy="0" r="2.1" fill="#f4e9d6"/>
    <animateTransform attributeName="transform" type="rotate" from="0" to="360" additive="sum" dur="17s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="translate" values="0,0;0,-9;0,0" additive="sum" dur="6s" repeatCount="indefinite"/>
  </g>

__CAUSTICS__

__BUBBLES__

  <!-- layered waves -->
  <g>
    <path d="__WAVE_C__" fill="url(#waveC)" opacity="0.55">
      <animateTransform attributeName="transform" type="translate" from="0,0" to="-__W__,0" dur="19s" repeatCount="indefinite"/>
    </path>
    <path d="__WAVE_B__" fill="url(#waveB)" opacity="0.7">
      <animateTransform attributeName="transform" type="translate" from="0,0" to="-__W__,0" dur="13s" repeatCount="indefinite"/>
    </path>
    <path d="__WAVE_A__" fill="url(#waveA)">
      <animateTransform attributeName="transform" type="translate" from="0,0" to="-__W__,0" dur="9s" repeatCount="indefinite"/>
    </path>
  </g>

__SPARKLES__

  <!-- name -->
  <g filter="url(#glowS)">
    <text x="502" y="128" text-anchor="middle" font-family="Georgia,'Times New Roman',serif"
          font-size="55" font-weight="bold" letter-spacing="13" fill="#03141f" opacity="0.45">TAN SZU JEAN</text>
    <text x="500" y="126" text-anchor="middle" font-family="Georgia,'Times New Roman',serif"
          font-size="55" font-weight="bold" letter-spacing="13" fill="url(#goldName)">TAN SZU JEAN</text>
  </g>
  <g clip-path="url(#nameClip)">
    <rect x="-320" y="70" width="300" height="80" fill="url(#shimmer)">
      <animate attributeName="x" values="-320;1000" dur="4.5s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- rule + subtitles -->
  <g>
    <line x1="268" y1="152" x2="452" y2="152" stroke="#f2c14e" stroke-width="1" opacity="0.6"/>
    <line x1="548" y1="152" x2="732" y2="152" stroke="#f2c14e" stroke-width="1" opacity="0.6"/>
    <g transform="translate(500,152)" filter="url(#glowS)">
      <use href="#spk" fill="#fff6dc">
        <animateTransform attributeName="transform" type="scale" values="1;1.7;1" dur="2.4s" repeatCount="indefinite"/>
      </use>
    </g>
    <text x="500" y="186" text-anchor="middle" font-family="'Courier New',monospace" font-size="14.5"
          letter-spacing="5" fill="#f4e9d6" opacity="0.95">SOFTWARE ENGINEER &#183; AI ENTHUSIAST &#183; OPEN SOURCE</text>
    <text x="500" y="212" text-anchor="middle" font-family="'Courier New',monospace" font-size="12.5"
          letter-spacing="3" fill="#3fd8d0" opacity="0.92">KUALA LUMPUR, MALAYSIA</text>
  </g>

  <rect x="0" y="0" width="__W__" height="3" fill="#f2c14e" opacity="0.85"/>
  <rect x="0.5" y="0.5" width="999" height="299" rx="12" fill="none" stroke="#f2c14e" stroke-width="1" opacity="0.5"/>
</g>
</svg>
"""

svg = TPL
svg = svg.replace("__W__", str(W)).replace("__H__", str(H))
svg = svg.replace("__RAYS__", NL.join(rays))
svg = svg.replace("__CAUSTICS__", NL.join(caustics))
svg = svg.replace("__BUBBLES__", NL.join(bubbles))
svg = svg.replace("__SPARKLES__", NL.join(sparkles))
svg = svg.replace("__WAVE_A__", sine_path(11, 300, 258, W, 0.0))
svg = svg.replace("__WAVE_B__", sine_path(15, 380, 268, W, 1.9))
svg = svg.replace("__WAVE_C__", sine_path(9, 230, 276, W, 3.4))

with open(os.path.join(ASSETS, 'header.svg'), "w", encoding="utf-8") as f:
    f.write(svg)
print("header.svg written:", len(svg), "bytes")
