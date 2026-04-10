# spec-first

A Claude Code skill that turns a vague project idea into a structured build plan — before writing any code.

Without a spec, Claude starts coding blindly, picks the wrong stack, and you lose all context when the session ends. With spec-first, you answer 10 simple questions, get two documents (`vision.md` + `blueprint.md`), and Claude in any future session knows exactly what to build and where you left off. Takes about **20 minutes**.

```
Idea → 10 questions → docs/vision.md → 7 interactive steps → docs/blueprint.md → CLAUDE.md updated → build
```

> **Language note:** The skill conducts the interview in Russian. English localization is planned.

---

## What you get

<details>
<summary><b>docs/vision.md</b> (excerpt) — click to expand</summary>

```markdown
# Vision: Daily Chat Summarizer

## One-liner
Telegram bot that sends a daily digest of group chat activity.

## Problem
Group chats accumulate 200+ messages/day. Most people stop reading and miss important things.

## User Stories
- User adds bot to a group chat → bot starts listening silently
- At 21:00 bot sends a summary to the user's DM → user reads it in 30 seconds

## Analogies & Differentiators
- Similar to Summarize Bot, but sends proactively on a schedule instead of on-demand
- Unlike ChatGPT group features — works in any Telegram group, no subscription

## MVP Scope
- [MUST] Listen to group messages and store them
- [MUST] Generate daily summary via LLM
- [NICE] Configurable summary time
- [LATER] Multi-language support

## NOT building in v1
- Web dashboard, analytics, paid plans
```

</details>

<details>
<summary><b>docs/blueprint.md</b> (excerpt) — click to expand</summary>

```markdown
## Build Plan
1. [ ] Project scaffold + bot token setup
   Files: bot.py, .env, requirements.txt
   Done when: /start returns a greeting

2. [ ] Message listener
   Files: handlers/listener.py, db/models.py
   Done when: messages from a group appear in the database

3. [ ] Daily summary job
   Files: jobs/summarize.py, prompts/summary.txt
   Done when: running the job manually produces a readable summary
```

</details>

---

## How it works

**Phase 1 — Vision (what and why)**

The skill asks 10 questions one at a time, in a specific order: dream first, context second, constraints third, verification last.

| # | Question | Purpose |
|---|----------|---------|
| Q1 | What do you want to build? | Core idea |
| Q1.5 | Why? What changes when it works? | Motivation — determines scope |
| Q2 | Who is it for? | Audience — you, friends, public |
| Q3 | Describe the main scenario step by step | Concrete user flow |
| Q4 | What should persist between sessions? | Data model seed |
| Q5 | How should the AI behave? *(only if AI is involved)* | Tone, boundaries |
| Q6 | Anything similar out there? How is yours different? | Competitive context |
| Q7 | Where does it run? Phone, desktop, Telegram? | Platform |
| Q7.5 | External services? Budget constraints? | Dependencies, budget |
| Q8 | What are we NOT building in v1? | Anti-scope |
| Q9 | How will you verify it works? | Acceptance tests |

If you struggle with any question, the skill offers smart defaults, analogies, and examples — it won't leave blanks.

**Output:** `docs/vision.md` with sections: problem, audience, user stories, competitive context, MVP scope (with Must/Nice/Later priorities), anti-scope, acceptance checks, data, risks.

**Gate:** Won't proceed to Blueprint until vision has at least 2 scenarios, 1 concrete check, and 1 anti-scope item. You can skip the gate, but it gets recorded as a risk.

---

**Phase 2 — Blueprint (how and in what order)**

Seven interactive steps, each shown and approved before moving on:

| Step | What happens |
|------|-------------|
| 1. Tech stack | Two options compared in plain language. Recommendation included |
| 2. Data model | Entities and fields as a table, based on Q4 answers |
| 3. Project structure | File/folder tree |
| 4. Deploy | Where will it live? Vercel, VPS, local? Based on Q7/Q7.5 answers |
| 5. Build plan | 3–15 tasks with files and "done when" criteria |
| 6. Acceptance checklist | 5+ checks in "Do X, see Y" format |
| 7. AI config | *(only if AI is involved)* Provider, system prompt, behavior checks |

**Output:** `docs/blueprint.md` with tech stack, structure, data model, deploy plan, task checklist, and acceptance criteria.

**Gate:** Stack approved, 3–15 tasks, 5+ checks, data described, no contradictions with vision.

**After gate:** Updates the project's `CLAUDE.md` with description, stack, boundaries (Always / Ask First / Never), and a rule to always check `docs/blueprint.md` before starting work — so Claude in any future session knows the plan.

---

## Key features

- **Retrospective mode.** Already have code but no docs? The skill analyzes your codebase first, drafts answers, and asks you to confirm — then proceeds with the standard flow.
- **Anti-pattern detection.** Watches for scope creep ("one more feature"), vague requirements ("make it work"), and deferred decisions ("we'll figure it out later") — and responds immediately.
- **Gate skip mechanism.** If you insist on skipping a gate, the skill records it as a risk with `[GATE SKIP]` — doesn't block you, but doesn't let you forget.
- **Session continuity.** The generated docs + CLAUDE.md update mean Claude in a new session can pick up exactly where you left off.
- **Must / Nice / Later prioritization.** MVP scope isn't a flat list — each feature is tagged so you know what to cut first if scope needs trimming.

---

## When to use

- Starting a new project from scratch
- You have code but no documentation or plan
- You want to explain your idea to Claude and get a structured build plan
- You keep losing context between sessions

## When NOT to use

- Reviewing an existing spec (use [multi-layer-review](../multi-layer-review) instead)
- Adding features to a project that already has `docs/vision.md`
- Debugging, code review, or general questions

---

## Installation

Check [what you're installing](SKILL.md) before running the command.

**As a slash command (recommended):**

macOS / Linux:
```bash
curl --fail -o ~/.claude/commands/spec-first.md \
  https://raw.githubusercontent.com/GuruDevvv/my-claude-skills/main/spec-first/SKILL.md
```

Windows (Git Bash or WSL):
```bash
curl --fail -o "$USERPROFILE/.claude/commands/spec-first.md" \
  https://raw.githubusercontent.com/GuruDevvv/my-claude-skills/main/spec-first/SKILL.md
```

**As a skill (auto-triggers on project ideas):**

macOS / Linux:
```bash
mkdir -p ~/.claude/skills/spec-first
curl --fail -o ~/.claude/skills/spec-first/SKILL.md \
  https://raw.githubusercontent.com/GuruDevvv/my-claude-skills/main/spec-first/SKILL.md
```

Windows (Git Bash or WSL):
```bash
mkdir -p "$USERPROFILE/.claude/skills/spec-first"
curl --fail -o "$USERPROFILE/.claude/skills/spec-first/SKILL.md" \
  https://raw.githubusercontent.com/GuruDevvv/my-claude-skills/main/spec-first/SKILL.md
```

Restart your Claude Code session — the terminal running `claude`, or reload the VS Code window.

**Verify:** type `/spec-first` or describe a new project idea — the skill activates automatically.
