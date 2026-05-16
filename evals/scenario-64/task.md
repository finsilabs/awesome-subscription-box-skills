# Theme Image Sections Without Files Library Access

## Problem/Feature Description

Copper & Oak is a monthly outdoor and camping gear subscription box. The store's Dawn theme is built out and ready to go, but the Shopify admin API / MCP connection is unavailable — the developer can't upload images to the store's Files library and won't be able to until the agency gets the client to approve the API access permissions.

The theme currently uses the standard image-banner section (see `inputs/image-banner.liquid`) which only renders an image when one is selected from the Files library. Without Files library access, the hero banner on the homepage shows a grey placeholder SVG instead of the brand hero shot. The same limitation applies to two other sections that use image pickers: `image-with-text` and the homepage `multicolumn` tier cards section.

The developer has already placed all the brand images in the theme's `assets/` folder (e.g. `hero.png`, `tier_trailhead.png`, `tier_summit.png`, `tier_basecamp.png`) and now needs to modify the theme sections to render those assets as fallbacks when no Files-library image is selected. This way the build can continue and be visually previewed without waiting for API access.

## Output Specification

Produce the following modified section file:

- `sections/image-banner.liquid` — the updated section with the theme-asset fallback pattern implemented

The updated section must support both modes: if a Files-library image is selected it renders normally; if not, it falls back to a theme asset specified via a text setting.

Also produce:
- `templates/index.json` — a minimal homepage template JSON showing how to wire the `image-banner` section so it renders `hero.png` from the theme assets
