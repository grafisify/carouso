#!/usr/bin/env python3
"""
render_carousel.py — render HTML carousel menjadi JPG per slide via Playwright.

Quality gate (exit 1 bila gagal):
  1. jumlah elemen .slide harus == --slides
  2. tidak boleh ada konten yang overflow (teks kepotong / elemen tabrakan)
  3. bounding box tiap slide harus == --width x --height
  4. font di --check-fonts harus termuat (tolak fallback tak disengaja)

Contoh:
  python3 scripts/render_carousel.py --html topik.html --out out/ \\
      --width 1080 --height 1350 --slides 10
"""
import argparse
import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True, help="file HTML carousel")
    ap.add_argument("--out", required=True, help="direktori output JPG")
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1350)
    ap.add_argument("--slides", type=int, default=10)
    ap.add_argument("--quality", type=int, default=88)
    ap.add_argument("--check-fonts", default="",
                    help="daftar family font (koma) yang wajib termuat, "
                         'cth: "Baloo 2,Quicksand". Gagal = exit 1.')
    args = ap.parse_args()

    html = Path(args.html).resolve()
    out = Path(args.out)
    if not html.exists():
        print(f"HTML tidak ditemukan: {html}", flush=True)
        return 1
    out.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": args.width, "height": args.height}
        )
        # file:// agar path gambar lokal relatif selalu bisa dibaca
        await page.goto(html.as_uri())
        await page.wait_for_timeout(2500)  # beri waktu font/gambar lokal termuat
        try:
            await page.evaluate("document.fonts.ready.then(()=>1)")
        except Exception:
            pass

        # gate font: webfont (mis. Google Fonts) yang gagal dimuat membuat
        # judul jatuh ke fallback — tolak sebelum render.
        if args.check_fonts.strip():
            missing = []
            for fam in [f.strip() for f in args.check_fonts.split(",") if f.strip()]:
                ok = await page.evaluate(
                    f'document.fonts.check(\'700 48px "{fam}"\')'
                )
                if not ok:
                    missing.append(fam)
            if missing:
                print(f"GATE GAGAL font: tidak termuat: {missing}. "
                      f"Pakai font lokal atau perbaiki akses webfont.", flush=True)
                await browser.close()
                return 1
            print(f"font OK: {args.check_fonts}", flush=True)

        n = await page.evaluate("document.querySelectorAll('.slide').length")
        if n != args.slides:
            print(f"GATE GAGAL: jumlah slide {n}, diminta {args.slides}", flush=True)
            await browser.close()
            return 1

        bad_overflow, bad_size = [], []
        for i in range(n):
            await page.evaluate(
                f"""document.querySelectorAll('.slide').forEach((c,idx)=>{{
                        c.style.display = idx==={i} ? 'block' : 'none'; }})"""
            )
            el = page.locator(".slide").nth(i)

            # gate dimensi via bounding box (tanpa dependensi PIL)
            box = await el.bounding_box()
            if not box or int(box["width"]) != args.width or int(box["height"]) != args.height:
                bad_size.append(i + 1)

            await el.screenshot(
                path=str(out / f"slide_{i+1:02d}.jpg"),
                type="jpeg",
                quality=args.quality,
            )

            # gate overflow: konten yang meluber = teks kepotong / tabrakan
            ovf = await page.evaluate(
                f"""(()=>{{
                    const s = document.querySelectorAll('.slide')[{i}];
                    const inner = s.querySelector('.content');
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
        print(f"GATE GAGAL dimensi: slide {bad_size} (minta {args.width}x{args.height})", flush=True)
        failed = True
    if bad_overflow:
        print(f"GATE GAGAL overflow: slide {bad_overflow} (konten meluber/kepotong)", flush=True)
        failed = True
    if failed:
        return 1

    files = sorted(out.glob("slide_*.jpg"))
    if len(files) != args.slides:
        print(f"GATE GAGAL: file output {len(files)}, diminta {args.slides}", flush=True)
        return 1

    print(f"OK: {len(files)} slide ter-render ke {out}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
