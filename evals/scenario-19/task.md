# Clickable Tier Cards for BrewCraft Beer Box

## Problem/Feature Description

BrewCraft is a craft beer discovery subscription that ships 12 curated cans or bottles monthly — Taster (12 beers, $49), Enthusiast (12 beers + tasting notes, $65), and Cellar (12 premium bottles, $95). Their Shopify Dawn homepage has a tier picker built with a multicolumn section, and each tier card has a "Subscribe to [tier]" link at the bottom.

The UX problem: the dev team has noticed that users on mobile swipe across the tier cards thinking the card itself is clickable, but only the tiny text link at the bottom fires. The analytics team confirmed that the click-through rate on tier cards is well below benchmark. The solution is to make the entire tier card clickable — not just the link text — using a CSS overlay technique.

The task is to produce both the homepage template and the CSS file that makes the tier cards fully clickable. The subscribe link inside each tier card should behave as a stretched link — clicking anywhere on the card navigates to the product page.

## Output Specification

Produce two files in the current working directory:

1. `templates/index.json` — complete Dawn homepage template with all sections including a tier picker multicolumn where each column block has a `link_label` and `link` pointing to the respective product URL (`/products/taster`, `/products/enthusiast`, `/products/cellar`)
2. `assets/custom.css` — CSS overrides that implement the stretched-link / full-card clickability for multicolumn tier cards
