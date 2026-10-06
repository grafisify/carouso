---
name: "carouso"
description: "Use when you need a carousel post for Instagram, TikTok, or Facebook. Carouso locks one reusable template with you first, then turns each topic brief into rendered JPG slides with placed images."
---

# Carouso

## Purpose
Produce carousel posts in two phases. Phase 1 designs and locks one template with the user. Phase 2 reuses that template for every carousel: write copy, place images, render through quality gates.

## Phase 1: lock the template (once per brand)

Two ways in. Pick one.

**A. Generate from a brand brief.** Collect: brand name, handle, two main colors plus one accent, one display font plus one body font, audience, and 2-3 adjectives for the feel (playful, premium, warm). Draft the template as HTML: a cover, one content slide, one closer. Render those three slides and show them to the user. Iterate until approved.

**B. Adapt from a reference.** The user sends a screenshot or an HTML file of a carousel they like. Study it: layout zones, type scale, spacing rhythm, color roles, recurring elements. Rebuild it as a clean template with CSS variables for every brand token (colors, fonts, radius), so future carousels can reskin it without touching the layout.

**Approval gate.** The template enters production only after the user approves the rendered samples. Save the approved file as the project's canonical template (for example `template.html`). Every future carousel starts as a copy of this file. When the brand evolves, repeat Phase 1 and re-lock.

## Phase 2: produce a carousel

### 1. Collect the brief
Get this clear before starting. Ask about anything missing. Do not guess.
- Topic and angle, as one hook sentence.
- Slide count (default 10) and size (default 1080x1350, alternative 1080x1440).
- Images. For each image: the source (uploaded file path, direct URL, or article URL), the target slide, and the role (hero, full-bleed, or card illustration). Without an explicit placement map, use no images.

### 2. Write the copy
One idea per slide. Headlines stay under 8 words. Body stays under 25 words per slide. Follow the copy standards below.

### 3. Ingest and verify images (hard gate)
1. Download or copy every image into the local `images/` folder. Never hotlink during render.
2. Look at each image before use. Reject it when the content does not match the slide topic, when it carries a watermark or foreign logo, when it is blurry, or when its shortest side is under 900px for large use.
3. Log provenance (source URL or upload filename) in `provenance.log`.
4. Never use generative AI imagery. This skill generates no images, without exception.

### 4. Fill the template
Copy the locked template to a working file. Fill the content and image slots. Reference images by local paths relative to the HTML. Do not redesign the layout per carousel. When the brief needs a layout the template cannot support, that is a Phase 1 discussion, not a Phase 2 improvisation.

### 5. Render with the quality gate
Run `scripts/render_carousel.py`:
```
python3 scripts/render_carousel.py --html <file.html> --out <dir-output> \
    --width 1080 --height 1350 --slides 10 \
    --check-fonts "Baloo 2,Quicksand"
```
The script exits 1 when the `.slide` count differs from the request, when content overflows its zone, when a slide bounding box differs from the requested size, or when a checked font failed to load. Fix the HTML and re-render until it passes. Never waive the gate manually.

### 6. Final visual check
Open slide 1, one middle slide, and the last slide. Confirm the display font rendered, no text is clipped, no elements overlap, images are undistorted with subjects intact, and brand, handle, and CTA stay consistent.

## Design thinking
Apply this reasoning at every step. It is what keeps the output from reading as AI slop.

### Before writing copy
- Name the single idea of the slide in one sentence. If you cannot, the slide does not exist yet.
- Write the headline first, then cut it under 8 words without losing meaning.
- Prefer concrete nouns and strong verbs over adjectives. Name the time, the temperature, the amount.
- Read each line back. If it could belong to any brand, rewrite it for this one.

### Before placing elements
- Decide the reading order first: what is seen first, second, third. Size and weight must enforce it.
- Every element needs a reason for its position. Align to the grid, or break it deliberately (cover only).
- Treat whitespace as a design element. When a slide feels cramped, cut content. Never shrink type below the minimum.

### Copy standards (anti-slop)
- Short declarative sentences. One idea per sentence.
- No em dashes. No "not just X, but Y" constructions. No forced triads.
- No filler openers and no AI vocabulary: "delve", "unlock", "elevate", "tapestry", "game-changer", "in today's fast-paced world".
- Active voice. Plain words: "use", not "utilize".
- Hooks use one of three patterns: a curiosity gap, a specific number, or direct address.
- The subhead makes a promise, not a summary. It says what the reader gets from swiping.
- No decorative emojis in headings. No title case headlines.

### Layout fundamentals
- Hierarchy: the headline is the largest, boldest element. One accent-colored word or phrase per headline, nothing more.
- Contrast: text over photos sits on a scrim or semi-solid card. Never on a busy photo directly.
- Alignment: one consistent inner margin everywhere. Left-aligned by default; the cover centers deliberately.
- Typography: two font families maximum. Every font must load; the render gate rejects silent fallback.
- Color: 60 percent base, 30 percent secondary, 10 percent accent.
- Consistency: topbar, footer, eyebrow pill, cards, radius, and shadows never change style across slides.
- Safe zones: 64px from each edge. Nothing important outside them.
- Anti-collision: fixed zones (topbar, content, footer) with vertical flex flow. Elements that touch are a failed design.

## Output contract
- The locked `template.html` (approved, versioned with the project).
- Per carousel: `slide_01.jpg` through `slide_NN.jpg` (exactly N files at the requested size), the source HTML, `images/` with local copies, and `provenance.log`.

## Operating rules
1. No template, no production. Phase 1 approval comes before any carousel.
2. Images come from user uploads or URLs/articles only. No generative AI imagery, no exceptions.
3. Use an image only after visual verification. Replace a failed slot with a graphic element.
4. A failed render gate means fix the HTML, not bypass the gate.
5. Do not redesign per carousel. Template changes go through Phase 1.
6. Ask about a missing brief detail instead of guessing it.
