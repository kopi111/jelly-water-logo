"""Builds the Jelly Water logo concepts as SVG files."""
from pathlib import Path

OUTPUT_DIRECTORY = Path(__file__).parent / "svg"

GREEN = "#009B3A"
DEEP_GREEN = "#0B5D2A"
GOLD = "#FED100"
BLACK = "#111111"
CREAM = "#FFF8DC"

FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Fredoka:wght@600;700&amp;family=Poppins:wght@600;800&amp;display=block');"
)

SHARED_DEFINITIONS = f"""
  <style>{FONT_IMPORT}</style>
  <linearGradient id="husk" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#5CC55E"/>
    <stop offset="0.55" stop-color="{GREEN}"/>
    <stop offset="1" stop-color="{DEEP_GREEN}"/>
  </linearGradient>
  <radialGradient id="jelly" cx="0.45" cy="0.4" r="0.7">
    <stop offset="0" stop-color="#FFFFFF"/>
    <stop offset="1" stop-color="{CREAM}"/>
  </radialGradient>
  <radialGradient id="sun" cx="0.5" cy="0.45" r="0.6">
    <stop offset="0" stop-color="#FFE766"/>
    <stop offset="1" stop-color="{GOLD}"/>
  </radialGradient>
"""


def coconut(transform=""):
    """A young jelly coconut, machete-cut at the top, with a flag-striped straw."""
    return f"""
  <g transform="{transform}">
    <path d="M200 142 L246 52 Q250 44 259 44 L292 44" fill="none" stroke="{BLACK}"
          stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M200 142 L246 52 Q250 44 259 44 L292 44" fill="none" stroke="{GOLD}"
          stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M200 142 L246 52 Q250 44 259 44 L292 44" fill="none" stroke="{GREEN}"
          stroke-width="13" stroke-dasharray="9 13" stroke-linejoin="round"/>
    <path d="M129 135 C68 172 70 300 148 352 Q200 386 252 352 C330 300 332 172 271 135 Z"
          fill="url(#husk)"/>
    <path d="M128 185 Q116 250 150 315" fill="none" stroke="#FFFFFF" stroke-opacity="0.35"
          stroke-width="16" stroke-linecap="round"/>
    <circle cx="160" cy="175" r="7" fill="#FFFFFF" fill-opacity="0.5"/>
    <ellipse cx="200" cy="135" rx="71" ry="17" fill="#8FD16A"/>
    <ellipse cx="200" cy="134" rx="62" ry="13" fill="url(#jelly)"/>
    <ellipse cx="200" cy="135" rx="18" ry="5" fill="#CFE9B4"/>
    <path d="M318 120 q10 16 0 22 q-10 -6 0 -22z" fill="#7FD3F0"/>
    <path d="M82 150 q7 11 0 15 q-7 -4 0 -15z" fill="#7FD3F0"/>
  </g>"""


def svg_document(width, height, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
<defs>{SHARED_DEFINITIONS}
  <path id="ringTop" d="M60 300 A240 240 0 0 1 540 300"/>
  <path id="ringBottom" d="M78 300 A222 222 0 0 0 522 300"/>
</defs>{body}
</svg>
"""


def badge_logo():
    rays = "".join(
        f'<rect x="296" y="96" width="8" height="40" rx="4" fill="#FFF3A6" '
        f'transform="rotate({angle} 300 300)"/>'
        for angle in range(0, 360, 30)
    )
    body = f"""
  <circle cx="300" cy="300" r="290" fill="{BLACK}"/>
  <circle cx="300" cy="300" r="282" fill="none" stroke="{GOLD}" stroke-width="4"/>
  <circle cx="300" cy="300" r="200" fill="url(#sun)"/>
  {rays}
  <circle cx="300" cy="300" r="200" fill="none" stroke="{GREEN}" stroke-width="10"/>
  {coconut("translate(115 85) scale(0.93)")}
  <text font-family="Fredoka" font-weight="700" font-size="58" fill="{GOLD}" letter-spacing="6"
        text-anchor="middle"><textPath href="#ringTop" startOffset="50%">JELLY WATER</textPath></text>
  <text font-family="Poppins" font-weight="600" font-size="26" fill="#FFFFFF" letter-spacing="8"
        text-anchor="middle" dominant-baseline="hanging"><textPath href="#ringBottom" startOffset="50%">FRESH · JAMAICA</textPath></text>
  <circle cx="72" cy="300" r="7" fill="{GREEN}"/>
  <circle cx="528" cy="300" r="7" fill="{GREEN}"/>"""
    return svg_document(600, 600, body)


def horizontal_logo():
    body = f"""
  {coconut("translate(-10 20) scale(0.95)")}
  <text x="360" y="215" font-family="Fredoka" font-weight="700" font-size="170" fill="{GREEN}">Jelly</text>
  <path d="M368 245 q40 -18 80 0 t80 0 t80 0" fill="none" stroke="{GOLD}" stroke-width="12"
        stroke-linecap="round"/>
  <text x="366" y="330" font-family="Poppins" font-weight="800" font-size="70" fill="{BLACK}"
        letter-spacing="22">WATER</text>
  <text x="368" y="380" font-family="Poppins" font-weight="600" font-size="22" fill="{DEEP_GREEN}"
        letter-spacing="3">STRAIGHT FROM THE COCONUT · JAMAICA</text>"""
    return svg_document(1000, 420, body)


def drop_logo():
    body = f"""
  <path d="M300 30 C300 30 110 250 110 360 A190 190 0 0 0 490 360 C490 250 300 30 300 30Z"
        fill="url(#husk)"/>
  <path d="M300 30 C300 30 110 250 110 360 A190 190 0 0 0 490 360 C490 250 300 30 300 30Z"
        fill="none" stroke="{GOLD}" stroke-width="10"/>
  <path d="M235 150 Q190 205 160 270" fill="none" stroke="#FFFFFF" stroke-opacity="0.3"
        stroke-width="18" stroke-linecap="round"/>
  <circle cx="300" cy="370" r="125" fill="url(#sun)"/>
  {coconut("translate(178 245) scale(0.62)")}
  <text x="300" y="640" font-family="Fredoka" font-weight="700" font-size="92" fill="{GREEN}"
        text-anchor="middle">Jelly Water</text>
  <rect x="150" y="664" width="100" height="8" rx="4" fill="{BLACK}"/>
  <rect x="250" y="664" width="100" height="8" rx="4" fill="{GOLD}"/>
  <rect x="350" y="664" width="100" height="8" rx="4" fill="{GREEN}"/>
  <text x="300" y="712" font-family="Poppins" font-weight="600" font-size="26" fill="{BLACK}"
        text-anchor="middle" letter-spacing="10">100% JAMAICAN</text>"""
    return svg_document(600, 740, body)


LOGOS = {
    "jelly-water-badge": badge_logo,
    "jelly-water-horizontal": horizontal_logo,
    "jelly-water-drop": drop_logo,
}


def main():
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    for name, build in LOGOS.items():
        (OUTPUT_DIRECTORY / f"{name}.svg").write_text(build())
        print(OUTPUT_DIRECTORY / f"{name}.svg")


if __name__ == "__main__":
    main()
