# skill-conductor

The lifecycle of a skill itself: design, build, test, evaluate, package.

## When to use

Writing a new skill, fixing one that will not trigger, testing one, reviewing someone else's, or
bundling one for distribution.

## What's inside — six modes

| Mode | For |
|------|-----|
| CREATE | new skill: intent, architecture, scaffold, write, test |
| IMPROVE | it exists but misbehaves: diagnose, eval loop, blind comparison |
| VALIDATE | structural checks, trigger testing, scoring |
| REVIEW | 11-point quality gate, aimed at third-party skills |
| OPTIMIZE | description tuning with a train/test split, so it triggers when it should |
| PACKAGE | validate and bundle |

Its point of view: choose the architecture **before** writing SKILL.md, because rewriting the wrong
pattern costs more than picking the right one. Evaluation is a blind A/B between versions with grader,
comparator and analyser agents rather than a self-assessed score.

## Caveats

Meta-tooling — worth having only if you actually author skills.

## Source

**Not my work.** By smixs — [smixs/skill-conductor](https://github.com/smixs/skill-conductor)

MIT. Full licence text: [`../licenses/`](../licenses/). Prefer installing from upstream — that copy is maintained, this one is a snapshot.
