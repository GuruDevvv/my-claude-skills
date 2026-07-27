# Motion — dependency-free animation that's actually visible

Static pages feel dead next to animated ones. Two failure modes to avoid: (1) **no motion**, and (2) **invisible motion** — a 6-second Ken Burns or a fade-in-on-scroll that nobody notices. Motion must be **perceptible in the first 3 seconds** and **matched to the product type**.

All recipes are standalone: inline CSS + tiny inline JS, **no CDN libraries** (GSAP/three.js/anime.js break the standalone principle and rot). Always include a `prefers-reduced-motion` path.

## Match motion to product type
- **Atmospheric / editorial / emotional** (landings, brand, story): fog drift, breathing glow, floating motes, Ken Burns, parallax, light-sweep, staggered reveals.
- **Functional / tools / dashboards:** count-up numbers, urgency pulse, staggered card reveal, hover lifts, progress rails. Restrained — clarity first.

---

## Core recipes

### Ken Burns (highest-ROI image motion)
```css
.kb{overflow:hidden}
.kb img{width:100%;height:100%;object-fit:cover;will-change:transform;animation:kb 28s ease-in-out infinite alternate}
@keyframes kb{from{transform:scale(1.06) translate(0,0)}to{transform:scale(1.18) translate(-2%,-3%)}}
```

### Reveal-on-scroll (reliable IntersectionObserver + optional CSS-native enhancement)
```css
.reveal{opacity:0;transform:translateY(34px);transition:opacity .8s ease,transform .8s ease}
.reveal.visible{opacity:1;transform:none}
```
```html
<script>
if(!('IntersectionObserver' in window)){document.querySelectorAll('.reveal').forEach(e=>e.classList.add('visible'));}
else{var io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){en.target.classList.add('visible');io.unobserve(en.target);}}),{threshold:.18});
document.querySelectorAll('.reveal').forEach(e=>io.observe(e));}
</script>
```
IntersectionObserver works everywhere. `animation-timeline: view()` is nicer but Firefox-gated (~18% miss) — only use it as progressive enhancement on top of the IO path.

### Animated gradient background (rich, zero assets)
```css
.grad{background:linear-gradient(-45deg,var(--c1),var(--c2),var(--c3),var(--c4));background-size:400% 400%;animation:gshift 12s ease infinite}
@keyframes gshift{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
```

### Staggered page-load reveal
Set `animation-delay` 0/120/240/360ms on successive hero elements entering with a `rise` keyframe (`translateY(26px)→0`, `opacity 0→1`). One orchestrated entrance > scattered micro-interactions.

### Count-up numbers (dashboards/stats — visible + functional)
```html
<span class="num" data-to="24">0</span>
<script>
var reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
document.querySelectorAll('[data-to]').forEach(function(el){var to=+el.dataset.to;if(reduce){el.textContent=to;return;}
var t0=null;requestAnimationFrame(function s(ts){t0=t0||ts;var p=Math.min((ts-t0)/900,1);el.textContent=Math.round(to*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(s);});});
</script>
```

### Urgency pulse (ring) — draws the eye to what matters
```css
.pulse{animation:ring 2s ease-out infinite}
@keyframes ring{0%{box-shadow:0 0 0 0 rgba(226,80,46,.55)}70%{box-shadow:0 0 0 12px rgba(226,80,46,0)}100%{box-shadow:0 0 0 0 rgba(226,80,46,0)}}
```

### CTA sheen / light-sweep
```css
.sheen{position:relative;overflow:hidden}
.sheen::after{content:'';position:absolute;top:0;left:-120%;width:60%;height:100%;background:linear-gradient(110deg,transparent,rgba(255,255,255,.5),transparent);animation:sweep 5.5s ease-in-out infinite}
@keyframes sweep{0%,100%{left:-120%}55%,70%{left:130%}}
```

### Atmospheric fog / breathing glow / floating motes (cinematic heroes)
- **Fog:** 2-3 absolutely-positioned large blurred radial-gradient layers, `mix-blend-mode:screen`, low opacity, slow `translate3d` drift (40-60s, `alternate`).
- **Glow:** a radial-gradient ellipse on the horizon, `animation:breathe 9s` toggling opacity .55↔1 and `scale(1)↔1.08`.
- **Motes:** JS-spawn ~26 tiny glowing dots with randomized `left`, duration, negative delay; CSS `float` drifts them up across the viewport. (Spawn only when not reduced-motion.)

### Parallax (hero image drifts slower than scroll)
```js
var img=document.querySelector('.hero__img');
addEventListener('scroll',()=>{requestAnimationFrame(()=>{img.style.transform='translateY('+(scrollY*0.18)+'px) scale(1.1)';});},{passive:true});
```

### View Transitions (section/tab/modal switches — Baseline since Oct 2025)
```js
function swap(fn){document.startViewTransition?document.startViewTransition(fn):fn();}
```

### Canvas particle system (dramatic — for the 1 "cinematic" prototype)
Inline `<canvas>` + `requestAnimationFrame` loop. Use for embers/snow/starfield/constellation/lightning. Template + effect recipes below.
```html
<canvas id="fx" style="position:fixed;inset:0;pointer-events:none;z-index:0;"></canvas>
<script>(function(){var c=document.getElementById('fx'),x=c.getContext('2d'),P=[];
function rs(){c.width=innerWidth;c.height=innerHeight;}rs();addEventListener('resize',rs);
var N=innerWidth<768?60:120; // perf budget
for(var i=0;i<N;i++)P.push({x:Math.random()*c.width,y:Math.random()*c.height,vx:(Math.random()-.5)*.5,vy:-Math.random()*1.5-.5,s:Math.random()*3+1,o:Math.random()*.5+.2});
(function a(){x.clearRect(0,0,c.width,c.height);P.forEach(function(p){p.x+=p.vx;p.y+=p.vy;if(p.y<-10){p.y=c.height+10;p.x=Math.random()*c.width;}x.beginPath();x.arc(p.x,p.y,p.s,0,7);x.fillStyle='#e8b08a';x.globalAlpha=p.o;x.fill();});x.globalAlpha=1;requestAnimationFrame(a);})();})();</script>
```
| Effect | Tweak |
|--------|------|
| Rising embers | `vy:-rand*2`, 1-3px, warm colors, slight `vx` wobble |
| Falling snow/ash | `vy:+rand*1`, white/grey, `sin` horizontal drift |
| Starfield/constellation | static dots + draw lines when `dist<100px` |
| Floating orbs | few large (10-30px), `sin/cos` motion, radial fill, blur |
| Smoke/mist | large semi-transparent (30-80px), `vy:-0.3`, high blur |

## Advanced / sophisticated motion (for the 1-2 "complex" prototypes)

Use one of these as the centerpiece of a prototype — orchestrated, multi-step, scroll- or pointer-driven.

### Sticky-stacking cards (cards stack & scale as you scroll)
```css
.stack section{position:sticky;top:8vh;height:80vh}
.stack section:nth-child(1){top:6vh}.stack section:nth-child(2){top:9vh}.stack section:nth-child(3){top:12vh}
```
Each section pins, the next slides over it — a tactile "deck" feel. Pair with a subtle scale-down on the pinned one.

### Scroll-driven storytelling (sticky visual + advancing text)
A tall wrapper with a `position:sticky` visual (image/canvas) on one side; as text blocks scroll past, swap the visual's state (class toggle via IntersectionObserver, or `animation-timeline: view()` for the visual's transform). One scene that *narrates* as you scroll = the strongest "designed" signal.

### Multi-layer parallax (depth)
Move 2-3 layers at different rates on scroll (`translateY(scrollY * rate)`, rates e.g. .05/.12/.22). Background image slowest, foreground fastest. `will-change:transform`, rAF-throttled.

### Cursor-reactive hero (pointer parallax / spotlight)
```js
addEventListener('pointermove',e=>{var x=(e.clientX/innerWidth-.5),y=(e.clientY/innerHeight-.5);
hero.style.setProperty('--mx',x);hero.style.setProperty('--my',y);});
```
Drive a `radial-gradient` spotlight that follows the cursor, or translate hero layers by `calc(var(--mx)*20px)`. Skip on touch / reduced-motion.

### Number/data build sequence
Stagger count-up + a bar/sparkline that draws in (`stroke-dashoffset` on an SVG path animating to 0). Great for dashboards — functional *and* sophisticated.

### Horizontal scroll-snap journey
A sideways-scrolling sequence of full panels (`scroll-snap-type:x mandatory`) — for step-by-step or gallery storytelling. (Markup in `interaction-patterns.md`.)

## Performance & accessibility (always)
```css
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important}
}
```
- Canvas particles: ≤60 mobile, ≤120 desktop (`innerWidth<768` check).
- CSS animations: only `transform`/`opacity` (GPU-composited) — never animate `width/height/top/left`.
- Always `requestAnimationFrame`, never `setInterval`.
- Don't animate text content (typewriter/scrolling) — delays comprehension. Don't bounce/shake the CTA.
