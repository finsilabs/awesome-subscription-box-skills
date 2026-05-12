---
name: shopify-landing-page
description: Use this skill when the user wants to create a specialized landing page for the Shopify shop — phrases like "create a landing page", "build a campaign page", "spin up a holiday landing page", "make a Black Friday page", "make a how-it-works page", "make a gift landing page". Creates a Shopify Page record + a custom Liquid/JSON template tailored to the campaign's goal.
---

# Shopify landing page

A landing page lives at `/pages/<handle>` and uses a custom JSON template (`templates/page.<handle>.json`) for a campaign-specific layout that the default `page.json` doesn't deliver.

## When to use

- Pre-launch / launch event page
- Holiday or seasonal campaign (Black Friday, Father's Day, Track Day Season)
- Gift / corporate gifting page
- "How it works" or "About" detail pages
- Audience-specific page driven from a paid ad

## Page archetypes

Pick the closest archetype as a starting point:

| Archetype | Sections (in order) | Color tone |
|---|---|---|
| **Promo / sale** | Image-banner hero with countdown copy → 2-3 product highlights → urgency-driven CTA → FAQ | Brand accent on dark |
| **Gift** | Image-banner hero ("Give X") → tier comparison → "How gifting works" 3-step → corporate CTA | Premium dark + warm accents |
| **How it works** | Image-banner → 3-step process → calendar / cadence → guarantee CTA | Brand neutral |
| **About / Story** | Image-banner → 3 principles → image-with-text "behind the scenes" → CTA | Brand neutral |
| **Audience-specific** | Tight image-banner → 1 pain-point / 1 solution → social proof → tight CTA | Match audience |

## Steps

### 1. Define the page

Ask the user:
- Goal (conversion, education, hype, gifting)
- Page handle / URL slug (e.g., `black-friday`, `gift`, `how-it-works`)
- Campaign window if time-bound
- Existing imagery available, or generate via Nano Banana?

### 2. Create the Shopify Page record

```graphql
mutation PageCreate($page: PageCreateInput!) {
  pageCreate(page: $page) {
    page { id handle title templateSuffix }
    userErrors { field message }
  }
}
```

Variables:
```json
{
  "page": {
    "title": "<Page Title>",
    "handle": "<handle>",
    "isPublished": true,
    "templateSuffix": "<handle>",
    "body": "<intro paragraph or two — rest of layout comes from JSON template>"
  }
}
```

### 3. Build the custom template

Write `templates/page.<handle>.json` following Dawn's section schema. Reference structure (from gearheadbox):

```json
{
  "sections": {
    "hero": { "type": "image-banner", "blocks": {...}, "settings": {...} },
    "main": { "type": "main-page", "settings": {} },
    "...campaign-specific sections": {...}
  },
  "order": ["hero", "main", "..."]
}
```

The `main-page` section renders the page body content from step 2. Surround it with hero above and CTA sections below.

### 4. Schema gotchas

(Same as `subscription-homepage-build` skill — see that for the full list)

- Range steps for paddings (step 4), shadows (step 5), corner radius (step 2)
- `email-signup-banner` is restricted to password template — use `newsletter` or `rich-text`
- `<code>` tag rejected in `row_content`
- `image-with-text` `layout` valid values: `image_first`, `text_first`
- `rich-text` button block uses `button_label` / `button_link` (not `_1` suffix)

### 5. Image needs

If the page needs imagery, generate via Nano Banana (see `shopify-product-with-images` skill for pattern). Common ratios:
- Hero: 16:9
- Section dividers: 4:3 or 16:9
- In-content product spots: 1:1

Upload to Shopify CDN via `stagedUploadsCreate` and reference in the template as `"image": "shopify://shop_images/<filename>.png"`.

### 6. Wire up navigation

If the page should be in the main nav or footer:

```graphql
mutation MenuUpdate($id: ID!, $items: [MenuItemUpdateInput!]!) {
  menuUpdate(id: $id, items: $items, ...) {
    menu { id items { title url type } }
    userErrors { field message }
  }
}
```

Add a new item with `type: PAGE, resourceId: <page GID>`.

### 7. Push the theme

`shopify theme push --theme=<id>` deploys the new template. After push, the page renders at `/pages/<handle>` automatically.

## Layout patterns by goal

**Conversion-focused (sale / promo):**
- Single CTA repeated 3x throughout the page
- Countdown / urgency copy in hero
- Social proof above the fold
- FAQ at bottom to handle objections

**Education-focused (how-it-works / about):**
- Image-with-text alternating left/right for variety
- 3-step process or 3 principles is the right amount
- Soft CTA at the very end, not throughout

**Audience-specific (paid traffic landing):**
- Lead with the pain point in the hero
- Single product or single CTA
- Cut the navigation noise (consider a stripped-down theme.liquid layout)

## Reference examples

In `~/dev/gearheadbox/templates/`:
- `page.how-it-works.json` — 5-section education-focused page
- `page.faq.json` — 6-section comprehensive FAQ with collapsible-content per topic
- `page.gift.json` — 7-section gifting page with tier comparison and corporate CTA
- `page.about.json` — 5-section brand story page

## Tradeoffs

- **Custom template vs. body-only** — using the default `page.json` template with rich body HTML is faster but limited. Custom JSON template gives you proper Dawn sections (image-banner, multicolumn, collapsible-content) for visual hierarchy.
- **Static vs. metaobject-driven** — for highly templated landing pages (e.g., 50 city-specific pages), use Shopify metaobjects to drive content. For 1-5 pages, the static JSON approach is simpler.
- **Page handles in URLs** — pick handles that age well (`how-it-works` lasts forever; `holiday-2026` doesn't).

## Cross-skill links

- `shopify-product-with-images` for image generation
- `brand-voice-extract` for the voice/tone source of truth
- `klaviyo-campaign-create` to drive traffic via email when the page is for a campaign

## Embedded in this skill folder

Scripts (copy to your project's `scripts/` directory and run with `uv run`):
- `scripts/generate_images.py`
- `scripts/upload_staged.py`

Reference templates / examples (copy or adapt):
- `examples/404.json`
- `examples/page.about.json`
- `examples/page.faq.json`
- `examples/page.gift.json`
- `examples/page.how-it-works.json`
