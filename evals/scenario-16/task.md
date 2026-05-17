# Homepage Template Build for GainStack Fitness Box

## Problem/Feature Description

GainStack is a monthly fitness subscription box targeting home gym enthusiasts. Each month subscribers receive resistance bands, protein samples, workout accessories, and motivational content — curated for intermediate athletes who train at home. The team has just finished brand photography and is ready to build the Shopify Horizon homepage.

The lead developer is out sick and the task has been handed to a junior team member who needs a complete `templates/index.json`. The last time a junior developer touched the theme, a section with an invalid padding value caused the theme customizer to throw a schema validation error and roll back the entire push. The team needs a homepage file that validates cleanly — with all numeric settings respecting the allowed ranges that Horizon enforces.

The homepage should include all standard sections: hero, how-it-works, tier picker (Foundations $45/mo, Optimizer $69/mo, Elite $95/mo), recent drops, testimonials, FAQ, and email capture. Use specific padding values on each section — at least four sections should have explicit `padding-block-start` and `padding-block-end` values set.

## Output Specification

Produce `templates/index.json` in the current working directory. Include all standard sections with appropriate content for a fitness subscription brand. For sections with padding or border settings, make sure numeric values are set explicitly (do not leave them at defaults).
