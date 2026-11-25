"""Builds all ten label designs, renders them to PNG and lays them out on one contact sheet."""
import html
import tempfile
from pathlib import Path

from PIL import Image

from build_label import label_document
from label_designs import DESIGNS
from render_png import render, screenshot

PROJECT_DIRECTORY = Path(__file__).parent
SVG_DIRECTORY = PROJECT_DIRECTORY / "svg" / "labels"
PNG_DIRECTORY = PROJECT_DIRECTORY / "png" / "labels"
SHEET_WIDTH, SHEET_HEIGHT = 1800, 2460
SHEET_SCALE = 1.5


def write_design(design):
    path = SVG_DIRECTORY / f"label-{design.slug}.svg"
    path.write_text(label_document(design, with_guides=False))
    return path


def design_card(design, png_path):
    number = design.slug.split("-")[0]
    return f"""
    <figure>
      <img src="{png_path.name}" alt="{html.escape(design.name)} label">
      <figcaption><b>{number} · {html.escape(design.name)}</b><span>{html.escape(design.strategy)}</span></figcaption>
    </figure>"""


def contact_sheet_html(cards):
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700;800&display=block" rel="stylesheet">
<style>
  body {{ margin: 0; width: {SHEET_WIDTH}px; height: {SHEET_HEIGHT}px; background: #F3F1EC;
         font-family: Poppins, sans-serif; color: #1B1B1B; }}
  header {{ padding: 36px 48px 8px; }}
  h1 {{ margin: 0; font-size: 40px; font-weight: 800; }}
  header p {{ margin: 4px 0 0; font-size: 18px; color: #555; }}
  main {{ display: grid; grid-template-columns: 1fr 1fr; gap: 28px 36px; padding: 24px 48px; }}
  figure {{ margin: 0; background: #FFF; border-radius: 14px; padding: 14px; box-shadow: 0 2px 8px rgba(0,0,0,.08); }}
  img {{ width: 100%; display: block; border-radius: 6px; }}
  figcaption {{ margin-top: 10px; font-size: 15px; line-height: 1.4; }}
  figcaption b {{ display: block; font-size: 20px; margin-bottom: 2px; }}
  figcaption span {{ color: #555; }}
</style></head><body>
<header><h1>Jelly Water · 600 mL label options</h1>
<p>Back panel · Front panel · Side panel, flat as printed. Pick a number.</p></header>
<main>{"".join(cards)}</main></body></html>
"""


def render_contact_sheet(html_path):
    sheet_path = PNG_DIRECTORY / "contact-sheet.png"
    with tempfile.TemporaryDirectory() as temporary_directory:
        raw_path = Path(temporary_directory) / "raw.png"
        screenshot(html_path, SHEET_WIDTH, SHEET_HEIGHT, raw_path, SHEET_SCALE)
        Image.open(raw_path).crop((0, 0, int(SHEET_WIDTH * SHEET_SCALE), int(SHEET_HEIGHT * SHEET_SCALE))).save(sheet_path)
    print(sheet_path)


def main():
    SVG_DIRECTORY.mkdir(parents=True, exist_ok=True)
    PNG_DIRECTORY.mkdir(parents=True, exist_ok=True)
    cards = [design_card(design, render(write_design(design), PNG_DIRECTORY)) for design in DESIGNS]
    html_path = PNG_DIRECTORY / "contact-sheet.html"
    html_path.write_text(contact_sheet_html(cards))
    render_contact_sheet(html_path)


if __name__ == "__main__":
    main()
