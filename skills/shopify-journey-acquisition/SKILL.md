---
name: shopify-journey-acquisition
description: Use this skill when the user wants to analyze where customers come from on their Shopify store — phrases like "channel attribution", "where is my traffic coming from", "best traffic source", "review my acquisition", "social vs paid vs organic", "referrer report". Pulls source/medium data via ShopifyQL, scores each channel by sessions / conv rate / AOV / revenue, and outputs a channel scoreboard plus where to invest more.
---

# Shopify journey acquisition analysis

Show where traffic and revenue come from at the channel and individual-source level. Score each by quality (conv rate, AOV) — not just volume — so the user can decide where to push spend or fix a leak.

## When to use

- Before or after deciding a media-budget allocation (quarterly review, campaign post-mortem)
- "Why aren't my [Meta / TikTok / SEO] dollars working?"
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

**Validation:** If the query returns 0 rows, check store connectivity and widen the date range to `-90d`. If `unknown` or `direct` accounts for >60% of sessions, flag a UTM hygiene issue immediately — note it in the report and do not proceed to scoring until the user acknowledges the data quality caveat.

### 2. Revenue and AOV by channel

```
FROM sales
SHOW orders, total_sales, average_order_value
GROUP BY order_referrer_source
ORDER BY total_sales DESC LIMIT 15
SINCE -30d UNTIL today
```

**Validation:** If `order_referrer_source` returns fewer channels than Step 1's `referrer_source`, note the schema mismatch — some sessions may not have converted and attribution columns may differ.

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

**Validation:** If `order_referrer_name` is blank or `(not set)` for most rows, UTM tagging on ads is missing — flag this as a P0 recommendation.

### 4. Trend per channel (find rising vs declining)

```
FROM sessions
SHOW sessions
GROUP BY referrer_source
TIMESERIES day SINCE -60d UNTIL today
```

Identify channels that are collapsing or surging week-over-week.

**Validation:** If the timeseries returns sparse or irregular data for recent days, check whether the store's analytics pipeline has a lag (Shopify can have up to 48h delay on session data).

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

**Revenue per 1k sessions** normalizes for volume so you can compare a small high-quality channel against a large low-quality one.

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
| Direct > 50% of revenue | Untracked traffic (ads losing UTMs, dark social, branded search) | Audit UTM tagging; treat direct as partial proxy for paid+brand |
| High sessions, low conv | Wrong audience or weak landing page | Run `page-critical-review` on those landing pages |
| Low sessions, high AOV | Underinvested winner | Increase spend or investment in that channel |
| Email conv rate < 5% | Klaviyo flows weak / list cold | Audit flows with `klaviyo-flow-build` |
| Search organic flat/declining | SEO regression or de-indexing | Check sitemap and indexed pages |

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
- Data may lag up to 48h; rerun queries if recent days look sparse
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

- **Attribution model** — Shopify = last-non-direct touch; complement with ad-platform attribution for paid channels, which are routinely under-credited.
- **Date window** — Use 30d for tactical decisions, 90d for strategic mix; below 1k sessions/month, use 90d minimum.
- **UTM hygiene** — Messy or missing UTM tags corrupt channel buckets; recommend a UTM audit as a P0 action when data is unclear.
