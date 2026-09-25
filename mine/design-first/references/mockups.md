# Mockups — the look is drawn by an image model, then built as a live page

## Why this path

Six blind rounds with the owner (Sept 2026, scores kept in the test protocol):
- HTML prototypes written by the coding model — never a "wow" in three rounds; two quite different
  rule sets tied on taste (12:12). The ceiling was the coding model's own visual taste, not the rules.
- First-screen **mockups drawn by an image model** from the same brief — mean 1.67 vs 1.33, and the
  **only "wow" in six rounds** (a torn-paper, stamped, big-serif pottery screen no HTML agent produced).
- Transfer: a live page built over the mockup (text removed → background plate, live text on top) was
  judged **"the same" as the mockup in all three pairs** on desktop. On the phone the same page dropped
  to 0–1 — until the phone got **its own vertical mockup**; then phone = mockup (2 = 2) in all three.
- A vision "critic" agent ranking prototypes did **not** track the owner (rank correlation −0.07) —
  so there is no automatic pre-selection: the user picks from the gallery.

## 0. Check the generator (once per session)

Any image tool the environment has — Codex CLI `image_gen` (gpt-image-2), an image MCP. One test call;
never assume a vendor. **No generator → use the fallback in SKILL.md (HTML first screens).**

Codex CLI recipe (Bash, one call per image, calls may run in parallel):
```bash
mkdir -p prototypes/mockups/_logs && cd prototypes/mockups && codex exec --skip-git-repo-check -o ../_logs/m1.txt \
  "ИСПОЛЬЗУЙ СВОЙ ВСТРОЕННЫЙ ИНСТРУМЕНТ image_gen (системный скилл imagegen, модель gpt-image-2, через подписку — OPENAI_API_KEY НЕ НУЖЕН). <prompt>. Сохрани как m1.png в текущей папке. В ответе только полный путь к файлу." < /dev/null
```
If the file isn't in the folder, take the path Codex printed (`~/.codex/generated_images/...`) — that
exact path, never "the newest file" (parallel calls collide). Delete any `.agents`/`.git` Codex leaves.
Cost: ~20–25k tokens per image on a Plus plan; a full run is ~9 images (6 + phone + 2 plates).

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

## 2. Gallery → pick → mix

Gallery page `prototypes/mockups/gallery.html`: the six images in a numbered grid, each opens large on
click, a light neutral page.
Serve it locally (`python -m http.server <free port> --bind 127.0.0.1`), confirm with curl, give the
link. Ask: "which one is closest, and what would you take from the others?" A mix ("as №3 but the
palette of №5") is **one more edit call** with both files named in the prompt — not a new round.

## 3. Phone mockup (always — never shrink the desktop one)

From the chosen desktop file as reference:
```
Файл <chosen>.png — макет десктопной версии. Сгенерируй по нему вертикальный макет 1024x1536 той же
страницы для ТЕЛЕФОНА (экран 390px, чистый скриншот без рамки телефона): тот же стиль, палитра, шрифты,
фактуры, те же тексты. <Landing: заголовок, подзаголовок и кнопка видны без прокрутки, изображение и
фактуры собраны в вертикальную композицию так же сильно, как в образце, а не фото под текстом.>
<Tool: одна колонка — переключатель (мастер/день/раздел) сверху, список ниже, главное действие рядом.>
```

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
