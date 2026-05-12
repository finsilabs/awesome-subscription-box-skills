---
name: shopify-landing-page
description: Use this skill when the user wants to create a specialized landing page for the Shopify shop — phrases like "create a landing page", "build a campaign page", "spin up a holiday landing page", "make a Black Friday page", "make a how-it-works page", "make a gift landing page". Creates a Shopify Page record + a custom Liquid/JSON template tailored to the campaign's goal.
---

# Shopify landing page

A landing page lives at `/pages/<handle>` and uses a custom JSON template (`templates/page.<handle>.json`) for a campaign-specific layout that the default `page.json` doesn't deliver.

## Page archetypes

Pick the closest archetype as a starting point:

| Archetype | Sections (in order) | Color tone | Layout notes |
|---|---|---|---|
| **Promo / sale** | Image-banner hero with countdown copy → 2-3 product highlights → urgency-driven CTA → FAQ | Brand accent on dark | Repeat CTA 3×; social proof above the fold; FAQ handles objections |
| **Gift** | Image-banner hero (