"""Accessibility and layout checks a machine can measure. Read-only: non-GET requests are aborted,
nothing is typed or submitted. Tab presses only move focus.

Usage:
  python a11y_audit.py URL OUT.json [--shots PREFIX]

Collects: axe-core violations + incomplete (needs human eye), zoom blocking, text sizes, touch targets
(24 px WCAG 2.5.8 / 44 px recommendation), form field names and keyboards, nameless controls,
fake buttons, autoplay with sound, 320 px + 200 % text reflow, keyboard focus pass (visibility,
hidden under sticky header, traps), prefers-reduced-motion, page without JavaScript.
"""
import argparse, json, os, sys
from playwright.sync_api import sync_playwright

AXE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor", "axe.min.js")
MOBILE = dict(viewport={"width": 360, "height": 800}, device_scale_factor=3, is_mobile=True, has_touch=True, locale="ru-RU")

def guarded(ctx):
    page = ctx.new_page()
    page.route("**/*", lambda r: r.abort() if r.request.method not in ("GET", "HEAD") else r.continue_())
    return page

def reveal(page):
    page.wait_for_timeout(2500)
    h = page.evaluate("document.documentElement.scrollHeight")
    for y in range(0, h + 800, 700): page.evaluate(f"scrollTo(0,{y})"); page.wait_for_timeout(120)
    page.evaluate("scrollTo(0,0)"); page.wait_for_timeout(1200)

CHECKS_JS = r"""() => {
  const vis = el => { const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && !el.closest('[hidden],[aria-hidden=true]'); };
  const desc = el => (el.tagName + (el.id ? '#' + el.id : '') + (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '')).slice(0, 60);
  const name = el => (el.getAttribute('aria-label') || (el.getAttribute('aria-labelledby') || '').split(' ').map(i => (document.getElementById(i) || {}).textContent || '').join(' ')
    || (el.id && (document.querySelector('label[for="' + CSS.escape(el.id) + '"]') || {}).textContent) || (el.closest('label') || {}).textContent
    || el.getAttribute('title') || '').trim();
  const out = {};
  const vp = (document.querySelector('meta[name=viewport]') || {}).content || '';
  const ms = vp.match(/maximum-scale\s*=\s*([\d.]+)/);
  out.viewport = {content: vp, zoomBlocked: /user-scalable\s*=\s*(no|0)/i.test(vp) || (!!ms && parseFloat(ms[1]) < 2)};
  out.lang = document.documentElement.getAttribute('lang');
  // text sizes
  const seen = new Set(); let bodySmall = [], tiny = [];
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) { const n = w.currentNode, p = n.parentElement; if (!p || seen.has(p) || !n.textContent.trim() || !vis(p)) continue; seen.add(p);
    const fs = parseFloat(getComputedStyle(p).fontSize), t = n.textContent.trim().slice(0, 40);
    if (fs < 12) tiny.push(fs + 'px ' + desc(p) + ': ' + t);
    else if (fs < 16 && p.closest('p,li') && n.textContent.trim().length > 40) bodySmall.push(fs + 'px ' + desc(p) + ': ' + t); }
  out.text = {under12: tiny.length, under12Ex: tiny.slice(0, 10), bodyUnder16: bodySmall.length, bodyUnder16Ex: bodySmall.slice(0, 10)};
  // touch targets
  const t24 = [], t44 = [];
  for (const el of document.querySelectorAll('a[href],button,input:not([type=hidden]),select,textarea,[role=button],[onclick]')) {
    if (!vis(el)) continue;
    const cs = getComputedStyle(el), par = el.parentElement;
    const inlineInText = el.tagName === 'A' && cs.display === 'inline' && par && par.closest('p,li') && (par.textContent.trim().length > el.textContent.trim().length + 15);
    if (inlineInText) continue;
    const r = el.getBoundingClientRect(), d = desc(el) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height) + ' «' + (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 25) + '»';
    if (r.width < 24 || r.height < 24) t24.push(d); else if (r.width < 44 || r.height < 44) t44.push(d); }
  out.touch = {under24: t24.length, under24Ex: t24.slice(0, 12), under44: t44.length, under44Ex: t44.slice(0, 12)};
  // form fields
  out.fields = [...document.querySelectorAll('input:not([type=hidden]):not([type=submit]):not([type=button]),select,textarea')].map(el => {
    const nm = name(el), ph = el.getAttribute('placeholder') || '', hint = (el.name + ' ' + el.id + ' ' + ph + ' ' + nm).toLowerCase();
    const wantsTel = /phone|tel|телефон/.test(hint), wantsEmail = /mail|почт/.test(hint);
    return {el: desc(el), type: el.type, accessibleName: nm.slice(0, 60), placeholderOnly: !nm && !!ph, noName: !nm && !ph,
            autocomplete: el.getAttribute('autocomplete'), inputmode: el.getAttribute('inputmode'),
            keyboardMismatch: (wantsTel && el.type !== 'tel' && el.getAttribute('inputmode') !== 'tel') || (wantsEmail && el.type !== 'email'),
            preChecked: el.type === 'checkbox' && el.checked, visible: vis(el)}; });
  out.checkboxes = [...document.querySelectorAll('input[type=checkbox]')].map(el => ({label: name(el).slice(0, 120), checked: el.checked}));
  // nameless controls and fake buttons
  out.nameless = [...document.querySelectorAll('a[href],button,[role=button]')].filter(el => vis(el) && !(el.textContent.trim() || el.getAttribute('aria-label') || el.getAttribute('title')
    || [...el.querySelectorAll('img[alt],svg title')].some(i => (i.getAttribute('alt') || i.textContent).trim()))).map(desc).slice(0, 15);
  out.fakeButtons = [...document.querySelectorAll('div[onclick],span[onclick],li[onclick]')].filter(el => !el.getAttribute('role') || !el.hasAttribute('tabindex')).map(desc).slice(0, 15);
  out.autoplaySound = [...document.querySelectorAll('video[autoplay],audio[autoplay]')].filter(v => !v.muted).map(v => v.currentSrc || v.src);
  out.genericLinkTexts = (() => { const c = {}; for (const a of document.querySelectorAll('a[href]')) { const t = a.textContent.trim().toLowerCase();
    if (/^(подробнее|читать|далее|тут|здесь|ссылка|more|click here)$/.test(t)) c[t] = (c[t] || 0) + 1; } return c; })();
  return out; }"""

def tab_pass(page, max_tabs=60):
    page.add_style_tag(content="html,body{scroll-behavior:auto !important}")  # smooth scroll would fake "offscreen"
    page.evaluate("scrollTo(0,0)"); page.mouse.click(1, 1)
    seq, issues = [], {"noVisibleFocus": [], "obscured": [], "offscreen": []}
    for i in range(max_tabs):
        page.keyboard.press("Tab"); page.wait_for_timeout(250)
        info = page.evaluate(r"""() => { const el = document.activeElement; if (!el || el === document.body) return null;
          const key = el.tagName + '|' + (el.id || '') + '|' + (el.getAttribute('href') || '') + '|' + (el.textContent || '').trim().slice(0, 20);
          const st = e => { const c = getComputedStyle(e); return [c.outlineStyle, c.outlineWidth, c.outlineColor, c.boxShadow, c.borderColor, c.backgroundColor, c.textDecorationLine].join('/'); };
          const box = el.parentElement || el;  // focus may be drawn on the wrapper via :focus-within
          const focused = st(el) + '|' + st(box); el.blur(); const plain = st(el) + '|' + st(box); el.focus({preventScroll: true});
          const r = el.getBoundingClientRect(); const cx = r.left + r.width / 2, cy = r.top + Math.min(r.height / 2, 10);
          const top = (cx >= 0 && cy >= 0 && cx < innerWidth && cy < innerHeight) ? document.elementFromPoint(cx, cy) : null;
          return {key, label: (el.textContent || el.getAttribute('aria-label') || el.tagName).trim().slice(0, 30), sameStyle: focused === plain,
                  offscreen: r.bottom < 0 || r.top > innerHeight || r.right < 0 || r.left > innerWidth,
                  obscured: !!top && top !== el && !el.contains(top) && !top.contains(el)}; }""")
        if not info: continue
        seq.append(info["key"])
        if info["sameStyle"]: issues["noVisibleFocus"].append(info["label"])
        if info["obscured"]: issues["obscured"].append(info["label"])
        if info["offscreen"]: issues["offscreen"].append(info["label"])
    uniq = list(dict.fromkeys(seq))
    trap = len(seq) >= 30 and len(uniq) <= 3
    return {"tabs": len(seq), "unique_focused": len(uniq), "trap_suspected": trap,
            **{k: list(dict.fromkeys(v))[:12] for k, v in issues.items()},
            "counts": {k: len(set(v)) for k, v in issues.items()}}

def motion_state(page):
    return page.evaluate(r"""() => ({runningAnimations: document.getAnimations().filter(a => a.playState === 'running').length,
      playingVideos: [...document.querySelectorAll('video')].filter(v => !v.paused).length})""")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("url"); ap.add_argument("out"); ap.add_argument("--shots")
    a = ap.parse_args(); R = {"url": a.url}
    axe_src = open(AXE, encoding="utf-8").read()
    with sync_playwright() as pw:
        br = pw.chromium.launch(channel="chrome", headless=True)
        ctx = br.new_context(bypass_csp=True, **MOBILE); page = guarded(ctx)
        page.goto(a.url, wait_until="load", timeout=120000); reveal(page)
        R["normal_motion"] = motion_state(page)
        page.add_script_tag(content=axe_src)
        r = page.evaluate("axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice']}, resultTypes: ['violations','incomplete']})")
        pack = lambda v: {"id": v["id"], "impact": v["impact"], "help": v["help"], "elements": len(v["nodes"]),
                          "targets": [", ".join(n["target"]) if isinstance(n["target"], list) else str(n["target"]) for n in v["nodes"][:6]]}
        R["axe"] = {"version": r.get("testEngine", {}).get("version"), "violations": [pack(v) for v in r["violations"]],
                    "incomplete": [pack(v) for v in r["incomplete"]],
                    "note": "a clean axe run does not mean accessible: automation catches about a third of the issues"}
        R["checks"] = page.evaluate(CHECKS_JS)
        R["keyboard"] = tab_pass(page)
        if a.shots: page.screenshot(path=f"{a.shots}_a11y_mobile.png")
        ctx.close()
        # reduced motion
        ctx = br.new_context(reduced_motion="reduce", **MOBILE); page = guarded(ctx)
        page.goto(a.url, wait_until="load", timeout=120000); page.wait_for_timeout(3000)
        R["reduced_motion"] = {"reduce": motion_state(page), "normal": R.pop("normal_motion")}
        ctx.close()
        # 320 px + 200 % text
        ctx = br.new_context(viewport={"width": 320, "height": 640}, device_scale_factor=2, is_mobile=True, has_touch=True); page = guarded(ctx)
        page.goto(a.url, wait_until="load", timeout=120000); page.wait_for_timeout(2000)
        R["reflow_320"] = page.evaluate(r"""() => { const de = document.documentElement, W = de.clientWidth, c = [];
          const clipped = el => { for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
            const ox = getComputedStyle(p).overflowX; if ((ox === 'hidden' || ox === 'clip' || ox === 'auto' || ox === 'scroll') && p.getBoundingClientRect().right <= W + 1) return true; } return false; };
          for (const el of document.querySelectorAll('body *')) { const r = el.getBoundingClientRect();
            if (r.width && r.right > W + 1 && getComputedStyle(el).position !== 'fixed' && !clipped(el) && !(el.parentElement && el.parentElement.getBoundingClientRect().right > W + 1))
              c.push(el.tagName + '.' + String(el.className || '').slice(0, 40) + ' right=' + Math.round(r.right) + (el.currentSrc || el.src ? ' ' + String(el.currentSrc || el.src).split('/').pop() : '')); }
          return {scrollWidth: de.scrollWidth, clientWidth: W, hscroll: (() => { const y = scrollY; scrollTo(60, y); const s = scrollX > 0; scrollTo(0, y); return s; })(), widthOverflow: de.scrollWidth > de.clientWidth, culprits: c.slice(0, 10)}; }""")
        # double every element's text size; sizes are read first so inherited sizes are not doubled twice
        page.evaluate("(() => { const els = [...document.querySelectorAll('body *')]; const fs = els.map(e => parseFloat(getComputedStyle(e).fontSize)); els.forEach((e, i) => { if (fs[i]) e.style.setProperty('font-size', (fs[i] * 2) + 'px', 'important'); }); })()")
        page.wait_for_timeout(800)
        R["text_200"] = page.evaluate(r"""() => { const de = document.documentElement; const clipped = [];
          for (const el of document.querySelectorAll('body *')) { const cs = getComputedStyle(el);
            if ((cs.overflow + cs.overflowX + cs.overflowY).includes('hidden') && el.textContent.trim() && el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 0)
              clipped.push((el.tagName + '.' + String(el.className || '').slice(0, 30)) + ' «' + el.textContent.trim().slice(0, 30) + '»'); }
          return {hscroll: (() => { const y = scrollY; scrollTo(60, y); const s = scrollX > 0; scrollTo(0, y); return s; })(), widthOverflow: de.scrollWidth > de.clientWidth, scrollWidth: de.scrollWidth, clippedText: clipped.length, clippedEx: clipped.slice(0, 10)}; }""")
        if a.shots: page.screenshot(path=f"{a.shots}_text200.png", full_page=True)
        ctx.close()
        # no JavaScript
        ctx = br.new_context(viewport={"width": 360, "height": 800}, java_script_enabled=False); page = ctx.new_page()
        page.goto(a.url, wait_until="load", timeout=120000); page.wait_for_timeout(1500)
        R["no_js"] = page.evaluate(r"""() => { const vis = el => { const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
            return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && +cs.opacity > 0.05; };
          const hs = [...document.querySelectorAll('h1,h2,h3')];
          return {headings: hs.length, visibleHeadings: hs.filter(vis).length, textChars: document.body.innerText.length}; }""")
        if a.shots: page.screenshot(path=f"{a.shots}_nojs.png", full_page=True)
        br.close()
    json.dump(R, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    c = R["checks"]
    print(f"ok: axe violations {len(R['axe']['violations'])}, incomplete {len(R['axe']['incomplete'])}; "
          f"zoom blocked: {c['viewport']['zoomBlocked']}; targets <24px: {c['touch']['under24']}; Tab without visible focus: {R['keyboard']['counts']['noVisibleFocus']}")

if __name__ == "__main__":
    main()
