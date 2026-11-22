#!/usr/bin/env python3
"""
render_carousel.py: render an HTML carousel to one JPG per slide with Playwright.

Quality gates (exit 1 on failure):
  1. the .slide count must equal --slides
  2. no content may overflow its zone (clipped text or colliding elements)
  3. every slide bounding box must equal --width x --height
  4. every font in --check-fonts must be loaded (reject silent fallback)
  5. no visible text may be smaller than --min-font px (default 20, readable on a phone)
  6. every <img> on a slide must load (no broken or missing files)
  7. no text may be cut off by the slide edge (except inside .peek or [data-bleed],
     which bleed off the edge on purpose)
  8. no word may be wider than the line it sits on (a long word in a big
     headline spills out of its column instead of wrapping)

Example:
  python3 scripts/render_carousel.py --html topic.html --out out/ \
      --width 1080 --height 1440 --slides 10 \
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
    ap.add_argument("--height", type=int, default=1440)
    ap.add_argument("--slides", type=int, default=10)
    ap.add_argument("--quality", type=int, default=88)
    ap.add_argument("--min-font", type=int, default=20,
                    help="smallest allowed text size in px at 1080 wide. 0 disables.")
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
        # file:// so relative local image paths always resolve. "load" waits for
        # stylesheets, images and CSS backgrounds; then wait for fonts and decoding.
        await page.goto(html.as_uri(), wait_until="load")
        await page.evaluate(
            """async()=>{
                // lazy images below the viewport never start loading, so decode() would hang
                document.querySelectorAll('img[loading="lazy"]').forEach(i=>i.loading='eager');
                await document.fonts.ready;
                await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));
            }""")

        # Image gate: a wrong path or unreadable file renders as an empty frame.
        broken = await page.evaluate(
            """()=>[...document.querySelectorAll('.slide img')]
                .filter(i=>!i.complete||i.naturalWidth===0)
                .map(i=>{const s=i.closest('.slide');
                  return `slide ${[...document.querySelectorAll('.slide')].indexOf(s)+1} ${i.getAttribute('src')}`;})""")
        if broken:
            print("GATE FAILED (image): not loaded:", flush=True)
            for line in broken[:12]:
                print("  " + line, flush=True)
            await browser.close()
            return 1

        # Font gate: a webfont (e.g. Google Fonts) that fails to load drops
        # headlines to a fallback. Reject before rendering.
        if args.check_fonts.strip():
            missing = []
            for fam in [f.strip() for f in args.check_fonts.split(",") if f.strip()]:
                # Declared fonts load lazily, so a family unused on these slides
                # would look "missing". Force the load, then check.
                try:
                    await page.evaluate(f'document.fonts.load(\'700 48px "{fam}"\')')
                except Exception:
                    pass
                # document.fonts.check() is true for unknown families, so compare
                # rendered widths against bare generic fallbacks instead.
                ok = await page.evaluate(
                    """(fam)=>{
                        const c=document.createElement('canvas').getContext('2d');
                        const t='mmmmmmmmmmlliWQ@#0123456789';
                        return ['monospace','serif','sans-serif'].some(g=>{
                          c.font='700 48px '+g; const a=c.measureText(t).width;
                          c.font='700 48px "'+fam+'",'+g; return c.measureText(t).width!==a;
                        });
                    }""", fam)
                if not ok:
                    missing.append(fam)
            if missing:
                print(f"GATE FAILED (font): not loaded: {missing}. "
                      f"Use local fonts or fix webfont access.", flush=True)
                await browser.close()
                return 1
            print(f"fonts OK: {args.check_fonts}", flush=True)

        # Type-size gate: a 1080px slide is viewed at roughly a third of its size
        # on a phone, so anything under ~20px is unreadable there.
        if args.min_font > 0:
            small = await page.evaluate(
                """(min)=>{
                    const out=[];
                    for (const s of document.querySelectorAll('.slide')){
                      const idx=[...document.querySelectorAll('.slide')].indexOf(s)+1;
                      const w=document.createTreeWalker(s,NodeFilter.SHOW_TEXT);
                      while(w.nextNode()){
                        const n=w.currentNode; if(!n.textContent.trim()) continue;
                        const el=n.parentElement; const cs=getComputedStyle(el);
                        if(cs.display==='none'||cs.visibility==='hidden') continue;
                        const fs=parseFloat(cs.fontSize);
                        if(fs<min) out.push(`slide ${idx} ${el.tagName.toLowerCase()}.${el.className||''} ${fs}px "${n.textContent.trim().slice(0,24)}"`);
                      }
                    }
                    return out;
                }""", args.min_font)
            if small:
                print(f"GATE FAILED (type size): text under {args.min_font}px:", flush=True)
                for line in small[:12]:
                    print("  " + line, flush=True)
                await browser.close()
                return 1
            print(f"type size OK: nothing under {args.min_font}px", flush=True)

        n = await page.evaluate("document.querySelectorAll('.slide').length")
        if n != args.slides:
            print(f"GATE FAILED (count): got {n} slides, expected {args.slides}", flush=True)
            await browser.close()
            return 1

        bad_overflow, bad_size, bad_edge, bad_word = [], [], [], []
        for i in range(n):
            await page.evaluate(
                f"""document.querySelectorAll('.slide').forEach((c,idx)=>{{
                        c.style.display = idx==={i} ? 'block' : 'none'; }})"""
            )
            el = page.locator(".slide").nth(i)

            # Size gate via bounding box (no PIL dependency)
            box = await el.bounding_box()
            if not box or round(box["width"]) != args.width or round(box["height"]) != args.height:
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

            # Edge gate: text past the slide edge is cut off in the JPG.
            cut = await page.evaluate(
                f"""(()=>{{
                    const s = document.querySelectorAll('.slide')[{i}];
                    const b = s.getBoundingClientRect(), out = [];
                    const w = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
                    while (w.nextNode()) {{
                      const n = w.currentNode, el = n.parentElement;
                      if (!n.textContent.trim() || el.closest('.peek,[data-bleed]')) continue;
                      const cs = getComputedStyle(el);
                      if (cs.display==='none' || cs.visibility==='hidden') continue;
                      const r = document.createRange(); r.selectNodeContents(n);
                      for (const q of r.getClientRects()) {{
                        if (q.width && (q.left < b.left-1 || q.top < b.top-1 ||
                            q.right > b.right+1 || q.bottom > b.bottom+1)) {{
                          out.push(n.textContent.trim().slice(0,24)); break;
                        }}
                      }}
                    }}
                    return out;
                }})()"""
            )
            if cut:
                bad_edge.append(f"{i + 1} {cut[:3]}")
            # Word gate: a word wider than its line cannot wrap, so it spills out
            # of its column. Long Indonesian words in display type do this.
            wide = await page.evaluate(
                f"""(()=>{{
                    const s = document.querySelectorAll('.slide')[{i}], out = [];
                    for (const el of s.querySelectorAll('h1,h2,h3,h4,p,li,blockquote,.quote')) {{
                      if (el.closest('.peek,[data-bleed]')) continue;
                      const cs = getComputedStyle(el);
                      if (cs.display==='none' || cs.visibility==='hidden' || cs.whiteSpace==='nowrap') continue;
                      const room = el.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
                      if (room <= 0) continue;
                      // A min-content copy is as wide as its longest unbreakable piece,
                      // in the real font of each span and with hyphens free to break.
                      const copy = el.cloneNode(true);
                      copy.removeAttribute('id');
                      copy.style.cssText += ';position:absolute;visibility:hidden;width:min-content;'
                        + 'min-width:0;max-width:none;padding:0;border:0;margin:0';
                      el.after(copy);
                      const need = copy.offsetWidth;
                      copy.remove();
                      if (need > room + 2) {{
                        const words = el.innerText.split(/\\s+/).sort((a, b) => b.length - a.length);
                        out.push(words[0]);
                      }}
                    }}
                    return out;
                }})()"""
            )
            if wide:
                bad_word.append(f"{i + 1} {wide[:3]}")
            print(f"slide {i+1:02d}: box={box['width']:.0f}x{box['height']:.0f} overflow={ovf}", flush=True)

        await browser.close()

    failed = False
    if bad_size:
        print(f"GATE FAILED (size): slides {bad_size} (expected {args.width}x{args.height})", flush=True)
        failed = True
    if bad_overflow:
        print(f"GATE FAILED (overflow): slides {bad_overflow} (content clipped or colliding)", flush=True)
        failed = True
    if bad_edge:
        print(f"GATE FAILED (edge): text cut off by the slide edge: {bad_edge}", flush=True)
        failed = True
    if bad_word:
        print(f"GATE FAILED (word): word wider than its line: {bad_word} "
              f"(use a shorter word or break it across lines)", flush=True)
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
