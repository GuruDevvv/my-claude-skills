# project-audit

Skill for auditing project organization health. Diagnoses CLAUDE.md quality, memory consistency, file structure, git hygiene, and Claude Code automations. Produces a severity-grouped report with actionable findings.

## Installation

1. Copy the `project-audit/` folder to a convenient location
2. Add the path to your Claude Code settings:
   ```json
   // ~/.claude/settings.json
   {
     "skills": [
       "/path/to/project-audit"
     ]
   }
   ```

## Usage

- `/project-audit` — Quick audit (~5 min): CLAUDE.md, memory, file architecture
- `/project-audit full` — Full audit (~8 min): everything from Quick + git hygiene, automations, deep analysis via 5 parallel agents

The skill auto-detects project type and adapts checks accordingly.

## Modes

| Mode | Time | Scope |
|------|------|-------|
| **Quick** | ~5 min | CLAUDE.md, memory, architecture scan |
| **Full** | ~8 min | Quick + git hygiene, automations, 5 parallel agents |

## Project Types

The skill auto-detects the project type and uses type-specific checklists:

- **Code** — source structure, tests, CI, dependencies, build/deploy
- **Product/Business** — audience, product, marketing, analytics, processes, strategy
- **Documentation** — section structure, navigation, completeness, freshness
- **Mixed** — both Code and Product/Business checklists apply

## Severity Levels

- **🔴 Critical** — must fix, blocks quality or safety
- **⚠️ Warning** — should fix, notable problem
- **🟢 Low** — minor, nice to fix

Severity is calibrated per project type (e.g., missing `.gitignore` is Critical for code projects but Warning for docs projects).

## Report

The audit produces a **detailed per-area report** (not just a summary table) with sections for each audit area: CLAUDE.md, Memory, Architecture, Git, Automations. Each section includes what was checked, findings with severity, and specific recommendations.

Reports are saved to `~/.claude/projects/<slug>/memory/audits/`. Subsequent audits can compare with previous reports to show what was fixed, what's new, and what persists.

## Safety

The skill is strictly **read-only** — it diagnoses and reports but never modifies, creates, or deletes project files. All changes require explicit user approval after the report.
