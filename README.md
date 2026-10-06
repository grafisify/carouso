# Carouso: a skill for AI agents

Carouso lets an AI agent produce **ready-to-post carousel posts** (Instagram, TikTok, Facebook) with real graphic design fundamentals, plus **image placement from user uploads or URLs/articles**. No generative AI imagery.

## Package contents

```
carouso/
├── SKILL.md                      ← read by the agent when the skill triggers
├── references/
│   ├── design-fundamentals.md    ← hierarchy, contrast, typography, color, safe zones
│   ├── layout-rules.md           ← slide anatomy, cover/content/closer rules, copy standards
│   └── image-workflow.md         ← upload/URL ingest, visual verification, crop and placement
├── assets/
│   └── base-template.html        ← 10-slide template with image slots, ready to fill
├── scripts/
│   └── render_carousel.py        ← Playwright render with quality gates (count, overflow, size, fonts)
└── examples/
    └── brief-example.md          ← a complete brief and how the skill handles it
```

## Install

Copy the `carouso/` folder into your agent's skills directory (for example `~/.claude/skills/`, `~/workspace/skills/`, or your agent platform's skills folder). The only extra dependency is **Playwright plus Chromium** for rendering (see `scripts/render_carousel.py`).

## Key principles

1. Images come **only** from user uploads or URLs/articles. No AI-generated images.
2. Every image passes **visual verification** before use.
3. Rendering runs through **automatic quality gates**: wrong slide count, overflow, wrong dimensions, or an unloaded webfont fails the render. The gate is fixed, never waived.
4. Fonts may come from Google Fonts or local installs, but they **must load**. The `--check-fonts` gate rejects output where a webfont failed and the headline fell back.
5. Minimal text (roughly 80 percent visual), one idea per slide, and a cover that earns the swipe.

## Render requirements

- Python 3 plus `playwright` (`pip install playwright && playwright install chromium`)
- The display and body fonts installed on the system (check: `fc-list | grep -i "<font-name>"`)
