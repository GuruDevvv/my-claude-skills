# UI verify — measure with numbers, don't trust the screenshot

Adapted from a `ui-verify` skill shared by a design-first user (Sept 2026), merged with
lessons from our own prototype rounds.

## Why

A screenshot is not a measuring instrument. Between the layout and the picture sit compositing
(the frame may be taken before the page finished painting) and image compression (low-contrast
differences vanish). That creates an asymmetry:

**A positive result is reliable, a negative one is not.** Effect visible on the shot → it exists.
Not visible → could be a real defect or a failure of the channel. Same with `grep`: "found" is a
fact, "not found" is a question. And symmetric to it: **a confident number is also the output of a
channel** — before calling something broken, make sure you measured what the eye sees.

In our own rounds this cost real time: two of five parallel builders shipped unreadable text
(ochre on ochre, a cream veil) that nobody saw in the code; a reveal-on-scroll left whole screens
empty on a phone; a portrait slid over the headline only on a monitor wider than ours; an hour went
into a "broken" 390px layout that was really headless Chrome refusing to go below ~500px.

## The automatic check — `scripts/check.mjs` (default)

```bash
node <skill-dir>/scripts/check.mjs prototypes/ --widths 390,1440,1920
node <skill-dir>/scripts/check.mjs page.html --shots prototypes/_check/   # + first-screen PNGs
```

Zero dependencies (Node 22+, installed Chrome/Edge). Emulates the exact viewport (so 390 is really
390), scrolls the whole page to fire reveals, then per file × width reports:

| Line | Meaning | Action |
|---|---|---|
| `FAIL horizontal scroll` | page wider than the window; names the outermost culprit | fix: `min-width:0`, `max-width:100%`, wrap |
| `FAIL unreadable, contrast < 3` | text nobody reads comfortably against every background layer under it (colours in any CSS format, semi-transparent veils composited) | fix colour or background |
| `NOTE … on a gradient` | fails on some gradient stops but not all — depends on where the text sits | check by eye |
| `FAIL invisible after full scroll` | text still at opacity 0 after scrolling and ~6s of waiting — a reveal that never fired (toggle states, carousel slides and looping demos are already excluded) | give reveals a fallback; never hide content by default without JS |
| `FAIL font has no Cyrillic` | text silently falls back to another font | swap the font (typography.md) |
| `FAIL request failed` / `image not loaded` / `JS error` | an image, CSS background or font file failed (HTTP ≥400 or network), or a script threw | fix |
| `FAIL font not loaded` | the font file never arrived — different from "no Cyrillic" | fix the link/name |
| `WARN weak contrast 3–4.5` | fine for big text, weak for small | fix if it's body copy or a CTA |
| `WARN text under 12px on phone` | tiny labels | raise if it carries meaning |
| `NOTE … on photos/video` | contrast not computable over images | check those by eye; add a scrim if in doubt |

Exit code 1 if anything FAILs. **Fix every FAIL before the gallery**, rerun until clean, and give
the user the numbers in one line ("6 макетов × 3 ширины, всё чисто; 2 слабых подписи поправил").

## Manual probes (for complaints and anything the script doesn't cover)

Run through the browser tool's JavaScript executor (`mcp__claude-in-chrome__javascript_tool` or
similar). The snippet ends with an expression in parentheses — `({ ... })` — and returns numbers and
strings, not DOM nodes.

### Gate first: does the viewport exist?
A hidden/collapsed preview pane still runs scripts but lays out against a **zero viewport** — every
geometry number comes back plausible and wrong.
```js
({ innerW: window.innerWidth, clientW: document.documentElement.clientWidth, visibility: document.visibilityState });
```
`innerW: 0` → don't read geometry; set an explicit size (`resize_window` with width/height). Colours,
pseudo-elements and fonts (`getComputedStyle`) don't depend on visibility.

### Contrast of one element (layers composited)
```js
const el = document.querySelector('SELECTOR');
const rgba = (s) => { const m = (s || '').match(/[\d.]+/g); return m ? [+m[0], +m[1], +m[2], m.length > 3 ? +m[3] : 1] : null; };
const over = (fg, bg) => fg.map((v, i) => (i < 3 ? fg[3] * v + (1 - fg[3]) * bg[i] : 1));
const lum = (c) => { const [r, g, b] = c.slice(0, 3).map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
const layers = []; let base = [255, 255, 255, 1];
for (let n = el; n; n = n.parentElement) {
  const cs = getComputedStyle(n);
  if (/gradient/.test(cs.backgroundImage)) { const st = (cs.backgroundImage.match(/rgba?\([^)]+\)/g) || []).map(rgba).filter(Boolean); if (st.length) layers.push(st); }
  const bc = rgba(cs.backgroundColor);
  if (bc && bc[3] > 0) { if (bc[3] >= 0.999) { base = bc; break; } layers.push([bc]); }
}
let bgs = [base];
for (let i = layers.length - 1; i >= 0; i--) bgs = layers[i].flatMap((s) => bgs.map((u) => over(s, u)));
const cs = getComputedStyle(el), fg0 = rgba(cs.color);
const ratios = bgs.map((b) => { const fg = fg0[3] < 1 ? over(fg0, b) : fg0; const [hi, lo] = [lum(fg), lum(b)].sort((x, y) => y - x); return +((hi + 0.05) / (lo + 0.05)).toFixed(2); });
({ contrast: Math.min(...ratios), perStop: ratios, color: cs.color, fontSize: cs.fontSize, theme: document.documentElement.dataset.theme || 'system' });
```
Thresholds: 4.5 normal text, 3 large (≥24px, or ≥18.7px bold) and icons/borders. Why not the naive
"first non-transparent background": it stops on a 0.14-alpha panel and reports 1.26 instead of the
real 8.80, and it ignores gradients (1.01 instead of 5.37). **A measuring tool that invents defects
is worse than one that misses them** — the next agent goes to "fix" working layout.

### Grid cells drifted apart
```js
const box = (el) => { const r = el.getBoundingClientRect(); return `${Math.round(r.width)}×${Math.round(r.height)}`; };
({ cells: [...new Set([...document.querySelectorAll('CELL')].map(box))], inner: [...new Set([...document.querySelectorAll('CELL_CONTENT')].map(box))] });
```
One size per list = even grid. `["358×367","500×367"]` needs no comment. Usual cause: a grid/flex child
without `min-width: 0`; with `aspect-ratio` images a width drift becomes "covers of different height".

### Did the rule actually apply?
`grep` on a build answers "is the string in the file", not "did it apply" (minifiers rewrite `::after`
to `:after`, hash classes, inline styles).
```js
const a = getComputedStyle(document.querySelector('SELECTOR'), '::after');
({ content: a.content, position: a.position });
```
`content: "none"` → not applied; anything else → applied.

### Theme switch round-trip
Measure → toggle → measure → toggle → measure. **The third must equal the first character for
character.** Known trap: Chromium doesn't recompute a property that has a `transition` when the new
value comes from `light-dark()` — the colour sticks. Fix: a class that disables transitions during
the switch, removed after two `requestAnimationFrame`s.

### Is the glyph in the font?
```js
const probe = (ch, fam) => { const c = document.createElement('canvas').getContext('2d');
  c.font = `72px "${fam}", monospace`; const a = c.measureText(ch).width; c.font = '72px monospace'; const b = c.measureText(ch).width;
  return { ch, missing: Math.abs(a - b) < 0.5 }; };
['→', '✓', '₽', '№', 'Ё'].map((ch) => probe(ch, 'FAMILY'));
```
Heuristic (a glyph of identical width gives a false "missing"); subsets lose arrows, ticks and
currency signs regularly.

## Negative-result rule

A tool said "no" → recheck by a **different mechanism**, not by rerunning the same one.

| First channel said "no" | Second way |
|---|---|
| effect/colour not visible on the shot | measure `getComputedStyle` / `getBoundingClientRect` |
| blank shot or shot after a timeout | half-painted frame: shoot again, or `navigate` again and wait |
| `grep` didn't find the rule in `dist` | ask the browser via CSSOM (above) |
| "no errors in the console" | read the console after a reload — early messages print before you attach |

## Environment traps we already paid for

- **Headless Chrome on Windows won't make a window narrower than ~500px.** A "390px" screenshot then
  crops the page and looks like a broken layout. Use device-metrics emulation (the script does) or
  wrap the page in a fixed-width frame; confirm with `innerWidth`.
- **Full-page (beyond-viewport) screenshots stretch `100vh` heroes** to the whole capture height.
  Judge heroes on first-screen shots only.
- **Check the wide end too.** Elements positioned from the window edge (`right: calc(50% - 512px)`)
  instead of the content column drift apart on monitors wider than yours — hence 1920 in the widths.
- **Rebuilt the source? Measure the rebuilt page.** Otherwise you argue with the old version.

## What this doesn't do

Composition, rhythm, air, "cheap vs expensive" — that's the eye and taste. **Numbers can be wrong
too** (gradients, overlapping layers, pseudo-elements, fonts still loading). If the shot and the
numbers disagree, find out why with a third probe before acting — don't let either win by default.
A clean run means "found nothing it knows how to find"; looking at every variant at phone and
desktop width stays mandatory.
