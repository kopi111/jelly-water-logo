"""The ten Jelly Water label designs. Each one supplies its own front panel and colours;
the back and side panels are laid out by build_label."""
from dataclasses import dataclass
from typing import Callable

from build_label import FRONT_PANEL, HEIGHT, centre_of, text
from build_logos import BLACK, GOLD, GREEN, coconut

LEFT, RIGHT = FRONT_PANEL
CENTRE = centre_of(FRONT_PANEL)
PANEL_WIDTH = RIGHT - LEFT
COCONUT_ARTWORK_TOP, COCONUT_ARTWORK_HEIGHT = 44, 342

EXTRA_FONTS = (
    "<style>@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&amp;"
    "family=Playfair+Display:ital,wght@0,700;1,700&amp;family=Pacifico&amp;"
    "family=Archivo+Black&amp;display=block');</style>"
)


@dataclass(frozen=True)
class LabelDesign:
    slug: str
    name: str
    strategy: str
    paper: str
    ink: str
    accent: str
    band: str
    band_ink: str
    warning_ink: str
    front: Callable[[], str]
    back_band_text: str = "STRAIGHT FROM THE COCONUT"
    side_band_text: str = "FRESH · NATURAL · JAMAICAN"
    definitions: str = EXTRA_FONTS


def coconut_transform(cx, top, height):
    scale = height / COCONUT_ARTWORK_HEIGHT
    return f"translate({cx - 200 * scale} {top - COCONUT_ARTWORK_TOP * scale}) scale({scale})"


def coconut_at(cx, top, height):
    return coconut(coconut_transform(cx, top, height))


def coconut_line(cx, top, height, ink):
    stroke = 0.45 * COCONUT_ARTWORK_HEIGHT / height
    return f"""
  <g transform="{coconut_transform(cx, top, height)}" fill="none" stroke="{ink}" stroke-width="{stroke}"
     stroke-linecap="round" stroke-linejoin="round">
    <path d="M200 142 L246 52 Q250 44 259 44 L292 44"/>
    <path d="M129 135 C68 172 70 300 148 352 Q200 386 252 352 C330 300 332 172 271 135 Z"/>
    <ellipse cx="200" cy="135" rx="71" ry="17"/>
    <ellipse cx="200" cy="135" rx="18" ry="5"/>
    <path d="M128 185 Q116 250 150 315"/>
  </g>"""


def panel_fill(fill):
    return f'<rect x="{LEFT}" width="{PANEL_WIDTH}" height="{HEIGHT}" fill="{fill}"/>'


def edge_bars(colour, width=1.2):
    return (f'<rect x="{LEFT}" width="{width}" height="{HEIGHT}" fill="{colour}"/>'
            f'<rect x="{RIGHT - width}" width="{width}" height="{HEIGHT}" fill="{colour}"/>')


def net_content(y, colour, size=5.6, family="Poppins"):
    return text(CENTRE, y, "600 mL", size, 800, colour, "middle", family)


def flag_stripe(cx, y, width=12, height=1.2):
    third = width / 3
    left = cx - width / 2
    return "".join(
        f'<rect x="{left + index * third}" y="{y}" width="{third}" height="{height}" fill="{colour}"/>'
        for index, colour in enumerate([BLACK, GOLD, GREEN])
    )


def palm_frond(x, y, angle, length, colour):
    leaflets = []
    for step in range(2, 12):
        t = step / 12
        along = t * length
        droop = 0.18 * length * t * t
        leaflet = (1 - t) * 0.35 * length + 1
        for side in (-1, 1):
            leaflets.append(
                f'<line x1="{along}" y1="{droop}" x2="{along - leaflet * 0.35}" '
                f'y2="{droop + side * leaflet}" stroke="{colour}" stroke-width="0.55" stroke-linecap="round"/>'
            )
    spine = f'<path d="M0 0 Q{length / 2} {0.02 * length} {length} {0.18 * length}" fill="none" stroke="{colour}" stroke-width="0.8"/>'
    return f'<g transform="translate({x} {y}) rotate({angle})">{spine}{"".join(leaflets)}</g>'


def palm_tree(base_x, base_y, height, lean, colour):
    top_x, top_y = base_x + lean, base_y - height
    trunk = (f'<path d="M{base_x} {base_y} Q{base_x + lean * 0.2} {base_y - height * 0.5} {top_x} {top_y}" '
             f'fill="none" stroke="{colour}" stroke-width="1.6" stroke-linecap="round"/>')
    fronds = "".join(palm_frond(top_x, top_y, angle, height * 0.55, colour)
                     for angle in (-175, -140, -105, -70, -35, 0))
    return trunk + fronds


def wave(y, amplitude, wavelength, colour, opacity=1.0):
    points = [f"M{LEFT} {y}"]
    x = LEFT
    while x < RIGHT:
        points.append(f"q{wavelength / 4} {-amplitude} {wavelength / 2} 0 t{wavelength / 2} 0")
        x += wavelength
    return (f'<path d="{" ".join(points)} L{RIGHT + wavelength} {HEIGHT} L{LEFT} {HEIGHT} Z" '
            f'fill="{colour}" fill-opacity="{opacity}"/>')


def ring_text(cx, cy, radius, content, size, colour, path_id, family="Poppins", weight=700):
    return f"""
  <path id="{path_id}" d="M{cx - radius} {cy} A{radius} {radius} 0 1 1 {cx + radius} {cy}" fill="none"/>
  <text font-family="{family}" font-weight="{weight}" font-size="{size}" fill="{colour}" letter-spacing="0.5"
        text-anchor="middle"><textPath href="#{path_id}" startOffset="50%">{content}</textPath></text>"""


def purity_seal(x, y):
    return f"""
  <circle cx="{x}" cy="{y}" r="8" fill="{BLACK}"/>
  <circle cx="{x}" cy="{y}" r="7.1" fill="none" stroke="{GOLD}" stroke-width="0.5"/>
  {text(x, y + 1.3, "100%", 4.4, 700, GOLD, "middle", "Fredoka")}
  {text(x, y + 4.2, "PURE", 1.8, 800, "#FFFFFF", "middle", spacing=0.4)}
  {text(x, y - 3.2, "JAMAICAN", 1.3, 700, "#FFFFFF", "middle", spacing=0.2)}"""


def yaad_classic_front():
    return f"""
  <rect x="{LEFT}" width="{PANEL_WIDTH}" height="{HEIGHT}" fill="url(#husk)"/>
  {edge_bars(GOLD)}
  <circle cx="{CENTRE}" cy="23" r="16.5" fill="url(#sun)"/>
  {coconut_at(CENTRE, 7.5, 30.8)}
  {text(CENTRE, 51, "Jelly", 15, 700, "#FFFFFF", "middle", "Fredoka")}
  {text(CENTRE, 61.4, "WATER", 7.5, 800, GOLD, "middle", spacing=2.5)}
  {text(CENTRE, 66.2, "100% PURE COCONUT WATER · NOTHING ADDED", 2.5, 600, "#FFFFFF", "middle", spacing=0.2)}
  {net_content(74.6, "#FFFFFF")}
  {purity_seal(RIGHT - 12.5, 13)}"""


def pure_white_front():
    green = "#0F7A3A"
    return f"""
  {panel_fill("#FFFFFF")}
  <rect x="{LEFT}" width="0.4" height="{HEIGHT}" fill="#DDE7DF"/>
  <rect x="{RIGHT - 0.4}" width="0.4" height="{HEIGHT}" fill="#DDE7DF"/>
  {text(CENTRE, 11, "PRODUCT OF JAMAICA", 1.9, 600, "#7A8A7E", "middle", spacing=1.2)}
  {flag_stripe(CENTRE, 13.2, 9, 0.7)}
  {coconut_at(CENTRE, 18, 25)}
  {text(CENTRE, 53, "jelly water", 9.5, 600, green, "middle")}
  <rect x="{CENTRE - 10}" y="56" width="20" height="0.35" fill="{green}"/>
  {text(CENTRE, 61, "100% pure coconut water", 2.6, 400, "#55625A", "middle", spacing=0.4)}
  {text(CENTRE, 64.6, "nothing added · nothing taken away", 2.1, 400, "#8A968E", "middle", spacing=0.3)}
  {net_content(74.6, green, 4.6)}"""


def ocean_hydration_front():
    return f"""
  <defs><linearGradient id="ocean" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#00B4D8"/><stop offset="1" stop-color="#0353A4"/></linearGradient></defs>
  {panel_fill("url(#ocean)")}
  {wave(48, 2.5, 18, "#FFFFFF", 0.15)}
  {wave(55, 2, 14, "#FFFFFF", 0.15)}
  <circle cx="{CENTRE}" cy="23" r="15.5" fill="#FFFFFF"/>
  {coconut_at(CENTRE, 9, 28)}
  {text(CENTRE, 51.5, "Jelly Water", 10.5, 700, "#FFFFFF", "middle", "Fredoka")}
  {text(CENTRE, 57.5, "NATURE'S HYDRATION", 3, 800, GOLD, "middle", spacing=1)}
  {text(CENTRE, 62.4, "Natural electrolytes · 100% coconut water", 2.3, 500, "#FFFFFF", "middle")}
  {net_content(74.6, "#FFFFFF")}"""


def kraft_farm_front():
    ink = "#2B1D10"
    return f"""
  {panel_fill("#C9A47A")}
  <rect x="{LEFT + 3}" y="5" width="{PANEL_WIDTH - 6}" height="64" fill="none" stroke="{ink}" stroke-width="0.4"/>
  <rect x="{LEFT + 4}" y="6" width="{PANEL_WIDTH - 8}" height="62" fill="none" stroke="{ink}" stroke-width="0.2"/>
  <circle cx="{CENTRE}" cy="24" r="14.5" fill="none" stroke="{ink}" stroke-width="0.35" stroke-dasharray="0.9 0.6"/>
  {ring_text(CENTRE, 24, 12.2, "FARM TO BOTTLE · JAMAICA", 1.7, ink, "kraftRing")}
  {coconut_line(CENTRE, 15.5, 17, ink)}
  {text(CENTRE, 48.5, "JELLY", 11, 400, ink, "middle", "Archivo Black", 1)}
  {text(CENTRE, 57, "WATER", 7, 400, ink, "middle", "Archivo Black", 3.2)}
  {text(CENTRE, 62.6, "Hand-cut · Bottled fresh · Nothing added", 2.2, 600, ink, "middle")}
  {net_content(74.6, ink)}"""


def island_reserve_front():
    gold = "#D4AF37"
    return f"""
  {panel_fill("#0E0E0E")}
  <rect x="{LEFT + 3}" y="5" width="{PANEL_WIDTH - 6}" height="64" fill="none" stroke="{gold}" stroke-width="0.3"/>
  {text(CENTRE, 12, "ISLAND RESERVE", 2.2, 600, gold, "middle", spacing=2)}
  {coconut_line(CENTRE, 16, 22, gold)}
  {text(CENTRE, 50, "Jelly Water", 9.2, 700, gold, "middle", "Playfair Display")}
  <rect x="{CENTRE - 14}" y="53.4" width="28" height="0.3" fill="{gold}"/>
  {text(CENTRE, 58.6, "SINGLE ORIGIN · JAMAICA", 2.3, 600, "#F2E6C2", "middle", spacing=1.2)}
  {text(CENTRE, 62.6, "100% pure young coconut water", 2.1, 400, "#BFB28C", "middle", spacing=0.3)}
  {net_content(74.6, gold, 4.6, "Playfair Display")}"""


def sunset_tropical_front():
    silhouette = "#3A1F2B"
    return f"""
  <defs><linearGradient id="sunset" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FF5E62"/><stop offset="0.55" stop-color="#FF9966"/>
    <stop offset="1" stop-color="#FFD26F"/></linearGradient></defs>
  {panel_fill("url(#sunset)")}
  <circle cx="{CENTRE}" cy="30" r="14" fill="#FFE29A" fill-opacity="0.9"/>
  {palm_tree(LEFT + 9, 44, 26, 6, silhouette)}
  {palm_tree(RIGHT - 8, 44, 20, -5, silhouette)}
  {coconut_at(CENTRE, 14, 26)}
  <path d="M{LEFT} 44 Q{CENTRE} 40 {RIGHT} 44 L{RIGHT} 46 L{LEFT} 46 Z" fill="{silhouette}"/>
  {text(CENTRE, 56, "Jelly Water", 9.6, 400, "#FFFFFF", "middle", "Pacifico")}
  {text(CENTRE, 62.4, "ISLAND-FRESH COCONUT WATER", 2.5, 800, silhouette, "middle", spacing=0.8)}
  {net_content(74.6, silhouette)}"""


def dancehall_bold_front():
    lime = "#C6FF00"
    stripes = "".join(
        f'<path d="M{LEFT + offset} {HEIGHT} L{LEFT + offset + 30} 0 L{LEFT + offset + 34} 0 '
        f'L{LEFT + offset + 4} {HEIGHT} Z" fill="{lime}" fill-opacity="0.12"/>'
        for offset in range(-30, 80, 11)
    )
    return f"""
  <clipPath id="frontClip"><rect x="{LEFT}" width="{PANEL_WIDTH}" height="{HEIGHT}"/></clipPath>
  {panel_fill(BLACK)}
  <g clip-path="url(#frontClip)">{stripes}</g>
  {edge_bars(lime, 1.6)}
  <g transform="rotate(-12 {CENTRE + 16} 20)">{coconut_at(CENTRE + 16, 5, 25)}</g>
  {text(LEFT + 7, 30, "JELLY", 19, 400, lime, family="Bebas Neue", spacing=0.5)}
  {text(LEFT + 7, 48, "WATER", 19, 400, "#FFFFFF", family="Bebas Neue", spacing=0.5)}
  <rect x="{LEFT + 7}" y="52" width="{PANEL_WIDTH - 14}" height="6" fill="{GOLD}"/>
  {text(CENTRE, 56.4, "STRAIGHT OUTTA DI COCONUT", 3.4, 400, BLACK, "middle", "Bebas Neue", 1)}
  {text(CENTRE, 63, "100% PURE · NO SUGAR ADDED", 2.5, 700, lime, "middle", spacing=0.8)}
  {net_content(74.6, "#FFFFFF", 6.4, "Bebas Neue")}"""


def botanical_front():
    leaf = "#1E5A44"
    cream = "#F4EBD0"
    fronds = "".join(palm_frond(x, y, angle, 26, leaf) for x, y, angle in
                     [(LEFT - 2, 6, 20), (RIGHT + 2, 10, 160), (LEFT - 3, 48, -15), (RIGHT + 3, 58, 195)])
    return f"""
  <clipPath id="frontClip"><rect x="{LEFT}" width="{PANEL_WIDTH}" height="{HEIGHT}"/></clipPath>
  {panel_fill("#0F3D2E")}
  <g clip-path="url(#frontClip)">{fronds}</g>
  <ellipse cx="{CENTRE}" cy="37" rx="25" ry="31" fill="#0F3D2E" fill-opacity="0.85"/>
  {coconut_at(CENTRE, 10, 26)}
  {text(CENTRE, 47.5, "Jelly Water", 8.8, 700, cream, "middle", "Playfair Display")}
  {text(CENTRE, 53.2, "PURE JAMAICAN COCONUT WATER", 2.2, 600, "#C8D9B0", "middle", spacing=0.9)}
  {text(CENTRE, 57.2, "grown in the sun · cut by hand", 2.1, 400, "#A9C3A0", "middle", spacing=0.3)}
  {net_content(74.6, cream, 5)}"""


def retro_vendor_front():
    red, cream, green = "#C8102E", "#F6EBD3", "#14853B"
    stripes = "".join(f'<rect x="{LEFT}" y="{y}" width="{PANEL_WIDTH}" height="1.6" fill="{colour}"/>'
                      for y, colour in [(4.5, red), (6.6, GOLD), (8.7, green)])
    return f"""
  {panel_fill(cream)}
  {stripes}
  <circle cx="{CENTRE}" cy="27" r="13.5" fill="{GOLD}" stroke="{red}" stroke-width="0.8"/>
  {coconut_at(CENTRE, 16, 21)}
  <path d="M{LEFT + 6} 40 L{RIGHT - 6} 40 L{RIGHT - 9} 44 L{RIGHT - 6} 48 L{LEFT + 6} 48 L{LEFT + 9} 44 Z" fill="{red}"/>
  {text(CENTRE, 46, "ICE COLD", 4.6, 400, cream, "middle", "Archivo Black", 1.5)}
  {text(CENTRE, 59, "Jelly Water", 10, 400, green, "middle", "Pacifico")}
  {text(CENTRE, 65.2, "ROADSIDE FRESH · SINCE YOU WERE SMALL", 2, 700, red, "middle", spacing=0.5)}
  {net_content(74.6, red, 5, "Archivo Black")}"""


def gym_fuel_front():
    lime = "#A3E635"
    return f"""
  {panel_fill("#FFFFFF")}
  <path d="M{LEFT} 0 L{RIGHT} 0 L{RIGHT} 22 L{LEFT} 34 Z" fill="{BLACK}"/>
  {text(LEFT + 6, 13, "JELLY WATER", 9, 400, "#FFFFFF", family="Bebas Neue", spacing=1)}
  {text(LEFT + 6, 18.4, "NATURAL ELECTROLYTES", 2.6, 700, lime, spacing=1)}
  {coconut_at(RIGHT - 16, 20, 22)}
  {text(LEFT + 6, 47, "625", 15, 400, BLACK, family="Bebas Neue")}
  {text(LEFT + 25, 41.4, "mg", 3.4, 800, BLACK)}
  {text(LEFT + 25, 46, "POTASSIUM", 2.6, 800, "#4D7C0F", spacing=0.4)}
  <rect x="{LEFT + 6}" y="50.5" width="{PANEL_WIDTH - 12}" height="0.5" fill="{BLACK}"/>
  {text(LEFT + 6, 56, "45 CAL · 0 G ADDED SUGAR · 100% COCONUT", 2.3, 700, BLACK, spacing=0.2)}
  {text(LEFT + 6, 60, "per 250 mL serving", 2, 400, "#555555")}
  {net_content(74.6, BLACK, 6.4, "Bebas Neue")}"""


DESIGNS = [
    LabelDesign("01-yaad-classic", "Yaad Classic",
                "Flag colours (black, green, gold). Says 'Jamaican' from across the shop. Safe, proud, but green is what every coconut brand uses.",
                "#FFFFFF", BLACK, GOLD, GREEN, "#FFFFFF", GREEN, yaad_classic_front),
    LabelDesign("02-pure-white", "Pure & Simple",
                "Mostly white, small type. Signals 'nothing added' and stands out on a shelf full of green. Supermarkets, health shoppers.",
                "#FFFFFF", "#24302A", "#0F7A3A", "#EEF5EF", "#0F7A3A", "#0F7A3A", pure_white_front,
                side_band_text="PRODUCT OF JAMAICA"),
    LabelDesign("03-ocean-hydration", "Ocean Hydration",
                "Blue = water, cool, refreshing. Sells hydration and electrolytes. Gyms, schools, hot-day buyers. Blue is rare in coconut water.",
                "#FFFFFF", "#0B2545", GOLD, "#0353A4", "#FFFFFF", "#0353A4", ocean_hydration_front,
                back_band_text="NATURE'S HYDRATION"),
    LabelDesign("04-kraft-farm", "Kraft Farm",
                "Brown paper and black stamp ink. Looks hand-made and local, like it came off the farm today. Markets, farm shops, artisan price.",
                "#E9DCC6", "#2B1D10", "#8B5E34", "#2B1D10", "#E9DCC6", "#8B3A1E", kraft_farm_front,
                back_band_text="FARM TO BOTTLE", side_band_text="HAND-CUT · BOTTLED FRESH"),
    LabelDesign("05-island-reserve", "Island Reserve",
                "Black and gold, serif type. Premium price for hotels, resorts, duty-free and gifts. One study found black can lower liking, so test it first.",
                "#F7F1E3", "#1A1A1A", "#D4AF37", "#0E0E0E", "#D4AF37", "#8C6D1F", island_reserve_front,
                back_band_text="ISLAND RESERVE", side_band_text="SINGLE ORIGIN · JAMAICA"),
    LabelDesign("06-sunset-tropical", "Sunset Tropical",
                "Sunset colours and palm trees. Holiday feeling for tourists, beach bars and Instagram photos.",
                "#FFFFFF", "#3A1F2B", "#FFB26B", "#FF5E62", "#FFFFFF", "#D9480F", sunset_tropical_front,
                back_band_text="ISLAND-FRESH", side_band_text="SUN · SEA · JELLY"),
    LabelDesign("07-dancehall-bold", "Dancehall Bold",
                "Black with neon lime, huge stacked letters. Loud and young. Gas stations, corner shops, events, street vendors.",
                "#FFFFFF", BLACK, "#C6FF00", BLACK, "#C6FF00", "#3F7D00", dancehall_bold_front,
                back_band_text="STRAIGHT OUTTA DI COCONUT", side_band_text="BIG UP DI YAAD"),
    LabelDesign("08-botanical", "Botanical",
                "Deep forest green with palm leaves, cream type. Natural and calm, a step above the bright greens. Health stores, cafés.",
                "#F4EBD0", "#0F3D2E", "#C8A951", "#0F3D2E", "#F4EBD0", "#1E5A44", botanical_front),
    LabelDesign("09-retro-vendor", "Retro Vendor",
                "Red, gold and green stripes and an 'ICE COLD' banner, like the roadside jelly cart. Nostalgia for Jamaicans at home and abroad.",
                "#F6EBD3", "#2A1A12", "#C8102E", "#C8102E", "#F6EBD3", "#C8102E", retro_vendor_front,
                back_band_text="ICE COLD JELLY", side_band_text="ROADSIDE FRESH"),
    LabelDesign("10-gym-fuel", "Gym Fuel",
                "White, black and lime with the potassium number as the hero. Sells coconut water as a natural sports drink. Gyms, runners, athletes.",
                "#FFFFFF", BLACK, "#A3E635", BLACK, "#A3E635", "#4D7C0F", gym_fuel_front,
                back_band_text="NATURAL ELECTROLYTES", side_band_text="FUEL · HYDRATE · RECOVER"),
]
