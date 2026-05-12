---
name: page-critical-review
description: Use this skill when the user wants a critical UX/conversion review of a homepage, product detail page, or landing page — phrases like "review my homepage", "critique this PDP", "review the URL", "tear down this page", "audit the landing page". Accepts a URL OR local theme files. Output is a structured ranked list of issues with reasoning + suggested fixes.
---

# Page critical review (homepage / PDP / landing)

A senior-eye review of a published or in-development page. Returns a prioritized issue list (P0 broken / P1 weakening conversion / P2 polish) with concrete fixes.

## When to use

- Page just shipped, before going live to traffic
- Page has been live but conversion or engagement is weaker than expected
- Pre-paid-traffic — checking before pushing budget against a URL

## Inputs the skill accepts

- A URL (preferred — review what real users see)
- A path to a Shopify theme repo (review the JSON templates + Liquid)
- Both (URL for live, repo for code-level fixes)

## Steps

### 1. Pull the live page

If a URL is given:
- Use `WebFetch` to grab text content
- If browser MCP is available, take a screenshot at desktop (1280×800) and mobile (375×812) — score visual hierarchy
- Note the rendering platform (Shopify, headless, etc.)

If a theme repo is given:
- Read `templates/<page>.json`
- Cross-reference referenced sections in `sections/`
- Read any custom CSS in `assets/custom.css`

### 2. Score against rubric

Score each dimension 1-5 (1 = blocking, 5 = best-in-class). Tag every issue P0/P1/P2.

**Hierarchy & first impression (weight 3x)**
- Above-the-fold value prop in <3 seconds?
- Single, clear primary CTA visible without scroll?
- Logo + nav legible? (font size, contrast)
- Hero image relevant or stock?

**Copy quality (weight 2x)**
- Headline: specific to brand or generic ("Welcome to our store")?
- Sub-copy: concrete benefit or vague vibe?
- Microcopy on buttons: action-oriented or "Click here"?
- Voice consistency across sections?

**Conversion mechanics (weight 3x for PDP, 2x for homepage)**
- CTA visible above fold AND repeated below
- Price clearly visible (and explained for subscriptions)
- Trust signals (guarantee, ratings, founder story) above the fold for PDP
- Friction in checkout flow (account required? tier picker clear?)

**Trust & objection handling (weight 2x)**
- Reviews / testimonials with names + photos > generic stars
- Return / refund policy linked clearly
- About / story element exists
- FAQ on the page or one click away

**Mobile (weight 2x for homepage, 3x for PDP)**
- All CTAs reachable thumb-friendly
- Images don't overflow
- Sticky elements (header, cart) don't block content
- Tap targets ≥ 44px

**Technical (weight 1x)**
- Page loads under 3s
- No broken images, dead links
- All anchor links work (`#tiers`, `#how-it-works`)
- Theme schema validates (run `shopify theme check` if repo given)

### 3. Format the output

Use this structure verbatim:

```
# Critical review: <page name> (<URL or path>)

## Verdict
<1-2 sentence overall — strengths + main gap>

## P0 — Ship-blockers (fix before next push)
- [Issue] — [why it matters] — [fix]

## P1 — Weakening conversion (fix this week)
- [Issue] — [why it matters] — [fix]

## P2 — Polish (fix when time allows)
- [Issue] — [why it matters] — [fix]

## Strengths to preserve
- [Specific things that work]

## Scores
| Dimension | Score | Note |
|---|---|---|
| Hierarchy | x/5 | |
| Copy | x/5 | |
| Conversion | x/5 | |
| Trust | x/5 | |
| Mobile | x/5 | |
| Technical | x/5 | |
| **Weighted total** | **x/100** | |
```

### 4. Suggest concrete fixes

For each P0/P1, provide actual code or copy. Don't say "improve the headline" — write 2-3 alternative headlines. Don't say "add testimonials" — provide 3 example testimonial cards in the brand's voice.

### 5. Visual cross-check

If you took screenshots, embed comparisons:
- "On mobile, the CTA falls below the fold at 375×812"
- "Hero image overlays the headline at certain widths — see screenshot"

## Specific patterns to watch for (subscription box brands)

- **Tier picker without prices** — common mistake; people bounce trying to figure out "what does this cost"
- **No "cancel anytime" near the CTA** — the #1 objection for subscription boxes
- **Hero copy that's generic** — "Quality you can trust" is meaningless; "A monthly box of gear, tools, and toys for the guy who'd rather be at the track" is specific
- **Recent drops gallery without context** — photos with no copy don't communicate value
- **No social proof above the fold** — testimonials at the bottom only catch the highly-motivated

## Specific patterns to watch for (PDP)

- **No subscription explainer near buy box** — people scroll for "what is this actually"
- **Single product image** — gallery should have 3-5 angles minimum
- **No size/tier comparison link** — users can't decide between options
- **Missing `cancel anytime` / `value guarantee` callout** above the buy button

## Cross-skill links

- After review, fixes often invoke: `subscription-homepage-build`, `shopify-landing-page`, or direct theme edits
- For voice-related issues: `brand-voice-extract`
- For email-side issues: `klaviyo-campaign-create`

## Reference example

Reviewing `gearheadbox.myshopify.com/products/apex` would surface:
- P0 if `/policies/refund-policy` is dead (link in pre-order banner)
- P1 if Apex's PDP has no third image (current state has 1)
- P2 if the "Not sure which tier?" image isn't loading
