"""Mode A: raw-HTML analysis of pages and every resource they reference. GET only.

Usage:
  python static_audit.py BASE_URL PAGES OUT.json [DELAY]
  PAGES is comma-separated relative paths, e.g. "v3.html,p.html,policy.html" ("" = the base itself).
  DELAY: 1.1 for a live site (default), 0.1 is fine for localhost.
Per page: inline share, title/description/h1, OG, canonical, images, links, forms, legal markers
(policy/offer links, INN/OGRNIP, refund phrases, erid, foreign form services), secret patterns.
Per resource: bytes, type, headers, hash, minification hints.
"""
import json, re, sys, time, hashlib, urllib.request, urllib.parse
from html.parser import HTMLParser
from collections import Counter

# browser-like UA with an honest tail: Google Fonts and others serve real CSS only to browsers
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36 SiteAudit-Bot (read-only audit)"
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8792/"
PAGES = sys.argv[2].split(",") if len(sys.argv) > 2 else ["v3.html"]
OUT = sys.argv[3]
DELAY = float(sys.argv[4]) if len(sys.argv) > 4 else 1.1
PAGES = [re.sub(r"^[A-Za-z]:/(?:Program Files/Git|msys64)?/?", "", p.replace("\\", "/")).lstrip("/") for p in PAGES]  # undo Git Bash path rewriting
SECRETS = {"telegram_bot_token": (r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b", "Blocker"), "telegram_api_url": (r"api\.telegram\.org/bot", "Blocker"),
           "anthropic_key": (r"sk-ant-[A-Za-z0-9_-]{20,}", "Blocker"), "openrouter_key": (r"sk-or-[A-Za-z0-9_-]{20,}", "Blocker"),
           "openai_like_key": (r"\bsk-[A-Za-z0-9]{32,}", "Blocker"), "supabase_service_role": (r"service_role", "Blocker"),
           "supabase_anon_or_firebase": (r"AIza[0-9A-Za-z_-]{35}|eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "Info")}

def legal_markers(html, links):
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html); text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    def lk(rx): return [(h, t) for h, t in links if re.search(rx, (t or "") + " " + (h or ""), re.I)][:5]
    return {
        "policy_links": lk(r"политик|конфиденц|персональн|privacy|data protection"),
        "offer_links": lk(r"оферт|договор|terms|услови|conditions"),
        "consent_links": lk(r"согласи|consent"),
        "inn": re.findall(r"ИНН[\s:]*(\d{10,12})", text), "ogrnip": re.findall(r"ОГРН(?:ИП)?[\s:]*(\d{13,15})", text),
        "refund_phrases": [m.group(0)[:120] for m in re.finditer(r"[^.]{0,60}(не\s+возвращ|возврат[а-я]*\s+не\s|не\s+подлежит\s+возврат|no\s+refunds?|non-refundable)[^.]{0,60}", text, re.I)][:5],
        "result_promises": [m.group(0)[:120] for m in re.finditer(r"[^.]{0,40}(гарантир[а-я]+|100\s?%\s*трудоустр|guarantee[ds]?\s+(income|results?|job))[^.]{0,60}", text, re.I)][:5],
        "erid": len(re.findall(r"erid", html, re.I)),
        "foreign_form_services": sorted(set(re.findall(r"(docs\.google\.com/forms|typeform\.com|calendly\.com|hubspot|tally\.so|jotform)", html, re.I))),
        "foreign_trackers": sorted(set(re.findall(r"(googletagmanager|google-analytics|connect\.facebook\.net|fbq\(|recaptcha|youtube\.com/embed|player\.vimeo)", html, re.I))),
        "metrika": bool(re.search(r"mc\.yandex\.ru|ym\(\s*\d+", html)), "webvisor": bool(re.search(r"webvisor\s*:\s*true", html)),
        "foreign_login": sorted(set(re.findall(r"(accounts\.google\.com|appleid\.apple\.com|telegram-widget|oauth\.telegram)", html, re.I))),
    }

def get(url, method="GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA, "Accept-Encoding": "gzip, br"})
    t = time.time()
    try:
        r = urllib.request.urlopen(req, timeout=20)
        body = r.read() if method == "GET" else b""
        return r.status, dict(r.headers), body, time.time() - t, r.version
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read() if method == "GET" else b"", time.time() - t, None
    except Exception as e:
        return None, {}, b"", time.time() - t, str(e)

class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True)
        s.tags = []; s.stack = []; s.styles = []; s.scripts = []; s.style_attrs = []; s.res = []
        s.ids = Counter(); s.headings = []; s.cur_h = None; s.imgs = []; s.links = []; s.metas = []
        s.title = ""; s.in_title = False; s.in_style = False; s.in_script = False; s.cur = ""
        s.inputs = []; s.forms = []; s.labels = []; s.handlers = 0; s.classes = Counter(); s.comments = []
        s.landmarks = Counter(); s.iframes = []; s.videos = []; s.head_blocking = []; s.in_head = False
        s.html_lang = None; s.counts = Counter(); s.canonical = None
    def handle_starttag(s, tag, a):
        a = dict(a); s.counts[tag] += 1
        if tag == "html": s.html_lang = a.get("lang")
        if tag == "head": s.in_head = True
        if tag == "body": s.in_head = False
        if "id" in a: s.ids[a["id"]] += 1
        if "style" in a: s.style_attrs.append(a["style"] or "")
        for k in a:
            if k.startswith("on"): s.handlers += 1
        for c in (a.get("class") or "").split(): s.classes[c] += 1
        if tag in ("header", "nav", "main", "footer", "aside") or a.get("role") in ("navigation", "main", "banner", "contentinfo"):
            s.landmarks[tag if tag in ("header","nav","main","footer","aside") else a.get("role")] += 1
        if tag == "title": s.in_title = True
        if tag == "style": s.in_style = True; s.cur = ""
        if tag == "script":
            if a.get("src"):
                s.res.append(("script", a["src"], a))
                if s.in_head and "async" not in a and "defer" not in a and a.get("type") != "module": s.head_blocking.append(a["src"])
            else: s.in_script = True; s.cur = ""
        if tag == "link":
            if (a.get("rel") or "") not in ("preconnect", "dns-prefetch", "canonical", "alternate"):  # hints and meta links are not resources
                s.res.append(("link:" + (a.get("rel") or ""), a.get("href"), a))
            elif a.get("rel") == "canonical": s.canonical = a.get("href")
            if s.in_head and (a.get("rel") or "") == "stylesheet": s.head_blocking.append(a.get("href"))
        if tag == "img": s.imgs.append(a); s.res.append(("img", a.get("src"), a))
        if tag == "source": s.res.append(("source", a.get("src") or a.get("srcset"), a))
        if tag == "video": s.videos.append(a); s.res.append(("video", a.get("src") or a.get("data-src"), a))
        if tag == "iframe": s.iframes.append(a)
        if tag == "a": s.links.append(a)
        if tag == "meta": s.metas.append(a)
        if tag in ("input", "textarea", "select"): s.inputs.append(a)
        if tag == "form": s.forms.append(a)
        if tag == "label": s.labels.append(a)
        if re.fullmatch(r"h[1-6]", tag): s.cur_h = [tag, ""]; s.headings.append(s.cur_h)
    def handle_endtag(s, tag):
        if tag == "title": s.in_title = False
        if tag == "style": s.in_style = False; s.styles.append(s.cur)
        if tag == "script" and s.in_script: s.in_script = False; s.scripts.append(s.cur)
        if re.fullmatch(r"h[1-6]", tag): s.cur_h = None
        if tag == "head": s.in_head = False
    def handle_data(s, d):
        if s.in_title: s.title += d
        if s.in_style or s.in_script: s.cur += d
        if s.cur_h is not None: s.cur_h[1] += d
    def handle_comment(s, d): s.comments.append(d)

result = {"base": BASE, "pages": {}, "resources": {}}
for page in PAGES:
    url = urllib.parse.urljoin(BASE, page)
    st, hd, body, dt, ver = get(url); time.sleep(DELAY)
    html = body.decode("utf-8", "replace")
    p = P(); p.feed(html)
    b = lambda x: len(x.encode("utf-8"))
    S_html = len(body)
    s_style = sum(b(x) for x in p.styles); s_script = sum(b(x) for x in p.scripts)
    s_attr = sum(b(x) for x in p.style_attrs)
    datauris = re.findall(r"data:[a-z]+/[a-z0-9+.-]+[;,][^\"')\s]+", html)
    s_data = sum(b(x) for x in datauris)
    S_inline = s_style + s_script + s_attr + s_data
    metas = {(m.get("name") or m.get("property") or m.get("http-equiv") or m.get("charset") and "charset"): m.get("content", m.get("charset")) for m in p.metas}
    desc = metas.get("description") or ""
    rec = {
        "url": url, "status": st, "headers": hd, "ttfb_total_s": round(dt, 4), "S_html": S_html,
        "sha256": hashlib.sha256(body).hexdigest(),
        "inline": {"style_tags": s_style, "inline_scripts": s_script, "style_attrs": s_attr, "data_uris": s_data,
                    "count_style_tags": len(p.styles), "count_inline_scripts": len(p.scripts), "count_style_attrs": len(p.style_attrs),
                    "count_data_uris": len(datauris), "S_inline": S_inline, "P_pct": round(S_inline / S_html * 100, 2) if S_html else None},
        "title": p.title.strip(), "title_len": len(p.title.strip()), "description": desc, "description_len": len(desc),
        "metas": metas, "html_lang": p.html_lang,
        "h1": [h[1].strip() for h in p.headings if h[0] == "h1"],
        "headings": [[h[0], re.sub(r"\s+", " ", h[1]).strip()[:80]] for h in p.headings],
        "dup_ids": {k: v for k, v in p.ids.items() if v > 1},
        "imgs_total": len(p.imgs), "imgs_no_alt": [i.get("src") for i in p.imgs if "alt" not in i],
        "imgs_empty_alt": [i.get("src") for i in p.imgs if i.get("alt") == ""],
        "imgs_no_wh": [i.get("src") for i in p.imgs if not ("width" in i and "height" in i)],
        "imgs_lazy": [i.get("src") for i in p.imgs if i.get("loading") == "lazy"],
        "imgs_srcset": sum(1 for i in p.imgs if "srcset" in i),
        "videos": p.videos, "iframes": p.iframes, "forms": p.forms, "inputs": p.inputs, "labels": len(p.labels),
        "links": [(l.get("href"), l.get("target"), l.get("rel")) for l in p.links],
        "handlers_inline": p.handlers, "landmarks": dict(p.landmarks), "head_blocking": p.head_blocking,
        "comments": [c.strip()[:160] for c in p.comments], "resources": [(t, u) for t, u, _ in p.res],
        "link_tags": [(t, u, a) for t, u, a in p.res if t.startswith("link")],
        "tag_counts": dict(p.counts), "class_count_unique": len(p.classes),
        "canonical": p.canonical,
        "og": {k: v for k, v in metas.items() if k and (k.startswith("og:") or k.startswith("twitter:"))},
        "jsonld": len(re.findall(r'application/ld\+json', html)),
        "mixed_http": re.findall(r'(?:src|href)="(http://[^"]+)"', html),
        "todo_fixme": re.findall(r"(?i)\b(TODO|FIXME|XXX|HACK)\b", html),
        "localhost_refs": re.findall(r"(?i)(?:localhost|127\.0\.0\.1|192\.168\.\d+\.\d+|staging)[^\"'\s<]*", html),
        "emails": [re.sub(r"(?<=.).(?=[^@]*@)", "*", e) for e in set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", html))],
        "href_hash_only": sum(1 for l in p.links if l.get("href") == "#"),
        "secrets": {k: sev for k, (rx, sev) in SECRETS.items() if re.search(rx, html)},
        "legal": legal_markers(html, [(h, re.sub(r"<[^>]+>", "", t)) for h, t in re.findall(r'<a\s[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', html, re.I | re.S)]),
        "placeholders": re.findall(r"(?i)lorem ipsum|class=\"todo\"|текст о компании|your text here|\{\{[^}]+\}\}", html)[:10],
        "links_no_href": sum(1 for l in p.links if "href" not in l),
    }
    result["pages"][page or "/"] = rec
    for t, u, a in p.res:
        if not u or u.startswith("data:"): continue
        full = urllib.parse.urljoin(url, u.split(" ")[0])
        if full in result["resources"]:
            result["resources"][full]["used_by"].append(page or "/"); continue
        rs, rh, rb, rdt, _ = get(full); time.sleep(DELAY)
        result["resources"][full] = {"type": t, "status": rs, "bytes": len(rb), "ctype": rh.get("Content-Type") or rh.get("Content-type"),
            "headers": rh, "sha256": hashlib.sha256(rb).hexdigest(), "used_by": [page or "/"], "lazy_attr": a.get("loading"), "preload": a.get("preload"),
            "third_party": urllib.parse.urlparse(full).netloc != urllib.parse.urlparse(BASE).netloc}
        if t == "link:stylesheet" or (rh.get("Content-Type") or rh.get("Content-type") or "").startswith(("text/css", "text/javascript", "application/javascript")):
            txt = rb.decode("utf-8", "replace")
            result["resources"][full]["text_stats"] = {"lines": txt.count("\n"), "comments": len(re.findall(r"/\*", txt)),
                "avg_line": round(len(txt) / max(1, txt.count("\n")), 1), "console_log": len(re.findall(r"console\.(log|debug)", txt)),
                "debugger": len(re.findall(r"\bdebugger\b", txt)), "important": txt.count("!important"),
                "sourceMappingURL": "sourceMappingURL" in txt,
                "secrets": {k: sev for k, (rx, sev) in SECRETS.items() if re.search(rx, txt)},
                # backend addresses the page calls -> pass to server_audit.py --api-paths
                "api_calls": sorted(set(re.findall(r"""(?:fetch|axios\.\w+|\.open)\(\s*(?:['"]\w+['"]\s*,\s*)?[`'"]([^`'"\s]+)""", txt)))[:20]}
json.dump(result, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("ok", len(result["resources"]), "resources")
