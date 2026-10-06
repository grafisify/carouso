# Example: how the skill works

## Phase 1: lock the design system (once)

The user answers the 7 onboarding questions: playful and friendly, warm earth colors, rounded type feel, "Morning Cup / @morningcup", coffee topics, English, named "morningcup-playful".

The agent sets the `:root` tokens in `design-system/system.css` to the brand, renders three sample patterns (cover-big-type, stat-band, takeaway), and shows them. The user asks for a warmer background. The agent adjusts the tokens, re-renders, and the user approves. The system is saved to `design-systems/morningcup-playful/`. Phase 1 is done.

## Phase 2: compose a carousel

### Input brief (from the user)

> Topic: "5 mistakes that ruin Turkish coffee at home"
> Design system: morningcup-playful
> Slides: 6, size 1080x1350
> Images:
> - Upload: `brewing.jpg` → slide 3, hero role (the brewing process)
> - Article URL: https://example.com/grind-size-guide → take the grind-size photo → slide 5, inline role

### What the agent does

1. **Brief complete?** Yes. Topic, system, count, size, and the image map (source, slide, role) are all explicit. Proceed.
2. **Composition plan.** Read `last-used.json` (previous carousel opened with cover-big-type). Plan: 1 cover-split, 2 kicker-statement, 3 image-hero, 4 myth-fact, 5 process-steps, 6 takeaway. Six slides, six different patterns, cover not repeated.
3. **Copy**: cover hook "Your Turkish coffee tastes burnt." Four content slides, one mistake each ("Water at a rolling boil", "Grind finer than espresso", ...). Closer: 3 recap points plus a Save/Share CTA. Concrete headlines, under 8 words each.
4. **Ingest images**: `brewing.jpg` → `images/slide03_hero_brewing.jpg`. From the article URL, pick the grind-size photo (not the site logo) → download → record the page_url.
5. **Visual verification**: both images match their slides, no watermarks, sharp enough. Pass.
6. **Build HTML**: copy the `<style>` from the locked `system.css`, copy the six chosen `<section>` blocks from `patterns.html`, fill copy and image slots. Point each `img` at a local file.
7. **Render**: `python3 scripts/render_carousel.py --html turkish-coffee.html --out out/ --width 1080 --height 1350 --slides 6 --check-fonts "Baloo 2,Quicksand"`. All gates pass.
8. **Final check and record**: slides 1, 3, 6 look right. Write the pattern sequence to `last-used.json`. Done.

### What the agent does NOT do

- Invent a new layout for this carousel.
- Repeat the previous carousel's cover pattern.
- Generate AI images, hotlink URLs at render time, or waive a failed gate.
