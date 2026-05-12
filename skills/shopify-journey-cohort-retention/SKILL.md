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

### 3. Validate data completeness before proceeding

Before computing rates or LTV, run these checks and surface any failures in the final report:

**Pagination completeness** — Verify `pageInfo.hasNextPage` is false before moving on for every GraphQL page fetch. If a cohort fetch is interrupted, log the cohort as `INCOMPLETE` and exclude it from trend comparisons.

**Minimum cohort size** — Only compute repeat % and LTV for cohorts with ≥ 30 customers. For smaller cohorts, report raw counts only and flag with a `*low-n*` warning.

**Data-quality sanity checks**
- Confirm `orders_count` on at least a sample of pulled customers matches their `orders` edge count.
- Check that no cohort month's order total is implausibly low (e.g., < 10% of adjacent months) — could indicate a data gap.
- Verify that the most recent incomplete cohort is excluded from decay-curve comparisons.

**Insufficient history** — If the store has < 60 days of orders, stop and report: 