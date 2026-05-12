# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow>=10.0.0", "numpy>=1.26.0"]
# ///
"""Remove a solid background from an image and save as transparent PNG.

The background color is sampled from the four corners (median) by default,
or you can pass --bg <hex>. Pixels close to the background color get alpha 0,
pixels far from it stay opaque, and the transition is feathered for clean edges.

Usage:
    uv run scripts/remove_background.py <input> [output]
    uv run scripts/remove_background.py --bg 1F2127 <input> [output]
    uv run scripts/remove_background.py --tolerance 60 --feather 30 <input>
    uv run scripts/remove_background.py generated/*.png --suffix _transparent

If output is omitted, writes <input>_transparent.png next to the source.
Globs and multiple inputs are supported; each gets its own output.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def parse_hex(s: str) -> tuple[int, int, int]:
    s = s.lstrip("#")
    if len(s) != 6:
        raise ValueError(f"--bg must be a 6-digit hex color, got {s!r}")
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def sample_background(rgb: np.ndarray) -> tuple[int, int, int]:
    h, w = rgb.shape[:2]
    pad = max(1, min(h, w) // 50)
    corners = np.concatenate([
        rgb[:pad, :pad].reshape(-1, 3),
        rgb[:pad, -pad:].reshape(-1, 3),
        rgb[-pad:, :pad].reshape(-1, 3),
        rgb[-pad:, -pad:].reshape(-1, 3),
    ])
    median = np.median(corners, axis=0).astype(int)
    return int(median[0]), int(median[1]), int(median[2])


def remove_background(
    src: Path,
    dst: Path,
    bg: tuple[int, int, int] | None,
    tolerance: int,
    feather: int,
) -> None:
    img = Image.open(src).convert("RGBA")
    arr = np.array(img)
    rgb = arr[..., :3].astype(np.int16)

    bg_rgb = bg if bg is not None else sample_background(rgb)
    bg_arr = np.array(bg_rgb, dtype=np.int16)
    distance = np.sqrt(((rgb - bg_arr) ** 2).sum(axis=-1))

    inner, outer = float(tolerance), float(tolerance + feather)
    if outer <= inner:
        outer = inner + 1.0
    alpha = np.clip((distance - inner) / (outer - inner), 0.0, 1.0)

    arr[..., 3] = (alpha * 255).astype(np.uint8)
    Image.fromarray(arr, "RGBA").save(dst, optimize=True)
    print(f"{src.name}: bg=#{bg_rgb[0]:02x}{bg_rgb[1]:02x}{bg_rgb[2]:02x} -> {dst}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="Image file(s) to process")
    ap.add_argument("--bg", type=parse_hex, default=None, help="Background hex color (default: auto-detect from corners)")
    ap.add_argument("--tolerance", type=int, default=40, help="Distance from bg color treated as fully transparent (default 40)")
    ap.add_argument("--feather", type=int, default=25, help="Width of soft transition between transparent and opaque (default 25)")
    ap.add_argument("-o", "--output", help="Output path (only valid with a single input)")
    ap.add_argument("--suffix", default="_transparent", help="Suffix for output filenames when -o is not given")
    args = ap.parse_args()

    paths: list[Path] = []
    for raw in args.inputs:
        p = Path(raw)
        paths.append(p) if p.is_file() else paths.extend(sorted(p.parent.glob(p.name)))
    if not paths:
        print("No input files matched.", file=sys.stderr)
        return 1
    if args.output and len(paths) > 1:
        print("--output can only be used with a single input.", file=sys.stderr)
        return 1

    for src in paths:
        dst = Path(args.output) if args.output else src.with_name(f"{src.stem}{args.suffix}.png")
        remove_background(src, dst, args.bg, args.tolerance, args.feather)
    return 0


if __name__ == "__main__":
    sys.exit(main())
