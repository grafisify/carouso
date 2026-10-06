# Layout and copy rules

## Slide anatomy (identical on every slide)
```
+-----------------------------------+
| topbar: brand (left) | 01 / 10    |  fixed height, divider line
+-----------------------------------+
| eyebrow pill (slide category)     |
|                                   |
| HEADLINE (display font, dominant) |  content zone: vertical flex flow,
| subhead/body (1-2 sentences)      |  no absolute positioning
| +-------------------------------+ |
| | support card                  | |  fact, step, quote, or
| | (icon/image + short text)     | |  illustration image
| +-------------------------------+ |
+-----------------------------------+
| footer: @handle | CTA              |  absolute bottom, safe zone
+-----------------------------------+
```

## Cover rules (slide 1)
- The headline block centers horizontally and vertically (it sits mid-slide, around 53 percent height), not pinned to the top.
- Cover headline runs 1.3-1.5x the size of content-slide headlines. An accent line may sit under the headline (cover only, as decoration).
- Structure: category eyebrow, hook headline (3-7 words), one explanatory sentence, one teaser card. The footer CTA is a pill that invites action (for example "Save this").
- The cover carries no details. Its job is to earn the swipe.

## Content slide rules (2 to N-1)
- One slide holds one idea. Headlines use descriptive labels, not numbers: "Chill the onion for 15 minutes", not "Tip 1".
- The support card holds one of: a short fact, a concrete step, a brief quote, or an illustration image with a one-line caption.
- Quote slides stay short and punchy, never a paragraph.
- Recap/takeaway slides hold 4 points, each one line with a clear label.

## Closer rules (slide N)
- A 3-4 point recap plus an explicit CTA: Save, Share, Follow.
- Write the CTA in the audience's own voice, not from a template.

## Text budget per slide
| Element | Maximum |
|---|---|
| Headline | 8 words |
| Subhead/body | 25 words |
| Support card | 30 words |
| Total above the footer | about 60 words |

When the brief copy exceeds the budget, cut the sentences. Do not shrink the font below the minimum and do not compress the spacing.

## Copy standards
Carousel copy follows the same bar as any prose surface. Concrete beats clever.
- Hooks use one of three patterns: a curiosity gap ("The 15-minute onion trick"), a specific number ("5 mistakes that ruin pour-over"), or direct address ("Your sourdough is overproofed").
- Prefer concrete nouns and verbs over adjectives. "Chill the onion" beats "prepare the onion properly".
- One specific detail beats three vague ones. Name the time, the temperature, the amount.
- Cut AI tells from slide copy: no "delve", "unlock", "elevate", "game-changer"; no "not just X, but Y" constructions; no forced triads; no emojis as bullet substitutes.
- The subhead makes a promise, not a summary. It tells the reader what they get from swiping, not what the carousel contains.

## Images inside the layout
- Image slots use fixed-ratio frames (see `.img-frame` in the template). Images fill the frame with `object-fit: cover`. Never stretch.
- Supported roles:
  - **hero**: a large image in the content area (4:3 or 16:10 ratio).
  - **illustration**: a small image beside text (1:1 or 4:3 ratio).
  - **full-bleed**: an image covering part of the slide with a scrim gradient so overlaid text stays readable.
- Keep the photo's subject inside the frame. Choose a safe crop (see the crop guide in `image-workflow.md`).
- One dominant image per slide that uses images. Two large photos on one slide almost always look messy.
