# Pattern catalog

Twelve structural patterns. Each is one full slide in `patterns.html`
(`data-pattern` marks the name). Copy the `<section>` block into the working
carousel file. Never edit the structure per carousel. Only the copy, images,
and token values change.

Patterns are structural, not topical. The sample psychology copy is placeholder.
Reuse any pattern for any niche.

## Covers (pick one per carousel)

### cover-big-type
Centered monumental headline, kicker, one-line promise, decorative ring and gold line.
Use when: the hook is a bold claim or a curiosity gap and no image is needed.

### cover-split
Image on one side, headline on the other, divided by a gradient edge.
Use when: a strong photo can carry half the cover.

## Openers

### kicker-statement
Kicker, accent rule, oversized editorial statement, one supporting paragraph.
Use when: opening with a strong opinion or reframing the topic.

## Body

### stat-band
Three statistics on a ruled band.
Use when: the slide's point is carried by numbers or research findings.

### concept-number
Oversized numeral plus a bordered explanation block.
Use when: one big idea deserves the whole slide.

### quote
Giant serif quote mark, large serif quote, source line.
Use when: a single memorable line is the message.

### two-cards
Two dark cards side by side, each with a label, headline, and line.
Use when: comparing two options, or pairing do and don't.

### image-hero
16:10 image frame with scrim and caption. Swap the `empty` class for a real
`<img>` when a verified image is placed.
Use when: a photo carries the slide's meaning.

### process-steps
Numbered rows with titles, one-liners, and right-side tags.
Use when: the content is a sequence, routine, or how-to.

### myth-fact
Two-column bordered grid: myth on the left, fact on the right.
Use when: correcting a misconception.

### big-number
One giant outlined figure plus a short headline and line.
Use when: a single jaw-dropping number makes the point alone.

## Closers (pick one per carousel)

### takeaway
Dot list of takeaways plus a centered CTA line.
Use when: closing with a recap and an action.

## Composition rules

- A carousel opens with one cover pattern and closes with one closer pattern.
- No two adjacent slides use the same pattern.
- Never run the same cover pattern on two consecutive carousels for one brand.
- Match the pattern to the content: numbers go to stat-band or big-number,
  sequences go to process-steps, a single line goes to quote. Do not force
  content into a pattern that fights it.
- Track usage per design system in `last-used.json` (cover pattern plus full
  sequence). Read it before composing the next carousel.

## Two modes

Every slide can be light or dark. Add the `mode-dark` class to the
`<section class="slide ...">` to flip that slide to the system's dark
tokens. All patterns read tokens, so the flip needs no other changes.

Rules:
- Alternate modes: no two adjacent slides share a mode.
- Each new carousel starts with the opposite mode of the previous
  carousel's first slide (recorded in `last-used.json` as `modes`).
- Use the flip deliberately: contrast pairs (myth vs fact, problem vs
  solution, before vs after) read naturally as mode changes.

`system.css` must define `.slide.mode-dark` with the brand's dark
tokens. The shipped file's block matches its dark theme; light systems
override it with their own dark palette.
