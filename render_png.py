"""Renders every SVG logo to a transparent PNG with headless Chrome."""
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

PROJECT_DIRECTORY = Path(__file__).parent
SVG_DIRECTORY = PROJECT_DIRECTORY / "svg"
PNG_DIRECTORY = PROJECT_DIRECTORY / "png"
SCALE = 3
WINDOW_PADDING = 300


def svg_size(svg_path):
    width, height = re.search(r'width="(\d+)" height="(\d+)"', svg_path.read_text()).groups()
    return int(width), int(height)


def screenshot(page_path, width, height, output_path, scale=SCALE):
    subprocess.run(
        [
            "google-chrome", "--headless=new", "--disable-gpu", "--hide-scrollbars",
            f"--force-device-scale-factor={scale}", "--default-background-color=00000000",
            "--virtual-time-budget=6000", f"--window-size={width},{height + WINDOW_PADDING}",
            f"--screenshot={output_path}", page_path.as_uri(),
        ],
        check=True, capture_output=True,
    )


def render(svg_path, output_directory=PNG_DIRECTORY):
    width, height = svg_size(svg_path)
    with tempfile.TemporaryDirectory() as temporary_directory:
        raw_path = Path(temporary_directory) / "raw.png"
        screenshot(svg_path, width, height, raw_path)
        cropped = Image.open(raw_path).crop((0, 0, width * SCALE, height * SCALE))
    output_path = output_directory / f"{svg_path.stem}.png"
    cropped.save(output_path)
    print(output_path, cropped.size)
    return output_path


def main():
    PNG_DIRECTORY.mkdir(exist_ok=True)
    for svg_path in sorted(SVG_DIRECTORY.glob("*.svg")):
        render(svg_path)


if __name__ == "__main__":
    main()
