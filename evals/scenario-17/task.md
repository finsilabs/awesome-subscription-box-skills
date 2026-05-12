# Homepage Build for PageTurner Book Box

## Problem/Feature Description

PageTurner is a curated book subscription that sends subscribers two to three hand-selected novels each month based on a reading profile questionnaire. The brand leans literary and sophisticated — their audience is avid readers who hate algorithm-picked recommendations. The team has been building on Shopify Dawn and is ready to create the full homepage template.

The previous developer left the project partway through and the theme has some issues: one test file they pushed had heading size values that Dawn rejected during theme check, causing the entire push to fail. The client needs a clean, validated homepage template with the correct heading hierarchy — the hero should have the largest heading, section titles should be prominent but secondary, and FAQ headings should be smaller. Pick heading sizes that create a clear visual hierarchy using the values Dawn supports.

The homepage should include all sections: hero, how-it-works (3 steps), tier picker (Reader $29/mo, Bibliophile $45/mo, Collector $69/mo), recent picks gallery, testimonials, FAQ with at least 4 questions, and email signup.

## Output Specification

Produce `templates/index.json` in the current working directory with all the sections above. Pay particular attention to heading sizes — use appropriate sizes that create a proper visual hierarchy. Include `heading_size` settings explicitly for at least 5 different sections.
