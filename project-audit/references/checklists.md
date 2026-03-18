# Fallback Checklists

Used as fallbacks in both **Quick mode** (always — Quick does not delegate to companion skills) and **Full mode** (when the companion skill is not installed). Each section maps to a specific audit step or agent.

---

## CLAUDE.md checklist

Read each CLAUDE.md found in the project. For each one:

1. **Project description** — Is there a clear 1-2 sentence explanation of what this project is?
2. **Folder structure** — Is a directory tree or structure section present? Does it match reality?
   - Run `ls` on the actual directories mentioned. Flag mismatches.
   - Example finding: "CLAUDE.md documents `src/components/` but that directory doesn't exist"
3. **File references** — Check that paths mentioned in CLAUDE.md actually exist.
   - Use Glob to verify: `docs/api.md` → does it exist?
   - Example finding: "Link to `docs/setup-guide.md` — file not found"
4. **Freshness** — Look for dates, version numbers, URLs that seem outdated.
   - Dates >6 months old in status sections
   - URLs to services that may have moved
5. **Duplication with MEMORY.md** — Same info in both places? Flag it — it will drift.
6. **Empty sections** — Headings with no content, TODO placeholders, "TBD" markers.
7. **Sensitive data** — API keys, tokens, passwords. Flag as `[SECRET found in CLAUDE.md]`.
8. **Instructions quality** — Are the instructions specific enough for Claude to follow? Vague instructions like "be careful" don't help.

---

## Automations checklist

Check what Claude Code automations exist and what's missing.

### Hooks
```bash
# Check for hook configurations
cat .claude/settings.local.json 2>/dev/null | head -30
cat .claude/settings.json 2>/dev/null | head -30
```
- Are there pre/post commit hooks?
- For code projects: is there a linting hook? formatting hook?
- Are hook paths valid (no dead references)?

### MCP servers
- Check if any MCP servers are configured in settings
- For the project type, would any be useful? (Don't recommend if unclear benefit)

### Settings
- Does `.claude/settings.local.json` exist?
- Are there stale paths or dead references in it?
- Are permissions appropriate?

### Project-type-specific recommendations

**Code projects** (has package.json / requirements.txt / etc.):
- Pre-commit hooks for linting/formatting
- Test runner integration
- CI pipeline if deploying

**Documentation projects** (mostly .md/.html/.txt):
- Don't recommend linters, formatters, or test runners — they add noise
- Focus on: link checking, structure validation, freshness monitoring
- Spell checking only if project is user-facing

**Mixed projects:**
- Split recommendations: code tooling for code parts, structure tools for docs

---

## File structure checklist

### Root directory
Standard root files (don't flag these):
- README.md, CLAUDE.md, LICENSE, CONTRIBUTING.md
- package.json, requirements.txt, go.mod, Cargo.toml, pyproject.toml
- .gitignore, .editorconfig, .prettierrc, tsconfig.json
- Makefile, Dockerfile, docker-compose.yml
- vercel.json, netlify.toml, .env.example

Flag these in root (they belong in subdirectories):
- Data files (.csv, .json with data, .xlsx)
- HTML pages (unless it's a static site root)
- Images, PDFs, documents
- Scripts that aren't project-level (random .py, .sh)

### Directory hygiene
- Empty directories (no files at all)
- Deeply nested single-file directories (3+ levels for one file)
- Temporary files: `.tmp`, `.bak`, `~`, `.swp`
- Duplicate-pattern files: `file (1).txt`, `file-copy.txt`, `file_old.txt`
- OS junk: `.DS_Store`, `Thumbs.db`, `desktop.ini`
- IDE artifacts: `.idea/` with non-standard contents, `.vscode/` committed without team agreement, `*.swp`

### Size
- Files >1MB — should they be in git? Or in .gitignore?
- Files >10MB — almost certainly shouldn't be tracked

---

## Memory checklist

### MEMORY.md index
- Is it well-organized (by topic, not chronologically)?
- Does it stay under ~200 lines? (Longer gets truncated by Claude Code)
- Are descriptions brief and useful for future relevance matching?

### Individual memory files
- **Frontmatter** — must have `name`, `description`, `type` fields:
  ```yaml
  ---
  name: example-memory
  description: One-line description used for relevance matching
  type: user|feedback|project|reference
  ---
  ```
- **Content** — is it still accurate? Check key claims against current project state.
- **References** — if the memory mentions specific files, do those files still exist?

### Cross-checks
- **Orphans**: files in `memory/` not linked from MEMORY.md
- **Broken links**: MEMORY.md links to files that don't exist
- **Duplicates**: same information in multiple memory files
- **CLAUDE.md overlap**: information that's both in CLAUDE.md and memory

---

## Git checklist

### .gitignore coverage by project type

**JavaScript/TypeScript:**
```
node_modules/
dist/
.next/
.env*
*.log
.DS_Store
```

**Python:**
```
__pycache__/
*.pyc
.env*
venv/
.venv/
*.egg-info/
dist/
build/
```

**General (all projects):**
```
.DS_Store
Thumbs.db
*.log
.env
.env.*
```

### What to flag
- Tracked binary files (images, PDFs, archives) — suggest Git LFS or .gitignore
- Tracked secret files (.env, *.pem, *.key) — Critical severity
- Large untracked files that should be ignored
- Missing .gitignore entirely — Critical severity
