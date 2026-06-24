# Feel Polish — make the built UI feel right

The prototype phase chose **what** to build. This is the pass that makes the *finished, real code* feel crafted instead of AI-default. Great polish is invisible: a collection of small details that compound. Run it on the **final build** (Step 5), not on throwaway prototypes — these rules reward real components, and forcing them onto concept prototypes brings back the "passes every check, moves no one" trap design-first fights.

> Distilled from **"Details that make interfaces feel better"** by **Jakub Krehel** (`jakubkrehel/make-interfaces-feel-better`, MIT). Principles re-expressed here; credit and the canonical, deeper reference are his.

When to skip the whole pass: pure throwaway, a one-off internal tool nobody will look at twice, or the user says "skip polish".

---

## The 16 principles

Grouped by area. The **exact numbers are non-negotiable** where marked — they're tuned values, not suggestions. (Principle numbers follow Krehel's canonical list, so they read out of sequence once grouped by area — that's intentional, not a typo.)

### Surfaces

1. **Concentric border radius.** `outerRadius = innerRadius + padding`. Mismatched radii on nested rounded elements is the single most common thing that makes UI feel "off". If padding > 24px, treat layers as separate surfaces and pick each radius freely instead of forcing the math.
2. **Optical over geometric alignment.** When centered-by-math looks wrong, nudge by eye. Button text+icon: `icon-side padding = text-side − 2px`. Play triangle: shift `~2px` right. Asymmetric icons (stars, carets): fix the SVG viewBox/path rather than adding margins.
3. **Shadows over borders** *for depth/elevation* (buttons, cards, containers). Layer transparent `box-shadow` so it adapts to any background. **Light mode** = three layers; **dark mode** = single white ring (`0 0 0 1px rgba(255,255,255,.08)`), layered depth is invisible on dark. **Keep real borders** for dividers, table cells, hairlines, input outlines — anything whose job is separation, not lift.
11. **Image outlines.** Inset `1px` outline for consistent depth: `outline:1px solid …; outline-offset:-1px` (outline doesn't affect layout). Colour is **non-negotiable**: pure black `rgba(0,0,0,.1)` (light) / pure white `rgba(255,255,255,.1)` (dark). **Never** a tinted near-black/near-white (slate/zinc/neutral) — it picks up the surface underneath and reads as dirt on the edge.
16. **Minimum hit area** ≥ 40×40px (44 is WCAG). If the visible control is smaller, extend with a pseudo-element. Two interactive elements must never have overlapping hit areas — shrink before they collide.

### Animation

4. **Interruptible animations.** CSS *transitions* for interactive state (hover, toggle, open/close) — they retarget mid-flight. Reserve *keyframes* for one-shot staged sequences (enter, loading). A keyframe on a toggle snaps/restarts when reversed = feels broken.
5. **Split & stagger enter.** Don't animate one big container. Break into semantic chunks (title / description / actions), stagger ~100ms; titles can split per word ~80ms. Combo `opacity + translateY(12px) + blur(4px)` → `0/0/0`.
6. **Subtle exit.** Softer and shorter than the enter — small fixed `translateY(-12px)`, not full height; duration ~150ms vs ~300ms enter. Keep slight directional movement; never just `display:none`. Full slide-out only when spatial context matters (card returning to a list, drawer).
7. **Contextual icon swaps** (play→pause, like→liked, hover-revealed). Animate, don't toggle visibility. **Exact values:** `scale 0.25→1`, `opacity 0→1`, `blur 4px→0`. With `motion`/`framer-motion` present: `transition:{ type:"spring", duration:0.3, bounce:0 }` — **bounce always 0**. No motion lib: keep both icons in DOM (one `absolute`), cross-fade with `cubic-bezier(0.2,0,0,1)`. Don't add a dependency just for this.
12. **Scale on press.** `scale(0.96)` on `:active` for tactile feedback — **never below 0.95** (feels exaggerated). CSS transition so a mid-press release returns smoothly. Give buttons a `static` prop to opt out where motion distracts. Not every button needs it.
13. **Skip enter-animation on page load.** `initial={false}` on `AnimatePresence` so default-state elements (icon swaps, tabs, segmented controls) don't animate in on first render — only on later changes. **Don't** use it where the component's first-time entrance *is* the point (staggered hero, loading) — it would kill the entrance. Verify on a full refresh.

### Typography

8. **Font smoothing (macOS).** `-webkit-font-smoothing:antialiased; -moz-osx-font-smoothing:grayscale` once on the root (`<html className="antialiased">`). Other platforms ignore it — safe universally.
9. **Tabular numbers.** `font-variant-numeric:tabular-nums` on anything that updates live (counters, prices, timers, scoreboards, numeric table columns) to kill layout shift. **Not** on static/decorative numbers, phone numbers, version strings. (Inter widens & centers `1` under this — expected.)
10. **Text wrapping.** `text-wrap:balance` on headings (≤6 lines Chromium / ≤10 Firefox — silently ignored on long text). `text-wrap:pretty` as the default for short-to-medium body (paragraphs, captions, list items) to avoid orphans. Long text (10+ lines) / code: leave default.

### Performance

14. **Never `transition: all`** (nor Tailwind's bare `transition`). Name exact properties: `transition-property: scale, opacity`. `all` watches everything, triggers unintended animations, blocks optimization. Tailwind `transition-transform` already covers `transform, translate, scale, rotate`; for mixed props use `transition-[scale,opacity,filter]`.
15. **`will-change` sparingly.** Only compositor-friendly props — `transform`, `opacity`, `filter`, `clip-path` — and only when you actually see first-frame stutter (Safari benefits most). Never `will-change: all`; never on non-GPU props (background, padding, color). Each layer costs memory.

---

## Output format (when you report a Feel pass)

Present every change as **markdown tables, grouped by principle**, with `Before` / `After` columns — not loose "Before:/After:" lines. One diff per row so it scans. Cite the file/property when not obvious from the snippet. If a principle was checked and nothing changed, **omit that table** (empty tables = noise).

```markdown
#### Concentric border radius
| Before | After |
| --- | --- |
| `rounded-xl` card + `rounded-xl` inner button (`p-2`) | `rounded-2xl` card (12+8), `rounded-lg` inner |

#### Scale on press
| Before | After |
| --- | --- |
| `scale(0.9)` on press | Raised to `scale(0.96)` — below 0.95 feels exaggerated |
```

---

## Feel-pass checklist

- [ ] Nested rounded elements use concentric radius
- [ ] Icons optically centered, not just geometric
- [ ] Depth via layered shadow; dividers stay borders
- [ ] Enter animations split & staggered; exits subtle & shorter
- [ ] Interactive state uses interruptible transitions, not keyframes
- [ ] Contextual icon swaps animate (scale 0.25→1, blur 4→0, bounce 0)
- [ ] Buttons scale to 0.96 on press where appropriate
- [ ] `AnimatePresence` uses `initial={false}` for default-state elements
- [ ] Dynamic numbers use `tabular-nums`
- [ ] Root has `antialiased`
- [ ] Headings `text-wrap:balance`, body `text-wrap:pretty`
- [ ] Images have a pure black/white inset outline (no tint)
- [ ] No `transition: all` — explicit properties only
- [ ] `will-change` only on transform/opacity/filter, only if stutter seen
- [ ] Interactive elements ≥ 40×40px hit area, no overlaps
