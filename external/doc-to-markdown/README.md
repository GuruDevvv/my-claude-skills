# doc-to-markdown

DOCX / PDF / PPTX / XLSX to clean Markdown, with tables and images intact.

## When to use

Any time a document has to become text an agent can actually read: a contract, a spec, a slide deck,
a report.

## What's inside

Two modes — **quick** (one tool, seconds) and **heavy** (several converters in parallel, then the best
version of each segment wins: the table with more rows and a real header, the image that kept its
caption). Then eight automatic repairs on pandoc output: broken grid tables, doubled image paths,
leftover attribute noise, mangled links, indented code blocks.

Ships a benchmark against Docling, MarkItDown, raw Pandoc and Mammoth.

## Requirements

`uv` and `pandoc` on PATH. Python dependencies resolve on first run.

## Patched — this is not upstream

`scripts/convert.py` asks pandoc for a different Markdown flavour than upstream:

```
-t markdown-simple_tables-multiline_tables-grid_tables   # upstream: -t markdown
```

**Why.** With plain `-t markdown` pandoc draws simple dash-underlined tables, and the skill's own
post-processing then turns them into a blockquote plus loose lines — *worse* than untouched pandoc
output. Reproduced on an ordinary 3x3 table in a Russian .docx.

Two other flavours were tried and rejected: `markdown-simple_tables-multiline_tables` yields grid
tables that the grid-repair pass splits into several empty ones; `gfm` fixes tables but breaks images
into raw `<figure>` HTML with a doubled path.

After the patch a table, bold, italics, lists and a captioned image all survive, and the skill's own
31 tests still pass.

## Source

**Not my work.** By daymade — [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills), `daymade-docs/doc-to-markdown/`

MIT. Full licence text: [`../licenses/`](../licenses/). Prefer installing from upstream — that copy is maintained, this one is a snapshot.
