# Example brief: how the skill works

## Input brief (from the user)

> Topic: "5 mistakes that ruin Turkish coffee at home"
> Slides: 10, size 1080x1350
> Brand: Morning Cup (@morningcup), colors: dark brown #3a2a1e plus cream #f5ead9,
> accent orange #d97b2b, display font: Baloo 2, body font: Quicksand
> Images:
> - Upload: `brewing.jpg` → slide 2, hero role (the brewing process)
> - Article URL: https://example.com/grind-size-guide → take the grind-size
>   photo → slide 4, illustration role

## What the agent does

1. **Brief complete?** Yes. Topic, count, size, brand, and the image map (source, slide, role) are all explicit. Proceed.
2. **Copy**: write 10 slides. Cover hook: "Your Turkish coffee tastes burnt." Eight content slides, one mistake each ("Water at a rolling boil", "Grind finer than espresso", ...). Closer: 4 recap points plus a Save/Share CTA. Every headline stays concrete and under 8 words.
3. **Ingest images**:
   - `brewing.jpg` → copied to `images/slide02_hero_brewing.jpg`
   - Open the article URL → pick the grind-size photo that fits (not the site logo) → `curl -sL -o images/slide04_illustration_grind.jpg <url>` → record the page_url
4. **Visual verification**: look at both images. Both match their slide topics, no watermarks, shortest side above 900px. Pass. (On failure: reject and swap in a graphic card.)
5. **Build HTML**: copy `assets/base-template.html`, set the `:root` tokens (colors, brand, handle, fonts), fill 10 slides, point each `img` at a local file.
6. **Render**: `python3 scripts/render_carousel.py --html turkish-coffee.html --out out/ --width 1080 --height 1350 --slides 10 --check-fonts "Baloo 2,Quicksand"`. All gates pass.
7. **Final check**: open slides 1, 5, 10. Baloo 2 rendered, no overflow, images undistorted.
8. **Output**: `out/slide_01.jpg` through `slide_10.jpg`, plus `turkish-coffee.html`, `images/`, and `provenance.log`.

## What the agent does NOT do

- Generate AI images for slides 2 and 4 (or any slide).
- Hotlink image URLs at render time.
- Waive a failed quality gate.
