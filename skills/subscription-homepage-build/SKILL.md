---
name: subscription-homepage-build
description: Use this skill when the user wants to build a homepage optimized for a subscription-box business — phrases like "build a subscription homepage", "subscription main page", "homepage for monthly box", "subscription tier picker page". Generates a Dawn-compatible templates/index.json with hero → how-it-works → tier picker → recent drops → testimonials → FAQ → email capture, with tier images and brand-aligned copy.
---

# Subscription homepage build

Generate `templates/index.json` for a subscription-box homepage on a Dawn-based theme. The structure is battle-tested for monthly-box brands: drives the visitor from emotional hook → mechanic explanation → tier choice → social proof → objection handling → email capture.

## When to use

- Working in a Dawn-based Shopify theme (current dir has `templates/`, `sections/`, `config/`)
- The store is a subscription box with 1–4 tiers
- The user wants the homepage built/rebuilt

## Prerequisites

1. Dawn theme present (`templates/index.json` exists)
2. Tier products exist or will exist soon (so handles like `/products/<tier>` resolve)
3. **Brand voice vault** at `~/.claude/brand-voice-vault/<brand>/` is helpful but not required

## Section order

```
1. Hero (image-banner)               — emotional hook + 2 CTAs
2. Anchor "how-it-works"             — custom-liquid for #how-it-works fragment
3. How it works (multicolumn, 3 cols)— pick / curate / box
4. Anchor "tiers"                    — custom-liquid for #tiers fragment
5. Tier picker (multicolumn, 3 cols) — each tier with image + price + CTA
6. Recent drops (collage, 3 images)  — past curation flat-lays
7. Testimonials (multicolumn, 3 cols)— named quotes with environmental images
8. FAQ (collapsible-content)         — 5 most common questions
9. Email capture (newsletter)        — for non-subscribers
```

## Steps

### 1. Gather brand inputs

If `~/.claude/brand-voice-vault/<brand>/` exists, read:
- `voice.md` for tone
- `palette.json` for color schemes
- `principles.md` for value-prop framing

Otherwise ask user for:
- Brand name and tagline
- Tier names + prices + 1-line description for each
- Brand color (single accent — palette inferred)
- Boxes ship cadence (monthly default, weekly, quarterly)

### 2. Pre-set anchor links

Hero CTAs typically link:
- Primary → `#tiers` (anchor on same page) OR `/collections/tiers`
- Secondary → `#how-it-works` (anchor)

For anchor links to work, prepend a `custom-liquid` section before each target section with:
```html
<a id="tiers" style="display:block;scroll-margin-top:120px"></a>
```
Use `scroll-margin-top` so a sticky header doesn't cover the heading on scroll.

### 3. Build the JSON

Use these section types from Dawn — they all support the right blocks for this layout:

| Section type | Used for |
|---|---|
| `image-banner` | Hero |
| `multicolumn` | How it works, Tiers, Testimonials |
| `collage` | Recent drops |
| `collapsible-content` | FAQ |
| `newsletter` | Email capture (NOT `email-signup-banner` — that's restricted to password page) |
| `custom-liquid` | Anchor injection |

### 4. Schema gotchas

These have caused failures in real builds — pre-validate:

- **Range steps:** `card_shadow_blur` must be a multiple of 5 (10, 15, 20…). `page_width` is step 100 (1100, 1200, 1300…). `padding_top/bottom` is step 4. `buttons_radius` step 2.
- **Section restrictions:** `email-signup-banner` is restricted to template "password" — use `newsletter` instead on index.
- **HTML in `row_content` (collapsible):** `<code>` is rejected. Use `<strong>` for emphasis.
- **Heading sizes:** valid are `h2 / h1 / h0 / hxl / hxxl`.
- **multicolumn `image_ratio`:** valid are `adapt / portrait / square / circle`.
- **Collage block image setting:** must be type `image` with an `image` setting populated (or empty string).

### 5. Tier card images

If the store has tier products with featured images uploaded, reference them as:
```json
"image": "shopify://shop_images/<filename>.png"
```

If images aren't uploaded yet, leave the field empty and tell the user to set them in the theme customizer after pushing — the file picker shows everything in their Files library.

### 6. Make tier cards clickable

Add this to `assets/custom.css` so the whole tier card is a click-target (not just the "Subscribe" link):

```css
.multicolumn-card { position: relative; }
.multicolumn-card .multicolumn-card__info a.link[href]::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 1;
}
.multicolumn-card .multicolumn-card__info a.link[href] {
  position: relative;
  z-index: 2;
}
```

### 7. Pre-launch / pre-order banner (optional)

If the store hasn't launched yet, prepend a custom-liquid section before `main` on each tier product template (not the homepage) with prominent ship-date messaging. See `~/dev/gearheadbox/templates/product.subscription.json` for a concrete example.

## Reference example

`~/dev/gearheadbox/templates/index.json` is the canonical Gear Head Box homepage:
- 9 sections total including 2 anchor injections
- Tiers have square images of physical box mockups
- Pre-order messaging in announcement bar instead of homepage hero
- FAQ has 6 questions including a pre-order disclosure

## Cross-skill links

- `brand-voice-extract` first if no vault exists
- `shopify-product-with-images` to populate tier products with photos
- `page-critical-review` to QA the result

## Tradeoffs

- **Section count vs. clutter** — 9 sections is the upper bound. If the brand is high-end / minimal, drop "Recent drops" and "Email capture" for a 6-section variant.
- **Tier comparison via cards vs. table** — multicolumn cards are mobile-friendly. A table (image-with-text variants) is denser but worse on mobile. Cards win for most subscription boxes.
- **Anchor links vs. real pages** — anchor scroll feels modern but fragmenting in URLs. Anchor for hero CTAs only; navigation menu should link to real pages (`/pages/how-it-works`, `/pages/faq`).

## Embedded in this skill folder

Reference templates / examples (copy or adapt):
- `examples/custom.css`
- `examples/footer-group.json`
- `examples/header-group.json`
- `examples/index.json`
