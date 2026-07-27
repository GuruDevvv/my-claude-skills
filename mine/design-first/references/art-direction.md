# Art Direction — inventing a concept per prototype

The difference between "6 skins of the same page" and 6 distinct designs is **concept-first thinking**. A constraint ("warm tones, centered layout") limits the solution space but injects no idea. A concept ("a telegram from 1920s Berlin") is a creative seed everything else grows from.

## How to invent a concept

1. **Start from the emotion + audience** (Step 1), not the product category.
2. **Reach outside the category** for the metaphor — art movement, era, material, place, object, film, ritual. (Step 2 "out of category".)
3. **Name it in one vivid line.** If you can't say it in a sentence, it's not a concept yet.
4. **Derive everything from it:** the metaphor dictates palette (the colours *of that thing*), type (the voice *of that thing*), layout (the structure *of that thing*), motion (how *that thing* moves), imagery (what *that thing* looks like).
5. **Give each structured prototype a different concept** — different enough that they survive the grayscale test.

### Concept seeds (examples, not a menu)
- "Порог сна — погружение в глубину перед рассветом" (cinematic, vast, held-breath)
- "Утренний дневник — страница, куда переносишь сон, пока он не растаял" (literary, paper, unhurried)
- "Командное табло дедлайнов, которые нельзя пропустить" (urgent, scannable, departures-board)
- "Telegram from 1920s Berlin" / "Soviet brutalist poster" / "wabi-sabi imperfection" / "field naturalist's notebook" / "a fog-covered Baltic beach at 6am"
- B2B / trust / financial (a third register — neither atmospheric nor utilitarian): "промышленный контракт — стальная точность", "term sheet as a precision instrument", "an aerospace spec plate", "a private bank's letterpress letterhead". Distinctive ≠ emotional — gravity, precision, and restraint can be the concept.

### The concept-derivation table (fill it per prototype in the brief)
| From the concept → | Decide |
|---|---|
| Palette | the actual colours of the metaphor (not a SaaS palette) |
| Type | the voice — display + body that *sound* like the concept (Cyrillic-verified) |
| Layout | the structure the metaphor implies (a board? a book page? a film frame?) |
| Motion | how the metaphor moves (drifting fog? a count-down? a turning page?) |
| Imagery | what the metaphor looks like — or none, if the concept is pure type |

## Worked examples (from real tests)

### A) Emotional landing — "Сновидец" (dream journal), dark variant
- **Concept:** the threshold of sleep, descending into depth before dawn.
- **Palette:** abyssal indigo `#0a0e1a` → void `#070b14`, one warm dawn accent `#e8b08a`. No purple gradient, no glass.
- **Type:** Prata (didone display, Cyrillic) + Manrope.
- **Layout:** full-bleed atmospheric photo, content anchored bottom-left, oversized headline.
- **Motion:** drifting fog layers, breathing horizon glow, floating motes, Ken Burns, scroll parallax.
- **Imagery:** bespoke generated dawn-lake (Tier A), downloaded to `assets/`, with a dark gradient behind it for self-sufficiency.

### B) Same product, light variant — the morning journal
- **Concept:** a typeset literary journal — the quiet page before the dream melts.
- **Palette:** warm paper `#F0EBE0`, ink `#211d16`, one dusty terracotta accent `#9B5C42`. Grain overlay = paper texture.
- **Type:** Alegreya (literary serif, Cyrillic) + JetBrains Mono labels ("field-notes" voice). Deliberately *different fonts* from variant A.
- **Layout:** asymmetric editorial split — text left, framed photo right, Roman-numeral steps, hairline rules. Not centered.
- **Motion:** Ken Burns + slow light-sweep on the photo; restrained, editorial.

### C) Functional dashboard — "Олимпиад-трекер" (deadline tracker for parents)
- **Concept:** a season command-board — deadlines you cannot miss.
- **Palette:** warm paper + ink + one vermilion `#e2502e` for **urgency** (signal "act now"), kept off the inherited gold. Status colors stay functional (green/amber/red).
- **Type:** Unbounded (expressive display, big countdown numerals, Cyrillic) + Golos Text (Russian UI body — also *fixed a real bug*: the live app used DM Sans, which has no Cyrillic).
- **Layout:** dark sidebar + light content; a dominant dark "urgent this week" strip with giant countdowns answers "what must I do now?"; calm card feed below with status rails and days-left.
- **Motion:** count-up stats, urgency pulse, staggered card reveal — *functional*, not atmospheric.
- **Imagery:** **none** — it's a data dashboard; typography + color + hierarchy carry it.

### D) B2B / investor dashboard — "AM Technology" (investment proposal)
- **Concept:** "промышленный контракт — стальная точность" — a factory spec-sheet crossed with a high-stakes financial instrument. Trust through precision, not emotion.
- **Palette:** oxidized steel `#0d0f12`/`#141720`, cold steel hairlines, one gold "ink/seal" accent `#c9a84c`. Premium and precise, not flashy; no SaaS blue.
- **Type:** Cormorant Garamond (document gravitas, Cyrillic) + Onest (RU-native UI body) + JetBrains Mono (stamped-data labels).
- **Layout:** term-sheet metaphor — deal rows with monospaced labels read like a contract; asymmetric (spec table + status cards), not centered.
- **Motion:** functional — count-up on KPI figures, a pulsing gold "seal", staggered entrance. No atmosphere.
- **Imagery:** **none** — financial document; type + color + tabular hierarchy carry it.
- *(Validated in a blind artifact test: a fresh agent reached this from the skill files alone — the trust register is a real third category beyond emotional/functional.)*

## The lesson across examples
- Atmospheric products earn wow through **mood** (image + motion + palette).
- Functional products earn wow through **hierarchy + a strong organizing metaphor** — and explicitly **no decorative imagery**.
- "Calm/safe/minimal" almost never means "plain" — it means *trustworthy*. You can be deeply atmospheric (A) or richly editorial (B) while staying calm.
- The same product yields genuinely different designs only when each starts from a different **concept** — never from a different colour.
