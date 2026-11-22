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

# name, expected gate (None = must pass), old, new
CASES = [
    ("untouched sample", None, "", ""),
    ("hyphenated word that wraps", None, HEADLINE, "Notes before-and-after-before-and-after-before-and-after"),
    ("word wider than its line", "word", HEADLINE, "Pertanggungjawabannyalah"),
    ("faint body text", "contrast", BODY, '<p style="color:#b9b9b9">Here is how to write the ones you will.</p>'),
    ("shape over the headline", "hidden", BODY,
     BODY + '<div style="position:absolute;left:0;right:0;top:500px;height:500px;background:#777"></div>'),
    ("body pulled onto the headline", "overlap", BODY,
     '<p style="margin-top:-90px">Here is how to write the ones you will.</p>'),
    ("slide packed with words", "density", BODY, "<p>" + "Notes pile up when nobody reads them. " * 12 + "</p>"),
    ("decoration opts out", None, BODY,
     BODY + '<div data-decor style="position:absolute;right:90px;top:260px;font-size:60px;color:#e4e4e4">draft</div>'),
]


def main() -> int:
    base = SAMPLE.read_text(encoding="utf-8")
    base = base.replace('href="../../', f'href="{ROOT.as_uri()}/')
    base = base.replace('href="tokens.css"', f'href="{SAMPLE.parent.as_uri()}/tokens.css"')
    slides = len(re.findall(r'<section class="slide', base))
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name, gate, old, new in CASES:
            if old and old not in base:
                print(f"FAIL {name}: the sample no longer holds the text this case edits")
                failed += 1
                continue
            page = Path(tmp) / "case.html"
            page.write_text(base.replace(old, new, 1) if old else base, encoding="utf-8")
            run = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "render_carousel.py"), "--html", str(page),
                 "--out", str(Path(tmp) / "out"), "--slides", str(slides), "--check-fonts", "Plus Jakarta Sans"],
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
