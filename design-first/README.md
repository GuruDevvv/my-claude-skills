# design-first

**Structured design exploration before coding.** Generate 4–6 diverse HTML prototypes, compare them side-by-side, pick the best — then build.

## The Problem

When AI generates a UI, you get one design. If you don't like it, you tweak endlessly. You never see the alternatives you're missing.

## The Solution

```
Interview → References → Design Brief → 6 Prototypes → Gallery → Pick & Mix → Build
```

The skill forces **divergent exploration** — 6 genuinely different visual directions, each a standalone HTML file you can open in a browser. A gallery page lets you compare them side by side with mobile/desktop toggle.

## What It Generates

- **Variant 0 (Free)** — AI's unconstrained best shot, generated first
- **Variants A–E** — 5 structured prototypes, each varying on temperature, typography, density, technique, and animation
- **Gallery page** — side-by-side comparison with iframe previews and direct links

## Key Features

- Context interview to understand audience, emotion, and goals
- Reference analysis (screenshots, URLs) → Design DNA extraction
- Design brief checkpoint before generation
- Cyrillic-safe font table (30+ verified Google Fonts)
- Mobile-first with desktop breakpoints (768px, 1440px)
- Animation guide with CSS-only and Canvas particle templates
- Parallel prototype generation via subagents
- Optional integration with `ui-ux-pro-max` for enhanced style selection

## Install

```bash
# Copy to Claude Code skills directory
cp -r design-first/ ~/.claude/skills/design-first/
```

Or symlink:
```bash
ln -s /path/to/my-claude-skills/design-first ~/.claude/skills/design-first
```

## Usage

Just describe what you need — the skill triggers on design-related requests:

- "Make a landing page for my bakery"
- "Design a dashboard for analytics"
- "Сделай дизайн для сайта психолога"

The skill walks you through the interview, generates prototypes, and helps you pick and refine.

## Example Output

```
prototypes/
├── BRIEF.md
├── gallery.html
├── hero-0-free.html
├── hero-A-warm-earthy.html
├── hero-B-dark-moody.html
├── hero-C-editorial.html
├── hero-D-playful-handcraft.html
└── hero-E-minimalist-zen.html
```

## Development

The `design-first-workspace/` directory contains iteration history and comparative evaluations used during skill development:
- `iteration-1/` through `iteration-6/` — skill evolution snapshots with eval outputs
- `eval-comparative/` — side-by-side comparison (with skill vs. without) across 3 scenarios

---

*Part of [my-claude-skills](../README.md)*
