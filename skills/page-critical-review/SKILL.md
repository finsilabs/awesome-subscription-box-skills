---
name: page-critical-review
description: Performs a senior-eye critical UX and conversion review of a homepage, product detail page, or landing page. Use when a user says "review my homepage", "critique this PDP", "review the URL", "tear down this page", or "audit the landing page". Accepts a URL or local Shopify theme files and outputs a structured ranked issue list (P0/P1/P2) with reasoning and concrete suggested fixes.
---

# Page critical review (homepage / PDP / landing)

Returns a prioritized issue list (P0 broken / P1 weakening conversion / P2 polish) with concrete fixes for any published or in-development page.

## Inputs the skill accepts

- A URL (preferred — review what real users see)
- A path to a Shopify theme repo (review the JSON templates + Liquid)
- Both (URL for live, repo for code-level fixes)

## Steps

### 1. Pull the live page

If a URL is given:
- Use `WebFetch` to grab text content
- If `WebFetch` fails (timeout, 4xx/5xx, redirect loop): note the failure, flag it as a P0 Technical issue, and proceed with any repo files provided. If no repo is given, halt and ask the user for an accessible URL or local files.
- If the URL returns a redirect (301/302), follow to the final destination and note the redirect chain.
- If browser MCP is available, take a screenshot at desktop (1280×800) and mobile (375×812) — score visual hierarchy
- Note the rendering platform (Shopify, headless, etc.)

If a theme repo is given:
- Read `templates/<page>.json` — if missing, note the gap and ask which template file to use
- Cross-reference referenced sections in `sections/`
- Read any custom CSS in `assets/custom.css` (skip silently if absent)
- If `shopify theme check` is available in the environment, run it and include schema errors in the Technical dimension

### 2. Score against rubric

Score each dimension 1-5 (1 = blocking, 5 = best-in-class). Tag every issue P0/P1/P2.

**Hierarchy & first impression (weight 3x)** — above-fold value prop readable in <3s; single clear primary CTA visible without scroll; logo + nav legible; hero image relevant (not stock).

**Copy quality (weight 2x)** — headline specific to brand (not generic); sub-copy concrete benefit (not vague vibe); button microcopy action-oriented; voice consistent across sections.

**Conversion mechanics (weight 3x PDP / 2x homepage)** — CTA above fold AND repeated below; price clearly visible (explained for subscriptions); trust signals above fold on PDP; no unnecessary checkout friction.

**Trust & objection handling (weight 2x)** — reviews with names + photos (not generic stars); return/refund policy linked; about/story element exists; FAQ on page or one click away.

**Mobile (weight 2x homepage / 3x PDP)** — tap targets ≥ 44px; images don't overflow; sticky elements don't block content.

**Technical (weight 1x)** — page loads under 3s; no broken images or dead links; anchor links work; theme schema validates.

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

For every P0 and P1 issue, provide actual copy rewrites or code snippets — never say "improve the headline" without showing the rewrite.

**Example P0 fix — no CTA above fold:**
```liquid
{%- comment -%} In sections/hero.liquid, add before closing </div> {%- endcomment -%}
<a href="{{ section.settings.cta_url }}" class="btn btn--primary btn--large">
  {{ section.settings.cta_label | default: 'Shop Now' }}
</a>
```

**Example P0 fix — generic headline:**
Before: "Welcome to our store"
After: "[Brand name] — [specific benefit, e.g., 'SPF 50 sunscreen that doesn't leave a white cast']"

**Example P1 fix — missing trust signal above fold on PDP:**
```liquid
{%- comment -%} In sections/product-template.liquid, directly below .product__price {%- endcomment -%}
<div class="trust-bar">
  <span>⭐ {{ product.metafields.reviews.rating }} ({{ product.metafields.reviews.count }} reviews)</span>
  <span>🔒 Free returns within 30 days</span>
</div>
```

**Example P2 fix — vague button microcopy:**
Before: "Submit"
After: "Add to Bag — Free Shipping Over $50"

**Issue calibration guide:**
- **P0**: The page cannot convert or is actively broken — missing primary CTA, broken checkout link, hero image 404, no price displayed on PDP, page returns an error.
- **P1**: Conversion is measurably harmed — value prop unclear above fold, no trust signals on PDP, CTA only appears below the fold, mobile tap targets too small, no return policy visible.
- **P2**: Experience is degraded but not a blocker — inconsistent font sizing, minor copy vagueness, low-contrast secondary text, missing alt text, slightly slow LCP.

### 5. Error handling and edge cases

- **URL inaccessible**: Flag as P0 Technical, state the HTTP status or error, and either proceed with repo files or ask for a corrected URL.
- **Password-protected Shopify store**: Inform the user that `WebFetch` cannot access the page behind a storefront password and request either a preview URL or theme files.
- **Repo missing `templates/` folder**: Ask the user to confirm the repo root path before proceeding.
- **No screenshots available**: Skip visual hierarchy scoring notes that depend on screenshots; document the limitation in the Verdict section.
- **Ambiguous page type**: If the URL or path doesn't make clear whether it's a homepage, PDP, or landing page, ask before applying weighted scores (weights differ by page type).
