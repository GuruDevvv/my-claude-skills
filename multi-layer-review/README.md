# multi-layer-review

[🇷🇺 Читать на русском](README.ru.md)

A Claude Code skill that runs your spec or technical design through a chain of up to 5 reviewers before you start coding. Each reviewer passes their findings to the next — so later reviewers can confirm, refute, or expand on them, in any combination.

---

## How it works

**Step 0 — Ambiguity Gate (automatic).**
Before any reviewer runs, the skill scans the spec for ambiguities: vague requirements ("fast", "convenient"), contradictions between sections, missing constraints. If found — it asks you to clarify or proceed anyway.

**Steps 1–5 — Reviewers.**
Each reviewer examines the spec from their own angle. From the second reviewer onwards, each sees what the previous ones found — and can confirm, refute, or expand on them in any combination. This eliminates duplication and sharpens the critique.

**Final — Synthesis.**
All findings are merged, deduplicated, and sorted by priority: Critical / Important / Minor.

---

## Reviewers

| # | Role | What they look for |
|---|------|--------------------|
| 1 | **Requirements Traceability** — analyst | Are we solving the right problem? Does the solution match the business goal? Are there success criteria? |
| 2 | **Plan Agent** — architect | Structural gaps, API design quality, edge cases, contradictions between sections |
| 3 | **Codex CLI** — developer *(requires [Codex CLI](https://github.com/openai/codex) installed)* | Implementation risks, unsafe patterns, dependency issues, missing error handling |
| 4 | **Devil's Advocate** — skeptical user | "What if..." — UX failures, unexpected behavior, what breaks on day one |
| 5 | **Robustness Checklist** — systems engineer | Scores 0–3 across 8 criteria: error handling, concurrency, security, testability, etc. |

You can choose which reviewers to run — all five is the default, but not required.

---

## When to use

- You've written a spec or design doc and want to find problems before coding
- You're designing an API or module architecture
- You're not sure you understood the task correctly or are solving the right problem

---

## Example

```
You: multi-layer review
```

The skill asks which reviewers to run, asks for your spec (file or text), runs it through the selected reviewers, and outputs a synthesis showing who found what. Results are saved to a file.

---

## Installation

Check [what you're installing](multi-layer-review/SKILL.md) before running the command.

**macOS / Linux:**
```bash
mkdir -p ~/.claude/skills/multi-layer-review
curl --fail -o ~/.claude/skills/multi-layer-review/SKILL.md \
  https://raw.githubusercontent.com/GuruDevvv/my-claude-skills/main/multi-layer-review/SKILL.md
```

**Windows (Git Bash or WSL):**
```bash
mkdir -p "$USERPROFILE/.claude/skills/multi-layer-review"
curl --fail -o "$USERPROFILE/.claude/skills/multi-layer-review/SKILL.md" \
  https://raw.githubusercontent.com/GuruDevvv/my-claude-skills/main/multi-layer-review/SKILL.md
```

Restart your Claude Code session — the terminal running `claude`, or reload the VS Code window.

**Verify:** type `multi-layer review` to your agent — the skill activates automatically.
