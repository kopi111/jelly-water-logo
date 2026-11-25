"""Lays out the 600 mL bottle wrap label around a design's front panel.

All coordinates are millimetres. The artwork is 225 x 75 mm at trim plus 3 mm bleed on
every side. Left to right on the wrap: back panel, front panel, side panel, glue overlap.
"""
from build_logos import BLACK, GOLD, GREEN, SHARED_DEFINITIONS

BLEED = 3
TRIM_WIDTH, TRIM_HEIGHT = 225, 75
WIDTH, HEIGHT = TRIM_WIDTH + 2 * BLEED, TRIM_HEIGHT + 2 * BLEED
PIXELS_PER_MILLIMETRE = 4

BACK_PANEL = (3, 73)
FRONT_PANEL = (73, 148)
SIDE_PANEL = (148, 218)
GLUE_OVERLAP = (218, 228)
BAND_TOP = 70

BENEFITS = [
    "Naturally hydrating",
    "Packed with electrolytes",
    "Rich in potassium",
    "Low in calories",
    "No added sugar",
    "Fat free",
    "Great after exercise",
]

def text(x, y, content, size, weight=600, fill=BLACK, anchor="start", family="Poppins", spacing=0):
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-weight="{weight}" font-size="{size}" '
        f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{spacing}">{content}</text>'
    )


def centre_of(panel):
    return (panel[0] + panel[1]) / 2


def background(design):
    return f"""
  <rect width="{WIDTH}" height="{HEIGHT}" fill="{design.paper}"/>
  <rect y="{BAND_TOP}" width="{WIDTH}" height="{HEIGHT - BAND_TOP}" fill="{design.band}"/>
  <rect y="{BAND_TOP}" width="{WIDTH}" height="0.8" fill="{design.accent}"/>
  <rect x="{GLUE_OVERLAP[0]}" width="{WIDTH - GLUE_OVERLAP[0]}" height="{HEIGHT}" fill="{design.paper}"/>"""


def benefit_line(x, y, content, design):
    return f"""
  <circle cx="{x + 1.8}" cy="{y - 1.1}" r="1.8" fill="{design.warning_ink}"/>
  <path d="M{x + 0.9} {y - 1.1} L{x + 1.55} {y - 0.4} L{x + 2.75} {y - 1.95}" fill="none" stroke="#FFFFFF"
        stroke-width="0.5" stroke-linecap="round" stroke-linejoin="round"/>
  {text(x + 5.2, y, content, 3.2, 600, design.ink)}"""


def back_panel(design):
    left = BACK_PANEL[0] + 6
    centre = centre_of(BACK_PANEL)
    lines = "".join(benefit_line(left, 25 + index * 6.2, benefit, design) for index, benefit in enumerate(BENEFITS))
    return f"""
  {text(left, 15, f'Why Coconut <tspan fill="{design.warning_ink}">Water?</tspan>', 4.4, 800, design.ink)}{lines}
  {text(centre, 75.4, design.back_band_text, 2.6, 700, design.band_ink, "middle", spacing=0.6)}"""


PROMISE_LINES = [
    "At Nature Fresh, we believe in using",
    "food as medicine and medicine as",
    "food. That is why we guarantee all",
    "our products are 100% natural.",
]
ORDER_PHONE = "(876) 464-4762"


def our_promise(x, design):
    lines = "".join(
        f"\n  {text(x, 40.5 + index * 5.8, line, 3.3, 400, design.ink)}" for index, line in enumerate(PROMISE_LINES)
    )
    return f"""
  {text(x, 33, "OUR PROMISE", 3.8, 800, design.warning_ink)}{lines}"""


def side_panel(design):
    left = SIDE_PANEL[0] + 5
    centre = centre_of(SIDE_PANEL)
    ink = design.ink
    return f"""
  {text(left, 9, "INGREDIENTS: Coconut water (100%).", 2.4, 700, ink)}
  {text(left, 14.4, "KEEP REFRIGERATED (0–4 °C). SHAKE WELL.", 2.4, 800, design.warning_ink)}
  <rect x="{left}" y="17.8" width="3" height="3.2" fill="{BLACK}"/>
  <rect x="{left + 3}" y="17.8" width="3" height="3.2" fill="{GOLD}"/>
  <rect x="{left + 6}" y="17.8" width="3" height="3.2" fill="{GREEN}"/>
  {text(left + 11, 20.6, "PRODUCT OF JAMAICA", 2.8, 800, ink)}
  {our_promise(left, design)}
  {text(centre, 75.4, design.side_band_text, 2.6, 700, design.band_ink, "middle", spacing=0.6)}"""


def proof_guides():
    panel_edges = [FRONT_PANEL[0], SIDE_PANEL[0], GLUE_OVERLAP[0]]
    dividers = "".join(
        f'<line x1="{x}" y1="0" x2="{x}" y2="{HEIGHT}" stroke="#2F6BFF" stroke-width="0.25" stroke-dasharray="1.5 1"/>'
        for x in panel_edges
    )
    labels = "".join(
        text(centre_of(panel), 1.9, name, 1.6, 700, "#2F6BFF", "middle")
        for panel, name in [(BACK_PANEL, "BACK"), (FRONT_PANEL, "FRONT"), (SIDE_PANEL, "SIDE"),
                            (GLUE_OVERLAP, "GLUE")]
    )
    return f"""
  <rect x="{BLEED}" y="{BLEED}" width="{TRIM_WIDTH}" height="{TRIM_HEIGHT}" fill="none" stroke="#E53935"
        stroke-width="0.3" stroke-dasharray="2 1"/>
  {dividers}{labels}"""


def label_document(design, with_guides):
    guides = proof_guides() if with_guides else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}"
     width="{WIDTH * PIXELS_PER_MILLIMETRE}" height="{HEIGHT * PIXELS_PER_MILLIMETRE}">
<defs>{SHARED_DEFINITIONS}{design.definitions}</defs>{background(design)}{design.front()}{back_panel(design)}{side_panel(design)}{guides}
</svg>
"""
