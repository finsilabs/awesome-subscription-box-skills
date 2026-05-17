# Shopify Product Upload and PDP Setup for HikePack Tiers

## Problem/Feature Description

HikePack is a monthly hiking gear subscription box launching with three tiers: Trailblazer ($49/mo), Summit ($69/mo), and Expedition ($99/mo). Product images have already been AI-generated and are sitting in the `generated/` directory. The next step is to get these products into Shopify with the images attached and a custom product detail page template applied.

The developer needs a working upload script and a custom PDP template so that the subscription products are created correctly and the product pages don't just show the default Shopify layout. The three tier products will each use the same custom PDP template.

Details about the images and products are in `inputs/generated_images.json`.

## Output Specification

Produce the following:

1. `scripts/upload_teabox_images.py` — A Python script following the Shopify staged upload pattern to upload the local image files to the Shopify CDN. The script should use the 3-step staged upload workflow (create staged upload targets, POST the binary files to the targets, create the file records). Write the script but do not run it.

2. `templates/product.subscription.json` — A Shopify Horizon-compatible product template JSON for the subscription tier PDP. Include sections appropriate for a subscription product (a featured product section, a tier comparison or value proposition section, and a related products section).

3. `product_creation_commands.md` — Documentation showing the Shopify GraphQL mutation to: (a) create one of the tier products with the correct SKU format, and (b) apply the custom template to the product using the correct templateSuffix approach.
