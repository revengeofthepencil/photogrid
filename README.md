# photogrid

Draws a bright red grid over an image and saves it alongside the original as
`<imagename>_grid.<extension>`.

## Requirements

[uv](https://docs.astral.sh/uv/). The script declares its own dependencies
(Pillow) inline, so uv installs them automatically on first run. No virtualenv
setup needed.

## Usage

```bash
uv run photogrid.py <image_path> <spacing_percent> <line_width_px>
```

| Argument          | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| `image_path`      | Path to the input image (JPEG, PNG, etc.)                          |
| `spacing_percent` | Distance between lines as a percentage of the image width/height   |
| `line_width_px`   | Thickness of each line in pixels                                   |

## Examples

```bash
# Quarter grid (one vertical + one horizontal line through the center), 2px lines
uv run photogrid.py photo.jpg 50 2
# -> photo_grid.jpg

# Rule of thirds, 4px lines
uv run photogrid.py photo.png 33.333 4
# -> photo_grid.png

# 10x10 grid, 1px lines
uv run photogrid.py photo.jpg 10 1
```

## Notes

- Spacing applies to each axis independently, so on a non-square image the grid
  cells are rectangles with the same proportions as the image.
- Lines are drawn only inside the image, not along its edges.
- Lines are centered on their grid position.
- The output keeps the input's format; JPEGs are saved at quality 95 with
  chroma subsampling off, so thin red lines stay crisp.
