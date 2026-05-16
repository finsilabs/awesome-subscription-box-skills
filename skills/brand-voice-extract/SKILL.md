---
name: brand-voice-extract
description: Extracts and codifies a brand's voice, visual identity, and messaging principles from a website URL into a reusable "brand voice vault." Use when someone says things like "analyze the brand at [url]", "extract brand voice", "save brand to vault", "study this brand", or needs a structured brand reference before creating content. Outputs files at ~/.claude/brand-voice-vault/[brand]/ that other skills can reference.
---

# Brand voice extraction → vault

Visit a brand's website, extract their voice / visual identity / messaging principles, and save to a structured "vault" at `~/.claude/brand-voice-vault/<brand>/` so other skills (theme creation, blog posts, landing pages, campaigns) can reference one source of truth.

## When to use

- Starting work on a brand for the first time
- The user wants a brand audit or voice document
- Other skills need a `brand-voice-vault/<brand>/` reference

## Vault structure

```
~/.claude/brand-voice-vault/<brand>/
  voice.md           — tone, vocabulary, dos/don'ts, sample copy
  visual.md          — typography, motifs, photographic style
  palette.json       — exact hex colors with usage roles
  principles.md      — what they stand for / against; positioning statement
  audience.md        — who they sell to, motivations, triggers
  examples/          — pull-quotes and phrases from the live site
  source.json        — source URLs, fetch date, summary metadata
```

## Steps

### 1. Confirm the brand and URL

Ask the user for:
- The canonical brand name (slug it for the directory: e.g., "Gear Head Box" → `gear-head-box`)
- One or more URLs to analyze (homepage, About, product pages, blog)

### 2. Fetch the source pages

Use `WebFetch` for the homepage and About page minimum. For richer extraction, also fetch one product page and one blog post if available.

For each fetched page, prompt for:
- Tagline and hero headline
- Key phrases and idiomatic word choices
- Pricing and tier framing
- Calls-to-action
- Tone (formal/casual, masculine/feminine/neutral, technical/lifestyle)

### 3. Inspect visual style

Take screenshots if browser MCP is available, or describe from rendered text + observed CSS:
- Dominant colors (extract hex values from inline styles or backgrounds)
- Type — serif / sans / display, weight, tracking
- Imagery style (editorial photography, illustration, lifestyle, minimalist)

### 4. Write the vault files

Each file under `~/.claude/brand-voice-vault/<slug>/`:

**voice.md** — tone summary, vocabulary list (words to use / avoid), 3-5 sample paragraphs in voice, common opening lines, common closing lines.

**visual.md** — typography pairing recommendation, photo direction, iconography rules.

**palette.json** —
```json
{
  "primary":   {"hex": "#XXXXXX", "use": "buttons, accents"},
  "secondary": {"hex": "#XXXXXX", "use": "supporting"},
  "page_bg":   {"hex": "#XXXXXX", "use": "main background"},
  "card_bg":   {"hex": "#XXXXXX", "use": "elevated surfaces"},
  "text":      {"hex": "#XXXXXX", "use": "body copy"},
  "muted":     {"hex": "#XXXXXX", "use": "captions, dividers"}
}
```

**principles.md** — 3-7 brand principles, each one sentence. Format: "We do X. We don't do Y. Why: Z."

**audience.md** — primary and secondary audience, motivations, life stage, what triggers them to buy.

**examples/source-quotes.md** — verbatim phrases pulled from the site (≤15 words each, in quotes), credited to their source URL.

**source.json** —
```json
{
  "brand": "<name>",
  "slug": "<slug>",
  "fetched_at": "<ISO date>",
  "sources": ["<url1>", "<url2>"],
  "notes": "<short summary>"
}
```

### 5. Summarize for the user

Show a 5-line summary in chat: brand name, archetype, audience, dominant color, dominant tone. Confirm the vault path and offer to extract more pages.

## Cross-skill integration

Other skills look for `~/.claude/brand-voice-vault/<slug>/` and should:
- Read `palette.json` to drive color schemes
- Read `voice.md` before writing site copy / blog posts / emails
- Read `principles.md` to stay on-message in CTAs and positioning

## Reference example

`~/.claude/brand-voice-vault/gear-head-box/` (if Gear Head Box vault is populated) — racing-themed subscription box, midlife-crisis-meets-gearhead audience, tire-gray palette with F1 red accent, masculine direct voice.

## Tradeoffs

- **Depth vs. speed** — for a quick first pass, just fetch homepage + about and skip the examples folder. The vault can be enriched later as more pages are analyzed.
- **Auto vs. user-confirmed** — when in doubt about voice classification, ask the user one or two yes/no questions ("Is this brand voice masculine-coded or neutral?") rather than guessing.

## Avoid copyright issues

Quote no more than 15 words verbatim per pull-quote. The vault is for internal reference, not public republishing.
