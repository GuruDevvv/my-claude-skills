---
name: site-audit
description: >
  Read-only outside audit of a website the user owns, the way any visitor sees it: speed and weight,
  server security headers and exposed files, indexing for Google and Yandex, link previews in
  Telegram/WhatsApp/VK, accessibility, code quality, Russian legal basics (152-FZ, offer, refunds).
  Works on a live domain and before deploy (local page + the domain it will go to). Every number comes
  from bundled scripts; the result opens as an interactive one-file dashboard plus a written report.
  Use when the user asks to audit, check or review a site or landing page: "audit my site",
  "check this landing before launch", "why is my site slow", "is my site secure", "website health check",
  «проверь сайт», «аудит сайта», «проверь лендинг», «проверь перед выкладкой».
  Do NOT use for: reviewing the site's source code (code-review), penetration testing or any active
  attack, sites the user does not own or have permission to check, design critique, keyword research.
---

# Site audit from the outside

A black-box check: only what the server hands to an ordinary visitor. Bundled scripts measure,
the model reads the numbers, compares them with thresholds and writes the report and the dashboard.
The model never invents a measurement or "estimates by eye".

Origin: a black-box audit prompt shared in a Telegram chat (October 2026), rebuilt after a first real
run and a review by five specialist agents (security, search, performance, accessibility, Russian law).

## Safety rules — not negotiable

Read only. Never break anything.

- **Whose site.** Before starting, make sure the site belongs to the user or they may audit it.
  Do not audit someone else's site without permission: probing service paths there is a grey zone.
- GET and HEAD only. No POST/PUT/DELETE. The browser scripts abort every non-GET request themselves.
- No forms, typing, sign-ups, carts, logins, password guessing, payloads (`' OR 1=1`, `<script>`, `../`),
  scanners, path brute-forcing or load testing.
- Service paths: only the list in `server_audit.py` (up to 30). Response bodies are never stored or
  printed: the script reads the first 256 bytes, matches a signature and returns exposed / not exposed.
  **Never test a found key or token against its service** — that is using someone else's credentials.
- Pace on a live site: at most 1 request per second for server checks. Browser runs (3 page loads per
  profile) are fine: that is what an ordinary visitor does.
- Stop on signs of protection: a captcha page, Cloudflare / DDoS-Guard challenge, HTTP 429. Stop that
  type of check and record the fact in the report. **403 on `/.git/HEAD` is a normal answer, not a WAF.**
- Do not follow `/logout`, `?action=`, `?delete=` and the like. Do not bypass robots.txt.
- Never click links or submit buttons. `render_audit.py --interact` presses only toggles outside forms
  (tabs, accordions, menus).

## Step 1. Inputs and mode

Take from the request or the project; ask only what cannot be found:

| What | Where from |
|---|---|
| Page or site address | the request |
| Mode | **live** — the site is on its domain; **pre-deploy** — the page is local (`127.0.0.1`, `localhost`) + the domain it will move to; **local only** — no domain yet |
| Project folder | if the site was built in this session or lives in the working directory — to know the drafts |
| Site type | one-pager (one landing page) or multi-page (4+ different pages) |
| Report language | the language the user writes in (`en` or `ru` for the dashboard) |

Pages: home, 404 (`/__no-such-page-<random>`), privacy policy and offer if they exist.
For a multi-page site, one page of each type: section, item, form, search. Types matter more than count.

In **pre-deploy** mode: measure the page locally and the server (headers, certificate, robots, service
files, previews for bots) on the live domain. Tag each finding `[page]` or `[server]`. Headers of the
local dev server (HTTP/1.0, no compression) are **not production problems** — mention them once as context.

## Step 2. Run the scripts

Results folder: `<project>/docs/audit-YYYY-MM-DD/`, or the session scratch folder without a project.
Run the scripts by full path. Pass page paths without a leading `/` (Git Bash on Windows rewrites
`/v3.html` into a Windows path; the scripts undo that, but better not to provoke it).

```bash
S=~/.claude/skills/site-audit/scripts; O=<results folder>
# 1. HTML and every referenced file (live: delay 1.1, local: 0.1)
python $S/static_audit.py <base> "<page1>,<page2>,policy.html" $O/static.json 1.1
# 2. Browser: 3 cold runs per profile + a warm one, weight, video, code coverage
python $S/render_audit.py <main page URL> $O/render.json --profiles mobile,mobile_slow,desktop --runs 3 --interact --shots $O/shot
# 3. Accessibility: axe, keyboard, 200 % text, 320 px, reduced motion, no JS
python $S/a11y_audit.py <page URL> $O/a11y.json --shots $O/shot
# 4. Server — live domain only
python $S/server_audit.py https://<domain> $O/server.json --pages "<page1>,<page2>" --api-paths "<from api_calls>" --extra-probes "<drafts from the site folder>"
```

- `--pages`: pages that **already exist** on the live domain (to test slash / no-slash duplicates).
  In pre-deploy mode pass only `/` — the new page is not on production yet.
- `--api-paths`: backend addresses the page calls. Take them from `static.json` →
  `resources.*.text_stats.api_calls` (fetch, XHR). One GET each: 404 = backend not deployed,
  405/400/401 = endpoint exists. **In pre-deploy mode this is the main risk**: the page is published
  while the thing its form relies on is not.
- `--extra-probes`: HTML files from the site folder that must not be on production (`proto.html`,
  `v2.html`, `_check*.html`). The most common leak in AI-built sites. They are probed first; the total
  limit is 30 paths, anything beyond it is listed in `probes.skipped_over_limit`.
- Video: for each clip in `render.json` (up to 5) run `ffprobe -v error -show_entries
  stream=codec_name,width,height,bit_rate -of json <url>` and compare with the displayed size.
- Field data (optional): PageSpeed Insights API, `loadingExperience` (CrUX, p75 over 28 days). Small
  sites usually have none — say so. Do not mix PSI lab numbers (measured from Google servers) with yours.
- Record where the measurement ran from: country of the IP and whether a VPN is on
  (`curl -s ipinfo.io/country`). Through a VPN foreign hosts (Google Fonts, YouTube) look faster than
  they are for visitors from Russia.
- Extra browser measurements of your own: Playwright with `channel="chrome"` (the bundled Chromium may
  not be installed).

A script fails — read the error, fix the call, retry. Still failing — "not measured: <reason>" in the
report; never invent numbers.

## Step 3. Analysis

Read the JSON files and go through the blocks in `references/checks.md`, comparing with
`references/thresholds.md`. Legal signals: `references/law-ru.md` (Russia; EU only if the site
clearly targets the EU).

Core rules:
- Every claim comes with a measurement or a quote of the response. Keep facts ("no CSP header")
  apart from guesses ("probably WordPress 5.8").
- Severity follows real harm for this site, not a checklist. Missing security headers on a static
  landing without logins are Minor; an exposed `.env` is a Blocker.
- Do not recommend what will not help in this setup: bundling files on HTTP/2, minification as the
  headline when gzip is on, lazy-loading the LCP image.
- The "page consistency" block runs only for 4+ different pages. For a one-pager, skip it and say why.
- Accessibility: a clean axe run does not mean accessible. Verdict: "no automated violations found",
  never "WCAG compliant". Everything a machine cannot judge goes to "Needs a human check".
- Law: only "signal or risk with a reference to the norm". A lawyer gives the verdict.
- If the project already has a previous `report.md` or notes with findings, mark each finding
  "already known" or "new".

## Step 4. Report and dashboard

1. Write `report.md` in the results folder — format in `references/report.md`.
   A subagent cannot create `.md` report files: if it did the analysis, it returns the text and the
   main agent writes the file.
2. Write `audit.json` — the dashboard data, schema in `references/report.md` ("Dashboard data").
   Plain language in every `name`, `summary`, `text` and `fix`: the dashboard is for the site owner,
   not for a developer. Each `fix` must read on its own, without the line above it.
3. Build and open the dashboard:
   ```bash
   python $S/build_dashboard.py $O/audit.json $O/dashboard.html
   ```
   It validates the data (scores 1–10, known levels, a fix for every broken/important item), embeds
   the screenshot and opens the page in the default browser. Validation fails — fix `audit.json`, rebuild.

To the user in chat — only the gist: the first two lines are the overall state and the most important
thing, then 2–4 points they did not expect, then the paths to `dashboard.html` and `report.md`.
Plain words, no header or metric names without explanation.

## Common mistakes

| Mistake | Instead |
|---|---|
| TTFB of a local page reported as server speed | Locally TTFB ≈ 0 and means nothing. Server time — only `server_audit.py` on the live domain |
| "Unused JS 54 %" as a problem | Code for states that never happened (the reply after a form submit) counts as unused. Judge in KB (threshold 50 KB) and explain why |
| One browser run → "LCP 2.1 s" | Median of three; spread over 20 % → mark "unstable" |
| 4.6 MB weight marked "Problem" without a split | Three numbers: first screen / everything except video / video. Judge video separately |
| 20 service paths returned 200 → "20 leaks" | The site answers 200 to everything (SPA, `try_files`). A finding only if the answer differs from the random-path fingerprint and the signature matches. The script does this: field `exposed` |
| nginx version → list of CVEs | Ubuntu/Debian patch packages without changing the number. Version leak is Minor, CVEs are "a guess" |
| Certificate has 25 days left — alarm | Let's Encrypt certificates live 90 days. Problem: under 14 days, or older than 65 days (renewal broken) |
| Headers taken from the home page only | nginx: `add_header` in a `location` drops server-level headers; without `always` they vanish on 404 and 301. Check all four responses in `security_headers` |
| Telegram preview "exists" because the tags are there | Check `og:image` (absolute https, 200, ≤300 KB, ~1200×630) and the answers to the Telegram / WhatsApp / VK bots. Remind about resetting the preview cache |
| Horizontal scroll at 320 px because `scrollWidth > width` | A finding only when `hscroll=true` (the script actually tries to scroll). `widthOverflow` alone means the extra is clipped by CSS |
| axe `video-caption` on a clip → "no captions" | `ffprobe` first: no audio stream — the rule does not apply; a decorative clip needs `aria-hidden="true"` |
| The whole report pasted into chat | Gist in chat, details in the files |

## Files

| Path | What it does |
|---|---|
| `scripts/static_audit.py` | HTML and resources: inline share, weight, meta, OG, forms, legal markers, secrets, backend calls |
| `scripts/render_audit.py` | Chrome: profiles, medians, cold/warm, weight in three numbers, video, coverage, lab INP via clicks |
| `scripts/a11y_audit.py` | axe-core (local copy in `vendor/`), keyboard, zoom, 320 px, text ×2, reduced motion, no JS |
| `scripts/server_audit.py` | Certificate, headers, compression, cache, robots, sitemap, duplicates, service files, backend paths, bot previews, TTFB, bare IP, DNS, crt.sh |
| `scripts/build_dashboard.py` | Validates `audit.json`, embeds the screenshot, builds `dashboard.html`, opens it |
| `assets/dashboard.html` | Dashboard template (English and Russian labels) |
| `assets/example-audit.json` | Sample data: a fictional pottery-studio landing |
| `references/checks.md` | What to check per block and which JSON fields hold it |
| `references/thresholds.md` | Thresholds (good / warning / problem) and the severity scale |
| `references/law-ru.md` | Legal signals for sites in Russia |
| `references/report.md` | Report template and the dashboard data schema |
