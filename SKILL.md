---
name: "carouso"
description: "Use when you need a carousel post for Instagram, TikTok, or Facebook. Carouso locks a design system with you first (brand tokens plus a pattern library), then composes each topic brief into rendered JPG slides with placed images."
---

# Carouso

## Purpose
Produce carousel posts in two phases. Phase 1 locks a design system with the user: brand tokens plus a library of layout patterns. Phase 2 composes each carousel from those patterns: pick patterns per slide, write copy, place images, render through quality gates.

Lock the tokens. Free the composition. That is what keeps every carousel on-brand without looking templated.

## First-run onboarding
When this skill triggers and no locked design system exists yet for the user's brand or project, do not start designing. Open the onboarding dialog first. Ask one question at a time, in this order, each with the listed choices. Accept a custom answer at any point. Seven questions, then design. If the user sends a screenshot or HTML reference instead of answering, skip the dialog and go to Phase 1, option B.

1. **Style.** "What vibe should the carousel have?" Choices: Playful and friendly / Clean and minimal / Bold and striking / Warm and elegant / Dark and premium.
2. **Colors.** "Pick a color mood." Choices: Warm earth (browns, cream, orange) / Fresh natural (greens, cream) / Ocean calm (blues, white) / Bold contrast (black, white, one strong accent) / Soft pastel.
3. **Fonts.** "Pick a type feel. No need to name fonts." Choices: Rounded and playful / Elegant serif / Bold and modern / Clean and simple. Map internally, never show font names: rounded-playful to Baloo 2 + Quicksand; elegant-serif to Playfair Display + Plus Jakarta Sans; bold-modern to Albert Sans + Plus Jakarta Sans; clean-simple to Plus Jakarta Sans + Quicksand.
4. **Brand.** "Brand name and handle for the watermark?" Free text, one message. Example: "Morning Cup / @morningcup".
5. **Topic.** "What are the carousels usually about?" Free text, one line. This sets the copy tone and the sample content.
6. **Language.** "Indonesian or English?" Two choices. This sets every fixed string: kickers, CTA, footer.
7. **System name.** "What should we call this design system?" Free text, one message. Suggest a default from the brand and style, for example "morningcup-playful". The name matters because the user may keep several systems and pick one per carousel.

After the seventh answer, summarize the locked choices in one short message, then move to Phase 1.

## Phase 1: lock the design system

Two ways in. Pick one.

**A. Generate from the onboarding answers.** Set the `:root` tokens in `design-system/system.css` to the brand (colors, fonts, radius). Render three sample patterns in those tokens (one cover, one body, one closer) and show them to the user. Iterate until approved.

**B. Adapt from a reference.** The user sends a screenshot or an HTML file of a carousel they like. Study it: color roles, type scale, spacing rhythm, recurring elements. Encode what you learn as `:root` tokens, then render the sample patterns. Iterate until approved.

**Approval gate.** The system enters production only after the user approves the rendered samples. Save it under its system name (for example `design-systems/morningcup-playful/`, containing `system.css`, `patterns.html`, and `last-used.json`). To build another system later, run the onboarding dialog again from question 1.

## Phase 2: compose a carousel

### 1. Collect the brief
Get this clear before starting. Ask about anything missing. Do not guess.
- Topic and angle, as one hook sentence.
- Design system: which locked system to use. Default to the most recently approved one. Ask when several exist.
- Slide count (default 6-10) and size (default 1080x1350, alternative 1080x1440).
- Images. For each image: the source (uploaded file path, direct URL, or article URL), the target slide, and the role (hero, split, or inline). Without an explicit placement map, use no images.

### 2. Plan the composition
Read the system's `last-used.json` and the pattern catalog in `design-system/PATTERNS.md`. Assign one pattern per slide:
- Open with one cover pattern, close with one closer pattern.
- No two adjacent slides share a pattern.
- Never repeat the cover pattern of the previous carousel for the same brand.
- Match pattern to content: numbers to stat-band or big-number, sequences to process-steps, a single line to quote. Do not force content into a fighting pattern.
- Alternate the two modes across slides: assign `mode-dark` to a slide or leave it light so no two adjacent slides share a mode. Start with the opposite mode of the previous carousel's first slide (read `last-used.json`). One carousel might open light, the next opens dark. Let the content guide which slides go dark: contrast pairs (myth vs fact, problem vs solution) are natural dark slides.
Write the plan as a simple list (slide number, pattern name, mode, one-line content) before building anything.

### 3. Write the copy
One idea per slide. Headlines stay under 8 words. Body stays under 25 words per slide. Follow the copy standards below.

### 4. Ingest and verify images (hard gate)
1. Download or copy every image into the local `images/` folder. Never hotlink during render.
2. Look at each image before use. Reject it when the content does not match the slide topic, when it carries a watermark or foreign logo, when it is blurry, or when its shortest side is under 900px for large use.
3. Log provenance (source URL or upload filename) in `provenance.log`.
4. Never use generative AI imagery. This skill generates no images, without exception.

### 5. Build the HTML
Start from the locked `system.css` (copy the `<style>` content or link the file) and copy the chosen `<section>` blocks from `patterns.html`. Fill copy and image slots. Reference images by local paths relative to the HTML. Do not invent new layouts per carousel. When the brief needs a structure no pattern covers, that is a Phase 1 discussion, not a Phase 2 improvisation.

### 6. Render with the quality gate
Run `scripts/render_carousel.py`:
```
python3 scripts/render_carousel.py --html <file.html> --out <dir-output> \
    --width 1080 --height 1440 --slides 6 \
    --check-fonts "Plus Jakarta Sans"
```
(Adjust width, height, slides, and fonts to the brief and the system tokens.)
The script exits 1 when the `.slide` count differs from the request, when content overflows its zone, when a slide bounding box differs from the requested size, or when a checked font failed to load. Fix the HTML and re-render until it passes. Never waive the gate manually.

### 7. Final visual check and record
Open slide 1, one middle slide, and the last slide. Confirm the display font rendered, no text is clipped, no elements overlap, images are undistorted with subjects intact, and brand, handle, and CTA stay consistent. Then update the system's `last-used.json` with this carousel's cover pattern, full pattern sequence, and the mode of each slide (for example `{"cover": "cover-big-type", "sequence": ["cover-big-type", "two-cards", "takeaway"], "modes": ["light", "dark", "light"]}`).

## Design thinking
Apply this reasoning at every step. It is what keeps the output from reading as AI slop.

### Before writing copy
- Name the single idea of the slide in one sentence. If you cannot, the slide does not exist yet.
- Write the headline first, then cut it under 8 words without losing meaning.
- Prefer concrete nouns and strong verbs over adjectives. Name the time, the temperature, the amount.
- Read each line back. If it could belong to any brand, rewrite it for this one.

### Before placing elements
- Decide the reading order first: what is seen first, second, third. Size and weight must enforce it.
- Every element needs a reason for its position. Align to the grid, or break it deliberately (covers only).
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
- Alignment: one consistent inner margin everywhere. Left-aligned by default; covers center deliberately.
- Typography: two font families maximum. Every font must load; the render gate rejects silent fallback.
- Color: 60 percent base, 30 percent secondary, 10 percent accent.
- Consistency: topbar, footer, kicker, cards, radius, and shadows never change style across slides. Patterns vary. Tokens do not.
- Safe zones: 64px from each edge. Nothing important outside them.
- Anti-collision: fixed zones with vertical flex flow. Elements that touch are a failed design.

## Output contract
- Locked design systems under `design-systems/<name>/`: `system.css`, `patterns.html`, `last-used.json`.
- Per carousel: `slide_01.jpg` through `slide_NN.jpg` (exactly N files at the requested size), the source HTML, `images/` with local copies, and `provenance.log`.

## Operating rules
1. No design system, no production. Phase 1 approval comes before any carousel.
2. Compose from the pattern library. Do not invent per-carousel layouts.
3. Variety rules are hard rules: no adjacent duplicate patterns, no repeated cover in a row, alternate light/dark modes with no two adjacent slides sharing a mode, invert the starting mode each carousel, always update `last-used.json`.
4. Images come from user uploads or URLs/articles only. No generative AI imagery, no exceptions.
5. Use an image only after visual verification. Replace a failed slot with a graphic element.
6. A failed render gate means fix the HTML, not bypass the gate.
7. Ask about a missing brief detail instead of guessing it.
