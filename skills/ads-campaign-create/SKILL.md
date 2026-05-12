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

Target 4-6 ads per ad set — fewer than 3 leaves Meta under-optimized; more than 8 spreads budget too thin during the learning phase.

### 7. Use catalog ads if applicable

For brands with large SKU catalogs, Dynamic Product Ads may outperform static creatives. Use `ads_catalog_get_catalogs()`, `ads_catalog_get_products()`, and `ads_catalog_get_product_sets()` to retrieve catalog data, then reference a `product_set_id` in the ad's targeting.

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

## Key tradeoffs

- **PAUSED start vs. ACTIVE start** — always paused; auto-activation risks budget burn on unreviewed creative.
- **CBO vs. ABO** — ABO for cold testing; CBO for scaling proven winners.
