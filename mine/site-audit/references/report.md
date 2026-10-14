# Report template and dashboard data

Two outputs in the results folder: `report.md` (the full written report, for whoever fixes things) and
`audit.json` → `dashboard.html` (the visual summary, for the site owner). Write both in the user's
language. There is no section "what to check with access to the code".

## report.md

```markdown
# Audit of <site> — YYYY-MM-DD

Target: <address>, mode <live / pre-deploy / local>. Measured from: <country>, VPN <yes/no>.
Tags: [page] — measured on the page, [server] — measured on the live domain.
Raw data: static.json, render.json, a11y.json, server.json, shot_*.png, dashboard.html.

## 1. Summary for the owner
5–7 plain sentences: the state of the site, what is on fire, what it costs (speed, leads, search
positions, risk of a break-in). No jargon.

## 2. Traffic light
| Block | Score 1–10 | One-line verdict |
(blocks A–M from checks.md; a skipped block — "not applicable" with the reason)

## 3. Top 10 quick wins
Sorted by impact / effort. Each: ID, what to do, effort.

## 4. All findings
### <ID, e.g. E-03>. <Title>
- Severity: Blocker / Critical / Major / Minor / Info
- Where: URLs, files, headers, [page] or [server]
- Evidence: the measured number next to the threshold, or a response fragment up to 5 lines (secrets masked)
- Why it matters: the concrete consequence
- What to do: a concrete action (a config line, an attribute, a file)
- Effort: S (up to 2 h) / M (up to a day) / L (up to a week) / XL
- Confidence: high / medium / a guess

## 5. Needs a human check
Item: the machine cannot judge this — what was seen — what to check by hand (~2 min).

## 6. Page consistency
Only for 4+ pages, otherwise one line "not applicable: one landing page".

## 7. Stack card
| What | Value | Evidence |
CMS and version, web server, protocol and TLS, CDN, IPv6, third-party services, own API, admin panel.

## 8. Work plan
Today / next sprint / roadmap.

## 9. Check log
What ran (scripts, profiles, number of requests to the live site), what was skipped and why
(form not submitted, protection triggered, no browser mode, no CrUX data).
```

## Dashboard data (`audit.json`)

`build_dashboard.py` validates this and refuses to build on errors. Everything a person reads must be in
plain language: name things by what the owner sees ("Link preview in Telegram"), not by the mechanism
("Open Graph tags"). Each `fix` must make sense on its own, without the `text` next to it.

```json
{
  "lang": "en",
  "site": "Pottery studio landing",
  "address": "https://claystudio.example",
  "date": "14 October 2026",
  "mode": "Live site",
  "verdict": "Fast and safe; the link preview and two legal pages are missing",
  "headline": { "title": "Telegram shows a bare link", "text": "Most visitors come from Telegram, and the page has no preview card", "ok": false },
  "screenshot": "shot_desktop_first.png",
  "kpis": [
    { "title": "Main content on a phone", "value": "0.9", "unit": "s", "sub": "2.1 s on slow internet", "good": true, "note": "Target: under 2.5 s" }
  ],
  "weight": [ { "label": "Images", "mb": 0.82 } ],
  "speed": [ { "label": "Phone", "s": 0.9 } ],
  "speed_norm": 2.5,
  "server": [ { "label": "Secure connection (HTTPS)", "ok": true } ],
  "blocks": [
    {
      "id": "preview", "name": "Link preview in Telegram", "short": "Preview", "score": 3,
      "summary": "A link arrives without a picture or title",
      "items": [
        { "level": "important", "text": "The page has no preview card", "fix": "Add a 1200×630 picture and a title for the preview", "time": "1 hour", "minutes": 60 },
        { "level": "ok", "text": "Bots get the same page as people" }
      ]
    }
  ]
}
```

| Field | Required | Notes |
|---|---|---|
| `lang` | no | `en` (default) or `ru` — labels of the dashboard |
| `site`, `blocks` | yes | |
| `address`, `date`, `mode`, `verdict` | no | shown in the top line |
| `headline` | no | the red card top right: the one thing that matters most. `ok: true` turns the switch green. Omit to hide the card |
| `screenshot` | no | path relative to `audit.json`; embedded into the HTML |
| `kpis` | no | up to 4 big numbers. `good` true/false draws a green up / red down arrow; omit for none |
| `weight` | no | MB by type after a full scroll on mobile → "Page weight" tab |
| `speed`, `speed_norm` | no | seconds until the main content (median LCP) per profile → "Speed" tab with the target line |
| `server` | no | live-domain checks as ✓/✕. Omit in local-only mode |
| `blocks[].id` | yes | unique, latin |
| `blocks[].name` | yes | plain-language section name |
| `blocks[].short` | no | ≤9 characters, used under the bars |
| `blocks[].score` | yes | 1–10, per `thresholds.md` |
| `blocks[].summary` | yes | one line |
| `items[].level` | yes | `broken` (Blocker/Critical), `important` (Major), `minor` (Minor), `ok` (fine / Info) |
| `items[].text` | yes | what is wrong (or what is fine) |
| `items[].fix` | for broken/important | what to do; items with a fix get a "done" checkbox |
| `items[].time`, `items[].minutes` | no | effort as text and in minutes (minutes sort the table) |

Map the 13 check blocks to dashboard blocks by meaning, not one to one: merge what the owner sees as
one thing (e.g. "Ready to launch" for blockers from different blocks), drop blocks that were not applicable.
Typical set: ready to launch, link preview, documents and law, visible to search, protection, how the
server delivers files, usable by everyone, videos, labels for search engines, speed, code cleanliness,
page weight.

## Message to the user in chat

Not a retelling of the report:
1. First two lines — overall state and the most important thing (bad news goes here).
2. 2–4 points with status icons, only the unexpected.
3. What was not checked, one line, if it matters.
4. Paths to `dashboard.html` and `report.md`.
