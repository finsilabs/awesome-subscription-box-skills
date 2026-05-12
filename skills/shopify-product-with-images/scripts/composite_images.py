# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow>=10.0.0"]
# ///
"""Composite the 3 tier boxes side-by-side into one image."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

inputs = [
    ROOT / "generated" / "tier_pit_stop_box.png",
    ROOT / "generated" / "tier_apex_box.png",
    ROOT / "generated" / "tier_podium_box.png",
]

target_h = 900
gap = 40
bg = (15, 17, 22, 255)

resized = []
for p in inputs:
    im = Image.open(p).convert("RGBA")
    ratio = target_h / im.height
    new_w = int(im.width * ratio)
    resized.append(im.resize((new_w, target_h), Image.LANCZOS))

total_w = sum(im.width for im in resized) + gap * (len(resized) - 1)
canvas = Image.new("RGBA", (total_w, target_h), bg)

x = 0
for im in resized:
    canvas.paste(im, (x, 0), im)
    x += im.width + gap

out = ROOT / "generated" / "tier_lineup.png"
canvas.convert("RGB").save(out, optimize=True)
print(f"Wrote {out} ({canvas.size})")
