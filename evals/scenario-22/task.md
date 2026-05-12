# Homepage and Pre-Order Setup for TechKit Box

## Problem/Feature Description

TechKit Box is a monthly electronics and maker subscription launching in pre-order mode. Subscribers choose from three tiers: Hobbyist ($55/mo, Arduino kits, cables, and tools), Builder ($79/mo, Raspberry Pi extras, sensors, LEDs), and Pro Maker ($109/mo, premium components including FPGAs and specialty ICs). The boxes ship starting next month, but the store is live in pre-order mode today.

Because this is a maker/electronics brand, the FAQ needs to answer technical questions — subscribers want to know about component specifications, compatibility standards (I2C, SPI, UART), and what programming environments are typically compatible with the included hardware. These are legitimately technical topics.

The store is currently in pre-order mode. Subscribers who land on the product pages to purchase need to clearly see the ship date ("ships November 15") before committing to a subscription. The marketing team has a strong view on where ship-date messaging belongs — they want it to catch customers at the moment of decision, not to dominate the first impression for cold visitors who haven't yet decided they're interested.

## Output Specification

Produce two files in the current working directory:

1. `templates/index.json` — the complete Dawn homepage template with all standard sections: hero, how-it-works, tier picker (Hobbyist, Builder, Pro Maker), recent drops gallery, testimonials, FAQ with at least 4 questions (including at least one about hardware compatibility or programming environments), and email capture.

2. `templates/product.subscription.json` — a Dawn product template for subscription tier product pages. This template should make the pre-order ship date ("ships November 15") clearly visible to customers viewing a subscription tier product page.
