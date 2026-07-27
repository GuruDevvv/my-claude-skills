# youtube-downloader

A wrapper around `yt-dlp` that handles the things which normally make it fail.

## What it adds over plain yt-dlp

- **Bot-check bypass** — when YouTube demands proof you are not a robot, it stands up a token provider
  in Docker and retries; without Docker it falls back to the browser-based route instead of giving up.
- **403 retry** — turns a refusal into a retry with the verification path enabled.
- **Locked platforms** — Vimeo, Mux and other HLS services where video arrives in chunks behind auth
  headers. That is the case where a course lives in a private player rather than on YouTube.
- Can reuse a Chrome session for login-only videos, and is explicitly forbidden from printing anything
  about cookie contents.
- 4K, audio-only MP3, subtitles, playlists (playlists only after confirmation).

Asks before installing dependencies, before touching cookies, before bulk downloads. Reminds you about
rights to the content.

## Requirements

`yt-dlp` and `ffmpeg`; Docker optional, used for the token provider.

## Source

**Not my work.** By daymade — [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills), `youtube-downloader/`

MIT. Full licence text: [`../licenses/`](../licenses/). Prefer installing from upstream — that copy is maintained, this one is a snapshot.
