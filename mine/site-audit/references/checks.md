# Check blocks

For each block: what to look at and which JSON field holds it. `S` = static.json, `R` = render.json,
`A` = a11y.json, `V` = server.json. Thresholds are in `thresholds.md`.

## A. Page weight and inline code

- Inline share `S.pages.*.inline.P_pct` split into `<style>`, inline scripts, `style="…"`, data: URIs.
  Tell deliberate critical CSS (small, in `<head>`, the rest in files) from a dump.
- Weight as **three numbers**: first screen `R.profiles.*.weight_first_screen.bytes`, everything except
  video `weight_full.non_video_bytes`, video `weight_full.by_kind.video`. Window: until `load` + 10 s of
  network silence, then a scroll to the bottom. Split by type `by_kind`, third-party share `third_party_bytes`.
- Warm visit `R.profiles.*.warm`: how many bytes went again and how many responses came from cache.
  Warm ≈ cold → static files have no cache lifetime (see block B).

## B. Delivery

- Compression: `V.static.*.headers.content-encoding` and `V.home.headers` (HTML, CSS, JS, SVG). Judge the
  production response; the local dev server says nothing.
- Cache: `cache-control`, `etag`, `last-modified` on static files (`V.static`); a version in the file name
  or `?v=` on CSS/JS (`S.pages.*.resources`) — without it long caching is risky.
- Minification: `S.resources.*.text_stats` (lines, comments, average line length).
- Protocol: `V.tls.alpn` (h2 = HTTP/2), `R.profiles.*.cold[].proto`. On HTTP/2 do not suggest bundling or sprites.
- Render-blocking: `S.pages.*.head_blocking`. Duplicate libraries: identical `sha256` at different URLs,
  two versions of one library, jQuery next to a framework.
- Images `R.profiles.*.images`: natural size vs displayed × DPR, `srcset`, `loading`, `width/height` (`wh`),
  format. Never lazy-load the LCP image.
- Fonts: woff2, number of weights, `font-display`, external host (Google Fonts is also a legal risk in Russia).

## C. Video (a separate block when the page has clips)

`R.profiles.*.videos`: `poster`, `preload`, `muted` + `playsinline` (without them no autoplay on iOS),
`bytes_transferred` vs `file_bytes` (206 responses = range requests), `bytes_before_scroll`
(clips below the first screen should not download before scrolling; a few KB from `preload="metadata"`
are fine), file resolution vs `disp` × DPR. `ffprobe`: codec, bitrate. The LCP element can be a video or
its poster — see `lcp_elements`.

## D. Speed as the visitor sees it

`R.profiles.*.summary`: median / min / max of `ttfb`, `fcp`, `lcp`, `cls`, `tbt`; `unstable` when the spread
is over 20 %. CLS uses session windows (max 5 s window, 1 s gap); `cls_after_scroll` separately.
INP only as `inp_lab` with `--interact`, labelled "lab, over N clicks". Server time: `V.ttfb.median`
(DNS / connect / TLS / wait) and `first_run_total` separately. Caveats for the report: CDP throttling does
not reproduce TCP slow start and understates HTTP/2 gains; state the profiles (`settings`), where the
measurement ran from, and the VPN.

## E. Security from the outside (observation only)

- **The page's backend** `V.api`: every address from `S.resources.*.text_stats.api_calls` answers on the live
  domain (`deployed`). 404 — the form or the page's main feature will break in production. Submitting the
  form is not part of this check — put "submit once by hand after deploy" into "Needs a human check".
- HTTPS: `V.http_redirect` (one-step 301 to https), `V.tls` (version, expiry, age, chain
  `verified`/`chain_incomplete_suspected`, SAN). An incomplete chain breaks Telegram's in-app browser on
  some Android phones — it matters for funnels.
- Headers `V.security_headers` across **four** responses: HTML, redirect, 404, static. A difference between
  them means `add_header` inside a `location` or a missing `always`.
  - Recommend: HSTS (`max-age=31536000`, no `preload` / `includeSubDomains` by default),
    `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`,
    `X-Frame-Options: SAMEORIGIN` / `frame-ancestors` (DENY if the site never frames itself),
    `Permissions-Policy`. **Do not recommend X-XSS-Protection** (obsolete).
  - CSP with `unsafe-inline` ≈ no CSP — say so only for pages with forms or third-party scripts.
- Version leaks: `server`, `x-powered-by`, meta generator. Minor.
- Service files `V.probes.results.*.exposed` (already checked against the false-200 fingerprint and a
  signature). `exposed=true` on `.git`, `.env`, a backup, the project folder, agent notes
  (`CLAUDE.md` / `HANDOFF.md`) — Blocker. Drafts from `--extra-probes` — Minor/Major by content.
- Bare IP `V.bare_ip`: what the server returns without a domain (another project, 502, the site itself).
  Certificate log `V.crtsh`: `dev.`, `test.`, `staging.` and neighbouring projects.
- Secrets: `S.pages.*.secrets`, `S.resources.*.text_stats.secrets`, `V.home.secrets_in_html`. Mask values.
  Supabase anon key, Firebase apiKey, analytics counter id, public captcha key — Info.
- Third-party scripts `V.home.third_party_scripts`: SRI (`sri_missing`), compromised CDNs (`compromised_cdn`:
  polyfill.io and mirrors, bootcss, staticfile). A third-party script on a page with a form or payment is a finding.
- Do not flag: `autocomplete` on fields; `Access-Control-Allow-Origin: *` on public static files without
  credentials (Info); cookie flags on analytics cookies (`_ym_*`, `_ga`) — check only the site's own session
  cookies; missing `security.txt` (Info); no OCSP stapling (Let's Encrypt dropped OCSP in 2025).
- Admin paths (`/wp-admin`, `/bitrix/admin`) only once the stack is known. On plain nginx they are noise.
- Anything that cannot be confirmed without active testing: "confirmed only by a pentest", and stop there.

## F. Indexing (Google and Yandex)

- robots.txt `V.robots`: real or not (`real` — text/plain, not an HTML fallback), `disallow_all`, blocked
  CSS/JS (`blocks_assets`), `sitemaps`, `clean_param` (for `utm`, `yclid`, `fbclid` — Yandex needs it),
  `host_directive` (obsolete since 2018, remove), `ai_bots` (YandexBot, Googlebot, OAI-SearchBot,
  PerplexityBot, ClaudeBot not blocked by accident).
- **Draft leftovers** — the most common reason a site is not in search: `noindex`, `Disallow: /`,
  canonical pointing at a test address or a temporary domain (nip.io).
- sitemap `V.sitemap`: present, URL count, sampled statuses. For a one-pager a missing sitemap is Info.
- Duplicates `V.duplicates`: `/index.html`, `?utm_source`, `?yclid`, www, trailing slash. 200 instead of 301
  plus no canonical = finding.
- 404 `V.not_found`: real 404 or a "soft" 200; no debug output.
- Text in raw HTML (`V.home.html_text_len`): search and AI crawlers do not run JS. Empty HTML + content from JS = risk.
- Yandex: `V.home.yandex` (verification, Metrica), favicon for results (`/favicon.ico` or `rel=icon` SVG/PNG ≥120×120).
- llms.txt — one line, "does not affect search".
- Multi-page site in addition: unique title/description, broken internal links, hreflang, pagination,
  sitemap vs real links.

## G. SEO markup

- title, description, h1 (`S.pages.*`): length, exactly one h1, uniqueness across pages.
- Heading hierarchy without gaps; empty headings.
- JSON-LD: for a landing page Organization (or Person, LocalBusiness) + WebSite is enough. Product/Offer
  where there is a price, BreadcrumbList where there is nesting. **Do not recommend FAQ, HowTo or Yandex
  Turbo pages** (Google rarely shows FAQ, HowTo and Turbo are discontinued).
- alt, `lang`, charset, viewport. Manifest and apple-touch-icon on a landing page — Info.

## H. Link preview (Telegram, WhatsApp, VK)

For sites whose traffic comes from messengers this is the main "search" check.
- Tags `V.previews.og`: `og:title`, `og:description`, `og:image`, `og:url`, `og:site_name`,
  `twitter:card=summary_large_image`.
- Image `V.previews.og_image`: absolute https, 200, `image/*`, about 1200×630, up to 300 KB (WhatsApp often
  drops larger ones), no redirect.
- Bot answers `V.previews.bots`: status and size for TelegramBot, facebookexternalhit (WhatsApp) and vkShare
  must match the normal answer. Bot protection and captchas silently break previews.
- Add a note to the report: after fixing the tags, Telegram refreshes the preview through @WebpageBot, VK
  through its own cache-reset tool; otherwise the owner sees the old card and decides nothing works.
- Multi-page: each page has its own preview, not one copied from the home page.

## I. Layout and accessibility

In order of what really stops people:
- Zoom blocked `A.checks.viewport.zoomBlocked` — Critical (WCAG 1.4.4).
- Horizontal scroll at **320 px** `A.reflow_320` (WCAG 1.4.10, culprits in `culprits`) and with text ×2
  `A.text_200` (clipped text `clippedEx`). A finding only when `hscroll=true`: the script actually tries
  to scroll sideways. `widthOverflow=true` with `hscroll=false` means the extra is clipped by CSS
  (`overflow-x: clip`) and the visitor sees nothing — not a finding. At 360: `R.profiles.mobile.layout.hscroll`.
- Touch targets `A.checks.touch`: under 24×24 — Major (WCAG 2.5.8); 24–44 — Minor, a recommendation.
  Links inside running text are already excluded.
- Text `A.checks.text`: anything under 12 px — Major; paragraph text under 16 px — Minor. Captions and
  footnotes at 12–13 px are normal on a landing page.
- Contrast: `A.axe.violations` `color-contrast` (4.5:1; large text from 24 px or 18.66 px bold — 3:1).
  `incomplete` with `color-contrast` (text on a photo or gradient) goes to "Needs a human check" with a screenshot.
- Keyboard `A.keyboard`: focus without a visible change `noVisibleFocus`, under a sticky header `obscured`,
  off screen `offscreen`, trap `trap_suspected`.
- Forms `A.checks.fields`: no accessible name (`noName`) or placeholder only (`placeholderOnly`) — Major;
  wrong keyboard for phone or email (`keyboardMismatch`) — Major on a lead form, it costs leads; `autocomplete`.
- Nameless buttons and links `nameless`, div "buttons" `fakeButtons`, autoplay with sound `autoplaySound`,
  "read more" ×N `genericLinkTexts`, `lang`.
- Reduced motion `A.reduced_motion`: with `reduce`, animations and clips must stop.
- axe: carry over each rule with `impact`, element count and selectors, not just the number of rules.
- Landmarks (`header`, `nav`, `main`, `footer`) — Minor.
- "HTML validity" — only what breaks people: duplicate ids referenced by `for` / `aria-*`, interactive inside
  interactive, `aria-hidden` on a focusable element. Wrappers and obsolete tags go to block J or nowhere.
- No JS `A.no_js`: what is left of the page.

**"Needs a human check"** is mandatory. Each item: "the machine cannot judge this — what was seen — what to
check by hand, ~2 minutes". It holds: meaningful alt text, clear link text, reading order when CSS reorders
blocks, a screen-reader pass, text on photos.

## J. CSS and JS quality

- Coverage `R.profiles.*.coverage`: judge in **KB**, unused JS threshold 50 KB. 60 % of 20 KB is not a
  problem. Compare mobile and desktop profiles (media queries); code for states after a form submit will
  look "unused" — explain it, do not scold.
- `!important`, `@import`, dead vendor prefixes, `console.log`, `debugger`, sourceMappingURL in production.
- Spread of colours, font sizes, radii — no design system (Info).
- Repeated declaration blocks → one shared class + modifier, with the byte saving.

## K. Page consistency (only 4+ different pages)

Goal: is there a template behind the site, or was each page made separately (a common trace of
page-by-page AI generation).
- Reuse ratio = resources shared by all pages / union of resources (`S.pages.*.resources`); matching `sha256`
  of shared files.
- Header, menu, footer: markup skeleton, menu items and their order.
- Class naming, design tokens, `<head>` structure, library versions.
- A big own `<style>` / `<script>` on every page.
- Signs of haste `S.pages.*.placeholders`: lorem ipsum, `class="todo"`, `{{…}}`, `href="#"`.
Verdict: "one template / partial reuse / a set of independent pages", with evidence.

## L. Law and privacy

Signals and risks only, details in `law-ru.md`. Fields: `S.pages.*.legal`, `A.checks.checkboxes`,
`V.home.yandex.webvisor`, third-party hosts from `R.profiles.*.weight_full.third_party_hosts`.

## M. Other

DNS `V.dns` (A, AAAA — IPv6 or not, MX, SPF, DMARC — if the domain sends mail), certificate expiry, site
search (indexable results, duplicates), obvious text defects in title and h1, anything else seen from the
outside that is not covered above.
