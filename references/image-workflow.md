# Image workflow: user uploads and URLs/articles

> Principle: images in this skill come from two sources only. Files the user uploads, or images taken from a URL or article. **Never use generative AI imagery in any form.**

## 1. Ingest (collect locally)

### From a user upload
- Read the file from the path the user gives. Record the original filename in `provenance.log`.
- Supported formats: JPG, PNG, WebP. Convert anything else to JPG or PNG first.

### From a direct URL (an image)
- Download with `curl` (avoid urllib behind a proxy for large bodies, it often dies mid-transfer):
  ```
  curl -sL -m 60 -o images/slide03_hero.jpg "<image-url>"
  ```
- Verify the download: open the file and confirm it is a valid image (not an HTML error page or a 1KB redirect).

### From an article URL
1. Open the article and pick the image that fits the slide topic (a content photo, not the site logo, ad banner, or author avatar).
2. Prefer photos that look natural and authentic over over-polished studio shots, unless the brief asks for a premium feel.
3. Download the image locally, same as a direct URL.
4. Record the article `page_url` as provenance. When the article credits a photographer or source, add a small credit in the image caption.

### General ingest rules
- Copy every image into the local `images/` folder before rendering. The render must not hotlink external URLs (nondeterministic output, fails offline).
- Name files clearly: `slide<NN>_<role>_<short-desc>.jpg` (example: `slide03_hero_red-onion.jpg`).

## 2. Visual verification (hard gate, never skipped)

Before an image goes on any slide, look at it and answer this checklist:
- [ ] Does the content fit the requested slide topic? (An onion photo for an onion slide, not a vaguely similar generic photo.)
- [ ] Free of watermarks, logos, and foreign text?
- [ ] Sharp, not blurry? Shortest side at least 900px for large use (hero or full-bleed), at least 500px for small illustrations.
- [ ] Croppable safely? The main subject does not touch the frame edges.

**One "no" rejects the image.** The options then: ask the user for another image, find an alternative from another URL or article, or replace the image slot with a graphic element (icon, color card, pattern). Never force a failed image into the design.

## 3. Placement and cropping
- Place images inside `.img-frame` (fixed-ratio frame) with `object-fit: cover; object-position: center;`. Never stretch.
- When the subject sits off-center (a face on the left side), adjust `object-position` (for example `20% 50%`) so the frame does not cut it.
- Full-bleed: add a scrim gradient (dark where the text sits). Text on a photo without a scrim fails readability.
- One dominant image per slide that uses images. The only exception is a collage the brief explicitly requests, with uniform frames.

## 4. Prohibitions
1. No AI-generated images, for any reason.
2. No image goes in before visual verification.
3. No hotlinked external images at render time.
4. No images with clearly restrictive or paid licensing (a watermark is the clearest signal). Choose freely licensed sources or the user's own photos.
