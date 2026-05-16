---
name: subscription-store-build
description: 'Use this skill when the user wants to build a COMPLETE Shopify store for a subscription-box business from scratch — phrases like "create a Shopify store for my subscription box", "build me a subscription box store", "set up my monthly box shop", "I''m starting a subscription box business", "spin up a store for my box". This is the top-level orchestrator: it sequences theme scaffold → brand voice → tier products → subscriptions config → homepage → supporting pages → navigation → imagery → email automation, delegating each phase to a specialist skill. Use this whenever the request is the WHOLE store, not a single piece. If the user only wants one piece (just the homepage, just the emails), use the specific skill instead.'
---

# Subscription store build — orchestrator

Build a complete, launch-ready Shopify store for a subscription-box business. This skill does not do the work itself — it is the **conductor**. It establishes the right build order, hands each phase to a specialist skill, and keeps the pieces consistent (one brand voice, one palette, one set of tier handles) so the result feels like a single coherent store instead of a pile of parts.

A subscription-box store has dependencies a normal store doesn't: the homepage tier cards link to product pages that must already exist; the email flows reference products and pages by handle; the pre-order messaging has to appear in three places at once. Getting the order wrong means rework. This skill encodes the order that avoids that.

## When to use

- The user wants the **entire store**, not one component ("build my subscription box store")
- Greenfield or near-greenfield — a new business, or a rebrand
- The product is a recurring box with 1–4 tiers

If the user only wants one slice — just the homepage, just the Klaviyo flows, just a landing page — skip this orchestrator and invoke the specific skill directly. This skill is for the full sequence.

## The dependency chain

Build phases in this order. Each arrow is a hard dependency — the later phase needs an artifact the earlier one produced.

```
brand voice ─→ theme ─→ tier products ─→ subscriptions ─→ homepage ─→ pages ─→ nav ─→ imagery ─→ email ─→ QA
     │            │           │                              │          │
     │            │           └── handles (/products/apex) ───┴──────────┘  homepage + pages link here
     │            └── palette + color schemes feed every later visual phase
     └── voice.md + principles.md feed copy in theme, homepage, pages, AND email
```

Why this order:
- **Brand voice first** because every copy decision downstream (theme tagline, homepage hooks, email subject lines) should pull from one source. Skipping this makes the store sound like three different writers.
- **Products before homepage** because the homepage tier cards and the "compare tiers" sections link to `/products/<handle>`. Build the homepage first and you hard-code dead links.
- **Subscriptions config before launch** because a subscription box that sells one-time purchases is broken in a way that's invisible until checkout.
- **Imagery late** because you need the products and pages in place to know exactly which images you need (hero, 3 tier boxes, recent drops, page heroes). Generating images first means guessing.
- **Email last** because flows reference product handles and page URLs that must resolve.

## Phase-by-phase

For each phase, confirm scope with the user if unknown, then invoke the named skill. Don't reimplement what the specialist skill does — read it and follow it.

### Phase 0 — Scope intake

Before touching anything, get these from the user. They drive every later phase:

- **Brand name** and one-line description of the box
- **Category** (car gear, coffee, books, beauty…) — sets tone and imagery
- **Tiers**: name, monthly price, 1-line value prop for each (1–4 tiers)
- **Cadence**: monthly (default), weekly, quarterly
- **Launch state**: live now, or pre-order with a ship date
- **Store URL**: the `*.myshopify.com` handle
- **Existing brand site** (if any) — a URL to extract voice from

If the user hasn't given a tier structure, that's the one thing you must pin down before proceeding — everything keys off it.

### Phase 1 — Brand voice → `brand-voice-extract`

If the user has an existing brand/site, run `brand-voice-extract` on the URL to produce `~/.claude/brand-voice-vault/<brand>/`. If they're fully greenfield, interview them briefly (tone words, who the customer is, what they'd never say) and write the vault files by hand. Either way, the outcome is `voice.md`, `palette.json`, `principles.md` that every later phase reads.

### Phase 2 — Theme → `shopify-theme-create` (or `shopify-theme-clone`)

Greenfield: `shopify-theme-create` scaffolds Dawn and applies the palette.
Existing theme to keep: `shopify-theme-clone` pulls it down for local editing.

Output: a versioned Dawn theme in the working directory, color schemes wired to the brand palette.

### Phase 3 — Tier products → `shopify-product-with-images`

Create one Shopify product per tier. Use `shopify-product-with-images` so each gets AI-generated box imagery and a PDP template. Set the product handles deliberately and write them down — `pit-stop`, `apex`, `podium`, etc. — because the homepage and emails will reference them.

Output: N subscription products, each with a handle, imagery, and a `product.<type>.json` template.

### Phase 4 — Subscriptions config

Configure Shopify Subscriptions (selling plans) on each tier product so the box actually recurs. Create a selling-plan group per cadence and attach it to every tier. Without this, checkout sells a one-time purchase.

If the Shopify MCP is connected, use `sellingPlanGroupCreate` + `productUpdate`. If not, direct the user to **Shopify admin → Settings → Subscriptions**.

### Phase 5 — Homepage → `subscription-homepage-build`

Now that products exist, build `templates/index.json`. `subscription-homepage-build` produces the hero → how-it-works → tier picker → recent drops → testimonials → FAQ → email-capture layout. The tier cards link to the `/products/<handle>` pages from Phase 3.

### Phase 6 — Supporting pages → `shopify-landing-page`

Subscription boxes need a predictable set of pages. Build each with `shopify-landing-page`:

- **How it works** — the cadence explained (pick → curate → ship)
- **About** — the human curation story
- **Gift** — gifting is a major acquisition channel for boxes
- **FAQ** — objection handling (cancellation, value guarantee, shipping)
- **Policies** — shipping, refund, subscription terms (Shopify policy pages)

### Phase 7 — Navigation

Wire the header and footer menus to the pages and the tier collection. Header: How it works, Tiers, Gift, FAQ. Footer: policies + about. If launching as pre-order, the announcement bar carries the ship-date message (not the homepage hero).

### Phase 8 — Imagery

With every page and product in place, you know the exact image manifest. Generate the set in one batch via the project's Nano Banana script (`scripts/generate_images.py` reading a prompts JSON). Keep one consistent visual treatment across all of them — same palette, same lighting, same era — so the store reads as one brand. See `references/build-playbook.md` for the image manifest and the asset-fallback pattern when the Shopify Files MCP is unavailable.

### Phase 9 — Email automation → `klaviyo-flow-build` + `klaviyo-campaign-create`

Stand up the lifecycle flows (welcome, pre-order series, order confirmation, shipped, browse/checkout abandonment, cancellation save, win-back, post-purchase) with `klaviyo-flow-build`, and any launch campaigns with `klaviyo-campaign-create`. Email copy pulls from the same brand vault; email imagery matches Phase 8.

Optionally also run `klaviyo-calendar-plan` for a forward calendar and the `ads-*` skills for paid acquisition.

### Phase 10 — QA → `page-critical-review`

Run `page-critical-review` on the homepage and each tier PDP. Fix the ranked issues. Confirm: tier cards click through, prices are right, subscription shows on the buy box, pre-order messaging is consistent, no dead links.

## Keeping phases consistent

The failure mode of a multi-phase build is drift — phase 9 forgets what phase 2 decided. Hold these invariant across every phase:

- **One palette.** The `palette.json` from Phase 1 drives theme color schemes, generated imagery, and email templates. Don't let a phase invent its own colors.
- **One set of tier handles.** Decided in Phase 3, referenced verbatim everywhere after. Keep them written down.
- **One voice.** Theme copy, page copy, and email copy all read `voice.md`. The store should sound like one person.
- **Pre-order in three places.** If launching pre-order: announcement bar, every tier PDP (a banner above `main`), and the email welcome series all need the same ship-date line. Miss one and the customer gets mixed signals.
- **Imagery is theme-asset-portable.** If the Shopify Files MCP is down, drop images into the theme `assets/` folder and use the `image_asset` fallback pattern (see `references/build-playbook.md`) rather than blocking the whole build.

## A realistic build is iterative

Don't try to land all ten phases in one perfect pass. Real builds loop: scaffold → push → look at it in the browser → fix → push again. After Phase 5 and again after Phase 7, push the theme to a preview/unpublished theme and actually look at it (browser MCP or a preview URL). Visual bugs — misaligned cards, invisible buttons, text overlap — are invisible in JSON and obvious on screen.

## Reference

`references/build-playbook.md` — the concrete artifact checklist, the image manifest, the `image_asset` theme-asset fallback pattern, schema gotchas, and the canonical example (the Gear Head Box build at `~/dev/gearheadbox/`).

## Cross-skill map

| Phase | Skill |
|---|---|
| Brand voice | `brand-voice-extract` |
| Theme | `shopify-theme-create`, `shopify-theme-clone` |
| Products | `shopify-product-with-images` |
| Homepage | `subscription-homepage-build` |
| Pages | `shopify-landing-page`, `shopify-blog-post` |
| Email | `klaviyo-flow-build`, `klaviyo-campaign-create`, `klaviyo-calendar-plan` |
| Ads | `ads-brief-create`, `ads-campaign-create`, `ads-calendar-plan` |
| QA | `page-critical-review` |
| Analytics (post-launch) | `shopify-journey-*` |
