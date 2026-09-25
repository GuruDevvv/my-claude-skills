# Imagery — sourcing real images autonomously (and when not to)

Real images are a major wow lever. But two hard constraints:

1. **The source must actually work.** (Pollinations' no-key path is dead — returns `402 Queue full`. Do not use it.)
2. **No binding to anyone's account/spec.** The skill is portable; it must not require the author's paid subscription, an API key the user doesn't have, or any project-specific service.

## When NOT to use images (decide this first)

- **Data dashboards, dense tools, admin panels** → no hero photos. Stock images look pasted-on. Do the work with typography, color, data hierarchy, and functional motion.
- **When a photo would dilute a pure-type/editorial concept.**

Whether a variant has an image at all is decided by its direction (a type-led poster or a concept screen may need none). If it does, use the cascade.

## The autonomous cascade (pick the highest tier available)

### Tier A — bespoke generation (best quality, only if a generator is present)
**The default whenever a direction calls for an image.** Use whatever image tool the environment has (Codex CLI `image_gen`, an image MCP, DALL·E…) — confirm it works with one call, never assume a specific vendor. Save the file locally to `assets/` so the prototype stays standalone.

**Build the prompt from the vibe card**, not from a generic subject:
```
<subject and action>, <who: age, look — from the audience read>, <light: source, warmth>,
<palette of the variant>, <crop, and empty area on the LEFT/RIGHT/TOP for the headline>,
photographic | illustration in <manner>. NO text, letters, logos or watermarks.
```
Look at the result before using it: light, pose, crop and text space must match the direction; a
wrong mood is worse than no image.
*Codex CLI specifics:* start the prompt with "ИСПОЛЬЗУЙ СВОЙ ВСТРОЕННЫЙ ИНСТРУМЕНТ image_gen … Сгенерируй изображение: …"; it may fail to copy the file and print a path under `~/.codex/generated_images/` instead — take **that exact path**, never "the newest file" (parallel runs collide).

### Tier B — Openverse (free, no key, keyword search) — fallback when no generator is present
Real Creative-Commons photos, searchable by keyword, **no account/key**:
```bash
curl -s -A "Mozilla/5.0" "https://api.openverse.org/v1/images/?q=foggy+lake+dawn&page_size=4"
# → JSON: results[].url (full image), .thumbnail, .license, .creator, .provider
```
Download the chosen `url` to `assets/` (Tier-B images are real photos; quality varies — pick from a few results). Record `creator`/`license` for attribution (CC-BY etc.). Verified working anonymously: HTTP 200, downloadable JPEG.

### Tier C — Lorem Picsum (placeholder only — never counts as "has imagery")
For texture, abstract, or when the exact subject doesn't matter:
```
https://picsum.photos/seed/{slug}/1600/900            (stable per seed)
https://picsum.photos/seed/{slug}/1600/900?grayscale&blur=2
```
No keyword search — seed is just a stable random key. Curate specific IDs (browse picsum.photos/images) if a subject matters.

### Tier D — user-provided
User drops images in `./assets/` → reference them directly. No external calls.

> Dead / avoid: `source.unsplash.com` (shut down 2024), Pollinations no-key (`402`), Pixabay hotlinking (URLs expire in 24h — must self-host), LoremFlickr (unstable). Unsplash/Pexels APIs work but need a free key — use only if a key is present in env.

## The self-sufficiency rule (non-negotiable)

**A prototype must look finished even if every image fails to load.** The biggest "позорище" failure mode is a hotlink that 402s, leaving an empty placeholder panel.
- Put a **concept-palette gradient/solid behind every `<img>`** so a missing image reads as intentional, not broken.
- Treat the image as *enhancement*, not load-bearing structure. Never leave a blank rectangle.
- For shareable/standalone deliverables: **download images locally** (Tier A/B/C → `assets/`) so nothing depends on a live network at view time.

## Motion on images
Ken Burns (slow scale+translate) makes any photo feel alive — highest-ROI image animation. A slow diagonal light-sweep adds life to editorial photos. See `motion.md`.
