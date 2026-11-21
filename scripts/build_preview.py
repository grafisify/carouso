#!/usr/bin/env python3
"""
build_preview.py: compose rendered slides into one README preview sheet.

Lays slide_01.jpg ... slide_NN.jpg out in a grid (4 columns by default) on a
dark background, the same layout as assets/templates/*.jpg.

Example:
  python3 scripts/render_carousel.py --html templates/10-sticky-mono/sample.html \\
      --out out/10-sticky-mono --slides 8 --check-fonts "JetBrains Mono"
  python3 scripts/build_preview.py --slides out/10-sticky-mono \\
      --out assets/templates/10-sticky-mono.jpg
"""
import argparse
import asyncio
import math
import sys
import tempfile
from pathlib import Path

from playwright.async_api import async_playwright


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slides", required=True, help="folder with slide_*.jpg")
    ap.add_argument("--out", required=True, help="preview JPG path")
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--tile", type=int, default=330, help="tile width in px")
    ap.add_argument("--ratio", type=float, default=1440 / 1080, help="slide height / width")
    ap.add_argument("--gap", type=int, default=14)
    ap.add_argument("--pad", type=int, default=18)
    ap.add_argument("--bg", default="#181818")
    ap.add_argument("--quality", type=int, default=88)
    args = ap.parse_args()

    files = sorted(Path(args.slides).glob("slide_*.jpg"))
    if not files:
        print(f"no slide_*.jpg in {args.slides}", flush=True)
        return 1
    rows = math.ceil(len(files) / args.cols)
    th = round(args.tile * args.ratio)
    w = args.pad * 2 + args.cols * args.tile + (args.cols - 1) * args.gap
    h = args.pad * 2 + rows * th + (rows - 1) * args.gap
    imgs = "".join(f'<img src="{f.resolve().as_uri()}">' for f in files)
    html = (f"<html><body style='margin:0;background:{args.bg}'>"
            f"<div style='display:grid;grid-template-columns:repeat({args.cols},{args.tile}px);"
            f"grid-auto-rows:{th}px;gap:{args.gap}px;padding:{args.pad}px'>{imgs}</div>"
            f"<style>img{{width:100%;height:100%;display:block}}</style></body></html>")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "preview.html"
        tmp.write_text(html)
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={"width": w, "height": h})
            await page.goto(tmp.resolve().as_uri(), wait_until="load")
            await page.screenshot(path=str(out), type="jpeg", quality=args.quality,
                                  clip={"x": 0, "y": 0, "width": w, "height": h})
            await browser.close()
    print(f"OK: {len(files)} slides -> {out} ({w}x{h})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
