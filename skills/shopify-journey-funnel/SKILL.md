---
name: shopify-journey-funnel
description: Use this skill when the user wants a conversion funnel snapshot of their Shopify store — phrases like "funnel analysis", "where are people dropping off", "checkout drop-off", "review my conversion funnel", "why isn't my store converting", "funnel report". Pulls session-to-order stage data via ShopifyQL, identifies the biggest leak, segments by device/geo, and outputs a prioritized fix list.
---

# Shopify journey funnel

End-to-end snapshot of how visitors move through the store: **sessions → cart additions → checkout reached → checkout completed → order**. Finds the biggest drop-off and recommends concrete fixes.

## When to use

- Weekly / monthly funnel review
- Conversion rate dropped suddenly ("what broke?")
- Before scaling paid traffic — diagnose leaks first
- Pre-launch check after any storefront change (theme, checkout, product changes)

## Prerequisites

- Shopify MCP connected (`mcp__9bf46487-...__run-analytics-query`)
- Store has at least 7 days of sessions data (otherwise samples too small)
- Optionally: target conversion rate from the user (defaults below)

## Steps

### 1. Pull the headline funnel (last 30d)

```
FROM sessions
SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout, conversion_rate
TIMESERIES day SINCE -30d UNTIL today
```

Also pull a single aggregate row (no TIMESERIES) for clean stage-to-stage rates:

```
FROM sessions
SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout, conversion_rate
SINCE -30d UNTIL today
```

### 2. Period-over-period comparison

```
FROM sessions
SHOW sessions, sessions_that_completed_checkout, conversion_rate
TIMESERIES day SINCE -30d UNTIL today
COMPARE TO previous_period
```

Flag any stage where the WoW change is > ±20%.

### 3. Segment the funnel by device

```
FROM sessions
SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout, conversion_rate
GROUP BY session_device_type
SINCE -30d UNTIL today
```

Mobile conversion typically lags desktop by 30-50%. If mobile is > 60% behind desktop, that's a mobile-UX bug.

### 4. Segment by geography (top 10 countries)

```
FROM sessions
SHOW sessions, sessions_that_completed_checkout, conversion_rate
GROUP BY session_country
ORDER BY sessions DESC LIMIT 10
SINCE -30d UNTIL today
```

Look for big-traffic / zero-conversion countries — usually a payments or shipping issue (e.g., country not enabled in Shopify Payments).

### 5. Compute stage-to-stage rates

| Stage | Volume | Rate from prior step | Industry healthy |
|---|---|---|---|
| Sessions | S | — | — |
| Cart additions | C | C/S | 8-12% |
| Reached checkout | R | R/C | 40-55% |
| Completed checkout | O | O/R | 65-80% |
| Overall conv rate | O/S | — | 1.5-3% (D2C) |

Use these benchmarks as defaults if the user hasn't given targets. Adjust by category — subscription D2C tends higher (3-5%), considered purchases lower (0.5-1.5%).

### 6. Identify the biggest leak

For each transition, compute `(prior_step_volume − this_step_volume) × revenue_per_completed_checkout`. The largest absolute lost-revenue number is the leak to fix first.

### 7. Map leak to likely cause

| Leak | Likely cause | Where to investigate |
|---|---|---|
| Sessions → cart < 5% | PDP weak (price, photos, copy) or wrong-traffic | Run `page-critical-review` on top PDPs; check `shopify-journey-acquisition` for bad sources |
| Cart → checkout < 35% | Sticker-shock at cart (shipping, taxes) or weak cart UX | Cart drawer audit; surface shipping cost earlier |
| Checkout → order < 60% | Payment / shipping config; account-required friction; coupon-bar abandonment | Test checkout end-to-end on mobile; check enabled payment methods; check geo-block patterns |
| Mobile conv rate < 50% of desktop | Mobile UX bug | Mobile-only audit; check tap targets, font size, load time |

### 8. Output

```markdown
# Funnel · <Brand> · <date range>

## TL;DR
<2-3 sentences: overall conv rate X%, biggest leak is at <stage> losing ~$Y/month, root cause hypothesis is Z.>

## Funnel snapshot (last 30d)

| Stage | Visitors | % of prior | vs. healthy |
|---|---|---|---|
| Sessions | X | 100% | — |
| Cart additions | X | X% | <verdict> |
| Reached checkout | X | X% | <verdict> |
| Completed checkout | X | X% | <verdict> |
| **Overall conv rate** | **X%** | — | <verdict> |

## Period-over-period
<WoW deltas, flag anything > ±20%>

## By device
| Device | Sessions | Conv rate |
|---|---|---|
| Desktop | X | X% |
| Mobile | X | X% |
| Tablet | X | X% |

## By geography
<top 10 countries, sessions, conv rate, flag zero-conversion at high traffic>

## Biggest leak
**<stage>** — losing ~<count> visitors / ~$<revenue> per month

Hypothesis: <cause>

## Recommendations (prioritized)

### P0 — Fix this week
1. <Action> — <expected impact>

### P1 — Test next
1. <Action> — <expected impact>

### P2 — Polish
1. <Action> — <expected impact>

## Open questions
<Things to investigate / get from user>
```

### 9. Save the report

Write to `<repo>/journey-reports/funnel-<YYYY-MM-DD>.md` so the user can compare across periods.

## Cross-skill links

- `shopify-journey-acquisition` — if the leak is sessions→cart, traffic quality may be the cause
- `shopify-journey-product-path` — if certain PDPs convert worse than others
- `shopify-journey-cohort-retention` — to check if returning visitors convert differently
- `page-critical-review` — for PDP / landing-page UX teardown
- `klaviyo-flow-build` — for cart-abandonment / checkout-abandonment flow setup

## Tradeoffs

- **30-day window is the default** — long enough for stable signal, short enough to catch recent regressions. For very low-traffic stores (< 1k sessions/mo), expand to 60-90d.
- **Don't over-react to one-day spikes** — Always look at the trend, not the latest day. A weekend / holiday dip can look like a "leak" but isn't.
- **Shopify session attribution** — `sessions` counts unique browser sessions, not unique visitors. A user across desktop+mobile is two sessions. Don't confuse with Klaviyo / GA reports.

## Notes on ShopifyQL

- The `sessions` table stops being available on stores without Shopify's analytics enabled — verify with a small `FROM sessions SHOW sessions SINCE -1d` before deeper queries.
- `conversion_rate` is `sessions_that_completed_checkout / sessions`, not `orders / sessions`. Repeat purchases in one session won't double-count.
