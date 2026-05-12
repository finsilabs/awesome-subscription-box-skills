---
name: ads-performance-analysis
description: Use this skill when the user wants to analyze paid ads performance — phrases like "review ad performance", "analyze the campaign", "why aren't my ads working", "audit my ads", "ads performance report". Pulls metrics from the Meta Ads MCP, compares to industry benchmarks, identifies what's working/breaking, and outputs a prioritized recommendation list.
---

# Ads performance analysis

Pull live metrics from Meta Ads, compare to industry benchmarks, identify trends and anomalies, and output a prioritized "what to change next" list. Designed to be run weekly during a campaign's life.

## When to use

- Campaign has been running ≥ 48 hours (the Meta learning phase)
- Weekly performance reviews
- "Something's broken" investigations (CPA spike, drop in volume)
- Pre-scaling decisions ("can we 2x this ad set?")

## Prerequisites

- Meta Ads MCP with insights tools (`ads_insights_*`, `ads_get_ad_entities`)
- Active campaigns to analyze
- Optional: brand revenue data (from Shopify) for true ROAS calculation

## Steps

### 1. Pull the campaign list

```python
ads_get_ad_entities(
    ad_account_id="<id>",
    entity_type="campaign",
    fields=["id", "name", "status", "objective", "daily_budget"],
)
```

If user specifies a campaign, scope to that. Otherwise pull everything active.

### 2. Get core metrics

For each campaign / ad set / ad:

```python
ads_insights_advertiser_context(
    ad_account_id="<id>",
    level="ad",  # or campaign / ad_set
    date_preset="last_7d",  # or last_14d / last_28d
    metrics=["impressions", "reach", "clicks", "ctr", "cpc", "cpm",
             "spend", "conversions", "cost_per_conversion", "roas"],
)
```

### 3. Compare to industry benchmarks

```python
ads_insights_industry_benchmark(
    ad_account_id="<id>",
    industry="<closest match>",  # e.g., e-commerce, subscription, fitness
)
```

Common Meta benchmarks (rough reference, validate via the API):

| Metric | Below avg | Avg | Top 25% |
|---|---|---|---|
| CTR (link click) | < 0.8% | 1.0-1.5% | > 2% |
| CPM | > $25 | $15-25 | < $12 |
| CPC | > $2.50 | $1.50-2.50 | < $1.20 |
| ROAS (e-commerce) | < 1.5 | 2.0-3.0 | > 4.0 |
| Frequency (cap warning) | > 4 | 2-3 | 1.5-2 |

### 4. Look for anomalies

```python
ads_insights_anomaly_signal(...)         # Meta auto-detects unusual patterns
ads_insights_performance_trend(...)      # WoW / MoM trend
ads_insights_auction_ranking_benchmarks(...)  # quality / engagement / conversion ranks
```

### 5. Identify the bottleneck

Use this decision tree:

```
Is CTR < benchmark?
  YES → Creative problem. Test new hooks/images.
  NO  ↓

Is CPC normal but CPA high?
  YES → Landing-page or offer problem. Use page-critical-review on the LP.
  NO  ↓

Is frequency > 3?
  YES → Audience saturation. Refresh audience or increase budget for more reach.
  NO  ↓

Is ROAS < target despite okay CPA?
  YES → AOV / pricing issue. Look at upsell on the Shopify side.
  NO  ↓

Hit your CPA goal? → Scale (20-30%/week budget bump)
```

### 6. Format the output

```markdown
# Ads performance · <Brand> · <date range>

## TL;DR
<2-3 sentences: spent $X, drove Y conversions at $Z CPA, ROAS A.B. Best variant: X. Biggest issue: Y.>

## Headline metrics

| Metric | Value | vs. last period | vs. industry |
|---|---|---|---|
| Spend | $X | +Y% | — |
| Impressions | X | +Y% | — |
| CTR | X% | +Y pp | <verdict> |
| CPC | $X | +Y% | <verdict> |
| Conversions | X | +Y% | — |
| CPA | $X | +Y% | <verdict> |
| ROAS | X | +Y% | <verdict> |

## What's working

- **<Ad name / variant>**: <metric>, <why it's working>
- ...

## What's breaking

- **<Ad name / variant>**: <metric>, <why>, <fix>
- ...

## Recommendations (prioritized)

### P0 — Do this week
1. <Action> — <expected impact>

### P1 — Test next
1. <Action> — <expected impact>

### P2 — Polish
1. <Action> — <expected impact>

## Scaling decision
<Yes / No — and the supporting numbers>

## Open questions
<Things to investigate or get from user>
```

### 7. Save the analysis

Write to a project-level file the user can compare across weeks:
- `<repo>/ads-reports/<YYYY-MM-DD>.md`

Or to the brand vault:
- `~/.claude/brand-voice-vault/<brand>/ads-reports/<YYYY-MM-DD>.md`

### 8. Suggest next actions

Based on findings, link to:
- `ads-campaign-create` — for new variants / new audiences
- `ads-brief-create` — if rebriefing creative is needed
- `page-critical-review` — if the LP is the bottleneck

## Common findings and their fixes

| Finding | Likely cause | Fix |
|---|---|---|
| Low CTR | Weak hook, generic creative | New hook variants, different format |
| Low CTR + high CPM | Audience too cold for offer | Warmer audience or simpler offer |
| High CTR but low conversion | LP / offer mismatch | Critical review of LP |
| ROAS plateau | Audience exhausted | New lookalikes, broader interests |
| Frequency > 4 | Same users seeing same ads | Refresh creative, expand audience |
| Spend not pacing | Bid too low | Move from cap bid to lowest-cost-without-cap |
| Mobile CPA much higher than desktop | LP mobile UX | Mobile audit on LP |

## Decision rules for scaling

**Scale UP an ad set when:**
- ≥ 50 conversions in last 7 days at or below target CPA
- Frequency < 2.5
- Spending less than 30% of campaign daily budget

**Pause an ad set when:**
- < 1 conversion per $50 of last 3 days' spend at any reasonable CPA target
- Frequency > 5
- Quality / engagement rank in bottom 35%

## Cross-skill links

- `ads-campaign-create` — for new variants
- `ads-brief-create` — for rebriefing
- `ads-calendar-plan` — for adjusting cadence / budget plan
- `page-critical-review` — for LP-side issues
- `klaviyo-calendar-plan` — to coordinate ad pulse with email cadence

## Tradeoffs

- **Hourly vs. daily vs. weekly checks** — Don't tweak daily during the learning phase (first 48-72 hours per ad set). Weekly is the sweet spot for active campaigns. Don't go more than 7 days without reviewing.
- **Statistical significance vs. speed** — Wait for ≥ 50 conversions per ad set before declaring a winner in A/B tests. < 20 conversions = noise.

## Embedded scripts

- `./scripts/ads_pull_insights.py` — wrapper for `ads_insights_*` calls that outputs CSV for spreadsheet review

## Reference example

For Gear Head Box at week 2 of launch ads:
- $2,000 spent, 38 conversions at $52.6 CPA (target was $50)
- ROAS 1.47 vs. target 2.0 — too low to scale
- Best variant: "Cold Lookalike, Hook 'For the guy who'd rather be at the track', square image"
- P0 fix: Pause two creatives at frequency > 5; rebrief 3 new hooks targeting Apex tier specifically
