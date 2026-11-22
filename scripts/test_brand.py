#!/usr/bin/env python3
"""
test_brand.py: prove that render_carousel.py --brand applies a kit, and rejects a bad one.

Each case writes a brand.json beside the example logos, renders one template
with it, and names what must happen: the gate that fires (None = must pass)
and the text the renderer must print.

  python3 scripts/test_brand.py
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KIT = ROOT / "examples" / "brand-kit"
BASE = {"name": "Kopi Pagi", "handle": "@kopipagi"}
LOGOS = {"logo": "logo.svg", "logo_on_dark": "logo-on-dark.svg"}
MONO = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96">'
        '<path d="M48 6 90 48 48 90 6 48Z"/></svg>')
WORD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 60" width="300" height="60">'
        '<rect width="300" height="60" rx="12"/></svg>')

# name, template, kit (a dict, or the raw text of brand.json), expected gate, text the output must hold
CASES = [
    ("name and handle only", "02-clean-minimal", BASE, None, "brand: Kopi Pagi @kopipagi: 8 names, 8 handles"),
    ("the example kit", "02-clean-minimal", json.loads((KIT / "brand.json").read_text(encoding="utf-8")), None,
     "logo on slides [1, 2, 3, 4, 5, 6, 7, 8]"),
    ("a template with its own placeholders", "01-morning-cup", BASE, None, "9 names, 7 handles"),
    ("file name and address forms of the brand", "25-code-editor", {**BASE, "url": "https://www.kopipagi.id/"}, None, "names"),
    ("an address where the template shows one", "13-news-card", {**BASE, "url": "kopipagi.id"}, None, "1 addresses"),
    ("no address in the kit: the handle stands in", "13-news-card", BASE, None, "8 handles"),
    ("accent that is readable as it is", "02-clean-minimal", {**BASE, "accent": "#0b1f4b", "accent_on_dark": "#7dd3fc"}, None,
     "accent on light slides: #0b1f4b\n"),
    ("pale accent is darkened on light slides", "02-clean-minimal", {**BASE, "accent": "#ffd400"}, None,
     "(from #ffd400, moved so text in it reads there)"),
    ("accent on a template with tag and band tokens", "14-news-split", {**BASE, "accent": "#ff4fa3"}, None, "accent on dark slides"),
    ("one-colour logo drawn in the text colour", "17-bento-grid", {**BASE, "logo": "mono.svg", "logo_tint": True}, None,
     "logo on slides"),
    ("wordmark in place of the name", "02-clean-minimal", {**BASE, "logo": "word.svg", "logo_type": "wordmark", "logo_tint": True},
     None, "logo on slides"),
    ("long name and handle", "07-paper-stack", {"name": "Sekolah Bisnis Nusantara", "handle": "@sekolahbisnisnusantara"}, None, "8 names"),
    ("black logo on dark slides", "03-bold-contrast", {**BASE, "logo": "mono.svg"}, "brand", "the logo cannot be seen on slides"),
    ("name missing", "02-clean-minimal", {"handle": "@kopipagi"}, "brand", '"name" is required'),
    ("unknown key", "02-clean-minimal", {**BASE, "colour": "#000"}, "brand", "unknown keys ['colour']"),
    ("accent that is not a hex colour", "02-clean-minimal", {**BASE, "accent": "orange"}, "brand", "must be a hex colour"),
    ("logo file missing", "02-clean-minimal", {**BASE, "logo": "nope.svg"}, "brand", "file not found"),
    ("logo of an unsupported type", "02-clean-minimal", {**BASE, "logo": "brand.json"}, "brand", "must be one of"),
    ("logo that is not an image", "02-clean-minimal", {**BASE, "logo": "broken.png"}, "brand", "not an image the browser can draw"),
    ("dark logo without the main one", "02-clean-minimal", {**BASE, "logo_on_dark": "logo-on-dark.svg"}, "brand", 'needs "logo"'),
    ("malformed JSON", "02-clean-minimal", '{"name": "Kopi Pagi",', "brand", "is not valid JSON"),
    ("name wider than its line", "21-bauhaus", {"name": "Perpustakaanwilayahnusantaraindonesiaraya" * 2, "handle": "@kopipagi"},
     "edge", ""),
]


def main() -> int:
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for file in ("logo.svg", "logo-on-dark.svg"):
            shutil.copy(KIT / file, tmp / file)
        (tmp / "mono.svg").write_text(MONO, encoding="utf-8")
        (tmp / "word.svg").write_text(WORD, encoding="utf-8")
        (tmp / "broken.png").write_text("not a picture", encoding="utf-8")
        for name, template, kit, gate, text in CASES:
            (tmp / "brand.json").write_text(kit if isinstance(kit, str) else json.dumps(kit), encoding="utf-8")
            meta = json.loads((ROOT / "templates" / template / "template.json").read_text(encoding="utf-8"))
            run = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "render_carousel.py"),
                 "--html", str(ROOT / "templates" / template / "sample.html"), "--out", str(tmp / "out"),
                 "--slides", str(len(meta["sequence"])), "--brand", str(tmp / "brand.json")],
                capture_output=True, text=True)
            fired = re.findall(r"GATE FAILED \((.+?)\)", run.stdout)
            ok = ((not fired and run.returncode == 0) if gate is None else gate in fired and run.returncode != 0) \
                and text in run.stdout
            print(f"{'ok  ' if ok else 'FAIL'} {name}: expected {gate or 'pass'}, got {fired or 'pass'}")
            if not ok:
                print(f"     wanted in the output: {text!r}\n" + run.stdout[-700:] + run.stderr[-700:])
                failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
