# Deck mode — a presentation instead of a site

The same idea as the site path: the image model draws, the user picks with their eyes, the coding
model builds over the picture and measures before showing. What changes: slides 16:9 instead of
screens, no phone mockup, every slide after the pick gets **its own composition from its own
content**, and the result is a deck (HTML → PDF; Google Slides or PPTX on request).

```
Context → Vibe → Outline → 3 test slides → 6 directions × 3 slides → Gallery → Pick/mix
→ Every slide drawn → Plates → Build deck → Check → Show → Export
```

**Files:** `prototypes/BRIEF.md`; `prototypes/mockups/` — `m1.png … m6.png` (title slides),
`m1-2.png`, `m1-3.png` … (test slides 2 and 3), `gallery.html`; after the pick `slides/s01.png …`
(one drawn slide per slide), `slides/s01-plate.png …`; `prototypes/deck.html` +
`prototypes/deck-assets/`; `prototypes/_check/`. Deck template: `assets/deck-template.html`.

## Why it differs from a page

- **Every slide is unique.** The owner's words (Oct 2026): «ключевым является не вопрос — как сделать
  слайды однотипными, а как упаковать информацию этого слайда уникальным образом». A spec with one grid
  for all slides ("two by two, four points") was rejected as an approach, and points invented to fill
  the grid were the worst part. Shared between slides: only the language of the picture — palette,
  type, manner, recurring characters — and one or two constant marks (logo, page number).
- **A deck choice needs several slides, not one.** The owner's reference gallery (Sept 2026, ten
  directions for a client's deck) showed every direction on the same six slides, and the client chose
  in "by slide" mode. A first round of five calm directions was rejected whole — «скучные и похожи
  друг на друга»: four of five palettes were muted. Run the grey test: strip colour, the six must
  still be different worlds.
- **Draw 16:9 directly.** A 3:2 mockup cropped to 16:9 pushes objects off the frame. Asked for
  "1824x1024 (16:9)", gpt-image-2 returns 1672×941 (probe 19.10.2026, 18 of 18) — that is fine;
  scale coordinates by 1920 / the image's own width.
- **No phone mockup.** Slides are watched on a screen or in a call; the readability floor is set for
  a slide shrunk into a video call (below), not for a phone layout.

## Step 1 — Context (one short block, wait for the answer)

Read what exists first: a script or outline, a previous deck, the brand, the landing of the offer.
Then ask only the gaps:
1. What is it for and who watches? (a live talk, a webinar in Zoom, a deck sent as a file, a sales
   meeting) — this sets density: a talk is one thought per slide, a file read alone carries more text.
2. The content: an outline, a script, a document — or should I write the outline? **Never invent
   facts or numbers**; where content is missing, write `[нужно: …]` on the slide and list it.
3. Roughly how many slides?
4. Where does it end up: PDF, Google Slides (will someone edit it there?), PowerPoint?
5. Brand, forbidden things, language (Cyrillic gate, `typography.md`).

**Autonomous:** take what the files give, write the rest into BRIEF.md as assumptions.

## Step 2 — Vibe → `vibe.md`

Same six reads as for a site, written into BRIEF.md. Genre codes: look at two or three decks of the
same genre if they are reachable (a conference talk, a webinar of the same niche); otherwise say they
are assumed. Show the vibe card in plain words and go on.

## Step 3 — The outline and the three test slides

**The outline first:** every slide in one line — its one thought — and next to it **how the thought
is built**: an expense, layers, a transformation, a conveyor, a check, a fork, a comparison, a scene,
a number, a quote, a pause. This line *is* the future composition. Don't pad the count of points to
make a grid even; a slide with two points has two.

**Three test slides** — the same in all six directions, named in BRIEF.md, exact words written once:
1. **Title** (emotion): the talk's name, a subtitle, who speaks.
2. **A number or a list** (how the style carries information): a real slide from the outline with
   one big number and a short caption, or three to five short points.
3. **A structure** (the hardest for any style): a real slide whose idea is a process, a fork or a
   comparison — the slide where a pretty style most often falls apart.

Pick 2 and 3 from the real outline, not made-up ones. Short words — long copy garbles in generated
images.

## Step 4 — Six directions × three slides → `mockups.md` §0, §1, §1a

Same generator, same wrapper `scripts/codex_img.py`, same diversity rule — six takes, not six
palettes. Skeleton hints for slides:

| # | Take | Skeleton hint |
|---|---|---|
| 1 | mood hypothesis 1, the genre done excellently | text field + large image, clear hierarchy |
| 2 | mood hypothesis 2, opposite light | full-bleed image, text over it |
| 3 | mood hypothesis 3 | editorial: asymmetric grid, a lot of air, huge numbers |
| 4 | type-led poster — typography and colour are the picture | words fill the frame, may cross the edge |
| 5 | texture: collage, paper, hand-drawn marks, illustration | layered, asymmetric |
| 6 | a concept from the topic's own objects (`concepts.md`) | the object *is* the layout |

Title slide prompt:
```
Сгенерируй изображение 1824x1024 (16:9): ТИТУЛЬНЫЙ СЛАЙД презентации, плоский кадр слайда без
рамки, без проектора и без интерфейса программы, уровень сильной дизайн-студии, не шаблон.
Весь текст на слайде — на русском, без ошибок, только строки из задания.
Тема: <what + for whom>. Кто смотрит: <audience line>. Где: <live talk | Zoom | file>.
Тексты: «…», «…», «…».
Настроение и подача: <this row: mood → light, colour temperature, human presence, density; skeleton>.
```
Slides 2 and 3 of a direction — one call each with its title slide as the reference:
```
Файл m<N>.png — титульный слайд презентации. Сгенерируй изображение 1824x1024 (16:9): другой слайд
ТОЙ ЖЕ презентации. Тот же стиль в точности: палитра, шрифты, фактуры, свет, манера изображений,
толщина линий. Композицию строй от содержания этого слайда, а не повторяй титульный.
Что на слайде и как устроена мысль: <the slide's words and its "how it's built" line from BRIEF.md>.
Весь текст на русском, только строки из задания.
```
Title slides first, look at each, regenerate a broken one once; then the twelve follow-ups in
parallel. Across directions, if all six "structure" slides came out as the same three boxes with
arrows, the hint was lost — say in the prompt how this direction draws a process (a staircase, a
river, stamps on a line, one long sentence broken into steps).

**One slide per direction is not offered here.** A title slide says little about how a style holds
a number or a process; that is exactly where deck styles fail. Under real time pressure (a talk in
three hours) say so once and draw title slides only.

## Step 5 — Gallery, pick, mix → `mockups.md` §2

The same `assets/gallery-template.html`, data block only: `PAGE.ratio:"16/9"`, `SCREENS` = the three
test slides by name (`{n:1,t:"Титул"},{n:2,t:"Цифра"},{n:3,t:"Схема"}`), each direction's `shots`
in that order, and in `T` say «слайд» instead of «экран» (`byScreen:"По слайдам"`, `screen:"Слайд"`,
`same:"Один и тот же слайд во всех вариантах, рядом."`). Passports, two modes, numbers not letters, «который ближе и что взять из других?» —
all as for a site. A mix is one edit call per slide with both files named.

## Step 6 — Every slide drawn in the chosen style

The chosen direction's three slides are the style references. For every slide of the outline, one
call (`codex_img.py … --ref m<N>.png`; for slides 2 and 3 of the outline reuse the test slides if
they are the same slide):
```
Файлы <refs> — слайды выбранного стиля. Сгенерируй изображение 1824x1024 (16:9): слайд №<k> той же
презентации, тот же стиль в точности (палитра, шрифты, фактуры, свет, манера, постоянные элементы:
<logo / номер слайда / …>). Композицию строй от того, как устроена мысль этого слайда:
<"how it's built" line>. Тексты: <exact words>. Весь текст на русском, только эти строки.
Сохрани как s<kk>.png.
```
Calls run four at a time (the wrapper queues the rest). Then look at the whole set as one strip: the
same hand on every slide; neighbouring slides that came out with the same composition — redraw one
of them with a different skeleton named in the prompt. Show the strip (a contact sheet of all
slides, `PIL` is enough) with one line and go on; it is the chosen direction, not a new vote.

**A long deck (over ~15 slides):** say the count of image calls once before drawing; a recurring
layout (a section divider, a quote) may be drawn once and reused with new words — that is a
constant element, not a template for content slides.

## Step 7 — Plates and the deck

1. **Plates** (`mockups.md` §4): every drawn slide with all text removed, composition untouched →
   `slides/s<kk>-plate.png`, copied to `prototypes/deck-assets/`. Compare each plate with its slide;
   list markers and small icons the edit removed are redrawn as SVG/CSS. A flat type-and-colour slide
   needs no plate — it is built in HTML/CSS.
2. **The deck** — copy `assets/deck-template.html` to `prototypes/deck.html`. Every slide is a
   1920×1080 frame; the plate is its background, every text line is live HTML in its own `.tx`
   block positioned in px of the frame, measured from the drawn slide (× 1920 / its width).
   Before writing CSS open the slide and write down positions, sizes, colours, type, as for a page.
   Fonts: the nearest Google Fonts with Cyrillic. Speaker notes, if the script has them, go into
   `data-notes` on the frame.
3. **Readability floor** (a 1920 slide shrunk into a Zoom window ~3×): body text ≥ 28px, captions
   ≥ 22px, headlines ≥ 56px, in px of the frame. The drawn slide smaller → enlarge and keep the
   composition; the floor wins over faithfulness, exactly as on the phone.
4. Several slides at once → one builder agent per 4–6 slides, each given BRIEF.md, its slides, plates
   and this step verbatim.

## Step 8 — Check before showing

```bash
node <skill-dir>/scripts/check.mjs prototypes/deck.html --widths 1920 --shots prototypes/_check/
```
Fix every FAIL and the WARNs on slide text. Then shoot every slide 1:1 and compare with its drawn
slide by eye:
```bash
chrome --headless=new --disable-gpu --hide-scrollbars --window-size=1920,1080 \
  --screenshot=prototypes/_check/s01.png "file:///<abs>/prototypes/deck.html?only=1"
```
Put the shots into one contact sheet next to the drawn slides (drawn | built) and look at the pair
for every slide: overlaps, text crossing the plate's objects, a line that wrapped differently, a
slide that grew denser than its picture. Two rounds usually leave only font metrics.

## Step 9 — Show and export

Serve `deck.html`, give the link and the contact sheet, one line on what the check found.
Complaints: about one slide → 2–3 variants of that slide; about the whole style → back to the gallery.

**Export after approval, in the format from Step 1:**
- **PDF** — Chrome prints one page per slide (the template sets `@page 1920×1080`):
  `chrome --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=deck.pdf "file:///…/deck.html"`.
  Open the PDF and look at it — this is the file the audience gets.
- **Google Slides, editable** — the deck stays the single source: render every slide's background
  with `?only=N&notext=1`, measure every text line in the browser, build a PPTX with the background
  as a picture and live text boxes on top (`python-pptx`), upload with conversion, then export the
  Google file to PDF and compare line widths with the HTML. Google Slides silently drops letter-spacing,
  text glow and per-word shadow: bake small spaced labels into the background, put glow on the text
  box, not the word. If the project has a transfer kit already, use it instead of writing a new one.
- **PowerPoint** — the same PPTX without the upload; open it (or its PDF) and check by eye.

Check on the final medium: the file the audience opens, not the HTML.

On approval add "Final Direction" to BRIEF.md: fonts, palette, constant elements, the chosen
direction's slides as the style references for any slide added later.
