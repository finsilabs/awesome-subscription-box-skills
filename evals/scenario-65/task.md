# Tier Product Gallery Override Using Theme Assets

## Problem/Feature Description

Summit Snacks is a monthly outdoor trail food subscription box with three tiers: Base Camp ($34/mo), Ridge Runner ($54/mo), and Summit ($79/mo). Each tier has a distinct box design — the images have been generated and placed in the theme's `assets/` folder as `tier_basecamp.png`, `tier_ridgerunner.png`, and `tier_summit.png`.

The store is built on Dawn but the Shopify MCP is not available to upload product media to the product records. Without uploaded media, each tier's PDP just shows "No media" using the default Dawn product gallery. The marketing lead wants each tier's product page to show the correct themed box image, not a blank gallery.

The solution is to modify the product section to detect which tier product is being viewed and display the appropriate theme asset image instead of the product media gallery. The current `main-product.liquid` is in `inputs/main-product.liquid`.

## Output Specification

Produce the following files:

- `sections/main-product.liquid` — the modified product section that implements the tier-specific image override
- `implementation-notes.md` — a short document explaining the approach: how the override works, which handles map to which images, and what falls back to the standard product media gallery for non-tier products
