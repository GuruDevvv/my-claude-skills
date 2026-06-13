---
name: design-first
description: Generate diverse, art-directed HTML design prototypes before coding — concept-led, not generic. Interview → references → parallel prototypes → gallery → pick → build. Use when: "сделай дизайн", "подготовь макет", "давай займёмся дизайном", "нарисуй страницу", "редизайн", "make a design", "design this", "prepare design", "how should this look", "visual direction", "prototypes", "варианты дизайна". Scope: landing pages, dashboards, portfolios, forms, apps, components — any visual/UI work. Do NOT use for: code review, debugging, backend logic, data processing, or non-visual tasks.
---

# Design First

A structured process for exploring visual direction before writing production code. Built for people who aren't designers but need professional, **distinctive** results.

Two ideas drive everything:

1. **Don't commit to one design.** Generate diverse options, compare, pick, then build. Eliminates the #1 vibe-coding trap — getting stuck with the first thing that came out.
2. **Lead with a creative concept, not a template.** The reason AI prototypes feel samey ("6 skins of the same page") is that they optimize for *technically correct* instead of *memorable*. Each prototype here is led by one bold visual concept, and color/type/layout/motion/imagery are **derived from that concept** — not picked from a safe default palette.

> The failure mode this skill fights: a prototype that passes every technical checklist and still makes nobody feel anything. "Adequate" is the enemy.

---

## How it works

```
Context → References → Brief → Prototypes → WOW-gate → Gallery → Pick → Refine & Build
 (gather    (in/out of  (concept   (parallel,   (creative   (compare)         (merge)
  + ASK)     category)   per proto)  art-directed) quality)
```

**Reference files** (loaded on demand — read the one you need, don't inline everything):
- `references/frontend-aesthetics.md` — the anti-"AI-slop" directive. **Read before generating any prototype.**
- `references/typography.md` — distinctive font pools, the **Cyrillic safety gate**, weight/size rules.
- `references/imagery.md` — how to source/generate real images (autonomous cascade), and when NOT to.
- `references/motion.md` — dependency-free animation recipes (the visible kind).
- `references/art-direction.md` — how to invent a concept per prototype, with worked examples.
- `references/interaction-patterns.md` — navigation patterns + non-standard, memorable elements.

---

## Step 1 — Context (mandatory: gather, then ASK)

Before any visuals, understand what you're designing. **Two sources, in order:**

### 1a. If this is an existing project — gather context from the files FIRST

Read what the project already tells you before asking the user anything. Look for: `PRODUCT.md`, `vision.md`, `README.md`, `CLAUDE.md`, `HANDOFF.md`, `docs/`, and **existing UI** (`globals.css`, components, live site, any `.html`). Extract: what it is, audience, stated emotion/tone, tech stack, language, existing brand (colors/fonts), and any UI requirements.

While reading, actively hunt for **gaps, contradictions, and doubts** — these are what you ask about:
- **Contradiction:** spec says one thing, the code/live site does another (e.g. spec wants a dark calm theme, the live CSS is a light purple-gradient SaaS). Surface it.
- **Bug/risk:** e.g. a body font with no Cyrillic on a Russian site (text silently falls back). Surface it.
- **Genuine ambiguity:** which screen/surface to design, light vs dark, how bold to go.

### 1b. Ask only what's missing or doubtful — never interrogate

Don't re-ask what the files already answered. Ask the gaps. Core questions (adapt phrasing):

1. **What surface?** (landing, dashboard, form, app screen, component…)
2. **Who uses it, on what device?** (mobile-first or desktop?)
3. **What should the user FEEL?** (trust, calm, urgency, premium, playful…)
4. **What should the user DO?** (buy, sign up, register, explore…)
5. **Existing brand/style?** (colors, fonts, logo, a site they like)
6. **How bold can the design be?** — from "консервативно, это серьёзно" ↔ "удиви меня, не бойся". This calibrates risk. (New, important: a non-designer often *says* "minimal/safe" meaning "trustworthy", not "visually plain". Probe that.)
7. **Anti-references?** (what to avoid — "not corporate", "not generic SaaS")
8. **Language** of the UI? (drives the **font gate** — see typography.md)

**Why surface contradictions instead of silently choosing:** the user knows things the files don't, and a wrong assumption wastes 6 prototypes. A 30-second question beats a confident mistake.

---

## Step 2 — Reference Analysis

### If the user provided references (images, URLs, screenshots)
Extract a **Design DNA profile** for each: Mood · Color strategy · Typography · Layout · **Signature moves** (what makes it unique — grain? bold type? glass? gradients?) · Animation vibe. Summarize back in 2-3 sentences to build shared vocabulary.

### Always — look OUTSIDE the product category
The strongest source of surprise is not other websites in the same niche. Pull inspiration from **art movements, editorial/print, fashion, packaging, architecture, film**. "A telegram from 1920s Berlin", "wabi-sabi imperfection", "a departures board you can't miss" — these are concept seeds the average SaaS page never reaches for.

### If no references
Ask for 1-2 examples they like (even from a different industry). If none — derive direction from the emotional answers (Step 1) and maximize spread on the structural + concept axes.

---

## Step 2.5 — Design Brief (checkpoint before generating)

Persist decisions to `prototypes/BRIEF.md` so a long session can't lose them and the user gets a correction point before 6 prototypes exist.

```markdown
# Design Brief: [Project]

## Context
- What / Audience / Emotion / Action / Tech / Language
- Boldness: [conservative … surprise-me]

## Brand & Style
- Existing assets: [colors, fonts — or "none"]
- References (in & out of category): [DNA one-liners]
- Anti-references: [avoid]
- **The boring version:** [what the obvious/generic take looks like] → AVOID it

## Content
- Headline / Subheadline / CTA: [exact or "write plausible"]
- Imagery: [tier from imagery.md — gen / Openverse / Picsum / none]

## Prototype Plan
| # | Concept (one bold line, concept-first) | Structural axes | Type | Color from concept |
|---|----------------------------------------|-----------------|------|--------------------|
| 0 (free) | AI's riskiest bet — see Step 3 | — | — | — |
| A | e.g. "telegram from 1920s Berlin" | nav + layout | display + body | derived |
| B | … | … | … | … |
```

**Show the brief and ask:** "This is what I'll build from. Anything to change before I generate?" Proceed only on an affirmative.

> **Interactive vs autonomous.** This skill is interactive by default — Steps 1 and 2.5 expect a human to answer and confirm. If you're running **autonomously / headless** (no human to ask), don't block: extract every answer you can from the project files, **write the gaps/assumptions you would have asked into `BRIEF.md`**, and proceed. (Sub-agents spawned for parallel generation in Step 3h are already given the finished brief and must NOT re-ask.)

---

## Step 3 — Generate Prototypes

### 3.0 — Read `references/frontend-aesthetics.md` now
It contains the anti-slop directive to apply to **every** prototype. This is the single highest-impact rule in the skill.

### What & how many
- **Default: 6 (1 free + 5 structured). Minimum: 4 (1 free + 3 structured).** Fewer only for simple components.
- **Scope:** full page → generate the Hero, **but at least 1-2 prototypes show a 2-3 section scroll narrative** (hero-only kills wow — the magic is in how sections flow). Component → in context. Dashboard → one key screen with real hierarchy.
- Each prototype is a **standalone HTML file**: opens in a browser, only Google Fonts CDN + local assets, inline CSS/JS, no build, no CDN libraries.

### 3a. Art Direction layer (the core of v3)
Before writing a prototype, give it **one bold concept in a single line** (concept-first, not constraint-first). Not "warm earthy tones" — that's a color note. Rather "a telegram from 1920s Berlin", "wabi-sabi imperfection", "командное табло дедлайнов". From the concept, **derive** color, type, layout, motion, imagery. See `references/art-direction.md` for how to invent these and worked examples.

The structured prototypes must differ **structurally**, not just visually. Vary ≥2 structural axes (navigation, layout architecture, information density, interaction model, content hierarchy) AND ≥1 visual axis. **Grayscale test:** strip all color → prototypes must STILL look different. If they don't, the diversity is fake.

### 3b. Free variant (variant 0) — generated FIRST, alone
Don't prompt it to be "polished and distinctive" (that yields the averaged, safe default). Prompt it to **take a risk**:
> "Decide on one visual idea you'd be *surprised* to see in this product category, and build the entire prototype around it. Use all the brief context. Make a bold bet, not a safe shot."
Generate it before the structured variants so it isn't contaminated by them. File: `[scope]-0-free.html`.

### 3c. Typography → read `references/typography.md`
Hard rules: **never** Inter/Roboto/Arial/system/Open Sans/Lato. Use distinctive fonts with weight extremes (200 vs 800, not 400 vs 600) and size jumps of 3x+. **Cyrillic gate:** for Russian/Cyrillic content, every font MUST be verified to support Cyrillic — many distinctive American fonts (Fraunces, Clash, Bricolage, DM Sans…) don't, and text silently breaks. The reference file has the verified RU-safe pool and a one-line checker command.

### 3d. Color from concept, NOT from a catalog
Derive the palette from the concept/mood ("the colour of fog on a Baltic beach at dawn"), not from a SaaS palette generator — those converge on generic. One dominant color + a sharp accent beats a timid even palette. (`ui-ux-pro-max` may be used as an *optional reference* to widen your style vocabulary, but it is not the foundation and its catalog skews generic-SaaS.)

### 3e. Imagery → read `references/imagery.md`
**Real imagery is MANDATORY, not optional — unless the surface is a pure data dashboard/dense tool.** The #1 observed failure is prototypes shipping with *zero* images because fetching feels like friction and "decide if images belong" became an easy out. Don't let that happen:
- **≥ half the prototypes (≥3 of 6) must use real images** — hero, full-bleed background, or section imagery. Only a genuine data dashboard is exempt (and even there, consider SVG diagrams / generated patterns / data-viz instead of nothing).
- **Source images CENTRALLY before spawning prototype agents** (see 3h): fetch/generate into `prototypes/assets/` in the main flow and pass the **local paths** to each agent — so no sub-agent skips images for lack of tools or effort.
- Autonomous cascade (no account/key): **image-gen tool if present → Openverse (free, no key) → Picsum → none**. Download to local `assets/`.
- **Self-sufficiency rule:** a prototype must look finished even if an image fails — concept-palette background behind every image, never an empty placeholder panel.
- **When a photo truly doesn't fit** (dashboards): use non-photographic imagery — SVG diagrams, generated/gradient patterns, textures, data-viz. "No stock photo" ≠ "no visual texture".

### 3f. Motion → read `references/motion.md`
Static pages feel dead next to animated ones, and **the motion must be visible** (a 6-second-cycle Ken Burns reads as "nothing happening"). Match motion to product type: atmospheric (fog drift, breathing glow, floating motes, parallax) for emotional/editorial; functional (count-up numbers, urgency pulse, staggered reveal) for tools/dashboards. Dependency-free only; always include a `prefers-reduced-motion` path.
- **Raise the bar (observed gap: too little motion):** **most prototypes (≥4 of 6) must have clearly visible motion**, and **at least 1-2 must use *sophisticated* motion** — scroll-driven sequences, sticky-stack reveals, multi-layer parallax, or cursor-reactive effects (see motion.md "Advanced"). At most 1-2 may be static-but-elegant.

### 3g. Layout & responsive (carry-over rules that still matter)
- **Mobile-first.** Base CSS = phone; `@media (min-width:768px)` and `(min-width:1440px)`.
- **Don't waste desktop space** (the #1 AI visual flaw): heading 56-80px at 1440px+, body max-width ≥500px, hero wrapper 1100-1400px for multi-column. At least 2 of 6 use a non-centered layout (split/editorial/asymmetric). Atmospheric ≠ empty — content must anchor and fill.
- Real content, never lorem ipsum. Mark placeholder text in `<!-- PLACEHOLDER -->` comments.

### 3i. Navigation & non-standard elements → read `references/interaction-patterns.md`
- **Understand navigation, don't ignore it.** If the content is list-heavy or has multiple sections (memo, docs, multi-section page, catalog), **≥1-2 prototypes must include real navigation** — a sticky table-of-contents / scroll-spy sidebar, sub-nav, or anchor rail — so the page is actually navigable, not just a long scroll. Vary the nav pattern across prototypes (it's a structural axis).
- **Reach for non-standard elements.** **≥1 prototype should feature one unconventional, memorable interaction/element** — bento grid, horizontal scroll-snap section, sticky-stacking cards, before/after slider, draggable cards, scroll-spy TOC, custom cursor, hover-reveal. The reference file has a dependency-free palette.

### 3h. Generation order & parallelization
**First, in the main flow: source imagery centrally** (3e) into `prototypes/assets/` so every agent gets working local paths. Then generate variant 0 alone. Then generate structured variants **in parallel** — one Agent per prototype, each given the full `BRIEF.md`, its concept row, the local asset paths, and the relevant reference files. If parallel isn't available, generate sequentially and **re-read BRIEF.md before each** to avoid drift toward repetition.

---

## Step 3.5 — WOW-gate (before saving each prototype)

The old checklist was 13 technical items and 0 creative ones — a forgettable prototype passed 13/13. Keep the technical checks (mobile-first, two breakpoints, Cyrillic verified, real content, perf, `prefers-reduced-motion`, standalone) **and** add these creative gates:

- [ ] **One bold concept** — can you name this prototype's idea in one line?
- [ ] **Stranger test** — someone seeing only this, no context, feels *something* (curiosity, desire, calm, awe)?
- [ ] **Novelty** — is there one move you haven't seen a hundred times?
- [ ] **Grayscale test** — different from the others with color removed?
- [ ] **Designed vs generated** — does it read as crafted, or as AI-default?
- [ ] **Image self-sufficiency** — looks finished even if images fail?
- [ ] **Motion is visible** — would a person notice movement in the first 3 seconds?

If the honest answer to a creative gate is "no", the concept is too weak — change it, don't just polish.

---

## Step 4 — Present & Evaluate

Create `gallery.html` (variant 0 shown first as "AI's Best Shot", structured variants after; dark neutral bg; "Open" link per card + iframes with relative paths; mobile/desktop note).

**Optional, recommended — real screenshots:** if a browser-screenshot tool is available (Playwright MCP, or headless Edge/Chrome `--screenshot`), capture each prototype to PNG for a reliable visual gallery (file:// iframes can be blocked). Note: full-bleed `100svh` heroes screenshot only the first viewport; capture sections separately if needed.

Give the user a simple frame:
> - Does it FEEL right for my audience? (not "do I like it" — "would my users trust/want this?")
> - Is the key action obvious?
> - Which one could you imagine as a full-page ad in a design magazine?
> - What grabs you / what repels you?

Don't ask "which is best?" — ask **"which 1-2 are closest, and what would you change?"** Then ask the **mixing question**: "Anything to borrow from the others — a font, color, motion, layout idea?" (How non-designers reach a unique result.)

---

## Step 5 — Refine & Build

1. Start from the chosen base; list what's borrowed explicitly.
2. Apply changes one category at a time (type → color → layout → effects); visual conflicts appear when you merge all at once.
3. Save as `prototypes/[scope]-FINAL-[name].html`; iterate in place (don't spawn v2, v3…).
4. On approval, add a **"Final Direction"** section to `BRIEF.md` (locked palette, fonts, layout) as the source of truth for the full build.

---

## Quick reference

| Situation | What to do |
|-----------|-----------|
| "make it look good" | Start Step 1 — they don't know what they want yet |
| Existing project | Read its files first; surface contradictions/bugs; ask only the gaps |
| Russian/Cyrillic UI | Verify every font for Cyrillic (typography.md) — this is non-negotiable |
| Data dashboard / dense tool | Skip photos; wow via hierarchy + type + functional motion |
| "minimal / safe / calm" | Probe: does it mean *plain*, or *trustworthy*? Calm can still be atmospheric |
| Wants to skip prototypes | "15 min of prototypes saves hours of rework" — hold the line at 4 minimum |
| Can't choose | Ask the eval questions; if stuck, combine top 2 |
| Time pressure | 4 instead of 6, skip anti-references question — never skip Step 1 |
