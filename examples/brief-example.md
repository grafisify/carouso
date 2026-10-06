# Example: how the skill works

## Phase 1: lock the template (once)

The user says: "Brand: Morning Cup (@morningcup). Dark brown and cream, orange accent. Playful but clean. Here is a screenshot of a carousel style I like: <screenshot.png>"

The agent studies the screenshot (layout zones, type scale, spacing, color roles), rebuilds it as a clean template with CSS variables for every brand token, renders a cover plus one content slide plus a closer, and shows them. The user asks for a warmer background. The agent adjusts, re-renders, and the user approves. The file is saved as `template.html`. Phase 1 is done.

## Phase 2: produce a carousel

### Input brief (from the user)

> Topic: "5 mistakes that ruin Turkish coffee at home"
> Template: morningcup-playful
> Slides: 10, size 1080x1350
> Images:
> - Upload: `brewing.jpg` → slide 2, hero role (the brewing process)
> - Article URL: https://example.com/grind-size-guide → take the grind-size photo → slide 4, illustration role

### What the agent does

1. **Brief complete?** Yes. Topic, count, size, and the image map (source, slide, role) are all explicit. The locked `template.html` supplies the design. Proceed.
2. **Copy**: 10 slides. Cover hook: "Your Turkish coffee tastes burnt." Eight content slides, one mistake each ("Water at a rolling boil", "Grind finer than espresso", ...). Closer: 4 recap points plus a Save/Share CTA. Concrete headlines, under 8 words each.
3. **Ingest images**: `brewing.jpg` → `images/slide02_hero_brewing.jpg`. From the article URL, pick the grind-size photo (not the site logo) → download → record the page_url.
4. **Visual verification**: both images match their slides, no watermarks, sharp enough. Pass.
5. **Fill the template**: copy `template.html`, fill the 10 slides, point each `img` at a local file. No layout redesign.
6. **Render**: `python3 scripts/render_carousel.py --html turkish-coffee.html --out out/ --width 1080 --height 1350 --slides 10 --check-fonts "Baloo 2,Quicksand"`. All gates pass.
7. **Final check**: slides 1, 5, 10 look right. Done.

### What the agent does NOT do

- Redesign the layout for this carousel.
- Generate AI images, hotlink URLs at render time, or waive a failed gate.
