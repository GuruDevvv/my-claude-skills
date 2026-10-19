# Deck mode — a presentation instead of a site

The same idea as the site path: the image model draws, the user picks with their eyes, the coding
model builds over the picture and measures before showing. What changes: slides 16:9 instead of
screens, no phone mockup, every slide after the pick gets **its own composition from its own
content**, and the result is a deck (HTML → PDF; Google Slides or PPTX on request).

```
Context → Vibe → Outline → 3 test slides → 6 directions × 3 slides → Gallery → Pick/mix
→ Every slide drawn → Plates → Build deck → Check → Show → Export
```

Scripts: `<skill-dir>/scripts/codex_img.py` (pictures), `<skill-dir>/scripts/deck_export.py` (slide
shots, PDF, the drawn | built sheet — it finds Chrome itself), `<skill-dir>/scripts/check.mjs --deck`.
Run them from the project folder.

**Files:** `prototypes/BRIEF.md`; `prototypes/mockups/` — `m1.png … m6.png` (title slides),
`m1-2.png`, `m1-3.png` … (test slides 2 and 3), `gallery.html`; after the pick `prototypes/slides/s01.png …`
(one drawn slide per slide), `prototypes/slides/s01-plate.png …`; `prototypes/deck.html` +
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

**Rhythm.** Read the outline as a sequence: dense scene slides must alternate with plain ones (a
number, a list on a flat colour, a pause with one line). Four rich pictures in a row tire the viewer;
the plain slides make the scenes land. Mark the plain ones in the outline.

**Three test slides** — the same in all six directions, named in BRIEF.md, exact words written once:
1. **Title** (emotion): the talk's name, a subtitle, who speaks.
2. **A number or a list** (how the style carries information): a real slide from the outline with
   one big number and a short caption, or three to five short points.
3. **A structure** (the hardest for any style): a real slide whose idea is a process, a fork or a
   comparison — the slide where a pretty style most often falls apart.

Pick 2 and 3 from the real outline, not made-up ones, and write next to each its number in the
outline (`тест 2 = слайд 5`) — after the pick these pictures become those slides and are not redrawn.
For each test slide also write **the thought and the feeling** in one line (title of a therapy webinar:
«помогать клиенту можно легче» → облегчение). That line is shared by all six directions; *how* it
is shown is not (Step 4).
Short words — long copy garbles in generated images. Speaker notes, if the script has them, stay in
the outline next to each slide; the PPTX export puts them into the slide notes.

## Step 4 — Six directions × three slides → `mockups.md` §0, §1, §1a

Same generator, same wrapper `<skill-dir>/scripts/codex_img.py`, same diversity rule — six takes, not six
palettes. Skeleton hints for slides:

| # | Take | Skeleton hint |
|---|---|---|
| 1 | mood hypothesis 1, the genre done excellently | text field + large image, clear hierarchy |
| 2 | mood hypothesis 2, opposite light | full-bleed image, text over it |
| 3 | mood hypothesis 3 | editorial: asymmetric grid, a lot of air, huge numbers |
| 4 | type-led poster — typography and colour are the picture | words fill the frame, may cross the edge |
| 5 | texture: collage, paper, hand-drawn marks, illustration | layered, asymmetric |
| 6 | a concept from the topic's own objects (`concepts.md`) | the object *is* the layout |

**Before any prompt, fill the direction table in BRIEF.md** — six rows, every cell concrete enough
to hand to the illustrator as is. A cell that names a technique ("metaphor", "scene", "bold type")
instead of a picture is not filled.

| Column | What goes in | Example (title, «помогать клиенту можно легче» → облегчение) |
|---|---|---|
| How we show it | the image that carries the shared thought and feeling — a scene, a living person, words doing something, matter, a diagram-object, or nothing | психолог распахивает окно, ветер сдувает со стола стопку бумаг «проблемы» · женщина-психолог смеётся вместе с клиенткой, крупный план · «НЕ ЗАСТРЕВАЯ» вырывается из тесной рамки · тугой узел из нитей распускается в свободную ленту · запутанная линия становится прямой стрелкой · только огромное название и воздух |
| Staging | shot size, direction of movement, where the light comes from, where the words sit | крупный план, движение вправо-вверх, свет из-за спины, текст в нижней трети слева |
| Type | Cyrillic font pair (`typography.md`), size contrast, where the text sits, the accent device: one word in colour, a small label above the headline, dates in pills, a word crossing the edge | Unbounded 800 + Manrope; заголовок в 5 раз крупнее подписи; «ЛЕГЧЕ» цветом акцента; плашка «ОТКРЫТЫЙ ЭФИР» над заголовком |
| Volume | quiet / medium / loud | громко |

The six "How we show it" cells are six different worlds: no two rows share the kind of image, at
least two rows are loud and at least one is quiet. A living person in emotion and movement is one
or two rows, not all — and it is allowed: invented people are fine, only real people's faces are
not invented (the speaker comes from a real photo, `mockups.md` face rule, or as a placeholder).
The type column is Claude's decision, written into the prompt in words; the image model's default
(caps headline top-left, subtitle under it) is what you get when this column is empty.

Title slide prompt:
```
Сгенерируй изображение 1824x1024 (16:9): ТИТУЛЬНЫЙ СЛАЙД презентации, плоский кадр слайда без
рамки, без проектора и без интерфейса программы, уровень сильной дизайн-студии, не шаблон.
Весь текст на слайде — на русском, без ошибок, только строки из задания.
Тема: <what + for whom>. Кто смотрит: <audience line>. Где: <live talk | Zoom | file>.
Тексты: «…», «…», «…».
Мысль и чувство: <the shared line>. Что на картинке: <"How we show it" cell>.
Постановка кадра: <"Staging" cell>. Шрифт и текст: <"Type" cell>.
Настроение и подача: <mood → light, colour temperature, density, volume; skeleton>.
```
Slides 2 and 3 of a direction — one call each with its title slide as the reference (`--ref` is
mandatory, see mockups.md §0):
```bash
python <skill-dir>/scripts/codex_img.py "<prompt>" prototypes/mockups/m<N>-2.png --ref prototypes/mockups/m<N>.png
```
```
Приложенная картинка — титульный слайд презентации. Сгенерируй изображение 1824x1024 (16:9): другой слайд
ТОЙ ЖЕ презентации. Тот же стиль в точности: палитра, шрифты, фактуры, свет, манера изображений,
толщина линий. Композицию строй от содержания этого слайда, а не повторяй титульный.
Что на слайде и как устроена мысль: <the slide's words and its "how it's built" line from BRIEF.md>.
Мысль и чувство: <shared line>. Чем показываем в этом стиле: <the image for this slide, same kind as the row>.
Весь текст на русском, только строки из задания.
```
Title slides first, look at each, regenerate a broken one once (`--replace`).

**Sameness check, before the twelve follow-ups.** Put the six titles on one sheet in greyscale
(`PIL`: `ImageOps.grayscale`, 3×2) and look: any two with the same skeleton (where the text block
sits, what fills the frame) or the same kind of image? Redraw one of the pair with its row changed
— a different "How we show it" and staging, written in the prompt. **One redraw per direction,
once.** If a pair is still alike, go on and say so in one line when showing the gallery. Then the
twelve follow-ups in parallel. Across directions, if all six "structure" slides came out as the same three boxes with
arrows, the hint was lost — say in the prompt how this direction draws a process (a staircase, a
river, stamps on a line, one long sentence broken into steps).

**One slide per direction is not offered here.** A title slide says little about how a style holds
a number or a process; that is exactly where deck styles fail. Under real time pressure (a talk in
three hours) say so once and draw title slides only: the gallery then has `SCREENS` with one entry
and shows the six titles in one grid; after the pick the chosen title is the only style reference
in Step 6 — draw the two test slides first, look at them, then add them as references for the rest.

**No image generator** (or the user declines to wait for its reset): six directions written by hand
straight into `assets/deck-template.html` — one file per direction, its three test slides as frames,
fonts and colours per the six rows (read `frontend-aesthetics.md` and `typography.md` first). Check
each with `check.mjs --deck`, shoot them with `deck_export.py shots`, and put the shots into the
gallery. After the pick the chosen file *is* the deck: add the remaining slides to it (Step 7 without
plates). Step 8 then has no drawn slides to pair with: skip the sheet and look at the shots on their
own (a contact sheet of `_check/s*.png`). Say once that this path is weaker on taste.

## Step 5 — Gallery, pick, mix → `mockups.md` §2

The same `assets/gallery-template.html`, data block only: `PAGE.ratio:"16/9"`, `SCREENS` = the three
test slides by name (`{n:1,t:"Титул"},{n:2,t:"Цифра"},{n:3,t:"Схема"}`), each direction's `shots`
in that order, and in `T` say «слайд» instead of «экран» (`byScreen:"По слайдам"`, `screen:"Слайд"`,
`same:"Один и тот же слайд во всех вариантах, рядом."`). Passports, two modes, numbers not letters, «который ближе и что взять из других?» —
all as for a site. A mix: one edit call mixes the title slide (both files as `--ref`, the prompt says
which gives what), then the mix's
test slides 2 and 3 are drawn from that mixed title as above — saved as `m7*.png`, variant 7.

## Step 6 — Every slide drawn in the chosen style

The chosen direction's slides are the style references — all of them, as files:
`--ref prototypes/mockups/m<N>.png --ref prototypes/mockups/m<N>-2.png --ref prototypes/mockups/m<N>-3.png`. The test slides already **are** slides of the deck: copy them to their outline numbers
(`m<N>.png` → `prototypes/slides/s01.png`, `m<N>-2.png` → the number written in BRIEF.md) and don't redraw them.
For every other slide of the outline, one call:
```
Приложенные картинки — слайды выбранного стиля. Сгенерируй изображение 1824x1024 (16:9): слайд №<k> той же
презентации, тот же стиль в точности (палитра, шрифты, фактуры, свет, манера, постоянные элементы:
<logo / номер слайда / …>). Композицию строй от того, как устроена мысль этого слайда:
<"how it's built" line>. Что на картинке: <the image that tells this slide's thought, in the
chosen row's kind; for a plain slide from the rhythm mark — "без картинки, только текст и цвет">.
Постановка кадра: <shot size, movement, light, where the words sit>. Тексты: <exact words>.
Весь текст на русском, только эти строки.
```
Write the "Что на картинке" line for every slide into the outline before drawing — a concrete image,
not a technique name. Optional: if the chosen title's main image has a concrete weakness (the gesture
is limp, the light is flat), draw 2–3 versions that each change one named thing — angle, action,
scale — and let the user pick; don't draw versions without a named weakness.
(output path: `prototypes/slides/s<kk>.png`)
Calls run four at a time (the wrapper queues the rest); a slide to redraw keeps its name with `--replace`. Then look at the whole set as one strip: the
same hand on every slide; neighbouring slides that came out with the same composition — redraw one
of them with a different skeleton named in the prompt. Show the strip (a contact sheet of all
slides, `PIL` is enough) with one line and go on; it is the chosen direction, not a new vote.

**A long deck (over ~15 slides):** say the count of image calls once before drawing; a recurring
layout (a section divider, a quote) may be drawn once and reused with new words — that is a
constant element, not a template for content slides.

## Step 7 — Plates and the deck

1. **Plates** (`mockups.md` §4, `--ref prototypes/slides/s<kk>.png`): every drawn slide with all text removed, composition untouched →
   `prototypes/slides/s<kk>-plate.png`, copied to `prototypes/deck-assets/`. Compare each plate with its slide;
   list markers and small icons the edit removed are redrawn as SVG/CSS. A flat type-and-colour slide
   needs no plate — it is built in HTML/CSS.
2. **The deck** — copy `assets/deck-template.html` to `prototypes/deck.html`. Every slide is a
   1920×1080 frame; the plate is its background, every text line is live HTML in its own `.tx`
   block positioned in px of the frame, measured from the drawn slide (× 1920 / its width).
   Before writing CSS open the slide and write down positions, sizes, colours, type, as for a page.
   Fonts: the nearest Google Fonts with Cyrillic.
3. **Readability floor** (a 1920 slide shrunk into a Zoom window ~3×): body text ≥ 28px, captions
   ≥ 22px, headlines ≥ 56px, in px of the frame. `check.mjs --deck` fails anything under 22px; the
   28 and 56 are checked by eye on the sheet. The drawn slide smaller → enlarge and keep the
   composition; the floor wins over faithfulness, exactly as on the phone.
4. Several slides at once → one builder agent per 4–6 slides, each given BRIEF.md, its slides, plates
   and this step verbatim.

## Step 8 — Check before showing

```bash
node <skill-dir>/scripts/check.mjs prototypes/deck.html --widths 1920 --deck
python <skill-dir>/scripts/deck_export.py shots prototypes/deck.html prototypes/_check/
python <skill-dir>/scripts/deck_export.py sheet prototypes/slides/ prototypes/_check/ prototypes/_check/pairs.jpg
```
Fix every FAIL and the WARNs on slide text. The shots are every slide 1:1 (`s01.png …`), the sheet
puts each next to its drawn slide (drawn | built). Look at the pair for every slide: overlaps, text crossing the plate's objects, a line that wrapped differently, a
slide that grew denser than its picture. Two rounds usually leave only font metrics.

## Step 9 — Show and export

Serve `deck.html`, give the link and the contact sheet, one line on what the check found.
Complaints: about one slide → 2–3 variants of that slide; about the whole style → back to the gallery.

**Export after approval, in the format from Step 1:**
- **PDF** — one page per slide (the template sets `@page 1920×1080`):
  `python <skill-dir>/scripts/deck_export.py pdf prototypes/deck.html prototypes/deck.pdf` — it prints
  the page count next to the slide count; they must match. Open the PDF and look at it — this is the
  file the audience gets.
- **Google Slides, editable** — the deck stays the single source: render every slide's background
  with `deck_export.py shots … --notext`, measure every text line in the browser, build a PPTX with the background
  as a picture and live text boxes on top (`python-pptx`), upload with conversion, then export the
  Google file to PDF and compare line widths with the HTML. Google Slides silently drops letter-spacing,
  text glow and per-word shadow: bake small spaced labels into the background, put glow on the text
  box, not the word. Speaker notes from the outline go into each slide's notes. If the project has a
  transfer kit already, use it instead of writing a new one.
- **PowerPoint** — the same PPTX without the upload; open it (or its PDF) and check by eye.

Check on the final medium: the file the audience opens, not the HTML.

On approval add "Final Direction" to BRIEF.md: fonts, palette, constant elements, the chosen
direction's slides as the style references for any slide added later.
