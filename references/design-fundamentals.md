# Graphic design fundamentals for carousels

Decision rules for laying out every slide. Written as a checklist, not theory.

## 1. Visual hierarchy
Each slide has one thing the eye meets first. The target reading order is headline, then visual, then body, then support card, then footer.
- The headline is the largest and boldest element on the slide (display font, 84-132px on a 1080x1350 canvas; the cover runs 1.3-1.5x larger than content slides).
- One key word or phrase in the headline gets the accent color. Nothing else does.
- Body copy is far smaller (24-28px) and lighter in color than the headline.

## 2. Contrast
- Text over a photo needs a layer between them (a gradient scrim or a semi-solid card). Never place text directly on a busy photo.
- Body text must read at a glance. When in doubt, darken the background or lighten the text.
- Spend the accent color sparingly: one accent for keyword highlights, accent lines, and the CTA. Everything else stays neutral.

## 3. Alignment and grid
- Every slide uses the same inner margins (for example 60-64px left and right).
- Default to left alignment. Centered text is allowed on the cover only, as a deliberate exception (the cover headline block centers horizontally and vertically).
- Do not mix left and centered alignment inside one content slide.

## 4. Whitespace
- Keep at least one body line-height of space between blocks. A cramped slide means the copy needs cutting, not a smaller font.
- Support cards always get inner padding (32px minimum) and a consistent corner radius.

## 5. Typography
- The standard pairing is one display font for headlines (characterful: a handwritten or bold rounded face reads playful) plus one clean, highly legible body font.
- Two font families per carousel, maximum. Never add a third.
- Source: Google Fonts (via a `link` tag with `display=swap`) or locally installed fonts. A font that fails to load is the failure. The render gate (`--check-fonts`) rejects output where a webfont did not load and the headline fell back.
- Minimum sizes: 24px for body, 14-15px only for non-essential text (counters, footer). Everything that must be read is 24px or larger.

## 6. Color (the 60-30-10 rule)
- 60 percent base background color, 30 percent secondary color (cards and panels), 10 percent accent.
- Backgrounds may layer (gradient plus subtle texture plus vignette) as long as readability holds. Texture should be barely visible.
- Main text uses the darkest color of the palette. Secondary text uses a muted version of it.

## 7. Consistency and repetition
These elements appear on every slide and never change style: the topbar (brand plus `01 / 10` numbering), the footer (handle plus CTA), the eyebrow pill, card styling, corner radius, and shadows. That repetition is what makes ten slides feel like one piece instead of ten loose designs.

## 8. Safe zones
- 64px from each edge is the safe zone. No important text sits outside it.
- The footer is absolutely positioned at the bottom with safe clearance from the lower edge.

## 9. Anti-collision
Layout uses fixed zones (topbar, content, footer), not free absolute positioning between content elements. Content flows vertically with flex. Overflow is hidden and detected automatically at render time (see `scripts/render_carousel.py`). Elements that touch each other are a failed design. Fix the spacing.
