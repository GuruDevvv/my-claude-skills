---
name: project-audit
description: >
  Project organization audit in Quick (~5 min) and Full (~8 min) modes.
  Diagnoses: CLAUDE.md quality, memory consistency, file structure,
  git hygiene, automations. Produces a severity-grouped report with
  actionable findings, then asks the user which items to address.
  Use when: "аудит проекта", "проверь проект", "проверь структуру",
  "audit project", "check project health", "что не так с проектом",
  "почисти проект", "проверь CLAUDE.md", "memory audit", "аудит memory",
  "project health check", "навести порядок в проекте", "ревью проекта",
  "что здесь происходит", "оцени состояние проекта", "clean up project".
  Also trigger on: quick audit, full audit, полный аудит, быстрый аудит,
  new/unfamiliar project assessment, pre-share/pre-publish cleanup.
  Do NOT use for: code review, PR review, debugging, runtime issues,
  or reviewing specs/designs (use multi-layer-review for those).
---

# Project Audit

Diagnose organizational health of any project: CLAUDE.md, memory, file structure, git, automations. Produce an actionable report grouped by severity, then let the user decide what to address.

**Why this exists:** Projects grow organically — CLAUDE.md gets stale, memory files accumulate dead links, files land in wrong places, secrets sneak into git. Without periodic checkups, Claude Code gets worse context and the user loses track of what's where.

**What this skill does NOT do:** It does not auto-fix anything. It diagnoses and recommends. The user decides which recommendations to act on — then can ask Claude to execute them.

**Two modes:**
- **Quick** (~5 min) — CLAUDE.md, memory, file architecture. No agents, no git, no automations. Best for regular checkups.
- **Full** (~8 min) — everything from Quick + git hygiene, automations, deep analysis via 5 parallel agents. Best for first audit, pre-share cleanup, or when something feels off.

---

## Safety rules

| Rule | Why |
|------|-----|
| **READ-ONLY: NEVER modify, create, or delete any project files** | This is a diagnostic tool. It observes and reports. All changes require explicit user approval after the report. |
| Don't read `.env`, `*.pem`, `*.key`, `*secret*`, `credentials*` | Content enters context and can leak into output. Note existence and size only. |
| Spotted a token/key → write `[SECRET hidden]` | Even accidental exposure in a report is a leak. |
| `| head -30` on any command with large output | Protects context window on large projects. |
| Don't read binary files (PDF, DOCX, images) | Note filename and size only. Reading wastes context. |
| Search secrets in git by filename pattern, not content | `git ls-files | grep -iE '\.env|\.pem'` — finds risk without reading secrets. |

---

## Mode selection

**MANDATORY:** Always ask the user which mode they want before proceeding.

**Args shortcut:** When invoked as `/project-audit full` or `/project-audit полный`, the skill receives the argument via the `args` parameter. If args contain "full" or "полный" — skip the question and go straight to Full mode. Same for "quick" or "быстрый" → Quick mode.

If no args match, ask (use AskUserQuestion if available, text otherwise):

> Какой режим аудита?
> - **Quick** (~5 мин) — CLAUDE.md, memory, архитектура проекта
> - **Full** (~8 мин) — всё из Quick + git гигиена, автоматизации, глубокий анализ через параллельных агентов

---

## Step 0 — Reconnaissance (both modes)

Before auditing, map the environment. Run all discovery commands in parallel where possible.

**First: root check.** If CWD is `/`, `C:\`, or a drive root — refuse immediately:
> "Запустите аудит из папки конкретного проекта, не из корня диска."

### Git, CLAUDE.md, Memory discovery
```
git rev-parse --is-inside-work-tree 2>/dev/null && echo "GIT: yes" || echo "GIT: no"
```
Use the Glob tool with pattern `**/CLAUDE.md` to find all CLAUDE.md files in the project.
```
ls ~/.claude/projects/ 2>/dev/null | head -20
```

If no CLAUDE.md found — that is itself a Critical finding. If not a git repo — note for "Skipped" section.

Match current project to a memory slug. Check for `MEMORY.md` inside the matched folder. Also check for `memory/` inside the project itself.

Read each found CLAUDE.md (first 100 lines) and store content for later analysis. Run `ls` on root and store output (first 20 lines).

### Project type detection

Check for code manifests and business folders. Use detection signals from `references/project-type-checklists.md` section "Project Type Detection".

```bash
# Code signals — manifests AND src/ directory
ls package.json requirements.txt go.mod Cargo.toml pyproject.toml *.sln 2>/dev/null
ls -d src/ app/ lib/ 2>/dev/null
```
For business/product signals (also match numbered prefixes like `02-audience`, `04-marketing`), use the Glob tool with pattern `*{audience,marketing,analytics,strategy,operations,products}*` — check first 2 directory levels only.

Classification:
- Code manifests found AND `src/`/`app/`/`lib/` exists, no business folders → **Code**
- Business folders found (3+), no `src/`/`app/`/`lib/` → **Product** (even if package.json exists — utility scripts don't make it a code project)
- Mostly `.md`/`.html`/`.txt` with no manifests or business folders → **Docs**
- `src/`/`app/`/`lib/` exists AND 3+ business folders → **Mixed**

**Key insight:** `package.json` alone doesn't indicate a Code project — many docs/product projects have it for utility scripts. The presence of `src/`, `app/`, or `lib/` is a much stronger signal.

If none of the above match (very few files, no clear signals) → treat as **Docs** and focus on file hygiene. Note the ambiguity in the report.

### File count
```bash
# Count project files (exclude common noise directories)
find . -type f -not -path '*/.git/*' -not -path '*/node_modules/*' -not -path '*/__pycache__/*' -not -path '*/.next/*' -not -path '*/dist/*' 2>/dev/null | wc -l
```
*(Note: `find` is acceptable here — Glob doesn't support counting. Pipe through `wc -l` only.)*

### Previous audit check

Derive memory slug from CWD: replace `/`, `\`, `:`, spaces with `-`, lowercase. Example: `E:\VibeCoding\MyProject` → `e--vibecoding-myproject`.

Check `~/.claude/projects/<slug>/memory/audits/` for existing reports. If found:
> Предыдущий аудит: [date]. Показать что изменилось?

If user agrees — after the current audit completes, read previous report and compare:
- **Fixed** — issues from previous audit no longer present
- **New** — issues not in previous audit
- **Persists** — issues still present from previous audit

Add a "Changes since last audit" section to the report before the Action plan.

### Show summary
```
Окружение:
- Git: yes/no
- CLAUDE.md: [locations or none]
- Memory: [path or none]
- Тип проекта: code/product/docs/mixed
- Файлов: ~N
```

---

## Quick mode

Quick runs Steps 1-3 sequentially. No agents, no git checks, no automations.

### Quick Step 1 — CLAUDE.md audit

Use checklist from `references/checklists.md`, section "CLAUDE.md checklist".

Key checks:
- **Documented folder structure vs reality** — run `ls` on project root and compare with what CLAUDE.md describes. Stale structure docs are the #1 source of Claude getting confused about where things are. This is the single most impactful check.
- **Broken internal links** — extract all paths/links from CLAUDE.md, verify each exists. Use Glob or `ls` to check.
- **Freshness** — look for dates in CLAUDE.md. If "Updated" date is >3 months old, flag as Warning. Check if described state matches current reality.
- **Empty or stub sections** — headers with no content underneath, or placeholder text like "TODO", "TBD".
- **Secrets or tokens** — scan for patterns like `sk-`, `ghp_`, `Bearer`, API keys. If found: Critical.
- **Missing critical sections** — project description, key files list, instructions for Claude, gotchas/warnings. Each missing section = Warning.
- **Multiple CLAUDE.md files** — if found at different depths, check for contradictions between them.

### Quick Step 2 — Memory audit

**Skip if no memory found in Step 0.** Note skip in report.

Use fallback checklist from `references/checklists.md`, section "Memory checklist".

Checks:
1. **Broken links** — does each link in MEMORY.md point to a file that actually exists? Check with Glob or `ls`.
2. **Orphan files** — `.md` files in memory folder not referenced by MEMORY.md. List all `.md` files, cross-reference with MEMORY.md links.
3. **Frontmatter** — each memory file should have `name`, `description`, `type` in YAML frontmatter. Missing fields = Warning.
4. **Zombie references** — memory files that mention specific project files, paths, or URLs that no longer exist. Read each linked memory file (don't recurse deeper) and verify key references.
5. **CLAUDE.md overlap** — same information maintained in both MEMORY.md and CLAUDE.md leads to drift. Flag overlapping content.
6. **Stale entries** — entries with dates >6 months old, or statuses like "В процессе" / "In progress" for clearly finished work.

### Quick Step 3 — Architecture scan

1. **Top-level scan:**
   Use the Glob tool with pattern `*/` and `*/*/` to list directories up to 2 levels deep. Also run `ls -la` for root contents.

2. **Load checklist** from `references/project-type-checklists.md` matching detected project type (Code/Product/Docs/Mixed). For Mixed projects, load both Code and Product checklists.

3. **Zone presence** — check expected folders for this project type exist. Missing critical zones = Warning.

4. **File hygiene:**
   - Root clutter — data files, HTML pages, images in root that should be in subdirectories. Standard root files are fine: README, CLAUDE.md, package.json, .gitignore, config files, LICENSE.
   - Temp/duplicate files — `.tmp`, `.bak`, `Copy of...`, files with `(1)`, `(2)` suffixes
   - Large files (>1MB):
     ```bash
     find . -type f -size +1M -not -path '*/.git/*' -not -path '*/node_modules/*' 2>/dev/null | head -20
     ```
     *(Note: `find -size` has no Glob equivalent — bash is acceptable here.)*
   - IDE artifacts — `.idea/`, `.vscode/` with non-standard contents, `*.swp`, `Thumbs.db`, `.DS_Store`
   - Empty directories:
     ```bash
     find . -type d -empty -not -path '*/.git/*' 2>/dev/null | head -10
     ```
     *(Note: empty dir detection has no Glob equivalent — bash is acceptable here.)*

5. **Apply severity modifiers** from `references/project-type-checklists.md` section "Severity Modifiers Table"

After Step 3, compile the detailed report (see Report template below). Fill in sections 1-3. Sections 4-5 go into "Пропущено" with note: "Quick mode — git и автоматизации не проверяются."

End Quick report with:
> Для полного аудита (git, автоматизации, глубокий анализ): `/project-audit full`

---

## Full mode

After Step 0, dispatch 5 parallel agents using the Agent tool. Full mode covers everything Quick does plus git hygiene, automations, and deeper analysis.

### Agent dispatch

**Preparation — read all reference files first:**

1. Read `references/agent-prompts.md` — get prompt templates, common blocks (Safety Rules, Output Format)
2. Read `references/checklists.md` — get all checklists
3. Read `references/project-type-checklists.md` — get type detection, severity modifiers
4. Build RECON RESULTS context block from Step 0 data:
   - Project name (derived from CWD folder name)
   - Project type (code/product/docs/mixed)
   - Git status (yes/no)
   - CLAUDE.md locations (paths found)
   - Memory path (or "none")
   - File count
   - Root listing (`ls` output, first 20 lines)
   - CLAUDE.md content (first 100 lines of each found file)

**Build each agent prompt by replacing these placeholders:**

| Placeholder | Content source |
|-------------|---------------|
| `{COMMON_CONTEXT_BLOCK}` | Filled RECON RESULTS from Step 0 |
| `{COMMON_SAFETY_RULES}` | "Common Safety Rules" section from agent-prompts.md |
| `{COMMON_OUTPUT_FORMAT}` | "Common Output Format" section from agent-prompts.md |
| `{CHECKLIST}` | The relevant checklist section from checklists.md (see agent-specific mapping below) |
| `{SEVERITY_MODIFIERS}` | "Severity Modifiers Table" section from project-type-checklists.md |

**Agent ↔ checklist mapping:**
- Agent 1 → "CLAUDE.md checklist" + "Severity Modifiers Table"
- Agent 2 → "Memory checklist"
- Agent 3 → "File structure checklist" + the project-type checklist (Code/Product/Docs) + "Severity Modifiers Table"
- Agent 4 → "Git checklist"
- Agent 5 → "Automations checklist"

**Why inject:** Agents run in the project directory, not the skill directory. They cannot access `references/` files themselves. The orchestrator MUST read these files and paste their content into each agent's prompt.

**Dispatch all 5 agents in parallel** using the Agent tool:
- **Agent 1** (CLAUDE.md deep audit) — `subagent_type: "Explore"`
- **Agent 2** (Memory audit) — `subagent_type: "Explore"`
- **Agent 3** (File structure) — `subagent_type: "Explore"`
- **Agent 4** (Git hygiene) — `subagent_type: "Explore"`
- **Agent 5** (Automations) — `subagent_type: "Explore"`

**Important:** Agents do NOT invoke companion skills. Checklists are injected into prompts by the orchestrator. This keeps agent context small and prevents token explosion from nested skill invocations.

### Synthesis

After all 5 agents return:
1. Collect all FINDINGS blocks from agent responses (each agent outputs findings in the Common Output Format)
2. Deduplicate — same issue found by multiple agents → keep the more detailed version, note which agents flagged it
3. Apply severity modifiers from `references/project-type-checklists.md` section "Severity Modifiers Table" (e.g., missing .gitignore in a docs project is Warning, not Critical)
4. **Build the detailed report** — map each agent's findings to the corresponding report section:
   - Agent 1 → Section "1. CLAUDE.md"
   - Agent 2 → Section "2. Memory"
   - Agent 3 → Section "3. Архитектура и файлы"
   - Agent 4 → Section "4. Git гигиена"
   - Agent 5 → Section "5. Автоматизации"
5. For each section, fill in "Что проверено" (from agent's ALL CLEAR + findings topics), "Находки" (findings with severity), "Рекомендации" (actionable fix for each finding)
6. Build the summary table from highest severity per area
7. Build the Action plan from all Critical + Warning findings across all areas
8. If any agent failed or timed out — note in "Пропущено" section with reason

---

## Report template

The report is a **detailed document with analysis per area**, not a summary table. Each area gets its own section with what was checked, what was found, and specific recommendations.

```markdown
# Аудит: [project name]

**Дата:** YYYY-MM-DD | **Режим:** Quick/Full | **Тип:** Code/Product/Docs/Mixed
**Файлов:** ~N | **Проблем:** Z

## Сводка

| Область | Статус | Находок |
|---------|--------|---------|
| CLAUDE.md | 🟢/⚠️/🔴 | N |
| Memory | 🟢/⚠️/🔴 | N |
| Архитектура | 🟢/⚠️/🔴 | N |
| Git | 🟢/⚠️/🔴 или ⏭️ | N |
| Автоматизации | 🟢/⚠️/🔴 или ⏭️ | N |

*Статус = наивысший severity среди находок в области. ⏭️ = пропущено (Quick mode).*

---

## 1. CLAUDE.md

### Что проверено
[Список проверок: структура, ссылки, свежесть, секреты, дубли с memory...]

### Находки
- 🔴 Critical: [конкретная проблема с путями/файлами]
- ⚠️ Warning: [проблема]
- 🟢 Low: [мелочь]

*(Если всё чисто: "Проблем не обнаружено.")*

### Рекомендации
- [Что конкретно сделать для каждой находки]

---

## 2. Memory

### Что проверено
[MEMORY.md индекс, ссылки, orphans, frontmatter, zombie references, overlap с CLAUDE.md...]

### Находки
- ...

### Рекомендации
- ...

---

## 3. Архитектура и файлы

### Что проверено
[Зоны по чеклисту типа проекта, root clutter, пустые папки, большие файлы, дубли...]

### Находки
- ...

### Рекомендации
- ...

---

## 4. Git гигиена *(только Full)*

### Что проверено
[.gitignore, секреты по имени файла, бинарники, untracked, статус...]

### Находки
- ...

### Рекомендации
- ...

---

## 5. Автоматизации *(только Full)*

### Что проверено
[Hooks, MCP серверы, settings, рекомендации по типу проекта...]

### Находки
- ...

### Рекомендации
- ...

---

## Пропущено
- [что пропущено и почему — Quick mode пропускает секции 4-5, отсутствие git/memory и т.д.]

---

## Action plan

Приоритезированный список действий (только Critical + Warning):

1. 🔴 [действие — конкретное, с указанием файлов]
2. 🔴 [действие]
3. ⚠️ [действие]
4. ⚠️ [действие]

**Какие пункты выполнить?**
```

### Report principles

- **Per-area structure** — each area has "Что проверено", "Находки", "Рекомендации". This makes the report a useful reference document, not just a list.
- **Summary table at top** — quick overview before the details
- **Findings are specific** — include file paths, counts, examples. Not "есть проблемы" but "CLAUDE.md:15 ссылается на `docs/api.md` — файл не найден"
- **Recommendations are actionable** — not "fix this" but "переместить `report.html` из корня в `docs/`"
- **Action plan = Critical + Warning only** — Low items stay informational in area sections
- **Language adaptation** — match the user's language (RU or EN), section structure stays constant
- **Closing question is key** — "Какие пункты выполнить?" lets the user pick what to address. Skill does NOT execute fixes.

### Severity criteria

| Severity | Criteria | Examples |
|----------|----------|----------|
| 🔴 Critical | Security risk, data loss, or breaks Claude's ability to work | Secrets in git, no .gitignore, CLAUDE.md missing, exposed API keys |
| ⚠️ Warning | Degrades quality, has workaround, fix before next milestone | Stale CLAUDE.md structure, orphan memory files, binaries in git, root clutter |
| 🟢 Low | Nice-to-have, can defer | Empty folders, missing IDE config, suboptimal .gitignore |

---

## Report saving

### Path derivation

1. Derive slug from CWD: replace `/`, `\`, `:`, spaces with `-`, lowercase
   - `E:\VibeCoding\MyProject` → `e--vibecoding-myproject`
2. Target: `~/.claude/projects/<slug>/memory/audits/YYYY-MM-DD-audit.md`

### Steps

```bash
SLUG=$(pwd | tr '[:upper:]' '[:lower:]' | sed 's/[\/\\: ]/-/g')
AUDIT_DIR="$HOME/.claude/projects/$SLUG/memory/audits"
mkdir -p "$AUDIT_DIR"
```

Write the full report to `$AUDIT_DIR/YYYY-MM-DD-audit.md`.

If a file with the same date already exists → append `-2`, `-3`, etc.:
```bash
BASE="$AUDIT_DIR/2026-03-18-audit"
if [ -f "$BASE.md" ]; then
  N=2; while [ -f "$BASE-$N.md" ]; do N=$((N+1)); done
  FILE="$BASE-$N.md"
else
  FILE="$BASE.md"
fi
```

After writing:
1. Verify the file exists: `ls -la "$FILE"`
2. Confirm to user: "Отчёт сохранён: [full path]"

---

## Edge cases

| Situation | Behavior |
|----------|----------|
| Run from filesystem root (`/` or `C:\`) | Refuse: "Запустите аудит из папки конкретного проекта, не из корня диска." |
| Project >200 files in Quick | Work normally, `| head` on all commands, no scope question |
| Project >1000 files in Full | Ask: "~N файлов. Сфокусироваться на корне и ключевых папках?" |
| No CLAUDE.md, no memory, no git | All three become Critical/Warning findings. Focus on file architecture |
| Agent times out or errors | Add to "Пропущено" section, continue with remaining agents' results |
| Previous audit exists in memory | Mention: "Предыдущий аудит: [date]. Показать что изменилось?" |
| Mixed project | Apply both checklists (code + product), take highest severity per finding |

---

## Reference files

All reference files live in `references/` relative to this skill's directory:

| File | Contains | Used by |
|------|----------|---------|
| `references/checklists.md` | Fallback checklists for CLAUDE.md, Memory, Automations, File structure, Git | Quick mode (all steps), Full mode (agent fallbacks) |
| `references/project-type-checklists.md` | Type detection signals, per-type checklists, severity modifiers | Step 0 (detection), Steps 1-3 (type-specific checks) |
| `references/agent-prompts.md` | Prompt templates for 5 parallel agents, common blocks | Full mode (agent dispatch) |

Every `references/` path in this file MUST point to an existing file. If a reference file is missing at runtime, skip the dependent check and note it in the report.
