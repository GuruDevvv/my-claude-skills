# video-by-code

A short vertical video for Reels, Shorts or Telegram, made by the agent in code. No editing app,
no paid service, no stock footage.

## When to use

You want an explainer, a promo or a "SaaS-style" motion piece — interface cards sliding in,
commands typing themselves out, a progress bar across the steps — or a dramatic cut-down from an
existing video: the hero's frames, a colour grade with grain and flicker, statements fading in
over the picture. Typical length 30–75 seconds.

## What it does

Two recipes, both deterministic: the same code gives the same video, and one scene can be fixed
without re-making the rest.

- **Canvas animation** (`templates/canvas/`). Every frame is a function of time drawn on an HTML
  canvas. Playwright drives a headless Chromium frame by frame and pipes PNGs into ffmpeg. Fonts are
  loaded explicitly, so the render matches the live preview in the browser.
- **Cut-down** (`templates/cutdown/`). A JSON plan of scenes (timestamp, text, accent line); one
  Python script builds an ffmpeg filter chain per scene — 9:16 crop, grade, flicker by formula,
  grain, text from files so quotes never break the command, a plate under the text — and joins
  the scenes.
- **Sound in code.** For the canvas, a Web Audio score rendered offline: chords from detuned saws
  through a filter, a kick from a falling sine, hats and scene-change whooshes from noise, all
  placed on the timeline. For the cut-down, ffmpeg `aevalsrc` formulas: a beating drone and a
  heartbeat. Both are normalised to −14 LUFS.

The agent runs it in three check-ins — script, look (a preview sheet of frames), all scenes — and
checks the result before handing it over: one frame per second on a contact sheet, black-frame
detection, loudness.

```bash
cp -r templates/canvas my-video && cd my-video
npm init -y && npm i playwright && npx playwright install chromium
node render.mjs --sheet      # preview: first frame + middle of every scene
node render.mjs              # out.mp4
```

[assets/example.mp4](assets/example.mp4) is the canvas template rendered as it ships (17 s).

## Not for

Illustrated or hand-drawn styles — cut paper, ink, pixel art, riso — that is
[`animate`](https://github.com/cth9191/animate) by cth9191, which this skill borrows its core idea
from. Editing a talking-head take is [`reels-console`](../reels-console/). There is no voice by
default; an optional step in `SKILL.md` adds text-to-speech and ducks the music under it.

## Needs

Node 18+, ffmpeg and ffprobe on PATH, `playwright` with its Chromium for the canvas recipe, Python
3.9+ for the cut-down. Internet for Google Fonts at render time (otherwise a system font and a
warning). `SKILL.md` has install commands for Windows, macOS and Linux.

## Honest about maturity

Built and checked on Windows: a clean install from the instructions, both recipes rendered, frame
sheets reviewed, loudness measured. Not yet run on macOS, and not yet in the hands of other
people's agents. The agent cannot hear the sound — it measures the level and says so.

🇷🇺 Инструкция для агента (`SKILL.md`) — на русском.
