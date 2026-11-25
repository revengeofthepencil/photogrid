# /// script
# requires-python = ">=3.9"
# dependencies = ["pillow>=10"]
# ///
"""Draw a grid over an image (bright red by default).

Usage:
    uv run photogrid.py <image_path> <spacing_percent> <line_width_px> [--color COLOR]

Example:
    uv run photogrid.py photo.jpg 50 2              # quarter grid, 2px red lines -> photo_grid.jpg
    uv run photogrid.py photo.jpg 50 2 -c white     # same, white lines
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw

DEFAULT_COLOR = "#ff0000"


def grid_positions(length: int, spacing_percent: float) -> list[int]:
    """Pixel positions of interior grid lines along one dimension."""
    positions = []
    step = spacing_percent / 100.0
    i = 1
    # Small epsilon so e.g. 3 x 33.333 doesn't put a line on the far edge.
    while i * step < 1.0 - 1e-9:
        positions.append(round(i * step * length))
        i += 1
    return positions


def draw_grid(
    img: Image.Image,
    spacing_percent: float,
    line_width: int,
    rgb: tuple[int, int, int] = (255, 0, 0),
) -> Image.Image:
    has_alpha = img.mode in ("RGBA", "LA") or "transparency" in img.info
    out = img.convert("RGBA" if has_alpha else "RGB")
    draw = ImageDraw.Draw(out)
    width, height = out.size
    color = rgb + (255,) if has_alpha else rgb

    # Center each line on its grid position.
    before = line_width // 2
    after = line_width - before - 1

    for x in grid_positions(width, spacing_percent):
        draw.rectangle([x - before, 0, x + after, height - 1], fill=color)
    for y in grid_positions(height, spacing_percent):
        draw.rectangle([0, y - before, width - 1, y + after], fill=color)

    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Draw a grid over an image (bright red by default).")
    parser.add_argument("image", type=Path, help="path to the input image")
    parser.add_argument("spacing", type=float, help="grid spacing as a percentage of the image size (e.g. 50 = quarters)")
    parser.add_argument("width", type=int, help="line width in pixels")
    parser.add_argument(
        "-c", "--color",
        default=DEFAULT_COLOR,
        help="line color: a name (red, white, yellow) or hex (#00ff00, #0f0); default %(default)s",
    )
    args = parser.parse_args()

    try:
        rgb = ImageColor.getrgb(args.color)[:3]
    except ValueError:
        parser.error(f"unrecognized color: {args.color!r} (use a name like 'white' or hex like '#00ff00')")

    if not args.image.is_file():
        parser.error(f"image not found: {args.image}")
    if not 0 < args.spacing < 100:
        parser.error("spacing must be greater than 0 and less than 100")
    if args.width < 1:
        parser.error("width must be at least 1 pixel")

    with Image.open(args.image) as img:
        fmt = img.format
        result = draw_grid(img, args.spacing, args.width, rgb)

    out_path = args.image.with_name(f"{args.image.stem}_grid{args.image.suffix}")
    # Disable chroma subsampling so thin red lines stay bright red in JPEGs.
    save_kwargs = {"quality": 95, "subsampling": 0} if fmt == "JPEG" else {}
    result.save(out_path, format=fmt, **save_kwargs)
    print(f"Saved {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
