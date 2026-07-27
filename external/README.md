# external/ — skills I did not write

**Nothing in this folder is mine.** These are third-party skills I use daily, vendored here so my
setup is reproducible from one repo. Every one of them is MIT-licensed, and every original license
text is kept verbatim in [`licenses/`](licenses/).

If you want any of these skills, **get them from the source repo below, not from here** — upstream
is maintained, this copy is a snapshot.

---

## Attribution

| Skill | Author | Source | License |
|-------|--------|--------|---------|
| [pricing](pricing/) | Corey Haines | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) → `pricing/` | MIT |
| [marketing-plan](marketing-plan/) | Corey Haines | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) → `marketing-plan/` | MIT |
| [site-architecture](site-architecture/) | Corey Haines | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) → `site-architecture/` | MIT |
| [negotiation](negotiation/) | Wondel.ai sp. z o.o. | [wondelai/skills](https://github.com/wondelai/skills) → `negotiation/` | MIT |
| [high-output-management](high-output-management/) | Wondel.ai sp. z o.o. | [wondelai/skills](https://github.com/wondelai/skills) → `high-output-management/` | MIT |
| [doc-to-markdown](doc-to-markdown/) | daymade | [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills) → `daymade-docs/doc-to-markdown/` | MIT |
| [mermaid-tools](mermaid-tools/) | daymade | [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills) → `daymade-docs/mermaid-tools/` | MIT |
| [ppt-creator](ppt-creator/) | daymade | [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills) → `daymade-docs/ppt-creator/` | MIT |
| [meeting-minutes-taker](meeting-minutes-taker/) | daymade | [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills) → `daymade-audio/meeting-minutes-taker/` | MIT |
| [youtube-downloader](youtube-downloader/) | daymade | [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills) → `youtube-downloader/` | MIT |
| [ui-ux-pro-max](ui-ux-pro-max/) | nextlevelbuilder | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT |
| [skill-conductor](skill-conductor/) | smixs | [smixs/skill-conductor](https://github.com/smixs/skill-conductor) | MIT |

Every upstream repo and license above was verified against the GitHub API on 2026-07-27, not guessed
from filenames.

---

## Deliberately NOT vendored here

**`remotion-best-practices`** (by the Remotion team, [remotion-dev/skills](https://github.com/remotion-dev/skills))
is excellent and I use it locally — but that repository ships **no license file at all**, which means
default copyright: all rights reserved. Redistributing it would not be legal, so it is not in this
folder. Install it from the source.

---

## Local modifications

Two skills are **not byte-identical to upstream** — both were broken on Windows and I patched them.
Each patch is documented at the top of that skill's `README.md`:

- **`doc-to-markdown`** — changed the pandoc output flavour so tables survive. Upstream asks pandoc
  for "simple" dash-drawn tables, and the skill's own post-processing then mangles them into a
  blockquote — worse than raw pandoc. Verified on a plain 3×3 table in a Russian .docx.
- **`mermaid-tools`** — upstream hardcodes Chrome at `/usr/bin/google-chrome-stable` (a WSL2/Ubuntu
  path) and exits if it is missing. Now it falls back to the browser bundled with `mermaid-cli`,
  which is what makes it run on Windows at all.

Both patches were sent nowhere upstream (yet). If you pull these, know you are getting my fork.

---

## Russian

Внутри большинства этих скиллов лежит файл `КАК_ИСПОЛЬЗОВАТЬ.md` — короткое описание на русском:
что делает, как звать, пример фразы. Он от сборщика русскоязычной подборки, не от авторов скиллов.
