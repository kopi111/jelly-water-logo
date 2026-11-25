"""Builds the green Yaad Classic label at 8 x 2 inches, with a 100% Natural logo on the front.

All coordinates are millimetres. Exports go to OUTPUT_DIRECTORY as:
  - an exact 8 x 2 inch PNG, PDF and SVG (cut size)
  - a PDF with 3 mm bleed on every side, for a print shop that trims the label itself
"""
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

from build_label import BENEFITS, centre_of, text
from build_logos import BLACK, DEEP_GREEN, GOLD, GREEN, SHARED_DEFINITIONS
from build_nature_fresh_logo import nature_fresh_logo_centred
from label_designs import coconut_at
from render_png import screenshot

OUTPUT_DIRECTORY = Path.home() / "Desktop/Images/Jelly Water Logo/FINAL - Jelly Water Label 8x2 inch"
MILLIMETRES_PER_INCH = 25.4

# The label size: 8 x 2 inches when cut, plus extra colour past the cut line (bleed).
BLEED = 3
TRIM_WIDTH, TRIM_HEIGHT = 8 * MILLIMETRES_PER_INCH, 2 * MILLIMETRES_PER_INCH
WIDTH, HEIGHT = TRIM_WIDTH + 2 * BLEED, TRIM_HEIGHT + 2 * BLEED

# Where each panel sits across the wrap, left to right, and where the bottom band starts.
BACK_PANEL = (BLEED, 63)
FRONT_PANEL = (63, 137)
SIDE_PANEL = (137, 200.2)
GLUE_START = 200.2
BAND_TOP = 46.5
BAND_TEXT_BASELINE = 50.9

# Export settings: 6.25 x 96 screen dots per inch gives a 600 dpi PNG.
SCREEN_DPI = 96
PNG_SCALE = 6.25

# The promise is wrapped to four lines in larger type so it fills the space under the heading.
PROMISE_LINES = [
    "At Nature Fresh, we believe in using",
    "food as medicine and medicine as",
    "food. That is why we guarantee all",
    "our products are 100% natural.",
]


def background():
    """White paper, the green bottom band with its gold line, and a plain white glue flap."""
    return f"""
  <rect width="{WIDTH}" height="{HEIGHT}" fill="#FFFFFF"/>
  <rect y="{BAND_TOP}" width="{WIDTH}" height="{HEIGHT - BAND_TOP}" fill="{GREEN}"/>
  <rect y="{BAND_TOP}" width="{WIDTH}" height="0.6" fill="{GOLD}"/>
  <rect x="{GLUE_START}" width="{WIDTH - GLUE_START}" height="{HEIGHT}" fill="#FFFFFF"/>"""


def natural_logo(x, y):
    """The 100% Natural seal: a cream circle with a gold ring and the words only, no leaves."""
    return f"""
  <circle cx="{x}" cy="{y}" r="7.4" fill="#FFF8DC"/>
  <circle cx="{x}" cy="{y}" r="6.7" fill="none" stroke="{GOLD}" stroke-width="0.5"/>
  {text(x, y + 0.3, "100%", 4.2, 700, DEEP_GREEN, "middle", "Fredoka")}
  {text(x, y + 3.1, "NATURAL", 1.5, 800, GREEN, "middle", spacing=0.12)}"""


def front_panel():
    """Company logo at the top middle; coconut, name and Natural seal below it; then tagline and 600 mL."""
    left, right = FRONT_PANEL
    centre = centre_of(FRONT_PANEL)
    name_centre = left + 41
    return f"""
  <rect x="{left}" width="{right - left}" height="{HEIGHT}" fill="url(#husk)"/>
  <rect x="{left}" width="1" height="{HEIGHT}" fill="{GOLD}"/>
  <rect x="{right - 1}" width="1" height="{HEIGHT}" fill="{GOLD}"/>
  <circle cx="{left + 13}" cy="24.5" r="10.5" fill="url(#sun)"/>
  {coconut_at(left + 13, 14.7, 19.6)}
  {nature_fresh_logo_centred(centre, 5, 6.5, "#FFFFFF", GOLD)}
  {text(name_centre, 23, "Jelly", 11.5, 700, "#FFFFFF", "middle", "Fredoka")}
  {text(name_centre, 31, "WATER", 5.8, 800, GOLD, "middle", spacing=1)}
  {natural_logo(left + 64, 24.5)}
  {text(centre, 39.5, "100% PURE COCONUT WATER · NOTHING ADDED", 2.3, 600, "#FFFFFF", "middle", spacing=0.15)}
  {text(centre, 47.5, "600 mL", 5.6, 800, "#FFFFFF", "middle")}"""


def benefit_line(x, y, content):
    """One benefit: a green tick in a circle, then the words."""
    return f"""
  <circle cx="{x + 1.4}" cy="{y - 0.9}" r="1.4" fill="{GREEN}"/>
  <path d="M{x + 0.7} {y - 0.9} L{x + 1.2} {y - 0.35} L{x + 2.15} {y - 1.55}" fill="none" stroke="#FFFFFF"
        stroke-width="0.4" stroke-linecap="round" stroke-linejoin="round"/>
  {text(x + 4.2, y, content, 2.5, 600, BLACK)}"""


def back_panel():
    """The heading, the seven benefits, and the band wording."""
    left = BACK_PANEL[0] + 5
    centre = (left - 5 + BACK_PANEL[1]) / 2
    benefits = "".join(benefit_line(left, 16.8 + index * 4.25, benefit) for index, benefit in enumerate(BENEFITS))
    heading = f'Why Coconut <tspan fill="{GREEN}">Water?</tspan>'
    return f"""
  {text(left, 11.5, heading, 3.8, 800, BLACK)}{benefits}
  {text(centre, BAND_TEXT_BASELINE, "STRAIGHT FROM THE COCONUT", 2.2, 700, "#FFFFFF", "middle", spacing=0.45)}"""


def jamaica_line(x, y):
    """The small flag-colour blocks followed by PRODUCT OF JAMAICA."""
    blocks = "".join(
        f'<rect x="{x + index * 2.4}" y="{y - 2.1}" width="2.4" height="2.5" fill="{colour}"/>'
        for index, colour in enumerate([BLACK, GOLD, GREEN])
    )
    return f"""
  {blocks}
  {text(x + 9, y, "PRODUCT OF JAMAICA", 2.3, 800, BLACK)}"""


def side_panel():
    """Ingredients and storage, the promise, and the band wording."""
    left = SIDE_PANEL[0] + 4
    centre = centre_of(SIDE_PANEL)
    promise = "".join(
        f"\n  {text(left, 29 + index * 4.2, line, 3, 400, BLACK)}" for index, line in enumerate(PROMISE_LINES)
    )
    return f"""
  {text(left, 9.5, "INGREDIENTS: Coconut water (100%).", 2.1, 700, BLACK)}
  {text(left, 13, "KEEP REFRIGERATED (0–4 °C). SHAKE WELL.", 2, 800, GREEN)}
  {jamaica_line(left, 17.8)}
  {text(left, 23.6, "OUR PROMISE", 3, 800, GREEN)}{promise}
  {text(centre, BAND_TEXT_BASELINE, "FRESH · NATURAL · JAMAICAN", 2.2, 700, "#FFFFFF", "middle", spacing=0.45)}"""


def label_svg(view_box, width_inches, height_inches):
    """The whole label as SVG, showing only the part of the artwork inside view_box."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" width="{width_inches}in" height="{height_inches}in">
<defs>{SHARED_DEFINITIONS}</defs>{background()}{back_panel()}{front_panel()}{side_panel()}
</svg>
"""


def trim_svg():
    """The label cut to exactly 8 x 2 inches."""
    return label_svg(f"{BLEED} {BLEED} {TRIM_WIDTH} {TRIM_HEIGHT}", 8, 2)


def bleed_svg():
    """The label with the extra 3 mm of colour left on, for a print shop."""
    return label_svg(f"0 0 {WIDTH} {HEIGHT}", WIDTH / MILLIMETRES_PER_INCH, HEIGHT / MILLIMETRES_PER_INCH)


def print_page(svg, width_inches, height_inches):
    """Wraps the SVG in a web page whose paper size matches it, so Chrome can print it."""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: {width_inches}in {height_inches}in; margin: 0; }}
html, body {{ margin: 0; padding: 0; }}
svg {{ display: block; }}
</style></head><body>{svg}</body></html>
"""


def export_pdf(page_path, output_path):
    """Prints the web page to PDF with headless Chrome, waiting for the fonts to load."""
    subprocess.run(
        ["google-chrome", "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         "--virtual-time-budget=6000", f"--print-to-pdf={output_path}", page_path.as_uri()],
        check=True, capture_output=True,
    )
    print(output_path)


def export_png(page_path, output_path):
    """Takes a 600 dpi screenshot of the page and crops it to exactly 8 x 2 inches."""
    width, height = 8 * SCREEN_DPI, 2 * SCREEN_DPI
    with tempfile.TemporaryDirectory() as temporary_directory:
        raw_path = Path(temporary_directory) / "raw.png"
        screenshot(page_path, width, height, raw_path, PNG_SCALE)
        size = (int(width * PNG_SCALE), int(height * PNG_SCALE))
        Image.open(raw_path).crop((0, 0, *size)).save(output_path, dpi=(600, 600))
    print(output_path, size)


def main():
    """Writes the SVG, PNG and both PDFs to the Desktop folder."""
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIRECTORY / "Jelly-Water-Label-8x2.svg").write_text(trim_svg())
    with tempfile.TemporaryDirectory() as temporary_directory:
        trim_page = Path(temporary_directory) / "trim.html"
        bleed_page = Path(temporary_directory) / "bleed.html"
        trim_page.write_text(print_page(trim_svg(), 8, 2))
        bleed_page.write_text(print_page(bleed_svg(), WIDTH / MILLIMETRES_PER_INCH, HEIGHT / MILLIMETRES_PER_INCH))
        export_png(trim_page, OUTPUT_DIRECTORY / "Jelly-Water-Label-8x2.png")
        export_pdf(trim_page, OUTPUT_DIRECTORY / "Jelly-Water-Label-8x2.pdf")
        export_pdf(bleed_page, OUTPUT_DIRECTORY / "Jelly-Water-Label-8x2-print-shop-with-bleed.pdf")


if __name__ == "__main__":
    main()
