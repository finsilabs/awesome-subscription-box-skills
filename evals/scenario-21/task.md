# Completing the Homepage for ArtHouse Print Box

## Problem/Feature Description

ArtHouse Print Box is a monthly art print subscription. Each month subscribers receive two to three museum-quality giclée prints by independent artists — curated by category: Classic ($49/mo, one large + one small print), Modern ($69/mo, two large prints), and Collector's Edition ($99/mo, three prints including one signed limited-edition). The physical boxes are photographed and the images have already been uploaded to Shopify's file library.

The brand manager has provided a list of the image filenames that have been uploaded to the Shopify CDN. The task is to build the complete homepage template and wire in these images at the right places. The template will be pushed to the Horizon store immediately — it's important that the image references use the correct URL format that Shopify uses for shop-hosted images, so the theme customizer picks them up correctly rather than showing broken image placeholders.

The uploaded image filenames are:
- `hero_gallery_wall.png` — hero banner image
- `tier_classic_box.png` — Classic tier card image
- `tier_modern_box.png` — Modern tier card image
- `tier_collector_box.png` — Collector's Edition tier card image
- `drops_jan.png`, `drops_feb.png`, `drops_mar.png` — recent drops gallery images
- `testimonial_sarah.png`, `testimonial_james.png`, `testimonial_anna.png` — testimonial avatars

## Output Specification

Produce `templates/index.json` in the current working directory. Include the full homepage with all standard sections. Wire in all the provided image filenames at the appropriate places. The image references must use the correct URL format so they resolve in the Shopify theme customizer.
