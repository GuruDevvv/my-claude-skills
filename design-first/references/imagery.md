# Imagery — sourcing real images autonomously (and when not to)

Real images are a major wow lever. But two hard constraints:

1. **The source must actually work.** (Pollinations' no-key path is dead — returns `402 Queue full`. Do not use it.)
2. **No binding to anyone's account/spec.** The skill is portable; it must not require the author's paid subscription, an API key the user doesn't have, or any project-specific service.

## When NOT to use images (decide this first)

- **Data dashboards, dense tools, admin panels** → no hero photos. Stock images look pasted-on. Do the work with typography, color, data hierarchy, and functional motion.
- **When a photo would dilute a pure-type/editorial concept.**

If imagery fits (landings, hero sections, atmospheric/editorial pages), use the cascade.

## The autonomous cascade (pick the highest tier available)

### Tier A — bespoke generation (best quality, only if a generator is present)
If the environment exposes an image-gen tool/MCP (Higgsfield, DALL·E, Replicate, a local SD, etc.) **and you've confirmed it's available**, generate a concept-matched image, then **download it locally** to `assets/` so the prototype stays standalone. This is optional and vendor-agnostic — never assume a specific one.
Pattern: generate → poll for the result URL → `curl -L "<url>" -o assets/hero.png` → reference `./assets/hero.png`.
(Example: Higgsfield `generate_image` → `job_status(sync:true)` → download `rawUrl`. ~2 credits/image. But treat as "if present", not required.)

### Tier B — Openverse (free, no key, keyword search) — the portable default ✓ tested
Real Creative-Commons photos, searchable by keyword, **no account/key**:
```bash
curl -s -A "Mozilla/5.0" "https://api.openverse.org/v1/images/?q=foggy+lake+dawn&page_size=4"
# → JSON: results[].url (full image), .thumbnail, .license, .creator, .provider
```
Download the chosen `url` to `assets/` (Tier-B images are real photos; quality varies — pick from a few results). Record `creator`/`license` for attribution (CC-BY etc.). Verified working anonymously: HTTP 200, downloadable JPEG.

### Tier C — Lorem Picsum (free, no key, random/texture)
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
