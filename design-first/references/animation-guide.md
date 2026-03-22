# Animation Guide

Prototypes are standalone HTML — no npm, no build step. Animation must work from a single file. Two approaches:

## Approach 1: CSS-only animations (for moderate effects)

Good for: floating elements, pulsing glows, rotating symbols, animated gradients, shimmer sweeps, parallax-like shifts.

```css
/* Floating particles (CSS-only, use multiple divs with staggered delays) */
@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.6; }
  50% { transform: translateY(-120px) rotate(180deg); opacity: 0; }
}
.particle {
  position: absolute;
  animation: float 4s ease-in-out infinite;
  /* Stagger: animation-delay: 0s, 0.5s, 1s, 1.5s... */
}

/* Animated gradient background */
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.hero {
  background: linear-gradient(270deg, #0a0a0f, #1a0a14, #0a0a0f);
  background-size: 400% 400%;
  animation: gradientShift 8s ease infinite;
}

/* Rotating decorative symbol */
@keyframes slowSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.symbol { animation: slowSpin 20s linear infinite; }

/* Shimmer sweep on text */
@keyframes shimmer {
  0% { background-position: -200% center; }
  100% { background-position: 200% center; }
}
.shimmer-text {
  background: linear-gradient(90deg, #fff 0%, #c9a84c 50%, #fff 100%);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shimmer 3s linear infinite;
}
```

## Approach 2: Inline JavaScript Canvas (for dramatic effects)

Good for: particle systems (sparks, snow, stars, embers), lightning, flowing lines, constellation networks. Write `<canvas>` + `<script>` directly in the HTML file.

**Particle system template** (inline, no dependencies):
```html
<canvas id="particles" style="position:fixed;inset:0;pointer-events:none;z-index:0;"></canvas>
<script>
(function() {
  const canvas = document.getElementById('particles');
  const ctx = canvas.getContext('2d');
  let particles = [];

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  // Customize: count, colors, speed, size, behavior
  for (let i = 0; i < 60; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.5,
      vy: -Math.random() * 1.5 - 0.5, // rising
      size: Math.random() * 3 + 1,
      opacity: Math.random() * 0.5 + 0.2,
      color: ['#c43a6e', '#c9a84c', '#d44a1a', '#fff'][Math.floor(Math.random() * 4)]
    });
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      if (p.y < -10) { p.y = canvas.height + 10; p.x = Math.random() * canvas.width; }
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.globalAlpha = p.opacity;
      ctx.fill();
    });
    ctx.globalAlpha = 1;
    requestAnimationFrame(animate);
  }
  animate();
})();
</script>
```

## Effect recipes

Modify the particle template above:

| Effect | How to customize |
|--------|-----------------|
| **Rising embers/sparks** | `vy: -random*2`, small size (1-3px), orange/red colors, add slight `vx` wobble |
| **Falling snow/ash** | `vy: +random*1`, white/gray, larger size (2-5px), add `Math.sin` horizontal drift |
| **Starfield/constellation** | Static particles + draw lines between nearby ones (`distance < 100px`), white/silver |
| **Lightning flashes** | Draw jagged `lineTo` paths at random intervals, bright white, fade quickly |
| **Floating orbs** | Few large particles (10-30px), `Math.sin`/`Math.cos` movement, radial gradient fill, blur |
| **Smoke/mist** | Large semi-transparent circles (30-80px), very slow `vy: -0.3`, gray, high blur |
| **Glowing fireflies** | Few particles (10-20), `Math.sin` both axes, pulsing opacity via `Math.sin(Date.now())` |
