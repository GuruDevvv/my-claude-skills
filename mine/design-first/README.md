# design-first

**Structured design exploration before coding.** Read the look from the topic's vibe, generate diverse HTML prototypes inside it, measure them with numbers, compare side-by-side, pick the best, then build.

## The Problem

When AI generates a UI you get one design, and usually a generic one: Inter, purple gradients, glassmorphism, centered hero — "AI slop". You tweak it endlessly and never see the distinctive alternatives you're missing.

## The Solution

```
Context (+ASK) → Read the vibe → Brief → Prototypes → Gates → Measure → Gallery → Pick & Mix → Build → Feel pass
```

Two principles:
1. **Diverge, don't commit.** Round 1: 4 light first screens (2 genre + 2 concept), compared in a gallery; round 2 develops the picked one.
2. **Read the vibe, then be excellent inside it.** Most people have no reference and can't describe the look they want — but recognise it instantly. The skill reads it from the topic: the audience, the genre's own visual codes, the feeling, the topic's objects. Next to genre versions go bold concepts grown from the topic's own objects (a till receipt for a money course, a clock face for a therapist's day) — not metaphors imported from outside the niche, which made pages feel alien to their audience.
3. **Measure before showing.** `scripts/check.mjs` checks every prototype at 390/1440/1920: sideways scroll, unreadable text, content stuck invisible, fonts without Cyrillic, broken images, JS errors.

## What It Generates

- **Variant 0 (Free)** — AI's *riskiest* bet (a bold idea, not the averaged safe shot), generated first.
- **Variants A–E** — structured prototypes, each a different take on the vibe, varying on structural axes (nav, layout, density, interaction, hierarchy) — verified by a grayscale test.
- **Gallery page** — side-by-side comparison with previews and direct links.

## Key Features

- Reads an **existing project's files first**, then asks only the gaps — and **surfaces contradictions/bugs** (e.g. spec says dark, code is light; a body font with no Cyrillic).
- **Anti-AI-slop directive** applied to every prototype (`references/frontend-aesthetics.md`).
- **Cyrillic safety gate** — verified distinctive RU font pool + a one-line checker; RU vs Latin font branching (`references/typography.md`).
- **Autonomous image sourcing** — works with no account/key: a generator if present → Openverse (free) → Picsum → none; downloads locally; self-sufficient if images fail; knows when *not* to use images (`references/imagery.md`).
- **Visible, dependency-free motion** matched to product type — atmospheric vs functional, incl. advanced scroll-driven/cursor-reactive recipes (`references/motion.md`).
- **Real imagery is mandatory** (≥ half the prototypes) and sourced centrally before generation, so prototypes never ship image-less.
- **Navigation-aware + non-standard elements** — sticky TOC/scroll-spy for content-heavy pages; one memorable unconventional interaction per set (`references/interaction-patterns.md`).
- **Vibe reading** — audience, genre codes, feeling → visual properties, decoding the client's verdict words («мрачно», «скучно», «всё сливается»), 3–4 topic interactives per landing (`references/vibe.md`).
- **Numeric check before the gallery** — zero-dependency headless Chrome script + manual probes for complaints (`references/ui-verify.md`, `scripts/check.mjs`).
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
├── scripts/check.mjs            ← numeric check (Node 22+, Chrome/Edge)
└── references/
    ├── frontend-aesthetics.md   ← anti-slop directive
    ├── typography.md            ← fonts + Cyrillic gate
    ├── imagery.md               ← image sourcing cascade
    ├── motion.md                ← animation recipes (+ advanced)
    ├── vibe.md                  ← reading the look from the topic
    ├── ui-verify.md             ← measuring with numbers
    ├── interaction-patterns.md  ← navigation + non-standard elements
    └── feel-polish.md           ← 16 micro-detail rules for the final build

prototypes/                      ← generated per project
├── BRIEF.md
├── gallery.html
├── hero-0-free.html
├── hero-A-[name].html  …  hero-E-[name].html
└── assets/                      ← downloaded images (standalone)
```

## Credits

`references/ui-verify.md` and the contrast/overflow/glyph probes in `scripts/check.mjs` grew out of a `ui-verify` skill shared by a design-first user in September 2026.


The Feel pass (`references/feel-polish.md`) distills principles from **["Details that make interfaces feel better"](https://jakub.kr/writing/details-that-make-interfaces-feel-better)** by **Jakub Krehel** — his standalone skill is [`jakubkrehel/make-interfaces-feel-better`](https://github.com/jakubkrehel/make-interfaces-feel-better) (MIT). For a deeper, code-heavy treatment, install his skill directly.

---

*Part of [my-claude-skills](../README.md)*
