#!/usr/bin/env python3
"""
render_carousel.py: render an HTML carousel to one JPG per slide with Playwright.

Quality gates (exit 1 on failure):
  1. the .slide count must equal --slides
  2. no content may overflow its zone (clipped text or colliding elements)
  3. every slide bounding box must equal --width x --height
  4. every font in --check-fonts must be loaded (reject silent fallback)

Example:
  python3 scripts/render_carousel.py --html topic.html --out out/ \
      --width 1080 --height 1350 --slides 10 \
      --check-fonts "Baloo 2,Quicksand"
"""
import argparse
import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True, help="carousel HTML file")
    ap.add_argument("--out", required=True, help="JPG output directory")
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1350)
    ap.add_argument("--slides", type=int, default=10)
    ap.add_argument("--quality", type=int, default=88)
    ap.add_argument("--check-fonts", default="",
                    help="comma-separated font families that must be loaded, "
                         'e.g. "Baloo 2,Quicksand". Missing = exit 1.')
    args = ap.parse_args()

    html = Path(args.html).resolve()
    out = Path(args.out)
    if not html.exists():
        print(f"HTML not found: {html}", flush=True)
        return 1
    out.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": args.width, "height": args.height}
        )
        # file:// so relative local image paths always resolve
        await page.goto(html.as_uri())
        await page.wait_for_timeout(2500)  # let local fonts/images load
        try:
            await page.evaluate("document.fonts.ready.then(()=>1)")
        except Exception:
            pass

        # Font gate: a webfont (e.g. Google Fonts) that fails to load drops
        # headlines to a fallback. Reject before rendering.
        if args.check_fonts.strip():
            missing = []
            for fam in [f.strip() for f in args.check_fonts.split(",") if f.strip()]:
                ok = await page.evaluate(
                    f'document.fonts.check(\'700 48px "{fam}"\')'
                )
                if not ok:
                    missing.append(fam)
            if missing:
                print(f"GATE FAILED (font): not loaded: {missing}. "
                      f"Use local fonts or fix webfont access.", flush=True)
                await browser.close()
                return 1
            print(f"fonts OK: {args.check_fonts}", flush=True)

        n = await page.evaluate("document.querySelectorAll('.slide').length")
        if n != args.slides:
            print(f"GATE FAILED (count): got {n} slides, expected {args.slides}", flush=True)
            await browser.close()
            return 1

        bad_overflow, bad_size = [], []
        for i in range(n):
            await page.evaluate(
                f"""document.querySelectorAll('.slide').forEach((c,idx)=>{{
                        c.style.display = idx==={i} ? 'block' : 'none'; }})"""
            )
            el = page.locator(".slide").nth(i)

            # Size gate via bounding box (no PIL dependency)
            box = await el.bounding_box()
            if not box or int(box["width"]) != args.width or int(box["height"]) != args.height:
                bad_size.append(i + 1)

            await el.screenshot(
                path=str(out / f"slide_{i+1:02d}.jpg"),
                type="jpeg",
                quality=args.quality,
            )

            # Overflow gate: overflowing content means clipped text or collisions.
            # Falls back to .inner or the slide itself, so freely composed
            # patterns without a .content wrapper do not crash the gate.
            ovf = await page.evaluate(
                f"""(()=>{{
                    const s = document.querySelectorAll('.slide')[{i}];
                    const inner = s.querySelector('.content') || s.querySelector('.inner') || s;
                    return {{ scrollW: inner.scrollWidth, clientW: inner.clientWidth,
                              scrollH: inner.scrollHeight, clientH: inner.clientHeight }};
                }})()"""
            )
            if ovf["scrollH"] > ovf["clientH"] + 2 or ovf["scrollW"] > ovf["clientW"] + 2:
                bad_overflow.append(i + 1)
            print(f"slide {i+1:02d}: box={box['width']:.0f}x{box['height']:.0f} overflow={ovf}", flush=True)

        await browser.close()

    failed = False
    if bad_size:
        print(f"GATE FAILED (size): slides {bad_size} (expected {args.width}x{args.height})", flush=True)
        failed = True
    if bad_overflow:
        print(f"GATE FAILED (overflow): slides {bad_overflow} (content clipped or colliding)", flush=True)
        failed = True
    if failed:
        return 1

    files = sorted(out.glob("slide_*.jpg"))
    if len(files) != args.slides:
        print(f"GATE FAILED (output): {len(files)} files, expected {args.slides}", flush=True)
        return 1

    print(f"OK: {len(files)} slides rendered to {out}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
