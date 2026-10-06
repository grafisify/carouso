---
name: "carouso"
description: "Use when you need a carousel post for Instagram, TikTok, or Facebook. Carouso turns a topic brief into a designed, rendered set of JPG slides, with images placed from user uploads or URLs."
---

# Carouso

## Purpose
Turn a topic brief into a ready-to-post carousel. Write the copy per slide. Lay it out with graphic design fundamentals. Place images from user uploads or URLs. Render to JPG through a quality gate that rejects defective output.

## Workflow

### 1. Collect the brief
Get this clear before starting. Ask about anything missing. Do not guess.
- Topic and angle, as one hook sentence.
- Slide count (default 10) and size (default 1080x1350, alternative 1080x1440).
- Brand style: brand name, handle, two main colors plus one accent color, one display font plus one body font. When the brief omits these, use the defaults in `assets/base-template.html`.
- Images. For each image: the source (uploaded file path, direct URL, or article URL), the target slide, and the role (hero, full-bleed, or card illustration). Without an explicit placement map, use no images.

### 2. Write the copy per slide
Follow the copy rules in [references/layout-rules.md](references/layout-rules.md). The fixed structure:
- Slide 1 (cover): a 3-7 word hook, one explanatory subhead of max two lines, no details. The cover must stand out from every other slide.
- Slides 2 to N-1: one idea per slide. A descriptive headline, 1-2 explanatory sentences, one support card (short fact, step, or quote).
- Slide N (closer): a 3-4 point recap plus a CTA (Save, Share, Follow).
- Text budget: headlines stay under 8 words, body under 25 words per slide. Aim for roughly 80 percent visual and minimal text.

### 3. Ingest and verify images (hard gate)
Follow [references/image-workflow.md](references/image-workflow.md) exactly.
1. Download or copy every image into the local working folder. Never hotlink during render.
2. Look at each image before use. Reject it when the content does not match the slide topic, when it carries a watermark or foreign logo, when it is blurry, or when its shortest side is under 900px for large use.
3. Log provenance (source URL or upload filename) in `provenance.log`.
4. Never use generative AI imagery. This skill generates no images, without exception.

### 4. Build the HTML from the template
- Copy `assets/base-template.html` to a working file. Do not hand-write a layout unless the brief asks for a style the template cannot support.
- Fill the content slots and image slots (`<!-- IMG: ... -->`). Reference images by local file paths relative to the HTML.
- Apply the fundamentals in [references/design-fundamentals.md](references/design-fundamentals.md): dominant headline, contrast, consistent alignment, whitespace, safe zones.
- Fonts: Google Fonts is allowed (uncomment the link block in the template, always use `display=swap`), or use locally installed fonts (check with `fc-list`). Render with `--check-fonts "Baloo 2,Quicksand"` so a webfont that fails to load fails the render instead of silently falling back. Where `fonts.googleapis.com` is unreachable, install the TTFs locally. The family names stay the same.

### 5. Render with the quality gate
Run `scripts/render_carousel.py`:
```
python3 scripts/render_carousel.py --html <file.html> --out <dir-output> \
    --width 1080 --height 1350 --slides 10 \
    --check-fonts "Baloo 2,Quicksand"
```
The script exits 1 when the `.slide` count differs from the request, when content overflows its zone, when a slide bounding box differs from the requested size, or when a checked font failed to load. Fix the HTML and re-render until it passes. Never waive the gate manually.

### 6. Final visual check
Open three files: slide 1, one middle slide, the last slide. Check that the display font rendered (not a fallback), that no text is clipped and no elements overlap, that images are undistorted with their subject intact, and that brand, handle, and CTA stay consistent.

## Output contract
- `<dir-output>/slide_01.jpg` through `slide_NN.jpg`: exactly N files at the requested size.
- The source HTML used for the render, stored next to the output.
- `images/` with every image used (local copies), plus `provenance.log` mapping each image to its source URL or upload filename.

## Operating rules
1. Images come from user uploads or URLs/articles only. No generative AI imagery, no exceptions.
2. Use an image only after visual verification. Replace an unverified image slot with a graphic element (icon or card).
3. A failed render gate means fix the HTML, not bypass the gate.
4. Minimal text. One idea per slide. The cover always stands out.
5. Keep every slide consistent: same topbar, footer, palette, and font pairing throughout.
6. Ask about a missing brief detail instead of guessing it.
