# Thresholds and severity

Always put the measured value next to the threshold in the report.

## Thresholds

| Metric | Good | Warning | Problem |
|---|---|---|---|
| Inline CSS+JS+data: share of HTML | ≤5 % | 5–10 % | >10 % |
| Inline critical CSS, absolute | ≤14 KB | 14–50 KB | >50 KB |
| HTML size | ≤100 KB | 100–200 KB | >200 KB |
| First screen (before scroll), no video | ≤1 MB | 1–2 MB | >2 MB |
| Whole page without video | ≤1.5 MB | 1.5–3 MB | >3 MB |
| Video on mobile after a full scroll | ≤2 MB | 2–5 MB | >5 MB |
| Requests | ≤50 | 50–80 | >80 |
| CSS files (HTTP/1.1 only) | ≤3 | 4–6 | >6 |
| JS files (HTTP/1.1 only) | ≤5 | 6–10 | >10 |
| Third-party hosts with resources | ≤3 | 4–6 | >6 |
| Unused JS, absolute | <50 KB | 50–150 KB | >150 KB |
| Unused CSS, absolute | <30 KB | 30–80 KB | >80 KB |
| Single image | ≤150 KB | 150–400 KB | >400 KB |
| og:image | ≤300 KB, ~1200×630 | 300–600 KB | >600 KB or not 200 |
| Server response (TTFB, median) | ≤0.8 s | 0.8–1.8 s | >1.8 s |
| FCP | ≤1.8 s | 1.8–3 s | >3 s |
| LCP | ≤2.5 s | 2.5–4 s | >4 s |
| CLS (session windows) | ≤0.1 | 0.1–0.25 | >0.25 |
| TBT (lab) | ≤200 ms | 200–600 ms | >600 ms |
| INP (lab, via clicks) | ≤200 ms | 200–500 ms | >500 ms |
| Title length (Cyrillic / Yandex: up to 70) | 30–60 | 20–30 / 60–80 | <20 / >80 |
| Description length | 70–160 | 160–200 | >200 (do not penalise a short one on a landing page) |
| h1 per page | exactly 1 | — | 0 or ≥2 |
| Duplicate title/description across the site | 0 % | up to 10 % | >10 % |
| Static reuse ratio (4+ pages) | >0.8 | 0.4–0.8 | <0.4 |
| Touch target | ≥44×44 | 24–44 | <24×24 |
| Text | body ≥16 px | body 12–16 px | anything <12 px |
| Text contrast | ≥4.5:1 (large ≥3:1) | — | lower |
| Certificate | >14 days left | — | <14 days, or older than 65 days on Let's Encrypt |
| CMS version lag | current branch | 1–2 minor | major / EOL |

Do not use FID (replaced by INP). Speed metrics are the median of three runs; spread over 20 % —
mark "unstable". A single run — confidence "a guess".

## Measurement profiles (`render_audit.py`)

| Profile | Screen | CPU | Network |
|---|---|---|---|
| `mobile` | 360×800, DPR 3 | ×1 | unthrottled |
| `mobile_390` | 390×844, DPR 3 | ×1 | unthrottled |
| `mobile_4g` | 360×800, DPR 3 | ×2 | 70 ms, 9 Mbit/s |
| `mobile_slow` | 360×800, DPR 3 | ×4 | 150 ms, 1.6 Mbit/s (Lighthouse mobile) |
| `desktop` | 1366×768 | ×1 | unthrottled |
| `desktop_1440` | 1440×900 | ×1 | unthrottled |

The CPU multiplier is relative to the machine running the audit: ×4 on a fast laptop is still a phone
faster than average. Say so in the caveats.

## Severity

| Level | What goes here | Dashboard `level` |
|---|---|---|
| **Blocker** | exposed `.git`, `.env`, backups, project folder, agent notes (`CLAUDE.md` / `HANDOFF.md`); a bot token or secret key in page code | `broken` |
| **Critical** | no HTTPS, expired certificate, admin panel open to everyone; zoom blocked; a placeholder or obvious defect where people decide to buy ("Starts: date"); the main form without field names; the backend of the page's main feature does not answer (`api.*.deployed=false` on a live site; in pre-deploy mode it blocks the release) | `broken` |
| **Major** | incomplete certificate chain, no redirect to https, no messenger preview when traffic comes from messengers, draft leftovers in indexing, touch targets <24 px, LCP >4 s, horizontal scroll at 360 px, signup button or price cut off at 320 px / with text ×2 | `important` |
| **Minor** | missing security headers on a static site without logins, server version leak, small text, no `<main>`, no canonical on a one-pager, horizontal scroll only at 320 px or with text ×2 | `minor` |
| **Info** | good practice, harmless observations, things that are fine | `ok` (when it is a "fine" item) |

Block score 1–10: at least one Critical in the block — 4 at most; a Blocker — 2 at most.
