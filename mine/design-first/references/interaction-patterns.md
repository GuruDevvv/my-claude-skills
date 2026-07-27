# Interaction patterns — navigation + non-standard elements

Two jobs: (1) make pages genuinely **navigable** when there's a lot of content, and (2) reach for **memorable, non-standard** elements so prototypes don't all default to "stack of sections". All dependency-free (inline CSS/JS, no libraries).

---

## Navigation — understand it, don't ignore it

A long scroll with no wayfinding is a usability failure. **If content is list-heavy or multi-section (memo, docs, catalog, multi-section landing), ≥1-2 prototypes must include real navigation.** Vary the pattern across prototypes — navigation is a structural diversity axis.

### Patterns (pick per concept)
| Pattern | When | Notes |
|---|---|---|
| **Sticky TOC / scroll-spy sidebar** | long-form, docs, memo,多-section | persistent list of sections; active item highlights as you scroll |
| **Top bar + anchor links** | marketing/landing | simple, familiar; can shrink/condense on scroll |
| **Sub-nav / segmented tabs** | dashboard sections, catalogs | switch views without leaving the page |
| **Bottom tab bar** | mobile-first apps | thumb-reachable |
| **Breadcrumb / progress rail** | wizards, multi-step | shows where you are |
| **Command bar (⌘K style)** | dense tools | power-user nav |

### Scroll-spy TOC (dependency-free)
```html
<nav class="toc"><a href="#terms">Условия</a><a href="#returns">Доходность</a><a href="#risks">Риски</a></nav>
```
```css
.toc{position:sticky;top:24px;display:flex;flex-direction:column;gap:8px}
.toc a{color:var(--muted);transition:.2s;border-left:2px solid transparent;padding-left:12px}
.toc a.active{color:var(--accent);border-color:var(--accent)}
```
```js
var links=[...document.querySelectorAll('.toc a')];
var io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){
  links.forEach(l=>l.classList.toggle('active',l.hash==='#'+e.target.id));}}),{rootMargin:'-40% 0px -55% 0px'});
document.querySelectorAll('section[id]').forEach(s=>io.observe(s));
```
Always `scroll-margin-top` on anchored sections so sticky headers don't cover them.

---

## Non-standard / memorable elements

**≥1 prototype should feature one unconventional interaction** — the thing a stranger remembers. Don't overdo it (one strong move per prototype, not a circus). Pick what fits the concept:

| Element | Effect | Dependency-free? |
|---|---|---|
| **Bento grid** | mixed-size tiles, modern, scannable | ✅ CSS grid with `grid-row/column span` |
| **Horizontal scroll-snap section** | gallery/steps that scroll sideways | ✅ `overflow-x:auto; scroll-snap-type:x mandatory` |
| **Sticky-stacking cards** | cards stack/overlap as you scroll | ✅ `position:sticky; top` per card (see motion.md) |
| **Before/after slider** | comparison (e.g. "до/после сделки") | ✅ range input + clip-path, ~15 lines JS |
| **Scroll-spy TOC** | live navigation (above) | ✅ |
| **Custom cursor** | dot that reacts to hover | ✅ ~10 lines JS (best for creative/portfolio, not dashboards) |
| **Hover-reveal / expand-in-place** | detail on demand, no page change | ✅ CSS `:hover` / `<details>` |
| **Draggable cards / sortable** | playful, tactile | ✅ pointer events, modest JS |
| **Marquee / ticker** | live data, logos, "running tape" | ✅ CSS keyframe translate |
| **Animated counter / data-viz** | numbers that build, inline charts | ✅ (see motion.md count-up; SVG/canvas charts) |

### Snippets
Bento grid:
```css
.bento{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:160px;gap:14px}
.bento .feature{grid-column:span 2;grid-row:span 2}
```
Horizontal scroll-snap:
```css
.rail{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch}
.rail>*{flex:0 0 80%;scroll-snap-align:center}
```
Before/after slider: two stacked images in a wrapper; a `range` input drives `clip-path:inset(0 calc(100% - var(--x)) 0 0)` on the top layer.

## Don't
- Don't add a non-standard element that hurts the core task (custom cursor on a dashboard, marquee on legal terms).
- Don't stack 5 gimmicks in one prototype — one memorable move beats five noisy ones.
- Keep everything keyboard-accessible and `prefers-reduced-motion`-aware.
