# spec-first

A Claude Code skill that turns a vague project idea into a structured build plan — before writing any code.

Without a spec, Claude starts coding blindly, picks the wrong stack, and you lose all context when the session ends. With spec-first, you answer **5 simple questions**, Claude proposes everything else as a short list of assumptions you can correct, and you get two documents (`vision.md` + `blueprint.md`). Claude in any future session knows exactly what to build and where you left off. Takes about **10 minutes**.

```
Idea → 5 questions → "decided for you" list → docs/vision.md → stack choice → whole plan in one block → docs/blueprint.md → CLAUDE.md updated → build
```

**Design principle:** you answer only what you alone know (what, why, for whom, the main scenario, what's out of scope). Data, platform, services, analogues, acceptance checks and stack details are Claude's job — it proposes them and shows its assumptions, so nothing is decided silently.

> **Language note:** The skill conducts the interview in Russian. English localization is planned.

---

## What you get

<details>
<summary><b>docs/vision.md</b> (excerpt) — click to expand</summary>

```markdown
# Vision: Daily Chat Summarizer

## One-liner
Telegram bot that sends a daily digest of group chat activity.

## Why
Group chats accumulate 200+ messages/day. Most people stop reading and miss important things.

## Scenarios
- User adds bot to a group chat → bot starts listening silently
- At 21:00 bot sends a summary to the user's DM → user reads it in 30 seconds

## Analogues & differences
- Similar to Summarize Bot, but sends proactively on a schedule instead of on-demand

## v1 scope
- [need] Listen to group messages and store them
- [need] Generate daily summary via LLM
- [nice] Configurable summary time
- [later] Multi-language support

## NOT building in v1
- Web dashboard, analytics, paid plans

## Assumptions and risks
- Decided by Claude: runs on the user's VPS, summary at 21:00 local time
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

The skill asks 5 questions one at a time:

| # | Question | Purpose |
|---|----------|---------|
| Q1 | What are we building? | Core idea |
| Q2 | Why? What changes when it works? | Motivation — determines scope |
| Q3 | Who is it for? | Audience — you, friends, public |
| Q4 | Describe the main scenario step by step | Concrete user flow |
| Q5 | What are we NOT building in v1? (with suggested extensions to postpone) | Anti-scope |

Along the way Claude flags contradictions between your answers right away instead of silently picking one.

Then Claude shows a **one-screen concept**: one-liner, why and for whom, the main flow, what's in and out of v1, open questions, and a **"decided for you"** list (what persists between sessions, where it runs, external services and budget, 2–3 analogues, AI tone if any, 3 acceptance checks). You fix what's wrong; "ok" confirms, and the concept becomes `docs/vision.md`.

**Output:** `docs/vision.md` with sections: why, audience, scenarios, analogues, v1 scope (need / nice / later), anti-scope, acceptance checks, data, AI behavior, assumptions and risks.

**Gate:** Won't proceed to Blueprint until vision has at least 2 scenarios, 1 concrete check, and 1 anti-scope item. You can skip the gate, but it gets recorded as a risk.

---

**Phase 2 — Blueprint (how and in what order)**

At most two stops instead of eight:

| Step | What happens |
|------|-------------|
| 1. Tech stack | Only if there are two genuinely different paths (bot vs site, free vs fast): both in plain language, with a recommendation — **you choose**. Otherwise Claude picks and lists it as an assumption |
| 2. Whole plan, one block | Data tables, file tree, where it lives (your own VPS by default, local if no server is needed; cloud hosts only on request), 3–15 tasks with "done when", 5+ acceptance checks, assumptions |
| — Fresh eyes | Claude re-reads vision + plan itself *before* showing it (coverage, order, checkability, phases, no contradictions) and fixes gaps silently |
| 3. Approval | **You approve** or ask for changes |

Visual projects get a "design screens (design-first)" task before layout; AI projects get a system-prompt task and AI behavior checks; Telegram projects on a server where Telegram is blocked get a bridge/proxy task.

**Output:** `docs/blueprint.md` with tech stack, structure, data model, deploy plan, task checklist, and acceptance criteria.

**Gate:** Stack approved, 3–15 tasks, 5+ checks, data described, no contradictions with vision.

**After gate:** Updates the project's `CLAUDE.md` with description, stack, boundaries (Always / Ask First / Never), and a rule to always check `docs/blueprint.md` before starting work — so Claude in any future session knows the plan.

---

## Key features

- **Retrospective mode.** Already have code but no docs? The skill analyzes your codebase first, drafts answers, and asks you to confirm — then proceeds with the standard flow.
- **Anti-pattern detection.** Watches for scope creep ("one more feature"), vague requirements ("make it work"), and deferred decisions ("we'll figure it out later") — and responds immediately.
- **Gate skip mechanism.** If you insist on skipping a gate, the skill records it as a risk with `[GATE SKIP]` — doesn't block you, but doesn't let you forget.
- **Session continuity.** The generated docs + CLAUDE.md update mean Claude in a new session can pick up exactly where you left off.
- **Need / Nice / Later prioritization.** v1 scope isn't a flat list — each feature is tagged so you know what to cut first if scope needs trimming.
- **Visible assumptions.** Everything Claude decided without asking lands in an "assumptions" section of both docs.

- **Concept page (optional).** At the end Claude offers to open the concept as a styled local page: `docs/concept.html`, built from a fixed template (`assets/concept.html`, light theme, full-width responsive grid) with links to `vision.md` and `blueprint.md`. Say no, and everything stays in the chat.

## Works with

- Not sure the idea is worth building? Run `product-check` first.
- No idea yet, just an itch? Brainstorm first (`idea-storm`).
- Screens to design? The plan hands off to `design-first` before layout.

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

Install as a skill (it auto-triggers on project ideas and also works as `/spec-first`). Two files: the instructions and the concept page template.

macOS / Linux:
```bash
mkdir -p ~/.claude/skills/spec-first/assets
curl --fail -o ~/.claude/skills/spec-first/SKILL.md \
  https://raw.githubusercontent.com/GuruDevvv/my-claude-skills/main/mine/spec-first/SKILL.md
curl --fail -o ~/.claude/skills/spec-first/assets/concept.html \
  https://raw.githubusercontent.com/GuruDevvv/my-claude-skills/main/mine/spec-first/assets/concept.html
```

Windows (Git Bash or WSL):
```bash
mkdir -p "$USERPROFILE/.claude/skills/spec-first/assets"
curl --fail -o "$USERPROFILE/.claude/skills/spec-first/SKILL.md" \
  https://raw.githubusercontent.com/GuruDevvv/my-claude-skills/main/mine/spec-first/SKILL.md
curl --fail -o "$USERPROFILE/.claude/skills/spec-first/assets/concept.html" \
  https://raw.githubusercontent.com/GuruDevvv/my-claude-skills/main/mine/spec-first/assets/concept.html
```

Restart your Claude Code session — the terminal running `claude`, or reload the VS Code window.

**Verify:** type `/spec-first` or describe a new project idea — the skill activates automatically.
