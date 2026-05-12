---
name: shopify-theme-create
description: Use this skill when the user wants to start a new Shopify theme from scratch in their working directory — phrases like "create a Shopify theme", "scaffold a theme", "start with Dawn", "build a custom Shopify storefront". Sets up Dawn as the baseline, applies brand styling if a brand-voice-vault entry exists, and provides commands for previewing and pushing.
---

# Shopify theme — new theme scaffold

Set up a fresh Shopify theme based on Dawn (Shopify's flagship reference theme) in the current working directory. The result is a fully-versioned theme repo the user can edit locally and push with `shopify theme push`.

## When to use

- User wants to create a Shopify storefront from scratch
- Working directory is empty or near-empty
- The brand needs a custom theme, not a pre-built template

## Prerequisites

1. **Shopify CLI installed** — verify with `shopify version`. Install via `brew install shopify-cli` if missing.
2. **Working directory** — empty or contains only `.env` / `.gitignore`. If not empty, ask user before proceeding.
3. **Store handle** — the `*.myshopify.com` URL. Ask if not provided.

## Steps

### 1. Confirm scope with the user

Ask if you don't know:
- The brand name and category (sets messaging tone and layout choices)
- Whether they have an existing brand-voice-vault entry under `~/.claude/brand-voice-vault/<brand>/`
- The store URL (`*.myshopify.com`)

### 2. Scaffold Dawn

```bash
git clone --depth=1 https://github.com/Shopify/dawn.git .
rm -rf .git
git init -b main
git add -A && git commit -q -m "Initial commit: Dawn theme baseline"
```

This may trigger a permission prompt for "untrusted code integration" — Dawn is Shopify's official theme, explain this and let user approve.

### 3. Apply brand voice (optional but recommended)

If `~/.claude/brand-voice-vault/<brand>/` exists, load:
- `palette.json` → drive `config/settings_data.json` color schemes
- `typography.md` → set `type_header_font` / `type_body_font` in settings
- `voice.md` → use as reference when writing site copy

Otherwise leave Dawn defaults; the brand can be applied later via the same files.

### 4. Add brand-specific structure

Create these as needed (typical for a brand site):
- `assets/custom.css` for brand CSS overrides on top of Dawn's `base.css`
- Link `custom.css` from `layout/theme.liquid` right after `base.css`
- Create custom page templates (`templates/page.<handle>.json`) for About, How It Works, FAQ, etc.

### 5. Hand off to user

Don't push automatically. Tell them:

```
shopify theme push --store=<their-store>.myshopify.com --unpublished
```

After their first push, return the theme ID and tell them future pushes use:
```
shopify theme push --store=<store> --theme=<id>
```

## Files this skill typically creates

```
config/settings_data.json   (modified for brand palette)
assets/custom.css           (brand-specific CSS layer)
templates/index.json        (homepage — see subscription-homepage-build skill)
.gitignore                  (add .env, .shopify, generated/)
```

## Cross-skill links

- For brand voice extraction: invoke `brand-voice-extract` first
- For homepage layout: invoke `subscription-homepage-build` after this skill
- For products + images: invoke `shopify-product-with-images`

## Reference implementation

A complete example of this skill applied: `~/dev/gearheadbox/` — Dawn-based Shopify theme for a subscription box brand with full homepage, product templates, custom CSS, and brand-applied palette.

## Tradeoffs

- **Dawn** is free and Shopify-supported — best default. Loses to paid themes (Impulse, Symmetry) on visual polish out of the box but is more flexible to customize.
- **Cloning vs. fresh init** — if the user has an existing theme on the store they want to start from, use `shopify-theme-clone` instead.
- **Dev plan vs. paid plan** — Dawn works on both. Mention to user that some sections (e.g., subscription apps) require a paid plan or app installation.
