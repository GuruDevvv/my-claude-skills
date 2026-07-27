# mine/ — skills I wrote

Everything in this folder is mine. Written for my own work, sharpened on real projects, kept here as
the published copy. Third-party skills live in [`../external/`](../external/) and are clearly marked
as not mine.

**Install:** copy any folder into `~/.claude/skills/<skill-name>/` and restart Claude Code.

---

| Skill | What it does | Reach for it when |
|-------|--------------|-------------------|
| [spec-first](spec-first/) | Project kickoff in two passes: Vision (what and why), then Blueprint (how and in what order) | A new project exists as an idea and nothing is written down yet |
| [product-check](product-check/) | Five jobs-to-be-done questions, then a readiness score with named risks | The idea exists and the real question is whether to build it at all |
| [deep-research](deep-research/) | Multi-agent research with web search, confidence ratings, saved artifact | The answer is worth several sources and being wrong is expensive |
| [design-first](design-first/) | 4–6 concept-led HTML prototypes, a gallery, then build the chosen one | Visual work is starting and "make it look good" is not a brief |
| [multi-layer-review](multi-layer-review/) | Up to 5 blind parallel reviewers: architecture, code, user POV, robustness, requirements | A spec is finished and you want it attacked before code exists |
| [project-audit](project-audit/) | Audits CLAUDE.md quality, memory consistency, file structure, git hygiene | A project has grown messy, or before handing it to someone |
| [human-text](human-text/) | Russian copy that reads as human-written — rhythm, honest hedging, no AI clichés | Anything a person will read: posts, articles, landing copy, letters |

Each folder has its own `README.md` with the detail: what is inside, what it will not do, and where it
gets awkward.

---

## The order they tend to run in

Not a pipeline, but there is a grain to it:

1. **product-check** — should this exist at all?
2. **spec-first** — what is it, and in what order does it get built?
3. **multi-layer-review** — attack the spec before any code exists.
4. **design-first** — decide what it looks like, from a concept rather than a template.
5. **deep-research** — pulled in at any point where a decision needs real sources.
6. **project-audit** — later, when the project has grown and drifted.
7. **human-text** — whenever something has to be read by a person rather than a machine.

---

🇷🇺 Внутри каждого скилла есть описание на русском. Порядок выше — не жёсткий конвейер, а привычная
последовательность: сначала проверить идею, потом спека, ревью спеки, дизайн; исследование
подключается там, где нужно решение с источниками; аудит — когда проект уже разросся.
