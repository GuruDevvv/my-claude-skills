# Reading the vibe — letting the topic tell you what it should look like

Most people who ask for a design have **no reference at hand** and no time or wish to hunt for one.
They carry a picture in their head that they can't describe in words — but they recognise it
instantly when they see it. The skill's job is to read that picture from the topic itself.

## Why

Earlier versions invented a bold metaphor from far outside the niche for every prototype. On real
projects that made pages feel alien to their audience (a webinar landing went through nine
rejected prototypes before the genre's own look landed at once), decorative metaphors on a work
tool were called «непрактичное творчество», and clean pages without topic behaviour were «скучно».
So: stand on the genre, add concepts grown from the topic's own objects (concepts.md), and give
the page behaviour from the topic.

## The six reads (do them in order, write the results into BRIEF.md)

### 1. Audience in one concrete line
Who, age range, situation, where they arrive from, device. **If the buyer isn't the person the
product is for** (parents buy a kids' camp, HR buys a training), name both: the tone of the page
follows who it's *about* — a kids' robotics camp is bright and light even though parents pay;
the buyer's needs (safety, schedule, price, trust) go into the content. Blind test 25.09: the
"trust for parents" reading turned a kids' school dark — «темноват для детской школы». Not "women 30–45" but
"a woman 35–45, married, reading an Instagram ad in bed at 1 a.m. on her phone, embarrassed
to ask anyone about this". The moment and the place drive the look more than demographics.

### 2. Genre codes — what this audience already trusts for this kind of offer
Look at **3 real, live pages of the same offer for the same audience** (more only if they disagree) (competitors, the
leaders of the niche) — **with your eyes, not as text.** A text fetch hides exactly what matters:
light, cropping, composition. Take first-screen screenshots
(`node <skill-dir>/scripts/check.mjs <url> --widths 390,1440 --shots prototypes/_genre/` gives you
PNGs of any URL) and look at them. If you truly can't get pages, derive from knowledge and mark
every such line in the brief as **assumption**. Write the genre DNA, keeping **seen** apart from
**assumed**:

| Code | What to note |
|---|---|
| Light | dark / light / mixed; is there a visible light source (glow, sunset, lamp)? |
| Imagery | photo / illustration / pure type; are people shown, faces or bodies, how close? |
| Temperature | warm / cold / neutral |
| Density | airy editorial vs dense info vs poster |
| Signature blocks | what almost every page in the niche has (author block, program, reviews, countdown…) |
| Signature effects | glow, grain, big numbers, handwriting, stickers… |

Genre codes are the **baseline, not an anti-reference.** You may break one code deliberately
(that is the "distinctive move"), never all of them. But popularity among competitors is a
hypothesis about what the audience trusts, not proof — that's why read 3 produces several
moods, not one.

### 3. Two or three mood hypotheses → concrete visual properties
**One reading of the topic is a single point of failure:** if it's wrong, all the prototypes are
wrong together. So name **2–3 different moods the topic could honestly carry** — e.g. intimacy can
be *sensual*, *homely-tender* or *bold-provocative*; a finance course can be *calm-competent*,
*ambitious* or *friendly-demystifying*. The prototypes are then spread across these hypotheses,
and the user recognises their picture in one of them — which is how every past success happened.

Explicit prohibitions from the user ("no nudity", "no faces") hold for all hypotheses. Vaguer
anti-references ("not corporate", "not dark") are hypotheses too — cover at least one variant
that respects them and don't let them veto the genre wholesale.

For each hypothesis translate the feeling into properties you can actually build:

| Feeling | Light | Colour | Human presence | Density | Motion |
|---|---|---|---|---|---|
| warmth, intimacy, desire | a warm light source, glow | warm, skin tones | close crop, body language | airy | slow, breathing |
| trust, expertise | even, calm | restrained, one accent | the author's face, credentials | ordered grid | functional (count-up) |
| urgency | high contrast | one hot accent | optional | tight | countdown, pulse |
| play, curiosity | bright | saturated | illustrated characters | varied rhythm | bouncy, interactive |
| calm, recovery | soft daylight | desaturated naturals | distant figure / nature | airy | drift, very slow |

**The user's verdict words are measurements — decode them** (all from real rejections):

| They say | What is usually wrong |
|---|---|
| «мрачно», «монотонно», «скучно» | every section the same luminance; no light source; no rhythm between sections |
| «мало секса», «холодно» | no human warmth — no body, skin, glow; too graphic or too clean |
| «всё сливается» | low contrast, blocks of equal weight, no clear focal point — **measure it** (ui-verify.md) |
| «все одинаковые» | the same layout skeleton, even if colours/metaphors differ |
| «перегружено текстом», «монолитно» | text walls; no icons; no interaction; cards with more than one line of substance |
| «дёшево» | default fonts, stock-looking photo, uneven spacing, too many accents |
| «не то», «плачу» | you left the genre — go back to the codes from read 2 |

### 4. Topic props → interactive pieces
List the objects and actions of the topic. For a landing plan **3–4 interactive pieces made from
them** — each must say "here they do exactly this", otherwise the page fits anything. In the first
(light) round each variant shows **one** of them working; the full set goes into the chosen
direction. Every piece must earn its place by helping the visitor understand or decide — effects
for their own sake replace "text wall" with "effect wall".
Real examples: a search bar typing the visitor's secret question with live suggestions (intimacy
webinar); a "how much is this about you" slider; a level slider A1→C2 and flip cards
"phrase in Russian / in English" with `speechSynthesis` (language tutor); a season deadline board
(olympiad tracker). For a tool/dashboard the "props" are usability mechanics instead:
filters, quick search, keyboard shortcuts, colour per section.

Icons: your own inline-SVG line set, ≥32px in cards, stroke ≥1.75. Emoji stay banned — but
"no emoji" never means "no icons".

### 5. Whose palette is it?
Before borrowing an organisation's palette, check it isn't already bound to **another author or
product** in the same project. A warm cream-terracotta palette once designed for one speaker made
a second speaker's product read as the first one's — "никуда не годится". Each author/product gets
its own colour character.

### 6. The vibe card — a few plain lines in the brief
```
Кто смотрит: <read 1>
Жанр и его коды (видел / предполагаю): <read 2, in 1–2 lines>
Настроения-гипотезы: 1) <mood> → <properties>  2) …  3) …
Фишки из темы: <read 4>
Один смелый ход поверх жанра: <what breaks one code, deliberately>
```
Show it with the brief. The user may correct it in one reply or just say "go" — never require
them to supply references. If they volunteer a picture or a link, it overrides reads 2–3.

## How the prototypes differ

All variants stay **inside the topic and its genre**, spread across the 2–3 mood hypotheses
(at least one variant per hypothesis). Within that they differ by:
- **style register** — dark cinematic, light editorial magazine, poster, soft app, strict grid;
- **layout skeleton** — the grayscale test still applies: strip colour, they must still differ;
- **palette** within the vibe's temperature — never six shades of one palette;
- **type** and **which topic interactive leads**.

First round (light, see SKILL.md Step 3): **4 variants — 2 genre + 2 concept** (concepts.md), every
mood hypothesis covered. Variant 0 is the boldest concept and may step outside the hypotheses
(a reading nobody wrote down) — that's its job. For a tool or dashboard: concepts only if they
work (clock face = the day, board = the queue), never as decoration.

## Worked examples

### A) Intimacy webinar for women (what finally worked)
- **Vibe card:** a woman 35–45, phone, 1 a.m., ashamed to ask → genre: dark, big warm back-lit
  photo, glow → feel: warmth, secrecy, being understood → props: the search bar with her
  question, the "is this about me" slider → bold move: embers drifting over the hero.
- **Built:** dark hero with a warmly lit clothed figure, embers; a "1 a.m." screen with the typing
  search; the slider; programme with the author; final CTA. Chosen in one reply.

### B) Business-English tutor for aviation staff
- **Genre:** premium personal-service landing — author's face, results, calm grid.
- **Missing in the rejected round:** props. Fixed with a level slider, flip cards with audio,
  a role-play with reply choice, inline-SVG icons, alternating dark cinematic / light editorial
  sections, cards cut to one line + tags.

### C) Olympiad deadline tracker for parents (functional)
- **Vibe:** "what must I do this week?" — urgency without panic.
- **Built:** a dominant dark strip with giant countdowns, calm card feed with status rails,
  vermilion only for "act now", count-up and pulse as the only motion. No photos.

### D) Investor proposal (trust register)
- **Vibe:** precision, gravity, restraint. Oxidised-steel dark, one gold "seal" accent,
  document serif + mono labels, term-sheet rows. Functional motion only. Distinctive ≠ emotional.
