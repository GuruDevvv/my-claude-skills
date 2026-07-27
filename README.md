# my-claude-skills

Skills for [Claude Code](https://claude.ai/claude-code) — the ones I wrote, and the third-party ones
I actually use, kept in one place so my setup is reproducible.

**Install any of them:** copy the folder into `~/.claude/skills/<skill-name>/` and restart Claude Code.

Two folders, and the distinction is not cosmetic:

- **root** — mine. Written by me, maintained here.
- **[`external/`](external/)** — **not mine.** Third-party MIT skills, vendored with full attribution
  and the original licence texts. Prefer installing those from upstream; see
  [external/README.md](external/README.md).

---

## Mine

| Skill | What it does | Reach for it when |
|-------|--------------|-------------------|
| [spec-first](spec-first/) | Project kickoff in two passes: Vision (what and why), then Blueprint (how and in what order) | A new project exists as an idea and nothing is written down yet |
| [product-check](product-check/) | Five jobs-to-be-done questions, then a readiness score with risks | The idea exists and the real question is whether to build it at all |
| [deep-research](deep-research/) | Multi-agent research with web search, confidence ratings, saved artifact | The answer is worth several sources and being wrong is expensive |
| [design-first](design-first/) | 4–6 concept-led HTML prototypes, then a gallery, then build the chosen one | Visual work is starting and "make it look good" is not a brief |
| [multi-layer-review](multi-layer-review/) | Up to 5 blind parallel reviewers: architecture, code, user POV, robustness, requirements | A spec is finished and you want it attacked before code exists |
| [project-audit](project-audit/) | Audits CLAUDE.md quality, memory consistency, file structure, git hygiene | A project has grown messy, or before handing it to someone |
| [human-text](human-text/) | Russian copy that reads as human-written — rhythm, honest hedging, no AI clichés | Anything a person will read: posts, articles, landing copy, letters |

*🇷🇺 У каждого скилла внутри есть описание на русском.*

---

## External — not my work

Vendored third-party skills, all MIT, each with author and source in
[external/README.md](external/README.md) and licence texts in
[external/licenses/](external/licenses/).

| Skill | What it does | Author |
|-------|--------------|--------|
| [pricing](external/pricing/) | Value metric, tiers, willingness-to-pay research, when and how to raise prices | Corey Haines |
| [marketing-plan](external/marketing-plan/) | 12-month plan across the funnel, 13 sections, 139-tactic library included | Corey Haines |
| [site-architecture](external/site-architecture/) | Page hierarchy, navigation, URL structure, redirects when restructuring | Corey Haines |
| [negotiation](external/negotiation/) | Chris Voss method: mirroring, labelling, calibrated questions, Ackerman ladder | Wondel.ai |
| [high-output-management](external/high-output-management/) | Grove: leverage, limiting step, indicators that cannot be gamed, 1:1s, OKRs | Wondel.ai |
| [doc-to-markdown](external/doc-to-markdown/) | DOCX/PDF/PPTX to clean Markdown, tables and images intact | daymade † |
| [mermaid-tools](external/mermaid-tools/) | Mermaid diagrams out of Markdown into high-resolution PNG | daymade † |
| [ppt-creator](external/ppt-creator/) | Decks with assertion-style headings, charts, speaker notes, self-scoring | daymade |
| [meeting-minutes-taker](external/meeting-minutes-taker/) | Transcript to minutes without losing content; honest about who spoke | daymade |
| [youtube-downloader](external/youtube-downloader/) | yt-dlp plus the bot-check, 403 and locked-platform handling | daymade |
| [ui-ux-pro-max](external/ui-ux-pro-max/) | Design reference as queryable data: styles, palettes, type, UX rules, 13 stacks | nextlevelbuilder |
| [skill-conductor](external/skill-conductor/) | Skill lifecycle: create, improve, validate, review, optimise, package | smixs |

† **Patched, not byte-identical to upstream** — both were broken on Windows. Each patch and the reason
for it is documented at the top of that skill's README.

**Not vendored on purpose:** `remotion-best-practices` (Remotion team) is excellent, but
[remotion-dev/skills](https://github.com/remotion-dev/skills) ships no licence file at all — default
copyright, all rights reserved. Redistributing it would not be legal. Install it from the source.

---

## Research

В `research/` лежат исследования, использованные при разработке скиллов:

- `spec-first-research.md` — полное исследование Spec-First методологии (10 методологий, 12 шаблонов,
  6 реальных катастроф → VIBE SPEC)
- `project-audit-prompt.txt` — детальный промпт-шаблон для полного аудита проекта (6 шагов)
- `design-first-wow-research.md`, `design-first-redesign-plan.md` — материалы к design-first
