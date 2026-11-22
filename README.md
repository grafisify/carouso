<div align="center">

# Carouso

**An AI agent skill for scroll-stopping carousel posts.**

Turn a topic into a designed, ready-to-post carousel for Instagram, TikTok, or Facebook.
Pick a ready-made template or lock your own design system. Real images only. No AI slop.

</div>

---

## Why Carouso

| | |
|---|---|
| **Locked tokens, free layouts** | Brand tokens (colors, fonts, spacing) stay locked. Slides are composed per topic from a 20-pattern library, so every carousel is consistent without looking copy-pasted. |
| **Ready to use** | Thirty-six numbered templates. Say `template 3, topic: ...` and get finished JPGs. No setup, no onboarding, fonts included. |
| **Or your own look** | Want a custom brand instead? A 7-question dialog (or a reference screenshot) locks your own design system. |
| **Real images only** | Images come from user uploads or URLs and every one passes visual verification. Four photo layouts ship with the skill. Generative AI imagery is banned, no exceptions. |
| **Built for phones** | Body copy is 28 to 32px, nothing is under 20px, and text keeps WCAG AA contrast (4.5:1) in both modes. |
| **Quality gates** | The render fails on wrong slide count, overflowing content, wrong dimensions, text under 20px, a missing font, a broken image, text cut off by the slide edge, a word too wide for its line, text under 4.5:1 contrast, text covered by an image or by other text, more than 80 words on a slide, or text under the app interface of a 9:16 slide. Defects never ship silently. |
| **Three sizes** | The same carousel renders at 1080x1440 (3:4), 1080x1350 (4:5 feed) and 1080x1920 (9:16 Stories and TikTok). Slides reflow to each size; the 9:16 render keeps text out of the top and bottom 250px. |

## Pick a template

Every template is a finished 8-slide look: colors, fonts, light and dark slides, and a slide order that works. Pick a number, give a topic, get a carousel.

```
template 3, topic: 5 habits that waste your week
```

The agent asks once for anything missing (brand name and handle, optional images), writes the copy, and renders print-clean JPGs at 1080x1440. Ask for 4:5 or for Stories/TikTok to get 1080x1350 or 1080x1920 from the same carousel. The sample copy in the previews is placeholder.

### 01 · Morning Cup
Playful and friendly. Warm earth tones, rounded type. Good for food, lifestyle, small brands.

<img src="assets/templates/01-morning-cup.jpg" width="860" alt="Template 01 · Morning Cup: eight sample slides">

### 02 · Clean Minimal
Clean and minimal. Lots of white space, one cool blue accent. Good for tips, tools, productivity.

<img src="assets/templates/02-clean-minimal.jpg" width="860" alt="Template 02 · Clean Minimal: eight sample slides">

### 03 · Bold Contrast
Bold and striking. Black and off-white, one hot accent, heavy type. Good for hot takes and hooks.

<img src="assets/templates/03-bold-contrast.jpg" width="860" alt="Template 03 · Bold Contrast: eight sample slides">

### 04 · Warm Elegant
Warm and elegant. Cream and burgundy, serif headlines. Good for wellness, beauty, slow living.

<img src="assets/templates/04-warm-elegant.jpg" width="860" alt="Template 04 · Warm Elegant: eight sample slides">

### 05 · Dark Premium
Dark and premium. Near-black and antique gold, editorial quotes. Good for finance, business, expertise.

<img src="assets/templates/05-dark-premium.jpg" width="860" alt="Template 05 · Dark Premium: eight sample slides">

### 06 · Fresh Garden
Fresh and natural. Sage and leaf green, soft rounded type. Good for health, nature, how-tos.

<img src="assets/templates/06-fresh-garden.jpg" width="860" alt="Template 06 · Fresh Garden: eight sample slides">

### 07 · Paper Stack
Teal and peach. A big left-aligned headline over a stack of paper sheets, graph-paper body slides, highlighter underlines on the key words and a segmented progress bar. Comes in three palettes: the default teal, `skin-sand` (warm sand and espresso) and `skin-slate` (cool slate and sky). Good for tutorials, tools, education.

<img src="assets/templates/07-paper-stack.jpg" width="860" alt="Template 07 · Paper Stack: eight sample slides">

<img src="assets/templates/07-paper-stack-skins.jpg" width="640" alt="Template 07 palettes: default teal, sand, slate">

*Default, `skin-sand`, `skin-slate`. Put the skin class on `<body>`.*

### 08 · Tape Label
Butter and charcoal. Huge left-aligned type with one word on a tilted paper label, taped label headlines, die-cut stickers and a hazard-tape footer band. Good for tips, creative and playful topics.

<img src="assets/templates/08-tape-label.jpg" width="860" alt="Template 08 · Tape Label: eight sample slides">

### 09 · Clean Object
White space, heavy grotesk headlines with a serif italic accent, a yellow pill, glossy objects and a numbered gallery that peeks off the edges. Good for design, business, creator content.

<img src="assets/templates/09-clean-object.jpg" width="860" alt="Template 09 · Clean Object: eight sample slides">

### 10 · Sticky Mono
Flat orange or paper slides, monospace notes, a sticky number tab and marker highlights. Good for stories, career notes, long-form tips.

<img src="assets/templates/10-sticky-mono.jpg" width="860" alt="Template 10 · Sticky Mono: eight sample slides">

### 11 · Neon Hook
Dark violet, a centered hook headline, a gradient CTA pill and glowing objects. Good for hooks, tech, short punchy explainers.

<img src="assets/templates/11-neon-hook.jpg" width="860" alt="Template 11 · Neon Hook: eight sample slides">

### 12 · News Wire
Full-bleed news photo under a dark scrim, a red angled tag, a big headline stack and a meta line. Body slides read like a wire desk: heavy masthead rule on top, ticker band at the foot. Good for breaking news, local news, announcements.

<img src="assets/templates/12-news-wire.jpg" width="860" alt="Template 12 · News Wire: eight sample slides">

### 13 · News Card
The photo melts into paper and a white rounded story card sits on top with a category chip, headline, short summary and a swipe pill. Body slides are soft cards. Good for sports, lifestyle, explainers.

<img src="assets/templates/13-news-card.jpg" width="860" alt="Template 13 · News Card: eight sample slides">

### 14 · News Split
A tall photo that fades into a dark panel, condensed uppercase headline and an orange footer bar. Body slides use solid top and bottom bars and include a claim vs fact-check slide. Good for weather, incidents, fact checks, short bulletins.

<img src="assets/templates/14-news-split.jpg" width="860" alt="Template 14 · News Split: eight sample slides">

### 15 · Riso Print
Two-ink risograph print: blue and fluorescent pink on warm paper, overprinted circles, halftone dots and slightly misregistered big type. Good for creative work, events, communities, zines.

<img src="assets/templates/15-riso-print.jpg" width="860" alt="Template 15 · Riso Print: eight sample slides">

### 16 · Blueprint
A technical drawing: blueprint blue and drafting paper, a grid, monospace titles, dimension lines, callout circles and a title block at the foot. Good for tech, how-it-works posts, processes.

<img src="assets/templates/16-blueprint.jpg" width="860" alt="Template 16 · Blueprint: eight sample slides">

### 17 · Bento Grid
Dashboard tiles on a quiet canvas: every block is a rounded tile, one lime highlight tile per slide, big figures. Good for data, product features, comparisons.

<img src="assets/templates/17-bento-grid.jpg" width="860" alt="Template 17 · Bento Grid: eight sample slides">

### 18 · Chat Thread
Every slide is a message thread: chat header, timestamp chips, incoming and outgoing bubbles, typing dots and a composer bar. Good for hooks, scripts, Q&A, myth vs fact.

<img src="assets/templates/18-chat-thread.jpg" width="860" alt="Template 18 · Chat Thread: eight sample slides">

### 19 · Receipt
A thermal receipt on a desk: torn zigzag paper, dashed rules, line items with prices, a total, a barcode and one red stamp. Good for pricing, costs, checklists, money topics.

<img src="assets/templates/19-receipt.jpg" width="860" alt="Template 19 · Receipt: eight sample slides">

### 20 · Comic Pop
A comic-book page: yellow and blue with halftone dots, inked panels with hard shadows, caption boxes, a speech bubble and a starburst. Good for casual education, myth busting, younger audiences.

<img src="assets/templates/20-comic-pop.jpg" width="860" alt="Template 20 · Comic Pop: eight sample slides">

### 21 · Bauhaus
Primary red, yellow and blue on paper and black: circles, quarter circles and triangles, heavy uppercase grotesk, a color strip and a solid footer band. Good for design, branding, principles.

<img src="assets/templates/21-bauhaus.jpg" width="860" alt="Template 21 · Bauhaus: eight sample slides">

### 22 · Retro OS
An early desktop computer: windows on a dithered desktop, striped title bars, pixel headlines, dialog boxes and beveled buttons. Good for digital tips, productivity, tech nostalgia.

<img src="assets/templates/22-retro-os.jpg" width="860" alt="Template 22 · Retro OS: eight sample slides">

### 23 · Pixel Quest
An 8-bit game screen: arcade headlines, a HUD with hearts and a level counter, pixel-bordered dialog boxes, XP tags and a ground strip. Good for gamified steps, challenges, habits.

<img src="assets/templates/23-pixel-quest.jpg" width="860" alt="Template 23 · Pixel Quest: eight sample slides">

### 24 · Notebook Doodle
A spiral notebook page: ruled lines, a red margin, handwritten headlines, highlighter strokes, hand-drawn circles and taped sticky notes, with a black-paper alternate. Good for study tips, personal notes, personal brands.

<img src="assets/templates/24-notebook-doodle.jpg" width="860" alt="Template 24 · Notebook Doodle: eight sample slides">

### 25 · Code Editor
An editor window: file tab, line numbers, syntax-coloured headlines, a red and green diff, a terminal prompt and a status bar. Good for coding tips, dev tools, tech tutorials.

<img src="assets/templates/25-code-editor.jpg" width="860" alt="Template 25 · Code Editor: eight sample slides">

### 26 · Browser Window
Every slide is a web page inside a browser frame: address bar, hero section, call-to-action button with a cursor, metric cards. Good for web, SEO and digital product tips.

<img src="assets/templates/26-browser-window.jpg" width="860" alt="Template 26 · Browser Window: eight sample slides">

### 27 · Search Results
The headline is typed into a search field; answers arrive as autocomplete suggestions, ranked results and a featured answer. Good for question hooks and FAQs.

<img src="assets/templates/27-search-results.jpg" width="860" alt="Template 27 · Search Results: eight sample slides">

### 28 · Lock Screen
A phone lock screen: oversized clock, stacked notification cards with app icons, widgets and a home indicator over a gradient wallpaper. Good for hooks, reminders, habits.

<img src="assets/templates/28-lock-screen.jpg" width="860" alt="Template 28 · Lock Screen: eight sample slides">

### 29 · Notes App
A clean notes app: serif note titles, yellow highlight, numbered lists, pinned note cards and a checklist. Good for short tips, lists, journaling.

<img src="assets/templates/29-notes-app.jpg" width="860" alt="Template 29 · Notes App: eight sample slides">

### 30 · Kanban Board
A task board: To do, Doing and Done columns, cards with coloured labels, a WIP limit and a done checklist. Good for process, productivity, project management.

<img src="assets/templates/30-kanban-board.jpg" width="860" alt="Template 30 · Kanban Board: eight sample slides">

### 31 · Calendar
A calendar app: date tiles with a red weekday band, a day agenda with timed, colour-coded events and week strips. Good for plans, routines, countdowns.

<img src="assets/templates/31-calendar.jpg" width="860" alt="Template 31 · Calendar: eight sample slides">

### 32 · Music Player
A now-playing screen: gradient album cover, transport controls, tracklist rows, lyric-style quotes and a scrubber that advances with every slide. Good for lifestyle, playlists, recommendations.

<img src="assets/templates/32-music-player.jpg" width="860" alt="Template 32 · Music Player: eight sample slides">

### 33 · App Store
A store listing: app icon, Get button, ratings strip with stars, screenshot cards, version notes and a starred review. Good for reviews, tool recommendations, launches.

<img src="assets/templates/33-app-store.jpg" width="860" alt="Template 33 · App Store: eight sample slides">

### 34 · Settings Screen
A phone settings page: grouped rows with toggles switched on or off, a slider and quick-setting tiles. Good for do versus don't, habits to turn on or off.

<img src="assets/templates/34-settings-screen.jpg" width="860" alt="Template 34 · Settings Screen: eight sample slides">

### 35 · Spreadsheet
A sheet: cell grid, lettered columns, formula bar, a selected cell with its fill handle, table rows and red and green conditional fills. Good for money, data, comparisons.

<img src="assets/templates/35-spreadsheet.jpg" width="860" alt="Template 35 · Spreadsheet: eight sample slides">

### 36 · Glass Widgets
Home-screen widgets in frosted glass over a soft mesh gradient, with progress rings and a mini bar chart. Good for light data, lifestyle, premium brands.

<img src="assets/templates/36-glass-widgets.jpg" width="860" alt="Template 36 · Glass Widgets: eight sample slides">

**About the news covers.** Templates 12 to 14 need a cover photo: swap the `src` in the `news-photo` figure (and set `--focus` on it to choose the crop) and add a photo to the slide that carries one. The sample photos are from the Kodak Lossless True Color Image Suite, released by Kodak for unrestricted use; replace them with your own before publishing.

**About the hero objects.** Templates 07 to 11 draw their default art (paper sheets, glossy cubes, balls and rings, die-cut stickers) as SVG, so the previews need no photos. To use your own transparent PNG or photo, put an `<img>` inside the `.object` element and it replaces the default. Generative AI imagery is still not allowed.

**About templates 15 to 36.** Each one is a themed skin over the same patterns: the paper strip, windows, bubbles, tiles, doodles and app chrome are drawn by its `tokens.css`, so they need no photos. Keep the slide markup as in `sample.html` and replace the copy. Templates 25 to 36 imitate app screens; where a value drives the decor (a toggle, a slider, a progress ring, the music scrubber) it is set in the markup, as noted in the comment at the top of each `sample.html`.

Need a different slide count (5 to 10), your own photos, or another pattern for one slide? Say so in the brief. Templates stay locked, so the look never drifts. The previews above use sample copy and no photos. See [Adding photos](#adding-photos).

---

## How it works

```mermaid
flowchart TD
    A[Install the skill] --> B{Template picked?}
    B -->|Yes: template N| G[Template locked]
    B -->|Custom look| C[Onboarding dialog or reference]
    C --> D[Agent sets brand tokens]
    D --> E[Render sample patterns]
    E --> F{User approves?}
    F -->|No| D
    F -->|Yes| G2[Design system locked by name]
    G --> H[Topic brief + image map]
    G2 --> H
    H --> I[Composition plan: one pattern per slide]
    I --> J[Copywriting + image verification]
    J --> K[Compose HTML from patterns]
    K --> L[Render through quality gates]
    L --> M[Ready-to-post JPGs]
```

**Template path (default).** Pick a number and send a topic. Phase 1 is already done for you.

**Phase 1, custom only: lock a design system.** Answer 7 quick questions, or send a screenshot or HTML file you like as reference. The agent sets your brand tokens, renders sample patterns in them, and iterates with you until you approve. Name it (for example `morningcup-playful`). Build more named systems anytime and pick one per carousel.

**Phase 2: compose carousels.** For each new topic the agent plans a composition (one pattern per slide, no two neighbors alike, light and dark alternating), writes the copy, verifies and places your images, and renders print-clean JPGs. A custom system also never repeats the previous carousel's cover. Variety is enforced by hard rules, not left to chance.

## The onboarding dialog (custom design system only)

Skip this when you use a template.

| # | Question | Choices |
|---|---|---|
| 1 | What vibe should the carousel have? | Playful and friendly / Clean and minimal / Bold and striking / Warm and elegant / Dark and premium |
| 2 | Pick a color mood. | Warm earth / Fresh natural / Ocean calm / Bold contrast / Soft pastel |
| 3 | Pick a type feel. | Rounded and playful / Elegant serif / Bold and modern / Clean and simple |
| 4 | Brand name and handle for the watermark? | Free text |
| 5 | What are the carousels usually about? | Free text |
| 6 | Indonesian or English? | Two choices |
| 7 | What should we call this design system? | Free text |

Font choices stay at the feel level. The agent maps them to real fonts internally. No font names, no jargon. All fonts are bundled in `fonts/`.

## The pattern library

Twenty structural patterns in `design-system/`, all token-driven. Each slide can also flip to the system's dark mode with one class (`mode-dark` on the `<section>`), so a carousel can alternate light and dark slides without any redesign.

| Pattern | Use for |
|---|---|
| cover-big-type, cover-split | Opening hooks |
| kicker-statement | Editorial openers, strong claims |
| stat-band, big-number | Numbers and research |
| concept-number | One big idea per slide |
| quote | A line worth remembering |
| two-cards | Paired ideas, do vs don't |
| image-hero | A photo that carries the slide (other photo layouts: see Adding photos) |
| process-steps | Sequences and how-tos |
| myth-fact | Correcting a misconception |
| takeaway | Closers, recaps, CTAs |
| cover-poster, cover-hook, cover-label, cover-object | Object-led covers (templates 07 to 11) |
| cover-news | Photo-led news covers (templates 12 to 14) |
| pointer | A story beat that ends in a turn |
| showcase | A gallery of examples or screenshots |
| note | Long-form tips in a personal voice |

## Adding photos

Any body slide can take a photo. Give the agent the file (or a URL) and say which slide it belongs on. Each image is checked before use: it must match the slide topic, carry no watermark or foreign logo, and be sharp enough (shortest side 900px or more for large use). Four layouts, all skinned by the template tokens:

| Layout | What it looks like | Use for |
|---|---|---|
| One framed photo (`photo`) | 16:10 frame under the copy. `wide` (5:2) and `band` (3:1) for dense slides. | Most body slides |
| Two photos (`photos`) | Two square frames side by side, same gutter as `two-cards`. `short` (4:3) for dense slides. | Before and after, two examples |
| Full-bleed top (`photo-top`) | One photo edge to edge on top with rounded bottom corners. The topbar sits on it, the copy starts below. | Hero-style slides. Pick a photo with a calm top edge |
| Photo slide (`image-hero`, `cover-split`) | The photo is the slide. | Strong covers and showpiece images |

<img src="assets/photo-layouts.jpg" width="860" alt="Photo layouts: one framed photo, two photos, full-bleed top photo, and a 3:1 band photo, each in a different template">

*Left to right: `photo` in Warm Elegant, `photos` in Fresh Garden, `photo-top` in Dark Premium, and `photo band` in Bold Contrast. Sample photos are from the Kodak Lossless True Color Image Suite, released by Kodak for unrestricted use.*

Every frame takes an optional caption on a scrim and a crop point (`--focus`). Details and markup are in `design-system/PATTERNS.md`.

## Design standards

Every slide is held to the same bar:

- **Hierarchy.** The headline is the largest, boldest element. One accent-colored word per headline.
- **Text on photos.** It sits on a scrim or card. Never on a busy photo directly.
- **Typography.** Two font families maximum. Every font must load, or the render fails. Body copy is 28 to 32px and nothing is smaller than 20px, so it stays readable on a phone.
- **Contrast.** Body, muted, footer, and accent text hold at least 4.5:1 against their background in both modes (WCAG AA).
- **Color.** 60 percent base, 30 percent secondary, 10 percent accent.
- **Copy.** Short declarative sentences. Concrete nouns and strong verbs. No AI tells: no em dashes, no "delve", no "unlock", no filler openers.
- **Consistency.** Tokens never change across slides. Patterns vary. That is the whole trick.
- **Two modes.** Every template and system ships a light and a dark token set. Slides alternate modes. Templates fix the order, custom systems open each carousel with the opposite mode of the last one.

## Quick start

1. Copy the `carouso/` folder into your agent's skills directory (`~/.claude/skills/`, `~/workspace/skills/`, or your platform's skills folder).
2. Install the renderer once: `pip install playwright && playwright install chromium`.
3. Tell your agent: `template 2, topic: how to write notes you will reopen`.
4. Get back `slide_01.jpg` to `slide_08.jpg` in `carousels/<name>/`.

Want your own brand instead? Ask for a custom design system and answer the 7 questions.

### Output sizes

| Format | Size | For |
|---|---|---|
| `portrait` (default) | 1080x1440 | Instagram and Facebook carousels |
| `feed` | 1080x1350 | 4:5 feed posts, LinkedIn |
| `story` | 1080x1920 | TikTok photo mode, Stories, Reels covers |

```
python3 scripts/render_carousel.py --html carousels/<name>/index.html --out carousels/<name>/story --format story --slides 8
```

The slides reflow to the new height instead of being scaled. At 9:16 the topbar, footer and every line of text stay out of the top and bottom 250px, where the app draws its own buttons and captions.

### Brand kit

Put your name, handle, logo and accent colour in one `brand.json` and render any template with it. The HTML keeps its placeholders, so the same carousel renders for another brand.

```json
{
  "name": "Kopi Pagi",
  "handle": "@kopipagi",
  "url": "kopipagi.id",
  "logo": "logo.svg",
  "logo_on_dark": "logo-on-dark.svg",
  "accent": "#c2410c"
}
```

```
python3 scripts/render_carousel.py --html carousels/<name>/index.html --out carousels/<name> --slides 8 --brand examples/brand-kit/brand.json
```

The accent keeps its hue and is darkened or lightened only where text in it would be too faint to read. A name too long for its line, or a logo that cannot be seen on a dark slide, fails the render. Every key is listed under "Brand kit" in `SKILL.md`; `examples/brand-kit/` is a working kit.

## Package contents

```
carouso/
├── SKILL.md                  ← the whole skill: workflow, design thinking, gates
├── templates/
│   └── NN-name/              ← thirty-six templates, each with:
│       ├── tokens.css        ←   colors, fonts, light and dark modes (07 to 11 and some of 15 to 36 also draw art from decor/; 12 to 14 ship sample photos in images/)
│       ├── template.json     ←   name, fonts, size, slide sequence
│       └── sample.html       ←   the finished 8-slide sample to copy from
├── design-system/
│   ├── system.css            ← structure + all 20 pattern styles (shared by every template)
│   ├── patterns.html         ← the first 12 patterns as full slides (07 to 14 demo the newer eight)
│   └── PATTERNS.md           ← catalog: what each pattern is for
├── fonts/                    ← bundled fonts (SIL OFL) + fonts.css
├── assets/
│   ├── photo-layouts.jpg     ← the four photo layouts in four templates
│   └── templates/            ← the thirty-six template previews
├── scripts/
│   ├── render_carousel.py    ← Playwright render with quality gates
│   ├── gates.py              ← the pixel gates: contrast, covered or colliding text, density
│   ├── test_gates.py         ← breaks a sample on purpose to prove each gate fires (runs in CI)
│   ├── brand.py              ← the brand kit: name, handle, logo and accent on any template
│   ├── test_brand.py         ← renders good and bad brand kits to prove each one is handled (runs in CI)
│   ├── check_templates.py    ← consistency check for every template (runs in CI)
│   ├── copy_budget.py        ← measures how many characters each slide's headline holds
│   └── build_preview.py      ← compose rendered slides into a README preview sheet
└── examples/
    ├── brief-example.md      ← a complete brief and how the skill handles it
    └── brand-kit/            ← a working brand kit: brand.json and two logo files
```

Output goes to `carousels/<name>/` (git-ignored).

## Render requirements

- Python 3 plus `playwright` (`pip install playwright && playwright install chromium`)
- Nothing else. Fonts are bundled in `fonts/`, so the font gate passes on a clean machine.

## Changing a template

1. Edit `templates/NN-slug/sample.html` and keep `template.json` in step (each `<section>` carries `data-pattern`, its `p-*` class, and `mode-dark` for dark slides). After any change to a headline, font or size, run `python3 scripts/copy_budget.py --write` so the `headline` budgets match.
2. `python3 scripts/check_templates.py` must report OK. CI runs it and renders every template on each pull request.
3. Refresh the preview: render the sample to `out/NN-slug/`, then `python3 scripts/build_preview.py --slides out/NN-slug --out assets/templates/NN-slug.jpg`.

## Rules the skill never breaks

1. No template and no approved design system, no production.
2. Compose from the pattern library and the photo layouts. No per-carousel layout inventions.
3. Variety rules are hard rules: no adjacent duplicate patterns, alternating light and dark slides.
4. Images from uploads or URLs only. No generative AI imagery.
5. Every image is visually verified before use.
6. A failed quality gate means fix the HTML, never bypass the gate.
