# Clickable Tier Cards for BrewCraft Beer Box

## Problem/Feature Description

BrewCraft is a craft beer discovery subscription that ships 12 curated cans or bottles monthly — Taster (12 beers, $49), Enthusiast (12 beers + tasting notes, $65), and Cellar (12 premium bottles, $95). Their Shopify Horizon homepage has a tier picker built as a `section` container holding three tier cards, where each tier card is a `group` block, and each card has a "Subscribe to [tier]" button at the bottom.

The UX problem: the dev team has noticed that users on mobile swipe across the tier cards thinking the card itself is clickable, but only the small button at the bottom fires. The analytics team confirmed that the click-through rate on tier cards is well below benchmark. The solution is to make the entire tier card clickable — not just the button.

On Horizon, `group` blocks support a native `link` setting: when a group block has a `link`, the whole card becomes a single clickable link with no CSS hacks required. The task is to wire each tier card's `group` block `link` to the matching product page, and add a small CSS hover affordance so visitors can see the card is interactive.

## Output Specification

Produce two files in the current working directory:

1. `templates/index.json` — complete Horizon homepage template with all standard sections, including a tier picker where each of the three tier-card `group` blocks has its `link` setting populated with the respective product URL (`/products/taster`, `/products/enthusiast`, `/products/cellar`). Each card should also keep a "Subscribe to [tier]" button block.
2. `assets/custom.css` — CSS that gives the clickable tier cards a hover affordance (e.g., a cursor change, lift/translate, or shadow on hover) so visitors recognize the whole card is clickable.
