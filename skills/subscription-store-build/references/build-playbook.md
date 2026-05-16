# Subscription store build — playbook

Concrete reference for the orchestrator. Read this when you need the artifact
checklist, the image manifest, the asset-fallback pattern, or schema gotchas.

## Table of contents

1. Artifact checklist (what "done" looks like)
2. Image manifest
3. The `image_asset` theme-asset fallback pattern
4. Subscriptions / selling-plan notes
5. Schema gotchas
6. Canonical example: Gear Head Box

---

## 1. Artifact checklist

A finished subscription-box store has all of this. Use it as a definition of done.

**Theme**
- [ ] Dawn-based theme, versioned in git, in the working directory
- [ ] `config/settings_data.json` color schemes wired to the brand palette
- [ ] `assets/custom.css` for brand component styling
- [ ] Pushed to a preview/unpublished theme and visually checked

**Products**
- [ ] One product per tier, deliberate handles (written down)
- [ ] Each tier has box imagery and a PDP template
- [ ] Each tier has a selling plan attached (recurs, not one-time)

**Templates**
- [ ] `templates/index.json` — homepage
- [ ] `templates/product.<type>.json` — tier PDP
- [ ] `templates/page.how-it-works.json`, `page.about.json`, `page.gift.json`
- [ ] `templates/404.json` styled on-brand

**Pages** (Shopify Page records)
- [ ] How it works, About, Gift, FAQ
- [ ] Policy pages: shipping, refund, subscription terms

**Navigation**
- [ ] Header menu: How it works, Tiers, Gift, FAQ
- [ ] Footer menu: policies, About
- [ ] Announcement bar (carries pre-order ship date if pre-launch)

**Imagery** — see manifest below

**Email** (Klaviyo)
- [ ] Lifecycle flows live (welcome, order, shipped, abandonment, save, win-back)
- [ ] Templates brand-styled with hero images
- [ ] Launch campaign(s) drafted

---

## 2. Image manifest

A 3-tier subscription box needs roughly this set. Generate them in one batch
with a single consistent visual treatment (palette, lighting, era) so the store
looks like one brand.

| Image | Used on | Ratio |
|---|---|---|
| Hero / garage shot | homepage hero | 16:9 |
| Tier box × N (one per tier) | homepage tier cards, PDPs | 1:1 |
| Recent drop × 3 | homepage "recent drops" collage | 1:1 |
| How-it-works hero | how-it-works page | 16:9 |
| Gift hero | gift page | 16:9 |
| 404 image | 404 template | 16:9 |
| Email hero × N (one per send) | Klaviyo templates | 16:9 |

Generate via `scripts/generate_images.py` reading a prompts JSON (Nano Banana /
`gemini-2.5-flash-image`). Keep prompts consistent: same palette hex values,
same lighting language ("hard side-light", "35mm grain"), same era cues, "no
people, no readable text" to avoid garbled lettering.

Email hero images: upload directly to Klaviyo's image library
(`POST /api/image-upload/`, multipart `file`) — Klaviyo returns a stable
CloudFront URL that survives theme re-pushes. Don't depend on Shopify-theme-asset
URLs for email images; the version hash changes on every push.

---

## 3. The `image_asset` theme-asset fallback pattern

**Problem:** Dawn section JSON references images as `shopify://shop_images/<file>.png`,
which only resolves if the file is in the store's Files library. Uploading there
needs the Shopify MCP / Admin API. When that's unavailable, the build stalls.

**Solution:** put the images in the theme's own `assets/` folder and add an
`image_asset` text setting to the sections that need them, rendered via
`{{ filename | asset_url }}` when no Files-library image is picked.

For each affected section (`image-banner`, `image-with-text`, and the
`multicolumn` / `collage` block schemas):

1. Add a text setting to the section/block schema:
   ```json
   { "type": "text", "id": "image_asset",
     "label": "Theme asset filename (fallback)",
     "info": "Used when no image is picked. e.g. hero.png" }
   ```

2. Add a Liquid branch that renders the asset when the picker image is blank:
   ```liquid
   {%- elsif section.settings.image_asset != blank -%}
     <img src="{{ section.settings.image_asset | asset_url }}" alt=""
          style="width:100%;height:100%;object-fit:cover;">
   ```

3. In the template JSON, use `"image_asset": "hero.png"` instead of
   `"image": "shopify://shop_images/hero.png"`.

This makes the whole imagery phase independent of Files-library access. The
images ship inside the theme and resolve from the theme CDN.

**Product media variant:** the tier PDP gallery pulls from `product.media`
(the Shopify product object), not section settings. To override it with a
theme asset, branch in `main-product.liquid` on `product.handle`:
```liquid
{%- liquid
  case product.handle
    when 'apex'  assign tier_asset = 'tier_apex.png'
  endcase
-%}
{%- if tier_asset != '' -%}
  <img src="{{ tier_asset | asset_url }}" alt="{{ product.title }}">
{%- else -%}
  {% render 'product-media-gallery' %}
{%- endif -%}
```

---

## 4. Subscriptions / selling-plan notes

A subscription box must recur. Configure Shopify Subscriptions:

- One **selling-plan group** per cadence (monthly / weekly / quarterly).
- Attach the group to **every** tier product.
- Via API: `sellingPlanGroupCreate`, then `productUpdate` to attach.
- Without API access: **Shopify admin → Settings → Subscriptions**, or the
  Shopify Subscriptions app.

Verify in QA: the tier PDP buy box should show the subscription option, and
checkout should create a subscription contract, not a one-time order.

---

## 5. Schema gotchas

From real builds — pre-validate to avoid push failures:

- **Range steps:** `card_shadow_blur` is a multiple of 5; `page_width` step 100;
  `padding_top`/`padding_bottom` step 4; `buttons_radius` step 2. An off-step
  value rejects the whole `settings_data.json`.
- **`email-signup-banner`** is restricted to the `password` template — use the
  `newsletter` section on the homepage.
- **`collapsible-content` `row_content`** rejects `<code>`. Use `<strong>`.
- **Heading sizes:** valid are `h2 / h1 / h0 / hxl / hxxl`.
- **`multicolumn` `image_ratio`:** `adapt / portrait / square / circle`.
- **Announcement bar color:** Dawn's `utility-bar` wrapper uses the
  section-level `color_scheme`; set it on the announcement-bar section in
  `header-group.json`, not globally.
- **Theme push to live** needs `--allow-live`; prefer pushing to an
  unpublished/preview theme and previewing before publishing.
- **Clickable cards:** to make a whole `multicolumn` tier card a link (not just
  the "Subscribe" text), wrap the card in an `<a>` when the block has a link,
  and convert the inner link to a `<span>` to avoid nested `<a>` elements.

---

## 6. Canonical example: Gear Head Box

`~/dev/gearheadbox/` is a complete worked example of this entire orchestration —
a vintage-racing-themed monthly car-gear box with three tiers (Pit Stop $54,
Apex $84, Podium $119).

Worth studying:
- `templates/index.json` — the 9-section homepage
- `templates/product.subscription.json` — tier PDP with pre-order banner
- `sections/image-banner.liquid`, `image-with-text.liquid`, `multicolumn.liquid`,
  `collage.liquid` — the `image_asset` fallback pattern in place
- `sections/main-product.liquid` — the product-handle media override
- `scripts/generate_images.py` + `scripts/prompts/*.json` — batch imagery
- `scripts/generate_email_templates.py` — the email template shell
- `scripts/klaviyo_*.py` — push templates, flows, campaigns; upload images;
  rebuild flows (note: Klaviyo clones template HTML into flow messages, so
  updating a template means delete-and-recreate the draft flow)
- `design-system/gear-head-box/MASTER.md` — the design system

The Gear Head Box build also surfaced the key operational lessons baked into
this skill: build products before the homepage, keep one palette, push to a
preview theme and look at it, and don't let the Shopify-MCP auth state block
the imagery phase (use the `image_asset` fallback).
