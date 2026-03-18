---
name: design-first
description: Generate 4-6 diverse HTML design prototypes before coding. Interview → references → parallel prototypes → gallery comparison → user picks → build. Use when: "сделай дизайн", "подготовь макет", "давай займёмся дизайном", "нарисуй страницу", "make a design", "design this", "prepare design", "how should this look", "visual direction", "prototypes", "варианты дизайна". Scope: landing pages, dashboards, portfolios, forms, apps, components — any visual/UI work.
---

# Design First

A structured process for exploring visual direction before writing production code. Built for people who aren't designers but need professional-quality results.

The core idea: **don't commit to one design. Generate diverse options, compare, pick the best, then build.** This eliminates the #1 problem in vibe-coding — getting stuck with the first thing that came out.

---

## How it works (overview)

```
Interview → References → Design DNA → Prototypes → Evaluation → Selection → Full build
   5 min      optional      10 min      parallel       user        mix       go
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

## Step 3 — Generate Prototypes

### Visual quality delegation (required dependency)

This skill handles process and diversity. Visual quality of each prototype is handled by **`ui-ux-pro-max`** — it has 67 styles, 96 palettes, 57 font pairings.

**Before generating prototypes, check that `ui-ux-pro-max` is available.** If it's not installed:
1. Stop and tell the user: "Для генерации качественных прототипов нужен навык `ui-ux-pro-max`. Установи его и перезапусти."
2. Provide install instructions: add the skill from the Claude Code skills registry or copy the SKILL.md file to `~/.claude/skills/ui-ux-pro-max/`
3. Do not proceed with prototype generation without it — the output quality will be generic.

### What to generate

Each prototype is a **standalone HTML file** — self-contained, opens directly in browser, no dependencies except Google Fonts CDN.

Prototype scope depends on what you're designing:
- **Full page** (landing, homepage): generate the Hero section only (above the fold). Hero sets the tone — if it works, the rest follows.
- **Component** (card, form, modal, navbar): generate the component in context (with enough surrounding UI to feel real).
- **Dashboard/app**: generate one key screen or panel.

### How many variants

**Default: 6 prototypes. Minimum: 4.**

Why 6: it's enough to cover diverse directions without overwhelming. Each variant must be *genuinely different* — not the same layout with tweaked colors. Different fonts, different color strategies, different visual techniques.

When 4 is enough:
- Simple components (button, card, form)
- User gave very specific references and the direction is clear
- Tight time constraints (user explicitly says "quick")

### Diversity strategy

Each prototype should vary on at least 2 of these axes:

| Axis | Example range |
|------|--------------|
| **Temperature** | Warm earthy tones ↔ Cool blues/grays ↔ High-contrast dark |
| **Typography** | Elegant serif ↔ Clean sans ↔ Bold display/statement |
| **Density** | Airy with lots of whitespace ↔ Rich and detailed |
| **Technique** | Glassmorphism, gradients, grain texture, illustration, photography, minimal flat, brutalist |
| **Animation** | None/subtle ↔ Cinematic particles ↔ Playful micro-interactions |

If references exist, allocate roughly:
- **Half** of prototypes inspired by references (extracting and remixing their DNA)
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
  </style>
</head>
<body>
  <!-- Real content, not lorem ipsum -->
  <!-- If user provided text — use it -->
  <!-- If not — write plausible placeholder that matches the project -->
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

### File naming

Save to `prototypes/` directory by default, or to the project's existing design/mockup directory if one exists. Create the directory if needed:
```
prototypes/
├── hero-A-warm-alchemy.html
├── hero-B-dark-rose.html
├── hero-C-editorial-night.html
├── hero-D-kintsugi.html
├── hero-E-ember.html
└── hero-F-grimoire.html
```

Pattern: `[scope]-[letter]-[style-name].html`
- Scope: `hero`, `card`, `dashboard`, `form`, etc.
- Letter: A through F (for ordering)
- Style name: 2-3 word description of the visual direction (kebab-case)

### Gallery page (mandatory)

After generating all prototypes, create `gallery.html` in the same directory. This is the user's primary way to compare variants. Requirements:
- Display all prototypes via `<iframe>` in a grid (1 column mobile, 2 columns desktop)
- Each card has: variant name, style tags, **"Open" link** (`target="_blank"`) to the standalone file
- Size toggle buttons: Mobile (600px height) / Tablet (768px) / Desktop (900px)
- Brief 1-line description under each iframe
- Dark background for neutral comparison context

### Parallelization

Generate all prototypes in parallel using subagents when available. Each prototype is independent — they don't share state. This is the biggest time-saver in the workflow.

For each subagent, provide:
- Full context from Steps 1-2 (interview answers, design DNA)
- The specific style direction for this variant
- The content/copy to use
- Technical requirements (mobile-first, standalone HTML, etc.)

If subagents aren't available, generate sequentially — but still make each one genuinely different.

---

## Step 4 — Present & Evaluate

After all prototypes are ready, help the user evaluate them. This is where the skill earns its value for non-designers.

### How to present

Tell the user:
1. Open each file in your browser (or provide file:// links)
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

Based on the user's choice and mix feedback:

1. **Create the refined prototype** — apply borrowed elements to the chosen base
2. **Show it to the user** — one more quick check before scaling up
3. **Hand off to production** — Step 5 is where this skill ends. The full build (expanding Hero to complete page) belongs to `ui-ux-pro-max` and `frontend-design` skills, with the visual direction already locked in from prototypes.

**Important note on generated palettes:** When working on emotionally-driven projects (personal brands, wellness, art, coaching), don't use palette/font generators from design tools — they tend to produce generic SaaS aesthetics. Derive colors from the mood and references instead.

---

## Quick reference

| Situation | What to do |
|-----------|-----------|
| User says "make it look good" | Start from Step 1 — they don't know what they want yet |
| User provides detailed references | Light Step 1, thorough Step 2, generate prototypes |
| User says "like this but different" | Extract DNA from "this", generate variations |
| User wants to skip prototypes | Warn them: "Last time we skipped this, we had to redo everything. 15 minutes of prototypes saves hours of rework." |
| User can't choose between variants | Ask the 4 evaluation questions. If still stuck — combine the top 2 into a new variant |
| User wants fewer than 4 variants | OK only for simple components. For pages — hold the line at 4 minimum |
| Time pressure | Generate 4 instead of 6, skip anti-references question, but never skip the context interview |
