# Homepage for GlowKit Beauty Box

## Problem/Feature Description

GlowKit is a skincare and beauty subscription box aimed at women 25–45 who want professional-grade products without the spa price tag. Each month subscribers receive 5–7 full-size products: serums, moisturizers, SPF, and a beauty tool. The brand's visual identity is clean, soft, and aspirational.

The Shopify Dawn store needs a homepage. The creative director is particular about image presentation in the multicolumn sections — tier cards should have a consistent, clean crop and the testimonials section should feel like a magazine editorial (images presented in a consistent ratio). She's left instructions that the image display in the multicolumn sections should be set to a specific ratio that creates a uniform look. The developer needs to implement the correct image ratio settings in the JSON template — the wrong values will cause Dawn to fall back to inconsistent sizing.

The homepage should cover: hero (with an emotional hook about skincare routines), how-it-works (3 steps), tier picker (Glow Starter $45/mo with 4 items, Radiance $65/mo with 6 items, Luminance $95/mo with full-size hero item), a recent boxes gallery, testimonials with three customer quotes and environmental images, a FAQ, and email capture.

## Output Specification

Produce `templates/index.json` in the current working directory. Set explicit `image_ratio` values on all multicolumn sections (how-it-works, tiers, testimonials). Choose image ratios that make sense for each section's content and create a cohesive look.
