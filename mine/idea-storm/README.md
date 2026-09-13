# idea-storm

Rails for thinking an idea through, so the outcome does not depend on how inspired the
conversation happened to be.

## The problem

Ask a model to brainstorm and you get the centre of the distribution: three sensible options
any advisor would have named, dressed in confident language. Asking it to "be bolder" changes
the adjectives, not the options.

The manual workaround most people land on is a second chat. Paste a cold brief into a fresh
window and read what a model says when it has not watched you fall in love with your idea.
The gap between the two answers is where the real uncertainty sits. It works — but it is
hand-run, unrepeatable, and it dies the moment you are tired.

This skill turns that ritual into a procedure, and makes the model's own critic blind by
construction rather than by copy-paste.

## How it runs

Five phases. Each one closes on a checkable output, not on a feeling that enough was said.

| Phase | What happens | Gate |
|-------|--------------|------|
| **Frame** | Four questions in one block: what is at stake, what "it worked" looks like in 6–12 months, what is off the table, deadline and cost of being wrong | A 4–8 line frame, confirmed |
| **Diverge** | Nine options on three shelves — Consensus, Shift, **Heresy** — each with its action and the assumption it rests on | Heresy shelf full; no two options die from the same fact |
| **Narrow** | Five axes: stake, horizon, reversibility, load-bearing assumption, asymmetry. Then three finalists, each with a killing question | At least one finalist is not from the Consensus shelf |
| **Shoot** | A clean brief goes to two independent reviewers in parallel, with a deliberately weak option planted among the finalists | Two answers in fixed form, plus the control result |
| **Decide** | One decision, one action for the next seven days, the sign that kills it, the date it gets checked | No death sign and no date means it is an intention, not a decision |

Everything is written to one artifact — including the six options that did not make the cut,
which is what you actually want when you come back to this in a month.

## The three mechanics that make it repeatable

**A quota on risk.** The consensus answer is kept deliberately, as a baseline to compare
against, and then the Heresy shelf has to be filled before the phase can close. An option
qualifies as heresy only if it contradicts something the owner said in the Frame, or if anyone
in the field would call it wrong — not merely because it is riskier. Riskier is not different
logic. Seven unsticking techniques do the work: inversion, borrowed self-interest, discarding
the first three answers, scale swaps, transfer from a higher-stakes industry, a note written
from two years in the future, and a ban on the strongest resource available.

**Blind review.** The critic sees a one-page brief with the discussion stripped out: no history,
no favourite, no authorship, finalists shuffled. Two reviewers run in parallel — a fresh
subagent with no conversation memory, and Codex, a different model family, for a second optics.
Both answer in the same fixed shape: pick one, name the single fact that kills each option,
name what the brief is missing, propose a better move if there is one, rank everything.

**A negative control.** One of the finalists sent for review is a plant — plausible in form,
hollow in substance. If a reviewer ranks it anywhere but last, that reviewer is not
discriminating and its verdict is thrown out, loudly. Without this, "both of them agreed" is
worth nothing.

And one rule that follows from all three: **disagreement is the finding.** Where the two
reviewers split, name the fact that split them — that is the cheap experiment for the week.
Where they agree, say plainly that a shared brief can produce a shared error.

## Modes and cost

Read off the cost of being wrong, not asked about separately:

- **reversible and cheap** → fast mode: six options, one reviewer, about fifteen minutes;
- **expensive or irreversible** → full mode: nine options, both reviewers, about an hour.

The Codex reviewer is optional. Without it the skill runs with one reviewer and says so —
narrowing the check silently is the one thing it must not do. Measured on a live run: one
Codex review cost roughly 11.7k tokens and correctly ranked the planted option last.

## Install

```bash
cp -r mine/idea-storm ~/.claude/skills/idea-storm
```

Restart Claude Code. Optional: `commands/storm.md` from this repo's owner's setup gives a
`/storm` shortcut; the skill triggers on its own from phrases like "help me decide",
"what are my options", "push back on this".

## Not for

Designing code or features — that is a coding brainstorm. Scoring an idea that already exists
and only needs a go/no-go — that is `product-check`. Gathering facts about a market — that is
`deep-research`, and if the storm stalls for lack of numbers it will stop and say so rather
than invent them. Writing the spec afterwards — `spec-first`.

---

🇷🇺 **Штурм идеи по рельсам.** Пять шагов, у каждого проверяемый выход: рамка → девять
вариантов по трём полкам, где полка «Ересь» обязательна → три финалиста по пяти осям →
слепая проверка двумя независимыми рецензентами → решение с первым шагом, признаком провала
и датой.

Главное здесь — чистый бриф: рецензент не видит обсуждения и не знает, какой вариант нравится
автору. Это машинный аналог переноса задачи во второй чат, откуда и берётся объективность.
Плюс подсадной вариант-пустышка: похвалил его рецензент — значит, прибор не различает, и его
вердикт не считается.

Разногласие рецензентов ценнее их согласия: там, где они разошлись, лежит настоящая
неопределённость — она и становится дешёвым опытом на неделю.
