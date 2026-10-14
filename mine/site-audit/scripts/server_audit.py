"""Passive server-side checks of a LIVE domain. Read-only: GET/HEAD only, ~1 request per second.

Usage:
  python server_audit.py https://example.ru OUT.json [--pages /,/about/] [--delay 1.1] [--no-crtsh]

Covers: TLS/certificate/chain, security headers on HTML + static + 404 + redirect, compression and
cache, robots.txt / sitemap.xml, URL duplicates, sensitive-file probes (with false-200 fingerprint,
bodies are never stored or printed), messenger-bot previews, og:image, TTFB breakdown, bare IP, DNS.
"""
import argparse, hashlib, json, random, re, socket, ssl, string, sys, time, urllib.parse, http.client
from datetime import datetime, timezone

UA = "SiteAudit-Bot (read-only audit)"
BOT_UAS = {
    "telegram": "TelegramBot (like TwitterBot)",
    "whatsapp_facebook": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "vk": "Mozilla/5.0 (compatible; vkShare; +http://vk.com/dev/Share)",
}
SEC_HEADERS = ["strict-transport-security", "content-security-policy", "x-content-type-options",
               "x-frame-options", "referrer-policy", "permissions-policy",
               "cross-origin-opener-policy", "cross-origin-resource-policy"]
# path -> signature regex on the first 256 bytes (None = any non-fingerprint answer counts)
PROBES = {
    "/.git/HEAD": rb"^ref: ", "/.git/config": rb"\[core\]", "/.env": rb"(?m)^[A-Z_]{2,}=",
    "/.env.local": rb"(?m)^[A-Z_]{2,}=", "/.env.production": rb"(?m)^[A-Z_]{2,}=",
    "/docker-compose.yml": rb"services:|version:", "/.vscode/settings.json": rb"^\s*\{",
    "/CLAUDE.md": rb"#", "/HANDOFF.md": rb"#", "/TASKS.md": rb"#", "/.claude/settings.json": rb"^\s*\{",
    "/node_modules/": None, "/package.json": rb"^\s*\{", "/backup.zip": rb"^PK\x03\x04",
    "/dump.sql": rb"(?i)(create table|insert into|-- mysql|postgresql)", "/index.html.bak": rb"(?i)<html|<!doctype",
    "/index-old.html": rb"(?i)<html|<!doctype", "/.DS_Store": rb"Bud1",
    "/.well-known/security.txt": rb"(?i)contact:",
}
AI_BOTS = ["YandexBot", "Googlebot", "OAI-SearchBot", "GPTBot", "PerplexityBot", "ClaudeBot", "Yandex", "*"]
SECRET_PATTERNS = {  # client-side code patterns, severity
    "telegram_bot_token": (r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b", "Blocker"),
    "telegram_api_url": (r"api\.telegram\.org/bot", "Blocker"),
    "anthropic_key": (r"sk-ant-[A-Za-z0-9_-]{20,}", "Blocker"),
    "openrouter_key": (r"sk-or-[A-Za-z0-9_-]{20,}", "Blocker"),
    "openai_like_key": (r"\bsk-[A-Za-z0-9]{32,}", "Blocker"),
    "supabase_service_role": (r"service_role", "Blocker"),
}

def rnd(n=10): return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))

class Client:
    def __init__(s, delay): s.delay = delay; s.last = 0; s.count = 0; s.stop = None
    def req(s, url, method="GET", headers=None, rng=None, ua=UA, verify=True, keep_body=True, max_body=3_000_000):
        if s.stop: return {"skipped": s.stop}
        wait = s.delay - (time.time() - s.last)
        if wait > 0: time.sleep(wait)
        s.last = time.time(); s.count += 1
        u = urllib.parse.urlsplit(url)
        h = {"User-Agent": ua, "Accept-Encoding": "gzip, br", "Accept": "*/*"}
        if rng: h["Range"] = rng
        h.update(headers or {})
        ctx = ssl.create_default_context() if verify else ssl._create_unverified_context()
        try:
            C = http.client.HTTPSConnection(u.hostname, u.port or 443, timeout=20, context=ctx) if u.scheme == "https" \
                else http.client.HTTPConnection(u.hostname, u.port or 80, timeout=20)
            C.request(method, (u.path or "/") + ("?" + u.query if u.query else ""), headers=h)
            r = C.getresponse()
            body = r.read(max_body) if (method == "GET") else b""
            hd = {k.lower(): v for k, v in r.getheaders()}
            C.close()
            res = {"status": r.status, "version": "HTTP/1.1" if r.version == 11 else "HTTP/1.0", "headers": hd,
                   "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}
            if r.status == 429 or re.search(rb"(?i)captcha|ddos-guard|cf-chl|just a moment", body[:20000]) and r.status in (403, 503):
                s.stop = f"protection triggered on {url}: {r.status}"
                res["protection"] = True
            if keep_body: res["_body"] = body
            return res
        except Exception as e:
            return {"error": f"{type(e).__name__}: {e}"[:300]}

def strip(r):
    return {k: v for k, v in r.items() if k != "_body"}

def decode_body(r):
    b = r.get("_body") or b""
    enc = (r.get("headers") or {}).get("content-encoding", "")
    try:
        if enc == "gzip":
            import gzip; b = gzip.decompress(b)
        elif enc == "br":
            try:
                import brotli; b = brotli.decompress(b)
            except ImportError: return None
    except Exception: return None
    return b.decode("utf-8", "replace")

def tls_info(host, port=443):
    out = {}
    try:
        ctx = ssl.create_default_context(); ctx.set_alpn_protocols(["h2", "http/1.1"])
        with socket.create_connection((host, port), timeout=15) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ss:
                c = ss.getpeercert()
                out.update(verified=True, tls_version=ss.version(), alpn=ss.selected_alpn_protocol(), cipher=ss.cipher()[0])
        nb = datetime.strptime(c["notBefore"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        na = datetime.strptime(c["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        out.update(not_before=nb.date().isoformat(), not_after=na.date().isoformat(),
                   days_left=(na - now).days, age_days=(now - nb).days,
                   lifetime_days=(na - nb).days,
                   issuer=dict(x[0] for x in c.get("issuer", [])).get("organizationName"),
                   issuer_cn=dict(x[0] for x in c.get("issuer", [])).get("commonName"),
                   san=[v for k, v in c.get("subjectAltName", []) if k == "DNS"])
    except ssl.SSLCertVerificationError as e:
        out.update(verified=False, verify_error=str(e)[:300],
                   chain_incomplete_suspected="unable to get local issuer" in str(e))
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {e}"[:300]
    return out

def ttfb_breakdown(url, n=5, delay=1.1):
    u = urllib.parse.urlsplit(url); host = u.hostname; port = u.port or 443
    runs = []
    for i in range(n):
        time.sleep(delay)
        try:
            t0 = time.perf_counter(); ip = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)[0][4][0]; t1 = time.perf_counter()
            sock = socket.create_connection((ip, port), timeout=20); t2 = time.perf_counter()
            ss = ssl.create_default_context().wrap_socket(sock, server_hostname=host); t3 = time.perf_counter()
            ss.sendall(f"GET {u.path or '/'} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {UA}\r\nAccept-Encoding: gzip\r\nConnection: close\r\n\r\n".encode())
            ss.recv(1); t4 = time.perf_counter(); ss.close()
            runs.append({"dns": t1 - t0, "connect": t2 - t1, "tls": t3 - t2, "wait": t4 - t3, "total": t4 - t0})
        except Exception as e:
            runs.append({"error": str(e)[:200]})
    ok = [r for r in runs if "error" not in r]
    med = lambda k: round(sorted(r[k] for r in ok)[len(ok) // 2], 4) if ok else None
    return {"runs": [{k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()} for r in runs],
            "median": {k: med(k) for k in ("dns", "connect", "tls", "wait", "total")},
            "first_run_total": round(ok[0]["total"], 4) if ok else None,
            "note": "median over successful runs; the first run separately (cold DNS/cache)"}

def parse_head(html):
    meta = {}
    for m in re.finditer(r"<meta\s+([^>]+)>", html, re.I):
        a = dict((k.lower(), v) for k, _, v in re.findall(r'([\w:-]+)\s*=\s*(["\'])(.*?)\2', m.group(1)))
        key = a.get("property") or a.get("name")
        if key: meta[key.lower()] = a.get("content")
    links = {}
    for m in re.finditer(r"<link\s+([^>]+)>", html, re.I):
        a = dict((k.lower(), v) for k, _, v in re.findall(r'([\w:-]+)\s*=\s*(["\'])(.*?)\2', m.group(1)))
        if a.get("rel"): links.setdefault(a["rel"].lower(), []).append(a.get("href"))
    title = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    srcs = re.findall(r'(?:src|href)=["\']([^"\']+\.(?:css|js|jpg|jpeg|png|webp|svg|woff2|mp4)(?:\?[^"\']*)?)["\']', html, re.I)
    return {"meta": meta, "links": links, "title": title.group(1).strip() if title else None, "assets": srcs}

def image_size(b):
    try:
        from PIL import Image; import io
        im = Image.open(io.BytesIO(b)); return list(im.size), im.format
    except Exception as e: return None, f"not read: {e}"[:80]

def dns_info(host):
    out = {}
    try:
        import dns.resolver
        for t in ("A", "AAAA", "MX", "TXT", "CAA"):
            try: out[t] = [r.to_text() for r in dns.resolver.resolve(host, t, lifetime=8)]
            except Exception as e: out[t] = []
        try: out["_dmarc"] = [r.to_text() for r in dns.resolver.resolve("_dmarc." + host, "TXT", lifetime=8)]
        except Exception: out["_dmarc"] = []
        out["spf"] = [t for t in out.get("TXT", []) if "v=spf1" in t]
    except ImportError:
        out["error"] = "dnspython is not installed — not measured"
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site"); ap.add_argument("out")
    ap.add_argument("--pages", default="/"); ap.add_argument("--delay", type=float, default=1.1)
    ap.add_argument("--no-crtsh", action="store_true"); ap.add_argument("--extra-probes", default="",
        help="comma-separated extra paths, e.g. /proto.html,/v2.html (drafts found in the project)")
    ap.add_argument("--api-paths", default="",
        help="comma-separated backend paths the page calls (fetch/XHR in its JS), e.g. /api/can,/api/build. "
             "Checked with one GET each: 404 = not deployed, 405/400/401/422 = endpoint exists")
    a = ap.parse_args()
    # Git Bash rewrites "/v3.html" into "C:/Program Files/Git/v3.html"; undo that and accept "v3.html" too
    def norm(p):
        p = re.sub(r"^[A-Za-z]:/(?:Program Files/Git|msys64)?/?", "/", p.replace("\\", "/"))
        return p if p.startswith("/") else "/" + p
    a.pages = ",".join(norm(p) for p in a.pages.split(",") if p)
    a.extra_probes = ",".join(norm(p) for p in a.extra_probes.split(",") if p)
    a.api_paths = ",".join(norm(p) for p in a.api_paths.split(",") if p)
    site = a.site.rstrip("/"); u = urllib.parse.urlsplit(site); host = u.hostname
    C = Client(a.delay); R = {"site": site, "started": datetime.now().isoformat(timespec="seconds"), "log": []}
    log = lambda m: (R["log"].append(m), print(m, file=sys.stderr))

    log("TLS"); R["tls"] = tls_info(host)
    log("DNS"); R["dns"] = dns_info(host)

    log("home page")
    home = C.req(site + "/")
    html = decode_body(home) or ""
    R["home"] = strip(home); R["home"]["head"] = parse_head(html)
    R["home"]["html_text_len"] = len(re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)).split())
    R["home"]["secrets_in_html"] = {k: sev for k, (p, sev) in SECRET_PATTERNS.items() if re.search(p, html)}
    R["home"]["yandex"] = {"verification": "yandex-verification" in html, "metrika": bool(re.search(r"mc\.yandex\.ru|ym\(\s*\d+", html)),
                           "webvisor": bool(re.search(r"webvisor\s*:\s*true", html))}
    R["home"]["third_party_scripts"] = sorted(set(m for m in re.findall(r'<script[^>]+src=["\'](https?://[^"\']+)', html, re.I)
                                                  if urllib.parse.urlsplit(m).hostname != host))
    R["home"]["sri_missing"] = [m for m in R["home"]["third_party_scripts"] if not re.search(re.escape(m) + r'[^>]*integrity=', html)]
    R["home"]["compromised_cdn"] = [m for m in R["home"]["third_party_scripts"] if re.search(r"polyfill\.io|bootcss|staticfile\.org|polyfill\.com", m)]

    log("headers: redirect, 404, static")
    R["http_redirect"] = strip(C.req(f"http://{host}/", keep_body=False))
    fp_path = f"/__no-such-page-{rnd()}"
    nf = C.req(site + fp_path); R["not_found"] = strip(nf); R["not_found"]["path"] = fp_path
    R["not_found"]["body_preview_debug"] = bool(re.search(rb"(?i)traceback|whoops|stack trace|debug", nf.get("_body") or b""))
    fingerprint = (nf.get("status"), nf.get("bytes"), nf.get("sha256"))
    statics = []
    for s in R["home"]["head"]["assets"]:
        full = urllib.parse.urljoin(site + "/", s)
        if urllib.parse.urlsplit(full).hostname == host and full not in statics: statics.append(full)
    R["static"] = {}
    by_type = {}
    for s in statics:
        ext = s.split("?")[0].rsplit(".", 1)[-1].lower(); by_type.setdefault(ext, s)
    for ext, s in list(by_type.items())[:6]:
        r = C.req(s, rng="bytes=0-1023" if ext == "mp4" else None, keep_body=False)
        R["static"][s] = strip(r)
    def sec(hd): return {h: hd.get(h) for h in SEC_HEADERS}
    R["security_headers"] = {name: sec(r.get("headers") or {}) for name, r in
        [("html", home), ("redirect", R["http_redirect"]), ("404", nf)] + [(k, v) for k, v in R["static"].items()]}

    log("duplicate URLs")
    dup = {}
    for v in ["/index.html", "/?utm_source=audit", "/?yclid=1"]:
        r = C.req(site + v, keep_body=False); dup[v] = {"status": r.get("status"), "location": (r.get("headers") or {}).get("location")}
    r = C.req(f"https://www.{host}/", keep_body=False); dup["www"] = {"status": r.get("status"), "error": r.get("error"),
                                                                    "location": (r.get("headers") or {}).get("location")}
    for p in [p for p in a.pages.split(",") if p not in ("", "/")][:3]:
        alt = p.rstrip("/") if p.endswith("/") else p + "/"
        r = C.req(site + alt, keep_body=False); dup[alt] = {"status": r.get("status"), "location": (r.get("headers") or {}).get("location")}
    R["duplicates"] = dup

    log("robots.txt, sitemap.xml")
    rb_ = C.req(site + "/robots.txt"); rtxt = decode_body(rb_) or ""
    is_real_robots = rb_.get("status") == 200 and (rb_.get("headers") or {}).get("content-type", "").startswith("text/plain")
    R["robots"] = {"status": rb_.get("status"), "ctype": (rb_.get("headers") or {}).get("content-type"), "real": is_real_robots}
    if is_real_robots:
        groups, cur, last_ua = {}, [], False
        for line in rtxt.splitlines():
            line = line.split("#")[0].strip()
            if not line or ":" not in line: continue
            k, v = [x.strip() for x in line.split(":", 1)]
            if k.lower() == "user-agent":
                if not last_ua: cur = []
                cur.append(v); groups.setdefault(v, []); last_ua = True
            else:
                last_ua = False
                for c in cur: groups[c].append((k.lower(), v))
        R["robots"].update(text_lines=len(rtxt.splitlines()), sitemaps=re.findall(r"(?im)^sitemap:\s*(\S+)", rtxt),
            clean_param=re.findall(r"(?im)^clean-param:\s*(.+)$", rtxt), host_directive=bool(re.search(r"(?im)^host:", rtxt)),
            disallow_all={ua: ("disallow", "/") in rules for ua, rules in groups.items()},
            blocks_assets=[v for rules in groups.values() for k, v in rules if k == "disallow" and re.search(r"\.(css|js)|/static|/assets", v)],
            ai_bots={b: ("disallow", "/") in groups.get(b, []) for b in AI_BOTS})
    sm_url = (R["robots"].get("sitemaps") or [site + "/sitemap.xml"])[0]
    sm = C.req(sm_url); stxt = decode_body(sm) or ""
    R["sitemap"] = {"url": sm_url, "status": sm.get("status"), "urls": re.findall(r"<loc>\s*([^<]+?)\s*</loc>", stxt)[:500]}
    R["sitemap"]["count"] = len(R["sitemap"]["urls"])
    R["sitemap"]["sample_status"] = {}
    for loc in R["sitemap"]["urls"][:10]:
        r = C.req(loc.strip(), method="HEAD"); R["sitemap"]["sample_status"][loc] = r.get("status")

    log("service files (bodies are not stored)")
    # extra probes (drafts from the project) go first: they are the most likely leak
    probes = {p: rb"(?i)<html|<!doctype" for p in a.extra_probes.split(",") if p}
    for k, v in PROBES.items(): probes.setdefault(k, v)
    LIMIT = 30
    R["probes"] = {"fingerprint_random_path": {"status": fingerprint[0], "bytes": fingerprint[1]}, "results": {},
                   "limit": LIMIT, "skipped_over_limit": list(probes)[LIMIT:]}
    if R["probes"]["skipped_over_limit"]: log(f"service paths over the limit of {LIMIT} not checked: {R['probes']['skipped_over_limit']}")
    for path, sig in list(probes.items())[:LIMIT]:
        r = C.req(site + path, rng="bytes=0-255")
        body = r.get("_body") or b""
        same_as_404 = (r.get("status"), r.get("bytes"), r.get("sha256")) == fingerprint
        hit = r.get("status") in (200, 206) and not same_as_404 and (sig is None or bool(re.search(sig, body[:256])))
        R["probes"]["results"][path] = {"status": r.get("status"), "ctype": (r.get("headers") or {}).get("content-type"),
                                        "same_as_404_fingerprint": same_as_404, "exposed": hit, "error": r.get("error")}
        del body

    if a.api_paths:
        log("backend paths the page calls")
        R["api"] = {}
        for p in a.api_paths.split(","):
            r = C.req(site + p, keep_body=False)
            st = r.get("status")
            R["api"][p] = {"status": st, "ctype": (r.get("headers") or {}).get("content-type"), "error": r.get("error"),
                           "deployed": None if st is None else (st not in (404, 502, 503, 504) and
                                       (r.get("status"), r.get("bytes"), r.get("sha256")) != fingerprint)}

    log("messenger previews")
    og = R["home"]["head"]["meta"]
    R["previews"] = {"og": {k: v for k, v in og.items() if k.startswith(("og:", "twitter:"))}, "bots": {}}
    for name, bua in BOT_UAS.items():
        r = C.req(site + "/", ua=bua); h2 = decode_body(r) or ""
        R["previews"]["bots"][name] = {"status": r.get("status"), "bytes": r.get("bytes"), "has_og_image": "og:image" in h2,
                                       "location": (r.get("headers") or {}).get("location"), "error": r.get("error")}
    img = og.get("og:image")
    if img:
        full = urllib.parse.urljoin(site + "/", img)
        r = C.req(full, ua=BOT_UAS["telegram"])
        size, fmt = image_size(r.get("_body") or b"")
        R["previews"]["og_image"] = {"url": full, "absolute_https": img.startswith("https://"), "status": r.get("status"),
            "ctype": (r.get("headers") or {}).get("content-type"), "bytes": r.get("bytes"), "size": size, "format": fmt,
            "redirect": (r.get("headers") or {}).get("location")}

    log("server response time (5 runs)")
    R["ttfb"] = ttfb_breakdown(site + "/", 5, a.delay)

    log("bare IP")
    ips = R["dns"].get("A") or []
    if not ips:
        try: ips = [socket.gethostbyname(host)]
        except Exception: ips = []
    R["bare_ip"] = {}
    for ip in ips[:1]:
        for sch in ("http", "https"):
            r = C.req(f"{sch}://{ip}/", verify=False); t = re.search(rb"(?is)<title[^>]*>(.*?)</title>", r.get("_body") or b"")
            R["bare_ip"][f"{sch}://{ip}/"] = {"status": r.get("status"), "server": (r.get("headers") or {}).get("server"),
                "title": t.group(1)[:120].decode("utf-8", "replace").strip() if t else None,
                "same_as_site": r.get("sha256") == home.get("sha256"), "error": r.get("error")}

    if a.no_crtsh:
        R["crtsh"] = {"skipped": "disabled with --no-crtsh"}
    elif host.endswith(("nip.io", "sslip.io")):
        R["crtsh"] = {"skipped": "temporary nip.io/sslip.io domain: the log is shared by thousands of other names, pointless"}
    else:
        log("certificate log crt.sh")
        r = C.req(f"https://crt.sh/?q=%25.{host}&output=json")
        try:
            names = sorted({n for e in json.loads(decode_body(r) or "[]") for n in e.get("name_value", "").split("\n")})
            R["crtsh"] = {"names": names[:100], "count": len(names)}
        except Exception as e:
            R["crtsh"] = {"error": f"not measured: {e}"[:200]}
    R["requests_made"] = C.count; R["stopped_by_protection"] = C.stop
    json.dump(R, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print(f"ok: {C.count} requests, protection: {C.stop or 'not triggered'}")

if __name__ == "__main__":
    main()
