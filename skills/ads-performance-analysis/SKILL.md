---
name: ads-performance-analysis
description: Use this skill when the user wants to analyze paid ads performance — phrases like "review ad performance", "analyze the campaign", "why aren't my ads working", "audit my ads", "ads performance report". Pulls metrics from the Meta Ads MCP, compares to industry benchmarks, identifies what's working/breaking, and outputs a prioritized recommendation list.
---

# Ads performance analysis

Pull live metrics from Meta Ads, compare to industry benchmarks, identify trends and anomalies, and output a prioritized "what to change next" list. Designed to be run weekly during a campaign's life.

## When to use

- Campaign ≥ 48 hours old (past the Meta learning phase)
- Weekly performance reviews or "something's broken" investigations (CPA spike, volume drop)
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

See `ADS-BENCHMARKS.md` for reference benchmark ranges by metric and industry tier. If that file does not yet exist in the project, create it from the benchmark table below and remove it from this file to reduce per-run token cost.

| Metric | Below avg | Avg | Top 25% |
|---|---|---|---|
| CTR (link click) | < 0.8% | 1.0–1.5% | > 2% |
| CPM | > $25 | $15–25 | < $12 |
| CPC | > $2.50 | $1.50–2.50 | < $1.20 |
| ROAS (e-commerce) | < 1.5 | 2.0–3.0 | > 4.0 |
| Frequency (cap warning) | > 4 | 2–3 | 1.5–2 |

### 4. Look for anomalies

```python
ads_insights_anomaly_signal(...)         # Meta auto-detects unusual patterns
ads_insights_performance_trend(...)      # WoW / MoM trend
ads_insights_auction_ranking_benchmarks(...)  # quality / engagement / conversion ranks
```

### 5. Identify the bottleneck

Use this decision tree. Each branch also notes the likely root cause and fix.

```
Is CTR < benchmark?
  YES → Creative problem.
        Likely cause: weak hook, generic creative, or audience too cold for offer.
        Fix: new hook variants, different format, or warmer audience / simpler offer.
  NO  ↓

Is CPC normal but CPA high?
  YES → Landing-page or offer problem.
        Likely cause: LP / offer mismatch, or poor mobile UX.
        Fix: critical review of LP; mobile audit if mobile CPA >> desktop CPA.
  NO  ↓

Is frequency > 3?
  YES → Audience saturation.
        Likely cause: same users repeatedly seeing same ads.
        Fix: refresh creative, expand audience, or increase budget for more reach.
  NO  ↓

Is ROAS < target despite okay CPA?
  YES → AOV / pricing issue.
        Likely cause: ROAS plateau from audience exhaustion, or low order value.
        Fix: new lookalikes / broader interests; look at upsell on the Shopify side.
  NO  ↓

Is spend not pacing?
  YES → Bid too low.
        Fix: move from cap bid to lowest-cost-without-cap.
  NO  ↓

Hit your CPA goal? → Scale (20–30%/week budget bump)
```

### 6. Format the output

See `ADS-REPORT-TEMPLATE.md` for the full report structure. If that file does not yet exist, create it from the template below and remove it from this file to reduce per-run token cost.

```markdown
# Ads performance · <Brand> · <date range>

## TL;DR
<2–3 sentences: spent $X, drove Y conversions at $Z CPA, ROAS A.B. Best variant: X. Biggest issue: Y.>

## Headline metrics

| Metric | Value | vs. last period | vs. industry |
|---|---|---|---|
| Spend | $X | +Y% | — |
| CTR | X% | +Y pp | <verdict> |
| CPA | $X | +Y% | <verdict> |
| ROAS | X | +Y% | <verdict> |

## What's working
- <Ad/variant> — <metric>, <diagnosis>

## What's breaking
- <Ad/variant> — <metric>, <diagnosis>, <fix>

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
<Anything requiring follow-up from the user>
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

- **Review cadence** — Don't tweak during the learning phase (first 48–72 hours per ad set). Weekly is the sweet spot; never go more than 7 days without reviewing.
- **Statistical significance** — Wait for ≥ 50 conversions per ad set before declaring a winner. < 20 conversions = noise.

## Reference example

For Gear Head Box at week 2 of launch ads:
- $2,000 spent, 38 conversions at $52.6 CPA (target was $50)
- ROAS 1.47 vs. target 2.0 — too low to scale
- Best variant: "Cold Lookalike, Hook 'For the guy who'd rather be at the track', square image"
- P0 fix: Pause two creatives at frequency > 5; rebrief 3 new hooks targeting Apex tier specifically
