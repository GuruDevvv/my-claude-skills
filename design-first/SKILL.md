---
name: design-first
description: Generate 4-6 diverse HTML design prototypes before coding. Interview → references → parallel prototypes → gallery comparison → user picks → build. Use when: "сделай дизайн", "подготовь макет", "давай займёмся дизайном", "нарисуй страницу", "make a design", "design this", "prepare design", "how should this look", "visual direction", "prototypes", "варианты дизайна". Scope: landing pages, dashboards, portfolios, forms, apps, components — any visual/UI work. Do NOT use for: code review, debugging, backend logic, data processing, or non-visual tasks.
---

# Design First

A structured process for exploring visual direction before writing production code. Built for people who aren't designers but need professional-quality results.

The core idea: **don't commit to one design. Generate diverse options, compare, pick the best, then build.** This eliminates the #1 problem in vibe-coding — getting stuck with the first thing that came out.

---

## How it works (overview)

```
Interview → References → Design Brief → Prototypes → Evaluation → Selection → Refine & Build
   5 min      optional     checkpoint     parallel       user        mix         go
```

---

## Step 1 — Context Interview (mandatory)

Before touching any code or visuals, understand what you're designing. Ask the user these questions (adapt phrasing to the conversation, don't interrogate):

### Must-know
1. **What is this?** (landing page, dashboard, form, app screen, component...)
2. **Who will use it?** (age, context, device — especially: mobile-first or desktop?)
3. **What should the user FEEL?** (trust, urgency, calm, excitement, premium, playful...)
4. **What should the user DO?** (buy, sign up, fill a form, explore, read...)
5. **Any existing brand/style?** (colors, fonts, logo, existing site, references)

### Good-to-know
6. **What content exists?** (headline, subheadline, CTA text, images, copy blocks)
7. **Any anti-references?** (what you definitely DON'T want — "not corporate", "not generic SaaS")
8. **Technical constraints?** (vanilla HTML? React? Specific framework?)

If user already shared context in conversation — extract answers from it first, then ask only what's missing. Don't repeat what you already know.

**Why this matters:** A non-designer often jumps straight to "make it pretty" without thinking about audience and goals. These questions shape every decision downstream — color warmth, typography weight, spacing density, animation intensity. Without them you're decorating, not designing.

---

## Step 2 — Reference Analysis

### If user provided references (images, URLs, screenshots):

Analyze each reference and extract a **Design DNA profile**:

| Aspect | What to look for |
|--------|-----------------|
| **Mood** | Dark/light, warm/cool, minimal/rich, quiet/loud |
| **Color strategy** | Dominant color, accent color, background tone, contrast level |
| **Typography** | Serif/sans/display, weight range, size hierarchy, letter-spacing |
| **Layout** | Density (airy vs packed), alignment (centered vs asymmetric), grid vs freeform |
| **Signature moves** | What makes it unique? Glassmorphism? Grain texture? Bold type? Gradients? Illustrations? |
| **Animation vibe** | Static, subtle hover, cinematic, playful bounce, particle effects |

Present this to the user as a short summary: "Here's what I see in your references: [2-3 sentences]". This builds shared vocabulary.

### If no references:

Ask: "Show me 1-2 examples of sites/designs you like — even from a completely different industry. I need to understand your taste, not copy someone's layout."

If user can't provide any, that's fine — work from the emotional direction (Step 1 answers) and maximize spread on **Temperature** and **Layout** axes in Step 3, as these create the most visible difference between prototypes.

---

## Step 2.5 — Design Brief (checkpoint)

Before generating anything, persist all decisions from Steps 1-2 into a file. This protects against context loss in long sessions and gives the user a correction point before 6 prototypes are generated.

**Create `prototypes/BRIEF.md`** with this structure:

```markdown
# Design Brief: [Project Name]

## Context
- **What:** [type of page/component]
- **Audience:** [who, age, device, context]
- **Emotion:** [what they should feel]
- **Action:** [what they should do]
- **Tech:** [vanilla HTML / React / etc.]

## Brand & Style
- **Existing assets:** [colors, fonts, logo — or "none"]
- **References:** [list with 1-line DNA summary each]
- **Anti-references:** [what to avoid]

## Content
- **Headline:** [exact text or "TBD — write plausible placeholder"]
- **Subheadline:** [exact text or TBD]
- **CTA:** [exact text or TBD]
- **Images/media:** [available assets or "generate decorative only"]

## Prototype Plan
| Variant | Direction | Key axes | Font strategy | Color strategy |
|---------|-----------|----------|---------------|----------------|
| 0 (free) | AI's best shot | No constraints — full creative freedom | — | — |
| A | [2-3 words] | Temperature: warm, Layout: centered | Elegant serif | Earth tones |
| B | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |
```

**Show the brief to the user** and ask: "This is what I'll build from. Anything to change before I generate 6 prototypes?"

Only proceed to Step 3 after user confirms (or says "go" / "looks good" / any affirmative).

---

## Step 3 — Generate Prototypes

### Visual quality: ui-ux-pro-max integration (optional, recommended)

This skill handles process and diversity. For enhanced visual quality, it can delegate style/palette/font selection to **`ui-ux-pro-max`** (67 styles, 96 palettes, 57 font pairings, Python CLI).

**Before generating prototypes, check if `ui-ux-pro-max` is available:**

```bash
python3 skills/ui-ux-pro-max/scripts/search.py --help 2>/dev/null && echo "AVAILABLE" || echo "NOT AVAILABLE"
```

**If available** — run design system generation for each prototype direction:
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<style keywords>" --design-system -p "<project>"
```
Use its output (palette, fonts, effects, anti-patterns) as the foundation for each prototype. This produces noticeably higher quality results.

**If not available** — proceed without it. Use:
- The Cyrillic font table below (Step 3 → Cyrillic font safety)
- The diversity axes table (Step 3 → Diversity strategy)
- Your own knowledge of color theory, typography, and layout
- References from Step 2 as the primary style guide

The skill is fully functional without `ui-ux-pro-max`. The dependency improves quality, not enables it.

### What to generate

Each prototype is a **standalone HTML file** — self-contained, opens directly in browser, no dependencies except Google Fonts CDN.

Prototype scope depends on what you're designing:
- **Full page** (landing, homepage): generate the Hero section only (above the fold). Hero sets the tone — if it works, the rest follows.
- **Component** (card, form, modal, navbar): generate the component in context (with enough surrounding UI to feel real).
- **Dashboard/app**: generate one key screen or panel.

### How many variants

**Default: 6 prototypes (1 free + 5 structured). Minimum: 4 (1 free + 3 structured).**

The 6 prototypes have two distinct types:

#### Variant 0 — "Free" (generated FIRST)

The first prototype is generated **without diversity axes, without checklists, without forced constraints**. Give it the full context from Steps 1-2 (audience, emotion, action, brand, references) and let the AI produce its best single shot — the design it would make if there were no skill process.

**Why first:** If generated after the structured variants, it gets contaminated by their patterns. Generated first, it's an honest baseline — sometimes it's the best one.

**File naming:** `[scope]-0-free.html` (e.g., `hero-0-free.html`)

**Prompt for free variant:** "Using all the context from the design brief, create the best possible hero section. No constraints on style, layout, or technique. Use your best judgment for fonts, colors, layout, and effects. Make it as polished and distinctive as you can."

#### Variants A–E — Structured (5 prototypes)

The remaining 5 prototypes follow the diversity strategy below. Each must be *genuinely different* — not the same layout with tweaked colors. Different fonts, different color strategies, different visual techniques.

When 3 structured (+ 1 free = 4 total) is enough:
- Simple components (button, card, form)
- User gave very specific references and the direction is clear
- Tight time constraints (user explicitly says "quick")

### Diversity strategy

Each structured prototype should vary on at least 2 of these axes:

| Axis | Example range |
|------|--------------|
| **Temperature** | Warm earthy tones ↔ Cool blues/grays ↔ High-contrast dark |
| **Typography** | Elegant serif ↔ Clean sans ↔ Bold display/statement |
| **Density** | Airy with lots of whitespace ↔ Rich and detailed |
| **Technique** | Glassmorphism, gradients, grain texture, illustration, photography, minimal flat, brutalist |
| **Animation** | Static/minimal ↔ Floating elements ↔ Particle systems ↔ Cinematic effects (see Animation Guide below) |

**Animation rule: at least 2 of 6 prototypes must have VISIBLE, dynamic animation** — not just fade-in-on-scroll or subtle hover. The audience notices movement first. Static pages feel dead next to animated ones. Allocate animation across the spread:
- **2-3 prototypes: static or minimal** (subtle hover, gentle fade-in)
- **2-3 prototypes: noticeable animation** (particles, floating objects, glowing pulses, animated gradients)
- **At least 1 prototype: cinematic/dramatic** (particle system, animated shapes, visual spectacle)

If references exist, allocate roughly:
- **Half** of structured prototypes inspired by references (extracting and remixing their DNA)
- **Half** exploring different directions (the user might not know they want something unexpected)

### Technical requirements for each prototype

```html
<!-- Structure of every prototype file -->
<!DOCTYPE html>
<html lang="...">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Project] — Variant [Letter]: [Style Name]</title>
  <!-- Google Fonts only -->
  <style>
    /* All CSS inline — no external files */
    /* CSS custom properties for colors/fonts */
    /* Mobile-first: base styles = mobile, @media for desktop */
    /* CSS animations: @keyframes for floating, pulsing, gradient shifts */
  </style>
</head>
<body>
  <!-- Real content, not lorem ipsum -->
  <!-- If user provided text — use it -->
  <!-- If not — write plausible placeholder that matches the project -->

  <!-- For animated variants: canvas + inline script -->
  <canvas id="fx" style="position:fixed;inset:0;pointer-events:none;z-index:0;"></canvas>
  <script>/* Particle system or other effects — see Animation Guide */</script>
</body>
</html>
```

**Critical: mobile-first.** Base CSS targets phone screens. Desktop layout via `@media (min-width: 768px)`. The user's audience likely comes from mobile (social media, messengers). A prototype that only looks good on desktop is a failed prototype.

**Use real content.** Lorem ipsum kills design evaluation. If the user gave you headlines and CTA text — use them. If not — write realistic copy that fits the project's tone.

**Desktop screen utilization.** AI-generated prototypes consistently waste space on 1440px+ screens. This is the #1 visual quality problem. Rules:

1. **Add a wide breakpoint** — at minimum `768px` and `1440px`. At 1440px+, widen the content and increase heading size.
2. **Don't hard-cap text width below 500px** — subtitle/description `max-width` should be at least `500px` on desktop (or use `min(60%, 600px)`).
3. **Hero content wrapper: 1100-1400px on desktop** for two-column/editorial layouts, **800-1000px** only for single-column centered text.
4. **At least 2 of 6 prototypes must use a non-centered layout** — split (text left + visual right), editorial columns, asymmetric grid. Centered layouts are overused by AI. On a 1440px screen, a centered 400px block looks broken.
5. **On 1440px+, heading font-size should be 56-80px** — large type fills space and looks intentional. Small headings on wide screens = phone layout stretched.

Keep CSS simple — use fixed values at each breakpoint. Don't overuse `clamp()` on every property; it makes spacing unpredictable and breaks visual rhythm.

**Cyrillic font safety.** When generating content in Russian (or any Cyrillic language), only use Google Fonts with `cyrillic` subset. Organized by visual character to ensure diversity across prototypes:

| Category | Fonts (all Cyrillic-safe) | Character |
|----------|--------------------------|-----------|
| **Elegant serif** | Cormorant Garamond, Playfair Display, Lora | Thin, refined, classic |
| **Sturdy serif** | Merriweather, PT Serif, Literata, Bitter, Noto Serif | Heavier, grounded, readable |
| **Clean sans** | Inter, Raleway, Jost, Commissioner | Neutral, modern, light |
| **Bold/geometric sans** | Montserrat, Nunito, Rubik, Outfit, Manrope | Rounder, punchier, more personality |
| **Condensed/display** | Oswald, Fira Sans, PT Sans, Philosopher | Tight, editorial, statement |
| **Expressive** | Unbounded, Podkova, Marmelad, Kurale, Caveat | Unusual, memorable |

**Font selection principle:** Choose fonts that serve each prototype's *design concept*, not for diversity's sake. If a variant's idea calls for elegant serif — use it, even if another variant already does. But if every variant ends up with the same pairing (e.g., elegant serif + light sans), that's a sign the concepts themselves aren't different enough. The table above is a reference to expand your palette, not a checklist to tick.

For Latin-script projects (English, etc.), any Google Font is fine — the table above is specifically for Cyrillic safety.

**Do NOT use** fonts without Cyrillic support for Russian content (e.g., DM Serif Display, DM Sans, Fraunces, Space Grotesk, Libre Baskerville, Cinzel). If unsure — check fonts.google.com for "Cyrillic" in Languages. Broken Cyrillic (□□□) instantly kills the prototype.

### Animation guide

Two approaches: CSS-only (for moderate effects like floating elements, gradients, shimmer) and inline JavaScript Canvas (for dramatic effects like particle systems, lightning, constellations).

See `references/animation-guide.md` for code templates, particle system boilerplate, and effect recipes.

#### Performance rule

Animation must not kill mobile. Rules:
- **Canvas particles: max 60 on mobile, up to 120 on desktop** — check `window.innerWidth < 768` and reduce count
- **CSS animations: avoid animating `width`, `height`, `top`, `left`** — only `transform` and `opacity` (GPU-composited)
- **Add `prefers-reduced-motion` media query** — disable or reduce animation for accessibility:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; }
}
```

#### What NOT to do
- Don't use animation libraries via CDN (GSAP, anime.js, three.js) — they add load time, break standalone principle, and CDN links rot
- Don't animate text content (scrolling text, typewriter on load) — it delays comprehension
- Don't use `setInterval` for animation — always `requestAnimationFrame`
- Don't make CTA button bounce/shake — it looks cheap and desperate

### Pre-generation checklist

**Scan this before writing each prototype.** Every item here was a real failure mode in testing.

- [ ] **Mobile-first CSS** — base styles = phone, `@media (min-width: 768px)` for tablet, `@media (min-width: 1440px)` for desktop
- [ ] **Two breakpoints minimum** — 768px and 1440px
- [ ] **Real content** — no lorem ipsum. Use brief text or write plausible copy
- [ ] **Heading 56-80px on 1440px+** — small headings on wide screens = phone layout stretched
- [ ] **Text max-width >= 500px on desktop** — don't hard-cap below that
- [ ] **At least 2 of 6 non-centered layouts** — split, editorial, asymmetric
- [ ] **Hero wrapper 1100-1400px** for multi-column, **800-1000px** only for single-column centered
- [ ] **Cyrillic fonts verified** (if RU content) — check the table below, no DM Sans/Cinzel/Fraunces
- [ ] **No clamp() overuse** — fixed values per breakpoint for predictable rhythm
- [ ] **Animation diversity** — at least 2 of 6 prototypes have VISIBLE animation (particles, floating elements, animated gradients, glowing pulses). At least 1 has a dramatic canvas-based effect. Check the Animation Guide above.
- [ ] **Animation performance** — canvas particles ≤60 on mobile, only `transform`/`opacity` in CSS animations, `prefers-reduced-motion` media query present
- [ ] **Standalone HTML** — no external CSS/JS libraries, only Google Fonts CDN. Inline `<script>` for canvas animations is OK.
- [ ] **Placeholder text visually marked** — wrap in `<!-- PLACEHOLDER -->` comments so it doesn't ship to prod

### File naming

Save to `prototypes/` directory by default, or to the project's existing design/mockup directory if one exists. Create the directory if needed:
```
prototypes/
├── hero-0-free.html          ← free variant (generated first)
├── hero-A-warm-alchemy.html  ← structured variants
├── hero-B-dark-rose.html
├── hero-C-editorial-night.html
├── hero-D-kintsugi.html
└── hero-E-ember.html
```

Pattern: `[scope]-[letter]-[style-name].html`
- Scope: `hero`, `card`, `dashboard`, `form`, etc.
- `0` for the free variant, `A` through `E` for structured (5 variants)
- Style name: 2-3 word description of the visual direction (kebab-case). Free variant always uses `free`.

### Gallery page (mandatory)

After generating all prototypes, create `gallery.html` in the same directory. This is the user's primary way to compare variants.

**Requirements:**
- Variant 0 (free) is displayed **first**, with a distinct label like "AI's Best Shot" — visually separated from the structured variants (e.g., different border color or a divider)
- Each card has: variant letter + name, style tags, 1-line description
- **"Open" link** (`target="_blank"`) to the standalone file — this is the primary navigation
- Dark background for neutral comparison context
- 1 column on mobile, 2 columns on desktop grid

**iframe display (with caveat):**
- Display prototypes via `<iframe src="./hero-A-warm-alchemy.html">` using **relative paths**
- Size toggle buttons: Mobile (600px height) / Tablet (768px) / Desktop (900px)
- **Important:** iframes with `file://` protocol may be blocked by browser security. The gallery MUST work even without iframes — every card must have a prominent "Open" link. If iframes fail to render, the user still has full access via direct links.
- If serving via local server (e.g., `python -m http.server`), iframes work reliably. Mention this to the user if they report blank iframes.

### Generation order and parallelization

**Step 1: Generate the free variant (variant 0) FIRST, alone.**
Give it the full brief context but no diversity constraints. This must complete before structured variants begin — it should not be influenced by them.

**Step 2: Generate structured variants A–E in parallel.**
Each prototype is independent — they don't share state. Use the Agent tool to generate prototypes in parallel when available: launch one agent per prototype, each with its own style direction.

**What to pass to each structured agent:**
- The full `prototypes/BRIEF.md` content (from Step 2.5)
- This variant's row from the Prototype Plan table
- The pre-generation checklist above
- The file naming pattern and target directory

**If parallel agents aren't available** (or the runtime doesn't support them), generate sequentially. The key rule: **re-read the BRIEF.md before each prototype** to avoid drift. After writing 3 similar files, the tendency is to repeat patterns — the brief anchors you back to the plan.

---

## Step 4 — Present & Evaluate

After all prototypes are ready, help the user evaluate them. This is where the skill earns its value for non-designers.

### How to present

Tell the user:
1. Open `gallery.html` in your browser (or open each prototype directly — they're standalone HTML files)
2. **Check mobile first** — resize browser to phone width or use DevTools responsive mode
3. Spend 3 seconds on each — first impression matters most

### Evaluation guide

Give the user this simple framework:

> Look at each prototype and ask yourself:
> - **Does this FEEL right for my audience?** (not "do I like it" — "would my users trust this?")
> - **Is the key action obvious?** (CTA visible, clear what to do next?)
> - **What grabs me?** (a color, a font, a layout trick, an animation)
> - **What repels me?** (too dark, too corporate, too playful, too busy)

Don't ask "which is best?" — ask **"which 1-2 are closest, and what would you change?"**

### The mixing question

After the user picks favorites, explicitly ask:

> "You picked [X]. Is there anything from the other variants you'd like to borrow? A font, a color, an animation, a layout idea?"

This is how non-designers create unique results — by combining elements they wouldn't have thought of independently.

---

## Step 5 — Refine & Build

Based on the user's choice and mix feedback, create the final design artifact.

### 5a. Merge elements

When the user wants to combine parts of different prototypes:

1. **Start from the chosen base** — copy it as the starting file
2. **List what's being borrowed** — be explicit: "Taking the font pairing from B, the color palette from D, and the layout from A"
3. **Apply changes one category at a time** — first typography, then colors, then layout, then effects. Don't try to merge everything at once — visual conflicts appear when you do
4. **Check each substitution** — a font that looked great in prototype B might clash with prototype A's color palette. Adjust if needed.

### 5b. Refined prototype

Save the merged result as `prototypes/hero-FINAL-[style-name].html` (same naming pattern, but "FINAL" instead of a letter).

**Show it to the user and ask:**
> "Here's the merged version. Check it on mobile and desktop. What needs tweaking before we build the full page?"

Iterate until the user says it's good. Keep iterations in the same file (overwrite, don't create hero-FINAL-v2, v3...).

### 5c. Hand off to production

Once the refined prototype is approved:

1. **Update `prototypes/BRIEF.md`** — add a "Final Direction" section with the locked-in palette, fonts, and layout decisions
2. **The full build** (expanding Hero to complete page) uses this brief as the source of truth for visual direction
3. If `ui-ux-pro-max` is available, use it for stack-specific guidelines and the pre-delivery UX checklist during the build phase

### Design quality note

When working on emotionally-driven projects (personal brands, wellness, art, coaching), don't use palette/font generators from design tools — they tend to produce generic SaaS aesthetics. Derive colors from the mood and references instead.

---

## Quick reference

| Situation | What to do |
|-----------|-----------|
| User says "make it look good" | Start from Step 1 — they don't know what they want yet |
| User provides detailed references | Light Step 1, thorough Step 2, generate prototypes |
| User says "like this but different" | Extract DNA from "this", generate variations |
| User wants to skip prototypes | Warn them: "Last time we skipped this, we had to redo everything. 15 minutes of prototypes saves hours of rework." |
| User can't choose between variants | Ask the 4 evaluation questions. If still stuck — combine the top 2 into a new variant |
| User wants fewer than 4 variants | OK only for simple components. For pages — hold the line at 4 minimum (1 free + 3 structured) |
| Time pressure | Generate 4 instead of 6, skip anti-references question, but never skip the context interview |
