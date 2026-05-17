# Tier Product Gallery Override Using Theme Assets

## Problem/Feature Description

Summit Snacks is a monthly outdoor trail food subscription box with three tiers: Base Camp ($34/mo), Ridge Runner ($54/mo), and Summit ($79/mo). Each tier has a distinct box design — the images have been generated and placed in the theme's `assets/` folder as `tier_basecamp.png`, `tier_ridgerunner.png`, and `tier_summit.png`.

The store is built on Horizon but the Shopify MCP is not available to upload product media to the product records. Without uploaded media, each tier's PDP just shows an empty gallery using the default Horizon product media block. The marketing lead wants each tier's product page to show the correct themed box image, not a blank gallery.

On Horizon, product media on the PDP is rendered by the `_product-media-gallery` block (`blocks/_product-media-gallery.liquid` — see `inputs/_product-media-gallery.liquid`). That block delegates to the `product-media-gallery-content` snippet and has access to the current product via `closest.product`.

The solution is to modify that block to detect which tier product is being viewed (by `closest.product.handle`) and display the appropriate theme asset image instead of the standard media gallery. Non-tier products must continue to render the normal gallery.

## Output Specification

Produce the following files:

- `blocks/_product-media-gallery.liquid` — the modified product media block that implements the tier-specific image override
- `implementation-notes.md` — a short document explaining the approach: how the override works, which handles map to which images, and what falls back to the standard product media gallery for non-tier products
