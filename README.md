# my-claude-skills

My custom skills for [Claude Code](https://claude.ai/claude-code).

Each skill is a folder with a `SKILL.md` file — drop it into `~/.claude/skills/<skill-name>/` and restart Claude Code.

---

## Skills

| Skill | Description |
|-------|-------------|
| [design-first](design-first/) | Generate 4–6 concept-led HTML design prototypes before coding — interview, references, parallel prototypes, gallery, pick & build, then a Feel pass polish on the real build |
| [multi-layer-review](multi-layer-review/) | Run your spec through up to 5 blind parallel reviewers before coding — architecture, code, user POV, robustness, requirements |
| [project-audit](project-audit/) | Audit project organization — CLAUDE.md quality, memory consistency, file structure, git hygiene |
| [spec-first](spec-first/) | Structured project kickoff: Vision (what/why) then Blueprint (how/order) — before writing any code |

---

*🇷🇺 Есть русские описания внутри каждого скилла*

---

## Research

В `research/` лежат исследования, использованные при разработке скиллов:
- `spec-first-research.md` — полное исследование Spec-First методологии (10 методологий, 12 шаблонов, 6 реальных катастроф → VIBE SPEC)
- `project-audit-prompt.txt` — детальный промпт-шаблон для полного аудита проекта (6 шагов)
