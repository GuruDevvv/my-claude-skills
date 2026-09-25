#!/usr/bin/env node
// design-first: measure prototypes with numbers before the user sees them.
// Zero dependencies: Node 22+ (global WebSocket) + an installed Chrome/Edge/Chromium.
//
//   node check.mjs prototypes/                 # every *.html in the folder (gallery skipped)
//   node check.mjs a.html b.html --widths 390,1440,1920 --shots out/ --json report.json
//
// Per file and width it reports: horizontal overflow (+ outermost culprit), text contrast
// (layered backgrounds under the text, image-backed text flagged separately, not guessed),
// content stuck invisible after scrolling (reveal-on-scroll that never fired), tiny text,
// fonts that lack Cyrillic, broken images, JS errors. Exit code 1 if anything FAILs.

import { spawn } from 'node:child_process';
import { mkdtempSync, readdirSync, statSync, existsSync, readFileSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve, basename } from 'node:path';
import { pathToFileURL } from 'node:url';

const argv = process.argv.slice(2);
const opt = (name, def) => { const i = argv.indexOf(name); if (i < 0) return def; const v = argv[i + 1]; argv.splice(i, 2); return v; };
const widths = opt('--widths', '390,1440,1920').split(',').map(Number);
const shotsDir = opt('--shots', null);
const jsonOut = opt('--json', null);
if (!argv.length) { console.error('usage: node check.mjs <file|dir|url>... [--widths 390,1440,1920] [--shots dir] [--json file]'); process.exit(2); }

const targets = argv.flatMap((a) => {
  if (/^https?:\/\//.test(a)) return [a];
  const p = resolve(a);
  if (statSync(p).isDirectory()) {
    return readdirSync(p).filter((f) => f.endsWith('.html') && !/^gallery/i.test(f)).sort()
      .map((f) => pathToFileURL(join(p, f)).href);
  }
  return [pathToFileURL(p).href];
});

if (!targets.length) { console.error('Nothing to check: no .html files found in ' + argv.join(' ')); process.exit(2); }

const chromePath = () => {
  const c = [process.env.CHROME_PATH,
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'].filter(Boolean);
  const hit = c.find((p) => existsSync(p));
  if (!hit) throw new Error('No Chrome/Edge found — set CHROME_PATH');
  return hit;
};

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ---------- the in-page measurement (runs inside the prototype) ----------
const MEASURE = String.raw`(async () => {
  await document.fonts.ready;
  const de = document.documentElement;
  const out = { innerW: innerWidth, scrollW: de.scrollWidth, clientW: de.clientWidth };
  const sel = (el) => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
    (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '');

  // 1. overflow: outermost elements sticking out that no ancestor clips
  out.overflow = de.scrollWidth > de.clientWidth + 1;
  if (out.overflow) {
    const clips = (el) => { for (let n = el.parentElement; n && n !== document.body; n = n.parentElement) {
      if (/hidden|clip|auto|scroll/.test(getComputedStyle(n).overflowX)) return true; } return false; };
    const bad = [...document.body.querySelectorAll('*')].filter((el) => {
      const r = el.getBoundingClientRect(); return r.width && (r.right > de.clientWidth + 1 || r.left < -1) && !clips(el);
    });
    const set = new Set(bad);
    out.culprits = bad.filter((el) => !set.has(el.parentElement)).slice(0, 5)
      .map((el) => { const r = el.getBoundingClientRect(); return sel(el) + ' right=' + Math.round(r.right) + ' w=' + Math.round(r.width); });
  }

  // text elements = elements with their own non-empty text node
  const texts = [...document.body.querySelectorAll('*')].filter((el) =>
    !/^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE|SVG|TITLE)$/i.test(el.tagName) &&
    [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1));

  // any CSS colour (rgb, hsl, oklch, lab, color(), named) → [r,g,b,a] in sRGB, via a 1×1 canvas
  const cc = document.createElement('canvas'); cc.width = cc.height = 1;
  const cx = cc.getContext('2d', { willReadFrequently: true });
  const rgba = (str) => {
    if (!str || str === 'none') return null;
    if (/^transparent$/i.test(str)) return [0, 0, 0, 0];
    cx.fillStyle = '#010203'; cx.fillStyle = str;
    if (cx.fillStyle === '#010203' && !/^(#010203|rgb\(1, 2, 3\))$/i.test(str)) return null;   // unparsable
    cx.clearRect(0, 0, 1, 1); cx.fillRect(0, 0, 1, 1);
    const d = cx.getImageData(0, 0, 1, 1).data;
    return [d[0], d[1], d[2], d[3] / 255];
  };
  const COLOR_RE = /(?:rgba?|hsla?|oklch|oklab|lch|lab|hwb|color)\([^()]*\)|#[0-9a-f]{3,8}\b|\btransparent\b/gi;
  const over = (fg, bg) => fg.map((v, i) => (i < 3 ? fg[3] * v + (1 - fg[3]) * bg[i] : 1));
  const lum = (c) => { const [r, g, b] = c.slice(0, 3).map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
  const effOpacity = (el) => { let o = 1; for (let n = el; n && n.nodeType === 1; n = n.parentElement) o *= +getComputedStyle(n).opacity; return o; };

  // 2. contrast, 3. stuck-invisible, 4. tiny text
  const lowContrast = [], invisible = [], tiny = [], overImage = [], onGradient = [];
  for (const el of texts) {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    if (!r.width || !r.height || cs.visibility === 'hidden') continue;
    const sample = el.textContent.trim().replace(/\s+/g, ' ').slice(0, 40);
    let op = effOpacity(el);
    if (op < 0.05) {
      // opacity 0 + pointer-events:none / aria-hidden = a deliberate toggle state (tabs, flip cards), not a stuck reveal
      let n = el; while (n && +getComputedStyle(n).opacity >= 0.05) n = n.parentElement;
      // …or a slide parked off-screen inside a horizontal scroller/carousel (shown when swiped to)
      const offSlide = () => { for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
        if (/auto|scroll|hidden|clip/.test(getComputedStyle(a).overflowX) && a.scrollWidth > a.clientWidth + 1) {
          const ar = a.getBoundingClientRect(); return r.right <= ar.left + 1 || r.left >= ar.right - 1; } } return false; };
      const collapsed = n && (n.getBoundingClientRect().height < 1 || n.getBoundingClientRect().width < 1);   // e.g. li.hid{opacity:0;height:0}
      // …or one half of a cross-fade (tabs, flip card, before/after): a visible sibling occupies the same spot
      const crossFade = () => { if (!n || !n.parentElement) return false; const nr = n.getBoundingClientRect();
        return [...n.parentElement.children].some((sib) => { if (sib === n) return false; const sr = sib.getBoundingClientRect();
          return +getComputedStyle(sib).opacity > 0.5 && sr.width && sr.height &&
            sr.left < nr.right && sr.right > nr.left && sr.top < nr.bottom && sr.bottom > nr.top; }); };
      const deliberate = (n && (collapsed || n.closest('[aria-hidden="true"],[hidden],[inert]'))) || offSlide() || crossFade();
      // inside a fixed/sticky overlay (scroll hints, toasts) it is UI chrome, not page content — warn only
      let overlay = false; for (let a = el; a && a !== document.body; a = a.parentElement) if (/fixed|sticky/.test(getComputedStyle(a).position)) { overlay = true; break; }
      if (!deliberate) invisible.push({ el, overlay, label: sel(el) + ' «' + sample + '»' });
      continue;
    }
    const fs = parseFloat(cs.fontSize);
    if (innerWidth < 768 && fs < 12) tiny.push(sel(el) + ' ' + fs + 'px «' + sample + '»');
    const fill = rgba(cs.webkitTextFillColor) || rgba(cs.color);
    if (!fill || fill[3] === 0) continue;                    // gradient/clip text — eye only
    // background layers: what is actually under the text's centre, top to bottom
    window.scrollTo(0, Math.max(0, r.top + scrollY - innerHeight / 2));
    if (op < 0.999) { await new Promise((z) => setTimeout(z, 900)); op = effOpacity(el); if (op < 0.05) continue; }   // let a reveal finish; faded out meanwhile = transient
    const rr = el.getBoundingClientRect();
    let stack = document.elementsFromPoint(rr.left + Math.min(rr.width / 2, 20), rr.top + rr.height / 2);
    const i = stack.indexOf(el);
    const below = i >= 0 ? stack.slice(i) : (() => { const a = []; for (let n = el; n; n = n.parentElement) a.push(n); return a; })();
    const layers = []; let base = [255, 255, 255, 1], image = false, gradient = false;
    for (const n of below) {
      if (n !== el && /^(IMG|VIDEO|CANVAS|PICTURE|IFRAME)$/.test(n.tagName)) { image = true; break; }
      const ns = getComputedStyle(n);
      if (/url\(/.test(ns.backgroundImage)) { image = true; break; }
      if (/gradient/.test(ns.backgroundImage)) {
        const stops = (ns.backgroundImage.match(COLOR_RE) || []).map(rgba).filter(Boolean);
        if (stops.length) { layers.push(stops); gradient = true; }
      }
      const bc = rgba(ns.backgroundColor);
      if (bc && bc[3] > 0) { if (bc[3] >= 0.999) { base = bc; break; } layers.push([bc]); }
    }
    if (image) { overImage.push(sel(el) + ' «' + sample + '»'); continue; }
    let bgs = [base];
    for (let k = layers.length - 1; k >= 0; k--) bgs = layers[k].flatMap((s) => bgs.map((u) => over(s, u)));
    const fg0 = [fill[0], fill[1], fill[2], fill[3] * op];
    const ratios = bgs.map((b) => { const fg = fg0[3] < 1 ? over(fg0, b) : fg0;
      const [hi, lo] = [lum(fg), lum(b)].sort((x, y) => y - x); return (hi + 0.05) / (lo + 0.05); });
    const large = fs >= 24 || (fs >= 18.6 && +cs.fontWeight >= 700);
    const need = large ? 3 : 4.5;
    // on a gradient the text sits on only part of it: fail only if it fails everywhere, otherwise ask for eyes
    if (gradient && Math.max(...ratios) >= need) { if (Math.min(...ratios) < need) onGradient.push(sel(el) + ' «' + sample + '»'); continue; }
    const ratio = gradient ? Math.max(...ratios) : Math.min(...ratios);
    // below 3 nobody reads it comfortably (FAIL); 3..4.5 is weak for small text (WARN)
    if (ratio < need) lowContrast.push({ el: sel(el), text: sample, ratio: +ratio.toFixed(2), need, color: cs.color,
      bg: bgs.map((b) => 'rgb(' + b.slice(0, 3).map(Math.round).join(',') + ')').join(' | '), fontSize: fs, opacity: +op.toFixed(2) });
  }
  // looping animations (typing demos, carousels) hide text only part of the time: resample over ~6s
  // back at the top first: scroll hints ("крутите вниз") hide on scroll and come back there
  window.scrollTo(0, 0);
  let still = invisible;
  for (let k = 0; k < 4 && still.length; k++) {
    await new Promise((z) => setTimeout(z, 1500));
    still = still.filter((x) => effOpacity(x.el) < 0.05);
  }
  window.scrollTo(0, 0);
  const dedup = (a) => [...new Map(a.map((x) => [typeof x === 'string' ? x : x.el + x.ratio, x])).values()];
  out.lowContrast = dedup(lowContrast).sort((a, b) => a.ratio - b.ratio);
  out.invisible = dedup(still.filter((x) => !x.overlay).map((x) => x.label));
  out.hiddenOverlay = dedup(still.filter((x) => x.overlay).map((x) => x.label));
  out.tiny = dedup(tiny);
  out.overImage = dedup(overImage).length;
  out.onGradient = dedup(onGradient);

  // 5. fonts without Cyrillic (only families used on Cyrillic text)
  const generic = /^(serif|sans-serif|monospace|cursive|fantasy|system-ui|ui-\w+|-apple-system|inherit|initial)$/i;
  const fams = new Set();
  for (const el of texts) if (/[А-Яа-яЁё]/.test(el.textContent)) {
    const f = getComputedStyle(el).fontFamily.split(',')[0].trim().replace(/^["']|["']$/g, '');
    if (f && !generic.test(f)) fams.add(f);
  }
  const ctx = document.createElement('canvas').getContext('2d');
  const w = (font) => { ctx.font = font; return ctx.measureText('ЖжЩщЫыЁёДдФф').width; };
  const same = (f, sample) => ['monospace', 'serif'].every((g) => {
    ctx.font = '72px "' + f + '", ' + g; const a = ctx.measureText(sample).width;
    ctx.font = '72px ' + g; return Math.abs(a - ctx.measureText(sample).width) < 0.5; });
  out.noCyrillic = []; out.fontNotLoaded = [];
  for (const f of fams) {
    try { await document.fonts.load('72px "' + f + '"', 'Жж'); } catch {}
    const faces = [...document.fonts].filter((ff) => ff.family.replace(/^["']|["']$/g, '') === f);
    const loaded = faces.some((ff) => ff.status === 'loaded');
    if (faces.length && !loaded) { out.fontNotLoaded.push(f); continue; }          // declared, file never arrived
    if (!faces.length && same(f, 'abcxyzABC')) { out.fontNotLoaded.push(f); continue; }   // not declared, not installed
    if (same(f, 'ЖжЩщЫыЁёДдФф')) out.noCyrillic.push(f);
  }

  // 6. broken images
  out.brokenImages = [...document.images].filter((im) => im.complete && im.naturalWidth === 0 && im.src)
    .map((im) => im.getAttribute('src')).slice(0, 5);
  out.pendingImages = [...document.images].filter((im) => !im.complete).map((im) => im.getAttribute('src')).slice(0, 5);
  return out;
})()`;

const SCROLL_THROUGH = String.raw`(async () => {
  const step = Math.max(200, innerHeight * 0.7);
  for (let y = 0; y < document.documentElement.scrollHeight; y += step) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 120)); }
  scrollTo(0, document.documentElement.scrollHeight); await new Promise((r) => setTimeout(r, 400));
  scrollTo(0, 0); await new Promise((r) => setTimeout(r, 600));
  return true;
})()`;

// ---------- minimal CDP client ----------
async function main() {
  const profile = mkdtempSync(join(tmpdir(), 'df-check-'));
  const chrome = spawn(chromePath(), ['--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', '--hide-scrollbars', '--allow-file-access-from-files', 'about:blank'],
    { stdio: 'ignore' });
  let port;
  for (let t = 0; t < 100 && !port; t++) {
    await sleep(100);
    const f = join(profile, 'DevToolsActivePort');
    if (existsSync(f)) port = readFileSync(f, 'utf8').split('\n')[0].trim();
  }
  if (!port) { chrome.kill(); throw new Error('Chrome did not start'); }
  let ws;
  try {
  const tab = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: 'PUT' })).json();
  ws = new WebSocket(tab.webSocketDebuggerUrl);
  await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
  let id = 0; const pending = new Map(); const listeners = [];
  ws.onmessage = (m) => { const d = JSON.parse(m.data);
    if (d.id && pending.has(d.id)) { const { res, rej } = pending.get(d.id); pending.delete(d.id); d.error ? rej(new Error(d.error.message)) : res(d.result); }
    else listeners.forEach((l) => l(d)); };
  const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id;
    const t = setTimeout(() => { pending.delete(i); rej(new Error(method + ' timed out')); }, 90000);
    pending.set(i, { res: (v) => { clearTimeout(t); res(v); }, rej: (e) => { clearTimeout(t); rej(e); } });
    ws.send(JSON.stringify({ id: i, method, params })); });
  ws.onclose = () => { for (const { rej } of pending.values()) rej(new Error('Chrome connection closed')); pending.clear(); };
  const once = (method, ms = 15000) => new Promise((res) => { const t = setTimeout(res, ms);
    const l = (d) => { if (d.method === method) { clearTimeout(t); listeners.splice(listeners.indexOf(l), 1); res(d); } }; listeners.push(l); });
  const evaluate = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true, timeout: 60000 });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text); return r.result.value; };

  await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
  let failedReqs = []; const reqUrl = new Map();
  listeners.push((d) => {
    if (d.method === 'Network.requestWillBeSent') reqUrl.set(d.params.requestId, d.params.request.url);
    if (d.method === 'Network.responseReceived' && d.params.response.status >= 400)
      failedReqs.push(d.params.response.status + ' ' + d.params.response.url);
    if (d.method === 'Network.loadingFailed' && !d.params.canceled)
      failedReqs.push(d.params.errorText + ' ' + (reqUrl.get(d.params.requestId) || '?'));
  });
  let jsErrors = [];
  listeners.push((d) => { if (d.method === 'Runtime.exceptionThrown') jsErrors.push(d.params.exceptionDetails.exception?.description?.split('\n')[0] || d.params.exceptionDetails.text); });
  if (shotsDir) mkdirSync(shotsDir, { recursive: true });

  const report = []; let fails = 0;
  for (const url of targets) {
    for (const width of widths) {
      jsErrors = []; failedReqs = [];
      const height = width < 768 ? 844 : 900;
      await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: width < 768 });
      const loaded = once('Page.loadEventFired');
      await send('Page.navigate', { url });
      await loaded; await sleep(800);
      await evaluate(SCROLL_THROUGH);
      const m = await evaluate(MEASURE);
      if (shotsDir) {
        const shot = await send('Page.captureScreenshot', { format: 'png' });
        writeFileSync(join(shotsDir, `${basename(url).replace(/\.html$/, '')}-${width}.png`), Buffer.from(shot.data, 'base64'));
      }
      const problems = [];
      // a phone zooms out to fit an over-wide page, so innerWidth > width means overflow, not a broken gate
      if (m.innerW < width - 1) problems.push(`FAIL viewport is ${m.innerW}, expected ${width} — numbers below are not trustworthy`);
      if (m.overflow || m.innerW > width + 1) problems.push(`FAIL horizontal scroll: page ${m.scrollW}px wide at ${width}px` +
        (m.innerW > width + 1 ? ' (phone would zoom the whole page out)' : '') + ` — ${(m.culprits || []).join('; ') || 'culprit not isolated'}`);
      const hard = m.lowContrast.filter((c) => c.ratio < 3), weak = m.lowContrast.filter((c) => c.ratio >= 3);
      for (const c of hard.slice(0, 8)) problems.push(`FAIL unreadable, contrast ${c.ratio} (need ${c.need}): ${c.el} «${c.text}» ${c.color} on ${c.bg.split(' | ')[0]}${c.opacity < 1 ? ` (element faded to opacity ${c.opacity})` : ''}`);
      if (hard.length > 8) problems.push(`FAIL …and ${hard.length - 8} more unreadable texts`);
      if (weak.length) problems.push(`WARN ${weak.length} small texts with weak contrast 3–4.5 (worst ${weak[0].ratio}: ${weak[0].el} «${weak[0].text}») — fix if it is body copy or a CTA`);
      for (const s of m.invisible.slice(0, 5)) problems.push(`FAIL invisible after full scroll (stuck reveal?): ${s}`);
      if (m.invisible.length > 5) problems.push(`FAIL …and ${m.invisible.length - 5} more invisible texts`);
      for (const s of m.hiddenOverlay.slice(0, 3)) problems.push(`WARN hidden text in a fixed/sticky overlay (fine if it is a hint that goes away on purpose): ${s}`);
      for (const f of m.fontNotLoaded) problems.push(`FAIL font not loaded (wrong name/link, or not installed): "${f}"`);
      for (const f of m.noCyrillic) problems.push(`FAIL font has no Cyrillic, text falls back: "${f}"`);
      for (const s of m.brokenImages) problems.push(`FAIL broken image: ${s}`);
      for (const s of [...new Set(failedReqs)].filter((u) => !/favicon/i.test(u)).slice(0, 5)) problems.push(`FAIL request failed: ${s.slice(0, 160)}`);
      for (const s of m.pendingImages) problems.push(`WARN image still not loaded after scroll: ${s}`);
      for (const e of [...new Set(jsErrors)].slice(0, 3)) problems.push(`FAIL JS error: ${e}`);
      for (const s of m.tiny.slice(0, 3)) problems.push(`WARN text under 12px on phone: ${s}`);
      if (m.overImage) problems.push(`NOTE ${m.overImage} text blocks sit on photos/video — contrast not computable, check those by eye`);
      if (m.onGradient.length) problems.push(`NOTE ${m.onGradient.length} texts on a gradient pass on some stops and fail on others — check by eye (first: ${m.onGradient[0]})`);
      const failed = problems.some((p) => p.startsWith('FAIL'));
      if (failed) fails++;
      console.log(`${failed ? '✗' : '✓'} ${decodeURIComponent(basename(url))} @${width}`);
      for (const p of problems) console.log('   ' + p);
      report.push({ url, width, failed, problems, raw: m, jsErrors });
    }
  }
  if (jsonOut) writeFileSync(jsonOut, JSON.stringify(report, null, 2));
  console.log(`\n${fails ? fails + ' page×width combinations FAILED' : 'Nothing found'} (${report.length} checked). ` +
    'A clean run means only that these checks found nothing — still look at every page yourself.');
  return fails ? 1 : 0;
  } finally {
    try { ws.close(); } catch {}
    chrome.kill();
    await sleep(300); try { rmSync(profile, { recursive: true, force: true }); } catch {}
  }
}

main().then((code) => process.exit(code)).catch((e) => { console.error(e.message); process.exit(2); });
