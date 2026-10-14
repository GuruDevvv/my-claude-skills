"""Browser measurements in real Chrome (Playwright + CDP). Read-only: non-GET requests are aborted,
no typing, no form submits, no link clicks.

Usage:
  python render_audit.py URL OUT.json [--profiles mobile,mobile_slow,desktop] [--runs 3] [--shots PREFIX] [--interact]

Per profile: N cold runs (fresh context each) -> median/min/max of TTFB, FCP, LCP, CLS (session windows), TBT;
one warm run (reload in the same context). The last cold run also scrolls the whole page and collects:
weight split (first screen / everything except video / video), videos, images, layout, coverage.
--interact clicks safe toggles (buttons that are not submit, [aria-expanded], summary) to get a lab INP.
"""
import argparse, json, statistics, sys, time
from playwright.sync_api import sync_playwright

UA_TAIL = " SiteAudit-Bot (read-only audit)"
PROFILES = {
    # name: viewport, dpr, mobile, cpu slowdown, network (latency ms, down Mbit/s, up Mbit/s) or None
    "mobile":      dict(vp=(360, 800), dpr=3, mobile=True, cpu=1, net=None),
    "mobile_390":  dict(vp=(390, 844), dpr=3, mobile=True, cpu=1, net=None),
    "mobile_4g":   dict(vp=(360, 800), dpr=3, mobile=True, cpu=2, net=(70, 9.0, 3.0)),
    "mobile_slow": dict(vp=(360, 800), dpr=3, mobile=True, cpu=4, net=(150, 1.6, 0.75)),
    "desktop":     dict(vp=(1366, 768), dpr=1, mobile=False, cpu=1, net=None),
    "desktop_1440": dict(vp=(1440, 900), dpr=1, mobile=False, cpu=1, net=None),
}
INIT = r"""
window.__m = {lcp: null, lcpEl: null, shifts: [], longtasks: [], fcp: null, events: []};
new PerformanceObserver(l => { for (const e of l.getEntries()) { __m.lcp = e.startTime; __m.lcpSize = e.size;
  __m.lcpEl = e.element ? (e.element.tagName + (e.element.id ? '#' + e.element.id : '') + '.' + String(e.element.className || '').slice(0, 40) + ' ' + (e.url || '')).slice(0, 180) : (e.url || ''); } })
  .observe({type: 'largest-contentful-paint', buffered: true});
new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) __m.shifts.push({t: e.startTime, v: e.value,
  src: (e.sources || []).map(s => s.node ? (s.node.nodeName + '.' + String(s.node.className || '')).slice(0, 60) : '?')}); })
  .observe({type: 'layout-shift', buffered: true});
new PerformanceObserver(l => { for (const e of l.getEntries()) __m.longtasks.push({t: e.startTime, d: e.duration}); })
  .observe({type: 'longtask', buffered: true});
new PerformanceObserver(l => { for (const e of l.getEntries()) if (e.name === 'first-contentful-paint') __m.fcp = e.startTime; })
  .observe({type: 'paint', buffered: true});
try { new PerformanceObserver(l => { for (const e of l.getEntries()) __m.events.push({name: e.name, d: e.duration, id: e.interactionId}); })
  .observe({type: 'event', durationThreshold: 16, buffered: true}); } catch (e) {}
window.__cls = () => { let best = 0, cur = 0, start = -1, prev = -1;
  for (const s of __m.shifts) { if (start < 0 || s.t - prev > 1000 || s.t - start > 5000) { cur = 0; start = s.t; } cur += s.v; prev = s.t; best = Math.max(best, cur); }
  return best; };
"""

def setup(br, prof):
    p = PROFILES[prof]
    ctx = br.new_context(viewport={"width": p["vp"][0], "height": p["vp"][1]}, device_scale_factor=p["dpr"],
                         is_mobile=p["mobile"], has_touch=p["mobile"], locale="ru-RU",
                         user_agent=(("Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v} Mobile Safari/537.36")
                                     if p["mobile"] else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v} Safari/537.36"
                                     ).format(v=br.version) + UA_TAIL)
    page = ctx.new_page(); cdp = ctx.new_cdp_session(page)
    cdp.send("Network.enable")
    if p["cpu"] > 1: cdp.send("Emulation.setCPUThrottlingRate", {"rate": p["cpu"]})
    if p["net"]:
        lat, down, up = p["net"]
        cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": lat,
                 "downloadThroughput": down * 1e6 / 8, "uploadThroughput": up * 1e6 / 8})
    blocked = []
    def guard(route):
        if route.request.method not in ("GET", "HEAD"):
            blocked.append([route.request.method, route.request.url]); return route.abort()
        return route.continue_()
    page.route("**/*", guard)
    page.add_init_script(INIT)
    return ctx, page, cdp, blocked

def track(cdp):
    reqs = {}
    def on_req(e):
        r = e["request"]; reqs[e["requestId"]] = {"url": r["url"], "method": r["method"], "type": e.get("type"), "t0": e["timestamp"], "bytes": 0}
    def on_resp(e):
        x = reqs.get(e["requestId"])
        if x:
            rr = e["response"]; h = {k.lower(): v for k, v in (rr.get("headers") or {}).items()}
            x.update(status=rr["status"], mime=rr.get("mimeType"), proto=rr.get("protocol"), enc=h.get("content-encoding"),
                     cache=h.get("cache-control"), from_cache=rr.get("fromDiskCache") or rr.get("fromPrefetchCache"),
                     content_length=h.get("content-length"), content_range=h.get("content-range"))
    def on_fin(e):
        x = reqs.get(e["requestId"])
        if x: x["bytes"] = e["encodedDataLength"]; x["t1"] = e["timestamp"]
    def on_fail(e):
        x = reqs.get(e["requestId"])
        if x: x["failed"] = e.get("errorText"); x["canceled"] = e.get("canceled")
    cdp.on("Network.requestWillBeSent", on_req); cdp.on("Network.responseReceived", on_resp)
    cdp.on("Network.loadingFinished", on_fin); cdp.on("Network.loadingFailed", on_fail)
    return reqs

def metrics(page):
    m = page.evaluate("({lcp: __m.lcp, lcpEl: __m.lcpEl, fcp: __m.fcp, cls: __cls(), longtasks: __m.longtasks})")
    nav = page.evaluate("(() => { const n = performance.getEntriesByType('navigation')[0]; return n ? {ttfb: n.responseStart, dcl: n.domContentLoadedEventEnd, load: n.loadEventEnd, proto: n.nextHopProtocol} : {}; })()")
    fcp = m["fcp"] or 0
    m["tbt"] = round(sum(max(0, t["d"] - 50) for t in m["longtasks"] if t["t"] >= fcp), 1)
    m["longtasks"] = len(m["longtasks"]); m.update(nav)
    return m

def wait_quiet(page, reqs, quiet_ms=2000, cap_ms=10000):
    t0 = time.time(); last = len(reqs)
    while (time.time() - t0) * 1000 < cap_ms:
        page.wait_for_timeout(quiet_ms)
        if len(reqs) == last: return
        last = len(reqs)

def kind(r):
    m = (r.get("mime") or ""); u = r["url"].split("?")[0].lower()
    if m.startswith("video") or u.endswith((".mp4", ".webm", ".mov", ".m3u8")): return "video"
    if m.startswith("image"): return "image"
    if "font" in m or u.endswith((".woff", ".woff2", ".ttf")): return "font"
    if "css" in m: return "css"
    if "javascript" in m or u.endswith(".js"): return "js"
    if "html" in m: return "html"
    return "other"

def weight(reqs, host):
    from urllib.parse import urlsplit
    out = {"requests": 0, "bytes": 0, "by_kind": {}, "third_party_bytes": 0, "third_party_hosts": set()}
    for r in reqs:
        if r["url"].startswith("data:"): continue
        out["requests"] += 1; b = r.get("bytes") or 0; out["bytes"] += b
        k = kind(r); out["by_kind"][k] = out["by_kind"].get(k, 0) + b
        h = urlsplit(r["url"]).hostname
        if h and h != host: out["third_party_bytes"] += b; out["third_party_hosts"].add(h)
    out["third_party_hosts"] = sorted(out["third_party_hosts"])
    out["non_video_bytes"] = out["bytes"] - out["by_kind"].get("video", 0)
    return out

NOISE_FLOOR = {"ttfb": 50, "fcp": 100, "lcp": 100, "tbt": 50, "load": 100, "cls": 0.02}  # below this, spread is noise

def summarize(vals, key):
    vals = [v for v in vals if v is not None]
    if not vals: return None
    med = statistics.median(vals)
    spread = (max(vals) - min(vals)) / med * 100 if med else 0
    return {"median": round(med, 4), "min": round(min(vals), 4), "max": round(max(vals), 4), "n": len(vals),
            "unstable": spread > 20 and len(vals) > 1 and med >= NOISE_FLOOR.get(key, 0)}

def deep(page, cdp, reqs, host, shots, prof, interact):
    from urllib.parse import urlsplit
    first = [dict(v) for v in reqs.values()]
    res = {"weight_first_screen": weight(first, host)}
    if shots: page.screenshot(path=f"{shots}_{prof}_first.png")
    res["layout"] = page.evaluate(r"""() => { const de = document.documentElement, W = de.clientWidth;
      const over = []; for (const el of document.querySelectorAll('body *')) { const r = el.getBoundingClientRect();
        if (r.width && (r.right > W + 1) && getComputedStyle(el).position !== 'fixed') over.push(el.tagName + '.' + String(el.className || '').slice(0, 40)); }
      return {clientWidth: W, scrollWidth: de.scrollWidth, hscroll: (() => { const y = scrollY; scrollTo(60, y); const s = scrollX > 0; scrollTo(0, y); return s; })(), widthOverflow: de.scrollWidth > de.clientWidth, overflowing: over.slice(0, 15), domNodes: document.getElementsByTagName('*').length,
              docHeight: de.scrollHeight}; }""")
    sheets = {}  # handler first: CSS.enable replays styleSheetAdded for sheets that already exist
    cdp.on("CSS.styleSheetAdded", lambda e: sheets.__setitem__(e["header"]["styleSheetId"], {"url": e["header"].get("sourceURL"), "len": e["header"].get("length")}))
    cdp.send("DOM.enable"); cdp.send("CSS.enable")
    cdp.send("CSS.startRuleUsageTracking")
    h = res["layout"]["docHeight"]; y = 0
    while y < h:
        y += 600; page.evaluate(f"window.scrollTo(0,{y})"); page.wait_for_timeout(300); h = page.evaluate("document.documentElement.scrollHeight")
    wait_quiet(page, reqs)
    res["cls_after_scroll"] = round(page.evaluate("__cls()"), 4)
    res["shifts_after_scroll"] = page.evaluate("__m.shifts.slice(0, 20)")
    if interact:
        clicked = page.evaluate(r"""() => { const out = [];
          const els = [...document.querySelectorAll('button:not([type=submit]), [aria-expanded], summary, [role=button]')]
            .filter(e => !e.closest('form') && !e.closest('a') && e.offsetParent !== null).slice(0, 5);
          els.forEach((e, i) => e.setAttribute('data-audit-click', i)); return els.map(e => (e.textContent || e.getAttribute('aria-label') || '').trim().slice(0, 30)); }""")
        for i in range(len(clicked)):
            try: page.click(f"[data-audit-click='{i}']", timeout=3000, no_wait_after=True); page.wait_for_timeout(400)
            except Exception: pass
        ev = page.evaluate("__m.events")
        by_id = {}
        for e in ev:
            if e.get("id"): by_id[e["id"]] = max(by_id.get(e["id"], 0), e["d"])
        res["inp_lab"] = {"interactions": len(by_id), "max_ms": max(by_id.values()) if by_id else None, "clicked": clicked,
                          "note": "lab INP over N safe clicks, not field data"}
    res["videos"] = page.evaluate(r"""() => [...document.querySelectorAll('video')].map(v => { const r = v.getBoundingClientRect();
      const raw = v.currentSrc || v.getAttribute('src') || (v.querySelector('source') || {}).src || v.dataset.src || '';
      return {src: raw ? new URL(raw, location.href).href : '', autoplay: v.autoplay, muted: v.muted,
              playsinline: v.playsInline, preload: v.getAttribute('preload'), poster: v.poster || null, w: v.videoWidth, h: v.videoHeight,
              disp: Math.round(r.width) + 'x' + Math.round(r.height), hasAudioTrackHint: v.mozHasAudio ?? null}; })""")
    res["images"] = page.evaluate(r"""() => [...document.images].map(i => { const r = i.getBoundingClientRect();
      return {src: i.currentSrc, nat: [i.naturalWidth, i.naturalHeight], disp: [Math.round(r.width), Math.round(r.height)], dpr: devicePixelRatio,
              loading: i.loading, wh: i.hasAttribute('width') && i.hasAttribute('height'), srcset: i.hasAttribute('srcset')}; })""")
    all_reqs = [dict(v) for v in reqs.values()]
    res["weight_full"] = weight(all_reqs, host)
    for v in res["videos"]:
        rs = [r for r in all_reqs if v["src"] and r["url"].split("?")[0] == v["src"].split("?")[0]]
        v["bytes_transferred"] = sum(r.get("bytes") or 0 for r in rs)
        cr = next((r.get("content_range") for r in rs if r.get("content_range")), None)
        v["file_bytes"] = int(cr.split("/")[-1]) if cr and cr.split("/")[-1].isdigit() else next((int(r["content_length"]) for r in rs if (r.get("content_length") or "").isdigit()), None)
        # bytes, not a yes/no: preload="metadata" fetches a few KB before scroll, which is not "downloaded early"
        v["bytes_before_scroll"] = sum(r.get("bytes") or 0 for r in first if v["src"] and r["url"].split("?")[0] == v["src"].split("?")[0])
    css = cdp.send("CSS.stopRuleUsageTracking")["ruleUsage"]; used = {}
    for r in css:
        if r["used"]: used.setdefault(r["styleSheetId"], []).append((r["startOffset"], r["endOffset"]))
    cov_css = []
    for sid, info in sheets.items():
        tot, last = 0, -1
        for a, b in sorted(used.get(sid, [])):
            a = max(a, last)
            if b > a: tot += b - a; last = b
        url = info["url"] or ""
        if not url and (info["len"] or 0) < 500: continue  # style attributes / tiny injected sheets
        if "fonts.googleapis" in url or "/css2?" in url: continue  # @font-face rules never count as "used"
        if info["len"]: cov_css.append({"url": info["url"] or "(inline)", "bytes": info["len"], "unused_bytes": info["len"] - tot,
                                        "unused_pct": round(100 - tot / info["len"] * 100, 1)})
    js = cdp.send("Profiler.takePreciseCoverage")["result"]; cov_js = []
    for s in js:
        if not s["url"] or s["url"].startswith(("chrome", "pptr", "__playwright")): continue
        total = max((f["ranges"][0]["endOffset"] for f in s["functions"] if f["ranges"]), default=0)
        unused = sum(r["endOffset"] - r["startOffset"] for f in s["functions"] for r in f["ranges"] if r["count"] == 0)
        cov_js.append({"url": s["url"], "bytes": total, "unused_bytes_approx": min(unused, total)})
    res["coverage"] = {"css": cov_css, "js": cov_js, "note": "after scrolling" + (" and clicks" if interact else "") + "; code for states that never happened (a form submit) counts as unused"}
    if shots: page.screenshot(path=f"{shots}_{prof}_full.png", full_page=True)
    return res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("out")
    ap.add_argument("--profiles", default="mobile,mobile_slow,desktop"); ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--shots"); ap.add_argument("--interact", action="store_true")
    a = ap.parse_args()
    from urllib.parse import urlsplit
    host = urlsplit(a.url).hostname
    R = {"url": a.url, "runs_per_profile": a.runs, "profiles": {}}
    with sync_playwright() as pw:
        br = pw.chromium.launch(channel="chrome", headless=True)
        R["chrome"] = br.version
        for prof in a.profiles.split(","):
            P = {"settings": PROFILES[prof], "cold": [], "console": [], "pageerrors": [], "blocked_non_get": []}
            for i in range(a.runs):
                ctx, page, cdp, blocked = setup(br, prof); reqs = track(cdp)
                if i == a.runs - 1:
                    cdp.send("Profiler.enable"); cdp.send("Profiler.startPreciseCoverage", {"callCount": False, "detailed": True})
                    page.on("console", lambda m: P["console"].append([m.type, m.text[:300]]) if m.type in ("error", "warning") else None)
                    page.on("pageerror", lambda e: P["pageerrors"].append(str(e)[:300]))
                page.goto(a.url, wait_until="load", timeout=180000)
                wait_quiet(page, reqs)
                m = metrics(page); P["cold"].append(m)
                if i == a.runs - 1:
                    P.update(deep(page, cdp, reqs, host, a.shots, prof, a.interact))
                    # warm: reload in the same context (HTTP cache kept)
                    wreqs = track(cdp); page.goto(a.url, wait_until="load", timeout=180000); wait_quiet(page, wreqs)
                    P["warm"] = metrics(page)
                    P["warm"]["bytes"] = sum(r.get("bytes") or 0 for r in wreqs.values())
                    P["warm"]["from_cache"] = sum(1 for r in wreqs.values() if r.get("from_cache"))
                    P["warm"]["requests"] = len(wreqs)
                P["blocked_non_get"] += blocked
                ctx.close()
            P["summary"] = {k: summarize([r.get(k) for r in P["cold"]], k) for k in ("ttfb", "fcp", "lcp", "cls", "tbt", "load")}
            P["lcp_elements"] = sorted({r.get("lcpEl") or "" for r in P["cold"]})
            R["profiles"][prof] = P
            print("done", prof, file=sys.stderr)
        br.close()
    json.dump(R, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("ok", ", ".join(f"{p}: LCP {v['summary']['lcp']['median'] if v['summary']['lcp'] else '—'} ms" for p, v in R["profiles"].items()))

if __name__ == "__main__":
    main()
