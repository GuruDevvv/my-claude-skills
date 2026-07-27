# ppt-creator

Slide decks: structure, charts, speaker notes.

## The one thing it gets right

Slide headings must be **assertions, not labels**. Not "Results" but "Conversion doubled after the
hero rewrite" — and the rest of the slide is the evidence for that sentence. Underneath it: conclusion
first, then three to five reasons, then facts. One idea per slide, five bullets maximum.

## How it runs

Ten intake questions (audience, goal, the action you want afterwards, length). No answer twice and it
takes sensible defaults **while writing down what it assumed**. Then a 12-15 slide skeleton, a chart
type chosen per point from a selection dictionary, contrast and font sizes checked against
accessibility rules, and 45-60 second speaker notes per slide (open, assertion, evidence, transition).

Then it **grades itself** against a rubric. Below 75 it finds the three weakest items, fixes them and
re-scores, up to twice.

Output: Markdown slides, chart PNGs, notes, sources, and a .pptx where possible.

## Caveats

One of its two .pptx export paths wants the `document-skills` plugin; without it the python-pptx path
is used. Writes to `/output/`.

## Source

**Not my work.** By daymade — [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills), `daymade-docs/ppt-creator/`

MIT. Full licence text: [`../licenses/`](../licenses/). Prefer installing from upstream — that copy is maintained, this one is a snapshot.
