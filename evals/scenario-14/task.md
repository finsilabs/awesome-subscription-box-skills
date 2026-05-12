# Homepage Anchor Navigation for FreshHarvest Box

## Problem/Feature Description

FreshHarvest Box is a seasonal produce subscription that ships farm-direct fruit and vegetable crates every month. Their Shopify Dawn homepage is almost done, but the marketing team has flagged a UX issue: when visitors click "How it works" or "Choose your crate" in the hero, they jump to the right section but the sticky header overlaps the section heading, making it look broken on desktop. The development team needs the homepage rebuilt so the anchor-based navigation works correctly — the target section headings must be visible below the sticky header after scroll.

The fix requires a specific HTML approach to inject invisible anchor targets that account for the sticky header offset. The developer has asked for a complete `templates/index.json` that implements this correctly, with two properly placed anchor targets: one for the "how-it-works" section and one for the "tiers" / "crates" section.

## Output Specification

Produce `templates/index.json` in the current working directory. The template should include a hero section, a how-it-works section, a tier/crate picker section, and at least one more section (testimonials, FAQ, or email capture). The critical requirement is that the anchor targets for in-page navigation are correctly placed and implemented so the sticky header does not obscure the destination heading on scroll.

Use three crate tiers: Seedling ($29/mo), Harvest ($49/mo), Farmstead ($79/mo). Make up fitting copy.
