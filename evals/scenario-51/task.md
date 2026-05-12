# Product Image Generation Script for TeaBox Subscription Tiers

## Problem/Feature Description

TeaBox is a monthly tea subscription box launching with three subscription tiers: Sampler ($29/mo, 4 teas), Curator ($49/mo, 8 teas + accessories), and Connoisseur ($79/mo, 12 premium teas + ceramic mug + tasting guide). Each tier needs a distinct product page on Shopify with professionally styled hero imagery.

The team doesn't have a product photographer lined up yet but needs product pages live within the week. The developer wants a reproducible image generation script that the team can re-run whenever they update the box contents, along with a custom product detail page template that showcases all three tiers.

The images should look like high-end editorial e-commerce photography — not AI-generated. The style should be clean and moody: kraft box on a dark slate surface with warm lighting, no visible people, and no text other than what's naturally on the packaging.

## Output Specification

Produce the following files:

1. `scripts/generate_teabox_images.py` — A Python script that generates product images for all three TeaBox tiers using the AI image generation API. The script should be runnable with `uv run scripts/generate_teabox_images.py` and should save each generated image to `generated/`. Write the script but do not run it.

2. `templates/product.subscription.json` — A Shopify product template for the subscription tier PDP. Base it on the standard subscription product template pattern — include at minimum a hero section, subscription tier comparison section, and value proposition section. 

3. `product_setup_notes.md` — Brief notes on the product SKU naming convention to use for each tier and how to apply the custom template to a product in Shopify.
