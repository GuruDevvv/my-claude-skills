---
name: design-first
description: Generate diverse HTML design prototypes before coding — the look is read from the topic's vibe and audience, not invented, and every prototype is measured for readability before the user sees it. Interview → read the vibe → parallel prototypes → numeric check → gallery → pick → build. Use when: "сделай дизайн", "подготовь макет", "давай займёмся дизайном", "нарисуй страницу", "редизайн", "make a design", "design this", "prepare design", "how should this look", "visual direction", "prototypes", "варианты дизайна". Scope: landing pages, dashboards, portfolios, forms, apps, components — any visual/UI work. Do NOT use for: code review, debugging, backend logic, data processing, or non-visual tasks.
---

# Design First

A structured process for exploring visual direction before writing production code. Built for people who aren't designers but need professional, **distinctive** results.

Two ideas drive everything:

1. **Don't commit to one design.** Generate diverse options, compare, pick, then build. Eliminates the #1 vibe-coding trap — getting stuck with the first thing that came out.
2. **Read the vibe, then be excellent inside it.** The user usually has no reference and can't describe the picture in their head — but recognises it instantly. That picture is mostly the *genre's own visual language* for this audience plus the feeling of the topic. So the look is **read from the topic** (audience, genre codes, emotional core, topic props), variants are different takes on that one vibe, and distinctiveness is one deliberate move on top — not a metaphor imported from far outside the niche.
3. **Measure before showing.** Unreadable text, empty screens and sideways scroll are invisible in code and obvious to the user. Every prototype passes a numeric check before the gallery.

> Two failure modes this skill fights: a prototype that passes every checklist and makes nobody feel anything — and a prototype so "original" that the audience doesn't recognise it as meant for them.

---

## How it works

```
Context → Read the vibe → Brief → Prototypes → Gates → Measure → Gallery → Pick → Refine & Build → Feel pass
 (gather    (audience, genre, (vibe card  (parallel,  (quality) (numbers,  (compare)      (merge)         (polish the
  + ASK)     feeling, props)   + plan)    in-vibe)              fix FAILs)                                 real build)
```

**Reference files** (loaded on demand — read the one you need, don't inline everything):
- `references/frontend-aesthetics.md` — the anti-"AI-slop" directive. **Read before generating any prototype.**
- `references/typography.md` — distinctive font pools, the **Cyrillic safety gate**, weight/size rules.
- `references/imagery.md` — how to source/generate real images (autonomous cascade), and when NOT to.
- `references/motion.md` — dependency-free animation recipes (the visible kind).
- `references/vibe.md` — **how to read the look from the topic**: audience, genre codes, feeling → visual properties, decoding the user's verdict words, topic interactives. Read before Step 2.
- `references/concepts.md` — **concept variants**: a bold metaphor from the topic's own objects that also does a job on the page (receipt, clock face, dispatcher's board). Read before Step 3.
- `references/ui-verify.md` — the numeric check (`scripts/check.mjs`) and manual probes; read at Step 3.6 and whenever the user complains about how something looks.
- `references/interaction-patterns.md` — navigation patterns + non-standard, memorable elements.
- `references/feel-polish.md` — the 16 micro-detail rules for the **final build** (Step 5), not prototypes.

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
5. **Existing brand/style?** (colors, fonts, logo). If they *volunteer* a site or picture they like — gold, use it. **Never require references** and never block on them: most people have none, and reading the vibe is your job (Step 2).
6. **How bold can the design be?** — from "консервативно, это серьёзно" ↔ "удиви меня, не бойся". This calibrates risk. (New, important: a non-designer often *says* "minimal/safe" meaning "trustworthy", not "visually plain". Probe that.)
7. **Anti-references?** (what to avoid). Caution: users often name the genre's own codes as an anti-reference and then pick exactly them. Note it, don't obey it blindly — see vibe.md.
8. **Language** of the UI? (drives the **font gate** — see typography.md)

Keep it short: ask only what the files and the topic can't answer. Feeling, boldness and anti-references are **optional** — if the user shrugs, read them from the topic yourself (Step 2) and show your reading in the vibe card instead of asking again.

**Why surface contradictions instead of silently choosing:** the user knows things the files don't, and a wrong assumption wastes a whole round. A 30-second question beats a confident mistake.

---

## Step 2 — Read the vibe → read `references/vibe.md`

Do the six reads and write them into the brief:
1. **Audience in one concrete line** — who, situation, the moment and the device they meet the page on.
2. **Genre codes** — **look at screenshots** of 3–5 live pages of the same offer for the same audience (`scripts/check.mjs <url> --shots` makes them); a text fetch doesn't show light or composition. Note light, imagery, temperature, density, signature blocks and effects, keeping *seen* apart from *assumed*. These are the **baseline**, not something to flee.
3. **2–3 mood hypotheses → visual properties** — one reading of the topic is a single point of failure; name several honest moods and translate each into light, colour temperature, human presence, density, motion (table in vibe.md).
4. **Topic props** — 3–4 interactive pieces made from the topic's own objects and actions (landings); usability mechanics (tools).
5. **Whose palette** — make sure the palette isn't already bound to another author/product in this project.
6. **The vibe card** — five plain lines that go into the brief.

If the user supplied a reference, it overrides reads 2–3. If they didn't — never ask them to go find one.

---

## Step 2.5 — Design Brief (checkpoint before generating)

Persist decisions to `prototypes/BRIEF.md` so a long session can't lose them and the user gets a record of what was decided.

```markdown
# Design Brief: [Project]

## Context
- What / Audience / Emotion / Action / Tech / Language
- Boldness: [conservative … surprise-me]

## Brand & Style
- Existing assets: [colors, fonts — or "none"]
- Anti-references: [avoid]

## Vibe card (vibe.md, read 6)
- Кто смотрит: …
- Жанр и его коды: …
- Что должен почувствовать → свойства: …
- Фишки из темы: …
- Один смелый ход поверх жанра: …

## Content
- Headline / Subheadline / CTA: [exact or "write plausible"]
- Imagery: [tier from imagery.md — gen / Openverse / Picsum / none]

## Prototype Plan
| # | Direction (one plain line, inside the vibe) | Register | Layout skeleton | Palette | Leading topic interactive |
|---|---------------------------------------------|----------|-----------------|---------|---------------------------|
| 0 (free) | AI's boldest bet for *this audience* — see 3b | — | — | — | — |
| A | genre: "done excellently, warm back-lit photo" | dark cinematic | full-bleed + stacked | warm amber | search with suggestions |
| B | genre: … | light editorial | split | … | … |
| C | concept: "a till receipt of an ordinary month" | receipt | single column | paper + ink | spending lines that print |
```

**Show the vibe card in plain words and go straight on** — don't wait for approval of a text the user can only judge by eye: «Вот как я прочитал тему, собираю четыре первых экрана. Если где-то мимо — скажи, поправлю по ходу.» The real checkpoint is the round-1 gallery. (Wait only if the project files contradict each other in a way that changes what to build.)

> **Interactive vs autonomous.** This skill is interactive by default — Steps 1 and 2.5 expect a human to answer and confirm. If you're running **autonomously / headless** (no human to ask), don't block: extract every answer you can from the project files, **write the gaps/assumptions you would have asked into `BRIEF.md`**, and proceed. (Sub-agents spawned for parallel generation in Step 3h are already given the finished brief and must NOT re-ask.)

---

## Step 3 — Generate Prototypes

### 3.0 — Read `references/frontend-aesthetics.md` now
It contains the anti-slop directive to apply to **every** prototype. This is the single highest-impact rule in the skill.

### What & how many — a light first round, then depth
- **Round 1: 4 light variants of equal scope — 2 genre + 2 concept.** Two "genre done excellently" (vibe.md) and two **concept variants** (concepts.md: a metaphor from the topic's own world that does a job; variant 0 is one of them, the boldest). Together they cover all mood hypotheses. Blind test 25.09: genre-only sets were reliable but lost to sets with bold topic-born concepts, especially on work screens. Page → **first screen + the next section**, so the flow is visible; tool → one key screen with real hierarchy; component → in context. Each shows **one** topic interactive working. Cheap and fast: the user recognises their picture with their eyes, not from the brief.
- **Round 2: develop the 1–2 picked** into a fuller page (3–4 sections, the full set of topic interactives, all breakpoints). This is where depth goes — not into variants nobody chose.
- More than 4 only if the user asks; fewer only for simple components.
- Each prototype is a **standalone HTML file**: opens in a browser, only Google Fonts CDN + local assets, inline CSS/JS, no build, no CDN libraries.

### 3a. Variants = different takes on one vibe
Each prototype gets **one plain line of direction**: which mood hypothesis it carries and how ("hypothesis 1, genre done excellently, light editorial register", "hypothesis 2 + embers over the hero"). Round 1: 2 genre variants + 2 concept variants (variant 0 = the boldest concept), every mood hypothesis covered. Genre variants take colour, type, layout and motion from the vibe card; concept variants derive them from their concept (concepts.md) within the audience's tone. For tools and dashboards concepts are welcome **only if they work** — a clock face that shows the day, a board that is the queue; a wheel or chart used as ornament is «непрактичное творчество».

The variants must differ **structurally**, not just visually: vary ≥2 structural axes (navigation, layout skeleton, density, interaction model, hierarchy) AND ≥1 visual axis. **Grayscale test:** strip all colour → they must STILL look different. Different metaphors on the same skeleton are the same prototype.

### 3b. Free variant (variant 0) — generated FIRST, alone
Don't prompt it to be "polished and distinctive" (that yields the averaged, safe default). Prompt it to **take a risk**:
> "Make the boldest version that this exact audience would still instantly recognise as meant for them. Use the vibe card. A bold bet, not a safe shot — and not an alien one."
Generate it before the structured variants so it isn't contaminated by them. File: `[scope]-0-free.html`.

### 3c. Typography → read `references/typography.md`
Hard rules: **never** Inter/Roboto/Arial/system/Open Sans/Lato. Use distinctive fonts with weight extremes (200 vs 800, not 400 vs 600) and size jumps of 3x+. **Cyrillic gate:** for Russian/Cyrillic content, every font MUST be verified to support Cyrillic — many distinctive American fonts (Fraunces, Clash, Bricolage, DM Sans…) don't, and text silently breaks. The reference file has the verified RU-safe pool and a one-line checker command.

### 3d. Color from the vibe, NOT from a catalog
Derive the palette from the vibe card (light, temperature, feeling), not from a SaaS palette generator — those converge on generic. **Palettes must differ across prototypes** — six shades of one palette is no choice at all; brand consistency comes at the final, not here. Check the palette isn't already bound to another author/product (vibe.md, read 5). One dominant color + a sharp accent beats a timid even palette. (`ui-ux-pro-max` may be used as an *optional reference* to widen your style vocabulary, but it is not the foundation and its catalog skews generic-SaaS.)

### 3e. Imagery → read `references/imagery.md`
**Real imagery is MANDATORY, not optional — unless the surface is a pure data dashboard/dense tool.** The #1 observed failure is prototypes shipping with *zero* images because fetching feels like friction and "decide if images belong" became an easy out. Don't let that happen:
- **≥ half the prototypes must use real images** — hero, full-bleed background, or section imagery. Only a genuine data dashboard is exempt (and even there, consider SVG diagrams / generated patterns / data-viz instead of nothing).
- **Source images CENTRALLY before spawning prototype agents** (see 3h): fetch/generate into `prototypes/assets/` in the main flow and pass the **local paths** to each agent — so no sub-agent skips images for lack of tools or effort.
- Autonomous cascade (no account/key): **image-gen tool if present → Openverse (free, no key) → Picsum → none**. Download to local `assets/`.
- **An image must fit the mood, not fill a quota.** Check light, pose, cropping and free space for text against the vibe card; a random Picsum photo that fights the mood does NOT count as "has imagery" — use a generated image, a well-chosen Openverse one, or honest non-photo texture.
- **Self-sufficiency rule:** a prototype must look finished even if an image fails — palette-coloured background behind every image, never an empty placeholder panel.
- **When a photo truly doesn't fit** (dashboards): use non-photographic imagery — SVG diagrams, generated/gradient patterns, textures, data-viz. "No stock photo" ≠ "no visual texture".

### 3f. Motion → read `references/motion.md`
Static pages feel dead next to animated ones, and **the motion must be visible** (a 6-second-cycle Ken Burns reads as "nothing happening"). Tie motion to the topic and the feeling (vibe card), matched to product type: atmospheric (fog drift, breathing glow, floating motes, parallax) for emotional/editorial; functional (count-up numbers, urgency pulse, staggered reveal) for tools/dashboards. Dependency-free only; always include a `prefers-reduced-motion` path.
- **Motion serves the mood.** Most variants should have motion a person notices in the first seconds; sophisticated motion (scroll-driven, sticky stacks, parallax, cursor-reactive — motion.md "Advanced") where it expresses the hypothesis, not as a quota. Effects never hide substance: key information stays visible without waiting for an animation.

### 3g. Layout & responsive (carry-over rules that still matter)
- **Mobile-first.** Base CSS = phone; `@media (min-width:768px)` and `(min-width:1440px)`.
- **Don't waste desktop space** (the #1 AI visual flaw): heading 56-80px at 1440px+, body max-width ≥500px, hero wrapper 1100-1400px for multi-column. At least one variant per round uses a non-centered layout (split/editorial/asymmetric). Atmospheric ≠ empty — content must anchor and fill.
- **Check the wide end too:** position things relative to the content column, never the window edge (`right: calc(50% - 512px)` drifts on monitors wider than yours).
- **Phone traps:** no `100vh` hero wrapped around small text (empty screen on a phone); reveal-on-scroll must never leave content hidden if the observer doesn't fire — hide via a `.js` class and time out to visible.
- **Cut text on the page:** short cards, one line of substance + tags; secondary detail may go behind a toggle, but what the offer *is*, the price/date and the action stay visible. Walls of text read as «монолитно».
- Real content, never lorem ipsum. Mark placeholder text in `<!-- PLACEHOLDER -->` comments.

### 3i. Navigation & non-standard elements → read `references/interaction-patterns.md`
- **Understand navigation, don't ignore it.** If the content is list-heavy or has multiple sections (memo, docs, multi-section page, catalog), **≥1-2 prototypes must include real navigation** — a sticky table-of-contents / scroll-spy sidebar, sub-nav, or anchor rail — so the page is actually navigable, not just a long scroll. Vary the nav pattern across prototypes (it's a structural axis).
- **Topic interactives (landings):** one working piece per round-1 variant, the full 3–4 in the round-2 build (vibe.md read 4). Each says "here they do exactly this" and helps the visitor understand or decide. A beautiful page without them gets called «скучно»; a page stuffed with them for show fails the other way.
- **Icons:** own inline-SVG line set, ≥32px in cards, stroke ≥1.75. Emoji banned; "no emoji" ≠ "no icons".
- **Reach for non-standard elements.** **≥1 prototype should feature one unconventional, memorable interaction/element** — bento grid, horizontal scroll-snap section, sticky-stacking cards, before/after slider, draggable cards, scroll-spy TOC, custom cursor, hover-reveal. The reference file has a dependency-free palette.

### 3h. Generation order & parallelization
**First, in the main flow: source imagery centrally** (3e) into `prototypes/assets/` so every agent gets working local paths. Then generate variant 0 alone. Then generate structured variants **in parallel** — one Agent per prototype, each given the full `BRIEF.md`, its direction row, the vibe card, the local asset paths, and the relevant reference files (always `vibe.md`). If parallel isn't available, generate sequentially and **re-read BRIEF.md before each** to avoid drift toward repetition.

---

## Step 3.5 — WOW-gate (before saving each prototype)

The old checklist was 13 technical items and 0 creative ones — a forgettable prototype passed 13/13. Keep the technical checks (mobile-first, two breakpoints, Cyrillic verified, real content, perf, `prefers-reduced-motion`, standalone) **and** add these creative gates:

- [ ] **Recognition** — would someone from the audience see "this is for me" in 3 seconds? (genre codes present)
- [ ] **Feeling** — does it produce the feeling from the vibe card, not just "look nice"?
- [ ] **One distinctive move** — is there one thing you haven't seen a hundred times in this niche?
- [ ] **Topic behaviour** — are the 3–4 topic interactives there and actually working (landings)?
- [ ] **Grayscale test** — different from the others with color removed?
- [ ] **Designed vs generated** — does it read as crafted, or as AI-default?
- [ ] **Image self-sufficiency** — looks finished even if images fail?
- [ ] **Motion is visible** — would a person notice movement in the first 3 seconds?

If the honest answer to a gate is "no", the direction is wrong — change it, don't just polish.

---

## Step 3.6 — Measure before showing (mandatory) → `references/ui-verify.md`

```bash
node <skill-dir>/scripts/check.mjs prototypes/ --widths 390,1440,1920
```
Fix **every FAIL** (sideways scroll, unreadable text, content stuck invisible, font without Cyrillic or not loaded, failed images/fonts, JS errors), fix WARNs on body copy and CTAs, check NOTE items (text on photos, gradients) by eye. Round 1: `--widths 390,1440` is enough; the final gets 390/1440/1920. Rerun until clean. **Then look at every variant's screenshots yourself at phone and desktop width** — a clean script only means it found nothing it knows how to find. The eye pass has a fixed list, because the script can't see these:
- **seams:** a scrim/overlay/panel that ends in the middle of the text block, a hard edge where a photo meets a panel (the script only flags "text on photo — check by eye");
- **empty or cramped first screen**, content hidden below the fold on 1440×900;
- **overlaps:** portrait over headline, sticker over button, text over a busy part of the photo;
- **tone vs audience:** would the person from the vibe card find it too dark / too childish / too corporate? Only then build the gallery, and tell the user the result in one line. Parallel builders don't exempt you: run it on their output too — two of five once shipped unreadable text. No Node/Chrome → run the manual probes from ui-verify.md through the browser tool.

---

## Step 4 — Present & Evaluate

**The user evaluates the prototypes themselves — always deliver a browsable gallery, by default.** Your own screenshot-and-review is at most a self-check, never a substitute: the deliverable is a gallery the user opens in a real browser and judges (visual taste and "does this feel right for my audience" are theirs to call, and prototypes carry interaction/motion a static image loses). Don't skip the gallery in favour of pasting your impressions.

Create `gallery.html` (variant 0 shown first as "AI's Best Shot", structured variants after; dark neutral bg; "Open" link per card + iframes with relative paths; mobile/desktop note). **Then hand the user a live way to view it, and give them the link/path explicitly:** serve the prototype directory over `http://127.0.0.1:<port>` (a local static server — most reliable, since some browsers block `file://` iframes and page-internal `fetch`) and/or give the `file://` path as fallback. Confirm the server responds (curl the gallery + one prototype) before telling the user it's ready.

**Optional self-check — real screenshots:** if a browser-screenshot tool is available (Playwright MCP, or headless Edge/Chrome `--screenshot`), you may capture PNGs to sanity-check the prototypes rendered (headless Chrome needs a writable `--user-data-dir`). This is for your verification only — it does not replace the user's own gallery review. Note: full-bleed `100svh` heroes screenshot only the first viewport; capture sections separately if needed.

Give the user a simple frame:
> - Does it FEEL right for my audience? (not "do I like it" — "would my users trust/want this?")
> - Is the key action obvious?
> - What grabs you / what repels you?

Don't ask "which is best?" — ask **"which 1-2 are closest, and what would you change?"** Then ask the **mixing question**: "Anything to borrow from the others — a font, color, motion, layout idea?" (How non-designers reach a unique result.)

---

## Step 5 — Refine & Build

1. Start from the chosen base; list what's borrowed explicitly.
2. Apply changes one category at a time (type → color → layout → effects); visual conflicts appear when you merge all at once.
3. Save as `prototypes/[scope]-FINAL-[name].html`; iterate in place (don't spawn v2, v3…).
4. On approval, add a **"Final Direction"** section to `BRIEF.md` (locked palette, fonts, layout) as the source of truth for the full build.
5. Run `scripts/check.mjs` on the FINAL file too, at 390/1440/1920.

**Point complaints on the built page** («слева пусто», «кнопка теряется», «тест некрасивый»): show **2–3 variants of that one element on top of the built page**, not a new round of prototypes — this has resolved every such complaint in one reply. A complaint about readability or «всё сливается» — **measure first** (ui-verify.md), then fix.

**Redesigning an existing screen:** list every action the old one had (including hover-only buttons) before you start, and check each one exists after — hidden actions disappear silently.

### 5.5 — Feel pass (default; runs on the real build, not prototypes)

Once the final direction is built into **real production code** (the component/page, not the throwaway prototype), run the polish pass: **read `references/feel-polish.md` and apply the 16 micro-detail rules.** This is the layer that separates "looks designed" from "AI-default" — concentric radii, optical alignment, interruptible animation, tabular numbers, image outlines, scale-on-press, and so on.

- **It runs by default** at this point — you don't need to ask permission to polish. The user can opt out with "skip polish", and individual buttons/elements can opt out via the `static` pattern.
- **Report it** in feel-polish.md's format: changes as Before/After tables grouped by principle; omit principles that needed nothing.
- **Don't apply it to the prototypes themselves** — they're concept bets, and a 16-point correctness checklist on a throwaway brings back the "passes every check, moves no one" failure this skill exists to fight. Polish the winner, in real code.

---

## Quick reference

| Situation | What to do |
|-----------|-----------|
| "make it look good" | Start Step 1 — they don't know what they want yet |
| Existing project | Read its files first; surface contradictions/bugs; ask only the gaps |
| Russian/Cyrillic UI | Verify every font for Cyrillic (typography.md) — this is non-negotiable |
| Data dashboard / dense tool | Skip photos; wow via hierarchy + type + functional motion |
| "minimal / safe / calm" | Probe: does it mean *plain*, or *trustworthy*? Calm can still be atmospheric |
| No references, no time | Normal case — read the vibe yourself (vibe.md); never send them hunting |
| Buyer ≠ user (parents buy a kids' camp) | The page's tone follows who it's *about*: kids → bright and light; trust signals for the buyer go into the content, not into a dark palette |
| «мрачно / скучно / мало секса / сливается / одинаковые» | Decode with the verdict table in vibe.md; «не то» usually means you left the genre |
| Complaint about one element | 2–3 variants of that element over the built page, not a new round |
| "Looks broken / pale / shifted" | Measure first (ui-verify.md) — the screenshot may be lying |
| Wants to skip prototypes | Say once that 4 light first screens cost little and save rework; if they still want one direction, build one and note the risk |
| Can't choose | Ask the eval questions; if stuck, combine top 2 |
| Time pressure | Round 1 only, minimal questions — never skip the Step 3.6 check |
| Final build is done | Run the Feel pass (Step 5.5, feel-polish.md) by default — unless user says "skip polish" |
