---
name: shopify-theme-clone
description: Pulls and downloads existing Shopify themes from live or unpublished stores into the local working directory, then initializes git versioning. Use when a user wants to clone, pull, or download a theme from their Shopify store — phrases like "clone the theme from my store", "pull existing theme", "download my Shopify theme". Authenticates with the store, lists available themes, downloads all theme files to the local directory, and sets up local git tracking via Shopify CLI's theme pull.
---

# Shopify theme — clone existing theme

Pull a theme that's already in a Shopify store down to a local directory and version it with git so the user can edit locally and re-push.

## Prerequisites

1. **Shopify CLI installed** — `shopify version`
2. **Working directory** — empty (or contains only .env/.gitignore). The pull will populate it.
3. **Store URL and theme ID** — see step 1 below

## Steps

### 1. Discover available themes

```bash
shopify theme list --store=<store>.myshopify.com
```

The output lists each theme with its ID and role (MAIN = live, UNPUBLISHED = draft).

If the user can't tell us which to clone:
- The MAIN theme = currently live to customers
- An UNPUBLISHED theme = draft / preview-only

### 2. Pull the theme

```bash
shopify theme pull --store=<store>.myshopify.com --theme=<id>
```

Pulls all theme files (templates/, sections/, assets/, snippets/, layout/, locales/, config/) into the current directory.

> **Tip:** Prefer pulling MAIN to get the live state unless the user specifically wants a draft. If the working directory already has a theme, this will cause merge conflicts — start fresh.

### 3. Initialize git tracking

```bash
git init -b main
echo -e ".env\n.shopify\nnode_modules/\ngenerated/" >> .gitignore
git add -A
git commit -q -m "Initial commit: cloned theme '<theme-name>' from <store>"
```

### 4. Verify the pull

```bash
ls config templates sections | head -30
```

Confirm the standard Shopify theme directories are present (Horizon, Dawn, or any derivative all share this layout).

### 5. Hand off

Tell the user:
- They can now edit any file locally
- To preview live: `shopify theme dev --store=<store> --theme=<id>`
- To push back: `shopify theme push --store=<store> --theme=<id>`
- If pushing to MAIN (live), they need `--allow-live` — this updates the storefront immediately, so for risky changes push to a new unpublished theme first

## Common follow-up tasks

Once the theme is cloned and versioned, consider invoking these skills for next steps:

| Goal | Skill to invoke |
|---|---|
| Critical review of theme pages | `page-critical-review` (`page-critical-review.md`) |
| Extract and apply brand voice | `brand-voice-extract` (`brand-voice-extract.md`), then update settings/templates |
| Add new landing pages | `shopify-landing-page` (`shopify-landing-page.md`) |
