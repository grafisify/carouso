# Carouso: a skill for AI agents

Carouso lets an AI agent produce **ready-to-post carousel posts** (Instagram, TikTok, Facebook) with real graphic design fundamentals, plus **image placement from user uploads or URLs**. No generative AI imagery.

## How it works: lock one template, then produce

**Step 1. Generate one template.** On first run the agent opens a short onboarding dialog: six quick questions with tappable choices (style vibe, color mood, type feel, brand name and handle, usual topic, language). Or send a screenshot or HTML file of a carousel you like as reference instead. The agent designs the template, renders sample slides, and iterates with you until you approve it. That one approved template becomes the design system for everything after. When your brand evolves, repeat this step and re-lock.

**Step 2. Produce carousels.** For each new topic, the agent writes the copy, places your images on the slides you choose, and renders JPGs through automatic quality gates. The layout never drifts, because every carousel starts from your locked template.

## Package contents

```
carouso/
├── SKILL.md                  ← the whole skill: workflow, design thinking, gates
├── assets/
│   └── base-template.html    ← starting scaffold for step 1 (not the final design)
├── scripts/
│   └── render_carousel.py    ← Playwright render with quality gates
└── examples/
    └── brief-example.md      ← a complete brief and how the skill handles it
```

There is no references folder. Everything the agent needs lives in `SKILL.md`: the two-phase workflow, the design thinking protocol, copy standards, layout fundamentals, and the operating rules.

## Install

Copy the `carouso/` folder into your agent's skills directory (for example `~/.claude/skills/`, `~/workspace/skills/`, or your agent platform's skills folder). The only extra dependency is **Playwright plus Chromium** for rendering (see `scripts/render_carousel.py`).

## Key principles

1. One locked template per brand. No template, no production.
2. Images come **only** from user uploads or URLs. No AI-generated images.
3. Every image passes **visual verification** before use.
4. Rendering runs through **automatic quality gates**: wrong slide count, overflow, wrong dimensions, or an unloaded webfont fails the render. The gate is fixed, never waived.
5. Fonts may come from Google Fonts or local installs, but they **must load**.
6. Minimal text (roughly 80 percent visual), one idea per slide, and a cover that earns the swipe.

## Render requirements

- Python 3 plus `playwright` (`pip install playwright && playwright install chromium`)
- The display and body fonts installed on the system (check: `fc-list | grep -i "<font-name>"`)
