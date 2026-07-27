# meeting-minutes-taker

Turns a raw call transcript into real minutes: decisions, action items with owners, open questions.

## Why not just ask for a summary

**It does not lose content.** A summary compresses and drops. This makes several independent passes
and **merges** them rather than picking a winner, then runs a separate completeness check against the
source: what did not make it in?

**It is honest about who spoke.** Faced with "Speaker 1 / Speaker 2" it first stops and asks you to
label the speakers in the recording platform and re-export — because there a human matched actual
voices, whereas text-only inference can only resolve people who happen to get named aloud. Only if
that is impossible does it infer, from talk time, turn length, style and topic, and then it presents
the mapping **with evidence and a confidence level**. It never assigns a name silently.

**Every decision carries a quote** from the transcript, so it can be checked.

Also: suggests a filename, merges multiple versions of minutes without loss, audits existing minutes
against the source.

## Caveats

Examples are Chinese (Feishu, Tencent Meeting) — the logic transfers, the flavour shows. It does not
transcribe; bring a transcript.

## Source

**Not my work.** By daymade — [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills), `daymade-audio/meeting-minutes-taker/`

MIT. Full licence text: [`../licenses/`](../licenses/). Prefer installing from upstream — that copy is maintained, this one is a snapshot.
