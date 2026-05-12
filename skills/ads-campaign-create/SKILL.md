---
name: ads-campaign-create
description: Use this skill to create paid ads campaigns on Meta (Facebook/Instagram) — phrases like "create a Meta ads campaign", "launch ads on Facebook", "build the campaign on Meta", "spin up the ad set". Creates campaign + ad sets + ads via the Meta Ads MCP tools, generates creative imagery via Nano Banana, and applies the brief from ads-brief-create if provided.
---

# Meta ads campaign creation

End-to-end Meta (Facebook/Instagram) ads campaign: campaign → ad set → ads, with creative imagery generated via Nano Banana and copy/targeting from the brief.

## When to use

- After a brief is approved (see `ads-brief-create`)
- Direct request to launch ads on Meta
- Spinning up retargeting ad sets, A/B testing variants

## Prerequisites

- Meta Ads MCP connected with `ads_create_campaign` / `ads_create_ad_set` / `ads_create_ad` write tools
- An ad account ID (use `ads_get_ad_accounts` to discover)
- A Facebook Page ID for the brand (use `ads_get_pages_for_business`)
- Approved brief — ideally from `ads-brief-create` skill output
- `GOOGLE_API_KEY` in `.env` for creative imagery (Nano Banana)

## Steps

### 1. Discover account context

```python
ads_get_ad_accounts()           # find ad_account_id
ads_get_pages_for_business()    # find page_id for the brand
ads_insights_industry_benchmark(...)  # get industry CPM / CTR / CPA benchmarks
```

Use the benchmarks to set realistic budget and bid expectations.

### 2. Translate brief to platform structure

Meta's hierarchy: **Campaign → Ad Set → Ad**.

| Brief element | Maps to |
|---|---|
| Objective | Campaign `objective` (OUTCOME_SALES, OUTCOME_LEADS, OUTCOME_TRAFFIC, OUTCOME_AWARENESS, OUTCOME_ENGAGEMENT, OUTCOME_APP_PROMOTION) |
| Audience | Ad Set `targeting` (countries, age range, interests, custom audiences) |
| Budget | Ad Set `daily_budget` or `lifetime_budget` |
| Schedule | Ad Set `start_time` / `end_time` |
| Placement | Ad Set `placements` (auto = recommended) |
| Hooks/copy/images | Ads (one Ad per creative variant) |
| Landing URL | Ad `link_url` |

### 3. Generate creative imagery

Use Nano Banana per the asset specs in the brief. Aspect ratios for Meta:

| Placement | Ratio | Resolution |
|---|---|---|
| Feed (square) | 1:1 | 1080×1080 |
| Stories / Reels | 9:16 | 1080×1920 |
| Feed (vertical) | 4:5 | 1080×1350 |
| Right-column (legacy) | 1.91:1 | 1200×628 |

See `./scripts/generate_images.py` for the generation pattern.

After generation, upload to Meta's CDN. Meta accepts public HTTPS URLs OR you can use their `adimage` upload — easier path is to host on a CDN you control (Shopify Files, S3, etc.).

### 4. Create the campaign

```python
ads_create_campaign(
    ad_account_id="<id>",
    name="<Brand> · <Campaign name> · <YYYY-MM>",
    objective="OUTCOME_SALES",  # or LEADS / TRAFFIC / AWARENESS
    status="PAUSED",  # always create paused, activate manually after review
    special_ad_categories=[],  # set if applicable (housing, employment, credit)
)
```

**Critical**: ALWAYS create `status="PAUSED"`. Do not auto-activate. Activation should be a deliberate human action via `ads_activate_entity()` after creative + targeting QA.

### 5. Create ad sets (one per audience variant)

```python
ads_create_ad_set(
    ad_account_id="<id>",
    campaign_id="<from step 4>",
    name="<Audience name>",
    daily_budget=5000,  # in cents (= $50)
    bid_strategy="LOWEST_COST_WITHOUT_CAP",  # or LOWEST_COST_WITH_BID_CAP
    optimization_goal="OFFSITE_CONVERSIONS",  # match objective
    targeting={
        "geo_locations": {"countries": ["US"]},
        "age_min": 38,
        "age_max": 55,
        "genders": [1],  # 1=male, 2=female, omit for all
        "interests": [{"id": "...", "name": "..."}],
        "custom_audiences": [{"id": "..."}],
        "publisher_platforms": ["facebook", "instagram"],
        "facebook_positions": ["feed", "story", "reels"],
        "instagram_positions": ["stream", "story", "reels", "explore"],
    },
    start_time="2026-08-04T13:00:00+00:00",
    status="PAUSED",
)
```

Best-practice budget rule of thumb for cold audiences: start at $30-50/day per ad set; scale 20-30% every 3-5 days if hitting CPA target.

### 6. Create ads (one per creative variant)

For each hook/image combination in the brief:

```python
ads_create_ad(
    ad_account_id="<id>",
    ad_set_id="<from step 5>",
    name="<Hook name> · <Image variant>",
    creative={
        "object_story_spec": {
            "page_id": "<from step 1>",
            "link_data": {
                "image_url": "<CDN URL>",
                "link": "<landing URL with UTM>",
                "message": "<primary text from brief>",
                "name": "<headline>",
                "description": "<description>",
                "call_to_action": {"type": "SUBSCRIBE", "value": {"link": "<landing URL>"}},
            },
        },
    },
    status="PAUSED",
)
```

### 7. Use catalog ads if applicable

For DTC brands with many SKUs, Dynamic Product Ads via catalog are higher-ROI than static creatives:

```python
ads_catalog_get_catalogs(...)
ads_catalog_get_products(...)
ads_catalog_get_product_sets(...)
# Then use product_set_id in the ad's targeting
```

For subscription boxes with 3-5 tier SKUs, static creatives usually outperform catalog ads — the variation is in the messaging, not the inventory.

### 8. Set up reporting baselines

Tag the campaign with a UTM convention so it's queryable in Klaviyo/GA4:
- `utm_source=meta`
- `utm_medium=paid`
- `utm_campaign=<campaign_slug>`
- `utm_content=<ad_variant_slug>`

### 9. Hand off to user

Output:
- Campaign ID + Meta Ads Manager URL
- Number of ad sets and ads created
- Total daily budget across all ad sets
- All entities are in PAUSED status — user reviews + activates via `ads_activate_entity`

## Pre-launch checklist (do not activate without all of these)

- [ ] Brief reviewed and approved
- [ ] All creative assets meet platform spec (no text > 20% of image, etc.)
- [ ] Landing page UTMs match the campaign config
- [ ] Pixel installed and firing on the LP
- [ ] Custom audiences defined for retargeting later
- [ ] Frequency cap set (typically 3-5 per week per user)
- [ ] Daily budget cap respects total campaign budget
- [ ] Excluded audience: existing subscribers, recent buyers
- [ ] At least 3 creative variants per ad set (Meta auto-optimizes)

## Cross-skill links

- `ads-brief-create` — must come first
- `shopify-product-with-images` — for the Nano Banana imagery generation pattern
- `ads-performance-analysis` — for after launch
- `klaviyo-calendar-plan` — coordinate ads + email cadence

## Tradeoffs

- **PAUSED start vs. ACTIVE start** — always paused. Auto-activation is a recipe for budget burn on bad creative.
- **Many ads per ad set vs. few** — Meta's algo wants variety in the first 48h. 4-6 ads per ad set is the sweet spot. < 3 = under-optimized; > 8 = budget gets spread too thin in the learning phase.
- **CBO vs. ABO** — Campaign Budget Optimization (CBO) lets Meta distribute budget across ad sets. Ad Set Budget Optimization (ABO) gives you control. ABO for cold testing; CBO for scaling proven winners.
- **Catalog ads vs. static creatives** — catalog is the win for 50+ SKU brands. Subscription/single-tier brands win with static.

## Embedded scripts

- `./scripts/generate_images.py` — Nano Banana generator for ad creative
- `./scripts/upload_staged.py` — Shopify CDN uploader (Meta also accepts public HTTPS URLs from any CDN)

## Reference example

For Gear Head Box launch:
- 1 campaign (OUTCOME_SALES) with $200/day total budget
- 3 ad sets — Cold Lookalike, Cold Interest-stack, Retargeting
- 5 ads per cold ad set, 3 ads in retargeting
- All paused on creation, activated after creative review

## Embedded in this skill folder

Scripts (copy to your project's `scripts/` directory and run with `uv run`):
- `scripts/generate_images.py`
- `scripts/remove_background.py`
- `scripts/upload_staged.py`
