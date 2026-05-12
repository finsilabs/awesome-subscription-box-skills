---
name: shopify-journey-cohort-retention
description: Use this skill when the user wants to analyze customer retention, repeat-purchase behavior, or LTV on their Shopify store — phrases like "cohort analysis", "repeat purchase rate", "customer LTV", "are customers coming back", "retention report", "time to second order". Pulls new vs returning customer data, builds an acquisition-month cohort table with repeat % at 30/60/90 days, and outputs LTV per cohort plus retention recommendations.
---

# Shopify journey cohort retention

Build the retention picture: how many first-time buyers come back, how fast, how much they spend, and which cohorts decay. The output drives both the email/SMS strategy (`klaviyo-flow-build`) and the unit economics for paid acquisition (`ads-performance-analysis`).

## When to use

- Quarterly retention review
- Before increasing paid spend (need LTV to justify CAC)
- After a flow / loyalty / subscription change — measure if it moved the needle
- "Why is revenue flat even though we're acquiring more customers?"
- Subscription / consumables brands (where retention IS the business)

## Prerequisites

- Shopify MCP connected (`mcp__9bf46487-...__run-analytics-query`, `list-customers`, `graphql_query`)
- Store has ≥ 60 days of order history (for any meaningful repeat signal)
- Ideally ≥ 6 months for cohort decay curves

## Steps

### 1. Headline new vs returning trend

```
FROM customers
SHOW new_customers, returning_customers
TIMESERIES day SINCE -90d UNTIL today
```

```
FROM sales
SHOW returning_customer_rate
TIMESERIES week SINCE -180d UNTIL today
```

Healthy returning_customer_rate by category (rough):

| Category | Returning customer rate (mature store) |
|---|---|
| Subscription / consumables | 40-60% |
| Apparel / home (replenishable) | 25-40% |
| Furniture / one-time / luxury | 5-15% |

### 2. Build the cohort table (last 6 acquisition months)

For each acquisition month, compute repeat % at 30 / 60 / 90 / 180 days. Use `list-customers` with date filters:

For each month M:
- Cohort size = customers with `created_at:>='M-01' AND created_at:<'M+1-01'`
- Repeat at 30d = of those, count where `orders_count:>1` AND second order within 30 days

Since `list-customers` doesn't expose second-order date directly, drop to GraphQL for accuracy:

```graphql
query CohortCustomers($query: String!, $cursor: String) {
  customers(first: 50, query: $query, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        id
        createdAt
        numberOfOrders
        amountSpent { amount currencyCode }
        orders(first: 5, sortKey: CREATED_AT) {
          edges { node { id createdAt totalPriceSet { shopMoney { amount } } } }
        }
      }
    }
  }
}
```

Then in code/spreadsheet:
- Group by acquisition month (`createdAt`)
- For each customer, compute days between order[0] and order[1]
- Repeat-by-30d = `count(days_to_2nd <= 30) / cohort_size`

### 3. Time-to-second-order distribution

From the GraphQL pull above, distribute `days_to_2nd_order` into buckets:

| Bucket | % of repeaters |
|---|---|
| 0-7 days | … |
| 8-30 days | … |
| 31-60 days | … |
| 61-90 days | … |
| 91-180 days | … |
| > 180 days | … |

The **median time to second order** is the most important number for sequencing your post-purchase email flow — your "we'd love you back" email should fire at ~70% of median.

### 4. LTV by cohort

For each acquisition cohort:
- Average orders per customer (cumulative at 30/60/90/180/365 days)
- Average revenue per customer (cumulative at the same checkpoints)

```
FROM sales
SHOW gross_sales / customers
GROUP BY cohort_acquisition_month
```

If ShopifyQL `cohort_acquisition_month` isn't exposed in your store version, derive from the GraphQL pull.

Output table:

| Acquisition month | Cohort size | LTV @ 30d | LTV @ 90d | LTV @ 180d | LTV @ 365d |
|---|---|---|---|---|---|

### 5. Repeat behavior by acquisition channel

Cross with `shopify-journey-acquisition`: are customers from one channel repeating better than another? Common pattern:

| Channel | Repeat % | Note |
|---|---|---|
| Direct / email | usually highest | warm, brand-aware |
| Search organic | high | intent-driven |
| Paid social | often lowest | discount-shopper acquisition |
| Referral | high | trust-driven |

Use this to refine paid-channel CAC targets — e.g., if Meta-acquired customers have 50% lower LTV, your max-CAC for Meta should be ~50% of your blended target.

### 6. Identify lapsed customers (for activation)

```
list-customers query: orders_count:>=1 AND last_order_date:<'<today minus 1.5x median repeat cycle>'
```

Translate to a date string and pass via the `query` field. This is the "win-back" pool — pipe to `shopify-journey-segments` for action.

### 7. Output

```markdown
# Cohort retention · <Brand> · <date range>

## TL;DR
<2-3 sentences: repeat rate is X%, median time to 2nd order Y days, top cohort LTV at 180d $Z, biggest opportunity is W>

## Headline
| Metric | Value | Healthy band | Verdict |
|---|---|---|---|
| Returning customer rate (last 30d) | X% | <band> | <verdict> |
| Repeat purchase rate (cumulative) | X% | <band> | <verdict> |
| Median time to 2nd order | X days | — | — |
| Avg orders per customer | X | — | — |
| Avg LTV (90d) | $X | — | — |

## Cohort table

| Acq. month | Cohort size | Repeat % @ 30d | @ 90d | @ 180d |
|---|---|---|---|---|
| … |

## LTV by cohort

| Acq. month | LTV @ 30d | @ 90d | @ 180d | @ 365d |
|---|---|---|---|---|
| … |

## Time-to-2nd-order distribution
<bucket table>

## Repeat by acquisition channel
| Channel | Acquired | Repeat % | LTV @ 90d |
|---|---|---|---|
| … |

## Lapsed-customer pool
<X customers haven't ordered in > <threshold>; ~$Y potential revenue if N% reactivate>

## Recommendations (prioritized)

### P0
1. <Action> — <expected impact>

### P1
1. <Action> — <expected impact>

### P2
1. <Action> — <expected impact>
```

### 8. Save

Write to `<repo>/journey-reports/cohort-retention-<YYYY-MM-DD>.md`.

## Cross-skill links

- `shopify-journey-segments` — turn the lapsed pool into named segments for activation
- `shopify-journey-acquisition` — cross channel × LTV
- `shopify-journey-product-path` — what products drive the second purchase
- `klaviyo-flow-build` — sequence post-purchase / win-back flows aligned to median repeat cycle
- `klaviyo-calendar-plan` — schedule activation campaigns to hit the lapsed pool
- `ads-performance-analysis` — recalibrate CAC targets using channel-specific LTV

## Tradeoffs

- **Cohorts need maturity** — Don't analyze a cohort before its 90-day window is complete. A 30-day-old cohort can look great because most repeats happen later.
- **GraphQL pulls are slow on large stores** — For stores with > 50k customers, use a sampled cohort (e.g., 500 random customers per acquisition month) and report sampling caveat.
- **Subscription stores are different** — Recurring orders inflate repeat counts artificially. Filter to exclude subscription-renewal orders (e.g., by `tag:subscription` or `source_name`) for true "voluntary repeat" measurement.
- **Promo cohorts decay fast** — Customers acquired during a heavy discount promo (BFCM, launch sale) almost always repeat at half the rate of full-price cohorts. Tag and exclude when comparing baseline retention.

## Quick benchmarks

| Metric | Weak | OK | Strong |
|---|---|---|---|
| 30-day repeat rate (D2C avg) | < 8% | 10-18% | > 22% |
| 90-day repeat rate | < 15% | 20-30% | > 35% |
| LTV / CAC | < 1.5 | 2-3 | > 3.5 |
| Avg orders per customer (year 1) | < 1.3 | 1.5-2.0 | > 2.5 |
