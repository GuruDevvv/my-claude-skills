# Project Type Checklists

Reference file for project-audit skill. Read by SKILL.md and parallel agent prompts during audits.

---

## 1. Project Type Detection

### Signals Table

| Signal | Type |
|--------|------|
| Code manifest + `src/`, `app/`, or `lib/` directory, no business folders | **Code** |
| 3+ business-oriented folders (audience, marketing, analytics, strategy, operations, products), no `src/`/`app/`/`lib/` | **Product/Business** |
| Only `.md`/`.html` without business structure or code dirs (wiki, tech docs, API docs) | **Documentation** |
| `src/`/`app/`/`lib/` exists AND 3+ business-oriented folders | **Mixed** — both checklists apply |

**Code manifests:** `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `*.sln`, `pyproject.toml`

**Business folder detection:** Also match numbered prefixes: `02-audience`, `04-marketing`, etc. Use glob patterns like `*-audience`, `*-marketing`.

### Mixed Detection Rule

`package.json` alone does NOT make a project "Code" — many Product/Business projects have it for utility scripts or deploy tooling.

The key signal is `src/`, `app/`, or `lib/` — these indicate actual application code.

- `src/` + 3+ business folders → **Mixed**
- `package.json` + 3+ business folders but no `src/` → **Product/Business**
- `src/` + only `docs/` → **Code**
- When in doubt → **ask user**

---

## 2. Code Project Checklist

Applies when project type is **Code** or **Mixed**.

| Zone | What to check |
|------|--------------|
| Source code | Has `src/` or equivalent, code not scattered in root |
| Tests | Has `tests/` or `__tests__/`, or co-located test files |
| Configuration | Configs separated from code (env, config files) |
| Build/Deploy | CI/CD, Dockerfile, deploy scripts — present or consciously absent |
| Documentation | At minimum README explaining how to run |
| Dependencies | Lock file up to date, no phantom dependencies |

---

## 3. Product/Business Project Checklist

Applies when project type is **Product/Business** or **Mixed**.

| Zone | What to check |
|------|--------------|
| Audience/Clients | Who is the user, segments, portraits |
| Product | Product/service description, roadmap, features |
| Marketing/Channels | Funnels, acquisition channels, content |
| Analytics/Metrics | Finances, KPIs, reports |
| Processes/Operations | Team, SOPs, regulations |
| Strategy | Goals, OKR, decisions |

---

## 4. Documentation Project Checklist

Applies when project type is **Documentation**.

| Zone | What to check |
|------|--------------|
| Section structure | Logical hierarchy, clear navigation |
| Index/TOC | Entry point exists (README, index) |
| Completeness | No empty stubs, TODO, TBD |
| Freshness | Dates, versions, links not outdated |
| Cross-references | Internal links work |

---

## 5. Severity Modifiers Table

Use these to calibrate finding severity based on project type.

**Mixed projects:** apply both checklists, take the highest severity.

| Finding | Code | Product/Biz | Docs |
|---------|------|-------------|------|
| Broken links in CLAUDE.md | ⚠️ Warning | 🔴 Critical | 🔴 Critical |
| No audience description | 🟢 Low | ⚠️ Warning | 🟢 Low |
| No tests/CI | ⚠️ Warning | 🟢 Low | 🟢 Low |
| Binaries in git | ⚠️ Warning | 🟢 Low | 🟢 Low |
| Secrets in git | 🔴 Critical | 🔴 Critical | 🔴 Critical |
| No README / entry point | ⚠️ Warning | 🔴 Critical | 🔴 Critical |
| Dead zones (empty planned folders) | 🟢 Low | ⚠️ Warning | ⚠️ Warning |
| CLAUDE.md <-> Memory duplication | ⚠️ Warning | ⚠️ Warning | ⚠️ Warning |
| No .gitignore | 🔴 Critical | ⚠️ Warning | ⚠️ Warning |
