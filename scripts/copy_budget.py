#!/usr/bin/env python3
"""
copy_budget.py: measure how much headline text each slide of a template holds.

For every templates/NN-slug/sample.html it measures, in the real fonts, the main
line of each slide (its h1, else its h2, else its quote) and reports:
  - chars_per_line: how many characters of ordinary Indonesian or English text
    fit on one line. This is also the longest single word that fits.
  - lines: how many lines the sample uses, which is what the layout was drawn for.

Default: compare against the "headline" entry of each slide in template.json and
exit 1 when a stored number is off by more than one character.
--write: store the measured numbers in template.json.
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
# ordinary running text, so the average includes spaces and both narrow and wide letters
REFERENCE = "kebiasaan menabung dimulai dari pengeluaran kecil setiap minggu"

MEASURE = """
(ref) => {
  const measure = (el) => {
    const cs = getComputedStyle(el);
    const lineHeight = parseFloat(cs.lineHeight);
    // count real line boxes: the element itself may be stretched or padded
    const range = document.createRange();
    range.selectNodeContents(el);
    const tops = [...range.getClientRects()].filter(r => r.width > 0).map(r => r.top + r.height / 2).sort((x, y) => x - y);
    let lines = 0, last = -Infinity;
    for (const t of tops) if (t - last > lineHeight / 2) { lines++; last = t; }
    lines = Math.max(1, lines);
    const saved = el.innerHTML, savedWrap = el.style.textWrap;
    el.style.textWrap = 'wrap';
    const probe = document.createElement('span');
    probe.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap';
    probe.textContent = ref;
    el.textContent = '';
    el.appendChild(probe);
    const charWidth = probe.getBoundingClientRect().width / ref.length;
    // two-character words wrap at every step, so the widest line is the usable width
    el.textContent = 'n '.repeat(400);
    const width = el.getBoundingClientRect().width;
    el.innerHTML = saved;
    el.style.textWrap = savedWrap;
    return {chars_per_line: Math.floor(width / charWidth), lines};
  };
  return [...document.querySelectorAll('section.slide')].map(s => {
    const el = s.querySelector('h1') || s.querySelector('h2') || s.querySelector('.quote');
    return el ? measure(el) : null;
  });
}
"""


async def measure_all(dirs):
    out = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1440})
        for d in dirs:
            await page.goto((d / "sample.html").as_uri(), wait_until="load")
            await page.evaluate("document.fonts.ready")
            out[d.name] = await page.evaluate(MEASURE, REFERENCE)
        await browser.close()
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true", help="store the measured budget in each template.json")
    args = ap.parse_args()

    dirs = sorted(d for d in (ROOT / "templates").iterdir() if (d / "sample.html").exists())
    measured = asyncio.run(measure_all(dirs))
    problems = 0
    for d in dirs:
        got = measured[d.name]
        path = d / "template.json"
        meta = json.loads(path.read_text())
        seq = meta["sequence"]
        if len(seq) != len(got):
            print(f"{d.name}: template.json lists {len(seq)} slides, sample.html has {len(got)}")
            problems += 1
            continue
        for entry, m in zip(seq, got):
            if args.write:
                entry.pop("headline", None)
                if m:
                    entry["headline"] = m
                continue
            s = entry.get("headline")
            if (s is None) != (m is None) or (m and (
                    abs(s.get("chars_per_line", -99) - m["chars_per_line"]) > 1 or s.get("lines") != m["lines"])):
                print(f"{d.name} slide {entry['slide']}: headline budget is {s or 'missing'}, measured {m}")
                problems += 1
        if args.write:
            path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
        print(f"{d.name}: " + "  ".join(f"{m['lines']}x{m['chars_per_line']}" if m else "-" for m in got))
    if problems:
        print(f"\n{problems} budget(s) out of date. Run: python3 scripts/copy_budget.py --write")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
