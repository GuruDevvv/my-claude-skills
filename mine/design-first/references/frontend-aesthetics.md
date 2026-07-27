# Frontend Aesthetics — the anti-"AI-slop" directive

Read this **before generating any prototype** and apply it to each one. This is adapted from Anthropic's own "frontend aesthetics" guidance (Claude Cookbook) — the most battle-tested anti-slop prompt available. Models converge toward the average of their training data; in frontend that average is "AI slop". This directive pushes against it.

## The directive (apply to every prototype)

> You tend to converge toward generic, "on-distribution" outputs. In frontend design this creates the "AI slop" aesthetic. Avoid it — make creative, distinctive frontends that surprise and delight.
>
> - **Typography.** Choose beautiful, unusual, intentional fonts. Avoid generic ones (Inter, Roboto, Arial, system). Distinctive type elevates everything. (See `typography.md` — and respect the Cyrillic gate.)
> - **Color & theme.** Commit to one cohesive aesthetic. Use CSS variables. A dominant colour with sharp accents beats a timid, evenly-distributed palette. Draw from IDE themes, film, and cultural aesthetics — not from SaaS palette generators.
> - **Motion.** Use animation for high-impact moments. One well-orchestrated page-load with staggered reveals (`animation-delay`) delivers more delight than scattered micro-interactions. (See `motion.md`.)
> - **Backgrounds.** Create atmosphere and depth — layer gradients, grain/noise, geometric patterns, contextual effects. Never default to a flat solid fill.

## The AI-slop fingerprint — explicitly avoid

- **Fonts:** Inter, Roboto, Open Sans, Lato, system-ui as the *design* choice.
- **Color:** purple→blue→cyan gradient text, purple-on-white, timid grey+blue palettes.
- **Layout:** everything centered; the hero = headline + subtitle + two buttons; three identical feature cards in a row.
- **Effects:** the same shadow on every element; glassmorphism everywhere (reads as "built from a Lovable preset"); blurred purple "orbs".
- **Icons:** emoji bullets; Lucide/Heroicons sprinkled on everything.

> Real example caught in testing: a production app's own CSS had the comment `/* Градиентный текст — главный маркер AI-дизайна */` above a purple gradient — they knew it was the slop marker and shipped it anyway. Don't.

## Negative rules — bake explicit "do NOT" into each prototype's prompt

Removing defaults forces distinctiveness. Tell each generation, e.g.:
> "No purple/blue gradient text. No white/`#FAFAFA` background. No centered three-column feature grid. No pill buttons unless intentional. No Inter/Roboto."

Plus the project's own anti-references from the brief.

## High-impact levers (ranked by impact ÷ effort)

1. **Distinctive type at weight + size extremes** — single biggest differentiator, zero perf cost.
2. **Grain/noise overlay** — SVG `feTurbulence` at ~0.05-0.12 opacity. Kills sterile flatness. (snippet in `motion.md`/below)
3. **Staggered page-load reveal** — `animation-delay` 0/120/240/360ms. "Designed", not "rendered".
4. **Saturated accent on a dark/neutral base** — instead of purple-on-white.
5. **Atmospheric background** — layered gradients / real image / pattern, never flat.
6. **Asymmetric or editorial layout** — non-centered, oversized type, content that breaks the grid.

Grain overlay snippet (drop into any prototype):
```css
body::after{content:'';position:fixed;inset:0;pointer-events:none;z-index:200;opacity:.06;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");}
```
