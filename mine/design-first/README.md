# design-first

**Structured, art-directed design exploration before coding.** Generate diverse HTML prototypes — each led by a bold creative concept — compare them side-by-side, pick the best, then build.

## The Problem

When AI generates a UI you get one design, and usually a generic one: Inter, purple gradients, glassmorphism, centered hero — "AI slop". You tweak it endlessly and never see the distinctive alternatives you're missing.

## The Solution

```
Context (+ASK) → References → Brief → Prototypes → WOW-gate → Gallery → Pick & Mix → Build → Feel pass
```

Two principles:
1. **Diverge, don't commit.** 4–6 genuinely different directions as standalone HTML, compared in a gallery.
2. **Concept-first, not template.** Each prototype is led by one bold idea ("a 1920s Berlin telegram", "a season command-board"); color, type, layout, motion, and imagery are *derived from the concept* — not picked from a safe default. This is what turns "6 skins of the same page" into 6 real designs.

## What It Generates

- **Variant 0 (Free)** — AI's *riskiest* bet (a bold idea, not the averaged safe shot), generated first.
- **Variants A–E** — structured prototypes, each a different **concept**, varying on structural axes (nav, layout, density, interaction, hierarchy) — verified by a grayscale test.
- **Gallery page** — side-by-side comparison with previews and direct links.

## Key Features

- Reads an **existing project's files first**, then asks only the gaps — and **surfaces contradictions/bugs** (e.g. spec says dark, code is light; a body font with no Cyrillic).
- **Anti-AI-slop directive** applied to every prototype (`references/frontend-aesthetics.md`).
- **Cyrillic safety gate** — verified distinctive RU font pool + a one-line checker; RU vs Latin font branching (`references/typography.md`).
- **Autonomous image sourcing** — works with no account/key: a generator if present → Openverse (free) → Picsum → none; downloads locally; self-sufficient if images fail; knows when *not* to use images (`references/imagery.md`).
- **Visible, dependency-free motion** matched to product type — atmospheric vs functional, incl. advanced scroll-driven/cursor-reactive recipes (`references/motion.md`).
- **Real imagery is mandatory** (≥ half the prototypes) and sourced centrally before generation, so prototypes never ship image-less.
- **Navigation-aware + non-standard elements** — sticky TOC/scroll-spy for content-heavy pages; one memorable unconventional interaction per set (`references/interaction-patterns.md`).
- **Concept-derivation method** with worked examples (`references/art-direction.md`).
- **WOW-gate** — creative quality gates, not just technical checks.
- **Feel pass** — after the final winner is built into real code, a default polish step applies 16 micro-detail rules (concentric radius, optical alignment, interruptible animation, tabular numbers, image outlines, scale-on-press…) and reports Before/After (`references/feel-polish.md`). Skippable with "skip polish".
- Mobile-first with desktop breakpoints; parallel prototype generation via subagents.

## Install

```bash
cp -r design-first/ ~/.claude/skills/design-first/
```
The skill is a folder (`SKILL.md` + `references/`); copy the directory. Reference files load on demand, so the core stays light in context.

## Usage

Describe what you need — the skill triggers on design requests:
- "Make a landing page for my bakery"
- "Design a dashboard for analytics"
- "Сделай дизайн для сайта психолога" / "редизайн дашборда"

## Example Output

```
design-first/
├── SKILL.md
└── references/
    ├── frontend-aesthetics.md   ← anti-slop directive
    ├── typography.md            ← fonts + Cyrillic gate
    ├── imagery.md               ← image sourcing cascade
    ├── motion.md                ← animation recipes (+ advanced)
    ├── art-direction.md         ← concept method + examples
    ├── interaction-patterns.md  ← navigation + non-standard elements
    └── feel-polish.md           ← 16 micro-detail rules for the final build

prototypes/                      ← generated per project
├── BRIEF.md
├── gallery.html
├── hero-0-free.html
├── hero-A-[concept].html  …  hero-E-[concept].html
└── assets/                      ← downloaded images (standalone)
```

## Credits

The Feel pass (`references/feel-polish.md`) distills principles from **["Details that make interfaces feel better"](https://jakub.kr/writing/details-that-make-interfaces-feel-better)** by **Jakub Krehel** — his standalone skill is [`jakubkrehel/make-interfaces-feel-better`](https://github.com/jakubkrehel/make-interfaces-feel-better) (MIT). For a deeper, code-heavy treatment, install his skill directly.

---

*Part of [my-claude-skills](../README.md)*
