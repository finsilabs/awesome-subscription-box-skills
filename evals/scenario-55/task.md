# How It Works Landing Page — VineBox Wine Subscription

## Problem/Feature Description

VineBox is a monthly wine subscription box curated by sommeliers. New visitors from search and referrals land on the homepage but bounce without converting — user research shows they don't understand how the curation process works or why VineBox is different from just buying wine at a store.

The team wants a dedicated education page at `/pages/how-it-works` that walks visitors through the subscription experience step by step. The page should alternate between image and text panels to keep it visually interesting, explain the curation methodology (how wines are chosen each month), show what the calendar and delivery cadence looks like, and end with a soft call-to-action that invites visitors to subscribe when they're ready.

The developer has the Shopify Page record created. They need the custom JSON template. The visual flow should feel like a magazine editorial layout — not a sales page. All section images can reference placeholder shopify://shop_images/ paths.

## Output Specification

Produce `templates/page.how-it-works.json` — a Horizon-compatible JSON template for the how-it-works education page. The template must include:

- A hero section
- The standard section that renders page body content
- Multiple image-with-text panels alternating layout direction
- A final CTA section (use a rich-text section with a button)

Also produce `template-notes.md` documenting the section structure you used, the layout direction for each image-with-text panel, and the button field names used in the CTA section.
