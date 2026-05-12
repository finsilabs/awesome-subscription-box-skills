---
name: shopify-theme-clone
description: Use this skill when the user wants to pull/download an existing Shopify theme from a live or unpublished store into their local working directory — phrases like "clone the theme from my store", "pull existing theme", "download my Shopify theme". Uses Shopify CLI's theme pull and sets up local versioning.
---

# Shopify theme — clone existing theme

Pull a theme that's already in a Shopify store down to a local directory and version it with git so the user can edit locally and re-push.

## When to use

- User has an existing theme on their Shopify store and wants to work on it locally
- They have a live theme they want to fork without breaking (pull a duplicate)
- They want to version-control a theme that was edited in the Shopify code editor

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

Confirm the standard Dawn-or-derivative directories are present.

### 5. Hand off

Tell the user:
- They can now edit any file locally
- To preview live: `shopify theme dev --store=<store> --theme=<id>`
- To push back: `shopify theme push --store=<store> --theme=<id>`
- If pushing to MAIN (live), they need `--allow-live`

## Common follow-up tasks

After cloning, the user might want to:
- Run a critical review of the theme: invoke `page-critical-review` skill
- Apply brand voice updates: invoke `brand-voice-extract` then update settings/templates
- Add new pages: invoke `shopify-landing-page` skill

## Tradeoffs

- **Pulling MAIN vs. UNPUBLISHED** — pulling MAIN gets the live state; pulling UNPUBLISHED gets the draft. Always pull MAIN unless the user has a specific draft they want to fork.
- **Pull-then-modify-and-repush** — be explicit with the user that pushing to MAIN with `--allow-live` updates the storefront immediately. For risky changes, push to a new unpublished theme first.

## When NOT to use

- If the working directory already has a theme (would error or merge conflicts)
- If the user wants to start fresh — use `shopify-theme-create` instead
