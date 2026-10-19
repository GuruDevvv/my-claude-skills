# design-first

**Design before code.** The look is read from the topic, six different directions are drawn by an image model as mockups, three screens each, you pick one, and it is built as a live page over the mockup — desktop and phone each from their own mockup — measured for readability before you see it. It first asks two things: a site or a presentation, and for a site, one screen per direction or three. A presentation has its own mode: six directions × three test slides (title, a number, a structure), then every slide drawn from its own content and built into a 16:9 deck (PDF, Google Slides on request). The six directions share the thought and the feeling of each test slide but not the picture: before drawing, a table gives each direction a concrete image (a scene, a living person, words doing something, matter, a diagram-object, or nothing), its staging, its type and its volume, and a greyscale check of the six titles sends a look-alike back for one redraw.

## The Problem

When AI writes a UI you get one design, and usually a generic one. Adding rules about taste doesn't fix it: in blind tests two very different rule sets for HTML prototypes tied on taste and never produced a "wow". The ceiling is the coding model's own visual taste.

## The Solution

```
Context → Vibe → Words → 6 directions × 3 screens → Gallery → Pick/mix → Phone mockup → Plates → Build → Check → Show
```

1. **Always a real choice.** Six directions, each shown on three screens (the first screen, a content screen, an action screen), that differ in composition — three mood readings of the topic, a type-led poster, a texture/collage screen, a concept grown from the topic's own objects.
2. **The image model draws, the coding model builds.** Mockups drawn by an image model earned every "wow" in seven blind rounds; in the acceptance round the new path beat the old one on all three topics. The text is removed from the chosen mockup (a background "plate"), and the page is built with live text on top — judged the same as the mockup on desktop, and on the phone once the phone has its own vertical mockup.
3. **Measure before showing.** `scripts/check.mjs` checks every page at 390/1440/1920: sideways scroll, unreadable text (layers and opacity composited the way the browser paints them), content stuck invisible, fonts without Cyrillic, broken images, JS errors.

The evidence — protocols, keys and scores of the blind rounds — is summarised in `references/mockups.md` ("Why this path").

## What It Produces

- `prototypes/BRIEF.md` — vibe card, fixed words, the chosen direction.
- `prototypes/mockups/` — six directions of three desktop mockups each, the phone mockup, plates; a gallery page.
- `prototypes/<scope>.html` — the live page (desktop + phone), checked.

## Key Features

- Reads an **existing project's files first**, asks only the gaps, surfaces contradictions and bugs.
- **Vibe reading** — audience, genre codes from screenshots of live pages, 2–3 mood hypotheses, topic props, decoding verdict words («мрачно», «скучно», «всё сливается») (`references/vibe.md`, `concepts.md`).
- **Mockup generation, gallery, phone mockup, plates** — prompts and recipes (`references/mockups.md`). Works with any image tool; with none, falls back to HTML first screens (`frontend-aesthetics.md`).
- **Cyrillic safety gate** and font matching (`references/typography.md`).
- **Numeric check** with control pages that must fail and pass (`scripts/check.mjs`, `scripts/controls/`, `references/ui-verify.md`).
- **Feel pass** for the production build — 16 micro-detail rules (`references/feel-polish.md`).

## Install

```bash
cp -r design-first/ ~/.claude/skills/design-first/
```
Needs Node 22+ and Chrome/Edge for the check; an image generator (e.g. Codex CLI `image_gen`) for the main path.

## Usage

- "Make a landing page for my bakery"
- "Design a dashboard for analytics"
- "Сделай дизайн для сайта психолога" / "редизайн дашборда"

## Layout

```
design-first/
├── SKILL.md
├── assets/
│   ├── gallery-template.html  ← gallery page, filled through its data block
│   └── deck-template.html     ← 16:9 deck: slide frames, one-slide and no-text modes, print to PDF
├── scripts/
│   ├── check.mjs          ← numeric check (Node 22+, Chrome/Edge); --deck for slides
│   ├── codex_img.py       ← lean image calls through Codex (queue of 4, --replace to redraw)
│   ├── deck_export.py     ← slide shots, PDF, drawn | built sheet
│   └── controls/          ← pages that must fail / pass, EXPECTED.md
└── references/
    ├── deck.md            ← presentation mode: test slides, every slide drawn, deck, export
    ├── mockups.md         ← six directions × three screens, gallery, phone mockup, plates
    ├── vibe.md            ← reading the look from the topic
    ├── concepts.md        ← concept from the topic's own objects
    ├── typography.md      ← fonts + Cyrillic gate
    ├── ui-verify.md       ← measuring with numbers, manual probes
    ├── motion.md          ← animation recipes
    ├── interaction-patterns.md
    ├── feel-polish.md     ← 16 micro-detail rules for production code
    └── frontend-aesthetics.md  ← fallback when no image generator exists
```

## Credits

`references/ui-verify.md` and the contrast/overflow/glyph probes in `scripts/check.mjs` grew out of a `ui-verify` skill shared by a design-first user in September 2026.

The Feel pass (`references/feel-polish.md`) distills principles from **["Details that make interfaces feel better"](https://jakub.kr/writing/details-that-make-interfaces-feel-better)** by **Jakub Krehel** — his standalone skill is [`jakubkrehel/make-interfaces-feel-better`](https://github.com/jakubkrehel/make-interfaces-feel-better) (MIT).

---

🇷🇺 Дизайн до кода: вид страницы читается из темы, модель картинок рисует шесть разных первых экранов, вы выбираете один, и по нему верстается живая страница — для компьютера и телефона по своим макетам, с проверкой читаемости цифрами. В слепых сравнениях с прежней версией выиграла три темы из трёх.
