# Mockups — the look is drawn by an image model, then built as a live page

## Why this path

Seven blind rounds with the owner (Sept 2026, scores kept in the test protocol):
- HTML prototypes written by the coding model — never a "wow" in three rounds; two quite different
  rule sets tied on taste (12:12). The ceiling was the coding model's own visual taste, not the rules.
- First-screen **mockups drawn by an image model** from the same brief — mean 1.67 vs 1.33, and the
  **only "wow" in six rounds** (a torn-paper, stamped, big-serif pottery screen no HTML agent produced).
- Transfer: a live page built over the mockup (text removed → background plate, live text on top) was
  judged **"the same" as the mockup in all three pairs** on desktop. On the phone the same page dropped
  to 0–1 — until the phone got **its own vertical mockup**; then phone = mockup (2 = 2) in all three.
- Acceptance round, three new topics, old skill (4 HTML screens) vs this path (6 mockups): this path
  won all three (best screen 3 vs 2, 2 vs 2 with more good ones, 3 vs 1); both new "wow"s were mockups.
- A vision "critic" agent ranking prototypes did **not** track the owner (rank correlation −0.07) —
  so there is no automatic pre-selection: the user picks from the gallery.

## 0. Check the generator (once per session)

Any image tool the environment has — Codex CLI `image_gen` (gpt-image-2), an image MCP. One test call;
never assume a vendor. **No generator → use the fallback in SKILL.md (HTML first screens).**

Codex CLI recipe — the lean wrapper `<skill-dir>/scripts/codex_img.py` (one call per image), run from
the project folder so relative output paths land in the project:
```bash
python <skill-dir>/scripts/codex_img.py "<prompt>" prototypes/mockups/m1.png [--ref plate.png] [--replace]
```
It starts Codex bare (no user config, no AGENTS.md, no plugins/hooks, cheap dispatcher model
`gpt-6-luna`, falls back to `gpt-6.1-sol`), forbids reading files, viewing the result and polling,
takes the image from that run's own `generated_images/<thread>` folder (no collisions) and copies it
to the target. At most 4 run at once, the rest queue. Measured 16.10.2026: ~60k tokens per image on
Luna, vs 150k–1.3M per image with a plain `codex exec` on Sol (it loaded ~43k of instructions, read
skill docs and memory, then polled "done?" ~10 times, resending everything each time — 28 mockups ate
a whole Plus window in 28 minutes). An existing target file is refused (no silent overwrite); to **redraw** a picture pass `--replace` —
after a successful run the old file is kept as `m1.v1.png` (`v2`, …). A new round goes into a new
folder (`mockups/round2/`), not over the first one.
**Never use a plain `codex exec` for images.**
**Usage limit hit** ("You've hit your usage limit… try again at <time>") → don't fall back silently:
tell the user the reset time and wait for it, or ask whether to go on with the HTML fallback — it is
measurably weaker on taste, so it is their call. Three parallel projects × 6 mockups exhausted a Plus
window in one night.

## 1. Six different mockups

**Fix the words first.** Headline, subheadline, CTA (and for a tool: the realistic data — names, times,
statuses) are written once in BRIEF.md and are **identical in all six** — the user compares design,
not copy. Keep them short; long copy garbles in generated images.

**Six different takes, not six palettes.** Assign each mockup one row; the layout skeletons must differ
(strip the colour — they must still look different):

| # | Take | Skeleton hint |
|---|---|---|
| 1 | mood hypothesis 1, the genre done excellently | split: text column + large photo |
| 2 | mood hypothesis 2, opposite light (dark if 1 is light) | full-bleed photo, text over it |
| 3 | mood hypothesis 3 | editorial / asymmetric grid |
| 4 | type-led poster — no photo, typography and colour are the picture | centred or poster crop |
| 5 | texture: collage, torn paper, stamps, hand-drawn marks, illustration | layered, asymmetric |
| 6 | a concept from the topic's own objects (concepts.md) | the object *is* the layout |

**Work tools and dashboards:** vary the organising idea instead — grid journal, action queue, timeline,
board, floor plan, calendar — plus light/dark and warm/cold. Real-looking data, no photos, readable in
the 2 seconds the user actually looks.

**Prompt template** (desktop):
```
Сгенерируй изображение 1536x1024: макет ПЕРВОГО ЭКРАНА веб-страницы на десктопе 1440px, как чистый
скриншот сайта без рамки браузера, уровень сильной дизайн-студии, не шаблон конструктора.
Весь текст на макете — на русском, без ошибок, только строки из задания.
Тема: <what + for whom, one line>. Кто смотрит: <audience line from the vibe card>.
Тексты: заголовок «…», подзаголовок «…», кнопка «…».
Настроение и подача: <this row: mood → light, colour temperature, human presence, density; skeleton>.
```
Look at every result before the gallery: the mood matches its row, nothing is cut off, people look
natural. Misspelled Cyrillic doesn't matter for the build (all text becomes live HTML) but distracts in
the gallery — regenerate once if it is glaring. **Don't curate by your own taste** — the critic test
showed it doesn't predict the user; drop only broken images.

## 1a. Screens 2 and 3 of every direction

Why three: the owner's reference gallery showed every variant on the same six slides, picked because
they test different things (emotion, a list, a path, complex graphics, a pause, cards), and the owner
confirmed (Oct 2026) that choosing is easier from several screens than from one. Three is the smallest
set that still tests different things; it has not been measured in a blind round yet.

Each follow-up is one call with the direction's first screen as the reference:
```
Файл m<N>.png — первый экран страницы. Сгенерируй изображение 1536x1024: <второй | третий> экран ТОЙ ЖЕ
страницы, чистый скриншот без рамки браузера. Тот же стиль в точности: палитра, шрифты, фактуры, свет,
манера изображений, толщина линий, скругления. Весь текст на русском, только строки из задания.
Что на экране: <the screen's content from BRIEF.md, word for word>.
Сохрани как m<N>-2.png | m<N>-3.png.
```
Look at each next to its first screen: the same hand, not a new direction; a follow-up that drifted is
regenerated once. The diversity rule holds across directions on every screen — if the six content
screens all came out as the same three-card row, the skeleton hint was lost: say in the prompt how
this direction lays a list out (a ledger, a staircase, stamps on paper, one long line).

## 2. Gallery → pick → mix

Gallery page `prototypes/mockups/gallery.html`: copy `<skill-dir>/assets/gallery-template.html` and
fill only its data block (`PAGE`, `SCREENS`, `VARIANTS`) — don't write a gallery from scratch. The
template is the owner's reference gallery (a deck choice made for a client in September 2026) with the
client's content taken out. What it carries and why:

- **Every image opens large on click.** Directions carry numbers, not letters: the user answers "№3
  with the palette of №5".
- **A passport for every direction:** a name, the idea in one or two plain sentences (what
  the person sees, not design terms), palette in words, font pair, the feeling in three words. Taken
  from the mockup's row and the vibe card. It describes; it never ranks or recommends — no "the
  strongest", no order by your taste (the critic test: your ranking doesn't predict the user's).
- **No header.** The page opens straight on the variants (and the mode switch); the owner found a
  big title with a "how to look" box ugly and useless (19.10.2026). The question goes into the chat.
- **"Open live" button** only on a variant that already has a live page (the HTML fallback path, or a
  built page after the pick). A drawn mockup has none — leave `live` out.
- **A rejected round stays on the page** (`round:"old"`), under a heading with the user's own reason —
  "none is close → new six" must show what was left behind.
- **Status block** (`PAGE.status`) once a direction is picked: what was chosen, what was changed, the
  link to the built page. The gallery then doubles as the record of the choice.
- **Two modes.** "By variant": each direction whole, its three screens in a row. "By screen": one
  screen in all six directions side by side — the mode people actually choose in. Fill `SCREENS` with
  the three screen names from BRIEF.md and each variant's `shots` in the same order
  (`["m1.png","m1-2.png","m1-3.png"]`). With one screen per direction (the time-pressure path) the
  switch disappears and the six images sit in one grid.

`PAGE.ratio`: `3/2` for drawn mockups, `16/10` for 1440×900 screenshots, `16/9` for slides. The
page's own look (dark, quiet, one amber accent) stays as it is — it frames the mockups and must not
compete with them; don't restyle it per project.
Serve it locally (`python -m http.server <free port> --bind 127.0.0.1`), confirm with curl, give the
link. Ask: "which one is closest, and what would you take from the others?" A mix ("as №3 but the
palette of №5") is not a new round: **one edit call mixes the first screen** with both files named in
the prompt, then the mix's other screens (if the round has three) are drawn from that mixed first
screen exactly as in §1a — so all screens of the mix share one hand. Save the mix as `m7.png`,
`m7-2.png`… and add it to the gallery as variant 7.

## 3. Phone mockup (always — never shrink the desktop one)

From the chosen desktop file as reference:
```
Файл <chosen>.png — макет десктопной версии. Сгенерируй по нему вертикальный макет 1024x1536 той же
страницы для ТЕЛЕФОНА (экран 390px, чистый скриншот без рамки телефона): тот же стиль, палитра, шрифты,
фактуры, те же тексты. Размеры для телефона: основной текст не мельче 36 px, подписи не мельче 30 px,
кнопка не ниже 115 px в этой картинке шириной 1024 (это 14 px, 11 px и 44 px на экране 390).
<Landing: заголовок, подзаголовок и кнопка видны без прокрутки, изображение и
фактуры собраны в вертикальную композицию так же сильно, как в образце, а не фото под текстом.>
<Tool: одна колонка — переключатель (мастер/день/раздел) сверху, список ниже, главное действие рядом.>
```

Why the sizes: in round 7 the builder had to enlarge 8–11 px mockup text to the readability floor, the
composition shifted, and the owner preferred the mockup on 2 of 3 phones (desktop stayed "the same" 3/3).
A phone mockup drawn at readable sizes needs no enlarging. Redrawn that way (and compared at the
mockup's own height, not a taller frame): both phones judged "the same" as their mockups; where the
image model still drew below the floor and the builder enlarged, the owner still judged it "the same"
— the readability floor wins over pixel faithfulness.

## 4. Plates — the mockup without its text

For each chosen mockup (desktop and phone) that has raster art — photo, paper or stamp texture,
illustration:
```
Возьми файл <m>.png и отредактируй: убери ВЕСЬ текст, заголовки, подписи, кнопки, строку поиска и
штрихи под заголовком — на их месте чистый фон той же фактуры и цвета. Всё остальное (фото, люди,
бумага, пятна, растения, фигуры, свет, кадрирование, размер) оставь в точности как было.
Сохрани как <m>-plate.png.
```
Copy the plates into `prototypes/<scope>-assets/` for the build.
Open the plate and compare with the mockup: composition must be unchanged. Small decorations the edit
removed (a heart, a sprig, a squiggle) are redrawn as SVG in the build. A pure-interface mockup (tool,
dashboard) needs no plate — it is built entirely in HTML/CSS; a decorative bit can be cropped out of the
mockup with PIL.

## 5. Images inside the next sections

Further sections may need their own pictures: generate them in the chosen mockup's style (same light,
palette, manner), no text in the image. No generator → Openverse (`https://api.openverse.org/v1/images/?q=…`,
free, no key; record creator/license). Never hotlink; download to `assets/`. Put a palette-coloured
background behind every image so a failed load never leaves an empty panel. Dead sources: Pollinations
no-key (402), source.unsplash.com (shut down), Pixabay hotlinks (expire).
