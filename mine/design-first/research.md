# Research: выводим design-first на уровень «ВАУ»

Дата: 2026-06-13. Параллельный ресёрч (3 агента): аудит наших скиллов, vibecoding design-лайфхаки, MCP-ландшафт.

---

## Главный вывод (все три потока сходятся)

Скилл оптимизирован под **техническую корректность** (брейкпоинты, шрифты с кириллицей, перф анимаций, 13 пунктов чеклиста) и под **структурную вариативность** (навигация/layout/плотность). Но в нём **полностью отсутствует слой art direction** — нет творческой концепции у каждого прототипа, нет анти-slop директивы, нет экспрессивной типографики, нет цвета, выведенного из концепции.

Результат: прототипы **архитектурно разные, но эстетически одинаково-средние** — ровно то, что сообщество называет «AI slop». Технически безупречный прототип проходит все 13 пунктов чеклиста и при этом не вызывает никаких эмоций.

> «6 architecturally distinct but conceptually empty prototypes — correctly recognized by the user as "6 skins of the same page".»

---

## A. Корневые причины (из аудита)

1. **Оси диверсити — это UX-архитектура, а не творческая концепция.** «Sidebar vs top-bar» меняет расположение, но не эстетическую вселенную. Нет вопроса «какая ОДНА визуальная идея ведёт этот прототип?».
2. **«Free variant first» усиливает проблему.** «Best shot без ограничений» = модальный SaaS-дефолт (центр, Inter, градиент, CTA). Сгенерированный первым, он якорит остальные к самому генеричному выходу.
3. **ui-ux-pro-max каталог тянет в generic SaaS.** colors.csv = дефолтная палитра Tailwind, typography.csv = топ-10 пар с каждого дизайн-блога 2020-2024. Дефолт ui-reasoning.csv = «Hero + Features + CTA», «Minimalism», «Professional» — платоновский идеал генеричной SaaS-страницы.
4. **Слова «concept», «aesthetic» не встречаются ни разу.** «Bold» = только про вес шрифта. Нет понятия творческого тезиса.
5. **Hero-only scope убивает wow.** Hero — наименее отличимая часть страницы. Wow рождается из нарратива при скролле, который из above-the-fold снимка не оценить.
6. **Анимация механическая, не концептуальная.** «Particle system» — техника без смысла. Гайд почти весь про перф, а не про драматургию.
7. **Оценка награждает «корректно», а не «незабываемо».** 13 технических пунктов, 0 творческих гейтов.

**Что оставить (хорошее):** контекст-интервью (Step 1), Design DNA extraction (Step 2, «Signature moves»), grayscale-тест («убери цвет → должны отличаться»), вопрос про микс вариантов, gallery, BRIEF.md чекпоинт, параллельная генерация субагентами.

---

## B. Что реально даёт «ВАУ» (из vibecoding-ресёрча)

### Топ-уровень: anti-slop фингерпринт
Признаки AI-слопа: Inter/Roboto, фиолетовые градиенты на белом, центрированный hero, 3-колоночный grid фич, одинаковая тень на всех элементах, emoji-буллеты, равномерная серо-синяя палитра.

### Anthropic `<frontend_aesthetics>` блок — самый проверенный артефакт
Официальный анти-slop системный промпт из Claude Cookbook (platform.claude.com/cookbook). Прямо адресует «converge toward generic outputs». Ключевые директивы:
- **Typography:** избегать Inter/Roboto/Arial/system; брать отличительные шрифты.
- **Color:** один доминирующий цвет + резкие акценты > робкая равномерная палитра; вдохновляться IDE-темами и культурными эстетиками.
- **Motion:** один хорошо оркестрованный page-load со staggered-reveal > разбросанные микро-интеракции.
- **Backgrounds:** атмосфера и глубина (слои градиентов, текстуры, паттерны), не плоский solid.

### Топ-10 рычагов (ранжировано по impact/effort)
1. **Типографика-экстремумы** — заменить Inter на Fraunces/Playfair/Clash Display, вес 800 на 3x+ размере. Самый большой дифференциатор, 0 перф-стоимости.
2. **CSS grain/noise overlay** (SVG feTurbulence ~0.12 opacity) — физическая глубина, чистый CSS.
3. **Staggered page-load reveal** (animation-delay 0/100/200/300ms) — «designed», не «rendered».
4. **Насыщенный акцент на тёмной/нейтральной базе** вместо purple-on-white.
5. **Negative rules** — «no purple gradients, no white bg, no centered 3-col grid, no pill buttons».
6. **Scroll-driven анимации** (нативный `animation-timeline: scroll()`, без JS).
7. **Variable font weight по скроллу** — кинетическая типографика, ~10 строк CSS.
8. **Асимметричный editorial grid** — оверсайз-текст, выходящий за контейнер.
9. **Neo-serif + monospace пара** (Fraunces + JetBrains Mono).
10. **Кастомный курсор / split-char анимация** (для creative/portfolio).

### Divergence > iteration (Stanford parallel prototyping, Dow et al.)
Параллельные прототипы объективно разнообразнее и оцениваются выше, чем серийная итерация одного. Подтверждает нашу базовую идею — но требует **радикально разных эстетических констрейнтов**, не просто разных цветов. Паттерн промпта: «Version A: minimal/editorial, B: dark/technical, C: bold/asymmetric, D: warm/humanist — same content, radically different direction».

### DESIGN.md / token-seeding
Дроп markdown-файла с визуальным языком бренда (библиотека реплик Stripe/Linear/Apple/Anthropic — 69+ файлов) в корень + «read DESIGN.md before any UI code» = устойчивое качество через всю сессию.

### Тренды 2025-2026 (свежее, не хайп)
Tactile brutalism (0px, 1px борды), кинетическая типографика, grain+gradient слои, neo-serif revival, dark-first с отдельной палитрой, scroll-as-narrative, насыщенные хроматические палитры. Хайп/переюзано: glassmorphism (= «сделано в Lovable пресете»), 3D везде, микро-интеракции на каждом элементе, кастомные курсоры в SaaS.

---

## C. MCP-ландшафт (вердикт)

**Wow приходит из art direction на уровне промпта, а НЕ из MCP.** Большинство дизайн-MCP тянут в обратную сторону (generic shadcn) или ломают наш standalone-HTML констрейнт.

### SKIP
- **21st.dev Magic** — React/TSX only (подтверждено схемой инструмента), не поддерживается ~11 мес, открытая prompt-injection дыра, generic shadcn-эстетика. Ломает standalone HTML.
- **shadcn/ui MCP** — требует React+build, гомогенизирует всё в один shadcn-вид (Radix neutral, Inter, rounded-md).
- **Figma Dev Mode / Framelink** — полезны только если у юзера УЖЕ есть Figma-дизайн; React-output; Framelink security Grade D.
- **Spline/3D MCP** — нерабочие (у Spline нет публичного API). Three.js Claude пишет нативно.

### Worth integrating
- **Playwright MCP** (`@playwright/mcp`, Microsoft, Apache-2.0) — **главная находка для нашего workflow.** Скриншотит standalone HTML → PNG. Решает реальную боль: текущая gallery на iframe ломается на `file://`. Даёт настоящую визуальную галерею для сравнения. Нужен флаг `--allow-unrestricted-file-access`.
- **mcp-universal-icons** (MIT, 60K+ SVG) и **LottieFiles MCP** — опционально для ассетов, но Claude и так пишет inline SVG. Низкий приоритет.

### Стандалон-HTML совместимость
Playwright ✅, universal-icons ✅, Lottie ✅ | 21st/shadcn/Figma ❌ (React).

---

## D. Предлагаемое направление редизайна

Сдвиг парадигмы: **от «генератор корректных вариантов» к «арт-директор, который заставляет себя рисковать».**

1. **Art Direction слой** — у каждого структурного прототипа обязательная одностроковая творческая концепция (concept-first: «телеграм из Берлина 1920-х», не «warm earthy tones»). Вывести из неё цвет/шрифт/layout.
2. **Встроить `<frontend_aesthetics>`** в каждый промпт генерации прототипа (дословно, это артефакт Anthropic).
3. **Шрифтовой запрет + мандат** — never Inter/Roboto/Arial; всегда отличительный шрифт + вес-экстремумы + 3x скачки размера. Обновить кириллическую таблицу отличительными вариантами.
4. **Цвет из концепции, не из каталога** — поднять текущее предупреждение (line 430) из футноута в core-принцип ДО генерации. Понизить ui-ux-pro-max с «foundation» до «опциональный референс».
5. **Negative rules** в брифе и в промпте.
6. **WOW-гейт** — заменить/дополнить 13 технических пунктов творческими: «увидел бы незнакомец это и почувствовал что-то сильное?», «есть здесь хоть один ход, которого ты раньше не видел?».
7. **Атмосфера по умолчанию** — grain overlay + слои градиентов, никогда не плоский фон.
8. **Мотион переосмыслить** — staggered page-load + scroll-driven CSS вместо механического «particle system mandate».
9. **Scope** — 1-2 прототипа показывают 2-3 секции scroll-нарратива, не только hero.
10. **Переосмыслить «free variant»** — дать ему creative challenge (рискованная ставка), а не «polished and distinctive» (→ среднее).
11. **Playwright-галерея** — опциональный шаг: скриншоты прототипов в PNG-галерею.

---

---

## E. Изображения и анимация (отдельный ресёрч — ответ на вопрос «может ли скилл сам находить картинки?»)

**Да, может — несколькими способами. Текущий скилл этого не делает вообще (только CSS/canvas-декор), и это половина причины «плоскости».**

### Tiered-стратегия изображений

| Tier | Метод | Когда | Ключ | Standalone |
|---|---|---|---|---|
| **0** | **Lorem Picsum** `picsum.photos/seed/{slug}/1600/900` | дефолт, мгновенно | нет | hotlink (Fastly CDN, стабилен) |
| **0b** | **Pollinations.ai** `image.pollinations.ai/prompt/{концепт}?width=..&seed=..` | нужна картинка под концепцию | нет | hotlink, 5-10с первый загруз |
| **1** | **Pexels / Unsplash API** | есть `PEXELS_API_KEY`/`UNSPLASH_ACCESS_KEY` в env, нужно фото по ключевику | да (free) | hotlink |
| **2** | **AI-генерация + `curl` локально** (Pollinations или **Higgsfield MCP `generate_image`** — доступен в сессии) | «standalone/shareable» или нужна bespoke-картинка под концепт | MCP/нет | ✅ полностью |
| **3** | юзер дал свои картинки в `./assets/` | есть ассеты | — | ✅ |

**Важные факты:** `source.unsplash.com` **МЁРТВ** (закрыт июнь 2024) — не использовать. Pixabay запрещает hotlink (URL живут 24ч). LoremFlickr нестабилен. Picsum не умеет поиск по ключевику → держать в скилле таблицу curated ID (architecture→id/1084, beach→id/559 и т.д.) или использовать seed для стабильности.

**Дефолт для прототипа:** Tier 0 (Picsum) для мгновенности; апгрейд до Tier 2 (download), когда юзер просит shareable или доступен Higgsfield. Для standalone-принципа правило: прототип эфемерен → hotlink ок; deliverable → скачать локально.

### Богатый мотион без тяжёлых библиотек (dependency-free)

4 дефолта в каждый прототип (inline CSS + JS-фолбэк):
1. **Ken Burns** на hero-фото (`scale(1)→scale(1.12)` + translate, 20s) — самый высокий ROI, делает любое реальное фото живым, поддержка везде.
2. **Reveal-on-scroll** — нативный `@supports (animation-timeline: view())` + IntersectionObserver-фолбэк (Firefox ~18% ещё не поддерживает scroll-driven по дефолту).
3. **Animated gradient** (`background-size:400%` + shift) — богатый фон без ассетов, когда нет фото.
4. **Scroll progress bar** (`animation-timeline: scroll(root)`).

Плюс: **View Transitions API** (Baseline с окт 2025, Chrome/FF/Safari) — анимированные переходы секций/табов/модалок, ~5 строк JS с фолбэком. **CSS-only parallax** (perspective trick) для всех браузеров. **Видео-фон**: Coverr/Pexels Video/Mixkit — нет стабильного hotlink, только скачать локально (`<video autoplay muted loop playsinline>`).

**Lottie-плеер** (CDN ~60KB) — единственное оправданное исключение из «no CDN libs», когда сложная JSON-анимация является центром прототипа. В остальных 90% — CSS + View Transitions + Ken Burns хватает.

---

## Источники
v0/Lovable/Claude prompting, Anthropic Cookbook frontend_aesthetics, MindStudio anti-slop, DESIGN.md (chatgate.ai), Stanford parallel prototyping (Dow et al., ACM TOCHI), MDN scroll-driven animations + View Transitions (web.dev Baseline), caniuse, web design trends 2026 (Kontra, Fireart), MCP reviews (ChatForest, MarkTechPost), Playwright MCP (Microsoft GitHub), Lorem Picsum, Pollinations APIDOCS, Unsplash/Pexels/Pixabay API docs, Higgsfield MCP. Полные URL — в логе сессии.
