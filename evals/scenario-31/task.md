# New Shopify Theme Setup for NightOwl Candles

## Problem/Feature Description

NightOwl Candles is a subscription candle box brand launching in two months. They need a Shopify theme set up in a fresh local directory so their developer can start building the storefront. The store will run on Horizon. Their brand palette has already been defined and is in `inputs/palette.json`.

The developer needs a fully initialized, version-controlled theme repo ready to work in — with the brand colors already applied so they can start customizing from day one rather than working in Shopify's default theme colors. The theme will need custom styling on top of Horizon's base styles, which they plan to develop iteratively.

The store URL is `nightowlcandles.myshopify.com`. The developer will push the theme to the store themselves once it's ready for review.

## Output Specification

Set up the Shopify theme in the current working directory. The deliverable is a working local theme repo that includes:

- The full Horizon theme files, version-controlled
- The brand palette from `inputs/palette.json` applied to the theme's configuration
- A structure in place for custom CSS so the developer can start adding brand-specific styling immediately
- A properly configured version control setup with appropriate files excluded

At the end, output `setup-instructions.md` explaining the exact commands the developer should run to preview and push the theme to the store, along with the git history showing the initial commit.
