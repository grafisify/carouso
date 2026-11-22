"""
gates.py: the legibility gates used by render_carousel.py.

They work on what the slide looks like, not on what the CSS says. Each slide is
captured twice, as rendered and with the text fill hidden, and the two captures
are compared in a canvas on a blank page, so nothing beyond Playwright is needed.

  measure(page, lab, i) -> {
    "words":   visible word count of the slide,
    "lines":   one entry per visible line of text, with the contrast against
               what is painted behind it and the longest stretch with no ink,
    "overlap": pairs of text lines from different elements that sit on each other,
    "unsafe":  text painted outside keep_clear, when it is given,
  }
  judge(info, min_contrast, max_words) -> {"contrast": [...], "hidden": [...],
                                           "overlap": [...], "density": [...], "safe": [...]}
"""
import base64

HIDE_TEXT = (
    "*,*::before,*::after{-webkit-text-fill-color:transparent!important;"
    "text-shadow:none!important;-webkit-text-stroke-color:transparent!important;"
    "text-decoration-color:transparent!important}"
)
# Text that is decoration on purpose opts out of the legibility gates.
DECOR = '[data-decor],[aria-hidden="true"]'
# Cards that run off the slide on purpose: their text may be cut, so it skips the
# legibility gates too, but it is still copy and must stay out of the story zones.
BLEED = '.peek,[data-bleed]'


def _hide_all_text(scopes):
    """CSS that hides whatever the text in these scopes paints: fill, outline, shadow,
    underline, and the gradient fills and SVG text that measure() tags."""
    def each(tail):
        return ','.join(f'{scope}{tail}' for scope in scopes)
    return (
        each('') + ',' + each('::before') + ',' + each('::after') + ',' + each('::marker') +
        "{-webkit-text-fill-color:transparent!important;text-shadow:none!important;"
        "-webkit-text-stroke-color:transparent!important;text-decoration-color:transparent!important}"
        + each('[data-gate-clip]') + "{background-image:none!important;background-color:transparent!important}"
        + each('[data-gate-svg]') + "{fill:transparent!important;stroke:transparent!important}"
    )


# The safe gate compares a story zone with the decoration's text hidden against the
# same zone with all text hidden, so what differs is copy. Hiding the copy alone
# would take the decoration inside it along: the text fill is inherited.
HIDE_DECOR = _hide_all_text([f'{d}{sub}' for d in DECOR.split(',') for sub in ('', ' *')])
HIDE_ALL = _hide_all_text(['*'])

COLLECT = """
([i, decor, bleed]) => {
  const s = document.querySelectorAll('.slide')[i];
  const b = s.getBoundingClientRect();
  // Painting the colour and reading the pixel back handles every CSS notation:
  // color-mix() computes to color(srgb 1 1 1), whose channels are not bytes.
  const dot = document.createElement('canvas').getContext('2d', {willReadFrequently: true});
  dot.canvas.width = dot.canvas.height = 1;
  const known = {};
  const rgba = (c) => {
    if (!known[c]) {
      dot.clearRect(0, 0, 1, 1); dot.fillStyle = c; dot.fillRect(0, 0, 1, 1);
      const d = dot.getImageData(0, 0, 1, 1).data;
      known[c] = [d[0], d[1], d[2], d[3] / 255];
    }
    return known[c];
  };
  const blocks = [], lines = [], boxes = [];
  const pen = document.createElement('canvas').getContext('2d');
  let words = 0;
  const w = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) {
    const n = w.currentNode, el = n.parentElement, text = n.textContent.trim();
    if (!text) continue;
    const cs = getComputedStyle(el);
    const r = document.createRange();
    r.selectNodeContents(n);
    const rects = [...r.getClientRects()];
    // Only painted text counts. No rect means no box (a display:none ancestor);
    // checkVisibility() would also drop display:contents, whose text does render.
    if (cs.visibility === 'hidden' || !rects.length) continue;
    let opacity = 1, block = el, clipped = false;
    for (let a = el; a && a !== s.parentElement; a = a.parentElement) {
      const as = getComputedStyle(a);
      // content-visibility:hidden keeps the boxes but paints nothing inside
      opacity *= as.contentVisibility === 'hidden' ? 0 : parseFloat(as.opacity);
      clipped = clipped || as.backgroundClip.includes('text');
    }
    const fill = rgba(cs.webkitTextFillColor || cs.color);
    // a transparent fill still shows when it is outlined, shadowed or lets a clipped background through
    const inked = fill[3] >= 0.05 || clipped || cs.textShadow !== 'none'
      || (parseFloat(cs.webkitTextStrokeWidth) > 0 && rgba(cs.webkitTextStrokeColor)[3] >= 0.05);
    if (opacity < 0.05 || !inked) continue;
    words += text.split(/\\s+/).filter(t => /[\\p{L}\\p{N}]/u.test(t)).length;
    if (el.closest(decor)) continue;
    // every painted piece of copy, so the safe gate can name what it finds in a story zone
    for (const q of rects) boxes.push({text: text.slice(0, 28), x: q.left - b.left, y: q.top - b.top,
                                       x2: q.right - b.left, y2: q.bottom - b.top});
    // marks with no letter or digit (quote marks, arrows) skip the legibility gates
    if (!/[\\p{L}\\p{N}]/u.test(text)) continue;
    // Where the glyphs really are inside the line box: a 300px numeral has a
    // tall box but its ink stops well short of the label under it.
    pen.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    const shown = cs.textTransform === 'uppercase' ? text.toUpperCase() : text;
    const m = pen.measureText(shown);
    const box = m.fontBoundingBoxAscent + m.fontBoundingBoxDescent;
    if (el.closest(bleed)) continue;
    if (fill[3] * opacity < 0.05) continue;   // outlined or gradient text has no one colour to measure
    while (block !== s && /^(inline|contents)/.test(getComputedStyle(block).display)) block = block.parentElement;
    let blockId = blocks.indexOf(block);
    if (blockId < 0) blockId = blocks.push(block) - 1;
    for (const q of rects) {
      if (q.width < 6 || q.height < 6) continue;
      const x = Math.max(0, q.left - b.left), y = Math.max(0, q.top - b.top);
      const x2 = Math.min(b.width, q.right - b.left), y2 = Math.min(b.height, q.bottom - b.top);
      if (x2 - x < 6 || y2 - y < 6) continue;
      // scaled to the rect, which is taller than the line box on rotated text
      const k = q.height / box;
      const top = q.top - b.top + k * (m.fontBoundingBoxAscent - m.actualBoundingBoxAscent);
      const bottom = q.top - b.top + k * (m.fontBoundingBoxAscent + m.actualBoundingBoxDescent);
      lines.push({text: text.slice(0, 28), block: blockId, x, y, w: x2 - x, h: y2 - y, top, bottom,
                  color: [fill[0], fill[1], fill[2]], alpha: fill[3] * opacity,
                  size: parseFloat(cs.fontSize), weight: parseInt(cs.fontWeight) || 400});
    }
  }
  const overlap = [];
  for (let a = 0; a < lines.length; a++) for (let c = a + 1; c < lines.length; c++) {
    const p = lines[a], q = lines[c];
    if (p.block === q.block) continue;
    const ow = Math.min(p.x + p.w, q.x + q.w) - Math.max(p.x, q.x);
    const oh = Math.min(p.bottom, q.bottom) - Math.max(p.top, q.top);
    if (ow > 8 && oh > 0.3 * Math.min(p.bottom - p.top, q.bottom - q.top)) overlap.push([p.text, q.text]);
  }
  return {words, lines, overlap, boxes};
}
"""

ANALYZE = """
async ([shown, hidden, lines]) => {
  const load = async (b64) => {
    const img = new Image();
    img.src = 'data:image/jpeg;base64,' + b64;
    await img.decode();
    const c = document.createElement('canvas');
    c.width = img.naturalWidth; c.height = img.naturalHeight;
    const g = c.getContext('2d', {willReadFrequently: true});
    g.drawImage(img, 0, 0);
    return g;
  };
  const A = await load(shown), B = await load(hidden);
  const lum = (c) => { const f = c.map(v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
                       return 0.2126 * f[0] + 0.7152 * f[1] + 0.0722 * f[2]; };
  return lines.map(l => {
    const x = Math.floor(l.x), y = Math.floor(l.y), w = Math.max(1, Math.floor(l.w)), h = Math.max(1, Math.floor(l.h));
    const a = A.getImageData(x, y, w, h).data, b = B.getImageData(x, y, w, h).data;
    // contrast of the text colour against the background, cell by cell
    const cell = Math.max(8, Math.round(h / 2)), ratios = [];
    for (let cx = 0; cx < w; cx += cell) for (let cy = 0; cy < h; cy += cell) {
      let r = 0, g = 0, bl = 0, n = 0;
      for (let px = cx; px < Math.min(w, cx + cell); px++) for (let py = cy; py < Math.min(h, cy + cell); py++) {
        const k = (py * w + px) * 4; r += b[k]; g += b[k + 1]; bl += b[k + 2]; n++;
      }
      const bg = [r / n, g / n, bl / n];
      const fg = l.color.map((v, j) => v * l.alpha + bg[j] * (1 - l.alpha));
      const L1 = lum(fg), L2 = lum(bg);
      ratios.push((Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05));
    }
    ratios.sort((p, q) => p - q);
    // The same contrast read off the glyphs as painted. Anything translucent
    // laid over the text fades them, and the declared colour cannot show that.
    const span = Math.max(48, 2 * h), seen = [], fade = [];
    for (let cx = 0; cx < w; cx += span) {
      const ink = [];
      for (let px = cx; px < Math.min(w, cx + span); px++) for (let py = 0; py < h; py++) {
        const k = (py * w + px) * 4;
        const d = Math.abs(a[k] - b[k]) + Math.abs(a[k + 1] - b[k + 1]) + Math.abs(a[k + 2] - b[k + 2]);
        if (d > 24) ink.push([d, k]);
      }
      if (ink.length < 40) continue;
      // the strongest pixels are stroke centres; the rest is anti-aliased edge
      ink.sort((p, q) => q[0] - p[0]);
      const core = ink.slice(0, Math.max(8, Math.floor(ink.length * 0.05)));
      const fg = [0, 0, 0], bg = [0, 0, 0];
      for (const [, k] of core) for (let j = 0; j < 3; j++) { fg[j] += a[k + j] / core.length; bg[j] += b[k + j] / core.length; }
      const want = l.color.map((v, j) => v * l.alpha + bg[j] * (1 - l.alpha));
      const ratio = (p, q) => { const L1 = lum(p), L2 = lum(q); return (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05); };
      seen.push(ratio(fg, bg)); fade.push(ratio(fg, bg) / ratio(want, bg));
    }
    seen.sort((p, q) => p - q); fade.sort((p, q) => p - q);
    // longest horizontal stretch where the text left no mark on the slide
    let gap = 0, run = 0;
    for (let px = 0; px < w; px++) {
      let ink = false;
      for (let py = 0; py < h && !ink; py++) {
        const k = (py * w + px) * 4;
        ink = Math.abs(a[k] - b[k]) > 30 || Math.abs(a[k + 1] - b[k + 1]) > 30 || Math.abs(a[k + 2] - b[k + 2]) > 30;
      }
      run = ink ? 0 : run + 1;
      if (run > gap) gap = run;
    }
    let contrast = ratios[Math.floor(ratios.length * 0.1)];
    // Anti-aliasing alone costs thin 20px type up to 15% (measured on the 36 samples),
    // so the painted value only takes over when the glyphs are clearly fainter than declared.
    if (seen.length && fade[Math.floor(fade.length / 2)] < 0.8) contrast = Math.min(contrast, seen[Math.floor(seen.length * 0.1)]);
    return {contrast, gap};
  });
}
"""


# Which copy leaves a mark in a strip of the slide: the strip with the copy showing
# against the strip with it hidden. Read off the pixels, so rotation, outlines,
# shadows, text-transform and generated content need no modelling.
ZONE = """
async ([shown, hidden, top, boxes]) => {
  const load = async (b64) => {
    const img = new Image();
    img.src = 'data:image/png;base64,' + b64;
    await img.decode();
    const c = document.createElement('canvas');
    c.width = img.naturalWidth; c.height = img.naturalHeight;
    const g = c.getContext('2d', {willReadFrequently: true});
    g.drawImage(img, 0, 0);
    return g.getImageData(0, 0, c.width, c.height);
  };
  const A = await load(shown), B = await load(hidden), w = A.width, h = A.height;
  const ink = new Uint8Array(w * h);
  let total = 0, first = -1;
  for (let k = 0; k < w * h; k++) {
    const d = Math.abs(A.data[4 * k] - B.data[4 * k]) + Math.abs(A.data[4 * k + 1] - B.data[4 * k + 1])
            + Math.abs(A.data[4 * k + 2] - B.data[4 * k + 2]);
    if (d > 48) { ink[k] = 1; total++; if (first < 0) first = Math.floor(k / w); }
  }
  const found = [];
  // an outline or a shadow reaches a little past the box of its text: look there
  // only when no box holds the ink, or the neighbours of the culprit get named too
  for (const pad of [0, 12]) {
    if (found.length || total < 4) break;
    for (const q of boxes) {
      const x = Math.max(0, Math.floor(q.x - pad)), x2 = Math.min(w, Math.ceil(q.x2 + pad));
      const y = Math.max(0, Math.floor(q.y - pad - top)), y2 = Math.min(h, Math.ceil(q.y2 + pad - top));
      let n = 0;
      for (let py = y; py < y2; py++) for (let px = x; px < x2; px++) n += ink[py * w + px];
      if (n >= 4 && !found.includes(q.text)) found.push(q.text);
    }
  }
  // generated content has no text node to name
  if (!found.length && total >= 4) found.push('text at y=' + (top + first));
  return found;
}
"""


async def measure(page, lab, i, keep_clear=None):
    """Measure slide i. The slide must already be the only one displayed.

    keep_clear is (top, bottom): the first and last slide rows copy may be painted on.
    """
    info = await page.evaluate(COLLECT, [i, DECOR, BLEED])
    el = page.locator(".slide").nth(i)
    # JPEG is ten times faster to capture than PNG and the thresholds below absorb its noise
    shown = await el.screenshot(type="jpeg", quality=92)
    style = await page.add_style_tag(content=HIDE_TEXT)
    hidden = await el.screenshot(type="jpeg", quality=92)
    await style.evaluate("s => s.remove()")
    px = await lab.evaluate(ANALYZE, [base64.b64encode(shown).decode(), base64.b64encode(hidden).decode(), info["lines"]])
    for line, m in zip(info["lines"], px):
        line.update(m)
    if keep_clear:
        box = await el.bounding_box()
        # one row of grace on each side, for anti-aliasing
        strips = [(0, min(keep_clear[0] - 1, box["height"])), (keep_clear[1] + 1, box["height"])]
        # a slide of the wrong height (the size gate reports it) may end before a zone starts
        strips = [(y, y2) for y, y2 in strips if y2 > y]
        clips = [{"x": box["x"], "y": box["y"] + y, "width": box["width"], "height": y2 - y} for y, y2 in strips]
        await page.evaluate(
            """i => { for (const e of document.querySelectorAll('.slide')[i].querySelectorAll('*')) {
                 if (getComputedStyle(e).backgroundClip.includes('text')) e.setAttribute('data-gate-clip', '');
                 if (e instanceof SVGTextContentElement) e.setAttribute('data-gate-svg', ''); } }""", i)
        style = await page.add_style_tag(content=HIDE_DECOR)
        shown = [await page.screenshot(type="png", clip=c) for c in clips]
        await style.evaluate("s => s.remove()")
        style = await page.add_style_tag(content=HIDE_ALL)
        hidden = [await page.screenshot(type="png", clip=c) for c in clips]
        await style.evaluate("s => s.remove()")
        await page.evaluate("""() => { for (const e of document.querySelectorAll('[data-gate-clip],[data-gate-svg]')) {
                                  e.removeAttribute('data-gate-clip'); e.removeAttribute('data-gate-svg'); } }""")
        info["unsafe"] = []
        for (y, _), a, b in zip(strips, shown, hidden):
            info["unsafe"] += await lab.evaluate(
                ZONE, [base64.b64encode(a).decode(), base64.b64encode(b).decode(), y, info["boxes"]])
    return info


def is_large(line):
    """WCAG large text (24px, or 18.66px bold) scaled from a 390px phone to a 1080px slide."""
    return line["size"] >= 66 or (line["size"] >= 52 and line["weight"] >= 700)


def judge(info, min_contrast=4.5, max_words=80):
    """Turn the measurements of one slide into gate failures. Empty lists mean pass."""
    bad = {"contrast": [], "hidden": [], "overlap": [], "density": [], "safe": []}
    bad["safe"] = [f"'{t}'" for t in dict.fromkeys(info.get("unsafe", []))]
    for line in info["lines"]:
        need = min(min_contrast, 3.0) if is_large(line) else min_contrast
        if min_contrast and round(line["contrast"], 2) < need:
            bad["contrast"].append(f"'{line['text']}' {line['contrast']:.2f}:1 (needs {need}:1)")
        if line["gap"] >= max(2 * line["size"], 40):
            bad["hidden"].append(f"'{line['text']}'")
    for a, b in info["overlap"]:
        bad["overlap"].append(f"'{a}' on '{b}'")
    if max_words and info["words"] > max_words:
        bad["density"].append(f"{info['words']} words (limit {max_words})")
    return bad
