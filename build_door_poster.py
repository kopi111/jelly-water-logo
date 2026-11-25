"""Builds the "Natural Coconut Water Sold Here" door poster at US Letter and 18 x 24 inches.

The artwork is laid out once on a Letter-sized grid and scaled up for larger paper. The colours,
coconut and logos come from the label code, so the poster always matches the bottle.
Exports a PNG and PDF for each size, plus a PDF with bleed for a print shop that trims the poster.

The layout follows shop-sign research: one short message at the top where people look,
sized to read from about ten feet, the product as the main picture, and the price beside it.
"""
import tempfile
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from build_label import ORDER_PHONE, text
from build_label_8x2 import export_pdf, print_page
from build_logos import BLACK, DEEP_GREEN, GOLD, SHARED_DEFINITIONS
from build_nature_fresh_logo import nature_fresh_logo_centred
from label_designs import coconut_at
from render_png import screenshot

OUTPUT_DIRECTORY = Path.home() / "Desktop/Images/Jelly Water Logo/Jelly Water Door Poster"
FILE_STEM = "Jelly-Water-Door-Poster"
WHITE = "#FFFFFF"
CREAM = "#FFF8DC"

# The artwork grid: US Letter in millimetres. Larger paper scales this grid up.
WIDTH, HEIGHT = 215.9, 279.4
CENTRE = WIDTH / 2

# Colour that reaches the page edge is drawn this far past the grid, so any paper shape stays covered.
EDGE_OVERHANG = 20

# The gold "SOLD HERE" band runs edge to edge straight under the headline.
BAND_TOP = 84
BAND_HEIGHT = 42

# The bottle is drawn on a 100 x 300 grid, then scaled to its size on the page.
BOTTLE_ARTWORK_WIDTH, BOTTLE_ARTWORK_HEIGHT = 100, 300
BOTTLE_CENTRE = 52
BOTTLE_HEIGHT = 141
BOTTLE_BASE = 272
BOTTLE_LABEL_TOP, BOTTLE_LABEL_HEIGHT = 100, 145
BOTTLE_OUTLINE = (
    "M38 29 L62 29 C62 52 92 60 92 96 L92 276 Q92 298 70 298 "
    "L30 298 Q8 298 8 276 L8 96 C8 60 38 52 38 29 Z"
)

# Everything to the right of the bottle lines up on this column.
COLUMN_LEFT = 106
COLUMN_RIGHT = 204
COLUMN_CENTRE = (COLUMN_LEFT + COLUMN_RIGHT) / 2

# The white write-in price box: left, top, width, height.
PRICE_BOX = (COLUMN_LEFT, 133, COLUMN_RIGHT - COLUMN_LEFT, 42)

# The three selling points, all taken from the label's benefits list.
BENEFITS = ["Naturally hydrating", "Natural electrolytes", "No added sugar"]
BENEFITS_TOP = 189
BENEFITS_GAP = 13

# Gradients only the bottle uses: pale coconut water, and the shading that makes the label look round.
BOTTLE_DEFINITIONS = """
  <linearGradient id="bottleLiquid" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#CFE5B0"/>
    <stop offset="0.45" stop-color="#FAFDF0"/>
    <stop offset="1" stop-color="#C2DDA2"/>
  </linearGradient>
  <linearGradient id="bottleCurve" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#000000" stop-opacity="0.28"/>
    <stop offset="0.22" stop-color="#000000" stop-opacity="0"/>
    <stop offset="0.3" stop-color="#FFFFFF" stop-opacity="0.2"/>
    <stop offset="0.42" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="0.8" stop-color="#000000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000000" stop-opacity="0.32"/>
  </linearGradient>
"""

# Chrome lays pages out at 96 dots per inch; a PNG's scale multiplies that up.
SCREEN_DPI = 96


@dataclass(frozen=True)
class PaperSize:
    """One paper size to export, and how to fit the artwork grid onto it."""

    file_suffix: str
    width_inches: float
    height_inches: float
    bleed_inches: float = 0

    @property
    def page_width_inches(self):
        """The full page width, including any bleed on both sides."""
        return self.width_inches + 2 * self.bleed_inches

    @property
    def page_height_inches(self):
        """The full page height, including any bleed at top and bottom."""
        return self.height_inches + 2 * self.bleed_inches

    @property
    def view_box(self):
        """The part of the artwork to show: centred up and down, with the bleed around it."""
        grid_units_per_inch = WIDTH / self.width_inches
        bleed = self.bleed_inches * grid_units_per_inch
        trimmed_height = self.height_inches * grid_units_per_inch
        top_padding = (trimmed_height - HEIGHT) / 2
        return f"{-bleed} {-top_padding - bleed} {WIDTH + 2 * bleed} {trimmed_height + 2 * bleed}"


LETTER = PaperSize("", 8.5, 11)
LARGE = PaperSize("-18x24", 18, 24)
LARGE_WITH_BLEED = PaperSize("-18x24-print-shop-with-bleed", 18, 24, bleed_inches=0.125)

# Each PNG size with its scale: 3.125 x 96 gives 300 dpi, and 1.5625 x 96 gives 150 dpi.
PNG_EXPORTS = [(LETTER, 3.125), (LARGE, 1.5625)]
PDF_EXPORTS = [LETTER, LARGE, LARGE_WITH_BLEED]


def full_width_bar(y, height, colour):
    """A strip of colour that runs past both edges of the page."""
    return f'<rect x="{-EDGE_OVERHANG}" y="{y}" width="{WIDTH + 2 * EDGE_OVERHANG}" height="{height}" fill="{colour}"/>'


def background():
    """The same green gradient as the front of the label, across the whole page and past its edges."""
    return full_width_bar(-EDGE_OVERHANG, HEIGHT + 2 * EDGE_OVERHANG, "url(#husk)")


def headline():
    """The product name in big type, reading straight down into SOLD HERE."""
    return f"""
  {text(CENTRE, 48, "Natural", 44, 700, WHITE, "middle", "Fredoka")}
  {text(CENTRE, 76, "Coconut Water", 27, 700, GOLD, "middle", "Fredoka")}"""


def sold_here_band():
    """The gold band that tells people they can buy it at this door."""
    baseline = BAND_TOP + BAND_HEIGHT - 8.5
    return f"""
  {full_width_bar(BAND_TOP, BAND_HEIGHT, GOLD)}
  {full_width_bar(BAND_TOP - 1.4, 1.4, BLACK)}
  {full_width_bar(BAND_TOP + BAND_HEIGHT, 1.4, BLACK)}
  {text(CENTRE, baseline, "SOLD HERE", 36, 800, BLACK, "middle")}"""


def natural_seal(x, y):
    """The cream 100% Natural seal from the label, drawn at poster size."""
    return f"""
  <circle cx="{x}" cy="{y}" r="17" fill="{CREAM}"/>
  <circle cx="{x}" cy="{y}" r="15.4" fill="none" stroke="{GOLD}" stroke-width="1.1"/>
  {text(x, y + 1, "100%", 9.6, 700, DEEP_GREEN, "middle", "Fredoka")}
  {text(x, y + 7.4, "NATURAL", 3.4, 800, DEEP_GREEN, "middle", spacing=0.25)}"""


def bottle_cap_and_body():
    """The gold ribbed cap, its neck ring, and the clear bottle filled with pale coconut water."""
    ribs = "".join(
        f'<line x1="{x}" y1="3" x2="{x}" y2="22" stroke="#D4AE00" stroke-width="1.6"/>' for x in range(38, 66, 5)
    )
    return f"""
    <rect x="33" y="0" width="34" height="24" rx="3" fill="{GOLD}"/>{ribs}
    <rect x="30" y="24" width="40" height="5" rx="2" fill="#D4AE00"/>
    <path d="{BOTTLE_OUTLINE}" fill="url(#bottleLiquid)"/>
    <path d="M22 84 Q24 62 40 46" fill="none" stroke="{WHITE}" stroke-width="5" stroke-linecap="round" stroke-opacity="0.9"/>
    <path d="M20 258 L20 282" fill="none" stroke="{WHITE}" stroke-width="5" stroke-linecap="round" stroke-opacity="0.9"/>"""


def bottle_label():
    """The green front of the label wrapped around the bottle, shaded so it looks curved."""
    return f"""
    <rect x="8" y="{BOTTLE_LABEL_TOP}" width="84" height="{BOTTLE_LABEL_HEIGHT}" fill="url(#husk)"/>
    <rect x="8" y="{BOTTLE_LABEL_TOP}" width="84" height="2.5" fill="{GOLD}"/>
    <rect x="8" y="{BOTTLE_LABEL_TOP + BOTTLE_LABEL_HEIGHT - 2.5}" width="84" height="2.5" fill="{GOLD}"/>
    {nature_fresh_logo_centred(50, 106, 11, WHITE, GOLD)}
    <circle cx="50" cy="146" r="22" fill="url(#sun)"/>
    {coconut_at(50, 125, 40)}
    {text(50, 198, "Jelly", 27, 700, WHITE, "middle", "Fredoka")}
    {text(50, 215, "WATER", 12, 800, GOLD, "middle", spacing=1.5)}
    {text(50, 236, "600 mL", 13, 800, WHITE, "middle")}
    <rect x="8" y="{BOTTLE_LABEL_TOP}" width="84" height="{BOTTLE_LABEL_HEIGHT}" fill="url(#bottleCurve)"/>"""


def bottle():
    """The whole 600 mL bottle, placed as the main picture on the left."""
    scale = BOTTLE_HEIGHT / BOTTLE_ARTWORK_HEIGHT
    left = BOTTLE_CENTRE - scale * BOTTLE_ARTWORK_WIDTH / 2
    top = BOTTLE_BASE - BOTTLE_HEIGHT
    return f"""
  <g transform="translate({left} {top}) scale({scale})">{bottle_cap_and_body()}{bottle_label()}
  </g>"""


def product_picture():
    """The bottle in front of a gold sun, with the 100% Natural seal by its neck."""
    return f"""
  <circle cx="{BOTTLE_CENTRE}" cy="205" r="46" fill="url(#sun)"/>
  {bottle()}
  {natural_seal(84, 156)}"""


def price_box():
    """A white box with J$ and a blank line, beside the bottle, so the price can be written in with a marker."""
    left, top, width, height = PRICE_BOX
    line_y = top + height - 7.5
    return f"""
  <rect x="{left}" y="{top}" width="{width}" height="{height}" rx="3" fill="{WHITE}"/>
  <rect x="{left}" y="{top}" width="{width}" height="{height}" rx="3" fill="none" stroke="{BLACK}" stroke-width="0.9"/>
  {text(left + 4.5, top + 7, "600 mL BOTTLE", 4.6, 800, DEEP_GREEN, spacing=0.4)}
  {text(left + 4.5, line_y, "J$", 17, 800, BLACK)}
  <line x1="{left + 28}" y1="{line_y}" x2="{left + width - 6}" y2="{line_y}" stroke="{BLACK}" stroke-width="0.6"/>"""


def benefit_line(y, words):
    """One selling point: a gold circle with a tick, then the words in white."""
    x = COLUMN_LEFT
    return f"""
  <circle cx="{x + 3.6}" cy="{y - 2.5}" r="3.6" fill="{GOLD}"/>
  <path d="M{x + 1.8} {y - 2.5} L{x + 3.1} {y - 1.1} L{x + 5.5} {y - 4.1}" fill="none" stroke="{DEEP_GREEN}"
        stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/>
  {text(x + 10.5, y, words, 7.5, 700, WHITE)}"""


def benefit_list():
    """The three selling points under the price box."""
    return "".join(benefit_line(BENEFITS_TOP + index * BENEFITS_GAP, words) for index, words in enumerate(BENEFITS))


def contact_block():
    """The ordering phone number and the Nature Fresh logo, at the foot of the column."""
    return f"""
  {text(COLUMN_CENTRE, 233, "CONTACT US TO ORDER", 4.4, 800, GOLD, "middle", spacing=0.8)}
  {text(COLUMN_CENTRE, 247, ORDER_PHONE, 12.5, 800, WHITE, "middle")}
  {nature_fresh_logo_centred(COLUMN_CENTRE, 254, 14, WHITE, GOLD)}"""


def poster_svg(paper):
    """The whole poster as one SVG, sized to the given paper."""
    sections = [background(), headline(), sold_here_band(), product_picture(), price_box(), benefit_list(), contact_block()]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{paper.view_box}" width="{paper.page_width_inches}in" height="{paper.page_height_inches}in">
<defs>{SHARED_DEFINITIONS}{BOTTLE_DEFINITIONS}</defs>{"".join(sections)}
</svg>
"""


def write_page(paper, directory):
    """Saves the poster as a web page whose paper size matches, and returns its path."""
    page_path = Path(directory) / f"poster{paper.file_suffix}.html"
    page_path.write_text(print_page(poster_svg(paper), paper.page_width_inches, paper.page_height_inches))
    return page_path


def export_png(paper, scale, directory):
    """Takes a screenshot of the poster at the given scale and crops it to exactly the paper size."""
    width, height = int(paper.page_width_inches * SCREEN_DPI), int(paper.page_height_inches * SCREEN_DPI)
    raw_path = Path(directory) / f"raw{paper.file_suffix}.png"
    screenshot(write_page(paper, directory), width, height, raw_path, scale)
    size = (int(width * scale), int(height * scale))
    dots_per_inch = round(SCREEN_DPI * scale)
    output_path = OUTPUT_DIRECTORY / f"{FILE_STEM}{paper.file_suffix}.png"
    Image.open(raw_path).crop((0, 0, *size)).save(output_path, dpi=(dots_per_inch, dots_per_inch))
    print(output_path, size)


def main():
    """Writes every PNG and PDF to the Desktop folder."""
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary_directory:
        for paper, scale in PNG_EXPORTS:
            export_png(paper, scale, temporary_directory)
        for paper in PDF_EXPORTS:
            export_pdf(write_page(paper, temporary_directory), OUTPUT_DIRECTORY / f"{FILE_STEM}{paper.file_suffix}.pdf")


if __name__ == "__main__":
    main()
