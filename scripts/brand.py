"""
brand.py: put one brand on any carousel while it renders.

A brand kit is a brand.json with the files it names next to it:

  {
    "name": "Kopi Pagi",              shown wherever the template says "Your Brand"
    "handle": "@kopipagi",            shown wherever the template says "@yourhandle"
    "url": "kopipagi.id",             optional, for templates that show an address
    "logo": "logo.svg",               optional, drawn beside the name on every slide
    "logo_on_dark": "logo-light.svg", optional, the version for dark surfaces
    "logo_type": "mark",              "mark" sits before the name, "wordmark" replaces it
    "logo_tint": false,               true draws a one-colour logo in the colour of the text around it
    "accent": "#c2410c",              optional, replaces the template's accent colour
    "accent_on_dark": "#fb923c",      optional, the accent for dark slides
    "language": "id",                 read by the skill when it writes the copy
    "address": "kamu"
  }

render_carousel.py --brand brand.json applies it to the page before the gates
run, so a long name or a faint colour fails the render like any other copy.
The HTML keeps its placeholders, and the same carousel renders for any brand.
"""
import base64
import json
import re
from pathlib import Path

import gates

KEYS = {"name", "handle", "url", "logo", "logo_on_dark", "logo_type", "logo_tint",
        "accent", "accent_on_dark", "language", "address"}
LOGO_FILES = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
# What a template with no template.json (a custom system) calls its brand.
BASE = {"--bg", "--bg2", "--panel", "--text", "--muted", "--soft", "--line", "--line2"}
PLACEHOLDERS = {"brand_placeholder": "Your Brand", "handle_placeholder": "@yourhandle"}


class KitError(ValueError):
    pass


def load(path):
    """Read and check a brand kit. Logos come back as data URIs."""
    path = Path(path).resolve()
    try:
        kit = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise KitError(f"brand kit not found: {path}")
    except json.JSONDecodeError as e:
        raise KitError(f"{path.name} is not valid JSON: {e}")
    if not isinstance(kit, dict):
        raise KitError(f"{path.name} must hold one JSON object")
    unknown = sorted(set(kit) - KEYS)
    if unknown:
        raise KitError(f"{path.name}: unknown keys {unknown}. Known keys: {sorted(KEYS)}")
    for key in ("name", "handle"):
        if not isinstance(kit.get(key), str) or not kit[key].strip():
            raise KitError(f'{path.name}: "{key}" is required')
        kit[key] = kit[key].strip()
    for key in ("accent", "accent_on_dark"):
        if key in kit and not (isinstance(kit[key], str) and re.fullmatch(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", kit[key])):
            raise KitError(f'{path.name}: "{key}" must be a hex colour like #c2410c')
    if kit.get("logo_type", "mark") not in ("mark", "wordmark"):
        raise KitError(f'{path.name}: "logo_type" is "mark" or "wordmark"')
    if not isinstance(kit.get("logo_tint", False), bool):
        raise KitError(f'{path.name}: "logo_tint" is true or false')
    for key in ("logo", "accent"):
        if f"{key}_on_dark" in kit and key not in kit:
            raise KitError(f'{path.name}: "{key}_on_dark" needs "{key}" as well')
    for key in ("logo", "logo_on_dark"):
        if key not in kit:
            continue
        file = (path.parent / str(kit[key])).resolve()
        if file.suffix.lower() not in LOGO_FILES:
            raise KitError(f'{path.name}: "{key}" must be one of {sorted(LOGO_FILES)}')
        if not file.is_file():
            raise KitError(f'{path.name}: "{key}" file not found: {file}')
        # inlined: a page opened from a file may not use another file as a CSS mask
        kit[key] = f"data:{LOGO_FILES[file.suffix.lower()]};base64,{base64.b64encode(file.read_bytes()).decode()}"
    return kit


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def tokens(html):
    """The names of the custom properties a carousel's stylesheets set."""
    text = Path(html).read_text(encoding="utf-8")
    for href in re.findall(r'<link[^>]+href="([^"]+\.css)"', text):
        file = (Path(html).parent / href).resolve()
        if "://" not in href and file.is_file():
            text += file.read_text(encoding="utf-8")
    names = set(re.findall(r"(--[\w-]+)\s*:", text))
    # the surfaces and text colours are not the accent, even where one matches it:
    # a page whose background is the other mode's accent keeps its background
    return sorted(names - {"--accent", "--news-accent", "--on-accent"} - BASE)


def swaps(kit, html):
    """[placeholder, value, what] for every way a template writes the brand.

    The name and handle placeholders come from the template.json beside the
    tokens.css the carousel links. Two more are the same in every template:
    yourbrand.com (an address) and your-brand (a file name)."""
    meta = dict(PLACEHOLDERS)
    link = re.search(r'href="([^"]*tokens\.css)"', Path(html).read_text(encoding="utf-8"))
    if link:
        file = (Path(html).parent / link.group(1)).resolve().parent / "template.json"
        if file.is_file():
            meta.update({k: v for k, v in json.loads(file.read_text(encoding="utf-8")).items() if k in PLACEHOLDERS})
    # the address as the kit writes it, with or without www, in every template
    url = re.sub(r"^https?://", "", kit.get("url", "").strip()).rstrip("/")
    # with no address in the kit, the handle stands where the template shows one
    address = [url, "addresses"] if url else [kit["handle"], "handles"]
    pairs = [
        [meta["brand_placeholder"], kit["name"], "names"],
        [meta["handle_placeholder"], kit["handle"], "handles"],
        ["your-brand", slug(kit["name"]), "names"],
        ["www.yourbrand.com", *address],
        ["yourbrand.com", *address],
    ]
    # the longer placeholder first, in case one contains the other
    pairs.sort(key=lambda p: -len(p[0]))
    return pairs


APPLY = r"""
async ({pairs, name, handle, logo, logoOnDark, wordmark, tint, accent, accentOnDark, tokens}) => {
  const lin = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
  const lum = (c) => 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2]);
  const ratio = (p, q) => { const a = lum(p), b = lum(q); return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05); };
  const dot = document.createElement('canvas').getContext('2d', {willReadFrequently: true});
  dot.canvas.width = dot.canvas.height = 1;
  // paint the colour and read it back: every CSS notation, alpha included
  const rgba = (c) => {
    if (!c || !CSS.supports('color', c)) return null;
    dot.clearRect(0, 0, 1, 1); dot.fillStyle = c; dot.fillRect(0, 0, 1, 1);
    const d = dot.getImageData(0, 0, 1, 1).data;
    return [d[0], d[1], d[2], d[3] / 255];
  };
  const hex = (c) => '#' + c.map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
  // OKLab, so a colour can get lighter or darker and keep its hue and as much of its strength as sRGB holds
  const toLab = (c) => {
    const [r, g, b] = c.map(lin);
    const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
    const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
    const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
    return [0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s];
  };
  const fromLab = ([L, a, b]) => {
    const l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3;
    const m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3;
    const s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3;
    return [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s];
  };
  // the colour at lightness L: full strength if sRGB can show it, else as strong as it can
  const shade = (lab, L) => {
    for (let k = 1; k >= 0; k -= 0.04) {
      const c = fromLab([L, lab[1] * k, lab[2] * k]);
      if (c.every(v => v > -0.002 && v < 1.002))
        return c.map(v => { v = Math.min(1, Math.max(0, v)); return 255 * (v <= 0.0031308 ? 12.92 * v : 1.055 * v ** (1 / 2.4) - 0.055); });
    }
    return L > 0.5 ? [255, 255, 255] : [0, 0, 0];
  };
  const slides = [...document.querySelectorAll('.slide')];
  const report = {counts: {}, logos: [], bare: [], error: null};

  // 1. Name, handle and address, wherever a placeholder stands in the copy.
  for (const s of slides) {
    const w = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
    while (w.nextNode()) {
      const n = w.currentNode;
      for (const [from, to, what] of pairs) {
        const parts = n.textContent.split(from);
        if (parts.length < 2) continue;
        n.textContent = parts.join(to);
        report.counts[what] = (report.counts[what] || 0) + parts.length - 1;
      }
    }
  }

  // 2. The logo, beside the name where the name stands alone, else beside the handle.
  if (logo) {
    const sizes = {};
    for (const src of [logo, logoOnDark]) {
      if (!src) continue;
      const img = new Image();
      img.src = src;
      try { await img.decode(); } catch (e) { report.error = 'the logo is not an image the browser can draw'; return report; }
      sizes[src] = img.naturalWidth / img.naturalHeight;
    }
    const css = document.createElement('style');
    // :where() so a template can restyle the logo; the negative margins keep it
    // from pushing its line taller than the text
    css.textContent = ':where(.brand-logo){display:inline-block;height:1.8em;width:auto;margin:-.4em .55em -.4em 0;'
      + 'vertical-align:middle;flex:none;object-fit:contain}'
      + ':where(.brand-logo.is-wordmark){height:1.6em;margin-right:0}';
    document.head.append(css);
    slides.forEach((s, i) => {
      const alone = (text) => [...s.querySelectorAll('*')].find(e => !e.children.length && e.textContent.trim() === text);
      const named = alone(name), host = named || alone(handle);
      if (!host) { report.bare.push(i + 1); return; }
      // Light text means a dark surface. A mid-tone label (a link blue) reads on
      // both, so there the fill behind it decides.
      const ink = rgba(getComputedStyle(host).color);
      let behind = null;
      for (let n = host; n && !behind; n = n.parentElement) {
        const c = rgba(getComputedStyle(n).backgroundColor);
        if (c && c[3] > 0.5) behind = c;
      }
      const onDark = ink && (lum(ink) > 0.4 || (lum(ink) > 0.175 && behind && lum(behind) < lum(ink)));
      const src = logoOnDark && onDark ? logoOnDark : logo;
      // a tag of its own, so no template rule for span or i lands on it
      const el = document.createElement(tint ? 'brand-logo' : 'img');
      el.className = 'brand-logo' + (tint ? ' is-tint' : '');
      if (tint) {
        el.style.aspectRatio = sizes[src];
        el.style.background = 'currentColor';
        el.style.mask = el.style.webkitMask = `url("${src}") center / contain no-repeat`;
      } else { el.src = src; el.alt = ''; }
      if (wordmark && named) {
        // the wordmark is the name, so it takes the place of the text
        el.classList.add('is-wordmark');
        el.setAttribute(tint ? 'aria-label' : 'alt', name);
        host.textContent = '';
      }
      host.prepend(el);
      report.logos.push(i + 1);
    });
  }

  // 3. The accent: the brand colour, made lighter or darker only as far as text
  // in it needs to stay readable on the surfaces of this slide.
  if (accent) {
    const probe = document.createElement('i');
    const same = (p, q) => p && q && p.every((v, j) => Math.abs(v - q[j]) < 0.01);
    const isDark = (s) => s.classList.contains('mode-dark');
    const token = (s, prop) => rgba(getComputedStyle(s).getPropertyValue(prop).trim());
    // A template repeats its accent in tokens of its own (a tag, a band). Each one that
    // holds the accent of this slide, or of the slides in the other mode, follows the brand.
    const was = slides.map(s => token(s, '--accent'));
    const follow = slides.map((s, i) => {
      const other = was.find((c, k) => isDark(slides[k]) !== isDark(s));
      const hits = tokens.map(prop => [prop, token(s, prop)]).filter(([, c]) => same(c, was[i]) || same(c, other));
      const names = hits.map(h => h[0]);
      // the tokens for text on a fill, by the names templates use: --tag-bg and --tag-fg, --label and --label-ink
      const inksOf = (prop) => tokens.filter(q => q !== prop
        && (q.startsWith(prop + '-') || q === prop.replace(/-bg$/, '-fg') || q === prop.replace(/-bg$/, '-ink')));
      const fills = hits.map(([prop, c]) => ({prop, own: same(c, was[i]), inks: inksOf(prop)}));
      const inked = new Set(fills.flatMap(f => f.inks));
      return fills.filter(f => !inked.has(f.prop))
        .map(f => ({...f, inks: f.inks.map(q => ({prop: q, brand: names.includes(q)}))}));
    });
    const derive = () => slides.forEach((s, i) => {
      const mine = states[i], theirs = states.find(st => st.dark !== mine.dark);
      for (const {prop, own, inks} of follow[i]) {
        const fill = own ? mine : theirs;
        if (!fill) continue;
        s.style.setProperty(prop, hex(fill.now));
        for (const ink of inks) {
          s.style.removeProperty(ink.prop);
          let c = token(s, ink.prop);
          if (ink.brand) {
            // an accent word on an accent fill: the brand colour, as far from the fill as it has to be
            const up = lum(fill.now) < 0.18;
            let L = fill.L;
            c = fill.now;
            while (ratio(c, fill.now) < 4.6 && (up ? L < 1 : L > 0)) {
              L = Math.min(1, Math.max(0, L + (up ? 0.015 : -0.015)));
              c = shade(fill.lab, L);
            }
            s.style.setProperty(ink.prop, hex(c));
          } else if (c && ratio(c, fill.now) < 4.6) {
            s.style.setProperty(ink.prop, ratio([255, 255, 255], fill.now) >= ratio([17, 17, 17], fill.now) ? '#fff' : '#111');
          }
        }
      }
    });
    const paint = (state) => {
      state.s.style.setProperty(state.prop, hex(state.now));
      if (state.prop !== '--accent') return;
      // text a template sets on an accent fill keeps its colour while it reads there
      state.s.style.removeProperty('--on-accent');
      const on = rgba(getComputedStyle(state.s).getPropertyValue('--on-accent').trim());
      if (on && ratio(on, state.now) < 4.6)
        state.s.style.setProperty('--on-accent', ratio([255, 255, 255], state.now) >= ratio([17, 17, 17], state.now) ? '#fff' : '#111');
    };
    // one step lighter or darker; false once it is white or black
    const step = (state) => {
      if (state.up ? state.L >= 1 : state.L <= 0) return false;
      state.L = Math.min(1, Math.max(0, state.L + (state.up ? 0.015 : -0.015)));
      state.now = shade(state.lab, state.L);
      paint(state);
      if (states) derive();
      return true;
    };
    let states = null;
    states = slides.map((s) => {
      s.append(probe);
      const cs = getComputedStyle(s);
      const base = rgba(cs.getPropertyValue('--bg').trim()) || rgba(cs.backgroundColor) || [255, 255, 255, 1];
      const surfaces = [];
      for (const prop of ['--bg', '--bg2', '--panel']) {
        const c = rgba(cs.getPropertyValue(prop).trim());
        if (c) surfaces.push(c.slice(0, 3).map((v, j) => v * c[3] + base[j] * (1 - c[3])));
      }
      probe.remove();
      if (!surfaces.length) surfaces.push(base.slice(0, 3));
      const dark = isDark(s);
      const lab = toLab(rgba(dark && accentOnDark ? accentOnDark : accent).slice(0, 3));
      // lighter on dark surfaces, darker on light ones
      const up = surfaces.reduce((a, q) => a + lum(q), 0) / surfaces.length < 0.18;
      const state = {s, prop: '--accent', dark, lab, up, L: lab[0], now: shade(lab, lab[0])};
      const worst = (c) => Math.min(...surfaces.map(q => ratio(c, q)));
      paint(state);
      while (worst(state.now) < 4.6 && step(state));
      return state;
    });
    derive();
    // the accent word of a headline set on a photo has a token of its own, lighter than the accent
    const onPhoto = slides.map((s) => {
      if (!getComputedStyle(s).getPropertyValue('--news-accent').trim()) return null;
      const lab = toLab(rgba(accentOnDark || accent).slice(0, 3));
      const state = {s, prop: '--news-accent', lab, up: true, L: lab[0], now: shade(lab, lab[0])};
      paint(state);
      while (ratio(state.now, [24, 24, 24]) < 4.6 && step(state));
      return state;
    });
    // kept for settle(), which goes on from here against the rendered pixels
    window.__brand = {
      step: (i, photo) => step(photo ? onPhoto[i] : states[i]),
      seen: () => states.map(st => [st.dark ? 'dark' : 'light', hex(st.now)]),
      now: (i) => [states[i].now, onPhoto[i] ? onPhoto[i].now : null],
      // one accent per mode: every slide takes the one that had to move furthest
      even: () => {
        for (const dark of [false, true]) {
          const group = states.filter(st => st.dark === dark);
          const far = group.reduce((a, st) => (!a || Math.abs(st.L - st.lab[0]) > Math.abs(a.L - a.lab[0]) ? st : a), null);
          for (const st of group) {
            if (st.lab.some((v, j) => v !== far.lab[j])) continue;
            st.L = far.L; st.now = far.now; paint(st);
          }
        }
        derive();
      },
    };
  }
  return report;
}
"""

async def apply(page, kit, html):
    """Apply the kit to the loaded page. Returns the lines to print, or raises KitError."""
    pairs = swaps(kit, html)
    report = await page.evaluate(APPLY, {
        "pairs": pairs, "name": kit["name"], "handle": kit["handle"],
        "logo": kit.get("logo"), "logoOnDark": kit.get("logo_on_dark"),
        "wordmark": kit.get("logo_type") == "wordmark", "tint": kit.get("logo_tint", False),
        "accent": kit.get("accent"), "accentOnDark": kit.get("accent_on_dark"), "tokens": tokens(html),
    })
    if report["error"]:
        raise KitError(report["error"])
    if not report["counts"] and not report["logos"]:
        raise KitError("nothing on the slides to brand: the copy holds none of the placeholders "
                       f"{[p[0] for p in pairs]}")
    found = ", ".join(f"{n} {what}" for what, n in report["counts"].items())
    lines = [f'brand: {kit["name"]} {kit["handle"]}: {found or "no placeholders in the copy"}']
    if kit.get("logo"):
        lines.append(f'  logo on slides {report["logos"]}' +
                     (f', none on {report["bare"]} (no name or handle standing alone there)' if report["bare"] else ""))
    return lines


async def settle(page, lab, kit, slides, min_contrast=4.5):
    """Finish the accent against the rendered slides, and return the lines to print.

    apply() made the accent readable on the surface tokens of each slide. Text in
    the accent also sits on cards, tints and photos, which only the pixels know,
    so each slide is measured and its accent moved on while such text is too faint.
    Leaves the slides hidden one by one, as the render loop expects to set them."""
    show = "i => document.querySelectorAll('.slide').forEach((c, k) => { c.style.display = k === i ? 'block' : 'none'; })"
    for i in range(slides if kit.get("accent") else 0):
        await page.evaluate(show, i)
        for _ in range(40):
            info = await gates.measure(page, lab, i)
            faint = [l for l in info["lines"]
                     if round(l["contrast"], 2) < (min(min_contrast, 3.0) if gates.is_large(l) else min_contrast)]
            moved = False
            for photo, now in enumerate(await page.evaluate("i => window.__brand.now(i)", i)):
                if now and any(all(abs(a - b) <= 2 for a, b in zip(l["color"], now)) for l in faint):
                    moved = await page.evaluate("([i, photo]) => window.__brand.step(i, photo)", [i, photo]) or moved
            if not moved:
                break
    seen = {}
    if kit.get("accent"):
        for mode, colour in await page.evaluate("() => { window.__brand.even(); return window.__brand.seen(); }"):
            if colour not in seen.setdefault(mode, []):
                seen[mode].append(colour)
        asked = {"light": kit["accent"].lower(), "dark": kit.get("accent_on_dark", kit["accent"]).lower()}
    lines = []
    for mode, colours in seen.items():
        moved = [c for c in colours if c != _hex6(asked[mode])]
        lines.append(f"  accent on {mode} slides: {', '.join(colours)}" +
                     (f" (from {asked[mode]}, moved so text in it reads there)" if moved else ""))
    # A logo the same colour as the surface under it is on the slide and cannot be seen.
    lost = []
    for i in range(slides if kit.get("logo") else 0):
        await page.evaluate(show, i)
        logo = page.locator(".slide").nth(i).locator(".brand-logo")
        if not await logo.count():
            continue
        box = await logo.first.bounding_box()
        if not box or box["width"] < 1 or box["height"] < 1:
            lost.append(i + 1)
            continue
        shown = await page.screenshot(type="png", clip=box)
        await logo.first.evaluate("e => { e.style.visibility = 'hidden'; }")
        hidden = await page.screenshot(type="png", clip=box)
        await logo.first.evaluate("e => { e.style.visibility = ''; }")
        if await lab.evaluate(SEEN, [base64.b64encode(shown).decode(), base64.b64encode(hidden).decode()]) < 0.04:
            lost.append(i + 1)
    if lost:
        raise KitError(f"the logo cannot be seen on slides {lost}: it is the colour of the surface under it. "
                       'Give "logo_on_dark" a version for dark surfaces, or set "logo_tint": true for a one-colour logo')
    return lines


# Share of the pixels in a box that the logo changes enough to see.
SEEN = """
async ([a, b]) => {
  const load = async (d) => { const i = new Image(); i.src = 'data:image/png;base64,' + d; await i.decode(); return i; };
  const [x, y] = [await load(a), await load(b)];
  const c = document.createElement('canvas'); c.width = x.width; c.height = x.height;
  const g = c.getContext('2d', {willReadFrequently: true});
  g.drawImage(x, 0, 0); const p = g.getImageData(0, 0, c.width, c.height).data;
  g.drawImage(y, 0, 0); const q = g.getImageData(0, 0, c.width, c.height).data;
  let n = 0;
  for (let k = 0; k < p.length; k += 4)
    if (Math.abs(p[k] - q[k]) + Math.abs(p[k + 1] - q[k + 1]) + Math.abs(p[k + 2] - q[k + 2]) > 96) n++;
  return n / (p.length / 4);
}
"""


def _hex6(colour):
    c = colour.lstrip("#")
    return "#" + ("".join(ch * 2 for ch in c) if len(c) == 3 else c)
