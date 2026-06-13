# Typography — distinctive fonts + the Cyrillic safety gate

Typography is the #1 wow lever and the #1 slop tell. Two rules govern everything:

1. **Never** use Inter, Roboto, Arial, system-ui, Open Sans, or Lato as the *design* font.
2. **For Russian/Cyrillic content, every font MUST be verified to support Cyrillic** — or the text silently falls back to a system font and the whole design breaks.

## Expressive defaults

- **Weight extremes:** pair 200/300 against 700/800 — not 400 vs 600.
- **Size jumps of 3x+:** a hero headline at 64-120px next to 14-16px body, not a timid 1.5x scale.
- **Pairing with contrast:** high-contrast display serif + clean grotesk; or serif + mono. Sameness across prototypes (every variant = elegant serif + light sans) means the *concepts* aren't different enough.
- **Choose the font from the concept**, not for diversity's sake. If the idea calls for a didone, use one even if another variant has a serif.

### ⚠️ Match the font to the DOMAIN — don't default to the "comfort serif"
A recurring failure: reaching for **Cormorant Garamond / Playfair Display on every project** because they read as "elegant". An elegant book-serif on a **fintech / hardware / tech** product is tonally wrong — it looks like a wedding invitation on a spec sheet ("свадебный гарамонд"). Before picking, ask *what does THIS product's world actually look like?*
| Domain | Lean toward | Avoid |
|--------|-------------|-------|
| PC hardware / tech / performance / SaaS tools | precise grotesques + mono (Geologica, Onest, Manrope, Inter Tight, JetBrains Mono), or a confident geometric display (Unbounded) | delicate literary serifs (Cormorant, Playfair) |
| Finance / B2B / trust | restrained modern grotesk, or a *sturdy* serif (Literata, Spectral) | dainty didones |
| Editorial / emotional / lifestyle | expressive/contrast serifs (Cormorant, Prata, Alegreya) shine here | generic grotesks |
**Anti-default check:** if Cormorant or Playfair shows up in more than one variant — or across more than one project — that's the comfort-zone tell. Reach into the full pool and pick for *this* domain.

## ⚠️ The Cyrillic gate (HARD rule for RU)

Many distinctive "American-standard" fonts have **no Cyrillic** and are unusable for Russian:
**Fraunces, Clash Display, Bricolage Grotesque, Cabinet Grotesque, Satoshi, DM Sans, DM Serif, Space Grotesk, Playfair (check), Fraunces, Cinzel, Libre Baskerville.**

> Caught in real testing twice: (1) a brief that wanted "distinctive fonts" kept reaching for Fraunces/Clash — broken for RU. (2) A live production app shipped **DM Sans** as its body font on a Russian site — no Cyrillic, so all body text was rendering in a system fallback. The gate catches both.

### How to verify a font has Cyrillic (one-line checker)

The old method (grep for the `/* cyrillic */` comment) is unreliable — it depends on the User-Agent. **Check the actual unicode-range** instead:

Bash / Git Bash:
```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
curl -s -H "User-Agent: $UA" "https://fonts.googleapis.com/css2?family=FONT+NAME:wght@400&display=swap" | grep -qi "U+0400" \
  && echo "✓ Cyrillic OK" || echo "✗ NO Cyrillic — do not use for RU"
```
PowerShell (Windows-default shell — the Bash here-string/pipe above fails there):
```powershell
$ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
$css=(Invoke-WebRequest "https://fonts.googleapis.com/css2?family=FONT+NAME:wght@400&display=swap" -Headers @{ "User-Agent"=$ua }).Content
if ($css -match "U\+0400") { "✓ Cyrillic OK" } else { "✗ NO Cyrillic — do not use for RU" }
```
(`U+0400`–`04FF` is the Cyrillic block. Replace `FONT+NAME`, e.g. `Golos+Text`.) Or, no shell: fonts.google.com → font → "Languages" → look for Cyrillic.

### Verified distinctive + Cyrillic-safe pool (RU)

| Role | Fonts (Cyrillic verified) | Character |
|------|---------------------------|-----------|
| **Elegant / didone serif** | Cormorant Garamond, Prata, Playfair Display, Lora, Spectral | Refined, high contrast, editorial |
| **Literary serif** | Alegreya, Literata, PT Serif, Merriweather, Bitter, Noto Serif, Vollkorn | Bookish, grounded, long-form |
| **Expressive display** | Unbounded, Yeseva One, Forum, El Messiri, Philosopher | Statement, unusual, memorable |
| **Modern UI sans** | Golos Text, Onest, Manrope, Inter Tight, Geologica, Wix Madefor Display | Clean, RU-native, neutral-modern |
| **Mono (accents/labels)** | JetBrains Mono | "field-notes" / technical texture |

Tip: **Golos Text** and **Onest** are Russian-designed — excellent, safe UI bodies. **Cormorant**, **Prata**, **Alegreya**, **Unbounded** give distinctive display with full Cyrillic.

## Latin-only projects
No Cyrillic constraint — the full distinctive arsenal is open: add Fraunces, Clash Display, Bricolage Grotesque, Cabinet Grotesque, Satoshi, Space Grotesk, Newsreader, Crimson Pro, etc. The skill should branch explicitly on **language**: RU → verified pool above; Latin → anything distinctive.

## Don't
Don't fake-glue Cyrillic onto a Latin-only font. Don't use 5 fonts in one prototype. Don't set everything at one weight (kills hierarchy). Don't `clamp()` every property — fixed values per breakpoint give predictable rhythm.
