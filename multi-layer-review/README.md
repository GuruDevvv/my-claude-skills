# multi-layer-review

[🇷🇺 Читать на русском](README.ru.md)

A Claude Code skill that runs your spec or technical design through up to 5 **independent blind reviewers** in parallel — before you start coding. Each reviewer works independently: no shared findings, no bias amplification. Convergence on the same issue from multiple reviewers is a strong signal.

---

## How it works

**Step 0.5 — Get spec.** File, path, or inline text.

**Step 0.6 — Review Brief (automatic).** Auto-generates project context: what project, what document, is there existing code for this topic, related files. Passed to all reviewers.

**Step 0.7 — Ambiguity Gate (automatic).** Scans the spec for vague requirements, contradictions, missing constraints. If found — asks you to clarify or proceed.

**Step 0.8 — Project Context Snapshot (automatic).** One-time scan of the codebase: structure, manifests, relevant code, configs. Shared with all reviewers so they ground analysis in real project state, not abstract reasoning.

**Steps 1–5 — Blind Reviewers (parallel).** Each reviewer examines the spec independently with the brief + project context. No reviewer sees another's findings. They use Read/Glob/Grep to check actual project files.

**Final — Synthesis.** All findings are merged, deduplicated, and sorted by priority. Independent convergence (2+ reviewers found the same thing) upgrades severity by one level.

---

## Reviewers

| # | Role | What they look for |
|---|------|--------------------|
| 1 | **Requirements Traceability** — analyst | Are we solving the right problem? Does the solution match the business goal? Are there success criteria? |
| 2 | **Plan Agent** — architect | Structural gaps, API design quality, edge cases, contradictions, compatibility with existing architecture |
| 3 | **Codex CLI** — developer *(requires [Codex CLI](https://github.com/openai/codex))* | Implementation risks, unsafe patterns, dependency issues, missing error handling |
| 4 | **Devil's Advocate** — skeptical user | "What if..." — UX failures, unexpected behavior, what breaks on day one |
| 5 | **Robustness Checklist** — systems engineer | Scores 0–3 across 8 criteria: error handling, concurrency, security, testability, etc. |

You can choose which reviewers to run — all five is the default, but not required.

**Output format:** Every finding is `[Critical/Important/Minor] Section: "X" — description`. Max 10 findings per reviewer. "No issues found" is a valid outcome.

---

## What's new in v3.0

- **Blind reviews** — no more finding propagation between reviewers (eliminates confirmation bias and panic escalation)
- **Parallel execution** — reviewers run simultaneously, faster results
- **Review Brief** — auto-generated project/document context for all reviewers
- **Project Context Snapshot** — one-time codebase scan, shared with all reviewers
- **Grounded analysis** — reviewers use Read/Glob/Grep to check actual files, not just reason abstractly
- **Unified output format** — consistent severity ratings, section references, max 10 findings
- **No invented problems** — explicit rule against generic advice and hypothetical issues

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

The skill asks which reviewers to run, asks for your spec (file or text), collects project context, runs reviewers in parallel, and outputs a synthesis showing who found what. Results are saved to a file.

---

## Installation

Check [what you're installing](SKILL.md) before running the command.

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
