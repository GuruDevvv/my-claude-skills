# mine/ — skills I wrote

Everything in this folder is mine. Written for my own work, sharpened on real projects, kept here as
the published copy. Third-party skills live in [`../external/`](../external/) and are clearly marked
as not mine.

**Install:** copy any folder into `~/.claude/skills/<skill-name>/` and restart Claude Code.

---

| Skill | What it does | Reach for it when |
|-------|--------------|-------------------|
| [idea-storm](idea-storm/) | Nine options across three shelves, three finalists, then two blind reviewers and a decision with a kill sign | A choice is open and the first sensible answer is not good enough |
| [spec-first](spec-first/) | Project kickoff in two passes: Vision (what and why), then Blueprint (how and in what order) | A new project exists as an idea and nothing is written down yet |
| [product-check](product-check/) | Five jobs-to-be-done questions, then a readiness score with named risks | The idea exists and the real question is whether to build it at all |
| [deep-research](deep-research/) | Multi-agent research with web search, confidence ratings, saved artifact | The answer is worth several sources and being wrong is expensive |
| [design-first](design-first/) | 4–6 concept-led HTML prototypes, a gallery, then build the chosen one | Visual work is starting and "make it look good" is not a brief |
| [multi-layer-review](multi-layer-review/) | Up to 5 blind parallel reviewers: architecture, code, user POV, robustness, requirements | A spec is finished and you want it attacked before code exists |
| [project-audit](project-audit/) | Audits CLAUDE.md quality, memory consistency, file structure, git hygiene | A project has grown messy, or before handing it to someone |
| [human-text](human-text/) | Russian copy that reads as human-written — rhythm, honest hedging, no AI clichés | Anything a person will read: posts, articles, landing copy, letters |
| [reels-console](reels-console/) | A vertical reel cut from one static take: pauses gone, crop levels anchored to the face, word-timed captions, music ducked | You filmed yourself talking to camera and need it edited without opening CapCut |

Each folder has its own `README.md` with the detail: what is inside, what it will not do, and where it
gets awkward.

Two of them also ship the research they grew out of, as `research.md` in the same folder:
[spec-first](spec-first/research.md) (10 methodologies, 12 templates, 6 real project disasters) and
[design-first](design-first/research.md) (why prototypes kept coming out technically flawless and
emotionally flat).

---

## The order they tend to run in

Not a pipeline, but there is a grain to it:

1. **idea-storm** — what are the options, and which one survives a critic who cannot see you?
2. **product-check** — should the chosen one exist at all?
3. **spec-first** — what is it, and in what order does it get built?
4. **multi-layer-review** — attack the spec before any code exists.
5. **design-first** — decide what it looks like, from a concept rather than a template.
6. **deep-research** — pulled in at any point where a decision needs real sources.
7. **project-audit** — later, when the project has grown and drifted.
8. **human-text** — whenever something has to be read by a person rather than a machine.

---

🇷🇺 Внутри каждого скилла есть описание на русском. Порядок выше — не жёсткий конвейер, а привычная
последовательность: сначала штурм вариантов, потом проверка идеи, спека, ревью спеки, дизайн; исследование
подключается там, где нужно решение с источниками; аудит — когда проект уже разросся.
