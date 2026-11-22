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
  }
  judge(info, min_contrast, max_words) -> {"contrast": [...], "hidden": [...],
                                           "overlap": [...], "density": [...]}
"""
import base64

HIDE_TEXT = (
    "*,*::before,*::after{-webkit-text-fill-color:transparent!important;"
    "text-shadow:none!important;-webkit-text-stroke-color:transparent!important;"
    "text-decoration-color:transparent!important}"
)
# Text that is decoration on purpose opts out of the legibility gates.
EXEMPT = '.peek,[data-bleed],[data-decor],[aria-hidden="true"]'

COLLECT = """
([i, exempt]) => {
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
  const blocks = [], lines = [];
  const pen = document.createElement('canvas').getContext('2d');
  let words = 0;
  const w = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) {
    const n = w.currentNode, el = n.parentElement, text = n.textContent.trim();
    if (!text) continue;
    const cs = getComputedStyle(el);
    // Only text that is painted counts: a display:none ancestor leaves no box,
    // and transparent or zero-opacity text leaves no ink.
    if (cs.visibility === 'hidden' || !el.checkVisibility()) continue;
    let opacity = 1, block = el;
    for (let a = el; a && a !== s.parentElement; a = a.parentElement) opacity *= parseFloat(getComputedStyle(a).opacity);
    const fill = rgba(cs.webkitTextFillColor || cs.color);
    if (fill[3] * opacity < 0.05) continue;   // clipped-gradient or invisible text
    words += text.split(/\\s+/).filter(t => /[\\p{L}\\p{N}]/u.test(t)).length;
    // decoration opts out, and so do marks with no letter or digit (quote marks, arrows)
    if (el.closest(exempt) || !/[\\p{L}\\p{N}]/u.test(text)) continue;
    while (block !== s && getComputedStyle(block).display.startsWith('inline')) block = block.parentElement;
    let blockId = blocks.indexOf(block);
    if (blockId < 0) blockId = blocks.push(block) - 1;
    // Where the glyphs really are inside the line box: a 300px numeral has a
    // tall box but its ink stops well short of the label under it.
    pen.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    const shown = cs.textTransform === 'uppercase' ? text.toUpperCase() : text;
    const m = pen.measureText(shown);
    const box = m.fontBoundingBoxAscent + m.fontBoundingBoxDescent;
    const r = document.createRange();
    r.selectNodeContents(n);
    for (const q of r.getClientRects()) {
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
  return {words, lines, overlap};
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


async def measure(page, lab, i):
    """Measure slide i. The slide must already be the only one displayed."""
    info = await page.evaluate(COLLECT, [i, EXEMPT])
    el = page.locator(".slide").nth(i)
    # JPEG is ten times faster to capture than PNG and the thresholds below absorb its noise
    shown = await el.screenshot(type="jpeg", quality=92)
    style = await page.add_style_tag(content=HIDE_TEXT)
    hidden = await el.screenshot(type="jpeg", quality=92)
    await style.evaluate("s => s.remove()")
    px = await lab.evaluate(ANALYZE, [base64.b64encode(shown).decode(), base64.b64encode(hidden).decode(), info["lines"]])
    for line, m in zip(info["lines"], px):
        line.update(m)
    return info


def is_large(line):
    """WCAG large text (24px, or 18.66px bold) scaled from a 390px phone to a 1080px slide."""
    return line["size"] >= 66 or (line["size"] >= 52 and line["weight"] >= 700)


def judge(info, min_contrast=4.5, max_words=80):
    """Turn the measurements of one slide into gate failures. Empty lists mean pass."""
    bad = {"contrast": [], "hidden": [], "overlap": [], "density": []}
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
