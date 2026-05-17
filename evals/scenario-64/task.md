# Theme Image Block Without Files Library Access

## Problem/Feature Description

Copper & Oak is a monthly outdoor and camping gear subscription box. The store's Horizon theme is built out and ready to go, but the Shopify admin API / MCP connection is unavailable — the developer can't upload images to the store's Files library and won't be able to until the agency gets the client to approve the API access permissions.

Horizon renders images through a shared `image` block (`blocks/image.liquid` — see `inputs/image.liquid`). The block only renders an image when one is picked from the Files library; otherwise it falls back to a grey placeholder SVG. Because the hero, the tier cards, and every other image-bearing area on the homepage are all composed from this one `image` block, none of the brand imagery shows up without Files library access.

The developer has already placed all the brand images in the theme's `assets/` folder (e.g. `hero.png`, `tier_trailhead.png`, `tier_summit.png`, `tier_basecamp.png`) and now needs to modify the `image` block to render those assets as a fallback when no Files-library image is picked. This way the build can continue and be visually previewed without waiting for API access.

## Output Specification

Produce the following modified block file:

- `blocks/image.liquid` — the updated `image` block with the theme-asset fallback pattern implemented

The updated block must support both modes: if a Files-library image is picked it renders normally; if not, it falls back to a theme asset whose filename is supplied via a new text setting.

Also produce:
- `templates/index.json` — a minimal homepage template JSON showing how to wire an `image` block (inside a `section`) so it renders `hero.png` from the theme assets via the new fallback setting
