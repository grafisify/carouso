---
name: "carouso"
description: "Use when you need a carousel post for Instagram, TikTok, or Facebook. Pick a ready-made numbered template (for example \"template 3, topic: ...\") and get rendered JPG slides right away, or build a custom design system first. Real images only, quality-gated render."
---

# Carouso

## Purpose
Produce carousel posts in two phases. Phase 1 locks a design system with the user: brand tokens plus a library of layout patterns. Phase 2 composes each carousel from those patterns: pick patterns per slide, write copy, place images, render through quality gates.

Lock the tokens. Free the composition. That is what keeps every carousel on-brand without looking templated.

## Using a template (default path)
Thirty-six ready-made templates ship in `templates/`. Each is a locked look (colors, fonts, light and dark tokens) plus a slide skeleton, so no onboarding is needed. The preview gallery is in `README.md`.

Triggers: "template 3", "template no 3", "pakai template 3", "use template 2 for ...", or a template name ("morning cup"). Match the number or name against `templates/NN-slug/template.json`.

Files per template: `tokens.css` (the skin), `template.json` (name, fonts, size, slide sequence with patterns, modes and a `headline` budget per slide), `sample.html` (the finished sample carousel to copy from).

1. **Resolve the template.** Read `templates/NN-slug/template.json`. If the person gave no number and no custom system exists, list every template (number, name, vibe) from the `template.json` files and ask which one. An unknown number gets the same list.
2. **Collect the brief.** Ask once, in one message, for whatever is missing: topic and angle (required), brand name and handle (the template placeholders are used when they decline), slide count (default is the sequence length, allowed 5 to 10), images with a placement map (optional, see step 6). The carousel language follows the language of the brief. Translate every fixed string in the markup too: "Myth", "Fact", "Save this", and the `NN / TT` footer stay, the words change. Set `<html lang>` to the carousel language. For Indonesian, use the fixed-string table under "Indonesian copy".
3. **Plan from the sequence.** Start from the template `sequence`. Keep the cover first, the takeaway last, and the mode of each slide as listed. For a different slide count, drop or repeat middle slides in sequence order, keeping modes alternating and no two adjacent slides on the same pattern. Swap a middle pattern when the content fits another one better (numbers to `stat-band` or `big-number`, steps to `process-steps`, one line to `quote`), keeping that slide's mode. Use `cover-split` only when a verified cover image is supplied. A placed image goes on the slide as a `.photo` slot (see below), or on an `image-hero` slide when the photo is the point. Write the plan as a list (slide number, pattern, mode, one-line content) before building.
4. **Write the copy** under the copy standards below. Replace every sample line. Nothing from the sample topic may remain. Write each headline to the slide's `headline` budget in `template.json`: `lines` is how many lines the layout was drawn for, `chars_per_line` is how many characters fit on one line and so the longest word that fits. A slide with `"lines": 2, "chars_per_line": 9` takes "Cari cahaya", never "Pencahayaan". Display templates are tight (21 Bauhaus and 23 Pixel Quest hold 8 to 11 characters a line), so choose the words to fit before building. Keep the sample's `<br>` rhythm and its one `.accent` span.
5. **Build the HTML.** Create `carousels/<slug>/index.html` by copying the chosen template's `sample.html`. Change only the `tokens.css` link to `../../templates/NN-slug/tokens.css`. The `fonts.css` and `system.css` links already resolve from that depth. Keep or remove `<section>` blocks per the plan, copy pattern blocks from `design-system/patterns.html` (or another template's `sample.html` for the newer patterns; the name-to-class table is in `design-system/PATTERNS.md`) for added slides, apply the `mode-dark` class per the plan, fill in brand, handle, and the `NN / TT` counters.
6. **Images** pass the hard gate in Phase 2 step 4 below. Put local copies in `carousels/<slug>/images/` and log provenance in `carousels/<slug>/provenance.log`.
7. **Render** with the template's size and fonts from `template.json`:
```
python3 scripts/render_carousel.py --html carousels/<slug>/index.html --out carousels/<slug>/ \
    --width 1080 --height 1440 --slides <N> --check-fonts "<fonts from template.json, comma separated>"
```
Fix the HTML until every gate passes. Never waive a gate.
8. **Final visual check** as in Phase 2 step 7, then deliver `slide_01.jpg` to `slide_NN.jpg`. Templates need no `last-used.json`, because modes come from the template.

Fonts are bundled in `fonts/`, so nothing needs installing besides Playwright. Templates 12 to 14 are news styles built on one `cover-news` cover: they need a cover photo (swap the `src` inside `figure.news-photo`; set `--focus` on it for the crop) and carry one photo on a body slide (`img` in `images/`). Templates 07 to 11 draw their hero art (`.object` elements and decor) from `templates/NN-slug/decor/` through `tokens.css`, so keep the slide markup as in `sample.html`. To use the person's own transparent PNG or photo as the hero, put `<img src="images/x.png" alt="">` inside the `.object` element; the image replaces the default art. Templates 15 to 24 are themed skins (risograph, blueprint, bento tiles, chat thread, receipt, comic, Bauhaus, retro desktop, pixel game, notebook): their `tokens.css` restyles the standard patterns heavily and some covers carry extra decor elements, so copy the slide markup from `sample.html` exactly and change only the copy. Their display fonts are wide or decorative, so keep headlines about as short as the sample ones. Templates 25 to 36 are app-screen skins (code editor, browser window, search results, lock screen, notes app, kanban board, calendar, music player, app store, settings screen, spreadsheet, glass widgets). The same rule applies: copy the markup from `sample.html` exactly. Read the comment at the top of each `sample.html` first, because some decor is driven from the markup and must match the new copy: `data-state="on"` or `"off"` on template 34 toggles, `style="--v:NN%"` on sliders, bars and progress rings (34, 35, 36), and on template 32 the footer scrubber (`--p` is the slide number, `--t` the slide total, mirrored in the two time labels). Every visible word in these templates, including button and label text, is in the markup, so translate all of it. Template 07 has optional skins: add `skin-sand` or `skin-slate` to `<body>` when the person asks for a warm sand or a cool slate palette (listed under `skins` in its `template.json`). The newer patterns (`cover-poster`, `cover-hook`, `cover-label`, `cover-object`, `pointer`, `showcase`, `note`) are described in `design-system/PATTERNS.md`; swap them only for patterns of the same kind (cover for cover, body for body).

A person who wants their own look instead of the bundled templates uses the custom path below.

## Custom design system (optional path)
Use this path only when the person asks for their own look, or sends a reference screenshot or HTML, instead of picking a template. When no template was chosen and no locked design system exists yet, offer the templates first, and run the onboarding below only if they want a custom one. When this path runs, do not start designing. Open the onboarding dialog first. Ask one question at a time, in this order, each with the listed choices. Accept a custom answer at any point. Seven questions, then design. If the user sends a screenshot or HTML reference instead of answering, skip the dialog and go to Phase 1, option B.

1. **Style.** "What vibe should the carousel have?" Choices: Playful and friendly / Clean and minimal / Bold and striking / Warm and elegant / Dark and premium.
2. **Colors.** "Pick a color mood." Choices: Warm earth (browns, cream, orange) / Fresh natural (greens, cream) / Ocean calm (blues, white) / Bold contrast (black, white, one strong accent) / Soft pastel.
3. **Fonts.** "Pick a type feel. No need to name fonts." Choices: Rounded and playful / Elegant serif / Bold and modern / Clean and simple. Map internally, never show font names: rounded-playful to Baloo 2 + Quicksand; elegant-serif to Playfair Display + Plus Jakarta Sans; bold-modern to Albert Sans + Plus Jakarta Sans; clean-simple to Plus Jakarta Sans + Quicksand. All five families are bundled in `fonts/`: link `fonts/fonts.css` from the carousel HTML.
4. **Brand.** "Brand name and handle for the watermark?" Free text, one message. Example: "Morning Cup / @morningcup".
5. **Topic.** "What are the carousels usually about?" Free text, one line. This sets the copy tone and the sample content.
6. **Language.** "Indonesian or English?" Two choices. This sets every fixed string: kickers, CTA, footer.
7. **System name.** "What should we call this design system?" Free text, one message. Suggest a default from the brand and style, for example "morningcup-playful". The name matters because the user may keep several systems and pick one per carousel.

After the seventh answer, summarize the locked choices in one short message, then move to Phase 1.

## Phase 1: lock the design system

Two ways in. Pick one.

Never edit the shared `design-system/system.css`: every template builds on it. Start each custom system by copying `design-system/system.css` and `design-system/patterns.html` into `design-systems/<name>/`, and edit only that copy. In the copied `patterns.html`, change the fonts link to `../../fonts/fonts.css` (the copy sits one level deeper).

**A. Generate from the onboarding answers.** Set the `:root` tokens (and the `.slide.mode-dark` block) in `design-systems/<name>/system.css` to the brand (colors, fonts, radius). Render three sample patterns in those tokens (one cover, one body, one closer) and show them to the user. Iterate until approved.

**B. Adapt from a reference.** The user sends a screenshot or an HTML file of a carousel they like. Study it: color roles, type scale, spacing rhythm, recurring elements. Encode what you learn as `:root` tokens in `design-systems/<name>/system.css`, then render the sample patterns. Iterate until approved.

**Approval gate.** The system enters production only after the user approves the rendered samples. It lives under its system name (for example `design-systems/morningcup-playful/`, containing `system.css`, `patterns.html`, and `last-used.json`). To build another system later, run the onboarding dialog again from question 1.

## Phase 2: compose a carousel

### 1. Collect the brief
Get this clear before starting. Ask about anything missing. Do not guess.
- Topic and angle, as one hook sentence.
- Design system: which locked system to use. Default to the most recently approved one. Ask when several exist. (On the template path, the template is the design system.)
- Slide count (default 6-10) and size (default 1080x1440, which is what `system.css` renders; a different height needs a matching `.slide` height override).
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

**Photo slot.** To add a picture to any body pattern, put `<figure class="photo"><img src="images/<file>.jpg" alt="..."></figure>` as the last child of that slide's `.content`. It sizes to the content width at 16:10 and takes the template's radius and colors. Use `class="photo wide"` (5:2) or `class="photo band"` (3:1) on dense slides such as `myth-fact` or `big-number`, `style="--focus:50% 40%"` to set the crop point, and a `<figcaption>` for a caption on a scrim. For two photos use `<div class="photos">` holding two `<figure class="photo">` (square, side by side, same gutter as `two-cards`), or `class="photos short"` (4:3) on dense slides. For a hero-style slide put the photo edge to edge on top: add `photo-top` to the `<section>` classes, `style="--bleed-h:600px"` on it, and `<figure class="photo-bleed"><img ...></figure>` as the first child. The topbar turns white on a scrim and the content starts below the photo. Use about `--bleed-h:440px` on dense slides (`myth-fact`, `big-number`). Pick a photo with a calm top edge, since the topbar sits on it. Check that the slide still passes the overflow gate and keeps at least 40px of air above and below the content.

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
The script exits 1 when the `.slide` count differs from the request, when content overflows its zone, when a slide bounding box differs from the requested size, when text is smaller than 20px, when a checked font failed to load, when an `<img>` failed to load, when text is cut off by the slide edge (elements inside `.peek` or `[data-bleed]` may bleed on purpose), or when a word is wider than the line it sits on. For that last one, pick a shorter word; do not shrink the type. Fix the HTML and re-render until it passes. Never waive the gate manually.

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

### Indonesian copy
When the brief is in Indonesian, every rule above still applies. These rules replace the English examples.

- **Write in Indonesian from the first draft.** Never translate an English draft line by line. "Level up your savings" becomes "Dana darurat pertama", not "Tingkatkan level tabunganmu".
- **Mind word length.** Affixes make Indonesian words long: "menyelesaikan" is 13 characters, "pengeluaran" is 11. Check the longest word of each headline against `chars_per_line`. Reach for the root or the everyday word first: "selesai" for "menyelesaikan", "biaya" for "pengeluaran", "pakai" for "menggunakan", "cek" for "memeriksa". Never hyphenate a word, abbreviate it, or shrink the type to make it fit.
- **One form of address, fixed at the brief.** "kamu" for casual consumer content (the default), "Anda" (always capitalized) for formal or B2B, "kita" for community voices. Never mix them in one carousel. Use "lo/gue" only when the brand already does.
- **Start with the verb.** Imperatives read fastest: "Cari cahaya jendela." "Sisihkan Rp50 ribu tiap Senin." The "di-" passive is natural in news headlines ("Mercusuar tua dibuka lagi") and weak everywhere else.
- **Be specific.** A rupiah amount, a day, a count, a place. "Sisihkan Rp50 ribu tiap Senin" beats "Mulailah menabung secara konsisten".
- **Banned openers and filler:** "Di era digital ini", "Tahukah kamu", "Pernahkah kamu merasa", "Yuk, simak", "Simak sampai habis", "Tanpa disadari", "Jangan sampai ketinggalan", "Nah,", "Jadi, tunggu apa lagi".
- **Banned constructions:** "bukan sekadar X, tapi Y", "bukan hanya X, melainkan Y", "tidak hanya X, tetapi juga Y", and their reversed forms.
- **Banned inflation:** "solusi terbaik", "wajib tahu", "rahasia sukses", "kunci utama", "game changer", "next level", and poster aphorisms such as "Sukses dimulai dari langkah kecil".
- **No English sprinkled in for style** ("which is", "literally", "somehow", "relate"). Keep English only for terms the audience already uses as the normal word: email, deadline, invoice, brief, feed.
- **Spelling and numbers follow EYD.** Preposition "di" stands apart ("di rumah"), prefix "di-" attaches ("dibuka"). Rupiah has no space: "Rp50.000". Thousands take a period, decimals a comma: "1.250", "2,5 juta". In tight slots write "Rp50 ribu", "Rp2,5 juta", "40 rb". Time is "09.41" or "pukul 9". Dates are day first: "8 Nov 2026". Sentence case, never Title Case Di Tiap Kata.

Fixed strings (translate these in every template, including `data-btn`, `alt` and `aria-label` values):

| Sample | Indonesian |
|---|---|
| Myth / Fact | Mitos / Fakta |
| Save this | Simpan dulu |
| Swipe | Geser |
| Read this | Baca ini |
| Takeaway, Recap | Ringkasan, Intinya |
| Step 1, Rule one | Langkah 1, Aturan satu |
| Before / After | Sebelum / Sesudah |
| Do / Don't | Lakukan / Hindari |
| Latest, Just in | Terbaru, Baru saja |
| 5 min read | 5 menit baca |
| Follow for more | Ikuti untuk kabar berikutnya |
| OK / Cancel / Open | Oke / Batal / Buka |

A rewrite, for calibration:

| Slop | Fixed |
|---|---|
| Di era digital ini, mengatur keuangan bukan sekadar pilihan, tapi kebutuhan. | Gajian tanggal 25. Tanggal 5 sudah habis? |
| Yuk, simak 5 tips jitu yang wajib kamu tahu! | Lima pos uang yang bocor tiap bulan. |
| Mulailah menabung secara konsisten demi masa depan. | Sisihkan Rp50 ribu tiap Senin. |

### Layout fundamentals
- Hierarchy: the headline is the largest, boldest element. One accent-colored word or phrase per headline, nothing more.
- Contrast: text over photos sits on a scrim or semi-solid card. Never on a busy photo directly.
- Alignment: one consistent inner margin everywhere. Left-aligned by default; covers center deliberately.
- Typography: two font families maximum. Every font must load; the render gate rejects silent fallback.
- Type size: designed for a phone, where a 1080px slide shows at about a third of its size. Body copy 28 to 32px, secondary text (labels, captions, stat labels, footers, tags) 20px or more, never smaller. The render gate rejects any text under 20px (`--min-font`).
- Contrast: body, muted, footer, and accent text hold at least 4.5:1 against their background and panel (WCAG AA). Templates already comply, so a custom system must check its own tokens in both modes.
- Color: 60 percent base, 30 percent secondary, 10 percent accent.
- Consistency: topbar, footer, kicker, cards, radius, and shadows never change style across slides. Patterns vary. Tokens do not.
- Safe zones: content stays inside the `.inner` box (78px top and bottom, 82px left and right). Only the topbar and footer chrome sit closer, at 34px from the edge. No text may be cut by the slide edge.
- Anti-collision: fixed zones with vertical flex flow. Elements that touch are a failed design.

## Output contract
- Templates under `templates/NN-slug/`: `tokens.css`, `template.json`, `sample.html`. Read-only for a normal run.
- Custom design systems under `design-systems/<name>/`: `system.css`, `patterns.html`, `last-used.json`.
- Per carousel (template path): `carousels/<slug>/` holding `slide_01.jpg` through `slide_NN.jpg` (exactly N files at the requested size), `index.html`, `images/` with local copies, and `provenance.log`. Custom systems keep the layout they were given.

## Operating rules
1. No template and no approved design system, no production. A named template counts as approved. A custom system needs Phase 1 approval first.
2. Compose from the pattern library. Do not invent per-carousel layouts, and never edit a template's `tokens.css` for a single carousel.
3. Variety rules are hard rules: no adjacent duplicate patterns, alternate light/dark modes with no two adjacent slides sharing a mode. On the custom path also: no repeated cover in a row, invert the starting mode each carousel, always update `last-used.json`. On the template path the template fixes the cover and the modes.
4. Images come from user uploads or URLs/articles only. No generative AI imagery, no exceptions.
5. Use an image only after visual verification. Replace a failed slot with a graphic element.
6. A failed render gate means fix the HTML, not bypass the gate.
7. Ask about a missing brief detail instead of guessing it.
