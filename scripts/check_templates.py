#!/usr/bin/env python3
"""
check_templates.py: static consistency check for every template in templates/.

For each templates/NN-slug/ it verifies:
  - template.json has the required keys and its number and id match the folder
  - every font is declared in fonts/fonts.css
  - the preview image exists
  - sample.html has one <section class="slide ..."> per sequence entry, and each
    one carries the listed pattern (data-pattern + its p-* class) and mode
  - modes alternate when modes_alternate is true
  - (warning only) no two adjacent slides share a pattern

Exit 1 on any problem. Pass --render-cmd to print the matching render commands
(one per line) for CI, and --format feed or --format story with it for the
commands of the other two output sizes.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ["number", "id", "name", "vibe", "fonts", "size", "sequence", "preview"]
PATTERN_CLASS = {
    "cover-big-type": "p-cover-bt", "cover-split": "p-cover-split",
    "kicker-statement": "p-statement", "stat-band": "p-stats",
    "concept-number": "p-concept", "quote": "p-quote", "two-cards": "p-cards",
    "image-hero": "p-imghero", "process-steps": "p-process",
    "myth-fact": "p-mythfact", "big-number": "p-bignumber",
    "takeaway": "p-takeaway", "cover-poster": "p-poster", "cover-hook": "p-hook",
    "cover-label": "p-label", "cover-object": "p-objcover",
    "pointer": "p-pointer", "showcase": "p-showcase", "note": "p-note",
    "cover-news": "p-news",
}
SECTION_TAG = re.compile(r'<section\b[^>]*>')
CLASS_ATTR = re.compile(r'\sclass="([^"]*)"')
DATA_PATTERN = re.compile(r'\sdata-pattern="([^"]+)"')


def slide_sections(html: str) -> list:
    out = []
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    for tag in SECTION_TAG.findall(html):
        m = CLASS_ATTR.search(tag)
        classes = m.group(1).split() if m else []
        if "slide" in classes:
            out.append((classes, tag))
    return out


def check(tdir: Path, fonts_declared: set) -> list:
    errs = []
    try:
        t = json.loads((tdir / "template.json").read_text())
    except Exception as e:
        return [f"template.json unreadable: {e}"]
    missing = [k for k in REQUIRED if k not in t]
    if missing:
        return [f"template.json missing keys: {missing}"]

    if t["id"] != tdir.name:
        errs.append(f"id {t['id']!r} does not match folder")
    if not tdir.name.startswith(f"{t['number']:02d}-"):
        errs.append(f"number {t['number']} does not match folder")
    for f in t["fonts"]:
        if f not in fonts_declared:
            errs.append(f"font {f!r} not declared in fonts/fonts.css")
    if not (ROOT / t["preview"]).exists():
        errs.append(f"preview {t['preview']} not found")

    html = (tdir / "sample.html").read_text()
    sections = slide_sections(html)
    seq = t["sequence"]
    if len(sections) != len(seq):
        errs.append(f"sample.html has {len(sections)} slides, sequence has {len(seq)}")
    for s, (classes, tag) in zip(seq, sections):
        n, pat, mode = s["slide"], s["pattern"], s["mode"]
        dp = DATA_PATTERN.search(tag)
        if not dp or dp.group(1) != pat:
            errs.append(f"slide {n}: data-pattern {dp.group(1) if dp else None!r}, expected {pat!r}")
        want = PATTERN_CLASS.get(pat)
        if want is None:
            errs.append(f"slide {n}: unknown pattern {pat!r}")
        elif want not in classes:
            errs.append(f"slide {n}: class {want!r} missing for {pat!r}")
        extra = [c for c in classes if c in PATTERN_CLASS.values() and c != want]
        if extra:
            errs.append(f"slide {n}: extra pattern classes {extra}")
        if mode not in ("light", "dark"):
            errs.append(f"slide {n}: unknown mode {mode!r}")
        elif (mode == "dark") != ("mode-dark" in classes):
            errs.append(f"slide {n}: mode {mode!r} does not match markup")
    if t.get("modes_alternate"):
        modes = [s["mode"] for s in seq]
        for i in range(1, len(modes)):
            if modes[i] == modes[i - 1]:
                errs.append(f"slides {i} and {i + 1} share mode {modes[i]!r}")
    return errs


def warnings(tdir: Path) -> list:
    seq = json.loads((tdir / "template.json").read_text())["sequence"]
    pats = [s["pattern"] for s in seq]
    return [f"slides {i} and {i + 1} share pattern {pats[i]!r}"
            for i in range(1, len(pats)) if pats[i] == pats[i - 1]]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--render-cmd", action="store_true",
                    help="print one render command per template instead of a report")
    ap.add_argument("--format", choices=["portrait", "feed", "story"], default="portrait",
                    help="with --render-cmd: print the commands for this output format")
    args = ap.parse_args()

    fonts_declared = set(re.findall(r'font-family:\s*"([^"]+)"',
                                    (ROOT / "fonts/fonts.css").read_text()))
    tdirs = sorted(p for p in (ROOT / "templates").iterdir() if p.is_dir())
    if args.render_cmd:
        for d in tdirs:
            t = json.loads((d / "template.json").read_text())
            if args.format == "portrait":
                size = f'--out out/{d.name} --width {t["size"]["width"]} --height {t["size"]["height"]}'
            else:
                size = f'--out out/{args.format}/{d.name} --format {args.format}'
            print(f'python3 scripts/render_carousel.py --html templates/{d.name}/sample.html {size} '
                  f'--slides {len(t["sequence"])} --check-fonts "{",".join(t["fonts"])}"')
        return 0

    failed = False
    for d in tdirs:
        errs = check(d, fonts_declared)
        print(f"{d.name}: {'OK' if not errs else 'FAILED'}")
        for e in errs:
            print(f"  {e}")
        if not errs:
            for w in warnings(d):
                print(f"  warning: {w}")
        failed |= bool(errs)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
