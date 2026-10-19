---
name: design-first
description: >-
  Design before code: an image model draws six different visual directions as mockups, the user picks one with their eyes, and it is built as a live page (desktop and phone) or a 16:9 presentation, measured for readability before it is shown. Use when: "сделай дизайн", "подготовь макет", "давай займёмся дизайном", "нарисуй страницу", "редизайн", "варианты дизайна", "дизайн презентации", "сделай презентацию", "оформи слайды", "make a design", "design this", "how should this look", "visual direction", "design a deck". Scope: landings, dashboards, portfolios, forms, app screens, components, presentations. Do NOT use for: editing an existing .pptx/.docx file, a small CSS fix on a finished page, code review, debugging, backend or non-visual tasks.
---

# Design First

Explore the look before writing production code — for people who aren't designers but need a
distinctive result.

Three ideas; the first two measured in blind rounds with the owner (`references/mockups.md` → "Why"), the third paid for in earlier rounds (`ui-verify.md`):

1. **Always a real choice.** Six directions that differ in composition, not just colour, by default
   each shown on three screens — a direction that wins on the first screen can fall apart on a list or
   a form (the user may choose one screen to save time, Step 1). The user recognises their picture
   with their eyes; nobody can describe it in words beforehand.
2. **The image model draws, the coding model builds.** HTML prototypes written by the coding model
   never earned a "wow"; mockups drawn by an image model did, and a live page built over the mockup
   was judged the same as the mockup — on the phone too, when the phone has its own mockup.
3. **Measure before showing.** Unreadable text, sideways scroll, content stuck invisible are invisible
   in code and obvious to the user. `scripts/check.mjs` runs before anything is shown.

```
Context → Vibe → Words → 6 directions × 3 screens (or × 1) → Gallery → Pick/mix → Phone mockup → Plates → Build → Check → Show
```

## Step 0 — Site or presentation

Usually the request already says it («сделай лендинг», «нужна презентация к эфиру») — then don't
ask. Only when it is unclear, ask this one question alone, before anything else: **«Сайт или
презентация?»** A site is anything people open in a browser — landing, dashboard, form, app screen.
**A presentation switches the whole skill to `references/deck.md`**: the same vibe reading and six
directions, but slides 16:9, no phone mockup, a deck at the end. The six directions differ by what
the picture shows (a direction table filled with concrete images before any drawing) and pass a
greyscale sameness check before the gallery. Read deck.md now and follow it;
Steps 1–10 below apply only where it says so. **Autonomous / headless:** site, written into BRIEF.md
as an assumption.

**Files:** `prototypes/BRIEF.md`; `prototypes/mockups/` — `m1.png … m6.png` (first screens), `m1-2.png`, `m1-3.png` … (screens 2 and 3), `gallery.html`,
`phone.png`, `*-plate.png`, `_logs/` (create the folders); `prototypes/<scope>.html` +
`prototypes/<scope>-assets/` (plates copied here); `prototypes/_check/` for screenshots.
Gallery template: `assets/gallery-template.html` in the skill folder.

**References** (read the one a step names, when it names it):
`deck.md` (presentation mode, the whole path) · `vibe.md` (reading the topic) · `concepts.md` (mockup 6) · `mockups.md` (generation, gallery, phone,
plates) · `typography.md` (matching fonts, Cyrillic gate) · `ui-verify.md` (the check, manual probes) ·
`motion.md`, `interaction-patterns.md` (next sections, optional) · `feel-polish.md` (production code) ·
`frontend-aesthetics.md` (fallback only).

---

## Step 1 — Context: gather, then ask only the gaps

**Existing project → read first:** `PRODUCT.md`, `vision.md`, `README.md`, `CLAUDE.md`, `HANDOFF.md`,
`docs/`, existing UI (`globals.css`, components, the live site). Extract what it is, audience, tone,
stack, language, brand colours/fonts. Surface **contradictions** (spec says dark, live CSS is light) and
**bugs** (a body font without Cyrillic) — ask about them instead of silently choosing.

Then ask only what the files and the topic can't answer, in one short block, and wait for the answer:
1. What surface? (landing, dashboard, form, app screen, component)
2. Who uses it, on what device?
3. What should they do? (buy, sign up, register, find the free slot…)
4. Existing brand? A volunteered site or picture is gold — **never require references**, never send the
   user hunting: reading the vibe is your job.
5. Anything forbidden? Explicit bans ("no faces", "not dark") and an existing brand **outrank every
   hypothesis** below.
6. Language of the UI (drives the Cyrillic gate).
7. **«Сколько экранов рисовать на каждое направление: один или три?»** — always in this block unless
   the request already answered it. Give the trade in one line each:
   - **один** — six first screens, about three times cheaper and faster; screens 2 and 3 are drawn
     after the pick, only for the chosen direction (Step 5);
   - **три** — 18 pictures before the pick; the user sees how each style carries a list and a form,
     a direction that wins on the first screen can fall apart on those.

   Write the answer into BRIEF.md as `Экранов на направление: 1 | 3`. No answer, or «на твоё
   усмотрение» → three (the measured default, mockups.md §1a). The image generator near its limit →
   recommend one and say why.

Feeling and boldness are optional — if the user shrugs, read them from the topic and show your reading
in the vibe card. **Autonomous / headless:** don't block; take every answer the files give, write the
questions you would have asked into BRIEF.md as assumptions (three screens per direction), go on.

## Step 2 — Read the vibe → `references/vibe.md`

Six reads, written into `prototypes/BRIEF.md`: audience in one concrete line (if the buyer isn't the
person the page is about, name both — the tone follows who it's *about*); genre codes seen on 3 live
pages of the same offer (`node <skill-dir>/scripts/check.mjs <url> --widths 1440 --shots prototypes/_genre/`,
look at the PNGs, keep *seen* apart from *assumed*); **2–3 mood hypotheses** → light, colour
temperature, human presence, density; topic props; whose palette; the vibe card.

**Show the vibe card in plain words and go straight on** — the real checkpoint is the gallery:
«Вот как я прочитал тему, рисую шесть первых экранов. Если где-то мимо — скажи, поправлю по ходу.»

## Step 3 — The words

Every direction is shown on **three screens that test different things** — name them in BRIEF.md:
1. the first screen (emotion): headline, subheadline, CTA;
2. a content screen (how the style carries a list): the topic prop from the vibe card — "is this about
   you" cards, a programme, steps, a price table — three to five short items;
3. an action screen (the moment of decision): a form, a slot picker, a pricing choice with its button.

A tool: the main view, one item opened, the adding/editing action — with realistic data (names, times,
statuses, counts). Write the exact words of all three screens; they are identical in all six
directions, so the user compares design, not copy. Short — long copy garbles in generated images.
Real content, never lorem ipsum.

## Step 4 — Six directions, three screens each → `references/mockups.md`

Check the image generator with one call. Then six desktop first-screen mockups, one per row of the
diversity table in mockups.md (three mood hypotheses, a type-led poster, a texture/collage screen, a
concept from the topic's objects — `concepts.md`); for a tool, six organising ideas. Run the calls in
parallel. Look at each: mood matches its row, nothing broken; regenerate a broken one once (same
file name with `--replace`, the old version stays as `.v1`). Don't drop a mockup for taste — your
taste doesn't predict the user's.

**Three screens per direction:** then screens 2 and 3 of every direction, each drawn **from that
direction's first screen as the style reference** (mockups.md §1a) — twelve more calls, in parallel.
First screens first: a broken first screen is fixed before two more are drawn in its style.
**One screen per direction:** stop after the six first screens; the gallery shows them in one grid.

**Generator hit its usage limit** → say when it resets and wait, or ask before using the fallback.
**No image generator available** → fallback: six standalone HTML first screens along the same six
rows, as many screens per direction as BRIEF.md says (read `frontend-aesthetics.md` and `typography.md` first), then
Step 8 on each, then the gallery.
Say once that this path is weaker on taste.

## Step 5 — Gallery, pick, mix

The gallery page is `assets/gallery-template.html` with its data block filled (mockups.md §2): two
modes — every direction with its three screens, and one screen in all six directions side by side —
each image opening large, a short passport per direction (name, idea, palette, fonts,
feeling — described, never ranked); served over `http://127.0.0.1:<free port>`, confirmed with curl,
link given. Ask: **"which one is closest, and what
would you take from the others?"** — not "which is best". A mix is not a new round: one edit call
mixes the first screen (both images passed as `--ref`, mockups.md §0), then the mix's other screens are drawn from that mixed
first screen as in mockups.md §1a; give the link in one line and go on unless they object. If none is close, decode the
verdict words with vibe.md and draw a new six — don't start building a "least bad" one.
**Autonomous / headless:** stop here and report the gallery — picking is the user's; if the task
explicitly demands a finished page, take direction 1 and write that choice into BRIEF.md as an assumption.

**One screen per direction → after the pick** draw screens 2 and 3 of the chosen direction only
(mockups.md §1a, two calls), append them to that variant's `shots` and give it `labels` with the three
screen names (the template then shows its own row of three; leave `SCREENS` as it is), and show them
in one line with the link. They are part of the chosen direction, not a new vote; a screen that drifted from the first one
is redrawn once.

## Step 6 — Phone mockup and plates → `references/mockups.md`

1. Draw the **vertical phone mockup** from the chosen direction's first screen (always — shrinking the desktop
   composition was the one measured failure of this path).
2. Make **plates** when a mockup has raster art (photo, paper or stamp texture, illustration): the
   chosen direction's three desktop screens and the phone mockup with all text removed, composition untouched; compare each plate with its
   mockup. A flat type-and-colour poster or an interface needs no plate — it is built in HTML/CSS.
3. Show the phone mockup in one line with a link — it is part of the chosen direction, not a new vote.

## Step 7 — Build the page over the mockups

Goal: at 1440×900 the page looks **like the desktop mockup**, at 390×844 **like the phone mockup**.
Faithfulness first, own ideas never.

- **Text, buttons, forms — live HTML.** Photos, paper, textures — the plate as background, positioned so
  the crop matches the mockup at 1440 (mockup 3:2, screen 16:10 — trim top/bottom sensibly). Small
  decorations the plate lost — inline SVG/CSS. An interface is built entirely in HTML/CSS.
- **Before writing CSS, open the mockup and write down** positions (in %), sizes, colours (hex), type
  (serif/grotesk, weight). Fonts: the nearest Google Fonts with Cyrillic (`typography.md`, the gate is
  mandatory for Russian).
- **Phone:** below 768px the layout follows the phone mockup and its plate. **Readability floor:** body
  text ≥14px, labels ≥11px, buttons ≥44px tall — if the mockup is smaller, scale up and keep the
  composition. Grow the bottom of a 2:3 mockup to the taller screen with its background, never by
  stretching a photo.
- **Below the first screen:** screens 2 and 3 of the chosen direction, each built over its own mockup
  the same way; on the phone they follow the phone mockup's type, spacing and colour in one column.
  Landings may add topic interactives
  (`interaction-patterns.md`), motion that serves the mood (`motion.md`, always with
  `prefers-reduced-motion`). Page → 1–2 sections at this stage; the full page comes after approval.
- Standalone HTML, inline CSS/JS, Google Fonts only. Files: `prototypes/<scope>.html`,
  `prototypes/<scope>-assets/`.
- Several pages at once → one builder agent per page, each given BRIEF.md, its mockups, plates and
  Step 7 verbatim.

## Step 8 — Check before showing → `references/ui-verify.md`

```bash
node <skill-dir>/scripts/check.mjs prototypes/<scope>.html --widths 390,1440 --shots prototypes/_check/
```
Fix **every FAIL**, fix WARNs on body copy and CTAs, rerun until clean; the last run adds 1920. Then
**compare by eye**: the 1440 shot next to the desktop mockup, the 390 shot next to the phone mockup,
and fix what differs until only font metrics are left (usually two rounds). The eye list the script can't see: seams (a panel ending mid-text), overlaps,
an empty or cramped first screen, tone vs audience. When editing only the phone, confirm the desktop
shot is unchanged: `python -c "from PIL import Image, ImageChops as C; print(C.difference(Image.open('a.png').convert('RGB'), Image.open('b.png').convert('RGB')).getbbox())"` prints `None`. Builder agents don't exempt you: run the check on their output.

## Step 9 — Show

Serve the page, give the link, and say in one line what the check found. Offer a side-by-side
"mockup | page" view if the user wants to judge the transfer. Complaints on the built page:
- **About one element** («кнопка теряется», «слева пусто») → 2–3 variants of that element over the built
  page, not a new round.
- **About readability** («всё сливается», «бледно») → measure first (ui-verify.md), then fix.
- **About the whole direction** → back to the gallery; another mockup or a mix.

On approval add a "Final Direction" section to BRIEF.md (locked fonts, palette, mockup files) as the
source of truth for the full build.

## Step 10 — Full page and feel pass → `references/feel-polish.md`

After approval build the rest of the page — in the prototype file for a static page, or as components
in the project's code — in the same style (further images per mockups.md §5), then by default apply the 16 feel-polish rules and report them as
Before/After tables ("skip polish" opts out). Run `check.mjs` on the production page at 390/1440/1920.
**Redesign of an existing screen:** list every action the old one had (including hover-only buttons)
before you start, and check each one exists after.

---

## Quick reference

| Situation | What to do |
|---|---|
| "make it look good", no brief | Step 1 — ask only the gaps (Step 0 only if site vs deck is unclear) |
| Presentation, slides, deck, «преза» | `references/deck.md` — the whole path is there |
| No references, no time | Normal case — read the vibe yourself, never send them hunting |
| Russian UI | Cyrillic gate on every font (typography.md) — non-negotiable |
| Buyer ≠ user (parents buy a kids' camp) | Tone follows who the page is *about*; buyer's trust goes into content |
| Dashboard / dense tool | Six organising ideas, no photos, no plates, built in HTML/CSS |
| «мрачно / скучно / сливается / одинаковые» | Decode with the verdict table in vibe.md |
| None of the six is close | New six from a corrected vibe card, not the "least bad" |
| Wants to skip the gallery | Say once that six pictures cost minutes and save rework; then draw one mockup of the best reading and build it |
| Page fine on desktop, weak on phone | The phone needs its own mockup (Step 6), not a squeezed layout |
| "Looks broken / pale / shifted" | Measure first (ui-verify.md) — the screenshot may lie |
| Time pressure, or the image generator is near its limit | Recommend «один» in Step 1 and say why; the gallery template then drops its mode switch by itself. Never skip the phone mockup or Step 8 |
