# Black Friday Landing Page — PaddlePack Subscription Box

## Problem/Feature Description

PaddlePack is a monthly subscription box for paddle sports enthusiasts — kayaking, SUP, and canoeing. This November they're running their biggest sale of the year: 20% off the first three months on any tier, valid through the end of Black Friday weekend.

The marketing manager wants a dedicated page at `/pages/black-friday` that lives outside the default page layout — it needs its own custom section structure with a campaign-specific hero, product highlights, and a targeted CTA section. The intro copy for the page has already been written and should be part of the page body content.

The developer needs to set up both the Shopify Page record in the admin (so it exists as a page resource) and the corresponding theme template file (so the custom layout renders). The store has already been connected and the developer has Shopify CLI available. No images are needed for now — placeholder image paths are fine.

## Output Specification

Produce two files:

1. `shopify/page-setup.md` — A document containing:
   - The exact Shopify GraphQL mutation (with variables) to create the Shopify Page record, including the intro body paragraph and all fields needed for the page to appear at its URL with the correct template applied
   - The shopify theme push command to deploy the new template

2. `templates/page.black-friday.json` — The custom Horizon-compatible JSON template for the Black Friday landing page. The template should render the full campaign experience: a strong hero, the page copy, and at least one campaign-specific section (product highlights or CTA).

The store URL is `paddlepack.myshopify.com` and the theme ID is `139847562302`.
