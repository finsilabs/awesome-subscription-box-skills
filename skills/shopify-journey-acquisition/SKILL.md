---
name: shopify-journey-acquisition
description: Use this skill when the user wants to analyze where customers come from on their Shopify store — phrases like "channel attribution", "where is my traffic coming from", "best traffic source", "review my acquisition", "social vs paid vs organic", "referrer report". Pulls source/medium data via ShopifyQL, scores each channel by sessions / conv rate / AOV / revenue, and outputs a channel scoreboard plus where to invest more.
---

# Shopify journey acquisition analysis

Show where traffic and revenue come from at the channel and individual-source level. Score each by quality (conv rate, AOV) — not just volume — so the user can decide where to push spend or fix a leak.

## When to use

- Quarterly channel review
- Before deciding a media-budget allocation
- "Why aren't my [Meta / TikTok / SEO] dollars working?"
- After a campaign — measure incremental revenue from a referrer source
- Suspicion that organic / direct is silently the biggest driver

## Prerequisites

- Shopify MCP connected (`mcp__9bf46487-...__run-analytics-query`)
- For ROAS: ad spend numbers from outside Shopify (Meta MCP, manual input)
- Optional: target CAC / target ROAS from the user

## Steps

### 1. Top-level channel breakdown

```
FROM sessions
SHOW sessions, sessions_that_completed_checkout, conversion_rate
GROUP BY referrer_source
ORDER BY sessions DESC LIMIT 15
SINCE -30d UNTIL today
```

`referrer_source` typical values: `direct`, `social`, `search`, `email`, `unknown`, `referral`, sometimes a specific platform.

### 2. Revenue and AOV by channel

```
FROM sales
SHOW orders, total_sales, average_order_value
GROUP BY order_referrer_source
ORDER BY total_sales DESC LIMIT 15
SINCE -30d UNTIL today
```

### 3. Specific-source breakdown (named campaigns / utm sources)

```
FROM sales
SHOW orders, total_sales, average_order_value
GROUP BY order_referrer_source, order_referrer_name
ORDER BY total_sales DESC LIMIT 25
SINCE -30d UNTIL today
```

`order_referrer_name` exposes utm_source / utm_campaign. Filter to a single channel for deeper looks:

```
FROM sessions
SHOW sessions, sessions_that_completed_checkout, conversion_rate
WHERE referrer_source = 'social'
GROUP BY referrer_name
ORDER BY sessions DESC LIMIT 15
SINCE -30d UNTIL today
```

### 4. Trend per channel (find rising vs declining)

```
FROM sessions
SHOW sessions
GROUP BY referrer_source
TIMESERIES day SINCE -60d UNTIL today
```

Eyeball: is any channel collapsing or surging week-over-week?

### 5. Build the channel scoreboard

For each channel compute:

| Channel | Sessions | Conv rate | AOV | Orders | Revenue | Revenue / 1k sessions |
|---|---|---|---|---|---|---|
| Direct | … | … | … | … | … | … |
| Social | … | … | … | … | … | … |
| Search (organic) | … | … | … | … | … | … |
| Email | … | … | … | … | … | … |
| Paid (utm_source=meta) | … | … | … | … | … | … |
| Referral | … | … | … | … | … | … |

The **Revenue per 1k sessions** column is the channel-quality metric — it normalizes for volume so you can compare a small high-quality channel against a big low-quality one.

### 6. ROAS overlay (if paid spend is available)

If you have ad spend numbers (from Meta MCP or user input):

| Paid channel | Spend | Attributed revenue | ROAS | CAC (assuming 1 order = 1 customer) |
|---|---|---|---|---|
| Meta | $X | $Y | Y/X | X/orders |
| TikTok | $X | $Y | Y/X | X/orders |
| Google | $X | $Y | Y/X | X/orders |

Note: Shopify's last-touch attribution often UNDER-counts paid social and OVER-counts direct/search. Flag this caveat in the report.

### 7. Diagnose oddities

| Pattern | Likely cause | Action |
|---|---|---|
| Direct > 50% of revenue | Untracked traffic (paid clicks losing UTMs, dark social, branded search) | Audit UTM tagging on ads/email; treat direct as a partial proxy for paid+brand |
| One source has high sessions but low conv | Wrong audience or weak landing page | Run `page-critical-review` on the landing pages those clicks hit |
| One source has low sessions but high AOV | Underinvested winner — scale | Increase spend or investment in that channel |
| Email conv rate < 5% | Klaviyo flows weak / list cold | Audit flows with `klaviyo-flow-build` |
| Search organic flat / declining | SEO regression or de-indexing | Manual SEO check; sitemap, indexed pages |

### 8. Output

```markdown
# Acquisition · <Brand> · <date range>

## TL;DR
<2-3 sentences: top channel by revenue, top channel by quality, biggest opportunity>

## Channel scoreboard

| Channel | Sessions | Conv % | AOV | Orders | Revenue | $/1k sessions |
|---|---|---|---|---|---|---|
| … |

## Trend
<which channels are rising / declining vs. previous 30d>

## Top named sources
| utm_source / utm_campaign | Sessions | Conv % | Revenue |
|---|---|---|---|

## ROAS (if available)
<paid-channel ROAS table>

## What's working
- <Channel / source>: <metrics>, <why>

## What's broken
- <Channel / source>: <metrics>, <fix>

## Recommendations (prioritized)

### P0 — Fix this month
1. <Action> — <expected impact>

### P1 — Test next
1. <Action> — <expected impact>

### P2 — Reallocate
1. <Action> — <expected impact>

## Caveats
- Shopify last-touch attribution under-counts paid social / over-counts direct
- Sessions may include bots; cross-check with GA or CF analytics for sanity
```

### 9. Save

Write to `<repo>/journey-reports/acquisition-<YYYY-MM-DD>.md`.

## Cross-skill links

- `shopify-journey-funnel` — if a channel converts poorly, the leak is downstream
- `shopify-journey-cohort-retention` — channel × LTV (paid often acquires worse repeat customers)
- `ads-performance-analysis` — pair with paid-side metrics for ROAS truth
- `ads-calendar-plan` — to reallocate budget across channels
- `klaviyo-calendar-plan` — if email is underperforming
- `page-critical-review` — for landing-page-side fixes per channel

## Tradeoffs

- **Last-click vs first-click attribution** — Shopify is essentially last-non-direct touch. Paid social often gets undervalued because users click an ad → bounce → search the brand → convert from "search". For paid evaluation, lean on the ad platform's own attribution as a complement.
- **30d vs 90d window** — Use 30d for tactical decisions, 90d for strategic mix. Below 1k sessions/month, use 90d minimum.
- **utm hygiene matters more than the analysis** — If your ads aren't UTM-tagged consistently, the "social" bucket will be a black box. Recommend the user audit their ad UTMs as part of the action plan if data is messy.
