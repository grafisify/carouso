#!/usr/bin/env python3
"""
test_gates.py: prove that each copy and legibility gate of render_carousel.py fires.

Every case breaks the Clean Minimal sample in one way and names the gate that
must reject it. A case with no gate must render clean. Exit 1 on any mismatch.

  python3 scripts/test_gates.py
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLE = ROOT / "templates" / "02-clean-minimal" / "sample.html"
HEADLINE = 'Most notes are <span class="accent">never read again.</span>'
BODY = "<p>Here is how to write the ones you will.</p>"

# name, expected gate (None = must pass), old, new, then any extra renderer arguments
CASES = [
    ("untouched sample", None, "", ""),
    ("hyphenated word that wraps", None, HEADLINE, "Notes before-and-after-before-and-after-before-and-after"),
    ("word wider than its line", "word", HEADLINE, "Pertanggungjawabannyalah"),
    ("faint body text", "contrast", BODY, '<p style="color:#b9b9b9">Here is how to write the ones you will.</p>'),
    ("translucent sheet over the slide", "contrast", BODY,
     BODY + '<div style="position:absolute;inset:0;background:rgba(255,255,255,.8)"></div>'),
    ("shape over the headline", "hidden", BODY,
     BODY + '<div style="position:absolute;left:0;right:0;top:500px;height:500px;background:#777"></div>'),
    ("body pulled onto the headline", "overlap", BODY,
     '<p style="margin-top:-90px">Here is how to write the ones you will.</p>'),
    ("slide packed with words", "density", BODY, "<p>" + "Notes pile up when nobody reads them. " * 12 + "</p>"),
    ("light text on a dark slide written with color-mix()", None, '<div class="kicker">The gap</div>',
     '<div class="kicker" style="color:color-mix(in srgb, var(--text) 92%, var(--bg))">The gap</div>'),
    ("unpainted words do not count", None, BODY,
     BODY + '<div style="display:none"><p>' + "Hidden draft copy. " * 40 + '</p></div>'
          + '<p style="color:transparent;position:absolute">' + "Clear ink. " * 40 + '</p>'
          + '<div style="content-visibility:hidden;position:absolute;left:90px;top:90px;width:600px"><p>' + "Skipped by the browser. " * 30 + '</p></div>'),
    ("faint text inside display:contents", "contrast", BODY,
     '<p style="display:contents;color:#b9b9b9">Here is how to write the ones you will.</p>'),
    ("outlined words still count", "density", BODY,
     '<p style="-webkit-text-fill-color:transparent;-webkit-text-stroke:1px #111">'
     + "Notes pile up when nobody reads them. " * 12 + "</p>"),
    ("decoration opts out", None, BODY,
     BODY + '<div data-decor style="position:absolute;right:90px;top:260px;font-size:60px;color:#e4e4e4">draft</div>'),
    ("sample reflowed to 4:5", None, "", "", "--format", "feed"),
    ("sample reflowed to 9:16", None, "", "", "--format", "story"),
    ("text under the app interface of a 9:16 slide", "safe", BODY,
     BODY + '<p style="position:absolute;left:0;top:-60px">Posted this morning</p>', "--format", "story"),
    ("a card that bleeds off the slide still keeps its text out of the 9:16 zones", "safe", BODY,
     BODY + '<div data-bleed style="position:absolute;left:82px;bottom:-40px;height:200px"><span>Layout</span></div>',
     "--format", "story"),
    ("the same text is fine at 3:4", None, BODY,
     BODY + '<p style="position:absolute;left:0;top:-60px">Posted this morning</p>'),
]


def main() -> int:
    base = SAMPLE.read_text(encoding="utf-8")
    base = base.replace('href="../../', f'href="{ROOT.as_uri()}/')
    base = base.replace('href="tokens.css"', f'href="{SAMPLE.parent.as_uri()}/tokens.css"')
    slides = len(re.findall(r'<section class="slide', base))
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name, gate, old, new, *extra in CASES:
            if old and old not in base:
                print(f"FAIL {name}: the sample no longer holds the text this case edits")
                failed += 1
                continue
            page = Path(tmp) / "case.html"
            page.write_text(base.replace(old, new, 1) if old else base, encoding="utf-8")
            run = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "render_carousel.py"), "--html", str(page),
                 "--out", str(Path(tmp) / "out"), "--slides", str(slides), "--check-fonts", "Plus Jakarta Sans", *extra],
                capture_output=True, text=True)
            fired = re.findall(r"GATE FAILED \((.+?)\)", run.stdout)
            ok = (not fired and run.returncode == 0) if gate is None else gate in fired
            print(f"{'ok  ' if ok else 'FAIL'} {name}: expected {gate or 'pass'}, got {fired or 'pass'}")
            if not ok:
                print(run.stdout[-600:] + run.stderr[-600:])
                failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
