# Reading the vibe — letting the topic tell you what it should look like

Most people who ask for a design have **no reference at hand** and no time or wish to hunt for one.
They carry a picture in their head that they can't describe in words — but they recognise it
instantly when they see it. The skill's job is to read that picture from the topic itself.

## Why this replaced "invent a concept from outside the category"

The previous version told each prototype to grab a bold metaphor from far outside the niche
("a telegram from 1920s Berlin"). On real projects that failed in a consistent way:

- **A women's-marathon webinar landing:** nine prototypes over three rounds rejected —
  "мрачные, монотонные, скучные", then "мало секса", then "смотрю на все это и плачу".
  What finally landed at once: the *typical look of that genre* — a dark page, a big warmly
  back-lit photo of a woman, glow and embers. The brief had listed exactly that genre as an
  anti-reference. The audience recognises "this is for me" through genre codes; fleeing them
  made the pages feel alien.
- **An internal knowledge-base tool:** five prototypes with metaphors (a wheel, a chart,
  a metro map) — "все очень похожи и мне не нравится… убрать это непрактичное творчество".
  Different metaphors on the same layout skeleton read as identical; decoration that doesn't
  speed up work is noise.
- **A business-English tutor site:** four clean, correct prototypes — "перегруженность текстом,
  монолитность, скучно, без иконок, анимаций и классных фишек, характерных для темы". The look was
  fine; the pages lacked *behaviour from the topic*.

Lesson: **stand on the genre, be excellent inside it, add one distinctive move on top.**
Distinctiveness is a garnish, not the foundation.

## The six reads (do them in order, write the results into BRIEF.md)

### 1. Audience in one concrete line
Who, age range, situation, where they arrive from, device. Not "women 30–45" but
"a woman 35–45, married, reading an Instagram ad in bed at 1 a.m. on her phone, embarrassed
to ask anyone about this". The moment and the place drive the look more than demographics.

### 2. Genre codes — what this audience already trusts for this kind of offer
Look at **3–5 real, live pages of the same offer for the same audience** (competitors, the
leaders of the niche). If web search/fetch is available, actually open them; if not, derive
from knowledge and say so in the brief. Write the genre DNA:

| Code | What to note |
|---|---|
| Light | dark / light / mixed; is there a visible light source (glow, sunset, lamp)? |
| Imagery | photo / illustration / pure type; are people shown, faces or bodies, how close? |
| Temperature | warm / cold / neutral |
| Density | airy editorial vs dense info vs poster |
| Signature blocks | what almost every page in the niche has (author block, program, reviews, countdown…) |
| Signature effects | glow, grain, big numbers, handwriting, stickers… |

Genre codes are the **baseline, not an anti-reference.** You may break one code deliberately
(that is the "distinctive move"), never all of them.

### 3. Emotional core → concrete visual properties
Name what the visitor should feel right before clicking, then translate the feeling into
properties you can actually build:

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
them** — each must say "here they do exactly this", otherwise the page fits anything.
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

### 6. The vibe card — five plain lines in the brief
```
Кто смотрит: <read 1>
Жанр и его коды: <read 2, in 1–2 lines>
Что должен почувствовать: <read 3> → <the 3–4 visual properties it implies>
Фишки из темы: <read 4>
Один смелый ход поверх жанра: <what breaks one code, deliberately>
```
Show it with the brief. The user may correct it in one reply or just say "go" — never require
them to supply references. If they volunteer a picture or a link, it overrides reads 2–3.

## How the prototypes differ

All variants stay **inside the read vibe**. They differ by:
- **style register** — dark cinematic, light editorial magazine, poster, soft app, strict grid;
- **layout skeleton** — the grayscale test still applies: strip colour, they must still differ;
- **palette** within the vibe's temperature — never six shades of one palette;
- **type** and **which topic interactive leads**.

Default composition of 6: **3–4 "the genre done excellently"** (different registers and
skeletons), **1–2 "genre + one bold move"**, plus **variant 0**, the free bet. For a tool or
dashboard: no decorative metaphors at all — variety comes from register and usability mechanics.

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
