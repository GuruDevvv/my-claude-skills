# mermaid-tools

Pulls Mermaid diagrams out of a Markdown file and renders them to high-resolution PNG.

## When to use

When a diagram has to live somewhere that does not render Mermaid — a Word document, a slide, a PDF,
a Telegram message. Chat and artifacts render it natively; everything else shows raw code.

## What's inside

One command per file: every diagram extracted in order, numbered 01, 02, ..., saved beside its source
along with the diagram code. Size and scale are configurable, with presets for presentation and print
(4-5x scale).

## Requirements

`npm install -g @mermaid-js/mermaid-cli` — a one-off, and it pulls its own browser (~150 MB).

## Patched — this is not upstream

Upstream `scripts/extract-and-generate.sh` hard-requires Chrome at `/usr/bin/google-chrome-stable`
(a WSL2/Ubuntu path) and exits if it is absent — so it never ran on Windows, even though the renderer
itself works there fine.

Now, if that path does not exist, `PUPPETEER_EXECUTABLE_PATH` is simply not set and mermaid-cli falls
back to its own bundled browser. Verified on Windows, including Cyrillic labels.

## Source

**Not my work.** By daymade — [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills), `daymade-docs/mermaid-tools/`

MIT. Full licence text: [`../licenses/`](../licenses/). Prefer installing from upstream — that copy is maintained, this one is a snapshot.
