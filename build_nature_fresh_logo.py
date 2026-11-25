"""Builds the Nature Fresh company logo: a green leaf on a gold sun, followed by the name.

Run this file to export a full-colour logo and a white-on-green logo, as SVG and PNG.
The label imports nature_fresh_logo() so the label and the logo files always match.
"""
from pathlib import Path

from build_label import text
from build_logos import DEEP_GREEN, GOLD, GREEN, SHARED_DEFINITIONS
from render_png import render

OUTPUT_DIRECTORY = Path.home() / "Desktop/Images/Jelly Water Logo/Nature Fresh Logo"
MARK_ARTWORK_SIZE = 100

# Size of the exported logo files, in pixels before the render scale is applied.
FILE_WIDTH, FILE_HEIGHT = 850, 260
FILE_MARGIN = 30

# How wide the whole logo is, as a multiple of its symbol size (measured from the render).
LOGO_WIDTH_PER_SIZE = 3.93


def leaf_mark(x, y, size):
    """The symbol alone: gold sun, green leaf with a white vein, and a small water drop."""
    scale = size / MARK_ARTWORK_SIZE
    return f"""
  <g transform="translate({x} {y}) scale({scale})">
    <circle cx="50" cy="50" r="50" fill="url(#sun)"/>
    <path d="M20 80 C14 42 42 16 84 14 C87 54 60 86 20 80 Z" fill="{GREEN}"/>
    <path d="M52 47 C70 34 84 14 84 14 C87 54 60 86 20 80 C30 72 42 58 52 47 Z" fill="{DEEP_GREEN}"/>
    <path d="M20 80 Q44 58 68 30" fill="none" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round"/>
    <path d="M38 63 L36 47 M50 51 L49 35 M38 63 L55 65 M50 51 L66 52" fill="none" stroke="#FFFFFF"
          stroke-width="2.4" stroke-linecap="round"/>
    <path d="M79 66 q9 13 0 20 q-9 -7 0 -20 Z" fill="#7FD3F0"/>
  </g>"""


def nature_fresh_logo_centred(centre_x, y, size, nature_ink, fresh_ink):
    """The full logo placed so its middle sits on centre_x."""
    return nature_fresh_logo(centre_x - size * LOGO_WIDTH_PER_SIZE / 2, y, size, nature_ink, fresh_ink)


def nature_fresh_logo(x, y, size, nature_ink, fresh_ink):
    """The full logo: the symbol at (x, y), then the name to its right in two colours."""
    font_size = size * 0.42
    name = f'Nature <tspan fill="{fresh_ink}">Fresh</tspan>'
    return f"""{leaf_mark(x, y, size)}
  {text(x + size * 1.14, y + size * 0.65, name, font_size, 800, nature_ink)}"""


def logo_file(background_rectangle, nature_ink, fresh_ink):
    """One complete SVG file holding the logo on the given background."""
    logo = nature_fresh_logo(FILE_MARGIN, FILE_MARGIN, FILE_HEIGHT - 2 * FILE_MARGIN, nature_ink, fresh_ink)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {FILE_WIDTH} {FILE_HEIGHT}" width="{FILE_WIDTH}" height="{FILE_HEIGHT}">
<defs>{SHARED_DEFINITIONS}</defs>{background_rectangle}{logo}
</svg>
"""


def main():
    """Writes both versions of the logo as SVG, then renders each one to PNG."""
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    green_background = f'<rect width="{FILE_WIDTH}" height="{FILE_HEIGHT}" fill="{GREEN}"/>'
    versions = {
        "nature-fresh-logo": logo_file("", DEEP_GREEN, GREEN),
        "nature-fresh-logo-on-green": logo_file(green_background, "#FFFFFF", GOLD),
    }
    for name, svg in versions.items():
        svg_path = OUTPUT_DIRECTORY / f"{name}.svg"
        svg_path.write_text(svg)
        render(svg_path, OUTPUT_DIRECTORY)


if __name__ == "__main__":
    main()
