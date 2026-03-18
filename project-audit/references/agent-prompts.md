# Agent Prompts for Full Audit Mode

Reference file for project-audit skill v2. Contains prompts for 5 parallel agents dispatched in Full mode.

---

## Common Context Block

Every agent receives this block at the top of its prompt, filled in by the orchestrator from recon results:

```
RECON RESULTS:
- Project: [name]
- Type: [code/product/docs/mixed]
- Git: [yes/no]
- CLAUDE.md locations: [paths]
- Memory path: [path or none]
- Files: ~N
- Root contents: [ls output, first 20 lines]
- CLAUDE.md: [content, first 100 lines]
```

---

## Common Output Format

Every agent MUST end its response with exactly this format:

```
FINDINGS:
- [severity] [finding description]
- ...

ALL CLEAR:
- [what was checked and found healthy]
```

Severity levels (use exactly these):
- `🔴 Critical` — must fix, blocks quality or safety
- `⚠️ Warning` — should fix, notable problem
- `🟢 Low` — minor, nice to fix

Rules:
- At least one section must be non-empty.
- If nothing is wrong, FINDINGS can be empty but ALL CLEAR must list what you checked.
- If everything is wrong, ALL CLEAR can be empty.
- Each finding is one line. Be specific: include file paths, counts, examples.

---

## Common Safety Rules

Every agent MUST follow these rules:

1. **Never read secret files.** Do not open `.env`, `*.pem`, `*.key`, `*secret*`, `credentials*`. Note their existence and size only.
2. **Redact secrets.** If you spot a token or key in any file, write `[SECRET hidden]` in your output. Never reproduce it.
3. **Limit large output.** Pipe any command that may produce large output through `| head -30`.
4. **Skip binary files.** Do not read PDFs, DOCX, images, archives. Note filename and size only.
5. **Search secrets by filename, not content.** Use `git ls-files | grep -iE '\.env|\.pem'` — never grep file contents for secrets.

---

## Agent 1 — CLAUDE.md Audit

```
You are auditing the CLAUDE.md file(s) of a project.

{COMMON_CONTEXT_BLOCK}

## Your Task

### Step 1: Try the specialized skill

Try to invoke the `claude-md-improver` skill via the Skill tool.
- If it runs successfully, integrate its findings into your output.
- If it is not available (error or not found), tell the user:
  "Skill `claude-md-improver` not installed (it provides detailed CLAUDE.md analysis and improvement suggestions). Running manual check."
  Then proceed to Step 2.

### Step 2: Manual fallback check

Use the checklist from `references/checklists.md`, section "CLAUDE.md checklist":

1. **Project description** — Is there a clear 1-2 sentence explanation of what this project is?
2. **Folder structure** — Is a directory tree or structure section present? Does it match reality?
   - Run `ls` on the actual directories mentioned. Flag mismatches.
3. **File references** — Check that paths mentioned in CLAUDE.md actually exist. Use Glob to verify.
4. **Freshness** — Look for dates >6 months old, outdated URLs, stale version numbers.
5. **Duplication with MEMORY.md** — Same info in both places? Flag it.
6. **Empty sections** — Headings with no content, TODO placeholders, "TBD" markers.
7. **Sensitive data** — API keys, tokens, passwords visible in CLAUDE.md. Flag as `[SECRET found in CLAUDE.md]`.
8. **Instructions quality** — Are instructions specific enough for Claude to follow?

### Step 3: Apply project-type severity

Read `references/project-type-checklists.md`, section "Severity Modifiers Table".
Adjust severity of your findings based on the project type from recon. For example:
- Broken links in CLAUDE.md: Warning for code projects, Critical for product/docs projects.
- No README/entry point: Warning for code, Critical for product/docs.

### Safety Rules

{COMMON_SAFETY_RULES}

### Output

{COMMON_OUTPUT_FORMAT}
```

---

## Agent 2 — Memory Audit

```
You are auditing the Claude Code memory system of a project.

{COMMON_CONTEXT_BLOCK}

## Pre-check

If the recon shows "Memory path: none" — skip the audit entirely and return:

FINDINGS:
- (none — no memory system found)

ALL CLEAR:
- Memory audit skipped: no MEMORY.md or memory directory detected.

## Your Task

Use the checklist from `references/checklists.md`, section "Memory checklist".

### MEMORY.md index
- Read MEMORY.md.
- Is it organized by topic (not chronologically)?
- Is it under ~200 lines? (Longer gets truncated by Claude Code)
- Are descriptions brief and useful for relevance matching?

### Link integrity (first-level only)
- For every link in MEMORY.md, check if the target file exists. Use Glob or Read.
- Only check first-level links (links directly in MEMORY.md), not links inside linked files.
- Flag broken links.

### Orphan detection
- List all files in the memory directory.
- Compare against links in MEMORY.md.
- Files not referenced from MEMORY.md are orphans. Flag them.

### Individual memory files
- For each linked memory file, check:
  - **Frontmatter** — does it have `name`, `description`, `type` fields?
  - **Staleness** — does the content reference files or facts that no longer exist?
  - **References** — if the memory mentions specific project files, do those files still exist?

### Cross-checks
- **CLAUDE.md overlap** — Is the same information duplicated in both CLAUDE.md and memory? Flag it.
- **Zombie references** — Memory files that reference deleted/moved project resources.

### Safety Rules

{COMMON_SAFETY_RULES}

### Output

{COMMON_OUTPUT_FORMAT}
```

---

## Agent 3 — Architecture + File Structure

```
You are auditing the architecture and file structure of a project.

{COMMON_CONTEXT_BLOCK}

## Your Task

### Step 1: Identify project type checklist

Read `references/project-type-checklists.md`. Based on the project type from recon, use the matching checklist:
- Code → section "Code Project Checklist"
- Product/Business → section "Product/Business Project Checklist"
- Documentation → section "Documentation Project Checklist"
- Mixed → apply both Code and Product/Business checklists

### Step 2: Deep architecture scan

Do NOT stop at 2 levels. Explore the full directory tree to understand the project structure.

Use `ls -la` on key directories (pipe through `| head -30` if output is large).
Use Glob patterns like `**/*.md`, `**/*.py`, `**/*.ts` to understand what's in the project.

For each zone in the applicable checklist, check whether the project covers it:
- Note what exists and what's missing.
- Note structural oddities (e.g., code scattered in root, configs mixed with source).

### Step 3: File hygiene

Use the checklist from `references/checklists.md`, section "File structure checklist".

**Root directory:**
- Identify files in root that don't belong there (data files, HTML pages, images, random scripts).
- Don't flag standard root files (README, CLAUDE.md, package.json, .gitignore, etc.).

**Directory hygiene:**
- Empty directories (no files at all)
- Deeply nested single-file directories (3+ levels for one file)
- Temporary files: `.tmp`, `.bak`, `~`, `.swp`
- Duplicate-pattern files: `file (1).txt`, `file-copy.txt`, `file_old.txt`
- OS junk: `.DS_Store`, `Thumbs.db`, `desktop.ini`

**Size:**
- Files >1MB — should they be in git?
- Files >10MB — almost certainly shouldn't be tracked

### Step 4: Apply severity modifiers

Read `references/project-type-checklists.md`, section "Severity Modifiers Table".
Calibrate severity based on project type. For mixed projects, apply both checklists and take the highest severity.

### Safety Rules

{COMMON_SAFETY_RULES}

### Output

{COMMON_OUTPUT_FORMAT}
```

---

## Agent 4 — Git Hygiene

```
You are auditing the git hygiene of a project.

{COMMON_CONTEXT_BLOCK}

## Pre-check

If the recon shows "Git: no" — skip the audit entirely and return:

FINDINGS:
- (none — not a git repository)

ALL CLEAR:
- Git audit skipped: project is not a git repository.

## Your Task

Use the checklist from `references/checklists.md`, section "Git checklist".

### Git status
```bash
git status | head -30
```
- How many untracked files?
- How many modified files?
- Any staged but uncommitted changes?
- Is the working tree clean?

### Binary files in git
```bash
git ls-files | grep -iE '\.(png|jpg|jpeg|gif|svg|ico|pdf|docx|xlsx|zip|tar|gz|mp3|mp4|woff|ttf|eot)$' | head -30
```
- Flag tracked binary files. Suggest Git LFS or .gitignore.
- For docs/product projects, lower severity (images in docs are normal).

### Secrets by filename pattern
```bash
git ls-files | grep -iE '\.env|\.pem|\.key|secret|credential|\.pfx|\.p12' | head -30
```
- IMPORTANT: search by filename only, NEVER read the file contents.
- Flag any matches as 🔴 Critical.
- Note: `.env.example` files are acceptable (they should not contain real values, but do NOT open to verify).

### .gitignore coverage
- Does `.gitignore` exist? If not → flag based on project type severity.
- Read `.gitignore` and compare against expected patterns for the project type:
  - JavaScript/TypeScript: node_modules/, dist/, .next/, .env*, *.log
  - Python: __pycache__/, *.pyc, .env*, venv/, .venv/
  - General: .DS_Store, Thumbs.db, *.log, .env
- Flag missing patterns.

### Recent commit history
```bash
git log --oneline -10
```
- Note any concerning patterns (e.g., "fix fix fix", secrets-related commits).
- This is informational, not a finding unless something is clearly wrong.

### Safety Rules

{COMMON_SAFETY_RULES}

### Output

{COMMON_OUTPUT_FORMAT}
```

---

## Agent 5 — Claude Code Automations

```
You are auditing the Claude Code automations (hooks, MCP servers, settings) of a project.

{COMMON_CONTEXT_BLOCK}

## Your Task

### Step 1: Try the specialized skill

Try to invoke the `claude-automation-recommender` skill via the Skill tool.
- If it runs successfully, integrate its findings into your output.
- If it is not available (error or not found), tell the user:
  "Skill `claude-automation-recommender` not installed (it analyzes Claude Code setup and suggests automations). Running manual check."
  Then proceed to Step 2.

### Step 2: Manual fallback check

Use the checklist from `references/checklists.md`, section "Automations checklist".

**Hooks:**
```bash
cat .claude/settings.local.json 2>/dev/null | head -30
cat .claude/settings.json 2>/dev/null | head -30
```
- Are there pre/post commit hooks?
- For code projects: is there a linting hook? formatting hook?
- Are hook paths valid (no dead references)?

**MCP servers:**
- Check if any MCP servers are configured in settings.
- For the project type, would any be useful? (Don't recommend if unclear benefit.)

**Settings:**
- Does `.claude/settings.local.json` exist?
- Are there stale paths or dead references in it?
- Are permissions appropriate?

### Step 3: Project-type-specific recommendations

IMPORTANT: Tailor recommendations to the project type from recon.

**Code projects** (has package.json / requirements.txt / etc.):
- Pre-commit hooks for linting/formatting
- Test runner integration
- CI pipeline if deploying

**Documentation projects** (mostly .md/.html/.txt):
- Do NOT recommend linters, formatters, or test runners — they add noise for docs projects.
- Focus on: link checking, structure validation, freshness monitoring.
- Spell checking only if project is user-facing.

**Product/Business projects:**
- Same as documentation: no linters/CI.
- Focus on: data validation, dashboard freshness, link integrity.

**Mixed projects:**
- Split recommendations: code tooling for code parts, structure tools for docs parts.

### Safety Rules

{COMMON_SAFETY_RULES}

### Output

{COMMON_OUTPUT_FORMAT}
```

---

## Template Substitution Reference

When the orchestrator builds the actual prompt for each agent, it replaces:

| Placeholder | Replaced with |
|-------------|---------------|
| `{COMMON_CONTEXT_BLOCK}` | The filled-in recon results block from the top of this file |
| `{COMMON_SAFETY_RULES}` | The 5 safety rules listed in the "Common Safety Rules" section |
| `{COMMON_OUTPUT_FORMAT}` | The FINDINGS + ALL CLEAR format from "Common Output Format" section |
